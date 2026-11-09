"""Analyse descriptive de la precision individuelle de l'age biologique (protocole : DECISIONS.md).

Scores calcules avec le modele JSON et le module autonome ; le pipeline ne sert qu'a charger la
cohorte de validation 2007-2010.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd

from . import plots
from .cohort import build_cohort
from .config import ROOT, load_panel, load_study
from .nhanes import build_harmonized
from .score import bioages, load_model, score_names
from .uncertainty import DEFAULT_VARIABILITY, cv_set, load_variability, simulate

N_DRAWS, N_DRAWS_CONTRIB, SEED = 1000, 200, 2026
GAP_BANDS = [0, 1, 3, 5, np.inf]
LABELS = plots.LABELS


def _summ(x: np.ndarray) -> dict:
    return {"mediane": float(np.median(x)), "q1": float(np.quantile(x, .25)),
            "q3": float(np.quantile(x, .75)), "p90": float(np.quantile(x, .90))}


def analyse(sims: dict, obs: dict, age: np.ndarray) -> dict:
    """Indicateurs par score a partir des remesures simulees."""
    res = {}
    half = sims["global"].shape[1] // 2
    for n, s in sims.items():
        sd = s.std(axis=1, ddof=1)
        width = np.quantile(s, .975, axis=1) - np.quantile(s, .025, axis=1)
        diff = np.abs(s[:, :half] - s[:, half:2 * half])
        rcv_emp = np.quantile(diff, .95, axis=1)
        gap_obs = obs[n] - age
        noise_var = float(np.mean(sd ** 2))
        icc = 1 - noise_var / float(np.var(gap_obs, ddof=1))
        g1, g2 = s[:, :half] - age[:, None], s[:, half:2 * half] - age[:, None]
        flip = (np.sign(g1) != np.sign(g2)).mean(axis=1)
        bands = pd.cut(np.abs(gap_obs), GAP_BANDS, right=False,
                       labels=["< 1 an", "1-3 ans", "3-5 ans", "≥ 5 ans"])
        res[n] = {"et": _summ(sd), "largeur_ic95": _summ(width), "rcv_empirique": _summ(rcv_emp),
                  "rcv_formule": _summ(1.96 * np.sqrt(2) * sd),
                  "variance_bruit": noise_var, "variance_observee": float(np.var(gap_obs, ddof=1)),
                  "cci": icc, "bascule_signe": float(flip.mean()),
                  "bascule_par_tranche": pd.Series(flip).groupby(bands, observed=True).mean().to_dict(),
                  "_sd": sd, "_width": width}
    return res


def _row(label, res, n):
    r = res[n]
    return {"scenario": label, "score": n,
            "et_median": r["et"]["mediane"],
            "largeur_ic95_mediane": r["largeur_ic95"]["mediane"],
            "largeur_ic95_q1": r["largeur_ic95"]["q1"], "largeur_ic95_q3": r["largeur_ic95"]["q3"],
            "largeur_ic95_p90": r["largeur_ic95"]["p90"],
            "rcv_mediane": r["rcv_empirique"]["mediane"],
            "rcv_q1": r["rcv_empirique"]["q1"], "rcv_q3": r["rcv_empirique"]["q3"],
            "rcv_formule_mediane": r["rcv_formule"]["mediane"],
            "cci": r["cci"], "bascule_signe": r["bascule_signe"]}


def run() -> dict:
    study = load_study()
    panel = load_panel("checkup_standard")
    out = ROOT / study["paths"]["reports"] / panel.name / "incertitude"
    out.mkdir(parents=True, exist_ok=True)
    model = load_model()
    variability = load_variability()
    names = score_names(model)

    val_c = study["cycles"]["validation"]
    h = build_harmonized(study["cycles"]["development"] + val_c,
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    co, _ = build_cohort(h, panel, study)
    val = co[co["cycle"].isin(val_c)].reset_index(drop=True)
    d = val[["age", "sex"] + list(model["variables"])]
    obs, _ = bioages(d, model)
    age = d["age"].to_numpy(float)

    # Frequence des valeurs remesurees hors plage du panel (bornees par le modele, non rejetees)
    rng = np.random.default_rng(SEED)
    base = cv_set(variability, model)
    clip_rows = []
    for v, spec in model["variables"].items():
        sig = np.sqrt(np.log1p(base[v] ** 2))
        x = d[v].to_numpy(float)[:, None] * np.exp(rng.standard_normal((len(d), 100)) * sig)
        lo, hi = spec["range"]
        clip_rows.append({"variable": v, "pct_hors_plage": 100 * float(((x < lo) | (x > hi)).mean())})
    pd.DataFrame(clip_rows).to_csv(out / "hors_plage.csv", index=False)

    scenarios = {
        "principal": cv_set(variability, model),
        "a. moyenne de 2 prises de sang": cv_set(variability, model, blood_divide=np.sqrt(2)),
        "b. toujours à jeun": cv_set(variability, model, fasting=True),
        "c. a + b": cv_set(variability, model, fasting=True, blood_divide=np.sqrt(2)),
        "sensibilité : bornes basses": cv_set(variability, model, which="cv_i_low"),
        "sensibilité : bornes hautes": cv_set(variability, model, which="cv_i_high"),
    }
    rows, main = [], None
    for label, cvs in scenarios.items():
        res = analyse(simulate(d, model, cvs, N_DRAWS, SEED), obs, age)
        rows += [_row(label, res, n) for n in names]
        if label == "principal":
            main = res
    table = pd.DataFrame(rows)
    table.to_csv(out / "resultats.csv", index=False)

    bands = pd.DataFrame([{"score": n, **{k: v for k, v in main[n]["bascule_par_tranche"].items()}}
                          for n in names])
    bands.to_csv(out / "bascule_par_tranche.csv", index=False)
    pd.DataFrame({f"largeur_ic95_{n}": main[n]["_width"] for n in names}).describe(
        percentiles=[.1, .25, .5, .75, .9]).to_csv(out / "distribution_largeurs.csv")

    # Contribution de chaque marqueur (un seul marqueur bruite a la fois)
    contrib = []
    for v in model["variables"]:
        sims = simulate(d, model, cv_set(variability, model, only=v), N_DRAWS_CONTRIB, SEED)
        for n in names:
            contrib.append({"variable": v, "score": n,
                            "variance": float(np.mean(sims[n].var(axis=1, ddof=1)))})
    contrib = pd.DataFrame(contrib)
    tot = contrib.groupby("score")["variance"].transform("sum")
    contrib["part_pct"] = 100 * contrib["variance"] / tot
    contrib.to_csv(out / "contributions.csv", index=False)
    additivity = {n: float(contrib.loc[contrib["score"] == n, "variance"].sum() / main[n]["variance_bruit"])
                  for n in names}

    plots.uncertainty_widths({LABELS.get(n, n): main[n]["_width"] for n in names},
                             out / "largeurs_ic95.png")
    plots.contribution_bars(contrib[contrib["score"] == "global"].sort_values("part_pct"),
                            out / "contributions_global.png")

    meta = {"n": len(d), "tirages": N_DRAWS, "tirages_contributions": N_DRAWS_CONTRIB, "graine": SEED,
            "variability_sha256": hashlib.sha256(DEFAULT_VARIABILITY.read_bytes()).hexdigest(),
            "modele": model["model"], "additivite_somme_contributions_sur_total": additivity}
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"table": table, "bands": bands, "contrib": contrib, "meta": meta, "dossier": out,
            "clip": pd.DataFrame(clip_rows)}


def write_report(out) -> None:
    from .report import _md
    t = pd.read_csv(out / "resultats.csv")
    bands = pd.read_csv(out / "bascule_par_tranche.csv")
    contrib = pd.read_csv(out / "contributions.csv")
    clip = pd.read_csv(out / "hors_plage.csv")
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    var = load_variability()
    lab = lambda n: LABELS.get(n, n)  # noqa: E731

    cv_tab = pd.DataFrame([{
        "Variable": k, "CV_I (%)": v["cv_i"], "Bornes": f"{v['cv_i_low']} – {v['cv_i_high']}",
        "CV_A (%)": v["cv_a"], "Source": v["source"]} for k, v in var.items()])

    main = t[t["scenario"] == "principal"]
    main_t = pd.DataFrame({
        "Score": main["score"].map(lab),
        "ET médian (ans)": main["et_median"].map("{:.1f}".format),
        "IC 95 % : largeur médiane [Q1 ; Q3] (ans)": [f"{m:.1f} [{a:.1f} ; {b:.1f}]" for m, a, b in
                                                     main[["largeur_ic95_mediane", "largeur_ic95_q1", "largeur_ic95_q3"]].to_numpy()],
        "90e centile de la largeur": main["largeur_ic95_p90"].map("{:.1f}".format),
    })
    rcv_t = pd.DataFrame({
        "Score": main["score"].map(lab),
        "Changement significatif : médiane [Q1 ; Q3] (ans)": [f"{m:.1f} [{a:.1f} ; {b:.1f}]" for m, a, b in
                                                             main[["rcv_mediane", "rcv_q1", "rcv_q3"]].to_numpy()],
        "1,96·√2·ET (médiane)": main["rcv_formule_mediane"].map("{:.1f}".format),
    })
    rel_t = pd.DataFrame({"Score": main["score"].map(lab), "CCI": main["cci"].map("{:.2f}".format),
                          "Bascule plus jeune / plus vieux (%)": (100 * main["bascule_signe"]).map("{:.1f}".format)})
    b = bands.copy()
    b["score"] = b["score"].map(lab)
    for c in b.columns[1:]:
        b[c] = (100 * b[c]).map("{:.1f}".format)

    cg = contrib[contrib["score"] == "global"].sort_values("part_pct", ascending=False)
    cpiv = contrib.pivot(index="variable", columns="score", values="part_pct").round(1)
    cpiv = cpiv.loc[cg["variable"]].reset_index()
    cpiv.columns = ["Variable"] + [lab(c) for c in cpiv.columns[1:]]

    sc = t[t["score"] == "global"]
    sc_t = pd.DataFrame({"Scénario": sc["scenario"],
                         "Largeur IC 95 % médiane (ans)": sc["largeur_ic95_mediane"].map("{:.1f}".format),
                         "Changement significatif médian (ans)": sc["rcv_mediane"].map("{:.1f}".format),
                         "CCI": sc["cci"].map("{:.2f}".format),
                         "Bascule (%)": (100 * sc["bascule_signe"]).map("{:.1f}".format)})
    sys_sc = t.pivot(index="scenario", columns="score", values="largeur_ic95_mediane").round(1)
    sys_sc = sys_sc.loc[sc["scenario"]].reset_index()
    sys_sc.columns = ["Scénario"] + [lab(c) for c in sys_sc.columns[1:]]
    add = ", ".join(f"{lab(k)} {v:.2f}" for k, v in meta["additivite_somme_contributions_sur_total"].items())
    clip_t = clip[clip["pct_hors_plage"] > 0.01].round(3)

    text = f"""# Précision individuelle de l'âge biologique

