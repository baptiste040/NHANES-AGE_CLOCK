"""Tests des metriques de fiabilite test-retest (retest.py), sans donnees NHANES."""
import numpy as np
import pytest

from aging_clock import retest


def test_icc_identical_measures_is_one():
    x = np.array([1.0, 3.0, -2.0, 5.0, 0.5])
    assert retest.icc_a1(x, x) == pytest.approx(1.0)


def test_icc_penalises_systematic_shift():
    """Accord absolu : un decalage constant baisse le CCI (contrairement a la correlation)."""
    x = np.random.default_rng(0).normal(size=200)
    assert retest.icc_a1(x, x + 2.0) < 0.5
    assert retest.icc_a1(x, x + 0.0) == pytest.approx(1.0)


def test_icc_matches_variance_ratio():
    rng = np.random.default_rng(1)
    t = rng.normal(0, 3, 20000)
    a, b = t + rng.normal(0, 1, t.size), t + rng.normal(0, 1, t.size)
    assert retest.icc_a1(a, b) == pytest.approx(9 / 10, abs=0.01)


def test_observed_metrics_definitions():
    a = np.array([0.0, 1.0, 2.0, 3.0])
    b = np.array([1.0, 1.0, 3.0, 2.0])
    m = retest.observed_metrics(a, b)
    sd_d = np.std(b - a, ddof=1)
    assert m["ba_biais"] == pytest.approx(0.25)
    assert m["ba_limite"] == pytest.approx(1.96 * sd_d)
    assert m["rcv"] == pytest.approx(1.96 * np.sqrt(2) * sd_d / np.sqrt(2))
    assert m["bascule"] == pytest.approx(0.25)     # seul 0 -> 1 change de signe (0 est « nul »)


def test_cv_scenario_fixes_physical_measures():
    cfg = {"principal": {"albumin": {"cv_i": 3.0, "cv_a": 4.0}, "sbp": {"cv_i": 8.0, "cv_a": 0.0}},
           "secondaire": {"albumin": 0.0}, "sensibilites": {}}
    assert retest.cv_scenario(cfg)["albumin"] == pytest.approx(0.05)
    assert retest.cv_scenario(cfg)["sbp"] == 0.0
    assert retest.cv_scenario(cfg, physical=True)["sbp"] == pytest.approx(0.08)
    assert retest.cv_scenario(cfg, "secondaire")["albumin"] == pytest.approx(0.04)


def test_marker_cv_recovers_lognormal_cv():
    rng = np.random.default_rng(2)
    x = np.exp(rng.normal(3, 0.5, 50000))
    s = np.sqrt(np.log1p(0.10 ** 2))
    x1, x2 = x * np.exp(rng.normal(0, s, x.size)), x * np.exp(rng.normal(0, s, x.size))
    assert retest.marker_cv(x1, x2) == pytest.approx(10.0, abs=0.2)
