"""Validation secondaire 2015-2018 (point 6) : versions brute et harmonisee, horizon 3 ans.

Protocole : DECISIONS.md, point 6. Modele gele (point 4) ; analyse descriptive.
"""
from __future__ import annotations

import functools
import json

import numpy as np
import pandas as pd
import yaml

from .cohort import DURATION, EVENT, build_cohort
from .config import CONFIG_DIR, ROOT, load_panel, load_study
from .harmonisation import apply_crosswalk, quantile_map
from .metrics import bootstrap, calibration, cox_hr, harrell_c, km_risk_at, summarize
from .nhanes import _load_xpt, build_harmonized, download
from .validate import fit_clock

HORIZON_SHORT = 36


def _adults(df, study):
    pop = study["population"]
    return df[df["age"].between(pop["age_min"], pop["age_max"])]


def reference_rdw(year: int, spec: dict, source_base: str, raw_dir) -> pd.DataFrame:
    suffix = spec["nhanes_file"].split("_")[1]
    frames = {}
    for name in ("DEMO", spec["nhanes_file"].split("_")[0]):
        fname = f"{name}_{suffix}"
        frames[name] = _load_xpt(download(source_base.format(year=year, file=fname),
                                          raw_dir / f"{year}_{fname}.xpt"))
    d = frames["DEMO"][["RIDAGEYR", "RIAGENDR"]].join(frames["CBC"][[spec["nhanes_var"]]], how="inner")
    return d.rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex", spec["nhanes_var"]: "rdw"})


def harmonise(h: pd.DataFrame, study: dict, cfg: dict, base_url: str, raw_dir) -> pd.DataFrame:
    out = h.copy()
    for year, specs in cfg["crosswalks"].items():
        rows = out["cycle"] == year
        for var, spec in specs.items():
            out.loc[rows, var] = apply_crosswalk(out.loc[rows, var], spec)
    for var, spec in cfg["quantile_mapping"].items():
        ref = _adults(reference_rdw(spec["reference_cycle"], spec, base_url, raw_dir), study)
        for year in spec["cycles"]:
            rows = (out["cycle"] == year) & out["age"].between(study["population"]["age_min"],
                                                               study["population"]["age_max"])
            out.loc[rows, var] = quantile_map(out.loc[rows], ref, var, spec["age_bands"])
    return out


def _c_stats(d):
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    c = harrell_c(t, e, d["risk_global"].to_numpy())
    return {"C": c, "gain_C": c - harrell_c(t, e, d["risk_ref"].to_numpy())}


def evaluate_subset(d, label, version, systems, n_boot, seed):
    summ = summarize(_c_stats(d), bootstrap(d[[DURATION, EVENT, "risk_global", "risk_ref"]],
                                             functools.partial(_c_stats), n_boot, seed)).set_index("statistique")
    hr = cox_hr(d, ["gap_global"], ["age", "female"], DURATION, EVENT).iloc[0]
    obs, lo, hi = km_risk_at(d[DURATION], d[EVENT], HORIZON_SHORT)
    pred = d["risk36_global"].mean()
    _, cal = calibration(d[DURATION], d[EVENT], d["risk36_global"], HORIZON_SHORT, groups=5)
    row = {"version": version, "cycles": label, "n": len(d), "deces": int(d[EVENT].sum()),
           "suivi_median_mois": d[DURATION].median()}
    for k in ("C", "gain_C"):
        row[k], row[f"{k}_bas"], row[f"{k}_haut"] = summ.loc[k, ["estimation", "ic95_bas", "ic95_haut"]]
    row |= {"HR_par_ET": hr["HR"], "HR_bas": hr["ic95_bas"], "HR_haut": hr["ic95_haut"],
            "ET_ecart": hr["ecart_type"],
            "predit_3ans": pred, "observe_3ans": obs, "O_P_3ans": obs / pred,
            "O_P_bas": lo / pred, "O_P_haut": hi / pred,
            "pente_3ans": cal["pente_calibration"], "pente_bas": cal["pente_ic95_bas"],
            "pente_haut": cal["pente_ic95_haut"],
            "ecart_moyen_global": d["gap_global"].mean()}
    row |= {f"ecart_moyen_{s}": d[f"gap_{s}"].mean() for s in systems}
    return row