Analyse **descriptive** (protocole : `DECISIONS.md`) : le modèle est figé et rien n'en découle pour
lui. Calculs avec le modèle exporté (`models/checkup_standard_v1.json`) et le module autonome ;
validation 2007-2010, n = {meta['n']} ; {meta['tirages']} remesures simulées par personne, graine
{meta['graine']}.

## Hypothèse

Pour chaque personne, on simule des « remesures » de ses biomarqueurs avec un bruit multiplicatif
log-normal de médiane 1 et de CV total = racine(CV_I² + CV_A²), indépendant entre marqueurs.
**On simule autour de la valeur observée, qui contient déjà du bruit** : la dispersion obtenue est
celle qu'aurait une nouvelle mesure de la même personne, pas l'écart entre la mesure et une
« vraie » valeur. L'âge et le sexe ne sont pas bruités.

## Variabilités utilisées

Fichier `config/variability.yaml` (hors dépôt public, licence EFLM ; gabarit
`config/variability.example.yaml`). Valeurs EFLM citées avec l'accord des conditions d'usage
académique de la base (source : EFLM Biological Variation Database, biologicalvariation.eu).

{_md(cv_tab, '.1f')}

## Intervalles individuels

{_md(main_t)}

![Largeurs](largeurs_ic95.png)

