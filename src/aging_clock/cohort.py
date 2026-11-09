"""Construction de la cohorte analytique a partir de la table harmonisee et d'un panel."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import Panel

DURATION = "PERMTH_EXM"
EVENT = "MORTSTAT"


def apply_panel_ranges(df: pd.DataFrame, panel: Panel) -> tuple[pd.DataFrame, pd.Series]:
    """Valeurs hors plage plausible -> NA. Renvoie aussi le nombre de valeurs rejetees."""
    df = df.copy()
    rejected = {}
    for v in panel.variables.values():
        if v.name not in df:
            continue
        if v.range is not None:
            lo, hi = v.range
            bad = df[v.name].notna() & ~df[v.name].between(lo, hi)
            rejected[v.name] = int(bad.sum())
            df.loc[bad, v.name] = np.nan
    return df, pd.Series(rejected, name="hors_plage")


def build_cohort(harmonized: pd.DataFrame, panel: Panel, study: dict,
                 age_min=None, age_max=None, exclude_pregnant=None) -> tuple[pd.DataFrame, list]:
    """Filtre la population, applique le panel et garde les cas complets.

    Renvoie la cohorte et le diagramme de flux (liste d'etapes, effectifs).
    """
    pop = study["population"]
    age_min = pop["age_min"] if age_min is None else age_min
    age_max = pop["age_max"] if age_max is None else age_max
    exclude_pregnant = pop["exclude_pregnant"] if exclude_pregnant is None else exclude_pregnant

    df = harmonized
    flow = [("participants NHANES", len(df))]

    df = df[df["age"].between(age_min, age_max)]
    flow.append((f"age {age_min}-{age_max} ans", len(df)))

    df = df[(df["ELIGSTAT"] == 1) & df[DURATION].notna() & (df[DURATION] > 0)]
    flow.append(("eligibles au chainage mortalite, suivi > 0", len(df)))

    if exclude_pregnant:
        df = df[df["pregnant"] != 1]
        flow.append(("hors femmes enceintes", len(df)))

    df, _ = apply_panel_ranges(df, panel)
    needed = panel.model_variables + ["sex"]
    df = df.dropna(subset=needed)
    flow.append(("cas complets sur le panel", len(df)))

    df = df.copy()
    df[EVENT] = df[EVENT].astype(int)
    return df.reset_index(drop=True), flow


def add_cause_events(df: pd.DataFrame, cause_groups: dict) -> pd.DataFrame:
    df = df.copy()
    for name, codes in cause_groups.items():
        df[f"event_{name}"] = ((df[EVENT] == 1) & df["UCOD_LEADING"].isin(codes)).astype(int)
    return df


def has_prevalent_condition(df: pd.DataFrame, conditions: list[str]) -> pd.Series:
    return (df[conditions].fillna(0) == 1).any(axis=1)
