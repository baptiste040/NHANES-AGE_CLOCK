import numpy as np
import pandas as pd
import pytest

from aging_clock.config import load_panel, load_study
from aging_clock.features import FeatureTransformer, rcs_basis
from aging_clock.metrics import harrell_c
from aging_clock.model import BioAgeClock, CoxAtHorizon
from aging_clock.nhanes import _extract, egfr_ckd_epi_2021


# ------------------------------------------------------------------ panels
@pytest.mark.parametrize("name", ["checkup_standard", "legacy_10markers"])
def test_panels_load(name):
    panel = load_panel(name)
    assert panel.model_variables
    for v in panel.variables.values():
        assert v.system in panel.systems


def test_checkup_panel_systems():
    panel = load_panel("checkup_standard")
    assert set(panel.active_systems) == {
        "cardiovasculaire", "metabolique", "renal", "hepatique", "inflammatoire_hematologique"}
    assert "ldl" not in panel.model_variables          # LDL facultatif
    assert set(panel.system_variables("cardiovasculaire")) == {"sbp", "dbp", "total_chol", "hdl", "tg"}


def test_panel_rejects_unknown_key(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("name: bad\nsystems: {a: x}\nvariables:\n  v: {unit: x, system: a, typo: 1}\n")
    with pytest.raises(ValueError, match="inconnues"):
        load_panel(p)


# --------------------------------------------------------- harmonisation
def test_extract_per_cycle_var_factor_and_calibration():
    frames = {"BIOPRO": pd.DataFrame({"LBXSCR": [1.0], "LBDSCR": [2.0]}, index=[1])}
    spec = {"file": "BIOPRO", "var": {2001: "LBDSCR", "default": "LBXSCR"}, "factor": 88.42,
            "calibration": {1999: [1.013, 0.147]}}
    assert _extract(frames, spec, 2001).iloc[0] == pytest.approx(2.0 * 88.42)
    assert _extract(frames, spec, 1999).iloc[0] == pytest.approx((1.013 + 0.147) * 88.42)
    assert _extract(frames, spec, 2007).iloc[0] == pytest.approx(88.42)


def test_extract_mean_ignores_zero_diastolic():
    frames = {"BPX": pd.DataFrame({"D1": [0.0], "D2": [70.0], "D3": [80.0]}, index=[1])}
    spec = {"file": "BPX", "var": ["D1", "D2", "D3"], "agg": "mean", "zero_is_missing": True}
    assert _extract(frames, spec, 2009).iloc[0] == pytest.approx(75.0)


def test_egfr_reference_value():
    # Femme 50 ans, creatinine 0.7 mg/dL -> 142 * 0.9938^50 * 1.012 ~ 105
    assert egfr_ckd_epi_2021(0.7 * 88.42, 50, 2) == pytest.approx(105.0, abs=1.0)


# ------------------------------------------------------------ features
def test_rcs_linear_beyond_last_knot():
    knots = np.array([0.0, 1.0, 2.0, 3.0])
    x = np.array([4.0, 5.0, 6.0])
    b = rcs_basis(x, knots)
    second_diff = b[2] - 2 * b[1] + b[0]
    assert np.allclose(second_diff, 0, atol=1e-10)


def test_rcs_zero_below_first_knot():
    assert np.allclose(rcs_basis(np.array([-1.0, 0.0]), np.array([0.0, 1.0, 2.0, 3.0])), 0)


def test_transformer_learns_on_fit_data_only():
    panel = load_panel("checkup_standard")
    train = pd.DataFrame({"crp": np.linspace(0.01, 10, 200)})
    tr = FeatureTransformer(panel, ["crp"]).fit(train)
    out = tr.transform(pd.DataFrame({"crp": [0.001, 1000.0]}))
    lo, hi = tr.state["crp"]["clip"]
    assert out["crp"].between(lo, hi).all()
    assert lo >= np.log(0.1)               # plancher de detection applique avant le log


# ------------------------------------------------------------- modele
def _synthetic(n=3000, seed=0):
    rng = np.random.default_rng(seed)
    age = rng.uniform(20, 80, n)
    sex = rng.integers(1, 3, n)
    df = pd.DataFrame({"age": age, "sex": sex})
    panel = load_panel("legacy_10markers")
    for v in panel.model_variables:
        lo, hi = panel.variables[v].range
        df[v] = rng.uniform(lo + (hi - lo) * 0.2, lo + (hi - lo) * 0.4, n)
    lp = 0.08 * (age - 50) + 0.05 * (df["rdw"] - df["rdw"].mean())
    t = rng.exponential(1 / (0.002 * np.exp(lp)))
    df["PERMTH_EXM"] = np.minimum(t, 180)
    df["MORTSTAT"] = (t <= 180).astype(int)
    return panel, df


def test_cox_at_horizon_matches_lifelines():
    panel, df = _synthetic()
    X = df[["age", "rdw"]]
    # horizon pris sur un temps d'evenement observe : lifelines interpole entre
    # deux evenements, alors que CoxAtHorizon utilise l'estimateur en escalier.
    h = float(np.sort(df.loc[df["MORTSTAT"] == 1, "PERMTH_EXM"])[500])
    m = CoxAtHorizon(["age", "rdw"], h).fit(X, df["PERMTH_EXM"], df["MORTSTAT"])
    ref = 1 - m.lifelines_.predict_survival_function(X.iloc[:50], times=[h]).iloc[0].to_numpy()
    assert np.allclose(m.risk(X.iloc[:50]), ref, atol=1e-8)


def test_bioage_inversion_is_identity_on_reference_curve():
    panel, df = _synthetic()
    study = load_study()
    study["model"]["penalizer"] = 0.0
    clock = BioAgeClock(panel, study).fit(df)
    grid = pd.DataFrame({"age": [30.0, 50.0, 70.0], "female": 0.0})
    risk = clock.reference.risk(grid)
    back = clock._invert(risk, np.zeros(3))
    assert np.allclose(back, [30, 50, 70], atol=0.05)


def test_bioage_increases_with_risk():
    panel, df = _synthetic()
    study = load_study()
    study["model"]["penalizer"] = 0.0
    pred = BioAgeClock(panel, study).fit(df).predict(df)
    order = np.argsort(pred["risk_global"].to_numpy())
    assert np.all(np.diff(pred["bioage_global"].to_numpy()[order]) >= -1e-9)


def test_harrell_c_perfect_and_reversed():
    t = np.array([1, 2, 3, 4, 5.0])
    e = np.ones(5)
    assert harrell_c(t, e, -t) == 1.0
    assert harrell_c(t, e, t) == 0.0
