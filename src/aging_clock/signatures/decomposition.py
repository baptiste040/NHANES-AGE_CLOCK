"""Piste « signatures » : decomposition des corrections du 2026-11-12 (vecteurs d'effet et bruit a 6 mois).

Croise deux choix : vecteurs d'effet (anciens : medianes de NHANES III ; nouveaux : medianes de 2001-2002,
comme Q1 corrige) et bruit a 6 mois (A/B : ALAT et ASAT seulement ; A/B/C : tous les marqueurs).
Meme graine pour toutes les cellules. Sortie : signatures_decomposition_corrections.csv.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import analyse as A
from . import vecteurs as V

# Anciens vecteurs (en %), avant la correction du 2026-11-12 (medianes de NHANES III)
MED_OLD = {"tc": 203.0, "hdl": 48.0, "tg": 118.0, "alt": 15.0, "ast": 19.0, "ggt": 23.0, "crp_mgL": 2.7, "wbc": 6.9}
OLD = {
    "perte_poids": {"tg_serum": 100 * (-4.0 * 7) / MED_OLD["tg"], "hdl": 100 * (0.46 * 7) / MED_OLD["hdl"],
                    "tc": 100 * (-1.28 * 7 + 0.46 * 7 + (-4.0 * 7) / 5) / MED_OLD["tc"], "alt": 100 * (-0.83 * 7) / MED_OLD["alt"],
                    "ast": 100 * (-2.8 / 5 * 7) / MED_OLD["ast"], "glu_serum": -4.1},
    "activite_aerobie": {"tc": -2.906, "hdl": 4.396, "tg_serum": -6.788, "glu_serum": -2.919},
    "mediterraneen": {"tc": -2.808, "hdl": 2.708, "tg_serum": -10.424, "glu_serum": -3.222, "hba1c": -2.830, "alt": -37.733,
                      "ggt": -10.913},
    "reduction_alcool": {"hdl": 100 * (-3.99) / MED_OLD["hdl"], "tg_serum": 100 * (-5.69) / MED_OLD["tg"]},
    "arret_tabac": {"hdl": 100 * (0.100 * 38.67) / MED_OLD["hdl"], "wbc": 100 * (-0.8) / MED_OLD["wbc"]},
}


def old_vector(iv, panel=V.PANEL):
    return np.array([np.log1p(OLD[iv].get(m, 0.0) / 100) for m in panel])


def table_vecteurs() -> pd.DataFrame:
    rows = []
    for iv in V.INTERVENTIONS:
        new = V.vector(iv)
        old = old_vector(iv)
        for m, a, b in zip(V.PANEL, old, new):
            if a or b:
                rows.append({"intervention": iv, "id": m, "effet_pct_avant": 100 * np.expm1(a), "effet_pct_apres": 100 * np.expm1(b)})
    return pd.DataFrame(rows)


def run():
    data = A.load()
    Dcal, _ = A.deltas(*data["2001"], A.P)
    Dev, _ = A.deltas(*data["nh3"], A.P)
    S2, _, _ = A.robust_cov(Dcal)
    rows = []
    for noise in ("AB", "ABC"):
        om = A.omega(A.P, noise)
        for vlab, vf in (("anciens", old_vector), ("nouveaux", V.vector)):
            vecs = {iv: vf(iv) for iv in A.IV}
            rng = np.random.default_rng(A.SEED)
            B, _, _ = A.run_detection(Dcal, Dev, S2, S2 + np.diag(om), om, vecs, rng, label=f"{vlab} vecteurs, bruit {noise}")
            b = B[B.horizon == "6 mois"]
            for _, r in b.iterrows():
                rows.append({"vecteurs": vlab, "bruit_6_mois": noise, "intervention": r.intervention, "sens_signature": r.sens_sig_principal,
                             "sens_meilleur_seul": r.sens_best_principal, "meilleur_marqueur": r.meilleur_marqueur,
                             "gain": r.sens_sig_principal - r.sens_best_principal, "fausses_alertes_signature": r.fausses_alertes_sig})
    t = pd.DataFrame(rows)
    t.to_csv(A.OUT / "signatures_decomposition_corrections.csv", index=False)
    table_vecteurs().to_csv(A.OUT / "signatures_vecteurs_avant_apres.csv", index=False)
    return t


if __name__ == "__main__":
    print(run().round(3).to_string())
