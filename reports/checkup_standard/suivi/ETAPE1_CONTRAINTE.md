# Suivi, étape 1 — variante « sang seul contrainte »

Protocole et prédiction : `DECISIONS.md` (« Suivi, étape 1 »), commité avant l'évaluation
(`e886322`). Code : `src/aging_clock/contrainte.py`. Sorties : `reports/checkup_sang_seul/contrainte/`.

**Contrainte clinique** : une valeur au-delà de la limite normale (seuils de Q2) ne peut jamais
rendre le score plus favorable que la valeur limite. Elle s'applique à chaque modèle (global et
systèmes), sans réentraînement.

## Validation 2007-2010 (9 276 personnes, 978 décès)

| Score | C contraint [IC 95 %] | C non contraint | Différence appariée [IC 95 %] | Gain vs âge + sexe | Obs./prédit ; pente [IC] |
|---|---|---|---|---|---|
| Global | 0,850 [0,839 ; 0,862] | 0,850 | **+0,0008** [+0,0001 ; +0,0016] | +0,044 [0,037 ; 0,050] | 0,90 ; 0,99 [0,94 ; 1,04] |
| Cardiovasculaire | 0,810 | 0,810 | −0,0001 [−0,0002 ; +0,0001] | +0,003 | 0,92 ; 0,95 [0,89 ; 1,01] |
| Métabolique | 0,811 | 0,811 | 0 | +0,005 | 0,95 ; 0,98 |
| Rénal | 0,820 | 0,820 | 0 | +0,013 | 0,96 ; 0,99 |
| Hépatique | 0,831 | 0,830 | +0,0005 [+0,0001 ; +0,0009] | +0,024 | 0,95 ; 1,02 |
| Inflammatoire | 0,833 | 0,833 | +0,0002 [−0,0004 ; +0,0010] | +0,027 | 0,94 ; 0,99 |

**Règle de décision** : perte < 0,005 de C sur le global. La variante contrainte ne perd rien : elle
**gagne** légèrement (+0,0008). Elle est **adoptée**, et la prédiction du développement (+0,0001)
allait dans le même sens.

## Qui voit son score changer, et de combien

| Score | Personnes concernées | Changement médian | 90ᵉ centile | Maximum |
|---|---|---|---|---|
| Global | 4 263 (46,0 %) | +0,22 an | +2,08 | +8,0 |
| Cardiovasculaire | 3 308 (35,7 %) | +0,33 | +0,43 | +0,43 |
| Hépatique | 1 020 (11,0 %) | +0,72 | +1,98 | +2,5 |
| Inflammatoire | 1 724 (18,6 %) | +0,46 | +3,40 | +8,2 |
| Métabolique, rénal | 0 | — | — | — |

Tous les changements vont dans le sens moins favorable, par construction.

## Signalement « à revoir par le médecin » (récompense indue > 1 an sur le système)

| | Personnes signalées | Par marqueur |
|---|---|---|
| Sans contrainte | 823 (8,9 %) | ALAT 375, VGM 330, lymphocytes 78, leucocytes 59 |
| Avec contrainte | 0 (par construction) | — |

Avec le seuil matériel de 1 an, la proportion de personnes signalées tombe de 51 % (règle sans
seuil) à 8,9 %. Le cholestérol, dont la récompense est d'environ 0,2 an, ne déclenche plus de
signalement.

## Note sur les systèmes cardiovasculaire et métabolique « sang seul »

La mortalité toutes causes à 10 ans **sous-estime l'importance des facteurs de risque
cardiovasculaire** (lipides, glycémie) :
- ils agissent sur des décennies ;
- ils sont souvent déjà traités dans les données (statines, antidiabétiques), ce qui atténue leur
  association avec le décès ;
- leur rôle causal est établi à plus long terme et sur des événements non mortels (infarctus,
  AVC).

Leur faible gain de C ici (+0,003 et +0,005) ne signifie **pas** qu'ils sont inutiles. Cela
signifie que ce modèle de mortalité n'est pas le bon outil pour les juger, et ces systèmes ne
doivent pas être présentés comme inutiles. C'est une interprétation, non testée ici : elle
demanderait des données d'incidence cardiovasculaire.
