"""ANALYSE EXPLORATOIRE (non pre-enregistree) sur les remesures NHANES 2001-2002.

Pourquoi la simulation ne retrouve-t-elle pas le bruit observe des scores, meme quand les CV des
marqueurs sont justes ? Deux hypotheses (DECISIONS.md, 2026-11-10) :
  a. les variations intra-individuelles des marqueurs sont correlees (dilution, posture...) ;
  b. quelques valeurs extremes (CRP tres elevee, infection) gonflent les CV classiques.
Les correlations et les CV sont estimes sur les memes donnees que celles qu'on cherche a
expliquer : resultats descriptifs, a confirmer sur NHANES III.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import retest as r
from .cohort import apply_panel_ranges
from .config import ROOT, load_panel, load_study
from .nhanes import read_xpt

EXTRA_PROTEIN = ("L40_B", "LBXSTP", "L40_2_B", "LB2STP")     # proteines totales (g/dL), hors modele


def _paired() -> tuple[pd.DataFrame, pd.DataFrame, list, r.Scorer]:
    """Memes personnes et memes valeurs que l'analyse principale (n = 387)."""
    panel = load_panel("checkup_standard")
    co, _ = r.population()
    sc = r.Scorer()
    V = list(sc.model["variables"])
    blood = [v for v in V if v in r.BLOOD_URINE]
    s2 = r.load_second_exam()
    s2r, _ = apply_panel_ranges(s2, panel)
    s2r = s2r.dropna(subset=blood)
    co = co[co["SEQN"].astype(int).isin(s2r.index)].reset_index(drop=True)
    e1 = co[["SEQN", "age", "sex"] + V].copy()
    e2 = e1.copy()
    e2[blood] = s2r.loc[e1["SEQN"].astype(int), blood].to_numpy()
    # Proteines totales (non utilisees par le modele), pour l'hypothese de dilution
    p1 = read_xpt(r._raw(EXTRA_PROTEIN[0])).set_index("SEQN")[EXTRA_PROTEIN[1]]
    p2 = read_xpt(r._raw(EXTRA_PROTEIN[2])).set_index("SEQN")[EXTRA_PROTEIN[3]]
    seqn = e1["SEQN"].astype(int).to_numpy()
    e1["protein"] = p1.reindex(seqn).to_numpy() * 10
    e2["protein"] = p2.reindex(seqn).to_numpy() * 10
    return e1, e2, blood, sc


def _robust_cv(dlog: np.ndarray) -> float:
    s = 1.4826 * np.median(np.abs(dlog - np.median(dlog))) / np.sqrt(2)
    return float(100 * np.sqrt(np.exp(s ** 2) - 1))


