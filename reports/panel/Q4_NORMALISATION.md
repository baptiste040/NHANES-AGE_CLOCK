# Q4 : normalisation spontanée des valeurs anormales

Programme « panel ». Protocole pré-enregistré dans `DECISIONS.md` (commit `ce82907`), table des
seuils D1 figée avant tout calcul sur NHANES III. Code : `src/aging_clock/panel/intervalles.py`,
`src/aging_clock/panel/q4.py`. Données : `D1_*.csv`, `Q4_normalisation_*.csv`, `Q4_synthese.csv`.

**Question.** Parmi les valeurs anormales au premier examen, quelle part redevient normale au
second, environ 2 semaines plus tard, sans aucune intervention ?

## À lire avant les chiffres

- **Deux sortes de « seuils », à ne pas confondre.**
  - **R, seuil fondé sur le risque** : c'est une recommandation de décision clinique (OMS, ADA,
    ESC/EAS, KDIGO, Endocrine Society).
  - **S, convention statistique** : c'est un intervalle de référence, les 95 % centraux d'une
    population en bonne santé. Par construction, il classe « anormaux » 5 % de personnes en bonne
    santé.
- **Bornes basses.** Les remesures ont lieu à 2 semaines. À 6 mois, il y aura plus de
  normalisations, et certaines seront réelles.
- **NHANES est américain.** Les intervalles S sont calculés sur NHANES 2003-2010, avec d'autres
  méthodes de laboratoire que les jeux de test (2001-2002 et surtout NHANES III, 1988-1994).
- **Évaluation non aveugle** pour les 19 marqueurs déjà vus dans la piste « suivi ».

## Les seuils (table D1)

### Seuils fondés sur le risque (R)

| Marqueur | Seuil | Source lue |
|---|---|---|
| Glycémie à jeun | **OMS : ≥ 6,1 mmol/L** ; **ADA : ≥ 5,6 mmol/L** | OMS 2006 ; ESC 2023 diabète, tableau 6 (qui donne les deux) |
| HbA1c | **OMS : ≥ 6,0 %** ; **ADA : ≥ 5,7 %** | ESC 2023 diabète, tableau 6 |
| LDL | ≥ 3,0 mmol/L (objectif du risque faible) | ESC/EAS 2019 |
| Cholestérol non-HDL | ≥ 3,4 mmol/L (objectif du risque modéré ; aucun pour le risque faible) | ESC/EAS 2019 |
| Triglycérides (à jeun et non à jeun) | ≥ 1,7 mmol/L | ESC/EAS 2019 |
| DFGe | < 60 mL/min/1,73 m² | KDIGO 2024 |
| Rapport albumine/créatinine urinaire | ≥ 3 mg/mmol (30 mg/g) | KDIGO 2024 |
| 25-OH vitamine D | < 20 ng/mL ; sensibilité < 30 ng/mL (seuil débattu) | Endocrine Society 2011 |

### Un désaccord d'experts est déjà un résultat

Pour la glycémie à jeun et l'HbA1c, l'OMS et l'ADA, deux organismes de référence, fixent le début
de la « prédiabète » à des valeurs différentes. Le choix change d'un facteur 2 environ la part de
personnes déclarées anormales sur la même prise de sang :

| | Anormaux au 1ᵉʳ examen, 2001-2002 | NHANES III |
|---|---|---|
| Glycémie à jeun, OMS (≥ 6,1) | 16 % | 17 % |
| Glycémie à jeun, ADA (≥ 5,6) | **38 %** | **30 %** |
| HbA1c, OMS (≥ 6,0 %) | 12 % | 18 % |
| HbA1c, ADA (≥ 5,7 %) | **21 %** | **32 %** |

