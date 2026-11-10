"""Fiabilite test-retest reelle sur les remesures NHANES 2001-2002 (protocole : DECISIONS.md,
pre-enregistrement du 2026-11-10).

Deux etapes, dans cet ordre :
1. `predictions()` : predictions de la simulation Monte-Carlo sur les personnes du second examen,
   a partir de leur PREMIER examen. Des fichiers du second examen, seule la colonne SEQN est
   conservee.
2. `analyse()` : comparaison avec les remesures reelles (lancee apres le commit du
   pre-enregistrement).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import phenoage as pa
from .cohort import apply_panel_ranges, build_cohort
from .config import ROOT, load_panel, load_study
from .nhanes import download, build_harmonized, read_xpt
from .score import bioages, load_model
from .uncertainty import BLOOD_URINE

SECOND_EXAM = ["L40_2_B", "L25_2_B", "L11_2_B", "L10_2_B", "L13_2_B", "L16_2_B"]
BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2001/DataFiles/{file}.xpt"
CYCLE = 2001
CONFIG = ROOT / "config" / "variability_retest.json"
N_DRAWS, SEED, N_BOOT = 1000, 2026, 2000
PHYSICAL = ["sbp", "dbp", "heart_rate", "bmi", "waist"]
SCORES_EXTRA = ["pheno_pub", "pheno9"]

# Second examen -> variables canoniques (memes unites et facteurs que le premier examen 2001)
SECOND_MAP = {
    "total_chol": ("L13_2_B", "LB2TC", 0.02586),
    "hdl": ("L13_2_B", "LB2HDL", 0.02586),
    "tg": ("L40_2_B", "LB2STR", 0.01129),
    "glucose": ("L40_2_B", "LB2SGL", 0.05551),
    "hba1c": ("L10_2_B", "LB2GH", 1.0),
    "creatinine": ("L40_2_B", "LB2SCR", 88.42),
    "alt": ("L40_2_B", "LB2SATSI", 1.0),
    "ast": ("L40_2_B", "LB2SASSI", 1.0),
    "ggt": ("L40_2_B", "LB2SGTSI", 1.0),
    "alp": ("L40_2_B", "LB2SAPSI", 1.0),
    "albumin": ("L40_2_B", "LB2SAL", 10.0),
    "crp": ("L11_2_B", "LB2CRP", 10.0),
    "wbc": ("L25_2_B", "LB2WBCSI", 1.0),
    "lymph_pct": ("L25_2_B", "LB2LYPCT", 1.0),
    "rdw": ("L25_2_B", "LB2RDW", 1.0),
    "mcv": ("L25_2_B", "LB2MCVSI", 1.0),
    "hb": ("L25_2_B", "LB2HGB", 1.0),
    "platelets": ("L25_2_B", "LB2PLTSI", 1.0),
}
# ACR : UR2UMA (ug/mL = mg/L) / UR2UCR (mg/dL) x 11.31 -> mg/mmol, comme le premier examen


# ------------------------------------------------------------------ donnees
def _raw(name: str) -> Path:
    study = load_study()
    return download(BASE_URL.format(file=name), ROOT / study["paths"]["raw"] / f"{CYCLE}_{name}.xpt")


def second_exam_seqn() -> set[int]:
    """SEQN presents dans les six fichiers du second examen. Aucune autre colonne n'est gardee."""
    sets = []
    for f in SECOND_EXAM:
        s = read_xpt(_raw(f))["SEQN"].astype(int)
        sets.append(set(s))
    return set.intersection(*sets)


