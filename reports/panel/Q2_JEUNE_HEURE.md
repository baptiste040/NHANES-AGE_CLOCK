# Q2 : jeûne et heure du prélèvement

Programme « panel ». Protocole pré-enregistré dans `DECISIONS.md` (commit `6404a61`). Code :
`src/aging_clock/panel/q2.py`. Données : `Q2_A_intra.csv` (chez une même personne),
`Q2_B_nhanes3.csv` et `Q2_B_nhanes_1999_2018.csv` (entre personnes), `Q2_synthese.csv`.

**Question.** De combien le jeûne, puis l'heure du prélèvement, déplacent-ils chaque marqueur, par
rapport au changement détectable à 6 mois (Q1) ? Quels marqueurs exigent un prélèvement à jeun ou
un horaire fixe pour qu'un suivi ait un sens ?

## À lire avant les chiffres

- **Deux sortes d'analyses, de solidité très différente.**
  - **Chez une même personne** (NHANES III, deux examens à environ 2 semaines) : la personne est sa
    propre témoin, ce qui supprime les différences entre personnes. C'est l'analyse principale.
    - Discordances de jeûne : 1 153 à 1 176 paires selon le marqueur, dont environ 170 avec plus de
      4 h d'écart de jeûne.
    - Discordances franches (< 4 h à un examen, ≥ 8 h à l'autre) : seulement 34 à 44 paires.
  - **Entre personnes** (NHANES 1999-2018, environ 40 000 adultes ; NHANES III, environ 13 000) :
    ce sont des **associations**. Les personnes vues l'après-midi ou non à jeun diffèrent des autres
    (âge, santé, emploi), même après ajustement sur l'âge, le sexe, l'IMC, l'ethnie, le revenu et
    le diabète.
- **Le changement détectable de Q1 sert d'étalon**, et c'est une borne basse : un effet jugé
  « négligeable » ici l'est par rapport à une variabilité déjà grande.
- **Seuils** : Q2 n'en utilise aucun.
- NHANES est américain ; NHANES III date de 1988-1994. La composition des repas est inconnue.

## Ce qu'il faut retenir

1. **Avec la règle pré-enregistrée, aucun marqueur n'exige un prélèvement à jeun ni un horaire
   fixe.**
   - Tous les ratios « effet / changement détectable » sont inférieurs à 0,5, sauf la CK, non
     estimable.
   - Raison : chez une même personne, l'effet du jeûne est faible face à une variabilité qui est
     déjà grande pour les marqueurs sensibles au repas. Par exemple, le changement détectable des
     TG est de +111 %.
2. **Les deux analyses ne disent pas la même chose, et c'est le résultat principal.**
   - Entre personnes, être non à jeun est associé à : TG +23 à +25 %, glycémie +5 à +10 %,
     insuline +77 %, HOMA-IR +94 %. C'est cohérent avec la physiologie.
   - Chez une même personne, les effets sont 3 à 8 fois plus petits, et presque nuls pour les TG
     dans le modèle principal : TG −0,2 % (modèle principal), +8 % en classes ou en contraste
     direct ; insuline +11 à +25 %.
   - Si l'on prenait les associations entre personnes, l'**insuline**, le **HOMA-IR** et le
     **QUICKI** passeraient « à enregistrer et corriger » (ratios 0,66 à 0,71).
3. **L'heure joue dans la journée, peu le matin.**
   - Entre 8 h et 11 h, aucun effet n'atteint 0,5 fois le changement détectable.
   - L'après-midi et le soir comptent davantage : TSH −16 % l'après-midi ; fer −17 % le soir ;
     leucocytes +9 % l'après-midi et +16 % le soir. Ces effets restent sous le seuil.

## Pourquoi les deux analyses divergent (interprétation, non testée)

- **Le modèle principal est linéaire en heures de jeûne.** La plupart des écarts de jeûne entre les
  deux examens ont lieu entre des personnes à jeun depuis 8, 12 ou 16 h, zone où les TG ne bougent
  presque plus. La pente moyenne sous-estime alors l'effet d'un repas récent. Les sensibilités en
  classes et le contraste direct, plus proches de la question « repas récent contre jeûne », donnent
  des effets 2 à 40 fois plus grands. Ils restent toutefois sous le seuil.
- **Les associations entre personnes peuvent surestimer l'effet.** Les personnes non à jeun
  diffèrent des autres d'une façon que l'ajustement ne capte pas entièrement.
- **Le second examen de NHANES III n'est pas tiré au hasard** : les personnes qui changent de
  statut de jeûne sont peu nombreuses et peut-être particulières.

**Conséquence pratique** : pour l'**insuline** et les indices qui en dérivent (HOMA-IR, QUICKI),
la prudence voudrait d'enregistrer le jeûne, même si la règle pré-enregistrée ne l'impose pas.

## Résultats par marqueur

Effets en %, sauf « (unités) » pour les marqueurs sur l'échelle additive.
- **Jeûne** : non à jeun (2 h) contre 10 h. Source A = même personne (NHANES III, modèle
  principal) ; B = association (NHANES 1999-2018), utilisée seulement quand A n'est pas estimable.
- **Heure** : 11 h contre 8 h (NHANES III, association).
- **16 h / 9 h** : contraste rapporté.

| Marqueur | Effet du jeûne [IC 95 %] | Ratio | Source | Effet de 11 h contre 8 h [IC 95 %] | Ratio | 16 h contre 9 h | **Catégorie** |
|---|---|---|---|---|---|---|---|
| Leucocytes | +1,4 [−1,1 ; +4,1] | 0,03 | A | −1,3 [−4,5 ; +1,9] | 0,04 | +10,8 | **indifférent** |
| Neutrophiles (%) | +2,0 [+1,3 ; +2,6] | 0,05 | B, NHANES 1999-2018 | +0,9 [−4,1 ; +5,9] | 0,02 | +3,7 | **indifférent** |
| Granulocytes (%, automate) | −0,3 [−1,7 ; +1,3] | 0,01 | A | +4,1 [+2,4 ; +6,1] | 0,14 | +1,6 | **indifférent** |
| Lymphocytes (%) | +0,3 [−1,8 ; +2,4] | 0,01 | A | −6,7 [−9,5 ; −4,0] | 0,21 | −1,3 | **indifférent** |
| Lymphocytes (nombre) | +1,8 [−0,7 ; +4,2] | 0,04 | A | −8,1 [−11,1 ; −4,9] | 0,26 | +9,3 | **indifférent** |
| Monocytes (%) | −0,5 [−1,5 ; +0,5] | 0,01 | B, NHANES 1999-2018 | −0,3 [−1,0 ; +0,4] | 0,01 | −0,7 | **indifférent** |
| Éosinophiles (%) | −0,1 [−0,2 ; −0,1] | 0,00 | B, NHANES 1999-2018 | −0,2 [−0,7 ; +0,5] | 0,00 | −0,8 | **indifférent** |
| Basophiles (%) | −0,0 (unités) [−0,0 ; −0,0] | 0,03 | B, NHANES 1999-2018 | −0,1 (unités) [−0,2 ; +0,1] | 0,08 | −0,1 | **indifférent** |
| Hématies | −0,5 [−1,1 ; +0,1] | 0,06 | A | +0,4 [−0,6 ; +1,4] | 0,04 | −0,9 | **indifférent** |
| Hémoglobine | −0,6 [−1,2 ; −0,0] | 0,07 | A | −0,1 [−1,1 ; +0,9] | 0,01 | −1,2 | **indifférent** |
| Hématocrite | −0,5 [−1,0 ; +0,1] | 0,05 | A | +0,0 [−0,9 ; +0,9] | 0,00 | −1,0 | **indifférent** |
| VGM | +0,1 [−0,0 ; +0,2] | 0,03 | A | −0,4 [−1,0 ; +0,4] | 0,14 | −0,1 | **indifférent** |
| TCMH | −0,1 [−0,3 ; +0,2] | 0,02 | A | −0,5 [−1,3 ; +0,3] | 0,11 | −0,2 | **indifférent** |
| CCMH | −0,2 [−0,4 ; +0,1] | 0,04 | A | −0,1 [−0,4 ; +0,2] | 0,03 | −0,1 | **indifférent** |
| RDW | −0,4 [−0,6 ; −0,1] | 0,05 | A | +0,8 [−0,0 ; +1,8] | 0,12 | −0,1 | **indifférent** |
| Plaquettes | +1,5 [−0,3 ; +3,5] | 0,04 | A | −1,0 [−3,8 ; +1,8] | 0,04 | +0,5 | **indifférent** |
| VPM | −0,7 [−1,4 ; −0,0] | 0,06 | A | −3,9 [−5,2 ; −2,8] | 0,33 | −2,2 | **indifférent** |
| Glycémie à jeun (plasma) | +1,1 [−0,7 ; +3,2] | 0,04 | A | −5,7 [−7,6 ; −4,0] | 0,25 | −8,2 | **indifférent** |
| Glucose sérique (non à jeun) | +1,6 [−0,5 ; +3,8] | 0,05 | A | −6,0 [−8,0 ; −3,7] | 0,24 | −8,7 | **indifférent** |
| Insuline (à jeun) | +11,1 [+4,1 ; +19,2] | 0,10 | A | −8,4 [−12,9 ; −2,5] | 0,16 | −17,8 | **indifférent** |
| HbA1c | +0,0 [−0,7 ; +0,9] | 0,00 | A | −1,2 [−2,6 ; +0,2] | 0,13 | −1,1 | **indifférent** |
| Cholestérol total | −1,2 [−2,5 ; +0,1] | 0,06 | A | −2,4 [−4,3 ; −0,2] | 0,11 | +0,1 | **indifférent** |
| LDL (calculé, à jeun) | −4,0 [−10,4 ; +2,7] | 0,12 | A | −0,3 [−8,4 ; +8,0] | 0,01 | +11,1 | **indifférent** |
| HDL | −1,1 [−3,0 ; +0,6] | 0,04 | A | −1,5 [−4,4 ; +1,4] | 0,05 | +1,5 | **indifférent** |
| Triglycérides (à jeun) | −0,2 [−5,2 ; +4,9] | 0,00 | A | −4,5 [−9,2 ; +1,5] | 0,09 | −0,2 | **indifférent** |
| Triglycérides sériques (non à jeun) | −1,4 [−5,8 ; +3,2] | 0,03 | A | −1,6 [−8,1 ; +4,9] | 0,03 | +0,0 | **indifférent** |
| ALAT | −6,2 [−9,5 ; −2,7] | 0,10 | A | +7,5 [+1,9 ; +14,4] | 0,04 | −1,0 | **indifférent** |
| ASAT | −3,8 [−6,3 ; −1,3] | 0,08 | A | +7,1 [+3,0 ; +11,5] | 0,08 | +1,7 | **indifférent** |
| GGT | −2,7 [−6,0 ; +0,3] | 0,08 | A | +4,3 [−3,6 ; +12,9] | 0,08 | +2,8 | **indifférent** |
| PAL | −0,0 [−1,3 ; +1,1] | 0,00 | A | −1,5 [−4,7 ; +2,0] | 0,08 | −0,3 | **indifférent** |
| Bilirubine totale | −3,5 [−7,5 ; +1,0] | 0,09 | A | +0,0 [−0,0 ; +0,0] | 0,00 | +0,0 | **indifférent** |
| Albumine | −0,8 [−1,5 ; −0,1] | 0,07 | A | +1,4 [+0,4 ; +2,3] | 0,11 | +3,0 | **indifférent** |
| Protéines totales | −0,5 [−1,0 ; +0,1] | 0,05 | A | +1,4 [+0,7 ; +2,1] | 0,14 | +1,5 | **indifférent** |
| Globulines | −0,6 [−1,6 ; +0,4] | 0,04 | A | +1,2 [−0,5 ; +2,7] | 0,07 | −0,5 | **indifférent** |
| Créatinine | +1,2 [+0,1 ; +2,3] | 0,06 | A | −1,4 [−3,2 ; +0,7] | 0,08 | +0,3 | **indifférent** |
| Urée | +2,3 [−0,8 ; +5,2] | 0,03 | A | −5,5 [−8,8 ; −2,2] | 0,14 | −3,0 | **indifférent** |
| Sodium | −0,3 [−0,5 ; −0,0] | 0,07 | A | +0,2 [+0,0 ; +0,4] | 0,07 | +0,2 | **indifférent** |
| Potassium | −0,1 [−0,9 ; +0,8] | 0,01 | A | +3,8 [+2,8 ; +4,9] | 0,24 | −1,4 | **indifférent** |
| Chlorure | −0,1 [−0,4 ; +0,2] | 0,02 | A | −0,1 [−0,4 ; +0,2] | 0,01 | −0,2 | **indifférent** |
| Bicarbonates | +0,5 [−1,4 ; +2,4] | 0,01 | A | −1,7 [−3,1 ; +0,0] | 0,06 | −0,5 | **indifférent** |
| Osmolalité mesurée | −0,0 [−0,3 ; +0,2] | 0,01 | A | +0,3 [+0,0 ; +0,6] | 0,07 | −0,1 | **indifférent** |
| CRP | −1,2 [−6,7 ; +4,6] | 0,02 | A | +3,6 [−3,6 ; +10,9] | 0,01 | +3,6 | **indifférent** |
| Vitamine B12 | +0,1 [−3,3 ; +3,1] | 0,00 | A | +5,7 [−1,9 ; +14,3] | 0,12 | −3,0 | **indifférent** |
| Folates érythrocytaires | −1,2 [−2,6 ; +0,2] | 0,05 | A | −5,8 [−10,6 ; −1,2] | 0,25 | −2,1 | **indifférent** |
| Calcium | −0,7 [−1,1 ; −0,2] | 0,08 | A | +0,9 [+0,4 ; +1,4] | 0,09 | +1,3 | **indifférent** |
| LH | +12,5 [−6,5 ; +35,1] | 0,03 | A | −16,4 [−33,1 ; +5,2] | 0,20 | −4,9 | **indifférent** |
| ApoA1 | −0,6 [−2,7 ; +1,3] | 0,03 | A | −1,3 [−4,0 ; +1,4] | 0,06 | +0,5 | **indifférent** |
| ApoB | +0,3 [−2,5 ; +3,2] | 0,01 | A | −3,6 [−6,9 ; +0,2] | 0,15 | −2,2 | **indifférent** |
| Lp(a) | +0,4 (unités) [−0,9 ; +1,7] | 0,02 | A | +2,5 (unités) [−1,8 ; +6,5] | 0,12 | −0,4 | **indifférent** |
| Fer sérique | −7,2 [−12,4 ; −1,4] | 0,13 | A | +0,2 [−4,3 ; +4,8] | 0,00 | −6,3 | **indifférent** |
| Ferritine | −1,0 [−4,2 ; +2,4] | 0,02 | A | −0,8 [−10,7 ; +10,5] | 0,02 | +5,1 | **indifférent** |
| Capacité totale de fixation du fer | −0,5 [−1,5 ; +0,5] | 0,03 | A | +0,5 [−1,3 ; +2,2] | 0,02 | +1,1 | **indifférent** |
| Saturation de la transferrine | −7,3 [−12,4 ; −1,6] | 0,13 | A | −0,2 [−5,3 ; +5,1] | 0,00 | −7,3 | **indifférent** |
| Acide urique | −1,4 [−3,0 ; +0,1] | 0,06 | A | +2,1 [−0,5 ; +4,5] | 0,07 | +0,6 | **indifférent** |
| Phosphate | +1,0 [−0,6 ; +2,5] | 0,03 | A | −0,1 [−1,7 ; +1,4] | 0,01 | +3,7 | **indifférent** |
| Sélénium | +0,1 [−1,1 ; +1,4] | 0,00 | A | +0,1 [−1,4 ; +1,9] | 0,01 | +0,2 | **indifférent** |
| Albumine urinaire | −4,6 [−17,5 ; +9,5] | 0,05 | A | +15,2 [−1,5 ; +33,5] | 0,01 | +11,6 | **indifférent** |
| Créatinine urinaire | −8,6 [−16,1 ; −0,5] | 0,11 | A | +9,9 [+1,8 ; +18,6] | 0,03 | +5,1 | **indifférent** |
| Iode urinaire | +8,4 [−2,3 ; +20,2] | 0,02 | A | +4,0 [−5,6 ; +15,1] | 0,01 | −3,7 | **indifférent** |
| HOMA-IR | +11,7 [+3,7 ; +20,9] | 0,08 | A | −13,7 [−19,2 ; −8,2] | 0,24 | −24,5 | **indifférent** |
| QUICKI | −1,6 [−2,7 ; −0,6] | 0,14 | A | +2,3 [+1,4 ; +3,2] | 0,17 | +4,2 | **indifférent** |
| Indice TyG | +0,0 (unités) [−0,0 ; +0,1] | 0,01 | A | −0,1 (unités) [−0,2 ; −0,0] | 0,13 | −0,1 | **indifférent** |
| LDL calculé (Friedewald) | −1,1 [−3,2 ; +1,3] | 0,03 | A | −1,7 [−5,4 ; +1,8] | 0,05 | −0,3 | **indifférent** |
| Créatine kinase | +4,9 [+0,9 ; +8,8] | — | B, NHANES 1999-2018 | +0,2 [−3,1 ; +3,7] | — | — | **non estimable** |
| 25-OH vitamine D | +3,4 [+1,8 ; +5,0] | 0,06 | B, NHANES 1999-2018 | −2,5 [−4,0 ; −1,2] | 0,07 | — | **indifférent** |
| TSH | −10,0 [−15,0 ; −4,8] | 0,23 | B, NHANES 1999-2018 | −16,0 [−20,3 ; −11,8] | 0,37 | — | **indifférent** |

### Jeûne : les marqueurs sensibles au repas, toutes analyses côte à côte

Effet d'être non à jeun, en %.
- A : même personne, modèle linéaire (principal), en classes, et contraste direct (< 4 h / ≥ 8 h).
- B : association, NHANES III et NHANES 1999-2018.
- Dernière colonne : ratio au changement détectable de Q1 si l'on prenait l'association de
  NHANES III.

| Marqueur | A linéaire (2 h / 10 h) | A en classes | A direct | B NHANES III | B 1999-2018 | Ratio si B |
|---|---|---|---|---|---|---|
| Triglycérides (à jeun) | −0,2 | +8,5 | +7,9 (n=43) | +23,3 | — | 0,21 |
| Triglycérides sériques (non à jeun) | −1,4 | +1,8 | +0,7 (n=34) | +23,1 | +25,1 | 0,23 |
| Glycémie à jeun (plasma) | +1,1 | +3,6 | +3,9 (n=43) | +9,8 | — | 0,33 |
| Glucose sérique (non à jeun) | +1,6 | +3,4 | +4,2 (n=43) | +10,5 | +4,7 | 0,32 |
| Insuline (à jeun) | +11,1 | +25,2 | +18,0 (n=43) | +76,6 | — | 0,66 |
| HOMA-IR | +11,7 | +27,3 | +19,6 (n=42) | +93,6 | — | 0,68 |
| QUICKI | −1,6 | −3,3 | −2,5 (n=42) | −8,2 | — | 0,71 |
| Indice TyG | +0,0 | +0,1 | +0,1 (n=42) | +0,3 | — | 0,38 |
| LDL calculé (Friedewald) | −1,1 | −1,1 | −1,7 (n=40) | −6,2 | — | 0,19 |
| Fer sérique | −7,2 | −6,8 | −8,0 (n=44) | +5,0 | +0,7 | 0,04 |
| TSH | — | — | — (n=—) | — | −10,0 | 0,23 |
| Phosphate | +1,0 | +0,7 | +1,8 (n=43) | −1,7 | −1,2 | 0,07 |
| Leucocytes | +1,4 | +1,4 | +2,2 (n=44) | +1,2 | +0,4 | 0,03 |

### Heure : contrastes pour les marqueurs à rythme connu

Effets en %, associations sauf la dernière colonne.

| Marqueur | 11 h contre 8 h (NHANES III) | 16 h contre 9 h (NHANES III) | Après-midi contre matin (1999-2018) [IC 95 %] | Soir contre matin (1999-2018) | Même personne, par heure de décalage |
|---|---|---|---|---|---|
| Fer sérique | +0,2 | −6,3 | +1,7 [+0,2 ; +3,1] | −16,5 | −3,5 |
| TSH | — | — | −16,0 [−20,3 ; −11,8] | +8,9 | — |
| Phosphate | −0,1 | +3,7 | +1,9 [+1,5 ; +2,4] | +6,8 | +0,9 |
| Leucocytes | −1,3 | +10,8 | +8,8 [+7,8 ; +9,8] | +16,1 | +0,5 |
| Potassium | +3,8 | −1,4 | −1,2 [−1,5 ; −0,9] | −2,6 | +0,6 |
| Glucose sérique (non à jeun) | −6,0 | −8,7 | −5,1 [−5,7 ; −4,4] | −4,6 | −0,6 |
| Insuline (à jeun) | −8,4 | −17,8 | — | — | −1,9 |
| Albumine | +1,4 | +3,0 | +1,4 [+1,2 ; +1,7] | +2,7 | +0,4 |
| Plaquettes | −1,0 | +0,5 | +2,8 [+2,0 ; +3,7] | +2,5 | +1,3 |

## Attentes physiologiques (données a priori par l'auteur du projet)

Une attente est confirmée si l'effet a le signe attendu et que son IC exclut 0. Pour le jeûne, on
teste sur l'analyse A ; pour l'heure, sur NHANES 1999-2018 (après-midi contre matin).

| Attente | Confirmée ? |
|---|---|
| Insuline, HOMA-IR plus hauts non à jeun ; QUICKI plus bas | **oui** (même personne) |
| TG, glycémie, TyG plus hauts non à jeun | **non** chez une même personne (modèle linéaire) ; **oui** entre personnes |
| TSH plus basse l'après-midi | **oui** (−16 %) |
| Phosphate plus haut l'après-midi | **oui** (+1,9 %) |
| Leucocytes plus hauts l'après-midi ou le soir | **oui** (+9 % et +16 %) |
| Fer plus bas plus tard dans la journée | **non** l'après-midi (+1,7 %) ; baisse de 17 % le soir |

## Conclusion pratique

| Catégorie | Marqueurs |
|---|---|
| À jeun requis | aucun |
| Horaire fixe requis | aucun |
| À enregistrer et corriger | aucun selon la règle pré-enregistrée. Insuline, HOMA-IR et QUICKI le seraient si l'on retenait les associations entre personnes. |
| Indifférent | tous les autres |
| Non estimable | créatine kinase (aucun changement détectable dans Q1) |

**Lecture** (interprétation) :
- Dans les conditions de NHANES (prélèvements du matin le plus souvent à jeun, laboratoire
  centralisé), le jeûne et l'heure pèsent peu, par rapport à la variabilité déjà importante des
  marqueurs.
- Ce n'est pas un feu vert pour ignorer le jeûne : les marqueurs les plus sensibles au repas
  (insuline, TG, glycémie) sont aussi les plus bruités. Leur suivi individuel est donc difficile,
  avec ou sans jeûne (Q1).
- Pour l'insuline, les indices qui en dérivent, et les prélèvements de l'après-midi ou du soir
  (fer, TSH, leucocytes), la prudence voudrait d'enregistrer le jeûne et l'heure.

## Écarts et corrections

- **Erreur de codage de la séance (corrigée avant la rédaction).** Le pré-enregistrement indiquait
  `PHDSESN` codé 1, 2 et 3 (matin, après-midi, soir). La documentation NHANES code 0, 1 et 2. La
  première exécution excluait donc les personnes vues le matin, et son contraste « après-midi
  contre matin » était en réalité soir contre après-midi. Corrigé selon la documentation, avant
  toute interprétation.
- **Bug de lecture de NHANES III** (code « 88 » des champs à 2 chiffres lu comme une valeur) :
  il touchait les bicarbonates et la formule leucocytaire manuelle. Corrigé avant la rédaction ;
  voir `DECISIONS.md`. Après correction, la formule manuelle n'a plus assez de paires discordantes
  pour l'analyse chez une même personne (« non estimable » en A ; B utilisée).
- **LDL Martin-Hopkins : non estimable.** Le tableau de facteurs n'est publié qu'en figure dans la
  source (Martin 2013, figure 2), illisible en texte. C'était prévu dans le pré-enregistrement.

## Limites

- Peu de discordances franches de jeûne chez une même personne (34 à 44 paires).
- La séance ne varie jamais entre les deux examens de NHANES III.
- Associations entre personnes sujettes à confusion résiduelle.
- Composition des repas inconnue.
- NHANES est américain.
- Changements détectables de Q1 = bornes basses.
