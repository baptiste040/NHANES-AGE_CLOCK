"""Programme « panel », Q5 : changements de methode et de laboratoire (protocole : DECISIONS.md,
pre-enregistrement du 2026-11-11).

(a) equations de passage publiees par le NCHS, appliquees au cycle precedant le changement ;
(b) decalage empirique (difference de differences entre cycles successifs) ;
classification autour des seuils D1 ; verifications V1-V3 ;
(c) ecarts entre laboratoires de routine (litterature, valeurs dans private/panel/Q5_litterature) ;
(d) comparaison aux effets des interventions de Q1.
"""
from __future__ import annotations

import csv
import json

import numpy as np
import pandas as pd
from scipy.stats import norm

from ..features import rcs_basis
from .q2 import CYC, SUF, _knots, _xpt
from .remesures import OUT, ROOT, add_derived

SEED = 2026
B = 500
PRIV = ROOT / "private" / "panel" / "Q5_litterature"
QS = [10, 25, 50, 75, 90]

# ------------------------------------------------------------------ fichiers
CBC = {1999: "LAB25", 2001: "L25_B", 2003: "L25_C", **{y: "CBC" + SUF[y] for y in CYC[3:]}}
BIO = {1999: "LAB18", 2001: "L40_B", 2003: "L40_C", **{y: "BIOPRO" + SUF[y] for y in CYC[3:]}}
GLU = {1999: "LAB10AM", 2001: "L10AM_B", 2003: "L10AM_C", **{y: "GLU" + SUF[y] for y in CYC[3:]}}
INS = {1999: "LAB10AM", 2001: "L10AM_B", 2003: "L10AM_C", 2005: "GLU_D", 2007: "GLU_E", 2009: "GLU_F",
       2011: "GLU_G", 2013: "INS_H", 2015: "INS_I", 2017: "INS_J"}
TRI = {1999: "LAB13AM", 2001: "L13AM_B", 2003: "L13AM_C", **{y: "TRIGLY" + SUF[y] for y in CYC[3:]}}
FILES = {  # id : ({cycle: fichier}, [variables candidates])
    **{k: (CBC, v) for k, v in {"wbc": ["LBXWBCSI"], "neut_pct": ["LBXNEPCT"], "lymph_pct": ["LBXLYPCT"],
                                 "mono_pct": ["LBXMOPCT"], "eos_pct": ["LBXEOPCT"], "baso_pct": ["LBXBAPCT"],
                                 "rbc": ["LBXRBCSI"], "hb": ["LBXHGB"], "hct": ["LBXHCT"], "mcv": ["LBXMCVSI"],
                                 "mch": ["LBXMCHSI"], "mchc": ["LBXMC"], "rdw": ["LBXRDW"], "plt": ["LBXPLTSI"],
                                 "mpv": ["LBXMPSI"]}.items()},
    **{k: (BIO, v) for k, v in {"alt": ["LBXSATSI"], "ast": ["LBXSASSI"], "ggt": ["LBXSGTSI"], "alp": ["LBXSAPSI", "LBDSAPSI"],
                                 "bili": ["LBXSTB", "LBDSTB"], "albumin": ["LBXSAL"], "protein": ["LBXSTP"],
                                 "creat": ["LBXSCR", "LBDSCR"], "urea": ["LBXSBU"], "na": ["LBXSNASI"], "k": ["LBXSKSI"],
                                 "cl": ["LBXSCLSI"], "hco3": ["LBXSC3SI"], "ca": ["LBXSCA"], "phos": ["LBXSPH", "LBDSPH"],
                                 "urate": ["LBXSUA"], "iron": ["LBXSIR"], "glu_serum": ["LBXSGL"], "tg_serum": ["LBXSTR"],
                                 "ck": ["LBXSCK"], "ldh": ["LBXSLDSI"], "tc_serum": ["LBXSCH"]}.items()},
    "glu_fast": (GLU, ["LBXGLU"]), "insulin": (INS, ["LBXIN"]),
    "tg_fast": (TRI, ["LBXTR"]), "ldl": (TRI, ["LBDLDL"]),
    "hba1c": ({1999: "LAB10", 2001: "L10_B", 2003: "L10_C", **{y: "GHB" + SUF[y] for y in CYC[3:]}}, ["LBXGH"]),
    "tc": ({1999: "Lab13", 2001: "l13_b", 2003: "l13_c", **{y: "TCHOL" + SUF[y] for y in CYC[3:]}}, ["LBXTC"]),
    "hdl": ({1999: "Lab13", 2001: "l13_b", 2003: "l13_c", **{y: "HDL" + SUF[y] for y in CYC[3:]}}, ["LBDHDL", "LBXHDD", "LBDHDD"]),
    "ferritin": ({1999: "LAB06", 2001: "L06_B", 2005: "FERTIN_D", 2007: "FERTIN_E", 2009: "FERTIN_F", 2015: "FERTIN_I",
                  2017: "FERTIN_J"}, ["LBXFER"]),
    "b12": ({1999: "LAB06", 2001: "L06_B", 2003: "L06NB_C", 2005: "B12_D", 2011: "VITB12_G", 2013: "VITB12_H"},
            ["LBDB12", "LBXB12"]),
    "rbc_folate": ({1999: "LAB06", 2001: "L06_B", 2003: "L06NB_C", **{y: "FOLATE" + SUF[y] for y in CYC[3:]}},
                   ["LBDRBFSI", "LBXRBFSI", "LBDRFOSI"]),
    "fol_serum": ({1999: "LAB06", 2001: "L06_B", 2003: "L06NB_C", 2005: "FOLATE_D", 2007: "FOLATE_E", 2009: "FOLATE_F"},
                  ["LBDFOLSI", "LBXFOLSI"]),
    "vitd": ({2001: "VID_B", 2003: "VID_C", 2005: "VID_D", **{y: "VID" + SUF[y] for y in CYC[4:]}}, ["LBDVIDMS", "LBXVIDMS"]),
    "vitd_ria": ({2001: "L06VID_B"}, ["LBXVID"]),
    "crp_hs": ({2015: "HSCRP_I", 2017: "HSCRP_J"}, ["LBXHSCRP"]),
    "apob": ({2005: "TRIGLY_D", 2007: "ApoB_E", 2009: "ApoB_F", 2011: "ApoB_G", 2013: "ApoB_H", 2015: "APOB_I"}, ["LBXAPB"]),
    "testo": ({2011: "TST_G", 2013: "TST_H", 2015: "TST_I"}, ["LBXTST"]),
    "tsh": ({1999: "LAB18T4", 2001: "L40T4_B", 2007: "THYROD_E", 2009: "THYROD_F", 2011: "THYROD_G"}, ["LBXTSH1", "LBXTSH"]),
    "ft4": ({2007: "THYROD_E", 2009: "THYROD_F", 2011: "THYROD_G"}, ["LBXT4F"]),
    "hcy": ({1999: "LAB06", 2001: "L06_B", 2003: "L06MH_C", 2005: "HCY_D"}, ["LBXHCY"]),
    "u_creat": ({1999: "LAB16", 2001: "L16_B", 2003: "L16_C", **{y: "ALB_CR" + SUF[y] for y in CYC[3:]}}, ["URXUCR"]),
    "u_alb": ({1999: "LAB16", 2001: "L16_B", 2003: "L16_C", **{y: "ALB_CR" + SUF[y] for y in CYC[3:]}}, ["URXUMA"]),
    "iron_fe": ({1999: "LAB06", 2001: "L40FE_B", 2003: "L40FE_C", 2005: "FETIB_D", 2017: "FETIB_J"}, ["LBXIRN"]),
}
# analyte du bilan biochimique -> meme analyte dans Q1 (parties c et d) ; CRP ultrasensible -> CRP de Q1
SAME = {"tg_serum": "tg_fast", "tc_serum": "tc", "glu_serum": "glu_fast", "crp_hs": "crp", "iron_fe": "iron"}


