# Journal des décisions

Règle (depuis le 2026-11-09) : la cohorte de validation 2007-2010 a été **vue** lors
du jalon 1. Toute modification du panel ou du modèle se décide par validation
croisée « un cycle retiré » sur le développement (1999-2006) uniquement, jamais
d'après les résultats de validation. Les résultats de validation ne sont rapportés
qu'une fois les changements arrêtés, en signalant que le panel a évolué.

Format : date — décision — pourquoi — données utilisées pour décider.

## Jalon 1 (avant ouverture de la validation)

| Date | Décision | Pourquoi | Données |
|---|---|---|---|
| 2026-11-09 | Découpage développement 1999-2006 / validation 2007-2010 / secondaire 2015-2018 | Seuls cycles avec CRP et suivi long ; validation temporelle | — |
| 2026-11-09 | Population 20-79 ans, hors femmes enceintes | Âge NHANES plafonné à 85 (≤ 2006) puis 80 ans ; biomarqueurs modifiés par la grossesse | Documentation NHANES |
| 2026-11-09 | Systèmes : cardiovasculaire, métabolique, rénal, hépatique, inflammatoire/hématologique | Choix clinique (CRP seule trop mince) | — |
| 2026-11-09 | LDL facultatif, hors modèle | Mesuré sur le seul sous-échantillon à jeun | Documentation NHANES |
| 2026-11-09 | Plancher CRP à 0,1 mg/L avant log | Limite de détection du dosage standard ; harmonise CRP et hs-CRP | Documentation NHANES |
| 2026-11-09 | Recalibration de la créatinine 1999-2000 et 2005-2006 | Équations recommandées par NHANES | Documentation NHANES |
| 2026-11-09 | Âge et sexe jamais pénalisés | Pénaliser l'âge déforme l'échelle de l'âge biologique | Développement (essai), constat méthodologique |
| 2026-11-09 | Pénalisation ridge des marqueurs = 0 | Meilleur C moyen en CV « un cycle retiré » sur la grille [0 ; 0,003 ; 0,01 ; 0,03] | CV 1999-2006 (`penalisation_cv.csv`) |

Transparence : lors d'un test de mise au point, le C de validation a été affiché pour
3 valeurs de pénalisation (0 ; 0,01 ; 0,05) avant que le choix ne soit confié à la CV
sur le développement. La valeur retenue est celle de la CV.

## Jalon 2 (validation vue — décisions sur CV 1999-2006 uniquement)

| Date | Décision | Pourquoi | Données |
|---|---|---|---|
