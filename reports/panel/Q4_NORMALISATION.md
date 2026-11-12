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
  dans NHANES III. **Depuis la correction du 2026-11-12**, la variance du bruit vient de l'autre jeu
  (2001-2002 pour NHANES III, et inversement), et non plus des mêmes paires.
- **Limites / nettes** : taux de normalisation des anomalies à moins d'un changement détectable du
  seuil, et des autres. **Depuis la même correction**, ce changement détectable vient de l'autre jeu.
  Avant, il était calculé sur les mêmes paires : une anomalie « nette » devait franchir plus que le
  95ᵉ centile du bruit de ces données pour se normaliser, ce qui ne pouvait presque pas arriver
  (résultat obtenu par construction). Les marqueurs sans changement détectable dans l'autre jeu (ACR,
  ApoB, globulines…) ne sont plus partagés (« — ») ; avant, toutes leurs anomalies étaient comptées
  « nettes ».
- **Limites / nettes (attendu sous le bruit)** : la même prédiction binormale, par classe.

| Marqueur | Type | Part anormaux | Normalisation 2001-02 (prédiction) | **Normalisation NHANES III** | Attendu sous le bruit | Limites / nettes (observé) | Limites / nettes (attendu sous le bruit) | Compatible | Conclusion (règle) |
|---|---|---|---|---|---|---|---|---|---|
| Rapport albumine/créatinine urinaire | R | 9 % / 11 % | 28 % (n=39) | **29 %** (n=136) | 32 % | — / — | — / — | oui | normalisation < 30 % (deux jeux) |
| DFGe (CKD-EPI 2021) | R | 4 % / 5 % | 12 % (n=16) | **32 %** (n=81) | 20 % | 47 % / 21 % | 43 % / 3 % | — | confirmer avant de signaler (un seul jeu) |
| Glycémie à jeun (plasma) (ADA) | R | 38 % / 30 % | 30 % (n=63) | **24 %** (n=359) | 21 % | 31 % / 2 % | 28 % / 0 % | non | normalisation < 30 % (deux jeux) |
| Glycémie à jeun (plasma) (OMS) | R | 16 % / 17 % | 19 % (n=26) | **26 %** (n=200) | 22 % | 38 % / 4 % | 33 % / 0 % | non | normalisation < 30 % (deux jeux) |
| HbA1c (ADA) | R | 21 % / 32 % | 16 % (n=90) | **19 %** (n=580) | 15 % | 35 % / 2 % | 29 % / 0 % | non | normalisation < 30 % (deux jeux) |
| HbA1c (OMS) | R | 12 % / 18 % | 10 % (n=52) | **16 %** (n=326) | 12 % | 36 % / 3 % | 29 % / 0 % | non | normalisation < 30 % (deux jeux) |
| LDL (calculé, à jeun) | R | 56 % / 61 % | 33 % (n=83) | **13 %** (n=358) | 14 % | 19 % / 2 % | 21 % / 1 % | non | normalisation < 30 % (deux jeux) |
| Cholestérol non-HDL | R | 66 % / 72 % | 13 % (n=268) | **9 %** (n=1282) | 8 % | 15 % / 3 % | 17 % / 0 % | non | normalisation < 30 % (deux jeux) |
| Triglycérides (à jeun) | R | 30 % / 35 % | 28 % (n=50) | **22 %** (n=621) | 25 % | 26 % / 3 % | 30 % / 2 % | non | normalisation < 30 % (deux jeux) |
| Triglycérides sériques (non à jeun) | R | 28 % / 33 % | 30 % (n=114) | **18 %** (n=437) | 26 % | 21 % / 1 % | 31 % / 2 % | non | normalisation < 30 % (deux jeux) |
| 25-OH vitamine D | R | 44 % / — | 11 % (n=150) | **—** (n=—) | — | — / — | — / — | — | normalisation < 30 % (un seul jeu) |
| 25-OH vitamine D (sensibilité 30) | R | 84 % / — | 8 % (n=286) | **—** (n=—) | — | — / — | — / — | — | normalisation < 30 % (un seul jeu) |
| Bicarbonates | S | 13 % / 33 % ⚠ | 69 % (n=55) | **54 %** (n=572) | 24 % | 54 % / 54 % | 29 % / 3 % | non | anomalie isolée peu informative (deux jeux) |
| Bilirubine totale | S | 2 % / 11 % | 78 % (n=9) | **60 %** (n=198) | 45 % | 61 % / 52 % | 48 % / 24 % | — | anomalie isolée peu informative (un seul jeu) |
| Calcium | S | 8 % / 15 % | 64 % (n=33) | **66 %** (n=260) | 45 % | 67 % / 42 % | 47 % / 7 % | oui | anomalie isolée peu informative (deux jeux) |
| Chlorure | S | 8 % / 15 % | 67 % (n=33) | **63 %** (n=262) | 52 % | 64 % / 43 % | 55 % / 9 % | oui | anomalie isolée peu informative (deux jeux) |
| Fer sérique | S | 6 % / 6 % | 65 % (n=23) | **62 %** (n=107) | 68 % | 63 % / 33 % | 71 % / 19 % | oui | anomalie isolée peu informative (deux jeux) |
| Homocystéine | S | 9 % / — | 54 % (n=37) | **—** (n=—) | — | — / — | — / — | — | anomalie isolée peu informative (un seul jeu) |
| Osmolalité mesurée | S | — / 21 % ⚠ | — (n=—) | **58 %** (n=279) | 47 % | — / — | — / — | — | anomalie isolée peu informative (un seul jeu) |
| Phosphate | S | 5 % / 7 % | 60 % (n=20) | **72 %** (n=123) | 62 % | 72 % / 57 % | 64 % / 18 % | non | anomalie isolée peu informative (deux jeux) |
| Potassium | S | 8 % / 8 % | 79 % (n=33) | **61 %** (n=139) | 73 % | 63 % / 0 % | 75 % / 40 % | non | anomalie isolée peu informative (deux jeux) |
| Protéines totales | S | 7 % / 6 % | 70 % (n=27) | **72 %** (n=102) | 58 % | 73 % / 25 % | 60 % / 13 % | oui | anomalie isolée peu informative (deux jeux) |
| Saturation de la transferrine | S | — / 4 % | — (n=—) | **62 %** (n=39) | 67 % | — / — | — / — | — | anomalie isolée peu informative (un seul jeu) |
| Sodium | S | 6 % / 22 % ⚠ | 61 % (n=23) | **69 %** (n=382) | 59 % | 69 % / 75 % | 61 % / 29 % | non | anomalie isolée peu informative (deux jeux) |
| Urée | S | 10 % / 9 % | 50 % (n=40) | **55 %** (n=162) | 50 % | 57 % / 20 % | 53 % / 7 % | oui | anomalie isolée peu informative (deux jeux) |
| Éosinophiles (%) | S | 4 % / 21 % ⚠ | 53 % (n=15) | **65 %** (n=57) | 61 % | 60 % / 66 % | 71 % / 59 % | — | anomalie isolée peu informative (un seul jeu) |
| ASAT | S | 8 % / 21 % ⚠ | 39 % (n=33) | **33 %** (n=377) | 36 % | 38 % / 4 % | 41 % / 4 % | non | confirmer avant de signaler (deux jeux) |
| Acide urique | S | 12 % / 12 % | 35 % (n=49) | **31 %** (n=209) | 31 % | 34 % / 15 % | 37 % / 2 % | oui | confirmer avant de signaler (deux jeux) |
| Albumine | S | 5 % / 11 % | 32 % (n=22) | **48 %** (n=199) | 27 % | 55 % / 15 % | 33 % / 2 % | non | confirmer avant de signaler (deux jeux) |
| ApoB | S | — / 8 % | — (n=—) | **47 %** (n=64) | 37 % | — / — | — / — | — | confirmer avant de signaler (un seul jeu) |
| CCMH | S | 2 % / 6 % | 50 % (n=10) | **49 %** (n=99) | 47 % | 53 % / 29 % | 53 % / 8 % | — | confirmer avant de signaler (un seul jeu) |
| CRP | S | 7 % / 6 % | 33 % (n=30) | **53 %** (n=114) | 79 % | 54 % / 20 % | 81 % / 45 % | non | confirmer avant de signaler (deux jeux) |
| Capacité totale de fixation du fer | S | — / 8 % | — (n=—) | **45 %** (n=75) | 49 % | — / — | — / — | — | confirmer avant de signaler (un seul jeu) |
| Cholestérol total | S | 7 % / 6 % | 41 % (n=29) | **46 %** (n=109) | 38 % | 49 % / 23 % | 43 % / 3 % | oui | confirmer avant de signaler (deux jeux) |
| Créatinine | S | 6 % / 11 % | 35 % (n=23) | **44 %** (n=194) | 37 % | 52 % / 3 % | 43 % / 2 % | non | confirmer avant de signaler (deux jeux) |
| Globulines | S | — / 12 % | — (n=—) | **41 %** (n=167) | 32 % | — / — | — / — | — | confirmer avant de signaler (un seul jeu) |
| HDL | S | 5 % / 9 % | 55 % (n=22) | **46 %** (n=156) | 33 % | 48 % / 35 % | 39 % / 3 % | non | confirmer avant de signaler (deux jeux) |
| Hémoglobine | S | 8 % / 8 % | 31 % (n=32) | **31 %** (n=137) | 25 % | 39 % / 6 % | 32 % / 1 % | oui | confirmer avant de signaler (deux jeux) |
| Insuline (à jeun) | S | 10 % / 8 % | 31 % (n=16) | **36 %** (n=94) | 36 % | 41 % / 12 % | 43 % / 1 % | — | confirmer avant de signaler (un seul jeu) |
| Leucocytes | S | 7 % / 9 % | 57 % (n=30) | **46 %** (n=157) | 46 % | 47 % / 22 % | 49 % / 4 % | non | confirmer avant de signaler (deux jeux) |
| Lymphocytes (%) | S | 8 % / 7 % | 62 % (n=32) | **48 %** (n=128) | 66 % | 49 % / 25 % | 69 % / 24 % | non | confirmer avant de signaler (deux jeux) |
| Monocytes (%) | S | 6 % / 39 % ⚠ | 42 % (n=26) | **48 %** (n=107) | 55 % | 56 % / 38 % | 62 % / 47 % | oui | confirmer avant de signaler (deux jeux) |
| Neutrophiles (%) | S | 7 % / 11 % | 61 % (n=31) | **40 %** (n=30) | 40 % | 44 % / 0 % | 44 % / 1 % | non | confirmer avant de signaler (deux jeux) |
| Plaquettes | S | 5 % / 8 % | 43 % (n=23) | **32 %** (n=142) | 30 % | 36 % / 24 % | 40 % / 2 % | non | confirmer avant de signaler (deux jeux) |
| VPM | S | 5 % / 9 % | 55 % (n=20) | **32 %** (n=157) | 32 % | 36 % / 16 % | 38 % / 1 % | non | confirmer avant de signaler (deux jeux) |
| ALAT | S | 6 % / 33 % ⚠ | 36 % (n=25) | **30 %** (n=578) | 23 % | 34 % / 10 % | 27 % / 1 % | non | normalisation < 30 % (deux jeux) |
| Basophiles (%) | S | 0 % / 71 % ⚠ | 50 % (n=2) | **18 %** (n=195) | 44 % | 17 % / 33 % | 46 % / 1 % | — | normalisation < 30 % (un seul jeu) |
| Ferritine | S | 14 % / 17 % ⚠ | 15 % (n=26) | **14 %** (n=162) | 19 % | 19 % / 2 % | 26 % / 1 % | oui | normalisation < 30 % (deux jeux) |
| Folates érythrocytaires | S | 7 % / 35 % ⚠ | 21 % (n=28) | **17 %** (n=408) | 15 % | 29 % / 1 % | 25 % / 1 % | non | normalisation < 30 % (deux jeux) |
| GGT | S | 5 % / 8 % | 32 % (n=19) | **17 %** (n=117) | 16 % | 32 % / 2 % | 32 % / 1 % | — | normalisation < 30 % (un seul jeu) |
| Hématies | S | 7 % / 7 % | 29 % (n=31) | **37 %** (n=118) | 30 % | 44 % / 0 % | 35 % / 2 % | non | normalisation < 30 % (deux jeux) |
| Hématocrite | S | 9 % / 7 % | 44 % (n=36) | **28 %** (n=122) | 32 % | 32 % / 5 % | 38 % / 2 % | non | normalisation < 30 % (deux jeux) |
| PAL | S | 4 % / 15 % | 44 % (n=18) | **17 %** (n=256) | 21 % | 26 % / 0 % | 31 % / 1 % | — | normalisation < 30 % (un seul jeu) |
| RDW | S | 6 % / 8 % | 36 % (n=25) | **21 %** (n=141) | 16 % | 40 % / 0 % | 29 % / 1 % | non | normalisation < 30 % (deux jeux) |
| TCMH | S | 6 % / 4 % | 19 % (n=26) | **13 %** (n=71) | 9 % | 36 % / 2 % | 27 % / 0 % | oui | normalisation < 30 % (deux jeux) |
| VGM | S | 6 % / 6 % | 16 % (n=25) | **12 %** (n=113) | 11 % | 29 % / 0 % | 26 % / 0 % | oui | normalisation < 30 % (deux jeux) |
| Vitamine B12 | S | 4 % / 5 % | 39 % (n=18) | **28 %** (n=46) | 29 % | 41 % / 0 % | 42 % / 1 % | — | normalisation < 30 % (un seul jeu) |

