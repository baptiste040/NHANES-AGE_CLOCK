"""src/model.py - Phase 3 : modele de Cox pour predire la mortalite.

Entraine un lifelines.CoxPHFitter sur la cohorte produite par
build_cohort.py, avec l'age et les marqueurs biologiques (CRP en log)
comme covariables, la duree de suivi PERMTH_EXM et l'evenement MORTSTAT.
"""
from pathlib import Path

import joblib
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.model_selection import train_test_split

COHORT_PATH = Path("data/processed/cohort_2009_2010.csv")
MODEL_PATH = Path("models/cox_2009_2010.pkl")

DURATION_COL = "PERMTH_EXM"
EVENT_COL = "MORTSTAT"

COVARIATES = [
    "age", "albumin", "creatinine", "glucose", "alp",
    "lymph_pct", "mcv", "rdw", "wbc", "crp_log",
]


def load_data():
    df = pd.read_csv(COHORT_PATH)
    df = df.dropna(subset=[DURATION_COL])

    model_df = df[COVARIATES + [DURATION_COL, EVENT_COL]]

    train_df, test_df = train_test_split(
        model_df, test_size=0.2, random_state=42, stratify=model_df[EVENT_COL]
    )
    return train_df, test_df


def train_model(train_df):
    cph = CoxPHFitter()
    cph.fit(train_df, duration_col=DURATION_COL, event_col=EVENT_COL)
    return cph


def evaluate(cph, train_df, test_df):
    print("\n--- Resume du modele ---")
    cph.print_summary()

    train_c_index = cph.concordance_index_
    print(f"\nC-index (train, via concordance_index_) : {train_c_index:.4f}")

    test_pred = -cph.predict_partial_hazard(test_df)
    test_c_index = concordance_index(
        test_df[DURATION_COL], test_pred, test_df[EVENT_COL]
    )
    print(f"C-index (test, calcul explicite) : {test_c_index:.4f}")

    print("\n--- Verification de l'hypothese de proportionnalite ---")
    cph.check_assumptions(train_df, show_plots=False)

    return train_c_index, test_c_index


def main():
    train_df, test_df = load_data()

    print(f"Train : {train_df.shape[0]} lignes | Test : {test_df.shape[0]} lignes")

    cph = train_model(train_df)
    evaluate(cph, train_df, test_df)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(cph, MODEL_PATH)
    print(f"\nModele sauve dans : {MODEL_PATH}")

    return cph


if __name__ == "__main__":
    main()
