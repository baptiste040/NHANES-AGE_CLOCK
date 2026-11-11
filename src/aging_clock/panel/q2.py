"""Programme « panel », Q2 : jeune et heure du prelevement (protocole : DECISIONS.md, 2026-11-11).

A. Jeune chez une meme personne (NHANES III, paires) : d = a + b (F2 - F1), contraste 2 h contre
   10 h ; sensibilite en classes ; contraste direct chez les discordants (< 4 h / >= 8 h).
B. Associations entre personnes : NHANES 1999-2018 (classes de jeune, seance) et NHANES III
   (classes de jeune, heure exacte en spline), ajustees.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .. import nhanes3 as n3
from ..features import rcs_basis
from ..nhanes import download, read_xpt
from .remesures import OUT, PAIRS, RAW, add_derived

SEED = 2026
URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{y}/DataFiles/{f}.xpt"
CYC = [1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017]
SUF = dict(zip(CYC, ["", "_B", "_C", "_D", "_E", "_F", "_G", "_H", "_I", "_J"]))
FAST = {1999: "PH", 2001: "PH_B", 2003: "PH_C", **{y: "FASTQX" + SUF[y] for y in CYC[3:]}}
ADD_SCALE = {"eos_n", "baso_pct", "baso_n", "tyg", "aip", "lpa"}

# Fichiers NHANES 1999-2018 par groupe : {cycle: fichier}, {id: [variables candidates]}
G = {
    "cbc": ({1999: "LAB25", 2001: "L25_B", 2003: "L25_C", **{y: "CBC" + SUF[y] for y in CYC[3:]}},
            {"wbc": ["LBXWBCSI"], "neut_pct": ["LBXNEPCT"], "lymph_pct": ["LBXLYPCT"], "mono_pct": ["LBXMOPCT"],
             "eos_pct": ["LBXEOPCT"], "baso_pct": ["LBXBAPCT"], "rbc": ["LBXRBCSI"], "hb": ["LBXHGB"], "hct": ["LBXHCT"],
             "mcv": ["LBXMCVSI"], "mch": ["LBXMCHSI"], "mchc": ["LBXMC"], "rdw": ["LBXRDW"], "plt": ["LBXPLTSI"], "mpv": ["LBXMPSI"]}),
    "bio": ({1999: "LAB18", 2001: "L40_B", 2003: "L40_C", **{y: "BIOPRO" + SUF[y] for y in CYC[3:]}},
            {"alt": ["LBXSATSI"], "ast": ["LBXSASSI"], "ggt": ["LBXSGTSI"], "alp": ["LBXSAPSI", "LBDSAPSI"],
             "bili": ["LBXSTB", "LBDSTB"], "albumin": ["LBXSAL"], "protein": ["LBXSTP"], "globulin": ["LBXSGB"],
             "creat": ["LBXSCR", "LBDSCR"], "urea": ["LBXSBU"], "na": ["LBXSNASI"], "k": ["LBXSKSI"], "cl": ["LBXSCLSI"],
             "hco3": ["LBXSC3SI"], "osmo": ["LBXSOSSI"], "ca": ["LBXSCA"], "phos": ["LBXSPH", "LBDSPH"], "urate": ["LBXSUA"],
             "iron": ["LBXSIR"], "glu_serum": ["LBXSGL"], "tg_serum": ["LBXSTR"], "ck": ["LBXSCK"]}),
    "ghb": ({1999: "LAB10", 2001: "L10_B", 2003: "L10_C", **{y: "GHB" + SUF[y] for y in CYC[3:]}}, {"hba1c": ["LBXGH"]}),
    "tc": ({1999: "Lab13", 2001: "l13_b", 2003: "l13_c", **{y: "TCHOL" + SUF[y] for y in CYC[3:]}}, {"tc": ["LBXTC"]}),
    "hdl": ({1999: "Lab13", 2001: "l13_b", 2003: "l13_c", **{y: "HDL" + SUF[y] for y in CYC[3:]}}, {"hdl": ["LBDHDL", "LBXHDD", "LBDHDD"]}),
    "crp": ({1999: "LAB11", 2001: "L11_B", 2003: "L11_C", 2005: "CRP_D", 2007: "CRP_E", 2009: "CRP_F"}, {"crp": ["LBXCRP"]}),
    "b12": ({1999: "LAB06", 2001: "L06_B", 2003: "L06NB_C", 2005: "B12_D", 2011: "VITB12_G", 2013: "VITB12_H"}, {"b12": ["LBXB12", "LBDB12"]}),
    "fol": ({1999: "LAB06", 2001: "L06_B", 2003: "L06NB_C", 2005: "FOLATE_D"}, {"rbc_folate": ["LBXRBF"]}),
    "vitd": ({2001: "VID_B", 2003: "VID_C", 2005: "VID_D", **{y: "VID" + SUF[y] for y in CYC[4:]}}, {"vitd": ["LBDVIDMS", "LBXVIDMS"]}),
    "fer": ({1999: "LAB06", 2001: "L06_B", 2005: "FERTIN_D", 2007: "FERTIN_E", 2009: "FERTIN_F", 2015: "FERTIN_I", 2017: "FERTIN_J"},
            {"ferritin": ["LBXFER"]}),
    "tsh": ({1999: "LAB18T4", 2001: "L40T4_B", 2007: "THYROD_E", 2009: "THYROD_F", 2011: "THYROD_G"}, {"tsh": ["LBXTSH", "LBXTSH1"]}),
}


def _xpt(f, y):
    p = RAW / f"{y}_{f}.xpt"
    download(URL.format(y=y, f=f), p)
    return read_xpt(p).set_index("SEQN")


# ------------------------------------------------------------------ donnees
def continuous() -> pd.DataFrame:
    frames = []
    for y in CYC:
        d = _xpt("DEMO" + SUF[y], y)[["RIDAGEYR", "RIAGENDR", "RIDEXPRG", "RIDRETH1", "INDFMPIR"]]
        fa = _xpt(FAST[y], y)
        d = d.join(fa[[c for c in ["PHAFSTHR", "PHAFSTMN", "PHDSESN"] if c in fa]], how="left")
        d = d.join(_xpt("BMX" + SUF[y], y)[["BMXBMI"]], how="left").join(_xpt("DIQ" + SUF[y], y)[["DIQ010"]], how="left")
        for files, vars_ in G.values():
            if y not in files:
                continue
            x = _xpt(files[y], y)
            for mid, cands in vars_.items():
                v = next((c for c in cands if c in x), None)
                if v is not None:
                    d[mid] = x[v].reindex(d.index)
        d["cycle"] = y
        frames.append(d)
    d = pd.concat(frames)
    d = d[d.RIDAGEYR.between(20, 79) & (d.RIDEXPRG != 1)]
    d["fast_h"] = d.PHAFSTHR + d.PHAFSTMN.fillna(0) / 60
    return d.rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})


def _hours(s: pd.Series) -> pd.Series:
    s = s.astype(str).where(s.astype(str).str.contains(":"))
    p = s.str.split(":")
    return p.str[0].astype(float) + p.str[1].astype(float) / 60


def _raw(name, cols):
    lay = n3.layout(n3.RAW / f"{name}.sas")
    cols = ["SEQN"] + cols
    r = pd.read_fwf(n3.RAW / f"{name}.dat", colspecs=[(lay[c][0] - 1, lay[c][1]) for c in cols], names=cols, dtype=str, header=None)
    r["SEQN"] = r.SEQN.astype(int)
    return r.set_index("SEQN")


def nh3() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Examen principal (avec covariables) et second examen, NHANES III, adultes 20-79 non enceintes."""
    n3.FILES.setdefault("adult", "1a/adult")
    v1 = {p[0]: p[3][0] for p in PAIRS if p[3]}
    v2 = {p[0]: p[3][1] for p in PAIRS if p[3]}
    lay = n3.layout(n3.RAW / "lab.sas")
    lab = n3.read_fixed("lab", ["HSAGEIR", "HSSEX", "PHPFAST"] + [v for v in v1.values() if v in lay])
    t1 = _hours(_raw("lab", ["PHPBEST"]).PHPBEST)
    se = n3.read_fixed("labse", ["PHRFAST"] + list(dict.fromkeys(v2.values())))
    t2 = _hours(_raw("labse", ["PHRBEST"]).PHRBEST)
    ex = n3.read_fixed("exam", ["MAPF12R", "BMPBMI"])
    ad = n3.read_fixed("adult", ["DMARETHN", "DMPPIR", "HAD1"])
    e1 = lab[["HSAGEIR", "HSSEX"]].rename(columns={"HSAGEIR": "age", "HSSEX": "sex"})
    e1 = e1.join(ex, how="left").join(ad, how="left")
    e1 = e1[e1.age.between(20, 79) & (e1.MAPF12R != 1)]
    e1["fast_h"], e1["hour"] = lab.PHPFAST.reindex(e1.index), t1.reindex(e1.index)
    for mid, v in v1.items():
        e1[mid] = lab[v].reindex(e1.index) if v in lab else np.nan
    e2 = e1[["age", "sex"]].copy()
    e2["fast_h"], e2["hour"] = se.PHRFAST.reindex(e1.index), t2.reindex(e1.index)
    for mid, v in v2.items():
        e2[mid] = se[v].reindex(e1.index) if v in se else np.nan
    e1, e2 = add_derived(e1), add_derived(e2)
    for e in (e1, e2):
        e["ldl_f"] = np.where(e.tg_fast < 400, e.tc - e.hdl - e.tg_fast / 5, np.nan)
    return e1, e2


