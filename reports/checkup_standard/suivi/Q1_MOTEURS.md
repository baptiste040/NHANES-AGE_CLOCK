# Q1 — Changement significatif et stabilité des moteurs

Protocole pré-enregistré puis amendé (`DECISIONS.md`, « Suivi, Q1 et Q2 » et son amendement) ;
calage sur 2001-2002 (n = 388), test sur NHANES III (n = 781). Code : `src/aging_clock/suivi.py`.
Données : `Q1_Q2_predictions.json`, `Q1_Q2_nhanes3.json`, `Q1_paires_*.csv`.

> **Borne basse.** Les remesures ont lieu à environ 2 semaines, et en NHANES III à la même heure,
> avec le même protocole. Entre deux bilans à 6 mois, sans contrôle de l'heure ni du jeûne, les
> changements « sans effet réel » seront plus fréquents que ceux-ci.

## Seuils de changement significatif (modèle sang seul)

| Score | Prédit (2001-02) | NHANES III : P95 [IC 95 %] | Gaussien | Médiane de \|d\| | Compatible |
|---|---|---|---|---|---|
| Global | 5,99 | **7,14** [6,47 ; 7,54] | 6,82 | 2,02 | non (plus bruité) |
| Cardiovasculaire (lipides) | 2,69 | 2,27 [2,12 ; 2,53] | 2,20 | 0,65 | non (moins bruité) |
| Métabolique (glycémie, HbA1c) | 0,93 | 1,11 [0,95 ; 1,23] | 1,16 | 0,29 | non |
| Rénal | 4,43 | 5,88 [5,39 ; 6,31] | 5,63 | 1,44 | non (ACR) |
| Hépatique | 4,95 | 5,19 [4,74 ; 5,60] | 4,93 | 1,47 | oui |
| Inflammatoire | 4,49 | 4,79 [4,43 ; 5,52] | 4,68 | 1,33 | oui |

Modèle complet, partie biologique : global 6,20 [5,82 ; 6,63] (prédit 5,29). Les seuils des
systèmes cardiovasculaire et métabolique « sang seul » sont petits en années, parce que ces
systèmes varient peu entre personnes (étape 0). Ils ne disent presque rien de plus que l'âge.

## Stabilité des moteurs (modèle sang seul)

![Stabilité des moteurs](Q1_stabilite.png)

| Indicateur | Prédit | NHANES III [IC 95 %] | Compatible | Règle des 80 % |
|---|---|---|---|---|
| Même système prioritaire (écart standardisé) | 64,2 % | 70,4 % [67,3 ; 73,8] | non | **non affichable** |
| Même premier moteur (tous) | 62,4 % | 74,3 % [71,2 ; 77,3] | non | non affichable |
| Même trio (tous) | 27,8 % | 40,7 % [37,4 ; 44,3] | non | non affichable |
| Trio largement stable, ≥ 2/3 (tous) | 82,2 % | **89,6 %** [87,4 ; 91,7] | non | **affichable avec confiance** |
| Même premier moteur actionnable | 58,5 % | 61,1 % [57,7 ; 64,5] | oui | non affichable |
| Même trio actionnable | 28,6 % | 30,9 % [27,7 ; 34,3] | oui | non affichable |
| Trio actionnable largement stable | 74,7 % | 79,9 % [77,1 ; 82,7] | non | non affichable (juste sous 80 %) |

Modèle complet (partie biologique) : système prioritaire 76,4 % ; trio actionnable largement
stable 80,3 % [77,5 ; 83,1], **affichable** mais pas « avec confiance ».

**Par tertile d'écart global au premier bilan** (sang seul) : la stabilité augmente avec l'écart.
- Système prioritaire : 63 %, 71 %, 77 %.
- Trio actionnable largement stable : 77 %, 78 %, 84 %.

Les personnes les plus « vieilles » ont des moteurs plus nets.

**Nombre de moteurs** : 3 pour toutes les personnes de NHANES III ; 3 moteurs actionnables pour
647 sur 781, moins de 3 pour 134, aucun pour 12.

## Lecture (interprétation)

- **Le classement des systèmes n'est pas stable** : une fois sur trois, le système affiché
  « prioritaire » change entre deux prises de sang à deux semaines, sans aucun changement de santé.
- **Le premier moteur non plus** : une fois sur quatre (tous) ou presque deux sur cinq
  (actionnables), il change.
