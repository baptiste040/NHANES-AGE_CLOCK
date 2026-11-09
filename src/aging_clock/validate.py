"""Validation temporelle (jalon 1).

Developpement 1999-2006 -> modeles figes -> evaluation sur 2007-2010 :
discrimination (C avec IC bootstrap, gain de C vs age + sexe), HR par
ecart-type de l'ecart d'age, calibration a 10 ans, independance des ecarts
par systeme, sensibilites (deces precoces, antecedents, causes de deces).
"""
from __future__ import annotations

import functools
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import leakage, plots
from .cohort import DURATION, EVENT, add_cause_events, build_cohort, has_prevalent_condition
from .config import ROOT, load_panel, load_study
from .metrics import bootstrap, calibration, cox_hr, harrell_c, summarize
from .model import GLOBAL, BioAgeClock
from .nhanes import build_harmonized


# --------------------------------------------------------------------- helpers
def discrimination_stats(d: pd.DataFrame, scores: list[str], event: str = EVENT) -> dict:
    t, e = d[DURATION].to_numpy(), d[event].to_numpy()
    c_ref = harrell_c(t, e, d["risk_ref"].to_numpy())
    out = {"C_ref": c_ref}
    for s in scores:
        c = harrell_c(t, e, d[f"risk_{s}"].to_numpy())
        out[f"C_{s}"] = c
        out[f"dC_{s}"] = c - c_ref
    return out


def evaluate(d: pd.DataFrame, scores: list[str], n_boot: int, seed: int,
             event: str = EVENT) -> pd.DataFrame:
    fn = functools.partial(discrimination_stats, scores=scores, event=event)
    point = fn(d)
    reps = bootstrap(d[[DURATION, event, "risk_ref"] + [f"risk_{s}" for s in scores]],
                     fn, n_boot, seed)
    return summarize(point, reps)


def gap_hrs(d: pd.DataFrame, scores: list[str], event: str = EVENT, include_sex=True) -> pd.DataFrame:
    adjust = ["age", "female"] if include_sex else ["age"]
    rows = [cox_hr(d, [f"gap_{s}"], adjust, DURATION, event) for s in scores]
    return pd.concat(rows, ignore_index=True)


def select_penalizer(dev: pd.DataFrame, panel, study) -> tuple[float, pd.DataFrame]:
    """Validation croisee « un cycle retire » sur le developpement uniquement."""
    rows = []
    for pen in study["model"]["penalizer_grid"]:
        cfg = {**study, "model": {**study["model"], "penalizer": pen}}
        for cycle in sorted(dev["cycle"].unique()):
            train, test = dev[dev["cycle"] != cycle], dev[dev["cycle"] == cycle]
            pred = BioAgeClock(panel, cfg).fit(train).predict(test)
            rows.append({"penalizer": pen, "cycle_retire": cycle,
                         "C_global": harrell_c(test[DURATION], test[EVENT], pred["risk_global"])})
    cv = pd.DataFrame(rows)
    best = cv.groupby("penalizer")["C_global"].mean().idxmax()
    return float(best), cv


def fit_clock(dev, panel, study, penalizer):
    cfg = {**study, "model": {**study["model"], "penalizer": penalizer}}
    return BioAgeClock(panel, cfg).fit(dev)


def with_predictions(df, clock):
    out = df.join(clock.predict(df))
    out["female"] = (out["sex"] == 2).astype(float)
    return out


