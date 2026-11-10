"""Piste « suivi », Q3 allegee : l'ACR (urines) est presente au premier bilan et absente au second
(protocole : DECISIONS.md). Modele de reference : « sang seul contraint » (etape 1).

Strategies pour le second bilan (sans urines) :
  1. imputation : ACR predite a partir des 18 autres marqueurs, de l'age et du sexe (regression
     lineaire du log de l'ACR, ajustee sur le developpement) ;
  2. marqueurs communs : ACR mise a la valeur de reference (mediane du developpement, meme sexe,
     meme tranche d'age de 10 ans) aux deux bilans ;
  3. modele dedie : Cox « sang seul, sans urines » (meme pipeline, ACR hors modele), contraint,
     applique aux deux bilans.
Sensibilite (non prevue au plan) : report de l'ACR du premier bilan.

Faux changement = (ecart_2 - ecart_1) avec la strategie, moins (ecart_2 - ecart_1) avec le panel
complet aux deux bilans : la part du changement due a la seule absence des urines.
"""
from __future__ import annotations

import functools
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .cohort import DURATION, EVENT
from .config import load_panel
from .contrainte import ConstrainedClock
from .metrics import bootstrap, harrell_c, summarize
from .suivi import OUT as SOUT
from .suivi import SEED, N_BOOT, pairs_2001, pairs_nh3
from .suivi_contraint import ModelsC
from .validate import fit_clock

OUT = SOUT
PRED = OUT / "Q3_predictions.json"
RES = OUT / "Q3_nhanes3.json"
SC = ["global", "renal"]
STRATS = ["complet", "imputation", "communs", "dedie", "report"]


class Q3Models(ModelsC):
    def __init__(self):
        super().__init__()
        from .config import load_study
        study = load_study()
        self.ded = ConstrainedClock(fit_clock(self.dev, load_panel("checkup_sang_sans_urines"), study, 0.0))
        self._fit_imputation()

    def _feat(self, df):
        panel = load_panel("checkup_sang_seul")
        X = {}
        for v in self.vars["sang"]:
            if v == "acr":
                continue
            x = df[v].to_numpy(float)
            X[v] = np.log(np.maximum(x, 1e-3)) if panel.variables[v].log else x
        X["age"], X["female"] = df["age"].to_numpy(float), (df["sex"].to_numpy() == 2).astype(float)
        X = pd.DataFrame(X)
        X.insert(0, "const", 1.0)
        return X

    def _fit_imputation(self):
        X = self._feat(self.dev).to_numpy()
        y = np.log(np.maximum(self.dev["acr"].to_numpy(float), 0.1))
        self.beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ self.beta
        self.imp_r2 = float(1 - res.var() / y.var())

    def impute_acr(self, df):
        return np.maximum(np.exp(self._feat(df).to_numpy() @ self.beta), 0.1)

    def ref_acr(self, df):
        return self.reference_values(df.reset_index(drop=True))["acr"].to_numpy()

    def gap(self, df, strat, bilan, other=None):
        """Ecarts (global, renal) d'un bilan selon la strategie. bilan 1 : urines presentes ;
        bilan 2 : urines absentes. `other` : premier bilan (pour le report)."""
        d = df.reset_index(drop=True).copy()
        if strat == "dedie":
            p = self.ded.predict(d)
        else:
            if strat == "communs":
                d["acr"] = self.ref_acr(d)
            elif bilan == 2 and strat == "imputation":
                d["acr"] = self.impute_acr(d)
            elif bilan == 2 and strat == "report":
                d["acr"] = other.reset_index(drop=True)["acr"].to_numpy()
            p = self.clocks["sang_contraint"].predict(d)
        return {s: p[f"gap_{s}"].to_numpy() for s in SC}


def _p95_ci(x, seed=SEED, n_boot=N_BOOT):
    x = np.abs(np.asarray(x, float))
    rng = np.random.default_rng(seed)
    b = [np.percentile(x[rng.integers(0, len(x), len(x))], 95) for _ in range(n_boot)]
    return float(np.percentile(x, 95)), [float(np.quantile(b, .025)), float(np.quantile(b, .975))]


def _mean_ci(x, seed=SEED, n_boot=N_BOOT):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(n_boot)]
    return float(x.mean()), [float(np.quantile(b, .025)), float(np.quantile(b, .975))]


