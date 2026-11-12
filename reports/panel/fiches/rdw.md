# RDW (`rdw`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +7 % / −6 % en 6 mois (extrapolé à 6 mois).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,79).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 11,3–12,6 ; HR 1,2 au-dessus de 12,4.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 2,0 % (jeu nhanes3) ; CV à 6 mois : 2,4 %.
- Changement détectable à 6 mois, 20-79 ans : +7 % / −6 % ; 30-55 ans : +7 % / −7 %.
- Statut : extrapolé à 6 mois.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,4 % (ratio 0,05) ; heure : +0,8 % (ratio 0,12) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : pilule, −3,2 % (0,47 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,79 (événement 17) ; un changement de laboratoire peut créer un faux changement.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 11,6 (sur une borne P5/P95) ; zone de risque minimal 11,3–12,6.
- Seuils HR 1,2 retenus : bas —, haut 12,4.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : intervalle trop large.
- Après ajustement (tabac, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 48 % ; écart de risque de décès à 10 ans à 45 ans : +0,7 / +0,4 point (hommes / femmes).
- Figure : `../figures_q6/rdw.png`.
