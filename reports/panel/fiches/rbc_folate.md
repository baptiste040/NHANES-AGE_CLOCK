# Folates érythrocytaires (`rbc_folate`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +30 % / −23 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (comparaison impossible sans équation de passage, ratio 2,84); décalage de +16 % chez les personnes « favorisée » (0,51 fois le changement détectable); pour classer, changement de méthode : +33 points (intervalle statistique D1, limite haute, événement 22).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 810–1,84e+03 ; HR 1,2 sous 828 et HR 1,2 au-dessus de 1,93e+03.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 9,4 % (jeu nhanes3) ; CV à 6 mois : 9,4 %.
- Changement détectable à 6 mois, 20-79 ans : +30 % / −23 % ; 30-55 ans : +31 % / −24 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −1,2 % (ratio 0,05) ; heure : −5,8 % (ratio 0,25) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, +16,1 % (0,51 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 2,84 (événement 22) ; comparaison impossible sans équation de passage.
- Effet sur la classification : +33 points (intervalle statistique D1, limite haute, événement 22).

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 1,27e+03 ; zone de risque minimal 810–1,84e+03.
- Seuils HR 1,2 retenus : bas 828, haut 1,93e+03.
- Comparaison aux bornes D1 : S H bas : non estimable; S H haut : non estimable; S F bas : non estimable; S F haut : non estimable.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 22 %; haut : 6 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/rbc_folate.png`.
