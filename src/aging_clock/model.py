"""Horloge de vieillissement : modeles de Cox (global + par systeme) et age biologique.

Methode :
1. Un Cox « complet » (age, sexe, marqueurs) donne le risque de deces a
   l'horizon H pour chaque personne.
2. Un Cox de reference (age, sexe) donne le risque attendu pour un age et
   un sexe donnes.
3. L'age biologique est l'age qui, sur la courbe de reference du meme sexe,
   donne le meme risque que le modele complet. L'ecart = age biologique - age.
Un age par systeme suit la meme methode avec les seuls marqueurs du systeme.
Tout est entraine sur le developpement et fige.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

from .cohort import DURATION, EVENT
from .config import Panel
from .features import FeatureTransformer

GLOBAL = "global"


class CoxAtHorizon:
    """Cox gele : prediction explicite du risque a horizon, sans dependre de lifelines."""

    def __init__(self, columns: list[str], horizon: float, penalizer: float = 0.0,
                 unpenalized: tuple[str, ...] = ("age", "female")):
        self.columns = columns
        self.horizon = horizon
        # Ridge sur les marqueurs uniquement : penaliser l'age deformerait l'echelle
        # de l'age biologique.
        self.penalizer = np.array([0.0 if c in unpenalized else penalizer for c in columns])

    def fit(self, X: pd.DataFrame, time: pd.Series, event: pd.Series) -> "CoxAtHorizon":
        data = X[self.columns].assign(_T=time.to_numpy(), _E=event.to_numpy())
        cph = CoxPHFitter(penalizer=self.penalizer if self.penalizer.any() else 0.0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cph.fit(data, duration_col="_T", event_col="_E")
        self.lifelines_ = cph
        self.coef_ = cph.params_[self.columns].to_numpy()
        self.mean_ = cph._norm_mean[self.columns].to_numpy()
        bs = cph.baseline_survival_.iloc[:, 0]
        self.s0_ = float(bs[bs.index <= self.horizon].iloc[-1])
        return self

    def linear_predictor(self, X: pd.DataFrame) -> np.ndarray:
        return (X[self.columns].to_numpy() - self.mean_) @ self.coef_

    def risk(self, X: pd.DataFrame) -> np.ndarray:
        return 1.0 - self.s0_ ** np.exp(self.linear_predictor(X))

    def risk_at(self, X: pd.DataFrame, horizon: float) -> np.ndarray:
        """Risque a un autre horizon : memes coefficients, survie de base du developpement."""
        bs = self.lifelines_.baseline_survival_.iloc[:, 0]
        s0 = float(bs[bs.index <= horizon].iloc[-1])
        return 1.0 - s0 ** np.exp(self.linear_predictor(X))


class BioAgeClock:
    def __init__(self, panel: Panel, study: dict):
        self.panel = panel
        m = study["model"]
        self.horizon = m["horizon_months"]
        self.penalizer = m["penalizer"]
        self.winsor = tuple(m["winsor_quantiles"])
        lo, hi, step = m["bioage_grid"]
        self.age_grid = np.arange(lo, hi + step / 2, step)

    # ------------------------------------------------------------------ design
    def _base_cols(self) -> list[str]:
        return ["age", "female"] if self.panel.include_sex else ["age"]

    def design(self, df: pd.DataFrame) -> pd.DataFrame:
        X = self.transformer.transform(df)
        X["age"] = df["age"].astype(float).to_numpy()
        X["female"] = (df["sex"] == 2).astype(float).to_numpy()
        return X

    # --------------------------------------------------------------------- fit
    def fit(self, df: pd.DataFrame) -> "BioAgeClock":
        self.transformer = FeatureTransformer(
            self.panel, self.panel.model_variables, self.winsor).fit(df)
        X = self.design(df)
        t, e = df[DURATION], df[EVENT]

        self.reference = CoxAtHorizon(self._base_cols(), self.horizon).fit(X, t, e)
        self.models: dict[str, CoxAtHorizon] = {}
        groups = {GLOBAL: self.panel.model_variables}
        if len(self.panel.active_systems) > 1:
            groups |= {s: self.panel.system_variables(s) for s in self.panel.active_systems}
        for name, variables in groups.items():
            cols = self._base_cols() + self.transformer.columns_for(variables)
            self.models[name] = CoxAtHorizon(cols, self.horizon, self.penalizer).fit(X, t, e)

        self.ref_grid = {}
        for female in ([0.0, 1.0] if self.panel.include_sex else [0.0]):
            grid = pd.DataFrame({"age": self.age_grid, "female": female})
            self.ref_grid[female] = self.reference.risk(grid)
        return self

    # ----------------------------------------------------------------- predict
    def _invert(self, risk: np.ndarray, female: np.ndarray) -> np.ndarray:
        out = np.empty_like(risk)
        for f, p_grid in self.ref_grid.items():
            mask = (female == f) if self.panel.include_sex else np.ones_like(risk, bool)
            out[mask] = np.interp(risk[mask], p_grid, self.age_grid)
        return out

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        X = self.design(df)
        female = X["female"].to_numpy()
        out = pd.DataFrame(index=df.index)
        out["risk_ref"] = self.reference.risk(X)
        for name, model in self.models.items():
            risk = model.risk(X)
            bioage = self._invert(risk, female)
            out[f"risk_{name}"] = risk
            out[f"bioage_{name}"] = bioage
            out[f"gap_{name}"] = bioage - df["age"].to_numpy()
            out[f"clipped_{name}"] = (bioage <= self.age_grid[0]) | (bioage >= self.age_grid[-1])
        return out

    @property
    def score_names(self) -> list[str]:
        return list(self.models)

    def hazard_ratios(self) -> pd.DataFrame:
        rows = []
        for name, model in self.models.items():
            s = model.lifelines_.summary
            for col in model.columns:
                rows.append({"modele": name, "covariable": col,
                             "coef": s.loc[col, "coef"], "HR": s.loc[col, "exp(coef)"],
                             "p": s.loc[col, "p"]})
        return pd.DataFrame(rows)
