# Globulines (`globulin`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +18 % / −15 % en 6 mois (borne basse (2 semaines)).
2. Pièges : seuils inadaptés pour : très actifs; très actifs (F); une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme montante, zone de risque minimal 2,1–3,2 ; HR 1,2 au-dessus de 3,16.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 5,8 % (jeu nhanes3) ; CV à 6 mois : 5,8 %.
- Changement détectable à 6 mois, 20-79 ans : +18 % / −15 % ; 30-55 ans : +18 % / −15 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,6 % (ratio 0,04) ; heure : +1,2 % (ratio 0,07) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : très actifs; très actifs (F).
- Plus grand décalage : favorisée, −4,7 % (0,31 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,49 (événement 5) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : montante ; minimum 2,61 ; zone de risque minimal 2,1–3,2.
- Seuils HR 1,2 retenus : bas —, haut 3,16.
- Comparaison aux bornes D1 : S H bas : intervalle trop strict; S H haut : intervalle trop large; S F bas : intervalle trop strict; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : haut : 27 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/globulin.png`.
