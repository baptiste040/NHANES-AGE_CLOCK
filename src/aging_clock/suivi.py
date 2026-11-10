"""Piste « suivi », questions 1 et 2 (protocole : DECISIONS.md, pre-enregistrement Q1-Q2).

Q1 : changement significatif et stabilite des moteurs (systeme prioritaire, 3 marqueurs).
Q2 : regression vers la moyenne quand on ne remesure que les marqueurs anormaux ; correction
     par retrecissement (CCI de 2001-2002, moyenne du meme sexe et de la meme tranche d'age).

Modele principal : « sang seul » (19 marqueurs) ; secondaire : modele complet, partie
biologique (mesures physiques figees, jamais candidates comme moteurs).
Calage et predictions : 2001-2002. Test : NHANES III.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import retest as r
from . import retest_nh3 as t3
from .cohort import apply_panel_ranges, build_cohort
from .config import ROOT, load_panel, load_study
from .nhanes import build_harmonized
from .uncertainty import BLOOD_URINE
from .validate import fit_clock

OUT = ROOT / "reports" / "checkup_standard" / "suivi"
PRED = OUT / "Q1_Q2_predictions.json"
SEED, N_BOOT = 2026, 2000
SYSTEMS = ["cardiovasculaire", "metabolique", "renal", "hepatique", "inflammatoire_hematologique"]
SCORES = ["global"] + SYSTEMS
PHYSICAL = ["sbp", "dbp", "heart_rate", "bmi", "waist"]

# Moteurs actionnables : marqueur -> sens actionnable (table pre-enregistree, DECISIONS.md)
ACTIONABLE = {"glucose": "haut", "hba1c": "haut", "tg": "haut", "total_chol": "haut", "hdl": "bas",
              "crp": "haut", "alt": "haut", "ast": "haut", "ggt": "haut", "wbc": "haut",
              "mcv": "haut", "acr": "haut"}

# Seuils « anormal » (pre-enregistres) : (bas, haut) ; (H, F) quand ils dependent du sexe
THRESHOLDS = {
    "glucose": (None, 5.6), "hba1c": (None, 5.7), "total_chol": (None, 5.2),
    "hdl": ((1.0, 1.3), None), "tg": (None, 1.7), "alt": (None, 40), "ast": (None, 40),
    "ggt": (None, (60, 40)), "alp": (None, 120), "albumin": (35, None),
    "creatinine": (None, (106, 89)), "acr": (None, 3.0), "crp": (None, 3.0),
    "wbc": (4.0, 10.0), "lymph_pct": (20, 40), "rdw": (None, 14.5), "mcv": (80, 100),
    "hb": ((13.0, 12.0), None), "platelets": (150, 400),
}


# ------------------------------------------------------------------ modeles et references
class Models:
    """Modele sang seul (principal) et complet (secondaire), references du developpement."""

    def __init__(self):
        study = load_study()
        h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                             cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
        co, _ = build_cohort(h, load_panel("checkup_standard"), study)
        dev = co[co["cycle"].isin(study["cycles"]["development"])].reset_index(drop=True)
        self.dev = dev
        self.clocks = {"sang": fit_clock(dev, load_panel("checkup_sang_seul"), study, 0.0),
                       "complet": fit_clock(dev, load_panel("checkup_standard"), study, 0.0)}
        self.vars = {"sang": load_panel("checkup_sang_seul").model_variables,
                     "complet": load_panel("checkup_standard").model_variables}
        dev = dev.assign(band=self.band(dev["age"]))
        allv = sorted(set(self.vars["complet"]))
        self.ref = dev.groupby(["sex", "band"])[allv].median()                 # valeurs de reference
        self.logmean = dev.groupby(["sex", "band"])[[v for v in allv if v in BLOOD_URINE]].agg(
            lambda x: np.log(x[x > 0]).mean())                                    # pour le retrecissement
        self.dev_gaps = {m: self.gaps(m, dev) for m in self.clocks}               # pour les centiles

    @staticmethod
    def band(age):
        return (np.clip(np.asarray(age, float), 20, 79) // 10 * 10).astype(int)

    def gaps(self, m, df):
        p = self.clocks[m].predict(df)
        return {s: p[f"gap_{s}"].to_numpy() for s in SCORES}

    def std_gap(self, m, df, gaps):
        """Centile de l'ecart de chaque systeme parmi les personnes du developpement de meme sexe
        et de meme tranche d'age de 10 ans (0 = le plus favorable, 1 = le plus defavorable)."""
        dev = self.dev
        dband, band = self.band(dev["age"]), self.band(df["age"])
        out = {}
        for s in SYSTEMS:
            ref = self.dev_gaps[m][s]
            res = np.empty(len(df))
            for sex in (1, 2):
                for b in np.unique(band):
                    msk = (df["sex"].to_numpy() == sex) & (band == b)
                    if not msk.any():
                        continue
                    pool = np.sort(ref[(dev["sex"].to_numpy() == sex) & (dband == b)])
                    res[msk] = np.searchsorted(pool, gaps[s][msk], side="right") / len(pool)
            out[s] = res
        return out

    def reference_values(self, df):
        idx = pd.MultiIndex.from_arrays([df["sex"].to_numpy(), self.band(df["age"])])
        return self.ref.reindex(idx).reset_index(drop=True)

    def contributions(self, m, df, candidates):
        """Contribution (annees d'ecart global) de chaque marqueur candidat : ecart global
        observe - ecart global quand le marqueur est remplace par sa valeur de reference."""
        df = df.reset_index(drop=True)
        base = self.gaps(m, df)["global"]
        refv = self.reference_values(df)
        out = {}
        for v in candidates:
            x = df.copy()
            x[v] = refv[v].to_numpy()
            out[v] = base - self.gaps(m, x)["global"]
        return pd.DataFrame(out), refv


