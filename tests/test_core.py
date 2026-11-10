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
    # Composition figee par les decisions du jalon 2 (DECISIONS.md, points 2 et 3)
    assert set(panel.system_variables("cardiovasculaire")) == {
        "sbp", "dbp", "total_chol", "hdl", "tg", "heart_rate"}
    assert set(panel.system_variables("renal")) == {"creatinine", "acr"}
    for optional in ("urea", "htn_treated", "lipid_treated", "rx_antihypertensive", "rx_statin"):
        assert optional not in panel.model_variables


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


def test_treatment_chain_codes_unknown_as_missing():
    from aging_clock.nhanes import treatment_chain
    df = pd.DataFrame({"A": [2, 1, 1, 1, 9, 1, np.nan],
                       "B": [np.nan, 2, 1, 1, np.nan, 7, np.nan],
                       "C": [np.nan, np.nan, 1, 2, np.nan, np.nan, np.nan]})
    out = treatment_chain(df, ["A", "B", "C"])
    expected = [0, 0, 1, 0, np.nan, np.nan, np.nan]
    assert np.allclose(out.to_numpy(), expected, equal_nan=True)


# ------------------------------------------------------------- PhenoAge publie
def _phenoage_case():
    # Adulte de 50 ans aux marqueurs « normaux », unites du projet (CRP en mg/L)
    return pd.DataFrame([{"age": 50, "albumin": 45.0, "creatinine": 80.0, "glucose": 5.0,
                          "crp": 1.0, "lymph_pct": 30.0, "mcv": 90.0, "rdw": 13.0,
                          "alp": 70.0, "wbc": 6.0}])


def test_phenoage_published_constants():
    from aging_clock import phenoage as pa
    # Levine 2018, tableau 1 et supplement 1 (conversion en annees) ; M : correction Liu 2019
    assert pa.COEFS == {"albumin": -0.0336, "creatinine": 0.0095, "glucose": 0.1953,
                        "ln_crp": 0.0954, "lymph_pct": -0.0120, "mcv": 0.0268,
                        "rdw": 0.3306, "alp": 0.00188, "wbc": 0.0554, "age": 0.0804}
    assert (pa.INTERCEPT, pa.GAMMA) == (-19.907, 0.0076927)
    assert (pa.AGE_CONST, pa.LOG_FACTOR, pa.AGE_DENOM) == (141.50225, -0.00553, 0.090165)
    # 1.51714 = exp(120 * gamma) - 1 : M est bien le risque Gompertz a 10 ans
    assert pa.SCALE == pytest.approx(np.exp(120 * pa.GAMMA) - 1, abs=1e-5)


def test_phenoage_worked_example():
    """Calcul a la main de l'equation publiee (CRP 1 mg/L = 0,1 mg/dL) :
    xb = -19.907 - 0.0336*45 + 0.0095*80 + 0.1953*5 + 0.0954*ln(0.1) - 0.012*30
         + 0.0268*90 + 0.3306*13 + 0.00188*70 + 0.0554*6 + 0.0804*50 = -9.06837
    M  = 1 - exp(-1.51714 * exp(xb) / 0.0076927)                     = 0.022474
    PhenoAge = 141.50225 + ln(-0.00553 * ln(1 - M)) / 0.090165        = 41.889
    """
    from aging_clock import phenoage as pa
    df = _phenoage_case()
    assert pa.linear_predictor(df)[0] == pytest.approx(-9.06837, abs=1e-5)
    assert pa.mortality_score(df)[0] == pytest.approx(0.022474, abs=1e-6)
    assert pa.phenoage(df)[0] == pytest.approx(41.889, abs=1e-3)


def test_phenoage_increases_with_crp_and_age():
    from aging_clock import phenoage as pa
    base = _phenoage_case()
    worse = base.assign(crp=10.0, age=60)
    assert pa.phenoage(worse)[0] > pa.phenoage(base)[0]


# ------------------------------------------------------------- harmonisation
def test_crosswalk_alt_backward_matches_nhanes_example():
    from aging_clock.harmonisation import apply_crosswalk
    spec = {"type": "linear", "slope": 1.013, "intercept": 2.688, "factor": 1}
    assert apply_crosswalk(pd.Series([18.0]), spec).iloc[0] == pytest.approx(20.922, abs=1e-3)


def test_crosswalk_units_and_range():
    from aging_clock.harmonisation import apply_crosswalk
    # albumine : equation en g/dL appliquee a des g/L (4,1 g/dL = 41 g/L)
    alb = {"type": "linear", "slope": 1.044, "intercept": 0.01128, "factor": 10}
    assert apply_crosswalk(pd.Series([41.0]), alb).iloc[0] == pytest.approx(10 * (1.044 * 4.1 + 0.01128))
    crp = {"type": "linear", "slope": 1.15, "intercept": -0.3397, "factor": 1, "max_input": 20}
    out = apply_crosswalk(pd.Series([10.0, 50.0]), crp)
    assert out.iloc[0] == pytest.approx(11.1603) and out.iloc[1] == 50.0


def test_quantile_map_identity_and_shift():
    from aging_clock.harmonisation import quantile_map
    rng = np.random.default_rng(1)
    ref = pd.DataFrame({"age": rng.integers(20, 80, 4000), "sex": rng.integers(1, 3, 4000),
                        "rdw": rng.normal(12.6, 0.8, 4000)})
    shifted = ref.assign(rdw=ref["rdw"] + 0.9)
    mapped = quantile_map(shifted, ref, "rdw", [20, 40, 60, 80])
    assert abs(mapped.median() - ref["rdw"].median()) < 0.05
    assert np.corrcoef(mapped, shifted["rdw"])[0, 1] > 0.999      # rangs conserves


def test_crosswalk_min_output_prevents_negative_crp():
    from aging_clock.harmonisation import apply_crosswalk
    crp = {"type": "linear", "slope": 1.15, "intercept": -0.3397, "factor": 1,
           "max_input": 20, "min_output": 0.1}
    assert apply_crosswalk(pd.Series([0.15]), crp).iloc[0] == 0.1


def test_read_xpt_restores_exact_zeros(tmp_path):
    """Defaut de pd.read_sas (xport) : 0 lu comme ~5.4e-79 ; read_xpt le remet a 0."""
    import pandas as pd
    from aging_clock import nhanes
    raw = pd.DataFrame({"SEQN": [1.0, 2.0, 3.0], "BPXDI1": [5.397605e-79, 70.0, np.nan]})
    orig = pd.read_sas
    pd.read_sas = lambda *a, **k: raw.copy()
    try:
        df = nhanes.read_xpt(tmp_path / "x.xpt")
    finally:
        pd.read_sas = orig
    assert df["BPXDI1"].iloc[0] == 0.0 and df["BPXDI1"].iloc[1] == 70.0 and np.isnan(df["BPXDI1"].iloc[2])


def test_zero_diastolic_reading_is_missing():
    """Une lecture diastolique a 0 est exclue de la moyenne (zero_is_missing)."""
    import pandas as pd
    from aging_clock import nhanes
    frames = {"BPX": pd.DataFrame({"BPXDI1": [0.0, 80.0], "BPXDI2": [70.0, 0.0],
                                   "BPXDI3": [72.0, 0.0], "BPXDI4": [np.nan, np.nan]})}
    spec = {"file": "BPX", "var": ["BPXDI1", "BPXDI2", "BPXDI3", "BPXDI4"], "agg": "mean",
            "zero_is_missing": True}
    out = nhanes._extract(frames, spec, 2001)
    assert out.tolist() == [71.0, 80.0]
