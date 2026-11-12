# GGT/HDL (`ggt_hdl`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +65 % / −39 % en 6 mois (borne basse (2 semaines)).
2. Pièges : décalage de −29 % chez les personnes « favorisée » (0,76 fois le changement détectable).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 0,11–0,797 ; HR 1,2 au-dessus de 0,634.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 18,2 % (jeu nhanes3) ; CV à 6 mois : 18,2 %.
- Changement détectable à 6 mois, 20-79 ans : +65 % / −39 % ; 30-55 ans : +63 % / −38 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, −29,3 % (0,76 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,14 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 0,16 (sur une borne P5/P95) ; zone de risque minimal 0,11–0,797.
- Seuils HR 1,2 retenus : bas —, haut 0,634.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 33 % ; écart de risque de décès à 10 ans à 45 ans : +0,7 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/ggt_hdl.png`.
