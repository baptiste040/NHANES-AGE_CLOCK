# Résultats de validation — panel `checkup_standard`

Rapport généré automatiquement par `python -m aging_clock validate --panel checkup_standard`.
Toutes les figures et tables sont dans ce dossier (CSV = vue tableau des figures).

> **Le panel a évolué depuis le jalon 1** (ajout de l'ACR urinaire au système rénal et de la
> fréquence cardiaque au système cardiovasculaire, décidés par validation croisée sur
> 1999-2006 uniquement). La cohorte 2007-2010 avait déjà été consultée au jalon 1 ; ce
> passage est l'unique consultation avec le panel final. Voir `DECISIONS.md`.
> Résultats du jalon 1 archivés dans `reports/archive/jalon1_checkup_standard/`.

- Développement : cycles NHANES 1999, 2001, 2003, 2005 ; validation temporelle : 2007, 2009.
- Mortalité : Linked Mortality Files 2019 (NCHS). Horizon de l'âge biologique : 10 ans.
- Pénalisation ridge des marqueurs choisie par validation croisée sur le développement : 0.0.
- IC à 95 % par bootstrap (1000 répliques ; 300 pour les sensibilités) ; graine 42.
- Empreinte SHA-256 du panel : `b01418dae864d6f6…`.

## Population

| etape | n |
|---|---|
| participants NHANES | 62160 |
| age 20-79 ans | 29725 |
| eligibles au chainage mortalite, suivi > 0 | 28396 |
| hors femmes enceintes | 27175 |
| cas complets sur le panel | 23179 |

| echantillon | n | deces | suivi_median_ans | age_moyen | pct_femmes | cycles |
|---|---|---|---|---|---|---|
| developpement | 13903 | 2796 | 16.1 | 47.4 | 48.7 | 1999, 2001, 2003, 2005 |
| validation | 9276 | 978 | 10.7 | 48.0 | 50.3 | 2007, 2009 |

## Discrimination et association (validation)

C de référence (Cox âge + sexe) : **0.807 [0.794; 0.819]**.

| Score | C (IC95) | Gain de C vs âge + sexe (IC95) | HR par ET d'écart (IC95) | ET de l'écart (ans) |
|---|---|---|---|---|
| Global | 0.853 [0.842; 0.865] | 0.047 [0.040; 0.053] | 2.01 [1.92; 2.12] | 7.5 |
| Cardiovasculaire | 0.819 [0.806; 0.831] | 0.012 [0.009; 0.016] | 1.41 [1.33; 1.49] | 3.7 |
| Métabolique | 0.819 [0.807; 0.832] | 0.013 [0.009; 0.016] | 1.47 [1.38; 1.56] | 3.9 |
| Rénal | 0.820 [0.807; 0.832] | 0.013 [0.010; 0.017] | 1.39 [1.33; 1.46] | 3.3 |
| Hépatique | 0.830 [0.818; 0.843] | 0.024 [0.019; 0.028] | 1.59 [1.51; 1.68] | 4.3 |
| Inflammatoire / hémato. | 0.833 [0.821; 0.845] | 0.026 [0.022; 0.031] | 1.67 [1.59; 1.75] | 5.1 |

HR par écart-type de l'écart d'âge, ajusté sur l'âge et le sexe, Cox ajusté dans l'échantillon de validation.

![HR](hr_par_ecart_type.png)

## Calibration à 10 ans (validation)

| Score | Risque prédit moyen | Risque observé (KM) | Observé / prédit | Pente (IC95) | Écart absolu moyen (déciles) |
|---|---|---|---|---|---|
| Global | 0.101 | 0.092 | 0.91 | 0.99 [0.94; 1.04] | 0.010 |
| Cardiovasculaire | 0.099 | 0.092 | 0.93 | 0.97 [0.91; 1.03] | 0.011 |
| Métabolique | 0.099 | 0.092 | 0.93 | 0.98 [0.93; 1.04] | 0.010 |
| Rénal | 0.096 | 0.092 | 0.96 | 0.99 [0.93; 1.05] | 0.007 |
| Hépatique | 0.096 | 0.092 | 0.96 | 1.02 [0.96; 1.08] | 0.006 |
| Inflammatoire / hémato. | 0.097 | 0.092 | 0.95 | 0.99 [0.93; 1.04] | 0.008 |

Pente = coefficient du log(-log(1 - risque prédit)) dans un Cox de validation (1 = idéal).

![Calibration](calibration.png)