def crp_concordance(study) -> pd.DataFrame:
    """Quantiles de CRP (mg/L, plancher 0,1) par strate : 2005-06, 2009-10 (standard), 2015-16 (hs)."""
    rows = []
    h = build_harmonized([2005, 2009, 2015], cache=ROOT / study["paths"]["processed"] / "nhanes_crp_check.csv")
    a = _adults(h, study).dropna(subset=["crp"])
    a = a.assign(crp=a["crp"].clip(lower=0.1),
                 tranche=pd.cut(a["age"], [20, 40, 60, 80], right=False, labels=["20-39", "40-59", "60-79"]),
                 sexe=a["sex"].map({1: "Homme", 2: "Femme"}))
    for (cyc, sexe, tr), g in a.groupby(["cycle", "sexe", "tranche"], observed=True):
        q = g["crp"].quantile([0.25, 0.5, 0.75, 0.9])
        rows.append({"cycle": cyc, "dosage": "hs-CRP" if cyc >= 2015 else "CRP standard",
                     "sexe": sexe, "age": tr, "n": len(g),
                     "pct_au_plancher": 100 * (g["crp"] <= 0.1).mean(),
                     "p25": q[0.25], "p50": q[0.5], "p75": q[0.75], "p90": q[0.9]})
    return pd.DataFrame(rows)


def run(n_boot: int | None = None) -> dict:
    study = load_study()
    panel = load_panel("checkup_standard")
    out = ROOT / study["paths"]["reports"] / panel.name / "secondaire"
    out.mkdir(parents=True, exist_ok=True)
    n_boot = n_boot or study["validation"]["bootstrap"]
    seed = study["validation"]["seed"]
    raw_dir = ROOT / study["paths"]["raw"]
    cfg = yaml.safe_load((CONFIG_DIR / "sources" / "nhanes_harmonisation.yaml").read_text(encoding="utf-8"))
    base_url = yaml.safe_load((CONFIG_DIR / "sources" / "nhanes.yaml").read_text(encoding="utf-8"))["base_url"]

    dev_c, sec_c = study["cycles"]["development"], study["cycles"]["secondary"]
    dev_h = build_harmonized(dev_c, cache=ROOT / study["paths"]["processed"] / "nhanes_dev.csv")
    dev, _ = build_cohort(dev_h, panel, study)
    meta_main = json.loads((out.parent / "meta.json").read_text(encoding="utf-8"))
    clock = fit_clock(dev, panel, study, meta_main["penalizer"])        # identique au point 4
    systems = [s for s in clock.score_names if s != "global"]

    raw = build_harmonized(sec_c, cache=ROOT / study["paths"]["processed"] / "nhanes_secondary.csv")
    versions = {"brute": raw, "harmonisee": harmonise(raw, study, cfg, base_url, raw_dir)}

    rows, medians = [], []
    for version, h in versions.items():
        co, flow = build_cohort(h, panel, study)
        X = clock.design(co)
        d = co.join(clock.predict(co)).assign(
            female=(co["sex"] == 2).astype(float),
            risk36_global=clock.models["global"].risk_at(X, HORIZON_SHORT),
            risk36_ref=clock.reference.risk_at(X, HORIZON_SHORT))
        for label, sub in [("2015-2016", d[d["cycle"] == 2015]), ("2017-2018", d[d["cycle"] == 2017]),
                           ("2015-2018", d)]:
            rows.append(evaluate_subset(sub, label, version, systems, n_boot, seed))
        med = _adults(h, study).groupby("cycle")[["rdw", "alt", "ast", "alp", "albumin", "ggt",
                                                    "creatinine", "tg", "crp"]].median()
        medians.append(med.assign(version=version))

    table = pd.DataFrame(rows)
    table.to_csv(out / "secondaire.csv", index=False)
    pd.concat(medians).round(2).to_csv(out / "medianes_marqueurs.csv")
    crp_concordance(study).round(2).to_csv(out / "concordance_crp.csv", index=False)
    meta = {"bootstrap": n_boot, "seed": seed, "horizon_mois": HORIZON_SHORT,
            "chainage_mortalite": "public-use 2019 (suivi au 31/12/2019)",
            "ecart_moyen_validation_2007_2010": -1.44}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"table": table, "dossier": out}


