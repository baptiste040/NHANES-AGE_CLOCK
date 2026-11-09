"""Telechargement et harmonisation multi-cycles de NHANES + Linked Mortality Files.

Produit une table une-ligne-par-participant, toutes variables en unites
canoniques, sans aucun filtre de population (fait dans cohort.py).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import requests

from .config import ROOT, load_source

MORT_COLSPECS = [(0, 6), (14, 15), (15, 16), (16, 19), (42, 45), (45, 48)]
MORT_NAMES = ["SEQN", "ELIGSTAT", "MORTSTAT", "UCOD_LEADING", "PERMTH_INT", "PERMTH_EXM"]


def _per_cycle(value, year):
    """Resout une valeur eventuellement specifiee par cycle ({annee: v, default: v})."""
    if isinstance(value, dict):
        return value.get(year, value.get("default"))
    return value


def download(url: str, dest: Path) -> Path:
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"[telecharge] {dest.name} ({len(r.content) // 1024} Ko)")
    return dest


def _load_xpt(path: Path) -> pd.DataFrame:
    df = pd.read_sas(path, format="xport")
    df["SEQN"] = df["SEQN"].astype(int)
    return df.set_index("SEQN")


def load_mortality(path: Path) -> pd.DataFrame:
    df = pd.read_fwf(path, colspecs=MORT_COLSPECS, names=MORT_NAMES, na_values=["", "."])
    df["SEQN"] = df["SEQN"].astype(int)
    return df.set_index("SEQN")


def _extract(frames: dict, spec: dict, year: int) -> pd.Series:
    df = frames[spec["file"]]
    var = _per_cycle(spec["var"], year)
    if isinstance(var, list):
        block = df[var].astype(float)
        if spec.get("zero_is_missing"):
            block = block.where(block > 0)
        values = block.mean(axis=1) if spec.get("agg") == "mean" else block.iloc[:, 0]
    else:
        values = df[var].astype(float)

    calib = (spec.get("calibration") or {}).get(year)
    if calib is not None:
        slope, intercept = calib
        values = slope * values + intercept

    factor = _per_cycle(spec.get("factor", 1), year)
    return values * factor


def harmonize_cycle(year: int, source: dict, raw_dir: Path) -> pd.DataFrame:
    files = source["cycles"][year]
    frames = {}
    for logical, fname in files.items():
        url = source["base_url"].format(year=year, file=fname)
        frames[logical] = _load_xpt(download(url, raw_dir / f"{year}_{fname}.xpt"))

    out = pd.DataFrame(index=frames["DEMO"].index)
    for block in ("demographics", "variables", "conditions"):
        for name, spec in source[block].items():
            out[name] = _extract(frames, spec, year).reindex(out.index)

    for cond in source["conditions"]:
        out[cond] = (out[cond] == 1).astype(float).where(out[cond].isin([1, 2]))

    mort_url = source["mortality_url"].format(year=year, year_end=year + 1)
    mort = load_mortality(download(mort_url, raw_dir / Path(mort_url).name))
    out = out.join(mort, how="left")
    out["cycle"] = year
    return out.reset_index()


def build_harmonized(years: list[int], raw_dir: Path | None = None,
                     cache: Path | None = None) -> pd.DataFrame:
    raw_dir = raw_dir or ROOT / "data" / "raw"
    if cache is not None and cache.exists():
        df = pd.read_parquet(cache) if cache.suffix == ".parquet" else pd.read_csv(cache)
        if set(years) <= set(df["cycle"].unique()):
            return df[df["cycle"].isin(years)].reset_index(drop=True)

    source = load_source("nhanes")
    df = pd.concat([harmonize_cycle(y, source, raw_dir) for y in years], ignore_index=True)
    df["UCOD_LEADING"] = pd.to_numeric(df["UCOD_LEADING"], errors="coerce")
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache, index=False)
    return df


def egfr_ckd_epi_2021(creatinine_umol, age, sex):
    """DFG CKD-EPI 2021 (sans coefficient ethnique), mL/min/1.73m2."""
    scr = np.asarray(creatinine_umol, dtype=float) / 88.42
    female = np.asarray(sex) == 2
    kappa = np.where(female, 0.7, 0.9)
    alpha = np.where(female, -0.241, -0.302)
    ratio = scr / kappa
    return (142 * np.minimum(ratio, 1) ** alpha * np.maximum(ratio, 1) ** -1.200
            * 0.9938 ** np.asarray(age, dtype=float) * np.where(female, 1.012, 1.0))
