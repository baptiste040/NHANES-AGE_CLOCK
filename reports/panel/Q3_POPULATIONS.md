# Q3 : populations particulières

Programme « panel ». Protocole pré-enregistré dans `DECISIONS.md` (commit `daba713`). Code :
`src/aging_clock/panel/q3.py`, `src/aging_clock/panel/accelerometre.py`. Données :
- `Q3_groupes.json` (effectifs, comptés avant toute lecture de marqueur) ;
- `Q3_decalages.csv`, `Q3_faux_signaux.csv`, `Q3_centiles_favorisee.csv`, `Q3_synthese.csv` ;
- `Q3_attentes.json`, `Q3_predictions.json`.

**Question.** Chez des groupes proches de la population cible, les marqueurs sont-ils décalés ? Les
seuils usuels (D1) donnent-ils trop de faux signaux chez les personnes en bonne santé ? De combien un
centile « population générale » flatte-t-il une population favorisée et en bonne santé ?

## À lire avant les chiffres

- **Données.** NHANES 2003-2010, américain, transversal. Ce sont les mêmes méthodes de laboratoire que
  les intervalles D1 ; elles ont changé depuis (Q5).
- **Changement détectable.** C'est celui de Q1 (groupe 30-55 ans), une **borne basse** : remesures à
  environ 2 semaines, dans un même laboratoire.
- **Seuils.**
  - R : seuil clinique fondé sur le risque ou la décision.
  - S : convention statistique (intervalle de référence calculé sur NHANES, 2,5e-97,5e centiles).
  - Un taux « hors S » élevé chez des personnes saines signale un intervalle mal adapté au groupe,
    **pas un risque**.
- **Les groupes sont des proxys.**
  - « Très actif » veut dire au moins 72 min/jour (hommes) ou 43 min/jour (femmes) d'activité
    modérée à vigoureuse. Ce sont des personnes actives, **pas des athlètes de compétition**.
  - L'accéléromètre porté à la hanche capte mal le vélo et la natation, et ne capte pas la
    musculation.
  - La contraception et la ménopause sont déclarées.
  - Le type de pilule vient des ordonnances.
- **« Sains »** : membres de la population de référence D1 (non-fumeurs, IMC 18,5-30, sans maladie ni
  traitement chronique déclarés).

## Ce qu'il faut retenir

1. **Les seuils usuels restent utilisables pour ces groupes, à trois exceptions près.** Sur
   l'ensemble des groupes principaux, un seul décalage atteint le changement détectable : la
   ferritine après la ménopause. Une seule autre règle de taux est franchie, chez les femmes très
   actives. Les trois exceptions sont :
   - **ferritine après la ménopause** : +196 % [+113 ; +288] face aux femmes réglées du même âge,
     soit 2,1 fois le changement détectable. Ce n'est mesuré qu'entre 45 et 49 ans : NHANES ne dose
     la ferritine que chez les femmes de moins de 50 ans en 2005-2010. Un intervalle « femme » unique
     ne convient pas : il mélange deux populations, avant et après l'arrêt des règles ;
   - **glycémie à jeun après la ménopause**, seuil OMS ≥ 6,1 mmol/L : 11,8 % des ménopausées saines
     sont au-dessus, contre 5,1 % des femmes de référence de 45 à 59 ans. Le décalage médian est
     pourtant nul (+1,3 %, IC incluant 0) : c'est la queue haute de la distribution qui s'épaissit ;
   - **protéines totales et globulines basses chez les femmes très actives** : 10,4 % et 12,5 % des
     48 femmes saines sont sous la limite basse S, contre environ 2,5 % attendus. Cela ne représente
     que 5 et 6 personnes, et le décalage médian est petit (−1,4 % et −3,6 %). C'est un signal
     fragile.
2. **Beaucoup de décalages nets restent sous le changement détectable**, dans tous les groupes. Le
   plus souvent ils valent la moitié à presque tout le changement détectable. Ils ne faussent pas
   une classification pour une personne, mais ils déplacent une cohorte entière. Les plus nets :
   - **pilule** :
     - CRP +112 % ;
     - vitamine D +46 % ;
     - TG +27 % ;
     - ferritine +31 % ;
     - B12 −19 % ;
     - PAL −15 % ;
     - CTF +14 % ;
     - HDL +12 % ;
     - ApoB +13 % ;
     - DFGe −9 %.
   - **très actifs** :
     - CRP −30 % (hommes) et −61 % (femmes) ;
     - GGT −16 et −21 % ;
     - HDL +10 % ;
     - insuline −33 % ;
     - TG −16 %.
   - **ménopause** : PAL +17 %.
   - **injectable** : ferritine +65 %, GGT +27 %, HDL −13 %.
   - **favorisée** : GGT −19 %, CRP −38 %, TG/HDL −28 %, HOMA-IR −24 %, folates érythrocytaires
     +16 %.
