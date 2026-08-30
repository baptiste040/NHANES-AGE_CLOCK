"""src/build_cohort.py - Phase 2 : construction de la cohorte analytique.

Assemble une table une-ligne-par-personne a partir des DataFrames NHANES
2009-2010 charges par src/load.py, prete a servir de base pour une horloge
biologique type PhenoAge. Aucune conversion d'unite n'est faite ici : les
marqueurs restent dans leurs unites natives NHANES (voir commentaires sur
chaque renommage). Les conversions necessaires a la formule PhenoAge seront
faites plus tard, au moment du calcul de l'age biologique.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from load import main as load_all

OUT_PATH = Path("data/processed/cohort_2009_2010.csv")

BIOMARKERS = [
    "albumin", "creatinine", "glucose", "alp",
    "lymph_pct", "mcv", "rdw", "wbc", "crp",
]


def select_rename(df, columns):
    df = df[list(columns.keys())].rename(columns=columns)
    return df


def build_cohort(frames):
    demo = select_rename(frames["DEMO"], {
        "SEQN": "SEQN",
        "RIDAGEYR": "age",          # annees
        "RIAGENDR": "sex",          # 1 = homme, 2 = femme
        "RIDRETH1": "race_eth",     # code categoriel NHANES
        "INDFMPIR": "income_pir",   # ratio revenu/seuil pauvrete, sans unite
    })

    biopro = select_rename(frames["BIOPRO"], {
        "SEQN": "SEQN",
        "LBXSAL": "albumin",        # g/dL
        "LBXSCR": "creatinine",     # mg/dL
        "LBXSGL": "glucose",        # mg/dL
        "LBXSAPSI": "alp",          # U/L (phosphatase alcaline)
    })

    cbc = select_rename(frames["CBC"], {
        "SEQN": "SEQN",
        "LBXLYPCT": "lymph_pct",    # % lymphocytes
        "LBXMCVSI": "mcv",          # fL (volume globulaire moyen)
        "LBXRDW": "rdw",            # % (largeur de distribution des GR)
        "LBXWBCSI": "wbc",          # 1000 cellules/uL
    })

    crp = select_rename(frames["CRP"], {
        "SEQN": "SEQN",
        "LBXCRP": "crp",            # mg/dL (CRP standard NHANES)
    })

    mort = frames["MORT"][
        ["SEQN", "ELIGSTAT", "MORTSTAT", "PERMTH_EXM", "UCOD_LEADING"]
    ]

    cohort = demo.merge(biopro, on="SEQN", how="left")
    cohort = cohort.merge(cbc, on="SEQN", how="left")
    cohort = cohort.merge(crp, on="SEQN", how="left")
    cohort = cohort.merge(mort, on="SEQN", how="left")

    cohort = cohort[cohort["ELIGSTAT"] == 1]
    cohort = cohort[cohort["age"] >= 20]
    cohort = cohort.dropna(subset=BIOMARKERS)

    cohort["crp_log"] = np.log(cohort["crp"] + 1e-4)

    return cohort


def main():
    frames = load_all()
    cohort = build_cohort(frames)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cohort.to_csv(OUT_PATH, index=False)

    print("\n--- Milestone Phase 2 ---")
    print(f"Table : {cohort.shape[0]} lignes x {cohort.shape[1]} colonnes")
    print(f"Sauve dans : {OUT_PATH}")

    deces = int((cohort["MORTSTAT"] == 1).sum())
    vivants = int((cohort["MORTSTAT"] == 0).sum())
    print(f"Deces : {deces} | Vivants : {vivants} | Total : {deces + vivants}")

    cols_head = ["age", "sex"] + BIOMARKERS + ["MORTSTAT", "PERMTH_EXM"]
    print("\n.head() :")
    print(cohort[cols_head].head())

    return cohort


if __name__ == "__main__":
    main()
