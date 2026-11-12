"""Export du modele gele en JSON, avec la specification des entrees et un exemple synthetique.

Le JSON contient tout ce qu'il faut pour calculer les scores sans le pipeline :
transformations apprises (planchers, bornes, noeuds), coefficients, moyennes de centrage,
survie de base, grille de l'age biologique. Le calcul est fait par `aging_clock.score`
(NumPy + pandas uniquement).
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from .cohort import EVENT, build_cohort
from .config import CONFIG_DIR, ROOT, load_panel, load_study
from .nhanes import build_harmonized
from .validate import fit_clock

MODEL_VERSION = "1.0.0"
SHORT_HORIZONS = [12, 24, 36, 60, 120]

WARNINGS = [
    "Un âge biologique absolu n'est interprétable que si les dosages de la cohorte d'application sont "
    "comparables à ceux du développement (section reference_lab_methods) ou harmonisés. Un "
    "changement d'automate peut décaler l'âge biologique de plusieurs années sans changer le "
    "classement des personnes (validation secondaire 2015-2018).",
    "Le score décrit un risque de mortalité toutes causes, pas l'effet protecteur des "
    "traitements ; ce n'est pas un outil de diagnostic.",
    "Le risque absolu est surestimé chez les groupes favorisés (revenu élevé, diplôme "
    "universitaire) : sans recalibrage local, l'âge biologique d'une cohorte de check-up "
    "de prévention sera probablement surestimé ; le classement reste valide.",
    "Domaine de validité : adultes de 20 à 79 ans ; valeurs dans les plages de "
    "variables[*].range ; unités canoniques de variables[*].unit.",
]


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:  # noqa: BLE001
        return "inconnu"


def _cox_dict(model) -> dict:
    bs = model.lifelines_.baseline_survival_.iloc[:, 0]
    return {
        "columns": list(model.columns),
        "coefficients": [float(c) for c in model.coef_],
        "means": [float(m) for m in model.mean_],
        "baseline_survival": {str(h): float(bs[bs.index <= h].iloc[-1]) for h in SHORT_HORIZONS},
    }


def build_model_dict(clock, panel, study, dev: pd.DataFrame) -> dict:
    methods = yaml.safe_load((CONFIG_DIR / "sources" / "nhanes_methodes_reference.yaml")
                             .read_text(encoding="utf-8"))
    variables = {}
    for name in panel.model_variables:
        v, st = panel.variables[name], clock.transformer.state[name]
        variables[name] = {
            "unit": v.unit, "system": v.system, "required": True,
            "range": list(v.range) if v.range else None,
            "floor": v.floor, "log": v.log,
            "clip_transformed": st["clip"],
            "spline_knots_transformed": st.get("knots"),
            "alt_units": v.alt_units,
        }
    optional = {n: {"unit": v.unit, "system": v.system, "required": False,
                    "note": "collectée, non utilisée par le modèle"}
                for n, v in panel.variables.items() if not v.in_model and not n.startswith("rx_")}
    lo, hi, step = study["model"]["bioage_grid"]
    meta = json.loads((ROOT / "reports" / panel.name / "meta.json").read_text(encoding="utf-8"))
    return {
        "format": "aging-clock-model",
        "format_version": 1,
        "model": {"name": panel.name, "version": MODEL_VERSION,
                  "created": dt.date.today().isoformat(), "code_commit": _git_commit(),
                  "panel_sha256": panel.sha256},
        "description": ("Score de vieillissement biologique par système, conçu pour être appliqué "
                        "à des cohortes de check-up de prévention. Âge biologique = âge auquel le "
                        "risque de décès à 10 ans de la population de référence (même sexe) égale "
                        "le risque prédit."),
        "warnings": WARNINGS,
        "training": {
            "data": "NHANES 1999-2006 chaînées aux Linked Mortality Files 2019 (NCHS)",
            "cycles": study["cycles"]["development"], "n": int(len(dev)),
            "deaths": int(dev[EVENT].sum()),
            "age_range": [study["population"]["age_min"], study["population"]["age_max"]],
            "exclusions": ["femmes enceintes", "non éligibles au chaînage", "cas incomplets"],
            "penalizer": meta["penalizer"],
            "decisions": "DECISIONS.md",
        },
        "reference_lab_methods": methods,
        "horizon_months": study["model"]["horizon_months"],
        "sex_coding": {"1": "homme", "2": "femme"},
        "include_sex": panel.include_sex,
        "systems": {s: panel.systems[s] for s in panel.active_systems},
        "variables": variables,
        "optional_variables": optional,
        "models": {"reference": _cox_dict(clock.reference)}
                  | {name: _cox_dict(m) for name, m in clock.models.items()},
        "bioage_grid": {"min": lo, "max": hi, "step": step},
    }


def synthetic_example(model: dict, n: int = 6, seed: int = 2026) -> pd.DataFrame:
    """Donnees ENTIEREMENT SYNTHETIQUES (tirages uniformes dans des plages cliniques usuelles)."""
    rng = np.random.default_rng(seed)
    typical = {"sbp": (105, 150), "dbp": (60, 92), "total_chol": (4.0, 6.8), "hdl": (0.9, 2.0),
               "tg": (0.6, 2.8), "heart_rate": (55, 90), "glucose": (4.4, 7.5), "hba1c": (4.9, 6.8),
               "bmi": (19, 34), "waist": (70, 112), "creatinine": (55, 110), "acr": (0.2, 5.0),
               "alt": (10, 45), "ast": (14, 40), "ggt": (10, 70), "alp": (40, 110),
               "albumin": (38, 49), "crp": (0.2, 8.0), "wbc": (4.0, 9.5), "lymph_pct": (18, 42),
               "rdw": (11.8, 14.5), "mcv": (82, 98), "hb": (11.8, 16.8), "platelets": (160, 360)}
    df = pd.DataFrame({"id": [f"SYNTH-{i + 1:03d}" for i in range(n)],
                       "age": rng.integers(25, 76, n), "sex": rng.integers(1, 3, n)})
    for var in model["variables"]:
        lo, hi = typical[var]
        df[var] = np.round(rng.uniform(lo, hi, n), 2)
    return df


def input_spec_markdown(model: dict) -> str:
    rows = ["| Variable | Unité | Système | Obligatoire | Plage acceptée | Transformation |",
            "|---|---|---|---|---|---|",
            "| `age` | années | — | oui | 20-79 (domaine de validité) | — |",
            "| `sex` | 1 = homme, 2 = femme | — | oui | 1 ou 2 | — |"]
    for name, v in model["variables"].items():
        tr = []
        if v["floor"] is not None:
            tr.append(f"plancher {v['floor']}")
        if v["log"]:
            tr.append("log")
        if v["spline_knots_transformed"]:
            tr.append(f"spline ({len(v['spline_knots_transformed'])} nœuds)")
        tr.append("bornée aux percentiles 0,5-99,5 du développement")
        rows.append(f"| `{name}` | {v['unit']} | {v['system']} | oui | "
                    f"{v['range'][0]} – {v['range'][1]} | {', '.join(tr)} |")
    for name, v in model["optional_variables"].items():
        rows.append(f"| `{name}` | {v['unit']} | {v['system']} | non | — | non utilisée |")
    conv = "\n".join(f"- `{n}` : " + ", ".join(
        f"{u} → × {f}" if not isinstance(f, list) else f"{u} → {f[0]} × valeur + {f[1]}"
        for u, f in v["alt_units"].items()) for n, v in model["variables"].items() if v["alt_units"])
    return f"""# Spécification des entrées — modèle `{model['model']['name']}` v{model['model']['version']}

