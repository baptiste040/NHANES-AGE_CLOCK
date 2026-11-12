# Protéines totales (`protein`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +10 % / −9 % en 6 mois (borne basse (2 semaines)).
2. Pièges : seuils inadaptés pour : très actifs; très actifs (F).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 6,74–7,66 ; HR 1,2 sous 6,71 et HR 1,2 au-dessus de 7,61 ; marqueur de maladie probable (seuil bas hors IC (6.45) sans les décès précoces).

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 3,6 % (jeu nhanes3) ; CV à 6 mois : 3,6 %.
- Changement détectable à 6 mois, 20-79 ans : +10 % / −9 % ; 30-55 ans : +10 % / −9 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,5 % (ratio 0,05) ; heure : +1,4 % (ratio 0,14) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : très actifs; très actifs (F).
- Plus grand décalage : très actifs, −1,7 % (0,18 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : anomalie isolée peu informative.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,03 (événement 5) ; négligeable au regard du bruit.
- Entre deux laboratoires de routine (littérature) : changement détectable +12 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 7,15 ; zone de risque minimal 6,74–7,66.
- Seuils HR 1,2 retenus : bas 6,71, haut 7,61.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Sans les décès des 3 premières années : seuil bas hors IC (6.45) (marqueur de maladie probable).
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement (alcool compris); haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 14 %; haut : 18 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/protein.png`.
