# Q1 : changement détectable à 6 mois, marqueur par marqueur

Programme « panel » : le comportement des biomarqueurs d'un check-up de prévention, sur un cas
générique (bilan large au départ, puis prise de sang tous les 6 mois, sans contrôle de l'heure ni
du jeûne). Protocole pré-enregistré dans `DECISIONS.md` (commit `76c3962`, avant tout calcul).
Code : `src/aging_clock/panel/` (`remesures.py`, `q1.py`, `q1_interventions.py`). Données :
`Q1_variabilite_remesures.csv`, `Q1_changement_detectable.csv`, `Q1_interventions.csv`.

## À lire avant les chiffres

- **Le changement détectable ne comprend pas la variabilité entre laboratoires.** Il suppose la
  même méthode aux deux bilans. Changer de laboratoire ajoute un décalage, étudié en Q5.
- **Les effets d'interventions sont des effets moyens.** Ils viennent de méta-analyses d'essais
  et ne disent rien de la variabilité de la réponse d'une personne à l'autre : certains répondent
  beaucoup plus, d'autres pas du tout.
- **Bornes basses.** Les remesures ont lieu à environ 2 semaines, avec le même laboratoire et le
  même protocole. À 6 mois, la variabilité est plus grande. On ne l'ajoute que lorsqu'une étude
  EFLM à long terme de bonne qualité existe (statut « extrapolé à 6 mois »). Sinon, le chiffre est
  une **borne basse**.
- **NHANES est américain**, et ses laboratoires sont centralisés : la variabilité analytique y est
  plus faible que dans un réseau de laboratoires.
- **Seuils.** Q1 n'utilise aucun seuil clinique. Dans les questions suivantes, on distinguera
  toujours les **conventions statistiques** (intervalles de référence : 95 % central d'une
  population saine) des **seuils fondés sur le risque** (recommandations de décision clinique).

## Méthode

1. **Variabilité observée** sur deux jeux de remesures, analysés séparément :
   - NHANES 2001-2002, second examen (environ 400 adultes) ;
   - NHANES III, second examen (jusqu'à 1 800 adultes).

   On garde les adultes de 20 à 79 ans, hors femmes enceintes. Avec $d = \ln x_2 - \ln x_1$ :
   - CV observé $= \sqrt{e^{\mathrm{Var}(d)/2}-1}$, en version classique et robuste ;
   - changement empirique = P95 de $|d|$ ;
   - IC par bootstrap (2 000 tirages).

   Les marqueurs qui peuvent valoir 0 (basophiles, éosinophiles en nombre, Lp(a), et certaines
   formules de NHANES III) sont sur l'échelle additive, en unités. Le jeu principal est NHANES III,
   sauf s'il manque ou si plus de 20 % de ses valeurs sont au plancher. C'est le cas de la CRP,
   censurée chez 62 % des personnes dans NHANES III.
2. **Extrapolation à 6 mois** : $CV_{6m}^2 = CV_{obs}^2 + \max(0, CV_{I,LT}^2 - CV_{I,CT}^2)$.
   - CV_I,CT : méta-analyse EFLM.
   - CV_I,LT : médiane des études EFLM (BIVAC) qui réunissent ces conditions :
     - durée ≥ 6 mois ;
     - adultes en bonne santé ;
     - sérum, plasma ou sang total ;
     - note A ou B.
3. **Changement détectable** (deux mesures, 95 %) : hausse $e^{1{,}96\sqrt2\,\sigma}-1$, baisse
   $1-e^{-1{,}96\sqrt2\,\sigma}$, avec $\sigma=\sqrt{\ln(1+CV_{6m}^2)}$. L'asymétrie vient de
   l'échelle log : +100 % et −50 % correspondent au même écart.
4. **Interventions** :
   - méta-analyses d'essais trouvées avec les requêtes pré-enregistrées, et lues (résumé « R » ou
     texte complet « TC ») ;
   - effet converti en % de la médiane NHANES des 30-55 ans ;
   - ratio = |effet| / changement détectable dans le même sens.

## Ce que montrent les données des remesures

Les trois prédictions pré-enregistrées sur la variabilité sont **vérifiées** :

| Prédiction | Observé | Vérifiée |
|---|---|---|
| L'EFLM sous-estime le CV observé pour ≥ 2/3 des marqueurs | 35 marqueurs sur 42 (83 %) | oui |
| Queues épaisses (changement empirique > 1,10 × celui du CV robuste) pour ≥ 50 % des marqueurs | 80 % (56 sur 70) | oui |
| Réplication : CV de 2001-2002 et de NHANES III à moins d'un facteur 1,5 pour ≥ 2/3 des marqueurs | 93 % (57 sur 61) | oui |

