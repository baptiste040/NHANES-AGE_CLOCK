"""Programme « panel », Q1 partie B : effets moyens d'interventions (meta-analyses lues) rapportes
au changement detectable a 6 mois. Protocole : DECISIONS.md.

Effets : difference moyenne intervention - controle, en unites de la meta-analyse, convertie en %
de la mediane NHANES des 30-55 ans au premier examen (memes unites), faute de moyenne de depart
dans les resumes lus. « R » = resume seul ; « TC » = texte complet.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .remesures import OUT

# (intervention, id marqueur, effet absolu, unite, conversion vers l'unite NHANES, source, lu, population, note)
EFFECTS = [
    ("Activité physique (toutes formes)", "tc", -5.90, "mg/dL", 1, "Smart 2025, Sports Med, doi:10.1007/s40279-024-02115-z", "R", "148 ECR, adultes", ""),
    ("Activité physique (toutes formes)", "hdl", 2.11, "mg/dL", 1, "Smart 2025", "R", "148 ECR, adultes", ""),
    ("Activité physique (toutes formes)", "ldl", -7.22, "mg/dL", 1, "Smart 2025", "R", "148 ECR, adultes", ""),
    ("Activité physique (toutes formes)", "tg_fast", -8.01, "mg/dL", 1, "Smart 2025", "R", "148 ECR, adultes", ""),
    ("Activité physique structurée", "hba1c", -0.67, "%", 1, "Umpierre 2011, JAMA, doi:10.1001/jama.2011.576", "R", "diabète de type 2", "population diabétique : effet probablement plus faible chez des non-diabétiques"),
    ("Activité physique aérobie", "glu_fast", -0.15, "mmol/L", 18.0, "Wewege 2018, Atherosclerosis, doi:10.1016/j.atherosclerosis.2018.05.002", "R", "syndrome métabolique", ""),
    ("Activité physique (toutes formes)", "insulin", -1.88, "µU/mL", 1, "Smart 2018, Br J Sports Med, doi:10.1136/bjsports-2016-096197", "R", "surpoids ou stéatose", "unité notée « UL » dans le résumé"),
    ("Alimentation méditerranéenne", "glu_fast", -2.98, "mg/dL", 1, "Papadaki 2020, Nutrients, doi:10.3390/nu12113342", "TC", "adultes, 57 essais contrôlés", ""),
    ("Alimentation méditerranéenne", "insulin", -0.94, "µU/mL", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "homa_ir", -0.42, "unités", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "hba1c", -0.15, "%", 1, "Papadaki 2020", "TC", "adultes", "non significatif"),
    ("Alimentation méditerranéenne", "tc", -5.70, "mg/dL", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "ldl", -8.24, "mg/dL", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "hdl", 1.30, "mg/dL", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "tg_fast", -12.30, "mg/dL", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "alt", -5.66, "U/L", 1, "Papadaki 2020", "TC", "adultes", ""),
    ("Alimentation méditerranéenne", "ggt", -2.51, "U/L", 1, "Papadaki 2020", "TC", "adultes", "non significatif"),
    ("Alimentation méditerranéenne", "crp", -0.77, "mg/L", 0.1, "Papadaki 2020", "TC", "adultes", ""),
    ("Perte de poids de 5 kg", "alt", -0.83 * 5, "U/L", 1, "Koutoukidis 2021, Metabolism, doi:10.1016/j.metabol.2020.154455", "R", "stéatose (NAFLD)", "−0,83 U/L par kg"),
    ("Perte de poids de 5 kg", "ast", -0.56 * 5, "U/L", 1, "Koutoukidis 2021", "R", "stéatose (NAFLD)", "−0,56 U/L par kg"),
    ("Perte de poids de 5 kg (poids stabilisé)", "hdl", 0.009 * 5, "mmol/L", 38.67, "Dattilo 1992, Am J Clin Nutr, doi:10.1093/ajcn/56.2.320", "R", "70 études", "+0,009 mmol/L par kg ; autres lipides : pente par kg absente du résumé"),
    ("Vitamine D3, 25 µg/j", "vitd", 1.95 * 25, "nmol/L", 0.4, "Autier 2012, J Clin Endocrinol Metab, doi:10.1210/jc.2012-1238", "R", "plus de 50 ans, sans calcium", "+1,95 nmol/L par µg/j"),
    ("Oméga-3 (EPA + DHA), 2 g/j", "tg_fast", -42.61, "mg/dL", 1, "Wang 2023, J Am Heart Assoc, doi:10.1161/JAHA.123.029512", "TC", "90 ECR, surtout hyperlipidémiques", "plateau d'environ 40 mg/dL sans hyperlipidémie"),
    ("Acide folique 0,8 mg/j", "hcy", None, "%", None, "Homocysteine Lowering Trialists' Collaboration 2005, Am J Clin Nutr, doi:10.1093/ajcn/82.4.806", "R", "25 ECR", "−23 % ; +B12 0,4 mg : −7 % de plus"),
    ("Fer oral (femmes réglées)", "hb", 0.53, "g/dL", 1, "Low 2016, Cochrane, doi:10.1002/14651858.CD009747.pub2", "R", "femmes réglées", "+5,30 g/L"),
]
PCT_DIRECT = {"hcy": -23.0}
NOT_FOUND = [
    ("Activité physique", "CRP", "résumés lus sans estimation chiffrée (Hejazi 2023 ; Batacan 2017)"),
    ("Activité physique", "ALAT", "résumé lu sans estimation chiffrée de l'ALAT (Smart 2018)"),
    ("Perte de poids", "TG, LDL, cholestérol total (par kg)", "pentes par kg absentes du résumé de Dattilo 1992"),
    ("Perte de poids", "glucose, HbA1c, insuline, CRP, acide urique", "rien trouvé avec ces requêtes hors médicaments (GLP-1, orlistat, chirurgie)"),
    ("Réduction de l'alcool", "GGT, HDL, TG, VGM", "rien trouvé avec ces requêtes"),
    ("Fer oral (sportifs)", "ferritine", "effet en différence standardisée seulement (DMS 1,27 ; Šmid 2024)"),
]


def run() -> pd.DataFrame:
    cd = pd.read_csv(OUT / "Q1_changement_detectable.csv")
    v = pd.read_csv(OUT / "Q1_variabilite_remesures.csv")
    main = cd[cd.groupe == "20-79 ans"].set_index("id")["jeu_principal"]
    v55 = v[v.groupe == "30-55 ans"]
    med = {i: g.set_index("jeu")["mediane_x1"].get(main.get(i), g.mediane_x1.iloc[0]) for i, g in v55.groupby("id")}
    rows = []
    for inter, mid, eff, unit, conv, src, lu, pop, note in EFFECTS:
        if mid in PCT_DIRECT:
            pct = PCT_DIRECT[mid]
            base = np.nan
        else:
            base = float(med.get(mid, np.nan))
            pct = 100 * eff * conv / base
        for grp in ["20-79 ans", "30-55 ans"]:
            c = cd[(cd.groupe == grp) & (cd.id == mid)]
            if c.empty:
                continue
            c = c.iloc[0]
            seuil = c.cd6m_baisse if pct < 0 else c.cd6m_hausse
            emp = c.get(f"cd_emp_baisse_{c.jeu_principal}") if pct < 0 else c.get(f"cd_emp_hausse_{c.jeu_principal}")
            ratio = abs(pct) / seuil
            concl = "détectable chez une personne" if ratio >= 1 else ("limite" if ratio >= 0.5 else "visible seulement en moyenne de groupe")
            rows.append({"groupe": grp, "intervention": inter, "id": mid, "marqueur": c.marqueur, "effet": eff, "unite": unit,
                         "mediane_nhanes_30_55": base, "effet_pct": pct, "cd6m_pct": seuil, "statut_cd": c.statut,
                         "ratio": ratio, "conclusion": concl,
                         "ratio_cd_empirique_2sem": abs(pct) / emp if emp and np.isfinite(emp) else np.nan,
                         "source": src, "lu": lu, "population": pop, "note": note})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "Q1_interventions.csv", index=False)
    pd.DataFrame(NOT_FOUND, columns=["intervention", "marqueurs", "motif"]).to_csv(OUT / "Q1_interventions_non_trouvees.csv", index=False)
    return t