def drivers(contrib: pd.DataFrame, values: pd.DataFrame, refv: pd.DataFrame, actionable: bool):
    """Jusqu'a 3 moteurs : contributions positives les plus fortes (actionnables : seulement les
    marqueurs de la table, du cote actionnable de la reference). Liste vide possible."""
    c = contrib.copy()
    if actionable:
        for v in c.columns:
            if v not in ACTIONABLE:
                c[v] = np.nan
            else:
                side = values[v].to_numpy() > refv[v].to_numpy() if ACTIONABLE[v] == "haut" \
                    else values[v].to_numpy() < refv[v].to_numpy()
                c.loc[~side, v] = np.nan
    res = []
    for _, row in c.iterrows():
        pos = row[row > 0].sort_values(ascending=False)
        res.append(list(pos.index[:3]))
    return res


def _jacc(a, b):
    if not a and not b:
        return 1.0
    return len(set(a) & set(b)) / len(set(a) | set(b))


# ------------------------------------------------------------------ donnees appariees
def pairs_2001(M: Models):
    from .retest_explore import _paired
    e1, e2, _, _ = _paired()
    return e1.reset_index(drop=True), e2.reset_index(drop=True)


def pairs_nh3(M: Models):
    """NHANES III : sang et urine du second examen ; mesures physiques figees (partie biologique)."""
    panel = load_panel("checkup_standard")
    d, _ = t3.population()
    V = M.vars["complet"]
    blood = [v for v in V if v in BLOOD_URINE]
    s2 = t3.harmonize(t3.second_exam(d["SEQN"].to_numpy()))
    s2r, _ = apply_panel_ranges(s2, panel)
    ok = s2r[blood].notna().all(axis=1).to_numpy()
    e1 = d.loc[ok, ["SEQN", "age", "sex"] + V].reset_index(drop=True)
    e2 = e1.copy()
    e2[blood] = s2r.loc[ok, blood].to_numpy()
    return e1, e2