**L'EFLM à long terme est rare.** Sur 572 jeux de données EFLM de 6 mois ou plus, seuls 30
remplissent les critères. La plupart des études longues ont la note BIVAC C. Un CV_I à long terme
n'existe donc que pour la numération, l'ALAT, l'ASAT, les bicarbonates, les plaquettes et la TSH.
Ailleurs, le changement détectable reste une borne basse à 2 semaines. 81 % des jeux utilisés
dans les méta-analyses EFLM durent moins de 6 mois : le CV_I « méta-analyse » est bien un CV à
court terme.

## Changement détectable à 6 mois

| Marqueur | Jeu principal | n | CV observé (%) | **Changement détectable à 6 mois (%)**, hausse / baisse, 20-79 ans | 30-55 ans | Statut |
|---|---|---|---|---|---|---|
| Leucocytes | NHANES III | 1791 | 13,0 | **+46 / −31** | +48 / −32 | extrapolé à 6 mois |
| Neutrophiles (%) | NHANES III | 272 | 12,0 | **+43 / −30** | +43 / −30 | extrapolé à 6 mois |
| Neutrophiles (nombre) | 2001-02 | 420 | 20,3 | **+77 / −44** | +72 / −42 | extrapolé à 6 mois |
| Lymphocytes (%) | NHANES III | 1792 | 13,9 | **+47 / −32** | +46 / −31 | extrapolé à 6 mois |
| Lymphocytes (nombre) | NHANES III | 1791 | 13,4 | **+45 / −31** | +46 / −32 | extrapolé à 6 mois |
| Monocytes (%) | 2001-02 | 420 | 14,5 | **+57 / −36** | +60 / −38 | extrapolé à 6 mois |
| Monocytes (nombre) | 2001-02 | 420 | 17,4 | **+69 / −41** | +70 / −41 | extrapolé à 6 mois |
| Éosinophiles (%) | 2001-02 | 420 | 28,3 | **+119 / −54** | +116 / −54 | extrapolé à 6 mois |
| Éosinophiles (nombre) | 2001-02 | 420 | ET intra 0,07 | **± 0,20 (unités)** | ± 0,17 | borne basse (2 semaines), échelle additive |
| Basophiles (%) | 2001-02 | 420 | ET intra 0,30 | **± 0,82 (unités)** | ± 0,83 | borne basse (2 semaines), échelle additive |
| Basophiles (nombre) | — | — | — | — | — | non interprétable (valeurs censurées > 20 %) |
| Hématies | NHANES III | 1790 | 2,9 | **+10 / −9** | +10 / −9 | extrapolé à 6 mois |
| Hémoglobine | NHANES III | 1792 | 3,0 | **+10 / −9** | +10 / −9 | extrapolé à 6 mois |
| Hématocrite | NHANES III | 1790 | 3,0 | **+10 / −9** | +10 / −9 | extrapolé à 6 mois |
| VGM | NHANES III | 1792 | 0,8 | **+3 / −3** | +3 / −3 | extrapolé à 6 mois |
| TCMH | NHANES III | 1791 | 1,4 | **+5 / −4** | +5 / −5 | extrapolé à 6 mois |
| CCMH | NHANES III | 1791 | 1,5 | **+5 / −4** | +4 / −4 | extrapolé à 6 mois |
| RDW | NHANES III | 1792 | 2,0 | **+7 / −6** | +7 / −7 | extrapolé à 6 mois |
| Plaquettes | NHANES III | 1766 | 10,9 | **+35 / −26** | +42 / −29 | extrapolé à 6 mois |
| VPM | NHANES III | 1792 | 4,5 | **+13 / −12** | +14 / −12 | borne basse (2 semaines) |
| Glycémie à jeun (plasma) | NHANES III | 1190 | 9,3 | **+29 / −23** | +24 / −19 | borne basse (2 semaines) |
| Glucose sérique (non à jeun) | NHANES III | 1756 | 10,4 | **+33 / −25** | +27 / −22 | borne basse (2 semaines) |
| Insuline (à jeun) | NHANES III | 1182 | 28,2 | **+115 / −54** | +120 / −55 | borne basse (2 semaines) |
| HbA1c | NHANES III | 1821 | 3,6 | **+10 / −9** | +11 / −10 | borne basse (2 semaines) |
| Cholestérol total | NHANES III | 1807 | 8,3 | **+26 / −21** | +26 / −21 | borne basse (2 semaines) |
| LDL (calculé, à jeun) | NHANES III | 583 | 14,0 | **+47 / −32** | +57 / −36 | borne basse (2 semaines) |
| HDL | NHANES III | 1779 | 12,9 | **+43 / −30** | +41 / −29 | borne basse (2 semaines) |
| Triglycérides (à jeun) | NHANES III | 1798 | 27,4 | **+111 / −53** | +115 / −54 | borne basse (2 semaines) |
| Triglycérides sériques (non à jeun) | NHANES III | 1342 | 25,7 | **+101 / −50** | +109 / −52 | borne basse (2 semaines) |
| ALAT | NHANES III | 1757 | 23,4 | **+181 / −64** | +186 / −65 | extrapolé à 6 mois |
| ASAT | NHANES III | 1757 | 17,2 | **+86 / −46** | +92 / −48 | extrapolé à 6 mois |
| GGT | NHANES III | 1392 | 15,5 | **+53 / −35** | +54 / −35 | borne basse (2 semaines) |
| PAL | NHANES III | 1757 | 7,1 | **+22 / −18** | +24 / −19 | borne basse (2 semaines) |
| Bilirubine totale | 2001-02 | 409 | 18,4 | **+66 / −40** | +68 / −41 | borne basse (2 semaines) |
| Albumine | NHANES III | 1757 | 4,4 | **+13 / −11** | +13 / −11 | borne basse (2 semaines) |
| Protéines totales | NHANES III | 1757 | 3,6 | **+10 / −9** | +10 / −9 | borne basse (2 semaines) |
| Créatinine | NHANES III | 1757 | 6,8 | **+21 / −17** | +21 / −17 | borne basse (2 semaines) |
| Urée | NHANES III | 1757 | 18,9 | **+68 / −40** | +69 / −41 | borne basse (2 semaines) |
| Sodium | NHANES III | 1757 | 1,3 | **+4 / −4** | +4 / −4 | borne basse (2 semaines) |
| Potassium | NHANES III | 1757 | 5,4 | **+16 / −14** | +15 / −13 | borne basse (2 semaines) |
| Chlorure | NHANES III | 1757 | 2,1 | **+6 / −6** | +6 / −6 | borne basse (2 semaines) |
| Bicarbonates | NHANES III | 1757 | 11,4 | **+38 / −27** | +41 / −29 | extrapolé à 6 mois |
| CRP | 2001-02 | 412 | 58,7 | **+351 / −78** | +397 / −80 | borne basse (2 semaines) |
| Vitamine B12 | NHANES III | 894 | 14,3 | **+48 / −33** | +58 / −37 | borne basse (2 semaines) |
| Folates érythrocytaires | NHANES III | 1176 | 9,4 | **+30 / −23** | +31 / −24 | borne basse (2 semaines) |
| 25-OH vitamine D | 2001-02 | 341 | 15,7 | **+54 / −35** | +58 / −37 | borne basse (2 semaines) |
| Calcium | NHANES III | 1757 | 3,3 | **+10 / −9** | +9 / −9 | borne basse (2 semaines) |
| LH | NHANES III | 275 | 67,6 | **+448 / −82** | +534 / −84 | borne basse (2 semaines) |
| FSH | 2001-02 | 86 | 43,8 | **+219 / −69** | +253 / −72 | borne basse (2 semaines) |
| PSA total | 2001-02 | 102 | 17,4 | **+62 / −38** | +63 / −39 | borne basse (2 semaines) |
| PSA libre | 2001-02 | 102 | 18,0 | **+64 / −39** | +63 / −39 | borne basse (2 semaines) |
| Fer sérique | NHANES III | 1817 | 31,1 | **+132 / −57** | +149 / −60 | borne basse (2 semaines) |
| Ferritine | NHANES III | 1807 | 22,3 | **+84 / −46** | +94 / −48 | borne basse (2 semaines) |
| Homocystéine | 2001-02 | 418 | 13,7 | **+46 / −32** | +44 / −31 | borne basse (2 semaines) |
| Acide urique | NHANES III | 1756 | 9,4 | **+30 / −23** | +30 / −23 | borne basse (2 semaines) |
| Phosphate | NHANES III | 1757 | 9,4 | **+30 / −23** | +32 / −24 | borne basse (2 semaines) |
| Albumine urinaire | NHANES III | 1196 | 107,5 | **+1034 / −91** | +1073 / −91 | borne basse (2 semaines) |
| Créatinine urinaire | NHANES III | 1196 | 56,4 | **+330 / −77** | +365 / −78 | borne basse (2 semaines) |
| HOMA-IR | NHANES III | 1174 | 32,1 | **+139 / −58** | +142 / −59 | borne basse (2 semaines) |
| QUICKI | NHANES III | 1174 | 4,5 | **+13 / −12** | +14 / −12 | borne basse (2 semaines) |
| Glycémie moyenne estimée | NHANES III | 1821 | 5,2 | **+15 / −13** | +17 / −14 | borne basse (2 semaines) |
| Indice TyG | NHANES III | 1159 | ET intra 0,29 | **± 0,79 (unités)** | ± 0,80 | borne basse (2 semaines), échelle additive |
| Cholestérol non-HDL | NHANES III | 1778 | 11,2 | **+36 / −27** | +35 / −26 | borne basse (2 semaines) |
| LDL/HDL | NHANES III | 583 | 19,4 | **+70 / −41** | +76 / −43 | borne basse (2 semaines) |
| TG/HDL | NHANES III | 1775 | 32,5 | **+141 / −58** | +143 / −59 | borne basse (2 semaines) |
| Indice athérogène (log10 TG/HDL, mmol) | NHANES III | 1775 | ET intra 0,14 | **± 0,38 (unités)** | ± 0,39 | borne basse (2 semaines), échelle additive |
| Albumine/globulines | NHANES III | 1757 | 8,3 | **+26 / −20** | +27 / −21 | borne basse (2 semaines) |
| FIB-4 | NHANES III | 1683 | 17,3 | **+61 / −38** | +69 / −41 | borne basse (2 semaines) |
| GGT/HDL | NHANES III | 1363 | 18,2 | **+65 / −39** | +63 / −38 | borne basse (2 semaines) |
| ASAT/ALAT | NHANES III | 1757 | 17,6 | **+62 / −38** | +64 / −39 | borne basse (2 semaines) |
| Urée/créatinine | NHANES III | 1757 | 18,8 | **+68 / −40** | +69 / −41 | borne basse (2 semaines) |
| Osmolalité effective (2 Na + glucose) | NHANES III | 1756 | 1,3 | **+4 / −4** | +4 / −4 | borne basse (2 semaines) |
| Neutrophiles/lymphocytes | NHANES III | 271 | 24,8 | **+97 / −49** | +84 / −46 | borne basse (2 semaines) |
| Indice SII | NHANES III | 269 | 28,8 | **+119 / −54** | +97 / −49 | borne basse (2 semaines) |
| Calcium corrigé | NHANES III | 1757 | 3,0 | **+9 / −8** | +9 / −8 | borne basse (2 semaines) |
| DFGe (CKD-EPI 2021) | NHANES III | 1757 | 8,0 | **+25 / −20** | +24 / −19 | borne basse (2 semaines) |
| Granulocytes (%, automate) | NHANES III | 1742 | 9,2 | **+29 / −22** | +30 / −23 | borne basse (2 semaines) |
| Globulines | NHANES III | 1342 | 5,8 | **+18 / −15** | +18 / −15 | borne basse (2 semaines) |
| Osmolalité mesurée | NHANES III | 1342 | 1,2 | **+4 / −3** | +3 / −3 | borne basse (2 semaines) |
| ApoA1 | NHANES III | 838 | 8,5 | **+27 / −21** | +26 / −21 | borne basse (2 semaines) |
| ApoB | NHANES III | 850 | 9,9 | **+31 / −24** | +28 / −22 | borne basse (2 semaines) |
| Lp(a) | NHANES III | 952 | ET intra 7,63 | **± 21,15 (unités)** | ± 22,13 | borne basse (2 semaines), échelle additive |
| Capacité totale de fixation du fer | NHANES III | 1756 | 6,7 | **+21 / −17** | +21 / −17 | borne basse (2 semaines) |
| Saturation de la transferrine | NHANES III | 1756 | 31,4 | **+134 / −57** | +153 / −60 | borne basse (2 semaines) |
| Sélénium | NHANES III | 1714 | 6,8 | **+21 / −17** | +21 / −17 | borne basse (2 semaines) |
| Iode urinaire | NHANES III | 1148 | 70,9 | **+486 / −83** | +465 / −82 | borne basse (2 semaines) |

