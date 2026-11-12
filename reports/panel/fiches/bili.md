# Bilirubine totale (`bili`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +66 % / −40 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,90); pour classer, changement de méthode : +14 points (intervalle statistique D1, limite basse, événement 5).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 0,706–1,8 ; HR 1,2 sous 0,712 et HR 1,2 au-dessus de 1,41 ; marqueur de maladie probable (côté haut disparaît sans les décès précoces).

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 18,4 % (jeu 2001_2002) ; CV à 6 mois : 18,4 %.
- Changement détectable à 6 mois, 20-79 ans : +66 % / −40 % ; 30-55 ans : +68 % / −41 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −3,5 % (ratio 0,09) ; heure : +0,0 % (ratio 0,00) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, +12,5 % (0,18 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : anomalie isolée peu informative.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,90 (événement 4) ; un changement de laboratoire peut créer un faux changement.
- Effet sur la classification : +14 points (intervalle statistique D1, limite basse, événement 5).
- Entre deux laboratoires de routine (littérature) : changement détectable +69 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 0,941 ; zone de risque minimal 0,706–1,8.
- Seuils HR 1,2 retenus : bas 0,712, haut 1,41.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : conforme au risque; S F bas : intervalle trop large; S F haut : conforme au risque.
- Sans les décès des 3 premières années : côté haut disparaît (marqueur de maladie probable).
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 56 %; haut : 3 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,4 point (hommes / femmes).
- Figure : `../figures_q6/bili.png`.
