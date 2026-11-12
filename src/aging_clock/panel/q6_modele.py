"""Programme « panel », Q6 : modele de Cox, courbes de HR, zones et seuils (protocole : DECISIONS.md).

Cox a vraisemblance partielle (ex aequo de Breslow) ecrit en numpy pour permettre le bootstrap ;
verifie contre lifelines (tests/test_q6_cox.py).
"""
from __future__ import annotations

import numpy as np
from scipy.stats import chi2

from ..features import rcs_basis

KN = [5, 35, 65, 95]          # centiles des noeuds (Harrell, 4 noeuds) : marqueur et age
GRID = (1, 99)                 # courbes entre les centiles 1 et 99 du developpement
WINSOR = (0.5, 99.5)           # valeurs tronquees aux centiles 0,5 et 99,5 du developpement
B_BOOT, SEED = 200, 2026


def cox_fit(X, t, e, w=None, iters=50, tol=1e-9):
    """Renvoie (beta, cov, loglik). Ex aequo de Breslow ; poids optionnels (estimation ponctuelle)."""
    n, p = X.shape
    w = np.ones(n) if w is None else np.asarray(w, float)
    o = np.argsort(-t, kind="mergesort")
    X, t, e, w = X[o], t[o], np.asarray(e)[o].astype(bool), w[o]
    last = np.searchsorted(-t, -t, side="right") - 1
    ev = np.where(e)[0]
    li = last[ev]
    Xc = X - X.mean(0)
    b = np.zeros(p)

    def stats(b):
        eta = Xc @ b
        eta = eta - eta.max()
        r = w * np.exp(eta)
        S0 = np.cumsum(r)[li]
        S1 = np.cumsum(r[:, None] * Xc, 0)[li]
        return r, S0, S1, float(np.sum(w[ev] * (eta[ev] - np.log(S0))))

    def hess(r, S0, S1):
        S2 = np.cumsum(r[:, None, None] * (Xc[:, :, None] * Xc[:, None, :]), 0)[li]
        m1 = S1 / S0[:, None]
        g = np.sum(w[ev, None] * (Xc[ev] - m1), 0)
        H = np.einsum("i,ijk->jk", w[ev], S2 / S0[:, None, None] - m1[:, :, None] * m1[:, None, :])
        return g, H

    r, S0, S1, ll = stats(b)
    for _ in range(iters):
        g, H = hess(r, S0, S1)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, g, rcond=None)[0]
        s = 1.0
        while True:
            nb = b + s * step
            r2, S02, S12, ll2 = stats(nb)
            if ll2 >= ll - 1e-12 or s < 1e-4:
                break
            s /= 2
        done = abs(ll2 - ll) < tol
        b, r, S0, S1, ll = nb, r2, S02, S12, ll2
        if done:
            break
    _, H = hess(r, S0, S1)
    return b, np.linalg.pinv(H), ll


class Spec:
    """Transformation, troncature, noeuds et grille d'un marqueur, fixes sur le developpement."""

    def __init__(self, x_dev, log):
        x_dev = np.asarray(x_dev, float)
        self.log = log
        self.clip = tuple(np.percentile(x_dev, WINSOR))
        self.knots = np.percentile(self.tr(x_dev), KN)
        g0, g1 = np.percentile(x_dev, GRID)
        self.grid = np.exp(np.linspace(np.log(g0), np.log(g1), 200)) if log else np.linspace(g0, g1, 200)
        self.k = 1 + len(KN) - 2

    def tr(self, x):
        x = np.clip(np.asarray(x, float), *self.clip)
        return np.log(x) if self.log else x

    def basis(self, x):
        z = self.tr(x)
        return np.column_stack([z, rcs_basis(z, self.knots)])


def age_basis(age, kn):
    age = np.asarray(age, float)
    return np.column_stack([age, rcs_basis(age, kn)])


def design(m, age, sex, spec, age_kn, extra=None):
    cols = [spec.basis(m), age_basis(age, age_kn), (np.asarray(sex) == 2).astype(float)[:, None]]
    if extra is not None and extra.shape[1]:
        cols.append(extra)
    return np.column_stack(cols)