def load() -> pd.DataFrame:
    frames = []
    for y in CYC:
        d = _xpt("DEMO" + SUF[y], y)[["RIDAGEYR", "RIAGENDR", "RIDEXPRG", "RIDRETH1", "INDFMPIR"]]
        d = d.join(_xpt("BMX" + SUF[y], y)[["BMXBMI"]], how="left").join(_xpt("DIQ" + SUF[y], y)[["DIQ010"]], how="left")
        cache = {}
        for mid, (files, cands) in FILES.items():
            if y not in files:
                continue
            f = files[y]
            if f not in cache:
                cache[f] = _xpt(f, y)
            x = cache[f]
            v = next((c for c in cands if c in x), None)
            if v is not None:
                d[mid] = x[v].reindex(d.index)
        for f in (GLU.get(y), INS.get(y)):
            if f in cache and "WTSAF2YR" in cache[f]:
                d["w_" + f] = cache[f]["WTSAF2YR"].reindex(d.index)
        d["cycle"] = y
        frames.append(d)
    d = pd.concat(frames).rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})
    d["globulin"] = d.protein - d.albumin
    d["osmo"] = 2 * d.na + d.glu_serum / 18 + d.urea / 2.8
    return d


def pop(d):
    return d[d.age.between(20, 79) & (d.RIDEXPRG != 1)]


# ------------------------------------------------------------------ equations (nouvelle = f(ancienne))
def lin(a, b):
    return lambda x: a * x + b


def loglin(a, b):
    return lambda x: 10 ** (a * np.log10(x) + b)


def pct(p):
    return lambda x: x * (1 + p / 100)


def ucr(x):
    x = np.asarray(x, float)
    return np.where(x < 75, (1.02 * np.sqrt(x) - 0.36) ** 2,
                    np.where(x < 250, (1.05 * np.sqrt(x) - 0.74) ** 2, (1.01 * np.sqrt(x) - 0.10) ** 2))


def rbf(df):
    """Evenement 22 : algorithme du NCHS (folates erythrocytaires, BR -> MA)."""
    h = df.hct / 100
    wbf = df.rbc_folate * h + df.fol_serum * (1 - h)
    wa = 10 ** (0.2204 + 1.017 * np.log10(wbf))
    X = np.log10(df.fol_serum)
    fa = 10 ** (0.0188 * X ** 3 - 2.7109 * X ** -0.5 + 3.8276)
    return (wa - fa * (1 - h)) / h


