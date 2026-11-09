"""Harmonisation de dosages entre cohortes / cycles.

Deux outils :
* equations de pontage publiees (lineaires ou log10) ;
* recalage par quantiles par strates sexe x age : chaque valeur est remplacee par le
  quantile de meme rang dans la distribution de reference de la meme strate. N'utilise que
  les marqueurs, jamais la survie. Methode candidate pour la transposition a une autre
  cohorte (point 4 du plan).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def apply_crosswalk(values: pd.Series, spec: dict) -> pd.Series:
    """`values` en unites canoniques ; l'equation est exprimee en unites NHANES."""
    x = values.astype(float)
    if spec["type"] == "log10":
        out = 10 ** (spec["slope"] * np.log10(x) + spec["intercept"])
    else:
        factor = spec.get("factor", 1)
        out = spec["slope"] * x + spec["intercept"] * factor
    if "max_input" in spec:
        out = out.where(x <= spec["max_input"], x)
    if "min_output" in spec:            # une equation lineaire peut sortir du domaine physique
        out = out.clip(lower=spec["min_output"])
    return out


def strata(age: pd.Series, sex: pd.Series, bands: list[int]) -> pd.Series:
    band = pd.cut(age, bands, right=False, labels=False)
    return sex.astype("Int64").astype(str) + "_" + band.astype("Int64").astype(str)


def quantile_map(target: pd.DataFrame, reference: pd.DataFrame, var: str, bands: list[int]) -> pd.Series:
    """Recalage par quantiles de `target[var]` sur `reference[var]`, strate par strate.

    `target` et `reference` contiennent les colonnes age, sex et `var`. Le rang est calcule
    dans la distribution de la strate de `target` (rang moyen pour les ex-aequo).
    """
    t_str = strata(target["age"], target["sex"], bands)
    r_str = strata(reference["age"], reference["sex"], bands)
    out = pd.Series(np.nan, index=target.index)
    for s in t_str.dropna().unique():
        tv = target.loc[(t_str == s) & target[var].notna(), var]
        rv = reference.loc[(r_str == s) & reference[var].notna(), var].to_numpy()
        if len(tv) == 0 or len(rv) == 0:
            continue
        pct = (tv.rank(method="average") - 0.5) / len(tv)
        out.loc[tv.index] = np.quantile(rv, pct.to_numpy())
    return out