# ------------------------------------------------------------------ outils
def _y(x, mid):
    x = np.asarray(x, float)
    return (x, "add") if (mid in ADD_SCALE or np.nanmin(x) <= 0) else (np.log(x), "log")


def _pct(v, scale):
    return float(100 * (np.exp(v) - 1)) if scale == "log" else float(v)


def _boot(fn, n, B, seed=SEED):
    rng = np.random.default_rng(seed)
    out = [fn(rng.integers(0, n, n)) for _ in range(B)]
    out = np.array([o for o in out if o is not None and np.isfinite(o)])
    return [float(np.quantile(out, .025)), float(np.quantile(out, .975))] if len(out) > 20 else [np.nan, np.nan]


MARKERS_A = [p[0] for p in PAIRS if p[3]] + ["homa_ir", "quicki", "tyg", "ldl_f"]


def within(e1, e2, B=2000) -> pd.DataFrame:
    rows = []
    f1, f2 = np.minimum(e1.fast_h, 24), np.minimum(e2.fast_h, 24)
    h1, h2 = e1.hour, e2.hour
    for mid in MARKERS_A:
        if mid not in e1 or e1[mid].isna().all():
            continue
        ok = (e1[mid].notna() & e2[mid].notna() & (e1[mid] > 0 if mid not in ADD_SCALE else True)
              & (e2[mid] > 0 if mid not in ADD_SCALE else True))
        x1, sc = _y(e1[mid][ok], mid)
        x2, _ = _y(e2[mid][ok], mid)
        d = x2 - x1
        F1, F2 = f1[ok].to_numpy(), f2[ok].to_numpy()
        m = np.isfinite(F1) & np.isfinite(F2)
        r = {"id": mid, "echelle": sc}
        # A principal : regression lineaire
        dd, dF = d[m], (F2 - F1)[m]
        r["n_A"] = int(m.sum())
        r["n_ecart_4h"] = int((np.abs(dF) >= 4).sum())
        if r["n_ecart_4h"] >= 30:
            X = np.column_stack([np.ones(len(dd)), dF])

            def eff(i, X=X, dd=dd):
                b = np.linalg.lstsq(X[i], dd[i], rcond=None)[0]
                return b[1] * (2 - 10)
            est = eff(np.arange(len(dd)))
            ci = _boot(eff, len(dd), B)
            r |= {"jeune_A": _pct(est, sc), "jeune_A_ic95": [_pct(c, sc) for c in ci]}
            # sensibilite en classes
            def cls(F):
                return np.column_stack([F < 4, (F >= 4) & (F < 8)]).astype(float)
            Xc = np.column_stack([np.ones(len(dd)), cls(F2[m]) - cls(F1[m])])
            bc = np.linalg.lstsq(Xc, dd, rcond=None)[0]
            r["jeune_A_classes"] = _pct(bc[1], sc)
        # contraste direct
        c1, c2 = F1 < 4, F2 < 4
        a1, a2 = F1 >= 8, F2 >= 8
        disc = (c1 & a2) | (a1 & c2)
        same = ((F1 < 4) & (F2 < 4)) | ((F1 >= 4) & (F1 < 8) & (F2 >= 4) & (F2 < 8)) | (a1 & a2)
        r["n_discordants"] = int(disc.sum())
        if disc.sum() >= 30:
            sign = np.where(c2[disc], 1.0, -1.0)            # +1 : le 2e examen est non a jeun
            dd2 = d[disc] * sign
            s_same = d[same]

            def eff2(i=None):
                return float(np.mean(dd2) - np.mean(sign) * np.mean(s_same))
            r["jeune_direct"] = _pct(eff2(), sc)
            rng = np.random.default_rng(SEED)
            bs = []
            for _ in range(B):
                i, j = rng.integers(0, len(dd2), len(dd2)), rng.integers(0, len(s_same), len(s_same))
                bs.append(np.mean(dd2[i]) - np.mean(sign[i]) * np.mean(s_same[j]))
            r["jeune_direct_ic95"] = [_pct(np.quantile(bs, .025), sc), _pct(np.quantile(bs, .975), sc)]
        # heure chez une meme personne
        H1, H2 = h1[ok].to_numpy(), h2[ok].to_numpy()
        mh = np.isfinite(H1) & np.isfinite(H2)
        r["n_ecart_heure_2h"] = int((np.abs(H2 - H1)[mh] > 2).sum())
        if mh.sum() > 30:
            Xh = np.column_stack([np.ones(mh.sum()), (H2 - H1)[mh]])
            bh = np.linalg.lstsq(Xh, d[mh], rcond=None)[0]
            r["heure_intra_par_h"] = _pct(bh[1], sc)
        rows.append(r)
    return pd.DataFrame(rows)


