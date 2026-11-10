"""Benchmark PhenoAge sur la validation 2007-2010 (point 5a).

Trois scores, memes participants :
  global   : score principal (panel checkup_standard, gele au point 4) ;
  pheno9   : PhenoAge reentraine avec la methode du score principal (9 marqueurs) ;
  pheno_pub: PhenoAge publie (Levine 2018), sans reentrainement.
Decomposition : pheno_pub -> pheno9 = effet de la methode a variables egales ;
pheno9 -> global = effet des variables supplementaires.
"""
from __future__ import annotations

import functools
import json

import numpy as np
import pandas as pd

from . import phenoage as pa
from . import plots
from .cohort import DURATION, EVENT, build_cohort, has_prevalent_condition
from .config import ROOT, load_panel, load_study
from .metrics import bootstrap, calibration, cox_hr, harrell_c, summarize
from .nhanes import build_harmonized
from .validate import fit_clock, select_penalizer

SCORES = {"global": "Score global (panel complet)",
          "pheno9": "PhenoAge réentraîné (9 marqueurs, notre méthode)",
          "pheno_pub": "PhenoAge publié (Levine 2018)"}
PAIRS = [("global", "pheno_pub"), ("global", "pheno9"), ("pheno9", "pheno_pub")]


def paired_stats(d: pd.DataFrame) -> dict:
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    c = {s: harrell_c(t, e, d[f"risk_{s}"].to_numpy()) for s in ["ref", *SCORES]}
    out = {f"C_{s}": v for s, v in c.items()}
    out |= {f"dC_{s}_vs_ref": c[s] - c["ref"] for s in SCORES}
    out |= {f"dC_{a}_moins_{b}": c[a] - c[b] for a, b in PAIRS}
    return out


def score_table(d: pd.DataFrame, n_boot: int, seed: int, horizon: int) -> tuple[pd.DataFrame, ...]:
    cols = [DURATION, EVENT, "risk_ref"] + [f"risk_{s}" for s in SCORES]
    point = paired_stats(d)
    reps = bootstrap(d[cols], functools.partial(paired_stats), n_boot, seed)
    summ = summarize(point, reps).set_index("statistique")

    hr = pd.concat([cox_hr(d, [f"accel_{s}"], ["age", "female"], DURATION, EVENT) for s in SCORES],
                   ignore_index=True)
    rows, cal_tables = [], {}
    for s in SCORES:
        table, cal = calibration(d[DURATION], d[EVENT], d[f"risk_{s}"], horizon)
        cal_tables[SCORES[s]] = table
        h = hr[hr["exposition"] == f"accel_{s}"].iloc[0]
        rows.append({
            "score": SCORES[s],
            "C": summ.loc[f"C_{s}", "estimation"],
            "C_ic95": f"[{summ.loc[f'C_{s}', 'ic95_bas']:.3f}; {summ.loc[f'C_{s}', 'ic95_haut']:.3f}]",
            "gain_C_vs_age_sexe": summ.loc[f"dC_{s}_vs_ref", "estimation"],
            "gain_ic95": f"[{summ.loc[f'dC_{s}_vs_ref', 'ic95_bas']:.3f}; {summ.loc[f'dC_{s}_vs_ref', 'ic95_haut']:.3f}]",
            "HR_par_ET_acceleration": h["HR"],
            "HR_ic95": f"[{h['ic95_bas']:.2f}; {h['ic95_haut']:.2f}]",
            "ET_acceleration_ans": h["ecart_type"],
            "obs_sur_predit_10ans": cal["ratio_observe_predit"],
            "pente_calibration": cal["pente_calibration"],
            "pente_ic95": f"[{cal['pente_ic95_bas']:.2f}; {cal['pente_ic95_haut']:.2f}]",
        })
    diffs = pd.DataFrame([{
        "comparaison": f"{SCORES[a]} − {SCORES[b]}",
        "difference_C": summ.loc[f"dC_{a}_moins_{b}", "estimation"],
        "ic95_bas": summ.loc[f"dC_{a}_moins_{b}", "ic95_bas"],
        "ic95_haut": summ.loc[f"dC_{a}_moins_{b}", "ic95_haut"],
        "p_bootstrap_bilateral": 2 * min((reps[f"dC_{a}_moins_{b}"] <= 0).mean(),
                                         (reps[f"dC_{a}_moins_{b}"] >= 0).mean()),
    } for a, b in PAIRS])
    ref = summ.loc["C_ref"]
    return pd.DataFrame(rows), diffs, cal_tables, ref