BIO17 = {"albumin": lin(0.9581, -0.0108), "alp": loglin(0.9986, 0.04288), "ast": lin(0.9822, -3.695), "alt": lin(0.9869, -2.653),
         "urea": lin(0.9992, -0.4484), "hco3": pct(1.74), "ca": pct(-2.12), "tc_serum": lin(0.9556, 2.105),
         "ck": lin(1.068, -1.131), "cl": pct(-1.44), "creat": lin(0.9515, 0.06608), "glu_serum": pct(2.41),
         "ggt": lin(1.243, -2.938), "iron": lin(1.023, 4.597), "k": pct(-1.398), "ldh": lin(1.167, -2.407), "na": pct(0.80),
         "phos": pct(-1.80), "bili": pct(-3.19), "protein": pct(0.36), "tg_serum": lin(1.036, 7.271), "urate": lin(1.073, -0.2495)}
MEAN_ONLY = {"hco3", "ca", "cl", "glu_serum", "k", "na", "phos", "bili", "protein"}

# num, ids, type, pre (cycle transforme), transform {id: f}, spans (b), diffusion ajustee, chiffre (a)
EVENTS = [
    ("1", ["creat"], "E", 1999, {"creat": lin(1.013, 0.147)}, [(1999, 2001)], "non"),
    ("2", ["creat"], "E", 2005, {"creat": lin(0.978, -0.016)}, [(2003, 2005)], "non"),
    ("3", ["creat"], "I", 2005, {"creat": lambda x: x - 0.08}, [(2005, 2009)], "oui"),
    ("4", ["alp", "creat", "ldh", "phos", "bili"], "L", None, {}, [(1999, 2003)], "oui"),
    ("5", list(BIO17), "L, I, M", 2015, BIO17, [(2015, 2017)], "non"),
    ("6", ["glu_fast"], "I", 2003, {"glu_fast": lin(0.9815, 3.5707)}, [(2003, 2005)], "non"),
    ("7", ["glu_fast"], "I", 2005, {"glu_fast": lin(1.0, 1.148)}, [(2005, 2007)], "non"),
    ("8", ["glu_fast"], "I", 2013, {"glu_fast": lin(1.023, -0.5108)}, [(2013, 2015)], "partielle"),
    ("9", ["insulin"], "M", 2001, {"insulin": lin(1.0027, -2.2934)}, [(2001, 2003)], "non"),
    ("10", ["insulin"], "M", 2003, {"insulin": lin(0.9501, 1.4890)}, [(2003, 2005)], "non"),
    ("11", ["insulin"], "M", 2009, {"insulin": lambda x: 0.8868 * x + 0.0011 * x ** 2 - 0.0744}, [(2009, 2011)], "partielle"),
    ("12", ["insulin"], "M", 2011, {"insulin": loglin(1.024, -0.0802)}, [(2011, 2013)], "non"),
    ("13", ["hdl"], "L, I", 2005, {"hdl": pct(-2.45)}, [(2005, 2007)], "non"),
    ("14", ["hdl"], "M", None, {}, [(2001, 2003)], "partielle"),
    ("15", ["tc", "tg_fast"], "L, I", None, {}, [(2005, 2007)], "non"),
    ("16", ["hba1c"], "inconnu", None, {}, [(2005, 2007)], "non"),
    ("17", ["wbc", "neut_pct", "lymph_pct", "mono_pct", "eos_pct", "baso_pct", "rbc", "hb", "hct", "mcv", "mch", "mchc",
            "rdw", "plt", "mpv"], "I", None, {}, [(2009, 2013)], "non"),
    ("18", ["ferritin"], "I", 2007, {"ferritin": loglin(0.989, 0.049)}, [(2007, 2009)], "non"),
    ("19", ["ferritin"], "I", 2009, {"ferritin": lin(1.079, 0.2243)}, [(2009, 2015)], "partielle"),
    ("20", ["b12"], "M", 2005, {"b12": loglin(0.97, 0.14)}, [(2005, 2011)], "non"),
    ("21", ["b12"], "K", None, {}, [(2011, 2013)], "oui"),
    ("22", ["rbc_folate"], "M", 2005, {"rbc_folate": "rbf"}, [(2005, 2007)], "non"),
    ("23a", ["vitd"], "M, E", 2001, {"vitd": lin(0.95212, 6.43435)}, [], "oui"),
    ("23b", ["vitd"], "M, E", 2003, {"vitd": lin(0.98284, 1.72786)}, [(2001, 2003), (2003, 2005)], "oui"),
    ("23c", ["vitd"], "M, E", 2005, {"vitd": lin(0.97012, 8.36753)}, [(2005, 2007)], "oui"),
    ("24", ["crp_hs"], "L, I, M", 2015, {"crp_hs": lambda x: np.where(x <= 23, 0.8695 * x + 0.2954, x)}, [(2015, 2017)], "non"),
    ("25", ["apob"], "L, I", 2005, {"apob": lin(0.923, 0.0)}, [(2005, 2007)], "non"),
    ("26", ["apob"], "I, M", 2013, {"apob": lin(1.001, 2.883)}, [(2013, 2015)], "non"),
    ("27", ["testo"], "M", 2011, {"testo": pct(3.9)}, [(2011, 2013)], "partielle"),
    ("28", ["ft4", "tsh"], "L", None, {}, [(2007, 2011)], "T4 totale seulement"),
    ("29", ["hcy"], "I", 1999, {"hcy": loglin(0.983, 0.0418)}, [(1999, 2003)], "non précisé"),
    ("30", ["hcy"], "K", None, {}, [(2003, 2005)], "oui"),
    ("31", ["u_creat"], "I, M", 2005, {"u_creat": ucr}, [(2005, 2007)], "non"),
    ("32", ["iron_fe"], "L", None, {}, [(1999, 2003)], "TIBC seulement"),
]
RIA = {2003: (0.98284, 1.72786), 2005: (0.97012, 8.36753)}  # inversion LBDVIDMS -> RIA d'origine

