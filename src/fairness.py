"""src/fairness.py - Phase 7 : audit d'equite de l'horloge de vieillissement.

Verifie que age_bio (et le gap qui en decoule) ne biaise pas
systematiquement certains sous-groupes demographiques - sexe, origine
ethnique, revenu - en termes de calibration (gap moyen) et de precision
predictive (C-index intra-groupe).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines.utils import concordance_index

COHORT_PATH = Path("data/processed/cohort_with_bioage.csv")
FIG_GAP_PATH = Path("figures/fairness_gap_by_group.png")
FIG_CINDEX_PATH = Path("figures/fairness_cindex_by_group.png")

DURATION_COL = "PERMTH_EXM"
EVENT_COL = "MORTSTAT"

SEX_LABELS = {1: "Homme", 2: "Femme"}
RACE_LABELS = {
    1: "Mexican American",
    2: "Other Hispanic",
    3: "Non-Hispanic White",
    4: "Non-Hispanic Black",
    5: "Other/Multi",
}


def load_data():
    df = pd.read_csv(COHORT_PATH)
    df = df[df[DURATION_COL] > 0].copy()
    return df


def prepare_groups(df):
    df["sex_label"] = df["sex"].map(SEX_LABELS)
    df["race_label"] = df["race_eth"].map(RACE_LABELS)

    income = df.dropna(subset=["income_pir"])
    income_group = pd.qcut(income["income_pir"], 5, labels=[f"Q{i}" for i in range(1, 6)])
    df["income_group"] = income_group

    return df


def audit_axis(df, group_col):
    rows = []
    for group, sub in df.groupby(group_col, observed=True):
        sub = sub.dropna(subset=["age_bio", "gap", DURATION_COL, EVENT_COL])
        if sub.shape[0] < 2 or sub[EVENT_COL].sum() == 0:
            c_index = np.nan
        else:
            c_index = concordance_index(
                sub[DURATION_COL], -sub["age_bio"], sub[EVENT_COL]
            )
        rows.append({
            "group": group,
            "n": sub.shape[0],
            "deaths": int(sub[EVENT_COL].sum()),
            "gap_mean": sub["gap"].mean(),
            "gap_std": sub["gap"].std(),
            "mae_gap": sub["gap"].abs().mean(),
            "c_index": c_index,
        })
    return pd.DataFrame(rows)


def print_table(title, table):
    print(f"\n--- {title} ---")
    fmt = table.copy()
    for col in ["gap_mean", "gap_std", "mae_gap", "c_index"]:
        fmt[col] = fmt[col].map(lambda v: f"{v:.4f}" if pd.notna(v) else "NA")
    print(fmt.to_string(index=False))


def plot_gap_by_group(axis_tables, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, len(axis_tables), figsize=(5 * len(axis_tables), 5))

    for ax, (axis_name, table) in zip(axes, axis_tables.items()):
        sem = table["gap_std"] / np.sqrt(table["n"])
        ci95 = 1.96 * sem
        ax.bar(table["group"].astype(str), table["gap_mean"], yerr=ci95, capsize=4)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(axis_name)
        ax.set_ylabel("gap moyen (IC95%)")
        ax.tick_params(axis="x", rotation=30)

    fig.suptitle("Biais de calibration (gap moyen) par sous-groupe")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nFigure sauvee dans : {path}")


def plot_cindex_by_group(axis_tables, global_c_index, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, len(axis_tables), figsize=(5 * len(axis_tables), 5))

    for ax, (axis_name, table) in zip(axes, axis_tables.items()):
        ax.bar(table["group"].astype(str), table["c_index"])
        ax.axhline(global_c_index, color="red", linestyle="--", label="C-index global")
        ax.set_title(axis_name)
        ax.set_ylabel("C-index intra-groupe")
        ax.set_ylim(0.5, 1.0)
        ax.tick_params(axis="x", rotation=30)
        ax.legend(fontsize=8)

    fig.suptitle("Precision predictive (C-index) par sous-groupe")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nFigure sauvee dans : {path}")


def print_summary(axis_tables):
    print("\n--- Resume de l'audit d'equite ---")
    for axis_name, table in axis_tables.items():
        valid = table.dropna(subset=["gap_mean"])
        over = valid.loc[valid["gap_mean"].idxmax()]
        under = valid.loc[valid["gap_mean"].idxmin()]
        c_valid = table.dropna(subset=["c_index"])
        c_gap = c_valid["c_index"].max() - c_valid["c_index"].min()

        print(f"\n{axis_name} :")
        print(f"  Groupe le plus sur-vieilli  : {over['group']} (gap moyen = {over['gap_mean']:.2f})")
        print(f"  Groupe le plus sous-vieilli : {under['group']} (gap moyen = {under['gap_mean']:.2f})")
        print(f"  Ecart de C-index max entre groupes : {c_gap:.4f}")


def main():
    df = load_data()
    df = prepare_groups(df)

    global_c_index = concordance_index(df[DURATION_COL], -df["age_bio"], df[EVENT_COL])
    print(f"C-index global (reference) : {global_c_index:.4f}")

    axis_tables = {
        "Sexe": audit_axis(df, "sex_label"),
        "Origine ethnique": audit_axis(df, "race_label"),
        "Revenu (quintiles)": audit_axis(df, "income_group"),
    }

    for axis_name, table in axis_tables.items():
        print_table(axis_name, table)

    plot_gap_by_group(axis_tables, FIG_GAP_PATH)
    plot_cindex_by_group(axis_tables, global_c_index, FIG_CINDEX_PATH)

    print_summary(axis_tables)

    return axis_tables


if __name__ == "__main__":
    main()
