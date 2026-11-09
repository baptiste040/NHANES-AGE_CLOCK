"""Assemble les sorties de validation en un rapport Markdown (RESULTATS.md)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .plots import LABELS


def _md(df: pd.DataFrame, floatfmt: str = ".3f") -> str:
    def fmt(v):
        if isinstance(v, float):
            return "" if pd.isna(v) else format(v, floatfmt)
        return str(v)
    head = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    body = ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, sep, *body])


def _lab(s: str) -> str:
    return LABELS.get(s.removeprefix("gap_"), s)


def _ci(est, lo, hi, f=".3f"):
    return f"{est:{f}} [{lo:{f}}; {hi:{f}}]"


def write(out: Path) -> Path:
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    flux = pd.read_csv(out / "flux.csv")
    ech = pd.read_csv(out / "echantillons.csv")
    disc = pd.read_csv(out / "discrimination.csv").set_index("statistique")
    hrs = pd.read_csv(out / "hr_par_ecart_type.csv")
    cal = pd.read_csv(out / "calibration.csv")
    sens = pd.read_csv(out / "sensibilites.csv")
    leak = pd.read_csv(out / "effet_correction_fuite.csv")
    scores = list(cal["score"])

    perf = pd.DataFrame([{
        "Score": _lab(s),
        "C (IC95)": _ci(*disc.loc[f"C_{s}", ["estimation", "ic95_bas", "ic95_haut"]]),
        "Gain de C vs âge + sexe (IC95)": _ci(*disc.loc[f"dC_{s}", ["estimation", "ic95_bas", "ic95_haut"]]),
        "HR par ET d'écart (IC95)": _ci(*hrs.loc[hrs["exposition"] == f"gap_{s}",
                                            ["HR", "ic95_bas", "ic95_haut"]].iloc[0], f=".2f"),
        "ET de l'écart (ans)": f"{hrs.loc[hrs['exposition'] == f'gap_{s}', 'ecart_type'].iloc[0]:.1f}",
    } for s in scores])
    ref = _ci(*disc.loc["C_ref", ["estimation", "ic95_bas", "ic95_haut"]])

    calt = pd.DataFrame([{
        "Score": _lab(r.score), "Risque prédit moyen": f"{r.risque_predit_moyen:.3f}",
        "Risque observé (KM)": f"{r.risque_observe_km:.3f}",
        "Observé / prédit": f"{r.ratio_observe_predit:.2f}",
        "Pente (IC95)": _ci(r.pente_calibration, r.pente_ic95_bas, r.pente_ic95_haut, ".2f"),
        "Écart absolu moyen (déciles)": f"{r.ecart_absolu_moyen_deciles:.3f}",
    } for r in cal.itertuples()])

    sens_t = sens.assign(Score=sens["score"].map(_lab))[
        ["scenario", "modele", "Score", "n", "deces", "C", "C_ic95", "dC", "dC_ic95", "HR_par_ET", "HR_ic95"]]

    parts = [f"""# Résultats de validation — panel `{meta['panel']}`

Rapport généré automatiquement par `python -m aging_clock validate --panel {meta['panel']}`.
Toutes les figures et tables sont dans ce dossier (CSV = vue tableau des figures).

> **Le panel a évolué depuis le jalon 1** (ajout de l'ACR urinaire au système rénal et de la
> fréquence cardiaque au système cardiovasculaire, décidés par validation croisée sur
> 1999-2006 uniquement). La cohorte 2007-2010 avait déjà été consultée au jalon 1 ; ce
> passage est l'unique consultation avec le panel final. Voir `DECISIONS.md`.
> Résultats du jalon 1 archivés dans `reports/archive/jalon1_checkup_standard/`.

- Développement : cycles NHANES {', '.join(map(str, meta['cycles_developpement']))} ; validation temporelle : {', '.join(map(str, meta['cycles_validation']))}.
- Mortalité : Linked Mortality Files 2019 (NCHS). Horizon de l'âge biologique : 10 ans.
- Pénalisation ridge des marqueurs choisie par validation croisée sur le développement : {meta['penalizer']}.
- IC à 95 % par bootstrap ({meta['bootstrap']} répliques ; {meta['bootstrap_sensibilites']} pour les sensibilités) ; graine {meta['seed']}.
- Empreinte SHA-256 du panel : `{meta['panel_sha256'][:16]}…`.

## Population

{_md(flux)}

{_md(ech, '.1f')}

## Discrimination et association (validation)

C de référence (Cox âge + sexe) : **{ref}**.

{_md(perf)}

HR par écart-type de l'écart d'âge, ajusté sur l'âge et le sexe, Cox ajusté dans l'échantillon de validation.

![HR](hr_par_ecart_type.png)

## Calibration à 10 ans (validation)

{_md(calt)}

Pente = coefficient du log(-log(1 - risque prédit)) dans un Cox de validation (1 = idéal).

![Calibration](calibration.png)
"""]

    if (out / "independance_spearman.csv").exists():
        sp = pd.read_csv(out / "independance_spearman.csv", index_col=0)
        sp.index = [_lab(i) for i in sp.index]
        sp.columns = [_lab(c) for c in sp.columns]
        joint = pd.read_csv(out / "independance_cox.csv")
        joint_t = pd.DataFrame([{
            "Système": _lab(r.exposition),
            "HR par ET, ajusté mutuellement (IC95)": _ci(r.HR, r.ic95_bas, r.ic95_haut, ".2f"),
            "p": f"{r.p:.1e}"} for r in joint.itertuples()])
        parts.append(f"""## Indépendance des écarts par système (validation)

Corrélations de Spearman entre écarts d'âge par système :

{_md(sp.reset_index(names='').round(2), '.2f')}

![Spearman](independance_spearman.png)

Cox avec tous les écarts par système ensemble (ajusté âge et sexe) :

{_md(joint_t)}

![Cox joint](independance_cox.png)
""")

    parts.append(f"""## Sensibilités

« figé » = modèle principal appliqué au sous-échantillon de validation ;
« ré-entraîné » = modèle ré-entraîné sur le développement filtré de la même façon.
Pour les causes spécifiques, les décès d'autres causes sont censurés.

{_md(sens_t)}

## Effet de la correction du protocole (prototype)

{_md(leak)}

`C_complet` : C du risque prédit par le modèle complet. `C_age` : Cox âge seul
(âge + sexe pour le panel check-up). `dC_age_ecart` : gain de C quand on ajoute
l'écart d'âge à ce Cox. A = valeurs du prototype relancé tel quel.
""")
    path = out / "RESULTATS.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path