def _fast_cls(F):
    return np.column_stack([F < 2, (F >= 2) & (F < 4), (F >= 4) & (F < 8), F >= 12]).astype(float)


def _knots(x, k=5):
    return np.quantile(x, [.05, .275, .5, .725, .95][:k])


def between_continuous(d: pd.DataFrame, B=500) -> pd.DataFrame:
    rows = []
    base = d[d.fast_h.notna() & d.PHDSESN.isin([0, 1, 2]) & d.BMXBMI.notna() & d.INDFMPIR.notna()].copy()
    for mid in [m for v in G.values() for m in v[1]]:
        g = base[base[mid].notna()]
        if len(g) < 500:
            continue
        y, sc = _y(g[mid], mid)
        ok = np.isfinite(y)
        g, y = g[ok], y[ok]
        F = g.fast_h.to_numpy()
        kn = _knots(g.age.to_numpy())
        cyc = pd.get_dummies(g.cycle, drop_first=True).to_numpy(float)
        eth = pd.get_dummies(g.RIDRETH1, drop_first=True).to_numpy(float)
        X = np.column_stack([np.ones(len(g)), _fast_cls(F), g.PHDSESN.to_numpy() == 1, g.PHDSESN.to_numpy() == 2,   # 0 matin (reference), 1 apres-midi, 2 soir
                             g.age, rcs_basis(g.age.to_numpy(), kn), g.sex == 2, g.BMXBMI, eth, g.INDFMPIR,
                             g.DIQ010.to_numpy() == 1, cyc]).astype(float)
        w = np.array([(F < 2).sum(), ((F >= 2) & (F < 4)).sum()], float)
        w = w / w.sum() if w.sum() else np.array([.5, .5])

        def fit(i):
            b = np.linalg.lstsq(X[i], y[i], rcond=None)[0]
            return w[0] * b[1] + w[1] * b[2], b[5], b[6]
        est = fit(np.arange(len(y)))
        rng = np.random.default_rng(SEED)
        bs = np.array([fit(rng.integers(0, len(y), len(y))) for _ in range(B)])
        ci = np.quantile(bs, [.025, .975], axis=0)
        rows.append({"id": mid, "echelle": sc, "n_B1": len(y),
                     "jeune_B1": _pct(est[0], sc), "jeune_B1_ic95": [_pct(ci[0, 0], sc), _pct(ci[1, 0], sc)],
                     "apresmidi_B1": _pct(est[1], sc), "apresmidi_B1_ic95": [_pct(ci[0, 1], sc), _pct(ci[1, 1], sc)],
                     "soir_B1": _pct(est[2], sc), "soir_B1_ic95": [_pct(ci[0, 2], sc), _pct(ci[1, 2], sc)]})
    return pd.DataFrame(rows)