3. **Un centile « population générale » flatte nettement une population favorisée et en bonne
   santé.**
   - **Ce qui est flatté.** Pour 56 couples (marqueur, sexe) sur 133, la personne médiane du groupe
     favorisé et sain se situe à au moins 10 points du 50e centile de la population générale de
     30-55 ans. Le décalage atteint jusqu'à 26 points : TG/HDL et indice athérogène au 24e centile
     chez les femmes, ApoB au 25e, HDL au 72e.
   - **Ce n'est pas un effet du milieu social.** C'est surtout l'effet du filtre « sain » : pour tout
     le groupe favorisé, sains ou non, seuls 22 couples sur 133 dépassent 10 points (écart absolu
     médian : 4,8 points, contre 8,4 pour les sains).
   - **Conséquence pratique.** Pour une population sélectionnée, affluente et en bonne santé, « au
     50e centile de la population » veut souvent dire « moins bien que la plupart des gens comme
     vous » pour les marqueurs du métabolisme (TG, insuline, HOMA-IR, glycémie, HbA1c), du foie (GGT)
     et de l'inflammation (CRP, leucocytes).
4. **La prédiction P1 n'est pas vérifiée.**
   - Chez les très actifs, aucun des quatre marqueurs prévus ne déclenche la règle du taux : ni la
     créatinine haute, ni le DFGe < 60, ni l'ASAT haute, ni l'hémoglobine basse.
   - Les taux sont proches de ceux de la référence, sauf la créatinine haute chez les femmes : 8,3 %
     contre 2,2 % (4 femmes sur 48), sous le seuil de 10 %.
   - Ce seuil d'activité ne produit ni « fausse insuffisance rénale » ni « fausse anémie ».

## Effectifs (comptés avant analyse)

| Groupe | Effectif (dont sains) | Comparaison |
|---|---|---|
| Très actifs (5 % par sexe, principal) | H 83 (44), F 83 (48) | H 1 573, F 1 555 |
| Très actifs, seuil global (sensibilité) | 168 (81) : H 136, F 32 | 3 126 |
| Très actifs, questionnaire (sensibilité) | 521 (204) | 8 739 |
| Pilule (principal) | 546 (294) | 3 236 |
| Pilule œstroprogestative confirmée par ordonnance | 344 (187) | 3 236 |
| Pilule progestative seule | 13 (9) : non estimable | 3 236 |
| Injectable (analyse séparée) | 103 (37) | 3 236 |
| Après la ménopause, sans traitement hormonal | 687 (144) | 780 |
| Ménopause sous traitement hormonal (à part) | 55 (20) | 780 |
| Favorisée | 1 075 (607) | 8 191 |

## Décalages, par groupe

Seuls les marqueurs dont le décalage vaut au moins 0,3 changement détectable sont montrés, plus les
cas « inadapté ». Le reste est dans `Q3_synthese.csv`.

Sens des colonnes :
- **Décalage** : régression médiane ajustée sur l'âge (et sur le sexe si mixte), IC 95 % par
  bootstrap (500 tirages).
- **Moindres carrés** : sensibilité (moyenne géométrique).
- **Rapport au CD** : |décalage| / changement détectable à 6 mois (Q1, 30-55 ans).

**Créatinine et DFGe chez les très actifs : lire la colonne des moindres carrés.** En 2003-2006, la
créatinine est arrondie à 0,1 mg/dL. La régression médiane saute alors d'une valeur à l'autre (−10 %
= 0,9 contre 1,0 mg/dL) et son IC bute sur ces marches. Ce n'était pas prévu au pré-enregistrement.
L'estimation principale reste rapportée, mais elle n'est pas fiable pour ces deux marqueurs.

### Très actifs, hommes (5 % les plus actifs, contre les autres hommes)

| Marqueur | n groupe | Décalage (médiane) [IC 95 %] | Moindres carrés | CD 6 mois | Rapport au CD | Catégorie |
|---|---|---|---|---|---|---|
| GGT/HDL | 82 | −22,9 % [−31,9 ; −10,8] | −21,5 | 38,5 | 0,60 | décalé, sous le changement détectable |
| Créatinine | 82 | −10,0 % [−10,0 ; −0,0] | −4,4 | 17,2 | 0,58 | décalé, sous le changement détectable |
| DFGe (CKD-EPI 2021) | 82 | +13,5 % [+0,1 ; +13,5] | +4,0 | 24,1 | 0,56 | décalé, sous le changement détectable |
| GGT | 82 | −16,0 % [−24,6 ; −5,0] | −15,8 | 34,9 | 0,46 | décalé, sous le changement détectable |
| Cholestérol non-HDL | 82 | −10,1 % [−13,7 ; −4,5] | −7,7 | 26,2 | 0,39 | décalé, sous le changement détectable |
| CRP | 82 | −29,9 % [−46,2 ; −8,4] | −31,5 | 79,9 | 0,37 | décalé, sous le changement détectable |
| Hémoglobine | 82 | +0,1 % [−1,3 ; +1,8] | −0,1 | 10,3 | 0,01 | sans différence |

### Très actifs, femmes (5 % les plus actives, contre les autres femmes)

