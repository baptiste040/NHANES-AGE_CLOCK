# GGT (`ggt`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +53 % / −35 % en 6 mois (borne basse (2 semaines)) ; la meilleure intervention étudiée (Alimentation méditerranéenne) atteint 0,31 fois ce seuil : visible seulement en moyenne de groupe.
2. Pièges : décalage de −19 % chez les personnes « très actifs » (0,54 fois le changement détectable).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 7–33,6 ; HR 1,2 au-dessus de 31,2.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 15,5 % (jeu nhanes3) ; CV à 6 mois : 15,5 %.
- Changement détectable à 6 mois, 20-79 ans : +53 % / −35 % ; 30-55 ans : +54 % / −35 %.
- Statut : borne basse (2 semaines).
- Interventions étudiées : 1 ; la plus forte, Alimentation méditerranéenne (adultes), −10,9 %, ratio 0,31 : visible seulement en moyenne de groupe.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −2,7 % (ratio 0,08) ; heure : +4,3 % (ratio 0,08) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, −18,9 % (0,54 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,18 (événement 5) ; négligeable au regard du bruit.
- Entre deux laboratoires de routine (littérature) : changement détectable +55 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 16 ; zone de risque minimal 7–33,6.
- Seuils HR 1,2 retenus : bas —, haut 31,2.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : haut : 27 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/ggt.png`.
