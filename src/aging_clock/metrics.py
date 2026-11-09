"""Metriques de validation : discrimination, association, calibration, bootstrap."""
from __future__ import annotations

import warnings

import numpy as np
from joblib import Parallel, delayed
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.utils import concordance_index


def harrell_c(time, event, risk) -> float:
    """C de Harrell : un risque predit plus eleve doit correspondre a un deces plus precoce."""
    return concordance_index(np.asarray(time), -np.asarray(risk), np.asarray(event))


def _bootstrap_chunk(df, stat_fn, seed, n):
    rng = np.random.default_rng(seed)
    size = len(df)
    return [stat_fn(df.iloc[rng.integers(0, size, size)]) for _ in range(n)]


def bootstrap(df: pd.DataFrame, stat_fn, n: int, seed: int, n_jobs: int = -1) -> pd.DataFrame:
    """Repliques bootstrap (re-echantillonnage des participants) d'un dict de statistiques.

    `stat_fn` doit etre picklable (fonction de module ou functools.partial).
    Reproductible : les graines des blocs derivent de `seed`.
    """
    n_chunks = min(n, 24)
    sizes = [n // n_chunks + (i < n % n_chunks) for i in range(n_chunks)]
    seeds = np.random.SeedSequence(seed).spawn(n_chunks)
    chunks = Parallel(n_jobs=n_jobs)(
        delayed(_bootstrap_chunk)(df, stat_fn, sd, k) for sd, k in zip(seeds, sizes))
    return pd.DataFrame([r for c in chunks for r in c])


def summarize(point: dict, reps: pd.DataFrame, alpha=0.05) -> pd.DataFrame:
    rows = []
    for k, v in point.items():
        lo, hi = np.nanquantile(reps[k], [alpha / 2, 1 - alpha / 2])
        rows.append({"statistique": k, "estimation": v, "ic95_bas": lo, "ic95_haut": hi})
    return pd.DataFrame(rows)


def cox_hr(df: pd.DataFrame, exposures: list[str], adjust: list[str],
           duration: str, event: str, standardize=True) -> pd.DataFrame:
    """HR (par ecart-type si standardize) des expositions, ajuste sur `adjust`."""
    data = df[exposures + adjust + [duration, event]].copy()
    sds = {}
    if standardize:
        for c in exposures:
            sds[c] = data[c].std()
            data[c] = (data[c] - data[c].mean()) / sds[c]
    cph = CoxPHFitter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cph.fit(data, duration_col=duration, event_col=event)
    s = cph.summary
    return pd.DataFrame({
        "exposition": exposures,
        "ecart_type": [sds.get(c, np.nan) for c in exposures],
        "HR": s.loc[exposures, "exp(coef)"].to_numpy(),
        "ic95_bas": s.loc[exposures, "exp(coef) lower 95%"].to_numpy(),
        "ic95_haut": s.loc[exposures, "exp(coef) upper 95%"].to_numpy(),
        "p": s.loc[exposures, "p"].to_numpy(),
    })


def km_risk_at(time, event, horizon) -> tuple[float, float, float]:
    kmf = KaplanMeierFitter().fit(np.asarray(time), np.asarray(event))
    s = float(kmf.survival_function_at_times(horizon).iloc[0])
    ci = kmf.confidence_interval_survival_function_
    ci_at = ci[ci.index <= horizon].iloc[-1]
    return 1 - s, 1 - float(ci_at.iloc[1]), 1 - float(ci_at.iloc[0])


def calibration(time, event, risk, horizon, groups=10) -> tuple[pd.DataFrame, dict]:
    """Calibration a horizon : deciles de risque predit vs risque observe (Kaplan-Meier)."""
    time, event, risk = map(np.asarray, (time, event, risk))
    bins = pd.qcut(risk, groups, labels=False, duplicates="drop")
    rows = []
    for g in np.unique(bins):
        m = bins == g
        obs, lo, hi = km_risk_at(time[m], event[m], horizon)
        rows.append({"groupe": int(g) + 1, "n": int(m.sum()), "predit": risk[m].mean(),
                     "observe": obs, "observe_ic95_bas": lo, "observe_ic95_haut": hi})
    table = pd.DataFrame(rows)

    obs_all, _, _ = km_risk_at(time, event, horizon)
    # Pente de calibration : coefficient du log(-log(1-p)) dans un Cox de validation
    cll = np.log(-np.log(np.clip(1 - risk, 1e-12, 1 - 1e-12)))
    cph = CoxPHFitter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cph.fit(pd.DataFrame({"cll": cll, "T": time, "E": event}), "T", "E")
    summary = {
        "risque_predit_moyen": float(risk.mean()),
        "risque_observe_km": obs_all,
        "ratio_observe_predit": obs_all / float(risk.mean()),
        "pente_calibration": float(cph.params_["cll"]),
        "pente_ic95_bas": float(cph.confidence_intervals_.iloc[0, 0]),
        "pente_ic95_haut": float(cph.confidence_intervals_.iloc[0, 1]),
        "ecart_absolu_moyen_deciles": float(np.average(
            np.abs(table["predit"] - table["observe"]), weights=table["n"])),
    }
    return table, summary
