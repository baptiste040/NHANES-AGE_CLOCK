# FIB-4 (`fib4`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +61 % / −38 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 0,646–1,54 ; HR 1,2 sous 0,723 et HR 1,2 au-dessus de 1,62.

Couverture : Q1 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 17,3 % (jeu nhanes3) ; CV à 6 mois : 17,3 %.
- Changement détectable à 6 mois, 20-79 ans : +61 % / −38 % ; 30-55 ans : +69 % / −41 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, +8,5 % (0,12 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,30 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 1,09 ; zone de risque minimal 0,646–1,54.
- Seuils HR 1,2 retenus : bas 0,723, haut 1,62.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 43 %; haut : 3 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/fib4.png`.