def run(n_boot: int | None = None) -> dict:
    study = load_study()
    panel, p9 = load_panel("checkup_standard"), load_panel("phenoage9")
    out = ROOT / study["paths"]["reports"] / panel.name / "benchmark_phenoage"
    out.mkdir(parents=True, exist_ok=True)
    n_boot = n_boot or study["validation"]["bootstrap"]
    seed, horizon = study["validation"]["seed"], study["model"]["horizon_months"]
    dev_c, val_c = study["cycles"]["development"], study["cycles"]["validation"]

    harmonized = build_harmonized(dev_c + val_c,
                                  cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    cohort, _ = build_cohort(harmonized, panel, study)
    dev = cohort[cohort["cycle"].isin(dev_c)].reset_index(drop=True)
    val = cohort[cohort["cycle"].isin(val_c)].reset_index(drop=True)

    meta_main = json.loads((out.parent / "meta.json").read_text(encoding="utf-8"))
    main = fit_clock(dev, panel, study, meta_main["penalizer"])        # identique au point 4
    pen9, cv9 = select_penalizer(dev, p9, study)
    cv9.to_csv(out / "penalisation_cv_pheno9.csv", index=False)
    clock9 = fit_clock(dev, p9, study, pen9)

    m, k = main.predict(val), clock9.predict(val)
    accel_coef = pa.fit_acceleration(dev)
    V = val.assign(
        female=(val["sex"] == 2).astype(float),
        risk_ref=m["risk_ref"], risk_global=m["risk_global"], accel_global=m["gap_global"],
        risk_pheno9=k["risk_global"], accel_pheno9=k["gap_global"],
        risk_pheno_pub=pa.mortality_score(val), phenoage_pub=pa.phenoage(val),
        accel_pheno_pub=pa.acceleration(val, accel_coef),
    )

    results = {}
    for label, d in [("validation", V),
                     ("sans_antecedent", V[~has_prevalent_condition(V, study["sensitivity"]["prevalent_conditions"])])]:
        table, diffs, cal_tables, ref = score_table(d, n_boot, seed, horizon)
        table.insert(1, "n", len(d))
        table.insert(2, "deces", int(d[EVENT].sum()))
        table.to_csv(out / f"scores_{label}.csv", index=False)
        diffs.to_csv(out / f"differences_C_{label}.csv", index=False)
        if label == "validation":
            plots.calibration_grid(cal_tables, horizon // 12, out / "calibration.png")
        results[label] = {"scores": table, "differences": diffs,
                          "C_ref": (ref["estimation"], ref["ic95_bas"], ref["ic95_haut"])}

    meta = {"penalizer_pheno9": pen9, "acceleration_pheno_pub": dict(zip(["intercept", "pente"], accel_coef)),
            "phenoage_pub_moyenne_validation": float(V["phenoage_pub"].mean()),
            "age_moyen_validation": float(V["age"].mean()),
            "corr_accel_global_pheno_pub": float(V[["accel_global", "accel_pheno_pub"]].corr().iat[0, 1]),
            "bootstrap": n_boot, "seed": seed,
            "C_ref": {k_: list(v["C_ref"]) for k_, v in results.items()}}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return results | {"meta": meta, "dossier": out}


def write_report(out) -> None:
    from .report import _md
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    parts = ["""# Benchmark PhenoAge — validation 2007-2010

Panel et modèle principaux gelés (point 4) ; protocole écrit avant exécution (`DECISIONS.md`, 5a).
Trois scores sur les mêmes participants. Différences de C par bootstrap **apparié**
(mêmes tirages pour les scores comparés).

- **PhenoAge publié**, sans réentraînement. Sources :
  - poids des marqueurs : Levine et al. 2018, *Aging* 10(4):573-591, tableau 1
    ([doi:10.18632/aging.101414](https://doi.org/10.18632/aging.101414)) ;
  - risque à 10 ans : M = 1 − exp(−1,51714·exp(xb)/0,0076927) (correction de Liu et al.,
    *PLoS Med* 2019, [doi:10.1371/journal.pmed.1002760](https://doi.org/10.1371/journal.pmed.1002760)) ;
  - conversion en années : supplément 1 de Levine et al. 2018 (lu le 2026-11-09) :
    PhenoAge = 141,50225 + ln(−0,00553·ln(1 − M))/0,090165.
  - La correction de Liu 2019 imprime 141,50 et 0,09165 (probable faute de frappe), constantes
    utilisées dans une première exécution (`DECISIONS.md`). Passer de l'une à l'autre est une
    transformation affine de PhenoAge : **seules les valeurs en années changent** (PhenoAge moyen,
    accélération en années et son écart-type). Le C, le HR par écart-type d'accélération et la
    calibration (calculée sur M, avant conversion) sont identiques.
- **PhenoAge réentraîné** : ses 9 marqueurs, méthode du score principal (Cox âge + sexe,
  transformations du panel, pénalisation par CV sur 1999-2006).
- Accélération : écart d'âge pour nos scores ; résidu PhenoAge ~ âge (régression estimée sur le
  développement) pour PhenoAge publié. HR par écart-type, ajusté âge + sexe.
- Calibration à 10 ans : M (risque à 10 ans) pour PhenoAge publié ; risque à 10 ans du Cox pour
  les versions réentraînées.
- Limite : glycémie non à jeun dans NHANES ici ; PhenoAge a été conçu sur des sujets à jeun.
"""]
    titles = {"validation": "Validation complète", "sans_antecedent": "Sans antécédent déclaré"}
    for label, title in titles.items():
        sc = pd.read_csv(out / f"scores_{label}.csv")
        df = pd.read_csv(out / f"differences_C_{label}.csv")
        c_ref = meta["C_ref"][label]
        sc_t = pd.DataFrame({
            "Score": sc["score"], "n": sc["n"], "Décès": sc["deces"],
            "C (IC95)": [f"{c:.3f} {ci}" for c, ci in zip(sc["C"], sc["C_ic95"])],
            "Gain de C vs âge + sexe": [f"{g:+.3f} {ci}" for g, ci in zip(sc["gain_C_vs_age_sexe"], sc["gain_ic95"])],
            "HR / ET d'accélération": [f"{h:.2f} {ci}" for h, ci in zip(sc["HR_par_ET_acceleration"], sc["HR_ic95"])],
            "Obs./prédit 10 ans": sc["obs_sur_predit_10ans"].map("{:.2f}".format),
            "Pente": [f"{p:.2f} {ci}" for p, ci in zip(sc["pente_calibration"], sc["pente_ic95"])],
        })
        df_t = pd.DataFrame({
            "Comparaison": df["comparaison"],
            "Différence de C (IC95, apparié)": [f"{d:+.4f} [{a:+.4f}; {b:+.4f}]" for d, a, b in
                                               zip(df["difference_C"], df["ic95_bas"], df["ic95_haut"])],
            "p bootstrap": df["p_bootstrap_bilateral"].map(lambda p: "< 0,001" if p < 0.001 else f"{p:.3f}"),
        })
        parts.append(f"""## {title}

C de référence (Cox âge + sexe) : {c_ref[0]:.3f} [{c_ref[1]:.3f}; {c_ref[2]:.3f}].

{_md(sc_t)}

{_md(df_t)}
""")
    parts.append(f"""## Notes

- PhenoAge publié moyen en validation : {meta['phenoage_pub_moyenne_validation']:.1f} ans pour un âge moyen de {meta['age_moyen_validation']:.1f} ans (valeur en années : dépend des constantes de conversion).
- Corrélation entre l'écart global et l'accélération PhenoAge : {meta['corr_accel_global_pheno_pub']:.2f}.
- Pénalisation retenue pour PhenoAge réentraîné (CV 1999-2006) : {meta['penalizer_pheno9']}.
- Bootstrap : {meta['bootstrap']} tirages appariés, graine {meta['seed']}.

![Calibration](calibration.png)
""")
    (out / "BENCHMARK.md").write_text("\n".join(parts), encoding="utf-8")