| Normalisation | Conclusion |
|---|---|
| ≥ 30 % | **confirmer avant de signaler** |
| ≥ 50 % | **anomalie isolée peu informative** |

**Bilan** (57 couples marqueur-seuil ; corrigé le 2026-11-12, créatinine de NHANES III recalibrée) :
- **14 couples : anomalie isolée peu informative**, dont 9 dans les deux jeux. Ce sont surtout les
  électrolytes (sodium, potassium, chlorure, calcium, bicarbonates), les protéines, le phosphate,
  l'urée et le fer.
- **20 couples : confirmer avant de signaler**, dont 14 dans les deux jeux. Parmi eux : leucocytes,
  formule, plaquettes, ASAT, CRP, HDL, cholestérol total, urate, albumine, et désormais la
  **créatinine** (deux jeux) et le **DFGe < 60** (un seul jeu).
- **23 couples : normalisation < 30 %**, dont 17 dans les deux jeux. Ce sont notamment presque tous les
  **seuils de risque** (glycémie, HbA1c, LDL, non-HDL, TG, ACR, vitamine D), et les marqueurs
  stables (VGM, TCMH, ferritine, folates).

**Ce que change la recalibration de la créatinine de NHANES III** (erreur corrigée le 2026-11-12) :

| Couple | Avant : part d'anormaux ; normalisation ; conclusion | Après |
|---|---|---|
| DFGe < 60 | 17 % (n = 292) ; 21 % ; normalisation < 30 % (un seul jeu) | **5 %** (n = 81) ; **32 %** ; **confirmer avant de signaler** (un seul jeu) |
| Créatinine, intervalle S | 22 % ⚠ (n = 391) ; 26 % ; normalisation < 30 % (deux jeux) | **11 %** (n = 194) ; **44 %** ; **confirmer avant de signaler** (deux jeux) |

