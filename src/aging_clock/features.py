"""Transformations des variables du panel : plancher, winsorisation, log, splines.

Tout ce qui est appris (bornes de winsorisation, noeuds) est appris sur le
developpement puis fige, pour etre exporte avec le modele.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import Panel

# Percentiles de Harrell pour le placement des noeuds
_KNOT_QUANTILES = {
    3: [0.10, 0.50, 0.90],
    4: [0.05, 0.35, 0.65, 0.95],
    5: [0.05, 0.275, 0.50, 0.725, 0.95],
}


def rcs_basis(x: np.ndarray, knots: np.ndarray) -> np.ndarray:
    """Termes non lineaires d'une spline cubique restreinte (parametrisation de Harrell).

    Renvoie k-2 colonnes ; le terme lineaire x est ajoute a part.
    """
    x = np.asarray(x, dtype=float)
    k = len(knots)
    t_last, t_prev = knots[-1], knots[-2]
    scale = (knots[-1] - knots[0]) ** 2
    cols = []
    for j in range(k - 2):
        tj = knots[j]
        term = (np.maximum(x - tj, 0) ** 3
                - np.maximum(x - t_prev, 0) ** 3 * (t_last - tj) / (t_last - t_prev)
                + np.maximum(x - t_last, 0) ** 3 * (t_prev - tj) / (t_last - t_prev))
        cols.append(term / scale)
    return np.column_stack(cols)


class FeatureTransformer:
    """Transforme les variables brutes (unites canoniques) en covariables de modele."""

    def __init__(self, panel: Panel, variables: list[str], winsor_quantiles=(0.005, 0.995)):
        self.panel = panel
        self.variables = variables
        self.winsor_quantiles = winsor_quantiles
        self.state: dict[str, dict] = {}

    def _pre(self, name: str, x: pd.Series) -> pd.Series:
        v = self.panel.variables[name]
        x = x.astype(float)
        if v.floor is not None:
            x = x.clip(lower=v.floor)
        if v.log:
            x = np.log(x)
        return x

    def fit(self, df: pd.DataFrame) -> "FeatureTransformer":
        lo_q, hi_q = self.winsor_quantiles
        for name in self.variables:
            x = self._pre(name, df[name])
            lo, hi = float(x.quantile(lo_q)), float(x.quantile(hi_q))
            st = {"clip": [lo, hi]}
            n_knots = self.panel.variables[name].spline
            if n_knots:
                xc = x.clip(lo, hi)
                st["knots"] = [float(q) for q in xc.quantile(_KNOT_QUANTILES[n_knots])]
            self.state[name] = st
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = {}
        for name in self.variables:
            st = self.state[name]
            x = self._pre(name, df[name]).clip(*st["clip"])
            out[name] = x.to_numpy()
            if "knots" in st:
                basis = rcs_basis(x.to_numpy(), np.array(st["knots"]))
                for j in range(basis.shape[1]):
                    out[f"{name}_s{j + 1}"] = basis[:, j]
        return pd.DataFrame(out, index=df.index)

    def columns_for(self, names: list[str]) -> list[str]:
        cols = []
        for name in names:
            cols.append(name)
            if "knots" in self.state[name]:
                cols += [f"{name}_s{j + 1}" for j in range(len(self.state[name]["knots"]) - 2)]
        return cols