Lecture : pour l'hémoglobine, un changement de moins de +10 % ou −9 % entre deux bilans à 6 mois
n'est pas distinguable de la variabilité normale. Pour les indices dérivés (HOMA-IR, rapports,
FIB-4…), il n'existe pas d'étude EFLM à long terme : ce sont des bornes basses. Les CV_I utilisés
viennent de l'EFLM Biological Variation Database (biologicalvariation.eu, consultée le 10 novembre
2026). Ils ne sont pas reproduits ici, pour respecter la licence de la base.

**Marqueurs sans remesure** (statut « EFLM seul »). Hypothèses :
$CV = \sqrt{CV_I^2 + (0{,}5\,CV_I)^2}$ ; CV_I de la base EFLM, à long terme si une étude A/B existe (TSH), sinon à
court terme. Les CV_I eux-mêmes ne sont pas reproduits ici (licence de la base EFLM).

| Marqueur | Changement détectable (%), hausse / baisse |
|---|---|
| Thyroid stimulating hormone (TSH) | +77 / −43 |
| Testosterone | +55 / −36 |
| Sex hormone-binding globulin (SHBG) | +29 / −23 |
| Thyroxine - free (FT4) | +16 / −14 |
| DHEAS | +84 / −46 |
| Estradiol | +59 / −37 |
| Magnesium | +9 / −9 |
| Lipase | +27 / −21 |