# derives recalcules quand leurs composants changent
DERIV_OF = {"glu_fast": ["homa_ir", "quicki", "tyg"], "insulin": ["homa_ir", "quicki"],
            "hdl": ["non_hdl", "ldl_hdl", "tg_hdl", "aip", "ggt_hdl", "ldl"],
            "creat": ["egfr", "urea_creat"], "albumin": ["alb_glob", "ca_corr", "globulin"], "protein": ["alb_glob", "globulin"],
            "ast": ["fib4", "ast_alt"], "alt": ["fib4", "ast_alt"], "ggt": ["ggt_hdl"], "urea": ["urea_creat", "osmo"],
            "ca": ["ca_corr"], "na": ["osmo_eff", "osmo"], "glu_serum": ["osmo_eff", "osmo"], "u_creat": ["acr"]}


def _with_derived(df):
    e = df.copy()
    if {"tc", "hdl", "tg_fast"} <= set(e):
        e["ldl"] = e.tc - e.hdl - e.tg_fast / 5
    e = add_derived(e)
    if {"protein", "albumin"} <= set(e):
        e["globulin"] = e.protein - e.albumin
    if {"na", "glu_serum", "urea"} <= set(e):
        e["osmo"] = 2 * e.na + e.glu_serum / 18 + e.urea / 2.8
    if {"u_alb", "u_creat"} <= set(e):
        e["acr"] = e.u_alb / e.u_creat * 100
    return e


# ------------------------------------------------------------------ changement detectable de Q1
def q1_table():
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    return cd[cd.groupe == "20-79 ans"].drop_duplicates("id").set_index("id")


def scale_of(mid, cd):
    k = SAME.get(mid, mid)
    return cd.loc[k, "echelle"] if k in cd.index else "log"


def ratio(shift, mid, cd, robust=False):
    """shift en % (log) ou en unites (add)."""
    k = SAME.get(mid, mid)
    if k not in cd.index or not np.isfinite(shift):
        return np.nan
    c = cd.loc[k]
    if c.echelle == "add":
        u = c.get("cd6m_unites_empirique" if robust else "cd6m_unites")
        return abs(shift) / u if pd.notna(u) and u else np.nan
    if robust:
        h = c.get("cd6m_hausse_robuste")
        if pd.isna(h):
            return np.nan
        s = h if shift > 0 else 100 * (1 - 1 / (1 + h / 100))
    else:
        s = c.cd6m_hausse if shift > 0 else c.cd6m_baisse
    return abs(shift) / s if pd.notna(s) and s else np.nan


def false_change(shift, mid, cd):
    k = SAME.get(mid, mid)
    if k not in cd.index or not np.isfinite(shift):
        return np.nan
    c = cd.loc[k]
    if c.echelle == "add":
        if pd.isna(c.get("cd6m_unites")):
            return np.nan
        s, dl = c.cd6m_unites / 1.96, shift
    else:
        if pd.isna(c.cd6m_hausse):
            return np.nan
        s, dl = np.log(1 + c.cd6m_hausse / 100) / 1.96, np.log(1 + shift / 100)
    return float(norm.cdf(-1.96 + dl / s) + norm.cdf(-1.96 - dl / s))


def category(r):
    if not np.isfinite(r):
        return "non estimable"
    return ("comparaison impossible sans équation de passage" if r >= 1 else
            "un changement de laboratoire peut créer un faux changement" if r >= 0.5 else "négligeable au regard du bruit")


# ------------------------------------------------------------------ partie (a)
def _pre(d, ev_num, cyc, ids):
    g = pop(d[d.cycle == cyc]).copy()
    if ev_num in ("23b", "23c"):
        a, b = RIA[cyc]
        g["vitd"] = (g.vitd - b) / a
    if ev_num == "23a":
        g["vitd"] = g.vitd_ria * 2.4959
    return g