Un seuil est une **convention** : même quand il s'appuie sur le risque, deux comités qui lisent les
mêmes données ne placent pas la limite au même endroit. Un produit qui affiche « anormal » choisit
une convention et doit le dire. Le taux de normalisation, lui, change peu (19 à 30 % pour la
glycémie, 10 à 19 % pour l'HbA1c).

### Intervalles statistiques (S), calculés selon le CLSI EP28

- **Population de référence** : NHANES 2003-2010, adultes de 20 à 79 ans, avec les critères
  suivants :
  - non-fumeurs (cotinine < 3 ng/mL, Benowitz 2009) ;
  - IMC de 18,5 à 30, femmes non enceintes ;
  - sans diabète, maladie cardiovasculaire, hépatique, rénale ni cancer déclarés ;
  - sans traitement antidiabétique, antihypertenseur ni hypolipémiant.

  Résultat : 4 769 adultes.
- **Méthode** : 2,5ᵉ et 97,5ᵉ centiles par sexe, avec un IC 90 % des bornes, et une partition par
  tranche d'âge selon un critère fixé à l'avance (`D1_intervalles_statistiques.csv`).
- **Limite** : les électrolytes ont des valeurs entières, et leurs ex aequo font déclencher la
  partition par âge plus souvent que nécessaire.

### Marqueurs exclus de l'analyse principale, et pourquoi

- **Lp(a), ApoA1** : aucune mesure dans NHANES 2003-2010 ; NHANES III sert de jeu de test.
- **Sélénium, iode urinaire** : pas de mesure chez tous les adultes en 2003-2010.
- **LH, FSH, PSA** : leurs intervalles dépendent du cycle, du sexe ou de l'âge.
- **Concentrations urinaires brutes** : seul le rapport albumine/créatinine est interprétable.
- **Glucose non à jeun** : aucun seuil de décision lu.
- **Seuils de risque de la hs-CRP** : la déclaration AHA/CDC de 2003 n'a pas pu être lue (accès
  refusé). La CRP n'est donc analysée qu'avec son intervalle statistique.
- **Indices dérivés** (HOMA-IR, TyG, rapports, FIB-4, NLR, SII…) : aucun seuil lu.
- Ferritine, capacité de fixation et saturation : intervalles chez les femmes seulement
  (sous-échantillon NHANES).

## Résultats

Dans le tableau :
- **Part anormaux** : 2001-2002 / NHANES III. ⚠ signale un intervalle S qui classe anormaux plus de
  15 % des personnes de NHANES III : sans doute une différence de méthode de laboratoire ou de
  population (voir plus bas).
- **Attendu sous le bruit** : normalisation prédite par le seul bruit de mesure (modèle binormal),
  dans NHANES III.
- **Limites / nettes** : taux de normalisation des anomalies à moins d'un changement détectable du
  seuil, et des autres.

