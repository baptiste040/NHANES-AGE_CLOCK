"""Piste « suivi », Q4 : agregation en une note globale (protocole : DECISIONS.md).
Modele de reference : « sang seul contraint » (etape 1).

Options (toutes en annees d'ecart d'age) :
  global   : score global du modele (reference) ;
  moyenne  : moyenne des 5 ecarts de systeme ;
  cox      : moyenne ponderee des 5 ecarts, poids = coefficients d'un Cox age + sexe + 5 ecarts
             ajuste sur le developpement (poids normalises a une somme de 1) ;
  pire     : ecart du systeme prioritaire (centile standardise le plus eleve, comme en Q1) ;
  hybride  : moyenne + lambda x (pire - moyenne), lambda choisi par validation croisee a 5 plis
             sur le developpement (C du Cox age + sexe + agregat).
Chaque agregat entre dans un Cox age + sexe + agregat ajuste sur le developpement, qui donne le
risque a 10 ans (C, calibration, cas « un systeme tres defavorable »).
"""
from __future__ import annotations

import functools
import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

from . import retest as r
from .cohort import DURATION, EVENT
from .metrics import bootstrap, calibration, harrell_c, km_risk_at, summarize
from .suivi import OUT, SEED, N_BOOT, SYSTEMS, pairs_2001, pairs_nh3
from .suivi_contraint import M_C, ModelsC

PRED = OUT / "Q4_predictions.json"
RES = OUT / "Q4_resultats.json"
OPTIONS = ["global", "moyenne", "cox", "pire", "hybride"]
LAMBDAS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]
HORIZON = 120


def _cox(X: pd.DataFrame, t, e):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return CoxPHFitter().fit(X.assign(T=np.asarray(t), E=np.asarray(e)), "T", "E")


class Q4:
    def __init__(self):
        self.M = ModelsC()
        dev = self.M.dev
        self.base_dev = self.parts(dev)
        X = pd.DataFrame({s: self.base_dev[s] for s in SYSTEMS})
        X["age"], X["female"] = dev["age"].to_numpy(float), (dev["sex"] == 2).to_numpy(float)
        cph = _cox(X, dev[DURATION], dev[EVENT])
        b = cph.params_[SYSTEMS]
        self.cox_beta = b.to_dict()
        self.w = (b / b.sum()).to_dict()
        self.lam, self.lam_cv = self._cv_lambda(dev)
        self.surv = {o: self._fit_surv(o, dev) for o in OPTIONS}

    def parts(self, df):
        df = df.reset_index(drop=True)
        g = self.M.gaps(M_C, df)
        sg = self.M.std_gap(M_C, df, g)
        top = np.argmax(np.column_stack([sg[s] for s in SYSTEMS]), axis=1)
        G = np.column_stack([g[s] for s in SYSTEMS])
        out = {s: g[s] for s in SYSTEMS}
        out["global"] = g["global"]
        out["moyenne"] = G.mean(axis=1)
        out["pire"] = G[np.arange(len(df)), top]
        out["pire_systeme"] = np.array(SYSTEMS)[top]
        out["centiles"] = sg
        return out

    def agg(self, p, o, lam=None):
        if o in ("global", "moyenne", "pire"):
            return p[o]
        if o == "cox":
            return sum(self.w[s] * p[s] for s in SYSTEMS)
        lam = self.lam if lam is None else lam
        return p["moyenne"] + lam * (p["pire"] - p["moyenne"])

    def _cv_lambda(self, dev):
        rng = np.random.default_rng(SEED)
        fold = rng.integers(0, 5, len(dev))
        t, e = dev[DURATION].to_numpy(), dev[EVENT].to_numpy()
        age, fem = dev["age"].to_numpy(float), (dev["sex"] == 2).to_numpy(float)
        p = self.base_dev
        res = {}
        for lam in LAMBDAS:
            a = p["moyenne"] + lam * (p["pire"] - p["moyenne"])
            cs = []
            for k in range(5):
                tr, te = fold != k, fold == k
                X = pd.DataFrame({"agg": a, "age": age, "female": fem})
                c = _cox(X[tr], t[tr], e[tr])
                cs.append(harrell_c(t[te], e[te], c.predict_partial_hazard(X[te]).to_numpy()))
            res[lam] = float(np.mean(cs))
        best = max(res, key=res.get)
        return best, res

    def _fit_surv(self, o, dev):
        X = pd.DataFrame({"agg": self.agg(self.base_dev, o), "age": dev["age"].to_numpy(float),
                          "female": (dev["sex"] == 2).to_numpy(float)})
        return _cox(X, dev[DURATION], dev[EVENT])

    def risk(self, o, df, p):
        X = pd.DataFrame({"agg": self.agg(p, o), "age": df["age"].to_numpy(float),
                          "female": (df["sex"] == 2).to_numpy(float)})
        sf = self.surv[o].predict_survival_function(X, times=[HORIZON])
        return 1.0 - sf.to_numpy().ravel()