Une part de 17 % de DFGe < 60 chez des adultes de 20 à 79 ans n'était pas plausible : c'était le
signal de l'oubli. Le ⚠ « intervalle non transposable » de la créatinine disparaît : il venait de
cet oubli, et non de la méthode ou de la population.

**Prédiction** : les taux de 2001-2002 tombent dans l'IC de NHANES III pour **13 couples sur 40**.
La prédiction est donc mauvaise au niveau de chaque marqueur, ce qu'expliquent en partie les petits
effectifs de 2001-2002 (souvent 20 à 40 anomalies). Les conclusions, elles, sont souvent les mêmes
dans les deux jeux.

## Ce que montrent les données (faits)

1. **La normalisation s'explique en grande partie par le bruit de mesure.** Avec un bruit tiré de
   l'autre jeu (correction du 2026-11-12), la normalisation attendue sous le seul bruit (modèle
   binormal) est à moins de 10 points de la normalisation observée pour 76 % des couples dans
   NHANES III (74 % en 2001-2002). L'écart médian est de +3 points dans NHANES III. Avant la
   correction, le bruit venait des mêmes paires : 87 % et un écart médian de 0 point, une
   concordance en partie obtenue par construction. Le « retour à la normale » en 2 semaines reste
   surtout de la mesure, pas une guérison ; NHANES III, aux méthodes plus anciennes, se normalise un
   peu plus que ne le prédit le bruit de 2001-2002.