def part_a(d, cd):
    rows, trans = [], {}
    for num, ids, typ, pre, tf, spans, adj in EVENTS:
        if pre is None:
            for mid in ids:
                rows.append({"evenement": num, "id": mid, "type": typ, "diffusion_ajustee": adj, "chiffre": False})
            continue
        g = _pre(d, num, pre, ids)
        new = g.copy()
        for mid, f in tf.items():
            new[mid] = rbf(g) if f == "rbf" else f(g[mid].to_numpy(float))
        old_d, new_d = _with_derived(g), _with_derived(new)
        trans[num] = (old_d, new_d)
        targets = list(ids) + [x for m in ids for x in DERIV_OF.get(m, [])]
        for mid in dict.fromkeys(targets):
            if mid not in old_d:
                continue
            ok = old_d[mid].notna() & new_d[mid].notna()
            if ok.sum() < 30:
                continue
            sc = scale_of(mid, cd)
            if sc == "log":  # comme Q1 : valeurs positives seulement sur l'echelle log
                ok &= (old_d[mid] > 0) & (new_d[mid] > 0)
            o, n_ = old_d[mid][ok].to_numpy(float), new_d[mid][ok].to_numpy(float)
            qo, qn = np.percentile(o, QS), np.percentile(n_, QS)
            sh = 100 * (qn / qo - 1) if sc == "log" else qn - qo
            s50 = float(sh[2])
            smax = float(sh[np.argmax(np.abs(sh))])
            r = ratio(s50, mid, cd)
            row = {"evenement": num, "id": mid, "type": typ, "diffusion_ajustee": adj, "chiffre": True,
                   "derive": mid not in ids, "cycle_transforme": pre, "n": int(ok.sum()), "echelle": sc,
                   **{f"decalage_p{q}": float(v) for q, v in zip(QS, sh)},
                   "decalage_principal": s50, "decalage_max_p10_p90": smax,
                   "moyenne_seulement": (num in ("3", "13", "27")) or (num == "5" and mid in MEAN_ONLY),
                   "ratio": r, "ratio_max_p10_p90": ratio(smax, mid, cd), "ratio_cd_empirique": ratio(s50, mid, cd, robust=True),
                   "taux_faux_changement": false_change(s50, mid, cd), "categorie": category(r)}
            if num == "27":  # testosterone : par sexe, et sensibilite sur l'equation
                for sx, lab in ((1, "H"), (2, "F")):
                    m = ok & (g.sex == sx)
                    x = g.testo[m].to_numpy(float)
                    row[f"decalage_{lab}"] = 3.9
                    for u, mult in (("ngdl", 1), ("ngml", 100)):
                        y = 1.021 * x + 0.182 * mult
                        row[f"decalage_{lab}_equation_{u}"] = float(100 * (np.median(y) / np.median(x) - 1))
            rows.append(row)
    return pd.DataFrame(rows), trans


# ------------------------------------------------------------------ partie (b)
def _design(g, extra=False):
    kn = _knots(g.age.to_numpy())
    eth = pd.get_dummies(g.RIDRETH1.astype("category"), drop_first=True).to_numpy(float)
    cols = [np.ones(len(g)), g.age.to_numpy(float), rcs_basis(g.age.to_numpy(float), kn), (g.sex == 2).to_numpy(float), eth]
    if extra:
        cols += [g.BMXBMI.to_numpy(float), g.INDFMPIR.to_numpy(float)]
    return np.column_stack([c if c.ndim > 1 else c[:, None] for c in [np.asarray(c, float) for c in cols]])


def _fit(y, X, cyc, levels, q=None):
    D = np.column_stack([(cyc == c).astype(float) for c in levels[1:]])
    M = np.column_stack([X, D])
    if q is None:
        b = np.linalg.lstsq(M, y, rcond=None)[0]
    else:  # regression mediane (moindres ecarts absolus) par moindres carres repondéres iteratifs
        b = np.linalg.lstsq(M, y, rcond=None)[0]
        for _ in range(100):
            w = 1 / np.maximum(np.abs(y - M @ b), 1e-6)
            sw = np.sqrt(w)
            nb = np.linalg.lstsq(M * sw[:, None], y * sw, rcond=None)[0]
            if np.max(np.abs(nb - b)) < 1e-7:
                b = nb
                break
            b = nb
    coef = np.concatenate([[0.0], b[X.shape[1]:]])
    return dict(zip(levels, coef))


def part_b(d, cd):
    d = pop(d)
    spans_by = {}
    for num, ids, *_r in EVENTS:
        for mid in ids:
            spans_by.setdefault(mid, []).extend([(num, s) for s in _r[3]])
    rows = []
    for mid, evs in spans_by.items():
        if mid not in d:
            continue
        sc = scale_of(mid, cd)
        g = d[d[mid].notna()].copy()
        if sc == "log":
            g = g[g[mid] > 0]
        g = g.dropna(subset=["age", "sex", "RIDRETH1"])
        levels = sorted(g.cycle.unique())
        if len(levels) < 2:
            continue
        y = np.log(g[mid].to_numpy(float)) if sc == "log" else g[mid].to_numpy(float)
        X = _design(g)
        cyc = g.cycle.to_numpy()
        trans = list(zip(levels[:-1], levels[1:]))
        excl = set()
        for _, (a, b) in evs:
            ia, ib = levels.index(a) if a in levels else None, levels.index(b) if b in levels else None
            if ia is None or ib is None:
                continue
            excl |= set(trans[ia:ib])
        free = [t for t in trans if t not in excl]

        def did(coef):
            out = {}
            ref = np.mean([coef[b] - coef[a] for a, b in free]) if len(free) >= 2 else np.nan
            for num, (a, b) in evs:
                if a not in coef or b not in coef:
                    continue
                steps = levels.index(b) - levels.index(a)
                out[(num, a, b)] = (coef[b] - coef[a], coef[b] - coef[a] - steps * ref, ref)
            return out
        est = did(_fit(y, X, cyc, levels))
        rng = np.random.default_rng(SEED)
        idx_by = {c: np.where(cyc == c)[0] for c in levels}
        bs = []
        for _ in range(B):
            ii = np.concatenate([rng.choice(v, len(v)) for v in idx_by.values()])
            bs.append(did(_fit(y[ii], X[ii], cyc[ii], levels)))
        ok = np.isfinite(g.BMXBMI) & np.isfinite(g.INDFMPIR)
        est_x = did(_fit(y[ok.to_numpy()], _design(g[ok], extra=True), cyc[ok.to_numpy()], levels))
        try:
            est_q = did(_fit(y, X, cyc, levels, q=0.5))
        except Exception:
            est_q = {}
        conv = (lambda v: 100 * (np.exp(v) - 1)) if sc == "log" else (lambda v: v)
        for key, (j, dd, ref) in est.items():
            vals = np.array([b_[key][1] for b_ in bs if key in b_])
            ci = [float(conv(np.nanquantile(vals, .025))), float(conv(np.nanquantile(vals, .975)))] if np.isfinite(dd) else None
            sh = float(conv(dd)) if np.isfinite(dd) else np.nan
            rows.append({"evenement": key[0], "id": mid, "de": key[1], "a": key[2], "echelle": sc,
                         "saut_brut": float(conv(j)), "saut_reference": float(conv(ref)) if np.isfinite(ref) else np.nan,
                         "transitions_sans_evenement": len(free), "decalage_empirique": sh, "ic95": ci,
                         "decalage_ajuste_imc_revenu": float(conv(est_x[key][1])) if key in est_x and np.isfinite(est_x[key][1]) else np.nan,
                         "decalage_mediane": float(conv(est_q[key][1])) if key in est_q and np.isfinite(est_q[key][1]) else np.nan,
                         "ratio": ratio(sh, mid, cd), "categorie": category(ratio(sh, mid, cd)) if np.isfinite(sh) else "non estimable"})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ classification
