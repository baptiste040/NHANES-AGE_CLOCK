# Neutrophiles/lymphocytes (`nlr`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +97 % / −49 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 0,648–2,71 ; HR 1,2 au-dessus de 2,61.

Couverture : Q1 Q3 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 24,8 % (jeu nhanes3) ; CV à 6 mois : 24,8 %.
- Changement détectable à 6 mois, 20-79 ans : +97 % / −49 % ; 30-55 ans : +84 % / −46 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, −15,9 % (0,35 fois le changement détectable).

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 1,63 ; zone de risque minimal 0,648–2,71.
- Seuils HR 1,2 retenus : bas —, haut 2,61.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 23 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,6 point (hommes / femmes).
- Figure : `../figures_q6/nlr.png`.