**Trois familles se dessinent** (interprétation) :

| Variabilité | Marqueurs | Changement détectable |
|---|---|---|
| **Très stables** | VGM, TCMH, CCMH, RDW, sodium, chlorure, osmolalité | moins de 7 % |
| **Stables** | hémoglobine, hématocrite, hématies, HbA1c, calcium, protéines, albumine, VPM | environ 10 à 13 % |
| **Bruités** | CRP, insuline, triglycérides, ALAT, fer, LH, FSH, urines | souvent plus de 100 % à la hausse : une valeur isolée ne se compare presque pas |

**Deux points d'attention :**
- **Bicarbonates.** CV de 11 % dans NHANES III contre 6 % en 2001-2002.
  - **Correction du 2026-11-11.** La première version de ce rapport donnait 18 % et l'attribuait à
    un artefact pré-analytique (perte de CO₂). C'était en réalité un **bug de lecture** : le code
    « 88 » (vide mais applicable) des champs à 2 chiffres de NHANES III était lu comme une valeur,
    sur 1 495 bicarbonates. Voir `DECISIONS.md`.
  - Après correction, le CV de NHANES III reste deux fois plus grand que celui de 2001-2002. Je n'en
    connais pas la cause.
- **Neutrophiles (%).** Dans NHANES III, la formule est faite à la main et ne porte que sur
  272 personnes.