def between_nh3(e1: pd.DataFrame, B=500) -> pd.DataFrame:
    rows = []
    base = e1[e1.fast_h.notna() & e1.hour.notna() & e1.BMPBMI.notna() & e1.DMPPIR.notna() & e1.DMARETHN.notna()].copy()
    for mid in MARKERS_A:
        if mid not in base:
            continue
        g = base[base[mid].notna()]
        if len(g) < 500:
            continue
        y, sc = _y(g[mid], mid)
        ok = np.isfinite(y)
        g, y = g[ok], y[ok]
        F = np.minimum(g.fast_h.to_numpy(), 24)
        ka, kh = _knots(g.age.to_numpy()), _knots(g.hour.to_numpy())
        eth = pd.get_dummies(g.DMARETHN, drop_first=True).to_numpy(float)
        Fc = np.column_stack([F < 4, (F >= 4) & (F < 8), F >= 12]).astype(float)   # reference 8-12 h
        X = np.column_stack([np.ones(len(g)), Fc, g.hour, rcs_basis(g.hour.to_numpy(), kh), g.age,
                             rcs_basis(g.age.to_numpy(), ka), g.sex == 2, g.BMPBMI, eth, g.DMPPIR, g.HAD1 == 1]).astype(float)
        nh = 1 + rcs_basis(np.array([8.0]), kh).shape[1]

        def hrow(h):
            return np.concatenate([[h], rcs_basis(np.array([h]), kh)[0]])

        def fit(i):
            b = np.linalg.lstsq(X[i], y[i], rcond=None)[0]
            bh = b[4:4 + nh]
            return b[1], hrow(11) @ bh - hrow(8) @ bh, hrow(16) @ bh - hrow(9) @ bh
        est = fit(np.arange(len(y)))
        rng = np.random.default_rng(SEED)
        bs = np.array([fit(rng.integers(0, len(y), len(y))) for _ in range(B)])
        ci = np.quantile(bs, [.025, .975], axis=0)
        rows.append({"id": mid, "echelle": sc, "n_B3": len(y),
                     "jeune_B3": _pct(est[0], sc), "jeune_B3_ic95": [_pct(ci[0, 0], sc), _pct(ci[1, 0], sc)],
                     "h11_8": _pct(est[1], sc), "h11_8_ic95": [_pct(ci[0, 1], sc), _pct(ci[1, 1], sc)],
                     "h16_9": _pct(est[2], sc), "h16_9_ic95": [_pct(ci[0, 2], sc), _pct(ci[1, 2], sc)]})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ synthese
