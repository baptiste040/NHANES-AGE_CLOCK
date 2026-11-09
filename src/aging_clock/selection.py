"""Selection de variables par validation croisee « un cycle retire » sur le developpement.

Ne charge QUE les cycles de developpement : la validation ne peut pas intervenir.
Critere (pre-enregistre dans DECISIONS.md) : une option est retenue si
  a. gain de C moyen du modele du systeme >= seuil (0,003) ;
  b. gain > 0 sur au moins `min_folds` cycles retires ;
  c. gain de C moyen du modele global >= 0.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pandas as pd

from .cohort import DURATION, EVENT, apply_panel_ranges, build_cohort
from .config import ROOT, Panel, load_panel, load_study
from .metrics import harrell_c
from .model import BioAgeClock
from .nhanes import build_harmonized


def with_variables(panel: Panel, add: list[str]) -> Panel:
    variables = {k: (dataclasses.replace(v, in_model=True) if k in add else v)
                 for k, v in panel.variables.items()}
    return dataclasses.replace(panel, variables=variables)


def missingness(dev_cohort: pd.DataFrame, harmonized: pd.DataFrame, panel: Panel,
                candidates: list[str]) -> pd.DataFrame:
    """Part de valeurs manquantes (ou hors plage) des candidats dans la cohorte de developpement."""
    h, _ = apply_panel_ranges(harmonized, panel)
    keyed = h.set_index(["cycle", "SEQN"])
    idx = pd.MultiIndex.from_frame(dev_cohort[["cycle", "SEQN"]])
    rows = []
    for c in candidates:
        miss = keyed.loc[idx, c].isna()
        rows.append({"variable": c, "n_cohorte": len(miss), "manquants": int(miss.sum()),
                     "pct_manquants": 100 * miss.mean()})
    return pd.DataFrame(rows)


def cv_compare(cohort: pd.DataFrame, base: Panel, option: Panel, system: str,
               study: dict, penalizer: float) -> pd.DataFrame:
    cfg = {**study, "model": {**study["model"], "penalizer": penalizer}}
    rows = []
    for cycle in sorted(cohort["cycle"].unique()):
        train, test = cohort[cohort["cycle"] != cycle], cohort[cohort["cycle"] == cycle]
        row = {"cycle_retire": int(cycle), "n_test": len(test), "deces_test": int(test[EVENT].sum())}
        for label, panel in (("base", base), ("option", option)):
            pred = BioAgeClock(panel, cfg).fit(train).predict(test)
            for score in ("global", system):
                row[f"C_{score}_{label}"] = harrell_c(test[DURATION], test[EVENT], pred[f"risk_{score}"])
        row["gain_systeme"] = row[f"C_{system}_option"] - row[f"C_{system}_base"]
        row["gain_global"] = row["C_global_option"] - row["C_global_base"]
        rows.append(row)
    return pd.DataFrame(rows)


def decide(folds: pd.DataFrame, min_gain=0.003, min_folds=3) -> dict:
    a = folds["gain_systeme"].mean()
    b = int((folds["gain_systeme"] > 0).sum())
    c = folds["gain_global"].mean()
    return {"gain_systeme_moyen": a, "plis_positifs": b, "gain_global_moyen": c,
            "critere_a": a >= min_gain, "critere_b": b >= min_folds, "critere_c": c >= 0,
            "retenu": bool(a >= min_gain and b >= min_folds and c >= 0)}


def run(system: str, options: dict[str, list[str]], panel_name="checkup_standard",
        penalizer: float = 0.0, out_name: str | None = None) -> dict:
    study = load_study()
    base = load_panel(panel_name)
    dev_cycles = study["cycles"]["development"]
    harmonized = build_harmonized(dev_cycles, cache=ROOT / "data" / "processed" / "nhanes_dev.csv")
    candidates = sorted({c for vs in options.values() for c in vs})

    base_cohort, _ = build_cohort(harmonized, base, study)
    miss = missingness(base_cohort, harmonized, base, candidates)

    # Memes participants pour toutes les options : cas complets sur base + tous les candidats
    full_panel = with_variables(base, candidates)
    cohort, flow = build_cohort(harmonized, full_panel, study)

    results, summary = {}, []
    for name, add in options.items():
        folds = cv_compare(cohort, base, with_variables(base, add), system, study, penalizer)
        results[name] = folds
        summary.append({"option": name, **decide(folds)})

    out = ROOT / "reports" / "selection" / (out_name or system)
    out.mkdir(parents=True, exist_ok=True)
    miss.to_csv(out / "manquants.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(out / "flux.csv", index=False)
    for name, folds in results.items():
        folds.to_csv(out / f"plis_{name}.csv", index=False)
    summary = pd.DataFrame(summary)
    summary.to_csv(out / "decision.csv", index=False)
    return {"manquants": miss, "flux": flow, "plis": results, "decision": summary, "dossier": out}
