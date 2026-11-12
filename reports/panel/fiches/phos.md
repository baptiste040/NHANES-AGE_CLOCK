# Phosphate (`phos`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +30 % / −23 % en 6 mois (borne basse (2 semaines)).
2. Pièges : aucun piège majeur repéré dans Q2 à Q5.
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 2,5–4,19 ; HR 1,2 au-dessus de 4,22.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 9,4 % (jeu nhanes3) ; CV à 6 mois : 9,4 %.
- Changement détectable à 6 mois, 20-79 ans : +30 % / −23 % ; 30-55 ans : +32 % / −24 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,0 % (ratio 0,03) ; heure : −0,1 % (ratio 0,01) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : injectable, +5,4 % (0,17 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : anomalie isolée peu informative.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,40 (événement 4) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 3,68 ; zone de risque minimal 2,5–4,19.
- Seuils HR 1,2 retenus : bas —, haut 4,22.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : haut : 15 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,6 point (hommes / femmes).
- Figure : `../figures_q6/phos.png`.
