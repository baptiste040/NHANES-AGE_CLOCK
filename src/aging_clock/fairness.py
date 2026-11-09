"""Audit d'equite sur la validation 2007-2010 (point 5b).

Protocole et regles d'interpretation fixes avant execution : DECISIONS.md, 5b.
Distingue un defaut du modele dans un groupe (calibration, discrimination) d'une
difference reelle de risque de mortalite entre groupes (ecart d'age moyen different
mais bien calibre).
"""
from __future__ import annotations

import functools
import json

import numpy as np
import pandas as pd

from . import plots
from .cohort import DURATION, EVENT, build_cohort
from .config import ROOT, load_panel, load_study
from .metrics import bootstrap, calibration, harrell_c, km_risk_at, summarize
from .nhanes import build_harmonized
from .validate import fit_clock

RACE = {1: "Mexicain-américain", 2: "Autre hispanique", 3: "Blanc non hispanique",
        4: "Noir non hispanique", 5: "Autre / multiethnique"}
EDUC = {1: "< secondaire", 2: "< secondaire", 3: "Secondaire (diplôme)",
        4: "Supérieur partiel", 5: "Diplôme universitaire"}
MIN_DEATHS = 50
OE_TOL, SLOPE_RANGE = 0.20, (0.80, 1.20)


def add_groups(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["Sexe"] = d["sex"].map({1: "Homme", 2: "Femme"})
    d["Groupe ethnique"] = d["race_eth"].map(RACE)
    d["Âge"] = pd.cut(d["age"], [19, 39, 59, 79], labels=["20-39", "40-59", "60-79"]).astype(str)
    d["Revenu / seuil de pauvreté"] = pd.cut(
        d["income_pir"], [-np.inf, 1.3, 3.5, np.inf], right=False,
        labels=["< 1,3", "1,3-3,5", "≥ 3,5"]).astype(object)
    d["Niveau d'études"] = d["education"].map(EDUC)
    return d


AXES = {"Sexe": ["Homme", "Femme"],
        "Groupe ethnique": list(dict.fromkeys(RACE.values())),
        "Âge": ["20-39", "40-59", "60-79"],
        "Revenu / seuil de pauvreté": ["< 1,3", "1,3-3,5", "≥ 3,5"],
        "Niveau d'études": ["< secondaire", "Secondaire (diplôme)", "Supérieur partiel",
                            "Diplôme universitaire"]}


def _c_stats(d: pd.DataFrame) -> dict:
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    c = harrell_c(t, e, d["risk_global"].to_numpy())
    c_ref = harrell_c(t, e, d["risk_ref"].to_numpy())
    return {"C": c, "gain_C": c - c_ref}


def group_row(axis, group, d, overall_gap_mean, n_boot, seed, horizon) -> dict:
    deaths = int(d[EVENT].sum())
    row = {"axe": axis, "groupe": group, "n": len(d), "deces": deaths}
    summ = summarize(_c_stats(d), bootstrap(d[[DURATION, EVENT, "risk_global", "risk_ref"]],
                                             functools.partial(_c_stats), n_boot, seed)).set_index("statistique")
    for k in ("C", "gain_C"):
        row[k], row[f"{k}_bas"], row[f"{k}_haut"] = summ.loc[k, ["estimation", "ic95_bas", "ic95_haut"]]

    pred = d["risk_global"].mean()
    obs, lo, hi = km_risk_at(d[DURATION], d[EVENT], horizon)
    row |= {"predit_10ans": pred, "observe_10ans": obs,
            "O_P": obs / pred, "O_P_bas": lo / pred, "O_P_haut": hi / pred}
    _, cal = calibration(d[DURATION], d[EVENT], d["risk_global"], horizon, groups=5)
    row |= {"pente": cal["pente_calibration"], "pente_bas": cal["pente_ic95_bas"],
            "pente_haut": cal["pente_ic95_haut"]}

    g = d["gap_global"]
    se = g.std() / np.sqrt(len(g))
    row |= {"ecart_moyen": g.mean(), "ecart_moyen_bas": g.mean() - 1.96 * se,
            "ecart_moyen_haut": g.mean() + 1.96 * se, "ecart_et": g.std(),
            "ecart_mediane": g.median(), "ecart_q1": g.quantile(0.25), "ecart_q3": g.quantile(0.75)}

    # --- Regle d'interpretation pre-enregistree
    calib_defect = ((row["O_P_bas"] > 1 or row["O_P_haut"] < 1) and abs(row["O_P"] - 1) > OE_TOL) or \
                   ((row["pente_bas"] > 1 or row["pente_haut"] < 1) and
                    not SLOPE_RANGE[0] <= row["pente"] <= SLOPE_RANGE[1])
    discr_defect = row["gain_C_bas"] <= 0 <= row["gain_C_haut"]
    gap_differs = not (row["ecart_moyen_bas"] <= overall_gap_mean <= row["ecart_moyen_haut"])
    if deaths < MIN_DEATHS:
        verdict = "effectif insuffisant"
    elif calib_defect or discr_defect:
        verdict = "défaut du modèle (" + " + ".join(
            x for x, f in [("calibration", calib_defect), ("discrimination", discr_defect)] if f) + ")"
    elif gap_differs:
        verdict = "différence de risque réelle (bien calibré)"
    else:
        verdict = "pas de différence"
    row |= {"defaut_calibration": calib_defect, "defaut_discrimination": discr_defect,
            "ecart_different_global": gap_differs, "verdict": verdict}
    return row


def run(n_boot: int | None = None) -> dict:
    study = load_study()
    panel = load_panel("checkup_standard")
    out = ROOT / study["paths"]["reports"] / panel.name / "equite"
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
    clock = fit_clock(dev, panel, study, meta_main["penalizer"])        # identique au point 4
    V = add_groups(val.join(clock.predict(val)))
    overall = V["gap_global"].mean()

    rows = []
    for axis, groups in AXES.items():
        for g in groups:
            d = V[V[axis] == g]
            if len(d):
                rows.append(group_row(axis, g, d, overall, n_boot, seed, horizon))
    table = pd.DataFrame(rows)
    table.to_csv(out / "equite.csv", index=False)

    missing = {a: int(V[a].isna().sum()) for a in AXES}
    systems = [s for s in clock.score_names if s != "global"]
    sys_gaps = pd.concat([V.groupby(a)[[f"gap_{s}" for s in systems]].mean().assign(axe=a)
                          for a in AXES]).round(2)
    sys_gaps.to_csv(out / "ecarts_par_systeme.csv")

    plots.group_intervals(table, "O_P", "O_P_bas", "O_P_haut", 1.0, (1 - OE_TOL, 1 + OE_TOL),
                          "Rapport observé / prédit à 10 ans (IC 95 %)", out / "calibration_groupes.png")
    plots.group_intervals(table, "ecart_moyen", "ecart_moyen_bas", "ecart_moyen_haut", overall, None,
                          "Écart d'âge moyen, ans (IC 95 %) — trait : moyenne de la validation",
                          out / "ecart_groupes.png")
    meta = {"n_validation": len(V), "ecart_moyen_validation": overall, "manquants_par_axe": missing,
            "bootstrap": n_boot, "seed": seed}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"table": table, "meta": meta, "systemes": sys_gaps, "dossier": out}