| Marqueur | Type | Part anormaux | Normalisation 2001-02 (prédiction) | **Normalisation NHANES III** | Attendu sous le bruit | Limites / nettes | Compatible | Conclusion (règle) |
|---|---|---|---|---|---|---|---|---|
| Rapport albumine/créatinine urinaire | R | 9 % / 11 % | 28 % (n=39) | **29 %** (n=136) | 32 % | — / 29 % | oui | normalisation < 30 % (deux jeux) |
| DFGe (CKD-EPI 2021) | R | 4 % / 17 % | 12 % (n=16) | **21 %** (n=292) | 23 % | 28 % / 0 % | — | normalisation < 30 % (un seul jeu) |
| Glycémie à jeun (plasma) (ADA) | R | 38 % / 30 % | 30 % (n=63) | **24 %** (n=359) | 24 % | 31 % / 2 % | non | normalisation < 30 % (deux jeux) |
| Glycémie à jeun (plasma) (OMS) | R | 16 % / 17 % | 19 % (n=26) | **26 %** (n=200) | 25 % | 38 % / 4 % | non | normalisation < 30 % (deux jeux) |
| HbA1c (ADA) | R | 21 % / 32 % | 16 % (n=90) | **19 %** (n=580) | 20 % | 28 % / 2 % | non | normalisation < 30 % (deux jeux) |
| HbA1c (OMS) | R | 12 % / 18 % | 10 % (n=52) | **16 %** (n=326) | 17 % | 29 % / 0 % | non | normalisation < 30 % (deux jeux) |
| LDL (calculé, à jeun) | R | 56 % / 61 % | 33 % (n=83) | **13 %** (n=358) | 18 % | 16 % / 3 % | non | normalisation < 30 % (deux jeux) |
| Cholestérol non-HDL | R | 66 % / 72 % | 13 % (n=268) | **9 %** (n=1282) | 10 % | 13 % / 2 % | non | normalisation < 30 % (deux jeux) |
| Triglycérides (à jeun) | R | 30 % / 35 % | 28 % (n=50) | **22 %** (n=621) | 26 % | 26 % / 2 % | non | normalisation < 30 % (deux jeux) |
| Triglycérides sériques (non à jeun) | R | 28 % / 33 % | 30 % (n=114) | **18 %** (n=437) | 24 % | 21 % / 1 % | non | normalisation < 30 % (deux jeux) |
| 25-OH vitamine D | R | 44 % / — | 11 % (n=150) | **—** (n=—) | — | — / — | — | normalisation < 30 % (un seul jeu) |
| 25-OH vitamine D (sensibilité 30) | R | 84 % / — | 8 % (n=286) | **—** (n=—) | — | — / — | — | normalisation < 30 % (un seul jeu) |
| Bilirubine totale | S | 2 % / 11 % | 78 % (n=9) | **60 %** (n=198) | 45 % | 63 % / 0 % | — | anomalie isolée peu informative (un seul jeu) |
| Calcium | S | 8 % / 15 % | 64 % (n=33) | **66 %** (n=260) | 62 % | 66 % / 50 % | oui | anomalie isolée peu informative (deux jeux) |
| Chlorure | S | 8 % / 15 % | 67 % (n=33) | **63 %** (n=262) | 63 % | 63 % / 50 % | oui | anomalie isolée peu informative (deux jeux) |
| Éosinophiles (%) | S | 4 % / 24 % ⚠ | 53 % (n=15) | **58 %** (n=67) | 23 % | 66 % / 18 % | — | anomalie isolée peu informative (un seul jeu) |
| Bicarbonates | S | 13 % / 35 % ⚠ | 69 % (n=55) | **55 %** (n=627) | 42 % | 54 % / 66 % | non | anomalie isolée peu informative (deux jeux) |
| Homocystéine | S | 9 % / — | 54 % (n=37) | **—** (n=—) | — | — / — | — | anomalie isolée peu informative (un seul jeu) |
| Fer sérique | S | 6 % / 6 % | 65 % (n=23) | **62 %** (n=107) | 67 % | 63 % / 33 % | oui | anomalie isolée peu informative (deux jeux) |
| Potassium | S | 8 % / 8 % | 79 % (n=33) | **61 %** (n=139) | 64 % | 63 % / 0 % | non | anomalie isolée peu informative (deux jeux) |
| Sodium | S | 6 % / 22 % ⚠ | 61 % (n=23) | **69 %** (n=382) | 60 % | 68 % / 80 % | non | anomalie isolée peu informative (deux jeux) |
| Osmolalité mesurée | S | — / 21 % ⚠ | — (n=—) | **58 %** (n=279) | 47 % | 58 % / 53 % | — | anomalie isolée peu informative (un seul jeu) |
| Phosphate | S | 5 % / 7 % | 60 % (n=20) | **72 %** (n=123) | 59 % | 72 % / 57 % | non | anomalie isolée peu informative (deux jeux) |
| Protéines totales | S | 7 % / 6 % | 70 % (n=27) | **72 %** (n=102) | 61 % | 73 % / 33 % | oui | anomalie isolée peu informative (deux jeux) |
| Saturation de la transferrine | S | — / 4 % | — (n=—) | **62 %** (n=39) | 67 % | 66 % / 25 % | — | anomalie isolée peu informative (un seul jeu) |
| Urée | S | 10 % / 9 % | 50 % (n=40) | **55 %** (n=162) | 51 % | 57 % / 22 % | oui | anomalie isolée peu informative (deux jeux) |
| Albumine | S | 5 % / 11 % | 32 % (n=22) | **48 %** (n=199) | 37 % | 52 % / 18 % | non | confirmer avant de signaler (deux jeux) |
| ApoB | S | — / 8 % | — (n=—) | **47 %** (n=64) | 37 % | 50 % / 17 % | — | confirmer avant de signaler (un seul jeu) |
| ASAT | S | 8 % / 21 % ⚠ | 39 % (n=33) | **33 %** (n=377) | 36 % | 37 % / 4 % | non | confirmer avant de signaler (deux jeux) |
| CRP | S | 7 % / 6 % | 33 % (n=30) | **53 %** (n=114) | 57 % | 55 % / 25 % | non | confirmer avant de signaler (deux jeux) |
| Globulines | S | — / 12 % | — (n=—) | **41 %** (n=167) | 32 % | 47 % / 4 % | — | confirmer avant de signaler (un seul jeu) |
| Hémoglobine | S | 8 % / 8 % | 31 % (n=32) | **31 %** (n=137) | 26 % | 39 % / 6 % | oui | confirmer avant de signaler (deux jeux) |
| HDL | S | 5 % / 9 % | 55 % (n=22) | **46 %** (n=156) | 44 % | 47 % / 30 % | non | confirmer avant de signaler (deux jeux) |
| Insuline (à jeun) | S | 10 % / 8 % | 31 % (n=16) | **36 %** (n=94) | 36 % | 41 % / 16 % | — | confirmer avant de signaler (un seul jeu) |
| Lymphocytes (%) | S | 8 % / 7 % | 62 % (n=32) | **48 %** (n=128) | 56 % | 49 % / 30 % | non | confirmer avant de signaler (deux jeux) |
| CCMH | S | 2 % / 6 % | 50 % (n=10) | **49 %** (n=99) | 54 % | 53 % / 20 % | — | confirmer avant de signaler (un seul jeu) |
| Monocytes (%) | S | 6 % / 41 % ⚠ | 42 % (n=26) | **47 %** (n=116) | 25 % | 48 % / 33 % | oui | confirmer avant de signaler (deux jeux) |
| VPM | S | 5 % / 9 % | 55 % (n=20) | **32 %** (n=157) | 39 % | 35 % / 17 % | non | confirmer avant de signaler (deux jeux) |
| Neutrophiles (%) | S | 7 % / 11 % | 61 % (n=31) | **40 %** (n=30) | 47 % | 44 % / 0 % | non | confirmer avant de signaler (deux jeux) |
| Plaquettes | S | 5 % / 8 % | 43 % (n=23) | **32 %** (n=142) | 38 % | 36 % / 19 % | non | confirmer avant de signaler (deux jeux) |
| Cholestérol total | S | 7 % / 6 % | 41 % (n=29) | **46 %** (n=109) | 45 % | 47 % / 30 % | oui | confirmer avant de signaler (deux jeux) |
| Capacité totale de fixation du fer | S | — / 8 % | — (n=—) | **45 %** (n=75) | 49 % | 47 % / 0 % | — | confirmer avant de signaler (un seul jeu) |
| Acide urique | S | 12 % / 12 % | 35 % (n=49) | **31 %** (n=209) | 31 % | 34 % / 15 % | oui | confirmer avant de signaler (deux jeux) |
| Leucocytes | S | 7 % / 9 % | 57 % (n=30) | **46 %** (n=157) | 45 % | 48 % / 18 % | non | confirmer avant de signaler (deux jeux) |
| PAL | S | 4 % / 15 % | 44 % (n=18) | **17 %** (n=256) | 19 % | 27 % / 0 % | — | normalisation < 30 % (un seul jeu) |
| ALAT | S | 6 % / 33 % ⚠ | 36 % (n=25) | **30 %** (n=578) | 29 % | 33 % / 10 % | non | normalisation < 30 % (deux jeux) |
| Vitamine B12 | S | 4 % / 5 % | 39 % (n=18) | **28 %** (n=46) | 28 % | 41 % / 0 % | — | normalisation < 30 % (un seul jeu) |
| Basophiles (%) | S | 0 % / 72 % ⚠ | 50 % (n=2) | **18 %** (n=204) | 6 % | 18 % / 22 % | — | normalisation < 30 % (un seul jeu) |
| Créatinine | S | 6 % / 22 % ⚠ | 35 % (n=23) | **26 %** (n=391) | 18 % | 31 % / 3 % | non | normalisation < 30 % (deux jeux) |
| Ferritine | S | 14 % / 17 % ⚠ | 15 % (n=26) | **14 %** (n=162) | 25 % | 18 % / 2 % | oui | normalisation < 30 % (deux jeux) |
| GGT | S | 5 % / 8 % | 32 % (n=19) | **17 %** (n=117) | 17 % | 34 % / 2 % | — | normalisation < 30 % (un seul jeu) |
| Hématocrite | S | 9 % / 7 % | 44 % (n=36) | **28 %** (n=122) | 30 % | 33 % / 5 % | non | normalisation < 30 % (deux jeux) |
| TCMH | S | 6 % / 4 % | 19 % (n=26) | **13 %** (n=71) | 11 % | 31 % / 2 % | oui | normalisation < 30 % (deux jeux) |
| VGM | S | 6 % / 6 % | 16 % (n=25) | **12 %** (n=113) | 11 % | 30 % / 0 % | oui | normalisation < 30 % (deux jeux) |
| Hématies | S | 7 % / 7 % | 29 % (n=31) | **37 %** (n=118) | 28 % | 45 % / 0 % | non | normalisation < 30 % (deux jeux) |
| Folates érythrocytaires | S | 7 % / 35 % ⚠ | 21 % (n=28) | **17 %** (n=408) | 15 % | 29 % / 1 % | non | normalisation < 30 % (deux jeux) |
| RDW | S | 6 % / 8 % | 36 % (n=25) | **21 %** (n=141) | 19 % | 33 % / 0 % | non | normalisation < 30 % (deux jeux) |
Règles pré-enregistrées, appliquées au plus petit des deux taux quand les deux jeux ont au moins
20 anomalies :

