# Q6 : zones fondées sur le risque de mortalité

Programme « panel ». Protocole pré-enregistré dans `DECISIONS.md` (commit `705e3d7`).

Code :
- `src/aging_clock/panel/q6.py` : données et méthodes ;
- `src/aging_clock/panel/q6_modele.py` : Cox, courbes et seuils ;
- `src/aging_clock/panel/q6_analyse.py` : analyses.

Données :
- `Q6_marqueurs.csv`, `Q6_methodes.json` ;
- `Q6_zones.csv`, `Q6_categories.csv` ;
- `Q6_courbes.csv` : HR et IC sur la grille, références minimum et médiane ; développement,
  validation, sexes et tranches d'âge ;
- `Q6_causes.csv`, `Q6_ages.csv`, `Q6_sensibilites.csv` ;
- `Q6_predictions.json`, `Q6_resultats_bruts.json`.

Une figure par marqueur dans `figures_q6/`.

**Question.** Pour chaque marqueur, comment le risque de mortalité varie-t-il selon sa valeur ? Cette
relation correspond-elle aux bornes usuelles (D1) ?

## À lire avant les chiffres

- **Une zone décrit un risque associé, pas une cible.** Rien ici ne dit qu'amener un marqueur dans la
  zone de risque minimal réduit le risque. Un marqueur bas ou haut peut être la conséquence d'une
  maladie (causalité inverse), ou le témoin d'autre chose (confusion).
- **Données.** NHANES 1999-2010, américain, adultes de 20 à 79 ans.
  - Mortalité à **10 ans** : 1 842 décès en développement (1999-2006) et 1 117 en validation
    (2007-2010).
  - Méthodes de laboratoire harmonisées vers celles de 2009-2010 (règle de Q5, `Q6_methodes.json`).
- **Lecture d'une courbe.**
  - HR par rapport au **point de risque minimal**, cherché entre les centiles 5 et 95.
  - Les **seuils de risque** sont les valeurs où le HR atteint 1,2 (puis 1,5), de chaque côté du
    minimum.
  - **Un HR de 1,2 est une barre basse** : 20 % de risque relatif en plus à âge et sexe égaux.
- **Réplication.** Un côté de risque n'est retenu que s'il existe aussi en validation. Une valeur de
  seuil n'est retenue (✓) que si le seuil de validation tombe dans l'IC bootstrap du développement
  (500 tirages).