# ------------------------------------------------------------------ Q1
def q1_metrics(M: Models, m: str, e1, e2):
    cand = [v for v in M.vars[m] if v not in PHYSICAL]
    g1, g2 = M.gaps(m, e1), M.gaps(m, e2)
    s1, s2 = M.std_gap(m, e1, g1), M.std_gap(m, e2, g2)
    top1 = np.array(SYSTEMS)[np.argmax(np.column_stack([s1[s] for s in SYSTEMS]), axis=1)]
    top2 = np.array(SYSTEMS)[np.argmax(np.column_stack([s2[s] for s in SYSTEMS]), axis=1)]
    c1, ref1 = M.contributions(m, e1, cand)
    c2, ref2 = M.contributions(m, e2, cand)
    per = pd.DataFrame({"systeme_meme": top1 == top2, "systeme_1": top1})
    for lab, act in [("tous", False), ("actionnables", True)]:
        d1 = drivers(c1, e1.reset_index(drop=True), ref1, act)
        d2 = drivers(c2, e2.reset_index(drop=True), ref2, act)
        per[f"n_moteurs_{lab}_1"] = [len(a) for a in d1]
        per[f"premier_meme_{lab}"] = [(a[:1] == b[:1]) for a, b in zip(d1, d2)]
        per[f"trio_identique_{lab}"] = [set(a) == set(b) for a, b in zip(d1, d2)]
        per[f"trio_jaccard_05_{lab}"] = [_jacc(a, b) >= 0.5 for a, b in zip(d1, d2)]
    per["tertile_ecart_global_1"] = pd.qcut(g1["global"], 3, labels=["T1", "T2", "T3"]).astype(str)
    thr = {}
    for s in SCORES:
        d = g2[s] - g1[s]
        rng = np.random.default_rng(SEED)
        bt = [np.percentile(np.abs(d[rng.integers(0, len(d), len(d))]), 95) for _ in range(N_BOOT)]
        thr[s] = {"p95_abs_d": float(np.percentile(np.abs(d), 95)),
                  "p95_ic95": [float(np.quantile(bt, .025)), float(np.quantile(bt, .975))],
                  "gaussien": float(1.96 * np.std(d, ddof=1)), "p50_abs_d": float(np.median(np.abs(d)))}
    return per, thr, g1, g2


RATES = ["systeme_meme", "premier_meme_tous", "trio_identique_tous", "trio_jaccard_05_tous",
         "premier_meme_actionnables", "trio_identique_actionnables", "trio_jaccard_05_actionnables"]


def rates_with_ci(per: pd.DataFrame, seed=SEED, n_boot=N_BOOT):
    rng = np.random.default_rng(seed)
    X = per[RATES].to_numpy(float)
    boots = np.array([X[rng.integers(0, len(X), len(X))].mean(axis=0) for _ in range(n_boot)])
    return {k: {"taux": float(X[:, i].mean()), "ic95": [float(np.quantile(boots[:, i], .025)),
                                                         float(np.quantile(boots[:, i], .975))]}
            for i, k in enumerate(RATES)}


# ------------------------------------------------------------------ Q2
def abnormal(df: pd.DataFrame, which: str = "clinique", M: Models | None = None) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    sex = df["sex"].to_numpy()
    for v, (lo, hi) in THRESHOLDS.items():
        x = df[v].to_numpy(float)
        if which == "centiles":
            q = M.dev.groupby("sex")[v].quantile([.1, .9]).unstack()
            lo_v = np.where(sex == 1, q.loc[1, .1], q.loc[2, .1]) if lo is not None else None
            hi_v = np.where(sex == 1, q.loc[1, .9], q.loc[2, .9]) if hi is not None else None
        else:
            sexed = lambda t: np.where(sex == 1, t[0], t[1]) if isinstance(t, tuple) else t  # noqa: E731
            lo_v = sexed(lo) if lo is not None else None
            hi_v = sexed(hi) if hi is not None else None
        a = np.zeros(len(df), bool)
        if lo_v is not None:
            a |= x < lo_v
        if hi_v is not None:
            a |= x > hi_v if v not in ("glucose", "hba1c", "total_chol", "tg", "acr") else x >= hi_v
        out[v] = a
    return out


def iccs_2001(e1, e2):
    """CCI(A,1) du log de chaque marqueur sanguin ou urinaire en 2001-2002."""
    return {v: r.icc_a1(np.log(e1[v].to_numpy(float)), np.log(e2[v].to_numpy(float)))
            for v in THRESHOLDS}


