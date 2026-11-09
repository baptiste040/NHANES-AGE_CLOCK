# Benchmark PhenoAge — validation 2007-2010

Panel et modèle principaux gelés (point 4) ; protocole écrit avant exécution (`DECISIONS.md`, 5a).
Trois scores sur les mêmes participants. Différences de C par bootstrap **apparié**
(mêmes tirages pour les scores comparés).

- **PhenoAge publié** : coefficients de Levine et al. 2018 (tableau 1), équation complète de la
  correction de Liu et al., PLoS Med 2019 (constantes 141,50 et 0,09165). Pas de réentraînement.
- **PhenoAge réentraîné** : ses 9 marqueurs, méthode du score principal (Cox âge + sexe,
  transformations du panel, pénalisation par CV sur 1999-2006).
- Accélération : écart d'âge pour nos scores ; résidu PhenoAge ~ âge (régression estimée sur le
  développement) pour PhenoAge publié. HR par écart-type, ajusté âge + sexe.
- Calibration à 10 ans : M (risque à 10 ans) pour PhenoAge publié ; risque à 10 ans du Cox pour
  les versions réentraînées.
- Limite : glycémie non à jeun dans NHANES ici ; PhenoAge a été conçu sur des sujets à jeun.

## Validation complète

C de référence (Cox âge + sexe) : 0.807 [0.794; 0.819].

| Score | n | Décès | C (IC95) | Gain de C vs âge + sexe | HR / ET d'accélération | Obs./prédit 10 ans | Pente |
|---|---|---|---|---|---|---|---|
| Score global (panel complet) | 9247 | 972 | 0.853 [0.841; 0.864] | +0.046 [0.040; 0.053] | 2.01 [1.91; 2.11] | 0.92 | 0.99 [0.94; 1.04] |
| PhenoAge réentraîné (9 marqueurs, notre méthode) | 9247 | 972 | 0.837 [0.825; 0.849] | +0.030 [0.024; 0.035] | 1.74 [1.66; 1.83] | 0.97 | 1.01 [0.95; 1.06] |
| PhenoAge publié (Levine 2018) | 9247 | 972 | 0.831 [0.820; 0.844] | +0.025 [0.018; 0.031] | 1.48 [1.43; 1.54] | 1.21 | 0.71 [0.68; 0.74] |

| Comparaison | Différence de C (IC95, apparié) | p bootstrap |
|---|---|---|
| Score global (panel complet) − PhenoAge publié (Levine 2018) | +0.0215 [+0.0166; +0.0267] | < 0,001 |
| Score global (panel complet) − PhenoAge réentraîné (9 marqueurs, notre méthode) | +0.0163 [+0.0126; +0.0202] | < 0,001 |
| PhenoAge réentraîné (9 marqueurs, notre méthode) − PhenoAge publié (Levine 2018) | +0.0052 [+0.0017; +0.0085] | 0.004 |

## Sans antécédent déclaré

C de référence (Cox âge + sexe) : 0.796 [0.775; 0.817].

| Score | n | Décès | C (IC95) | Gain de C vs âge + sexe | HR / ET d'accélération | Obs./prédit 10 ans | Pente |
|---|---|---|---|---|---|---|---|
| Score global (panel complet) | 7123 | 431 | 0.838 [0.817; 0.858] | +0.042 [0.030; 0.053] | 2.01 [1.86; 2.17] | 0.82 | 0.99 [0.92; 1.07] |
| PhenoAge réentraîné (9 marqueurs, notre méthode) | 7123 | 431 | 0.822 [0.802; 0.842] | +0.027 [0.018; 0.035] | 1.69 [1.56; 1.83] | 0.83 | 0.97 [0.90; 1.05] |
| PhenoAge publié (Levine 2018) | 7123 | 431 | 0.816 [0.795; 0.837] | +0.020 [0.011; 0.029] | 1.38 [1.31; 1.46] | 1.18 | 0.73 [0.68; 0.78] |

| Comparaison | Différence de C (IC95, apparié) | p bootstrap |
|---|---|---|
| Score global (panel complet) − PhenoAge publié (Levine 2018) | +0.0221 [+0.0139; +0.0303] | < 0,001 |
| Score global (panel complet) − PhenoAge réentraîné (9 marqueurs, notre méthode) | +0.0153 [+0.0089; +0.0218] | < 0,001 |
| PhenoAge réentraîné (9 marqueurs, notre méthode) − PhenoAge publié (Levine 2018) | +0.0068 [+0.0023; +0.0108] | 0.004 |

## Notes

- PhenoAge publié moyen en validation : 44.0 ans pour un âge moyen de 47.9 ans.
- Corrélation entre l'écart global et l'accélération PhenoAge : 0.63.
- Pénalisation retenue pour PhenoAge réentraîné (CV 1999-2006) : 0.003.
- Bootstrap : 1000 tirages appariés, graine 42.

![Calibration](calibration.png)
