"""Programme « panel », Q1 partie A (suite) : changement detectable a 6 mois et predictions.

CV_6m^2 = CV_obs^2 + max(0, CV_I,LT^2 - CV_I,CT^2) (echelle log). CV_obs : NHANES III (principal),
2001-2002 et version robuste (sensibilites). CV_I,LT : etudes EFLM >= 6 mois, adultes sains,
note BIVAC A ou B (principal) ; note C incluse en sensibilite non pre-enregistree.
Les valeurs EFLM sont lues dans private/panel/ (hors depot, licence EFLM).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from ..config import ROOT
from .remesures import OUT

PRIV = ROOT / "private" / "panel"


def cd_from_cv(cv):
    """Changement detectable (2 mesures, 95 %) en % : (hausse, baisse)."""
    s = np.sqrt(np.log(1 + (np.asarray(cv, float) / 100) ** 2))
    q = 1.96 * np.sqrt(2) * s
    return 100 * (np.exp(q) - 1), 100 * (1 - np.exp(-q))


def combine(cv_obs, ct, lt):
    extra = np.where(np.isfinite(lt) & np.isfinite(ct), np.maximum(0, lt ** 2 - ct ** 2), 0.0)
    return np.sqrt(cv_obs ** 2 + extra)


def run() -> dict:
    v = pd.read_csv(OUT / "Q1_variabilite_remesures.csv")
    lt = pd.read_csv(PRIV / "eflm_long_terme.csv").set_index("id")
    pred = pd.read_csv(PRIV / "Q1_predictions_eflm.csv")
    rows = []
    for grp in ["20-79 ans", "30-55 ans"]:
        g = v[v.groupe == grp]
        for pid in g.id.unique():
            a = g[g.id == pid].set_index("jeu")
            r = {"groupe": grp, "id": pid, "marqueur": a.marqueur.iloc[0], "echelle": a.echelle.iloc[0]}
            for jeu in ["nhanes3", "2001_2002"]:
                if jeu in a.index:
                    x = a.loc[jeu]
                    for k in ["n", "cv_obs", "cv_robuste", "cd_emp_hausse", "cd_emp_baisse", "cd_robuste_hausse", "part_au_minimum",
                              "sd_intra", "cd_emp_unites", "decalage_moyen"]:
                        if k in x and pd.notna(x[k]):
                            r[f"{k}_{jeu}"] = x[k]
            # jeu principal : NHANES III sauf si absent, ou CRP censuree (> 20 % au minimum)
            key = "cv_obs" if r["echelle"] == "log" else "sd_intra"
            main = "nhanes3"
            if f"{key}_nhanes3" not in r or r.get("part_au_minimum_nhanes3", 0) > 0.20:
                main = "2001_2002" if (f"{key}_2001_2002" in r and r.get("part_au_minimum_2001_2002", 0) <= 0.20) else None
            if main and f"cv_obs_{main}" not in r and f"sd_intra_{main}" in r:
                r["echelle"] = "add"                         # echelle additive dans le jeu retenu
            r["jeu_principal"] = main
            ct = lt.loc[pid, "cv_i_ct_meta"] if pid in lt.index else np.nan
            lab = lt.loc[pid, "cv_i_lt_AB"] if pid in lt.index else np.nan
            lc = lt.loc[pid, "cv_i_lt_ABC"] if pid in lt.index else np.nan
            r |= {"cv_i_ct_eflm": ct, "cv_i_lt_AB": lab, "cv_i_lt_ABC": lc}
            if main and r["echelle"] == "log":
                cvo = r[f"cv_obs_{main}"]
                cv6 = float(combine(np.array(cvo), np.array(ct), np.array(lab)))
                cv6c = float(combine(np.array(cvo), np.array(ct), np.array(lc)))
                r |= {"cv_obs_principal": cvo, "cv_6m": cv6, "cv_6m_sens_noteC": cv6c,
                      "statut": "extrapolé à 6 mois" if np.isfinite(lab) else "borne basse (2 semaines)"}
                r["cd6m_hausse"], r["cd6m_baisse"] = [float(x) for x in cd_from_cv(cv6)]
                r["cd6m_hausse_sens_noteC"], r["cd6m_baisse_sens_noteC"] = [float(x) for x in cd_from_cv(cv6c)]
                rob = r.get(f"cv_robuste_{main}")
                if rob is not None:
                    r["cd6m_hausse_robuste"] = float(cd_from_cv(combine(np.array(rob), np.array(ct), np.array(lab)))[0])
                alt = "2001_2002" if main == "nhanes3" else "nhanes3"
                if f"cv_obs_{alt}" in r:
                    r["cd6m_hausse_autre_jeu"] = float(cd_from_cv(combine(np.array(r[f"cv_obs_{alt}"]), np.array(ct), np.array(lab)))[0])
            elif main:
                sd = r[f"sd_intra_{main}"]
                r |= {"sd_intra_principal": sd, "cd6m_unites": float(1.96 * np.sqrt(2) * sd),
                      "cd6m_unites_empirique": r.get(f"cd_emp_unites_{main}"),
                      "statut": "borne basse (2 semaines), échelle additive"}
            else:
                r["statut"] = "non interprétable (valeurs censurées > 20 %)"
            rows.append(r)
    t = pd.DataFrame(rows)
    # marqueurs sans remesure : EFLM seul (CV_A = 0,5 CV_I faute de fiche lue)
    have = set(t.id)
    eflm_only = []
    for pid in lt.index:
        if pid in have:
            continue
        ct, lab = lt.loc[pid, "cv_i_ct_meta"], lt.loc[pid, "cv_i_lt_AB"]
        cvi = lab if np.isfinite(lab) else ct
        cv = float(np.sqrt(cvi ** 2 + (0.5 * cvi) ** 2))
        h, b = cd_from_cv(cv)
        eflm_only.append({"groupe": "20-79 ans", "id": pid, "marqueur": lt.loc[pid, "mesurande_eflm"], "echelle": "log",
                          "cv_i_ct_eflm": ct, "cv_i_lt_AB": lab, "cv_i_lt_ABC": lt.loc[pid, "cv_i_lt_ABC"], "cv_6m": cv,
                          "cd6m_hausse": float(h), "cd6m_baisse": float(b), "statut": "EFLM seul (CV_A = 0,5 × CV_I)"})
    t = pd.concat([t, pd.DataFrame(eflm_only)], ignore_index=True)
    # version complete (avec les CV_I EFLM bruts) hors depot ; version publique sans ces colonnes
    t.to_csv(PRIV / "Q1_changement_detectable_complet.csv", index=False)
    pub = t.drop(columns=["cv_i_ct_eflm", "cv_i_lt_AB", "cv_i_lt_ABC"])
    pub.loc[pub.statut.astype(str).str.startswith("EFLM"), "cv_6m"] = np.nan
    pub.to_csv(OUT / "Q1_changement_detectable.csv", index=False)

    # ---------------------------------------------------------------- predictions
    a = t[(t.groupe == "20-79 ans") & (t.echelle == "log")]
    name_map = {  # id -> nom du fichier de predictions
        "wbc": "Leucocytes", "neut_pct": "Neutrophiles", "lymph_pct": "Lymphocytes", "mono_pct": "Monocytes",
        "eos_pct": "Éosinophiles", "baso_pct": "Basophiles", "rbc": "Hématies", "hb": "Hémoglobine", "hct": "Hématocrite",
        "mcv": "VGM", "mch": "TCMH", "mchc": "CCMH", "rdw": "RDW", "plt": "Plaquettes", "mpv": "VPM", "glu_fast": "Glycémie à jeun",
        "insulin": "Insuline", "hba1c": "HbA1c", "tc": "Cholestérol total", "ldl": "LDL", "hdl": "HDL", "tg_fast": "Triglycérides",
        "alt": "ALAT", "ast": "ASAT", "ggt": "GGT", "alp": "PAL", "bili": "Bilirubine totale", "albumin": "Albumine",
        "protein": "Protéines totales", "creat": "Créatinine", "urea": "Urée", "na": "Sodium", "k": "Potassium", "cl": "Chlorure",
        "hco3": "Bicarbonates", "crp": "hs-CRP", "b12": "Vitamine B12", "vitd": "Vitamine D (25-OH)", "ca": "Calcium",
        "lh": "LH", "fsh": "FSH", "psa_total": "PSA total", "psa_free": "PSA libre", "apoa1": "ApoA1", "apob": "ApoB", "lpa": "Lp(a)",
        "iron": "Fer sérique", "ferritin": "Ferritine", "hcy": "Homocystéine", "urate": "Acide urique", "phos": "Phosphate",
        "selenium": "Sélénium", "tibc": "Transferrine (CTF)"}
    p = pred.set_index("marqueur")
    comp = []
    for _, r in a.iterrows():
        nm = name_map.get(r.id)
        if nm in p.index and pd.notna(r.get("cv_obs_nhanes3")) and r.get("part_au_minimum_nhanes3", 0) <= 0.20:
            comp.append({"id": r.id, "cv_obs": r.cv_obs_nhanes3, "cv_pred": p.loc[nm, "cv_pred_2sem"]})
    comp = pd.DataFrame(comp)
    p1 = float((comp.cv_obs > comp.cv_pred).mean()) if len(comp) else np.nan
    tails = a[a.cd_emp_hausse_nhanes3.notna() & a.cd_robuste_hausse_nhanes3.notna()]
    p2 = float((tails.cd_emp_hausse_nhanes3 > 1.10 * tails.cd_robuste_hausse_nhanes3).mean())
    both = a[a.cv_obs_nhanes3.notna() & a.cv_obs_2001_2002.notna()]
    ratio = np.maximum(both.cv_obs_nhanes3, both.cv_obs_2001_2002) / np.minimum(both.cv_obs_nhanes3, both.cv_obs_2001_2002)
    p3 = float((ratio < 1.5).mean())
    res = {"prediction_1_part_cv_obs_sup_attendu": p1, "n_1": len(comp), "verifiee_1": bool(p1 >= 2 / 3),
           "prediction_2_part_queues_epaisses": p2, "n_2": len(tails), "verifiee_2": bool(p2 >= 0.5),
           "prediction_3_part_replication": p3, "n_3": len(both), "verifiee_3": bool(p3 >= 2 / 3),
           "comparaison_1": comp.round(2).to_dict(orient="records")}
    (PRIV / "Q1_predictions_verifiees_complet.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    pub_res = {k: v for k, v in res.items() if k != "comparaison_1"}
    (OUT / "Q1_predictions_verifiees.json").write_text(json.dumps(pub_res, indent=1, default=float), encoding="utf-8")
    return res
