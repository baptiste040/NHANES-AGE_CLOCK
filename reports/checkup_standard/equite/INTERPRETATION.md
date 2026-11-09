# Interprétation de l'audit d'équité (écrite après lecture des résultats)

Ce texte est une lecture des résultats de `EQUITE.md`. Les verdicts eux-mêmes viennent de la règle
fixée avant exécution ; rien ici ne modifie le modèle (gelé au point 4).

Repère : sur toute la validation, le rapport observé/prédit est de 0,92 (le modèle, appris sur
1999-2006, surestime légèrement la mortalité de 2007-2010). Un groupe à 0,92 est donc « dans la
moyenne ».

## Défauts du modèle (règle pré-enregistrée)

1. **Gradient socio-économique non entièrement capté (revenu ≥ 3,5 : O/P 0,62 ; diplôme
   universitaire : 0,69).** Ces groupes ont déjà l'écart d'âge le plus bas (−3,6 et −3,8 ans),
   mais leur mortalité réelle est encore plus faible que prédit. Les biomarqueurs captent une
   partie de l'avantage social, pas la totalité (comportements, accès aux soins, facteurs non
   mesurés). La discrimination dans ces groupes reste bonne (gain de C positif, pente ≈ 1) :
   le classement des personnes est correct, c'est le niveau absolu de risque qui est surestimé.
   **Conséquence pour une cohorte de check-up**, souvent plus favorisée que la population
   générale : le risque absolu (et donc l'âge biologique moyen) sera probablement surestimé ;
   le classement relatif devrait tenir. Argument direct pour une recalibration locale (point 4
   du plan, transposition).
2. **Mexicains-américains (O/P 0,65).** Cohérent avec le « paradoxe hispanique » de mortalité
   décrit dans la littérature, et possiblement avec une sous-détection des décès par le chaînage
   NDI chez les personnes reparties hors des États-Unis. Hypothèses non testées ici. Le groupe
   « autre hispanique » va dans le même sens (0,85) sans franchir le seuil.
3. **40-59 ans, pente 1,21 [1,07 ; 1,34]** : prédictions légèrement trop resserrées dans cette
   tranche (juste au-dessus du seuil de 1,20) ; rapport O/P correct (1,03).

## Différences de risque réelles, bien calibrées

- **Revenu < 1,3** : écart moyen +0,7 an contre −1,4 en moyenne, O/P 1,12 (dans la tolérance) :
  le score montre un vieillissement biologique plus élevé chez les plus pauvres, et ce surcroît de
  risque se retrouve dans les décès observés.
- **Noirs non hispaniques** (−0,2 an) et **niveau d'études inférieur au secondaire** (−0,3 an) :
  écarts plus élevés que la moyenne, calibration correcte.
- **Sexe** : écarts moyens différents (hommes −2,3, femmes −0,6) ; calibration correcte selon la
  règle. Le rapport O/P des femmes (0,87) a un IC qui exclut 1 mais reste dans la tolérance de ±20 %.

## Effectifs insuffisants (< 50 décès)

20-39 ans (41 décès) et « autre / multiethnique » (30 décès) : résultats rapportés, pas de conclusion.
Chez les 20-39 ans, le gain de C reste positif [+0,017 ; +0,174].
