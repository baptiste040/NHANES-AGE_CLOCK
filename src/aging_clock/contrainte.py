"""Piste « suivi », etape 1 : variante « sang seul contrainte » (protocole : DECISIONS.md).

Contrainte clinique : une valeur anormale ne rend jamais le score plus favorable. Pour chaque
marqueur et chaque cote anormal (seuils de Q2), si la valeur est au-dela de la limite de la zone
normale, le terme du marqueur dans le predicteur lineaire de chaque modele (global, systemes)
devient le moins favorable des deux : terme a la valeur observee ou terme a la valeur limite.
Une valeur au-dela de la limite dans le sens que le modele recompense compte donc comme la
valeur limite. Pas de reentrainement : memes coefficients que le modele « sang seul ».
"""
from __future__ import annotations

import functools
import json

import numpy as np
import pandas as pd

from .cohort import DURATION, EVENT, build_cohort
from .config import ROOT, load_panel, load_study
from .metrics import bootstrap, calibration, cox_hr, harrell_c, summarize
from .nhanes import build_harmonized
from .suivi import SCORES, THRESHOLDS
from .validate import fit_clock

OUT = ROOT / "reports" / "checkup_sang_seul" / "contrainte"
MATERIAL = 1.0           # seuil materiel de signalement (annees sur le score du systeme)


def limits(df: pd.DataFrame, v: str):
    """(limite basse, limite haute) par personne, ou None."""
    lo, hi = THRESHOLDS[v]
    sex = df["sex"].to_numpy()
    f = lambda t: (np.where(sex == 1, t[0], t[1]).astype(float) if isinstance(t, tuple)  # noqa: E731
                   else np.full(len(df), float(t)))
    return (f(lo) if lo is not None else None), (f(hi) if hi is not None else None)


def abnormal_side(df, v):
    """Masques (au-dela de la limite basse, au-dela de la limite haute) et valeurs limites."""
    x = df[v].to_numpy(float)
    lo, hi = limits(df, v)
    strict_hi = v not in ("glucose", "hba1c", "total_chol", "tg", "acr")
    out = []
    if lo is not None:
        out.append((x < lo, lo))
    if hi is not None:
        out.append(((x > hi) if strict_hi else (x >= hi), hi))
    return out


class ConstrainedClock:
    def __init__(self, clock, markers=None):
        self.clock = clock
        self.markers = [v for v in (markers or THRESHOLDS) if v in clock.panel.model_variables]

    def _terms(self, df):
        """Predicteurs lineaires non contraints et ajustements (recompense indue retiree)."""
        c = self.clock
        df = df.reset_index(drop=True)
        X = c.design(df)
        lp = {n: m.linear_predictor(X) for n, m in c.models.items()}
        adj = {n: np.zeros(len(df)) for n in c.models}
        for v in self.markers:
            for mask, lim in abnormal_side(df, v):
                if not mask.any():
                    continue
                d2 = df.copy()
                d2.loc[mask, v] = lim[mask]
                Xl = c.design(d2)
                for n, m in c.models.items():
                    delta = m.linear_predictor(Xl) - lp[n]     # >0 : la limite est moins favorable
                    adj[n] += np.where(mask & (delta > 0), delta, 0.0)
        return X, lp, adj

    def predict(self, df, constrained=True):
        c = self.clock
        df = df.reset_index(drop=True)
        X, lp, adj = self._terms(df)
        female = X["female"].to_numpy()
        out = pd.DataFrame(index=df.index)
        out["risk_ref"] = c.reference.risk(X)
        for n, m in c.models.items():
            eta = lp[n] + (adj[n] if constrained else 0.0)
            risk = 1.0 - m.s0_ ** np.exp(eta)
            bio = c._invert(risk, female)
            out[f"risk_{n}"], out[f"bioage_{n}"] = risk, bio
            out[f"gap_{n}"] = bio - df["age"].to_numpy()
        return out


def _data():
    study = load_study()
    h = build_harmonized(study["cycles"]["development"] + study["cycles"]["validation"],
                         cache=ROOT / study["paths"]["processed"] / "nhanes_harmonized.csv")
    co, _ = build_cohort(h, load_panel("checkup_standard"), study)
    dev = co[co["cycle"].isin(study["cycles"]["development"])].reset_index(drop=True)
    val = co[co["cycle"].isin(study["cycles"]["validation"])].reset_index(drop=True)
    clock = fit_clock(dev, load_panel("checkup_sang_seul"), study, 0.0)
    return study, dev, val, clock


def _paired(d):
    t, e = d[DURATION].to_numpy(), d[EVENT].to_numpy()
    out = {"C_ref": harrell_c(t, e, d["risk_ref"])}
    for s in SCORES:
        cu, cc = harrell_c(t, e, d[f"u_risk_{s}"]), harrell_c(t, e, d[f"c_risk_{s}"])
        out |= {f"C_libre_{s}": cu, f"C_contraint_{s}": cc, f"gain_contraint_{s}": cc - out["C_ref"],
                f"dC_contraint_moins_libre_{s}": cc - cu}
    return out