| Marqueur | n groupe | Décalage (médiane) [IC 95 %] | Moindres carrés | CD 6 mois | Rapport au CD | Catégorie |
|---|---|---|---|---|---|---|
| GGT/HDL | 81 | −33,0 % [−42,6 ; −22,3] | −28,5 | 38,5 | 0,86 | décalé, sous le changement détectable |
| PAL | 81 | −15,3 % [−21,8 ; −9,6] | −13,2 | 19,1 | 0,80 | décalé, sous le changement détectable |
| CRP | 81 | −60,6 % [−74,8 ; −42,8] | −53,9 | 79,9 | 0,76 | décalé, sous le changement détectable |
| GGT | 81 | −21,0 % [−29,1 ; −12,0] | −17,7 | 34,9 | 0,60 | décalé, sous le changement détectable |
| Folates érythrocytaires | 80 | +13,3 % [+5,1 ; +18,7] | +9,9 | 31,4 | 0,42 | décalé, sous le changement détectable |
| VGM | 82 | +1,0 % [−0,2 ; +2,0] | +0,7 | 2,7 | 0,37 | sans différence |
| Cholestérol non-HDL | 81 | −8,2 % [−12,8 ; +0,2] | −6,4 | 26,2 | 0,31 | sans différence |
| Globulines | 81 | −3,6 % [−7,4 ; −0,4] | −5,0 | 15,0 | 0,24 | **inadapté** (taux : bas S) |
| Protéines totales | 81 | −1,4 % [−2,9 ; −0,0] | −1,5 | 9,4 | 0,15 | **inadapté** (taux : bas S) |
| Hémoglobine | 82 | −1,2 % [−3,8 ; +0,7] | −1,0 | 9,4 | 0,13 | sans différence |
| Créatinine | 81 | −0,0 % [−6,5 ; +4,1] | −0,1 | 17,2 | 0,00 | sans différence |
| DFGe (CKD-EPI 2021) | 81 | +0,0 % [−4,6 ; +8,4] | +0,3 | 24,1 | 0,00 | sans différence |

Les marqueurs à jeun (TG, insuline) ne sont pas estimables par sexe : moins de 50 personnes à jeun
dans chaque sexe. Ils le sont en commun (deux sexes, ajustés sur le sexe), voir les sensibilités.

**Les sensibilités confirment le sens des signaux principaux**, sur l'estimation commune aux deux
sexes :

| Marqueur | Principal (5 % par sexe, deux sexes ajustés) | Seuil global | Questionnaire |
|---|---|---|---|
| HDL | +10,5 % [+5,7 ; +19,3] | +15,2 % [+8,5 ; +20,8] | +12,1 % [+8,0 ; +15,8] |
| Triglycérides (à jeun) | −16,4 % [−23,8 ; −3,8] | −17,0 % [−28,7 ; +1,2] | −16,1 % [−24,3 ; −10,3] |
| CRP | −42,5 % [−56,3 ; −31,3] | −42,1 % [−52,8 ; −26,7] | −35,3 % [−42,8 ; −25,9] |
| GGT | −18,9 % [−22,5 ; −11,2] | −16,3 % [−21,7 ; −8,6] | −6,2 % [−12,9 ; −3,2] |
| GGT/HDL | −27,4 % [−33,6 ; −20,6] | −25,8 % [−32,5 ; −17,8] | −22,7 % [−28,1 ; −14,8] |
| Insuline (à jeun) | −33,4 % [−45,9 ; −7,8] | −26,5 % [−40,3 ; −12,3] | −28,0 % [−37,2 ; −19,0] |
| PAL | −9,2 % [−12,3 ; −2,9] | −2,5 % [−8,0 ; +1,7] | −6,0 % [−9,4 ; −2,3] |
| Urée | +10,1 % [+2,5 ; +17,9] | +2,2 % [+0,0 ; +13,5] | +8,3 % [+4,3 ; +8,6] |
| Leucocytes | −4,1 % [−7,1 ; +3,3] | −1,9 % [−9,1 ; +3,5] | −5,7 % [−9,5 ; −3,5] |
| Hémoglobine | −0,2 % [−1,9 ; +1,0] | −0,1 % [−1,2 ; +0,9] | −0,1 % [−1,3 ; +0,2] |
| Créatinine | −10,0 % [−10,0 ; −0,1] | −10,0 % [−10,0 ; −10,0] | +5,5 % [+3,0 ; +7,9] |
| DFGe (CKD-EPI 2021) | +13,5 % [+0,0 ; +13,5] | +13,5 % [+13,5 ; +13,5] | −6,2 % [−8,8 ; −3,5] |

- **La créatinine diverge selon la définition de l'activité.**
  - Avec l'accéléromètre, qui mesure surtout la marche et la course, elle est plutôt plus basse.
    Par moindres carrés : −2,2 % pour les deux sexes, −4,4 % chez les hommes.
  - Avec le questionnaire, qui capte aussi les sports et la musculation, elle est plus haute
    (+5,5 %), ce qui va avec une masse musculaire plus grande.
- **Dans les deux cas**, la créatinine reste loin du changement détectable et ne fausse pas le DFGe
  < 60.

### Pilule et injectable (femmes de 20 à 49 ans, contre les femmes sans contraception hormonale)

