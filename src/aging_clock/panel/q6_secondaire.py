"""Programme « panel », Q6 : analyses secondaires NON pre-enregistrees (demandees apres validation de Q6).

1. Risque absolu : difference de risque de deces a 10 ans, a 45 ans et par sexe, entre le point de risque
   minimal et chaque seuil retenu (HR 1,2 et 1,5) ; proportion des 30-55 ans de NHANES au-dela du seuil.
2. Tenue des categories « intervalle trop large » apres ajustement sur tabac, IMC, diabete et revenu
   (sensibilite 3 de Q6).
"""
from __future__ import annotations

import ast
import json

import numpy as np
import pandas as pd

from . import q6_analyse as A
from . import q6_modele as M
from .remesures import OUT


def breslow_risk(X, t, e, b, X0, horizon=120.0):
    """Risque cumule a `horizon` pour les lignes de X0 (estimateur de Breslow du risque de base)."""
    lp = X @ b
    lp0 = lp.max()
    r = np.exp(lp - lp0)
    o = np.argsort(t)
    ts, es, rs = t[o], e[o].astype(bool), r[o]
    at_risk = np.cumsum(rs[::-1])[::-1]  # somme des r pour t_j >= t_i (ex aequo : premier de chaque groupe)
    first = np.searchsorted(ts, ts, side="left")
    denom = at_risk[first]
    keep = es & (ts <= horizon)
    H0 = float(np.sum(1.0 / denom[keep]))
    return 1 - np.exp(-H0 * np.exp(X0 @ b - lp0))


def absolute_risk(p):
    Z = pd.read_csv(OUT / "Q6_zones.csv").set_index("id")
    rows = []
    for mid, z in Z.iterrows():
        sides = [s for s in ("bas", "haut") if z[f"cote_{s}_retenu"] is True or z[f"cote_{s}_retenu"] == "True"]
        if not sides:
            continue
        q = p[p[mid].notna()]
        if mid in A.FAST:
            q = q[q.WTSAF2YR.notna() & (q.WTSAF2YR > 0)]
        dv = q[q.dev]
        spec = M.Spec(dv[mid].to_numpy(float), z.echelle == "log")
        akn = np.percentile(dv.age, M.KN)
        m, a, s, t, e = dv[mid].to_numpy(float), dv.age.to_numpy(float), dv.sex.to_numpy(), dv.t10.to_numpy(float), dv.e10.to_numpy().astype(bool)
        X = M.design(m, a, s, spec, akn)
        b, _, _ = M.cox_fit(X, t, e)
        young = q[q.age.between(30, 55)]
        wcol = "WTSAF2YR" if mid in A.FAST else "WTMEC2YR"
        for side in sides:
            for level, col in ((1.2, "seuil12"), (1.5, "seuil15")):
                thr = z[f"{col}_{side}"]
                if not np.isfinite(thr):
                    continue
                out = (young[mid] < thr) if side == "bas" else (young[mid] > thr)
                w = young[wcol].fillna(0).to_numpy(float)
                row = {"id": mid, "cote": side, "niveau_hr": level, "seuil": float(thr), "xmin": float(z.xmin),
                       "seuil_retenu": (z[f"seuil_{side}_retenu"] in (True, "True")) if level == 1.2 else None,
                       "part_30_55_ponderee": float(np.sum(w * out) / np.sum(w)) if np.sum(w) > 0 else np.nan,
                       "part_30_55_non_ponderee": float(out.mean()), "n_30_55": int(len(young))}
                for sx, lab in ((1, "H"), (2, "F")):
                    X0 = M.design(np.array([z.xmin, thr]), np.array([45.0, 45.0]), np.array([sx, sx]), spec, akn)
                    r0, r1 = breslow_risk(X, t, e, b, X0)
                    row |= {f"risque_10a_min_{lab}": float(r0), f"risque_10a_seuil_{lab}": float(r1),
                            f"difference_points_{lab}": float(100 * (r1 - r0))}
                rows.append(row)
    return pd.DataFrame(rows)


def adjustment_hold():
    """Pour chaque comparaison « intervalle trop large », le seuil HR 1,2 de la sensibilite 3 reste-t-il du cote
    normal de la borne D1 ?"""
    C = pd.read_csv(OUT / "Q6_categories.csv")
    S = pd.read_csv(OUT / "Q6_sensibilites.csv")
    s3 = S[S.sensibilite.str.startswith("3")].set_index("id")
    rows = []
    for _, c in C[C.categorie == "intervalle trop large"].iterrows():
        thr3 = s3.loc[c.id, f"seuil12_{c.cote}"] if c.id in s3.index else np.nan
        if not np.isfinite(thr3):
            hold, why = False, "le côté de risque disparaît après ajustement"
        elif (c.cote == "haut" and thr3 < c.borne) or (c.cote == "bas" and thr3 > c.borne):
            hold, why = True, "le seuil reste du côté normal de la borne"
        else:
            hold, why = False, "le seuil passe au-delà de la borne"
        ci = ast.literal_eval(c.ic95) if isinstance(c.ic95, str) else None
        in_ci = bool(ci and np.isfinite(thr3) and ci[0] <= thr3 <= ci[1])
        rows.append({"id": c.id, "type": c.type, "sexe": c.sexe, "cote": c.cote, "borne": c.borne, "seuil_principal": c.seuil_1_2,
                     "ic95_principal": ci, "seuil_ajuste": thr3, "tient_apres_ajustement": hold, "seuil_ajuste_dans_ic": in_ci,
                     "motif": why})
    t = pd.DataFrame(rows)
    g = t.groupby(["id", "cote"]).agg(tient=("tient_apres_ajustement", "all"), tient_un_sexe=("tient_apres_ajustement", "any"),
                                      dans_ic=("seuil_ajuste_dans_ic", "all"), seuil_principal=("seuil_principal", "first"),
                                      seuil_ajuste=("seuil_ajuste", "first")).reset_index()
    g["classe"] = np.select(
        [g.tient & g.dans_ic, g.tient, g.tient_un_sexe],
        ["association indépendante : seuil inchangé après ajustement",
         "association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel",
         "mixte selon le sexe"],
        "marqueur de risque : l'association passe par le tabac, l'IMC, le diabète ou le revenu")
    return t, g