def changes(cc: ConstrainedClock, df):
    pu, pc = cc.predict(df, False), cc.predict(df, True)
    rows = []
    for s in SCORES:
        d = pc[f"gap_{s}"] - pu[f"gap_{s}"]
        ch = d > 1e-9
        rows.append({"score": s, "n": len(d), "n_changes": int(ch.sum()), "pct_changes": float(100 * ch.mean()),
                     "changement_median_si_change": float(d[ch].median()) if ch.any() else 0.0,
                     "p90_si_change": float(d[ch].quantile(.9)) if ch.any() else 0.0,
                     "max": float(d.max())})
    return pd.DataFrame(rows), pu, pc


def flags(cc: ConstrainedClock, df, constrained: bool):
    """Signalement « a revoir par le medecin » : recompense indue > MATERIAL ans sur le score du
    systeme du marqueur. Recompense indue = ecart du systeme avec la valeur observee - ecart avec
    la valeur limite (< 0 : la valeur anormale est plus favorable que la limite)."""
    c = cc.clock
    panel = c.panel
    df = df.reset_index(drop=True)
    base = cc.predict(df, constrained)
    flag = np.zeros(len(df), bool)
    per = {}
    for v in cc.markers:
        sysn = panel.variables[v].system
        for mask, lim in abnormal_side(df, v):
            if not mask.any():
                continue
            d2 = df.copy()
            d2.loc[mask, v] = lim[mask]
            at_lim = cc.predict(d2, constrained)
            reward = base[f"gap_{sysn}"] - at_lim[f"gap_{sysn}"]
            f = mask & (reward < -MATERIAL)
            if f.any():
                per[v] = per.get(v, 0) + int(f.sum())
            flag |= f
    return {"n_signales": int(flag.sum()), "pct": float(100 * flag.mean()), "par_marqueur": per}


def predictions() -> dict:
    """Prediction pre-enregistree (developpement, apparent) : difference de C et changements."""
    OUT.mkdir(parents=True, exist_ok=True)
    study, dev, _, clock = _data()
    cc = ConstrainedClock(clock)
    ch, pu, pc = changes(cc, dev)
    res = {"n_dev": len(dev), "dC": {}}
    for s in SCORES:
        res["dC"][s] = (harrell_c(dev[DURATION], dev[EVENT], pc[f"risk_{s}"])
                        - harrell_c(dev[DURATION], dev[EVENT], pu[f"risk_{s}"]))
    res["changements"] = ch.to_dict(orient="records")
    (OUT / "prediction_developpement.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


def run(n_boot: int | None = None) -> dict:
    study, dev, val, clock = _data()
    vcfg = study["validation"]
    n_boot = n_boot or vcfg["bootstrap"]
    horizon = study["model"]["horizon_months"]
    cc = ConstrainedClock(clock)
    ch, pu, pc = changes(cc, val)
    d = val.copy()
    d["female"] = (d["sex"] == 2).astype(float)
    d["risk_ref"] = pu["risk_ref"].to_numpy()
    for s in SCORES:
        d[f"u_risk_{s}"], d[f"c_risk_{s}"] = pu[f"risk_{s}"].to_numpy(), pc[f"risk_{s}"].to_numpy()
        d[f"c_gap_{s}"] = pc[f"gap_{s}"].to_numpy()
    cols = [DURATION, EVENT, "risk_ref"] + [f"{p}_risk_{s}" for p in "uc" for s in SCORES]
    point = _paired(d)
    reps = bootstrap(d[cols], functools.partial(_paired), n_boot, vcfg["seed"])
    summ = summarize(point, reps).set_index("statistique")
    rows = []
    for s in SCORES:
        _, cal = calibration(d[DURATION], d[EVENT], d[f"c_risk_{s}"], horizon)
        hr = cox_hr(d, [f"c_gap_{s}"], ["age", "female"], DURATION, EVENT).iloc[0]
        k = f"dC_contraint_moins_libre_{s}"
        rows.append({"score": s, "C_contraint": summ.loc[f"C_contraint_{s}", "estimation"],
                     "C_ic95": (summ.loc[f"C_contraint_{s}", "ic95_bas"], summ.loc[f"C_contraint_{s}", "ic95_haut"]),
                     "C_libre": summ.loc[f"C_libre_{s}", "estimation"],
                     "gain_vs_age_sexe": summ.loc[f"gain_contraint_{s}", "estimation"],
                     "gain_ic95": (summ.loc[f"gain_contraint_{s}", "ic95_bas"], summ.loc[f"gain_contraint_{s}", "ic95_haut"]),
                     "dC_contraint_moins_libre": summ.loc[k, "estimation"],
                     "dC_ic95": (summ.loc[k, "ic95_bas"], summ.loc[k, "ic95_haut"]),
                     "HR_par_ET": hr["HR"], "obs_sur_predit": cal["ratio_observe_predit"],
                     "pente": cal["pente_calibration"], "pente_ic95": (cal["pente_ic95_bas"], cal["pente_ic95_haut"])})
    pd.DataFrame(rows).to_csv(OUT / "validation_contrainte.csv", index=False)
    ch.to_csv(OUT / "changements_validation.csv", index=False)
    fl = {"sans_contrainte": flags(cc, val, False), "avec_contrainte": flags(cc, val, True),
          "seuil_materiel_ans": MATERIAL, "n_validation": len(val)}
    (OUT / "signalements_validation.json").write_text(json.dumps(fl, indent=1), encoding="utf-8")
    return {"dossier": OUT, "adopte": bool(point["dC_contraint_moins_libre_global"] > -0.005)}
