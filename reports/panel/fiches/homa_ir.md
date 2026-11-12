# HOMA-IR (`homa_ir`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +139 % / −58 % en 6 mois (borne basse (2 semaines)) ; la meilleure intervention étudiée (Alimentation méditerranéenne) atteint 0,33 fois ce seuil : visible seulement en moyenne de groupe.
2. Pièges : décalage de −36 % chez les personnes « très actifs » (0,61 fois le changement détectable); pour classer, jeûne : jusqu'à +39 points au-dessus d'un seuil illustratif si le jeûne n'est pas vérifié ; ne pas calculer sans jeûne vérifié.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 1,16–4,82 ; HR 1,2 sous 1,35 et HR 1,2 au-dessus de 4,9.

Couverture : Q1 Q2 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 32,1 % (jeu nhanes3) ; CV à 6 mois : 32,1 %.
- Changement détectable à 6 mois, 20-79 ans : +139 % / −58 % ; 30-55 ans : +142 % / −59 %.
- Statut : borne basse (2 semaines).
- Interventions étudiées : 1 ; la plus forte, Alimentation méditerranéenne (adultes), −18,9 %, ratio 0,33 : visible seulement en moyenne de groupe.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +11,7 % (ratio 0,08) ; heure : −13,7 % (ratio 0,24) ; catégorie : indifférent.
- Pour classer : jusqu'à +39 points au-dessus d'un seuil illustratif si le jeûne n'est pas vérifié ; ne pas calculer sans jeûne vérifié.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, −35,9 % (0,61 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,38 (événement 9) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 2,76 ; zone de risque minimal 1,16–4,82.
- Seuils HR 1,2 retenus : bas 1,35, haut 4,9.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 25 %; haut : 15 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/homa_ir.png`.
