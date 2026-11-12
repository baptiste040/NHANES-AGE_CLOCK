"""Programme « panel », Q1, analyse secondaire (declaree apres les resultats, a la demande de
l'auteur du projet) : population des effets, references (perte de poids de 5 %, statine), et nombre
de mesures a moyenner pour qu'un effet moyen atteigne le changement detectable.

Nombre de mesures, echelle log, sigma = sqrt(ln(1 + CV^2)) :
  sigma_6m^2 = sigma_obs^2 + sigma_LT^2   (sigma_LT : supplement a long terme, 0 si borne basse)
  seuil a atteindre : |ln(1 + effet)| >= 1,96 * sqrt(2) * sigma_effectif
  A. k prelevements rapproches a chaque bilan, moyennes : sigma_eff^2 = sigma_obs^2 / k + sigma_LT^2
     (la variation a long terme ne se moyenne pas avec des prelevements rapproches) ;
  B. m bilans espaces avant et m apres, moyennes (tendance) : sigma_eff^2 = sigma_6m^2 / m.
Hypotheses : erreurs independantes, effet stable, meme laboratoire.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .remesures import OUT

# Effets ajoutes (secondaire) : (intervention, id, effet en %, source, lu, population, note)
ADDED = [
    ("Statine (atorvastatine 10 mg/j ou équivalent)", "ldl", -40.0, "Law 2003, BMJ, doi:10.1136/bmj.326.7404.1423", "R",
     "164 essais contre placebo", "−1,8 mmol/L depuis 4,8 mmol/L"),
    ("Perte de poids de 7 kg (≈ 5-10 %), méta-analyse", "tg_fast", -4.0 * 7, "Hasan 2020, J Clin Endocrinol Metab, doi:10.1210/clinem/dgaa673", "R",
     "73 ECR, surpoids ou obésité (IMC moyen 36)", "−4,0 mg/dL par kg, interventions sur le mode de vie, 12 mois"),
    ("Perte de poids de 7 kg (≈ 5-10 %), méta-analyse", "ldl", -1.28 * 7, "Hasan 2020", "R", "73 ECR, surpoids ou obésité", "−1,28 mg/dL par kg"),
    ("Perte de poids de 7 kg (≈ 5-10 %), méta-analyse", "hdl", 0.46 * 7, "Hasan 2020", "R", "73 ECR, surpoids ou obésité", "+0,46 mg/dL par kg"),
    ("Perte de poids de 7 kg (≈ 5-10 %), méta-analyse", "alt", -0.83 * 7, "Koutoukidis 2021", "R", "stéatose (NAFLD)", "−0,83 U/L par kg"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "glu_fast", -4.1, "Magkos 2016, Cell Metab, doi:10.1016/j.cmet.2016.02.005", "TC",
     "obèses non diabétiques, n = 19 contre 14", "différence des variations des médianes, 95→91 contre 98→98 mg/dL"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "insulin", -13.6, "Magkos 2016", "TC", "obèses non diabétiques", "16,7→15,0 contre 20,6→21,3 mU/L"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "tg_fast", -37.9, "Magkos 2016", "TC", "obèses non diabétiques", "153→105 contre 107→114 mg/dL"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "hdl", 0.3, "Magkos 2016", "TC", "obèses non diabétiques", "41→40 contre 47→46 mg/dL ; non significatif"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "alt", -16.7, "Magkos 2016", "TC", "obèses non diabétiques", "18→15 contre 17→17 U/L"),
    ("Perte de poids de 5 % (essai unique, petite taille)", "crp", 5.1, "Magkos 2016", "TC", "obèses non diabétiques", "3,70→4,68 contre 3,59→4,36 mg/L ; non significatif"),
]
NOTES = {
    "hba1c": "Chez des non-diabétiques : rien trouvé avec ces requêtes (méta-analyses d'activité physique sur l'HbA1c "
             "hors diabète). Perte de poids de 5-10 % : seulement chez des diabétiques (Look AHEAD, Wing 2011, TC, "
             "rapports de cotes), pas d'effet moyen chez des non-diabétiques.",
}


def needed(eff_pct, cv_obs, cv6):
    so2 = np.log(1 + (cv_obs / 100) ** 2)
    s62 = np.log(1 + (cv6 / 100) ** 2)
    sx2 = max(0.0, s62 - so2)
    star2 = (abs(np.log(1 + eff_pct / 100)) / (1.96 * np.sqrt(2))) ** 2
    k = "impossible" if star2 <= sx2 else int(np.ceil(so2 / (star2 - sx2)))
    m = int(np.ceil(s62 / star2))
    return k, m


def run() -> pd.DataFrame:
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    iv = pd.read_csv(OUT / "Q1_interventions.csv")
    rows = []
    base = iv[["groupe", "intervention", "id", "marqueur", "effet_pct", "source", "lu", "population", "note"]].copy()
    base["origine"] = "principale"
    add = []
    v = pd.read_csv(OUT / "Q1_variabilite_remesures.csv")
    # mediane de conversion : jeu principal de Q1 (correction du 2026-11-12 ; avant : NHANES III)
    jp = cd[cd.groupe == "20-79 ans"].set_index("id")["jeu_principal"]
    vv = v[v.groupe == "30-55 ans"]
    v55 = pd.Series({i: g.set_index("jeu")["mediane_x1"].get(jp.get(i), g.mediane_x1.iloc[0]) for i, g in vv.groupby("id")})
    for grp in ["20-79 ans", "30-55 ans"]:
        for inter, mid, pct, src, lu, pop, note in ADDED:
            if "méta-analyse" in inter:          # effet absolu -> % de la mediane des 30-55 ans (jeu principal)
                pct = 100 * pct / v55[mid]
            c = cd[(cd.groupe == grp) & (cd.id == mid)].iloc[0]
            add.append({"groupe": grp, "intervention": inter, "id": mid, "marqueur": c.marqueur, "effet_pct": pct,
                        "source": src, "lu": lu, "population": pop, "note": note, "origine": "secondaire"})
    allp = pd.concat([base, pd.DataFrame(add)], ignore_index=True)
    for _, r in allp.iterrows():
        c = cd[(cd.groupe == r.groupe) & (cd.id == r.id)].iloc[0]
        seuil = c.cd6m_baisse if r.effet_pct < 0 else c.cd6m_hausse
        k, m = needed(r.effet_pct, c.cv_obs_principal, c.cv_6m)
        ratio = abs(r.effet_pct) / seuil
        rows.append({**r.to_dict(), "cd6m_pct": seuil, "statut_cd": c.statut, "ratio": ratio,
                     "conclusion": "détectable chez une personne" if ratio >= 1 else ("limite" if ratio >= 0.5 else "visible seulement en moyenne de groupe"),
                     "prelevements_par_bilan_k": k, "bilans_avant_et_apres_m": m,
                     "note_population": NOTES.get(r.id, "")})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "Q1_secondaire_moyenner.csv", index=False)
    return t
