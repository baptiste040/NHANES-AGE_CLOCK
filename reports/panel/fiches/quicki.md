# QUICKI (`quicki`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +13 % / −12 % en 6 mois (borne basse (2 semaines)).
2. Pièges : décalage de +7 % chez les personnes « très actifs » (0,53 fois le changement détectable); pour classer, jeûne : indice défini à jeun : ne pas calculer sans jeûne vérifié.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 0,306–0,374 ; HR 1,2 sous 0,304 et HR 1,2 au-dessus de 0,363.

Couverture : Q1 Q2 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 4,5 % (jeu nhanes3) ; CV à 6 mois : 4,5 %.
- Changement détectable à 6 mois, 20-79 ans : +13 % / −12 % ; 30-55 ans : +14 % / −12 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −1,6 % (ratio 0,14) ; heure : +2,3 % (ratio 0,17) ; catégorie : indifférent.
- Pour classer : indice défini à jeun : ne pas calculer sans jeûne vérifié.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : très actifs, +7,2 % (0,53 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,28 (événement 9) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 0,328 ; zone de risque minimal 0,306–0,374.
- Seuils HR 1,2 retenus : bas 0,304, haut 0,363.
- Comparaison aux bornes D1 : —.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 16 %; haut : 27 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/quicki.png`.