2. **Les anomalies limites se normalisent souvent, les anomalies nettes rarement** (recalculé le
   2026-11-12 avec un changement détectable de l'autre jeu ; couples d'au moins 20 anomalies dans
   la classe). Les anomalies limites redeviennent normales dans 41 % des cas (médiane de
   47 couples, NHANES III ; 39 % attendus sous le seul bruit). Les anomalies nettes,
   dans 4 % des cas (médiane de 31 couples ; 1 % attendus sous le seul bruit).
   - Ce chiffre n'est plus obtenu par construction, mais il reste en partie attendu : une anomalie
     loin du seuil se normalise peu, par définition. **L'ancien « 5 % »** (même changement
     détectable que les paires analysées) **était circulaire** : il ne décrivait que le découpage.
   - **Ce qui est nouveau** : pour 12 couples sur 31, les anomalies nettes se normalisent
     nettement plus que ne le prédit le bruit de 2001-2002 (plus de 5 points d'écart) : bicarbonates
     (54 % contre 3 %), sodium, HDL (35 % contre 3 %), plaquettes, DFGe (21 % contre 3 %), albumine,
     acide urique. Deux explications possibles, que ces données ne séparent pas : un bruit de NHANES
     III plus grand que celui de 2001-2002 (méthodes plus anciennes), ou de vraies variations en
     2 semaines.
3. **Les seuils de risque ont des taux de normalisation plus faibles** : de 9 à 29 % dans NHANES
   III, et jusqu'à 33 % en 2001-2002 (LDL). Ils classent
   anormaux beaucoup de personnes loin du seuil : 61 % de LDL ≥ 3,0 mmol/L et 72 % de non-HDL
   ≥ 3,4 mmol/L dans NHANES III.
4. **Intervalles statistiques non transposables** (⚠) pour l'ALAT, l'ASAT, la formule
   leucocytaire de NHANES III (basophiles, éosinophiles, monocytes), les bicarbonates, le sodium,
   l'osmolalité, les folates et la ferritine. Ils classent anormaux 15 à 71 % des personnes de
   NHANES III, contre environ 5 % attendus. (La créatinine figurait dans cette liste avant la
   correction du 2026-11-12 : c'était l'effet de la recalibration oubliée.) C'est l'illustration directe d'une limite connue :
   un intervalle de référence ne vaut que pour la méthode et la population où il a été établi.
   Pour la formule leucocytaire, NHANES III utilise une formule manuelle sur 100 cellules, avec
   beaucoup de valeurs 0 pour les basophiles.

## Lecture (interprétation)

- **Pour un produit de check-up** :
  - une anomalie **limite**, isolée, d'un marqueur bruité (électrolytes, enzymes, formule, CRP,
    lipides) se confirme avant d'être signalée : elle disparaît une fois sur deux à la mesure
    suivante, sans rien changer ;
  - une anomalie **nette**, elle, persiste le plus souvent, mais pas toujours pour les marqueurs
    bruités (bicarbonates, sodium, HDL, plaquettes). Un premier DFGe < 60 se confirme lui aussi avant
    d'être signalé : il disparaît une fois sur trois.
