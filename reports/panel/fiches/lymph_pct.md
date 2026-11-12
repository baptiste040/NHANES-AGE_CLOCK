# Lymphocytes (%) (`lymph_pct`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +47 % / −32 % en 6 mois (extrapolé à 6 mois).
2. Pièges : une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme descendante, zone de risque minimal 24,4–52,8 ; HR 1,2 sous 25,2.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 13,9 % (jeu nhanes3) ; CV à 6 mois : 14,0 %.
- Changement détectable à 6 mois, 20-79 ans : +47 % / −32 % ; 30-55 ans : +46 % / −31 %.
- Statut : extrapolé à 6 mois.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +0,3 % (ratio 0,01) ; heure : −6,7 % (ratio 0,21) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, +12,0 % (0,26 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,08 (événement 17) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : descendante ; minimum 33,5 ; zone de risque minimal 24,4–52,8.
- Seuils HR 1,2 retenus : bas 25,2, haut —.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop strict; S F bas : intervalle trop large; S F haut : intervalle trop strict.
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 26 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,6 point (hommes / femmes).
- Figure : `../figures_q6/lymph_pct.png`.
