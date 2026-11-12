"""Piste « signatures », partie C : donnees de la demo (personnes fictives, synthetiques) et page HTML.

Les personnes sont des tirages synthetiques : valeurs de depart = medianes des 30-55 ans (premier examen
2001-2002), variation = bruit gaussien de covariance Sigma_6mois (partie B) + effet eventuel + piege eventuel.
Pour chaque cas, on retient le premier tirage (graine 2026, puis +1...) qui illustre le cas annonce ; la regle
est ecrite sur la page.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import analyse as A
from . import vecteurs as V

LABELS = {"tc": "Cholestérol total", "hdl": "HDL", "tg_serum": "Triglycérides", "glu_serum": "Glycémie", "hba1c": "HbA1c",
          "alt": "ALAT", "ast": "ASAT", "ggt": "GGT", "alp": "PAL", "albumin": "Albumine", "creat": "Créatinine", "urea": "Urée",
          "urate": "Acide urique", "wbc": "Leucocytes", "hb": "Hémoglobine", "mcv": "VGM", "rdw": "RDW", "plt": "Plaquettes"}
UNITS = {"tc": "mg/dL", "hdl": "mg/dL", "tg_serum": "mg/dL", "glu_serum": "mg/dL", "hba1c": "%", "alt": "U/L", "ast": "U/L", "ggt": "U/L",
         "alp": "U/L", "albumin": "g/dL", "creat": "mg/dL", "urea": "mg/dL", "urate": "mg/dL", "wbc": "G/L", "hb": "g/dL", "mcv": "fL",
         "rdw": "%", "plt": "G/L"}


def _cases():
    return [
        ("A", "Sans intervention, programme « perte de poids » prescrit", "perte_poids", 0.0, None,
         lambda naive, t, tc, thr, thrc: naive >= 3 and t <= thr,
         "premier tirage avec au moins 3 marqueurs « significatifs » isolés et une signature muette"),
        ("B", "Perte de poids, réponse moyenne (k = 1)", "perte_poids", 1.0, None,
         lambda naive, t, tc, thr, thrc: t > thr, "premier tirage où la signature détecte l'effet"),
        ("C", "Perte de poids, réponse faible (k = 0,3)", "perte_poids", 0.3, None,
         lambda naive, t, tc, thr, thrc: t <= thr, "premier tirage où la signature ne détecte pas l'effet (le cas le plus fréquent)"),
        ("D", "Sans intervention, changement de laboratoire (biochimie), programme « perte de poids »", "perte_poids", 0.0, "labo_biochimie",
         lambda naive, t, tc, thr, thrc: t > thr and tc <= thrc,
         "premier tirage où la signature simple se déclenche à tort et la signature insensible aux pièges reste muette"),
        ("E", "Sans intervention, début d'une pilule, programme « arrêt du tabac »", "arret_tabac", 0.0, "pilule",
         lambda naive, t, tc, thr, thrc: t > thr, "premier tirage où la signature se déclenche à tort"),
    ]


def build_people():
    data = A.load()
    e1, e2 = data["2001"]
    base = e1[e1.age.between(30, 55)][A.P].median()
    Dcal, _ = A.deltas(*data["2001"], A.P)
    S2, _, _ = A.robust_cov(Dcal)
    om = A.omega(A.P)
    S6 = S2 + np.diag(om)
    q1 = A.q1()
    hi = np.array([np.log(1 + q1.loc[m, "cd6m_hausse"] / 100) for m in A.P])
    lo = np.array([np.log(1 - q1.loc[m, "cd6m_baisse"] / 100) for m in A.P])
    det_rows = pd.read_csv(A.OUT / "signatures_detection.csv")
    pits, _ = A.pitfalls(A.P)
    rng_L = np.random.default_rng(A.SEED)
    Lcal = A.sample_L(len(Dcal), om, rng=rng_L)
    people = []
    chol = np.linalg.cholesky(S6)
    for code, title, iv, k, pit, cond, rule in _cases():
        d = V.vector(iv)
        det = A.Det(d, S6)
        thr = float(det_rows[(det_rows.variante == "principal") & (det_rows.horizon == "6 mois") & (det_rows.intervention == iv)].seuil_sig.iloc[0])
        # signature insensible aux pieges (laboratoire de biochimie et pilule)
        Pm = np.column_stack([pits["labo_biochimie"], pits["pilule"]])
        dc = A.constrained(d, S6, Pm)
        detc = A.Det(dc, S6)
        thrc = float(np.quantile(detc.sig(Dcal[None] + Lcal).ravel(), 0.95))
        seed = 2026
        while True:
            z = np.random.default_rng(seed).standard_normal(len(A.P))
            delta = chol @ z + k * d + (pits[pit] if pit else 0.0)
            exc = (delta > hi) | (delta < lo)
            t, tc = float(det.sig(delta)), float(detc.sig(delta))
            if cond(int(exc.sum()), t, tc, thr, thrc) or seed > 2026 + 5000:
                break
            seed += 1
        x1 = base.to_numpy(float)
        x2 = x1 * np.exp(delta)
        people.append({"code": code, "titre": title, "intervention": V.NOMS[iv], "regle": rule, "graine": seed,
                       "marqueurs": [{"id": m, "nom": LABELS[m], "unite": UNITS[m], "b1": float(a), "b2": float(b),
                                      "variation_pct": float(100 * (np.exp(dd) - 1)), "naif": ("hausse" if dd > h else "baisse" if dd < l_ else "")}
                                     for m, a, b, dd, h, l_ in zip(A.P, x1, x2, delta, hi, lo)],
                       "n_naif": int(exc.sum()), "signature": t, "seuil": thr, "signature_contrainte": tc, "seuil_contrainte": thrc,
                       "alerte": t > thr, "alerte_contrainte": tc > thrc})
    return people


def run():
    p = build_people()
    (A.OUT / "demo_personnes.json").write_text(json.dumps(p, indent=1, ensure_ascii=False), encoding="utf-8")
    return p


if __name__ == "__main__":
    run()
