# Q5 : changements de méthode et de laboratoire

Programme « panel ». Protocole pré-enregistré dans `DECISIONS.md` (commit `22c38f5`). Code :
`src/aging_clock/panel/q5.py`. Données :
- `Q5_evenements.csv` (table des événements) ;
- `Q5_passage.csv` (a), `Q5_empirique.csv` (b), `Q5_classification.csv` ;
- `Q5_entre_laboratoires.csv` (c), `Q5_interventions.csv` (d) ;
- `Q5_synthese.csv`, `Q5_verifications.json`, `Q5_verification_V1_variantes.csv`, `Q5_predictions.json`.

**Question.** De combien un changement de méthode, d'instrument ou de laboratoire déplace-t-il
chaque marqueur, comparé au changement détectable à 6 mois (Q1) ? Combien de personnes changent de
classe autour d'un seuil ? Un changement de laboratoire peut-il imiter ou masquer l'effet d'une
intervention réaliste ?

## À lire avant les chiffres

- **Deux sortes de laboratoires.**
  - NHANES : des laboratoires de référence, très contrôlés. Ses changements de méthode donnent
    l'**ordre de grandeur** des décalages possibles, pas ceux des laboratoires de la population
    cible.
  - Laboratoires de routine européens : ils ne sont vus ici qu'à travers la littérature des
    évaluations externes de la qualité (EEQ), et seulement pour quelques marqueurs.
- **L'écart entre laboratoires de routine reste inconnu pour les lipides, la numération (NFS),
  les vitamines et l'insuline**, faute d'étude trouvée avec les requêtes pré-enregistrées. Il ne
  pourra être mesuré que sur des données réelles venant de plusieurs laboratoires (mêmes personnes
  ou mêmes échantillons mesurés dans plusieurs laboratoires).
- **Le changement détectable de Q1 sert d'étalon**, et c'est une borne basse : remesures à
  environ 2 semaines, dans un même laboratoire. Un décalage « négligeable » ici l'est face à un bruit
  déjà grand.
- **Seuils** : ceux de la table D1 figée. R = seuil clinique fondé sur le risque (ou la décision),
  S = convention statistique (intervalle de référence calculé sur NHANES, CLSI EP28).
- NHANES est américain.

## Ce qu'il faut retenir

1. **Pour suivre une personne, la plupart des changements de méthode de NHANES restent petits devant
   le bruit** (ratio < 0,5), parce que ce bruit est déjà grand. Les exceptions :
   - **ratio ≥ 1, comparaison impossible sans équation de passage** :
     - folates érythrocytaires en 2007 (radio-essai → méthode microbiologique) : +85 % ;
     - créatinine de 1999-2000 (étalonnage non aligné sur la référence) : +22 % ;
   - **ratio de 0,5 à 1, faux changement possible** :
     - créatinine (changement d'instrument en 2007) et DFGe ;
     - rapport albumine/globulines (2017) ;
     - en empirique (b) : PAL et bilirubine (1999 → 2003), RDW et VPM (changement d'automate en
       2012), insuline (2003).
2. **Entre laboratoires de routine (c), le changement détectable grandit surtout pour les marqueurs
   très régulés.**
   - Calcium : ×1,49 ; PAL : ×1,30 ; HbA1c : ×1,27 ; magnésium : ×1,22 ; protéines : ×1,18.
   - Ce sont des bornes basses pour la plupart (CV mesurés au sein des groupes de méthode).
   - Pour les enzymes, le bruit domine : ×1,02 à ×1,04.
3. **Pour classer, un changement de laboratoire compte beaucoup.**
   - Passage Beckman → Roche en 2017 (bilan biochimique) : +26 points de personnes sous la limite basse de l'ASAT, +13 pour
     le chlore, +14 pour la bilirubine, +10 pour le calcium et l'ALAT (intervalles S).
   - Glycémie, seuil ADA : +4 à +5 points à chaque changement d'instrument, pour des décalages de
     seulement 1 à 2 %.
     - Pour le passage Roche Cobas C501 → C311 de 2015, on trouve +6,8 points (adultes de 18 ans et
       plus sans diabète connu, pondéré), contre +12,2 points dans le texte du NCHS.
     - L'écart vient du chiffre « avant correction » du NCHS, que nous ne retrouvons pas (voir V1).
       Hypothèse : il a été calculé sur une version antérieure du fichier.
   - Vitamine D, RIA → LC-MS/MS : −10 points sous 50 nmol/L.
   - Un intervalle de référence n'est donc valable que pour la méthode qui l'a produit.
4. **Un changement de laboratoire peut imiter ou masquer l'effet moyen d'une intervention
   réaliste.**
   - TG : +9,6 % en 2017 (Beckman → Roche), contre −6,8 % pour l'activité physique (ρ = 1,4 : il **masque** l'effet).
   - Insuline : jusqu'à ρ = 2,3 ; cholestérol total : ρ = 1,2 ; HDL : ρ ≥ 0,5 pour quatre
     interventions.
   - ALAT : ρ = 0,83 face à une perte de poids de 5 %, 0,50 face à une perte de 5 kg ; ASAT : 1,2.
   - Entre deux laboratoires de routine : glycémie (ρ ≈ 1) et HbA1c (1,4) face au régime
     méditerranéen.
   - **Pas la vitamine D** : l'effet d'une supplémentation (+97 %) dépasse de loin les décalages
     de méthode (au plus +15 % au centile 50).

**Conséquence pratique.**
- **Enregistrer le laboratoire et la méthode** à chaque bilan.
- **Pour juger l'effet d'une intervention**, surtout sur les TG, l'insuline, le cholestérol, le
  HDL, la glycémie, l'HbA1c et les transaminases : garder le même laboratoire et la même méthode,
  ou disposer d'une équation de passage.
- **Pour classer**, n'appliquer un intervalle de référence qu'aux résultats de la méthode qui l'a
  produit.
- **Pour évaluer l'effet d'un protocole à l'échelle d'une cohorte** (lien avec Q1) :
  - les effets d'hygiène de vie ne sont visibles qu'en moyenne de groupe (Q1) ;
  - un changement de laboratoire peut imiter ou masquer ces effets pour 11 marqueurs sur 15
    (partie d) ;
  - toute évaluation doit donc **enregistrer le laboratoire de chaque prélèvement et en tenir
    compte**, soit en comparant à laboratoire identique, soit en mettant le laboratoire en
    covariable.

## Vérifications de l'implémentation

| Vérification | Attendu | Obtenu | Résultat |
|---|---|---|---|
| V1 : glycémie 2015-2016, équation inverse ; part 100-125 mg/dL avant → après | 53,7 → 41,5 % | 48,3 → 41,5 % | **échec partiel** (après : oui ; avant : non) |
| V1 : part ≥ 126 mg/dL avant → après | 5,5 → 3,4 % | 5,0 → 3,4 % | idem |
| V2 : insuline 2013-2014, moyenne géométrique pondérée avant → après | 9,20 → 10,46 µU/mL | 9,19 → 10,45 | réussie |
| V3 : vitamine D 2001-2002, équation appliquée à la valeur RIA | écart médian < 0,5 nmol/L | 0,03 nmol/L | réussie |

