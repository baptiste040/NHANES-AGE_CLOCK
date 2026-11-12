# Leucocytes (`wbc`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +48 % / −32 % en 6 mois (extrapolé à 6 mois).
2. Pièges : une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 3,4–8,26 ; HR 1,2 sous 4,14 et HR 1,2 au-dessus de 8,1 ; marqueur de maladie probable (côté bas disparaît sans les décès précoces).

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 13,4 % (jeu 2001_2002) ; CV à 6 mois : 14,1 %.
- Changement détectable à 6 mois, 20-79 ans : +48 % / −32 % ; 30-55 ans : +47 % / −32 %.
- Statut : extrapolé à 6 mois.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,4 % (ratio 0,03) ; heure : −1,3 % (ratio 0,04) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, −9,9 % (0,31 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,06 (événement 17) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 6,06 ; zone de risque minimal 3,4–8,26.
- Seuils HR 1,2 retenus : bas 4,14, haut 8,1.
- Comparaison aux bornes D1 : S H bas : conforme au risque; S H haut : intervalle trop large; S F bas : conforme au risque; S F haut : intervalle trop large.
- Sans les décès des 3 premières années : côté bas disparaît (marqueur de maladie probable).
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : haut : association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 3 %; haut : 31 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/wbc.png`.
