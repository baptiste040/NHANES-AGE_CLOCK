# TCMH (`mch`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +5 % / −4 % en 6 mois (extrapolé à 6 mois).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 29,7–32,2 ; HR 1,2 sous 29,7 et HR 1,2 au-dessus de 32,4.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 1,4 % (jeu nhanes3) ; CV à 6 mois : 1,6 %.
- Changement détectable à 6 mois, 20-79 ans : +5 % / −4 % ; 30-55 ans : +5 % / −5 %.
- Statut : extrapolé à 6 mois.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,1 % (ratio 0,02) ; heure : −0,5 % (ratio 0,11) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : pilule, +1,9 % (0,41 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,28 (événement 17) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 31,3 ; zone de risque minimal 29,7–32,2.
- Seuils HR 1,2 retenus : bas 29,7, haut 32,4.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement (alcool compris); haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 27 %; haut : 15 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/mch.png`.
