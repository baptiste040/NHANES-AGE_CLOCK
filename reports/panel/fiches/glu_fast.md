# Glycémie à jeun (plasma) (`glu_fast`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +29 % / −23 % en 6 mois (borne basse (2 semaines)) ; la meilleure intervention étudiée (Alimentation méditerranéenne) atteint 0,14 fois ce seuil : visible seulement en moyenne de groupe.
2. Pièges : pour classer, jeûne : jusqu'à +31 points au seuil ADA (5,6 mmol/L) et +16 au seuil OMS si le jeûne n'est pas vérifié; pour classer, changement de méthode : +5 points (≥ 5,6 mmol/L (100 mg/dL) (ADA), événement 6).
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 91–137 ; HR 1,2 au-dessus de 122.

Couverture : Q1 Q2 Q3 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 9,3 % (jeu nhanes3) ; CV à 6 mois : 9,3 %.
- Changement détectable à 6 mois, 20-79 ans : +29 % / −23 % ; 30-55 ans : +24 % / −19 %.
- Statut : borne basse (2 semaines).
- Interventions étudiées : 2 ; la plus forte, Alimentation méditerranéenne (adultes, 57 essais contrôlés), −3,2 %, ratio 0,14 : visible seulement en moyenne de groupe.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,1 % (ratio 0,04) ; heure : −5,7 % (ratio 0,25) ; catégorie : indifférent.
- Pour classer : jusqu'à +31 points au seuil ADA (5,6 mmol/L) et +16 au seuil OMS si le jeûne n'est pas vérifié.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Note : ménopause : risque réellement plus élevé, seuil à conserver (amendement du 2026-11-12).
- Plus grand décalage : favorisée, −3,1 % (0,16 fois le changement détectable).

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,06 (événement 6) ; négligeable au regard du bruit.
- Effet sur la classification : +5 points (≥ 5,6 mmol/L (100 mg/dL) (ADA), événement 6).
- Entre deux laboratoires de routine (littérature) : changement détectable +30 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 98,6 ; zone de risque minimal 91–137.
- Seuils HR 1,2 retenus : bas —, haut 122.
- Comparaison aux bornes D1 : R OMS haut : conforme au risque; R ADA haut : intervalle trop strict.
- 30-55 ans au-delà du seuil HR 1,2 : haut : 7 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/glu_fast.png`.
