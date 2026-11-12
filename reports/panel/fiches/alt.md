# ALAT (`alt`)

Fiche générée automatiquement à partir de `resultats_par_marqueur.csv` (programme « panel », Q1 à Q6). Données NHANES (américaines) ; changements détectables à partir de remesures à environ 2 semaines (bornes basses).

## Conclusion en trois lignes

1. Suivre : un changement n'est détectable chez une personne qu'à partir de +181 % / −64 % en 6 mois (extrapolé à 6 mois) ; la meilleure intervention étudiée (Alimentation méditerranéenne) atteint 0,59 fois ce seuil : limite.
2. Pièges : pour classer, changement de méthode : +10 points (intervalle statistique D1, limite basse, événement 5).
3. Risque (mortalité à 10 ans, association) : forme en U ou en J, zone de risque minimal 18,1–44 ; HR 1,2 sous 18,8 et HR 1,2 au-dessus de 45,1.

Couverture : Q1 Q2 Q3 Q4 Q5 Q6.

## Q1 : bruit de mesure et changement détectable

- CV observé : 23,4 % (jeu nhanes3) ; CV à 6 mois : 38,7 %.
- Changement détectable à 6 mois, 20-79 ans : +181 % / −64 % ; 30-55 ans : +186 % / −65 %.
- Statut : extrapolé à 6 mois.
- Interventions étudiées : 2 ; la plus forte, Alimentation méditerranéenne (adultes), −37,7 %, ratio 0,59 : limite.

## Q2 : jeûne et heure

- Effet du jeûne (même personne) : −6,2 % (ratio 0,10) ; heure : +7,5 % (ratio 0,04) ; catégorie : indifférent.

## Q3 : populations particulières

- Seuils inadaptés : aucun groupe.
- Plus grand décalage : ménopause, +15,8 % (0,08 fois le changement détectable).

## Q4 : normalisation spontanée d'une anomalie

- S tous : normalisation < 30 %.

## Q5 : changements de méthode et de laboratoire

- Plus grand décalage de méthode NHANES : ratio 0,22 (événement 5) ; négligeable au regard du bruit.
- Effet sur la classification : +10 points (intervalle statistique D1, limite basse, événement 5).
- Entre deux laboratoires de routine (littérature) : changement détectable +189 %.

## Q6 : zones fondées sur le risque de mortalité (association, pas cible)

- Forme retenue en validation : en U ou en J ; minimum 28,3 ; zone de risque minimal 18,1–44.
- Seuils HR 1,2 retenus : bas 18,8, haut 45,1.
- Comparaison aux bornes D1 : S H bas : intervalle trop large; S H haut : intervalle trop large; S F bas : intervalle trop large; S F haut : conforme au risque.
- Après ajustement (tabac, IMC, diabète, revenu) : bas : association atténuée : le seuil s'éloigne du minimum mais reste dans l'intervalle usuel; haut : association indépendante : seuil inchangé après ajustement.
- 30-55 ans au-delà du seuil HR 1,2 : bas : 32 %; haut : 10 % ; écart de risque de décès à 10 ans à 45 ans : +0,8 / +0,5 point (hommes / femmes).
- Figure : `../figures_q6/alt.png`.
