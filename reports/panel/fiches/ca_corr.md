# Calcium corrigé (`ca_corr`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +9 % / −8 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 8,34–9,26 ; HR 1,2 sous 8,49 et HR 1,2 au-dessus de 9,27 ; marqueur de maladie probable (côté bas disparaît sans les décès précoces).

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 3,0 % (jeu nhanes3) ; CV à 6 mois : 3,0 %.
- Changement détectable à 6 mois, 20-79 ans : +9 % / −8 % ; 30-55 ans : +9 % / −8 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : pilule, +1,1 % (0,13 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,06 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 8,95 ; zone de risque minimal 8,34–9,26.
- Seuils HR 1,2 retenus : bas 8,49, haut 9,27.
- Comparaison aux bornes D1 : —.
- Sans les décès des 3 premières années : côté bas disparaît (marqueur de maladie probable).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 2 %; haut : 39 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/ca_corr.png`.
