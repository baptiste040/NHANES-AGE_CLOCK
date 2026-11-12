# PAL (`alp`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +22 % / −18 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,77); décalage de −15 % chez les personnes « pilule » (0,79 fois le changement détectable).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 33–81,9 ; HR 1,2 au-dessus de 69,2.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 7,1 % (jeu nhanes3) ; CV à 6 mois : 7,1 %.
- Changement détectable à 6 mois, 20-79 ans : +22 % / −18 % ; 30-55 ans : +24 % / −19 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,0 % (ratio 0,00) ; heure : −1,5 % (ratio 0,08) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : pilule, −15,1 % (0,79 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,77 (événement 4) ; un changement de laboratoire peut créer un faux changement.
- Entre deux laboratoires de routine (littérature) : changement détectable +28 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 41,2 (sur une borne P5/P95) ; zone de risque minimal 33–81,9.
- Seuils HR 1,2 retenus : bas —, haut 69,2.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : haut : 37 % ; écart de risque de décès à 10 ans à 45 ans : +0,7 / +0,4 point (hommes / femmes).
- Figure : `../figures_q6/alp.png`.
