# DFGe (CKD-EPI 2021) (`egfr`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +25 % / −20 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,59); décalage de +13 % chez les personnes « très actifs » (0,56 fois le changement détectable).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 68,7–102 ; HR 1,2 sous 66,4 et HR 1,2 au-dessus de 101.

Couverture : Q1 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 8,0 % (jeu nhanes3) ; CV à 6 mois : 8,0 %.
- Changement détectable à 6 mois, 20-79 ans : +25 % / −20 % ; 30-55 ans : +24 % / −19 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, +13,5 % (0,56 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- R tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,59 (événement 1) ; un changement de laboratoire peut créer un faux changement.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 82,7 ; zone de risque minimal 68,7–102.
- Seuils HR 1,2 retenus : bas 66,4, haut 101.
- Comparaison aux bornes D1 : R bas : intervalle trop large; R les deux : relation en U non signalée.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 2 %; haut : 53 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/egfr.png`.