| Marqueur | Pilule (546) | Œstroprogestative confirmée (344) | Injectable (103) |
|---|---|---|---|
| Triglycérides (à jeun) | +26,8 % [+17,0 ; +41,6] | +22,0 % [+12,0 ; +38,1] | non estimable |
| HDL | +11,7 % [+9,1 ; +15,0] | +13,8 % [+11,0 ; +18,1] | −12,7 % [−17,4 ; −6,2] |
| CRP | +112,3 % [+86,4 ; +138,4] | +116,3 % [+81,9 ; +149,4] | −3,8 % [−46,2 ; +42,0] |
| Ferritine | +31,3 % [+18,3 ; +47,8] | +36,2 % [+19,9 ; +53,9] | +64,9 % [+26,9 ; +104,3] |
| CTF | +13,6 % [+11,0 ; +15,8] | +14,0 % [+11,4 ; +16,2] | non estimable |
| Albumine | −2,5 % [−4,6 ; −2,4] | −2,7 % [−4,7 ; −2,4] | +2,4 % [−0,0 ; +3,9] |
| Vitamine B12 | −18,9 % [−24,1 ; −13,3] | −24,3 % [−28,2 ; −16,0] | non estimable |
| PAL | −15,1 % [−17,6 ; −13,0] | −19,0 % [−21,9 ; −15,6] | +6,6 % [−3,4 ; +13,2] |
| Vitamine D | +46,1 % [+39,0 ; +52,6] | +54,8 % [+48,7 ; +62,8] | +2,4 % [−8,4 ; +9,3] |
| DFGe (CKD-EPI 2021) | −9,4 % [−12,2 ; −5,6] | −12,4 % [−14,6 ; −9,3] | −2,5 % [−6,4 ; +0,2] |
| LDL | +3,1 % [−1,6 ; +8,8] | +3,9 % [−1,4 ; +10,6] | non estimable |
| ApoB | +13,2 % [+7,2 ; +16,9] | +13,9 % [+8,1 ; +19,5] | non estimable |

- **Pilule et injectable vont dans des sens opposés.**
  - Sous pilule : TG, HDL, CRP, CTF, ApoB et vitamine D plus hauts ; albumine, B12 et PAL plus bas.
    La pilule œstroprogestative confirmée par ordonnance donne les mêmes résultats, en un peu plus
    fort.
  - Sous injectable (progestatif seul) : HDL plus bas (−13 %), CRP sans différence, et une ferritine
    nettement plus haute (+65 %), sans doute par aménorrhée, ce que nous ne vérifions pas.
  - Séparer les deux analyses était justifié.
- **Aucun de ces décalages n'atteint le changement détectable**, ni ne rend un seuil « inadapté »
  par la règle du taux.
  - Le plus proche : les TG ≥ 1,7 mmol/L touchent 19,4 % des femmes saines sous pilule, contre
    10,6 % des femmes de référence de 20 à 49 ans (×1,83, sous le seuil ×2).
  - Ces décalages restent grands à l'échelle d'une cohorte : une CRP doublée sous pilule fausse
    toute lecture « inflammation » si le statut contraceptif n'est pas noté.
- **Vitamine D +46 % sous pilule.** C'est un résultat non anticipé, sans source lue. L'explication
  courante (les œstrogènes augmentent la protéine porteuse, donc la vitamine D totale) n'a pas été
  vérifiée ici.

### Après la ménopause (femmes de 45 à 59 ans, contre les femmes réglées du même âge)

| Marqueur | n groupe | Décalage (médiane) [IC 95 %] | Moindres carrés | CD 6 mois | Rapport au CD | Catégorie |
|---|---|---|---|---|---|---|
| Ferritine (45-49 ans seulement) | 60 | +196,4 % [+113,1 ; +288,1] | +201,8 | 93,5 | 2,10 | **inadapté** |
| PAL | 655 | +16,9 % [+10,1 ; +24,9] | +16,2 | 23,7 | 0,71 | décalé, sous le changement détectable |
| Neutrophiles/lymphocytes | 661 | −15,9 % [−20,8 ; −8,5] | −11,6 | 45,6 | 0,35 | décalé, sous le changement détectable |
| Indice SII | 661 | −16,7 % [−23,4 ; −8,6] | −16,8 | 49,2 | 0,34 | décalé, sous le changement détectable |
| Folates érythrocytaires | 242 | −7,5 % [−16,3 ; +3,6] | −1,3 | 23,9 | 0,31 | sans différence |
| Glycémie à jeun (plasma) | 292 | +1,3 % [−2,7 ; +3,8] | +2,7 | 24,2 | 0,05 | **inadapté** (taux : ≥ 6,1 mmol/L, OMS) |

- **Le décalage est ajusté sur l'âge** (spline, dans l'intervalle 45-59 ans).
- **Ferritine.** Ménopausées : 60 femmes ; comparaison : 401 femmes réglées, toutes de 45 à 49 ans.
  Médianes brutes : 86,5 contre 32,0 µg/L.
- **Lipides.** Cholestérol total +3,5 % [+0,4 ; +6,2] et TG +17 % [+1 ; +40]. Le LDL, l'ApoB et le
  HDL ne diffèrent pas.
- **Les autres seuils glycémiques s'épaississent aussi.** HbA1c ≥ 5,7 % (ADA) : 29,2 % contre
  18,8 % (×1,55, sous la règle).
- **Ménopause sous traitement hormonal.** Ce groupe de 55 femmes est rapporté dans les fichiers,
  sans règle.

### Population favorisée (30-55 ans, contre les autres 30-55 ans)

