"""Programme « panel », Q2 : analyses secondaires NON pre-enregistrees (demandees par l'auteur du
projet apres les resultats).

1. Jeune chez une meme personne, modele par morceaux (0-4 h, 4-8 h, >= 8 h ; noeuds a 4 et 8 h),
   compare au modele lineaire pre-enregistre. Effet rapporte : 2 h contre 10 h.
2. Comparaison a la declaration EAS/EFLM (Nordestgaard 2016) : changements moyens maximaux 1-6 h
   apres un repas habituel, convertis en % de la mediane a jeun de NHANES III.
3. Effet sur la classification : part des personnes a jeun (>= 8 h, NHANES III) qui passeraient
   au-dessus d'un seuil si leur prelevement etait non a jeun, selon la fourchette d'effets.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .q2 import _pct, _y, nh3
from .remesures import OUT

SEED = 2026
KEY = ["tg_fast", "tg_serum", "glu_fast", "glu_serum", "insulin", "homa_ir", "quicki", "tyg", "tc", "hdl", "ldl", "ldl_f"]
# Nordestgaard 2016 (Eur Heart J, doi:10.1093/eurheartj/ehw152), resume : changements maximaux moyens
# 1-6 h apres un repas habituel, mg/dL
NORDESTGAARD = {"tg_fast": 26.0, "tc": -8.0, "ldl_f": -8.0, "hdl": 0.0}


def _phi(F):
    F = np.minimum(F, 24)
    return np.column_stack([np.minimum(F, 4), np.clip(F - 4, 0, 4), np.maximum(F - 8, 0)])


def piecewise(e1, e2, B=2000) -> pd.DataFrame:
    rows = []
    lin = pd.read_csv(OUT / "Q2_A_intra.csv").set_index("id")
    for mid in KEY:
        if mid not in e1:
            continue
        ok = e1[mid].notna() & e2[mid].notna() & e1.fast_h.notna() & e2.fast_h.notna()
        if mid not in ("tyg",):
            ok &= (e1[mid] > 0) & (e2[mid] > 0)
        x1, sc = _y(e1[mid][ok], mid)
        x2, _ = _y(e2[mid][ok], mid)
        d = x2 - x1
        dphi = _phi(e2.fast_h[ok].to_numpy()) - _phi(e1.fast_h[ok].to_numpy())
        X = np.column_stack([np.ones(len(d)), dphi])
        cvec = _phi(np.array([2.0]))[0] - _phi(np.array([10.0]))[0]

        def eff(i):
            b = np.linalg.lstsq(X[i], d[i], rcond=None)[0]
            return float(b[1:] @ cvec)
        est = eff(np.arange(len(d)))
        rng = np.random.default_rng(SEED)
        bs = [eff(rng.integers(0, len(d), len(d))) for _ in range(B)]
        l = lin.loc[mid] if mid in lin.index else None
        rows.append({"id": mid, "n": int(len(d)), "echelle": sc, "par_morceaux_2h_10h": _pct(est, sc),
                     "ic95": [_pct(np.quantile(bs, .025), sc), _pct(np.quantile(bs, .975), sc)],
                     "lineaire_preenregistre": l.jeune_A if l is not None else np.nan,
                     "classes": l.jeune_A_classes if l is not None else np.nan,
                     "direct": l.jeune_direct if l is not None else np.nan})
    return pd.DataFrame(rows)


def literature(e1) -> pd.DataFrame:
    fast = e1[e1.fast_h >= 8]
    rows = []
    for mid, delta in NORDESTGAARD.items():
        med = float(fast[mid].median())
        rows.append({"id": mid, "changement_mg_dL": delta, "mediane_a_jeun_nh3": med, "changement_pct": 100 * delta / med})
    return pd.DataFrame(rows)


def classification(e1, effects: pd.DataFrame) -> pd.DataFrame:
    """Part des personnes a jeun (>= 8 h) au-dessus du seuil, avant et apres application d'un effet
    multiplicatif du jeune (scenarios : meme personne lineaire, par morceaux, classes ; entre
    personnes NHANES III)."""
    fast = e1[(e1.fast_h >= 8)]
    homa75 = float(np.nanpercentile(fast.homa_ir, 75))
    rules = [("glu_fast", 110.0, "glycémie ≥ 6,1 mmol/L (OMS)"), ("glu_fast", 100.0, "glycémie ≥ 5,6 mmol/L (ADA)"),
             ("tg_fast", 150.0, "TG ≥ 1,7 mmol/L (ESC/EAS, à jeun)"),
             ("homa_ir", homa75, f"HOMA-IR ≥ {homa75:.2f} (75ᵉ centile à jeun de NHANES III, valeur illustrative : aucun seuil lu)")]
    b3 = pd.read_csv(OUT / "Q2_B_nhanes3.csv").set_index("id")
    rows = []
    for mid, thr, lab in rules:
        x = fast[mid].dropna().to_numpy(float)
        before = float((x >= thr).mean())
        e = effects.set_index("id").loc[mid]
        scen = {"même personne, linéaire (pré-enregistré)": e.lineaire_preenregistre,
                "même personne, par morceaux": e.par_morceaux_2h_10h,
                "même personne, classes": e.classes,
                "entre personnes (NHANES III)": b3.loc[mid, "jeune_B3"]}
        for s, pct in scen.items():
            after = float((x * (1 + pct / 100) >= thr).mean())
            rows.append({"seuil": lab, "n_a_jeun": len(x), "scenario": s, "effet_pct": pct,
                         "part_au_dessus_a_jeun": before, "part_au_dessus_non_a_jeun": after,
                         "basculent_points": 100 * (after - before)})
    return pd.DataFrame(rows)


def run():
    e1, e2 = nh3()
    p = piecewise(e1, e2)
    p.to_csv(OUT / "Q2_secondaire_par_morceaux.csv", index=False)
    lit = literature(e1)
    lit.to_csv(OUT / "Q2_secondaire_litterature.csv", index=False)
    c = classification(e1, p)
    c.to_csv(OUT / "Q2_secondaire_classification.csv", index=False)
    return p, lit, c