def classification(trans):
    clin = pd.read_csv(OUT / "D1_seuils_cliniques.csv")
    stat = pd.read_csv(OUT / "D1_intervalles_statistiques.csv")
    rows = []
    for num, (o, n_) in trans.items():
        # osmolalite : l'intervalle D1 porte sur la valeur diffusee (LBXSOSSI), pas sur la formule de Q5
        ids = [i for i in o.columns if i in set(clin.id) | set(stat.id) and i != "osmo"]
        for mid in ids:
            ok = o[mid].notna() & n_[mid].notna()
            if ok.sum() < 30 or (o[mid][ok] == n_[mid][ok]).all():
                continue
            rules = []
            for _, r in clin[clin.id == mid].iterrows():
                thr = r.seuil * (2.4959 if mid == "vitd" else 1)
                rules.append((f"{r.libelle} ({r.variante})" if isinstance(r.variante, str) else r.libelle, r.sens, thr, None, "R/clinique"))
            if not len(clin[clin.id == mid]):
                for _, r in stat[stat.id == mid].iterrows():
                    if mid == "rbc_folate":  # D1 en ng/mL, Q5 en nmol/L
                        r = r.copy(); r.borne_basse *= 2.265; r.borne_haute *= 2.265
                    sel = (o.sex == (1 if r.sexe == "H" else 2)) & o.age.between(r.age_min, r.age_max)
                    rules.append((f"limite basse S ({r.sexe}, {r.age_min}-{r.age_max} ans)", "bas", r.borne_basse, sel, "S"))
                    rules.append((f"limite haute S ({r.sexe}, {r.age_min}-{r.age_max} ans)", "haut", r.borne_haute, sel, "S"))
            agg = {}
            for lab, sens, thr, sel, kind in rules:
                m = ok if sel is None else ok & sel
                x0, x1 = o[mid][m].to_numpy(float), n_[mid][m].to_numpy(float)
                f = (lambda v: v >= thr) if sens == "haut" else (lambda v: v < thr)
                if kind == "S":  # agrege par sens sur les strates
                    a = agg.setdefault(sens, [0, 0, 0])
                    a[0] += f(x0).sum(); a[1] += f(x1).sum(); a[2] += len(x0)
                    continue
                rows.append({"evenement": num, "id": mid, "seuil": lab, "type": "R" if "ESC" in lab or "KDIGO" in lab or "OMS" in lab or "ADA" in lab else kind,
                             "n": len(x0), "part_avant": float(f(x0).mean()), "part_apres": float(f(x1).mean()),
                             "points": float(100 * (f(x1).mean() - f(x0).mean()))})
            for sens, (a0, a1, nn) in agg.items():
                rows.append({"evenement": num, "id": mid, "seuil": f"intervalle statistique D1, limite {'haute' if sens == 'haut' else 'basse'}",
                             "type": "S", "n": nn, "part_avant": a0 / nn, "part_apres": a1 / nn, "points": 100 * (a1 - a0) / nn})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ verifications
def verifications(d):
    out = {}
    g = d[(d.cycle == 2015) & (d.age >= 18) & (d.RIDEXPRG != 1) & (d.DIQ010 != 1) & d.glu_fast.notna()]
    w = g["w_GLU_I"].fillna(0).to_numpy(float)
    x = g.glu_fast.to_numpy(float)
    xb = 0.9776 * x + 0.4994
    m = w > 0
    p = lambda v, lo, hi: float(np.sum(w[m] * ((v[m] >= lo) & (v[m] < hi))) / np.sum(w[m]) * 100)
    v1 = {"100_125_avant": p(x, 100, 126), "100_125_apres": p(xb, 100, 126), "ge126_avant": p(x, 126, 1e9), "ge126_apres": p(xb, 126, 1e9),
          "attendu": {"100_125_avant": 53.7, "100_125_apres": 41.5, "ge126_avant": 5.5, "ge126_apres": 3.4}}
    v1["reussie"] = all(abs(v1[k] - e) <= 1.5 for k, e in v1["attendu"].items())
    out["V1"] = v1
    g = d[(d.cycle == 2013) & d.insulin.notna() & (d.insulin > 0)]
    w = g["w_INS_H"].fillna(0).to_numpy(float)
    x = g.insulin.to_numpy(float)
    m = w > 0
    gm = lambda v: float(np.exp(np.sum(w[m] * np.log(v[m])) / np.sum(w[m])))
    xb = 10 ** (0.9765 * np.log10(x) + 0.07832)
    v2 = {"avant": gm(x), "apres": gm(xb), "attendu": {"avant": 9.20, "apres": 10.46}}
    v2["reussie"] = abs(v2["avant"] - 9.20) <= 0.15 and abs(v2["apres"] - 10.46) <= 0.15
    out["V2"] = v2
    g = d[(d.cycle == 2001) & d.vitd.notna() & d.vitd_ria.notna()]
    dif = np.abs(0.95212 * 2.4959 * g.vitd_ria + 6.43435 - g.vitd)
    out["V3"] = {"ecart_absolu_median": float(dif.median()), "n": int(len(g)), "reussie": bool(dif.median() < 0.5)}
    return out


