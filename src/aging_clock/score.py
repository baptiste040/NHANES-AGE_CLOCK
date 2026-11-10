"""Calcul autonome des ages biologiques a partir du modele gele (JSON).

Dependances : NumPy et pandas uniquement (plus la bibliotheque standard). Ne depend ni du
pipeline d'entrainement, ni de lifelines.

Usage :
    python -m aging_clock score --input fichier.csv [--output scores.csv] [--model modele.json]
ou en Python :
    from aging_clock.score import load_model, score
    scores = score(df, load_model("models/checkup_standard_v1.json"))
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_MODEL = Path(__file__).resolve().parents[2] / "models" / "checkup_standard_v1.json"
_SEX_MAP = {1: 1, 2: 2, "1": 1, "2": 2, "H": 1, "M": 1, "homme": 1, "F": 2, "femme": 2}


def load_model(path: str | Path = DEFAULT_MODEL) -> dict:
    with open(path, encoding="utf-8") as f:
        model = json.load(f)
    if model.get("format") != "aging-clock-model":
        raise ValueError(f"{path} n'est pas un modele aging-clock")
    return model


def _rcs_basis(x: np.ndarray, knots: list[float]) -> np.ndarray:
    k = np.asarray(knots, dtype=float)
    t_last, t_prev, scale = k[-1], k[-2], (k[-1] - k[0]) ** 2
    cols = []
    for tj in k[:-2]:
        term = (np.maximum(x - tj, 0) ** 3
                - np.maximum(x - t_prev, 0) ** 3 * (t_last - tj) / (t_last - t_prev)
                + np.maximum(x - t_last, 0) ** 3 * (t_prev - tj) / (t_last - t_prev))
        cols.append(term / scale)
    return np.column_stack(cols)


def _design(df: pd.DataFrame, model: dict) -> pd.DataFrame:
    X = {"age": df["age"].to_numpy(float), "female": (df["sex"] == 2).astype(float).to_numpy()}
    for name, v in model["variables"].items():
        x = df[name].to_numpy(float)
        if v["floor"] is not None:
            x = np.maximum(x, v["floor"])
        if v["log"]:
            with np.errstate(divide="ignore", invalid="ignore"):
                x = np.log(x)
        x = np.clip(x, *v["clip_transformed"])
        X[name] = x
        if v["spline_knots_transformed"]:
            basis = _rcs_basis(x, v["spline_knots_transformed"])
            for j in range(basis.shape[1]):
                X[f"{name}_s{j + 1}"] = basis[:, j]
    return pd.DataFrame(X, index=df.index)


def _risk(X: pd.DataFrame, m: dict, horizon: int) -> np.ndarray:
    lp = (X[m["columns"]].to_numpy() - np.asarray(m["means"])) @ np.asarray(m["coefficients"])
    return 1.0 - m["baseline_survival"][str(horizon)] ** np.exp(lp)


def score_names(model: dict) -> list[str]:
    return [n for n in model["models"] if n != "reference"]


def _grid(model: dict) -> np.ndarray:
    g = model["bioage_grid"]
    return np.arange(g["min"], g["max"] + g["step"] / 2, g["step"])


def bioages(df: pd.DataFrame, model: dict) -> tuple[dict[str, np.ndarray], np.ndarray]:
    """Ages biologiques (par score) et risque global a 10 ans, SANS controle des entrees.

    `df` : colonnes age, sex (1/2) et variables du modele, en unites canoniques, valeurs valides.
    """
    horizon = model["horizon_months"]
    grid = _grid(model)
    X = _design(df, model)
    female = X["female"].to_numpy()
    curves = {f: _risk(pd.DataFrame({"age": grid, "female": f}), model["models"]["reference"], horizon)
              for f in ([0.0, 1.0] if model["include_sex"] else [0.0])}
    out, risk_global = {}, None
    for n in score_names(model):
        risk = _risk(X, model["models"][n], horizon)
        bio = np.empty_like(risk)
        for f, curve in curves.items():
            mask = (female == f) if model["include_sex"] else np.ones_like(risk, bool)
            bio[mask] = np.interp(risk[mask], curve, grid)
        out[n] = bio
        if n == "global":
            risk_global = risk
    return out, risk_global


def _check(df: pd.DataFrame, model: dict) -> pd.Series:
    """Statut par ligne : 'ok' ou liste des motifs (scores mis a NA)."""
    issues = pd.Series([[] for _ in range(len(df))], index=df.index)
    lo, hi = model["training"]["age_range"]
    for idx in df.index[df["age"].isna()]:
        issues[idx].append("age manquant")
    for idx in df.index[df["age"].notna() & ~df["age"].between(lo, hi)]:
        issues[idx].append(f"age hors domaine {lo}-{hi} (score calcule, a interpreter avec prudence)")
    for idx in df.index[~df["sex"].isin([1, 2])]:
        issues[idx].append("sexe invalide (1 = homme, 2 = femme)")
    for name, v in model["variables"].items():
        col = df[name]
        for idx in df.index[col.isna()]:
            issues[idx].append(f"{name} manquant")
        if v["range"]:
            bad = col.notna() & ~col.between(*v["range"])
            for idx in df.index[bad]:
                issues[idx].append(f"{name} hors plage {v['range'][0]}-{v['range'][1]} {v['unit']}")
    return issues.map(lambda x: "ok" if not x else " ; ".join(x))


def score(df: pd.DataFrame, model: dict) -> pd.DataFrame:
    """Ages biologiques global et par systeme. `df` en unites canoniques (voir la specification)."""
    missing = [c for c in ["age", "sex", *model["variables"]] if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes obligatoires absentes : {', '.join(missing)}")
    df = df.copy()
    df["sex"] = df["sex"].map(lambda s: _SEX_MAP.get(s, s)).astype("float")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    for name in model["variables"]:
        df[name] = pd.to_numeric(df[name], errors="coerce")

    status = _check(df, model)
    blocking = status.str.contains("manquant|hors plage|sexe invalide", regex=True)
    valid = df.index[~blocking]

    out = pd.DataFrame(index=df.index)
    if "id" in df.columns:
        out["id"] = df["id"]
    names = score_names(model)
    for n in names:
        out[f"age_bio_{n}"] = np.nan
        out[f"ecart_{n}"] = np.nan
    out["risque_deces_10ans"] = np.nan
    if len(valid):
        d = df.loc[valid]
        bio, risk = bioages(d, model)
        grid = _grid(model)
        for n in names:
            out.loc[valid, f"age_bio_{n}"] = bio[n]
            out.loc[valid, f"ecart_{n}"] = bio[n] - d["age"].to_numpy()
        out.loc[valid, "risque_deces_10ans"] = risk
        edge = (bio["global"] <= grid[0]) | (bio["global"] >= grid[-1])
        for idx in d.index[edge]:
            status[idx] = ("" if status[idx] == "ok" else status[idx] + " ; ") +                 "age biologique en limite de grille"
    out["statut"] = status
    return out


DEFAULT_THRESHOLDS = Path(__file__).resolve().parents[2] / "models" / "seuils_changement_v1.json"


def add_change_thresholds(res: pd.DataFrame, df: pd.DataFrame,
                          thresholds_path: str | Path = DEFAULT_THRESHOLDS) -> pd.DataFrame:
    """Seuil empirique de changement significatif (annees) par score.

    Un ecart entre deux bilans est considere comme un vrai changement s'il depasse le seuil.
    Seuils = 95e centile des ecarts observes sur des remesures a quelques semaines (NHANES 2001-2002
    et NHANES III ; models/seuils_changement_v1.json). Valables si la CRP est <= 10 mg/L aux deux
    bilans : si CRP > 10 mg/L, seuil non fourni (alerte_crp). Pas d'intervalle gaussien : le bruit
    reel a des queues epaisses (voir docs/fiche_modele.md).
    """
    with open(thresholds_path, encoding="utf-8") as f:
        th = json.load(f)
    res = res.copy()
    crp_hi = pd.to_numeric(df["crp"], errors="coerce") > 10
    res["alerte_crp"] = crp_hi.to_numpy()
    for n, spec in th["scores"].items():
        col = f"seuil_changement_{n}"
        res[col] = np.where(res[f"age_bio_{n}"].notna() & ~crp_hi.to_numpy(), spec["seuil_ans"], np.nan)
    return res


def main(input_path: str, output_path: str | None = None, model_path: str | None = None,
         uncertainty: bool = False, thresholds_path: str | None = None) -> Path:
    model = load_model(model_path or DEFAULT_MODEL)
    df = pd.read_csv(input_path)
    res = score(df, model)
    if uncertainty:
        res = add_change_thresholds(res, df, thresholds_path or DEFAULT_THRESHOLDS)
        print("Seuils de changement significatif ajoutes (95e centile des ecarts observes sur des "
              "remesures reelles ; valables si CRP <= 10 mg/L aux deux bilans).")
    num = [c for c in res.columns if c.startswith(("age_bio_", "ecart_"))]
    res[num] = res[num].round(2)
    res["risque_deces_10ans"] = res["risque_deces_10ans"].round(4)
    out = Path(output_path) if output_path else Path(input_path).with_name(Path(input_path).stem + "_scores.csv")
    res.to_csv(out, index=False)
    n_ok = int((res["statut"] == "ok").sum())
    print(f"{len(res)} lignes, {n_ok} sans alerte. Scores : {out}")
    for w in model["warnings"][:1]:
        print(f"Attention : {w}")
    return out