## Changement significatif entre deux mesures

Écart minimal entre deux âges biologiques successifs d'une même personne pour conclure, à 95 %, à un
vrai changement (95e centile de |âge bio 1 − âge bio 2| sur 500 paires de remesures, par personne).

{_md(rcv_t)}

## Fiabilité et stabilité du classement

CCI ≈ 1 − variance due au bruit / variance de l'écart entre personnes (approximation : la variance
observée contient déjà du bruit). Bascule : part des paires de remesures où l'écart change de signe.

{_md(rel_t)}

Bascule par tranche d'écart observé (%) :

{_md(b)}

## Contribution de chaque marqueur (% de la variance due au bruit)

Un seul marqueur bruité à la fois ({meta['tirages_contributions']} tirages). Somme des variances par
marqueur / variance totale : {add} (≈ 1 si les contributions s'additionnent).

{_md(cpiv, '.1f')}

![Contributions](contributions_global.png)

## Scénarios pratiques et sensibilité (score global)

{_md(sc_t)}

Largeur médiane de l'IC 95 % par système et par scénario (ans) :

{_md(sys_sc, '.1f')}

## Remesures hors plage du panel

Valeurs simulées sortant des plages acceptées (bornées par les transformations du modèle, non
rejetées), en % des tirages :

{_md(clip_t) if len(clip_t) else "Aucune au-delà de 0,01 %."}

## Limites

- Les CV viennent de populations et de protocoles différents de la cohorte cible ; plusieurs sont
  des approximations ou des valeurs de travail (lymphocytes %, RDW %, ACR, fréquence cardiaque,
  IMC, tour de taille). La sensibilité aux bornes encadre cette incertitude.
- Bruit indépendant entre marqueurs : les variations corrélées (hémodilution, repas, inflammation
  intercurrente) ne sont pas représentées.
- Le scénario « à jeun » ne modifie que la variabilité ; le décalage moyen à jeun / non à jeun
  (triglycérides plus bas à jeun) est un biais non simulé, alors que le modèle a été entraîné sur
  des valeurs non à jeun.
- Les intervalles décrivent la reproductibilité de la mesure, pas l'incertitude du modèle lui-même
  (coefficients estimés), ni l'erreur due à des dosages non harmonisés (voir validation 2015-2018).
"""
    (out / "INCERTITUDE.md").write_text(text, encoding="utf-8")
