# Créatinine (`creat`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +21 % / −17 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (comparaison impossible sans équation de passage, ratio 1,19); décalage de −10 % chez les personnes « très actifs » (0,58 fois le changement détectable); pour classer, changement de méthode : −13 points (intervalle statistique D1, limite basse, événement 1).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 0,66–1,09 ; HR 1,2 au-dessus de 1,09.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 6,8 % (jeu nhanes3) ; CV à 6 mois : 6,8 %.
- Changement détectable à 6 mois, 20-79 ans : +21 % / −17 % ; 30-55 ans : +21 % / −17 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,2 % (ratio 0,06) ; heure : −1,4 % (ratio 0,08) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, −10,0 % (0,58 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 1,19 (événement 4) ; comparaison impossible sans équation de passage.
- Effet sur la classification : −13 points (intervalle statistique D1, limite basse, événement 1).
- Entre deux laboratoires de routine (littérature) : changement détectable +23 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 0,872 ; zone de risque minimal 0,66–1,09.
- Seuils HR 1,2 retenus : bas —, haut 1,09.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : conforme au risque.
- Après ajustement (tabac, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 12 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,6 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/creat.png`.
