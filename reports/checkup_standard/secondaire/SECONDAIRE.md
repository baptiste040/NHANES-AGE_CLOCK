# Validation secondaire 2015-2018

Modèle gelé (point 4) ; protocole écrit avant exécution (`DECISIONS.md`, point 6). Analyse
**descriptive** de transposition ; aucune décision sur le modèle. Chaînage de mortalité public
le plus récent : 2019 (suivi jusqu'au 31/12/2019 ; la mise à jour 2022 est en accès restreint).
Peu de décès (162, dont 44 en 2017-2018) : intervalles larges.

## Harmonisation des dosages

- **RDW** : changement d'automate en 2013-2014 (Beckman DxH 800) sans étude de pontage →
  recalage par quantiles sur **2011-2012**, dernier cycle avant le changement, par strates
  sexe × âge.
- **Biochimie 2017-2018** (Roche Cobas 6000) : équations de pontage NHANES (`BIOPRO_J`, sens
  Cobas → DxC 660i) pour ALAT, ASAT, PAL, albumine, créatinine, GGT, triglycérides ; glucose non
  ajusté (recommandation NHANES). **hs-CRP 2017-2018** : équation NHANES (`HSCRP_J`), bornée au
  plancher de 0,1 mg/L (l'équation donne des valeurs négatives sous ~0,3 mg/L).
- **Triglycérides** : l'équation officielle éloigne la médiane 2017-2018 de celle de 2015-2016
  (1,33 → 1,21 mmol/L, contre 1,38 en 2015-2016). Appliquée comme prévu ; à garder en tête.

Médianes des marqueurs (adultes 20-79 ans) :

| cycle | rdw | alt | ast | alp | albumin | ggt | creatinine | tg | crp | version |
|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 13.500 | 21.000 | 23.000 | 66.000 | 43.000 | 20.000 | 72.500 | 1.380 | 2.000 | brute |
| 2017 | 13.500 | 18.000 | 19.000 | 75.000 | 41.000 | 22.000 | 74.270 | 1.330 | 2.020 | brute |
| 2015 | 12.720 | 21.000 | 23.000 | 66.000 | 43.000 | 20.000 | 72.500 | 1.380 | 2.000 | harmonisee |
| 2017 | 12.800 | 20.920 | 23.100 | 68.230 | 42.920 | 20.060 | 71.920 | 1.210 | 1.980 | harmonisee |

## CRP standard (≤ 2010) contre hs-CRP (2015-2016)

**Concordance non vérifiable formellement** : NHANES ne documente pas la comparaison entre le
dosage standard (néphélométrie, mg/dL) et la hs-CRP (DxC), aucun échantillon n'a été dosé par les
deux méthodes, et 2011-2014 n'ont pas de CRP. Vérification descriptive : quantiles (mg/L, plancher
0,1) par strate. Les écarts 2009-10 → 2015-16 sont du même ordre que ceux de 2005-06 → 2009-10, ce
qui est compatible avec une concordance au-dessus du plancher, sans la démontrer.

| sexe | age | p50 2005 | p50 2009 | p50 2015 | p75 2005 | p75 2009 | p75 2015 | p90 2005 | p90 2009 | p90 2015 |
|---|---|---|---|---|---|---|---|---|---|---|
| Femme | 20-39 | 3.3 | 2.0 | 2.1 | 7.4 | 5.3 | 5.4 | 14.8 | 11.4 | 11.7 |
| Femme | 40-59 | 2.8 | 2.4 | 2.6 | 7.0 | 5.6 | 6.2 | 13.2 | 11.7 | 12.9 |
| Femme | 60-79 | 3.0 | 2.7 | 2.7 | 6.5 | 5.7 | 5.8 | 13.6 | 12.2 | 11.4 |
| Homme | 20-39 | 1.1 | 1.2 | 1.1 | 3.0 | 2.9 | 2.9 | 6.4 | 6.0 | 6.5 |
| Homme | 40-59 | 1.9 | 1.6 | 1.8 | 4.1 | 3.6 | 3.9 | 8.0 | 7.6 | 7.3 |
| Homme | 60-79 | 2.3 | 2.0 | 1.9 | 5.1 | 4.3 | 4.6 | 12.2 | 9.3 | 9.2 |

## Résultats (versions brute et harmonisée)

| Version | Cycles | n | Décès | Suivi médian (mois) | C | Gain de C vs âge + sexe | HR / ET d'écart | Obs. / prédit 3 ans | Pente 3 ans | Écart moyen (ans) |
|---|---|---|---|---|---|---|---|---|---|---|
| brute | 2015-2016 | 4341 | 118 | 47 | 0.861 [0.826; 0.893] | +0.048 [+0.027; +0.070] | 2.18 [1.92; 2.48] | 0.82 [0.67; 1.01] | 1.07 [0.94; 1.21] | +1.15 |
| brute | 2017-2018 | 4064 | 44 | 24 | 0.818 [0.743; 0.892] | +0.061 [+0.017; +0.106] | 2.34 [1.89; 2.90] | 0.58 [0.37; 0.89] | 0.95 [0.73; 1.17] | +2.62 |
| brute | 2015-2018 | 8405 | 162 | 36 | 0.848 [0.812; 0.877] | +0.050 [+0.030; +0.070] | 2.21 [1.97; 2.47] | 0.68 [0.57; 0.81] | 1.02 [0.91; 1.14] | +1.86 |
| harmonisee | 2015-2016 | 4341 | 118 | 47 | 0.860 [0.825; 0.892] | +0.048 [+0.027; +0.070] | 2.19 [1.92; 2.48] | 0.98 [0.79; 1.20] | 1.08 [0.94; 1.22] | -1.02 |
| harmonisee | 2017-2018 | 4063 | 44 | 24 | 0.820 [0.738; 0.889] | +0.062 [+0.020; +0.109] | 2.33 [1.89; 2.88] | 0.78 [0.50; 1.20] | 0.95 [0.74; 1.17] | -1.16 |
| harmonisee | 2015-2018 | 8404 | 162 | 36 | 0.850 [0.815; 0.882] | +0.051 [+0.033; +0.073] | 2.22 [1.99; 2.47] | 0.86 [0.72; 1.02] | 1.03 [0.92; 1.15] | -1.08 |

Écarts moyens par système :

| version | cycles | cardiovasculaire | metabolique | renal | hepatique | inflammatoire_hematologique |
|---|---|---|---|---|---|---|
| brute | 2015-2016 | +0.50 | +0.02 | +0.06 | -1.39 | +2.28 |
| brute | 2017-2018 | +0.04 | +0.01 | +0.06 | +1.90 | +2.19 |
| brute | 2015-2018 | +0.27 | +0.01 | +0.06 | +0.20 | +2.23 |
| harmonisee | 2015-2016 | +0.50 | +0.02 | +0.06 | -1.39 | -0.29 |
| harmonisee | 2017-2018 | -0.11 | +0.01 | +0.13 | -0.65 | -0.76 |
| harmonisee | 2015-2018 | +0.21 | +0.01 | +0.09 | -1.03 | -0.52 |

Repère : écart moyen en validation 2007-2010 = −1,44 an.

## Lecture

- **Les changements de laboratoire déplacent fortement l'âge biologique.** En version brute,
  l'écart moyen passe à +1,2 an (2015-16) et +2,6 ans (2017-18) ; harmonisé, il revient à −1,0 et
  −1,2 an, proche de la validation (−1,4). Le RDW explique l'essentiel en 2015-16 (système
  inflammatoire/hémato. +2,3 → −0,3 an) ; en 2017-18 s'ajoute la biochimie (hépatique +1,9 → −0,7).
- **Le classement est robuste aux dosages** : C, gain de C et HR quasi identiques entre les deux
  versions (C 0,85 ; gain +0,05 ; HR 2,2 par écart-type) — les décalages de laboratoire touchent
  tout le monde de la même façon.
- **La calibration en dépend** : à 3 ans, rapport observé/prédit 0,68 en brut (risque surestimé
  de 32 %) contre 0,86 [0,72 ; 1,02] harmonisé (0,98 en 2015-16).

## Note pour le point 4 (transposition)

Le **recalage par quantiles par strates d'âge et de sexe** est une méthode candidate pour la
transposition à une autre cohorte : il aligne la distribution d'un marqueur sur celle de la
population d'entraînement sans données de survie. Sa limite : il efface aussi les vraies
différences de distribution entre populations (ici, entre cycles). À n'utiliser que lorsqu'un
changement de méthode est documenté, ou en analyse de sensibilité.
