# Urée (`urea`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +68 % / −40 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 11,5–17,3 ; HR 1,2 sous 11,4 et HR 1,2 au-dessus de 18.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 18,9 % (jeu nhanes3) ; CV à 6 mois : 18,9 %.
- Changement détectable à 6 mois, 20-79 ans : +68 % / −40 % ; 30-55 ans : +69 % / −41 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +2,3 % (ratio 0,03) ; heure : −5,5 % (ratio 0,14) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, +10,1 % (0,15 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : anomalie isolée peu informative.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,08 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 14,4 ; zone de risque minimal 11,5–17,3.
- Seuils HR 1,2 retenus : bas 11,4, haut 18.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement; haut : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 45 %; haut : 7 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/urea.png`.
