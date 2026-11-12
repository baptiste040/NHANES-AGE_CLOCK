# Chlorure (`cl`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +6 % / −6 % en 6 mois (borne basse (2 semaines)).
2. Pièges : pour classer, changement de méthode : +13 points (intervalle statistique D1, limite basse, événement 5).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 101–109 ; HR 1,2 sous 101 et HR 1,2 au-dessus de 108 ; marqueur de maladie probable (côté haut disparaît sans les décès précoces).

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 2,1 % (jeu nhanes3) ; CV à 6 mois : 2,1 %.
- Changement détectable à 6 mois, 20-79 ans : +6 % / −6 % ; 30-55 ans : +6 % / −6 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,1 % (ratio 0,02) ; heure : −0,1 % (ratio 0,01) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : injectable, +1,0 % (0,16 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : anomalie isolée peu informative.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,25 (événement 5) ; négligeable au regard du bruit.
- Effet sur la classification : +13 points (intervalle statistique D1, limite basse, événement 5).
- Entre deux laboratoires de routine (littérature) : changement détectable +7 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 104 ; zone de risque minimal 101–109.
- Seuils HR 1,2 retenus : bas 101, haut 108.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : conforme au risque; S F bas : intervalle trop large; S F haut : non estimable.
- Sans les décès des 3 premières années : côté haut disparaît (marqueur de maladie probable).
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 13 %; haut : 6 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/cl.png`.