def shrink(M: Models, e1, rho: dict, markers, target: str = "developpement"):
    """Valeur attendue au second bilan sans changement reel : exp(mu + rho (ln x1 - mu))."""
    x = e1.reset_index(drop=True).copy()
    if target == "developpement":
        idx = pd.MultiIndex.from_arrays([x["sex"].to_numpy(), M.band(x["age"])])
        mu = M.logmean.reindex(idx).reset_index(drop=True)
    else:                                                         # moyenne interne de l'echantillon
        tmp = x.assign(band=M.band(x["age"]))
        lm = tmp.groupby(["sex", "band"])[list(THRESHOLDS)].agg(lambda s: np.log(s[s > 0]).mean())
        mu = lm.reindex(pd.MultiIndex.from_arrays([x["sex"].to_numpy(), M.band(x["age"])])).reset_index(drop=True)
    for v in markers:
        lx = np.log(x[v].to_numpy(float))
        x[v] = np.exp(mu[v].to_numpy() + rho[v] * (lx - mu[v].to_numpy()))
    return x


def score_shrink(M: Models, m: str, df, g1, rho_score):
    """Retrecissement au niveau du score : mu + rho_score (ecart_1 - mu), mu = ecart moyen du
    developpement, meme sexe et meme tranche d'age (variante ajoutee au calage, DECISIONS.md)."""
    dev = M.dev
    key = pd.MultiIndex.from_arrays([dev["sex"].to_numpy(), M.band(dev["age"])])
    idx = pd.MultiIndex.from_arrays([df["sex"].to_numpy(), M.band(df["age"])])
    out = {}
    for s in SCORES:
        mu = pd.Series(M.dev_gaps[m][s], index=key).groupby(level=[0, 1]).mean().reindex(idx).to_numpy()
        out[s] = mu + rho_score[s] * (g1[s] - mu)
    return out


def q2_metrics(M: Models, m: str, e1, e2, rho, which="clinique", target="developpement", rho_score=None):
    e1, e2 = e1.reset_index(drop=True), e2.reset_index(drop=True)
    ab = abnormal(e1, which, M)
    rows_m = []
    for v in THRESHOLDS:
        a = ab[v].to_numpy()
        if a.sum() < 5:
            rows_m.append({"marqueur": v, "n_anormaux_1": int(a.sum())})
            continue
        still = abnormal(e2, which, M)[v].to_numpy()[a]
        dl = np.log(e2[v].to_numpy(float)[a]) - np.log(e1[v].to_numpy(float)[a])
        rows_m.append({"marqueur": v, "n_anormaux_1": int(a.sum()),
                       "normalises_2": float(1 - still.mean()), "variation_log_moy": float(dl.mean())})
    sysvars = {s: [v for v in M.vars[m] if v in THRESHOLDS and load_panel("checkup_standard").variables[v].system == s]
               for s in SYSTEMS}
    sel = e1.copy()                                               # remesure selective
    for v in THRESHOLDS:
        a = ab[v].to_numpy()
        sel.loc[a, v] = e2.loc[a, v]
    g1, gfull, gsel = M.gaps(m, e1), M.gaps(m, e2), M.gaps(m, sel)
    exp_full = M.gaps(m, shrink(M, e1, rho, list(THRESHOLDS), target))
    sh_sel = e1.copy()
    shr = shrink(M, e1, rho, list(THRESHOLDS), target)
    for v in THRESHOLDS:
        a = ab[v].to_numpy()
        sh_sel.loc[a, v] = shr.loc[a, v]
    exp_sel = M.gaps(m, sh_sel)
    exp_score = score_shrink(M, m, e1, g1, rho_score) if rho_score else None
    top20 = g1["global"] >= np.quantile(g1["global"], .8)
    per = {}
    for s in SCORES:
        grp = ab[[v for v in (THRESHOLDS if s == "global" else sysvars[s])]].any(axis=1).to_numpy() \
            if (s == "global" or sysvars[s]) else np.zeros(len(e1), bool)
        per[s] = {"anormal": grp,
                  "d_complet": gfull[s] - g1[s], "d_selectif": gsel[s] - g1[s],
                  "corr_complet": gfull[s] - exp_full[s], "corr_selectif": gsel[s] - exp_sel[s],
                  "corr_score_complet": gfull[s] - exp_score[s] if exp_score else np.full(len(e1), np.nan)}
    per["selection_score"] = {"anormal": top20, "d_complet": gfull["global"] - g1["global"],
                              "d_selectif": gfull["global"] - g1["global"],
                              "corr_complet": gfull["global"] - exp_full["global"],
                              "corr_selectif": gfull["global"] - exp_full["global"],
                              "corr_score_complet": gfull["global"] - exp_score["global"] if exp_score else np.full(len(e1), np.nan)}
    return pd.DataFrame(rows_m), per


