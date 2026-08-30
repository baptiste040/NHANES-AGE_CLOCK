"""src/biological_age.py - Phase 4 : conversion risque -> age biologique.

Methode "maison" (sans les constantes publiees de Levine) :
1. Le modele Cox complet donne un risque de deces a horizon fixe pour
   chaque personne (covariables = age + marqueurs biologiques).
2. Un second Cox, entraine avec l'age comme seule covariable, sert de
   courbe de reference "risque attendu pour un age donne".
3. L'age biologique d'une personne est l'age, sur cette courbe de
   reference, qui produirait le meme risque que celui predit par le
   modele complet (inversion par interpolation).
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

COHORT_PATH = Path("data/processed/cohort_2009_2010.csv")
MODEL_PATH = Path("models/cox_2009_2010.pkl")
OUT_PATH = Path("data/processed/cohort_with_bioage.csv")

DURATION_COL = "PERMTH_EXM"
EVENT_COL = "MORTSTAT"

COVARIATES = [
    "age", "albumin", "creatinine", "glucose", "alp",
    "lymph_pct", "mcv", "rdw", "wbc", "crp_log",
]

HORIZON = 120  # mois
AGE_GRID = np.arange(20, 110.5, 0.5)


def load_data():
    df = pd.read_csv(COHORT_PATH)
    df = df[df[DURATION_COL] > 0].reset_index(drop=True)

    cph_full = joblib.load(MODEL_PATH)
    return df, cph_full


def compute_full_risk(cph_full, df):
    X = df[COVARIATES]
    surv = cph_full.predict_survival_function(X, times=[HORIZON])
    p_full = 1 - surv.loc[HORIZON].to_numpy()
    return p_full


def train_reference_curve(df):
    age_only_df = df[["age", DURATION_COL, EVENT_COL]]
    cph_age = CoxPHFitter()
    cph_age.fit(age_only_df, duration_col=DURATION_COL, event_col=EVENT_COL)

    grid_df = pd.DataFrame({"age": AGE_GRID})
    surv_grid = cph_age.predict_survival_function(grid_df, times=[HORIZON])
    p_age_grid = 1 - surv_grid.loc[HORIZON].to_numpy()

    return cph_age, p_age_grid


def invert_to_bioage(p_full, p_age_grid):
    age_bio = np.interp(p_full, p_age_grid, AGE_GRID)
    return age_bio


def main():
    df, cph_full = load_data()

    p_full = compute_full_risk(cph_full, df)
    cph_age, p_age_grid = train_reference_curve(df)
    age_bio = invert_to_bioage(p_full, p_age_grid)

    df["age_bio"] = age_bio
    df["gap"] = df["age_bio"] - df["age"]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Cohorte : {df.shape[0]} lignes (PERMTH_EXM > 0)")
    print(f"Sauve dans : {OUT_PATH}")

    print("\n--- describe() age_bio ---")
    print(df["age_bio"].describe())

    print("\n--- describe() gap ---")
    print(df["gap"].describe())

    corr = df["age_bio"].corr(df["age"], method="pearson")
    print(f"\nCorrelation Pearson age_bio vs age : {corr:.4f}")

    print("\n--- Exemples ---")
    print(df[["age", "age_bio", "gap", "MORTSTAT"]].sample(5, random_state=42))

    return df


if __name__ == "__main__":
    main()
