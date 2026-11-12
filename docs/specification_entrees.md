# Spécification des entrées — modèle `checkup_standard` v1.0.0

Fichier CSV, une ligne par personne, une colonne par variable, **unités canoniques** ci-dessous.
Colonne facultative `id` (recopiée en sortie). Une valeur manquante ou hors plage dans une
variable obligatoire rend les scores de la ligne manquants (motif indiqué dans `statut`).

| Variable | Unité | Système | Obligatoire | Plage acceptée | Transformation |
|---|---|---|---|---|---|
| `age` | années | — | oui | 20-79 (domaine de validité) | — |
| `sex` | 1 = homme, 2 = femme | — | oui | 1 ou 2 | — |
| `sbp` | mmHg | cardiovasculaire | oui | 70 – 260 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `dbp` | mmHg | cardiovasculaire | oui | 30 – 150 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `total_chol` | mmol/L | cardiovasculaire | oui | 1.5 – 15 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `hdl` | mmol/L | cardiovasculaire | oui | 0.2 – 5 | log, spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `tg` | mmol/L | cardiovasculaire | oui | 0.2 – 30 | log, bornée aux percentiles 0,5-99,5 du développement |
| `heart_rate` | bpm | cardiovasculaire | oui | 30 – 200 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `glucose` | mmol/L | metabolique | oui | 2 – 35 | log, bornée aux percentiles 0,5-99,5 du développement |
| `hba1c` | % | metabolique | oui | 3 – 18 | bornée aux percentiles 0,5-99,5 du développement |
| `bmi` | kg/m2 | metabolique | oui | 13 – 80 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `waist` | cm | metabolique | oui | 50 – 200 | bornée aux percentiles 0,5-99,5 du développement |
| `creatinine` | umol/L | renal | oui | 20 – 1500 | log, spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `acr` | mg/mmol | renal | oui | 0 – 500 | plancher 0.1, log, bornée aux percentiles 0,5-99,5 du développement |
| `alt` | U/L | hepatique | oui | 3 – 2000 | log, spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `ast` | U/L | hepatique | oui | 3 – 2000 | log, bornée aux percentiles 0,5-99,5 du développement |
| `ggt` | U/L | hepatique | oui | 3 – 3000 | log, bornée aux percentiles 0,5-99,5 du développement |
| `alp` | U/L | hepatique | oui | 10 – 1500 | log, bornée aux percentiles 0,5-99,5 du développement |
| `albumin` | g/L | hepatique | oui | 15 – 60 | bornée aux percentiles 0,5-99,5 du développement |
| `crp` | mg/L | inflammatoire_hematologique | oui | 0 – 300 | plancher 0.1, log, bornée aux percentiles 0,5-99,5 du développement |
| `wbc` | 10^9/L | inflammatoire_hematologique | oui | 1 – 50 | log, bornée aux percentiles 0,5-99,5 du développement |
| `lymph_pct` | % | inflammatoire_hematologique | oui | 2 – 90 | bornée aux percentiles 0,5-99,5 du développement |
| `rdw` | % | inflammatoire_hematologique | oui | 9 – 30 | bornée aux percentiles 0,5-99,5 du développement |
| `mcv` | fL | inflammatoire_hematologique | oui | 55 – 130 | bornée aux percentiles 0,5-99,5 du développement |
| `hb` | g/dL | inflammatoire_hematologique | oui | 6 – 20 | spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `platelets` | 10^9/L | inflammatoire_hematologique | oui | 20 – 1000 | log, spline (4 nœuds), bornée aux percentiles 0,5-99,5 du développement |
| `ldl` | mmol/L | cardiovasculaire | non | — | non utilisée |
| `htn_treated` | 0/1 | cardiovasculaire | non | — | non utilisée |
| `lipid_treated` | 0/1 | cardiovasculaire | non | — | non utilisée |
| `urea` | mmol/L | renal | non | — | non utilisée |

Conversions vers l'unité canonique (multiplier la valeur) :

- `total_chol` : mg/dL → × 0.02586, g/L → × 2.586
- `hdl` : mg/dL → × 0.02586, g/L → × 2.586
- `tg` : mg/dL → × 0.01129, g/L → × 1.129
- `glucose` : mg/dL → × 0.05551, g/L → × 5.551
- `hba1c` : mmol/mol → 0.09148 × valeur + 2.152
- `creatinine` : mg/dL → × 88.42, mg/L → × 8.842
- `acr` : mg/g → × 0.1131
- `albumin` : g/dL → × 10
- `crp` : mg/dL → × 10
- `hb` : g/L → × 0.1, mmol/L → × 1.611

## Avertissements

- Un âge biologique absolu n'est interprétable que si les dosages de la cohorte d'application sont comparables à ceux du développement (section reference_lab_methods) ou harmonisés. Un changement d'automate peut décaler l'âge biologique de plusieurs années sans changer le classement des personnes (validation secondaire 2015-2018).
- Le score décrit un risque de mortalité toutes causes, pas l'effet protecteur des traitements ; ce n'est pas un outil de diagnostic.
- Le risque absolu est surestimé chez les groupes favorisés (revenu élevé, diplôme universitaire) : sans recalibrage local, l'âge biologique d'une cohorte de check-up de prévention sera probablement surestimé ; le classement reste valide.
- Domaine de validité : adultes de 20 à 79 ans ; valeurs dans les plages de variables[*].range ; unités canoniques de variables[*].unit.

## Sorties

`age_bio_global`, `ecart_global` (âge biologique − âge), `age_bio_<système>` et
`ecart_<système>` pour chaque système, `risque_deces_10ans`, `statut` (ok, ou motifs).

Commande : `python -m aging_clock score --input fichier.csv [--output scores.csv]`.