- **Afficher « anormal » suppose de dire de quel seuil on parle** : une convention statistique
  propre à une méthode et une population, ou un seuil de risque choisi par un comité. Pour la
  glycémie et l'HbA1c, les deux grands comités ne sont pas d'accord.
- **Les intervalles d'un laboratoire ne se transportent pas** dans un autre laboratoire ni dans une
  autre population sans vérification : c'est le sujet de Q5.

## Limites

- **Limite connue : créatinine de 2005-2006 non recalibrée dans la table D1.** La table des seuils
  D1 (intervalles statistiques, NHANES 2003-2010, `intervalles.py`) n'applique pas la recalibration
  recommandée de la créatinine de 2005-2006 (0,978 x − 0,016 mg/dL), alors que le pipeline principal
  l'applique. L'effet est limité à la créatinine et au DFGe, dans les questions qui utilisent D1
  (Q3, Q4, Q6). Signalée par l'audit indépendant du 2026-11-12, non corrigée (analyses gelées).
- Remesures à 2 semaines ; NHANES III date de 1988-1994 et utilise d'autres méthodes.
- Intervalles statistiques calculés sur une population américaine, avec des méthodes de
  2003-2010.
- La partition par âge est sensible aux ex aequo des valeurs entières.
- Petits effectifs d'anomalies en 2001-2002 : la règle n'est souvent appliquée qu'à un seul jeu.
- Vitamine D : 2001-2002 seulement, dosée avant la standardisation LC-MS/MS. CRP de NHANES III
  censurée.