def mean_ci(x, seed=SEED, n_boot=N_BOOT):
    x = np.asarray(x, float)
    if len(x) < 5:
        return {"n": int(len(x))}
    rng = np.random.default_rng(seed)
    b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(n_boot)]
    return {"n": int(len(x)), "moyenne": float(x.mean()),
            "ic95": [float(np.quantile(b, .025)), float(np.quantile(b, .975))]}


def summarise_q2(per):
    out = {}
    for s, d in per.items():
        a = d["anormal"]
        out[s] = {k: mean_ci(d[k][a]) for k in ["d_complet", "d_selectif", "corr_complet", "corr_selectif",
                                                 "corr_score_complet"]}
    return out


# ------------------------------------------------------------------ etapes
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def predictions() -> Path:
    """Calage sur 2001-2002 : seuils, taux de stabilite, CCI, amelioration apparente."""
    OUT.mkdir(parents=True, exist_ok=True)
    M = Models()
    e1, e2 = pairs_2001(M)
    rho = iccs_2001(e1, e2)
    res = {"n": len(e1), "cci_log_2001": rho, "modeles": {}}
    for m in ["sang", "complet"]:
        per, thr, g1, g2 = q1_metrics(M, m, e1, e2)
        rho_s = {s: r.icc_a1(g1[s], g2[s]) for s in SCORES}
        mk, q2 = q2_metrics(M, m, e1, e2, rho, rho_score=rho_s)
        mk.to_csv(OUT / f"Q2_marqueurs_2001_{m}.csv", index=False)
        per.to_csv(OUT / f"Q1_paires_2001_{m}.csv", index=False)
        res["modeles"][m] = {"seuils": thr, "stabilite": rates_with_ci(per),
                             "n_moteurs_tous": per["n_moteurs_tous_1"].value_counts().sort_index().to_dict(),
                             "n_moteurs_actionnables": per["n_moteurs_actionnables_1"].value_counts().sort_index().to_dict(),
                             "q2": summarise_q2(q2), "cci_score_2001": rho_s}
    res["sha256_code"] = _sha(Path(__file__))
    PRED.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return PRED


def analyse() -> Path:
    """Test sur NHANES III (apres commit du pre-enregistrement)."""
    pred = json.loads(PRED.read_text(encoding="utf-8"))
    M = Models()
    e1, e2 = pairs_nh3(M)
    rho = {k: float(v) for k, v in pred["cci_log_2001"].items()}
    res = {"n": len(e1), "modeles": {}}
    for m in ["sang", "complet"]:
        per, thr, _, _ = q1_metrics(M, m, e1, e2)
        per.to_csv(OUT / f"Q1_paires_nh3_{m}.csv", index=False)
        strat = {f"{c}={lvl}": rates_with_ci(per[per[c] == lvl])
                 for c in ["tertile_ecart_global_1"] for lvl in sorted(per[c].unique())}
        rho_s = {k: float(v) for k, v in pred["modeles"][m]["cci_score_2001"].items()}
        mk, q2 = q2_metrics(M, m, e1, e2, rho, rho_score=rho_s)
        mk.to_csv(OUT / f"Q2_marqueurs_nh3_{m}.csv", index=False)
        mk_c, q2c = q2_metrics(M, m, e1, e2, rho, which="centiles", rho_score=rho_s)
        _, q2i = q2_metrics(M, m, e1, e2, rho, target="interne", rho_score=rho_s)
        res["modeles"][m] = {"seuils": thr, "stabilite": rates_with_ci(per), "stabilite_par_tertile": strat,
                             "n_moteurs_tous": per["n_moteurs_tous_1"].value_counts().sort_index().to_dict(),
                             "n_moteurs_actionnables": per["n_moteurs_actionnables_1"].value_counts().sort_index().to_dict(),
                             "q2": summarise_q2(q2), "q2_seuils_centiles": summarise_q2(q2c),
                             "q2_moyenne_interne": summarise_q2(q2i)}
        mk_c.to_csv(OUT / f"Q2_marqueurs_nh3_centiles_{m}.csv", index=False)
    res["sha256_code"] = _sha(Path(__file__))
    out = OUT / "Q1_Q2_nhanes3.json"
    out.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return out
