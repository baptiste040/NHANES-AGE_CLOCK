# ASAT (`ast`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +86 % / −46 % en 6 mois (extrapolé à 6 mois) ; la meilleure intervention étudiée (Perte de poids de 5 kg) atteint 0,32 fois ce seuil : visible seulement en moyenne de groupe.
2. Pièges : pour classer, changement de méthode : +26 points (intervalle statistique D1, limite basse, événement 5); une anomalie limite se normalise souvent seule : confirmer avant de signaler.
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 18,8–33,5 ; HR 1,2 sous 18,8 et HR 1,2 au-dessus de 34,6.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 17,2 % (jeu nhanes3) ; CV à 6 mois : 22,8 %.
- Changement détectable à 6 mois, 20-79 ans : +86 % / −46 % ; 30-55 ans : +92 % / −48 %.
- Statut : extrapolé à 6 mois.
- Interventions étudiées : 1 ; la plus forte, Perte de poids de 5 kg (stéatose (NAFLD)), −14,7 %, ratio 0,32 : visible seulement en moyenne de groupe.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −3,8 % (ratio 0,08) ; heure : +7,1 % (ratio 0,08) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, +9,1 % (0,10 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : confirmer avant de signaler.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,38 (événement 5) ; négligeable au regard du bruit.
- Effet sur la classification : +26 points (intervalle statistique D1, limite basse, événement 5).
- Entre deux laboratoires de routine (littérature) : changement détectable +88 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 25,1 ; zone de risque minimal 18,8–33,5.
- Seuils HR 1,2 retenus : bas 18,8, haut 34,6.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : intervalle trop large.
- Après ajustement (tabac, alcool, IMC, diabète, revenu) : bas : mixte selon le sexe; haut : association indépendante : seuil inchangé après ajustement (alcool compris).
- 30-55 ans au-delà du seuil HR 1,2 : bas : 19 %; haut : 10 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/ast.png`.
