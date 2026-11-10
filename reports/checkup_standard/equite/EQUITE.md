# Audit d'équité — validation 2007-2010

Modèle gelé (point 4), score global, analyses non pondérées. Protocole et règle d'interprétation
fixés avant exécution (`DECISIONS.md`, 5b). n = 9276 ; écart d'âge moyen de la
validation : -1.43 an(s). Valeurs manquantes par axe : Revenu / seuil de pauvreté : 790, Niveau d'études : 9.

**Règle** — défaut de calibration : IC du rapport observé/prédit (O/P) excluant 1 et
|O/P − 1| > 0,20, ou IC de la pente excluant 1 et pente hors [0,80 ; 1,20] ; défaut de
discrimination : IC du gain de C incluant 0 ; différence de risque réelle : écart moyen différent
de la moyenne de validation sans défaut du modèle ; < 50 décès : effectif insuffisant.

| Axe | Groupe | n | Décès | C | Gain de C vs âge + sexe | Obs. / prédit 10 ans | Pente | Écart moyen (ans) | Écart médian [Q1; Q3] | Verdict (règle pré-enregistrée) |
|---|---|---|---|---|---|---|---|---|---|---|
| Sexe | Homme | 4612 | 597 | 0.847 [0.833; 0.862] | +0.048 [+0.039; +0.057] | 0.95 [0.88; 1.03] | 0.94 [0.88; 1.00] | -2.3 [-2.5; -2.0] | -3.3 [-7.6; +1.9] | différence de risque réelle (bien calibré) |
| Sexe | Femme | 4664 | 381 | 0.853 [0.836; 0.870] | +0.049 [+0.036; +0.061] | 0.86 [0.77; 0.95] | 1.06 [0.98; 1.14] | -0.6 [-0.8; -0.4] | -1.3 [-5.7; +3.4] | différence de risque réelle (bien calibré) |
| Groupe ethnique | Mexicain-américain | 1764 | 94 | 0.843 [0.794; 0.887] | +0.045 [+0.020; +0.070] | 0.65 [0.53; 0.80] | 0.97 [0.82; 1.11] | -1.8 [-2.1; -1.4] | -2.4 [-6.6; +2.1] | défaut du modèle (calibration) |
| Groupe ethnique | Autre hispanique | 1024 | 79 | 0.887 [0.854; 0.915] | +0.051 [+0.029; +0.075] | 0.84 [0.66; 1.06] | 1.19 [1.01; 1.38] | -2.2 [-2.6; -1.7] | -3.0 [-7.3; +1.8] | différence de risque réelle (bien calibré) |
| Groupe ethnique | Blanc non hispanique | 4373 | 573 | 0.849 [0.833; 0.864] | +0.049 [+0.040; +0.058] | 0.98 [0.90; 1.06] | 0.95 [0.89; 1.01] | -1.5 [-1.7; -1.3] | -2.4 [-6.7; +2.6] | pas de différence |
| Groupe ethnique | Noir non hispanique | 1684 | 202 | 0.830 [0.804; 0.856] | +0.054 [+0.036; +0.072] | 0.97 [0.85; 1.12] | 0.97 [0.86; 1.08] | -0.2 [-0.6; +0.2] | -0.9 [-5.9; +4.3] | différence de risque réelle (bien calibré) |
| Groupe ethnique | Autre / multiethnique | 431 | 30 | 0.857 [0.765; 0.928] | -0.004 [-0.036; +0.023] | 0.83 [0.58; 1.20] | 1.15 [0.87; 1.44] | -2.1 [-2.9; -1.4] | -3.0 [-7.5; +2.4] | effectif insuffisant |
| Âge | 20-39 | 3194 | 41 | 0.720 [0.641; 0.796] | +0.095 [+0.024; +0.172] | 1.15 [0.84; 1.57] | 1.00 [0.67; 1.33] | -1.0 [-1.3; -0.8] | -1.6 [-5.7; +2.8] | effectif insuffisant |
| Âge | 40-59 | 3346 | 219 | 0.774 [0.741; 0.809] | +0.116 [+0.083; +0.148] | 1.03 [0.90; 1.18] | 1.21 [1.08; 1.35] | -2.1 [-2.4; -1.9] | -3.1 [-7.7; +2.2] | défaut du modèle (calibration) |
| Âge | 60-79 | 2736 | 718 | 0.758 [0.740; 0.775] | +0.101 [+0.083; +0.120] | 0.87 [0.81; 0.94] | 1.02 [0.94; 1.09] | -1.0 [-1.3; -0.7] | -2.2 [-6.7; +3.4] | différence de risque réelle (bien calibré) |
| Revenu / seuil de pauvreté | < 1,3 | 2699 | 347 | 0.853 [0.834; 0.872] | +0.038 [+0.027; +0.048] | 1.11 [1.00; 1.23] | 0.96 [0.88; 1.03] | +0.7 [+0.4; +1.0] | -0.1 [-4.5; +5.2] | différence de risque réelle (bien calibré) |
| Revenu / seuil de pauvreté | 1,3-3,5 | 3155 | 384 | 0.848 [0.831; 0.866] | +0.038 [+0.027; +0.048] | 0.97 [0.88; 1.08] | 0.95 [0.87; 1.03] | -1.4 [-1.7; -1.2] | -2.2 [-6.5; +2.8] | pas de différence |
| Revenu / seuil de pauvreté | ≥ 3,5 | 2632 | 172 | 0.842 [0.809; 0.871] | +0.041 [+0.025; +0.058] | 0.62 [0.52; 0.73] | 0.99 [0.88; 1.10] | -3.6 [-3.8; -3.3] | -4.3 [-8.2; +0.2] | défaut du modèle (calibration) |
| Niveau d'études | < secondaire | 2681 | 387 | 0.841 [0.822; 0.860] | +0.051 [+0.039; +0.064] | 0.98 [0.89; 1.09] | 0.96 [0.89; 1.04] | -0.2 [-0.5; +0.1] | -1.1 [-5.9; +4.2] | différence de risque réelle (bien calibré) |
| Niveau d'études | Secondaire (diplôme) | 2175 | 241 | 0.842 [0.820; 0.865] | +0.041 [+0.027; +0.054] | 0.95 [0.83; 1.08] | 0.96 [0.86; 1.06] | -0.8 [-1.1; -0.5] | -1.6 [-5.9; +3.5] | différence de risque réelle (bien calibré) |
| Niveau d'études | Supérieur partiel | 2537 | 222 | 0.859 [0.834; 0.882] | +0.044 [+0.029; +0.059] | 0.92 [0.81; 1.06] | 1.03 [0.93; 1.13] | -1.5 [-1.8; -1.2] | -2.3 [-6.7; +2.5] | pas de différence |
| Niveau d'études | Diplôme universitaire | 1874 | 126 | 0.865 [0.834; 0.893] | +0.036 [+0.020; +0.054] | 0.70 [0.58; 0.84] | 0.99 [0.86; 1.12] | -3.8 [-4.1; -3.5] | -4.5 [-8.2; -0.1] | défaut du modèle (calibration) |

![O/P](calibration_groupes.png)

![Écart](ecart_groupes.png)

Écarts moyens par système et par groupe : `ecarts_par_systeme.csv`.
Interprétation (écrite après lecture des résultats) : `INTERPRETATION.md`.
