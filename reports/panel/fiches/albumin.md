# Albumine (`albumin`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +13 % / −11 % en 6 mois (borne basse (2 semaines)).
2. Pièges : pour classer, changement de méthode : +7 points (intervalle statistique D1, limite basse, événement 5); une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme descendante, zone de risque minimal 4,18–5,1 ; HR 1,2 sous 4,55.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 4,4 % (jeu nhanes3) ; CV à 6 mois : 4,4 %.
- Changement détectable à 6 mois, 20-79 ans : +13 % / −11 % ; 30-55 ans : +13 % / −11 %.
- Statut : borne basse (2 semaines).

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −0,8 % (ratio 0,07) ; heure : +1,4 % (ratio 0,11) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : pilule, −2,5 % (0,23 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,39 (événement 5) ; négligeable au regard du bruit.
- Effet sur la classification : +7 points (intervalle statistique D1, limite basse, événement 5).

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : descendante ; minimum 4,8 (sur une borne P5/P95) ; zone de risque minimal 4,18–5,1.
- Seuils HR 1,2 retenus : bas 4,55, haut —.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop strict; S F bas : intervalle trop large; S F haut : intervalle trop strict.
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 78 % ; écart de risque de décès à 10 ans à 45 ans : +0,7 / +0,4 point (hommes / femmes).
- Interaction avec l'âge répliquée : lire les seuils par tranche d'âge.
- Figure : `../figures_q6/albumin.png`.