## Effets d'interventions rapportés au changement détectable

| Intervention | Marqueur | Effet moyen | Changement détectable à 6 mois | **Ratio**, 20-79 ans | Ratio, 30-55 ans | Conclusion | Source (lecture) ; population |
|---|---|---|---|---|---|---|---|
| Activité physique (toutes formes) | Cholestérol total | −3 % | 21 % | **0,14** | 0,14 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | HDL | +4 % | 43 % | **0,10** | 0,11 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | LDL (calculé, à jeun) | −6 % | 32 % | **0,18** | 0,16 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | Triglycérides (à jeun) | −7 % | 53 % | **0,13** | 0,13 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique structurée | HbA1c | −13 % | 9 % | **1,34** | 1,26 | détectable chez une personne | Umpierre 2011 (R) ; diabète de type 2 |
| Activité physique aérobie | Glycémie à jeun (plasma) | −3 % | 23 % | **0,13** | 0,15 | visible seulement en moyenne de groupe | Wewege 2018 (R) ; syndrome métabolique |
| Activité physique (toutes formes) | Insuline (à jeun) | −20 % | 54 % | **0,37** | 0,36 | visible seulement en moyenne de groupe | Smart 2018 (R) ; surpoids ou stéatose |
| Alimentation méditerranéenne | Glycémie à jeun (plasma) | −3 % | 23 % | **0,14** | 0,17 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes, 57 essais contrôlés |
| Alimentation méditerranéenne | Insuline (à jeun) | −10 % | 54 % | **0,18** | 0,18 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HOMA-IR | −19 % | 58 % | **0,33** | 0,32 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HbA1c | −3 % | 9 % | **0,30** | 0,28 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | Cholestérol total | −3 % | 21 % | **0,14** | 0,13 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | LDL (calculé, à jeun) | −7 % | 32 % | **0,21** | 0,19 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HDL | +3 % | 43 % | **0,06** | 0,07 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | Triglycérides (à jeun) | −10 % | 53 % | **0,20** | 0,19 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | ALAT | −38 % | 64 % | **0,59** | 0,58 | limite | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | GGT | −11 % | 35 % | **0,31** | 0,31 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | CRP | −29 % | 78 % | **0,37** | 0,36 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Perte de poids de 5 kg | ALAT | −28 % | 64 % | **0,43** | 0,43 | visible seulement en moyenne de groupe | Koutoukidis 2021 (R) ; stéatose (NAFLD) |
| Perte de poids de 5 kg | ASAT | −15 % | 46 % | **0,32** | 0,31 | visible seulement en moyenne de groupe | Koutoukidis 2021 (R) ; stéatose (NAFLD) |
| Perte de poids de 5 kg (poids stabilisé) | HDL | +4 % | 43 % | **0,08** | 0,09 | visible seulement en moyenne de groupe | Dattilo 1992 (R) ; 70 études |
| Vitamine D3, 25 µg/j | 25-OH vitamine D | +98 % | 54 % | **1,80** | 1,67 | détectable chez une personne | Autier 2012 (R) ; plus de 50 ans, sans calcium |
| Oméga-3 (EPA + DHA), 2 g/j | Triglycérides (à jeun) | −36 % | 53 % | **0,69** | 0,67 | limite | Wang 2023 (TC) ; 90 ECR, surtout hyperlipidémiques |
| Acide folique 0,8 mg/j | Homocystéine | −23 % | 32 % | **0,73** | 0,75 | limite | Homocysteine Lowering Trialists' Collaboration 2005 (R) ; 25 ECR |
| Fer oral (femmes réglées) | Hémoglobine | +4 % | 10 % | **0,37** | 0,37 | visible seulement en moyenne de groupe | Low 2016 (R) ; femmes réglées |

Règle pré-enregistrée :
- **≥ 1** : un effet moyen est détectable chez une personne ;
- **0,5 à 1** : limite ;
- **< 0,5** : visible seulement en moyenne de groupe.