Fichier CSV, une ligne par personne, une colonne par variable, **unités canoniques** ci-dessous.
Colonne facultative `id` (recopiée en sortie). Une valeur manquante ou hors plage dans une
variable obligatoire rend les scores de la ligne manquants (motif indiqué dans `statut`).

{chr(10).join(rows)}

Conversions vers l'unité canonique (multiplier la valeur) :

{conv}

## Avertissements

{chr(10).join('- ' + w for w in model['warnings'])}

## Sorties

`age_bio_global`, `ecart_global` (âge biologique − âge), `age_bio_<système>` et
`ecart_<système>` pour chaque système, `risque_deces_10ans`, `statut` (ok, ou motifs).

Commande : `python -m aging_clock score --input fichier.csv [--output scores.csv]`.
"""


def run(out_dir: Path | None = None) -> Path:
    study = load_study()
    panel = load_panel("checkup_standard")
    dev_h = build_harmonized(study["cycles"]["development"],
                             cache=ROOT / study["paths"]["processed"] / "nhanes_dev.csv")
    dev, _ = build_cohort(dev_h, panel, study)
    meta = json.loads((ROOT / "reports" / panel.name / "meta.json").read_text(encoding="utf-8"))
    clock = fit_clock(dev, panel, study, meta["penalizer"])
    model = build_model_dict(clock, panel, study, dev)

    out_dir = out_dir or ROOT / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{panel.name}_v{MODEL_VERSION.split('.')[0]}.json"
    path.write_text(json.dumps(model, indent=1, ensure_ascii=False), encoding="utf-8")
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "specification_entrees.md").write_text(input_spec_markdown(model), encoding="utf-8")
    (ROOT / "examples").mkdir(exist_ok=True)
    synthetic_example(model).to_csv(ROOT / "examples" / "exemple_entree_synthetique.csv", index=False)
    return path
