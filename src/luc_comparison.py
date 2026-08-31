"""src/luc_comparison.py - Phase 8 : application des deux horloges aux marqueurs de Luc.

Reutilise directement la logique de biological_age.py (horloge Cox maison)
et de phenoage_crosscheck.py (formule fermee de Levine) pour comparer les
deux methodes sur un cas individuel, a mettre en regard du rapport Lucis.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from biological_age import (
    COVARIATES,
    compute_full_risk,
    invert_to_bioage,
    load_data as load_bioage_data,
    train_reference_curve,
)
from phenoage_crosscheck import compute_phenoage

LUC_PATH = Path("data/private/luc_markers.json")

LUC_MARKERS = {
    "age": 27,
    "albumin": 4.5,
    "creatinine": 1.086,
    "glucose": 94,
    "alp": 55,
    "lymph_pct": 40.3,
    "mcv": 92.7,
    "rdw": 13,
    "wbc": 6.2,
    "crp": 0.017,  # mg/dL
}


def save_luc_markers():
    LUC_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LUC_PATH, "w") as f:
        json.dump(LUC_MARKERS, f, indent=2)
    print(f"Marqueurs de Luc sauves dans : {LUC_PATH}")
    return LUC_MARKERS


def compute_bioage_for_luc(luc, cph_full, cohort_df):
    luc_row = {**luc, "crp_log": np.log(luc["crp"] + 1e-4)}
    luc_X = pd.DataFrame([luc_row])[COVARIATES]

    p_full_luc = compute_full_risk(cph_full, luc_X)
    _, p_age_grid = train_reference_curve(cohort_df)
    age_bio_luc = invert_to_bioage(p_full_luc, p_age_grid)[0]

    return age_bio_luc, luc_row["crp_log"]


def compute_phenoage_for_luc(luc, crp_log):
    return compute_phenoage(
        age=luc["age"],
        albumin=luc["albumin"],
        creatinine=luc["creatinine"],
        glucose=luc["glucose"],
        crp_log=crp_log,
        lymph_pct=luc["lymph_pct"],
        mcv=luc["mcv"],
        rdw=luc["rdw"],
        alp=luc["alp"],
        wbc=luc["wbc"],
    )


def main():
    luc = save_luc_markers()

    cohort_df, cph_full = load_bioage_data()

    age_bio_luc, crp_log = compute_bioage_for_luc(luc, cph_full, cohort_df)
    gap_bioage = age_bio_luc - luc["age"]

    print("\n--- Horloge maison (Cox) ---")
    print(f"age_bio : {age_bio_luc:.2f} ans")
    print(f"gap     : {gap_bioage:+.2f} ans")

    phenoage_luc = compute_phenoage_for_luc(luc, crp_log)
    gap_phenoage = phenoage_luc - luc["age"]

    print("\n--- PhenoAge (formule Levine 2018) ---")
    print(f"phenoage : {phenoage_luc:.2f} ans")
    print(f"gap      : {gap_phenoage:+.2f} ans")

    print("\n--- Recap final ---")
    print(f"{'age chrono':<25}{luc['age']:>10}")
    print(f"{'age_bio (horloge maison)':<25}{age_bio_luc:>10.2f}")
    print(f"{'phenoage (Levine)':<25}{phenoage_luc:>10.2f}")
    print(f"{'gap horloge maison':<25}{gap_bioage:>+10.2f}")
    print(f"{'gap phenoage':<25}{gap_phenoage:>+10.2f}")

    return age_bio_luc, phenoage_luc


if __name__ == "__main__":
    main()
