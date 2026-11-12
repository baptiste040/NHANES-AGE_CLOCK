"""Piste « signatures » : parties A et B (protocole : DECISIONS.md, pre-enregistrement du 2026-11-12).

Calibration : paires de remesures NHANES 2001-2002. Evaluation : paires NHANES III.
Horizons : 2 semaines (paires reelles) et 6 mois (composante a long terme L ~ N(0, Omega) ajoutee, simulee).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr
from sklearn.covariance import ledoit_wolf_shrinkage

from ..config import ROOT
from ..panel import q4
from ..panel.remesures import pairs_2001, pairs_nh3
from . import vecteurs as V

OUT = ROOT / "reports" / "signatures"
Q = ROOT / "reports" / "panel"
SEED, NREP, NBOOT = 2026, 200, 1000
P = V.PANEL
IV = V.INTERVENTIONS


# ------------------------------------------------------------------ donnees
def load():
    out = {}
    for name, f in (("2001", pairs_2001), ("nh3", pairs_nh3)):
        e1, e2 = f()
        out[name] = (e1, e2)
    return out


def deltas(e1, e2, panel, crp_fill=False):
    a, b = e1[panel].copy(), e2[panel].copy()
    if crp_fill and "crp" in panel:
        pos = pd.concat([a.crp[a.crp > 0], b.crp[b.crp > 0]])
        lim = pos.min() / np.sqrt(2)
        a.loc[a.crp <= pos.min(), "crp"] = lim
        b.loc[b.crp <= pos.min(), "crp"] = lim
    ok = a.notna().all(1) & b.notna().all(1) & (a > 0).all(1) & (b > 0).all(1)
    D = np.log(b[ok].to_numpy(float)) - np.log(a[ok].to_numpy(float))
    return D, ok


def q1():
    t = pd.read_csv(Q / "Q1_changement_detectable.csv")
    return t[t.groupe == "20-79 ans"].drop_duplicates("id").set_index("id")


# Correction du 2026-11-12 (audit, point 4c) : l'analyse principale a 6 mois extrapole TOUS les marqueurs,
# avec la variabilite a long terme de toutes les etudes longues EFLM (notes A, B et C) ; l'ancienne version
# (notes A et B seulement : en pratique ALAT et ASAT) devient une borne optimiste.
NOISE = "ABC"
CV6 = {"ABC": "cv_6m_sens_noteC", "AB": "cv_6m"}
CDH = {"ABC": ("cd6m_hausse_sens_noteC", "cd6m_baisse_sens_noteC"), "AB": ("cd6m_hausse", "cd6m_baisse")}


def omega(panel, noise=None):
    c = q1()
    col = CV6[noise or NOISE]
    w = []
    for m in panel:
        cv_o, cv_6 = c.loc[m, "cv_obs_principal"] / 100, c.loc[m, col] / 100
        w.append(max(0.0, 2 * (np.log(1 + cv_6 ** 2) - np.log(1 + cv_o ** 2))))
    return np.array(w)


def cd_bounds(panel, noise=None):
    """Seuils « naifs » par marqueur (changement detectable de Q1 a 6 mois, meme hypothese de bruit)."""
    c = q1()
    h, b = CDH[noise or NOISE]
    hi = np.array([np.log(1 + c.loc[m, h] / 100) for m in panel])
    lo = np.array([np.log(1 - c.loc[m, b] / 100) for m in panel])
    return hi, lo


# ------------------------------------------------------------------ covariance
def nearest_pd(C):
    w, U = np.linalg.eigh((C + C.T) / 2)
    w = np.maximum(w, 1e-6 * np.trace(C) / len(C))
    return (U * w) @ U.T


def robust_cov(D, robust=True):
    if robust:
        med = np.median(D, 0)
        s = 1.4826 * np.median(np.abs(D - med), 0)
        # repli si l'ecart absolu median est nul (valeurs arrondies, tirages bootstrap) : IQR, puis ecart type
        iqr = (np.quantile(D, 0.75, 0) - np.quantile(D, 0.25, 0)) / 1.349
        s = np.where(s > 0, s, np.where(iqr > 0, iqr, D.std(0, ddof=1)))
        rho = spearmanr(D).correlation
        R = 2 * np.sin(np.pi * rho / 6)
        np.fill_diagonal(R, 1.0)
        Z = (D - med) / s
    else:
        s = D.std(0, ddof=1)
        R = np.corrcoef(D, rowvar=False)
        Z = (D - D.mean(0)) / s
    R = nearest_pd(R)
    R = R / np.sqrt(np.outer(np.diag(R), np.diag(R)))
    delta = float(ledoit_wolf_shrinkage(Z))
    Rs = (1 - delta) * R + delta * np.eye(len(R))
    return np.outer(s, s) * Rs, delta, R


def sample_L(n, om, R=None, rng=None, nrep=NREP):
    """Composante a long terme : diagonale (R=None) ou correlee (R = correlation du bruit)."""
    sd = np.sqrt(om)
    if R is None:
        return rng.standard_normal((nrep, n, len(om))) * sd
    Lc = np.linalg.cholesky(nearest_pd(np.outer(sd, sd) * R + 1e-12 * np.eye(len(om))))
    return rng.standard_normal((nrep, n, len(om))) @ Lc.T


# ------------------------------------------------------------------ detecteurs
class Det:
    def __init__(self, d, S):
        self.d, self.S = d, S
        Si = np.linalg.inv(S)
        self.w = Si @ d / np.sqrt(d @ Si @ d)
        self.snr = float(np.sqrt(d @ Si @ d))
        s = np.abs(d) / np.sqrt(np.diag(S))
        self.j = int(np.argmax(s))
        self.sgn = np.sign(d[self.j]) if d[self.j] != 0 else 1.0
        self.Si = Si

    def sig(self, D):
        return D @ self.w

    def best(self, D):
        return self.sgn * D[..., self.j] / np.sqrt(self.S[self.j, self.j])

    def maha(self, D):
        return np.einsum("...i,ij,...j->...", D, self.Si, D)


def thresholds(det, Dcal):
    return {k: float(np.quantile(getattr(det, k)(Dcal).ravel(), 0.95)) for k in ("sig", "best", "maha")}


def boot_ci(per_person, rng, n=NBOOT):
    per_person = np.asarray(per_person, float)
    idx = rng.integers(0, len(per_person), (n, len(per_person)))
    m = per_person[idx].mean(1)
    return [float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))]


def k_draws(scen, shape, rng):
    if scen == "principal":
        return rng.normal(1.0, 0.5, shape)
    if scen == "non_repondeurs_30":
        k = rng.normal(1.0, 0.3, shape)
        return np.where(rng.random(shape) < 0.3, 0.0, k)
    return np.ones(shape)


# ------------------------------------------------------------------ partie A
def partie_a(data, rng):
    c = q1()
    om_all = {}
    rows, persons = [], []
    for jeu, (e1, e2) in data.items():
        panels = [("18", P)] + ([("19 avec CRP", V.PANEL_CRP)] if jeu == "2001" else [])
        for plab, panel in panels:
            hi, lo = cd_bounds(panel)
            om = omega(panel)
            D, ok = deltas(e1, e2, panel, crp_fill=("crp" in panel))
            for hz in ("2 semaines", "6 mois"):
                if hz == "2 semaines":
                    X = D[None]
                else:
                    X = D[None] + sample_L(len(D), om, rng=rng)
                exc = (X > hi) | (X < lo)                      # (rep, n, p)
                cnt = exc.sum(-1)                               # (rep, n)
                p_j = exc.mean((0, 1))
                # attendu sous independance (Poisson-binomial)
                dist = np.array([1.0])
                for p in p_j:
                    dist = np.convolve(dist, [1 - p, p])
                ge1, ge3 = (cnt >= 1).mean(0), (cnt >= 3).mean(0)
                rows.append({"jeu": jeu, "panel": plab, "horizon": hz, "n_paires_completes": len(D),
                             "nb_moyen_marqueurs_au_dela": float(cnt.mean()),
                             "part_au_moins_1": float(ge1.mean()), "ic95_au_moins_1": boot_ci(ge1, rng),
                             "part_au_moins_3": float(ge3.mean()), "ic95_au_moins_3": boot_ci(ge3, rng),
                             "attendu_independance_au_moins_1": float(1 - dist[0]),
                             "attendu_independance_au_moins_3": float(1 - dist[:3].sum()),
                             **{f"taux_{m}": float(p) for m, p in zip(panel, p_j)}})
            # transitions anormal <-> normal (seuils D1 S et R applicables)
            if plab == "18":
                a = e1[ok].reset_index(drop=True)
                b = e2[ok].reset_index(drop=True)
                rules = [r for r in q4.thresholds() if r[0] in panel]
                for hz in ("2 semaines", "6 mois"):
                    nrep = 1 if hz == "2 semaines" else 50
                    Ls = np.zeros((1, len(a), len(panel))) if nrep == 1 else sample_L(len(a), om, rng=rng, nrep=nrep)
                    good = np.zeros((nrep, len(a)), bool)
                    bad = np.zeros((nrep, len(a)), bool)
                    for mid, typ, var, f in rules:
                        if typ == "R" and var not in ("principal", "ADA", "OMS"):
                            continue
                        lo_, hi_ = f(a)
                        j = panel.index(mid)
                        x1 = a[mid].to_numpy(float)
                        l1, h1 = q4._abn(x1, lo_, hi_, typ)
                        for r_ in range(nrep):
                            x2 = b[mid].to_numpy(float) * np.exp(Ls[r_, :, j])
                            l2, h2 = q4._abn(x2, lo_, hi_, typ)
                            good[r_] |= (l1 | h1) & ~(l2 | h2)
                            bad[r_] |= ~(l1 | h1) & (l2 | h2)
                    persons.append({"jeu": jeu, "horizon": hz, "n": len(a),
                                    "part_fausse_bonne_nouvelle": float(good.mean()), "ic95_fbn": boot_ci(good.mean(0), rng),
                                    "part_fausse_alerte_seuil": float(bad.mean()), "ic95_fas": boot_ci(bad.mean(0), rng),
                                    "part_l_un_ou_l_autre": float((good | bad).mean())})
    return pd.DataFrame(rows), pd.DataFrame(persons)


# ------------------------------------------------------------------ pieges
def pitfalls(panel):
    def vec(d):
        return np.array([np.log1p(d.get(m, 0.0) / 100) for m in panel])
    a = pd.read_csv(Q / "Q5_passage.csv")
    a = a[(a.evenement.astype(str) == "5") & a.chiffre & ~a.derive.astype(bool)].set_index("id").decalage_principal.to_dict()
    bio = {m: a[m] for m in panel if m in a}
    b = pd.read_csv(Q / "Q5_empirique.csv")
    b = b[b.evenement.astype(str) == "17"].set_index("id").decalage_empirique.to_dict()
    cbc = {m: b[m] for m in panel if m in b}
    s3 = pd.read_csv(Q / "Q3_decalages.csv")
    s3 = s3[(s3.groupe == "pilule") & (s3.sexe == "ensemble")].set_index("id")
    pil = {m: float(s3.loc[m, "decalage"]) for m in panel if m in s3.index and np.isfinite(s3.loc[m, "decalage"])
           and s3.loc[m, "echelle"] == "log"}
    q2 = pd.read_csv(Q / "Q2_synthese.csv").set_index("id")
    fa = {m: float(q2.loc[m, "jeune"]) for m in panel if m in q2.index}
    q2b = pd.read_csv(Q / "Q2_B_nhanes_1999_2018.csv").set_index("id")
    fb = {m: float(q2b.loc[m, "jeune_B1"]) for m in panel if m in q2b.index}
    out = {"labo_biochimie": vec(bio), "labo_numeration": vec(cbc), "pilule": vec(pil), "non_a_jeun_meme_personne": vec(fa),
           "non_a_jeun_entre_personnes": vec(fb)}
    out["labo_complet"] = out["labo_biochimie"] + out["labo_numeration"]
    return out, {"labo_biochimie": bio, "labo_numeration": cbc, "pilule": pil, "non_a_jeun_meme_personne": fa,
                 "non_a_jeun_entre_personnes": fb}


def constrained(d, S, Pm):
    Si = np.linalg.inv(S)
    return d - Pm @ np.linalg.solve(Pm.T @ Si @ Pm, Pm.T @ Si @ d)


# ------------------------------------------------------------------ partie B
def run_detection(Dcal, Deval, S2, S6, om, vecs, rng, Rcorr=None, label="principal"):
    """Seuils sur 2001-2002, evaluation sur NHANES III, deux horizons, trois scenarios d'heterogeneite."""
    rows = []
    L_cal = sample_L(len(Dcal), om, R=Rcorr, rng=rng)
    L_ev = sample_L(len(Deval), om, R=Rcorr, rng=rng)
    dets = {}
    for hz, S, Xc, Xe in (("2 semaines", S2, Dcal[None], Deval[None]), ("6 mois", S6, Dcal[None] + L_cal, Deval[None] + L_ev)):
        for iv, d in vecs.items():
            det = Det(d, S)
            thr = thresholds(det, Xc)
            dets[(hz, iv)] = (det, thr)
            fa = {k: (getattr(det, k)(Xe) > thr[k]).mean(0) for k in ("sig", "best", "maha")}
            row = {"variante": label, "horizon": hz, "intervention": iv, "meilleur_marqueur": P[det.j] if len(d) == len(P) else det.j,
                   "snr": det.snr, **{f"seuil_{k}": v for k, v in thr.items()},
                   **{f"fausses_alertes_{k}": float(v.mean()) for k, v in fa.items()},
                   **{f"ic95_fa_{k}": boot_ci(v, rng) for k, v in fa.items()}}
            reps = Xe.shape[0]
            for scen in ("principal", "non_repondeurs_30", "k_1"):
                k = k_draws(scen, (NREP if reps == 1 else reps, len(Deval), 1), rng)
                base = np.broadcast_to(Xe, (k.shape[0],) + Xe.shape[1:])
                X = base + k * d
                det_s = (det.sig(X) > thr["sig"]).mean(0)
                det_b = (det.best(X) > thr["best"]).mean(0)
                det_m = (det.maha(X) > thr["maha"]).mean(0)
                row |= {f"sens_sig_{scen}": float(det_s.mean()), f"sens_best_{scen}": float(det_b.mean()),
                        f"sens_maha_{scen}": float(det_m.mean())}
                if scen == "principal":
                    row |= {"ic95_sens_sig": boot_ci(det_s, rng), "ic95_sens_best": boot_ci(det_b, rng),
                            "diff_sig_moins_best": float((det_s - det_b).mean()), "ic95_diff": boot_ci(det_s - det_b, rng)}
            # effet necessaire (k fixe)
            for lab_, f_ in (("sig", det.sig), ("best", det.best)):
                for target in (0.5, 0.8):
                    need = np.nan
                    for c in np.arange(0.25, 15.01, 0.25):
                        if (f_(Xe + c * d) > thr[lab_]).mean() >= target:
                            need = float(c)
                            break
                    row[f"multiple_effet_{lab_}_{int(target * 100)}"] = need
            rows.append(row)
    return pd.DataFrame(rows), dets, (L_cal, L_ev)


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    data = load()
    # ---------------- partie A
    A, Apers = partie_a(data, rng)
    A.to_csv(OUT / "signatures_partie_a.csv", index=False)
    Apers.to_csv(OUT / "signatures_partie_a_transitions.csv", index=False)
    # ---------------- covariance
    Dcal, _ = deltas(*data["2001"], P)
    Dev, _ = deltas(*data["nh3"], P)
    S2, delta, Rrob = robust_cov(Dcal)
    om = omega(P)
    S6 = S2 + np.diag(om)
    pd.DataFrame(S2, index=P, columns=P).to_csv(OUT / "signatures_covariance_2semaines.csv")
    pd.DataFrame(S6, index=P, columns=P).to_csv(OUT / "signatures_covariance_6mois.csv")
    corr = S2 / np.sqrt(np.outer(np.diag(S2), np.diag(S2)))
    pd.DataFrame(corr, index=P, columns=P).to_csv(OUT / "signatures_correlation_bruit.csv")
    vecs = {iv: V.vector(iv) for iv in IV}
    pd.DataFrame(vecs, index=P).to_csv(OUT / "signatures_vecteurs_log.csv")
    V.table().to_csv(OUT / "signatures_vecteurs_sources.csv", index=False)
    meta = {"n_calibration": len(Dcal), "n_evaluation": len(Dev), "retrecissement_ledoit_wolf": delta, "omega": dict(zip(P, om.tolist()))}
    # ---------------- detection principale
    B, dets, (L_cal, L_ev) = run_detection(Dcal, Dev, S2, S6, om, vecs, rng)
    # usage global : au moins une des 5 signatures
    glob = []
    for hz, Xe in (("2 semaines", Dev[None]), ("6 mois", Dev[None] + L_ev)):
        any_ = np.zeros(Xe.shape[:2], bool)
        for iv in IV:
            det, thr = dets[(hz, iv)]
            any_ |= det.sig(Xe) > thr["sig"]
        glob.append({"horizon": hz, "fausses_alertes_5_signatures": float(any_.mean()), "ic95": boot_ci(any_.mean(0), rng)})
    # contributions (B9)
    contrib = []
    for (hz, iv), (det, _) in dets.items():
        d = det.d
        Sid = det.Si @ d
        tot = d @ Sid
        for j, m in enumerate(P):
            contrib.append({"horizon": hz, "intervention": iv, "id": m, "effet_log": d[j], "poids": det.w[j],
                            "poids_standardise": det.w[j] * np.sqrt(det.S[j, j]), "part_signal": d[j] * Sid[j] / tot if tot else np.nan})
    # recouvrement et declenchements croises (B6), 6 mois
    pits, pit_src = pitfalls(P)
    allv = {**vecs, **pits}
    Si6 = np.linalg.inv(S6)
    cos = pd.DataFrame({a: {b: float(allv[a] @ Si6 @ allv[b] / np.sqrt((allv[a] @ Si6 @ allv[a]) * (allv[b] @ Si6 @ allv[b])))
                            if np.any(allv[a]) and np.any(allv[b]) else np.nan for b in allv} for a in allv})
    cross = []
    Xe6 = Dev[None] + L_ev
    for i in IV:
        k = k_draws("principal", (L_ev.shape[0], len(Dev), 1), rng)
        X = Xe6 + k * vecs[i]
        for j in IV:
            det, thr = dets[("6 mois", j)]
            cross.append({"intervention_appliquee": i, "signature_testee": j, "taux_declenchement": float((det.sig(X) > thr["sig"]).mean())})
    # pieges (B7)
    pitrows = []
    for hz, Xe in (("2 semaines", Dev[None]), ("6 mois", Dev[None] + L_ev)):
        for pn, pv in pits.items():
            for sgn in (1, -1):
                X = Xe + sgn * pv
                for iv in IV:
                    det, thr = dets[(hz, iv)]
                    pitrows.append({"horizon": hz, "piege": pn, "sens": "+" if sgn > 0 else "−", "intervention": iv,
                                    "declenchement_signature": float((det.sig(X) > thr["sig"]).mean()),
                                    "declenchement_meilleur_seul": float((det.best(X) > thr["best"]).mean())})
    pitdf = pd.DataFrame(pitrows)
    # correction : signature contrainte aux pieges qui la declenchent au-dela de 10 %
    corr_rows = []
    for hz, S, Xc, Xe in (("2 semaines", S2, Dcal[None], Dev[None]), ("6 mois", S6, Dcal[None] + L_cal, Dev[None] + L_ev)):
        for iv in IV:
            trig = pitdf[(pitdf.horizon == hz) & (pitdf.intervention == iv) & (pitdf.declenchement_signature > 0.10)
                         & ~pitdf.piege.isin(["labo_complet", "non_a_jeun_entre_personnes"])].piege.unique().tolist()
            if not trig:
                continue
            Pm = np.column_stack([pits[t] for t in trig])
            dc = constrained(vecs[iv], S, Pm)
            det = Det(dc, S)
            thr = thresholds(det, Xc)
            k = k_draws("principal", (NREP if Xe.shape[0] == 1 else Xe.shape[0], len(Dev), 1), rng)
            X = np.broadcast_to(Xe, (k.shape[0],) + Xe.shape[1:]) + k * vecs[iv]
            r = {"horizon": hz, "intervention": iv, "pieges_neutralises": ", ".join(trig),
                 "sens_contrainte": float((det.sig(X) > thr["sig"]).mean()),
                 "sens_originale": float(B[(B.horizon == hz) & (B.intervention == iv)].sens_sig_principal.iloc[0]),
                 "fausses_alertes_contrainte": float((det.sig(Xe) > thr["sig"]).mean())}
            for pn in pits:
                for sgn in (1, -1):
                    r[f"declenchement_{pn}_{'+' if sgn > 0 else '-'}"] = float((det.sig(Xe + sgn * pits[pn]) > thr["sig"]).mean())
            corr_rows.append(r)
    # sensibilites hepatiques (B8)
    liv = []
    for fac in (0.5, 0.0):
        vv = {iv: V.vector(iv, liver_factor=fac) for iv in IV}
        b8, _, _ = run_detection(Dcal, Dev, S2, S6, om, vv, rng, label=f"enzymes x{fac}")
        liv.append(b8)
    # alcool illustratif
    va = {"reduction_alcool": V.vector("reduction_alcool", alcool_illustratif=True)}
    b_alc, _, _ = run_detection(Dcal, Dev, S2, S6, om, va, rng, label="alcool GGT -15 % (illustratif)")
    # hypothese de bruit a 6 mois : notes A/B seulement (ancienne analyse principale, borne optimiste)
    om_ab = omega(P, "AB")
    b_ab, _, _ = run_detection(Dcal, Dev, S2, S2 + np.diag(om_ab), om_ab, vecs, rng, label="bruit 6 mois A/B (borne optimiste)")
    meta["omega_AB"] = dict(zip(P, om_ab.tolist()))
    meta["marqueurs_extrapoles"] = {"ABC": [m for m, w in zip(P, om) if w > 0], "AB": [m for m, w in zip(P, om_ab) if w > 0]}
    # covariance non robuste, L correlee
    S2n, _, _ = robust_cov(Dcal, robust=False)
    b_nr, _, _ = run_detection(Dcal, Dev, S2n, S2n + np.diag(om), om, vecs, rng, label="covariance non robuste")
    S6c = S2 + np.outer(np.sqrt(om), np.sqrt(om)) * Rrob
    b_lc, _, _ = run_detection(Dcal, Dev, S2, nearest_pd(S6c), om, vecs, rng, Rcorr=Rrob, label="long terme corrélé")
    # CRP : validation croisee a deux plis dans 2001-2002
    Dc, _ = deltas(*data["2001"], V.PANEL_CRP, crp_fill=True)
    omc = omega(V.PANEL_CRP)
    perm = rng.permutation(len(Dc))
    halves = [perm[: len(Dc) // 2], perm[len(Dc) // 2:]]
    crp_rows = []
    for a_, b_ in ((0, 1), (1, 0)):
        Sa, _, _ = robust_cov(Dc[halves[a_]])
        vv = {iv: V.vector(iv, panel=V.PANEL_CRP) for iv in IV}
        bc, _, _ = run_detection(Dc[halves[a_]], Dc[halves[b_]], Sa, Sa + np.diag(omc), omc, vv, rng, label=f"avec CRP, pli {a_ + 1}")
        crp_rows.append(bc)
    crp = pd.concat(crp_rows)
    sens_all = pd.concat([B] + liv + [b_alc, b_ab, b_nr, b_lc, crp])
    # plusieurs bilans (B10), gaussien
    multi = []
    for iv in IV:
        d = vecs[iv]
        Sm = S6 / 2

        def p_det(C, single=False):
            if single:
                s = np.max(np.abs(d) / np.sqrt(np.diag(C)))
            else:
                s = np.sqrt(d @ np.linalg.solve(C, d))
            return float(norm.cdf((s - 1.645) / np.sqrt(1 + 0.25 * s ** 2)))
        r = {"intervention": iv, "un_bilan_6_mois_sig": p_det(S6), "un_bilan_6_mois_best": p_det(S6, True),
             "bilans_6_et_12_mois_sig": p_det(0.75 * S6), "bilans_6_et_12_mois_best": p_det(0.75 * S6, True)}
        for lab_, single in (("sig", False), ("best", True)):
            r[f"m_symetrique_80_{lab_}"] = next((m for m in range(1, 21) if p_det(S6 / m, single) >= 0.8), None)
            r[f"n_apres_un_depart_80_{lab_}"] = next((n for n in range(1, 21) if p_det(Sm * (1 + 1 / n), single) >= 0.8), None)
            r[f"plafond_un_depart_{lab_}"] = p_det(Sm, single)
        multi.append(r)
    # ---------------- ecriture
    sens_all.to_csv(OUT / "signatures_detection.csv", index=False)
    pd.DataFrame(glob).to_csv(OUT / "signatures_usage_global.csv", index=False)
    pd.DataFrame(contrib).to_csv(OUT / "signatures_contributions.csv", index=False)
    cos.to_csv(OUT / "signatures_recouvrement_cosinus.csv")
    pd.DataFrame(cross).to_csv(OUT / "signatures_declenchements_croises.csv", index=False)
    pitdf.to_csv(OUT / "signatures_pieges.csv", index=False)
    pd.DataFrame(corr_rows).to_csv(OUT / "signatures_correction.csv", index=False)
    pd.DataFrame(multi).to_csv(OUT / "signatures_plusieurs_bilans.csv", index=False)
    meta["pieges_sources"] = {k: {m: float(v) for m, v in d.items()} for k, d in pit_src.items()}
    (OUT / "signatures_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    return sens_all


if __name__ == "__main__":
    run()