| Marqueur | n groupe | Décalage (médiane) [IC 95 %] | Moindres carrés | CD 6 mois | Rapport au CD | Catégorie |
|---|---|---|---|---|---|---|
| GGT/HDL | 1071 | −29,3 % [−32,7 ; −25,9] | −28,9 | 38,5 | 0,76 | décalé, sous le changement détectable |
| PAL | 1071 | −11,4 % [−13,1 ; −9,5] | −11,8 | 19,1 | 0,59 | décalé, sous le changement détectable |
| GGT | 1071 | −18,9 % [−22,0 ; −16,8] | −20,7 | 34,9 | 0,54 | décalé, sous le changement détectable |
| Folates érythrocytaires | 498 | +16,1 % [+11,7 ; +20,8] | +14,9 | 31,4 | 0,51 | décalé, sous le changement détectable |
| TG/HDL | 489 | −28,2 % [−32,9 ; −22,3] | −27,7 | 58,9 | 0,48 | décalé, sous le changement détectable |
| CRP | 1075 | −37,5 % [−43,7 ; −30,8] | −33,7 | 79,9 | 0,47 | décalé, sous le changement détectable |
| ApoB | 403 | −9,8 % [−11,6 ; −7,2] | −8,3 | 21,8 | 0,45 | décalé, sous le changement détectable |
| HOMA-IR | 488 | −23,9 % [−29,8 ; −17,1] | −23,2 | 58,6 | 0,41 | décalé, sous le changement détectable |
| Insuline (à jeun) | 488 | −20,6 % [−25,7 ; −13,5] | −18,4 | 54,6 | 0,38 | décalé, sous le changement détectable |
| Triglycérides (à jeun) | 489 | −19,5 % [−23,0 ; −14,2] | −18,8 | 53,5 | 0,36 | décalé, sous le changement détectable |
| LDL/HDL | 489 | −15,5 % [−18,4 ; −11,8] | −13,6 | 43,3 | 0,36 | décalé, sous le changement détectable |
| DFGe (CKD-EPI 2021) | 1071 | −6,6 % [−8,9 ; −5,0] | −3,3 | 19,5 | 0,34 | décalé, sous le changement détectable |
| Cholestérol non-HDL | 1073 | −8,0 % [−9,5 ; −5,9] | −5,9 | 26,2 | 0,31 | décalé, sous le changement détectable |
| HDL | 1073 | +12,5 % [+9,7 ; +15,1] | +11,4 | 41,3 | 0,30 | décalé, sous le changement détectable |
| Leucocytes | 1074 | −9,9 % [−11,4 ; −7,6] | −9,7 | 32,5 | 0,30 | décalé, sous le changement détectable |

- Aucun marqueur n'atteint le changement détectable.
- Aucun taux de faux signaux ne franchit la règle : les taux restent proches de la référence, comme
  attendu.
- L'indice athérogène, le QUICKI et les globulines dépassent aussi 0,3 changement détectable
  (`Q3_synthese.csv`).

## Faux signaux : taux hors seuil chez les personnes saines

Ce tableau liste les cas où le taux du groupe atteint au moins 10 % et 1,5 fois la référence. La règle
« inadapté » demande 2 fois la référence et 10 %.

| Groupe | Sexe | Marqueur | Seuil | Sains du groupe (n) | Taux, groupe | Taux, référence D1 | Rapport | Règle |
|---|---|---|---|---|---|---|---|---|
| Injectable | F | Vitamine D | < 20 ng/mL (50 nmol/L) | 35 | 57,1 % | 34,5 % | ×1,66 | non |
| Ménopause | F | Glycémie à jeun | ≥ 6,1 mmol/L (110 mg/dL), OMS | 68 | 11,8 % | 5,1 % | ×2,33 | **inadapté** |
| Ménopause | F | HbA1c | ≥ 5,7 %, ADA | 144 | 29,2 % | 18,8 % | ×1,55 | non |
| Pilule | F | Triglycérides (à jeun) | ≥ 1,7 mmol/L (150 mg/dL) | 129 | 19,4 % | 10,6 % | ×1,83 | non |
| Très actifs | F | Globulines | bas (S) | 48 | 12,5 % | 2,3 % | ×5,42 | **inadapté** |
| Très actifs | F | Protéines totales | bas (S) | 48 | 10,4 % | 2,6 % | ×4,02 | **inadapté** |

**Prédiction P1** (très actifs, règle du taux) : **non vérifiée.**

| Sexe | Seuil | Sains (n) | Taux, groupe | Taux, référence |
|---|---|---|---|---|
| H | Hémoglobine, limite basse S | 44 | 2,3 % | 2,8 % |
| H | ASAT, limite haute S | 44 | 4,5 % | 2,7 % |
| H | Créatinine, limite haute S | 44 | 2,3 % | 2,6 % |
| H | DFGe < 60 | 44 | 0,0 % | 0,9 % |
| F | Hémoglobine, limite basse S | 47 | 2,1 % | 2,7 % |
| F | ASAT, limite haute S | 48 | 2,1 % | 2,7 % |
| F | Créatinine, limite haute S | 48 | 8,3 % | 2,2 % |
| F | DFGe < 60 | 48 | 0,0 % | 0,6 % |

## Centile « population générale » du groupe favorisé et sain

- **Ce qui est calculé.** Pour chaque marqueur et chaque sexe : la médiane du groupe favorisé et
  sain, puis son centile dans la population générale de 30 à 55 ans du même sexe.
- **Pondération.** Le centile est pondéré par les poids d'examen NHANES (poids à jeun pour les
  marqueurs à jeun).
