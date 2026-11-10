"""Programme « panel », Q1 partie A : variabilite observee sur les remesures a ~2 semaines.

Deux jeux analyses separement : NHANES 2001-2002 (second examen) et NHANES III (second examen).
Adultes de 20 a 79 ans, hors femmes enceintes, valeur aux deux examens.
Echelle log sauf marqueurs pouvant valoir 0 (echelle additive). Protocole : DECISIONS.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .. import nhanes3 as n3
from ..config import ROOT
from ..nhanes import download, read_xpt

RAW = ROOT / "data" / "raw" / "panel"
OUT = ROOT / "reports" / "panel"
URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2001/DataFiles/{f}.xpt"
SEED, N_BOOT = 2026, 2000

# id, libelle, (2001 : fichier 1, variable 1, fichier 2, variable 2), (NHANES III : var 1, var 2)
PAIRS = [
    ("wbc", "Leucocytes", ("L25_B", "LBXWBCSI", "l25_2_b", "LB2WBCSI"), ("WCPSI", "WCRSI")),
    ("neut_pct", "Neutrophiles (%)", ("L25_B", "LBXNEPCT", "l25_2_b", "LB2NEPCT"), ("GRPDIF", "GRRDIF")),
    ("neut_n", "Neutrophiles (nombre)", ("L25_B", "LBDNENO", "l25_2_b", "LB2NENO"), None),
    ("gran_pct", "Granulocytes (%, automate)", None, ("GRPPCNT", "GRRPCNT")),
    ("lymph_pct", "Lymphocytes (%)", ("L25_B", "LBXLYPCT", "l25_2_b", "LB2LYPCT"), ("LMPPCNT", "LMRPCNT")),
    ("lymph_n", "Lymphocytes (nombre)", ("L25_B", "LBDLYMNO", "l25_2_b", "LB2LYMNO"), ("LMP", "LMR")),
    ("mono_pct", "Monocytes (%)", ("L25_B", "LBXMOPCT", "l25_2_b", "LB2MOPCT"), ("MOPDIF", "MORDIF")),
    ("mono_n", "Monocytes (nombre)", ("L25_B", "LBDMONO", "l25_2_b", "LB2MONO"), None),
    ("eos_pct", "Éosinophiles (%)", ("L25_B", "LBXEOPCT", "l25_2_b", "LB2EOPCT"), ("EOP", "EOR")),
    ("eos_n", "Éosinophiles (nombre)", ("L25_B", "LBDEONO", "l25_2_b", "LB2EONO"), None),
    ("baso_pct", "Basophiles (%)", ("L25_B", "LBXBAPCT", "l25_2_b", "LB2BAPCT"), ("BOP", "BOR")),
    ("baso_n", "Basophiles (nombre)", ("L25_B", "LBDBANO", "l25_2_b", "LB2BANO"), None),
    ("rbc", "Hématies", ("L25_B", "LBXRBCSI", "l25_2_b", "LB2RBCSI"), ("RCPSI", "RCRSI")),
    ("hb", "Hémoglobine", ("L25_B", "LBXHGB", "l25_2_b", "LB2HGB"), ("HGP", "HGR")),
    ("hct", "Hématocrite", ("L25_B", "LBXHCT", "l25_2_b", "LB2HCT"), ("HTP", "HTR")),
    ("mcv", "VGM", ("L25_B", "LBXMCVSI", "l25_2_b", "LB2MCVSI"), ("MVPSI", "MVRSI")),
    ("mch", "TCMH", ("L25_B", "LBXMCHSI", "l25_2_b", "LB2MCHSI"), ("MCPSI", "MCRSI")),
    ("mchc", "CCMH", ("L25_B", "LBXMC", "l25_2_b", "LB2MC"), ("MHP", "MHR")),
    ("rdw", "RDW", ("L25_B", "LBXRDW", "l25_2_b", "LB2RDW"), ("RWP", "RWR")),
    ("plt", "Plaquettes", ("L25_B", "LBXPLTSI", "l25_2_b", "LB2PLTSI"), ("PLPSI", "PLRSI")),
    ("mpv", "VPM", ("L25_B", "LBXMPSI", "l25_2_b", "LB2MPSI"), ("PVPSI", "PVRSI")),
    ("glu_fast", "Glycémie à jeun (plasma)", ("L10AM_B", "LBXGLU", "L10_2_B", "LB2GLU"), ("G1P", "G1R")),
    ("glu_serum", "Glucose sérique (non à jeun)", ("L40_B", "LBXSGL", "L40_2_B", "LB2SGL"), ("SGP", "SGR")),
    ("insulin", "Insuline (à jeun)", ("L10AM_B", "LBXIN", "L10_2_B", "LB2IN"), ("I1P", "I1R")),
    ("hba1c", "HbA1c", ("L10_B", "LBXGH", "L10_2_B", "LB2GH"), ("GHP", "GHR")),
    ("tc", "Cholestérol total", ("l13_b", "LBXTC", "l13_2_b", "LB2TC"), ("TCP", "TCR")),
    ("ldl", "LDL (calculé, à jeun)", ("L13AM_B", "LBDLDL", "l13_2_b", "LB2LDL"), ("LCP", "LCR")),
    ("hdl", "HDL", ("l13_b", "LBDHDL", "l13_2_b", "LB2HDL"), ("HDP", "HDR")),
    ("tg_fast", "Triglycérides (à jeun)", ("L13AM_B", "LBXTR", "l13_2_b", "LB2TR"), ("TGP", "TGR")),
    ("tg_serum", "Triglycérides sériques (non à jeun)", ("L40_B", "LBXSTR", "L40_2_B", "LB2STR"), ("TRP", "TRR")),
    ("alt", "ALAT", ("L40_B", "LBXSATSI", "L40_2_B", "LB2SATSI"), ("ATPSI", "ATRSI")),
    ("ast", "ASAT", ("L40_B", "LBXSASSI", "L40_2_B", "LB2SASSI"), ("ASPSI", "ASRSI")),
    ("ggt", "GGT", ("L40_B", "LBXSGTSI", "L40_2_B", "LB2SGTSI"), ("GGPSI", "GGRSI")),
    ("alp", "PAL", ("L40_B", "LBDSAPSI", "L40_2_B", "LB2SAPSI"), ("APPSI", "APRSI")),
    ("bili", "Bilirubine totale", ("L40_B", "LBDSTB", "L40_2_B", "LB2STB"), ("TBP", "TBR")),
    ("albumin", "Albumine", ("L40_B", "LBXSAL", "L40_2_B", "LB2SAL"), ("AMP", "AMR")),
    ("protein", "Protéines totales", ("L40_B", "LBXSTP", "L40_2_B", "LB2STP"), ("TPP", "TPR")),
    ("globulin", "Globulines", None, ("GBP", "GBR")),
    ("creat", "Créatinine", ("L40_B", "LBDSCR", "L40_2_B", "LB2SCR"), ("CEP", "CER")),
    ("urea", "Urée", ("L40_B", "LBXSBU", "L40_2_B", "LB2SBU"), ("BUP", "BUR")),
    ("na", "Sodium", ("L40_B", "LBXSNASI", "L40_2_B", "LB2SNASI"), ("NAPSI", "NARSI")),
    ("k", "Potassium", ("L40_B", "LBXSKSI", "L40_2_B", "LB2SKSI"), ("SKPSI", "SKRSI")),
    ("cl", "Chlorure", ("L40_B", "LBXSCLSI", "L40_2_B", "LB2SCLSI"), ("CLPSI", "CLRSI")),
    ("hco3", "Bicarbonates", ("L40_B", "LBXSC3SI", "L40_2_B", "LB2SC3SI"), ("C3PSI", "C3RSI")),
    ("osmo", "Osmolalité mesurée", None, ("OSPSI", "OSRSI")),
    ("crp", "CRP", ("L11_B", "LBXCRP", "L11_2_b", "LB2CRP"), ("CRP", "CRR")),
    ("b12", "Vitamine B12", ("L06_B", "LBXB12", "L06_2_B", "LB2B12"), ("VBP", "VBR")),
    ("rbc_folate", "Folates érythrocytaires", ("L06_B", "LBXRBF", "L06_2_B", "LB2RBF"), ("RBP", "RBR")),
    ("vitd", "25-OH vitamine D", ("L06VID_B", "LBXVID", "VID_2_B", "LB2VID"), None),
    ("ca", "Calcium", ("L40_B", "LBXSCA", "L40_2_B", "LB2SCA"), ("SCP", "SCR")),
    ("lh", "LH", ("L40_B", "LBXLH", "L40_2_B", "LB2LH"), ("LHPSI", "LHRSI")),
    ("fsh", "FSH", ("L40_B", "LBXFSH", "L40_2_B", "LB2FSH"), None),
    ("psa_total", "PSA total", ("L11PSA_B", "LBXP1", "l11p_2_b", "LB2P1"), None),
    ("psa_free", "PSA libre", ("L11PSA_B", "LBXP2", "l11p_2_b", "LB2P2"), None),
    ("apoa1", "ApoA1", None, ("AAP", "AAR")),
    ("apob", "ApoB", None, ("ABP", "ABR")),
    ("lpa", "Lp(a)", None, ("LPP", "LPR")),
    ("iron", "Fer sérique", ("L40_B", "LBXSIR", "L40_2_B", "LB2SIR"), ("FEP", "FER")),
    ("ferritin", "Ferritine", ("L06_B", "LBXFER", "L06_2_B", "LB2FER"), ("FRP", "FRR")),
    ("tibc", "Capacité totale de fixation du fer", None, ("TIP", "TIR")),
    ("tsat", "Saturation de la transferrine", None, ("PXP", "PXR")),
    ("hcy", "Homocystéine", ("L06_B", "LBDHCY", "L06_2_B", "LB2HCY"), None),
    ("urate", "Acide urique", ("L40_B", "LBXSUA", "L40_2_B", "LB2SUA"), ("UAP", "UAR")),
    ("phos", "Phosphate", ("L40_B", "LBDSPH", "L40_2_B", "LB2SPH"), ("PSP", "PSR")),
    ("selenium", "Sélénium", None, ("SEP", "SER")),
    ("u_alb", "Albumine urinaire", ("L16_B", "URXUMA", "L16_2_B", "UR2UMA"), ("UBP", "UBR")),
    ("u_creat", "Créatinine urinaire", ("L16_B", "URXUCR", "L16_2_B", "UR2UCR"), ("URP", "URR")),
    ("u_iodine", "Iode urinaire", None, ("UIP", "UIR")),
]
LABEL = {p[0]: p[1] for p in PAIRS}

# Indices derives : (id, libelle, fonction des colonnes, echelle)
DERIVED = [
    ("homa_ir", "HOMA-IR", lambda d: d.glu_fast * d.insulin / 405, "log"),
    ("quicki", "QUICKI", lambda d: 1 / (np.log10(d.insulin) + np.log10(d.glu_fast)), "log"),
    ("eag", "Glycémie moyenne estimée", lambda d: 28.7 * d.hba1c - 46.7, "log"),
    ("tyg", "Indice TyG", lambda d: np.log(d.tg_fast * d.glu_fast / 2), "add"),
    ("non_hdl", "Cholestérol non-HDL", lambda d: d.tc - d.hdl, "log"),
    ("ldl_hdl", "LDL/HDL", lambda d: d.ldl / d.hdl, "log"),
    ("tg_hdl", "TG/HDL", lambda d: d.tg_fast / d.hdl, "log"),
    ("aip", "Indice athérogène (log10 TG/HDL, mmol)", lambda d: np.log10((d.tg_fast * 0.01129) / (d.hdl * 0.02586)), "add"),
    ("alb_glob", "Albumine/globulines", lambda d: d.albumin / (d.protein - d.albumin), "log"),
    ("fib4", "FIB-4", lambda d: d.age * d.ast / (d.plt * np.sqrt(d.alt)), "log"),
    ("ggt_hdl", "GGT/HDL", lambda d: d.ggt / d.hdl, "log"),
    ("ast_alt", "ASAT/ALAT", lambda d: d.ast / d.alt, "log"),
    ("urea_creat", "Urée/créatinine", lambda d: d.urea / d.creat, "log"),
    ("osmo_eff", "Osmolalité effective (2 Na + glucose)", lambda d: 2 * d.na + d.glu_serum / 18.0, "log"),
    ("nlr", "Neutrophiles/lymphocytes", lambda d: d.neut_pct / d.lymph_pct, "log"),
    ("sii", "Indice SII", lambda d: d.plt * d.neut_pct / d.lymph_pct, "log"),
    ("ca_corr", "Calcium corrigé", lambda d: d.ca + 0.8 * (4.0 - d.albumin), "log"),
    ("egfr", "DFGe (CKD-EPI 2021)", None, "log"),
]


# ------------------------------------------------------------------ chargement des paires
def _xpt(f):
    p = RAW / f"2001_{f}.xpt"
    download(URL.format(f=f), p)
    return read_xpt(p).set_index("SEQN")


def pairs_2001() -> tuple[pd.DataFrame, pd.DataFrame]:
    demo = _xpt("DEMO_B")
    base = demo[["RIDAGEYR", "RIAGENDR", "RIDEXPRG"]].rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})
    base = base[base.age.between(20, 79) & (base.RIDEXPRG != 1)]
    e1, e2 = base[["age", "sex"]].copy(), base[["age", "sex"]].copy()
    cache = {}
    for pid, _, a, _ in PAIRS:
        if a is None:
            continue
        f1, v1, f2, v2 = a
        for f in (f1, f2):
            if f not in cache:
                cache[f] = _xpt(f)
        e1[pid] = cache[f1][v1].reindex(e1.index) if v1 in cache[f1] else np.nan
        e2[pid] = cache[f2][v2].reindex(e2.index) if v2 in cache[f2] else np.nan
    return e1, e2


def pairs_nh3() -> tuple[pd.DataFrame, pd.DataFrame]:
    lay = n3.layout(n3.RAW / "lab.sas")
    v1s = [b[0] for *_, b in PAIRS if b]
    v2s = [b[1] for *_, b in PAIRS if b]
    lab = n3.read_fixed("lab", ["HSAGEIR", "HSSEX"] + [v for v in v1s if v in lay])
    ex = n3.read_fixed("exam", ["MAPF12R"])
    se = n3.read_fixed("labse", list(dict.fromkeys(v2s)))
    base = lab[["HSAGEIR", "HSSEX"]].rename(columns={"HSAGEIR": "age", "HSSEX": "sex"})
    preg = ex["MAPF12R"].reindex(base.index) == 1
    base = base[base.age.between(20, 79) & ~preg & base.index.isin(se.index)]
    e1, e2 = base.copy(), base.copy()
    for pid, _, _, b in PAIRS:
        if b is None:
            continue
        e1[pid] = lab[b[0]].reindex(base.index)
        e2[pid] = se[b[1]].reindex(base.index)
    return e1, e2


def add_derived(e: pd.DataFrame) -> pd.DataFrame:
    e = e.copy()
    for did, _, f, _ in DERIVED:
        if did == "egfr":
            from ..nhanes import egfr_ckd_epi_2021
            if "creat" in e:
                e[did] = egfr_ckd_epi_2021(e.creat * 88.42, e.age, e.sex)
            continue
        try:
            with np.errstate(all="ignore"):
                e[did] = f(e)
        except (AttributeError, KeyError):
            e[did] = np.nan
    return e.replace([np.inf, -np.inf], np.nan)


# ------------------------------------------------------------------ indicateurs
def _cv_from_sd_log(sd_d):
    return float(100 * np.sqrt(np.exp(sd_d ** 2 / 2) - 1))


def metrics(x1, x2, scale, seed=SEED, n_boot=N_BOOT):
    x1, x2 = np.asarray(x1, float), np.asarray(x2, float)
    ok = np.isfinite(x1) & np.isfinite(x2)
    x1, x2 = x1[ok], x2[ok]
    n = len(x1)
    if n < 20:
        return {"n": n}
    allv = np.concatenate([x1, x2])
    vmin = allv.min()
    cens = float(np.mean(allv == vmin)) if np.mean(allv == vmin) > 0.01 else 0.0
    if scale == "log" and vmin <= 0:
        scale = "add"
    d = np.log(x2) - np.log(x1) if scale == "log" else x2 - x1
    dc = d - d.mean()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, (n_boot, n))

    def stats(dd):
        sd = dd.std(ddof=1)
        mad = 1.4826 * np.median(np.abs(dd - np.median(dd)))
        q = np.percentile(np.abs(dd - dd.mean()), 95)
        return sd, mad, q
    sd, mad, q = stats(d)
    bs = np.array([stats(d[i]) for i in idx])
    lo, hi = np.quantile(bs, .025, axis=0), np.quantile(bs, .975, axis=0)
    out = {"n": n, "echelle": scale, "part_au_minimum": cens, "decalage_moyen": float(d.mean()),
           "mediane_x1": float(np.median(x1))}
    if scale == "log":
        out |= {"cv_obs": _cv_from_sd_log(sd), "cv_obs_ic95": [_cv_from_sd_log(lo[0]), _cv_from_sd_log(hi[0])],
                "cv_robuste": _cv_from_sd_log(mad), "cv_robuste_ic95": [_cv_from_sd_log(lo[1]), _cv_from_sd_log(hi[1])],
                "cd_emp_hausse": float(100 * (np.exp(q) - 1)), "cd_emp_baisse": float(100 * (1 - np.exp(-q))),
                "cd_emp_hausse_ic95": [float(100 * (np.exp(lo[2]) - 1)), float(100 * (np.exp(hi[2]) - 1))],
                # changement detectable deduit du CV robuste (pour la prediction « queues epaisses »)
                "cd_robuste_hausse": float(100 * (np.exp(1.96 * mad) - 1))}
    else:
        out |= {"sd_intra": float(sd / np.sqrt(2)), "sd_intra_ic95": [float(lo[0] / np.sqrt(2)), float(hi[0] / np.sqrt(2))],
                "sd_intra_robuste": float(mad / np.sqrt(2)), "cd_emp_unites": float(q),
                "cd_emp_unites_ic95": [float(lo[2]), float(hi[2])], "cd_robuste_unites": float(1.96 * mad)}
    return out


def analyse() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    sets = {"2001_2002": pairs_2001(), "nhanes3": pairs_nh3()}
    rows = []
    scales = {p[0]: "log" for p in PAIRS} | {d[0]: d[3] for d in DERIVED}
    labels = LABEL | {d[0]: d[1] for d in DERIVED}
    for jeu, (e1, e2) in sets.items():
        e1, e2 = add_derived(e1), add_derived(e2)
        for grp, m in [("20-79 ans", np.ones(len(e1), bool)), ("30-55 ans", e1.age.between(30, 55).to_numpy())]:
            for pid in scales:
                if pid not in e1 or e1[pid].isna().all():
                    continue
                r = metrics(e1[pid].to_numpy()[m], e2[pid].to_numpy()[m], scales[pid])
                rows.append({"jeu": jeu, "groupe": grp, "id": pid, "marqueur": labels[pid], **r})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "Q1_variabilite_remesures.csv", index=False)
    (OUT / "Q1_variabilite_meta.json").write_text(json.dumps({
        "n_paires": {k: int(len(v[0])) for k, v in sets.items()}, "graine": SEED, "bootstrap": N_BOOT}, indent=1), encoding="utf-8")
    return OUT / "Q1_variabilite_remesures.csv"