# ------------------------------------------------------------------ parties (c) et (d)
def part_c(cd):
    p = PRIV / "cv_inter.csv"
    if not p.exists():
        return pd.DataFrame()
    lit = pd.read_csv(p)
    rows = []
    for _, r in lit.iterrows():
        k = SAME.get(r.id, r.id)
        if k not in cd.index:
            continue
        c = cd.loc[k]
        row = {"id": r.id, "reference": r.reference, "lu": r.lu, "europeen": r.europeen, "commutable": r.commutable,
               "nature": r.nature, "principale": bool(r.principale),
               # la note (valeurs brutes extraites) reste dans private/panel ; seul un qualificatif est public
               "qualite": ("borne basse (CV au sein des groupes de méthode)" if "intra-groupe" in r.note else
                           "ordre de grandeur lu dans le texte" if "ordre de grandeur" in r.note else
                           "sensibilité" if "sensibilité" in r.note else "")}
        if r.nature == "cv_inter":
            si = np.sqrt(np.log(1 + (r.valeur / 100) ** 2))
            dl = 100 * (np.exp(np.sqrt(2) * si) - 1)
            row["decalage_typique_pct"] = dl
            if c.echelle == "log" and pd.notna(c.cd6m_hausse):
                s6 = np.log(1 + c.cd6m_hausse / 100) / (1.96 * np.sqrt(2))
                tot = np.sqrt(s6 ** 2 + si ** 2)
                row["cd_meme_labo_hausse"] = c.cd6m_hausse
                row["cd_deux_labos_hausse"] = 100 * (np.exp(1.96 * np.sqrt(2) * tot) - 1)
                row["cd_deux_labos_baisse"] = 100 * (1 - np.exp(-1.96 * np.sqrt(2) * tot))
                row["rapport_cd"] = row["cd_deux_labos_hausse"] / c.cd6m_hausse
            row["ratio"] = ratio(dl, r.id, cd)
        else:  # biais entre methodes
            row["decalage_typique_pct"] = r.valeur
            row["ratio"] = ratio(r.valeur, r.id, cd)
        row["categorie"] = category(row["ratio"])
        rows.append(row)
    return pd.DataFrame(rows)


def part_d(A, Bm, C):
    inter = pd.read_csv(OUT / "Q1_secondaire_moyenner.csv")
    inter = inter[inter.groupe == "20-79 ans"]
    shifts = []
    for _, r in A[A.chiffre == True].iterrows():  # noqa: E712
        if r.echelle == "log" and np.isfinite(r.decalage_principal):
            shifts.append((SAME.get(r.id, r.id), r.id, f"(a) événement {r.evenement}", r.decalage_principal, False))
    done = set(A[A.chiffre == True].evenement)  # noqa: E712
    for _, r in Bm.iterrows():
        if r.evenement not in done and r.echelle == "log" and np.isfinite(r.decalage_empirique):
            shifts.append((SAME.get(r.id, r.id), r.id, f"(b) événement {r.evenement}", r.decalage_empirique, False))
    for _, r in C[C.principale].iterrows() if len(C) else []:
        if np.isfinite(r.get("decalage_typique_pct", np.nan)):
            shifts.append((SAME.get(r.id, r.id), r.id, f"(c) {r.reference}", r.decalage_typique_pct, r.nature == "cv_inter"))
    rows = []
    for _, it in inter.iterrows():
        for k, src_id, src, sh, unsigned in shifts:
            if k != it.id or not np.isfinite(it.effet_pct) or it.effet_pct == 0:
                continue
            rho = abs(sh) / abs(it.effet_pct)
            if rho < 0.5:
                flag = "non"
            elif unsigned:
                flag = "peut imiter ou masquer"
            else:
                flag = "peut imiter" if np.sign(sh) == np.sign(it.effet_pct) else "peut masquer"
            rows.append({"id": k, "analyte_du_decalage": src_id, "intervention": it.intervention, "effet_pct": it.effet_pct,
                         "source_effet": it.source, "decalage": src, "decalage_pct": sh, "rho": rho, "signalement": flag,
                         "suffit": rho >= 1})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ predictions et synthese
LOWVAR = {"albumin", "protein", "ca", "na", "cl", "hco3", "creat", "hba1c", "glu_fast", "tc", "hdl"}
ENZ = {"alt", "ast", "ggt", "alp", "ck"}