- **Résultat d'ensemble.** Écart absolu médian : 8,4 points. 56 couples sur 133 sont à au moins
  10 points du 50e centile ; le tableau ci-dessous les liste.
- **Tout le groupe favorisé, sains ou non** : écart absolu médian de 4,8 points, et seulement 22
  couples sur 133 à 10 points ou plus.
- Le centile non pondéré est dans `Q3_centiles_favorisee.csv`. L'écart avec le centile pondéré est
  de 1,8 point en médiane, au plus 9 points (vitamine D, femmes).

| Marqueur | Sexe | n | Médiane du groupe | Centile (pondéré) | Écart (points) |
|---|---|---|---|---|---|
| Indice athérogène (log10 TG/HDL, mmol) | F | 153 | −0,34 | 24 | −26 |
| TG/HDL | F | 153 | 1,05 | 24 | −26 |
| ApoB | F | 128 | 76,00 | 25 | −25 |
| Indice TyG | F | 153 | 8,08 | 26 | −24 |
| LDL/HDL | F | 153 | 1,56 | 28 | −22 |
| GGT/HDL | F | 327 | 0,20 | 28 | −22 |
| Triglycérides (à jeun) | F | 153 | 73,00 | 28 | −22 |
| GGT/HDL | H | 279 | 0,41 | 29 | −21 |
| HbA1c | H | 279 | 5,20 | 29 | −21 |
| Glycémie moyenne estimée | H | 279 | 102,54 | 29 | −21 |
| Indice TyG | H | 115 | 8,46 | 30 | −20 |
| Indice athérogène (log10 TG/HDL, mmol) | H | 115 | −0,09 | 30 | −20 |
| TG/HDL | H | 115 | 1,88 | 30 | −20 |
| Glycémie à jeun (plasma) | F | 154 | 90,05 | 31 | −19 |
| HOMA-IR | H | 113 | 1,61 | 31 | −19 |
| PAL | F | 327 | 53,00 | 31 | −19 |
| HOMA-IR | F | 153 | 1,33 | 31 | −19 |
| Triglycérides (à jeun) | H | 115 | 96,00 | 32 | −18 |
| GGT | F | 327 | 13,00 | 32 | −18 |
| Leucocytes | H | 279 | 6,10 | 32 | −18 |
| Glycémie à jeun (plasma) | H | 115 | 96,00 | 32 | −18 |
| CRP | F | 328 | 0,10 | 32 | −18 |
| Insuline (à jeun) | F | 153 | 5,97 | 32 | −18 |
| Insuline (à jeun) | H | 113 | 6,83 | 33 | −17 |
| CRP | H | 279 | 0,09 | 33 | −17 |
| Homocystéine | F | 150 | 6,30 | 33 | −17 |
| Leucocytes | F | 327 | 6,30 | 34 | −16 |
| RAC urinaire | H | 276 | 3,94 | 35 | −15 |
| GGT | H | 279 | 21,00 | 35 | −15 |
| Acide urique | F | 327 | 4,10 | 35 | −15 |
| PAL | H | 279 | 59,00 | 35 | −15 |
| LDL/HDL | H | 115 | 2,25 | 35 | −15 |
| Cholestérol non-HDL | F | 327 | 124,00 | 36 | −14 |
| RDW | F | 327 | 12,30 | 36 | −14 |
| Glycémie moyenne estimée | F | 327 | 102,54 | 37 | −13 |
| HbA1c | F | 327 | 5,20 | 37 | −13 |
| ApoB | H | 93 | 93,00 | 37 | −13 |
| LDL | F | 153 | 103,00 | 37 | −13 |
| Hémoglobine | H | 279 | 15,10 | 38 | −12 |
| Hématies | F | 327 | 4,36 | 39 | −11 |
| Chlorure | H | 279 | 103,00 | 39 | −11 |
| ALAT | H | 277 | 25,00 | 39 | −11 |
| Bicarbonates | F | 326 | 25,00 | 60 | +10 |
| Saturation de la transferrine | F | 150 | 24,30 | 60 | +10 |
| ASAT/ALAT | F | 326 | 1,20 | 62 | +12 |
| Albumine/globulines | H | 279 | 1,67 | 62 | +12 |
| Bilirubine totale | F | 327 | 0,70 | 62 | +12 |
| Sodium | H | 279 | 140,00 | 63 | +13 |
| Bicarbonates | H | 277 | 26,00 | 65 | +15 |
| Bilirubine totale | H | 279 | 0,90 | 65 | +15 |
| HDL | H | 279 | 50,00 | 66 | +16 |
| Albumine | H | 279 | 4,50 | 66 | +16 |
| ASAT/ALAT | H | 277 | 1,04 | 67 | +17 |
| QUICKI | F | 153 | 0,37 | 69 | +19 |
| QUICKI | H | 113 | 0,36 | 69 | +19 |
| HDL | F | 327 | 66,00 | 72 | +22 |

## Attentes physiologiques

- **Règle.** Une attente est confirmée si le décalage a le signe attendu et que son IC exclut 0. Elle
  est contredite si l'IC exclut 0 dans l'autre sens.
- **Pour les très actifs**, l'estimation utilisée est celle des deux sexes ensemble, ajustée sur le
  sexe.
