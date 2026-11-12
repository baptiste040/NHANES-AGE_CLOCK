"""Piste « signatures » : complements demandes apres les resultats (amendement du 2026-11-12).

1. IC qui integrent l'incertitude du calage : chaque tirage bootstrap reechantillonne les 403 paires de
   calibration (2001-2002), reestime la covariance robuste, recale les seuils, puis reechantillonne les
   personnes d'evaluation (NHANES III). Nombres aleatoires communs (L et k fixes par paire).
2. Levier du bilan de depart : sensibilite a 6 mois selon le nombre de prelevements au depart (1, 2, 3, a
   quelques semaines d'intervalle) et de bilans de suivi (1, 2). Modele gaussien (comme B10).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from . import analyse as A
from . import vecteurs as V

NB = 500
SEUIL = 1.645


def _quant(x, q):
    return float(np.quantile(x, q))


def bootstrap_ci(nb=NB):
    rng = np.random.default_rng(A.SEED + 1)
    data = A.load()
    Dcal, _ = A.deltas(*data["2001"], A.P)
    Dev, _ = A.deltas(*data["nh3"], A.P)
    om = A.omega(A.P)
    vecs = {iv: V.vector(iv) for iv in A.IV}
    nrep = 100
    Lc = A.sample_L(len(Dcal), om, rng=rng, nrep=nrep)
    Le = A.sample_L(len(Dev), om, rng=rng, nrep=nrep)
    K = A.k_draws("principal", (nrep, len(Dev), 1), rng)
    res = {(hz, iv): {"fa_sig": [], "fa_best": [], "sens_sig": [], "sens_best": [], "diff": []} for hz in ("2 semaines", "6 mois")
           for iv in A.IV}
    glob = {hz: [] for hz in ("2 semaines", "6 mois")}
    for b in range(nb + 1):
        ic = np.arange(len(Dcal)) if b == 0 else rng.integers(0, len(Dcal), len(Dcal))
        ie = np.arange(len(Dev)) if b == 0 else rng.integers(0, len(Dev), len(Dev))
        S2, _, _ = A.robust_cov(Dcal[ic])
        S6 = S2 + np.diag(om)
        for hz, S, Xc, Xe in (("2 semaines", S2, Dcal[ic][None], Dev[ie][None]),
                              ("6 mois", S6, Dcal[ic][None] + Lc[:, ic], Dev[ie][None] + Le[:, ie])):
            any_ = np.zeros(Xe.shape[:2], bool)
            for iv, d in vecs.items():
                det = A.Det(d, S)
                ts = np.quantile(det.sig(Xc).ravel(), 0.95)
                tb = np.quantile(det.best(Xc).ravel(), 0.95)
                Xi = np.broadcast_to(Xe, (nrep,) + Xe.shape[1:]) + K[:, ie] * d
                s_sig, s_best = det.sig(Xi) > ts, det.best(Xi) > tb
                r = res[(hz, iv)]
                r["fa_sig"].append(float((det.sig(Xe) > ts).mean()))
                r["fa_best"].append(float((det.best(Xe) > tb).mean()))
                r["sens_sig"].append(float(s_sig.mean()))
                r["sens_best"].append(float(s_best.mean()))
                r["diff"].append(float(s_sig.mean() - s_best.mean()))
                any_ |= det.sig(Xe) > ts
            glob[hz].append(float(any_.mean()))
    rows = []
    for (hz, iv), r in res.items():
        row = {"horizon": hz, "intervention": iv}
        for k, v in r.items():
            v = np.array(v)
            row[k] = v[0]
            row[f"{k}_ic95"] = [_quant(v[1:], 0.025), _quant(v[1:], 0.975)]
        rows.append(row)
    g = [{"horizon": hz, "fausses_alertes_5_signatures": v[0], "ic95": [_quant(v[1:], 0.025), _quant(v[1:], 0.975)]}
         for hz, v in glob.items()]
    return pd.DataFrame(rows), pd.DataFrame(g)


def levier_depart():
    """Sensibilite a 6 mois (gaussien) selon b prelevements au depart et f bilans de suivi.
    Mesure = vraie valeur + composante a long terme (propre a la periode, partagee par les prelevements
    rapproches du depart, independante entre bilans de suivi) + bruit a court terme (independant).
    Cov(delta) = Sigma_ct (1/b + 1/f) + (Omega/2)(1 + 1/f), avec Sigma_ct = Sigma_2sem / 2."""
    data = A.load()
    Dcal, _ = A.deltas(*data["2001"], A.P)
    S2, _, _ = A.robust_cov(Dcal)
    om = A.omega(A.P)
    Sct, Olt = S2 / 2, np.diag(om) / 2
    rows = []
    for iv in ("perte_poids", "mediterraneen", "arret_tabac", "activite_aerobie"):
        d = V.vector(iv)
        for b in (1, 2, 3):
            for f in (1, 2):
                C = Sct * (1 / b + 1 / f) + Olt * (1 + 1 / f)
                s_sig = float(np.sqrt(d @ np.linalg.solve(C, d)))
                s_best = float(np.max(np.abs(d) / np.sqrt(np.diag(C))))
                p = lambda s: float(norm.cdf((s - SEUIL) / np.sqrt(1 + 0.25 * s ** 2)))  # noqa: E731
                rows.append({"intervention": iv, "prelevements_depart": b, "bilans_suivi": f, "sens_signature": p(s_sig),
                             "sens_meilleur_seul": p(s_best), "sens_signature_k1": float(norm.cdf(s_sig - SEUIL))})
    return pd.DataFrame(rows)


def run():
    ci, g = bootstrap_ci()
    ci.to_csv(A.OUT / "signatures_ic_recalage.csv", index=False)
    g.to_csv(A.OUT / "signatures_usage_global_ic_recalage.csv", index=False)
    lv = levier_depart()
    lv.to_csv(A.OUT / "signatures_levier_depart.csv", index=False)
    return ci, g, lv


if __name__ == "__main__":
    run()
