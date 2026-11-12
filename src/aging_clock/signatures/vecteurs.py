"""Piste « signatures » : vecteurs d'effet des interventions (pre-enregistres dans DECISIONS.md).

Chaque composante : variation relative (%) au scenario fixe, source lue, population, lecture (R = resume,
TC = texte complet), et note de conversion. Une composante sans source lue vaut 0 et est signalee.
Les effets absolus sont convertis en % par la mediane NHANES des 30-55 ans au premier examen des
remesures, comme dans Q1 (Q1_interventions.csv), sauf mention.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PANEL = ["tc", "hdl", "tg_serum", "glu_serum", "hba1c", "alt", "ast", "ggt", "alp", "albumin", "creat", "urea", "urate",
         "wbc", "hb", "mcv", "rdw", "plt"]                      # signature principale (CRP exclue : NHANES III censure a 62 %)
PANEL_CRP = PANEL + ["crp"]                                      # sensibilite (2001-2002 seulement)

# Medianes de conversion (30-55 ans, premier examen des remesures, comme Q1)
MED = {"tc": 203.0, "hdl": 48.0, "tg": 118.0, "alt": 15.0, "ast": 19.0, "ggt": 23.0, "crp_mgL": 2.7, "wbc": 6.9}
SD_LN_CRP = 1.274                                                # 30-55 ans, 2001-2002, premier examen (CRP > 0)

# (intervention, marqueur, effet %, source, population, lecture, note)
C = [
    # --- perte de poids de 7 kg (environ 5 a 10 %)
    ("perte_poids", "tg_serum", 100 * (-4.0 * 7) / MED["tg"], "Hasan 2020, J Clin Endocrinol Metab, doi:10.1210/clinem/dgaa673",
     "73 ECR, surpoids ou obésité (IMC moyen 36)", "R", "−4,0 mg/dL par kg (TG à jeun) × 7 kg ; appliqué aux TG non à jeun"),
    ("perte_poids", "hdl", 100 * (0.46 * 7) / MED["hdl"], "Hasan 2020", "73 ECR, surpoids ou obésité", "R", "+0,46 mg/dL par kg × 7 kg"),
    ("perte_poids", "tc", 100 * (-1.28 * 7 + 0.46 * 7 + (-4.0 * 7) / 5) / MED["tc"], "Hasan 2020 (dérivé)", "73 ECR, surpoids ou obésité", "R",
     "dérivé par Friedewald : ΔLDL + ΔHDL + ΔTG/5 (pas de pente du cholestérol total lue)"),
    ("perte_poids", "alt", 100 * (-0.83 * 7) / MED["alt"], "Koutoukidis 2021, Metabolism, doi:10.1016/j.metabol.2020.154455",
     "stéatose (NAFLD)", "R", "−0,83 U/L par kg × 7 kg ; autre étude que les lipides"),
    ("perte_poids", "ast", 100 * (-2.8 / 5 * 7) / MED["ast"], "Koutoukidis 2021", "stéatose (NAFLD)", "R", "−2,8 U/L pour 5 kg, mis à l'échelle de 7 kg"),
    ("perte_poids", "glu_serum", -4.1, "Magkos 2016, Cell Metab, doi:10.1016/j.cmet.2016.02.005", "obèses non diabétiques, n = 19 contre 14",
     "TC", "essai unique, perte de 5 % ; glycémie à jeun appliquée à la glycémie sérique"),
    ("perte_poids", "crp", 100 * (-0.06 * 7) / MED["crp_mgL"], "Selvin 2007, Arch Intern Med, doi:10.1001/archinte.167.1.31",
     "33 études, interventions sur le mode de vie", "R", "pente des interventions sur le mode de vie, 0,06 mg/L par kg × 7 kg (sensibilité avec CRP)"),
    # --- activite physique aerobie structuree
    ("activite_aerobie", "tc", -2.906, "Smart 2025, Sports Med, doi:10.1007/s40279-024-02115-z", "148 ECR, adultes", "R",
     "toutes formes d'activité (sous-groupe aérobie non lu)"),
    ("activite_aerobie", "hdl", 4.396, "Smart 2025", "148 ECR, adultes", "R", "idem"),
    ("activite_aerobie", "tg_serum", -6.788, "Smart 2025", "148 ECR, adultes", "R", "TG à jeun ; appliqué aux TG non à jeun"),
    ("activite_aerobie", "glu_serum", -2.919, "Wewege 2018, Atherosclerosis, doi:10.1016/j.atherosclerosis.2018.05.002",
     "syndrome métabolique", "R", "glycémie à jeun ; autre étude que les lipides"),
    ("activite_aerobie", "alt", 0.0, "Smart 2018, Br J Sports Med, doi:10.1136/bjsports-2016-096197", "surpoids ou stéatose", "R",
     "ALAT, ASAT, GGT « non significativement modifiées » : 0 sourcé"),
    ("activite_aerobie", "ast", 0.0, "Smart 2018", "surpoids ou stéatose", "R", "0 sourcé"),
    ("activite_aerobie", "ggt", 0.0, "Smart 2018", "surpoids ou stéatose", "R", "0 sourcé"),
    ("activite_aerobie", "crp", 100 * (np.exp(-0.18 * SD_LN_CRP) - 1), "Wang 2023, Front Psychol, doi:10.3389/fpsyg.2023.1253329",
     "38 ECR, adultes en bonne santé", "TC", "DMS −0,18 × écart type de ln CRP (1,27, 30-55 ans) ; conversion par hypothèse"),
    # --- alimentation mediterraneenne (une seule meta-analyse)
    *[("mediterraneen", m, v, "Papadaki 2020, Nutrients, doi:10.3390/nu12113342", "adultes, 57 essais contrôlés", "TC", note)
      for m, v, note in [("tc", -2.808, ""), ("hdl", 2.708, ""), ("tg_serum", -10.424, "TG à jeun ; appliqué aux TG non à jeun"),
                         ("glu_serum", -3.222, "glycémie à jeun ; appliquée à la glycémie sérique"), ("hba1c", -2.830, ""),
                         ("alt", -37.733, "−5,66 U/L sur une médiane de 15 : effet très grand, probablement porté par des études chez des personnes avec stéatose"),
                         ("ggt", -10.913, ""), ("crp", -28.519, "sensibilité avec CRP")]],
    # --- reduction de l'alcool (de 30 g/j a 0)
    ("reduction_alcool", "hdl", 100 * (-3.99) / MED["hdl"], "Rimm 1999, BMJ, doi:10.1136/bmj.319.7224.1523",
     "adultes sans maladie chronique ni dépendance", "R", "effet de +30 g/j inversé (arrêt de 30 g/j) ; Brien 2011 (R) confirme le HDL"),
    ("reduction_alcool", "tg_serum", 100 * (-5.69) / MED["tg"], "Rimm 1999", "adultes sans maladie chronique ni dépendance", "R",
     "effet inversé ; Brien 2011 (R) ne trouve pas d'effet sur les TG : composante incertaine"),
    ("reduction_alcool", "ggt", 0.0, "Munsterman 2018, Alcohol Alcohol, doi:10.1093/alcalc/agy031 ; Kechagias 2015, Alcohol Alcohol, "
     "doi:10.1093/alcalc/agv038", "buveurs modérés en bonne santé ; 44 volontaires sains (essai randomisé, 3 mois)", "R",
     "aucun chiffre d'intervention lu ; l'essai chez des sains ne voit pas la GGT distinguer 16-32 g/j de l'abstinence : 0 ; "
     "signature non interprétable (sensibilité illustrative non sourcée : GGT −15 %)"),
    ("reduction_alcool", "mcv", 0.0, "Kechagias 2015", "44 volontaires sains (essai randomisé, 3 mois)", "R",
     "le VGM ne distingue pas la consommation modérée de l'abstinence : 0"),
    # --- arret du tabac
    ("arret_tabac", "hdl", 100 * (0.100 * 38.67) / MED["hdl"], "Maeda 2003, Prev Med, doi:10.1016/s0091-7435(03)00110-5",
     "27 études prospectives de fumeurs abstinents", "R", "+0,100 mmol/L ; TC, LDL et TG inchangés (0 sourcé)"),
    ("arret_tabac", "tc", 0.0, "Maeda 2003", "27 études prospectives", "R", "0 sourcé (non significatif)"),
    ("arret_tabac", "tg_serum", 0.0, "Maeda 2003 ; van der Plas 2023, Toxicol Rep, doi:10.1016/j.toxrep.2023.03.001", "fumeurs abstinents", "R",
     "0 sourcé (non significatif à 1 an)"),
    ("arret_tabac", "wbc", 100 * (-0.8) / MED["wbc"], "King 2017, Arterioscler Thromb Vasc Biol, doi:10.1161/ATVBAHA.116.308728",
     "888 fumeurs tentant d'arrêter, essai et soins courants", "TC", "−0,6 contre +0,2 G/L à 1 an (abstinents contre fumeurs) ; étude unique"),
    ("arret_tabac", "crp", 0.0, "King 2017", "fumeurs tentant d'arrêter", "TC", "CRP non modifiée à 1 an : 0 sourcé (sensibilité avec CRP)"),
]
INTERVENTIONS = ["perte_poids", "activite_aerobie", "mediterraneen", "reduction_alcool", "arret_tabac"]
NOMS = {"perte_poids": "Perte de poids de 7 kg (5 à 10 %)", "activite_aerobie": "Activité physique aérobie structurée",
        "mediterraneen": "Alimentation méditerranéenne", "reduction_alcool": "Réduction de l'alcool (de 30 g/j à 0)",
        "arret_tabac": "Arrêt du tabac"}


def table() -> pd.DataFrame:
    return pd.DataFrame(C, columns=["intervention", "id", "effet_pct", "source", "population", "lu", "note"])


LIVER = ("alt", "ast", "ggt")
GGT_ALCOOL_ILLUSTRATIF = -15.0   # sensibilite illustrative, non sourcee


def vector(intervention: str, panel=PANEL, liver_factor: float = 1.0, alcool_illustratif: bool = False) -> np.ndarray:
    """Vecteur d'effet sur l'echelle log (ln(1 + effet)) ; 0 pour les composantes sans source.
    liver_factor : multiplicateur des composantes ALAT, ASAT, GGT (sensibilites B8 : 0,5 et 0)."""
    t = table()
    t = t[t.intervention == intervention].set_index("id")
    out = []
    for m in panel:
        e = t.loc[m, "effet_pct"] if m in t.index else 0.0
        if alcool_illustratif and intervention == "reduction_alcool" and m == "ggt":
            e = GGT_ALCOOL_ILLUSTRATIF
        if m in LIVER:
            e = e * liver_factor
        out.append(np.log1p(e / 100))
    return np.array(out)
