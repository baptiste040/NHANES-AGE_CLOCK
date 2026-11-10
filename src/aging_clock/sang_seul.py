"""Piste « suivi », etape 0 : variante « sang seul » du modele (sans tension, pouls, IMC, tour de
taille). Protocole : DECISIONS.md (pre-enregistrement du 2026-11-10).

Analyse principale : memes personnes que le modele complet (developpement et validation),
penalisation figee a 0 (valeur choisie pour le modele complet), memes transformations.
Analyse secondaire : cohorte propre au panel « sang seul » (cas complets sur ses 19 marqueurs).

    predictions()  -> validation croisee « un cycle retire » sur 1999-2006 (prediction)
    run()          -> validation 2007-2010, comparaison appariee avec le modele complet
"""
from __future__ import annotations

import functools
import json

import numpy as np
import pandas as pd

from .cohort import DURATION, EVENT, build_cohort
from .config import ROOT, load_panel, load_study
from .metrics import bootstrap, calibration, cox_hr, harrell_c, summarize
from .model import BioAgeClock
from .nhanes import build_harmonized
from .validate import fit_clock

PENALIZER = 0.0
FULL, BLOOD = "checkup_standard", "checkup_sang_seul"
SCORES = ["global", "cardiovasculaire", "metabolique", "renal", "hepatique",
          "inflammatoire_hematologique"]
OUT = ROOT / "reports" / BLOOD


def _data():
    study = load_study()
    h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    full_co, _ = build_cohort(h, load_panel(FULL), study)
    blood_co, flow = build_cohort(h, load_panel(BLOOD), study)
    return study, full_co, blood_co, flow


def _split(study, co):
    dev = co[co["cycle"].isin(study["cycles"]["development"])].reset_index(drop=True)
    val = co[co["cycle"].isin(study["cycles"]["validation"])].reset_index(drop=True)
    return dev, val


def predictions() -> dict:
    """Prediction pre-enregistree : CV « un cycle retire » sur le developpement (memes personnes)."""
    OUT.mkdir(parents=True, exist_ok=True)
    study, full_co, _, _ = _data()
    dev, _ = _split(study, full_co)
    cfg = {**study, "model": {**study["model"], "penalizer": PENALIZER}}
    rows = []
    for cycle in sorted(dev["cycle"].unique()):
        train, test = dev[dev["cycle"] != cycle], dev[dev["cycle"] == cycle]
        pf = BioAgeClock(load_panel(FULL), cfg).fit(train).predict(test)
        pb = BioAgeClock(load_panel(BLOOD), cfg).fit(train).predict(test)
        for s in SCORES:
            cf = harrell_c(test[DURATION], test[EVENT], pf[f"risk_{s}"])
            cb = harrell_c(test[DURATION], test[EVENT], pb[f"risk_{s}"])
            rows.append({"cycle_retire": cycle, "score": s, "C_complet": cf, "C_sang": cb,
                         "dC_sang_moins_complet": cb - cf})
    cv = pd.DataFrame(rows)
    cv.to_csv(OUT / "prediction_cv_developpement.csv", index=False)
    pred = cv.groupby("score")["dC_sang_moins_complet"].mean().to_dict()
    (OUT / "prediction.json").write_text(json.dumps(pred, indent=2), encoding="utf-8")
    return pred


def _paired(d: pd.DataFrame) -> dict:
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    out = {"C_ref": harrell_c(t, e, d["risk_ref"])}
    for s in SCORES:
        cf, cb = harrell_c(t, e, d[f"f_risk_{s}"]), harrell_c(t, e, d[f"b_risk_{s}"])
        out |= {f"C_complet_{s}": cf, f"C_sang_{s}": cb, f"gain_sang_{s}": cb - out["C_ref"],
                f"dC_sang_moins_complet_{s}": cb - cf}
    return out