| Normalisation | Conclusion |
|---|---|
| ≥ 30 % | **confirmer avant de signaler** |
| ≥ 50 % | **anomalie isolée peu informative** |

**Bilan** (57 couples marqueur-seuil) :
- **14 couples : anomalie isolée peu informative**, dont 9 dans les deux jeux. Ce sont surtout les
  électrolytes (sodium, potassium, chlorure, calcium, bicarbonates), les protéines, le phosphate,
  l'urée et le fer.
- **18 couples : confirmer avant de signaler**, dont 13 dans les deux jeux. Parmi eux : leucocytes,
  formule, plaquettes, ASAT, CRP, HDL, cholestérol total, urate et albumine.
- **25 couples : normalisation < 30 %**, dont 18 dans les deux jeux. Ce sont notamment tous les
  **seuils de risque** (glycémie, HbA1c, LDL, non-HDL, TG, DFGe, ACR, vitamine D), et les marqueurs
  stables (VGM, TCMH, ferritine, folates).

**Prédiction** : les taux de 2001-2002 tombent dans l'IC de NHANES III pour **13 couples sur 40**.
La prédiction est donc mauvaise au niveau de chaque marqueur, ce qu'expliquent en partie les petits
effectifs de 2001-2002 (souvent 20 à 40 anomalies). Les conclusions, elles, sont souvent les mêmes
dans les deux jeux.