def predictions(A, Bm, D):
    a = A[(A.chiffre == True) & (A.derive == False)].dropna(subset=["ratio"])  # noqa: E712
    top = a.sort_values("ratio", ascending=False).drop_duplicates("id").head(5)
    p1 = {"top5": top[["id", "evenement", "ratio"]].to_dict("records"),
          "n_faible_variabilite": int(top.id.isin(LOWVAR).sum()),
          "enzyme_ratio_ge_1": bool((a[a.id.isin(ENZ)].ratio >= 1).any())}
    p1["verifiee"] = p1["n_faible_variabilite"] >= 3 and not p1["enzyme_ratio_ge_1"]
    nonadj = A[(A.chiffre == True) & (A.diffusion_ajustee == "non") & (A.derive == False) & (A.decalage_principal.abs() >= 3)]  # noqa: E712
    agree = []
    for _, r in nonadj.iterrows():
        b = Bm[(Bm.evenement == r.evenement) & (Bm.id == r.id)]
        if len(b) and np.isfinite(b.decalage_empirique.iloc[0]):
            agree.append({"evenement": r.evenement, "id": r.id, "a": r.decalage_principal, "b": float(b.decalage_empirique.iloc[0]),
                          "meme_signe": bool(np.sign(r.decalage_principal) == np.sign(b.decalage_empirique.iloc[0]))})
    p2 = {"cas": agree, "part_meme_signe": float(np.mean([x["meme_signe"] for x in agree])) if agree else None}
    p2["verifiee"] = p2["part_meme_signe"] is not None and p2["part_meme_signe"] >= 0.75
    p3 = {}
    if len(D):
        ac = D[D.decalage.str.startswith(("(a)", "(c)"))]
        p3["par_marqueur_tg_alt_vitd"] = {m: bool((ac[ac.id == m].rho >= 0.5).any()) for m in ("tg_fast", "alt", "vitd")}
        mx = D.groupby("id").rho.max()
        p3["marqueurs_avec_decalage_et_intervention"] = int(len(mx))
        p3["part_rho_ge_0_5"] = float((mx >= 0.5).mean())
        p3["verifiee"] = all(p3["par_marqueur_tg_alt_vitd"].values()) and p3["part_rho_ge_0_5"] >= 0.5
    return {"P1": p1, "P2": p2, "P3": p3}


def events_table():
    return pd.DataFrame([{"evenement": n, "ids": " ".join(i), "type": t, "cycle_transforme": p, "chiffre": p is not None,
                          "spans_b": " ".join(f"{a}-{b}" for a, b in s), "diffusion_ajustee": adj}
                         for n, i, t, p, _, s, adj in EVENTS])


def synthese(A, Bm, C):
    rows = []
    cd = q1_table()
    for mid in sorted(set(A.id) | set(Bm.id) | (set(C.id) if len(C) else set())):
        a = A[(A.id == mid) & (A.chiffre == True)].dropna(subset=["ratio"]) if "ratio" in A else A.iloc[0:0]  # noqa: E712
        b = Bm[(Bm.id == mid)].dropna(subset=["ratio"])
        src, r, ev = None, np.nan, None
        if len(a):
            i = a.ratio.idxmax(); r, ev, src = a.ratio[i], a.evenement[i], "(a)"
        noa = set(Bm[Bm.id == mid].evenement) - set(A[(A.id == mid) & (A.chiffre == True)].evenement)  # noqa: E712
        bb = b[b.evenement.isin(noa)]
        if len(bb) and (not np.isfinite(r) or bb.ratio.max() > r):
            i = bb.ratio.idxmax(); r, ev, src = bb.ratio[i], bb.evenement[i], "(b), empirique"
        c = C[(C.id == mid) & C.principale] if len(C) else C
        rows.append({"id": mid, "ratio_max": r, "evenement": ev, "source": src, "categorie": category(r),
                     "ratio_entre_labos_c": float(c.ratio.max()) if len(c) else np.nan,
                     "cd_deux_labos_hausse": float(c.cd_deux_labos_hausse.max()) if len(c) and "cd_deux_labos_hausse" in c else np.nan,
                     "cd_meme_labo_hausse": float(cd.loc[SAME.get(mid, mid), "cd6m_hausse"]) if SAME.get(mid, mid) in cd.index else np.nan})
    return pd.DataFrame(rows)


def run(do_b=True):
    cd = q1_table()
    d = load()
    ver = verifications(d)
    (OUT / "Q5_verifications.json").write_text(json.dumps(ver, indent=2, ensure_ascii=False), encoding="utf-8")
    events_table().to_csv(OUT / "Q5_evenements.csv", index=False)
    A, trans = part_a(d, cd)
    A.to_csv(OUT / "Q5_passage.csv", index=False)
    Bm = part_b(d, cd) if do_b else pd.read_csv(OUT / "Q5_empirique.csv")
    Bm.to_csv(OUT / "Q5_empirique.csv", index=False)
    classification(trans).to_csv(OUT / "Q5_classification.csv", index=False)
    C = part_c(cd)
    if len(C):
        C.to_csv(OUT / "Q5_entre_laboratoires.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    D = part_d(A, Bm, C)
    D.to_csv(OUT / "Q5_interventions.csv", index=False)
    synthese(A, Bm, C).to_csv(OUT / "Q5_synthese.csv", index=False)
    pr = predictions(A, Bm, D)
    (OUT / "Q5_predictions.json").write_text(json.dumps(pr, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    return ver, A, Bm, C, D, pr
