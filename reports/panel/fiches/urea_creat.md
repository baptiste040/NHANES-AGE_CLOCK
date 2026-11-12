# Urée/créatinine (`urea_creat`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +68 % / −40 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,51).
3. Risque (mortalité à 10 ans, association) : forme descendante, zone de risque minimal 10,7–30 ; HR 1,2 sous 10,8.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 18,8 % (jeu nhanes3) ; CV à 6 mois : 18,8 %.
- Changement détectable à 6 mois, 20-79 ans : +68 % / −40 % ; 30-55 ans : +69 % / −41 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, +13,6 % (0,20 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,51 (événement 1) ; un changement de laboratoire peut créer un faux changement.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : descendante ; minimum 15,5 ; zone de risque minimal 10,7–30.
- Seuils HR 1,2 retenus : bas 10,8, haut —.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 20 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/urea_creat.png`.