def curve(spec, b, cov):
    Bg = spec.basis(spec.grid)
    k = spec.k
    f = Bg @ b[:k]
    i0 = int(np.argmin(f))
    D = Bg - Bg[i0]
    se = np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", D, cov[:k, :k], D), 0))
    lhr = f - f[i0]
    return {"xmin": float(spec.grid[i0]), "i0": i0, "hr": np.exp(lhr), "lo": np.exp(lhr - 1.96 * se), "hi": np.exp(lhr + 1.96 * se)}


def thresholds(spec, c, level):
    """Premiere valeur, en s'eloignant du minimum, ou le HR (point) atteint `level`, de chaque cote."""
    g, hr, i0 = spec.grid, c["hr"], c["i0"]
    out = {}
    for side, rng in (("bas", range(i0, -1, -1)), ("haut", range(i0, len(g)))):
        val, prev = None, None
        for i in rng:
            if hr[i] >= level:
                if prev is None:
                    val = float(g[i])
                else:
                    h0, h1 = hr[prev], hr[i]
                    a = (level - h0) / (h1 - h0) if h1 != h0 else 0.0
                    val = float(g[prev] + a * (g[i] - g[prev]))
                break
            prev = i
        out[side] = val
    return out


def min_zone(spec, c):
    ok = c["lo"] < 1.1
    a = z = c["i0"]
    while a - 1 >= 0 and ok[a - 1]:
        a -= 1
    while z + 1 < len(ok) and ok[z + 1]:
        z += 1
    return [float(spec.grid[a]), float(spec.grid[z])]


def shape(t12, t15):
    lo, hi = t12["bas"] is not None, t12["haut"] is not None
    if lo and hi:
        return "en U" if (t15["bas"] is not None) == (t15["haut"] is not None) else "en J"
    return "montante" if hi else "descendante" if lo else "plate"


def fit(m, age, sex, t, e, spec, age_kn, extra=None, w=None, keep_curve=True):
    X = design(m, age, sex, spec, age_kn, extra)
    b, cov, ll = cox_fit(X, t, e, w)
    _, _, ll0 = cox_fit(X[:, spec.k:], t, e, w)
    c = curve(spec, b, cov)
    t12, t15 = thresholds(spec, c, 1.2), thresholds(spec, c, 1.5)
    out = {"n": int(len(t)), "deces": int(np.sum(e)), "p_global": float(chi2.sf(2 * (ll - ll0), spec.k)), "xmin": c["xmin"],
           "zone_min": min_zone(spec, c), "seuil_1_2": t12, "seuil_1_5": t15, "forme": shape(t12, t15)}
    if keep_curve:
        out["_curve"] = c
    return out


def interaction_p(m, age, sex, t, e, spec, age_kn, v):
    X = design(m, age, sex, spec, age_kn)
    Bm = spec.basis(m)
    _, _, ll0 = cox_fit(X, t, e)
    _, _, ll1 = cox_fit(np.column_stack([X, Bm * np.asarray(v, float)[:, None]]), t, e)
    return float(chi2.sf(2 * (ll1 - ll0), spec.k))


def boot_thresholds(m, age, sex, t, e, spec, age_kn, B=B_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    X = design(m, age, sex, spec, age_kn)
    res = {k: [] for k in ("bas", "haut", "bas15", "haut15")}
    for _ in range(B):
        ix = rng.integers(0, len(t), len(t))
        b, cov, _ = cox_fit(X[ix], t[ix], e[ix], iters=25, tol=1e-7)
        c = curve(spec, b, cov)
        t12, t15 = thresholds(spec, c, 1.2), thresholds(spec, c, 1.5)
        for s in ("bas", "haut"):
            res[s].append(t12[s])
            res[s + "15"].append(t15[s])
    out = {}
    for s, v in res.items():
        vals = np.array([x for x in v if x is not None])
        out[s] = {"part": float(len(vals) / B),
                  "ic95": [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if len(vals) >= 20 else None}
    return out
