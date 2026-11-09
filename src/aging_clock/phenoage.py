"""PhenoAge publie (Levine et al. 2018), sans reentrainement.

Coefficients : Levine et al., Aging 2018, tableau 1 (doi:10.18632/aging.101414).
Equation complete : correction de Liu et al., PLoS Med 2019 (doi:10.1371/journal.pmed.1002760) :
    M        = 1 - exp(-1.51714 * exp(xb) / 0.0076927)
    PhenoAge = 141.50 + ln(-0.00553 * ln(1 - M)) / 0.09165
1.51714 = exp(120 * 0.0076927) - 1 : M est le risque de deces a 10 ans d'un modele de Gompertz.

Entrees en unites canoniques du projet (identiques a la publication sauf la CRP,
fournie en mg/L et convertie ici en mg/dL).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

INTERCEPT = -19.907
COEFS = {                       # unite attendue par la formule
    "albumin": -0.0336,         # g/L
    "creatinine": 0.0095,       # umol/L
    "glucose": 0.1953,          # mmol/L
    "ln_crp": 0.0954,           # ln(mg/dL)
    "lymph_pct": -0.0120,       # %
    "mcv": 0.0268,              # fL
    "rdw": 0.3306,              # %
    "alp": 0.00188,             # U/L
    "wbc": 0.0554,              # 1000 cellules/uL = 10^9/L
    "age": 0.0804,              # annees
}
GAMMA = 0.0076927
HORIZON_MONTHS = 120
SCALE = 1.51714                 # exp(HORIZON_MONTHS * GAMMA) - 1, tel que publie
AGE_CONST, LOG_FACTOR, AGE_DENOM = 141.50, -0.00553, 0.09165

MARKERS = ["albumin", "creatinine", "glucose", "crp", "lymph_pct", "mcv", "rdw", "alp", "wbc"]


def linear_predictor(df: pd.DataFrame) -> np.ndarray:
    crp_mgdl = df["crp"].to_numpy(float) / 10.0             # mg/L -> mg/dL
    terms = {k: df[k].to_numpy(float) for k in COEFS if k != "ln_crp"}
    terms["ln_crp"] = np.log(crp_mgdl)
    return INTERCEPT + sum(COEFS[k] * terms[k] for k in COEFS)


def mortality_score(df: pd.DataFrame) -> np.ndarray:
    """Risque de deces a 10 ans (M)."""
    return 1.0 - np.exp(-SCALE * np.exp(linear_predictor(df)) / GAMMA)


def phenoage(df: pd.DataFrame) -> np.ndarray:
    m = np.clip(mortality_score(df), 1e-12, 1 - 1e-12)
    return AGE_CONST + np.log(LOG_FACTOR * np.log(1.0 - m)) / AGE_DENOM


def fit_acceleration(dev: pd.DataFrame) -> tuple[float, float]:
    """Regression lineaire PhenoAge ~ age, estimee sur le developpement (Liu et al. 2018)."""
    slope, intercept = np.polyfit(dev["age"].to_numpy(float), phenoage(dev), 1)
    return float(intercept), float(slope)


def acceleration(df: pd.DataFrame, coef: tuple[float, float]) -> np.ndarray:
    intercept, slope = coef
    return phenoage(df) - (intercept + slope * df["age"].to_numpy(float))
