# Indice SII (`sii`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +119 % / −54 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 245–713 ; HR 1,2 sous 243 et HR 1,2 au-dessus de 701 ; marqueur de maladie probable (seuil bas hors IC (174) sans les décès précoces).

Couverture : Q1 Q3 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 28,8 % (jeu nhanes3) ; CV à 6 mois : 28,8 %.
- Changement détectable à 6 mois, 20-79 ans : +119 % / −54 % ; 30-55 ans : +97 % / −49 %.
- Statut : borne basse (2 semaines).

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, −16,7 % (0,34 fois le changement détectable).

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 429 ; zone de risque minimal 245–713.
- Seuils HR 1,2 retenus : bas 243, haut 701.
- Comparaison aux bornes D1 : —.
- Sans les décès des 3 premières années : seuil bas hors IC (174) (marqueur de maladie probable).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 6 %; haut : 26 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/sii.png`.
