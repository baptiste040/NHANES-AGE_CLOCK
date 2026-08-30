"""src/phenoage_crosscheck.py - Phase 5 : cross-check contre PhenoAge (Levine 2018).

Calcule le PhenoAge par la formule fermee publiee par Levine et al. (2018)
et le compare a notre horloge maison (age_bio de biological_age.py). Sert
de validation externe : deux methodes independantes (Cox sur risque de
mortalite vs formule fermee sur biomarqueurs) devraient produire des ages
biologiques correles.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COHORT_PATH = Path("data/processed/cohort_with_bioage.csv")
FIGURE_PATH = Path("figures/bioage_vs_phenoage.png")

HORIZON = 120
GAMMA = 0.0076927


def compute_phenoage(age, albumin, creatinine, glucose, crp_log,
                      lymph_pct, mcv, rdw, alp, wbc):
    # Conversions vers les unites de la formule PhenoAge (locales uniquement)
    albumin_gL = albumin * 10        # g/dL -> g/L
    creat_umol = creatinine * 88.4   # mg/dL -> umol/L
    gluc_mmol = glucose * 0.0555     # mg/dL -> mmol/L
    ln_crp = crp_log                 # deja ln(CRP en mg/dL)

    xb = (
        -19.907
        - 0.0336 * albumin_gL
        + 0.0095 * creat_umol
        + 0.1953 * gluc_mmol
        + 0.0954 * ln_crp
        - 0.0120 * lymph_pct
        + 0.0268 * mcv
        + 0.3306 * rdw
        + 0.00188 * alp
        + 0.0554 * wbc
        + 0.0804 * age
    )

    M = 1 - np.exp(-np.exp(xb) * (np.exp(HORIZON * GAMMA) - 1) / GAMMA)
    M = np.clip(M, 1e-8, 1 - 1e-8)

    phenoage = 141.50225 + np.log(-0.00553 * np.log(1 - M)) / 0.090165
    return phenoage


def load_data():
    return pd.read_csv(COHORT_PATH)


def add_phenoage(df):
    df["phenoage"] = compute_phenoage(
        age=df["age"],
        albumin=df["albumin"],
        creatinine=df["creatinine"],
        glucose=df["glucose"],
        crp_log=df["crp_log"],
        lymph_pct=df["lymph_pct"],
        mcv=df["mcv"],
        rdw=df["rdw"],
        alp=df["alp"],
        wbc=df["wbc"],
    )
    return df


def sanity_check():
    crp = 0.1
    crp_log = np.log(crp + 1e-4)
    result = compute_phenoage(
        age=40, albumin=4.7, creatinine=0.8, glucose=99, crp_log=crp_log,
        lymph_pct=33, mcv=90, rdw=13, alp=50, wbc=5.0,
    )
    print("\n--- Sanity check ---")
    print("Cas type : quadra en bonne sante (age=40)")
    print(f"PhenoAge obtenu : {result:.2f} ans (attendu ~31 ans)")
    return result


def plot_comparison(df):
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(df["age_bio"], df["phenoage"], s=8, alpha=0.3)

    lims = [
        min(df["age_bio"].min(), df["phenoage"].min()),
        max(df["age_bio"].max(), df["phenoage"].max()),
    ]
    ax.plot(lims, lims, color="red", linestyle="--", label="y = x")

    ax.set_xlabel("age_bio (horloge maison, Cox)")
    ax.set_ylabel("phenoage (formule Levine 2018)")
    ax.set_title("Cross-check : age biologique maison vs PhenoAge")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)
    print(f"\nFigure sauvee dans : {FIGURE_PATH}")


def main():
    df = load_data()
    df = add_phenoage(df)
    df.to_csv(COHORT_PATH, index=False)

    print(f"Cohorte : {df.shape[0]} lignes")
    print(f"Sauve dans : {COHORT_PATH}")

    print("\n--- describe() phenoage ---")
    print(df["phenoage"].describe())

    n_nan = df["phenoage"].isna().sum()
    print(f"\nNombre de NaN dans phenoage : {n_nan}")

    corr_bioage = df["phenoage"].corr(df["age_bio"], method="pearson")
    corr_age = df["phenoage"].corr(df["age"], method="pearson")
    print(f"\nCorrelation Pearson phenoage vs age_bio : {corr_bioage:.4f}")
    print(f"Correlation Pearson phenoage vs age      : {corr_age:.4f}")

    sanity_check()

    plot_comparison(df)

    return df


if __name__ == "__main__":
    main()
