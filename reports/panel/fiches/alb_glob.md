# Albumine/globulines (`alb_glob`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +18 % / −15 % en 6 mois (borne basse (2 semaines)).
2. Pièges : changement de méthode ou de laboratoire (un changement de laboratoire peut créer un faux changement, ratio 0,74).
3. Risque (mortalité à 10 ans, association) : forme descendante, zone de risque minimal 1,38–2,14 ; HR 1,2 sous 1,48.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 5,9 % (jeu 2001_2002) ; CV à 6 mois : 5,9 %.
- Changement détectable à 6 mois, 20-79 ans : +18 % / −15 % ; 30-55 ans : +17 % / −15 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, +6,7 % (0,39 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,74 (événement 5) ; un changement de laboratoire peut créer un faux changement.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : descendante ; minimum 1,88 (sur une borne P5/P95) ; zone de risque minimal 1,38–2,14.
- Seuils HR 1,2 retenus : bas 1,48, haut —.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 48 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,4 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/alb_glob.png`.
