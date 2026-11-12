"""Programme « panel », Q4 : tableau du rapport et chiffres de synthese, generes depuis les CSV.

Ajoute le 2026-11-12 (corrections d'erreurs apres audit) : le tableau etait recopie a la main.
Changement detectable « limites / nettes » et variance de bruit du modele binormal : autre jeu.
"""
from __future__ import annotations

import ast

import numpy as np
import pandas as pd

from .remesures import DERIVED, LABEL, OUT

LAB = LABEL | {d[0]: d[1] for d in DERIVED} | {"acr": "Rapport albumine/créatinine urinaire", "egfr": "DFGe (CKD-EPI 2021)"}
ORDER = {"anomalie isolée peu informative": 0, "confirmer avant de signaler": 1, "normalisation < 30 %": 2}


def _p(x, d=0):
    return "—" if x is None or not np.isfinite(x) else f"{100 * x:.{d}f} %".replace(".", ",")


def _lst(s):
    return ast.literal_eval(s) if isinstance(s, str) else s


def table() -> tuple[str, dict]:
    s = pd.read_csv(OUT / "Q4_synthese.csv")
    t3 = pd.read_csv(OUT / "Q4_normalisation_nhanes3.csv")
    t1 = pd.read_csv(OUT / "Q4_normalisation_2001.csv")
    key = ["id", "type", "variante"]
    a3 = t3[t3.cote == "tous"].set_index(key)
    a1 = t1[t1.cote == "tous"].set_index(key)
    rows = []
    for _, r in s.iterrows():
        k = (r.id, r.type, r.variante)
        x3 = a3.loc[k] if k in a3.index else None
        x1 = a1.loc[k] if k in a1.index else None
        p1 = x1.part_anormaux_1 if x1 is not None else np.nan
        p3 = x3.part_anormaux_1 if x3 is not None else np.nan
        warn = " ⚠" if r.type == "S" and np.isfinite(p3) and p3 > 0.15 else ""
        name = LAB.get(r.id, r.id) + ("" if r.variante == "principal" else f" ({r.variante})")
        lim = f"{_p(x3.taux_limites)} / {_p(x3.taux_nettes)}" if x3 is not None else "— / —"
        att = f"{_p(x3.attendu_bruit_limites)} / {_p(x3.attendu_bruit_nettes)}" if x3 is not None else "— / —"
        comp = "—" if pd.isna(r.compatible) else ("oui" if r.compatible in (True, "True") else "non")
        concl = r.conclusion + (f" ({r.statut})" if isinstance(r.statut, str) and r.statut else "")
        n1 = "—" if not np.isfinite(r.n_2001) or r.n_2001 == 0 else int(r.n_2001)
        n3 = "—" if not np.isfinite(r.n_nh3) or r.n_nh3 == 0 else int(r.n_nh3)
        rows.append((0 if r.type == "R" else 1, ORDER.get(r.conclusion, 3), name,
                     f"| {name} | {r.type} | {_p(p1)} / {_p(p3)}{warn} | {_p(r.taux_2001)} (n={n1}) | **{_p(r.taux_nh3)}** (n={n3}) | "
                     f"{_p(r.attendu_bruit_nh3)} | {lim} | {att} | {comp} | {concl} |"))
    rows.sort(key=lambda z: (z[0], z[1], z[2]) if z[0] == 1 else (z[0], 0, ""))
    head = ("| Marqueur | Type | Part anormaux | Normalisation 2001-02 (prédiction) | **Normalisation NHANES III** | "
            "Attendu sous le bruit | Limites / nettes (observé) | Limites / nettes (attendu sous le bruit) | Compatible | Conclusion (règle) |\n"
            "|---|---|---|---|---|---|---|---|---|---|")
    md = head + "\n" + "\n".join(z[3] for z in rows)
    # chiffres de synthese (couples avec au moins 20 anomalies dans la classe)
    stats = {}
    for jeu, t in (("nhanes3", t3), ("2001", t1)):
        a = t[t.cote == "tous"]
        lim, net = a[a.n_limites >= 20], a[a.n_nettes >= 20]
        ok = a[a.n_anormaux_1 >= 20]
        stats[jeu] = {
            "n_couples_limites": len(lim), "mediane_limites": float(lim.taux_limites.median()),
            "mediane_limites_attendu": float(lim.attendu_bruit_limites.median()),
            "n_couples_nettes": len(net), "mediane_nettes": float(net.taux_nettes.median()),
            "mediane_nettes_attendu": float(net.attendu_bruit_nettes.median()),
            "part_ecart_moins_10": float((abs(ok.taux_normalisation - ok.attendu_bruit) < 0.10).mean()),
            "ecart_median_points": float(100 * (ok.taux_normalisation - ok.attendu_bruit).median()),
            "nettes_au_dessus_attendu_5pts": int((net.taux_nettes - net.attendu_bruit_nettes > 0.05).sum()),
        }
    cnt = s.conclusion.value_counts().to_dict()
    both = s[s.statut == "deux jeux"].conclusion.value_counts().to_dict()
    stats["bilan"] = {"total": int(len(s)), **{k: int(v) for k, v in cnt.items()}, "deux_jeux": {k: int(v) for k, v in both.items()}}
    stats["prediction"] = {"compatibles": int((s.compatible.astype(str) == "True").sum()),
                           "testables": int(s.compatible.notna().sum())}
    return md, stats


if __name__ == "__main__":
    md, st = table()
    print(md)
    print(st)