def _c_all(d):
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    out = {f"C_{o}": harrell_c(t, e, d[f"risk_{o}"]) for o in OPTIONS}
    for o in OPTIONS[1:]:
        out[f"dC_{o}_moins_global"] = out[f"C_{o}"] - out["C_global"]
    return out


def special_case(p):
    """Un systeme au-dessus de son 90e centile, tous les autres sous leur mediane."""
    C = np.column_stack([p["centiles"][s] for s in SYSTEMS])
    high, low = C > 0.9, C < 0.5
    return (high.sum(axis=1) == 1) & ((high | low).all(axis=1))


def evaluate(Q: Q4, df, n_boot=None):
    df = df.reset_index(drop=True)
    p = Q.parts(df)
    d = df[[DURATION, EVENT]].copy()
    for o in OPTIONS:
        d[f"risk_{o}"] = Q.risk(o, df, p)
    point = _c_all(d)
    out = {"point": point}
    if n_boot:
        reps = bootstrap(d, functools.partial(_c_all), n_boot, SEED)
        out["resume"] = summarize(point, reps).to_dict(orient="records")
    cal = {}
    for o in OPTIONS:
        _, c = calibration(d[DURATION], d[EVENT], d[f"risk_{o}"], HORIZON)
        cal[o] = {"obs_sur_predit": c["ratio_observe_predit"], "pente": c["pente_calibration"],
                  "pente_ic95": [c["pente_ic95_bas"], c["pente_ic95_haut"]]}
    out["calibration"] = cal
    sc = special_case(p)
    obs, lo, hi = km_risk_at(d[DURATION].to_numpy()[sc], d[EVENT].to_numpy()[sc], HORIZON)
    cas = {"n": int(sc.sum()), "deces": int(d[EVENT].to_numpy()[sc].sum()), "risque_observe_km": obs,
           "risque_observe_ic95": [lo, hi], "par_systeme": pd.Series(p["pire_systeme"][sc]).value_counts().to_dict()}
    for o in OPTIONS:
        pr = float(d[f"risk_{o}"].to_numpy()[sc].mean())
        cas[o] = {"risque_predit_moyen": pr, "obs_sur_predit": obs / pr, "ic95": [lo / pr, hi / pr],
                  "agregat_moyen": float(Q.agg(p, o)[sc].mean())}
    out["cas_un_systeme"] = cas
    return out


def reliability(Q: Q4, e1, e2):
    p1, p2 = Q.parts(e1), Q.parts(e2)
    out = {}
    for o in OPTIONS:
        a1, a2 = Q.agg(p1, o), Q.agg(p2, o)
        d = a2 - a1
        sd = float(np.std(Q.agg(Q.base_dev, o), ddof=1))
        out[o] = {"cci": float(r.icc_a1(a1, a2)), "p95_abs_d": float(np.percentile(np.abs(d), 95)),
                  "et_entre_personnes_dev": sd, "p95_sur_et": float(np.percentile(np.abs(d), 95)) / sd,
                  "pire_systeme_meme": float(np.mean(p1["pire_systeme"] == p2["pire_systeme"]))}
    return out


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _meta(Q):
    return {"poids_cox": Q.w, "coef_cox": Q.cox_beta, "lambda": Q.lam, "lambda_cv": Q.lam_cv}


def predictions() -> Path:
    Q = Q4()
    e1, e2 = pairs_2001(Q.M)
    res = {**_meta(Q), "developpement_apparent": evaluate(Q, Q.M.dev),
           "fiabilite_2001": reliability(Q, e1, e2), "sha256_code": _sha(Path(__file__))}
    PRED.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return PRED


def analyse() -> Path:
    from .cohort import build_cohort
    from .config import ROOT, load_panel, load_study
    from .nhanes import build_harmonized
    Q = Q4()
    study = load_study()
    h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    co, _ = build_cohort(h, load_panel("checkup_standard"), study)
    val = co[co["cycle"].isin(study["cycles"]["validation"])].reset_index(drop=True)
    e1, e2 = pairs_nh3(Q.M)
    res = {**_meta(Q), "validation": evaluate(Q, val, study["validation"]["bootstrap"]),
           "fiabilite_nh3": reliability(Q, e1, e2), "sha256_code": _sha(Path(__file__))}
    RES.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return RES


if __name__ == "__main__":
    import sys
    {"predictions": predictions, "analyse": analyse}[sys.argv[1]]()
