# LDL/HDL (`ldl_hdl`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +70 % / −41 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 1,6–5,65 ; HR 1,2 sous 1,81 et HR 1,2 au-dessus de 4,54.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 19,4 % (jeu nhanes3) ; CV à 6 mois : 19,4 %.
- Changement détectable à 6 mois, 20-79 ans : +70 % / −41 % ; 30-55 ans : +76 % / −43 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, −16,8 % (0,39 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,05 (événement 13) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 2,92 ; zone de risque minimal 1,6–5,65.
- Seuils HR 1,2 retenus : bas 1,81, haut 4,54.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 26 %; haut : 5 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/ldl_hdl.png`.