ALCOOL_MIN = ["ggt", "alt", "ast", "mcv", "tg_fast", "tg_serum", "hdl"]


def alcohol(p: pd.DataFrame) -> pd.DataFrame:
    """Consommation d'alcool (questionnaire ALQ, 20 ans et plus) : verres par semaine, en classes.
    jamais ou pas dans l'annee / < 7 / 7-14 / > 14 verres par semaine / inconnu."""
    from .q2 import SUF, _xpt
    F = []
    for y in sorted(p.cycle.unique()):
        x = _xpt("ALQ" + SUF[int(y)], int(y))
        ever12 = next(c for c in ("ALQ100", "ALD100", "ALQ101") if c in x)
        freq = x.ALQ120Q.where(x.ALQ120Q < 777)
        per_week = freq * x.ALQ120U.map({1: 1.0, 2: 12 / 52.0, 3: 1 / 52.0})
        dpd = x.ALQ130.where(x.ALQ130 < 77)
        dw = (per_week * dpd).where(freq > 0, 0.0)
        never = (x[ever12] == 2) & (x.ALQ110 == 2)
        dw = dw.where(~never, 0.0)
        F.append(pd.DataFrame({"verres_semaine": dw}, index=x.index))
    a = pd.concat(F).reindex(p.index)
    v = a.verres_semaine
    cls = np.select([v == 0, v < 7, v <= 14, v > 14], ["aucun", "<7", "7-14", ">14"], "inconnu")
    return pd.DataFrame({"alc_lt7": (cls == "<7").astype(float), "alc_7_14": (cls == "7-14").astype(float),
                         "alc_gt14": (cls == ">14").astype(float), "alc_inconnu": (cls == "inconnu").astype(float),
                         "alc_classe": cls}, index=p.index)


def alcohol_adjustment(p: pd.DataFrame):
    """Seuils HR 1,2 apres ajustement sur tabac, IMC, diabete, revenu ET alcool (developpement), compares a
    l'analyse principale et a la sensibilite 3."""
    p = p.join(alcohol(p))
    Z = pd.read_csv(OUT / "Q6_zones.csv").set_index("id")
    G = pd.read_csv(OUT / "Q6_secondaire_ajustement_par_cote.csv")
    ids = list(dict.fromkeys(ALCOOL_MIN + G.id.tolist()))
    rows = []
    for mid in ids:
        z = Z.loc[mid]
        q = p[p[mid].notna()]
        if mid in A.FAST:
            q = q[q.WTSAF2YR.notna() & (q.WTSAF2YR > 0)]
        dv = q[q.dev]
        spec = M.Spec(dv[mid].to_numpy(float), z.echelle == "log")
        akn = np.percentile(dv.age, M.KN)
        bkn = np.percentile(dv.bmi, M.KN)
        base = dv[["smk_ancien", "smk_actuel", "smk_inconnu", "diab", "pir", "pir_na", "bmi_na"]].to_numpy(float)
        ex = np.column_stack([base, M.age_basis(dv.bmi.to_numpy(float), bkn),
                              dv[["alc_lt7", "alc_7_14", "alc_gt14", "alc_inconnu"]].to_numpy(float)])
        r = M.fit(dv[mid].to_numpy(float), dv.age.to_numpy(float), dv.sex.to_numpy(), dv.t10.to_numpy(float),
                  dv.e10.to_numpy().astype(bool), spec, akn, extra=ex, keep_curve=False)
        for side in ("bas", "haut"):
            ci = _lit(z[f"ic95_seuil12_{side}"])
            thr = r["seuil_1_2"][side]
            rows.append({"id": mid, "cote": side, "cote_retenu": z[f"cote_{side}_retenu"] in (True, "True"),
                         "seuil_principal": z[f"seuil12_{side}"], "seuil_tabac_imc_diabete_revenu_alcool": thr,
                         "dans_ic_principal": bool(ci and thr is not None and ci[0] <= thr <= ci[1]),
                         "forme_ajustee": r["forme"], "p_global_ajuste": r["p_global"], "deces": r["deces"],
                         "part_alcool_inconnu": float(dv.alc_inconnu.mean()), "part_plus_14_verres": float(dv.alc_gt14.mean())})
    return pd.DataFrame(rows)


def _lit(s):
    return ast.literal_eval(s) if isinstance(s, str) and s.startswith("[") else None


def run():
    p, _ = A.prepare()
    R = absolute_risk(p)
    R.to_csv(OUT / "Q6_secondaire_risque_absolu.csv", index=False)
    t, g = adjustment_hold()
    t.to_csv(OUT / "Q6_secondaire_ajustement.csv", index=False)
    g.to_csv(OUT / "Q6_secondaire_ajustement_par_cote.csv", index=False)
    return R, t, g


if __name__ == "__main__":
    run()