- **Ce qui est stable**, c'est un **groupe** de moteurs (au moins 2 sur 3 en commun), surtout
  sans restriction aux actionnables. Le trio actionnable est à la limite de la règle.
- NHANES III est plus stable que prévu pour les moteurs « tous », probablement en partie parce que
  la CRP y est censurée (58 % à 2,1 mg/L), ce qui fige un moteur fréquent. Les moteurs
  actionnables, eux, ont été bien prédits.

## Note sur les systèmes cardiovasculaire et métabolique « sang seul »

La mortalité toutes causes à 10 ans sous-estime l'importance des facteurs de risque
cardiovasculaire (lipides, glycémie). Ils agissent sur des décennies, ils sont souvent déjà
traités, et leur rôle causal porte aussi sur des événements non mortels. Le faible gain de C de
ces deux systèmes (+0,003 et +0,005) ne signifie pas qu'ils sont inutiles. Ils ne doivent pas être
présentés comme tels ; ce modèle de mortalité n'est simplement pas le bon outil pour les juger
(interprétation, non testée ici).

## Analyse secondaire — modèle « sang seul contraint » (non aveugle)

Reprise demandée après l'adoption de la variante contrainte (étape 1). Mêmes définitions et mêmes
règles. Prédictions de 2001-2002 commitées avant la relance (`33cb504`), mais NHANES III avait déjà
été consulté avec le modèle non contraint : **l'évaluation n'est pas aveugle**. Les résultats
pré-enregistrés ci-dessus sont inchangés. Données : `Q1_Q2_contraint_*.json`,
`Q1_comparaison_libre_contraint.csv`.

| Indicateur (NHANES III, n = 781) | Non contraint (pré-enregistré) [IC 95 %] | Contraint [IC 95 %] | Prédit contraint (2001-02) | Règle des 80 % (contraint) |
|---|---|---|---|---|
| Seuil P95 global (ans) | 7,14 [6,47 ; 7,54] | 6,99 [6,64 ; 7,54] | 5,97 (non compatible) | — |
| Seuil P95 cardiovasculaire | 2,27 [2,12 ; 2,53] | 2,21 [2,08 ; 2,43] | 2,61 (non) | — |
| Seuil P95 métabolique | 1,11 [0,95 ; 1,23] | 1,11 [0,95 ; 1,23] | 0,93 (non) | — |
| Seuil P95 rénal | 5,88 [5,39 ; 6,31] | 5,88 [5,39 ; 6,31] | 4,43 (non) | — |
| Seuil P95 hépatique | 5,19 [4,74 ; 5,60] | 5,14 [4,74 ; 5,60] | 4,95 (oui) | — |
| Seuil P95 inflammatoire | 4,79 [4,43 ; 5,52] | 4,71 [4,24 ; 5,23] | 4,43 (oui) | — |
| Même système prioritaire | 70,4 % [67,3 ; 73,8] | 71,1 % [67,7 ; 74,4] | 64,9 % (non) | non affichable |
| Même premier moteur (tous) | 74,3 % [71,2 ; 77,3] | 74,3 % [71,2 ; 77,3] | 62,4 % (non) | non affichable |
| Même trio (tous) | 40,7 % [37,4 ; 44,3] | 40,6 % [37,1 ; 44,2] | 27,8 % (non) | non affichable |
| Trio largement stable (tous) | 89,6 % [87,4 ; 91,7] | 89,6 % [87,5 ; 91,7] | 82,5 % (non) | **affichable avec confiance** |
| Même premier moteur actionnable | 61,1 % [57,7 ; 64,5] | 61,2 % [57,9 ; 64,8] | 58,2 % (oui) | non affichable |
| Même trio actionnable | 30,9 % [27,7 ; 34,3] | 31,0 % [27,8 ; 34,4] | 28,9 % (oui) | non affichable |
| Trio actionnable largement stable | 79,9 % [77,1 ; 82,7] | 79,6 % [76,8 ; 82,5] | 74,0 % (non) | non affichable (juste sous 80 %) |

Par tertile d'écart global (contraint) : système prioritaire 64 %, 72 %, 78 % ; trio actionnable
largement stable 76 %, 79 %, 85 %.

**Lecture.** La contrainte ne change aucune conclusion de Q1. Les taux de stabilité bougent de moins
d'un point. Le seuil du score global baisse de 0,15 an (7,14 → 6,99), un peu plus que les 0,1 an
attendus : en plafonnant les valeurs anormales « récompensées », la contrainte retire une partie
des fluctuations de part et d'autre de la limite normale.
