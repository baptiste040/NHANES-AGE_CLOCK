"""Programme « panel », Q6 : zones fondees sur le risque de mortalite (protocole : DECISIONS.md,
pre-enregistrement du 2026-11-12).

NHANES 1999-2010 relie aux Linked Mortality Files 2019. Developpement 1999-2006, validation
2007-2010. Cox, splines cubiques restreintes. Ce module contient :
- le chargement et l'harmonisation des methodes (regle de Q5) ;
- un modele de Cox (Breslow) en numpy, verifie contre lifelines ;
- les courbes de HR, zones, seuils, replication, categories D1, sensibilites.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from ..config import ROOT
from ..features import rcs_basis
from ..nhanes import load_mortality
from . import intervalles
from .q2 import SUF, _xpt
from .q5 import EVENTS, FILES, _with_derived, rbf
from .remesures import OUT

CYC = [1999, 2001, 2003, 2005, 2007, 2009]
DEV, VAL = [1999, 2001, 2003, 2005], [2007, 2009]
MORT = ROOT / "data" / "raw"
COT = {1999: "LAB06", 2001: "L06_B", **intervalles.COT}
EXTRA = {  # id : ({cycle: fichier}, [variables])
    "tibc": ({1999: "LAB06", 2001: "L40FE_B", 2003: "L40FE_C", 2005: "FETIB_D"}, ["LBXTIB", "LBDTIB"]),
    "tsat": ({2001: "L40FE_B", 2003: "L40FE_C", 2005: "FETIB_D"}, ["LBDPCT"]),
    "crp": ({1999: "LAB11", 2001: "L11_B", 2003: "L11_C", 2005: "CRP_D", 2007: "CRP_E", 2009: "CRP_F"}, ["LBXCRP"]),
}
HORMONES = {"lh", "fsh", "psa_total", "psa_free", "testo", "shbg", "estradiol", "dheas"}


# ------------------------------------------------------------------ chargement
def load() -> pd.DataFrame:
    frames = []
    for y in CYC:
        s = SUF[y]
        d = _xpt("DEMO" + s, y)[["RIDAGEYR", "RIAGENDR", "RIDEXPRG", "RIDRETH1", "INDFMPIR", "WTMEC2YR"]]
        d = d.join(_xpt(COT[y], y)[["LBXCOT"]], how="left").join(_xpt("BMX" + s, y)[["BMXBMI"]], how="left")
        smq = _xpt("SMQ" + s, y)
        d = d.join(smq[[c for c in ["SMQ020", "SMQ040"] if c in smq]], how="left")
        diq = _xpt("DIQ" + s, y)
        d = d.join(diq[[c for c in ["DIQ010", "DIQ050", "DIQ070"] if c in diq]], how="left")
        mcq = _xpt("MCQ" + s, y)
        d = d.join(mcq[[c for c in ["MCQ160B", "MCQ160C", "MCQ160D", "MCQ160E", "MCQ160F", "MCQ160L", "MCQ220"] if c in mcq]], how="left")
        try:
            kiq = _xpt("KIQ_U" + s, y)
        except Exception:  # 1999-2000 : fichier KIQ
            kiq = _xpt("KIQ" + s, y)
        d = d.join(kiq[[c for c in ["KIQ022"] if c in kiq]], how="left")
        bpq = _xpt("BPQ" + s, y)
        d = d.join(bpq[[c for c in ["BPQ050A", "BPQ100D"] if c in bpq]], how="left")
        cache = {}
        for mid, (files, cands) in {**FILES, **EXTRA}.items():
            if y not in files:
                continue
            f = files[y]
            if f not in cache:
                cache[f] = _xpt(f, y)
            x = cache[f]
            v = next((c for c in cands if c in x), None)
            if v is not None:
                d[mid] = x[v].reindex(d.index)
            if mid == "glu_fast" and "WTSAF2YR" in x:
                d["WTSAF2YR"] = x["WTSAF2YR"].reindex(d.index)
        m = load_mortality(MORT / f"NHANES_{y}_{y + 1}_MORT_2019_PUBLIC.dat")
        d = d.join(m, how="left")
        d["cycle"] = y
        frames.append(d)
    d = pd.concat(frames)
    for c in ["DIQ050", "DIQ070", "BPQ100D", "MCQ160L", "SMQ040", "WTSAF2YR", "KIQ022"]:
        if c not in d:
            d[c] = np.nan
    return d.rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})


# ------------------------------------------------------------------ harmonisation des methodes
# Regle (pre-enregistree) : pour chaque evenement de Q5 entre 1999 et 2010, (i) equation publiee et
# donnees diffusees non ajustees -> equation appliquee aux cycles anterieurs, enchainee jusqu'a la
# methode de 2009-2010 ; (ii) sinon, si le decalage empirique de Q5 (b) vaut >= 0,5 changement
# detectable, restriction aux cycles posterieurs ; (iii) sinon, aucune correction.
APPLY = {  # id : [(numero d'evenement, cycles transformes)]
    "creat": [("1", [1999]), ("2", [2005])],
    "glu_fast": [("6", [1999, 2001, 2003]), ("7", [1999, 2001, 2003, 2005])],
    "insulin": [("9", [1999, 2001]), ("10", [1999, 2001, 2003])],
    "hdl": [("13", [1999, 2001, 2003, 2005])],
    "ferritin": [("18", [1999, 2001, 2005, 2007])],
    "apob": [("25", [2005])],
    "u_creat": [("31", [1999, 2001, 2003, 2005])],
}
RESTRICT = {"alp": [2003, 2005, 2007, 2009], "bili": [2003, 2005, 2007, 2009]}  # evenement 4 (ratio 0,77 et 0,90)


def harmonise(d: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    d = d.copy()
    log = []
    ev = {e[0]: e for e in EVENTS}
    for mid, steps in APPLY.items():
        if mid not in d:
            continue
        for num, cycles in steps:
            f = ev[num][4][mid]
            m = d.cycle.isin(cycles) & d[mid].notna()
            d.loc[m, mid] = f(d.loc[m, mid].to_numpy(float))
            log.append({"id": mid, "evenement": num, "action": "équation de passage", "cycles": cycles, "n": int(m.sum())})
    # folates erythrocytaires : algorithme du NCHS (evenement 22), cycles <= 2005
    m = d.cycle.isin([1999, 2001, 2003, 2005]) & d.rbc_folate.notna() & d.fol_serum.notna() & d.hct.notna()
    d.loc[m, "rbc_folate"] = rbf(d.loc[m]).to_numpy(float)
    d.loc[d.cycle.isin([1999, 2001, 2003, 2005]) & ~m, "rbc_folate"] = np.nan
    log.append({"id": "rbc_folate", "evenement": "22", "action": "algorithme NCHS (BR -> MA)", "cycles": [1999, 2001, 2003, 2005],
                "n": int(m.sum())})
    for mid, keep in RESTRICT.items():
        m = ~d.cycle.isin(keep) & d[mid].notna()
        d.loc[m, mid] = np.nan
        log.append({"id": mid, "evenement": "4", "action": "restriction de cycles", "cycles": keep, "n_retires": int(m.sum())})
    d["globulin"] = d.protein - d.albumin
    for c in ["neut", "lymph", "mono", "eos", "baso"]:
        d[f"{c}_n"] = d.wbc * d[f"{c}_pct"] / 100
    d = _with_derived(d)
    return d, log


def population(d: pd.DataFrame) -> pd.DataFrame:
    """Adultes 20-79 ans, non enceintes, eligibles au couplage, suivi connu."""
    return d[d.age.between(20, 79) & (d.RIDEXPRG != 1) & (d.ELIGSTAT == 1) & d.PERMTH_EXM.notna() & d.MORTSTAT.notna()].copy()


def panel_ids() -> list[str]:
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    return [i for i in cd[cd.groupe == "20-79 ans"].id.drop_duplicates() if i not in HORMONES]


def deaths_by_marker(p: pd.DataFrame, ids) -> pd.DataFrame:
    rows = []
    fast = {"glu_fast", "insulin", "tg_fast", "ldl", "homa_ir", "quicki", "tyg", "tg_hdl", "aip", "ldl_hdl"}
    for mid in ids:
        if mid not in p:
            rows.append({"id": mid, "present_1999_2010": False})
            continue
        q = p[p[mid].notna()]
        if mid in fast:
            q = q[q.WTSAF2YR.notna() & (q.WTSAF2YR > 0)]
        dv, vl = q[q.cycle.isin(DEV)], q[q.cycle.isin(VAL)]
        rows.append({"id": mid, "present_1999_2010": len(q) > 0, "cycles": " ".join(str(c) for c in sorted(q.cycle.unique())),
                     "n": len(q), "deces": int(q.MORTSTAT.sum()), "n_dev": len(dv), "deces_dev": int(dv.MORTSTAT.sum()),
                     "n_val": len(vl), "deces_val": int(vl.MORTSTAT.sum())})
    return pd.DataFrame(rows)