def simulate_corr(df, scorer, cvs, corr: pd.DataFrame | None, n_draws=r.N_DRAWS, seed=r.SEED, chunk=100):
    """Comme retest.simulate, avec un bruit log-normal correle entre marqueurs (matrice `corr`)."""
    variables = list(cvs)
    sig = np.array([np.sqrt(np.log1p(cvs[v] ** 2)) for v in variables])
    R = np.eye(len(variables))
    if corr is not None:
        idx = [i for i, v in enumerate(variables) if v in corr.index]
        names = [variables[i] for i in idx]
        R[np.ix_(idx, idx)] = corr.loc[names, names].to_numpy()
        w, U = np.linalg.eigh(R)                      # projection sur les matrices definies positives
        R = U @ np.diag(np.clip(w, 1e-6, None)) @ U.T
        d = np.sqrt(np.diag(R))
        R = R / np.outer(d, d)
    L = np.linalg.cholesky(R)
    base = df.reset_index(drop=True)
    seeds = np.random.SeedSequence(seed).spawn((len(base) + chunk - 1) // chunk)
    out = None
    for c, start in enumerate(range(0, len(base), chunk)):
        block = base.iloc[start:start + chunk]
        rng = np.random.default_rng(seeds[c])
        rep = block.loc[block.index.repeat(n_draws)].reset_index(drop=True)
        z = rng.standard_normal((len(rep), len(variables))) @ L.T
        rep[variables] = rep[variables].to_numpy(float) * np.exp(z * sig)
        g = scorer(rep)
        if out is None:
            out = {n: np.empty((len(base), n_draws)) for n in g}
        for n in g:
            out[n][start:start + len(block)] = g[n].reshape(len(block), n_draws)
    return out


def run() -> dict:
    study = load_study()
    out = ROOT / study["paths"]["reports"] / "checkup_standard" / "fiabilite_reelle" / "exploratoire"
    out.mkdir(parents=True, exist_ok=True)
    cfg = r.load_cv()
    e1, e2, blood, sc = _paired()
    V = list(sc.model["variables"])
    markers = blood + ["protein"]
    dlog = pd.DataFrame({v: np.log(e2[v].to_numpy(float)) - np.log(e1[v].to_numpy(float)) for v in markers})

    # a. correlations des variations intra-individuelles
    pear = dlog.corr(method="pearson")
    spear = dlog.corr(method="spearman")
    pear.round(3).to_csv(out / "correlation_variations_pearson.csv")
    spear.round(3).to_csv(out / "correlation_variations_spearman.csv")
    pairs = (spear.where(np.triu(np.ones(spear.shape, bool), 1)).stack()
             .rename("spearman").reset_index().rename(columns={"level_0": "a", "level_1": "b"}))
    pairs["abs"] = pairs["spearman"].abs()
    pairs.sort_values("abs", ascending=False).drop(columns="abs").to_csv(out / "paires_correlees.csv", index=False)

    g1, g2 = sc(e1), sc(e2)
    x = e1[["age", "sex"] + V]
    obs = {n: r.observed_metrics(g1[n], g2[n])["et_intra"] for n in g1}
    corr_model = spear.loc[blood, blood]
    rows = []
    for label, scen, corr in [("principal (EFLM), independant", "principal", None),
                              ("principal (EFLM), bruit correle", "principal", corr_model),
                              ("secondaire (Lacher), independant", "secondaire", None),
                              ("secondaire (Lacher), bruit correle", "secondaire", corr_model)]:
        cvs = r.cv_scenario(cfg, scen, False)
        p = r.predicted_metrics(simulate_corr(x, sc, cvs, corr), g1).set_index("score")
        for n in g1:
            rows.append({"simulation": label, "score": n, "et_intra_pred": p.loc[n, "et_intra"],
                         "et_intra_obs": obs[n], "ratio_obs_pred": obs[n] / p.loc[n, "et_intra"]})
    # Simulation « ideale » : CV observes de chaque marqueur + correlation observee
    cv_obs = {v: float(np.sqrt(np.exp((dlog[v].std(ddof=1) / np.sqrt(2)) ** 2) - 1)) for v in blood}
    cvs_obs = {**r.cv_scenario(cfg, "principal", False), **cv_obs}
    for label, corr in [("CV observes, independant", None), ("CV observes, bruit correle", corr_model)]:
        p = r.predicted_metrics(simulate_corr(x, sc, cvs_obs, corr), g1).set_index("score")
        for n in g1:
            rows.append({"simulation": label, "score": n, "et_intra_pred": p.loc[n, "et_intra"],
                         "et_intra_obs": obs[n], "ratio_obs_pred": obs[n] / p.loc[n, "et_intra"]})
    sim = pd.DataFrame(rows)
    sim.to_csv(out / "simulation_bruit_correle.csv", index=False)

    # b. valeurs extremes : CV classiques contre robustes ; influence des personnes extremes
    mk = []
    for v in markers:
        d = dlog[v].dropna().to_numpy()
        classic = float(100 * np.sqrt(np.exp((d.std(ddof=1) / np.sqrt(2)) ** 2) - 1))
        q = np.quantile(np.abs(d), .975)
        trimmed = d[np.abs(d) <= q]
        mk.append({"variable": v, "cv_classique": classic, "cv_robuste_mad": _robust_cv(d),
                   "cv_sans_2_5pct_extremes": float(100 * np.sqrt(np.exp((trimmed.std(ddof=1) / np.sqrt(2)) ** 2) - 1)),
                   "cv_pred_principal": 100 * r.cv_scenario(cfg, "principal")[v] if v in blood else np.nan,
                   "cv_pred_secondaire": 100 * r.cv_scenario(cfg, "secondaire")[v] if v in blood else np.nan})
    pd.DataFrame(mk).to_csv(out / "cv_robustes.csv", index=False)

    crp_hi = ((e1["crp"] > 10) | (e2["crp"] > 10)).to_numpy()
    infl = []
    for n in g1:
        d = g2[n] - g1[n]
        share = np.sort(d ** 2)[::-1]
        infl.append({"score": n, "et_intra_tous": obs[n],
                     "et_intra_sans_crp_sup_10": r.observed_metrics(g1[n][~crp_hi], g2[n][~crp_hi])["et_intra"],
                     "et_intra_robuste_mad": float(1.4826 * np.median(np.abs(d - np.median(d))) / np.sqrt(2)),
                     "part_variance_5_personnes": float(share[:5].sum() / share.sum()),
                     "part_variance_1pct": float(share[:max(1, len(d) // 100)].sum() / share.sum())})
    pd.DataFrame(infl).to_csv(out / "influence_extremes.csv", index=False)
    meta = {"n": len(e1), "crp_sup_10_a_un_examen": int(crp_hi.sum()),
            "statut": "exploratoire, non pre-enregistre"}
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"dossier": out, **meta}
