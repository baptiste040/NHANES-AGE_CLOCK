"""Incertitude individuelle de l'age biologique par simulation de Monte-Carlo.

Dependances : NumPy, pandas, bibliotheque standard. Utilise par l'option
`python -m aging_clock score --uncertainty` et par l'analyse descriptive.

Hypothese : on simule des « remesures » autour de la valeur observee, qui contient deja du
bruit. La dispersion obtenue est celle d'une nouvelle mesure, pas l'ecart a une vraie valeur.
Bruit multiplicatif log-normal de mediane 1 : x* = x · exp(N(0, σ)), σ = racine(ln(1 + CV²)).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .score import bioages, score_names

DEFAULT_VARIABILITY = Path(__file__).resolve().parents[2] / "config" / "variability.yaml"
BLOOD_URINE = {"albumin", "creatinine", "glucose", "tg", "total_chol", "hdl", "alp", "alt", "ast",
               "ggt", "crp", "hba1c", "wbc", "lymph_pct", "rdw", "mcv", "hb", "platelets", "acr"}


def load_variability(path: str | Path = DEFAULT_VARIABILITY) -> dict:
    """Fichier en syntaxe JSON (valide en YAML) ; voir config/variability.example.yaml."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} absent. Copier config/variability.example.yaml en config/variability.yaml "
            "et renseigner les valeurs manquantes (voir la licence de la base EFLM).")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k, v in data["variables"].items() if v.get("cv_i") is None]
    if missing:
        raise ValueError(f"CV_I non renseignes dans {path.name} : {', '.join(missing)}")
    return data["variables"]


def total_cv(var: dict, which: str = "cv_i", fasting: bool = False, divide: float = 1.0) -> float:
    """CV total (fraction) = racine(CV_I² + CV_A²) / divide."""
    cvi = var.get("cv_i_fasting") if fasting and var.get("cv_i_fasting") is not None else var[which]
    cva = var.get("cv_a") or 0.0
    return float(np.sqrt(cvi ** 2 + cva ** 2)) / 100.0 / divide


def cv_set(variability: dict, model: dict, which: str = "cv_i", fasting: bool = False,
           blood_divide: float = 1.0, only: str | None = None) -> dict[str, float]:
    out = {}
    for name in model["variables"]:
        cv = total_cv(variability[name], which, fasting,
                      blood_divide if name in BLOOD_URINE else 1.0)
        out[name] = cv if only in (None, name) else 0.0
    return out


def simulate(df: pd.DataFrame, model: dict, cvs: dict[str, float], n_draws: int = 1000,
             seed: int = 2026, chunk: int = 200) -> dict[str, np.ndarray]:
    """Ages biologiques remesures : {score: tableau (n_personnes, n_draws)}.

    Reproductible : le flux aleatoire depend de `seed` et de la position de la personne.
    """
    names = score_names(model)
    out = {n: np.empty((len(df), n_draws)) for n in names}
    variables = list(model["variables"])
    sig = np.array([np.sqrt(np.log1p(cvs[v] ** 2)) for v in variables])
    base = df[["age", "sex"] + variables].reset_index(drop=True)
    seeds = np.random.SeedSequence(seed).spawn((len(df) + chunk - 1) // chunk)
    for c, start in enumerate(range(0, len(df), chunk)):
        block = base.iloc[start:start + chunk]
        rng = np.random.default_rng(seeds[c])
        rep = block.loc[block.index.repeat(n_draws)].reset_index(drop=True)
        noise = np.exp(rng.standard_normal((len(rep), len(variables))) * sig)
        rep[variables] = rep[variables].to_numpy(float) * noise
        bio, _ = bioages(rep, model)
        for n in names:
            out[n][start:start + len(block)] = bio[n].reshape(len(block), n_draws)
    return out


def intervals(sims: dict[str, np.ndarray], level: float = 0.95) -> pd.DataFrame:
    a = (1 - level) / 2
    cols = {}
    for n, s in sims.items():
        cols[f"age_bio_{n}_et"] = s.std(axis=1, ddof=1)
        cols[f"age_bio_{n}_ic95_bas"] = np.quantile(s, a, axis=1)
        cols[f"age_bio_{n}_ic95_haut"] = np.quantile(s, 1 - a, axis=1)
    return pd.DataFrame(cols)