def write_report(out) -> None:
    from .report import _md
    t = pd.read_csv(out / "secondaire.csv")
    med = pd.read_csv(out / "medianes_marqueurs.csv")
    crp = pd.read_csv(out / "concordance_crp.csv")
    ci = lambda r, k, f: f"{r[k]:{f}} [{r[k + '_bas']:{f}}; {r[k + '_haut']:{f}}]"  # noqa: E731
    tab = pd.DataFrame([{
        "Version": r["version"], "Cycles": r["cycles"], "n": r["n"], "Décès": r["deces"],
        "Suivi médian (mois)": f"{r['suivi_median_mois']:.0f}",
        "C": ci(r, "C", ".3f"), "Gain de C vs âge + sexe": ci(r, "gain_C", "+.3f"),
        "HR / ET d'écart": f"{r['HR_par_ET']:.2f} [{r['HR_bas']:.2f}; {r['HR_haut']:.2f}]",
        "Obs. / prédit 3 ans": f"{r['O_P_3ans']:.2f} [{r['O_P_bas']:.2f}; {r['O_P_haut']:.2f}]",
        "Pente 3 ans": f"{r['pente_3ans']:.2f} [{r['pente_bas']:.2f}; {r['pente_haut']:.2f}]",
        "Écart moyen (ans)": f"{r['ecart_moyen_global']:+.2f}",
    } for _, r in t.iterrows()])
    sys_cols = [c for c in t.columns if c.startswith("ecart_moyen_") and c != "ecart_moyen_global"]
    sys_t = t[["version", "cycles"] + sys_cols].rename(columns=lambda c: c.replace("ecart_moyen_", ""))
    crp_w = crp.pivot_table(index=["sexe", "age"], columns="cycle", values=["p50", "p75", "p90"]).round(1)
    crp_w.columns = [f"{q} {c}" for q, c in crp_w.columns]
    crp_w = crp_w.reset_index()
    text = f"""# Validation secondaire 2015-2018

Modèle gelé (point 4) ; protocole écrit avant exécution (`DECISIONS.md`, point 6). Analyse
**descriptive** de transposition ; aucune décision sur le modèle. Chaînage de mortalité public
le plus récent : 2019 (suivi jusqu'au 31/12/2019 ; la mise à jour 2022 est en accès restreint).
Peu de décès (162, dont 44 en 2017-2018) : intervalles larges.

## Harmonisation des dosages

- **RDW** : changement d'automate en 2013-2014 (Beckman DxH 800) sans étude de pontage →
  recalage par quantiles sur **2011-2012**, dernier cycle avant le changement, par strates
  sexe × âge.
- **Biochimie 2017-2018** (Roche Cobas 6000) : équations de pontage NHANES (`BIOPRO_J`, sens
  Cobas → DxC 660i) pour ALAT, ASAT, PAL, albumine, créatinine, GGT, triglycérides ; glucose non
  ajusté (recommandation NHANES). **hs-CRP 2017-2018** : équation NHANES (`HSCRP_J`), bornée au
  plancher de 0,1 mg/L (l'équation donne des valeurs négatives sous ~0,3 mg/L ; voir la correction
  d'implémentation dans `DECISIONS.md`).
- **Triglycérides** : l'équation officielle éloigne la médiane 2017-2018 de celle de 2015-2016
  (1,33 → 1,21 mmol/L, contre 1,38 en 2015-2016). Appliquée comme prévu ; à garder en tête.

Médianes des marqueurs (adultes 20-79 ans) :

{_md(med)}

## CRP standard (≤ 2010) contre hs-CRP (2015-2016)

**Concordance non vérifiable formellement** : NHANES ne documente pas la comparaison entre le
dosage standard (néphélométrie, mg/dL) et la hs-CRP (DxC), aucun échantillon n'a été dosé par les
deux méthodes, et 2011-2014 n'ont pas de CRP. Vérification descriptive : quantiles (mg/L, plancher
0,1) par strate. Les écarts 2009-10 → 2015-16 sont du même ordre que ceux de 2005-06 → 2009-10, ce
qui est compatible avec une concordance au-dessus du plancher, sans la démontrer.

{_md(crp_w, '.1f')}

## Résultats (versions brute et harmonisée)

{_md(tab)}

Écarts moyens par système :

{_md(sys_t, '+.2f')}

Repère : écart moyen en validation 2007-2010 = −1,44 an.

## Lecture

- **Les changements de laboratoire déplacent fortement l'âge biologique.** En version brute,
  l'écart moyen passe à +1,2 an (2015-16) et +2,6 ans (2017-18) ; harmonisé, il revient à −1,0 et
  −1,2 an, proche de la validation (−1,4). Le RDW explique l'essentiel en 2015-16 (système
  inflammatoire/hémato. +2,3 → −0,3 an) ; en 2017-18 s'ajoute la biochimie (hépatique +1,9 → −0,7).
- **Le classement est robuste aux dosages** : C, gain de C et HR quasi identiques entre les deux
  versions (C 0,85 ; gain +0,05 ; HR 2,2 par écart-type) — les décalages de laboratoire touchent
  tout le monde de la même façon.
- **La calibration en dépend** : à 3 ans, rapport observé/prédit 0,68 en brut (risque surestimé
  de 32 %) contre 0,86 [0,72 ; 1,02] harmonisé (0,98 en 2015-16).

## Note pour le point 4 (transposition)

Le **recalage par quantiles par strates d'âge et de sexe** est une méthode candidate pour la
transposition à une autre cohorte : il aligne la distribution d'un marqueur sur celle de la
population d'entraînement sans données de survie. Sa limite : il efface aussi les vraies
différences de distribution entre populations (ici, entre cycles). À n'utiliser que lorsqu'un
changement de méthode est documenté, ou en analyse de sensibilité.

Première exécution (avant correction de la hs-CRP négative) : version harmonisée 2017-2018,
n = 3 991, C 0,819, O/P 3 ans 0,78, écart moyen −1,16 an — conclusions identiques.
"""
    (out / "SECONDAIRE.md").write_text(text, encoding="utf-8")
