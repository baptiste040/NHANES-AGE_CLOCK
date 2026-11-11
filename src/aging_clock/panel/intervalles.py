"""Programme « panel », table D1 : intervalles de reference statistiques calcules sur NHANES
(methode CLSI EP28-A3c), et seuils de decision clinique (sources lues). Protocole : DECISIONS.md.

Population de reference (definie a l'avance) : adultes de 20 a 79 ans, NHANES 2003-2010 (cycles
distincts des jeux de remesures de Q4 : 2001-2002 et NHANES III), non-fumeurs (cotinine
< 3 ng/mL, Benowitz 2009), sans diabete, maladie cardiovasculaire, renale, hepatique ni cancer
declares, sans traitement antidiabetique, antihypertenseur ni hypolipemiant declare, IMC de 18,5
a 30, femmes non enceintes.
Intervalles non parametriques (2,5e et 97,5e centiles) par sexe, IC 90 % des bornes par bootstrap
(2 000 tirages). Partition par tranche d'age (20-39, 40-59, 60-79) si, pour une tranche, la part de
ses valeurs au-dela d'une borne commune au sexe est < 1 % ou > 5 % (idee de Harris et Boyd, decrite
par Lahti 2004 ; seuils 1 % et 5 % choisis ici), et si chaque tranche compte au moins 120 personnes.
Cycles : 2003-2010 pour tous les marqueurs (avant le changement d'automate de la numeration en
2012, des instruments de biochimie en 2017 et le passage a la hs-CRP en 2015), sauf folates
erythrocytaires et B12 : 2003-2006 (changements de methode en 2007 et 2011).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from ..config import ROOT
from ..nhanes import download, read_xpt

RAW = ROOT / "data" / "raw" / "panel"
OUT = ROOT / "reports" / "panel"
URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{y}/DataFiles/{f}.xpt"
SUF = {2003: "_C", 2005: "_D", 2007: "_E", 2009: "_F"}
SEED, N_BOOT = 2026, 2000

# Fichiers de laboratoire par cycle (variable NHANES -> id du marqueur, unite des jeux de Q4)
LAB = {
    "cbc": ({2003: "L25_C", 2005: "CBC_D", 2007: "CBC_E", 2009: "CBC_F"},
            {"LBXWBCSI": "wbc", "LBXNEPCT": "neut_pct", "LBXLYPCT": "lymph_pct", "LBXMOPCT": "mono_pct",
             "LBXEOPCT": "eos_pct", "LBXBAPCT": "baso_pct", "LBXRBCSI": "rbc", "LBXHGB": "hb", "LBXHCT": "hct",
             "LBXMCVSI": "mcv", "LBXMCHSI": "mch", "LBXMC": "mchc", "LBXRDW": "rdw", "LBXPLTSI": "plt", "LBXMPSI": "mpv"}),
    "bio": ({2003: "L40_C", 2005: "BIOPRO_D", 2007: "BIOPRO_E", 2009: "BIOPRO_F"},
            {"LBXSATSI": "alt", "LBXSASSI": "ast", "LBXSGTSI": "ggt", "LBXSAPSI": "alp", "LBXSTB": "bili",
             "LBXSAL": "albumin", "LBXSTP": "protein", "LBXSGB": "globulin", "LBXSCR": "creat", "LBXSBU": "urea",
             "LBXSNASI": "na", "LBXSKSI": "k", "LBXSCLSI": "cl", "LBXSC3SI": "hco3", "LBXSOSSI": "osmo",
             "LBXSCA": "ca", "LBXSIR": "iron", "LBXSUA": "urate", "LBXSPH": "phos"}),
    "tc": ({2003: "l13_c", 2005: "TCHOL_D", 2007: "TCHOL_E", 2009: "TCHOL_F"}, {"LBXTC": "tc"}),
    "hdl": ({2003: "l13_c", 2005: "HDL_D", 2007: "HDL_E", 2009: "HDL_F"}, {"LBXHDD": "hdl", "LBDHDD": "hdl"}),
    "ins": ({2003: "L10AM_C", 2005: "GLU_D", 2007: "GLU_E", 2009: "GLU_F"}, {"LBXIN": "insulin"}),
    "crp": ({2003: "L11_C", 2005: "CRP_D", 2007: "CRP_E", 2009: "CRP_F"}, {"LBXCRP": "crp"}),
    "b12fol": ({2003: "L06NB_C", 2005: "B12_D"}, {"LBXB12": "b12"}),
    "fol": ({2003: "L06NB_C", 2005: "FOLATE_D"}, {"LBXRBF": "rbc_folate"}),
    "fer": ({2005: "FERTIN_D", 2007: "FERTIN_E", 2009: "FERTIN_F"}, {"LBXFER": "ferritin"}),
    "fe": ({2003: "L40FE_C", 2005: "FETIB_D"}, {"LBXTIB": "tibc", "LBDPCT": "tsat"}),
    "hcy": ({2003: "L06MH_C", 2005: "HCY_D"}, {"LBXHCY": "hcy"}),
    "apob": ({2005: "TRIGLY_D", 2007: "ApoB_E", 2009: "ApoB_F"}, {"LBXAPB": "apob"}),
}
COT = {2003: "L06COT_C", 2005: "COT_D", 2007: "COTNAL_E", 2009: "COTNAL_F"}

# Seuils de decision clinique (type R), unites des jeux de Q4. variante : None = principal
CLINICAL = [
    # id, sens, seuil, variante, libelle, source (lue)
    ("glu_fast", "haut", 110.0, "OMS", "≥ 6,1 mmol/L (110 mg/dL)", "OMS 2006 (recommandation 4) ; ESC 2023 diabète, tableau 6"),
    ("glu_fast", "haut", 100.0, "ADA", "≥ 5,6 mmol/L (100 mg/dL)", "ADA (2021), rapporté par ESC 2023 diabète, tableau 6"),
    ("hba1c", "haut", 6.0, "OMS", "≥ 6,0 %", "OMS (2011, 2019), rapporté par ESC 2023 diabète, tableau 6"),
    ("hba1c", "haut", 5.7, "ADA", "≥ 5,7 %", "ADA (2021), rapporté par ESC 2023 diabète, tableau 6"),
    ("ldl", "haut", 116.0, None, "≥ 3,0 mmol/L (116 mg/dL), objectif du risque faible", "ESC/EAS 2019, objectifs de traitement"),
    ("non_hdl", "haut", 130.0, None, "≥ 3,4 mmol/L (130 mg/dL), objectif du risque modéré", "ESC/EAS 2019, objectifs secondaires"),
    ("tg_fast", "haut", 150.0, None, "≥ 1,7 mmol/L (150 mg/dL)", "ESC/EAS 2019 (« < 1,7 mmol/L indique un risque plus faible »)"),
    ("tg_serum", "haut", 150.0, None, "≥ 1,7 mmol/L (150 mg/dL), non à jeun", "ESC/EAS 2019"),
    ("egfr", "bas", 60.0, None, "< 60 mL/min/1,73 m² (G3a et au-delà)", "KDIGO 2024, catégories G"),
    ("acr", "haut", 30.0, None, "≥ 3 mg/mmol (30 mg/g), A2", "KDIGO 2024, catégories A"),
    ("vitd", "bas", 20.0, None, "< 20 ng/mL (50 nmol/L)", "Endocrine Society 2011, recommandation 1.2"),
    ("vitd", "bas", 30.0, "sensibilité 30", "< 30 ng/mL (75 nmol/L)", "Endocrine Society 2011, recommandation 2.1 (cible)"),
]
STAT_IDS = ["wbc", "neut_pct", "lymph_pct", "mono_pct", "eos_pct", "baso_pct", "rbc", "hb", "hct", "mcv", "mch", "mchc", "rdw",
            "plt", "mpv", "insulin", "tc", "hdl", "alt", "ast", "ggt", "alp", "bili", "albumin", "protein", "globulin", "creat",
            "urea", "na", "k", "cl", "hco3", "osmo", "ca", "iron", "urate", "phos", "crp", "b12", "rbc_folate", "ferritin",
            "tibc", "tsat", "hcy", "apob"]
EXCLUS = {
    "Lp(a), ApoA1": "pas de mesure dans NHANES 2003-2010 (NHANES III seulement, qui sert de jeu de test)",
    "Sélénium, iode urinaire": "pas de mesure dans NHANES 2003-2010 chez tous les adultes",
    "LH, FSH, PSA": "intervalles dépendant du sexe, du cycle ou de l'âge, hors population de référence générale",
    "Albumine et créatinine urinaires brutes": "concentrations brutes sans intervalle interprétable ; seul le rapport (KDIGO) est utilisé",
    "Glucose sérique non à jeun": "aucun seuil de décision lu pour une glycémie non à jeun",
    "CRP (seuil de risque)": "seuils de risque AHA/CDC 2003 non lus (accès refusé) : seul l'intervalle statistique est utilisé",
    "Indices dérivés (HOMA-IR, TyG, rapports, FIB-4, NLR, SII…)": "aucun seuil lu ; non calculés comme intervalles dans ce protocole",
}


def _xpt(f, y):
    p = RAW / f"{y}_{f}.xpt"
    download(URL.format(y=y, f=f), p)
    return read_xpt(p).set_index("SEQN")


def reference_population() -> pd.DataFrame:
    frames = []
    for y, s in SUF.items():
        d = _xpt("DEMO" + s, y)[["RIDAGEYR", "RIAGENDR", "RIDEXPRG"]]
        d = d.join(_xpt(COT[y], y)[["LBXCOT"]], how="left")
        d = d.join(_xpt("BMX" + s, y)[["BMXBMI"]], how="left")
        diq = _xpt("DIQ" + s, y)
        d = d.join(diq[[c for c in ["DIQ010", "DIQ050", "DIQ070"] if c in diq]], how="left")
        mcq = _xpt("MCQ" + s, y)
        d = d.join(mcq[[c for c in ["MCQ160B", "MCQ160C", "MCQ160D", "MCQ160E", "MCQ160F", "MCQ160L", "MCQ220"] if c in mcq]], how="left")
        d = d.join(_xpt("KIQ_U" + s, y)[["KIQ022"]], how="left")
        bpq = _xpt("BPQ" + s, y)
        d = d.join(bpq[[c for c in ["BPQ050A", "BPQ100D"] if c in bpq]], how="left")
        d["cycle"] = y
        frames.append(d)
    d = pd.concat(frames)
    flow = [("adultes 20-79 ans, NHANES 2003-2010", int(d.RIDAGEYR.between(20, 79).sum()))]
    keep = d.RIDAGEYR.between(20, 79)
    rules = [("non enceintes", d.RIDEXPRG != 1),
             ("non-fumeurs (cotinine < 3 ng/mL)", d.LBXCOT < 3),
             ("IMC 18,5-30", d.BMXBMI.between(18.5, 30)),
             ("sans diabète ni traitement antidiabétique", (d.DIQ010 != 1) & (d.DIQ050 != 1) & (d.DIQ070 != 1)),
             ("sans maladie cardiovasculaire déclarée", ~(d[["MCQ160B", "MCQ160C", "MCQ160D", "MCQ160E", "MCQ160F"]] == 1).any(axis=1)),
             ("sans maladie hépatique déclarée", d.MCQ160L != 1),
             ("sans cancer déclaré", d.MCQ220 != 1),
             ("sans maladie rénale déclarée", d.KIQ022 != 1),
             ("sans antihypertenseur ni hypolipémiant déclaré", (d.BPQ050A != 1) & (d.BPQ100D != 1))]
    for lab, m in rules:
        keep &= m.fillna(False) if lab.startswith("non-fumeurs") or lab.startswith("IMC") else m.fillna(True)
        flow.append((lab, int(keep.sum())))
    ref = d[keep].rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})[["age", "sex", "cycle"]]
    for key, (files, vars_) in LAB.items():
        parts = []
        for y, f in files.items():
            x = _xpt(f, y)
            cols = {v: i for v, i in vars_.items() if v in x}
            parts.append(x[list(cols)].rename(columns=cols))
        lab = pd.concat(parts)
        lab = lab.T.groupby(level=0).first().T if lab.columns.duplicated().any() else lab
        ref = ref.join(lab, how="left")
    return ref, flow


def _limits(x, seed=SEED):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    lo, hi = np.percentile(x, [2.5, 97.5])
    rng = np.random.default_rng(seed)
    b = np.array([np.percentile(x[rng.integers(0, len(x), len(x))], [2.5, 97.5]) for _ in range(N_BOOT)])
    return {"n": len(x), "borne_basse": float(lo), "borne_haute": float(hi),
            "ic90_basse": [float(np.quantile(b[:, 0], .05)), float(np.quantile(b[:, 0], .95))],
            "ic90_haute": [float(np.quantile(b[:, 1], .05)), float(np.quantile(b[:, 1], .95))]}


BANDS = [(20, 39), (40, 59), (60, 79)]


def statistical_intervals(ref: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mid in STAT_IDS:
        if mid not in ref:
            continue
        for sex in (1, 2):
            g = ref[(ref.sex == sex) & ref[mid].notna()]
            if len(g) < 120:
                continue
            comb = _limits(g[mid])
            part = False
            props = {}
            for a, b in BANDS:
                gb = g[g.age.between(a, b)][mid]
                if len(gb) < 120:
                    props = None
                    break
                pl, ph = float((gb < comb["borne_basse"]).mean()), float((gb > comb["borne_haute"]).mean())
                props[f"{a}-{b}"] = (pl, ph)
                if not (0.01 <= pl <= 0.05 and 0.01 <= ph <= 0.05):
                    part = True
            cycles = " ".join(str(c) for c in sorted(g.cycle.unique()))
            if part and props:
                for a, b in BANDS:
                    r = _limits(g[g.age.between(a, b)][mid])
                    rows.append({"id": mid, "sexe": "H" if sex == 1 else "F", "age_min": a, "age_max": b, **r, "cycles": cycles,
                                 "partition_age": True})
            else:
                rows.append({"id": mid, "sexe": "H" if sex == 1 else "F", "age_min": 20, "age_max": 79, **comb, "cycles": cycles,
                             "partition_age": False})
    return pd.DataFrame(rows)


def run() -> pd.DataFrame:
    OUT.mkdir(parents=True, exist_ok=True)
    ref, flow = reference_population()
    t = statistical_intervals(ref)
    t.to_csv(OUT / "D1_intervalles_statistiques.csv", index=False)
    pd.DataFrame(CLINICAL, columns=["id", "sens", "seuil", "variante", "libelle", "source"]).to_csv(OUT / "D1_seuils_cliniques.csv", index=False)
    (OUT / "D1_population_reference.json").write_text(json.dumps({"flux": flow, "exclus_de_q4": EXCLUS}, indent=1, ensure_ascii=False), encoding="utf-8")
    return t