- **Les sources lues sont citées.** « Sans source lue » veut dire qu'aucune revue lue n'appuie
  l'attente.

| Groupe | Attente | Résultat | Statut | Source lue |
|---|---|---|---|---|
| Très actifs | TG ↓ | −16,4 % [−23,8 ; −3,8] | confirmée | Lee 2017 |
| | cholestérol total ↓ | −1,9 % [−4,6 ; +0,7] | non confirmée | Lee 2017 |
| | glycémie à jeun ↓ | −2,3 % [−5,9 ; −1,2] | confirmée | Lee 2017 |
| | ferritine ↓ | — | non estimable : NHANES ne dose la ferritine que chez les femmes de moins de 50 ans en 2005-2010 (37 dans le groupe) | Lee 2017 ; Solberg 2023 |
| | CK ↑ | — | non estimable : CK absente des fichiers 2003-2010 | Lee 2017 |
| | hémoglobine ↓, hématocrite ↓ | −0,2 % [−1,9 ; +1,0] ; −0,6 % [−2,0 ; +1,0] | non confirmées | Mairbäurl 2013 |
| | HDL ↑ | +10,5 % [+5,7 ; +19,3] | confirmée | sans source lue |
| | créatinine ↑ | −10,0 % [−10,0 ; −0,1] (moindres carrés −2,2 %) | contredite (régression médiane peu fiable, voir plus haut) | sans source lue |
| | DFGe ↓ | +13,5 % [+0,0 ; +13,5] (moindres carrés +2,0 %) | contredite (même réserve) | sans source lue |
| | ASAT ↑ | +0,0 % [−4,0 ; +5,2] | non confirmée | sans source lue |
| | leucocytes ↓ | −4,1 % [−7,1 ; +3,3] | non confirmée | sans source lue |
| | CRP ↓ | −42,5 % [−56,3 ; −31,3] | confirmée | sans source lue |
| | insuline ↓ | −33,4 % [−45,9 ; −7,8] | confirmée | sans source lue |
| Pilule | TG ↑ | +26,8 % [+17,0 ; +41,6] | confirmée | Regidor 2023 |
| | HDL ↑ | +11,7 % [+9,1 ; +15,0] | confirmée | Regidor 2023 |
| | ferritine ↑ | +31,3 % [+18,3 ; +47,8] | confirmée | Fischer 2021 |
| | CRP ↑ | +112,3 % [+86,4 ; +138,4] | confirmée | sans source lue |
| | CTF ↑ | +13,6 % [+11,0 ; +15,8] | confirmée | sans source lue |
| | albumine ↓ | −2,5 % [−4,6 ; −2,4] | confirmée | sans source lue |
| | B12 ↓ | −18,9 % [−24,1 ; −13,3] | confirmée | sans source lue |
| Après la ménopause | cholestérol total ↑ | +3,5 % [+0,4 ; +6,2] | confirmée | Fasero 2025 |
| | LDL ↑ | +0,8 % [−6,5 ; +9,3] | non confirmée | Fasero 2025 |
| | TG ↑ | +17,2 % [+0,9 ; +40,2] | confirmée | Fasero 2025 |
| | ApoB ↑ | +4,2 % [−4,8 ; +9,8] | non confirmée | Fasero 2025 |
| | HDL ↓ | +2,4 % [−1,6 ; +7,0] | non confirmée | Fasero 2025 |
| | PAL ↑ | +16,9 % [+10,1 ; +24,9] | confirmée | Bhattoa 2025 (lien indirect, PAL osseuse) |
| | ferritine ↑ | +196,4 % [+113,1 ; +288,1] | confirmée | sans source lue |
| | hémoglobine ↑ | +2,7 % [+1,5 ; +3,7] | confirmée | sans source lue |
| | acide urique ↑ | +4,0 % [+1,1 ; +7,1] | confirmée | sans source lue |

- **Bilan.**
  - Sous pilule, les 7 attentes sont confirmées (7 sur 7 aussi pour la pilule œstroprogestative
    confirmée, `Q3_attentes.json`).
  - Après la ménopause : 6 sur 9.
  - Chez les très actifs : 5 sur 14, avec 2 non estimables et 2 contredites sous réserve de la
    créatinine arrondie.
- **Les deux attentes « hémodilution » ne sont pas confirmées chez les très actifs.** Ce sont
  l'hémoglobine et l'hématocrite plus bas, qui s'appuient sur Mairbäurl 2013. Avec ce niveau
  d'activité, l'« anémie du sportif » n'apparaît pas.

Revues lues (texte intégral) :
- Lee EC et al., J Strength Cond Res 2017, doi:10.1519/JSC.0000000000002122 ;
- Solberg A et al., Life 2023, doi:10.3390/life13102007 ;
- Mairbäurl H, Front Physiol 2013, doi:10.3389/fphys.2013.00332 ;
- Regidor PA et al., Womens Health 2023, doi:10.1177/17455057221147388 ;
- Fischer JAJ et al., Nutrients 2021, doi:10.3390/nu13072340 ;
- Glisic M et al., Eur J Prev Cardiol 2018, doi:10.1177/2047487318774847 ;
- Fasero M et al., J Clin Med 2025, doi:10.3390/jcm14113663 ;
- Bhattoa HP et al., Osteoporos Int 2025, doi:10.1007/s00198-025-07422-3.