EXPECT = {"tg_fast": ("jeune", +1), "tg_serum": ("jeune", +1), "glu_fast": ("jeune", +1), "glu_serum": ("jeune", +1),
          "insulin": ("jeune", +1), "homa_ir": ("jeune", +1), "tyg": ("jeune", +1), "quicki": ("jeune", -1),
          "iron": ("heure", -1), "tsh": ("heure", -1), "phos": ("heure", +1), "wbc": ("heure", +1)}


def _ratio(eff, mid, cd, scale):
    if eff is None or not np.isfinite(eff):
        return np.nan
    key = "ldl" if mid == "ldl_f" else mid
    if key not in cd.index:
        return np.nan
    c = cd.loc[key]
    if scale == "add" or c.echelle == "add":
        u = c.get("cd6m_unites")
        return abs(eff) / u if pd.notna(u) and u else np.nan
    s = c.cd6m_hausse if eff > 0 else c.cd6m_baisse
    return abs(eff) / s if pd.notna(s) else np.nan


def run() -> pd.DataFrame:
    OUT.mkdir(parents=True, exist_ok=True)
    e1, e2 = nh3()
    A = within(e1, e2)
    A.to_csv(OUT / "Q2_A_intra.csv", index=False)
    B3 = between_nh3(e1)
    B3.to_csv(OUT / "Q2_B_nhanes3.csv", index=False)
    B1 = between_continuous(continuous())
    B1.to_csv(OUT / "Q2_B_nhanes_1999_2018.csv", index=False)
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    cd = cd[cd.groupe == "20-79 ans"].set_index("id")
    ids = list(dict.fromkeys(list(A.id) + list(B3.id) + list(B1.id)))
    A_, B3_, B1_ = A.set_index("id"), B3.set_index("id"), B1.set_index("id")
    rows = []
    for mid in ids:
        a = A_.loc[mid] if mid in A_.index else None
        b3 = B3_.loc[mid] if mid in B3_.index else None
        b1 = B1_.loc[mid] if mid in B1_.index else None
        sc = (a if a is not None else (b3 if b3 is not None else b1)).echelle
        if a is not None and pd.notna(a.get("jeune_A")):
            fj, fj_ci, fsrc = a.jeune_A, a.jeune_A_ic95, "A (même personne)"
        elif b1 is not None:
            fj, fj_ci, fsrc = b1.jeune_B1, b1.jeune_B1_ic95, "B, NHANES 1999-2018 (association)"
        else:
            fj, fj_ci, fsrc = np.nan, None, "non estimable"
        if b3 is not None:
            hj, hj_ci, hsrc = b3.h11_8, b3.h11_8_ic95, "B, NHANES III, 11 h contre 8 h (association)"
        elif b1 is not None:
            hj, hj_ci, hsrc = b1.apresmidi_B1, b1.apresmidi_B1_ic95, "B, NHANES 1999-2018, après-midi contre matin (association)"
        else:
            hj, hj_ci, hsrc = np.nan, None, "non estimable"
        h16 = b3.h16_9 if b3 is not None else np.nan
        rf, rh, r16 = _ratio(fj, mid, cd, sc), _ratio(hj, mid, cd, sc), _ratio(h16, mid, cd, sc)
        cats = []
        if np.isfinite(rf) and rf >= 1:
            cats.append("à jeun requis")
        if np.isfinite(rh) and rh >= 1:
            cats.append("horaire fixe requis")
        if (np.isfinite(rf) and 0.5 <= rf < 1) or (np.isfinite(rh) and 0.5 <= rh < 1):
            cats.append("à enregistrer et corriger")
        if not cats:
            cats.append("non estimable" if not (np.isfinite(rf) or np.isfinite(rh)) else "indifférent")
        extra = "horaire fixe requis si prélèvements l'après-midi" if np.isfinite(r16) and r16 >= 1 and "horaire fixe requis" not in cats else ""
        exp = EXPECT.get(mid)
        conf = None
        if exp:
            v, ci = (fj, fj_ci) if exp[0] == "jeune" else ((b1.apresmidi_B1, b1.apresmidi_B1_ic95) if b1 is not None else (hj, hj_ci))
            if ci is not None and np.isfinite(v):
                conf = bool(np.sign(v) == exp[1] and (ci[0] > 0 if exp[1] > 0 else ci[1] < 0))
        rows.append({"id": mid, "echelle": sc, "jeune": fj, "jeune_ic95": fj_ci, "jeune_source": fsrc, "ratio_jeune": rf,
                     "heure": hj, "heure_ic95": hj_ci, "heure_source": hsrc, "ratio_heure": rh,
                     "h16_9": h16, "ratio_h16_9": r16, "categorie": " ; ".join(cats), "mention": extra,
                     "attente": f"{exp[0]} {'+' if exp[1] > 0 else '−'}" if exp else "", "attente_confirmee": conf})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "Q2_synthese.csv", index=False)
    (OUT / "Q2_meta.json").write_text(json.dumps({"n_paires_jeune_connu": int((e1.fast_h.notna() & e2.fast_h.notna()).sum()),
                                                   "martin_hopkins": "non estimable : tableau de facteurs publié en figure (Martin 2013, Figure 2), non lisible en texte"},
                                                  indent=1, ensure_ascii=False), encoding="utf-8")
    return t
