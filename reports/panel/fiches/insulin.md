# Insuline (à jeun) (`insulin`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +115 % / −54 % en 6 mois (borne basse (2 semaines)) ; la meilleure intervention étudiée (Activité physique (toutes formes)) atteint 0,37 fois ce seuil : visible seulement en moyenne de groupe.
2. Pièges : décalage de −33 % chez les personnes « très actifs » (0,61 fois le changement détectable); pour classer, changement de méthode : +6 points (intervalle statistique D1, limite basse, événement 9); une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 4,79–17,1 ; HR 1,2 sous 5,4 et HR 1,2 au-dessus de 17,2.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 28,2 % (jeu nhanes3) ; CV à 6 mois : 28,2 %.
- Changement détectable à 6 mois, 20-79 ans : +115 % / −54 % ; 30-55 ans : +120 % / −55 %.
- Statut : borne basse (2 semaines).
- Interventions étudiées : 2 ; la plus forte, Activité physique (toutes formes) (surpoids ou stéatose), −19,8 %, ratio 0,37 : visible seulement en moyenne de groupe.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +11,1 % (ratio 0,10) ; heure : −8,4 % (ratio 0,16) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, −33,4 % (0,61 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,42 (événement 9) ; négligeable au regard du bruit.
- Effet sur la classification : +6 points (intervalle statistique D1, limite basse, événement 9).

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 10,2 ; zone de risque minimal 4,79–17,1.
- Seuils HR 1,2 retenus : bas 5,4, haut 17,2.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel; haut : association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 22 %; haut : 17 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/insulin.png`.
