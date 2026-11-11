"""Programme « panel », Q4 : normalisation spontanee des valeurs anormales (protocole : DECISIONS.md).

Seuils : table D1 (reports/panel/D1_*.csv), type R (fonde sur le risque) ou S (convention
statistique). Paires : celles de Q1 (2001-2002 et NHANES III, separement).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from .remesures import OUT, add_derived, pairs_2001, pairs_nh3

PRED = OUT / "Q4_predictions_2001.json"
MIN_N = 20


def _wilson(k, n, z=1.96):
    if n == 0:
        return [np.nan, np.nan]
    p = k / n
    d = 1 + z ** 2 / n
    c = (p + z ** 2 / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / d
    return [float(c - h), float(c + h)]


def thresholds():
    """Liste de regles : (id, type, variante, fonction (df) -> (bas, haut) par personne)."""
    st = pd.read_csv(OUT / "D1_intervalles_statistiques.csv")
    cl = pd.read_csv(OUT / "D1_seuils_cliniques.csv")
    rules = []
    for mid, g in st.groupby("id"):
        def f(df, g=g):
            lo = np.full(len(df), np.nan)
            hi = np.full(len(df), np.nan)
            for _, r in g.iterrows():
                m = ((df.sex.to_numpy() == (1 if r.sexe == "H" else 2)) & (df.age.to_numpy() >= r.age_min)
                     & (df.age.to_numpy() <= r.age_max))
                lo[m], hi[m] = r.borne_basse, r.borne_haute
            return lo, hi
        rules.append((mid, "S", "principal", f))
    for _, r in cl.iterrows():
        var = r.variante if isinstance(r.variante, str) else "principal"

        def f(df, r=r):
            n = len(df)
            return (np.full(n, r.seuil), np.full(n, np.nan)) if r.sens == "bas" else (np.full(n, np.nan), np.full(n, r.seuil))
        rules.append((r.id, "R", var, f))
    return rules


def _abn(x, lo, hi, rid):
    """Anormal bas / haut. Seuils R : haut si x >= seuil ; bas si x < seuil. S : hors [lo, hi]."""
    low = np.where(np.isfinite(lo), x < lo, False)
    high = np.where(np.isfinite(hi), (x >= hi) if rid == "R" else (x > hi), False)
    return low, high


def _prep(e1, e2):
    e1, e2 = add_derived(e1), add_derived(e2)
    for e in (e1, e2):
        if "u_alb" in e and "u_creat" in e:
            e["acr"] = e.u_alb / e.u_creat * 100          # ug/mL / mg/dL -> mg/g
    return e1, e2


def _cd(jeu):
    v = pd.read_csv(OUT / "Q1_variabilite_remesures.csv")
    v = v[(v.groupe == "20-79 ans") & (v.jeu == jeu)].set_index("id")
    return v


def metrics(e1, e2, jeu):
    cdv = _cd(jeu)
    rows = []
    for mid, typ, var, f in thresholds():
        if mid not in e1 or e1[mid].isna().all():
            continue
        ok = e1[mid].notna() & e2[mid].notna()
        a, b = e1[ok].reset_index(drop=True), e2[ok].reset_index(drop=True)
        lo, hi = f(a)
        has = np.isfinite(lo) | np.isfinite(hi)
        a, b, lo, hi = a[has].reset_index(drop=True), b[has].reset_index(drop=True), lo[has], hi[has]
        x1, x2 = a[mid].to_numpy(float), b[mid].to_numpy(float)
        l1, h1 = _abn(x1, lo, hi, typ)
        l2, h2 = _abn(x2, lo, hi, typ)
        abn1, abn2 = l1 | h1, l2 | h2
        # modele binormal (echelle log si possible)
        logs = (x1 > 0).all() and (x2 > 0).all()
        t1, t2 = (np.log(x1), np.log(x2)) if logs else (x1, x2)
        tlo, thi = (np.log(np.where(lo > 0, lo, np.nan)), np.log(np.where(hi > 0, hi, np.nan))) if logs else (lo, hi)
        sw2 = np.var(t2 - t1, ddof=1) / 2
        st2 = np.var(np.concatenate([t1, t2]), ddof=1)
        rho = max(0.0, 1 - sw2 / st2)
        mu = np.mean(np.concatenate([t1, t2]))
        cm, cs = mu + rho * (t1 - mu), np.sqrt(st2 * (1 - rho ** 2))
        p_norm = (np.where(np.isfinite(thi), norm.cdf((thi - cm) / cs), 1.0) - np.where(np.isfinite(tlo), norm.cdf((tlo - cm) / cs), 0.0))
        # anomalies limites : a moins d'un changement detectable empirique (2 semaines) du seuil
        c = cdv.loc[mid] if mid in cdv.index else None
        if c is not None and pd.notna(c.get("cd_emp_hausse")):
            qh, ql = np.log(1 + c.cd_emp_hausse / 100), -np.log(1 - c.cd_emp_baisse / 100)
            lim_h = h1 & (np.log(x1) - np.log(hi) < qh)
            lim_l = l1 & (np.log(lo) - np.log(x1) < ql)
        elif c is not None and pd.notna(c.get("cd_emp_unites")):
            lim_h = h1 & (x1 - hi < c.cd_emp_unites)
            lim_l = l1 & (lo - x1 < c.cd_emp_unites)
        else:
            lim_h = lim_l = np.zeros(len(x1), bool)
        lim = lim_h | lim_l
        for side, m in [("bas", l1), ("haut", h1), ("tous", abn1)]:
            k = int((m & ~abn2).sum())
            n = int(m.sum())
            r = {"jeu": jeu, "id": mid, "type": typ, "variante": var, "cote": side, "n_paires": len(x1), "n_anormaux_1": n,
                 "taux_normalisation": k / n if n else np.nan, "ic95": _wilson(k, n),
                 "attendu_bruit": float(p_norm[m].mean()) if n else np.nan}
            if side == "tous":
                for lab, mm in [("limites", m & lim), ("nettes", m & ~lim)]:
                    kk, nn = int((mm & ~abn2).sum()), int(mm.sum())
                    r[f"n_{lab}"] = nn
                    r[f"taux_{lab}"] = kk / nn if nn else np.nan
                nn = int((~abn1).sum())
                r["taux_apparition"] = float((~abn1 & abn2).sum() / nn) if nn else np.nan
                r["part_anormaux_1"] = float(abn1.mean())
            rows.append(r)
    return pd.DataFrame(rows)


def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def predictions() -> Path:
    e1, e2 = _prep(*pairs_2001())
    t = metrics(e1, e2, "2001_2002")
    t.to_csv(OUT / "Q4_normalisation_2001.csv", index=False)
    PRED.write_text(json.dumps({"sha256_D1_stat": _sha(OUT / "D1_intervalles_statistiques.csv"),
                                "sha256_D1_clin": _sha(OUT / "D1_seuils_cliniques.csv"),
                                "sha256_csv_2001": _sha(OUT / "Q4_normalisation_2001.csv")}, indent=1), encoding="utf-8")
    return OUT / "Q4_normalisation_2001.csv"


def analyse() -> Path:
    meta = json.loads(PRED.read_text(encoding="utf-8"))
    for k, f in [("sha256_D1_stat", "D1_intervalles_statistiques.csv"), ("sha256_D1_clin", "D1_seuils_cliniques.csv")]:
        if _sha(OUT / f) != meta[k]:
            raise RuntimeError(f"{f} modifie depuis le pre-enregistrement")
    e1, e2 = _prep(*pairs_nh3())
    t3 = metrics(e1, e2, "nhanes3")
    t3.to_csv(OUT / "Q4_normalisation_nhanes3.csv", index=False)
    t1 = pd.read_csv(OUT / "Q4_normalisation_2001.csv")
    key = ["id", "type", "variante", "cote"]
    m = t1[t1.cote == "tous"].merge(t3[t3.cote == "tous"], on=key, how="outer", suffixes=("_2001", "_nh3"))
    rows = []
    for _, r in m.iterrows():
        n1, n3 = r.get("n_anormaux_1_2001", 0) or 0, r.get("n_anormaux_1_nh3", 0) or 0
        ok1, ok3 = n1 >= MIN_N, n3 >= MIN_N
        rates = [x for x, ok in [(r.get("taux_normalisation_2001"), ok1), (r.get("taux_normalisation_nh3"), ok3)] if ok]
        if not rates:
            concl, statut = "pas de conclusion (moins de 20 anomalies)", ""
        else:
            statut = "deux jeux" if len(rates) == 2 else "un seul jeu"
            mn = min(rates)
            concl = ("anomalie isolée peu informative" if mn >= 0.5 else
                     "confirmer avant de signaler" if mn >= 0.3 else "normalisation < 30 %")
        ic = r.get("ic95_nh3")
        ic = json.loads(ic) if isinstance(ic, str) else ic
        comp = (ic[0] <= r.taux_normalisation_2001 <= ic[1]) if (ok1 and ok3 and isinstance(ic, (list, tuple))) else None
        rows.append({**{k: r[k] for k in key}, "n_2001": n1, "taux_2001": r.get("taux_normalisation_2001"),
                     "n_nh3": n3, "taux_nh3": r.get("taux_normalisation_nh3"), "ic95_nh3": ic,
                     "attendu_bruit_nh3": r.get("attendu_bruit_nh3"), "compatible": comp,
                     "conclusion": concl, "statut": statut})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "Q4_synthese.csv", index=False)
    return OUT / "Q4_synthese.csv"