def _evaluate(dev, val, study, label, n_boot, seed, horizon):
    full = fit_clock(dev, load_panel(FULL), study, PENALIZER)
    blood = fit_clock(dev, load_panel(BLOOD), study, PENALIZER)
    pf, pb = full.predict(val), blood.predict(val)
    d = val.copy()
    d["risk_ref"] = pf["risk_ref"]
    d["female"] = (d["sex"] == 2).astype(float)
    for s in SCORES:
        d[f"f_risk_{s}"], d[f"b_risk_{s}"] = pf[f"risk_{s}"], pb[f"risk_{s}"]
        d[f"b_gap_{s}"] = pb[f"gap_{s}"]
    cols = [DURATION, EVENT, "risk_ref"] + [f"{p}_risk_{s}" for p in "fb" for s in SCORES]
    point = _paired(d)
    reps = bootstrap(d[cols], functools.partial(_paired), n_boot, seed)
    summ = summarize(point, reps).set_index("statistique")
    rows = []
    for s in SCORES:
        table, cal = calibration(d[DURATION], d[EVENT], d[f"b_risk_{s}"], horizon)
        hr = cox_hr(d, [f"b_gap_{s}"], ["age", "female"], DURATION, EVENT).iloc[0]
        k = f"dC_sang_moins_complet_{s}"
        rows.append({"analyse": label, "score": s, "n": len(d), "deces": int(d[EVENT].sum()),
                     "C_sang": summ.loc[f"C_sang_{s}", "estimation"],
                     "C_sang_ic95": (summ.loc[f"C_sang_{s}", "ic95_bas"], summ.loc[f"C_sang_{s}", "ic95_haut"]),
                     "gain_vs_age_sexe": summ.loc[f"gain_sang_{s}", "estimation"],
                     "gain_ic95": (summ.loc[f"gain_sang_{s}", "ic95_bas"], summ.loc[f"gain_sang_{s}", "ic95_haut"]),
                     "C_complet": summ.loc[f"C_complet_{s}", "estimation"],
                     "dC_sang_moins_complet": summ.loc[k, "estimation"],
                     "dC_ic95": (summ.loc[k, "ic95_bas"], summ.loc[k, "ic95_haut"]),
                     "p_bootstrap": 2 * min((reps[k] <= 0).mean(), (reps[k] >= 0).mean()),
                     "HR_par_ET": hr["HR"], "HR_ic95": (hr["ic95_bas"], hr["ic95_haut"]),
                     "ET_ecart_ans": hr["ecart_type"],
                     "obs_sur_predit": cal["ratio_observe_predit"], "pente": cal["pente_calibration"],
                     "pente_ic95": (cal["pente_ic95_bas"], cal["pente_ic95_haut"]),
                     "C_ref": summ.loc["C_ref", "estimation"]})
    return rows, blood


def run(n_boot: int | None = None) -> dict:
    study, full_co, blood_co, flow = _data()
    vcfg = study["validation"]
    n_boot = n_boot or vcfg["bootstrap"]
    seed, horizon = vcfg["seed"], study["model"]["horizon_months"]
    dev, val = _split(study, full_co)
    rows, clock = _evaluate(dev, val, study, "principale (memes personnes)", n_boot, seed, horizon)
    dev2, val2 = _split(study, blood_co)
    # Secondaire : cohorte propre au panel sang seul, sans comparaison appariee (le modele complet
    # n'y est pas calculable pour les personnes sans mesures physiques).
    b2 = fit_clock(dev2, load_panel(BLOOD), study, PENALIZER)
    p2 = b2.predict(val2)
    sec = []
    for s in SCORES:
        _, cal = calibration(val2[DURATION], val2[EVENT], p2[f"risk_{s}"], horizon)
        sec.append({"analyse": "secondaire (cohorte propre)", "score": s, "n": len(val2),
                    "deces": int(val2[EVENT].sum()),
                    "C_sang": harrell_c(val2[DURATION], val2[EVENT], p2[f"risk_{s}"]),
                    "C_ref": harrell_c(val2[DURATION], val2[EVENT], p2["risk_ref"]),
                    "obs_sur_predit": cal["ratio_observe_predit"], "pente": cal["pente_calibration"]})
    pd.DataFrame(rows + sec).to_csv(OUT / "validation_sang_seul.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(OUT / "flux_cohorte_propre.csv", index=False)
    clock.hazard_ratios().to_csv(OUT / "coefficients.csv", index=False)
    meta = {"penalizer": PENALIZER, "bootstrap": n_boot, "seed": seed,
            "n_dev_principale": len(dev), "n_val_principale": len(val),
            "n_dev_propre": len(dev2), "n_val_propre": len(val2),
            "panel_sha256": load_panel(BLOOD).sha256}
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"dossier": OUT, **meta}