- **Bornes D1.** Elles sont de deux sortes :
  - S : convention statistique (2,5e-97,5e centiles d'une population de référence) ;
  - R : seuil clinique fondé sur le risque.

  On ne s'attend pas à ce qu'un intervalle S coïncide avec un seuil de risque. La comparaison dit
  seulement où il s'en écarte.
- **Changement détectable.** Ceux de Q1 sont des bornes basses (remesures à environ 2 semaines).
  Une mesure unique est bruitée, ce qui aplatit les courbes : les seuils réels sont probablement plus
  proches du minimum que ceux estimés ici.

## Ce qu'il faut retenir

1. **La plupart des marqueurs ont une relation en U ou en J avec la mortalité, répliquée en
   validation.** Sur 68 marqueurs testables, après réplication :
   - 37 sont en U ou en J ;
   - 14 sont montants ;
   - 11 sont descendants ;
   - 6 ne sont pas répliqués : basophiles (% et nombre), VPM, triglycérides à jeun et sériques,
     TG/HDL.

   « Plus c'est bas, mieux c'est » (ou l'inverse) est l'exception, pas la règle.
2. **Les intervalles statistiques D1 sont souvent plus larges que la zone de risque.** On a comparé
   les bornes D1 (par sexe et par côté) aux seuils HR 1,2 répliqués. Sur 179 comparaisons :
   - 90 sont « trop larges » : des valeurs jugées normales sont déjà associées à un HR ≥ 1,2 ;
   - 42 sont « trop strictes » ;
   - 22 sont « conformes » ;
   - 22 sont « non estimables » ;
   - 3 sont des relations en U non signalées.

   Exemples d'écart entre le seuil de risque (HR 1,2) et la borne D1 :

   | Marqueur | Seuil de risque (HR 1,2) | Borne D1 |
   |---|---|---|
   | Leucocytes | au-dessus de 8,1 G/L | 10,6 G/L (hommes), 10,3 G/L (femmes) |
   | RDW | au-dessus de 12,4 % | 14,1 % (hommes), 16,5 % (femmes) |
   | GGT | au-dessus de 31 U/L | 108 U/L (hommes), 67 U/L (femmes) |
   | PAL | au-dessus de 69 U/L | 112 U/L |
   | CRP | au-dessus de 2,4 mg/L | environ 11 mg/L |
   | Albumine | en dessous de 4,55 g/dL | 3,9 g/dL (hommes), 3,7 g/dL (femmes) |
   | HDL | en dessous de 43 mg/dL et au-dessus de 71 mg/dL | intervalle 29-82 mg/dL (hommes), 36-97 mg/dL (femmes) |
   | ALAT | en dessous de 19 U/L et au-dessus de 45 U/L | intervalle 15-75 U/L (hommes) |

   C'est attendu : un intervalle statistique décrit une population, pas un risque. Ces écarts
   chiffrent ce qu'un intervalle de laboratoire ne dit pas.
3. **Seuils cliniques (R).**
   - **Conformes** : glycémie à jeun ≥ 110 mg/dL (OMS), HbA1c ≥ 5,7 et 6,0 %, vitamine D
     < 50 nmol/L (20 ng/mL).
   - **Trop stricts** pour la mortalité :
     - glycémie à jeun ≥ 100 mg/dL (ADA) ;
     - LDL ≥ 116 mg/dL : pas de côté haut répliqué ;
     - non-HDL ≥ 130 mg/dL : le risque ne monte qu'au-dessus de 205 mg/dL ;
     - TG ≥ 150 mg/dL : pas d'association répliquée ;
     - vitamine D < 75 nmol/L.
     Ces seuils visent l'événement cardiovasculaire ou le diabète, pas la mortalité toutes causes à
     10 ans (voir les causes plus bas).
   - **Trop large** : RAC ≥ 30 mg/g. Le risque monte dès 4,7 mg/g, comme dans la méta-analyse
     CKD-PC lue (dès 10 mg/g).
   - **Relations en U non signalées** par un seuil R d'un seul côté :
     - DFGe : risque aussi au-dessus de 101 mL/min/1,73 m², en plus de sous 66 ;
     - HbA1c : risque aussi sous 4,9 % ;
     - non-HDL : risque aussi sous 124 mg/dL.
4. **Causalité inverse.** Exclure les décès des 3 premières années fait disparaître plusieurs côtés
   de risque :
   - le côté bas des leucocytes, des neutrophiles (% et nombre), de la CRP, du phosphore et du
     calcium corrigé ;
   - le côté haut de la bilirubine, du chlorure et des bicarbonates.

   Ces côtés reflètent probablement des maladies déjà présentes à l'examen : ce sont des **marqueurs
   de maladie** plutôt que des facteurs de risque.
5. **Prédictions tirées de la littérature : 17 sur 34 vérifiées.**
   - **Vérifiées** :
     - GGT, PAL, RAC, RDW et phosphore montants ;
     - albumine, CCMH, bicarbonates et vitamine D descendantes ;
     - HDL, cholestérol total, VGM, TCMH, acide urique et HbA1c en U ;
     - TG à jeun plats ;
     - NLR montant.
   - **Non vérifiées, avec un côté de plus que prévu** : ALAT, bilirubine, leucocytes, lymphocytes,
     potassium, chlorure, DFGe, CRP, urée, HOMA-IR, FIB-4, insuline. Leur relation est en U alors
     que les sources décrivaient un seul côté, ou aucun pour l'insuline.
   - **Non vérifiées, avec un côté de moins** :
     - sodium : seul le côté bas est répliqué ;
     - glycémie à jeun, LDL, urée/créatinine : un côté au lieu de deux ;
     - TG sériques : aucun côté répliqué.
6. **Âge et sexe.**
   - L'interaction avec l'âge est répliquée (p < 0,05 dans les deux périodes) pour :
     - le rein : créatinine, urée, DFGe, RAC ;
     - l'albumine et les globulines ;
     - le foie : GGT, FIB-4, ASAT/ALAT ;
     - VGM, TCMH, chlorure, calcium corrigé.
   - L'interaction avec le sexe est répliquée pour les hématies, l'hémoglobine, l'hématocrite, le
     HDL, la créatinine et l'acide urique. Pour ces marqueurs, les catégories du modèle commun sont
     moins fiables (courbes par sexe dans `Q6_courbes.csv`).

## Zones et seuils, par marqueur

Sens des colonnes :
- **Minimum** : point de risque minimal, cherché entre les centiles 5 et 95. « (borne) » veut dire
  que le minimum tombe sur le 5e ou le 95e centile : le risque continue probablement de baisser
  au-delà (formes montantes ou descendantes).
- **Zone de risque minimal** : valeurs où la borne basse de l'IC du HR reste sous 1,1.
- **Seuils** : estimation de développement [IC 95 % bootstrap, 500 tirages], puis seuil de validation
  entre parenthèses. ✓ = valeur de seuil retenue (le seuil de validation tombe dans l'IC).
- **Retenu en validation** : forme qui découle des côtés de risque retenus.

Unités NHANES (mg/dL pour la plupart des marqueurs biochimiques). La CRP est en mg/dL : 0,235 mg/dL =
2,35 mg/L.

| Marqueur | Décès dév. / val. | Minimum (P5-P95) | Zone de risque minimal | Seuil HR 1,2 bas [IC] (val.) | Seuil HR 1,2 haut [IC] (val.) | Forme dév. / val. | Retenu en validation |
|---|---|---|---|---|---|---|---|
| Leucocytes (G/L) | 1705 / 1016 | 6,06 | 3,4–8,26 | 4,14 [3,49 ; 4,75] (4,74) ✓ | 8,1 [7,42 ; 8,7] (7,23) | en J / en U | en U ou en J (bas, haut) |
| Neutrophiles (%) | 1691 / 1011 | 57,5 | 33,4–64,3 | 40,2 [35,3 ; 48,3] (—) | 64,9 [62,7 ; 66] (61,3) | en J / montante | montante (haut) |
| Neutrophiles (G/L) | 1691 / 1011 | 3,25 | 1,45–4,95 | 1,84 [1,53 ; 2,29] (2,22) ✓ | 4,81 [4,26 ; 5,28] (4,1) | en J / en U | en U ou en J (bas, haut) |
| Lymphocytes (%) | 1691 / 1011 | 33,5 | 24,4–52,8 | 25,2 [22,8 ; 27,7] (26,4) ✓ | 46,2 [41,1 ; 51,8] (—) | en J / descendante | descendante (bas) |
| Lymphocytes (G/L) | 1691 / 1011 | 2,01 | 1,45–2,88 | 1,43 [1,34 ; 1,6] (1,42) ✓ | 2,9 [2,59 ; 3,27] (3,19) ✓ | en U / en J | en U ou en J (bas, haut) |
| Monocytes (%) | 1691 / 1011 | 7,83 | 5,72–10,5 | 5,74 [5,34 ; 6,39] (6,89) | 10,7 [9,75 ; 12] (11,2) ✓ | en U / en U | en U ou en J (bas, haut) |
| Monocytes (G/L) | 1691 / 1011 | 0,466 | 0,243–0,68 | 0,312 [0,251 ; 0,353] (0,331) ✓ | 0,66 [0,583 ; 0,731] (0,7) ✓ | en J / en U | en U ou en J (bas, haut) |
| Éosinophiles (%) | 1691 / 1011 | 2,38 | 1,47–10,5 | 1,36 [1,15 ; 1,56] (1,32) ✓ | 8,48 [3,67 ; 10,1] (—) | en J / descendante | descendante (bas) |
| Éosinophiles (G/L) | 1691 / 1011 | 0,148 | 0,0796–0,354 | 0,079 [0,0461 ; 0,0935] (0,0779) ✓ | 0,298 [0,231 ; 0,549] (0,284) ✓ | en U / en J | en U ou en J (bas, haut) |
| Basophiles (%) | 1691 / 1011 | 0,54 | 0,163–2,5 | 0,207 [0,0473 ; 0,291] (0,228) | 1,33 [0,843 ; 2,15] (—) | en U / descendante | non répliquée |
| Basophiles (G/L) | 1691 / 1011 | 0,0325 | 0,00985–0,0621 | 0,0133 [0,00326 ; 0,0185] (0,00936) | 0,0587 [0,05 ; 0,0868] (0,124) | en J / en U | non répliquée |
| Hématies (T/L) | 1705 / 1016 | 4,99 | 4,38–5,89 | 4,44 [4,31 ; 4,64] (4,27) | — | descendante / descendante | descendante (bas) |
| Hémoglobine (g/dL) | 1705 / 1016 | 15,2 | 14–17,5 | 14 [13,5 ; 14,3] (13,4) | 16,8 [16,2 ; 17,4] (17,3) ✓ | en J / en J | en U ou en J (bas, haut) |
| Hématocrite (%) | 1705 / 1016 | 44,7 | 40–51,7 | 40,5 [39,1 ; 41,7] (38,4) | 50,7 [48 ; 51,5] (49) ✓ | en J / en J | en U ou en J (bas, haut) |
| VGM (fL) | 1705 / 1016 | 91,8 | 86,1–94,3 | 86,9 [82,2 ; 88,8] (81,7) | 95 [94,7 ; 95,5] (95,1) ✓ | en U / en U | en U ou en J (bas, haut) |
| TCMH (pg) | 1705 / 1016 | 31,3 | 29,7–32,2 | 29,7 [28,7 ; 30,2] (29,4) ✓ | 32,4 [32,3 ; 32,6] (33,1) | en U / en U | en U ou en J (bas, haut) |
| CCMH (g/dL) | 1705 / 1016 | 34,1 | 32,9–35,6 | 33,1 [32,7 ; 33,5] (34,3) | 35,1 [34,8 ; 35,5] (—) | en J / descendante | descendante (bas) |
| RDW (%) | 1705 / 1016 | 11,6 (borne) | 11,3–12,6 | — | 12,4 [12 ; 12,6] (12) | montante / montante | montante (haut) |
| Plaquettes (G/L) | 1705 / 1016 | 232 | 196–291 | 188 [180 ; 195] (190) ✓ | 286 [267 ; 330] (294) ✓ | en U / en U | en U ou en J (bas, haut) |
| VPM (fL) | 1705 / 1016 | 8,2 | 6,62–10,7 | 6,99 [6,52 ; 7,42] (6,7) | 9,99 [9,17 ; 10,6] (9,47) | en U / en U | non répliquée |
| Glycémie à jeun (mg/dL) | 707 / 452 | 98,6 | 91–137 | 90,6 [88,5 ; 92,7] (—) | 122 [107 ; 148] (118) ✓ | en U / montante | montante (haut) |
| Glycémie sérique (mg/dL) | 1659 / 1003 | 89,4 | 80,8–116 | 79,6 [77,3 ; 81,1] (—) | 112 [101 ; 126] (122) ✓ | en U / montante | montante (haut) |
| Insuline à jeun (µU/mL) | 692 / 445 | 10,2 | 4,79–17,1 | 5,4 [3,86 ; 7,4] (5,03) ✓ | 17,2 [14 ; 19,1] (16,7) ✓ | en U / en U | en U ou en J (bas, haut) |
| HbA1c (%) | 1699 / 1014 | 5,26 | 4,94–6,06 | 4,94 [4,81 ; 5] (4,99) ✓ | 5,94 [5,66 ; 6,49] (6,26) ✓ | en U / en U | en U ou en J (bas, haut) |
| Cholestérol total (mg/dL) | 1657 / 1004 | 204 | 166–266 | 166 [160 ; 177] (165) ✓ | 261 [245 ; 293] (284) ✓ | en U / en J | en U ou en J (bas, haut) |
| LDL (mg/dL) | 691 / 445 | 148 | 98,3–218 | 112 [89,1 ; 127] (83,2) | 204 [174 ; 215] (—) | en J / descendante | descendante (bas) |
| HDL (mg/dL) | 1657 / 1004 | 55,6 | 41,2–69,6 | 42,7 [37,4 ; 46,5] (44,7) ✓ | 70,8 [67,5 ; 76,9] (77,6) | en U / en U | en U ou en J (bas, haut) |
| Triglycérides à jeun (mg/dL) | 691 / 445 | 155 | 39–604 | 55 [43,1 ; 111] (49,4) | 318 [202 ; 518] (243) | en J / en J | non répliquée |
| Triglycérides sériques (mg/dL) | 1658 / 1002 | 128 | 35–267 | 49,7 [37,4 ; 74,4] (—) | 269 [210 ; 349] (—) | en J / plate | non répliquée |
| Cholestérol non-HDL (mg/dL) | 1657 / 1004 | 160 | 122–203 | 124 [113 ; 135] (106) | 205 [195 ; 228] (234) | en U / en J | en U ou en J (bas, haut) |
| ALAT (U/L) | 1653 / 1002 | 28,3 | 18,1–44 | 18,8 [16,7 ; 21,5] (19,1) ✓ | 45,1 [40,5 ; 54,7] (39) | en U / en U | en U ou en J (bas, haut) |
| ASAT (U/L) | 1653 / 1002 | 25,1 | 18,8–33,5 | 18,8 [17,7 ; 20,2] (20,5) | 34,6 [31,6 ; 36,5] (34,7) ✓ | en U / en U | en U ou en J (bas, haut) |
| GGT (U/L) | 1659 / 1003 | 16 | 7–33,6 | — | 31,2 [24 ; 39,1] (35,1) ✓ | montante / montante | montante (haut) |
| PAL (U/L) | 799 / 1002 | 41,2 (borne) | 33–81,9 | — | 69,2 [48,4 ; 83,8] (70,9) ✓ | montante / montante | montante (haut) |
| Bilirubine totale (mg/dL) | 797 / 1002 | 0,941 | 0,706–1,8 | 0,712 [0,645 ; 0,778] (0,639) | 1,41 [1,16 ; 1,73] (1,32) ✓ | en J / en J | en U ou en J (bas, haut) |
| Albumine (g/dL) | 1659 / 1003 | 4,8 (borne) | 4,18–5,1 | 4,55 [4,08 ; 4,68] (4,44) ✓ | — | descendante / descendante | descendante (bas) |
| Protéines totales (g/dL) | 1657 / 1003 | 7,15 | 6,74–7,66 | 6,71 [6,56 ; 6,8] (6,59) ✓ | 7,61 [7,46 ; 7,8] (7,66) ✓ | en U / en J | en U ou en J (bas, haut) |
| Globulines (g/dL) | 1657 / 1003 | 2,61 | 2,1–3,2 | — | 3,16 [2,91 ; 3,31] (2,76) | montante / montante | montante (haut) |
| Créatinine (mg/dL) | 1659 / 1003 | 0,872 | 0,66–1,09 | 0,669 [0,599 ; 0,736] (—) | 1,09 [1,01 ; 1,14] (1,12) ✓ | en U / montante | montante (haut) |
| Urée (mg/dL) | 1659 / 1002 | 14,4 | 11,5–17,3 | 11,4 [10,3 ; 12,1] (11,8) ✓ | 18 [17,5 ; 18,5] (18,4) ✓ | en U / en U | en U ou en J (bas, haut) |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | 1659 / 1003 | 82,7 | 68,7–102 | 66,4 [64,5 ; 69,9] (69,3) ✓ | 101 [95 ; 108] (106) ✓ | en U / en U | en U ou en J (bas, haut) |
| RAC urinaire (mg/g) | 1704 / 1044 | 2,49 (borne) | 1,13–5,87 | — | 4,67 [3,44 ; 6,8] (6,36) ✓ | montante / montante | montante (haut) |
| Sodium (mmol/L) | 1659 / 1002 | 140 | 137–144 | 137 [136 ; 138] (138) | — | descendante / en J | descendante (bas) |
| Potassium (mmol/L) | 1659 / 1002 | 3,94 | 3,6–4,31 | 3,59 [3,41 ; 3,68] (3,35) | 4,31 [4,17 ; 4,39] (4,15) | en U / en J | en U ou en J (bas, haut) |
| Chlorure (mmol/L) | 1659 / 1002 | 104 | 101–109 | 101 [100 ; 102] (102) | 108 [106 ; 109] (107) ✓ | en J / en J | en U ou en J (bas, haut) |
| Bicarbonates (mmol/L) | 1653 / 1002 | 24,9 | 22,3–29 | 22,5 [21,9 ; 23,3] (23,5) | 28,3 [27,1 ; 28,9] (—) | en J / descendante | descendante (bas) |
| Calcium (mg/dL) | 1659 / 1002 | 9,37 | 9,04–10,5 | 9,01 [8,91 ; 9,09] (9,06) ✓ | 10,1 [9,68 ; 10,4] (10,2) ✓ | en J / en J | en U ou en J (bas, haut) |
| Phosphore (mg/dL) | 1659 / 1003 | 3,68 | 2,5–4,19 | 2,63 [2,53 ; 3,12] (—) | 4,22 [4,04 ; 4,33] (4,21) ✓ | en J / montante | montante (haut) |
| Osmolalité calculée (mOsm/kg) | 1658 / 1002 | 290 | 285–293 | 285 [283 ; 287] (287) | 294 [293 ; 295] (294) ✓ | en U / en U | en U ou en J (bas, haut) |
| CRP (mg/dL) | 1673 / 1011 | 0,0817 | 0,01–0,227 | 0,0216 [0,0109 ; 0,0369] (0,0105) | 0,235 [0,181 ; 0,31] (0,243) ✓ | en J / en J | en U ou en J (bas, haut) |
| Acide urique (mg/dL) | 1659 / 1002 | 5,69 | 4,18–6,56 | 4,34 [3,7 ; 4,85] (2,89) | 6,75 [6,55 ; 6,91] (6,82) ✓ | en U / en J | en U ou en J (bas, haut) |
| Fer sérique (µg/dL) | 1657 / 1002 | 101 | 74,3–156 | 73,5 [65,1 ; 78,8] (75,9) ✓ | 143 [130 ; 179] (134) ✓ | en U / en U | en U ou en J (bas, haut) |
| Folates érythrocytaires (nmol/L) | 1665 / 1010 | 1,27e+03 | 810–1,84e+03 | 828 [728 ; 958] (941) ✓ | 1,93e+03 [1,75e+03 ; 2,19e+03] (1,91e+03) ✓ | en U / en U | en U ou en J (bas, haut) |
| Vitamine D 25-OH (nmol/L) | 1238 / 931 | 69,8 | 48,5–118 | 49,7 [43,8 ; 56,8] (51,7) ✓ | 117 [86,7 ; 116] (—) | en J / descendante | descendante (bas) |
| HOMA-IR | 692 / 445 | 2,76 | 1,16–4,82 | 1,35 [0,968 ; 1,88] (1,05) ✓ | 4,9 [3,92 ; 5,5] (3,96) ✓ | en U / en U | en U ou en J (bas, haut) |
| QUICKI | 692 / 445 | 0,328 | 0,306–0,374 | 0,304 [0,3 ; 0,311] (0,312) | 0,363 [0,346 ; 0,385] (0,382) ✓ | en U / en U | en U ou en J (bas, haut) |
| Indice TyG | 691 / 445 | 8,96 | 7,51–9,71 | 8,16 [7,72 ; 8,6] (—) | 9,66 [9,23 ; 10] (9,42) ✓ | en U / montante | montante (haut) |
| LDL/HDL | 691 / 445 | 2,92 | 1,6–5,65 | 1,81 [1,49 ; 2,33] (1,43) | 4,54 [3,53 ; 5,46] (3,2) | en J / en U | en U ou en J (bas, haut) |
| TG/HDL | 691 / 445 | 2,92 | 0,544–18,5 | 0,851 [0,602 ; 2,05] (—) | 8,19 [4,36 ; 14,6] (5,1) | en J / montante | non répliquée |
| Albumine/globulines | 1657 / 1003 | 1,88 (borne) | 1,38–2,14 | 1,48 [1,33 ; 1,71] (1,64) ✓ | — | descendante / descendante | descendante (bas) |
| FIB-4 | 1652 / 1000 | 1,09 | 0,646–1,54 | 0,723 [0,553 ; 0,841] (0,766) ✓ | 1,62 [1,44 ; 1,76] (1,7) ✓ | en U / en U | en U ou en J (bas, haut) |
| GGT/HDL | 1654 / 1003 | 0,16 (borne) | 0,11–0,797 | — | 0,634 [0,275 ; 0,868] (0,586) ✓ | montante / montante | montante (haut) |
| ASAT/ALAT | 1653 / 1002 | 0,721 | 0,491–1,2 | — | 1,14 [0,818 ; 1,26] (1,16) ✓ | montante / en J | montante (haut) |
| Urée/créatinine | 1659 / 1002 | 15,5 | 10,7–30 | 10,8 [10 ; 12,1] (12) ✓ | 25 [21,1 ; 29,2] (—) | en J / descendante | descendante (bas) |
| Osmolalité effective (mOsm/kg) | 1658 / 1002 | 283 | 279–291 | 278 [278 ; 280] (282) | 290 [287 ; 293] (289) ✓ | en J / en U | en U ou en J (bas, haut) |
| Calcium corrigé (mg/dL) | 1659 / 1002 | 8,95 | 8,34–9,26 | 8,49 [8,36 ; 8,7] (8,65) ✓ | 9,27 [9,19 ; 9,37] (9,27) ✓ | en J / en U | en U ou en J (bas, haut) |
| Neutrophiles/lymphocytes | 1691 / 1011 | 1,63 | 0,648–2,71 | 0,874 [0,675 ; 1,1] (—) | 2,61 [2,25 ; 2,91] (2,34) ✓ | en J / montante | montante (haut) |
| Indice SII | 1691 / 1011 | 429 | 245–713 | 243 [179 ; 279] (219) ✓ | 701 [595 ; 790] (568) | en U / en U | en U ou en J (bas, haut) |
| Vitamine B12 (pg/mL) | 1665 / — | 465 | 214–998 | 237 [181 ; 298] (—) | 966 [717 ; 1,4e+03] (—) | en J / — | non répliquée (pas de validation) |
| Homocystéine (µmol/L) | 1251 / — | 6,42 | 4,12–8,76 | — | 8,48 [6,26 ; 9,57] (—) | montante / — | non répliquée (pas de validation) |

## Comparaison aux bornes D1

Bornes D1 utilisées : intervalles S par sexe, tranche 40-59 ans quand D1 a partitionné par âge ; seuils
R dans le sens du seuil. Seuls comptent les seuils HR 1,2 retenus en validation.

Sens des catégories :
- **conforme** : la borne D1 tombe dans l'IC 95 % du seuil HR 1,2 ;
- **trop large** : le seuil HR 1,2 est, avec son IC, du côté normal de la borne. Des valeurs jugées
  normales sont déjà associées à un HR ≥ 1,2 ;
- **trop strict** : le seuil est, avec son IC, au-delà de la borne, ou il n'y a pas de côté de risque
  retenu. Des valeurs signalées anormales n'ont pas de HR ≥ 1,2 ;
- **non estimable** : borne hors des centiles 1 à 99, marqueur sans validation, ou méthode différente
  de D1 (folates érythrocytaires, osmolalité).

| Marqueur | Borne D1 | Côté bas | Côté haut |
|---|---|---|---|
| Leucocytes (G/L) | S, hommes | conforme (borne 3,8) | trop large (borne 10,6) |
| Leucocytes (G/L) | S, femmes | conforme (borne 3,59) | trop large (borne 10,3) |
| Neutrophiles (%) | S, hommes | trop strict (borne 38,8) | trop large (borne 74,1) |
| Neutrophiles (%) | S, femmes | trop strict (borne 37) | trop large (borne 74,1) |
| Lymphocytes (%) | S, hommes | trop large (borne 16,9) | trop strict (borne 47,5) |
| Lymphocytes (%) | S, femmes | trop large (borne 17,3) | trop strict (borne 49,5) |
| Monocytes (%) | S, hommes | trop large (borne 4,6) | trop large (borne 13,4) |
| Monocytes (%) | S, femmes | trop large (borne 4,1) | conforme (borne 11,9) |
| Éosinophiles (%) | S, hommes | trop large (borne 0,6) | trop strict (borne 8,92) |
| Éosinophiles (%) | S, femmes | trop large (borne 0,6) | trop strict (borne 7,9) |
| Basophiles (%) | S, hommes | trop strict (borne 0,1) | trop strict (borne 1,92) |
| Basophiles (%) | S, femmes | trop strict (borne 0,1) | trop strict (borne 1,8) |
| Hématies (T/L) | S, hommes | trop large (borne 4,25) | trop strict (borne 5,75) |
| Hématies (T/L) | S, femmes | trop large (borne 3,76) | trop strict (borne 5,14) |
| Hémoglobine (g/dL) | S, hommes | trop large (borne 13,3) | conforme (borne 17,1) |
| Hémoglobine (g/dL) | S, femmes | trop large (borne 10,4) | trop strict (borne 15,2) |
| Hématocrite (%) | S, hommes | trop large (borne 38,9) | conforme (borne 50,4) |
| Hématocrite (%) | S, femmes | trop large (borne 31,5) | trop strict (borne 45) |
| VGM (fL) | S, hommes | trop large (borne 80,4) | trop large (borne 98,2) |
| VGM (fL) | S, femmes | trop large (borne 73,9) | trop large (borne 97,5) |
| TCMH (pg) | S, hommes | trop large (borne 26,6) | trop large (borne 33,8) |
| TCMH (pg) | S, femmes | trop large (borne 23,6) | trop large (borne 33,8) |
| CCMH (g/dL) | S, hommes | trop large (borne 32,3) | non estimable (borne 35,8) |
| CCMH (g/dL) | S, femmes | trop large (borne 31,9) | non estimable (borne 35,8) |
| RDW (%) | S, hommes | trop strict (borne 11,5) | trop large (borne 14,1) |
| RDW (%) | S, femmes | trop strict (borne 11,4) | trop large (borne 16,5) |
| Plaquettes (G/L) | S, hommes | trop large (borne 150) | trop large (borne 369) |
| Plaquettes (G/L) | S, femmes | trop large (borne 164) | trop large (borne 415) |
| VPM (fL) | S, hommes | non estimable (borne 6,35) | trop strict (borne 9,8) |
| VPM (fL) | S, femmes | trop strict (borne 6,4) | trop strict (borne 10) |
| Glycémie à jeun (mg/dL) | R OMS |  | conforme (borne 110) |
| Glycémie à jeun (mg/dL) | R ADA |  | trop strict (borne 100) |
| Insuline à jeun (µU/mL) | S, hommes | trop large (borne 2,25) | trop large (borne 28,4) |
| Insuline à jeun (µU/mL) | S, femmes | trop large (borne 2,22) | trop large (borne 23,5) |
| HbA1c (%) | R OMS |  | conforme (borne 6) |
| HbA1c (%) | R ADA |  | conforme (borne 5,7) |
| HbA1c (%) | R (ensemble) | **U non signalée** : risque des deux côtés, seuil R d'un seul côté | |
| Cholestérol total (mg/dL) | S, hommes | trop large (borne 149) | conforme (borne 289) |
| Cholestérol total (mg/dL) | S, femmes | trop large (borne 140) | conforme (borne 287) |
| LDL (mg/dL) | R |  | trop strict (borne 116) |
| HDL (mg/dL) | S, hommes | trop large (borne 28,9) | trop large (borne 82) |
| HDL (mg/dL) | S, femmes | trop large (borne 36) | trop large (borne 97) |
| Triglycérides à jeun (mg/dL) | R |  | trop strict (borne 150) |
| Triglycérides sériques (mg/dL) | R |  | trop strict (borne 150) |
| Cholestérol non-HDL (mg/dL) | R |  | trop strict (borne 130) |
| Cholestérol non-HDL (mg/dL) | R (ensemble) | **U non signalée** : risque des deux côtés, seuil R d'un seul côté | |
| ALAT (U/L) | S, hommes | trop large (borne 15) | trop large (borne 74,6) |
| ALAT (U/L) | S, femmes | trop large (borne 10,9) | conforme (borne 49) |
| ASAT (U/L) | S, hommes | trop large (borne 17) | trop large (borne 57,6) |
| ASAT (U/L) | S, femmes | trop large (borne 15) | trop large (borne 40) |
| GGT (U/L) | S, hommes | trop strict (borne 9) | trop large (borne 108) |
| GGT (U/L) | S, femmes | trop strict (borne 7) | trop large (borne 67,1) |
| PAL (U/L) | S, hommes | trop strict (borne 38) | trop large (borne 112) |
| PAL (U/L) | S, femmes | trop strict (borne 33) | trop large (borne 112) |
| Bilirubine totale (mg/dL) | S, hommes | trop large (borne 0,4) | conforme (borne 1,7) |
| Bilirubine totale (mg/dL) | S, femmes | trop large (borne 0,3) | conforme (borne 1,3) |
| Albumine (g/dL) | S, hommes | trop large (borne 3,9) | trop strict (borne 4,9) |
| Albumine (g/dL) | S, femmes | trop large (borne 3,7) | trop strict (borne 4,7) |
| Protéines totales (g/dL) | S, hommes | trop large (borne 6,5) | trop large (borne 8,1) |
| Protéines totales (g/dL) | S, femmes | trop large (borne 6,4) | trop large (borne 8,1) |
| Globulines (g/dL) | S, hommes | trop strict (borne 2,2) | trop large (borne 3,7) |
| Globulines (g/dL) | S, femmes | trop strict (borne 2,2) | trop large (borne 3,8) |
| Créatinine (mg/dL) | S, hommes | trop strict (borne 0,7) | trop large (borne 1,32) |
| Créatinine (mg/dL) | S, femmes | trop strict (borne 0,5) | conforme (borne 1,02) |
| Urée (mg/dL) | S, hommes | trop large (borne 7) | trop large (borne 21) |
| Urée (mg/dL) | S, femmes | trop large (borne 6) | trop large (borne 19) |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | R | trop large (borne 60) |  |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | R (ensemble) | **U non signalée** : risque des deux côtés, seuil R d'un seul côté | |
| RAC urinaire (mg/g) | R |  | trop large (borne 30) |
| Sodium (mmol/L) | S, hommes | trop large (borne 135) | trop strict (borne 143) |
| Sodium (mmol/L) | S, femmes | trop large (borne 135) | trop strict (borne 143) |
| Potassium (mmol/L) | S, hommes | trop large (borne 3,4) | trop large (borne 4,6) |
| Potassium (mmol/L) | S, femmes | trop large (borne 3,4) | trop large (borne 4,5) |
| Chlorure (mmol/L) | S, hommes | trop large (borne 99) | conforme (borne 108) |
| Chlorure (mmol/L) | S, femmes | trop large (borne 100) | non estimable (borne 109) |
| Bicarbonates (mmol/L) | S, hommes | conforme (borne 22) | trop strict (borne 29) |
| Bicarbonates (mmol/L) | S, femmes | trop large (borne 21) | trop strict (borne 29) |
| Calcium (mg/dL) | S, hommes | trop large (borne 8,8) | conforme (borne 10,1) |
| Calcium (mg/dL) | S, femmes | trop large (borne 8,8) | conforme (borne 10,1) |
| Phosphore (mg/dL) | S, hommes | trop strict (borne 2,7) | trop large (borne 4,7) |
| Phosphore (mg/dL) | S, femmes | trop strict (borne 2,9) | trop large (borne 4,9) |
| Osmolalité calculée (mOsm/kg) | S, hommes | non estimable (borne 270) | non estimable (borne 287) |
| Osmolalité calculée (mOsm/kg) | S, femmes | non estimable (borne 269) | non estimable (borne 284) |
| CRP (mg/dL) | S, hommes | non estimable (borne 0,01) | trop large (borne 1,08) |
| CRP (mg/dL) | S, femmes | non estimable (borne 0,01) | trop large (borne 1,28) |
| Acide urique (mg/dL) | S, hommes | conforme (borne 3,8) | trop large (borne 8,2) |
| Acide urique (mg/dL) | S, femmes | trop large (borne 2,8) | trop strict (borne 6,2) |
| Fer sérique (µg/dL) | S, hommes | trop large (borne 41) | conforme (borne 174) |
| Fer sérique (µg/dL) | S, femmes | trop large (borne 20,9) | conforme (borne 161) |
| Folates érythrocytaires (nmol/L) | S, hommes | non estimable (borne 130) | non estimable (borne 518) |
| Folates érythrocytaires (nmol/L) | S, femmes | non estimable (borne 135) | non estimable (borne 544) |
| Vitamine D 25-OH (nmol/L) | R | conforme (borne 49,9) |  |
| Vitamine D 25-OH (nmol/L) | R sensibilité 30 | trop strict (borne 74,9) |  |
| Vitamine B12 (pg/mL) | S, hommes | non estimable (borne 203) | non estimable (borne 1,13e+03) |
| Vitamine B12 (pg/mL) | S, femmes | non estimable (borne 216) | non estimable (borne 1,44e+03) |
| Homocystéine (µmol/L) | S, hommes | non estimable (borne 5,56) | non estimable (borne 14,1) |
| Homocystéine (µmol/L) | S, femmes | non estimable (borne 4,47) | non estimable (borne 11,1) |

Lecture :
- **Numération.** Les intervalles S sont souvent trop larges du côté « haut » pour l'inflammation :
  leucocytes au-dessus de 8,1 G/L, monocytes, plaquettes au-dessus de 286 G/L. Ils sont trop larges
  du côté « bas » pour la masse rouge : hémoglobine sous 14,0 g/dL, hématies, hématocrite.
- **Hémoglobine.** Chez les femmes, la borne haute (15,2 g/dL) est jugée « trop stricte » par le
  modèle commun. Or l'interaction avec le sexe est répliquée pour ce marqueur : il faut lire la
  courbe des femmes (`Q6_courbes.csv`, `sexe_F`).
- **Foie et protéines.**
  - ALAT, ASAT, protéines et albumine : la zone de risque minimal est étroite, et les deux côtés de
    l'intervalle S sont trop larges.
  - GGT et PAL : seul le côté haut compte. Leur borne basse est trop stricte : une valeur basse n'est
    pas un risque.

## Prédictions (formes attendues d'après la littérature)

- **Base des prédictions.** Toutes reposent sur un résumé seulement, sauf celle des lymphocytes
  (passages du texte intégral).
- **Règle de vérification.** Une prédiction est vérifiée si les côtés de risque **retenus en
  validation** sont ceux prévus. La colonne « Développement » donne la forme brute avant
  réplication.

| Marqueur | Attendu | Retenu en validation | Développement | Vérifiée |
|---|---|---|---|---|
| ALAT (U/L) | descendante | en U ou en J | en U ou en J | non |
| GGT (U/L) | montante | montante | montante | oui |
| PAL (U/L) | montante | montante | montante | oui |
| Bilirubine totale (mg/dL) | montante | en U ou en J | en U ou en J | non |
| Albumine (g/dL) | descendante | descendante | descendante | oui |
| HDL (mg/dL) | en U ou en J | en U ou en J | en U ou en J | oui |
| LDL (mg/dL) | en U ou en J | descendante | en U ou en J | non |
| Cholestérol total (mg/dL) | en U ou en J | en U ou en J | en U ou en J | oui |
| Triglycérides à jeun (mg/dL) | plate | plate | en U ou en J | oui |
| Triglycérides sériques (mg/dL) | montante | plate | en U ou en J | non |
| RDW (%) | montante | montante | montante | oui |
| VGM (fL) | en U ou en J | en U ou en J | en U ou en J | oui |
| TCMH (pg) | en U ou en J | en U ou en J | en U ou en J | oui |
| CCMH (g/dL) | descendante | descendante | en U ou en J | oui |
| Leucocytes (G/L) | montante | en U ou en J | en U ou en J | non |
| Neutrophiles/lymphocytes | montante | montante | en U ou en J | oui |
| Lymphocytes (G/L) | descendante | en U ou en J | en U ou en J | non |
| Sodium (mmol/L) | en U ou en J | descendante | descendante | non |
| Potassium (mmol/L) | montante | en U ou en J | en U ou en J | non |
| Chlorure (mmol/L) | descendante | en U ou en J | en U ou en J | non |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | descendante | en U ou en J | en U ou en J | non |
| RAC urinaire (mg/g) | montante | montante | montante | oui |
| Acide urique (mg/dL) | en U ou en J | en U ou en J | en U ou en J | oui |
| Glycémie à jeun (mg/dL) | en U ou en J | montante | en U ou en J | non |
| HbA1c (%) | en U ou en J | en U ou en J | en U ou en J | oui |
| Insuline à jeun (µU/mL) | plate | en U ou en J | en U ou en J | non |
| HOMA-IR | montante | en U ou en J | en U ou en J | non |
| CRP (mg/dL) | montante | en U ou en J | en U ou en J | non |
| Vitamine D 25-OH (nmol/L) | descendante | descendante | en U ou en J | oui |
| Phosphore (mg/dL) | montante | montante | en U ou en J | oui |
| Bicarbonates (mmol/L) | descendante | descendante | en U ou en J | oui |
| Urée (mg/dL) | montante | en U ou en J | en U ou en J | non |
| Urée/créatinine | en U ou en J | descendante | en U ou en J | non |
| FIB-4 | montante | en U ou en J | en U ou en J | non |
| Homocystéine (µmol/L) | montante | — | montante | sans validation |

**Bilan : 17 prédictions vérifiées sur 34** (15 sur 35 si on juge sur le développement seul).

- **Le développement voit presque toujours deux côtés**, et la validation en retire souvent un. Elle
  sert donc de filtre, en particulier pour les côtés « bas » des marqueurs de l'inflammation.
- **Points notables :**
  - **ALAT : relation en U**, et pas seulement « ALAT basse » ;
  - **bilirubine : en J**. La source NHANES lue la décrivait montante ; le côté bas apparaît ici,
    mais son côté haut disparaît quand on exclut les décès précoces ;
  - **potassium : en U** (votre exemple), alors que les sources lues ne décrivaient que le côté
    haut ;
  - **sodium : seul le côté bas** (sous 137 mmol/L) est répliqué ;
  - **RDW : montant dès 12,4 %**, à l'intérieur de l'intervalle usuel.

## Mortalité par cause (analyse secondaire)

Décès cardiovasculaires (UCOD 1 et 5) et par cancer (UCOD 2) à 10 ans, modèles par cause. Même critère
de réplication des côtés, sans IC bootstrap.

| Marqueur | Cause | Décès dév. / val. | p dév. / val. | Forme dév. / val. | Côtés retenus |
|---|---|---|---|---|---|
| Cholestérol total (mg/dL) | cardiovasculaire | 497 / 266 | 0,000 / 0,270 | en U / descendante | aucun |
| Cholestérol total (mg/dL) | cancer | 442 / 289 | 0,028 / 0,019 | descendante / en U | bas |
| LDL (mg/dL) | cardiovasculaire | 202 / 131 | 0,006 / 0,040 | en J / en U | bas, haut |
| LDL (mg/dL) | cancer | 190 / 131 | 0,303 / 0,390 | descendante / descendante | aucun |
| HDL (mg/dL) | cardiovasculaire | 497 / 266 | 0,011 / 0,002 | en U / en U | bas, haut |
| HDL (mg/dL) | cancer | 442 / 289 | 0,026 / 0,011 | en J / en U | bas, haut |
| Cholestérol non-HDL (mg/dL) | cardiovasculaire | 497 / 266 | 0,000 / 0,117 | en U / en J | aucun |
| Cholestérol non-HDL (mg/dL) | cancer | 442 / 289 | 0,032 / 0,229 | descendante / en J | aucun |
| Triglycérides à jeun (mg/dL) | cardiovasculaire | 202 / 131 | 0,074 / 0,593 | montante / montante | aucun |
| Triglycérides à jeun (mg/dL) | cancer | 190 / 131 | 0,588 / 0,956 | en J / montante | aucun |
| Triglycérides sériques (mg/dL) | cardiovasculaire | 500 / 265 | 0,017 / 0,782 | montante / montante | aucun |
| Triglycérides sériques (mg/dL) | cancer | 440 / 289 | 0,246 / 0,613 | en U / montante | aucun |
| Glycémie à jeun (mg/dL) | cardiovasculaire | 208 / 132 | 0,000 / 0,031 | en U / montante | haut |
| Glycémie à jeun (mg/dL) | cancer | 191 / 133 | 0,580 / 0,349 | en J / montante | aucun |
| HbA1c (%) | cardiovasculaire | 516 / 267 | 0,000 / 0,000 | en J / en U | bas, haut |
| HbA1c (%) | cancer | 449 / 293 | 0,722 / 0,041 | descendante / en U | aucun |
| CRP (mg/dL) | cardiovasculaire | 503 / 266 | 0,000 / 0,000 | en U / montante | haut |
| CRP (mg/dL) | cancer | 443 / 291 | 0,000 / 0,000 | en J / montante | haut |
| Créatinine (mg/dL) | cardiovasculaire | 499 / 266 | 0,000 / 0,000 | montante / montante | haut |
| Créatinine (mg/dL) | cancer | 441 / 289 | 0,018 / 0,023 | en U / montante | haut |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | cardiovasculaire | 499 / 266 | 0,000 / 0,000 | en U / en U | bas, haut |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | cancer | 441 / 289 | 0,022 / 0,026 | en U / descendante | bas |
| RAC urinaire (mg/g) | cardiovasculaire | 508 / 271 | 0,000 / 0,000 | montante / montante | haut |
| RAC urinaire (mg/g) | cancer | 474 / 310 | 0,000 / 0,000 | montante / montante | haut |
| Urée (mg/dL) | cardiovasculaire | 499 / 265 | 0,000 / 0,000 | en U / en J | bas, haut |
| Urée (mg/dL) | cancer | 441 / 289 | 0,000 / 0,000 | en U / en U | bas, haut |
| Acide urique (mg/dL) | cardiovasculaire | 499 / 265 | 0,000 / 0,000 | en U / montante | haut |
| Acide urique (mg/dL) | cancer | 441 / 289 | 0,017 / 0,001 | en J / en U | bas, haut |

- **Lipides.**
  - Le HDL reste en U pour la mortalité cardiovasculaire comme pour le cancer.
  - Pour la mortalité **cardiovasculaire**, le LDL a deux côtés répliqués, bas et haut (petit
    effectif à jeun : 202 et 131 décès). Pour le cancer, il n'a aucun côté répliqué.
  - Pour le cholestérol total, seul le côté bas est répliqué, et seulement pour le cancer. C'est la
    signature habituelle de la causalité inverse.
  - Les TG ne sont associés de façon répliquée à aucune cause.
- **Glycémie et HbA1c.**
  - Glycémie à jeun : son côté haut est répliqué pour la mortalité cardiovasculaire, pas pour le
    cancer.
  - HbA1c : en U pour la mortalité cardiovasculaire ; pas d'association répliquée avec le cancer.
- **CRP.** Côté haut répliqué pour les deux causes.
- **Rein.**
  - La créatinine et le RAC sont montants pour les deux causes.
  - Le DFGe est en U pour la mortalité cardiovasculaire. Pour le cancer, seul le côté bas est
    répliqué.
- **Acide urique.** Côté haut pour la mortalité cardiovasculaire ; en U pour le cancer.

## Âge (analyse secondaire) et population visée

- **Ce qui est ajusté.** Courbes séparées pour les 20-59 ans et les 60-79 ans, et pour les 30-55 ans,
  sur 1999-2010 réunis (non répliquées).
- **Minimum de décès.** Seuil fixé à 150 décès ; aucune tranche n'est sous ce minimum. Les décès vont
  de 277 à 721 pour les 20-59 ans, de 846 à 2 027 pour les 60-79 ans et de 197 à 514 pour les
  30-55 ans selon les marqueurs.
- **Interaction avec l'âge.** Test spline × âge, en développement puis en validation.

| Marqueur | 20-59 ans (décès) | 60-79 ans (décès) | 30-55 ans (décès) | Interaction âge, p dév. / val. |
|---|---|---|---|---|
| Cholestérol total (mg/dL) | en J (674) | en J (1987) | en U (483) | 0,112 / 0,396 |
| LDL (mg/dL) | en U (290) | descendante (846) | en U (221) | 0,161 / 0,161 |
| HDL (mg/dL) | en U (674) | en U (1987) | en U (483) | 0,008 / 0,210 |
| Cholestérol non-HDL (mg/dL) | en U (674) | en J (1987) | en U (483) | 0,860 / 0,178 |
| Triglycérides à jeun (mg/dL) | montante (290) | en U (846) | montante (221) | 0,068 / 0,598 |
| Triglycérides sériques (mg/dL) | montante (675) | en U (1985) | montante (483) | 0,013 / 0,509 |
| Glycémie à jeun (mg/dL) | en U (298) | en U (861) | en U (225) | 0,085 / 0,033 |
| HbA1c (%) | en U (691) | en U (2022) | en U (494) | 0,147 / 0,005 |
| CRP (mg/dL) | montante (681) | en U (2003) | en J (486) | 0,045 / 0,125 |
| Créatinine (mg/dL) | en U (676) | montante (1986) | en U (483) | 0,005 / 0,009 |
| DFGe CKD-EPI 2021 (mL/min/1,73 m²) | en U (676) | en J (1986) | en U (483) | 0,000 / 0,004 |
| RAC urinaire (mg/g) | montante (721) | montante (2027) | montante (514) | 0,001 / 0,038 |
| Urée (mg/dL) | en U (676) | en U (1985) | en U (483) | 0,000 / 0,000 |
| Acide urique (mg/dL) | en J (676) | en U (1985) | en J (483) | 0,121 / 0,176 |
| ALAT (U/L) | en U (675) | en U (1980) | en U (482) | 0,876 / 0,214 |
| GGT (U/L) | montante (676) | en J (1986) | montante (483) | 0,038 / 0,001 |
| Albumine (g/dL) | descendante (676) | descendante (1986) | descendante (483) | 0,001 / 0,006 |
| RDW (%) | montante (695) | montante (2026) | montante (497) | 0,065 / 0,116 |
| Leucocytes (G/L) | en U (695) | en U (2026) | en J (497) | 0,250 / 0,098 |
| Hémoglobine (g/dL) | en J (695) | en J (2026) | en J (497) | 0,826 / 0,166 |
| Plaquettes (G/L) | en U (695) | en U (2026) | en U (497) | 0,000 / 0,148 |
| Sodium (mmol/L) | descendante (676) | en J (1985) | descendante (483) | 0,031 / 0,082 |
| Potassium (mmol/L) | en U (676) | en J (1985) | en U (483) | 0,053 / 0,031 |
| Vitamine D 25-OH (nmol/L) | en J (559) | descendante (1610) | en J (401) | 0,506 / 0,036 |

- **Pour les 30-55 ans, la plupart des formes sont les mêmes que chez tous les adultes.** Quelques
  différences :
  - **LDL et cholestérol total** : en U chez les 30-55 ans, mais **descendants** (LDL) ou en J chez
    les 60-79 ans. Le côté bas « protecteur » du LDL élevé est surtout un fait des personnes âgées,
    ce qui va avec la causalité inverse.
  - **Triglycérides** : montants chez les 20-59 ans, en U chez les 60-79 ans.
  - **Créatinine, urée, DFGe, RAC, albumine** : l'interaction avec l'âge est répliquée. Les seuils
    de ces marqueurs devraient être lus par âge (`Q6_ages.csv`, `Q6_courbes.csv`).

## Sensibilités : facteur de risque ou marqueur de maladie ?

Chaque sensibilité est comparée à l'analyse principale de développement. Il y a **changement net**
si un côté de risque apparaît ou disparaît, ou si le seuil HR 1,2 sort de l'IC bootstrap principal.

| Sensibilité | Marqueurs avec un changement net |
|---|---|
| 1. Décès des 3 premières années exclus | 14 |
| 2. Population saine (critères D1) | 54 (sur 58 estimables), voir la réserve ci-dessous |
| 3. Ajustement tabac, IMC, diabète, revenu | 26 |
| 4. Ajustement traitements (lipides, glycémie) | 5 sur 15 |
| 5. Poids d'enquête | 10 |
| 6. Suivi complet (jusqu'à 2019) | 25 |

**Sensibilité 1 (décès précoces exclus) : marqueurs de maladie probables.**

| Marqueur | Changement net (décès des 3 premières années exclus) |
|---|---|
| Leucocytes (G/L) | côté bas disparaît |
| Neutrophiles (%) | côté bas disparaît |
| Neutrophiles (G/L) | côté bas disparaît |
| Lymphocytes (G/L) | seuil bas hors IC (1.32) |
| Bilirubine totale (mg/dL) | côté haut disparaît |
| Protéines totales (g/dL) | seuil bas hors IC (6.45) |
| Chlorure (mmol/L) | côté haut disparaît |
| Bicarbonates (mmol/L) | côté haut disparaît |
| Phosphore (mg/dL) | côté bas disparaît |
| CRP (mg/dL) | côté bas disparaît |
| Vitamine D 25-OH (nmol/L) | seuil haut hors IC (116) |
| Calcium corrigé (mg/dL) | côté bas disparaît |
| Indice SII | seuil bas hors IC (174) |
| Vitamine B12 (pg/mL) | seuil haut hors IC (1.48e+03) |

- **Sensibilité 2 : la règle fonctionne mal, et ce n'était pas prévu.** Il faut le dire clairement.
  - La population saine (critères D1 complets) ne compte que **138 décès** en développement, contre
    1 705.
  - Les IC bootstrap de l'analyse principale sont étroits. Presque toute courbe estimée sur un
    effectif dix fois plus petit en sort : 54 marqueurs sur 58 sont signalés.
  - Lue à la lettre, la règle pré-enregistrée classerait ces 54 marqueurs « marqueurs de maladie
    probables ». Cette conclusion n'est pas défendable : la sensibilité manque de puissance.
  - Nous rapportons la liste (`Q6_sensibilites.csv`) sans en tirer de conclusion marqueur par
    marqueur. Seule la sensibilité 1 sert à repérer les marqueurs de maladie.
- **Sensibilités 3 et 4.**
  - Ajuster sur le diabète et les traitements repousse le seuil haut de la glycémie à jeun et de
    l'HbA1c (156 et 7,4 % une fois les traitements pris en compte). Une part du risque « glycémie
    haute » passe par le diabète traité.
  - Ajuster sur le tabac, l'IMC et le revenu fait disparaître le côté haut du LDL.
- **Sensibilité 6 (suivi complet).** Sur 20 ans, le côté bas des TG et des indices TG disparaît, et
  plusieurs seuils bougent. Les relations ne sont pas stables dans le temps : c'est une raison de
  plus pour s'en tenir à l'horizon de 10 ans.

## Conséquences pour un produit de suivi

1. **Ne pas présenter un intervalle de laboratoire comme une « zone de santé ».** Pour beaucoup de
   marqueurs, le risque associé commence à l'intérieur de l'intervalle usuel. Exemples : leucocytes,
   RDW, GGT, PAL, CRP, albumine, HDL des deux côtés.
2. **Les zones de risque minimal sont étroites.** Exemples : ALAT 18-44 U/L, albumine 4,2-5,1 g/dL,
   HDL 41-70 mg/dL, DFGe 69-102. Un HR de 1,2 est vite atteint. Pour une personne, cela reste une
   association de population, sans preuve qu'agir sur le marqueur change le risque.
3. **Plusieurs côtés de risque sont des marqueurs de maladie, pas des leviers.** C'est le cas des
   côtés bas des leucocytes et de la CRP, du côté haut de la bilirubine et du LDL bas chez les
   personnes âgées. Ils ne doivent pas être présentés comme des cibles.
4. **Pour les 30-55 ans, les formes sont proches de celles de l'ensemble.** Le rein, l'albumine et
   la GGT dépendent de l'âge : leurs seuils doivent être lus par âge.

## Limites

- **Association, pas causalité.** Les sensibilités 1 à 4 ne corrigent qu'en partie la causalité
  inverse et la confusion. La sensibilité 2 manque de puissance.
- **Mortalité seule.** Pas de morbidité, de qualité de vie ni d'événements non mortels. Un seuil
  « trop strict » pour la mortalité peut être juste pour l'événement cardiovasculaire ou le diabète.
- **Population américaine, 1999-2010.** Méthodes de laboratoire de l'époque, harmonisées vers
  2009-2010 ; traitements de l'époque (moins de statines qu'aujourd'hui).
- **Traitements.** Les personnes traitées ont des valeurs modifiées. La sensibilité 4 ne concerne que
  les lipides et la glycémie, et les traitements sont déclarés.
- **Une mesure unique.** Le bruit (Q1 : changements détectables, bornes basses) aplatit les courbes
  et éloigne les seuils du minimum.
- **Nombre de tests.** 68 marqueurs, plusieurs issues et sensibilités : la réplication sert de
  garde-fou, mais certains côtés retenus restent des faux positifs.
- **Modèle commun aux deux sexes.** Pour les 6 marqueurs à interaction répliquée, il faut lire les
  courbes par sexe.
- **Point minimal.** Il est traité comme fixe dans l'IC delta. Le bootstrap des seuils en tient
  compte.
- **Effectifs.** Marqueurs à jeun : 691 à 707 décès en développement. B12 et homocystéine n'ont pas
  de validation.

## Écarts au pré-enregistrement et analyses non prévues

1. **Minimum de 100 décès pour la sensibilité 2 et les causes.** Le code fixait ce minimum avant
   l'analyse, mais le texte pré-enregistré ne le mentionnait pas.
   - Conséquence : la sensibilité 2 est « non estimable » pour les 12 marqueurs à jeun.
   - Les causes ne sont jamais concernées : elles ont au moins 131 décès.
2. **Lecture de la sensibilité 2.** Nous ne l'utilisons pas pour classer les marqueurs (voir plus
   haut), faute de puissance. C'est une interprétation non pré-enregistrée.
3. **Figures redessinées** après l'analyse : graduations lisibles et libellés en français, à partir
   des courbes sauvegardées. Aucun modèle n'a été refait.
4. **Bootstrap.** Les 500 tirages prévus ont été faits (46 minutes sur 4 processus).
5. **IC bootstrap parfois présents d'un côté sans seuil de développement.** Certains tirages trouvent
   un seuil d'un côté où l'estimation principale n'en a pas (GGT, côté bas). Ces IC sont rapportés
   dans `Q6_zones.csv`, mais ne servent à rien : le côté n'est pas retenu.