**Non trouvé ou non chiffré** (`Q1_interventions_non_trouvees.csv`) :
- **CRP sous activité physique**, et **ALAT sous activité physique** : les résumés lus ne donnent
  pas d'estimation chiffrée ;
- **TG, LDL et cholestérol par kg perdu** : absents du résumé de Dattilo 1992 ;
- **glucose, HbA1c, insuline, CRP et acide urique sous perte de poids sans médicament** : rien
  trouvé avec ces requêtes ;
- **réduction de l'alcool** (GGT, HDL, TG, VGM) : rien trouvé avec ces requêtes ;
- **ferritine sous fer chez les sportifs** : différence standardisée seulement.

**Résultat.** Sur 25 couples intervention-marqueur, chez les 20-79 ans :
- **2 sont détectables chez une personne** :
  - 25-OH vitamine D sous supplémentation (ratio 1,8) ;
  - HbA1c sous activité physique structurée (ratio 1,3), mais chez des diabétiques de type 2,
    dont l'HbA1c baisse plus que celle de personnes en bonne santé ;
- **3 sont limites** : ALAT sous alimentation méditerranéenne (0,6), TG sous oméga-3 à 2 g/j
  (0,7), homocystéine sous acide folique (0,7) ;
- **20 ne sont visibles qu'en moyenne de groupe**, dont tous les effets de l'activité physique et
  de l'alimentation méditerranéenne sur les lipides et la glycémie (ratios de 0,06 à 0,21).

Les conclusions sont les mêmes chez les 30-55 ans.

**Prédiction 4 (qualitative)** : **en partie fausse**.
- Bien prédit :
  - vitamine D ≥ 1 ;
  - activité physique sur les lipides < 0,5.
- Mal prédit :
  - TG sous oméga-3 à 2 g/j : 0,7, et non ≥ 1 ;
  - HbA1c sous activité physique : 1,3, et non < 0,5. Mais l'effet vient de diabétiques.

## Lecture (interprétation)

1. **La plupart des interventions réalistes ne produisent pas, en moyenne, un changement
   détectable chez une personne en 6 mois.** C'est vrai même avec des seuils qui sont des bornes
   basses. Les lipides sont l'exemple le plus net : leur effet moyen représente 6 à 21 % du
   changement détectable.
2. **Les exceptions ont un point commun** : un effet direct sur le marqueur lui-même
   (supplémentation en vitamine D, acide folique) ou une population de départ très anormale
   (HbA1c de diabétiques, TG d'hyperlipidémiques).
3. **Pour une personne, un changement au-delà du seuil reste possible** si elle répond plus que la
   moyenne. Ces effets moyens ne disent rien de la dispersion des réponses individuelles.
4. **Montrer un effet moyen demande un groupe** : un groupe d'environ 100 personnes, par exemple,
   suffirait à voir des effets que personne ne peut voir seul (non calculé ici).

## Écarts et compléments au protocole

- **CV_A des marqueurs sans remesure.** Le protocole prévoyait les fiches de contrôle qualité
  NHANES, sinon la spécification EFLM. Les fiches n'ont pas été lues ; la spécification EFLM
  (0,5 × CV_I) a été utilisée pour tous.
- **Filtre de matrice ajouté** (sérum, plasma, sang total) pour le CV_I à long terme. Il ne change
  rien aux études A/B. Il écarte des études urinaires de note C, qui donnaient des CV aberrants
  pour le sodium et le potassium.
- **Sensibilité non pré-enregistrée** : CV_I à long terme avec les études de note C
  (colonne `cd6m_hausse_sens_noteC`). Elle relève les seuils, par exemple :
  - triglycérides : +125 % au lieu de +111 % ;
  - GGT : +77 % au lieu de +53 % ;
  - B12 : +69 % au lieu de +48 %.
- **Médiane de départ** pour convertir les effets en % : médiane NHANES des 30-55 ans, issue du jeu
  principal (NHANES III, ou 2001-2002 pour la CRP et la vitamine D). La vitamine D de 2001-2002 a
  été dosée avant la standardisation LC-MS/MS.

## Limites

- Remesures à 2 semaines. Une extrapolation à 6 mois n'existe que pour quelques marqueurs.
- NHANES est américain, avec des laboratoires centralisés. Les données de NHANES III datent de
  1988-1994.
- Les effets d'interventions viennent souvent de populations malades (diabète, stéatose,
  hyperlipidémie). Chez des personnes en bonne santé, ils sont probablement plus faibles.
- Plusieurs effets ne viennent que de résumés. Les essais diffèrent en durée et en dose.

## Analyse secondaire (déclarée après les résultats, à la demande de l'auteur du projet)

Trois compléments, sans nouvelle donnée NHANES. Fichier : `Q1_secondaire_moyenner.csv` ; code : `q1_secondaire.py`.