def load_second_exam() -> pd.DataFrame:
    """Valeurs du second examen en unites canoniques (etape 2 seulement)."""
    frames = {f: read_xpt(_raw(f)).assign(SEQN=lambda d: d["SEQN"].astype(int))
              .set_index("SEQN") for f in SECOND_EXAM}
    out = pd.DataFrame(index=sorted(set.intersection(*[set(f.index) for f in frames.values()])))
    for v, (f, col, k) in SECOND_MAP.items():
        out[v] = frames[f][col].reindex(out.index).astype(float) * k
    u = frames["L16_2_B"]
    out["acr"] = (u["UR2UMA"] / u["UR2UCR"]).reindex(out.index).astype(float) * 11.31
    out["delai_jours"] = frames["L40_2_B"]["LB2DAY"].reindex(out.index)
    out["glycemie_plasma_2"] = frames["L10_2_B"]["LB2GLU"].reindex(out.index).notna()
    out.index.name = "SEQN"
    return out


def first_exam_session() -> pd.DataFrame:
    """Seance et duree de jeune du premier examen (PH_B)."""
    ph = read_xpt(_raw("PH_B"))
    ph["SEQN"] = ph["SEQN"].astype(int)
    # Le lecteur SAS xport de pandas rend les 0 sous la forme 5.4e-79 : arrondi (ecart 2026-11-10)
    return ph.set_index("SEQN")[["PHDSESN", "PHAFSTHR"]].round(6)


def population() -> tuple[pd.DataFrame, list]:
    """Cohorte de developpement, cycle 2001, restreinte aux SEQN du second examen."""
    study = load_study()
    panel = load_panel("checkup_standard")
    h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    co, flow = build_cohort(h, panel, study)
    co = co[co["cycle"] == CYCLE]
    flow.append(("cycle 2001-2002", len(co)))
    co = co[co["SEQN"].astype(int).isin(second_exam_seqn())].reset_index(drop=True)
    flow.append(("present dans les 6 fichiers du second examen", len(co)))
    return co, flow


# ------------------------------------------------------------------ CV
def load_cv(path: Path = CONFIG) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cv_scenario(cfg: dict, scenario: str = "principal", physical: bool = False) -> dict[str, float]:
    """CV totaux (fraction) par variable. physical=False : tension, pouls, IMC, tour de taille fixes."""
    base = cfg["principal"]
    cvi = {v: base[v]["cv_i"] for v in base}
    cva = {v: base[v]["cv_a"] for v in base}
    if scenario == "secondaire":
        cvi.update({k: v for k, v in cfg["secondaire"].items() if not k.startswith("_")})
    elif scenario != "principal":
        s = cfg["sensibilites"][scenario]
        cvi.update(s.get("cv_i", {}))
        cva.update(s.get("cv_a", {}))
    out = {}
    for v in cvi:
        cv = np.sqrt(cvi[v] ** 2 + cva[v] ** 2) / 100.0
        out[v] = cv if (physical or v in BLOOD_URINE) else 0.0
    return out


# ------------------------------------------------------------------ scores
class Scorer:
    """Age global, 5 systemes (modele JSON), PhenoAge publie et reentraine."""

    def __init__(self):
        from .validate import fit_clock
        study = load_study()
        self.model = load_model()
        h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                             cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
        co, _ = build_cohort(h, load_panel("checkup_standard"), study)
        dev = co[co["cycle"].isin(study["cycles"]["development"])].reset_index(drop=True)
        meta9 = json.loads((ROOT / study["paths"]["reports"] / "checkup_standard" /
                            "benchmark_phenoage" / "meta.json").read_text(encoding="utf-8"))
        self.clock9 = fit_clock(dev, load_panel("phenoage9"), study, meta9["penalizer_pheno9"])
        self.accel = pa.fit_acceleration(dev)

    def __call__(self, df: pd.DataFrame) -> dict[str, np.ndarray]:
        """Ecarts a l'age (annees) : age biologique - age ; PhenoAge publie : acceleration."""
        bio, _ = bioages(df, self.model)
        age = df["age"].to_numpy(float)
        out = {n: bio[n] - age for n in bio}
        out["pheno_pub"] = pa.acceleration(df, self.accel)
        out["pheno9"] = self.clock9.predict(df)["gap_global"].to_numpy()
        return out