## Conséquences pour le programme

1. **Noter le statut hormonal à chaque prélèvement** : pilule (et laquelle), injectable, ménopause,
   traitement de la ménopause.
   - La pilule déplace la CRP (×2), la vitamine D (+46 %), les TG, la B12, la CTF, la PAL et le DFGe
     d'une fraction importante du changement détectable.
   - Dans une cohorte de femmes, un début ou un arrêt de pilule entre deux bilans imite donc un
     changement d'inflammation, de statut vitaminique ou de fonction rénale.
2. **Pour les femmes, prévoir des repères distincts avant et après la ménopause**, au moins pour la
   ferritine, la PAL et la glycémie.
3. **Ne pas présenter un centile « population générale » comme une norme** à une population affluente
   et en bonne santé. La population de comparaison doit lui ressembler. À défaut, il faut dire que la
   personne médiane d'une population favorisée et saine se situe vers le 30e centile général pour
   le métabolisme, le foie et l'inflammation.
4. **Chez les personnes très actives (au sens de l'accéléromètre), les seuils usuels de créatinine,
   de DFGe, d'ASAT et d'hémoglobine ne produisent pas d'excès de faux signaux.** Pour des athlètes de
   compétition ou des pratiquants de musculation, la question reste ouverte : la créatinine est plus
   haute quand l'activité vient du questionnaire.

## Limites

- **Les proxys sont imparfaits.**
  - « Très actif » n'est pas « athlète de compétition ».
  - L'accéléromètre de hanche capte mal le vélo et la natation, et ne capte pas la musculation.
  - La contraception et la ménopause sont déclarées.
  - Le type de pilule vient des ordonnances des 30 derniers jours, pas toujours retrouvées : 344 des
    546 femmes sous pilule ont une ordonnance d'œstroprogestatif.
- **Les effectifs de sains sont petits** : très actifs 44 hommes et 48 femmes, injectable 37,
  ménopause 144. Les deux cas « inadapté » chez les femmes très actives reposent sur 5 et 6
  personnes.
- **Ferritine et CK.** La ferritine n'est mesurée que chez les femmes de moins de 50 ans en
  2005-2010 ; la CK n'est pas mesurée en 2003-2010.
- **Les marqueurs à jeun** ne portent que sur le sous-échantillon du matin. Ils ne sont pas estimables
  par sexe chez les très actifs.
- **Hormones exclues** (testostérone, estradiol, SHBG, FSH) : elles ne sont pas mesurées chez tous les
  adultes en 2003-2010.
  - Or l'éthinylestradiol augmente fortement la SHBG (Regidor 2023). C'est un faux signal classique
    sous pilule.
  - L'indice d'androgènes libres (testostérone/SHBG) en dépend : un bilan hormonal sous pilule ne
    s'interprète pas avec des seuils généraux. Q3 ne peut pas le chiffrer.
- **L'accéléromètre de 2011-2014 n'est pas utilisé**, alors que le plan le prévoyait. Ses unités
  (MIMS) diffèrent, et les méthodes de laboratoire de ces cycles ne sont pas celles de D1.
- **Données et étalon.** NHANES est américain, transversal, cycles 2003-2010 : les méthodes ont
  changé depuis (Q5). Les changements détectables de Q1 sont des bornes basses.

## Écarts au pré-enregistrement et analyses non prévues

1. **Vitamine D, unité des seuils R** (erreur repérée à la lecture des premiers résultats ; même
   conversion que dans Q5).
   - La vitamine D de NHANES (LBXVIDMS) est en nmol/L, alors que les seuils D1 (20 et 30) sont en
     ng/mL.
   - Le premier calcul comparait des nmol/L à des ng/mL. Les seuils sont maintenant convertis
     (×2,4959), et seuls les taux ont été recalculés. Les décalages ne changent pas.
   - Avant correction, l'injectable était classé « inadapté » sur le seuil de sensibilité < 30. Après
     correction, aucun groupe n'est « inadapté » pour la vitamine D.
2. **Calcul en parallèle.**
   - Le premier lancement (12 processus) a été arrêté par manque de mémoire. Il a été relancé avec 4
     processus.
   - L'analyse est identique : même graine et mêmes tirages par marqueur.
3. **Créatinine arrondie à 0,1 mg/dL (2003-2006).** La régression médiane est peu fiable pour la
   créatinine et le DFGe. La sensibilité par moindres carrés, pré-enregistrée, sert de lecture ; ce
   choix n'était pas prévu.
4. **Ferritine et CK.** Les restrictions d'âge et l'absence de mesure n'étaient pas connues au
   pré-enregistrement. L'attente ferritine des très actifs et l'attente CK sont non estimables.
5. **Synthèse des groupes mixtes.** La ligne « ensemble » de `Q3_synthese.csv` reprend les déclenchements
   de la règle du taux des deux sexes, avec le sexe indiqué. La décision principale des très actifs
   se lit par sexe.
6. **Non pré-enregistrés, signalés comme tels.**
   - Le commentaire sur la vitamine D sous pilule.
   - La comparaison de la créatinine entre accéléromètre et questionnaire.
   - Le centile du groupe favorisé entier (le principal est le groupe favorisé et sain ; les deux
     étaient prévus, la comparaison entre eux ne l'était pas).