## Ce que montrent les données (faits)

1. **La normalisation s'explique presque entièrement par le bruit de mesure.** La normalisation
   attendue sous le seul bruit (modèle binormal) est à moins de 10 points de la normalisation
   observée pour 81 % des couples dans NHANES III (73 % en 2001-2002). L'écart médian est de 0
   point. Le « retour à la normale » en 2 semaines n'est pas une guérison : c'est la mesure.
2. **Les anomalies limites se normalisent, les anomalies nettes presque jamais.** Les anomalies
   limites (à moins d'un changement détectable du seuil) redeviennent normales dans 41 % des cas
   (médiane, NHANES III). Les anomalies nettes, dans 8 % des cas. Seule exception : les
   électrolytes et les bicarbonates, dont l'intervalle est très étroit.
3. **Les seuils de risque ont des taux de normalisation plus faibles** : de 9 à 29 % dans NHANES
   III, et jusqu'à 33 % en 2001-2002 (LDL). Ils classent
   anormaux beaucoup de personnes loin du seuil : 61 % de LDL ≥ 3,0 mmol/L et 72 % de non-HDL
   ≥ 3,4 mmol/L dans NHANES III.
4. **Intervalles statistiques non transposables** (⚠) pour l'ALAT, l'ASAT, la créatinine, la
   formule leucocytaire de NHANES III (basophiles, éosinophiles, monocytes), les bicarbonates, le
   sodium, l'osmolalité, les folates et la ferritine. Ils classent anormaux 15 à 72 % des personnes
   de NHANES III, contre environ 5 % attendus. C'est l'illustration directe d'une limite connue :
   un intervalle de référence ne vaut que pour la méthode et la population où il a été établi.
   Pour la formule leucocytaire, NHANES III utilise une formule manuelle sur 100 cellules, avec
   beaucoup de valeurs 0 pour les basophiles.

## Lecture (interprétation)

- **Pour un produit de check-up** :
  - une anomalie **limite**, isolée, d'un marqueur bruité (électrolytes, enzymes, formule, CRP,
    lipides) se confirme avant d'être signalée : elle disparaît une fois sur deux à la mesure
    suivante, sans rien changer ;
  - une anomalie **nette**, elle, persiste presque toujours.
- **Afficher « anormal » suppose de dire de quel seuil on parle** : une convention statistique
  propre à une méthode et une population, ou un seuil de risque choisi par un comité. Pour la
  glycémie et l'HbA1c, les deux grands comités ne sont pas d'accord.
- **Les intervalles d'un laboratoire ne se transportent pas** dans un autre laboratoire ni dans une
  autre population sans vérification : c'est le sujet de Q5.

## Limites

- Remesures à 2 semaines ; NHANES III date de 1988-1994 et utilise d'autres méthodes.
- Intervalles statistiques calculés sur une population américaine, avec des méthodes de
  2003-2010.
- La partition par âge est sensible aux ex aequo des valeurs entières.
- Petits effectifs d'anomalies en 2001-2002 : la règle n'est souvent appliquée qu'à un seul jeu.
- Vitamine D : 2001-2002 seulement, dosée avant la standardisation LC-MS/MS. CRP de NHANES III
  censurée.

## Écarts au protocole

- Le pré-enregistrement renvoie, pour le détail des indicateurs, à un brouillon conservé hors du
  dépôt. Les indicateurs calculés sont exactement ceux décrits ci-dessus et dans `DECISIONS.md`.
- La signalisation ⚠ (plus de 15 % d'anormaux avec un intervalle S) n'était pas prévue. C'est une
  aide à la lecture, sans effet sur les conclusions de la règle.