## Indépendance des écarts par système (validation)

Corrélations de Spearman entre écarts d'âge par système :

|  | Cardiovasculaire | Métabolique | Rénal | Hépatique | Inflammatoire / hémato. |
|---|---|---|---|---|---|
| Cardiovasculaire | 1.00 | 0.19 | 0.23 | 0.13 | 0.17 |
| Métabolique | 0.19 | 1.00 | 0.17 | 0.13 | 0.16 |
| Rénal | 0.23 | 0.17 | 1.00 | 0.12 | 0.17 |
| Hépatique | 0.13 | 0.13 | 0.12 | 1.00 | 0.32 |
| Inflammatoire / hémato. | 0.17 | 0.16 | 0.17 | 0.32 | 1.00 |

![Spearman](independance_spearman.png)

Cox avec tous les écarts par système ensemble (ajusté âge et sexe) :

| Système | HR par ET, ajusté mutuellement (IC95) | p |
|---|---|---|
| Cardiovasculaire | 1.15 [1.08; 1.22] | 1.5e-05 |
| Métabolique | 1.22 [1.14; 1.30] | 4.5e-10 |
| Rénal | 1.18 [1.12; 1.24] | 1.2e-11 |
| Hépatique | 1.30 [1.23; 1.38] | 1.1e-19 |
| Inflammatoire / hémato. | 1.41 [1.33; 1.49] | 2.4e-32 |

![Cox joint](independance_cox.png)

## Sensibilités

« figé » = modèle principal appliqué au sous-échantillon de validation ;
« ré-entraîné » = modèle ré-entraîné sur le développement filtré de la même façon.
Pour les causes spécifiques, les décès d'autres causes sont censurés.

