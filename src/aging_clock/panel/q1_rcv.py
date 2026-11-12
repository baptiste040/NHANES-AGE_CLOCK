"""Programme « panel », Q1 : comparaison du changement detectable a 6 mois aux RCV publies (ajout du 2026-11-12).

RCV publie = exp(1,96 * sqrt(2) * sigma) - 1 (hausse) et 1 - exp(-1,96 * sqrt(2) * sigma) (baisse),
sigma = sqrt(ln(1 + CV^2)). Valeurs reprises du tableau de l'audit independant (point 3) :
- Westgard, Desirable Biological Variation Database specifications (Ricos et al., edition 2014) :
  CV = sqrt(CV_I^2 + I^2), I = imprecision desirable ;
- EFLM (meta-analyse a court terme) : CV_A = 0,5 CV_I. Seuls les RCV derives sont publies ici.
Le RCV publie est a court terme : un rapport > 1 au jeu de 2001-2002 ne signale pas une erreur.
"""
from __future__ import annotations

import pandas as pd

from .remesures import OUT

# id : (Westgard hausse, baisse ; EFLM hausse, baisse), en %
RCV = {
    "glu_fast": (19, 16, 16, 14), "hba1c": (6, 6, 4, 4), "tc": (20, 17, 18, 15), "ldl": (27, 21, 27, 21),
    "hdl": (25, 20, 19, 16), "tg_fast": (84, 46, 83, 45), "alt": (81, 45, 47, 32), "ggt": (51, 34, 29, 22),
    "creat": (20, 17, 15, 13), "crp": (246, 71, 182, 65),
}
# Valeurs du depot avant les corrections du 2026-11-12 (tableau de l'audit) : hausse, baisse
AVANT = {"glu_fast": (29, 23), "hba1c": (10, 9), "tc": (26, 21), "ldl": (47, 32), "hdl": (43, 30), "tg_fast": (111, 53),
         "alt": (181, 64), "ggt": (53, 35), "creat": (21, 17), "crp": (351, 78)}


def run() -> pd.DataFrame:
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    cd = cd[cd.groupe == "20-79 ans"].set_index("id")
    rows = []
    for mid, (wh, wb, eh, eb) in RCV.items():
        c = cd.loc[mid]
        rows.append({"id": mid, "marqueur": c.marqueur, "jeu_principal": c.jeu_principal,
                     "cd6m_hausse_avant": AVANT[mid][0], "cd6m_baisse_avant": AVANT[mid][1],
                     "cd6m_hausse": c.cd6m_hausse, "cd6m_baisse": c.cd6m_baisse,
                     "cd6m_hausse_nhanes3": c.get("cd6m_hausse_nhanes3"), "cd6m_hausse_noteC": c.cd6m_hausse_sens_noteC,
                     "rcv_westgard_hausse": wh, "rcv_westgard_baisse": wb, "rcv_eflm_hausse": eh, "rcv_eflm_baisse": eb,
                     "rapport_westgard_hausse_avant": AVANT[mid][0] / wh, "rapport_westgard_hausse": c.cd6m_hausse / wh,
                     "rapport_westgard_baisse": c.cd6m_baisse / wb, "rapport_eflm_hausse": c.cd6m_hausse / eh,
                     "rapport_eflm_baisse": c.cd6m_baisse / eb})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "Q1_comparaison_rcv_publies.csv", index=False)
    return t


if __name__ == "__main__":
    print(run().round(2).to_string())
