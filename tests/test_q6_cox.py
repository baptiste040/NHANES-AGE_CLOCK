"""Le Cox numpy de Q6 donne les memes coefficients que lifelines sans ex aequo."""
import numpy as np
import pandas as pd
import pytest

from aging_clock.panel.q6_modele import cox_fit

lifelines = pytest.importorskip("lifelines")


def test_cox_matches_lifelines_without_ties():
    rng = np.random.default_rng(3)
    n = 3000
    X = rng.normal(size=(n, 4))
    t = rng.exponential(50 * np.exp(-X @ np.array([0.4, -0.3, 0.1, 0.0])))
    e = rng.random(n) < 0.7
    b, cov, _ = cox_fit(X, t, e)
    df = pd.DataFrame(X, columns=list("abcd")).assign(T=t, E=e)
    c = lifelines.CoxPHFitter().fit(df, "T", "E")
    assert np.allclose(b, c.params_.values, atol=1e-4)
    assert np.allclose(np.sqrt(np.diag(cov)), c.standard_errors_.values, atol=1e-4)