def pair_metrics(M: Q3Models, e1, e2):
    e1, e2 = e1.reset_index(drop=True), e2.reset_index(drop=True)
    g = {}
    for st in STRATS:
        g1 = M.gap(e1, "complet" if st in ("imputation", "report") else st, 1)
        g2 = M.gap(e2, st, 2 if st != "complet" else 1, other=e1)
        g[st] = (g1, g2)
    full_d = {s: g["complet"][1][s] - g["complet"][0][s] for s in SC}
    out = {}
    for st in STRATS:
        out[st] = {}
        for s in SC:
            d = g[st][1][s] - g[st][0][s]
            fc = d - full_d[s]
            p95, p95ci = _p95_ci(d)
            m, mci = _mean_ci(d)
            fm, fmci = _mean_ci(fc)
            fp, fpci = _p95_ci(fc)
            out[st][s] = {"changement_moyen": m, "changement_moyen_ic95": mci, "p95_abs_d": p95,
                          "p95_ic95": p95ci, "ratio_p95_vs_complet": p95 / float(np.percentile(np.abs(full_d[s]), 95)),
                          "faux_changement_moyen": fm, "faux_changement_moyen_ic95": fmci,
                          "faux_changement_p95_abs": fp, "faux_changement_p95_ic95": fpci}
        if st in ("communs", "dedie"):
            gfull1 = g["complet"][0]
            # ecart d'affichage au bilan 1 quand on le recalcule sans urines
            out[st]["ecart_bilan1_vs_complet"] = {
                s: {"moyen": float(np.mean(g[st][0][s] - gfull1[s])),
                    "p95_abs": float(np.percentile(np.abs(g[st][0][s] - gfull1[s]), 95))} for s in SC}
            # comparaison mixte (bilan 1 complet affiche tel quel, bilan 2 avec la strategie)
            out[st]["comparaison_mixte"] = {}
            for s in SC:
                dm = g[st][1][s] - gfull1[s]
                m, mci = _mean_ci(dm)
                p95, p95ci = _p95_ci(dm)
                out[st]["comparaison_mixte"][s] = {"changement_moyen": m, "changement_moyen_ic95": mci,
                                                   "p95_abs_d": p95, "p95_ic95": p95ci}
    return out


def _c_paired(d):
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    out = {}
    for s in SC:
        cf = harrell_c(t, e, d[f"risk_complet_{s}"])
        for st in ["imputation", "communs", "dedie"]:
            c = harrell_c(t, e, d[f"risk_{st}_{s}"])
            out[f"C_{st}_{s}"], out[f"dC_{st}_{s}"] = c, c - cf
        out[f"C_complet_{s}"] = cf
    return out


def discrimination(M: Q3Models, df, n_boot=None):
    """C a un seul bilan (sans urines) : strategie contre panel complet, difference appariee."""
    df = df.reset_index(drop=True)
    d = df[[DURATION, EVENT]].copy()
    cc = M.clocks["sang_contraint"]
    variants = {"complet": df, "imputation": df.assign(acr=M.impute_acr(df)),
                "communs": df.assign(acr=M.ref_acr(df))}
    for st, x in variants.items():
        p = cc.predict(x)
        for s in SC:
            d[f"risk_{st}_{s}"] = p[f"risk_{s}"].to_numpy()
            d[f"gap_{st}_{s}"] = p[f"gap_{s}"].to_numpy()
    p = M.ded.predict(df)
    for s in SC:
        d[f"risk_dedie_{s}"] = p[f"risk_{s}"].to_numpy()
        d[f"gap_dedie_{s}"] = p[f"gap_{s}"].to_numpy()
    point = _c_paired(d)
    res = {"point": point}
    if n_boot:
        cols = [DURATION, EVENT] + [c for c in d.columns if c.startswith("risk_")]
        reps = bootstrap(d[cols], functools.partial(_c_paired), n_boot, SEED)
        res["resume"] = summarize(point, reps).to_dict(orient="records")
    res["biais_vs_complet"] = {f"{st}_{s}": {"moyen": float((d[f"gap_{st}_{s}"] - d[f"gap_complet_{s}"]).mean()),
                                             "p95_abs": float(np.percentile(np.abs(d[f"gap_{st}_{s}"] - d[f"gap_complet_{s}"]), 95))}
                               for st in ["imputation", "communs", "dedie"] for s in SC}
    return res


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def predictions() -> Path:
    """Calage : paires 2001-2002 et developpement (apparent). A commiter avant NHANES III et la
    validation 2007-2010."""
    M = Q3Models()
    e1, e2 = pairs_2001(M)
    res = {"n_2001": len(e1), "r2_imputation_log_acr_dev": M.imp_r2,
           "paires_2001": pair_metrics(M, e1, e2), "developpement": discrimination(M, M.dev),
           "sha256_code": _sha(Path(__file__))}
    PRED.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return PRED


def analyse() -> Path:
    from .config import ROOT, load_study
    from .cohort import build_cohort
    from .nhanes import build_harmonized
    M = Q3Models()
    e1, e2 = pairs_nh3(M)
    study = load_study()
    h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    co, _ = build_cohort(h, load_panel("checkup_standard"), study)
    val = co[co["cycle"].isin(study["cycles"]["validation"])].reset_index(drop=True)
    res = {"n_nh3": len(e1), "paires_nh3": pair_metrics(M, e1, e2),
           "validation": discrimination(M, val, study["validation"]["bootstrap"]),
           "sha256_code": _sha(Path(__file__))}
    RES.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return RES


if __name__ == "__main__":
    import sys
    {"predictions": predictions, "analyse": analyse}[sys.argv[1]]()