def write_report(out) -> None:
    from .report import _md
    t = pd.read_csv(out / "equite.csv")
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    f2 = lambda v, a, b, f=".2f": f"{v:{f}} [{a:{f}}; {b:{f}}]"  # noqa: E731
    tab = pd.DataFrame({
        "Axe": t["axe"], "Groupe": t["groupe"], "n": t["n"], "Décès": t["deces"],
        "C": [f2(*r, f=".3f") for r in t[["C", "C_bas", "C_haut"]].to_numpy()],
        "Gain de C vs âge + sexe": [f2(*r, f="+.3f") for r in t[["gain_C", "gain_C_bas", "gain_C_haut"]].to_numpy()],
        "Obs. / prédit 10 ans": [f2(*r) for r in t[["O_P", "O_P_bas", "O_P_haut"]].to_numpy()],
        "Pente": [f2(*r) for r in t[["pente", "pente_bas", "pente_haut"]].to_numpy()],
        "Écart moyen (ans)": [f2(*r, f="+.1f") for r in t[["ecart_moyen", "ecart_moyen_bas", "ecart_moyen_haut"]].to_numpy()],
        "Écart médian [Q1; Q3]": [f"{m:+.1f} [{a:+.1f}; {b:+.1f}]" for m, a, b in t[["ecart_mediane", "ecart_q1", "ecart_q3"]].to_numpy()],
        "Verdict (règle pré-enregistrée)": t["verdict"],
    })
    miss = ", ".join(f"{k} : {v}" for k, v in meta["manquants_par_axe"].items() if v)
    text = f"""# Audit d'équité — validation 2007-2010

Modèle gelé (point 4), score global, analyses non pondérées. Protocole et règle d'interprétation
fixés avant exécution (`DECISIONS.md`, 5b). n = {meta['n_validation']} ; écart d'âge moyen de la
validation : {meta['ecart_moyen_validation']:+.2f} an(s). Valeurs manquantes par axe : {miss}.

**Règle** — défaut de calibration : IC du rapport observé/prédit (O/P) excluant 1 et
|O/P − 1| > 0,20, ou IC de la pente excluant 1 et pente hors [0,80 ; 1,20] ; défaut de
discrimination : IC du gain de C incluant 0 ; différence de risque réelle : écart moyen différent
de la moyenne de validation sans défaut du modèle ; < 50 décès : effectif insuffisant.

{_md(tab)}

![O/P](calibration_groupes.png)

![Écart](ecart_groupes.png)

Écarts moyens par système et par groupe : `ecarts_par_systeme.csv`.
Interprétation (écrite après lecture des résultats) : `INTERPRETATION.md`.
"""
    (out / "EQUITE.md").write_text(text, encoding="utf-8")