| scenario | modele | Score | n | deces | C | C_ic95 | dC | dC_ic95 | HR_par_ET | HR_ic95 |
|---|---|---|---|---|---|---|---|---|---|---|
| principal | fige | Global | 9276 | 978 | 0.853 | [0.842; 0.865] | 0.047 | [0.041; 0.053] | 2.015 | [1.92; 2.12] |
| principal | fige | Cardiovasculaire | 9276 | 978 | 0.819 | [0.806; 0.830] | 0.012 | [0.008; 0.016] | 1.411 | [1.33; 1.49] |
| principal | fige | Métabolique | 9276 | 978 | 0.819 | [0.806; 0.832] | 0.013 | [0.009; 0.016] | 1.467 | [1.38; 1.56] |
| principal | fige | Rénal | 9276 | 978 | 0.820 | [0.807; 0.832] | 0.013 | [0.010; 0.017] | 1.393 | [1.33; 1.46] |
| principal | fige | Hépatique | 9276 | 978 | 0.830 | [0.818; 0.843] | 0.024 | [0.020; 0.028] | 1.591 | [1.51; 1.68] |
| principal | fige | Inflammatoire / hémato. | 9276 | 978 | 0.833 | [0.821; 0.846] | 0.026 | [0.022; 0.031] | 1.670 | [1.59; 1.75] |
| 1. sans deces < 24 mois | fige | Global | 9172 | 874 | 0.856 | [0.846; 0.868] | 0.046 | [0.039; 0.053] | 2.006 | [1.90; 2.12] |
| 1. sans deces < 24 mois | fige | Cardiovasculaire | 9172 | 874 | 0.821 | [0.810; 0.833] | 0.011 | [0.008; 0.015] | 1.386 | [1.30; 1.47] |
| 1. sans deces < 24 mois | fige | Métabolique | 9172 | 874 | 0.824 | [0.811; 0.836] | 0.013 | [0.009; 0.017] | 1.490 | [1.40; 1.59] |
| 1. sans deces < 24 mois | fige | Rénal | 9172 | 874 | 0.823 | [0.810; 0.834] | 0.013 | [0.009; 0.017] | 1.390 | [1.33; 1.46] |
| 1. sans deces < 24 mois | fige | Hépatique | 9172 | 874 | 0.833 | [0.820; 0.844] | 0.023 | [0.018; 0.027] | 1.572 | [1.49; 1.66] |
| 1. sans deces < 24 mois | fige | Inflammatoire / hémato. | 9172 | 874 | 0.836 | [0.825; 0.848] | 0.026 | [0.021; 0.031] | 1.656 | [1.57; 1.75] |
| 1. sans deces < 24 mois | re-entraine | Global | 9172 | 874 | 0.856 | [0.845; 0.867] | 0.046 | [0.039; 0.052] | 1.999 | [1.90; 2.11] |
| 1. sans deces < 24 mois | re-entraine | Cardiovasculaire | 9172 | 874 | 0.821 | [0.809; 0.833] | 0.011 | [0.007; 0.015] | 1.376 | [1.29; 1.46] |
| 1. sans deces < 24 mois | re-entraine | Métabolique | 9172 | 874 | 0.823 | [0.811; 0.836] | 0.013 | [0.009; 0.017] | 1.488 | [1.40; 1.58] |
| 1. sans deces < 24 mois | re-entraine | Rénal | 9172 | 874 | 0.823 | [0.810; 0.834] | 0.013 | [0.009; 0.017] | 1.389 | [1.33; 1.45] |
| 1. sans deces < 24 mois | re-entraine | Hépatique | 9172 | 874 | 0.832 | [0.820; 0.843] | 0.022 | [0.018; 0.026] | 1.574 | [1.49; 1.66] |
| 1. sans deces < 24 mois | re-entraine | Inflammatoire / hémato. | 9172 | 874 | 0.835 | [0.824; 0.847] | 0.025 | [0.020; 0.030] | 1.659 | [1.57; 1.75] |
| 2. sans antecedent declare | fige | Global | 7144 | 434 | 0.838 | [0.820; 0.859] | 0.042 | [0.031; 0.052] | 2.018 | [1.87; 2.18] |
| 2. sans antecedent declare | fige | Cardiovasculaire | 7144 | 434 | 0.806 | [0.786; 0.830] | 0.010 | [0.005; 0.017] | 1.384 | [1.27; 1.51] |
| 2. sans antecedent declare | fige | Métabolique | 7144 | 434 | 0.805 | [0.784; 0.826] | 0.009 | [0.004; 0.014] | 1.437 | [1.32; 1.57] |
| 2. sans antecedent declare | fige | Rénal | 7144 | 434 | 0.804 | [0.783; 0.827] | 0.008 | [0.004; 0.012] | 1.333 | [1.25; 1.42] |
| 2. sans antecedent declare | fige | Hépatique | 7144 | 434 | 0.818 | [0.800; 0.839] | 0.022 | [0.015; 0.029] | 1.566 | [1.45; 1.69] |
| 2. sans antecedent declare | fige | Inflammatoire / hémato. | 7144 | 434 | 0.822 | [0.802; 0.844] | 0.026 | [0.019; 0.033] | 1.653 | [1.53; 1.78] |
| 2. sans antecedent declare | re-entraine | Global | 7144 | 434 | 0.837 | [0.819; 0.857] | 0.041 | [0.030; 0.051] | 2.015 | [1.86; 2.18] |
| 2. sans antecedent declare | re-entraine | Cardiovasculaire | 7144 | 434 | 0.809 | [0.790; 0.831] | 0.012 | [0.006; 0.019] | 1.428 | [1.31; 1.56] |
| 2. sans antecedent declare | re-entraine | Métabolique | 7144 | 434 | 0.805 | [0.785; 0.827] | 0.008 | [0.003; 0.013] | 1.439 | [1.32; 1.57] |
| 2. sans antecedent declare | re-entraine | Rénal | 7144 | 434 | 0.804 | [0.783; 0.827] | 0.008 | [0.004; 0.011] | 1.360 | [1.26; 1.46] |
| 2. sans antecedent declare | re-entraine | Hépatique | 7144 | 434 | 0.819 | [0.800; 0.838] | 0.022 | [0.015; 0.028] | 1.587 | [1.47; 1.71] |
| 2. sans antecedent declare | re-entraine | Inflammatoire / hémato. | 7144 | 434 | 0.822 | [0.800; 0.843] | 0.025 | [0.018; 0.032] | 1.639 | [1.52; 1.76] |
| 4. deces cardiovasculaire (cause specifique) | fige | Global | 9276 | 253 | 0.886 | [0.869; 0.904] | 0.045 | [0.029; 0.060] | 1.997 | [1.81; 2.21] |
| 4. deces cardiovasculaire (cause specifique) | fige | Cardiovasculaire | 9276 | 253 | 0.851 | [0.830; 0.872] | 0.010 | [0.003; 0.017] | 1.370 | [1.22; 1.54] |
| 4. deces cardiovasculaire (cause specifique) | fige | Métabolique | 9276 | 253 | 0.851 | [0.829; 0.871] | 0.009 | [0.002; 0.016] | 1.443 | [1.28; 1.62] |
| 4. deces cardiovasculaire (cause specifique) | fige | Rénal | 9276 | 253 | 0.860 | [0.838; 0.879] | 0.019 | [0.011; 0.027] | 1.462 | [1.35; 1.59] |
| 4. deces cardiovasculaire (cause specifique) | fige | Hépatique | 9276 | 253 | 0.863 | [0.842; 0.881] | 0.022 | [0.013; 0.031] | 1.553 | [1.40; 1.72] |
| 4. deces cardiovasculaire (cause specifique) | fige | Inflammatoire / hémato. | 9276 | 253 | 0.868 | [0.850; 0.888] | 0.026 | [0.016; 0.038] | 1.682 | [1.53; 1.85] |
| 4. deces cancer (cause specifique) | fige | Global | 9276 | 290 | 0.848 | [0.828; 0.866] | 0.037 | [0.027; 0.049] | 1.847 | [1.68; 2.03] |
| 4. deces cancer (cause specifique) | fige | Cardiovasculaire | 9276 | 290 | 0.819 | [0.800; 0.838] | 0.009 | [0.002; 0.015] | 1.341 | [1.20; 1.49] |
| 4. deces cancer (cause specifique) | fige | Métabolique | 9276 | 290 | 0.817 | [0.799; 0.836] | 0.006 | [-0.001; 0.013] | 1.309 | [1.17; 1.46] |
| 4. deces cancer (cause specifique) | fige | Rénal | 9276 | 290 | 0.816 | [0.796; 0.837] | 0.006 | [-0.000; 0.012] | 1.227 | [1.12; 1.34] |
| 4. deces cancer (cause specifique) | fige | Hépatique | 9276 | 290 | 0.832 | [0.815; 0.850] | 0.022 | [0.013; 0.031] | 1.587 | [1.44; 1.75] |
| 4. deces cancer (cause specifique) | fige | Inflammatoire / hémato. | 9276 | 290 | 0.833 | [0.815; 0.852] | 0.023 | [0.015; 0.032] | 1.614 | [1.47; 1.77] |
| 4. deces autre (cause specifique) | fige | Global | 9276 | 435 | 0.837 | [0.815; 0.857] | 0.054 | [0.044; 0.063] | 2.135 | [1.98; 2.30] |
| 4. deces autre (cause specifique) | fige | Cardiovasculaire | 9276 | 435 | 0.799 | [0.777; 0.820] | 0.016 | [0.010; 0.022] | 1.479 | [1.36; 1.61] |
| 4. deces autre (cause specifique) | fige | Métabolique | 9276 | 435 | 0.802 | [0.781; 0.822] | 0.019 | [0.011; 0.027] | 1.589 | [1.46; 1.73] |
| 4. deces autre (cause specifique) | fige | Rénal | 9276 | 435 | 0.798 | [0.775; 0.818] | 0.015 | [0.010; 0.020] | 1.458 | [1.37; 1.55] |
| 4. deces autre (cause specifique) | fige | Hépatique | 9276 | 435 | 0.809 | [0.786; 0.827] | 0.026 | [0.020; 0.033] | 1.615 | [1.49; 1.75] |
| 4. deces autre (cause specifique) | fige | Inflammatoire / hémato. | 9276 | 435 | 0.812 | [0.790; 0.833] | 0.029 | [0.021; 0.037] | 1.696 | [1.57; 1.83] |

## Effet de la correction du protocole (prototype)

| protocole | n_eval | deces_eval | C_complet | C_age | dC_age_ecart | HR_par_an_ecart | ET_ecart_ans |
|---|---|---|---|---|---|---|---|
| A. prototype (avec fuites) | 1129 |  | 0.867 | 0.847 | 0.019 | 1.100 |  |
| B. memes donnees, sans fuite | 1128 | 146.000 | 0.862 | 0.837 | 0.025 | 1.103 | 6.500 |
| C. 10 marqueurs, validation temporelle | 10088 | 1141.000 | 0.839 | 0.803 | 0.036 | 1.107 | 5.298 |
| D. panel checkup_standard, validation temporelle | 9276 | 978.000 | 0.853 | 0.807 | 0.047 | 1.098 | 7.494 |

`C_complet` : C du risque prédit par le modèle complet. `C_age` : Cox âge seul
(âge + sexe pour le panel check-up). `dC_age_ecart` : gain de C quand on ajoute
l'écart d'âge à ce Cox. A = valeurs du prototype relancé tel quel.