## Correction du 2026-11-11

Un bug de lecture de NHANES III (code « 88 » des champs à 2 chiffres lu comme une valeur) touchait les bicarbonates et la formule leucocytaire manuelle. Après correction, aucune conclusion de la règle ne change. Deux chiffres de synthèse changent : 81 % devient 87 % (écart observé − attendu < 10 points), et 8 % devient 5 % (normalisation des anomalies nettes). Voir `DECISIONS.md`.

## Corrections du 2026-11-12 (audit indépendant)

1. **Créatinine de NHANES III recalibrée** (0,960 x − 0,184 mg/dL), avant le calcul du DFGe. Elle
   l'était dans le pipeline principal, pas dans le programme panel. Deux conclusions changent
   (tableau plus haut).
2. **Changement détectable « limites / nettes » et bruit du modèle binormal tirés de l'autre jeu**,
   pour supprimer la circularité. Le taux des anomalies nettes est recalculé et reformulé.
3. **Tableau généré depuis les CSV** (`q4_rapport.py`), avec une colonne d'attendu par classe.

Détail et tableaux avant/après : `DECISIONS.md`, « Corrections d'erreurs après audit ».

## Écarts au protocole

- Le pré-enregistrement renvoie, pour le détail des indicateurs, à un brouillon conservé hors du
  dépôt. Les indicateurs calculés sont exactement ceux décrits ci-dessus et dans `DECISIONS.md`.
- La signalisation ⚠ (plus de 15 % d'anormaux avec un intervalle S) n'était pas prévue. C'est une
  aide à la lecture, sans effet sur les conclusions de la règle.
