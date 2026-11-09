"""Effet de la correction du protocole d'evaluation du premier prototype.

Le prototype (10 marqueurs, NHANES 2009-2010) avait deux fuites :
  * la courbe de reference age -> risque etait entrainee sur toute la cohorte,
    test compris ;
  * le test du gain de l'ecart (age vs age + ecart) reposait sur un decoupage
    train/test refait sur un sous-ensemble different des lignes, donc des
    participants du test avaient servi a entrainer le Cox complet.

On compare, a donnees egales puis a protocole egal :
  A. prototype tel quel (valeurs mesurees en relancant le code d'origine) ;
  B. memes donnees, meme panel, un seul decoupage, tout entraine sur le train ;
  C. meme panel, validation temporelle 1999-2006 -> 2007-2010 ;
  D. panel check-up standard, validation temporelle (modele principal).
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from sklearn.model_selection import train_test_split

from .cohort import DURATION, EVENT, build_cohort
from .config import load_panel
from .metrics import harrell_c
from .model import BioAgeClock

# Mesures obtenues le 2026-11-09 en relancant src/model.py, src/biological_age.py
# et src/validate_gap.py du commit a5a857b (cohorte 2009-2010, n = 5645).
PROTOTYPE = {
    "protocole": "A. prototype (avec fuites)", "n_eval": 1129, "deces_eval": np.nan,
    "C_complet": 0.8666, "C_age": 0.8471, "dC_age_ecart": 0.0194,
    "HR_par_an_ecart": 1.10,
}


def _cox(df, cols):
    cph = CoxPHFitter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cph.fit(df[cols + [DURATION, EVENT]], duration_col=DURATION, event_col=EVENT)
    return cph


def _row(label, train, test, clock):
    """Metriques au format du prototype : C du risque complet, C age seul,
    gain de C d'un Cox age(+sexe) + ecart, HR par annee d'ecart."""
    tr = train.join(clock.predict(train))
    te = test.join(clock.predict(test))
    base = ["age", "female"] if clock.panel.include_sex else ["age"]
    for d in (tr, te):
        d["female"] = (d["sex"] == 2).astype(float)
    m_a = _cox(tr, base)
    m_b = _cox(tr, base + ["gap_global"])
    c_a = harrell_c(te[DURATION], te[EVENT], m_a.predict_partial_hazard(te[base]))
    c_b = harrell_c(te[DURATION], te[EVENT], m_b.predict_partial_hazard(te[base + ["gap_global"]]))
    hr = _cox(te, base + ["gap_global"]).summary.loc["gap_global", "exp(coef)"]
    return {"protocole": label, "n_eval": len(te), "deces_eval": int(te[EVENT].sum()),
            "C_complet": harrell_c(te[DURATION], te[EVENT], te["risk_global"]),
            "C_age": c_a, "dC_age_ecart": c_b - c_a, "HR_par_an_ecart": hr,
            "ET_ecart_ans": te["gap_global"].std()}


def run(harmonized: pd.DataFrame, study: dict, main_panel: str, penalizer: float) -> pd.DataFrame:
    legacy = load_panel("legacy_10markers")
    cfg0 = {**study, "model": {**study["model"], "penalizer": 0.0}}
    rows = [PROTOTYPE]

    # B. memes donnees que le prototype (2009-2010, >= 20 ans, sans autre filtre)
    c09, _ = build_cohort(harmonized[harmonized["cycle"] == 2009], legacy, study,
                          age_min=20, age_max=200, exclude_pregnant=False)
    train, test = train_test_split(c09, test_size=0.2, random_state=42, stratify=c09[EVENT])
    clock = BioAgeClock(legacy, cfg0).fit(train)
    rows.append(_row("B. memes donnees, sans fuite", train, test, clock))

    dev_c, val_c = study["cycles"]["development"], study["cycles"]["validation"]
    # C. panel historique, validation temporelle
    co, _ = build_cohort(harmonized, legacy, study)
    dev, val = co[co["cycle"].isin(dev_c)], co[co["cycle"].isin(val_c)]
    rows.append(_row("C. 10 marqueurs, validation temporelle", dev, val,
                     BioAgeClock(legacy, cfg0).fit(dev)))

    # D. panel principal
    panel = load_panel(main_panel)
    cfg = {**study, "model": {**study["model"], "penalizer": penalizer}}
    co, _ = build_cohort(harmonized, panel, study)
    dev, val = co[co["cycle"].isin(dev_c)], co[co["cycle"].isin(val_c)]
    rows.append(_row(f"D. panel {panel.name}, validation temporelle", dev, val,
                     BioAgeClock(panel, cfg).fit(dev)))
    return pd.DataFrame(rows)
