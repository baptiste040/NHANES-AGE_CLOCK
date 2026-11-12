"""Programme « panel », Q3 : populations particulieres (protocole : DECISIONS.md, pre-enregistrement
du 2026-11-11).

Groupes : tres actifs (accelerometre 2003-2006), contraception hormonale (pilule, injectable),
apres la menopause, population favorisee. NHANES 2003-2010 (methodes de laboratoire de D1).
Mesures : decalage (regression mediane), taux hors seuil D1 chez les sains du groupe compare a la
population de reference D1, centile « population generale » de la mediane du groupe favorise.

`groups()` ne lit aucune valeur de marqueur (effectifs du pre-enregistrement).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from ..features import rcs_basis
from . import intervalles
from .accelerometre import OUTF as ACC
from .q2 import _knots, _xpt
from .q5 import _with_derived
from .remesures import OUT

SEED, B = 2026, 500
VITD_NG_TO_NMOL = 2.4959
SUF = {2003: "_C", 2005: "_D", 2007: "_E", 2009: "_F"}
FILES = {  # id : ({cycle: fichier}, variable)
    **{k: (intervalles.LAB["cbc"][0], v) for v, k in intervalles.LAB["cbc"][1].items()},
    **{k: (intervalles.LAB["bio"][0], v) for v, k in intervalles.LAB["bio"][1].items()},
    "ck": (intervalles.LAB["bio"][0], "LBXSCK"), "glu_serum": (intervalles.LAB["bio"][0], "LBXSGL"),
    "tc": (intervalles.LAB["tc"][0], "LBXTC"),
    "hdl": (intervalles.LAB["hdl"][0], ["LBXHDD", "LBDHDD"]),
    "insulin": (intervalles.LAB["ins"][0], "LBXIN"),
    "glu_fast": ({2003: "L10AM_C", 2005: "GLU_D", 2007: "GLU_E", 2009: "GLU_F"}, "LBXGLU"),
    "tg_fast": ({2003: "L13AM_C", 2005: "TRIGLY_D", 2007: "TRIGLY_E", 2009: "TRIGLY_F"}, "LBXTR"),
    "hba1c": ({2003: "L10_C", 2005: "GHB_D", 2007: "GHB_E", 2009: "GHB_F"}, "LBXGH"),
    "crp": (intervalles.LAB["crp"][0], "LBXCRP"),
    "b12": (intervalles.LAB["b12fol"][0], "LBXB12"),
    "rbc_folate": (intervalles.LAB["fol"][0], "LBXRBF"),
    "ferritin": (intervalles.LAB["fer"][0], "LBXFER"),
    "tibc": (intervalles.LAB["fe"][0], "LBXTIB"), "tsat": (intervalles.LAB["fe"][0], "LBDPCT"),
    "hcy": (intervalles.LAB["hcy"][0], "LBXHCY"),
    "apob": (intervalles.LAB["apob"][0], "LBXAPB"),
    "u_alb": ({2003: "L16_C", 2005: "ALB_CR_D", 2007: "ALB_CR_E", 2009: "ALB_CR_F"}, "URXUMA"),
    "u_creat": ({2003: "L16_C", 2005: "ALB_CR_D", 2007: "ALB_CR_E", 2009: "ALB_CR_F"}, "URXUCR"),
    "vitd": ({2003: "VID_C", 2005: "VID_D", 2007: "VID_E", 2009: "VID_F"}, ["LBXVIDMS", "LBDVIDMS"]),
}
FASTING = {"glu_fast", "insulin", "tg_fast", "ldl", "homa_ir", "quicki", "tyg", "tg_hdl", "aip", "ldl_hdl"}
DERIVED_IDS = ["egfr", "non_hdl", "ldl", "acr", "homa_ir", "quicki", "tyg", "tg_hdl", "aip", "ldl_hdl", "alb_glob", "fib4",
               "ggt_hdl", "ast_alt", "urea_creat", "nlr", "sii", "ca_corr", "eag"]

# ordonnances (RXQ_RX, 30 derniers jours)
COC = r"ETHINYL ESTRADIOL|MESTRANOL"
PATCH_RING = r"NORELGESTROMIN|ETONOGESTREL"
POP = r"^(?:NORETHINDRONE|NORGESTREL)$"
HRT_RX = r"ESTRADIOL|ESTROGEN|ESTROPIPATE|ESTRIOL|MEDROXYPROGESTERONE|^PROGESTERONE|NORETHINDRONE"


# ------------------------------------------------------------------ groupes (sans marqueur)
def _pick(x, cols):
    return x[[c for c in cols if c in x]]


def questionnaire() -> pd.DataFrame:
    F = []
    for y, s in SUF.items():
        d = _xpt("DEMO" + s, y)[["RIDAGEYR", "RIAGENDR", "RIDEXPRG", "RIDRETH1", "INDFMPIR", "DMDEDUC2", "WTMEC2YR"]]
        d = d.join(_xpt(intervalles.COT[y], y)[["LBXCOT"]]).join(_xpt("BMX" + s, y)[["BMXBMI"]])
        d = d.join(_pick(_xpt("RHQ" + s, y), ["RHQ031", "RHD042", "RHD280", "RHD442", "RHQ520", "RHQ558", "RHQ566",
                                              "RHQ574", "RHQ584", "RHQ600"]))
        d = d.join(_xpt("SMQ" + s, y)[["SMQ020", "SMQ040"]])
        p = _xpt("PAQ" + s, y)
        if y >= 2007:
            vig = pd.Series(np.where(p.PAQ650 == 1, p.PAQ655 * p.PAD660, 0.0), index=p.index).where(p.PAQ650.isin([1, 2]))
        else:
            ia = _xpt("PAQIAF" + s, y)
            ia = ia[ia.PADLEVEL == 2]
            v = (ia.PADTIMES * ia.PADDURAT).groupby(level=0).sum() / 30 * 7
            vig = pd.Series(0.0, index=p.index).add(v, fill_value=0).reindex(p.index)
        d["vig_min_sem"] = vig
        rx = _xpt("RXQ_RX" + s, y)
        drug = rx.RXDDRUG.astype(str).str.strip()
        for name, pat in (("rx_coc", COC), ("rx_patch_anneau", PATCH_RING), ("rx_pop", POP), ("rx_thm", HRT_RX)):
            hit = drug.str.contains(pat, regex=True)
            d[name] = pd.Series(hit.groupby(level=0).any()).reindex(d.index).fillna(False).astype(bool)
        d["cycle"] = y
        F.append(d)
    d = pd.concat(F)
    for c in ["RHQ566", "RHQ600"]:
        if c not in d:
            d[c] = np.nan
    ref, _ = intervalles.reference_population()
    d["sain"] = d.index.isin(ref.index)
    acc = pd.read_csv(ACC).set_index("SEQN")
    d = d.join(acc[["fiable", "jours_valides", "mvpa_min_jour"]], how="left")
    return d.rename(columns={"RIDAGEYR": "age", "RIAGENDR": "sex"})


def groups(q: pd.DataFrame) -> dict:
    """{nom: (masque du groupe, masque de comparaison, sexes, description)} ; masques sur q.index."""
    np_ = q.RIDEXPRG != 1
    a = q.age.between(30, 55) & np_
    G = {}
    # tres actifs : accelerometre 2003-2006
    acc = a & (q.fiable == True) & (q.jours_valides >= 4)  # noqa: E712
    thr_sex = q[acc].groupby("sex").mvpa_min_jour.quantile(.95)
    top_sex = acc & (q.mvpa_min_jour >= q.sex.map(thr_sex))
    thr = q[acc].mvpa_min_jour.quantile(.95)
    top = acc & (q.mvpa_min_jour >= thr)
    G["tres_actifs"] = (top_sex, acc & ~top_sex, (1, 2), f"5 % les plus actifs au sein de chaque sexe (seuils H {thr_sex[1]:.0f}, F {thr_sex[2]:.0f} min/jour)")
    G["tres_actifs_seuil_global"] = (top, acc & ~top, (1, 2), f"5 % les plus actifs, seuil global ({thr:.0f} min/jour)")
    vig = a & q.vig_min_sem.notna()
    G["tres_actifs_questionnaire"] = (vig & (q.vig_min_sem >= 300), vig & (q.vig_min_sem < 300), (1, 2),
                                      "activité vigoureuse de loisir ≥ 300 min/semaine")
    # contraception hormonale : femmes 20-49 non enceintes
    w = (q.sex == 2) & q.age.between(20, 49) & np_
    pill = w & (q.RHD442 == 1) & (q.RHQ520 != 1) & ~q.rx_patch_anneau
    inj = w & (q.RHQ520 == 1) & (q.RHD442 != 1)
    hormonal_rx = q.rx_coc | q.rx_pop | q.rx_patch_anneau
    comp = w & (q.RHD442 != 1) & (q.RHQ520 != 1) & (q.RHQ031 == 1) & ~hormonal_rx
    G["pilule"] = (pill, comp, (2,), "pilule actuelle (RHD442 = 1), sans injectable ni patch ou anneau sur ordonnance")
    G["pilule_oestroprogestative"] = (pill & q.rx_coc, comp, (2,), "pilule + ordonnance d'éthinylestradiol (ou mestranol) oral")
    G["pilule_progestative"] = (pill & q.rx_pop & ~q.rx_coc, comp, (2,), "pilule + ordonnance de progestatif seul (noréthindrone, norgestrel)")
    G["injectable"] = (inj, comp, (2,), "injectable actuel (RHQ520 = 1), sans pilule")
    # apres la menopause : femmes 45-59
    m = (q.sex == 2) & q.age.between(45, 59) & np_
    hrt = (q[["RHQ558", "RHQ566", "RHQ574", "RHQ584", "RHQ600"]] == 1).any(axis=1) | q.rx_thm
    post = m & (q.RHQ031 == 2) & (q.RHD042 == 7) & (q.RHD280 != 1)
    pre = m & (q.RHQ031 == 1) & (q.RHD442 != 1) & ~q.rx_thm & ~hormonal_rx
    G["menopause"] = (post & ~hrt, pre, (2,), "sans règles depuis 12 mois (ménopause), sans hystérectomie ni traitement hormonal")
    G["menopause_thm"] = (post & hrt, pre, (2,), "ménopause sous traitement hormonal (rapporté à part, sans règle)")
    # favorisee
    fav = a & (q.INDFMPIR >= 3.5) & (q.DMDEDUC2 == 5) & (q.LBXCOT < 10) & ((q.SMQ020 == 2) | (q.SMQ040 == 3))
    G["favorisee"] = (fav, a & ~fav, (1, 2), "revenu ≥ 3,5 × seuil de pauvreté, diplôme universitaire, non-fumeur")
    return G


def counts(q, G) -> dict:
    out = {}
    for k, (g, c, sexes, desc) in G.items():
        out[k] = {"definition": desc, "n": int(g.sum()), "n_sains": int((g & q.sain).sum()), "n_comparaison": int(c.sum()),
                  "par_sexe": {("H" if s == 1 else "F"): {"n": int((g & (q.sex == s)).sum()), "n_sains": int((g & q.sain & (q.sex == s)).sum()),
                                                          "n_comparaison": int((c & (q.sex == s)).sum())} for s in sexes}}
    return out


# ------------------------------------------------------------------ marqueurs
def markers(q: pd.DataFrame) -> pd.DataFrame:
    d = q.copy()
    for y in SUF:
        cache = {}
        idx = d.index[d.cycle == y]
        for mid, (files, var) in FILES.items():
            if y not in files:
                continue
            f = files[y]
            if f not in cache:
                cache[f] = _xpt(f, y)
            x = cache[f]
            v = next((c for c in ([var] if isinstance(var, str) else var) if c in x), None)
            if v is None:
                continue
            if mid not in d:
                d[mid] = np.nan
            d.loc[idx, mid] = x[v].reindex(idx)
            if mid == "glu_fast" and "WTSAF2YR" in x:
                if "WTSAF2YR" not in d:
                    d["WTSAF2YR"] = np.nan
                d.loc[idx, "WTSAF2YR"] = x["WTSAF2YR"].reindex(idx)
    # sous-echantillon a jeun : les mesures a jeun n'existent que la ou glu_fast/tg_fast sont mesures
    d = _with_derived(d)
    return d


# ------------------------------------------------------------------ CD de Q1
def q1_cd():
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    a = cd[cd.groupe == "30-55 ans"].drop_duplicates("id").set_index("id")
    b = cd[cd.groupe == "20-79 ans"].drop_duplicates("id").set_index("id")
    a = a.assign(source_cd="30-55 ans")
    b = b.loc[b.index.difference(a.index)].assign(source_cd="20-79 ans (absent du groupe 30-55)")
    return pd.concat([a, b])


def scale(mid, cd):
    return cd.loc[mid, "echelle"] if mid in cd.index else "log"


# ------------------------------------------------------------------ decalage
def _irls(M, y, b0=None, iters=60, tol=1e-7):
    b = np.linalg.lstsq(M, y, rcond=None)[0] if b0 is None else b0
    for _ in range(iters):
        w = 1 / np.maximum(np.abs(y - M @ b), 1e-6)
        sw = np.sqrt(w)
        nb = np.linalg.lstsq(M * sw[:, None], y * sw, rcond=None)[0]
        if np.max(np.abs(nb - b)) < tol:
            return nb
        b = nb
    return b


def _design(sub, both_sexes):
    age = sub.age.to_numpy(float)
    cols = [np.ones(len(sub)), age, rcs_basis(age, _knots(age))]
    if both_sexes:
        cols.append((sub.sex == 2).to_numpy(float))
    cols.append(sub.grp.to_numpy(float))
    return np.column_stack([c if c.ndim > 1 else c[:, None] for c in [np.asarray(c, float) for c in cols]])


def _shift_one(sub, mid, sc, both_sexes, boot=True, seed=SEED):
    x = sub[mid].to_numpy(float)
    ok = np.isfinite(x) & ((x > 0) if sc == "log" else True)
    sub, x = sub[ok], x[ok]
    ng = int(sub.grp.sum())
    res = {"n_groupe": ng, "n_comparaison": int(len(sub) - ng)}
    if ng < 50:
        return res
    y = np.log(x) if sc == "log" else x
    M = _design(sub, both_sexes)
    b = _irls(M, y)
    ols = np.linalg.lstsq(M, y, rcond=None)[0]
    conv = (lambda v: 100 * (np.exp(v) - 1)) if sc == "log" else (lambda v: v)
    res |= {"decalage": float(conv(b[-1])), "decalage_moindres_carres": float(conv(ols[-1]))}
    if boot:
        rng = np.random.default_rng(seed)
        gi, ci = np.where(sub.grp.to_numpy() == 1)[0], np.where(sub.grp.to_numpy() == 0)[0]
        bs = []
        for _ in range(B):
            ix = np.concatenate([rng.choice(gi, len(gi)), rng.choice(ci, len(ci))])
            bb = _irls(M[ix], y[ix], b0=b, iters=30, tol=1e-6)
            bs.append(bb[-1])
        lo, hi = np.quantile(bs, [.025, .975])
        res |= {"ic95": [float(conv(lo)), float(conv(hi))]}
    return res


SHIFT_IDS = None  # fixe dans run()


def shifts(d, G, cd, ids, primary_only=False):
    jobs = []
    for k, (g, c, sexes, _) in G.items():
        strata = [("ensemble", sexes)] + ([("H", (1,)), ("F", (2,))] if len(sexes) == 2 else [])
        for lab, sx in strata:
            m = (g | c) & d.sex.isin(sx)
            sub = d[m].assign(grp=g[m].astype(int))
            for mid in ids:
                if mid not in d:
                    continue
                s = sub
                if mid in FASTING:
                    s = sub[sub.WTSAF2YR.notna() & (sub.WTSAF2YR > 0)]
                jobs.append((k, lab, mid, s[["age", "sex", "grp", mid]], scale(mid, cd), len(sx) == 2))
    out = Parallel(n_jobs=4, verbose=0)(delayed(_shift_one)(s, mid, sc, both) for (_, _, mid, s, sc, both) in jobs)
    rows = []
    for (k, lab, mid, _, sc, both), r in zip(jobs, out):
        rows.append({"groupe": k, "sexe": lab, "id": mid, "echelle": sc, "ajuste_sexe": both, **r})
    return pd.DataFrame(rows)


def cd_side(mid, shift, cd):
    if mid not in cd.index or not np.isfinite(shift):
        return np.nan
    c = cd.loc[mid]
    if c.echelle == "add":
        return c.cd6m_unites
    return c.cd6m_hausse if shift > 0 else c.cd6m_baisse


# ------------------------------------------------------------------ taux hors seuil
def _limits_for(d, S, mid):
    lo = pd.Series(np.nan, index=d.index)
    hi = pd.Series(np.nan, index=d.index)
    for _, r in S[S.id == mid].iterrows():
        m = (d.sex == (1 if r.sexe == "H" else 2)) & d.age.between(r.age_min, r.age_max)
        lo[m], hi[m] = r.borne_basse, r.borne_haute
    return lo, hi


def rates(d, G, S, R):
    """Taux hors seuil chez les sains du groupe et dans la population de reference D1 (meme sexe, meme ages)."""
    rows = []
    ref = d[d.sain]
    for k, (g, c, sexes, _) in G.items():
        gs = d[g & d.sain]
        for sx in sexes:
            a0, a1 = int(d[g].age.min()), int(d[g].age.max())
            gg = gs[gs.sex == sx]
            rr = ref[(ref.sex == sx) & ref.age.between(a0, a1)]
            tests = []
            for mid in S.id.unique():
                if mid not in d:
                    continue
                cyc = [int(c_) for c_ in S[S.id == mid].cycles.iloc[0].split()]
                for side in ("bas", "haut"):
                    tests.append((mid, side, "S", None, cyc))
            for _, r in R.iterrows():
                if r.id in d:
                    tests.append((r.id, r.sens, "R", r, list(SUF)))
            for mid, side, typ, r, cyc in tests:
                vals = []
                for pop in (gg, rr):
                    p = pop[pop.cycle.isin(cyc) & pop[mid].notna()]
                    if mid in FASTING:
                        p = p[p.WTSAF2YR.notna() & (p.WTSAF2YR > 0)]
                    if typ == "S":
                        lo, hi = _limits_for(p, S, mid)
                        out = (p[mid] < lo) if side == "bas" else (p[mid] > hi)
                        ok = lo.notna()
                    else:
                        # LBXVIDMS est en nmol/L, les seuils D1 de la vitamine D en ng/mL (comme Q5)
                        thr = r.seuil * VITD_NG_TO_NMOL if mid == "vitd" else r.seuil
                        out = (p[mid] < thr) if side == "bas" else (p[mid] >= thr)
                        ok = pd.Series(True, index=p.index)
                    vals.append((int(ok.sum()), float(out[ok].mean()) if ok.sum() else np.nan))
                (ng, tg), (nr, tr) = vals
                lab = f"{side} ({typ})" if typ == "S" else f"{r.libelle}" + (f" [{r.variante}]" if isinstance(r.variante, str) else "")
                rows.append({"groupe": k, "sexe": "H" if sx == 1 else "F", "ages": f"{a0}-{a1}", "id": mid, "type": typ,
                             "cote": side, "seuil": lab, "variante": (r.variante if typ == "R" and isinstance(r.variante, str) else None),
                             "n_sains_groupe": ng, "taux_groupe": tg, "n_reference": nr, "taux_reference": tr,
                             "rapport": tg / tr if tr and np.isfinite(tr) and tr > 0 else np.nan})
    t = pd.DataFrame(rows)
    est = t.n_sains_groupe >= 30
    t["regle_taux"] = est & (t.taux_groupe >= 0.10) & ((t.taux_groupe >= 2 * t.taux_reference) | ((t.taux_reference == 0) & (t.taux_groupe > 0)))
    t["estimable"] = est
    return t


# ------------------------------------------------------------------ centile « population generale »
def _wcentile(x, w, v):
    return float(100 * (w[x < v].sum() + 0.5 * w[x == v].sum()) / w.sum())


def centiles(d, G, ids):
    g, c, _, _ = G["favorisee"]
    gen = d[g | c]  # population generale 30-55 ans (non enceintes), favorises compris
    rows = []
    for mid in ids:
        if mid not in d:
            continue
        for sx in (1, 2):
            p = gen[(gen.sex == sx) & gen[mid].notna()]
            wcol = "WTSAF2YR" if mid in FASTING else "WTMEC2YR"
            p = p[p[wcol].notna() & (p[wcol] > 0)]
            x, w = p[mid].to_numpy(float), p[wcol].to_numpy(float)
            for lab, mm in (("favorisée et saine", g & d.sain), ("favorisée", g)):
                f = p[mm.reindex(p.index)]
                if len(f) < 50:
                    rows.append({"id": mid, "sexe": "H" if sx == 1 else "F", "groupe": lab, "n_groupe": len(f)})
                    continue
                med = float(np.median(f[mid]))
                cw = _wcentile(x, w, med)
                cu = _wcentile(x, np.ones_like(x), med)
                rows.append({"id": mid, "sexe": "H" if sx == 1 else "F", "groupe": lab, "n_groupe": len(f), "n_population": len(p),
                             "mediane_groupe": med, "centile_pondere": cw, "centile_non_pondere": cu, "ecart_points": cw - 50,
                             "flatte_10_points": abs(cw - 50) >= 10})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ attentes et synthese
EXPECT = {  # groupe : {id: signe}
    "tres_actifs": {"tg_fast": -1, "tc": -1, "glu_fast": -1, "ferritin": -1, "ck": 1, "hb": -1, "hct": -1,
                    "hdl": 1, "creat": 1, "egfr": -1, "ast": 1, "wbc": -1, "crp": -1, "insulin": -1},
    "pilule": {"tg_fast": 1, "hdl": 1, "ferritin": 1, "crp": 1, "tibc": 1, "albumin": -1, "b12": -1},
    "pilule_oestroprogestative": {"tg_fast": 1, "hdl": 1, "ferritin": 1, "crp": 1, "tibc": 1, "albumin": -1, "b12": -1},
    "menopause": {"tc": 1, "ldl": 1, "tg_fast": 1, "apob": 1, "hdl": -1, "alp": 1, "ferritin": 1, "hb": 1, "urate": 1},
}
SOURCED = {
    "tres_actifs": {"tg_fast": "Lee 2017", "tc": "Lee 2017", "glu_fast": "Lee 2017", "ferritin": "Lee 2017 ; Solberg 2023",
                    "ck": "Lee 2017", "hb": "Mairbäurl 2013", "hct": "Mairbäurl 2013"},
    "pilule": {"tg_fast": "Regidor 2023", "hdl": "Regidor 2023", "ferritin": "Fischer 2021"},
    "pilule_oestroprogestative": {"tg_fast": "Regidor 2023", "hdl": "Regidor 2023", "ferritin": "Fischer 2021"},
    "menopause": {"tc": "Fasero 2025", "ldl": "Fasero 2025", "tg_fast": "Fasero 2025", "apob": "Fasero 2025",
                  "hdl": "Fasero 2025", "alp": "Bhattoa 2025 (marqueurs osseux, dont la PAL osseuse : indirect)"},
}


def expectations(Sh):
    rows = []
    for k, ex in EXPECT.items():
        for mid, sg in ex.items():
            r = Sh[(Sh.groupe == k) & (Sh.sexe == "ensemble") & (Sh.id == mid)]
            if not len(r) or "decalage" not in r or pd.isna(r.decalage.iloc[0]):
                rows.append({"groupe": k, "id": mid, "signe_attendu": sg, "source": SOURCED.get(k, {}).get(mid, "sans source lue"),
                             "statut": "non estimable"})
                continue
            r = r.iloc[0]
            lo, hi = r.ic95
            conf = (np.sign(r.decalage) == sg) and (lo > 0 if sg > 0 else hi < 0)
            contra = (lo > 0 and sg < 0) or (hi < 0 and sg > 0)
            rows.append({"groupe": k, "id": mid, "signe_attendu": sg, "source": SOURCED.get(k, {}).get(mid, "sans source lue"),
                         "decalage": r.decalage, "ic95": [lo, hi],
                         "statut": "confirmée" if conf else ("contredite" if contra else "non confirmée (IC inclut 0)")})
    return rows


def synthese(Sh, T, cd):
    rows = []
    for (k, sx, mid), r in Sh.set_index(["groupe", "sexe", "id"]).iterrows():
        tt = T[(T.groupe == k) & (T.id == mid) & ((T.sexe == sx) if sx != "ensemble" else True)]
        ne_rate = tt.estimable.any() if len(tt) else False
        side_hits = tt[tt.regle_taux]
        sh = r.get("decalage", np.nan)
        cdv = cd_side(mid, sh, cd) if np.isfinite(sh) else np.nan
        cd_hit = bool(np.isfinite(sh) and np.isfinite(cdv) and abs(sh) >= cdv)
        ci = r.get("ic95")
        ci_ex = isinstance(ci, list) and (ci[0] > 0 or ci[1] < 0)
        if cd_hit or len(side_hits):
            cat = "inadapté"
        elif not np.isfinite(sh) and not ne_rate:
            cat = "non estimable"
        elif ci_ex:
            cat = "décalé, sous le changement détectable"
        else:
            cat = "sans différence"
        rows.append({"groupe": k, "sexe": sx, "id": mid, "decalage": sh, "ic95": ci, "cd6m": cdv,
                     "rapport_au_cd": abs(sh) / cdv if np.isfinite(sh) and np.isfinite(cdv) and cdv else np.nan,
                     "regle_cd": cd_hit, "regle_taux": "; ".join(f"{a.sexe} {a.seuil}" for _, a in side_hits.iterrows()),
                     "categorie": cat})
    return pd.DataFrame(rows)


def predictions(T):
    t = T[T.groupe == "tres_actifs"]
    cands = [("creat", "haut", "S"), ("egfr", "bas", "R"), ("ast", "haut", "S"), ("hb", "bas", "S")]
    hits = []
    for mid, side, typ in cands:
        x = t[(t.id == mid) & (t.cote == side) & (t.type == typ) & t.regle_taux]
        hits += [f"{mid} {side} {typ} ({a.sexe})" for _, a in x.iterrows()]
    return {"P1": {"enonce": "Au moins un couple (très actifs, marqueur) « inadapté » par la règle du taux : créatinine (haut S), "
                             "DFGe (< 60), ASAT (haut S) ou hémoglobine (bas S).",
                   "verifiee": bool(hits), "couples": hits}}


def run_after_shifts():
    """Recalcule taux, centiles, synthese et predictions a partir de Q3_decalages.csv (sans refaire le bootstrap)."""
    import ast
    q = questionnaire()
    G = groups(q)
    d = markers(q)
    S = pd.read_csv(OUT / "D1_intervalles_statistiques.csv")
    R = pd.read_csv(OUT / "D1_seuils_cliniques.csv")
    cd = q1_cd()
    Sh = pd.read_csv(OUT / "Q3_decalages.csv")
    Sh["ic95"] = Sh.ic95.apply(lambda s: ast.literal_eval(s) if isinstance(s, str) else s)
    T = rates(d, G, S, R)
    T.to_csv(OUT / "Q3_faux_signaux.csv", index=False)
    Sy = synthese(Sh, T, cd)
    Sy.to_csv(OUT / "Q3_synthese.csv", index=False)
    (OUT / "Q3_attentes.json").write_text(json.dumps(expectations(Sh), indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    (OUT / "Q3_predictions.json").write_text(json.dumps(predictions(T), indent=1, ensure_ascii=False), encoding="utf-8")
    return Sh, T, Sy


def run(only_groups=False):
    q = questionnaire()
    G = groups(q)
    C = counts(q, G)
    (OUT / "Q3_groupes.json").write_text(json.dumps(C, indent=1, ensure_ascii=False), encoding="utf-8")
    if only_groups:
        return C
    d = markers(q)
    S = pd.read_csv(OUT / "D1_intervalles_statistiques.csv")
    R = pd.read_csv(OUT / "D1_seuils_cliniques.csv")
    cd = q1_cd()
    ids = list(dict.fromkeys([*intervalles.STAT_IDS, "ck", "glu_fast", "tg_fast", "hba1c", "vitd", *DERIVED_IDS]))
    ids = [i for i in ids if i in d]
    Sh = shifts(d, G, cd, ids)
    Sh.to_csv(OUT / "Q3_decalages.csv", index=False)
    T = rates(d, G, S, R)
    T.to_csv(OUT / "Q3_faux_signaux.csv", index=False)
    Ce = centiles(d, G, ids)
    Ce.to_csv(OUT / "Q3_centiles_favorisee.csv", index=False)
    Sy = synthese(Sh, T, cd)
    Sy.to_csv(OUT / "Q3_synthese.csv", index=False)
    (OUT / "Q3_attentes.json").write_text(json.dumps(expectations(Sh), indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    (OUT / "Q3_predictions.json").write_text(json.dumps(predictions(T), indent=1, ensure_ascii=False), encoding="utf-8")
    return Sh, T, Ce, Sy


if __name__ == "__main__":
    run()
