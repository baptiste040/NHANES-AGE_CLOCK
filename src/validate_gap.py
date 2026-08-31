"""src/validate_gap.py - Phase 6 : le gap predit-il la mortalite au-dela de l'age ?

Test central du projet : compare un modele Cox baseline (age seul) a un
modele Cox augmente (age + gap) sur le meme test set hors echantillon que
la Phase 3, pour verifier que age_bio - age apporte un signal de mortalite
independant de l'age chronologique.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from scipy.stats import chi2
from sklearn.model_selection import train_test_split

COHORT_PATH = Path("data/processed/cohort_with_bioage.csv")
FIGURE_PATH = Path("figures/gap_distribution_by_mortality.png")

DURATION_COL = "PERMTH_EXM"
EVENT_COL = "MORTSTAT"


def load_data():
    df = pd.read_csv(COHORT_PATH)
    df = df[df[DURATION_COL] > 0]

    model_df = df[["age", "gap", DURATION_COL, EVENT_COL]]

    train_df, test_df = train_test_split(
        model_df, test_size=0.2, random_state=42, stratify=model_df[EVENT_COL]
    )
    return df, train_df, test_df


def train_models(train_df):
    cph_a = CoxPHFitter()
    cph_a.fit(train_df[["age", DURATION_COL, EVENT_COL]],
              duration_col=DURATION_COL, event_col=EVENT_COL)

    cph_b = CoxPHFitter()
    cph_b.fit(train_df[["age", "gap", DURATION_COL, EVENT_COL]],
              duration_col=DURATION_COL, event_col=EVENT_COL)

    return cph_a, cph_b


def test_c_index(cph, test_df, covariates):
    pred = -cph.predict_partial_hazard(test_df[covariates])
    return concordance_index(test_df[DURATION_COL], pred, test_df[EVENT_COL])


def likelihood_ratio_test(cph_a, cph_b):
    stat = 2 * (cph_b.log_likelihood_ - cph_a.log_likelihood_)
    df = 1  # un parametre supplementaire (gap) dans le modele B
    p_value = chi2.sf(stat, df)
    return stat, df, p_value


def plot_gap_distribution(df):
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    gap_alive = df.loc[df[EVENT_COL] == 0, "gap"]
    gap_dead = df.loc[df[EVENT_COL] == 1, "gap"]

    ax.hist(gap_alive, bins=40, alpha=0.5, density=True, label="Vivants (MORTSTAT=0)")
    ax.hist(gap_dead, bins=40, alpha=0.5, density=True, label="Decedes (MORTSTAT=1)")

    ax.set_xlabel("gap = age_bio - age")
    ax.set_ylabel("Densite")
    ax.set_title("Distribution du gap selon le statut de mortalite")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)
    print(f"\nFigure sauvee dans : {FIGURE_PATH}")


def main():
    df, train_df, test_df = load_data()
    print(f"Train : {train_df.shape[0]} lignes | Test : {test_df.shape[0]} lignes")

    cph_a, cph_b = train_models(train_df)

    print("\n--- Resume du modele B (age + gap) ---")
    cph_b.print_summary()

    c_index_a = test_c_index(cph_a, test_df, ["age"])
    c_index_b = test_c_index(cph_b, test_df, ["age", "gap"])
    delta = c_index_b - c_index_a

    print("\n--- Comparaison C-index (test, hors echantillon) ---")
    print(f"{'Modele':<25}{'C-index test':>15}")
    print(f"{'A (age seul)':<25}{c_index_a:>15.4f}")
    print(f"{'B (age + gap)':<25}{c_index_b:>15.4f}")
    print(f"{'Delta (B - A)':<25}{delta:>15.4f}")

    stat, df_lrt, p_value = likelihood_ratio_test(cph_a, cph_b)
    print("\n--- Likelihood ratio test (A vs B) ---")
    print(f"log-likelihood A : {cph_a.log_likelihood_:.2f}")
    print(f"log-likelihood B : {cph_b.log_likelihood_:.2f}")
    print(f"Statistique LR   : {stat:.2f} (df={df_lrt})")
    print(f"p-value          : {p_value:.2e}")

    plot_gap_distribution(df)

    return cph_a, cph_b


if __name__ == "__main__":
    main()