**Recherche de l'écart sur V1** (demandée par l'auteur du projet, sans changement de l'analyse ;
détail dans `Q5_verification_V1_variantes.csv`). On a testé 36 variantes de calcul :
- poids : sous-échantillon à jeun (WTSAF2YR) ou examen (WTMEC2YR) ;
- âge minimal : 18 ou 20 ans ;
- diabète connu : exclusion des réponses « oui » (DIQ010 ≠ 1), restriction aux « non » (DIQ010 = 2),
  ou aucune exclusion ;
- jeûne : aucun filtre, ≥ 8 h, ou 8-24 h.

| Variante | Part 100-125, avant | ≥ 126, avant | Part 100-125, après | ≥ 126, après |
|---|---|---|---|---|
| Publié par le NCHS | 53,7 | 5,5 | 41,5 | 3,4 |
| WTSAF2YR, ≥ 18 ans, DIQ010 ≠ 1 (population décrite par le NCHS) | 48,3 | 5,0 | 41,5 | 3,4 |
| idem, jeûne ≥ 8 h | 48,3 | 5,0 | 41,5 | 3,4 |
| WTMEC2YR, ≥ 20 ans, DIQ010 = 2, jeûne ≥ 8 h (variante la plus proche) | 50,7 | 4,8 | 43,8 | 3,1 |

**Résultat de la vérification.**
- Avec la population décrite par le NCHS et les poids du sous-échantillon à jeun, on retrouve
  exactement ses valeurs **après** correction.
- Le filtre de jeûne ne change rien : les poids WTSAF2YR sont nuls pour les personnes hors du
  sous-échantillon à jeun.
- Aucune variante ne retrouve la valeur **avant** correction (53,7 %).
- L'écart n'est donc ni dû aux poids, ni à l'âge, ni à l'exclusion des diabétiques connus, ni au
  jeûne. Il reste inexpliqué. Hypothèse non testable ici : le chiffre « avant » du NCHS a été
  calculé sur une version antérieure du fichier, avant la mise à l'échelle C311 d'une partie des
  échantillons.
- Conséquence : l'implémentation de l'équation est vérifiée (valeurs « après »). Mais l'effet du
  changement d'instrument sur la classification (part de 100-125 mg/dL) diffère :
  - **+6,8 points** dans nos calculs (48,3 → 41,5 %) ;
  - **+12,2 points** dans le texte du NCHS (53,7 → 41,5 %).

  L'hypothèse retenue est que le chiffre « avant » du NCHS a été calculé sur une version antérieure
  du fichier GLU_I, avant que la partie des échantillons dosés sur C501 soit mise à l'échelle C311.

## Partie (a) : équations de passage publiées

