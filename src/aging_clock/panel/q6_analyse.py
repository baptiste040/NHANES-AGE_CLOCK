"""Programme « panel », Q6 : analyses (protocole : DECISIONS.md, pre-enregistrement du 2026-11-12)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from . import q6
from . import q6_modele as M
from .intervalles import CLINICAL
from .remesures import OUT

H10 = 120
MIN_DEATHS, MIN_PERIOD, MIN_BAND = 1000, 250, 150
REPL = [  # 68 marqueurs avec replication
    "wbc", "neut_pct", "neut_n", "lymph_pct", "lymph_n", "mono_pct", "mono_n", "eos_pct", "eos_n", "baso_pct", "baso_n",
    "rbc", "hb", "hct", "mcv", "mch", "mchc", "rdw", "plt", "mpv",
    "glu_fast", "glu_serum", "insulin", "hba1c",
    "tc", "ldl", "hdl", "tg_fast", "tg_serum", "non_hdl",
    "alt", "ast", "ggt", "alp", "bili", "albumin", "protein", "globulin",
    "creat", "urea", "egfr", "acr", "na", "k", "cl", "hco3", "ca", "phos", "osmo",
    "crp", "urate", "iron", "rbc_folate", "vitd",
    "homa_ir", "quicki", "tyg", "ldl_hdl", "tg_hdl", "alb_glob", "fib4", "ggt_hdl", "ast_alt", "urea_creat", "osmo_eff",
    "ca_corr", "nlr", "sii"]
DEV_ONLY = ["b12", "hcy"]
FAST = {"glu_fast", "insulin", "tg_fast", "ldl", "homa_ir", "quicki", "tyg", "tg_hdl", "ldl_hdl"}
LIPGLU = {"tc", "ldl", "hdl", "tg_fast", "tg_serum", "non_hdl", "ldl_hdl", "tg_hdl", "tyg", "glu_fast", "glu_serum", "hba1c",
          "insulin", "homa_ir", "quicki"}
CAUSES = {"cardiovasculaire": [1, 5], "cancer": [2]}
PRED = {  # cotes de risque attendus (bas, haut), d'apres les sources lues
    "alt": (1, 0), "ggt": (0, 1), "alp": (0, 1), "bili": (0, 1), "albumin": (1, 0), "hdl": (1, 1), "ldl": (1, 1), "tc": (1, 1),
    "tg_fast": (0, 0), "tg_serum": (0, 1), "rdw": (0, 1), "mcv": (1, 1), "mch": (1, 1), "mchc": (1, 0), "wbc": (0, 1),
    "nlr": (0, 1), "lymph_n": (1, 0), "na": (1, 1), "k": (0, 1), "cl": (1, 0), "egfr": (1, 0), "acr": (0, 1), "urate": (1, 1),
    "glu_fast": (1, 1), "hba1c": (1, 1), "insulin": (0, 0), "homa_ir": (0, 1), "crp": (0, 1), "vitd": (1, 0), "phos": (0, 1),
    "hco3": (1, 0), "urea": (0, 1), "urea_creat": (1, 1), "fib4": (0, 1), "hcy": (0, 1)}


# ------------------------------------------------------------------ donnees
def prepare():
    d = q6.load()
    h, log = q6.harmonise(d)
    p = q6.population(h)
    p["t10"] = np.minimum(p.PERMTH_EXM, H10)
    p["e10"] = ((p.MORTSTAT == 1) & (p.PERMTH_EXM <= H10)).astype(int)
    p["tfull"] = p.PERMTH_EXM
    p["efull"] = (p.MORTSTAT == 1).astype(int)
    p["dev"] = p.cycle.isin(q6.DEV)
    # covariables des sensibilites
    smk = np.select([p.SMQ020 == 2, (p.SMQ020 == 1) & (p.SMQ040 == 3), p.SMQ040.isin([1, 2])], ["jamais", "ancien", "actuel"], "inconnu")
    p["smk_ancien"], p["smk_actuel"], p["smk_inconnu"] = [(smk == s).astype(float) for s in ("ancien", "actuel", "inconnu")]
    p["diab"] = (p.DIQ010 == 1).astype(float)
    p["pir_na"] = p.INDFMPIR.isna().astype(float)
    p["pir"] = p.INDFMPIR.fillna(p.INDFMPIR.median())
    p["bmi_na"] = p.BMXBMI.isna().astype(float)
    p["bmi"] = p.BMXBMI.fillna(p.BMXBMI.median())
    p["rx_lip"], p["rx_hta"] = (p.BPQ100D == 1).astype(float), (p.BPQ050A == 1).astype(float)
    p["rx_diab"] = ((p.DIQ050 == 1) | (p.DIQ070 == 1)).astype(float)
    ok = lambda m: m.fillna(True)  # noqa: E731 (comme intervalles.reference_population)
    p["sain_d1"] = ((p.LBXCOT < 3) & p.BMXBMI.between(18.5, 30) & ok((p.DIQ010 != 1) & (p.DIQ050 != 1) & (p.DIQ070 != 1))
                    & ok(~(p[["MCQ160B", "MCQ160C", "MCQ160D", "MCQ160E", "MCQ160F"]] == 1).any(axis=1)) & ok(p.MCQ160L != 1)
                    & ok(p.MCQ220 != 1) & ok(p.KIQ022 != 1) & ok((p.BPQ050A != 1) & (p.BPQ100D != 1)))
    return p, log


def _scale(mid, x_dev):
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    cd = cd[cd.groupe == "20-79 ans"].drop_duplicates("id").set_index("id")
    ech = cd.loc[mid, "echelle"] if mid in cd.index else "log"
    return bool(ech == "log" and np.all(np.asarray(x_dev) > 0))


def _bmi_basis(b, kn):
    return M.age_basis(b, kn)


# ------------------------------------------------------------------ analyse d'un marqueur
def _arrays(q, time="t10", event="e10", cause=None):
    t = q[time].to_numpy(float)
    e = q[event].to_numpy().astype(bool)
    if cause is not None:
        e = e & q.UCOD_LEADING.isin(cause).to_numpy()
    return q.m.to_numpy(float), q.age.to_numpy(float), q.sex.to_numpy(), t, e


def _summ(r, spec):
    c = r.pop("_curve", None)
    return r, c


def analyse_marker(p, mid, log, boot=M.B_BOOT):
    q = p[p[mid].notna()].assign(m=lambda x: x[mid])
    if mid in FAST:
        q = q[q.WTSAF2YR.notna() & (q.WTSAF2YR > 0)]
    dv, vl = q[q.dev], q[~q.dev]
    spec = M.Spec(dv.m.to_numpy(float), log)
    akn = np.percentile(dv.age, M.KN)
    res = {"id": mid, "echelle": "log" if log else "additive", "n_dev": len(dv), "deces_dev": int(dv.e10.sum()),
           "n_val": len(vl), "deces_val": int(vl.e10.sum()), "grille": [float(spec.grid[0]), float(spec.grid[-1])],
           "centiles_5_95": [float(spec.grid[spec.search[0]]), float(spec.grid[spec.search[-1]])], "mediane": spec.median}
    curves = {}
    m, a, s, t, e = _arrays(dv)
    r, c = _summ(M.fit(m, a, s, t, e, spec, akn), spec)
    res["dev"], curves["dev"] = r, c
    res["boot"] = M.boot_thresholds(m, a, s, t, e, spec, akn, B=boot)
    res["p_inter_sexe_dev"] = M.interaction_p(m, a, s, t, e, spec, akn, (s == 2).astype(float))
    res["p_inter_age_dev"] = M.interaction_p(m, a, s, t, e, spec, akn, (a - 50) / 10)
    # sensibilites (developpement)
    sens = {}
    keep = t > 36
    keep |= ~e  # exclusion des deces des 3 premieres annees (les survivants restent)
    keep = ~(e & (t <= 36))
    sens["1_deces_3_ans_exclus"] = M.fit(m[keep], a[keep], s[keep], t[keep], e[keep], spec, akn, keep_curve=False)
    hz = dv.sain_d1.to_numpy()
    sens["2_population_saine_d1"] = (M.fit(m[hz], a[hz], s[hz], t[hz], e[hz], spec, akn, keep_curve=False)
                                     if e[hz].sum() >= 100 else {"non_estimable": int(e[hz].sum())})
    bkn = np.percentile(dv.bmi, M.KN)
    ex3 = np.column_stack([dv[["smk_ancien", "smk_actuel", "smk_inconnu", "diab", "pir", "pir_na", "bmi_na"]].to_numpy(float),
                           _bmi_basis(dv.bmi.to_numpy(float), bkn)])
    sens["3_ajust_tabac_imc_diabete_revenu"] = M.fit(m, a, s, t, e, spec, akn, extra=ex3, keep_curve=False)
    if mid in LIPGLU:
        ex4 = dv[["rx_lip", "rx_hta", "rx_diab"]].to_numpy(float)
        sens["4_ajust_traitements"] = M.fit(m, a, s, t, e, spec, akn, extra=ex4, keep_curve=False)
    w = (dv.WTSAF2YR if mid in FAST else dv.WTMEC2YR).to_numpy(float)
    okw = w > 0
    sens["5_poids_enquete"] = M.fit(m[okw], a[okw], s[okw], t[okw], e[okw], spec, akn, w=w[okw] / w[okw].mean(), keep_curve=False)
    mf, af, sf, tf, ef = _arrays(dv, "tfull", "efull")
    sens["6_suivi_complet"] = M.fit(mf, af, sf, tf, ef, spec, akn, keep_curve=False)
    res["sensibilites"] = sens
    # validation
    if mid in REPL and vl.e10.sum() >= MIN_PERIOD:
        m2, a2, s2, t2, e2 = _arrays(vl)
        r2, c2 = _summ(M.fit(m2, a2, s2, t2, e2, spec, akn), spec)
        res["val"], curves["val"] = r2, c2
        res["p_inter_sexe_val"] = M.interaction_p(m2, a2, s2, t2, e2, spec, akn, (s2 == 2).astype(float))
        res["p_inter_age_val"] = M.interaction_p(m2, a2, s2, t2, e2, spec, akn, (a2 - 50) / 10)
    # causes (developpement et validation)
    res["causes"] = {}
    for cname, codes in CAUSES.items():
        cc = {}
        for lab, part in (("dev", dv), ("val", vl)):
            if lab == "val" and mid not in REPL:
                continue
            mm, aa, ss, tt, ee = _arrays(part, cause=codes)
            cc[lab] = M.fit(mm, aa, ss, tt, ee, spec, akn, keep_curve=False) if ee.sum() >= 100 else {"non_estimable": int(ee.sum())}
        res["causes"][cname] = cc
    # tranches d'age (1999-2010 reunis)
    res["ages"] = {}
    for lab, (lo, hi) in (("20-59", (20, 59)), ("60-79", (60, 79)), ("30-55", (30, 55))):
        part = q[q.age.between(lo, hi)]
        mm, aa, ss, tt, ee = _arrays(part)
        if ee.sum() < MIN_BAND:
            res["ages"][lab] = {"non_estimable": True, "deces": int(ee.sum())}
            continue
        kk = np.percentile(part.age, M.KN)
        r3, c3 = _summ(M.fit(mm, aa, ss, tt, ee, spec, kk), spec)
        res["ages"][lab], curves["age_" + lab] = r3, c3
    # courbes par sexe (developpement), rapportees si l'interaction est repliquee
    for sx, lab in ((1, "H"), (2, "F")):
        part = dv[dv.sex == sx]
        mm, aa, ss, tt, ee = _arrays(part)
        X = np.column_stack([spec.basis(mm), M.age_basis(aa, akn)])
        b, cov, _ = M.cox_fit(X, tt, ee)
        curves["sexe_" + lab] = M.curve(spec, b, cov)
    return res, {k: _curve_frame(spec, v) for k, v in curves.items()}


def _curve_frame(spec, c):
    return pd.DataFrame({"x": spec.grid, "hr": c["hr"], "lo": c["lo"], "hi": c["hi"], "hr_med": c["hr_med"], "lo_med": c["lo_med"],
                         "hi_med": c["hi_med"]})


# ------------------------------------------------------------------ replication, categories
def sides(r):
    return {s: r["seuil_1_2"][s] is not None for s in ("bas", "haut")}


def replication(res):
    out = {"association": False, "bas": False, "haut": False, "U": False, "seuil_bas_retenu": None, "seuil_haut_retenu": None,
           "forme_retenue": "non répliquée"}
    if "val" not in res:
        out["forme_retenue"] = "non répliquée (pas de validation)"
        return out
    d, v = res["dev"], res["val"]
    out["association"] = d["p_global"] < 0.05 and v["p_global"] < 0.05
    if not out["association"]:
        return out
    for s in ("bas", "haut"):
        out[s] = d["seuil_1_2"][s] is not None and v["seuil_1_2"][s] is not None
        if out[s]:
            ci = res["boot"][s]["ic95"]
            out[f"seuil_{s}_retenu"] = bool(ci and ci[0] <= v["seuil_1_2"][s] <= ci[1])
    out["U"] = out["bas"] and out["haut"]
    out["forme_retenue"] = ("en U ou en J" if out["U"] else "montante" if out["haut"] else "descendante" if out["bas"] else "plate")
    return out


def d1_bounds(mid):
    S = pd.read_csv(OUT / "D1_intervalles_statistiques.csv")
    rows = []
    for sx in ("H", "F"):
        x = S[(S.id == mid) & (S.sexe == sx)]
        if not len(x):
            continue
        x = x[(x.age_min <= 40) & (x.age_max >= 59)] if (x.partition_age.any()) else x
        if not len(x):
            x = S[(S.id == mid) & (S.sexe == sx) & (S.age_min == 40)]
        r = x.iloc[0]
        rows += [("S", sx, "bas", float(r.borne_basse)), ("S", sx, "haut", float(r.borne_haute))]
    for cid, sens, seuil, var, lib, _ in CLINICAL:
        if cid == mid:
            v = seuil * 2.4959 if mid == "vitd" else seuil
            rows.append(("R" + (f" {var}" if var else ""), "H+F", "bas" if sens == "bas" else "haut", float(v)))
    return rows


NON_COMPARABLE = {"rbc_folate": "méthode et unités différentes de D1 (Q6 harmonisé vers la méthode microbiologique)",
                  "osmo": "D1 : osmolalité mesurée ; Q6 : osmolalité calculée"}


def categories(res, rep):
    mid = res["id"]
    out = []
    g0, g1 = res["grille"]
    for typ, sx, side, b in d1_bounds(mid):
        row = {"id": mid, "type": typ, "sexe": sx, "cote": side, "borne": b}
        if mid in NON_COMPARABLE or "val" not in res:
            row["categorie"] = "non estimable"
            row["motif"] = NON_COMPARABLE.get(mid, "pas de validation")
        elif not (g0 <= b <= g1):
            row["categorie"], row["motif"] = "non estimable", "borne hors des centiles 1-99"
        elif not rep[side]:
            row["categorie"], row["motif"] = "intervalle trop strict", "aucun seuil 1,2 retenu de ce côté"
        else:
            ci = res["boot"][side]["ic95"]
            t = res["dev"]["seuil_1_2"][side]
            row["seuil_1_2"], row["ic95"] = t, ci
            if ci is None:
                row["categorie"], row["motif"] = "non estimable", "IC bootstrap non estimable"
            elif ci[0] <= b <= ci[1]:
                row["categorie"] = "conforme au risque"
            elif (side == "haut" and ci[1] < b) or (side == "bas" and ci[0] > b):
                row["categorie"] = "intervalle trop large"
            else:
                row["categorie"] = "intervalle trop strict"
        out.append(row)
    only_r = out and all(r["type"].startswith("R") for r in out)
    if rep.get("U") and only_r:
        out.append({"id": mid, "type": "R", "sexe": "H+F", "cote": "les deux", "categorie": "relation en U non signalée"})
    return out


def net_change(res, s):
    if "non_estimable" in s:
        return None
    d = res["dev"]
    msg = []
    for side in ("bas", "haut"):
        a, b = d["seuil_1_2"][side], s["seuil_1_2"][side]
        if (a is None) != (b is None):
            msg.append(f"côté {side} {'disparaît' if b is None else 'apparaît'}")
        elif a is not None:
            ci = res["boot"][side]["ic95"]
            if ci and not (ci[0] <= b <= ci[1]):
                msg.append(f"seuil {side} hors IC ({b:.3g})")
    return "; ".join(msg)


def predictions(allres, reps):
    rows = []
    for mid, (lo, hi) in PRED.items():
        if mid not in allres:
            continue
        r, rep = allres[mid], reps[mid]
        dside = sides(r["dev"])
        obs_rep = (int(rep["bas"]), int(rep["haut"]))
        obs_dev = (int(dside["bas"]), int(dside["haut"]))
        rows.append({"id": mid, "attendu": {"bas": lo, "haut": hi}, "retenu_validation": {"bas": obs_rep[0], "haut": obs_rep[1]},
                     "developpement": {"bas": obs_dev[0], "haut": obs_dev[1]},
                     "verifiee": (obs_rep == (lo, hi)) if "val" in r else None, "verifiee_developpement": obs_dev == (lo, hi)})
    return rows


# ------------------------------------------------------------------ figures
def figure(mid, res, curves, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=110)
    c = curves["dev"]
    ax.fill_between(c.x, c.lo, c.hi, color="#9ab6d9", alpha=0.45, lw=0)
    ax.plot(c.x, c.hr, color="#1f4e8c", lw=2, label="Développement (1999-2006), IC 95 %")
    if "val" in curves:
        v = curves["val"]
        ax.plot(v.x, v.hr, color="#c0392b", lw=1.6, ls="--", label="Validation (2007-2010)")
    for typ, sx, side, b in d1_bounds(mid):
        if c.x.min() <= b <= c.x.max():
            st = {"H": ":", "F": "-.", "H+F": "-"}[sx]
            col = "#555555" if typ == "S" else "#2e7d32"
            ax.axvline(b, color=col, ls=st, lw=1.1)
    ax.axhline(1.2, color="#999999", lw=0.8)
    ax.axhline(1.5, color="#bbbbbb", lw=0.8)
    ax.axhline(1.0, color="#000000", lw=0.6)
    if res["echelle"] == "log":
        ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(0.7, max(3.0, float(np.nanmax(c.hr)) * 1.1) if np.isfinite(np.nanmax(c.hr)) else 3)
    from matplotlib.ticker import NullFormatter, ScalarFormatter
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(ScalarFormatter())
        axis.set_minor_formatter(NullFormatter())
    ax.set_yticks([0.8, 1.0, 1.2, 1.5, 2.0, 3.0])
    ax.set_xlabel(LABELS.get(mid, mid))
    ax.set_ylabel("HR (référence : minimum entre P5 et P95)")
    from matplotlib.lines import Line2D
    h, l_ = ax.get_legend_handles_labels()
    h += [Line2D([], [], color="#555555", ls=":"), Line2D([], [], color="#555555", ls="-."), Line2D([], [], color="#2e7d32", ls="-")]
    l_ += ["Intervalle S de D1, hommes", "Intervalle S de D1, femmes", "Seuil R de D1"]
    ax.legend(h, l_, fontsize=7, loc="upper center", frameon=False)
    ax.set_title(f"{LABELS.get(mid, mid).split(' (')[0]} : mortalité toutes causes à 10 ans", fontsize=10)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


LABELS = {"wbc": "Leucocytes (G/L)", "neut_pct": "Neutrophiles (%)", "neut_n": "Neutrophiles (G/L)", "lymph_pct": "Lymphocytes (%)",
          "lymph_n": "Lymphocytes (G/L)", "mono_pct": "Monocytes (%)", "mono_n": "Monocytes (G/L)", "eos_pct": "Éosinophiles (%)",
          "eos_n": "Éosinophiles (G/L)", "baso_pct": "Basophiles (%)", "baso_n": "Basophiles (G/L)", "rbc": "Hématies (T/L)",
          "hb": "Hémoglobine (g/dL)", "hct": "Hématocrite (%)", "mcv": "VGM (fL)", "mch": "TCMH (pg)", "mchc": "CCMH (g/dL)",
          "rdw": "RDW (%)", "plt": "Plaquettes (G/L)", "mpv": "VPM (fL)", "glu_fast": "Glycémie à jeun (mg/dL)",
          "glu_serum": "Glycémie sérique (mg/dL)", "insulin": "Insuline à jeun (µU/mL)", "hba1c": "HbA1c (%)",
          "tc": "Cholestérol total (mg/dL)", "ldl": "LDL (mg/dL)", "hdl": "HDL (mg/dL)", "tg_fast": "Triglycérides à jeun (mg/dL)",
          "tg_serum": "Triglycérides sériques (mg/dL)", "non_hdl": "Cholestérol non-HDL (mg/dL)", "alt": "ALAT (U/L)", "ast": "ASAT (U/L)",
          "ggt": "GGT (U/L)", "alp": "PAL (U/L)", "bili": "Bilirubine totale (mg/dL)", "albumin": "Albumine (g/dL)",
          "protein": "Protéines totales (g/dL)", "globulin": "Globulines (g/dL)", "creat": "Créatinine (mg/dL)", "urea": "Urée (mg/dL)",
          "egfr": "DFGe CKD-EPI 2021 (mL/min/1,73 m²)", "acr": "RAC urinaire (mg/g)", "na": "Sodium (mmol/L)", "k": "Potassium (mmol/L)",
          "cl": "Chlorure (mmol/L)", "hco3": "Bicarbonates (mmol/L)", "ca": "Calcium (mg/dL)", "phos": "Phosphore (mg/dL)",
          "osmo": "Osmolalité calculée (mOsm/kg)", "crp": "CRP (mg/dL)", "urate": "Acide urique (mg/dL)", "iron": "Fer sérique (µg/dL)",
          "rbc_folate": "Folates érythrocytaires (nmol/L)", "vitd": "Vitamine D 25-OH (nmol/L)", "homa_ir": "HOMA-IR", "quicki": "QUICKI",
          "tyg": "Indice TyG", "ldl_hdl": "LDL/HDL", "tg_hdl": "TG/HDL", "alb_glob": "Albumine/globulines", "fib4": "FIB-4",
          "ggt_hdl": "GGT/HDL", "ast_alt": "ASAT/ALAT", "urea_creat": "Urée/créatinine", "osmo_eff": "Osmolalité effective (mOsm/kg)",
          "ca_corr": "Calcium corrigé (mg/dL)", "nlr": "Neutrophiles/lymphocytes", "sii": "Indice SII", "b12": "Vitamine B12 (pg/mL)",
          "hcy": "Homocystéine (µmol/L)"}


def redraw_figures():
    """Refait les figures a partir de Q6_courbes.csv et Q6_resultats_bruts.json (sans refaire les modeles)."""
    allres = json.loads((OUT / "Q6_resultats_bruts.json").read_text(encoding="utf-8"))
    cv = pd.read_csv(OUT / "Q6_courbes.csv")
    for mid, r in allres.items():
        c = {k: g.drop(columns=["id", "modele"]) for k, g in cv[cv.id == mid].groupby("modele")}
        figure(mid, r, c, OUT / "figures_q6" / f"{mid}.png")


# ------------------------------------------------------------------ execution
def _job(p, mid, boot):
    q = p[p[mid].notna()]
    if mid in FAST:
        q = q[q.WTSAF2YR.notna() & (q.WTSAF2YR > 0)]
    log = _scale(mid, q[q.dev][mid])
    return mid, analyse_marker(p, mid, log, boot)


def run(n_jobs=4, boot=M.B_BOOT, ids=None):
    p, log = prepare()
    (OUT / "Q6_methodes.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
    ids = ids or REPL + DEV_ONLY
    cols = ["age", "sex", "cycle", "dev", "t10", "e10", "tfull", "efull", "UCOD_LEADING", "WTSAF2YR", "WTMEC2YR", "sain_d1",
            "smk_ancien", "smk_actuel", "smk_inconnu", "diab", "pir", "pir_na", "bmi", "bmi_na", "rx_lip", "rx_hta", "rx_diab"]
    out = Parallel(n_jobs=n_jobs, verbose=5)(delayed(_job)(p[cols + [mid]], mid, boot) for mid in ids)
    allres, allcurves = {}, {}
    for mid, (r, c) in out:
        allres[mid], allcurves[mid] = r, c
    reps = {m: replication(r) for m, r in allres.items()}
    figs = OUT / "figures_q6"
    figs.mkdir(exist_ok=True)
    zones, cats, sens, causes, ages, curv = [], [], [], [], [], []
    for mid, r in allres.items():
        rep = reps[mid]
        d = r["dev"]
        zones.append({"id": mid, "echelle": r["echelle"], "n_dev": r["n_dev"], "deces_dev": r["deces_dev"], "n_val": r["n_val"],
                      "deces_val": r["deces_val"], "mediane": r["mediane"], "p_global_dev": d["p_global"],
                      "p_global_val": r.get("val", {}).get("p_global"), "xmin": d["xmin"], "min_sur_borne": d["min_sur_borne"],
                      "zone_min": d["zone_min"], "forme_dev": d["forme"], "forme_val": r.get("val", {}).get("forme"),
                      **{f"seuil12_{s}": d["seuil_1_2"][s] for s in ("bas", "haut")},
                      **{f"seuil15_{s}": d["seuil_1_5"][s] for s in ("bas", "haut")},
                      **{f"ic95_seuil12_{s}": r["boot"][s]["ic95"] for s in ("bas", "haut")},
                      **{f"part_boot_seuil12_{s}": r["boot"][s]["part"] for s in ("bas", "haut")},
                      **{f"val_seuil12_{s}": r.get("val", {}).get("seuil_1_2", {}).get(s) for s in ("bas", "haut")},
                      "association_retenue": rep["association"], "cote_bas_retenu": rep["bas"], "cote_haut_retenu": rep["haut"],
                      "U_retenue": rep["U"], "seuil_bas_retenu": rep["seuil_bas_retenu"], "seuil_haut_retenu": rep["seuil_haut_retenu"],
                      "forme_retenue": rep["forme_retenue"], "p_inter_sexe_dev": r["p_inter_sexe_dev"],
                      "p_inter_sexe_val": r.get("p_inter_sexe_val"),
                      "inter_sexe_repliquee": bool(r["p_inter_sexe_dev"] < 0.01 and (r.get("p_inter_sexe_val") or 1) < 0.05),
                      "p_inter_age_dev": r["p_inter_age_dev"], "p_inter_age_val": r.get("p_inter_age_val")})
        cats += categories(r, rep)
        for k, s in r["sensibilites"].items():
            sens.append({"id": mid, "sensibilite": k, **({"forme": s.get("forme"), "seuil12_bas": s["seuil_1_2"]["bas"],
                                                         "seuil12_haut": s["seuil_1_2"]["haut"], "deces": s["deces"],
                                                         "changement_net": net_change(r, s)} if "seuil_1_2" in s else {"non_estimable": True})})
        for cname, cc in r["causes"].items():
            row = {"id": mid, "cause": cname}
            for lab, x in cc.items():
                if "seuil_1_2" in x:
                    row |= {f"{lab}_deces": x["deces"], f"{lab}_p": x["p_global"], f"{lab}_forme": x["forme"],
                            f"{lab}_seuil12_bas": x["seuil_1_2"]["bas"], f"{lab}_seuil12_haut": x["seuil_1_2"]["haut"]}
                else:
                    row[f"{lab}_non_estimable"] = x["non_estimable"]
            if "dev_p" in row and "val_p" in row:
                ok = row["dev_p"] < 0.05 and row["val_p"] < 0.05
                row["cote_bas_retenu"] = bool(ok and row["dev_seuil12_bas"] is not None and row["val_seuil12_bas"] is not None)
                row["cote_haut_retenu"] = bool(ok and row["dev_seuil12_haut"] is not None and row["val_seuil12_haut"] is not None)
            causes.append(row)
        for lab, x in r["ages"].items():
            ages.append({"id": mid, "tranche": lab, **({"non_estimable": True, "deces": x["deces"]} if x.get("non_estimable") else
                         {"deces": x["deces"], "p_global": x["p_global"], "forme": x["forme"], "xmin": x["xmin"],
                          "seuil12_bas": x["seuil_1_2"]["bas"], "seuil12_haut": x["seuil_1_2"]["haut"]})})
        for k, c in allcurves[mid].items():
            curv.append(c.assign(id=mid, modele=k))
        figure(mid, r, allcurves[mid], figs / f"{mid}.png")
    pd.DataFrame(zones).to_csv(OUT / "Q6_zones.csv", index=False)
    pd.DataFrame(cats).to_csv(OUT / "Q6_categories.csv", index=False)
    pd.DataFrame(sens).to_csv(OUT / "Q6_sensibilites.csv", index=False)
    pd.DataFrame(causes).to_csv(OUT / "Q6_causes.csv", index=False)
    pd.DataFrame(ages).to_csv(OUT / "Q6_ages.csv", index=False)
    pd.concat(curv).to_csv(OUT / "Q6_courbes.csv", index=False)
    pd.DataFrame([{"id": m, "echelle": r["echelle"], "n_dev": r["n_dev"], "deces_dev": r["deces_dev"], "n_val": r["n_val"],
                   "deces_val": r["deces_val"], "replication": m in REPL} for m, r in allres.items()]).to_csv(OUT / "Q6_marqueurs.csv", index=False)
    (OUT / "Q6_predictions.json").write_text(json.dumps(predictions(allres, reps), indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "Q6_resultats_bruts.json").write_text(json.dumps(allres, indent=0, ensure_ascii=False, default=float), encoding="utf-8")
    return allres, reps


if __name__ == "__main__":
    run()
