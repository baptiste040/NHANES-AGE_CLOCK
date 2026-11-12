"""Fiabilite test-retest sur le second examen de NHANES III (1988-1994) : replication independante.

Protocole : DECISIONS.md, pre-enregistrement NHANES III. Deux etapes :
1. `predictions()` : population (SEQN seulement pour le second examen), parametres issus de
   2001-2002, predictions des trois scenarios, references pour les mesures physiques.
2. `analyse()` : comparaison avec les remesures reelles (apres relecture du pre-enregistrement).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import nhanes3 as n3
from . import retest as r
from .cohort import apply_panel_ranges
from .config import ROOT, load_panel, load_study
from .uncertainty import BLOOD_URINE

SEED, N_DRAWS, N_BOOT = 2026, 1000, 2000
CRP_LOD = 2.1                      # mg/L : limite de detection NHANES III (0,21 mg/dL)
CREAT_CAL = (0.960, -0.184)        # creatinine standardisee (mg/dL), NHANES III (note CDC, Selvin 2007)
INTERPRETED = ["global", "metabolique", "renal", "hepatique", "inflammatoire_hematologique",
               "pheno_pub", "pheno9"]
CENTILES = [50, 90, 95]
OUT = ROOT / "reports" / "checkup_standard" / "fiabilite_nhanes3"
PARAMS_2001 = OUT / "parametres_2001_2002.json"
VECTORS_2001 = ROOT / "data" / "processed" / "vecteurs_variation_2001_2002.csv"

# Variables canoniques -> (fichier, variable examen principal, variable second examen, facteur)
MAP = {
    "albumin": ("lab", "AMPSI", "AMRSI", 1.0), "creatinine": ("lab", "CEPSI", "CERSI", 1.0),
    "glucose": ("lab", "SGPSI", "SGRSI", 1.0), "tg": ("lab", "TRPSI", "TRRSI", 1.0),
    "total_chol": ("lab", "TCPSI", "TCRSI", 1.0), "hdl": ("lab", "HDPSI", "HDRSI", 1.0),
    "alp": ("lab", "APPSI", "APRSI", 1.0), "alt": ("lab", "ATPSI", "ATRSI", 1.0),
    "ast": ("lab", "ASPSI", "ASRSI", 1.0), "ggt": ("lab", "GGPSI", "GGRSI", 1.0),
    "crp": ("lab", "CRP", "CRR", 10.0), "hba1c": ("lab", "GHP", "GHR", 1.0),
    "wbc": ("lab", "WCPSI", "WCRSI", 1.0), "lymph_pct": ("lab", "LMPPCNT", "LMRPCNT", 1.0),
    "rdw": ("lab", "RWP", "RWR", 1.0), "mcv": ("lab", "MVPSI", "MVRSI", 1.0),
    "hb": ("lab", "HGP", "HGR", 1.0), "platelets": ("lab", "PLPSI", "PLRSI", 1.0),
    "sbp": ("exam", "PEPMNK1R", "PERMNK1R", 1.0), "dbp": ("exam", "PEPMNK5R", "PERMNK5R", 1.0),
    "heart_rate": ("exam", "PEP6DR", "PER6DR", 1.0), "bmi": ("exam", "BMPBMI", "BMRBMI", 1.0),
    "waist": ("exam", "BMPWAIST", "BMRWAIST", 1.0),
}
ACR = ("lab", ("UBP", "URP"), ("UBR", "URR"))
BP_READINGS = {"sbp": ["PEP6G1", "PEP6H1", "PEP6I1"], "dbp": ["PEP6G3", "PEP6H3", "PEP6I3"]}


def harmonize(df: pd.DataFrame) -> pd.DataFrame:
    """Methodes NHANES III -> reference du modele : creatinine recalibree ; CRP censuree a la LD."""
    df = df.copy()
    mgdl = df["creatinine"] / 88.42
    df["creatinine"] = (CREAT_CAL[0] * mgdl + CREAT_CAL[1]) * 88.42
    df["crp"] = df["crp"].clip(lower=CRP_LOD)
    return df


def primary_exam() -> pd.DataFrame:
    labv = [v[1] for v in MAP.values() if v[0] == "lab"] + list(ACR[1])
    examv = [v[1] for v in MAP.values() if v[0] == "exam"] + sum(BP_READINGS.values(), [])
    lab = n3.read_fixed("lab", ["HSAGEIR", "HSSEX", "MXPSESSR", "PHPFAST"] + labv)
    exam = n3.read_fixed("exam", ["MAPF12R"] + examv)
    d = lab.join(exam, how="inner")
    out = pd.DataFrame(index=d.index)
    out["age"], out["sex"] = d["HSAGEIR"], d["HSSEX"]
    out["pregnant"] = (d["MAPF12R"] == 1).astype(float)
    for v, (f, p, _, k) in MAP.items():
        out[v] = d[p] * k
    out["acr"] = d[ACR[1][0]] / d[ACR[1][1]] * 11.31
    out["seance_1"], out["jeune_1_h"] = d["MXPSESSR"], d["PHPFAST"]
    for v, cols in BP_READINGS.items():
        out[[f"{v}_l{i + 1}" for i in range(3)]] = d[cols].to_numpy()
    mort = n3.load_mortality()
    out = out.join(mort[["ELIGSTAT", "PERMTH_EXM"]], how="left")
    return out


def population() -> tuple[pd.DataFrame, list]:
    study = load_study()
    panel = load_panel("checkup_standard")
    pop = study["population"]
    d = primary_exam()
    flow = [("NHANES III, examen principal (lab + examen)", len(d))]
    d = d[d["age"].between(pop["age_min"], pop["age_max"])]
    flow.append((f"age {pop['age_min']}-{pop['age_max']} ans", len(d)))
    d = d[(d["ELIGSTAT"] == 1) & (d["PERMTH_EXM"] > 0)]
    flow.append(("eligibles au chainage mortalite, suivi > 0", len(d)))
    d = d[d["pregnant"] != 1]
    flow.append(("hors femmes enceintes", len(d)))
    d = harmonize(d)
    d, _ = apply_panel_ranges(d, panel)
    d = d.dropna(subset=panel.model_variables + ["sex"])
    flow.append(("cas complets sur le panel", len(d)))
    second = n3.seqn_only("labse") & n3.seqn_only("examse")
    d = d[d.index.isin(second)]
    flow.append(("presents au second examen (labse et examse)", len(d)))
    d.index.name = "SEQN"
    return d.reset_index(), flow


# ------------------------------------------------------------------ parametres 2001-2002
def params_2001() -> dict:
    """CV classiques, correlations (Spearman) et vecteurs de variation de 2001-2002."""
    from .retest_explore import _paired
    e1, e2, blood, _ = _paired()
    dlog = pd.DataFrame({v: np.log(e2[v].to_numpy(float)) - np.log(e1[v].to_numpy(float))
                         for v in blood})
    VECTORS_2001.parent.mkdir(parents=True, exist_ok=True)
    dlog.to_csv(VECTORS_2001, index=False)
    sd = (dlog.std(ddof=1) / np.sqrt(2))
    return {"n": len(dlog), "sigma_log": sd.to_dict(),
            "cv_pct": {v: float(100 * np.sqrt(np.exp(s ** 2) - 1)) for v, s in sd.items()},
            "spearman": dlog.corr(method="spearman").round(6).to_dict(),
            "sha256_vecteurs": hashlib.sha256(VECTORS_2001.read_bytes()).hexdigest()}


# ------------------------------------------------------------------ simulation
def _noise_factory(scenario: str, variables: list, cfg: dict, p2001: dict, physical: bool):
    """Renvoie f(n, rng) -> matrice (n, len(variables)) de bruit en log."""
    blood = [v for v in variables if v in BLOOD_URINE]
    phys = [v for v in variables if v not in BLOOD_URINE]
    lit = r.cv_scenario(cfg, "principal", True)
    sig_phys = np.array([np.sqrt(np.log1p(lit[v] ** 2)) for v in phys])
    ib = [variables.index(v) for v in blood]
    ip = [variables.index(v) for v in phys]
    if scenario == "1_eflm_independant":
        cv = r.cv_scenario(cfg, "principal", False)
        sig_b = np.array([np.sqrt(np.log1p(cv[v] ** 2)) for v in blood])
        gen_b = lambda n, rng: rng.standard_normal((n, len(blood))) * sig_b
    elif scenario == "2_cv2001_correle":
        sig_b = np.array([p2001["sigma_log"][v] for v in blood])
        R = pd.DataFrame(p2001["spearman"]).loc[blood, blood].to_numpy()
        w, U = np.linalg.eigh(R)
        R = U @ np.diag(np.clip(w, 1e-6, None)) @ U.T
        dd = np.sqrt(np.diag(R))
        L = np.linalg.cholesky(R / np.outer(dd, dd))
        gen_b = lambda n, rng: (rng.standard_normal((n, len(blood))) @ L.T) * sig_b
    elif scenario == "3_vecteurs2001":
        V = pd.read_csv(VECTORS_2001)[blood].to_numpy()
        V = (V - V.mean(axis=0)) / np.sqrt(2)          # amendement 2026-11-10 : centre (bruit seul)
        gen_b = lambda n, rng: V[rng.integers(0, len(V), n)] * np.where(rng.random((n, 1)) < .5, 1, -1)
    else:
        raise ValueError(scenario)

    def f(n, rng):
        z = np.zeros((n, len(variables)))
        z[:, ib] = gen_b(n, rng)
        if physical:
            z[:, ip] = rng.standard_normal((n, len(phys))) * sig_phys
        return z
    return f


SCENARIOS = ["1_eflm_independant", "2_cv2001_correle", "3_vecteurs2001"]


def simulate(df, scorer, variables, noise, n_draws=N_DRAWS, seed=SEED, chunk=100):
    base = df.reset_index(drop=True)
    seeds = np.random.SeedSequence(seed).spawn((len(base) + chunk - 1) // chunk)
    out = None
    for c, start in enumerate(range(0, len(base), chunk)):
        block = base.iloc[start:start + chunk]
        rng = np.random.default_rng(seeds[c])
        rep = block.loc[block.index.repeat(n_draws)].reset_index(drop=True)
        rep[variables] = rep[variables].to_numpy(float) * np.exp(noise(len(rep), rng))
        rep["crp"] = rep["crp"].clip(lower=CRP_LOD)      # meme censure que les donnees reelles
        g = scorer(rep)
        if out is None:
            out = {n: np.empty((len(base), n_draws)) for n in g}
        for n in g:
            out[n][start:start + len(block)] = g[n].reshape(len(block), n_draws)
    return out


def predicted(sims: dict, obs: dict) -> pd.DataFrame:
    t = r.predicted_metrics(sims, obs).set_index("score")
    for n, s in sims.items():
        h = s.shape[1] // 2
        d = np.abs(s[:, :h] - s[:, h:2 * h]).ravel()
        for q in CENTILES:
            t.loc[n, f"p{q}_abs_d"] = float(np.percentile(d, q))
    return t.reset_index()


def loss(table: pd.DataFrame, ratio_col: str, cent_cols: list[str]) -> float:
    """Critere pre-enregistre : moyenne sur les scores interpretes de
    |ln R| + moyenne des |ln(centile predit / centile observe)|."""
    t = table[table["score"].isin(INTERPRETED)]
    return float((np.abs(np.log(t[ratio_col])) +
                  np.mean([np.abs(np.log(t[c])) for c in cent_cols], axis=0)).mean())


# ------------------------------------------------------------------ references physiques
def physical_references(d: pd.DataFrame) -> pd.DataFrame:
    """CV intra-visite (3 lectures de tension), CV de la moyenne de 3 ; litterature."""
    lit = {"sbp": 8.6, "dbp": 8.6, "heart_rate": 8.0, "bmi": 1.5, "waist": 2.0}
    rows = []
    for v, cols in {k: [f"{k}_l{i + 1}" for i in range(3)] for k in BP_READINGS}.items():
        x = d[cols].where(d[cols] > 0)
        x = x[x.notna().sum(axis=1) == 3]
        cv_read = float(100 * np.sqrt((x.var(axis=1, ddof=1) / x.mean(axis=1) ** 2).mean()))
        rows.append({"variable": v, "cv_intra_visite_lecture": cv_read,
                     "cv_intra_visite_moyenne_3": cv_read / np.sqrt(3), "n": len(x),
                     "cv_litterature": lit[v]})
    for v in ["heart_rate", "bmi", "waist"]:
        rows.append({"variable": v, "cv_litterature": lit[v]})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ etape 1
def predictions() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = r.load_cv()
    p2001 = params_2001()
    PARAMS_2001.write_text(json.dumps(p2001, indent=1), encoding="utf-8")
    d, flow = population()
    scorer = r.Scorer()
    variables = list(scorer.model["variables"])
    x = d[["age", "sex"] + variables]
    obs = scorer(x)
    rows = []
    for comp, physical in [("biologique", False), ("complete", True)]:
        for sc in SCENARIOS:
            t = predicted(simulate(x, scorer, variables,
                                   _noise_factory(sc, variables, cfg, p2001, physical)), obs)
            t.insert(0, "scenario", sc)
            t.insert(0, "comparaison", comp)
            rows.append(t)
    pred = pd.concat(rows, ignore_index=True)
    pred.to_csv(OUT / "predictions.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(OUT / "flux_predictions.csv", index=False)
    d[["SEQN"]].to_csv(OUT / "seqn_population.csv", index=False)
    physical_references(primary_exam().loc[lambda z: z["age"].between(20, 79)]).to_csv(
        OUT / "references_physiques.csv", index=False)
    meta = {"n": len(d), "age_moyen": float(d["age"].mean()),
            "pct_femmes": float(100 * (d["sex"] == 2).mean()),
            "pct_crp_a_la_limite": float(100 * (d["crp"] <= CRP_LOD).mean()),
            "sha256_cv": hashlib.sha256(r.CONFIG.read_bytes()).hexdigest(),
            "sha256_parametres_2001": hashlib.sha256(PARAMS_2001.read_bytes()).hexdigest(),
            "sha256_code": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / "meta_predictions.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return OUT


# ------------------------------------------------------------------ etape 2
def second_exam(seqn) -> pd.DataFrame:
    labv = [v[2] for v in MAP.values() if v[0] == "lab"] + list(ACR[2])
    examv = [v[2] for v in MAP.values() if v[0] == "exam"]
    lab = n3.read_fixed("labse", ["MXRSESSR", "PHRFAST", "MXPRDAYS"] + labv)
    exam = n3.read_fixed("examse", ["MXRRDAYS"] + examv)
    d = lab.join(exam, how="outer").reindex(seqn)
    out = pd.DataFrame(index=d.index)
    for v, (f, _, s, k) in MAP.items():
        out[v] = d[s] * k
    out["acr"] = d[ACR[2][0]] / d[ACR[2][1]] * 11.31
    out["seance_2"], out["jeune_2_h"] = d["MXRSESSR"], d["PHRFAST"]
    out["delai_jours"] = d["MXPRDAYS"].fillna(d["MXRRDAYS"])
    return out


def analyse() -> Path:
    meta_p = json.loads((OUT / "meta_predictions.json").read_text(encoding="utf-8"))
    if hashlib.sha256(r.CONFIG.read_bytes()).hexdigest() != meta_p["sha256_cv"]:
        raise RuntimeError("Fichier des CV modifie depuis le pre-enregistrement")
    if hashlib.sha256(PARAMS_2001.read_bytes()).hexdigest() != meta_p["sha256_parametres_2001"]:
        raise RuntimeError("Parametres 2001-2002 modifies depuis le pre-enregistrement")
    cfg = r.load_cv()
    p2001 = json.loads(PARAMS_2001.read_text(encoding="utf-8"))
    panel = load_panel("checkup_standard")
    d, flow = population()
    scorer = r.Scorer()
    V = list(scorer.model["variables"])
    blood = [v for v in V if v in BLOOD_URINE]
    phys = [v for v in V if v not in BLOOD_URINE]
    s2 = harmonize(second_exam(d["SEQN"].to_numpy()))
    s2r, _ = apply_panel_ranges(s2, panel)
    ok_b = s2r[blood].notna().all(axis=1).to_numpy()
    ok_p = s2r[phys].notna().all(axis=1).to_numpy()
    d, s2r = d[ok_b].reset_index(drop=True), s2r[ok_b].reset_index(drop=True)
    flow.append(("second examen : sang et urine complets et plausibles", len(d)))
    ok_p = ok_p[ok_b]
    e1 = d[["age", "sex"] + V].copy()
    e2 = e1.copy()
    e2[blood] = s2r[blood].to_numpy()
    g1, g2 = scorer(e1), scorer(e2)
    res = {}

    # Comparaison principale (partie biologique) et complete (mesures physiques reelles)
    e2c = e2.copy()
    e2c[phys] = s2r[phys].to_numpy()
    sub = ok_p
    flow.append(("second examen : mesures physiques completes et plausibles", int(sub.sum())))
    g2c = scorer(e2c[sub])
    g1c = {n: g1[n][sub] for n in g1}
    comps = {"biologique": (g1, g2, e1, False), "complete": (g1c, g2c, e1[sub], True)}
    rows, losses = [], []
    for comp, (a, b, x, physical) in comps.items():
        for sc in SCENARIOS:
            p = predicted(simulate(x, scorer, V, _noise_factory(sc, V, cfg, p2001, physical)),
                          a).set_index("score")
            for n in a:
                o = r.observed_metrics(a[n], b[n])
                dd = np.abs(b[n] - a[n])
                ci = r._boot_ci(lambda i: r.observed_metrics(a[n][i], b[n][i])["et_intra"], len(dd))
                row = {"comparaison": comp, "scenario": sc, "score": n, "n": len(dd),
                       **{f"obs_{k}": v for k, v in o.items()},
                       **{f"pred_{k}": p.loc[n, k] for k in ["et_intra", "rcv", "cci", "bascule"]},
                       "R": o["et_intra"] / p.loc[n, "et_intra"],
                       "R_ic95": (ci[0] / p.loc[n, "et_intra"], ci[1] / p.loc[n, "et_intra"])}
                for q in CENTILES:
                    row[f"obs_p{q}"] = float(np.percentile(dd, q))
                    row[f"pred_p{q}"] = p.loc[n, f"p{q}_abs_d"]
                    row[f"ratio_p{q}"] = row[f"pred_p{q}"] / row[f"obs_p{q}"]
                row["rcv_empirique_obs"] = row["obs_p95"]
                row["obs_cci_ic95"] = r._boot_ci(lambda i: r.icc_a1(a[n][i], b[n][i]), len(dd))
                rows.append(row)
            t = pd.DataFrame([x_ for x_ in rows if x_["comparaison"] == comp and x_["scenario"] == sc])
            t["R_ic_contient_1"] = t["R_ic95"].apply(lambda c: c[0] <= 1 <= c[1])
            adequate = bool(t[t.score.isin(INTERPRETED)]["R_ic_contient_1"].all() and
                            t[t.score.isin(INTERPRETED)][[f"ratio_p{q}" for q in CENTILES]]
                            .apply(lambda s: s.between(.8, 1.25)).all().all())
            losses.append({"comparaison": comp, "scenario": sc,
                           "perte": loss(t, "R", [f"ratio_p{q}" for q in CENTILES]),
                           "adequat": adequate})
    pd.DataFrame(rows).to_csv(OUT / "comparaison.csv", index=False)
    L = pd.DataFrame(losses)
    L["meilleur"] = L.groupby("comparaison")["perte"].transform("min") == L["perte"]
    L.to_csv(OUT / "choix_scenario.csv", index=False)

    # Decalage systematique (prediction directionnelle de 2001-2002)
    shift = []
    for n in g1:
        dd = g2[n] - g1[n]
        shift.append({"variable": f"score {n}", "moyenne": float(dd.mean()),
                      "ic95": r._boot_ci(lambda i: float(dd[i].mean()), len(dd))})
    for v in blood:
        dl = np.log(e2[v].to_numpy(float)) - np.log(e1[v].to_numpy(float))
        shift.append({"variable": v, "moyenne": float(dl.mean()),
                      "ic95": r._boot_ci(lambda i: float(dl[i].mean()), len(dl))})
    pd.DataFrame(shift).to_csv(OUT / "decalage.csv", index=False)

    # Regle CRP > 10 mg/L (a l'un des deux examens)
    hi = ((e1["crp"] > 10) | (e2["crp"] > 10)).to_numpy()
    crp = []
    for n in g1:
        f = lambda i: (r.observed_metrics(g1[n][i][~hi[i]], g2[n][i][~hi[i]])["et_intra"] /
                       r.observed_metrics(g1[n][i], g2[n][i])["et_intra"])
        crp.append({"score": n, "ratio_obs": f(np.arange(len(hi))), "ic95": r._boot_ci(f, len(hi))})
    pd.DataFrame(crp).assign(n_exclus=int(hi.sum())).to_csv(OUT / "regle_crp.csv", index=False)

    # Marqueurs : CV classiques et robustes observes ; mesures physiques
    mk = []
    allv = blood + phys
    for v in allv:
        m = ok_p if v in phys else np.ones(len(e1), bool)
        x1 = e1[v].to_numpy(float)[m]
        x2 = (s2r[v].to_numpy(float) if v in phys else e2[v].to_numpy(float))[m]
        dl = np.log(x2) - np.log(x1)
        s_mad = 1.4826 * np.median(np.abs(dl - np.median(dl))) / np.sqrt(2)
        mk.append({"variable": v, "n": int(m.sum()), "cv_obs": r.marker_cv(x1, x2),
                   "cv_robuste": float(100 * np.sqrt(np.exp(s_mad ** 2) - 1)),
                   "cv_eflm_ou_litterature": 100 * r.cv_scenario(cfg, "principal", True)[v],
                   "cv_2001_2002": p2001["cv_pct"].get(v), "biais_log_pct": float(100 * dl.mean())})
    pd.DataFrame(mk).to_csv(OUT / "cv_marqueurs.csv", index=False)

    # Facteurs
    info = pd.DataFrame({"delai": s2r["delai_jours"].to_numpy(),
                         "meme_seance": (d["seance_1"].to_numpy() == s2r["seance_2"].to_numpy()),
                         "a_jeun_aux_deux": (d["jeune_1_h"].to_numpy() >= 8) & (s2r["jeune_2_h"].to_numpy() >= 8)})
    fac = []
    groups = {"tous": np.ones(len(info), bool), "meme seance": info["meme_seance"].to_numpy(),
              "seance differente": ~info["meme_seance"].to_numpy(),
              "a jeun aux deux (>= 8 h)": info["a_jeun_aux_deux"].to_numpy()}
    terc = pd.qcut(info["delai"], 3, labels=False, duplicates="drop")
    for t in sorted(terc.dropna().unique()):
        m = (terc == t).to_numpy()
        groups[f"delai tertile {int(t) + 1} ({info['delai'][m].min():.0f}-{info['delai'][m].max():.0f} j)"] = m
    for gname, m in groups.items():
        for n in g1:
            if m.sum() >= 20:
                fac.append({"sous_groupe": gname, "score": n, "n": int(m.sum()),
                            **r.observed_metrics(g1[n][m], g2[n][m])})
    pd.DataFrame(fac).to_csv(OUT / "facteurs.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(OUT / "flux_analyse.csv", index=False)
    meta = {"n_biologique": len(e1), "n_complete": int(sub.sum()), "n_crp_sup_10": int(hi.sum()),
            "delai_median": float(np.nanmedian(info["delai"])),
            "sha256_code": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / "meta_analyse.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return OUT


# ------------------------------------------------------------------ analyses finales (non pre-enregistrees)
NO_ACR = ["metabolique", "hepatique", "inflammatoire_hematologique", "pheno_pub", "pheno9"]


def selection_bias() -> Path:
    """NON PRE-ENREGISTRE (demande du 2026-11-10). Les 781 personnes avec ACR au second examen
    sont-elles representatives ? Fiabilite des scores sans ACR : 781 contre toutes les personnes
    disponibles (sang complet hors ACR) et contre les personnes sans ACR. Mesures physiques fixes."""
    panel = load_panel("checkup_standard")
    d, _ = population()
    scorer = r.Scorer()
    V = list(scorer.model["variables"])
    blood = [v for v in V if v in BLOOD_URINE and v != "acr"]
    s2 = harmonize(second_exam(d["SEQN"].to_numpy()))
    s2r, _ = apply_panel_ranges(s2, panel)
    ok = s2r[blood].notna().all(axis=1).to_numpy()
    d, s2r = d[ok].reset_index(drop=True), s2r[ok].reset_index(drop=True)
    has_acr = s2r["acr"].notna().to_numpy()
    e1 = d[["age", "sex"] + V].copy()
    e2 = e1.copy()
    e2[blood] = s2r[blood].to_numpy()        # ACR du premier examen : sans effet sur ces scores
    g1, g2 = scorer(e1), scorer(e2)
    rows = []
    for n in NO_ACR:
        for label, m in [("avec ACR (analyse principale)", has_acr),
                         ("tous disponibles", np.ones(len(d), bool)),
                         ("sans ACR au second examen", ~has_acr)]:
            a, b = g1[n][m], g2[n][m]
            o = r.observed_metrics(a, b)
            rows.append({"score": n, "groupe": label, "n": int(m.sum()), **o,
                         "et_intra_ic95": r._boot_ci(lambda i: r.observed_metrics(a[i], b[i])["et_intra"], len(a)),
                         "cci_ic95": r._boot_ci(lambda i: r.icc_a1(a[i], b[i]), len(a))})
        rng = np.random.default_rng(SEED)
        ia, ic = np.where(has_acr)[0], np.where(~has_acr)[0]
        rat = []
        for _ in range(N_BOOT):
            x, y = rng.choice(ia, len(ia)), rng.choice(ic, len(ic))
            rat.append(r.observed_metrics(g1[n][y], g2[n][y])["et_intra"] /
                       r.observed_metrics(g1[n][x], g2[n][x])["et_intra"])
        rows.append({"score": n, "groupe": "rapport ET_w sans ACR / avec ACR",
                     "et_intra": float(np.median(rat)),
                     "et_intra_ic95": (float(np.quantile(rat, .025)), float(np.quantile(rat, .975)))})
    pd.DataFrame(rows).to_csv(OUT / "biais_selection_acr.csv", index=False)
    desc = pd.DataFrame({"groupe": np.where(has_acr, "avec ACR", "sans ACR"), "age": d["age"],
                         "femme": (d["sex"] == 2).astype(float),
                         "seance_matin": (d["seance_1"] == 1).astype(float),
                         "ecart_global_1": g1["global"]})
    desc.groupby("groupe").agg(["mean", "count"]).round(3).to_csv(OUT / "biais_selection_caracteristiques.csv")
    return OUT


THRESHOLD_SCORES = {"global": "complet", "cardiovasculaire": "complet", "metabolique": "complet",
                    "renal": "biologique", "hepatique": "biologique",
                    "inflammatoire_hematologique": "biologique"}
THRESHOLDS = ROOT / "models" / "seuils_changement_v1.json"
# Ajout du 2026-11-12 (audit, point 1.3) : signaler que les seuils regroupes ne sont pas independants.
NOTE_REGROUPE = ("Seuil regroupe 2001-2002 + NHANES III : il inclut les 388 personnes de 2001-2002 dont le premier "
                 "examen a servi au developpement du modele (pas une estimation independante).")


def empirical_thresholds() -> Path:
    """NON PRE-ENREGISTRE (demande du 2026-11-10). Seuil empirique de changement significatif :
    95e centile de |ecart_2 - ecart_1|, IC 95 % par bootstrap stratifie par source, avec et sans les
    personnes dont la CRP depasse 10 mg/L a l'un des deux examens.
    Scores sans mesure physique (renal, hepatique, inflammatoire) : 2001-2002 + NHANES III regroupes.
    Scores avec mesures physiques (global, cardiovasculaire, metabolique) : NHANES III seul, ou tout
    est reellement remesure (2001-2002 n'a pas remesure la tension ni les mensurations)."""
    from .retest_explore import _paired
    panel = load_panel("checkup_standard")
    scorer = r.Scorer()
    V = list(scorer.model["variables"])
    blood = [v for v in V if v in BLOOD_URINE]
    phys = [v for v in V if v not in BLOOD_URINE]
    a1, a2, _, _ = _paired()
    s01 = {"g1": scorer(a1), "g2": scorer(a2),
           "crp_hi": ((a1["crp"] > 10) | (a2["crp"] > 10)).to_numpy()}
    d, _ = population()
    s2 = harmonize(second_exam(d["SEQN"].to_numpy()))
    s2r, _ = apply_panel_ranges(s2, panel)
    ok_b = s2r[blood].notna().all(axis=1).to_numpy()
    ok_p = ok_b & s2r[phys].notna().all(axis=1).to_numpy()
    e1 = d[["age", "sex"] + V].reset_index(drop=True)
    e2b = e1.copy()
    e2b.loc[ok_b, blood] = s2r.loc[ok_b, blood].to_numpy()
    e2c = e2b.copy()
    e2c.loc[ok_p, phys] = s2r.loc[ok_p, phys].to_numpy()
    crp_hi3 = ((e1["crp"] > 10) | (e2b["crp"] > 10)).to_numpy()
    nb = {"g1": scorer(e1[ok_b]), "g2": scorer(e2b[ok_b]), "crp_hi": crp_hi3[ok_b]}
    nc = {"g1": scorer(e1[ok_p]), "g2": scorer(e2c[ok_p]), "crp_hi": crp_hi3[ok_p]}
    rng = np.random.default_rng(SEED)
    rows = []
    for n, kind in THRESHOLD_SCORES.items():
        sources = [("NHANES III", nc)] if kind == "complet" else [("2001-2002", s01), ("NHANES III", nb)]
        for rule in ["tous", "sans CRP > 10 mg/L"]:
            parts, diffs = [], []
            for _, s in sources:
                m = np.ones(len(s["crp_hi"]), bool) if rule == "tous" else ~s["crp_hi"]
                dd = (s["g2"][n] - s["g1"][n])[m]
                parts.append(np.abs(dd))
                diffs.append(dd)
            allv = np.concatenate(parts)
            boot = [np.percentile(np.concatenate([p[rng.integers(0, len(p), len(p))] for p in parts]), 95)
                    for _ in range(N_BOOT)]
            rows.append({"score": n, "comparaison": kind, "regle": rule,
                         "sources": " + ".join(s for s, _ in sources), "n": len(allv),
                         "seuil_p95": float(np.percentile(allv, 95)),
                         "ic95_bas": float(np.quantile(boot, .025)), "ic95_haut": float(np.quantile(boot, .975)),
                         "p50": float(np.percentile(allv, 50)), "p90": float(np.percentile(allv, 90)),
                         "gaussien": float(1.96 * np.std(np.concatenate(diffs), ddof=1))})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "seuils_changement.csv", index=False)
    main = t[t.regle == "sans CRP > 10 mg/L"]
    seuils = {"format": "aging-clock-thresholds", "version": 1,
              "definition": ("95e centile de |age biologique 2 - age biologique 1| observe sur des remesures "
                             "a 1-48 jours d'intervalle (NHANES 2001-2002 et NHANES III), en conditions "
                             "standardisees : borne basse pour un suivi reel."),
              "regle_crp": ("Seuils valables si la CRP est <= 10 mg/L aux deux bilans ; au-dela, refaire le "
                            "bilan avant de comparer."),
              "scores": {row.score: {"seuil_ans": round(row.seuil_p95, 2),
                                     "ic95": [round(row.ic95_bas, 2), round(row.ic95_haut, 2)],
                                     "n": int(row.n), "sources": row.sources,
                                     **({"note": NOTE_REGROUPE} if "2001" in row.sources else {})}
                         for row in main.itertuples()},
              "seuils_toutes_personnes": {row.score: round(row.seuil_p95, 2)
                                          for row in t[t.regle == "tous"].itertuples()}}
    THRESHOLDS.write_text(json.dumps(seuils, indent=1, ensure_ascii=False), encoding="utf-8")
    return OUT