Décalage = nouvelle méthode − ancienne, appliqué aux adultes du cycle précédant le changement.
- ᵐ : décalage moyen seulement (pas d'équation publiée), appliqué à tous les centiles.
- Faux changement : probabilité qu'une personne sans changement réel franchisse le changement
  détectable à cause du décalage (5 % sans décalage).

| Év. | Marqueur | Décalage au centile 50 | Centiles 10 → 90 | Ratio | Faux changement | Catégorie |
|---|---|---|---|---|---|---|
| 1 | Créatinine | +22,3 % | +30,7 → +16,0 | 1,07 | 55 % | **impossible sans équation** |
| 2 | Créatinine | −4,0 % | −4,5 → −3,5 | 0,23 | 7 % | négligeable |
| 3 | Créatinine | −8,9 % ᵐ | −11,4 → −6,7 | 0,52 | 16 % | **faux changement possible** |
| 5 | Albumine | −4,4 % | −4,5 → −4,4 | 0,39 | 11 % | négligeable |
| 5 | PAL | +9,7 % | +9,8 → +9,7 | 0,44 | 15 % | négligeable |
| 5 | ASAT | −17,8 % | −23,5 → −12,3 | 0,38 | 9 % | négligeable |
| 5 | ALAT | −13,9 % | −20,3 → −7,6 | 0,22 | 6 % | négligeable |
| 5 | Urée | −3,3 % | −5,1 → −2,3 | 0,08 | 5 % | négligeable |
| 5 | Bicarbonates | +1,7 % ᵐ | +1,7 → +1,7 | 0,05 | 5 % | négligeable |
| 5 | Calcium | −2,1 % ᵐ | −2,1 → −2,1 | 0,24 | 7 % | négligeable |
| 5 | Cholestérol (bilan biochimique) | −3,3 % | −3,0 → −3,6 | 0,16 | 6 % | négligeable |
| 5 | CK | +5,8 % | +4,8 → +6,4 | — | — | non estimable |
| 5 | Chlorure | −1,4 % ᵐ | −1,4 → −1,4 | 0,25 | 8 % | négligeable |
| 5 | Créatinine | +3,2 % | +6,5 → +0,9 | 0,15 | 6 % | négligeable |
| 5 | Glucose sérique (non à jeun) | +2,4 % ᵐ | +2,4 → +2,4 | 0,08 | 5 % | négligeable |
| 5 | GGT | +9,6 % | −2,4 → +18,4 | 0,18 | 7 % | négligeable |
| 5 | Fer sérique | +8,3 % | +13,5 → +6,0 | 0,06 | 5 % | négligeable |
| 5 | Potassium | −1,4 % ᵐ | −1,4 → −1,4 | 0,10 | 5 % | négligeable |
| 5 | LDH | +14,8 % | +14,3 → +15,2 | — | — | non estimable |
| 5 | Sodium | +0,8 % ᵐ | +0,8 → +0,8 | 0,21 | 7 % | négligeable |
| 5 | Phosphate | −1,8 % ᵐ | −1,8 → −1,8 | 0,08 | 5 % | négligeable |
| 5 | Bilirubine totale | −3,2 % ᵐ | −3,2 → −3,2 | 0,08 | 5 % | négligeable |
| 5 | Protéines totales | +0,4 % ᵐ | +0,4 → +0,4 | 0,03 | 5 % | négligeable |
| 5 | Triglycérides sériques (non à jeun) | +9,6 % | +16,4 → +6,0 | 0,09 | 6 % | négligeable |
| 5 | Acide urique | +2,6 % | +0,6 → +3,8 | 0,09 | 5 % | négligeable |
| 6 | Glycémie à jeun (plasma) | +1,9 % | +2,4 → +1,0 | 0,06 | 5 % | négligeable |
| 7 | Glycémie à jeun (plasma) | +1,2 % | +1,3 → +0,9 | 0,04 | 5 % | négligeable |
| 8 | Glycémie à jeun (plasma) | +1,8 % | +1,7 → +1,9 | 0,06 | 5 % | négligeable |
| 9 | Insuline (à jeun) | −22,3 % | −43,8 → −9,1 | 0,42 | 10 % | négligeable |
| 10 | Insuline (à jeun) | +13,1 % | +44,5 → +1,3 | 0,11 | 6 % | négligeable |
| 11 | Insuline (à jeun) | −10,7 % | −12,3 → −8,5 | 0,20 | 6 % | négligeable |
| 12 | Insuline (à jeun) | −12,0 % | −13,8 → −10,0 | 0,22 | 6 % | négligeable |
| 13 | HDL | −2,4 % ᵐ | −2,5 → −2,4 | 0,08 | 5 % | négligeable |
| 18 | Ferritine | +7,6 % | +9,3 → +6,3 | 0,09 | 6 % | négligeable |
| 19 | Ferritine | +8,4 % | +10,1 → +8,1 | 0,10 | 6 % | négligeable |
| 20 | Vitamine B12 | +14,7 % | +16,7 → +12,7 | 0,30 | 10 % | négligeable |
| 22 | Folates érythrocytaires | +84,7 % | +82,7 → +86,9 | 2,84 | 100 % | **impossible sans équation** |
| 23a | 25-OH vitamine D | +7,5 % | +21,0 → +3,0 | 0,14 | 6 % | négligeable |
| 23b | 25-OH vitamine D | +1,4 % | +4,6 → +0,3 | 0,03 | 5 % | négligeable |
| 23c | 25-OH vitamine D | +14,6 % | +34,2 → +8,2 | 0,27 | 9 % | négligeable |
| 24 | CRP ultrasensible | +2,5 % | +85,4 → −10,0 | 0,01 | 5 % | négligeable |
| 25 | ApoB | −7,7 % | −7,7 → −7,7 | 0,32 | 9 % | négligeable |
| 26 | ApoB | +3,3 % | +4,8 → +2,5 | 0,11 | 6 % | négligeable |
| 27 | Testostérone totale | +3,9 % ᵐ | +3,9 → +3,9 | 0,07 | 5 % | négligeable |
| 29 | Homocystéine | +6,4 % | +7,0 → +5,6 | 0,14 | 6 % | négligeable |
| 31 | Créatinine urinaire | −3,3 % | −7,4 → +0,3 | 0,04 | 5 % | négligeable |

Indices dérivés avec un ratio ≥ 0,3 (recalculés à partir des analytes transformés) :

| Év. | Indice dérivé | Décalage au centile 50 | Ratio | Catégorie |
|---|---|---|---|---|
| 1 | DFGe (CKD-EPI 2021) | −11,6 % | 0,59 | **faux changement possible** |
| 1 | Urée/créatinine | −20,5 % | 0,51 | **faux changement possible** |
| 3 | DFGe (CKD-EPI 2021) | +8,6 % | 0,35 | négligeable |
| 5 | Albumine/globulines | −11,2 % | 0,55 | **faux changement possible** |
| 5 | Globulines | +8,5 % | 0,49 | négligeable |
| 5 | FIB-4 | −11,5 % | 0,30 | négligeable |
| 9 | HOMA-IR | −22,0 % | 0,38 | négligeable |

**Lecture.**
- Les plus grands décalages en % sont ceux des enzymes en 2017 (ASAT −18 %, ALAT −14 %, LDH
  +15 %) et de l'insuline (−22 à +13 % selon le changement de dosage). Leur bruit est encore plus
  grand : ratios ≤ 0,45.
- Les ratios les plus élevés viennent :
  - de méthodes **non standardisées** à l'époque : folates (radio-essai), créatinine de
    1999-2000 ;
  - ou d'analytes **très régulés** : albumine (ratio 0,39 pour −4,4 %), rapport albumine/globulines.
- La CK et la LDH ne sont pas estimables : pas de changement détectable dans Q1.

## Partie (b) : décalage empirique

Saut entre cycles successifs, ajusté sur l'âge, le sexe et le groupe ethnique, moins le saut moyen
aux transitions sans événement. Moyennes géométriques ajustées ; sensibilités : ajustement sur l'IMC
et le revenu, et régression médiane.

| Év. | Marqueur | Cycles | (a) | (b) [IC 95 %] | (b) ajusté IMC, revenu | (b) médiane | Ratio (b) |
|---|---|---|---|---|---|---|---|
| 1 | Créatinine | 1999-2001 | +22,3 | +23,7 [+22,2 ; +25,0] | +23,4 | +24,8 | 1,14 |
| 2 | Créatinine | 2003-2005 | −4,0 | +4,7 [+3,8 ; +5,7] | +4,6 | +4,2 | 0,23 |
| 3 | Créatinine | 2005-2009 | −8,9 | −4,0 [−5,3 ; −2,7] | −3,8 | −4,5 | 0,23 |
| 4 | Créatinine | 1999-2003 | non chiffré | +24,7 [+23,2 ; +26,2] | +24,2 | +25,9 | 1,19 |
| 5 | Créatinine | 2015-2017 | +3,2 | +2,0 [+0,9 ; +3,2] | +1,9 | +2,2 | 0,10 |
| 4 | PAL | 1999-2003 | non chiffré | −13,9 [−15,4 ; −12,3] | −14,1 | −14,4 | 0,77 |
| 5 | PAL | 2015-2017 | +9,7 | +14,1 [+12,5 ; +15,5] | +14,5 | +14,5 | 0,65 |
| 4 | LDH | 1999-2003 | non chiffré | −16,3 [−17,2 ; −15,4] | −16,5 | −16,8 | — |
| 5 | LDH | 2015-2017 | +14,8 | +22,1 [+21,1 ; +23,2] | +22,1 | +22,0 | — |
| 4 | Phosphate | 1999-2003 | non chiffré | +11,9 [+11,1 ; +12,8] | +11,9 | +11,5 | 0,40 |
| 5 | Phosphate | 2015-2017 | −1,8 | −3,0 [−3,6 ; −2,3] | −2,9 | −3,2 | 0,13 |
| 4 | Bilirubine totale | 1999-2003 | non chiffré | +58,9 [+55,6 ; +61,8] | +57,8 | +53,4 | 0,90 |
| 5 | Bilirubine totale | 2015-2017 | −3,2 | −12,6 [−14,5 ; −10,8] | −13,1 | −21,4 | 0,32 |
| 5 | Albumine | 2015-2017 | −4,4 | −5,7 [−6,0 ; −5,4] | −5,6 | −5,7 | 0,50 |
| 5 | ASAT | 2015-2017 | −17,8 | −16,7 [−17,8 ; −15,4] | −16,3 | −17,6 | 0,36 |
| 5 | ALAT | 2015-2017 | −13,9 | −13,8 [−15,6 ; −12,0] | −13,5 | −13,4 | 0,21 |
| 5 | Urée | 2015-2017 | −3,3 | +0,8 [−0,5 ; +2,1] | +0,7 | +0,7 | 0,01 |
| 5 | Bicarbonates | 2015-2017 | +1,7 | +4,2 [+3,7 ; +4,6] | +4,1 | +3,8 | 0,11 |
| 5 | Calcium | 2015-2017 | −2,1 | −0,7 [−0,9 ; −0,5] | −0,7 | −0,7 | 0,08 |
| 5 | Cholestérol (bilan biochimique) | 2015-2017 | −3,3 | −2,2 [−3,1 ; −1,3] | −2,3 | −3,0 | 0,11 |
| 5 | CK | 2015-2017 | +5,8 | −0,7 [−3,7 ; +2,0] | −0,8 | −0,0 | — |
| 5 | Chlorure | 2015-2017 | −1,4 | −2,2 [−2,4 ; −2,1] | −2,3 | −2,4 | 0,39 |
| 5 | Glucose sérique (non à jeun) | 2015-2017 | +2,4 | −2,1 [−3,1 ; −1,1] | −1,9 | −1,0 | 0,09 |
| 5 | GGT | 2015-2017 | +9,6 | +9,9 [+7,0 ; +12,8] | +10,8 | +9,2 | 0,19 |
| 5 | Fer sérique | 2015-2017 | +8,3 | +9,9 [+7,9 ; +12,0] | +9,9 | +8,9 | 0,07 |
| 5 | Potassium | 2015-2017 | −1,4 | +3,9 [+3,5 ; +4,3] | +3,8 | +3,4 | 0,24 |
| 5 | Sodium | 2015-2017 | +0,8 | +1,3 [+1,2 ; +1,3] | +1,2 | +1,1 | 0,34 |
| 5 | Protéines totales | 2015-2017 | +0,4 | +0,3 [+0,1 ; +0,6] | +0,4 | +0,3 | 0,03 |
| 5 | Triglycérides sériques (non à jeun) | 2015-2017 | +9,6 | −3,5 [−5,9 ; −1,2] | −3,7 | −5,8 | 0,07 |
| 5 | Acide urique | 2015-2017 | +2,6 | −0,2 [−1,2 ; +1,0] | −0,6 | +0,4 | 0,01 |
| 6 | Glycémie à jeun (plasma) | 2003-2005 | +1,9 | +1,9 [+0,1 ; +3,6] | +1,6 | +2,3 | 0,06 |
| 7 | Glycémie à jeun (plasma) | 2005-2007 | +1,2 | +3,3 [+1,9 ; +4,8] | +3,7 | +2,1 | 0,11 |
| 8 | Glycémie à jeun (plasma) | 2013-2015 | +1,8 | +4,1 [+2,4 ; +5,6] | +3,9 | +2,7 | 0,14 |
| 9 | Insuline (à jeun) | 2001-2003 | −22,3 | −28,9 [−32,4 ; −24,6] | −28,8 | −23,6 | 0,54 |
| 10 | Insuline (à jeun) | 2003-2005 | +13,1 | +1,8 [−4,3 ; +8,3] | −0,4 | +2,5 | 0,02 |
| 11 | Insuline (à jeun) | 2009-2011 | −10,7 | −11,5 [−15,8 ; −7,5] | −9,7 | −10,3 | 0,22 |
| 12 | Insuline (à jeun) | 2011-2013 | −12,0 | −16,8 [−21,0 ; −12,8] | −17,0 | −17,6 | 0,31 |
| 13 | HDL | 2005-2007 | −2,4 | −5,2 [−6,5 ; −4,0] | −5,1 | −3,2 | 0,18 |
| 14 | HDL | 2001-2003 | non chiffré | +2,9 [+1,5 ; +4,2] | +3,5 | +3,3 | 0,07 |
| 15 | Cholestérol total | 2005-2007 | non chiffré | +0,3 [−0,8 ; +1,4] | +0,5 | −0,0 | 0,01 |
| 15 | Triglycérides (à jeun) | 2005-2007 | non chiffré | +0,4 [−2,9 ; +4,5] | +1,9 | +3,0 | 0,00 |
| 16 | HbA1c | 2005-2007 | non chiffré | +1,7 [+1,0 ; +2,4] | +1,5 | +1,7 | 0,16 |
| 17 | Leucocytes | 2009-2013 | non chiffré | +2,7 [+1,2 ; +4,2] | +3,2 | +3,4 | 0,06 |
| 17 | Neutrophiles (%) | 2009-2013 | non chiffré | +0,5 [−0,3 ; +1,2] | +0,5 | +0,3 | 0,01 |
| 17 | Lymphocytes (%) | 2009-2013 | non chiffré | −2,4 [−3,7 ; −1,1] | −2,4 | −1,9 | 0,08 |
| 17 | Monocytes (%) | 2009-2013 | non chiffré | +9,9 [+8,5 ; +11,4] | +9,7 | +6,4 | 0,17 |
| 17 | Éosinophiles (%) | 2009-2013 | non chiffré | −5,1 [−8,1 ; −1,6] | −4,3 | −6,6 | 0,09 |
| 17 | Basophiles (%) | 2009-2013 | non chiffré | +0,0 [+0,0 ; +0,1] | +0,0 | +0,1 | 0,05 |
| 17 | Hématies | 2009-2013 | non chiffré | +1,3 [+0,8 ; +1,7] | +1,2 | +1,2 | 0,12 |
| 17 | Hémoglobine | 2009-2013 | non chiffré | −0,0 [−0,5 ; +0,4] | −0,1 | −0,2 | 0,00 |
| 17 | Hématocrite | 2009-2013 | non chiffré | +1,4 [+0,9 ; +1,9] | +1,3 | +1,1 | 0,14 |
| 17 | VGM | 2009-2013 | non chiffré | +0,1 [−0,2 ; +0,5] | +0,1 | +0,0 | 0,05 |
| 17 | TCMH | 2009-2013 | non chiffré | −1,3 [−1,6 ; −0,9] | −1,3 | −1,2 | 0,28 |
| 17 | CCMH | 2009-2013 | non chiffré | −1,4 [−1,6 ; −1,3] | −1,4 | −1,4 | 0,32 |
| 17 | RDW | 2009-2013 | non chiffré | +5,5 [+5,0 ; +5,9] | +5,5 | +5,9 | 0,79 |
| 17 | Plaquettes | 2009-2013 | non chiffré | −0,6 [−1,8 ; +0,7] | −0,7 | −0,1 | 0,02 |
| 17 | VPM | 2009-2013 | non chiffré | +10,4 [+9,8 ; +10,9] | +10,6 | +8,7 | 0,77 |
| 18 | Ferritine | 2007-2009 | +7,6 | +11,0 [+0,7 ; +19,2] | +13,1 | +14,5 | 0,13 |
| 19 | Ferritine | 2009-2015 | +8,4 | −2,2 [−10,2 ; +5,7] | −2,9 | −2,4 | 0,05 |
| 20 | Vitamine B12 | 2005-2011 | +14,7 | +11,1 [+8,0 ; +14,1] | +11,7 | +10,4 | 0,23 |
| 21 | Vitamine B12 | 2011-2013 | non chiffré | −1,9 [−4,2 ; +0,2] | −1,6 | −3,1 | 0,06 |
| 22 | Folates érythrocytaires | 2005-2007 | +84,7 | +81,6 [+78,7 ; +85,4] | +83,5 | +83,6 | 2,73 |
| 23b | 25-OH vitamine D | 2001-2003 | +1,4 | −3,8 [−5,5 ; −2,2] | −3,5 | −2,9 | 0,11 |
| 23b | 25-OH vitamine D | 2003-2005 | +1,4 | −1,6 [−3,3 ; +0,3] | −2,0 | −2,7 | 0,04 |
| 23c | 25-OH vitamine D | 2005-2007 | +14,6 | +2,1 [+0,4 ; +4,1] | +2,9 | +5,7 | 0,04 |
| 24 | CRP ultrasensible | 2015-2017 | +2,5 | — | — | — | — |
| 25 | ApoB | 2005-2007 | −7,7 | −6,6 [−8,4 ; −4,9] | −5,8 | −7,1 | 0,28 |
| 26 | ApoB | 2013-2015 | +3,3 | +4,8 [+3,1 ; +7,0] | +5,1 | +3,7 | 0,15 |
| 27 | Testostérone totale | 2011-2013 | +3,9 | — | — | — | — |
| 28 | T4 libre | 2007-2011 | non chiffré | — | — | — | — |
| 28 | TSH | 2007-2011 | non chiffré | −5,4 [−11,1 ; +1,1] | −5,6 | −7,6 | 0,12 |
| 29 | Homocystéine | 1999-2003 | +6,4 | — | — | — | — |
| 30 | Homocystéine | 2003-2005 | non chiffré | — | — | — | — |
| 31 | Créatinine urinaire | 2005-2007 | −3,3 | −4,0 [−6,8 ; −0,9] | −3,8 | −5,6 | 0,05 |
| 32 | Fer (fichier fer/CTF) | 1999-2003 | non chiffré | −6,3 [−11,6 ; +0,2] | −8,2 | −6,4 | 0,11 |

**Lecture.**
- **(b) retrouve (a) quand la diffusion n'est pas ajustée** : même signe dans 20 cas sur 24
  (prédiction P2).
  - Exemples d'accord : ASAT −17 % contre −18 % ; ALAT −14 % contre −14 % ; GGT +10 % contre
    +10 % ; folates +82 % contre +85 % ; créatinine de 1999 +24 % contre +22 %.
  - Désaccords : TG sériques 2017 (−3,5 % contre +9,6 %), CK (−0,7 % contre +5,8 %), urée
    (+0,8 % contre −3,3 %) et créatinine 2005-2006.
  - La créatinine 2005-2006 est un artefact de sens. (a) mesure le passage du laboratoire de
    2005-2006 à la méthode de référence, alors que (b) mesure l'entrée dans ce laboratoire depuis
    2003-2004. Les deux disent la même chose : ce laboratoire mesurait environ 4 % trop haut. En
    alignant les sens, l'accord est de 21 sur 24 (88 %).
- **Quand la diffusion est ajustée, il reste parfois un décalage résiduel.**
  - Bilirubine, PAL, phosphore et LDH entre 1999 et 2003 : de −16 à +59 %. Le changement de
    laboratoire de 2001-2002 a été corrigé, mais le laboratoire de 1999-2000 diffère encore.
  - Vitamine D (2001-2007) : de −4 à +2 %. La conversion LC-MS/MS du NCHS laisse un écart faible.
- **Changements non chiffrés par le NCHS** :
  - NFS (automate Coulter HMX → DxH en 2012) : RDW +5,5 % et VPM +10 % (ratios 0,79 et 0,77,
    « faux changement possible ») ; hématocrite +1,4 % ;
  - HbA1c (2007) : +1,7 % ;
  - HDL : −5 % (2007) et +3 % (méthode directe, 2003).

## Effet sur la classification

Part des adultes du cycle transformé au-delà du seuil, avant et après application de l'équation
(écarts d'au moins 2 points). R = seuil clinique ; S = limite de l'intervalle statistique D1.

| Év. | Marqueur | Seuil | Type | Avant | Après | Points |
|---|---|---|---|---|---|---|
| 1 | Créatinine | intervalle statistique D1, limite basse | S | 16,7 % | 3,6 % | **−13,1** |
| 1 | Créatinine | intervalle statistique D1, limite haute | S | 3,0 % | 6,5 % | **+3,4** |
| 1 | DFGe (CKD-EPI 2021) | < 60 mL/min/1,73 m² (G3a et au-delà) | R | 3,3 % | 5,6 % | **+2,3** |
| 2 | Créatinine | intervalle statistique D1, limite basse | S | 0,6 % | 3,0 % | **+2,4** |
| 3 | Créatinine | intervalle statistique D1, limite basse | S | 0,6 % | 4,2 % | **+3,6** |
| 3 | Créatinine | intervalle statistique D1, limite haute | S | 8,2 % | 5,0 % | **−3,1** |
| 3 | DFGe (CKD-EPI 2021) | < 60 mL/min/1,73 m² (G3a et au-delà) | R | 7,1 % | 5,0 % | **−2,1** |
| 5 | ALAT | intervalle statistique D1, limite basse | S | 2,3 % | 12,7 % | **+10,4** |
| 5 | ASAT | intervalle statistique D1, limite basse | S | 3,3 % | 29,4 % | **+26,1** |
| 5 | PAL | intervalle statistique D1, limite haute | S | 4,0 % | 7,0 % | **+3,0** |
| 5 | Bilirubine totale | intervalle statistique D1, limite basse | S | 18,7 % | 32,4 % | **+13,7** |
| 5 | Albumine | intervalle statistique D1, limite basse | S | 3,2 % | 9,8 % | **+6,6** |
| 5 | Albumine | intervalle statistique D1, limite haute | S | 6,0 % | 0,7 % | **−5,3** |
| 5 | Créatinine | intervalle statistique D1, limite basse | S | 6,5 % | 4,0 % | **−2,5** |
| 5 | Urée | intervalle statistique D1, limite haute | S | 10,6 % | 8,0 % | **−2,6** |
| 5 | Sodium | intervalle statistique D1, limite haute | S | 2,6 % | 7,3 % | **+4,7** |
| 5 | Chlorure | intervalle statistique D1, limite basse | S | 6,4 % | 19,1 % | **+12,7** |
| 5 | Chlorure | intervalle statistique D1, limite haute | S | 3,1 % | 0,5 % | **−2,6** |
| 5 | Calcium | intervalle statistique D1, limite basse | S | 3,9 % | 13,9 % | **+9,9** |
| 5 | Acide urique | intervalle statistique D1, limite haute | S | 7,9 % | 9,9 % | **+2,1** |
| 5 | Triglycérides sériques (non à jeun) | ≥ 1,7 mmol/L (150 mg/dL), non à jeun | R | 38,8 % | 43,3 % | **+4,6** |
| 5 | Globulines | intervalle statistique D1, limite basse | S | 3,6 % | 0,9 % | **−2,7** |
| 5 | Globulines | intervalle statistique D1, limite haute | S | 3,4 % | 6,9 % | **+3,5** |
| 6 | Glycémie à jeun (plasma) | ≥ 5,6 mmol/L (100 mg/dL) (ADA) | R | 38,8 % | 44,2 % | **+5,4** |
| 7 | Glycémie à jeun (plasma) | ≥ 5,6 mmol/L (100 mg/dL) (ADA) | R | 46,7 % | 51,1 % | **+4,4** |
| 8 | Glycémie à jeun (plasma) | ≥ 5,6 mmol/L (100 mg/dL) (ADA) | R | 47,5 % | 51,6 % | **+4,1** |
| 9 | Insuline (à jeun) | intervalle statistique D1, limite basse | S | 0,3 % | 6,0 % | **+5,7** |
| 10 | Insuline (à jeun) | intervalle statistique D1, limite basse | S | 4,8 % | 0,7 % | **−4,1** |
| 11 | Insuline (à jeun) | intervalle statistique D1, limite haute | S | 12,0 % | 9,8 % | **−2,3** |
| 12 | Insuline (à jeun) | intervalle statistique D1, limite haute | S | 10,9 % | 8,6 % | **−2,3** |
| 22 | Folates érythrocytaires | intervalle statistique D1, limite basse | S | 3,4 % | 0,1 % | **−3,2** |
| 22 | Folates érythrocytaires | intervalle statistique D1, limite haute | S | 3,3 % | 36,7 % | **+33,4** |
| 23a | 25-OH vitamine D | < 20 ng/mL (50 nmol/L) | R | 43,2 % | 38,9 % | **−4,3** |
| 23a | 25-OH vitamine D | < 30 ng/mL (75 nmol/L) (sensibilité 30) | R | 82,9 % | 79,9 % | **−2,9** |
| 23b | 25-OH vitamine D | < 30 ng/mL (75 nmol/L) (sensibilité 30) | R | 80,4 % | 77,9 % | **−2,5** |
| 23c | 25-OH vitamine D | < 20 ng/mL (50 nmol/L) | R | 52,4 % | 42,5 % | **−9,9** |
| 23c | 25-OH vitamine D | < 30 ng/mL (75 nmol/L) (sensibilité 30) | R | 90,5 % | 83,4 % | **−7,1** |
| 25 | ApoB | intervalle statistique D1, limite haute | S | 5,5 % | 3,1 % | **−2,4** |
| 29 | Homocystéine | intervalle statistique D1, limite basse | S | 5,1 % | 2,7 % | **−2,4** |

**Lecture.** Des décalages faibles devant le bruit déplacent beaucoup de personnes autour d'un
seuil, comme le jeûne dans Q2.
- Les limites basses des enzymes et des électrolytes sont les plus touchées en 2017.
- Pour la glycémie, chaque changement d'instrument ajoute 4 à 5 points au-dessus du seuil ADA.
- Les intervalles S de D1 ont été calculés sur NHANES 2003-2010, donc avec les méthodes de ces
  années. Ils ne sont pas transposables tels quels aux résultats d'une autre méthode.

## Partie (c) : écarts entre laboratoires de routine (littérature)

Études retenues selon les critères pré-enregistrés (5 requêtes, 93 références examinées) :
- **EEQ espagnole de catégorie 1**, 2019, matériau commutable, texte complet. Les CV sont publiés
  au sein de chaque groupe de méthode et d'instrument ; les biais entre groupes ne le sont qu'en
  figure. Ces CV sont donc des **bornes basses** de l'écart entre laboratoires.
- **EurA1c**, 2026, sang total frais, résumé.
- **INSTAND**, 2019, CRP, texte complet. C'est la CRP classique, pas la CRP ultrasensible ; le CV
  est un ordre de grandeur lu dans le texte.
- En sensibilité : **RfB** (Allemagne, 2021, texte complet, matériau lyophilisé) et **Equalis**
  (Suède, 2019, résumé).

Les valeurs brutes extraites restent dans `private/panel/Q5_litterature/`. Le tableau ne donne que
les valeurs dérivées.

| Marqueur | Étude (lu) | Décalage typique entre deux laboratoires | Changement détectable, même laboratoire (Q1) | Changement détectable, deux laboratoires | Rapport | Ratio | Qualité |
|---|---|---|---|---|---|---|---|
| Calcium | Spain 2019 (TC) | ±5,1 % | +9,5 % | +14,2 % | ×1,49 | 0,53 | borne basse (CV au sein des groupes de méthode) |
| Chlorure | Spain 2019 (TC) | ±1,5 % | +6,1 % | +6,8 % | ×1,12 | 0,25 | borne basse (CV au sein des groupes de méthode) |
| Magnésium | Spain 2019 (TC) | ±3,2 % | +9,4 % | +11,5 % | ×1,22 | 0,34 | borne basse (CV au sein des groupes de méthode) |
| Potassium | Spain 2019 (TC) | ±1,3 % | +16,0 % | +16,3 % | ×1,02 | 0,08 | borne basse (CV au sein des groupes de méthode) |
| Sodium | Spain 2019 (TC) | ±0,9 % | +3,7 % | +4,2 % | ×1,12 | 0,25 | borne basse (CV au sein des groupes de méthode) |
| PAL | Spain 2019 (TC) | ±8,1 % | +21,9 % | +28,4 % | ×1,30 | 0,37 | borne basse (CV au sein des groupes de méthode) |
| ALAT | Spain 2019 (TC) | ±13,2 % | +181,4 % | +189,5 % | ×1,04 | 0,07 | borne basse (CV au sein des groupes de méthode) |
| ASAT | Spain 2019 (TC) | ±6,0 % | +86,4 % | +88,4 % | ×1,02 | 0,07 | borne basse (CV au sein des groupes de méthode) |
| GGT | Spain 2019 (TC) | ±4,6 % | +53,3 % | +54,7 % | ×1,03 | 0,09 | borne basse (CV au sein des groupes de méthode) |
| Bilirubine totale | Spain 2019 (TC) | ±6,9 % | +65,8 % | +68,6 % | ×1,04 | 0,11 | borne basse (CV au sein des groupes de méthode) |
| Créatinine | Spain 2019 (TC) | ±4,3 % | +20,8 % | +22,9 % | ×1,10 | 0,21 | borne basse (CV au sein des groupes de méthode) |
| Glycémie à jeun (plasma) | Spain 2019 (TC) | ±3,2 % | +29,4 % | +30,4 % | ×1,03 | 0,11 | borne basse (CV au sein des groupes de méthode) |
| Protéines totales | Spain 2019 (TC) | ±3,1 % | +10,4 % | +12,2 % | ×1,18 | 0,30 | borne basse (CV au sein des groupes de méthode) |
| Créatinine | Germany RfB 2019 (publié 2021) (TC) — sensibilité | ±6,9 % | +20,8 % | +25,8 % | ×1,24 | 0,33 | sensibilité |
| Calcium | Germany RfB 2019 (publié 2021) (TC) — sensibilité | ±4,5 % | +9,5 % | +13,3 % | ×1,40 | 0,47 | sensibilité |
| HbA1c | EurA1c 2026 (R) | ±3,9 % | +10,4 % | +13,2 % | ×1,27 | 0,37 |  |
| HbA1c | Germany RfB 2019 (publié 2021) (TC) — sensibilité | ±7,5 % | +10,4 % | +18,8 % | ×1,81 | 0,72 | sensibilité |
| Créatinine | Equalis (Suède) 2019 (R) — sensibilité | ±6,6 % | +20,8 % | +25,4 % | ×1,22 | 0,32 | sensibilité |
| CRP ultrasensible | INSTAND 2019 (TC) | ±32,3 % | +351,4 % | +397,3 % | ×1,13 | 0,09 | ordre de grandeur lu dans le texte |

**Lecture.**
- Passer d'un laboratoire de routine à un autre élargit le changement détectable de 2 à 50 %.
  L'élargissement est fort pour les analytes très régulés (calcium, PAL, HbA1c, magnésium,
  protéines), faible pour les enzymes, dont le bruit biologique domine.
- Le calcium atteint un ratio de 0,53 (« faux changement possible »), même avec une borne basse.
- **Rien trouvé avec ces requêtes** pour les marqueurs suivants :
  - lipides (cholestérol total, LDL, HDL, TG) ;
  - numération (NFS) ;
  - vitamines (B12, folates, vitamine D) ;
  - insuline ;
  - albumine, urée, bicarbonates, lipase, bilirubine conjuguée, globulines, osmolalité.

  Pour ces marqueurs, **l'écart entre laboratoires de routine reste inconnu**. Il ne peut être
  mesuré que sur des données réelles venant de plusieurs laboratoires.

## Partie (d) : un changement de laboratoire peut-il imiter ou masquer une intervention ?

ρ = |décalage| / |effet moyen de l'intervention| (Q1, en %). Pour chaque couple, le plus grand
décalage du marqueur.
- « Peut imiter » : même signe que l'effet. « Peut masquer » : signe opposé. ρ ≥ 0,5 dans les deux
  cas.
- « Suffit » : ρ ≥ 1.
- Les décalages de (c) n'ont pas de signe (deux laboratoires pris au hasard).
- Pour les TG, le cholestérol et la glycémie, le décalage vient de l'analyte du bilan biochimique :
  c'est le même dosage, fait dans un autre laboratoire.

| Marqueur | Intervention | Effet (Q1) | Décalage | ρ | Signalement |
|---|---|---|---|---|---|
| ALAT | Perte de poids de 5 % (essai unique, petite taille) | −16,7 % | −13,9 % ((a) év. 5) | 0,83 | peut imiter |
| ALAT | Perte de poids de 5 kg | −27,7 % | −13,9 % ((a) év. 5) | 0,50 | peut imiter |
| ALAT | Alimentation méditerranéenne | −37,7 % | −13,9 % ((a) év. 5) | 0,37 | non |
| ALAT | Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | −38,7 % | −13,9 % ((a) év. 5) | 0,36 | non |
| ASAT | Perte de poids de 5 kg | −14,7 % | −17,8 % ((a) év. 5) | 1,21 | peut imiter (suffit) |
| CRP | Perte de poids de 5 % (essai unique, petite taille) | +5,1 % | +32,3 % ((c) INSTAND 2019, PLoS One, doi:10.1371/journal.pone.0221426) | 6,34 | peut imiter ou masquer (suffit) |
| CRP | Alimentation méditerranéenne | −28,5 % | +32,3 % ((c) INSTAND 2019, PLoS One, doi:10.1371/journal.pone.0221426) | 1,13 | peut imiter ou masquer (suffit) |
| GGT | Alimentation méditerranéenne | −10,9 % | +9,6 % ((a) év. 5) | 0,88 | peut masquer |
| Glycémie à jeun (plasma) | Activité physique aérobie | −2,9 % | +3,2 % ((c) Spain 2019, Biochem Med (Zagreb), doi:10.11613/BM.2019.010701) | 1,11 | peut imiter ou masquer (suffit) |
| Glycémie à jeun (plasma) | Alimentation méditerranéenne | −3,2 % | +3,2 % ((c) Spain 2019, Biochem Med (Zagreb), doi:10.11613/BM.2019.010701) | 1,00 | peut imiter ou masquer (suffit) |
| Glycémie à jeun (plasma) | Perte de poids de 5 % (essai unique, petite taille) | −4,1 % | +3,2 % ((c) Spain 2019, Biochem Med (Zagreb), doi:10.11613/BM.2019.010701) | 0,79 | peut imiter ou masquer |
| Hémoglobine | Fer oral (femmes réglées) | +3,8 % | −0,0 % ((b) év. 17) | 0,00 | non |
| HbA1c | Alimentation méditerranéenne | −2,8 % | +3,9 % ((c) EurA1c 2026, Clin Chem Lab Med, doi:10.1515/cclm-2026-0276) | 1,37 | peut imiter ou masquer (suffit) |
| HbA1c | Activité physique structurée | −12,6 % | +3,9 % ((c) EurA1c 2026, Clin Chem Lab Med, doi:10.1515/cclm-2026-0276) | 0,31 | non |
| Homocystéine | Acide folique 0,8 mg/j | −23,0 % | +6,4 % ((a) év. 29) | 0,28 | non |
| HDL | Perte de poids de 5 % (essai unique, petite taille) | +0,3 % | +2,9 % ((b) év. 14) | 9,74 | peut imiter (suffit) |
| HDL | Alimentation méditerranéenne | +2,7 % | +2,9 % ((b) év. 14) | 1,08 | peut imiter (suffit) |
| HDL | Perte de poids de 5 kg (poids stabilisé) | +3,6 % | +2,9 % ((b) év. 14) | 0,81 | peut imiter |
| HDL | Activité physique (toutes formes) | +4,4 % | +2,9 % ((b) év. 14) | 0,66 | peut imiter |
| HDL | Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | +6,7 % | +2,9 % ((b) év. 14) | 0,44 | non |
| HOMA-IR | Alimentation méditerranéenne | −18,9 % | −22,0 % ((a) év. 9) | 1,16 | peut imiter (suffit) |
| Insuline (à jeun) | Alimentation méditerranéenne | −9,9 % | −22,3 % ((a) év. 9) | 2,26 | peut imiter (suffit) |
| Insuline (à jeun) | Perte de poids de 5 % (essai unique, petite taille) | −13,6 % | −22,3 % ((a) év. 9) | 1,64 | peut imiter (suffit) |
| Insuline (à jeun) | Activité physique (toutes formes) | −19,8 % | −22,3 % ((a) év. 9) | 1,13 | peut imiter (suffit) |
| LDL (calculé, à jeun) | Activité physique (toutes formes) | −5,9 % | +1,4 % ((a) év. 13) | 0,23 | non |
| LDL (calculé, à jeun) | Alimentation méditerranéenne | −6,7 % | +1,4 % ((a) év. 13) | 0,20 | non |
| LDL (calculé, à jeun) | Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | −7,3 % | +1,4 % ((a) év. 13) | 0,19 | non |
| LDL (calculé, à jeun) | Statine (atorvastatine 10 mg/j ou équivalent) | −40,0 % | +1,4 % ((a) év. 13) | 0,03 | non |
| Cholestérol total | Alimentation méditerranéenne | −2,8 % | −3,3 % ((a) év. 5) | 1,19 | peut imiter (suffit) |
| Cholestérol total | Activité physique (toutes formes) | −2,9 % | −3,3 % ((a) év. 5) | 1,15 | peut imiter (suffit) |
| Triglycérides (à jeun) | Activité physique (toutes formes) | −6,8 % | +9,6 % ((a) év. 5) | 1,41 | peut masquer (suffit) |
| Triglycérides (à jeun) | Alimentation méditerranéenne | −10,4 % | +9,6 % ((a) év. 5) | 0,92 | peut masquer |
| Triglycérides (à jeun) | Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | −23,7 % | +9,6 % ((a) év. 5) | 0,40 | non |
| Triglycérides (à jeun) | Oméga-3 (EPA + DHA), 2 g/j | −36,1 % | +9,6 % ((a) év. 5) | 0,26 | non |
| Triglycérides (à jeun) | Perte de poids de 5 % (essai unique, petite taille) | −37,9 % | +9,6 % ((a) év. 5) | 0,25 | non |
| 25-OH vitamine D | Vitamine D3, 25 µg/j | +97,5 % | +14,6 % ((a) év. 23c) | 0,15 | non |

**Lecture.**
- Les effets moyens des interventions réalistes sont du même ordre que les décalages de méthode
  pour les TG, l'insuline, le HOMA-IR, le cholestérol total, le HDL, la glycémie, l'HbA1c, la
  GGT, l'ALAT, l'ASAT et la CRP. Pour 11 des 15 marqueurs comparables, ρ ≥ 0,5.
- Un changement de laboratoire entre deux bilans peut donc faire croire à un effet, ou l'effacer.
  C'est un effet moyen : il s'ajoute au bruit individuel, déjà grand (Q1).
- Exceptions :
  - vitamine D : la supplémentation (+97 %) dépasse de loin tout décalage de méthode ;
  - LDL sous statine (−40 %) ;
  - homocystéine sous acide folique (−23 %) ;
  - hémoglobine sous fer (pas de décalage observé).

## Prédictions

| Prédiction | Résultat | Verdict |
|---|---|---|
| P1 : au moins 3 des 5 ratios (a) les plus élevés viennent d'analytes à faible variabilité, et aucune enzyme n'atteint 1 | 5 plus élevés : folates érythrocytaires, créatinine, PAL, insuline, albumine (2 à faible variabilité) ; aucune enzyme ≥ 1 | **non vérifiée** |
| P2 : (b) a le même signe que (a) dans au moins 75 % des cas (diffusion non ajustée, décalage ≥ 3 %) | 20 sur 24 (83 %) ; 21 sur 24 en alignant le sens de la créatinine 2005-2006 | **vérifiée** |
| P3 : ρ ≥ 0,5 pour les TG, l'ALAT et la vitamine D, et pour au moins la moitié des marqueurs | TG : oui ; ALAT : oui ; vitamine D : **non** (ρ ≤ 0,15) ; 11 marqueurs sur 15 (73 %) | **non vérifiée** |

**Lecture de P1.** Elle échoue pour une raison instructive. Les plus grands ratios viennent de
méthodes alors non standardisées (folates par radio-essai, créatinine de 1999), plus que de la
faible variabilité. La seconde moitié de P1 tient : les enzymes, malgré des décalages de −14 à
−18 %, restent sous le changement détectable. Et la partie (c) va dans le sens de l'idée de départ :
les analytes très régulés sont ceux dont le changement détectable grandit le plus entre deux
laboratoires.

**Lecture de P3.** Elle échoue sur la vitamine D. La prédiction supposait un effet d'intervention
de l'ordre des décalages de méthode. Or l'effet de 25 µg/j (+97 %, calculé sur une médiane basse de
2001-2002) est cinq fois plus grand que le plus fort décalage au centile 50.

## Écarts et corrections

- **Régression médiane (sensibilité de b).** Le premier calcul, par programmation linéaire, était
  trop long (plus d'une heure). Il a été arrêté sans qu'aucun résultat soit lu. La médiane est
  estimée par moindres carrés repondérés itératifs, qui convergent vers le même estimateur
  (moindres écarts absolus).
- **Échelle log (corrigé avant la lecture des ratios).** Pour la bilirubine, le LDL et le rapport
  LDL/HDL, quelques valeurs nulles ou négatives faisaient passer le décalage sur l'échelle
  additive. Le ratio était alors calculé contre un changement détectable exprimé en %. Corrigé
  comme dans Q1 : valeurs positives seulement.
- **Unités dans la classification (corrigé avant la rédaction).**
  - Les intervalles D1 des folates érythrocytaires sont en ng/mL, ceux de Q5 en nmol/L :
    conversion ×2,265.
  - L'osmolalité est exclue de la classification : l'intervalle D1 porte sur la valeur diffusée
    par NHANES, alors que Q5 la recalcule par une autre formule.
- **Événement 4 (biochimie, 2001-2002)** : la comparaison 1999 → 2003 englobe aussi l'événement 1
  (créatinine de 1999-2000). Le décalage empirique de la créatinine sur cette période cumule les
  deux.
- **Recherche bibliographique.** Le filtre de date de l'outil de recherche n'a pas été appliqué
  par le serveur. Les références antérieures à 2005 ont été écartées à la lecture des titres, comme
  le prévoit le critère 6.
- **V1** : échec partiel, rapporté ci-dessus sans changement du protocole.

## Limites

- Les méthodes de NHANES ne sont pas celles des laboratoires de la population cible.
- Les IC des équations de passage ne sont pas propagés (92 à 773 échantillons par étude).
- La partie (b) ne retire qu'en partie la tendance séculaire et les changements de composition de
  l'échantillon.
- Les CV de l'EEQ espagnole sont des bornes basses. Plusieurs marqueurs n'ont aucune donnée entre
  laboratoires de routine.
- Les effets d'intervention de Q1 sont des effets moyens d'essais. ρ compare des moyennes, pas des
  personnes.
- Les changements détectables de Q1 sont des bornes basses (remesures à environ 2 semaines).
- NHANES est américain.