**1. Population des méta-analyses.** Elle figure pour chaque couple dans le tableau ci-dessous. Beaucoup d'effets viennent de populations malades ou à risque : diabétiques, syndrome métabolique, stéatose, obésité, hyperlipidémie. Chez des adultes en bonne santé, ils sont probablement plus petits.
- **HbA1c sous activité physique** : ratio 1,3 chez des diabétiques de type 2 (Umpierre 2011). Chez des **non-diabétiques**, rien trouvé avec ces requêtes : aucune méta-analyse d'activité physique sur l'HbA1c hors diabète. On ne peut donc pas dire si l'effet serait détectable chez une personne non diabétique.
- **Oméga-3** : sans hyperlipidémie, l'effet plafonne vers −40 mg/dL (Wang 2023, TC), soit le même ordre de grandeur que l'effet global.

**2. Deux références.**
- **Statine** (atorvastatine 10 mg/j ou équivalent) : −40 % de LDL (Law 2003, BMJ, résumé). C'est un effet **clairement détectable** chez une personne : ratio 1,25.
- **Perte de poids de 5-10 %**, d'après deux méta-analyses, sur un scénario de 7 kg :
  - lipides : Hasan 2020 (73 ECR, surpoids ou obésité, IMC moyen 36), par kg perdu après une intervention sur le mode de vie : TG −4,0 mg/dL, LDL −1,28, HDL +0,46 ;
  - ALAT : Koutoukidis 2021, −0,83 U/L par kg, chez des personnes avec stéatose.
  - L'article de Dattilo 1992, également lu, ne donne dans son résumé que la pente du HDL.
- **En appui seulement** : Magkos 2016 (Cell Metab, texte complet), un **petit essai unique** (19 personnes contre 14), chez des obèses non diabétiques. Il donne les seuls chiffres trouvés pour la glycémie, l'insuline et la CRP hors diabète. Ses effets sont estimés grossièrement, par la différence des variations des médianes.
- **Non trouvé avec ces requêtes** : une méta-analyse de l'effet d'une perte de poids sans médicament sur la glycémie, l'HbA1c ou la CRP chez des non-diabétiques. Look AHEAD (Wing 2011) ne porte que sur des diabétiques et ne donne que des rapports de cotes.

**3. Combien de mesures faudrait-il ?** Deux façons de réduire le bruit :
- **A, prélèvements rapprochés** : k prises de sang à quelques jours d'intervalle autour de chaque bilan, moyennées. Elles réduisent le bruit à court terme, mais pas la variation biologique à long terme. Si celle-ci dépasse à elle seule l'effet, c'est **impossible** ;
- **B, tendance** : m bilans espacés avant l'intervention et m après, moyennés. Tout le bruit à 6 mois se divise par m.