def cohort_summary(parts: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, d in parts.items():
        rows.append({"echantillon": name, "n": len(d), "deces": int(d[EVENT].sum()),
                     "suivi_median_ans": d[DURATION].median() / 12,
                     "age_moyen": d["age"].mean(), "pct_femmes": 100 * (d["sex"] == 2).mean(),
                     "cycles": ", ".join(str(c) for c in sorted(d["cycle"].unique()))})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------ main
def run(panel_name: str = "checkup_standard", n_boot: int | None = None) -> Path:
    study = load_study()
    panel = load_panel(panel_name)
    out = ROOT / study["paths"]["reports"] / panel.name
    out.mkdir(parents=True, exist_ok=True)
    vcfg, scfg = study["validation"], study["sensitivity"]
    n_boot = n_boot or vcfg["bootstrap"]
    n_boot_s = min(n_boot, vcfg["bootstrap_sensitivity"])
    seed = vcfg["seed"]
    horizon = study["model"]["horizon_months"]
    dev_cycles, val_cycles = study["cycles"]["development"], study["cycles"]["validation"]

    harmonized = build_harmonized(dev_cycles + val_cycles,
                                  cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    cohort, flow = build_cohort(harmonized, panel, study)
    cohort = add_cause_events(cohort, scfg["cause_groups"])
    dev = cohort[cohort["cycle"].isin(dev_cycles)].reset_index(drop=True)
    val = cohort[cohort["cycle"].isin(val_cycles)].reset_index(drop=True)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(out / "flux.csv", index=False)
    cohort_summary({"developpement": dev, "validation": val}).to_csv(
        out / "echantillons.csv", index=False)

    # --- Penalisation (developpement uniquement) puis modele fige
    if study["model"]["penalizer"] == "cv":
        penalizer, cv = select_penalizer(dev, panel, study)
        cv.to_csv(out / "penalisation_cv.csv", index=False)
    else:
        penalizer = float(study["model"]["penalizer"])
    clock = fit_clock(dev, panel, study, penalizer)
    scores = clock.score_names
    systems = [s for s in scores if s != GLOBAL]
    clock.hazard_ratios().to_csv(out / "coefficients.csv", index=False)
    V = with_predictions(val, clock)

    # --- Discrimination
    disc = evaluate(V, scores, n_boot, seed)
    disc.to_csv(out / "discrimination.csv", index=False)

    # --- HR par ecart-type de l'ecart d'age (ajuste age + sexe)
    hrs = gap_hrs(V, scores, include_sex=panel.include_sex)
    hrs.to_csv(out / "hr_par_ecart_type.csv", index=False)
    plots.forest(hrs, "exposition", out / "hr_par_ecart_type.png",
                 "Mortalité toutes causes, par écart-type d'écart d'âge (validation)",
                 "HR par écart-type (ajusté âge et sexe)")

    # --- Calibration a 10 ans
    cal_tables, cal_rows = {}, []
    for s in scores:
        table, summ = calibration(V[DURATION], V[EVENT], V[f"risk_{s}"], horizon,
                                  vcfg["calibration_groups"])
        cal_tables[s] = table
        cal_rows.append({"score": s, **summ})
        table.assign(score=s).to_csv(out / f"calibration_deciles_{s}.csv", index=False)
    cal = pd.DataFrame(cal_rows)
    cal.to_csv(out / "calibration.csv", index=False)
    plots.calibration_grid(cal_tables, horizon // 12, out / "calibration.png")

    # --- Independance des ecarts par systeme
    if systems:
        gap_cols = [f"gap_{s}" for s in systems]
        spear = V[gap_cols].corr(method="spearman")
        spear.to_csv(out / "independance_spearman.csv")
        plots.correlation_heatmap(spear, out / "independance_spearman.png",
                                  "Corrélations des écarts d'âge par système (validation)")
        joint = cox_hr(V, gap_cols, ["age", "female"], DURATION, EVENT)
        joint.to_csv(out / "independance_cox.csv", index=False)
        plots.forest(joint, "exposition", out / "independance_cox.png",
                     "Écarts par système ajustés mutuellement (validation)",
                     "HR par écart-type (ajusté âge, sexe et autres systèmes)")

    # --- Sensibilites
    sens_rows = []

    def record(scenario, model_label, d, event=EVENT):
        ev = evaluate(d, scores, n_boot_s, seed, event=event).set_index("statistique")
        hr = gap_hrs(d, scores, event=event, include_sex=panel.include_sex).set_index("exposition")
        for s in scores:
            sens_rows.append({
                "scenario": scenario, "modele": model_label, "score": s,
                "n": len(d), "deces": int(d[event].sum()),
                "C": ev.loc[f"C_{s}", "estimation"],
                "C_ic95": f"[{ev.loc[f'C_{s}', 'ic95_bas']:.3f}; {ev.loc[f'C_{s}', 'ic95_haut']:.3f}]",
                "dC": ev.loc[f"dC_{s}", "estimation"],
                "dC_ic95": f"[{ev.loc[f'dC_{s}', 'ic95_bas']:.3f}; {ev.loc[f'dC_{s}', 'ic95_haut']:.3f}]",
                "HR_par_ET": hr.loc[f"gap_{s}", "HR"],
                "HR_ic95": f"[{hr.loc[f'gap_{s}', 'ic95_bas']:.2f}; {hr.loc[f'gap_{s}', 'ic95_haut']:.2f}]",
            })

    record("principal", "fige", V)

    early = scfg["early_death_months"]
    not_early = lambda d: d[~((d[EVENT] == 1) & (d[DURATION] < early))]  # noqa: E731
    healthy = lambda d: d[~has_prevalent_condition(d, scfg["prevalent_conditions"])]  # noqa: E731
    for scenario, filt in [(f"1. sans deces < {early} mois", not_early),
                           ("2. sans antecedent declare", healthy)]:
        record(scenario, "fige", filt(V))
        refit = fit_clock(filt(dev), panel, study, penalizer)
        record(scenario, "re-entraine", with_predictions(filt(val), refit))

    for cause in scfg["cause_groups"]:
        record(f"4. deces {cause} (cause specifique)", "fige", V, event=f"event_{cause}")

    sens = pd.DataFrame(sens_rows)
    sens.to_csv(out / "sensibilites.csv", index=False)

    leakage.run(harmonized, study, panel.name, penalizer).to_csv(
        out / "effet_correction_fuite.csv", index=False)

    meta = {"panel": panel.name, "panel_sha256": panel.sha256, "penalizer": penalizer,
            "bootstrap": n_boot, "bootstrap_sensibilites": n_boot_s, "seed": seed,
            "cycles_developpement": dev_cycles, "cycles_validation": val_cycles,
            "ages_bio_hors_grille_validation": {s: int(V[f"clipped_{s}"].sum()) for s in scores}}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return out
