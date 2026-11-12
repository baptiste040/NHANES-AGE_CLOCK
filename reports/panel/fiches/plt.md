# Plaquettes (`plt`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +35 % / −26 % en 6 mois (extrapolé à 6 mois).
2. Pièges : une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 196–291 ; HR 1,2 sous 188 et HR 1,2 au-dessus de 286.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 10,9 % (jeu nhanes3) ; CV à 6 mois : 10,9 %.
- Changement détectable à 6 mois, 20-79 ans : +35 % / −26 % ; 30-55 ans : +42 % / −29 %.
- Statut : extrapolé à 6 mois.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : +1,5 % (ratio 0,04) ; heure : −1,0 % (ratio 0,04) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, −6,9 % (0,23 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,02 (événement 17) ; négligeable au regard du bruit.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 232 ; zone de risque minimal 196–291.
- Seuils HR 1,2 retenus : bas 188, haut 286.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : association indépendante : seuil inchangé après ajustement (alcool compris); haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 8 %; haut : 36 % ; écart de risque de décès à 10 ans à 45 ans : +0,9 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/plt.png`.