def simulate(df: pd.DataFrame, scorer: Scorer, cvs: dict, n_draws: int = N_DRAWS,
             seed: int = SEED, chunk: int = 100) -> dict[str, np.ndarray]:
    """Ecarts simules (n_personnes, n_draws) ; bruit log-normal de mediane 1 (comme uncertainty)."""
    variables = list(cvs)
    sig = np.array([np.sqrt(np.log1p(cvs[v] ** 2)) for v in variables])
    base = df.reset_index(drop=True)
    seeds = np.random.SeedSequence(seed).spawn((len(base) + chunk - 1) // chunk)
    out = None
    for c, start in enumerate(range(0, len(base), chunk)):
        block = base.iloc[start:start + chunk]
        rng = np.random.default_rng(seeds[c])
        rep = block.loc[block.index.repeat(n_draws)].reset_index(drop=True)
        rep[variables] = rep[variables].to_numpy(float) * np.exp(
            rng.standard_normal((len(rep), len(variables))) * sig)
        g = scorer(rep)
        if out is None:
            out = {n: np.empty((len(base), n_draws)) for n in g}
        for n in g:
            out[n][start:start + len(block)] = g[n].reshape(len(block), n_draws)
    return out


# ------------------------------------------------------------------ metriques
def predicted_metrics(sims: dict, obs: dict) -> pd.DataFrame:
    """Memes definitions que la precision individuelle (DECISIONS.md), par score."""
    rows = []
    for n, s in sims.items():
        half = s.shape[1] // 2
        sd = s.std(axis=1, ddof=1)
        sd_w = float(np.sqrt(np.mean(sd ** 2)))
        g1, g2 = s[:, :half], s[:, half:2 * half]
        rows.append({"score": n, "et_intra": sd_w, "rcv": 1.96 * np.sqrt(2) * sd_w,
                     "ba_biais": 0.0, "ba_limite": 1.96 * np.sqrt(2) * sd_w,
                     "cci": 1 - sd_w ** 2 / float(np.var(obs[n], ddof=1)),
                     "bascule": float((np.sign(g1) != np.sign(g2)).mean())})
    return pd.DataFrame(rows)


def icc_a1(x1: np.ndarray, x2: np.ndarray) -> float:
    """CCI(A,1), accord absolu, modele a deux facteurs (McGraw et Wong 1996), 2 mesures."""
    y = np.column_stack([x1, x2]).astype(float)
    n, k = y.shape
    gm = y.mean()
    ms_r = k * ((y.mean(axis=1) - gm) ** 2).sum() / (n - 1)
    ms_c = n * ((y.mean(axis=0) - gm) ** 2).sum() / (k - 1)
    resid = y - y.mean(axis=1, keepdims=True) - y.mean(axis=0, keepdims=True) + gm
    ms_e = (resid ** 2).sum() / ((n - 1) * (k - 1))
    return float((ms_r - ms_e) / (ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n))


def observed_metrics(g1: np.ndarray, g2: np.ndarray) -> dict:
    d = g2 - g1
    sd_d = float(np.std(d, ddof=1))
    sd_w = sd_d / np.sqrt(2)
    return {"et_intra": sd_w, "rcv": 1.96 * np.sqrt(2) * sd_w, "ba_biais": float(d.mean()),
            "ba_limite": 1.96 * sd_d, "cci": icc_a1(g1, g2),
            "bascule": float((np.sign(g1) != np.sign(g2)).mean())}


def marker_cv(x1: np.ndarray, x2: np.ndarray) -> float:
    """CV intra-individuel total observe (%) : ET(ln x2 - ln x1)/racine(2), converti en CV."""
    ok = (x1 > 0) & (x2 > 0)
    s = np.std(np.log(x2[ok]) - np.log(x1[ok]), ddof=1) / np.sqrt(2)
    return float(100 * np.sqrt(np.exp(s ** 2) - 1))


# ------------------------------------------------------------------ etape 1
def predictions() -> Path:
    study = load_study()
    out = ROOT / study["paths"]["reports"] / "checkup_standard" / "fiabilite_reelle"
    out.mkdir(parents=True, exist_ok=True)
    cfg = load_cv()
    co, flow = population()
    scorer = Scorer()
    variables = list(scorer.model["variables"])
    d = co[["SEQN", "age", "sex"] + variables].copy()
    obs = scorer(d)

    scenarios = ["principal", "secondaire"] + list(cfg["sensibilites"])
    rows = []
    for comp, physical in [("biologique", False), ("complete", True)]:
        for sc in scenarios:
            if comp == "complete" and sc != "principal":
                continue
            sims = simulate(d[["age", "sex"] + variables], scorer, cv_scenario(cfg, sc, physical))
            t = predicted_metrics(sims, obs)
            t.insert(0, "scenario", sc)
            t.insert(0, "comparaison", comp)
            rows.append(t)
    pred = pd.concat(rows, ignore_index=True)
    pred.to_csv(out / "predictions.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(out / "flux_predictions.csv", index=False)
    co[["SEQN"]].to_csv(out / "seqn_population.csv", index=False)
    meta = {"n": len(d), "tirages": N_DRAWS, "graine": SEED,
            "sha256_cv": hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
            "sha256_code": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "age_moyen": float(d["age"].mean()), "pct_femmes": float(100 * (d["sex"] == 2).mean())}
    (out / "meta_predictions.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out


# ------------------------------------------------------------------ etape 2
def _boot_ci(f, n: int, n_boot: int = N_BOOT, seed: int = SEED) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = [f(rng.integers(0, n, n)) for _ in range(n_boot)]
    return float(np.quantile(vals, .025)), float(np.quantile(vals, .975))


def _compare(g1: dict, g2: dict, pred: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    for n in g1:
        a, b = g1[n], g2[n]
        o = observed_metrics(a, b)
        p = pred.set_index("score").loc[n]
        ratio = o["et_intra"] / p["et_intra"]
        ci_et = _boot_ci(lambda i: observed_metrics(a[i], b[i])["et_intra"], len(a))
        ci_cci = _boot_ci(lambda i: icc_a1(a[i], b[i]), len(a))
        ci_bias = _boot_ci(lambda i: float((b[i] - a[i]).mean()), len(a))
        ci_flip = _boot_ci(lambda i: float((np.sign(a[i]) != np.sign(b[i])).mean()), len(a))
        ci_ratio = (ci_et[0] / p["et_intra"], ci_et[1] / p["et_intra"])
        verdict = ("compatible" if ci_ratio[0] <= 1 <= ci_ratio[1]
                   else "bruit sous-estime par la simulation" if ci_ratio[0] > 1
                   else "bruit surestime par la simulation")
        rows.append({"comparaison": label, "score": n, "n": len(a),
                     **{f"obs_{k}": v for k, v in o.items()},
                     "obs_et_intra_ic95": ci_et, "obs_cci_ic95": ci_cci,
                     "obs_biais_ic95": ci_bias, "obs_bascule_ic95": ci_flip,
                     **{f"pred_{k}": p[k] for k in ["et_intra", "rcv", "ba_limite", "cci", "bascule"]},
                     "ratio_et_obs_pred": ratio, "ratio_ic95": ci_ratio, "verdict": verdict})
    return pd.DataFrame(rows)


def analyse() -> Path:
    study = load_study()
    panel = load_panel("checkup_standard")
    out = ROOT / study["paths"]["reports"] / "checkup_standard" / "fiabilite_reelle"
    meta_pred = json.loads((out / "meta_predictions.json").read_text(encoding="utf-8"))
    if hashlib.sha256(CONFIG.read_bytes()).hexdigest() != meta_pred["sha256_cv"]:
        raise RuntimeError("Fichier des CV modifie depuis le pre-enregistrement")
    cfg = load_cv()
    co, flow = population()
    scorer = Scorer()
    variables = list(scorer.model["variables"])
    blood = [v for v in variables if v in BLOOD_URINE]

    # Second examen : memes plages plausibles que le premier ; cas complets sur le sang et l'urine
    s2 = load_second_exam()
    s2_r, _ = apply_panel_ranges(s2, panel)
    s2_r = s2_r.dropna(subset=blood)
    co = co[co["SEQN"].astype(int).isin(s2_r.index)].reset_index(drop=True)
    flow.append(("valeurs du second examen completes et plausibles (sang, urine)", len(co)))
    e1 = co[["SEQN", "age", "sex"] + variables].copy()
    e2 = e1.copy()
    e2[blood] = s2_r.loc[e1["SEQN"].astype(int), blood].to_numpy()
    ses = first_exam_session().reindex(e1["SEQN"].astype(int))
    info = pd.DataFrame({"SEQN": e1["SEQN"].astype(int).to_numpy(),
                         "delai_jours": s2.loc[e1["SEQN"].astype(int), "delai_jours"].to_numpy(),
                         "seance_1": ses["PHDSESN"].to_numpy(), "jeune_1_h": ses["PHAFSTHR"].to_numpy(),
                         "glycemie_plasma_2": s2.loc[e1["SEQN"].astype(int), "glycemie_plasma_2"].to_numpy()})
    info["a_jeun_aux_deux"] = ((info["seance_1"] == 0) & (info["jeune_1_h"] >= 8)
                               & info["glycemie_plasma_2"]).to_numpy()

    g1, g2 = scorer(e1), scorer(e2)
    x = e1[["age", "sex"] + variables]

    # Predictions recalculees sur la population finale (meme code, memes CV, meme graine)
    pred_bio = predicted_metrics(simulate(x, scorer, cv_scenario(cfg, "principal", False)), g1)
    pred_full = predicted_metrics(simulate(x, scorer, cv_scenario(cfg, "principal", True)), g1)
    pred_sec = predicted_metrics(simulate(x, scorer, cv_scenario(cfg, "secondaire", False)), g1)

    res = [_compare(g1, g2, pred_bio, "biologique (principal)"),
           _compare(g1, g2, pred_sec, "biologique (scenario secondaire)")]

    # Comparaison secondaire : bruit simule des mesures physiques ajoute au second examen
    rng = np.random.default_rng(SEED)
    cv_phys = cv_scenario(cfg, "principal", True)
    draws = []
    for _ in range(200):
        e2b = e2.copy()
        for v in PHYSICAL:
            s = np.sqrt(np.log1p(cv_phys[v] ** 2))
            e2b[v] = e2b[v].to_numpy(float) * np.exp(rng.standard_normal(len(e2b)) * s)
        g2b = scorer(e2b)
        draws.append(pd.DataFrame([{"score": n, **observed_metrics(g1[n], g2b[n])} for n in g1]))
    full = pd.concat(draws).groupby("score", sort=False).mean().reset_index()
    full = full.merge(pred_full.add_prefix("pred_").rename(columns={"pred_score": "score"}), on="score")
    full["ratio_et_obs_pred"] = full["et_intra"] / full["pred_et_intra"]
    full.insert(0, "comparaison", "complete (physique simulee, 200 tirages)")

    # Sous-groupes descriptifs
    sub = []
    groups = {"tous": np.ones(len(info), bool), "a jeun aux deux (indicateur indirect)": info["a_jeun_aux_deux"].to_numpy(),
              "seance 1 = matin": (info["seance_1"] == 0).to_numpy(),
              "seance 1 = apres-midi ou soir": (info["seance_1"] > 0).to_numpy()}
    terc = pd.qcut(info["delai_jours"], 3, labels=["delai T1", "delai T2", "delai T3"])
    for t in terc.cat.categories:
        groups[f"{t} ({info.loc[terc == t, 'delai_jours'].min():.0f}-{info.loc[terc == t, 'delai_jours'].max():.0f} j)"] = (terc == t).to_numpy()
    for gname, m in groups.items():
        if m.sum() < 20:
            sub.append({"sous_groupe": gname, "n": int(m.sum())})
            continue
        for n in g1:
            sub.append({"sous_groupe": gname, "score": n, "n": int(m.sum()),
                        **observed_metrics(g1[n][m], g2[n][m])})
    corr_delay = {n: float(pd.Series(np.abs(g2[n] - g1[n])).corr(info["delai_jours"], method="spearman"))
                  for n in g1}

    # CV intra-individuels observes par marqueur
    mk = []
    for v in blood:
        mk.append({"variable": v, "cv_obs_pct": marker_cv(e1[v].to_numpy(float), e2[v].to_numpy(float)),
                   "cv_obs_ic95": _boot_ci(lambda i: marker_cv(e1[v].to_numpy(float)[i], e2[v].to_numpy(float)[i]), len(e1)),
                   "cv_pred_principal_pct": 100 * cv_scenario(cfg, "principal")[v],
                   "cv_pred_secondaire_pct": 100 * cv_scenario(cfg, "secondaire")[v],
                   "biais_moyen_log_pct": float(100 * np.mean(np.log(e2[v].to_numpy(float) / e1[v].to_numpy(float))))})

    pd.concat(res, ignore_index=True).to_csv(out / "comparaison.csv", index=False)
    full.to_csv(out / "comparaison_complete.csv", index=False)
    pd.DataFrame(sub).to_csv(out / "sous_groupes.csv", index=False)
    pd.DataFrame(mk).to_csv(out / "cv_marqueurs.csv", index=False)
    pd.DataFrame(flow, columns=["etape", "n"]).to_csv(out / "flux_analyse.csv", index=False)
    pd.DataFrame({"score": list(corr_delay), "spearman_abs_diff_delai": list(corr_delay.values())}).to_csv(
        out / "delai.csv", index=False)
    meta = {"n": len(e1), "a_jeun_aux_deux": int(info["a_jeun_aux_deux"].sum()),
            "delai_median": float(info["delai_jours"].median()), "bootstrap": N_BOOT,
            "sha256_code": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out / "meta_analyse.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out


def complete_corrected() -> Path:
    """Comparaison secondaire corrigee (NON pre-enregistree, ecart du 2026-11-10) : bruit physique
    simule independamment sur les DEUX examens (deux mesures reelles en portent chacune un)."""
    study = load_study()
    panel = load_panel("checkup_standard")
    out = ROOT / study["paths"]["reports"] / "checkup_standard" / "fiabilite_reelle"
    cfg = load_cv()
    co, _ = population()
    scorer = Scorer()
    V = list(scorer.model["variables"])
    blood = [v for v in V if v in BLOOD_URINE]
    s2 = load_second_exam()
    s2r, _ = apply_panel_ranges(s2, panel)
    s2r = s2r.dropna(subset=blood)
    co = co[co["SEQN"].astype(int).isin(s2r.index)].reset_index(drop=True)
    e1 = co[["SEQN", "age", "sex"] + V].copy()
    e2 = e1.copy()
    e2[blood] = s2r.loc[e1["SEQN"].astype(int), blood].to_numpy()
    cv = cv_scenario(cfg, "principal", True)
    rng = np.random.default_rng(SEED)
    draws = []
    for _ in range(200):
        a, b = e1.copy(), e2.copy()
        for v in PHYSICAL:
            s = np.sqrt(np.log1p(cv[v] ** 2))
            a[v] = e1[v].to_numpy(float) * np.exp(rng.standard_normal(len(a)) * s)
            b[v] = e1[v].to_numpy(float) * np.exp(rng.standard_normal(len(b)) * s)
        g1, g2 = scorer(a), scorer(b)
        draws.append(pd.DataFrame([{"score": n, **observed_metrics(g1[n], g2[n])} for n in g1]))
    f = pd.concat(draws).groupby("score", sort=False).mean()
    p = pd.read_csv(out / "comparaison_complete.csv").set_index("score")
    f["pred_et_intra"], f["pred_rcv"], f["pred_cci"] = p["pred_et_intra"], p["pred_rcv"], p["pred_cci"]
    f["ratio_et_obs_pred"] = f["et_intra"] / f["pred_et_intra"]
    f.to_csv(out / "comparaison_complete_corrigee_non_preenregistree.csv")
    return out
