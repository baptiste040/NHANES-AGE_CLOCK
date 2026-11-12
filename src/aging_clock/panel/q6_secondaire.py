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
