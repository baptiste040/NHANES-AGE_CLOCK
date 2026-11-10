"""Piste « suivi » : reprise de Q1 et Q2 avec le modele « sang seul contraint » (analyse
secondaire, protocole : DECISIONS.md). Memes definitions et memes regles que Q1-Q2 ; seul le
modele change. Les resultats pre-enregistres (modele non contraint) ne sont pas modifies.

NHANES III a deja ete consulte pour Q1-Q2 avec le modele non contraint : evaluation non aveugle.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from . import retest as r
from . import suivi as s
from .contrainte import ConstrainedClock

M_C = "sang_contraint"
PRED = s.OUT / "Q1_Q2_contraint_predictions.json"
RES = s.OUT / "Q1_Q2_contraint_nhanes3.json"


class ModelsC(s.Models):
    """Ajoute le modele « sang seul contraint » (memes coefficients que « sang », contrainte
    clinique appliquee a chaque prediction, y compris pour les contributions des moteurs)."""

    def __init__(self):
        super().__init__()
        self.clocks[M_C] = ConstrainedClock(self.clocks["sang"])
        self.vars[M_C] = self.vars["sang"]
        self.dev_gaps[M_C] = self.gaps(M_C, self.dev)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _block(M, e1, e2, rho, rho_s=None, nh3=False):
    per, thr, g1, g2 = s.q1_metrics(M, M_C, e1, e2)
    if rho_s is None:
        rho_s = {k: r.icc_a1(g1[k], g2[k]) for k in s.SCORES}
    tag = "nh3" if nh3 else "2001"
    per.to_csv(s.OUT / f"Q1_paires_{tag}_{M_C}.csv", index=False)
    mk, q2 = s.q2_metrics(M, M_C, e1, e2, rho, rho_score=rho_s)
    mk.to_csv(s.OUT / f"Q2_marqueurs_{tag}_{M_C}.csv", index=False)
    out = {"seuils": thr, "stabilite": s.rates_with_ci(per),
           "n_moteurs_tous": per["n_moteurs_tous_1"].value_counts().sort_index().to_dict(),
           "n_moteurs_actionnables": per["n_moteurs_actionnables_1"].value_counts().sort_index().to_dict(),
           "q2": s.summarise_q2(q2), "cci_score_2001": rho_s}
    if nh3:
        out["stabilite_par_tertile"] = {f"tertile_ecart_global_1={lvl}": s.rates_with_ci(
            per[per["tertile_ecart_global_1"] == lvl]) for lvl in sorted(per["tertile_ecart_global_1"].unique())}
        _, q2c = s.q2_metrics(M, M_C, e1, e2, rho, which="centiles", rho_score=rho_s)
        _, q2i = s.q2_metrics(M, M_C, e1, e2, rho, target="interne", rho_score=rho_s)
        out["q2_seuils_centiles"], out["q2_moyenne_interne"] = s.summarise_q2(q2c), s.summarise_q2(q2i)
    return out


def predictions() -> Path:
    """Calage sur 2001-2002 seulement (a commiter avant l'analyse NHANES III)."""
    M = ModelsC()
    e1, e2 = s.pairs_2001(M)
    rho = s.iccs_2001(e1, e2)
    res = {"n": len(e1), "cci_log_2001": rho, "modeles": {M_C: _block(M, e1, e2, rho)},
           "sha256_code": _sha(Path(__file__))}
    PRED.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return PRED


def analyse() -> Path:
    pred = json.loads(PRED.read_text(encoding="utf-8"))
    M = ModelsC()
    e1, e2 = s.pairs_nh3(M)
    rho = {k: float(v) for k, v in pred["cci_log_2001"].items()}
    rho_s = {k: float(v) for k, v in pred["modeles"][M_C]["cci_score_2001"].items()}
    res = {"n": len(e1), "modeles": {M_C: _block(M, e1, e2, rho, rho_s, nh3=True)},
           "sha256_code": _sha(Path(__file__))}
    RES.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    return RES


def comparison() -> "pd.DataFrame":  # noqa: F821
    """Tableau « non contraint (pre-enregistre) / contraint » : seuils et stabilite, NHANES III."""
    import pandas as pd
    U = json.loads((s.OUT / "Q1_Q2_nhanes3.json").read_text(encoding="utf-8"))["modeles"]["sang"]
    Pu = json.loads(s.PRED.read_text(encoding="utf-8"))["modeles"]["sang"]
    C = json.loads(RES.read_text(encoding="utf-8"))["modeles"][M_C]
    Pc = json.loads(PRED.read_text(encoding="utf-8"))["modeles"][M_C]
    rows = []
    for k in s.SCORES:
        rows.append({"indicateur": f"seuil_P95_{k}", "pred_libre": Pu["seuils"][k]["p95_abs_d"],
                     "libre": U["seuils"][k]["p95_abs_d"], "libre_ic95": U["seuils"][k]["p95_ic95"],
                     "pred_contraint": Pc["seuils"][k]["p95_abs_d"],
                     "contraint": C["seuils"][k]["p95_abs_d"], "contraint_ic95": C["seuils"][k]["p95_ic95"]})
    for k in s.RATES:
        rows.append({"indicateur": k, "pred_libre": Pu["stabilite"][k]["taux"],
                     "libre": U["stabilite"][k]["taux"], "libre_ic95": U["stabilite"][k]["ic95"],
                     "pred_contraint": Pc["stabilite"][k]["taux"],
                     "contraint": C["stabilite"][k]["taux"], "contraint_ic95": C["stabilite"][k]["ic95"]})
    t = pd.DataFrame(rows)
    t.to_csv(s.OUT / "Q1_comparaison_libre_contraint.csv", index=False)
    return t


if __name__ == "__main__":
    import sys
    {"predictions": predictions, "analyse": analyse, "comparaison": comparison}[sys.argv[1]]()
