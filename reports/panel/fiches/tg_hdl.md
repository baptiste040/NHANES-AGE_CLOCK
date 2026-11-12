# TG/HDL (`tg_hdl`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +141 % / −58 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme non répliquée, zone de risque minimal 0,544–18,5.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 32,5 % (jeu nhanes3) ; CV à 6 mois : 32,5 %.
- Changement détectable à 6 mois, 20-79 ans : +141 % / −58 % ; 30-55 ans : +143 % / −59 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : favorisée, −28,2 % (0,48 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,02 (événement 13) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : non répliquée ; minimum 2,92 ; zone de risque minimal 0,544–18,5.
- Seuils HR 1,2 retenus : bas —, haut —.
- Comparaison aux bornes D1 : —.
- Figure : `../figures_q6/tg_hdl.png`.
