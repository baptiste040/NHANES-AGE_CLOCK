# Glucose sérique (non à jeun) (`glu_serum`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +33 % / −25 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 80,8–116 ; HR 1,2 au-dessus de 112.

Couverture : Q1 Q2 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 10,4 % (jeu nhanes3) ; CV à 6 mois : 10,4 %.
- Changement détectable à 6 mois, 20-79 ans : +33 % / −25 % ; 30-55 ans : +27 % / −22 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,6 % (ratio 0,05) ; heure : −6,0 % (ratio 0,24) ; catégorie : indifférent.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,08 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 89,4 ; zone de risque minimal 80,8–116.
- Seuils HR 1,2 retenus : bas —, haut 112.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 9 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/glu_serum.png`.
