"""Modele JSON gele et module de calcul autonome."""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from aging_clock.score import DEFAULT_MODEL, load_model, score

ROOT = Path(__file__).resolve().parents[1]
DATA_OK = (ROOT / "data" / "raw" / "2007_DEMO_E.xpt").exists() and (ROOT / "data" / "raw" / "1999_DEMO.xpt").exists()


def test_score_module_imports_only_numpy_pandas():
    tree = ast.parse((ROOT / "src" / "aging_clock" / "score.py").read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0] if node.level == 0 else "relatif:" + (node.module or ""))
    assert mods <= {"__future__", "json", "pathlib", "numpy", "pandas"}, mods


def test_score_runs_without_pipeline_dependencies():
    code = ("import sys; import aging_clock.score as s; "
            "bad=[m for m in sys.modules if m.split('.')[0] in ('lifelines','sklearn','scipy','yaml','matplotlib','joblib')]; "
            "print(bad); assert not bad")
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                       env={**os.environ, "PYTHONPATH": str(ROOT / "src")})
    assert r.returncode == 0, r.stdout + r.stderr


def test_synthetic_example_scores_without_alert():
    df = pd.read_csv(ROOT / "examples" / "exemple_entree_synthetique.csv")
    assert df["id"].str.startswith("SYNTH-").all()          # donnees synthetiques uniquement
    res = score(df, load_model())
    assert (res["statut"] == "ok").all()
    assert res["age_bio_global"].between(10, 120).all()


def test_input_checks():
    model = load_model()
    row = pd.read_csv(ROOT / "examples" / "exemple_entree_synthetique.csv").iloc[[0]].copy()
    bad = pd.concat([row.assign(crp=np.nan), row.assign(rdw=99.0), row.assign(sex=3)], ignore_index=True)
    res = score(bad, model)
    assert res["age_bio_global"].isna().all()
    assert "crp manquant" in res.loc[0, "statut"] and "rdw hors plage" in res.loc[1, "statut"]
    with pytest.raises(ValueError, match="Colonnes obligatoires absentes"):
        score(row.drop(columns=["acr"]), model)


def test_json_contains_lab_methods_and_warning():
    model = json.loads(Path(DEFAULT_MODEL).read_text(encoding="utf-8"))
    assert "reference_lab_methods" in model and "numeration" in model["reference_lab_methods"]
    assert any("dosages" in w and "harmonisés" in w for w in model["warnings"])


@pytest.mark.skipif(not DATA_OK, reason="donnees NHANES absentes")
def test_json_reproduces_pipeline_on_validation():
    """Le calcul depuis le JSON reproduit exactement le pipeline sur la validation 2007-2010."""
    from aging_clock.cohort import build_cohort
    from aging_clock.config import load_panel, load_study
    from aging_clock.export import build_model_dict
    from aging_clock.nhanes import build_harmonized
    from aging_clock.validate import fit_clock

    study, panel = load_study(), load_panel("checkup_standard")
    dev_c, val_c = study["cycles"]["development"], study["cycles"]["validation"]
    h = build_harmonized(dev_c + val_c, cache=ROOT / "data" / "processed" / "nhanes_harmonized.csv")
    co, _ = build_cohort(h, panel, study)
    dev, val = co[co["cycle"].isin(dev_c)], co[co["cycle"].isin(val_c)]
    committed = load_model()
    clock = fit_clock(dev, panel, study, committed["training"]["penalizer"])
    fresh = build_model_dict(clock, panel, study, dev)

    # le JSON versionne correspond au pipeline actuel (hors date et commit)
    for key in ("variables", "models", "bioage_grid", "horizon_months"):
        assert fresh[key] == committed[key], key

    ref = clock.predict(val)
    res = score(val, committed)
    assert (res["statut"].str.startswith("ok") | res["statut"].str.contains("limite de grille")).all()
    for n in clock.score_names:
        assert np.allclose(res[f"age_bio_{n}"], ref[f"bioage_{n}"], atol=1e-8, rtol=0), n
    assert np.allclose(res["risque_deces_10ans"], ref["risk_global"], atol=1e-12, rtol=0)


# ------------------------------------------------------------- incertitude
def _uncertainty_inputs():
    from aging_clock.uncertainty import cv_set
    model = load_model()
    df = pd.read_csv(ROOT / "examples" / "exemple_entree_synthetique.csv")
    cvs = {v: 0.05 for v in model["variables"]}
    return model, df, cvs


def test_simulation_reproducible_with_fixed_seed():
    from aging_clock.uncertainty import simulate
    model, df, cvs = _uncertainty_inputs()
    a = simulate(df, model, cvs, n_draws=200, seed=7)
    b = simulate(df, model, cvs, n_draws=200, seed=7)
    c = simulate(df, model, cvs, n_draws=200, seed=8)
    for n in a:
        assert np.array_equal(a[n], b[n])
    assert not np.array_equal(a["global"], c["global"])


def test_zero_noise_gives_zero_width_interval():
    from aging_clock.score import bioages
    from aging_clock.uncertainty import intervals, simulate
    model, df, _ = _uncertainty_inputs()
    sims = simulate(df, model, {v: 0.0 for v in model["variables"]}, n_draws=50, seed=1)
    iv = intervals(sims)
    obs, _ = bioages(df, model)
    for n in sims:
        assert np.allclose(iv[f"age_bio_{n}_ic95_haut"], iv[f"age_bio_{n}_ic95_bas"], atol=1e-10)
        assert np.allclose(iv[f"age_bio_{n}_ic95_bas"], obs[n], atol=1e-10)


def test_uncertainty_module_imports_only_numpy_pandas():
    tree = ast.parse((ROOT / "src" / "aging_clock" / "uncertainty.py").read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0] if node.level == 0 else "relatif:" + (node.module or ""))
    assert mods <= {"__future__", "json", "pathlib", "numpy", "pandas", "relatif:score"}, mods


# ------------------------------------------------------------- seuils de changement
def test_change_thresholds_added_and_crp_rule():
    from aging_clock.score import DEFAULT_THRESHOLDS, add_change_thresholds
    th = json.loads(Path(DEFAULT_THRESHOLDS).read_text(encoding="utf-8"))
    model = load_model()
    df = pd.read_csv(ROOT / "examples" / "exemple_entree_synthetique.csv")
    df.loc[0, "crp"] = 25.0
    res = add_change_thresholds(score(df, model), df)
    for n in [x for x in model["models"] if x != "reference"]:
        col = f"seuil_changement_{n}"
        assert np.isnan(res.loc[0, col])                                   # CRP > 10 : pas de seuil
        assert np.allclose(res.loc[1:, col], th["scores"][n]["seuil_ans"])
    assert res["alerte_crp"].tolist()[0] and not res["alerte_crp"].iloc[1:].any()