Hypothèses : erreurs indépendantes, effet stable dans le temps, même laboratoire. Quand le seuil est une borne basse (pas d'étude à long terme), A et B donnent le même chiffre, **optimiste**. Calcul : $k = \sigma_{obs}^2 / (\sigma^{*2} - \sigma_{LT}^2)$ et $m = \sigma_{6m}^2 / \sigma^{*2}$, avec $\sigma^* = |\ln(1+\text{effet})| / (1{,}96\sqrt2)$.

| Intervention | Marqueur | Population | Effet moyen | Ratio | **A : prises de sang par bilan** | **B : bilans avant et après** | 30-55 ans (A / B) | Source (lecture) |
|---|---|---|---|---|---|---|---|---|
| Activité physique (toutes formes) | Cholestérol total | 148 ECR, adultes | −3 % | 0,14 | **62** | **62** | 64 / 64 | Smart 2025 (R) |
| Activité physique (toutes formes) | HDL | 148 ECR, adultes | +4 % | 0,10 | **69** | **69** | 65 / 65 | Smart 2025 (R) |
| Activité physique (toutes formes) | LDL (calculé, à jeun) | 148 ECR, adultes | −6 % | 0,18 | **41** | **41** | 55 / 55 | Smart 2025 (R) |
| Activité physique (toutes formes) | Triglycérides (à jeun) | 148 ECR, adultes | −7 % | 0,13 | **> 100** | **> 100** | > 100 / > 100 | Smart 2025 (R) |
| Activité physique structurée | HbA1c | diabète de type 2 | −13 % | 1,34 | **1** | **1** | 1 / 1 | Umpierre 2011 (R) |
| Activité physique aérobie | Glycémie à jeun (plasma) | syndrome métabolique | −3 % | 0,13 | **76** | **76** | 54 / 54 | Wewege 2018 (R) |
| Activité physique (toutes formes) | Insuline (à jeun) | surpoids ou stéatose | −20 % | 0,37 | **13** | **13** | 13 / 13 | Smart 2018 (R) |
| Alimentation méditerranéenne | Glycémie à jeun (plasma) | adultes, 57 essais contrôlés | −3 % | 0,14 | **62** | **62** | 44 / 44 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Insuline (à jeun) | adultes | −10 % | 0,18 | **55** | **55** | 58 / 58 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HOMA-IR | adultes | −19 % | 0,33 | **18** | **18** | 18 / 18 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HbA1c | adultes | −3 % | 0,30 | **12** | **12** | 14 / 14 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Cholestérol total | adultes | −3 % | 0,14 | **66** | **66** | 68 / 68 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | LDL (calculé, à jeun) | adultes | −7 % | 0,21 | **31** | **31** | 42 / 42 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HDL | adultes | +3 % | 0,06 | **> 100** | **> 100** | > 100 / > 100 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Triglycérides (à jeun) | adultes | −10 % | 0,20 | **46** | **46** | 49 / 49 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | ALAT | adultes | −38 % | 0,59 | **impossible** | **5** | impossible / 5 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | GGT | adultes | −11 % | 0,31 | **14** | **14** | 14 / 14 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | CRP | adultes | −29 % | 0,37 | **21** | **21** | 23 / 23 | Papadaki 2020 (TC) |
| Perte de poids de 5 kg | ALAT | stéatose (NAFLD) | −28 % | 0,43 | **impossible** | **11** | impossible / 11 | Koutoukidis 2021 (R) |
| Perte de poids de 5 kg | ASAT | stéatose (NAFLD) | −15 % | 0,32 | **impossible** | **16** | impossible / 17 | Koutoukidis 2021 (R) |
| Perte de poids de 5 kg (poids stabilisé) | HDL | 70 études | +4 % | 0,08 | **100** | **100** | 95 / 95 | Dattilo 1992 (R) |
| Vitamine D3, 25 µg/j | 25-OH vitamine D | plus de 50 ans, sans calcium | +98 % | 1,80 | **1** | **1** | 1 / 1 | Autier 2012 (R) |
| Oméga-3 (EPA + DHA), 2 g/j | Triglycérides (à jeun) | 90 ECR, surtout hyperlipidémiques | −36 % | 0,69 | **3** | **3** | 3 / 3 | Wang 2023 (TC) |
| Acide folique 0,8 mg/j | Homocystéine | 25 ECR | −23 % | 0,73 | **3** | **3** | 2 / 2 | Homocysteine Lowering Trialists' Collaboration 2005 (R) |
| Fer oral (femmes réglées) | Hémoglobine | femmes réglées | +4 % | 0,37 | **impossible** | **7** | impossible / 7 | Low 2016 (R) |
| Statine (atorvastatine 10 mg/j ou équivalent) | LDL (calculé, à jeun) | 164 essais contre placebo | −40 % | 1,25 | **1** | **1** | 1 / 1 | Law 2003 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | Triglycérides (à jeun) | 73 ECR, surpoids ou obésité (IMC moyen 36) | −24 % | 0,45 | **8** | **8** | 8 / 8 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | LDL (calculé, à jeun) | 73 ECR, surpoids ou obésité | −7 % | 0,23 | **26** | **26** | 36 / 36 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | HDL | 73 ECR, surpoids ou obésité | +7 % | 0,16 | **30** | **30** | 29 / 29 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | ALAT | stéatose (NAFLD) | −39 % | 0,60 | **impossible** | **5** | impossible / 5 | Koutoukidis 2021 (R) |
| Perte de poids de 5 % (essai unique, petite taille) | Glycémie à jeun (plasma) | obèses non diabétiques, n = 19 contre 14 | −4 % | 0,18 | **38** | **38** | 27 / 27 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | Insuline (à jeun) | obèses non diabétiques | −14 % | 0,25 | **28** | **28** | 30 / 30 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | Triglycérides (à jeun) | obèses non diabétiques | −38 % | 0,72 | **3** | **3** | 3 / 3 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | HDL | obèses non diabétiques | +0 % | 0,01 | **> 100** | **> 100** | > 100 / > 100 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | ALAT | obèses non diabétiques | −17 % | 0,26 | **impossible** | **33** | impossible / 34 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | CRP | obèses non diabétiques | +5 % | 0,01 | **> 100** | **> 100** | > 100 / > 100 | Magkos 2016 (TC) |

**Lecture pratique** (interprétation) :
- **Une seule mesure suffit** quand l'effet est direct et fort : vitamine D sous supplémentation, LDL sous statine, et HbA1c chez des diabétiques.
- **Environ 3 à 8 mesures de part et d'autre** pour les TG sous oméga-3 ou sous perte de poids, et pour l'homocystéine sous acide folique.
- **Des dizaines de mesures** pour les lipides et la glycémie sous activité physique, alimentation ou perte de poids modérée : en pratique, ce n'est jamais faisable pour une personne.
- **Impossible par des prélèvements rapprochés** pour l'ALAT et l'hémoglobine : la variation à long terme dépasse déjà l'effet. Seule une tendance sur plusieurs bilans peut alors le montrer.
- Ces nombres supposent le même laboratoire. Un changement de laboratoire (Q5) les augmente.
