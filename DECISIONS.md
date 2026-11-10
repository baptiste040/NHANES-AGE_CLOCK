# Journal des décisions

Règle (depuis le 2026-11-09) : la cohorte de validation 2007-2010 a été **vue** lors
du jalon 1. Toute modification du panel ou du modèle se décide par validation
croisée « un cycle retiré » sur le développement (1999-2006) uniquement, jamais
d'après les résultats de validation. Les résultats de validation ne sont rapportés
qu'une fois les changements arrêtés, en signalant que le panel a évolué.

Format : date — décision — pourquoi — données utilisées pour décider.

## Jalon 1 (avant ouverture de la validation)

| Date | Décision | Pourquoi | Données |
|---|---|---|---|
| 2026-11-09 | Découpage développement 1999-2006 / validation 2007-2010 / secondaire 2015-2018 | Seuls cycles avec CRP et suivi long ; validation temporelle | — |
| 2026-11-09 | Population 20-79 ans, hors femmes enceintes | Âge NHANES plafonné à 85 (≤ 2006) puis 80 ans ; biomarqueurs modifiés par la grossesse | Documentation NHANES |
| 2026-11-09 | Systèmes : cardiovasculaire, métabolique, rénal, hépatique, inflammatoire/hématologique | Choix clinique (CRP seule trop mince) | — |
| 2026-11-09 | LDL facultatif, hors modèle | Mesuré sur le seul sous-échantillon à jeun | Documentation NHANES |
| 2026-11-09 | Plancher CRP à 0,1 mg/L avant log | Limite de détection du dosage standard ; harmonise CRP et hs-CRP | Documentation NHANES |
| 2026-11-09 | Recalibration de la créatinine 1999-2000 et 2005-2006 | Équations recommandées par NHANES | Documentation NHANES |
| 2026-11-09 | Âge et sexe jamais pénalisés | Pénaliser l'âge déforme l'échelle de l'âge biologique | Développement (essai), constat méthodologique |
| 2026-11-09 | Pénalisation ridge des marqueurs = 0 | Meilleur C moyen en CV « un cycle retiré » sur la grille [0 ; 0,003 ; 0,01 ; 0,03] | CV 1999-2006 (`penalisation_cv.csv`) |

Transparence : lors d'un test de mise au point, le C de validation a été affiché pour
3 valeurs de pénalisation (0 ; 0,01 ; 0,05) avant que le choix ne soit confié à la CV
sur le développement. La valeur retenue est celle de la CV.

## Jalon 2 (validation vue — décisions sur CV 1999-2006 uniquement)

| Date | Décision | Pourquoi | Données |
|---|---|---|---|
| 2026-11-09 | Système rénal : + ACR urinaire + urée | Option (iii) passe le critère pré-enregistré (voir 2.1) | CV 1999-2006 |
| 2026-11-09 | **Déviation** : urée retirée, système rénal = créatinine + ACR | Apport marginal de l'urée sous le seuil (voir 2.1, déviation) | CV 1999-2006 |
| 2026-11-09 | Critère de sélection corrigé pour la suite (voir « Critère corrigé ») | Défaut de formulation révélé en 2.1 | — |
| 2026-11-09 | Fréquence cardiaque en spline à 4 nœuds | Non-linéarité, LR p = 0,017 (règle pré-enregistrée, voir 3.0) | Développement 1999-2006 |
| 2026-11-09 | Système cardiovasculaire : + fréquence cardiaque ; traitements non retenus | Critère corrigé (voir 3) | CV 1999-2006 |

### Pré-enregistrement 2.1 — système rénal (écrit avant le test, 2026-11-09)

**Candidats** (testés comme ajouts au système rénal, pas comme fusion) :
- ACR urinaire (albumine/créatinine), mg/mmol = albumine urinaire (mg/L) / créatinine
  urinaire (mg/dL) × 100 / 8,842 ; plage plausible [0 ; 500] ; plancher 0,1 ; log ; linéaire.
- Urée sérique, mmol/L = BUN (mg/dL) × 0,357 ; plage [0,5 ; 60] ; log ; linéaire.

Ces transformations sont fixées a priori (pas d'ajustement après coup).

**Options évaluées** : (i) + ACR ; (ii) + urée ; (iii) + ACR + urée.

**Procédure** : CV « un cycle retiré » sur 1999, 2001, 2003, 2005 (4 plis). Entraînement
sur 3 cycles, C de Harrell sur le cycle retiré. Comparaison sur les **mêmes participants** :
cohorte de développement en cas complets sur le panel actuel **et** les candidats.
Pénalisation 0 (décision du jalon 1). Mortalité toutes causes, horizon 10 ans.

**Critère** : une option est retenue si les trois conditions sont réunies :
- a. gain de C moyen du modèle **rénal** ≥ 0,003 sur les 4 cycles retirés ;
- b. gain de C du modèle rénal > 0 sur au moins 3 des 4 cycles retirés ;
- c. gain de C moyen du modèle **global** ≥ 0.

Si plusieurs options passent : on retient l'option (iii) si elle passe, sinon la ou les
variables qui passent individuellement.

**Garde-fou** : si un candidat manque chez plus de 15 % des participants de la cohorte de
développement actuelle, c'est signalé avant la décision (perte d'effectif, biais de
sélection possible), et la décision est soumise à validation humaine.

### Résultat 2.1 — système rénal (2026-11-09)

Données : cycles 1999-2006 uniquement (la validation n'a pas été chargée).
Manquants dans la cohorte de développement (n = 13 986) : ACR 0,7 % (103), urée 0 % —
sous le garde-fou de 15 %. Cohorte commune aux options : n = 13 883.

| Option | Gain C rénal moyen (a ≥ 0,003) | Plis positifs (b ≥ 3/4) | Gain C global moyen (c ≥ 0) | Retenue |
|---|---|---|---|---|
| + ACR | +0,0080 | 4/4 | +0,0018 | oui |
| + urée | +0,0007 | 4/4 | +0,0000 | non (a) |
| + ACR + urée | +0,0087 | 4/4 | +0,0019 | oui |

Détail par pli : `reports/selection/renal/`.

**Décision (application stricte de la règle pré-enregistrée)** : l'option (iii) passe,
donc ACR **et** urée entrent dans le système rénal.

Remarque : la règle « (iii) si elle passe » laisse entrer l'urée alors que son apport
propre (+0,0007 seule ; +0,0007 en plus de l'ACR) est sous le seuil (a). Défaut de
formulation de la règle, identifié après le test ; toute modification serait une
déviation à documenter ici.

### Déviation documentée 2.1 — retrait de l'urée (2026-11-09)

- **Ce que disait la règle** : « si plusieurs options passent, on retient l'option (iii)
  si elle passe ». L'option (iii) ACR + urée passait les trois conditions
  (+0,0087 ; 4/4 ; +0,0019), d'où l'entrée de l'urée.
- **Déviation** : l'urée est retirée. Son gain marginal en plus de l'ACR est de +0,0007
  (0,0087 − 0,0080), et de +0,0007 seule : sous le seuil (a) de 0,003. Elle n'apporte
  rien au système et ajouterait une variable à collecter.
- **Données** : la décision repose uniquement sur la validation croisée 1999-2006 ; la
  cohorte 2007-2010 n'a pas été consultée.
- Décidé par le responsable du projet après lecture des résultats de CV.

### Critère corrigé (applicable à partir du point 3, écrit avant tout test)

Une option (variable ou groupe) est retenue si les trois conditions a, b, c sont réunies
(inchangées : gain de C moyen du système ≥ 0,003 ; gain > 0 sur au moins 3 des 4 cycles
retirés ; gain de C moyen du modèle global ≥ 0).

**Correction** : au sein d'un groupe retenu, une variable n'est conservée que si :
- elle passe le critère seule ; **ou**
- son apport marginal dans le groupe (gain de C moyen du système du groupe complet moins
  celui du groupe sans elle) atteint 0,003.

Les variables d'un groupe qui ne remplissent aucune des deux conditions sont retirées.
Garde-fou des 15 % de manquants inchangé.

### Pré-enregistrement 3 — système cardiovasculaire (écrit avant le test, 2026-11-09)

**Candidats**
- Fréquence cardiaque de repos (`BPXPLS`, pouls sur 60 s), bpm, plage [30 ; 200].
- Traitement antihypertenseur déclaré (questionnaire `BPQ` : BPQ020 → BPQ040A → BPQ050A), 0/1.
- Traitement hypolipémiant déclaré (questionnaire `BPQ` : BPQ060 → BPQ080 → BPQ090D → BPQ100D), 0/1.

**Codage des traitements** : à chaque étape des filtres, 1 = oui → étape suivante ;
2 = non → 0 ; « refus » (7), « ne sait pas » (9) ou absence de réponse → **manquant**
(jamais 0). Manquants après codage dans la cohorte de développement (n = 13 883) :
antihypertenseur 0,87 % ; hypolipémiant 3,44 % ; fréquence cardiaque 0 %.

**Forme de la fréquence cardiaque, décidée avant les options** : sur l'ensemble du
développement, modèle cardiovasculaire actuel + fréquence cardiaque linéaire, comparé
au même modèle + spline cubique restreinte à 4 nœuds (comme l'IMC). Test du rapport de
vraisemblance sur les 2 termes non linéaires : spline si p < 0,05, sinon linéaire.
Résidus de martingale tracés à titre descriptif.

**Options** (ajouts au système cardiovasculaire) : (i) fréquence cardiaque ;
(ii) antihypertenseur ; (iii) hypolipémiant ; (iv) (ii) + (iii) ; (v) (i) + (ii) + (iii).

**Procédure** : identique au point 2 (CV « un cycle retiré » sur 1999-2006, mêmes
participants pour toutes les options = cas complets sur le panel actuel et tous les
candidats, pénalisation 0, C de Harrell sur le cycle retiré).

**Décision** (critère corrigé) :
1. Une option passe si a (gain C cardiovasculaire moyen ≥ 0,003), b (gain > 0 sur ≥ 3/4
   plis) et c (gain C global moyen ≥ 0).
2. On part de l'option passante la plus large, par priorité (v) > (iv) > options simples.
3. Dans ce groupe, une variable n'est conservée que si elle passe seule, ou si son apport
   marginal (gain C cardiovasculaire moyen du groupe moins celui du groupe sans elle) est
   ≥ 0,003. Les sous-groupes « groupe sans la variable » sont évalués par la même CV.
4. Si aucun groupe ne passe, on retient les options simples qui passent.

**Sensibilité (non décisionnelle)** : options (ii) à (v) refaites avec le fichier des
médicaments (antihypertenseur par classe Multum, statine par molécule) à la place du
questionnaire. Rapportée, sans effet sur la décision.

### Résultat 3.0 — forme de la fréquence cardiaque (2026-11-09, avant les options)

Développement entier, cas complets sur le panel et les candidats (n = 13 292 ; 2 651 décès).
Modèle cardiovasculaire + FC : linéaire vs spline à 4 nœuds.
LR des termes non linéaires = 8,15 (2 ddl), **p = 0,017** ; AIC partiel 44 768,7 (linéaire)
vs 44 764,6 (spline). Résidus de martingale : plats jusqu'à ~70 bpm puis croissants, avec
une hausse marquée au-delà de 88 bpm (`reports/selection/cardiovasculaire/linearite_fc.*`).

**Décision (règle pré-enregistrée)** : p < 0,05 → **spline à 4 nœuds** pour la FC dans
les options (i) et (v).

### Résultat 3 — système cardiovasculaire (2026-11-09)

Données : 1999-2006 uniquement. Cohorte commune : n = 13 292 (cas complets sur le panel et
les candidats du questionnaire). Manquants : antihypertenseur 0,87 %, hypolipémiant 3,44 %,
FC 0 % — sous le garde-fou de 15 %.

| Option | Gain C cardio. moyen (a ≥ 0,003) | Plis > 0 (b ≥ 3/4) | Gain C global (c ≥ 0) | Passe |
|---|---|---|---|---|
| (i) FC (spline) | +0,0042 | 4/4 | +0,0008 | oui |
| (ii) antihypertenseur | +0,0011 | 3/4 | +0,0002 | non (a) |
| (iii) hypolipémiant | +0,0000 | 1/4 | +0,0000 | non (a, b) |
| (iv) deux traitements | +0,0013 | 4/4 | +0,0002 | non (a) |
| (v) FC + deux traitements | +0,0054 | 4/4 | +0,0010 | oui |

Application du critère corrigé à l'option passante la plus large, (v) :

| Variable | Passe seule | Apport marginal dans (v) (≥ 0,003) | Conservée |
|---|---|---|---|
| FC | oui | +0,0040 | **oui** |
| Antihypertenseur | non | +0,0012 | non |
| Hypolipémiant | non | +0,0001 | non |

**Décision** : système cardiovasculaire = PAS, PAD, CT, HDL, TG **+ fréquence cardiaque
(spline 4 nœuds)**. Les traitements ne sont pas retenus ; ils restent dans le panel comme
variables facultatives (non utilisées par le modèle).

**Sensibilité (fichier des médicaments, non décisionnelle, n = 13 868)** : antihypertenseur
+0,0017 ; statine +0,0000 ; deux traitements +0,0020 ; FC + deux traitements +0,0059.
Même conclusion qu'avec le questionnaire : apport des traitements sous le seuil, statines nulles.
Détail : `reports/selection/cardiovasculaire*/`.

## Point 4 — gel du panel final et engagement avant le passage sur la validation

### Panel final figé (2026-11-09)

- Commit de référence : `d335c349b7992354de7077fd1f3e14eb423f8b67` (dernière modification
  du panel : `c021053a9c81a51070e0714cc18e7ac8d5ebd1c4`).
- `config/panels/checkup_standard.yaml` : blob git `54faf0858045b48c71efc5faa384b59460f9862f` ;
  SHA-256 du fichier (copie de travail) `b01418dae864d6f6b86abf7ab660f1a39a5de77925e9d31884d029dc8c27dc86`
  (reporté dans `reports/checkup_standard/meta.json` à l'exécution).
- `config/study.yaml` : SHA-256 `2202ace1cae086d59c1ce4aef879df00130acf52ae012325e09e346255fb3510`.
- `config/sources/nhanes.yaml` : SHA-256 `98eb5d24ac091f41d562ffb07127ccb1abbcea4888725c3dd20fc1ad4b7a0fe3`.

Variables du modèle, par système (toutes ajustées sur l'âge et le sexe) :

| Système | Variables (transformation) |
|---|---|
| Cardiovasculaire | PAS (spline 4), PAD (spline 4), cholestérol total (spline 4), HDL (log, spline 4), triglycérides (log), **fréquence cardiaque (spline 4)** |
| Métabolique | glycémie (log), HbA1c, IMC (spline 4), tour de taille |
| Rénal | créatinine (log, spline 4), **ACR urinaire (log, plancher 0,1)** |
| Hépatique | ALAT (log, spline 4), ASAT (log), GGT (log), PAL (log), albumine |
| Inflammatoire / hématologique | CRP (log, plancher 0,1), leucocytes (log), lymphocytes %, RDW, VGM, hémoglobine (spline 4), plaquettes (log, spline 4) |

En gras : ajouts du jalon 2. Variables facultatives (collectées, non utilisées) : LDL, urée,
traitement antihypertenseur, traitement hypolipémiant (et, pour NHANES seulement, les
indicateurs du fichier des médicaments). Pénalisation : choisie par CV sur 1999-2006 à
l'exécution (procédure inchangée depuis le jalon 1).

### Engagement (écrit avant le passage)

La cohorte de validation 2007-2010 est consultée **une seule fois** avec ce panel, par une
exécution unique de `python -m aging_clock validate --panel checkup_standard`.
**Aucune modification du panel, des transformations ou du modèle ne suivra d'après ces
résultats.** Toute évolution ultérieure du panel exigera une nouvelle cohorte de
validation (par exemple 2015-2018 ou une cohorte externe) et sera consignée ici.

### Résultat 4 — passage unique sur la validation 2007-2010 (2026-11-09, 17:39-17:48)

Exécution unique au commit `e2a2581`, panel SHA-256 `b01418da…` (identique au gel).
Validation : n = 9 247, 972 décès (jalon 1 : 9 310 / 997 ; l'écart vient des cas complets
sur l'ACR et la FC). Pénalisation retenue par CV : 0.

| Score | C (IC95) | Gain de C vs âge + sexe | HR / ET | Obs./prédit 10 ans | Pente |
|---|---|---|---|---|---|
| Global | 0,853 [0,841 ; 0,864] | +0,046 [0,040 ; 0,053] | 2,01 | 0,92 | 0,99 |
| Cardiovasculaire | 0,819 [0,806 ; 0,831] | +0,012 [0,008 ; 0,015] | 1,41 | 0,93 | 0,97 |
| Métabolique | 0,819 [0,807 ; 0,832] | +0,013 [0,009 ; 0,016] | 1,47 | 0,93 | 0,99 |
| Rénal | 0,820 [0,807 ; 0,833] | +0,013 [0,010 ; 0,017] | 1,39 | 0,97 | 0,99 |
| Hépatique | 0,830 [0,819 ; 0,842] | +0,024 [0,019 ; 0,028] | 1,59 | 0,96 | 1,02 |
| Inflammatoire / hémato. | 0,833 [0,820 ; 0,845] | +0,026 [0,021 ; 0,031] | 1,66 | 0,95 | 0,99 |

Conformément à l'engagement, aucune modification du panel ne découle de ces résultats.
Rapport complet : `reports/checkup_standard/RESULTATS.md`.

## Point 5a — benchmark PhenoAge (protocole écrit avant exécution, 2026-11-09)

Benchmark sur la validation 2007-2010, **sans modifier le panel ni le modèle** (gelés au point 4).

**PhenoAge publié** (Levine et al. 2018, Aging, doi:10.18632/aging.101414, tableau 1 ;
équation complète d'après la correction de Liu et al., PLoS Med 2019,
doi:10.1371/journal.pmed.1002760) :
- xb = −19,907 − 0,0336·albumine(g/L) + 0,0095·créatinine(µmol/L) + 0,1953·glucose(mmol/L)
  + 0,0954·ln(CRP mg/dL) − 0,0120·lymphocytes(%) + 0,0268·VGM(fL) + 0,3306·RDW(%)
  + 0,00188·PAL(U/L) + 0,0554·leucocytes(10⁹/L) + 0,0804·âge ;
- M = 1 − exp(−1,51714·exp(xb)/0,0076927) (risque de décès à 10 ans) ;
- PhenoAge = 141,50 + ln(−0,00553·ln(1 − M))/0,09165.
- Constantes publiées retenues (0,09165 ; 141,50). Le prototype de ce dépôt et le paquet R
  BioAge utilisaient 0,090165 et 141,50225. *Phrase précisée le 2026-11-09 après vérification* :
  passer d'un jeu à l'autre est une transformation affine de PhenoAge (pente 0,09165/0,090165).
  Seules les valeurs exprimées en années en dépendent (PhenoAge, accélération en années, son
  écart-type) ; le C, le HR par écart-type d'accélération et la calibration (calculée sur M,
  avant conversion) n'en dépendent pas. Vérifié sur le développement : HR identiques à 10⁻⁶.
- CRP : valeur NHANES convertie en mg/dL, sans plancher (comme la publication).
- Accélération = résidu de la régression linéaire PhenoAge ~ âge, **estimée sur le
  développement** puis appliquée à la validation.
- Limite connue : glycémie non à jeun dans notre cohorte (PhenoAge a été construit et
  validé sur des sujets majoritairement à jeun).

**PhenoAge réentraîné** : même méthode que le score principal (Cox âge + sexe, transformations
du panel principal pour ces 9 marqueurs, pénalisation par CV sur 1999-2006), sur les 9
marqueurs de PhenoAge seulement (panel `phenoage9`). Sépare l'effet de la méthode de l'effet
du nombre de variables.

**Comparaisons** : mêmes participants que la validation principale (n = 9 247) ; C (IC 95 %),
gain de C vs Cox âge + sexe, HR par écart-type d'accélération (ajusté âge + sexe), calibration
à 10 ans (M pour PhenoAge publié ; risque à 10 ans pour les versions réentraînées) ; différence
de C score global − chaque PhenoAge par bootstrap apparié (1000 tirages, mêmes indices) ; mêmes
analyses chez les personnes sans antécédent déclaré.

### Résultat 5a — benchmark PhenoAge (2026-11-09)

Validation (n = 9 247, 972 décès), différences de C par bootstrap apparié (1000 tirages) :
- score global − PhenoAge publié : +0,0215 [+0,0166 ; +0,0267] ;
- score global − PhenoAge réentraîné (9 marqueurs) : +0,0163 [+0,0126 ; +0,0202] ;
- PhenoAge réentraîné − PhenoAge publié (effet de la méthode) : +0,0052 [+0,0017 ; +0,0085].
Sans antécédent déclaré (n = 7 123) : +0,0221, +0,0153, +0,0068, mêmes conclusions.
PhenoAge publié : sous-estime le risque (obs./prédit 1,21) et pente 0,71 (prédictions trop
dispersées). Aucune modification du panel ni du modèle. Rapport :
`reports/checkup_standard/benchmark_phenoage/BENCHMARK.md`.

### Précision 5a — sources des constantes de PhenoAge (2026-11-09)

- **Levine et al. 2018**, Aging 10(4):573-591, doi:10.18632/aging.101414 : tableau 1 = poids des
  9 marqueurs et de l'âge (PAL arrondie à 0,0019). L'équation de conversion en années renvoie au
  supplément 1 (PDF), **non lu** (non accessible lors de la vérification) : constantes non vérifiées
  dans cette source.
- **Liu et al., correction**, PLoS Med 2019;16(2):e1002760, doi:10.1371/journal.pmed.1002760
  (PMC6388911) : équation complète, xb (intercept −19,907, PAL 0,00188, glucose 0,1953, RDW 0,3306),
  M = 1 − exp(−1,51714·exp(xb)/0,0076927), PhenoAge = 141,50 + ln(−0,00553·ln(1 − M))/0,09165.
  La version originale (PLoS Med 2018, doi:10.1371/journal.pmed.1002718) contenait des erreurs
  (glucose 0,0195, RDW 0,3356, étape M absente). **Source retenue.**
- **Paquet R BioAge** (Kwon et Belsky), `R/phenoage_calc.R`, branche `orig = TRUE` : coefficients
  non arrondis, 141,50225, −0,0055305 et 0,090165 ; aucune référence citée dans le fichier.
  Origine probable de la paire du prototype, non retenue.

## Point 5b — audit d'équité (protocole écrit avant exécution, 2026-11-09)

Validation 2007-2010, modèle gelé, score global (écarts par système en annexe descriptive).
Analyses non pondérées.

**Sous-groupes** (fixés a priori) :
- sexe ;
- groupe ethnique NHANES (`RIDRETH1`) : mexicain-américain, autre hispanique, blanc non
  hispanique, noir non hispanique, autre / multiethnique ;
- âge : 20-39, 40-59, 60-79 ans ;
- ratio revenu / seuil de pauvreté (`INDFMPIR`), seuils usuels NHANES : < 1,3 ; 1,3-3,5 ; ≥ 3,5 ;
- niveau d'études (`DMDEDUC2`) : < fin du secondaire (codes 1-2) ; diplôme du secondaire (3) ;
  études supérieures partielles (4) ; diplôme universitaire (5). Refus / ne sait pas = manquant.

**Par sous-groupe** : n, décès ; C (IC 95 %, bootstrap 1000) et gain de C vs Cox âge + sexe dans
le groupe ; rapport observé / prédit à 10 ans (IC 95 % du Kaplan-Meier) ; pente de calibration
(IC 95 %) ; écart d'âge : moyenne (IC 95 %), écart-type, médiane, intervalle interquartile.

**Règle d'interprétation** (fixée avant exécution) :
- *Défaut de calibration* : IC du rapport O/P excluant 1 **et** |O/P − 1| > 0,20 ; ou IC de la
  pente excluant 1 **et** pente hors [0,80 ; 1,20].
- *Défaut de discrimination* : IC du gain de C (vs âge + sexe dans le groupe) incluant 0.
- *Différence de santé réelle* : écart d'âge moyen du groupe différent de celui de la
  population de validation (IC excluant la moyenne globale) **sans** défaut de calibration ni de
  discrimination dans ce groupe.
- *Effectif insuffisant* : < 50 décès dans le groupe → résultats rapportés, pas de conclusion.
- Les C entre tranches d'âge ne sont pas comparés entre eux (un intervalle d'âge étroit réduit
  mécaniquement le C) ; seul le gain de C vs âge + sexe dans le groupe est interprété.

### Résultat 5b — audit d'équité (2026-11-09)

Verdicts de la règle pré-enregistrée (validation, n = 9 247) :
- **Défaut de calibration** : revenu ≥ 3,5 (O/P 0,62 [0,53 ; 0,73]) ; diplôme universitaire (0,69
  [0,58 ; 0,84]) ; mexicains-américains (0,65 [0,53 ; 0,80]) ; 40-59 ans (pente 1,21 [1,07 ; 1,34]).
  Aucun défaut de discrimination (gain de C > 0 dans tous les groupes à ≥ 50 décès).
- **Différence de risque réelle, bien calibrée** : revenu < 1,3 (écart +0,7 an), noirs non
  hispaniques, niveau d'études < secondaire et diplôme du secondaire, sexe, autres hispaniques,
  60-79 ans.
- **Effectif insuffisant** : 20-39 ans (41 décès), autre / multiethnique (30 décès).
Aucune modification du modèle (gelé). Interprétation : `reports/checkup_standard/equite/INTERPRETATION.md`.

## Point 6 — validation secondaire 2015-2018 (protocole écrit avant exécution, 2026-11-09)

Modèle gelé (point 4). Analyse descriptive de transposition : **aucune décision sur le modèle**.
Seule information de survie vue auparavant sur ces cycles : la proportion brute de décès
(jalon 1, 3,3 % et 1,7 %).

**Chaînage de mortalité** : le fichier public le plus récent reste celui de 2019 (suivi jusqu'au
31/12/2019) ; la mise à jour 2022 n'existe qu'en accès restreint (CDC, page « Public-use linked
mortality files », consultée le 2026-11-09). Suivi : environ 4 ans (2015-2016) et 2 ans (2017-2018).

**Médianes des marqueurs, adultes 20-79 ans** (sans la mortalité) — RDW : 12,6 (2007-08),
12,6 (2009-10), 12,7 (2011-12), **13,4 (2013-14)**, 13,5 (2015-16), 13,5 (2017-18). ALAT/ASAT/PAL/
albumine stables jusqu'en 2015-16, sauts en 2017-18 (ALAT 21 → 18, ASAT 23 → 19, PAL 66 → 75,
albumine 43 → 41 g/L).

**Harmonisation (version « harmonisée »)** — documentation NHANES d'abord, recalage sinon :
1. *RDW* (2015-16 et 2017-18) : changement d'automate en 2013-14 (Beckman DxH 800, `CBC_H`) ;
   NHANES précise qu'aucune étude de comparaison n'a pu être faite. → **Recalage par quantiles**
   sur le dernier cycle avant le changement, **2011-2012**, par strates sexe × âge (20-39, 40-59,
   60-79), à partir de tous les adultes de chaque cycle (marqueurs seulement, jamais la mortalité).
   Les autres paramètres de la numération ne sont pas recalés (pas de changement documenté,
   médianes dans la variation habituelle entre cycles).
2. *Biochimie 2017-18* (`BIOPRO_J`, passage du Beckman DxC 660i au Roche Cobas 6000) : équations
   « backward » de l'étude de pontage NHANES (Cobas → DxC 660i), appliquées en unités NHANES avant
   conversion : ALAT X = 1,013·Y + 2,688 ; ASAT X = 1,018·Y + 3,762 ; log10 PAL = 1,001·log10 Y − 0,04294 ;
   albumine (g/dL) X = 1,044·Y + 0,01128 ; créatinine (mg/dL) X = 1,051·Y − 0,06945 ;
   GGT X = 0,8042·Y + 2,363 ; triglycérides (mg/dL) X = 0,9655·Y − 7,020. Glucose : « ajustement non
   recommandé » par NHANES → non modifié. Cholestérol total, HDL, HbA1c, ACR : pas de changement
   documenté → non modifiés. Référence de fait : 2015-16 (DxC 660i), dernier cycle avant le changement.
3. *hs-CRP 2017-18* (`HSCRP_J`, Cobas, valeurs 19,6 % plus basses) : équation backward NHANES
   Y(DxC 660i) = 1,150·X(Cobas) − 0,3397, pour X ≤ 20 mg/L (au-delà : non recommandé, non modifié).
4. *CRP standard (≤ 2010) vs hs-CRP (2015-16)* : aucune documentation NHANES sur leur concordance.
   Vérification descriptive : quantiles (25, 50, 75, 90 %) au-dessus du plancher de 0,1 mg/L par
   strates sexe × âge, 2009-10 vs 2015-16 ; la tendance 2005-06 → 2009-10 sert de repère de variation
   « naturelle ». **Non vérifiable formellement** (pas d'échantillon commun ; 2011-2014 sans CRP) :
   ce sera dit dans le rapport. Pas de correction de la CRP 2015-16.

**Versions rapportées côte à côte** : brute (valeurs telles quelles) et harmonisée.

**Analyses** (par cycle et sur les deux cycles) : n, décès ; C (IC 95 %, bootstrap 1000) sur tout le
suivi ; gain de C vs âge + sexe ; HR par écart-type de l'écart d'âge (ajusté âge + sexe) ;
calibration à **3 ans** (risque prédit par le même modèle gelé avec la survie de base du
développement à 36 mois ; rapport observé/prédit, pente) ; écart d'âge moyen global et par système.
Attendu : en version harmonisée, écart moyen proche de la validation 2007-2010 (−1,4 an).

**Note pour le point 4** : le recalage par quantiles par strates d'âge et de sexe est une méthode
candidate pour la transposition à une autre cohorte (alignement de distributions de marqueurs
sans données de survie).

### Bug de traitement des données corrigé — point 6 (2026-11-09, après une première exécution)

Bug de traitement des données, pas une décision de modélisation. Le rapport ne présente que
l'exécution corrigée ; la première exécution n'est consignée qu'ici (version harmonisée 2017-18 :
n = 3 991, C 0,819, observé/prédit à 3 ans 0,78, écart moyen −1,16 an).


Première exécution : en version harmonisée 2017-18, 82 participants avaient une hs-CRP < 0,30 mg/L
pour laquelle l'équation NHANES (1,150·X − 0,3397) donne une **concentration négative**, rejetée
comme hors plage : ils sortaient de la cohorte (n = 3 991 au lieu de 4 064 ; décès inchangés, 44).
Correction : résultat de l'équation borné au plancher du panel (0,1 mg/L). Neutre pour le modèle
(toute CRP ≤ 0,1 est déjà ramenée à 0,1) ; rétablit la même population que la version brute.
Le protocole n'est pas modifié ; les deux exécutions sont conservées dans le rapport.

### Résultat 6 — validation secondaire 2015-2018 (2026-11-09)

n = 8 404 (harmonisée), 162 décès (44 en 2017-18), suivi médian 37 mois. Version harmonisée
(brute entre parenthèses) : C 0,850 (0,848) ; gain de C +0,051 (+0,050) ; HR/ET 2,22 (2,21) ;
observé/prédit à 3 ans 0,86 [0,72 ; 1,02] (0,68) ; écart moyen −1,08 an (+1,86).
Les dosages déplacent fortement l'âge biologique et la calibration, pas le classement.
CRP standard vs hs-CRP : concordance non vérifiable formellement ; quantiles par strate
compatibles. Aucune modification du modèle. Rapport : `reports/checkup_standard/secondaire/SECONDAIRE.md`.

## Point 7 — modèle figé exportable (2026-11-09)

`models/checkup_standard_v1.json` : modèle gelé du point 4 (mêmes coefficients), transformations
apprises, survie de base à 12/24/36/60/120 mois, méthodes de dosage de référence (pages NHANES des
cycles 1999-2006) et avertissements. Module `aging_clock.score` (NumPy + pandas). Test de
reproductibilité : le calcul depuis le JSON reproduit le pipeline sur la validation 2007-2010
(écart < 10⁻⁸ an sur tous les âges biologiques). Aucune modification du modèle.

## Piste de recherche — précision individuelle de l'âge biologique (protocole écrit avant exécution, 2026-11-09)

**Questions.** (1) Marge d'erreur de l'âge biologique d'une personne due à la variabilité
biologique intra-individuelle et à l'erreur analytique ; (2) écart minimal entre deux mesures
successives traduisant un vrai changement.

**Cadre.** Analyse descriptive : le modèle reste figé, aucune modification n'en découle. Calculs
avec le modèle exporté `models/checkup_standard_v1.json` et le module autonome (`aging_clock.score`,
NumPy + pandas), pas le pipeline d'entraînement. Population : validation 2007-2010 (n = 9 247).

**Variabilité.** Fichier `config/variability.yaml` (syntaxe JSON, valide en YAML ; **hors dépôt
public** à cause de la licence de la base EFLM ; gabarit public `config/variability.example.yaml`).
SHA-256 du fichier utilisé : `15483e3fb89eb1aa06640f5cf47a3b9fc184330d94df4d8773f34c0b40bfce83`.
- Valeur centrale : Lacher et al., NCHS 2010 (NHANES 1999-2002, mêmes laboratoires que le
  développement, prélèvements non à jeun, ~19 jours, domaine public) pour albumine, créatinine,
  glucose, TG, cholestérol total, PAL, ALAT, ASAT, GGT (CV_A = imprécision NHANES publiée).
- Base EFLM (méta-analyses, IC 95 %) pour HDL, CRP, HbA1c (NGSP), leucocytes, VGM, hémoglobine,
  plaquettes ; approximations signalées : lymphocytes % (CV du **nombre**), RDW % (CV du **RDW-SD**) ;
  CV_A = 0,5 × CV_I (spécification souhaitable).
- Valeurs de travail signalées : ACR 40 % [25 ; 60] (aucune étude éligible à la méta-analyse EFLM) ;
  fréquence cardiaque 8 % [5 ; 11] ; IMC 1,5 % [1 ; 3] ; tour de taille 2 % [1 ; 3] (non sourcées).
- Tension : CV entre visites au cabinet 8,6 % (Br J Gen Pract 2010) ; borne basse = CV intra-visite
  mesuré dans NHANES 1999-2006 (développement) pour la moyenne de 3 mesures : PAS 2,0 %, PAD 3,9 %
  (ET intra-visite d'une mesure : PAS 4,5 mmHg, PAD 4,2 mmHg).
- Jeûne : la valeur centrale (Lacher, non à jeun) inclut la variabilité liée au repas, cohérente
  avec un modèle entraîné sur des valeurs non à jeun. Scénario « toujours à jeun » : CV_I EFLM à
  jeun (glucose 4,9 %, TG 19,8 %). Le décalage moyen à jeun / non à jeun (TG jusqu'à +0,3 mmol/L,
  Langsted et al. 2008) est un biais, non simulé, documenté.

**Méthode.**
1. Monte-Carlo, graine 2026 : pour chaque personne, 1 000 jeux de biomarqueurs « remesurés » ;
   bruit multiplicatif log-normal de médiane 1, σ = racine(ln(1 + CV_total²)),
   CV_total = racine(CV_I² + CV_A²) ; tirages indépendants entre marqueurs. **Hypothèse :** on
   simule autour de la valeur observée, qui contient déjà du bruit ; la dispersion obtenue est celle
   d'une remesure, pas l'écart à une « vraie » valeur. Âge et sexe non bruités. Les valeurs tirées
   passent par les mêmes transformations que le modèle (plancher, log, bornes) ; pas de contrôle de
   plage (fréquence des bornages rapportée).
2. Par personne : écart-type et intervalle à 95 % (percentiles 2,5-97,5) de l'âge biologique global
   et de chaque âge par système ; distributions rapportées (médiane, IQR, 90e centile).
3. Valeur de changement significatif : tirages appariés en 500 paires de remesures indépendantes ;
   seuil = 95e centile de |âge bio 1 − âge bio 2| par personne ; médiane et IQR sur les personnes,
   global et par système ; comparaison avec 1,96 × racine(2) × écart-type.
4. Fiabilité : CCI ≈ 1 − (variance moyenne due au bruit) / (variance observée de l'écart entre
   personnes) ; approximation (la variance observée contient déjà du bruit).
5. Stabilité du classement : proportion de paires de remesures où le signe de l'écart change
   (plus jeune / plus vieux), globalement et par tranches d'écart observé (|écart| < 1, 1-3, 3-5, ≥ 5 ans).
6. Contribution de chaque marqueur : simulation en ne bruitant qu'un marqueur à la fois
   (200 tirages, mêmes personnes) ; part = variance due au marqueur / somme des variances.
7. Scénarios : (a) moyenne de deux prises de sang (CV des marqueurs sanguins et urinaires / racine(2) ;
   mesures physiques inchangées) ; (b) prise de sang toujours à jeun ; (c) (a) + (b).
8. Sensibilité : tout aux bornes basses, puis tout aux bornes hautes (CV_A inchangés).

**Livrables.** `reports/checkup_standard/incertitude/INCERTITUDE.md` ; option
`python -m aging_clock score --input fichier.csv --uncertainty` (intervalle à 95 % par personne,
NumPy + pandas) ; tests : reproductibilité à graine fixe, bruit nul → intervalle nul.

### Résultat — précision individuelle (2026-11-09)

Validation 2007-2010, n = 9 247, 1 000 remesures par personne, CV de `config/variability.yaml`
(SHA-256 `15483e3f…`). Score global : IC 95 % individuel de largeur médiane 10,6 ans (ET 2,7 ans) ;
changement significatif entre deux mesures 7,5 ans [6,9 ; 7,9] ; CCI 0,87 ; 15,7 % de bascules
plus jeune / plus vieux (47 % quand |écart| < 1 an, 1,5 % quand ≥ 5 ans). Principal contributeur :
ALAT (36 % de la variance du global). Moyenne de deux prises de sang : 8,4 ans ; à jeun : sans effet ;
sensibilité 6,8 (bornes basses) – 13,1 ans (bornes hautes). Aucune modification du modèle.
Rapport : `reports/checkup_standard/incertitude/INCERTITUDE.md`.

## Correction — constantes de conversion de PhenoAge (2026-11-10)

- **Source d'origine lue** : supplément 1 de Levine et al. 2018 (Aging, doi:10.18632/aging.101414,
  PMC5940111, fichier `aging-10-101414-s001.pdf`) : PhenoAge = 141,50225 + ln(−0,00553·ln(1 − M))/0,090165 ;
  tableau S1 identique à nos poids (constante −19,9067, RDW 0,3306, ln CRP 0,0954, γ = 0,0076927).
- La correction de Liu et al. 2019 (retenue au point 5a) imprime 141,50 et 0,09165. C'est
  probablement une faute de frappe (un « 0 » manquant). C'est notre interprétation, pas un
  erratum des auteurs.
- **Décision** (validée par l'auteur du projet) : adopter 141,50225 et 0,090165 (`phenoage.py`),
  relancer le benchmark 5a.
- **Effet constaté** : transformation affine, comme prévu. C, gain de C, HR par écart-type,
  calibration et différences de C appariées inchangés. Seules les valeurs en années changent :
  PhenoAge publié moyen en validation 44,0 → 42,4 ans ; écart-type de l'accélération
  7,54 → 7,66 ans. La première exécution (0,09165) n'est plus rapportée que dans ce paragraphe.

## Fiabilité test-retest réelle — NHANES 2001-2002 (pré-enregistrement, 2026-11-10)

Écrit et commité **avant** toute lecture des valeurs des marqueurs du second examen.
Code : `src/aging_clock/retest.py` (`python -m aging_clock fiabilite predictions | analyse`).

**Ce qui a déjà été vu des fichiers du second examen** (pendant la revue de littérature) :
effectifs par fichier (544 à 557 personnes) et distribution du délai `LB2DAY` (3 à 47 jours,
moyenne 18,9, médiane 17). Aucune valeur de marqueur. Pour calculer les prédictions, seule la
colonne `SEQN` des six fichiers est conservée (`second_exam_seqn`).

**Population.** Cohorte de développement (mêmes critères qu'ailleurs : 20-79 ans, éligibles au
chaînage, suivi > 0, hors grossesse, cas complets sur le panel au premier examen), cycle 2001-2002,
`SEQN` présent dans les six fichiers du second examen (L40_2_B, L25_2_B, L11_2_B, L10_2_B, L13_2_B,
L16_2_B) : **n = 389** (44,2 ans en moyenne, 46 % de femmes). À l'analyse, on exclut en plus les
personnes dont une valeur sanguine ou urinaire du second examen est manquante ou hors des plages
plausibles du panel. Les prédictions sont alors recalculées sur cette population finale, avec le même
code, les mêmes CV et la même graine ; les deux jeux de prédictions sont rapportés.
**Ces personnes font partie de la cohorte de développement** : leur premier examen a servi à
ajuster le modèle, le second jamais. La fiabilité dépend surtout du bruit de mesure, donc le biais
attendu est faible ; NHANES III (indépendant) servira de confirmation après validation.

**Correspondance des variables du second examen** (mêmes unités et facteurs que le premier examen
2001) : cholestérol `LB2TC`, HDL `LB2HDL`, TG sériques `LB2STR`, glucose sérique `LB2SGL`, HbA1c
`LB2GH`, créatinine `LB2SCR` (« pas de correction nécessaire en 2001-2002 », documentation L40_2_B),
ALAT `LB2SATSI`, ASAT `LB2SASSI`, GGT `LB2SGTSI`, PAL `LB2SAPSI`, albumine `LB2SAL`, CRP `LB2CRP`,
leucocytes `LB2WBCSI`, lymphocytes % `LB2LYPCT`, RDW `LB2RDW`, VGM `LB2MCVSI`, hémoglobine `LB2HGB`,
plaquettes `LB2PLTSI`, ACR = `UR2UMA`/`UR2UCR` × 11,31.

**Deux comparaisons.**
1. **Principale : « fiabilité de la partie biologique du score »**. Seuls les marqueurs sanguins et
   urinaires changent entre les deux examens. Tension, pouls, IMC et tour de taille gardent leur
   valeur du premier examen, dans l'observé comme dans la simulation. **Le système
   cardiovasculaire n'y est pas interprété** (tension et pouls fixes).
2. **Secondaire : score complet**. Observé = second examen sanguin + bruit simulé sur la tension,
   le pouls, l'IMC et le tour de taille (200 tirages, métriques moyennées) ; prédit = simulation de
   tout le panel. Seule comparaison où le système cardiovasculaire est interprété.

**Scores** : âge global, 5 âges par système (modèle gelé `checkup_standard_v1.json`), PhenoAge
publié (constantes du supplément de Levine 2018 ; accélération = résidu sur l'âge, régression du
développement), PhenoAge réentraîné (9 marqueurs, notre méthode, pénalisation 0,003 du benchmark 5a).
Tous les scores sont analysés comme des écarts à l'âge (années). L'âge ne change pas entre les deux
examens.

**CV de la simulation principale** (`config/variability_retest.json`, hors dépôt public,
SHA-256 `b7674478…`). CV_I : EFLM pour tous les marqueurs sanguins (PAL : Carobene 2017,
EuBIVAS), **aucune valeur issue des remesures NHANES**. CV_A : précision de méthode documentée
par le laboratoire NHANES ; sinon le fabricant ; sinon 0,5 × CV_I.

| Marqueur | CV_I | CV_A | Source CV_A | Remarque |
|---|---|---|---|---|
| Albumine | 2,5 | 1,3 | NHSR 21, colonne CV_a (précision de méthode, contrôles qualité) | |
| Créatinine | 4,4 | 4,6 | idem | |
| Glucose | 4,9 | 1,5 | idem | CV_I à jeun appliqué à tous |
| Triglycérides | 19,8 | 1,9 | idem | CV_I à jeun appliqué à tous |
| Cholestérol total | 5,4 | 1,5 | idem | |
| PAL | 5,3 | 2,1 | idem | |
| ALAT | 12,4 | 4,0 | idem | |
| ASAT | 8,4 | 3,1 | idem | |
| GGT | 8,2 | 3,0 | idem | |
| HDL | 5,7 | 3,2 | fiche NHANES 2001-02 (lipides) : méthode héparine-Mn (majorité des participants), pool à 49,8 mg/dL | |
| CRP | 34,7 | 5,7 | fabricant, N Latex CRP mono (FDA 510(k) K962523) : CV inter-séries 2,6-5,7 % entre 10 et 60 mg/L, borne haute | non documenté aux faibles concentrations |
| HbA1c | 1,2 | 2,5 | fiche NHANES 2001-02 : pool à 5,1 %, CV 2,54 % | |
| Leucocytes | 11,1 | 2,1 | NHSR 54, colonne CV_a (contrôles de paillasse ou fabricant) | |
| Lymphocytes % | 10,9 | 2,9 | idem | CV_I du nombre (aucune valeur trouvée pour le %) |
| RDW | 1,7 | 1,2 | idem | CV_I du RDW-SD (aucune valeur trouvée pour le %) |
| VGM | 0,8 | 0,7 | idem | |
| Hémoglobine | 2,7 | 1,1 | idem | |
| Plaquettes | 7,2 | 3,1 | idem | |
| ACR | 40 | inclus | — | valeur de travail |
| PAS, PAD, pouls, IMC, tour de taille | 8,6 ; 8,6 ; 8,0 ; 1,5 ; 2,0 | — | — | comparaison secondaire seulement |

Vérification : les CV_a de Lacher (NHSR 21 et 54) sont la précision de la méthode de laboratoire
(« laboratory method precision », contrôles qualité ou fabricant). Ils ne sont pas calculés sur les
participants reprélevés. Recherches sans résultat : CV_I du pourcentage de lymphocytes et du RDW en %
(Coskun et al. 2018, CCLM, texte complet : seulement le nombre de lymphocytes et le RDW-SD) ;
précision de la CRP dans la fiche NHANES (aucun chiffre).

**Configuration précédente (Lacher pour la biochimie) : partiellement circulaire pour ce test.**
Elle utilisait les CV_w de Lacher 2010, calculés sur les remesures NHANES 1999-2002, donc en
partie sur les personnes testées ici. Les résultats déjà publiés de la précision individuelle
(±5 ans, changement significatif de 7,5 ans) en dépendent. Ils restent dans le rapport comme
**scénario secondaire**.
- **Scénario secondaire** : CV_I de Lacher 2010 (biochimie) et Lacher 2012 (hématologie, moyenne
  hommes/femmes ; hémoglobine femmes 3,15 %, recalculé depuis le CV total et le CV_a publiés).
  CV_A et autres marqueurs comme le principal.
- **Sensibilités** : lymphocytes % × 0,5 ; RDW × 0,5 ; CRP avec CV_A = 0,5 × CV_I ; ACR à 25 % et à 55 %.

**Métriques** (par score). Observé : d = écart₂ − écart₁.
- CCI(A,1), accord absolu, modèle à deux facteurs (McGraw et Wong 1996), sur les écarts à l'âge ;
- Bland-Altman : biais moyen de d et limites d'accord biais ± 1,96 × ET(d) ;
- écart-type intra-individuel ET_w = ET(d)/racine(2) ; valeur de changement significatif
  empirique = 1,96 × racine(2) × ET_w ;
- taux de bascule : proportion de personnes dont le signe de l'écart change entre les deux examens ;
- CV intra-individuels observés par marqueur : ET(ln x₂ − ln x₁)/racine(2), converti en CV
  (inclut CV_I et CV_A) ; comparés à racine(CV_I² + CV_A²) ;
- IC 95 % par bootstrap des personnes (2 000 tirages, graine 2026).
Prédit (simulation, 1 000 remesures par personne, graine 2026, mêmes définitions que la précision
individuelle) : ET_w = racine(moyenne des variances simulées) ; changement significatif =
1,96 × racine(2) × ET_w ; CCI = 1 − ET_w²/variance observée des écarts ; bascule entre paires de
remesures simulées. Note : le changement significatif publié précédemment (7,5 ans) était le 95ᵉ
centile par personne. Ici, c'est la formule 1,96 × racine(2) × ET_w, des deux côtés.

**Règle de lecture** (fixée maintenant). Pour chaque score, rapport R = ET_w observé / ET_w prédit
(principal), avec son IC 95 % bootstrap (prédiction tenue fixe) :
- IC contenant 1 → **simulation compatible** ;
- borne basse > 1 → **la simulation sous-estime le bruit** (variabilité non modélisée : délai,
  jeûne, séance, saison) ;
- borne haute < 1 → **la simulation surestime le bruit** (CV trop élevés).
Le scénario secondaire et les sensibilités sont rapportés à titre descriptif, sans règle de décision.

**Facteurs contrôlés** (descriptifs, pas de test d'hypothèse) :
- délai : corrélation de Spearman entre |d| et `LB2DAY` ; métriques par tertile de délai ;
- séance et jeûne : les fichiers publics du second examen **ne contiennent ni la séance ni la durée
  de jeûne**. Indicateur indirect, déclaré comme tel : « à jeun aux deux prélèvements » = premier
  examen le matin (`PHDSESN` = 0) et jeûne ≥ 8 h (`PHAFSTHR`, fichier PH_B), **et** glycémie
  plasmatique présente au second examen (`LB2GLU`). Au premier examen, elle n'est mesurée que chez
  les examinés du matin à jeun ; l'application de cette règle au second examen est notre déduction.
  Métriques rapportées dans ce sous-groupe et selon la séance du premier examen. Sous-groupe
  rapporté seulement s'il compte au moins 20 personnes.

**Prédictions figées** (n = 389, population avant exclusions du second examen ;
`reports/checkup_standard/fiabilite_reelle/predictions.csv`).

| Score | ET_w | Changement significatif | Limites d'accord | CCI | Bascule |
|---|---|---|---|---|---|
| **Partie biologique, principal** | | | | | |
| Global | 1,78 | 4,93 | ± 4,93 | 0,930 | 10,8 % |
| Cardiovasculaire (non interprété) | 0,60 | 1,67 | ± 1,67 | 0,972 | 7,0 % |
| Métabolique | 0,26 | 0,72 | ± 0,72 | 0,995 | 2,6 % |
| Rénal | 1,17 | 3,23 | ± 3,23 | 0,901 | 15,5 % |
| Hépatique | 1,69 | 4,69 | ± 4,69 | 0,833 | 17,9 % |
| Inflammatoire et hématologique | 1,46 | 4,05 | ± 4,05 | 0,916 | 12,5 % |
| PhenoAge publié | 1,60 | 4,43 | ± 4,43 | 0,941 | 11,0 % |
| PhenoAge réentraîné | 1,41 | 3,91 | ± 3,91 | 0,930 | 11,3 % |
| **Score complet, principal** | | | | | |
| Global | 2,20 | 6,09 | ± 6,09 | 0,894 | 13,4 % |
| Cardiovasculaire | 1,90 | 5,25 | ± 5,25 | 0,721 | 22,3 % |
| Métabolique | 0,87 | 2,42 | ± 2,42 | 0,943 | 8,4 % |
| **Partie biologique, scénario secondaire (Lacher)** | | | | | |
| Global | 2,28 | 6,32 | ± 6,32 | 0,886 | 13,4 % |
| Hépatique | 2,59 | 7,18 | ± 7,18 | 0,610 | 25,3 % |
| PhenoAge publié | 1,83 | 5,08 | ± 5,08 | 0,923 | 12,7 % |

Sensibilités, ET_w du global (partie biologique) : lymphocytes % × 0,5 : 1,77 ; RDW × 0,5 :
1,70 ; CRP CV_A = 0,5 × CV_I : 1,78 ; ACR 25 % : 1,71 (rénal 0,80) ; ACR 55 % : 1,87 (rénal 1,51).
Biais prédit : 0 partout. CV totaux prédits par marqueur : racine(CV_I² + CV_A²) du tableau
ci-dessus.

Empreintes : CV `b76744785b175e4f…`, code de `retest.py` à la génération des prédictions
`644bf578655ee10a…` (fichier `meta_predictions.json`). L'analyse refuse de tourner si le fichier
des CV a changé.

### Résultat — fiabilité test-retest réelle NHANES 2001-2002 (2026-11-10)

Exécution du protocole pré-enregistré (commit `1795991`). Fichier des CV inchangé (empreinte
vérifiée par le code). Population finale : **n = 387** (2 exclues : valeur du second examen
manquante ou hors plage). Délai médian 17 jours (6-47).

**Écarts au protocole.**
1. *Erreur de codage corrigée* : le lecteur SAS xport de pandas rend les 0 sous la forme
   5,4 × 10⁻⁷⁹. La séance du matin (`PHDSESN` = 0) n'était donc jamais reconnue : la première
   exécution classait les 387 personnes « après-midi ou soir » et le sous-groupe « à jeun aux
   deux » était vide. Arrondi ajouté dans `first_exam_session`. Effet limité aux sous-groupes de
   séance et de jeûne ; les comparaisons principales sont identiques.
2. *Défaut de conception de la comparaison secondaire* (score complet) : le bruit physique simulé
   était ajouté au second examen seulement, alors que deux mesures réelles en portent chacune un.
   Sa contribution était donc comptée pour moitié. La version pré-enregistrée est conservée
   (`comparaison_complete.csv`). Une version corrigée, **non pré-enregistrée**, ajoute un bruit
   indépendant aux deux examens (`comparaison_complete_corrigee_non_preenregistree.csv`). Elle est
   seule interprétée.
3. *Défaut du pipeline principal découvert à cette occasion, non corrigé* : la même lecture des
   0 empêche la règle « diastolique = 0 → manquant ». Pour 37 personnes de la cohorte (16 en
   développement, 21 en validation, aucune dans la population de fiabilité), une lecture à 0
   entre dans la moyenne, ce qui sous-estime la diastolique d'environ 19 mmHg (médiane).
   Correction en attente d'une décision : elle modifie le modèle gelé.

**Partie biologique du score, simulation principale (EFLM).** R = ET_w observé / ET_w prédit
(IC 95 %) :

| Score | ET_w obs. | ET_w prédit | R [IC 95 %] | Lecture | Chgt signif. obs. / prédit | CCI obs. [IC] / prédit | Biais moyen (ans) [IC] | Bascule obs. / prédit |
|---|---|---|---|---|---|---|---|---|
| Global | 1,87 | 1,78 | 1,05 [0,96 ; 1,14] | compatible | 5,2 / 4,9 | 0,92 [0,90 ; 0,94] / 0,93 | +0,32 [+0,05 ; +0,58] | 13,7 % / 10,8 % |
| Métabolique | 0,31 | 0,26 | 1,20 [1,03 ; 1,38] | bruit sous-estimé | 0,9 / 0,7 | 0,993 / 0,995 | +0,01 | 2,8 % / 2,6 % |
| Rénal | 1,56 | 1,16 | 1,34 [1,19 ; 1,49] | bruit sous-estimé | 4,3 / 3,2 | 0,82 [0,73 ; 0,87] / 0,90 | −0,23 [−0,44 ; 0,00] | 21,4 % / 15,6 % |
| Hépatique | 1,76 | 1,69 | 1,04 [0,93 ; 1,17] | compatible | 4,9 / 4,7 | 0,82 [0,77 ; 0,86] / 0,83 | +0,55 [+0,30 ; +0,80] | 20,2 % / 17,8 % |
| Inflammatoire et hématologique | 1,67 | 1,46 | 1,15 [1,03 ; 1,27] | bruit sous-estimé | 4,6 / 4,0 | 0,89 [0,85 ; 0,91] / 0,92 | +0,22 | 14,5 % / 12,6 % |
| PhenoAge publié | 2,04 | 1,60 | 1,28 [1,13 ; 1,44] | bruit sous-estimé | 5,7 / 4,4 | 0,91 [0,87 ; 0,93] / 0,94 | +0,43 [+0,15 ; +0,70] | 12,1 % / 10,8 % |
| PhenoAge réentraîné | 1,51 | 1,41 | 1,07 [0,97 ; 1,17] | compatible | 4,2 / 3,9 | 0,92 [0,89 ; 0,94] / 0,93 | +0,40 [+0,19 ; +0,62] | 12,1 % / 11,0 % |

Cardiovasculaire (non interprété dans cette comparaison) : R = 1,24.
Scénario secondaire (Lacher), descriptif : global R = 0,82 [0,75 ; 0,89], hépatique 0,68 (bruit
surestimé), rénal 1,29, PhenoAge publié 1,12.

**Score complet, version corrigée (non pré-enregistrée)** : global ET_w 2,27 contre 2,20 prédit
(R = 1,03), changement significatif 6,3 contre 6,1 ans, CCI 0,89 contre 0,89 ; cardiovasculaire
R = 1,02 ; métabolique 1,02. Le bruit physique y est simulé des deux côtés : ce n'est pas une
mesure réelle.

**CV intra-individuels observés par marqueur** (observé / prédit EFLM / prédit Lacher, %) :
CRP 59,7 / 35,2 / 35,2 ; ACR 57,1 / 40 / 40 ; TG 28,2 / 19,9 / 27,9 ; ALAT 18,6 / 13,0 / 20,7 ;
ASAT 17,7 / 9,0 / 15,8 ; lymphocytes % 16,6 / 11,3 / 15,5 ; GGT 15,2 / 8,7 / 16,5 ; leucocytes
13,4 / 11,3 / 15,3 ; HDL 9,4 / 6,5 / 6,5 ; plaquettes 8,5 / 7,8 / 9,0 ; glucose 8,3 / 5,1 / 7,7 ;
PAL 7,8 / 5,7 / 8,4 ; créatinine 7,3 / 6,4 / 8,1 ; cholestérol 7,2 / 5,6 / 7,1 ; albumine 3,4 /
2,8 / 3,7 ; hémoglobine 2,7 / 2,9 / 3,0 ; HbA1c 1,9 / 2,8 / 2,8 ; RDW 1,6 / 2,1 / 1,6 ; VGM 0,8 /
1,1 / 0,8. Biais moyens les plus nets (second − premier, en log) : ACR −9,6 %, TG +3,6 %,
hémoglobine −1,9 %, leucocytes −1,8 %, cholestérol −1,6 %, albumine −1,6 %.

**Facteurs.** Délai : aucune corrélation entre |d| et le délai (Spearman |ρ| ≤ 0,05 pour tous les
scores). « À jeun aux deux » (indicateur indirect, n = 142) : global ET_w 2,03, sans réduction.
Séance du premier examen : matin (n = 207) 1,94 ; après-midi ou soir (n = 180) 1,78.
Rapport : `reports/checkup_standard/fiabilite_reelle/`. Interprétation en attente de validation ;
NHANES III non commencé.

## Correction de bug — lecture des zéros des fichiers SAS (2026-11-10)

**Nature** : correction de bug, pas un réglage. Aucune décision de modélisation n'a changé (panel,
transformations, pénalisation, protocoles) ; seules les données d'entrée sont corrigées.

**Bug.** `pandas.read_sas` (format xport) rend les valeurs 0 sous la forme d'un flottant minuscule
(≈ 5,4 × 10⁻⁷⁹). Les règles écrites pour 0 ne s'appliquaient donc pas.

**Audit** (`scripts/audit_zeros_sas.py`, sortie `reports/audit_zeros_sas.csv`). Le script couvre
tous les fichiers XPT de tous les cycles (1999-2009, 2015-2018), toutes les colonnes numériques,
plus le fichier des médicaments, le second examen 2001-2002 et PH_B. Il trouve 323 colonnes
contenant de tels zéros, dont 56 lues par le pipeline, dans quatre familles :

| Variable | Usage dans le pipeline | Effet |
|---|---|---|
| `BPXDI1-4` (diastolique), tous cycles | moyenne des lectures, règle « 0 = manquant » | **touchée** : un 0 entrait dans la moyenne (diastolique sous-estimée), ou une moyenne quasi nulle était rejetée par la plage plausible au lieu d'ignorer la seule lecture nulle |
| `RIDAGEYR` (âge) | filtre 20-79 ans | aucun : les 0 sont des nourrissons, exclus dans les deux cas |
| `INDFMPIR` (revenu / seuil de pauvreté) | classes < 1,3 / 1,3-3,5 / ≥ 3,5 (équité) | aucun : 5 × 10⁻⁷⁹ et 0 tombent dans la même classe |
| `WTMEC2YR` (poids d'enquête) | lu, non utilisé dans les analyses | aucun |
| `PHDSESN`, `PHAFSTHR` (PH_B, fiabilité) | séance et jeûne du premier examen | déjà corrigé par arrondi le 2026-11-10 (écart au protocole de fiabilité) |

Aucun zéro exact n'apparaît dans aucun fichier : tous les 0 sont lus comme 5 × 10⁻⁷⁹. Les
codes des questionnaires (1, 2, 7, 9), les variables de laboratoire, les codes de médicaments et
les fichiers de mortalité (texte à largeur fixe, lus sans `read_sas`) ne sont pas touchés.

**Correction.** Fonction `nhanes.read_xpt` : lecture SAS puis remise à 0 exact de toute valeur
0 < |x| < 10⁻³⁰. Elle sert à toutes les lectures XPT (pipeline, médicaments, fiabilité). Deux tests
ajoutés. Caches harmonisés supprimés, pipeline entier relancé : validation, export du modèle,
PhenoAge, équité, 2015-2018, incertitude, prédictions et analyse de fiabilité. La sélection des
variables (points 1-2) n'a pas été relancée : le panel reste figé.

**Effet sur les effectifs.** +50 personnes complètes dans la cohorte (23 129 → 23 179) : leur
diastolique n'est plus rejetée. 37 diastoliques sont corrigées (biais médian −19 mmHg).

**Avant / après.**

| Indicateur | Avant | Après |
|---|---|---|
| n développement (décès) | 13 882 (2 785) | 13 903 (2 796) |
| n validation (décès) | 9 247 (972) | 9 276 (978) |
| C âge + sexe | 0,8067 | 0,8065 |
| C global [IC 95 %] | 0,8530 [0,841 ; 0,864] | 0,8532 [0,842 ; 0,865] |
| Gain de C global | +0,0464 | +0,0467 |
| Gain de C cardio / métab. / rénal / hépat. / inflam. | 0,0120 / 0,0126 / 0,0133 / 0,0237 / 0,0259 | 0,0121 / 0,0126 / 0,0132 / 0,0237 / 0,0263 |
| HR par écart-type (global) | 2,007 | 2,015 |
| Obs./prédit 10 ans ; pente (global) | 0,921 ; 0,991 | 0,915 ; 0,990 |
| Écart-type de l'écart d'âge global | 7,48 ans | 7,49 ans |
| ΔC global − PhenoAge publié | +0,0215 | +0,0216 |
| ΔC global − PhenoAge réentraîné ; réentraîné − publié | +0,0163 ; +0,0052 | +0,0164 ; +0,0052 |
| Équité, obs./prédit : revenu ≥ 3,5 ; mexicain-américain ; diplôme universitaire | 0,620 ; 0,649 ; 0,69 | 0,616 ; 0,648 ; 0,695 |
| 2015-2018 brut : C ; écart moyen | 0,848 ; +1,86 an | 0,850 ; +1,89 an |
| 2015-2018 harmonisé : C ; écart moyen | 0,850 ; −1,08 an | 0,851 ; −1,07 an |
| Incertitude (CV Lacher) : largeur IC 95 % ; chgt significatif ; CCI ; bascule | 10,58 ; 7,47 ; 0,873 ; 15,7 % | 10,62 ; 7,49 ; 0,873 ; 15,7 % |
| Fiabilité 2001-2002 : n (prédictions / analyse) | 389 / 387 | 390 / 388 |
| Fiabilité : ET_w prédit / observé (global) ; R | 1,779 / 1,868 ; 1,051 | 1,785 / 1,871 ; 1,049 |
| Fiabilité : R rénal / hépatique / inflam. / PhenoAge publié / réentraîné | 1,337 / 1,039 / 1,145 / 1,278 / 1,068 | 1,336 / 1,038 / 1,147 / 1,279 / 1,067 |

Toutes les conclusions sont inchangées ; tous les verdicts de fiabilité aussi. Les prédictions
de fiabilité figées le 2026-11-10 (`1795991`) ont été recalculées avec le modèle corrigé : une
personne de plus, ET_w prédit du global 1,779 → 1,785. La règle de lecture reste celle du
pré-enregistrement. Rapports régénérés ; `README.md` et `docs/fiche_modele.md` mis à jour.
Les chiffres des paragraphes antérieurs de ce fichier sont ceux d'avant la correction.

### Analyse exploratoire (non pré-enregistrée) — pourquoi la simulation se trompe (2026-11-10)

**Statut : exploratoire.** Les corrélations et les CV sont estimés sur les données mêmes qu'on
cherche à expliquer. Les deux hypothèses ont été posées par l'auteur du projet après les résultats.
À confirmer sur NHANES III. Code : `src/aging_clock/retest_explore.py` ; sorties :
`reports/checkup_standard/fiabilite_reelle/exploratoire/`. Même population (n = 388, modèle
corrigé). L'explication avancée plus haut (« simuler autour d'une valeur déjà bruitée rend la
méthode trop pessimiste ») n'est pas retenue : l'hypothèse a ci-dessous rend compte des données.

**a. Corrélation des variations intra-individuelles.** Corrélations de Spearman des différences
ln x₂ − ln x₁. Les protéines totales sont ajoutées (`LBXSTP`/`LB2STP`, hors modèle).
- Signature de dilution ou de posture : albumine-protéines 0,70 ; hémoglobine-protéines 0,58 ;
  albumine-hémoglobine 0,51 ; cholestérol-protéines 0,43 ; PAL-protéines 0,41 ; cholestérol-albumine
  0,38 ; plaquettes-protéines 0,34.
- Foie : ALAT-ASAT 0,64 ; ALAT-GGT 0,37. Leucocytes-lymphocytes % −0,37.
- Simulation avec un bruit log-normal corrélé (matrice de Spearman observée, projetée sur les
  matrices définies positives). Rapport R = ET_w observé / ET_w prédit, partie biologique :

| Simulation | Global | Hépatique | Inflam. | Rénal | Métab. | PhenoAge publié | PhenoAge réentraîné |
|---|---|---|---|---|---|---|---|
| CV observés de chaque marqueur, indépendants | 0,82 | 0,72 | 1,08 | 0,99 | 1,07 | 1,09 | 1,01 |
| CV observés, bruit corrélé | **0,99** | **1,04** | **1,00** | **0,99** | **1,04** | **1,05** | **0,98** |
| EFLM, indépendants (pré-enregistré) | 1,05 | 1,04 | 1,15 | 1,34 | 1,21 | 1,28 | 1,07 |
| EFLM, bruit corrélé | 1,18 | 1,38 | 1,09 | 1,34 | 1,17 | 1,27 | 1,05 |
| Lacher, indépendants | 0,82 | 0,68 | 1,16 | 1,29 | 1,00 | 1,12 | 1,01 |
| Lacher, bruit corrélé | 1,02 | 0,95 | 1,08 | 1,30 | 0,96 | 1,09 | 1,00 |

Lecture : avec les CV observés et leur corrélation, la simulation retrouve le bruit réel de tous
les scores (R entre 0,98 et 1,05). L'hypothèse d'indépendance surestimait le bruit du global et
de l'hépatique. Les variations corrélées se compensent en partie dans le score : par exemple,
ALAT et ASAT bougent ensemble (ρ = 0,64) alors que leurs effets sont de sens opposés : +10 %
d'ALAT donne −0,8 an d'âge global (médiane), +10 % d'ASAT +0,5 an. Même chose pour l'albumine
(+10 % → −1,5 an) et la PAL (+10 % → +0,3 an), corrélées à 0,29. Le
« compatible » pré-enregistré du score global vient donc de deux erreurs qui se compensent :
des CV EFLM trop bas et une hypothèse d'indépendance trop pessimiste.

**b. Valeurs extrêmes.** CV classiques comparés à des CV robustes (écart absolu médian) :
CRP 59,6 contre 35,1 % (EFLM 35,2) ; ACR 57,1 contre 39,9 % (valeur de travail 40) ; ASAT 17,7
contre 11,5 ; GGT 15,2 contre 11,5 ; glucose 8,2 contre 5,9 ; lymphocytes % 16,8 contre 12,7 ;
leucocytes 13,6 contre 10,7. Le cœur de la distribution varie à peu près comme le prévoient l'EFLM
et nos valeurs de travail. L'excès vient des queues : une minorité de personnes varie beaucoup plus.
- Cinq personnes portent 15 % (global) à 27 % (métabolique) de la somme des d².
- Sans les 47 personnes dont la CRP dépasse 10 mg/L à l'un des deux examens : ET_w de PhenoAge
  publié 2,04 → 1,74 ; inflammatoire 1,67 → 1,47 ; global 1,87 → 1,82 (peu sensible).
- ET_w robuste (écart absolu médian de d) : global 1,69 (prédit EFLM 1,79) ; PhenoAge publié 1,66.

**Conséquences (interprétation).** (1) Le bruit de mesure n'est ni indépendant entre marqueurs,
ni gaussien : il a des queues épaisses. Un changement significatif calculé avec
1,96 × racine(2) × ET suppose une loi normale. Il est trop large pour la plupart des personnes et
trop étroit pour celles qui traversent un épisode aigu. (2) La simulation doit intégrer la
corrélation des variations, et probablement un mélange « variation habituelle + épisode aigu ».
(3) Une CRP > 10 mg/L signale déjà un bilan peu fiable pour les scores qui l'utilisent.

## Fiabilité test-retest — réplication sur le second examen de NHANES III (pré-enregistrement, 2026-11-10)

Écrit et commité **avant** toute lecture des valeurs du second examen de NHANES III. Code :
`src/aging_clock/retest_nh3.py` (`predictions()` puis `analyse()`) et `src/aging_clock/nhanes3.py`
(lecture des fichiers ASCII à positions fixes d'après les programmes SAS du NCHS). L'analyse ne
sera lancée qu'après relecture de ce paragraphe par l'auteur du projet.

**Ce qui a déjà été vu.** La documentation NCHS (readme, codebooks LABSE, LAB2SE, EXAMSE) :
noms des variables, effectifs, plage du délai (1 à 52 jours). Les fichiers `labse.dat` et
`examse.dat` sont téléchargés, mais **seule la colonne SEQN en a été lue** (`nhanes3.seqn_only`).
L'examen principal de NHANES III (lab.dat, exam.dat) a été lu : il sert à la population et aux
prédictions.

**Sélection du sous-échantillon** (documentation EXAMSE, NCHS). « No statistical sampling design
was applied for the second exam. » Échantillon non aléatoire d'environ 5 % des personnes examinées
à chaque site (environ 400 par site), choisi par le personnel du centre mobile selon trois
consignes : surtout des adultes ; moitié 20-39 ans, moitié plus de 40 ans ; moitié hommes, moitié
femmes. Second examen programmé après le premier, si possible à la même heure, avec les mêmes
protocoles et le même personnel. Le NCHS recommande de ne pas utiliser les poids d'enquête et
d'examiner le biais de sélection. Pour comparaison, en 2001-2002 (Lacher et al. 2010, NHSR 21) :
recrutement non aléatoire, sexes et âges équilibrés de 16 à 69 ans, environ 5 % des personnes
prélevées, second prélèvement au moins 8 jours après le premier.

**Population.** Mêmes critères que la cohorte du modèle (20-79 ans, éligibles au chaînage de
mortalité NHANES III 2019, suivi > 0, hors grossesse `MAPF12R` = 1, cas complets sur le panel
au premier examen), et présence dans `labse` et `examse` : **n = 1 388** (47,4 ans en moyenne,
54 % de femmes). NHANES III est **indépendant** du développement du modèle (1999-2006).
À l'analyse, on exclura en plus les valeurs du second examen manquantes ou hors plage plausible.
On exigera le sang et l'urine pour la comparaison biologique, et les mesures physiques pour la
comparaison complète. Les prédictions seront alors recalculées sur ces populations finales, avec
le même code et les mêmes graines.

**Variables.** Examen principal / second examen : albumine `AMPSI`/`AMRSI`, créatinine
`CEPSI`/`CERSI`, glucose sérique `SGPSI`/`SGRSI`, TG sériques `TRPSI`/`TRRSI`, cholestérol
`TCPSI`/`TCRSI`, HDL `HDPSI`/`HDRSI`, PAL `APPSI`/`APRSI`, ALAT `ATPSI`/`ATRSI`, ASAT
`ASPSI`/`ASRSI`, GGT `GGPSI`/`GGRSI`, CRP `CRP`/`CRR` (× 10, mg/L), HbA1c `GHP`/`GHR`, leucocytes
`WCPSI`/`WCRSI`, lymphocytes % `LMPPCNT`/`LMRPCNT`, RDW `RWP`/`RWR`, VGM `MVPSI`/`MVRSI`,
hémoglobine `HGP`/`HGR`, plaquettes `PLPSI`/`PLRSI`, ACR (`UBP`/`URP` et `UBR`/`URR`, × 11,31),
PAS `PEPMNK1R`/`PERMNK1R`, PAD `PEPMNK5R`/`PERMNK5R`, pouls `PEP6DR`/`PER6DR`, IMC
`BMPBMI`/`BMRBMI`, tour de taille `BMPWAIST`/`BMRWAIST`. Codes « tout en 8 ou en 9 » sur toute la
largeur du champ (au moins 3 chiffres) traités comme manquants.

**Harmonisation vers les méthodes du modèle** (identique aux deux examens) :
- **créatinine** : standardisée = 0,960 × créatinine (mg/dL) − 0,184. Source : note CDC sur la
  créatinine sérique et Selvin et al. 2007, *Am J Kidney Dis* (doi:10.1053/j.ajkd.2007.08.020,
  résumé lu). La note CDC n'a pas pu être ouverte ; l'équation vient d'un extrait de recherche.
  Elle est cohérente avec la recalibration 1999-2000 de notre configuration (1,013 ; +0,147), tirée
  de la même note ;
- **CRP** : limite de détection de NHANES III 0,21 mg/dL = 2,1 mg/L. 58 % de la population y est.
  Toute valeur inférieure est fixée à 2,1 mg/L, **dans les remesures simulées comme dans les
  données réelles** ;
- autres marqueurs sans correction. Les automates diffèrent de ceux de 1999-2006 (limite déclarée).
  Cela décale les niveaux mais touche peu les différences entre deux examens mesurés par la même
  méthode.

**Comparaisons.**
1. **Biologique** (comme 2001-2002) : seuls le sang et l'urine changent ; mesures physiques fixes ;
   système cardiovasculaire non interprété.
2. **Complète** : mesures physiques **réellement remesurées** au second examen. Prédiction : bruit
   physique tiré des CV de la littérature (PAS et PAD 8,6 %, pouls 8,0 %, IMC 1,5 %, tour de
   taille 2,0 %), indépendant du sang.

**Trois scénarios de simulation** (bruit multiplicatif en log, 1 000 remesures par personne,
graine 2026, censure de la CRP à 2,1 mg/L après bruit) :
1. **EFLM, indépendant** : CV du pré-enregistrement 2001-2002 (`variability_retest.json`).
2. **CV et corrélations de 2001-2002** : écarts-types en log = ET(ln x₂ − ln x₁)/racine(2) observés
   en 2001-2002 ; corrélation de Spearman des variations de 2001-2002 ; loi normale multivariée.
3. **Vecteurs de variation de 2001-2002** : chaque remesure simulée tire au hasard le vecteur complet
   (ln x₂ − ln x₁)/racine(2) d'une des 388 personnes de 2001-2002, avec un signe aléatoire. Cela
   conserve la corrélation et les queues épaisses observées. C'est la version non paramétrique du
   mélange « variation habituelle + épisode aigu ».
Paramètres figés : `reports/checkup_standard/fiabilite_nhanes3/parametres_2001_2002.json`
(SHA-256 `aae70c0a…`) ; vecteurs dans `data/processed/vecteurs_variation_2001_2002.csv`
(hors dépôt, empreinte dans le JSON).

**Critère de comparaison des scénarios** (fixé maintenant), sur les 7 scores interprétés (global,
métabolique, rénal, hépatique, inflammatoire et hématologique, PhenoAge publié, PhenoAge
réentraîné) :
- pour chaque score : R = ET_w observé / ET_w prédit, avec IC 95 % bootstrap (2 000 tirages) ; et
  rapports centile prédit / centile observé de |écart₂ − écart₁| aux centiles 50, 90 et 95 ;
- **perte** d'un scénario = moyenne sur les 7 scores de [ |ln R| + moyenne des trois |ln(rapport
  de centiles)| ] ;
- **meilleur scénario** = perte la plus faible, pour chaque comparaison (biologique, complète) ;
- un scénario est dit **adéquat** si, pour les 7 scores, l'IC de R contient 1 **et** les trois
  rapports de centiles sont dans [0,80 ; 1,25]. Le meilleur scénario peut ne pas être adéquat ;
  ce sera alors écrit.

**Métriques rapportées** (par score, observées et prédites) : ET_w ; changement significatif
gaussien 1,96 × racine(2) × ET_w **et** empirique (95ᵉ centile de |d|) ; CCI(A,1) avec IC ;
Bland-Altman (biais, limites) ; taux de bascule ; centiles 50, 90, 95 de |d| ; CV classiques et
robustes (écart absolu médian) par marqueur.

**Prédiction directionnelle du décalage systématique** (d'après 2001-2002) : au second examen, le
score global est **plus vieux** (moyenne de d > 0), l'albumine et l'hémoglobine sont **en
baisse** (moyenne de ln x₂ − ln x₁ < 0). Test : IC 95 % bootstrap de la moyenne.
- Confirmé si la borne basse > 0 (global) et la borne haute < 0 (albumine, hémoglobine) ;
- contredit si l'IC est entièrement du côté opposé ;
- non concluant sinon.
Les autres scores et marqueurs sont décrits.

**Règle pratique « CRP > 10 mg/L à l'un des deux examens ».** Prédiction d'après 2001-2002 :
rapport ET_w sans ces personnes / ET_w de tous = global 0,975 ; métabolique 0,875 ; rénal 1,018 ;
hépatique 0,982 ; inflammatoire 0,879 ; PhenoAge publié 0,852 ; PhenoAge réentraîné 0,897.
Test : IC 95 % bootstrap du rapport observé.
- Prédiction compatible si la valeur prédite est dans l'IC ;
- effet confirmé pour l'inflammatoire et PhenoAge publié si la borne haute < 1.

**Mesures physiques.** CV observés (classiques et robustes) de la PAS, de la PAD, du pouls, de
l'IMC et du tour de taille. Ils sont comparés à deux références :
- la littérature (8,6 ; 8,6 ; 8,0 ; 1,5 ; 2,0 %) ;
- la variabilité intra-visite de NHANES III, estimée sur les trois lectures de l'examen principal
  (14 692 adultes de 20-79 ans) : PAS 3,6 % par lecture, 2,1 % pour la moyenne de 3 ; PAD 5,5 %
  et 3,2 %.
Descriptif, sans règle de décision.

**Facteurs** (descriptifs) : tertiles du délai (`MXPRDAYS`, sinon `MXRRDAYS`) ; même séance
(`MXPSESSR` = `MXRSESSR`) ou non ; à jeun ≥ 8 h aux deux examens (`PHPFAST`, `PHRFAST`). Ces
variables existent cette fois pour les deux examens : pas d'indicateur indirect.

**Prédictions figées** (n = 1 388 ; `predictions.csv`). Partie biologique : ET_w ;
changement significatif gaussien ; centiles 50 / 90 / 95 de |d|.

| Score | Scénario 1 (EFLM) | Scénario 2 (CV + corrélation 2001-02) | Scénario 3 (vecteurs 2001-02) |
|---|---|---|---|
| Global | 1,74 ; 4,8 ; 1,64 / 4,05 / 4,86 | 1,84 ; 5,1 ; 1,75 / 4,28 / 5,13 | 1,81 ; 5,0 ; 1,65 / 4,17 / 5,08 |
| Métabolique | 0,26 ; 0,7 ; 0,25 / 0,61 / 0,73 | 0,31 ; 0,8 ; 0,29 / 0,71 / 0,85 | 0,30 ; 0,8 ; 0,25 / 0,68 / 0,85 |
| Rénal | 1,11 ; 3,1 ; 1,02 / 2,60 / 3,12 | 1,50 ; 4,1 ; 1,37 / 3,51 / 4,21 | 1,48 ; 4,1 ; 1,17 / 3,38 / 4,31 |
| Hépatique | 1,62 ; 4,5 ; 1,46 / 3,77 / 4,58 | 1,63 ; 4,5 ; 1,51 / 3,78 / 4,54 | 1,63 ; 4,5 ; 1,44 / 3,71 / 4,53 |
| Inflammatoire | 1,46 ; 4,0 ; 1,37 / 3,38 / 4,04 | 1,58 ; 4,4 ; 1,49 / 3,68 / 4,41 | 1,65 ; 4,6 ; 1,40 / 3,72 / 4,70 |
| PhenoAge publié | 1,63 ; 4,5 ; 1,52 / 3,77 / 4,52 | 1,97 ; 5,5 ; 1,83 / 4,54 / 5,47 | 2,07 ; 5,7 ; 1,69 / 4,54 / 5,82 |
| PhenoAge réentraîné | 1,41 ; 3,9 ; 1,34 / 3,28 / 3,92 | 1,50 ; 4,2 ; 1,42 / 3,49 / 4,16 | 1,51 ; 4,2 ; 1,31 / 3,44 / 4,29 |

Comparaison complète, global : ET_w 2,18 / 2,26 / 2,23 ; changement significatif 6,0 / 6,3 / 6,2 ;
cardiovasculaire 2,00 / 2,04 / 2,04. CCI prédits du global : 0,947 / 0,941 / 0,943 (biologique).

Empreintes (`meta_predictions.json`) : CV `b7674478…`, paramètres 2001-2002 `aae70c0a…`, code
de `retest_nh3.py` `4f89054e…`. L'analyse refuse de tourner si les CV ou les paramètres 2001-2002
ont changé.

### Amendement au pré-enregistrement NHANES III (2026-11-10, avant toute lecture des valeurs du second examen)

Demandé par l'auteur du projet après relecture. Commité avant le lancement de `analyse()`.

1. **Scénario 3 centré.** Les vecteurs de variation de 2001-2002 sont centrés (moyenne de chaque
   marqueur retirée) avant le rééchantillonnage. Le scénario ne prédit ainsi que le bruit ; le
   décalage systématique est testé à part. Moyennes retirées (en log) : par exemple ACR −0,095,
   TG +0,036, CRP −0,030, leucocytes −0,019, ALAT −0,019, hémoglobine −0,018, albumine −0,016,
   cholestérol −0,015. Les vecteurs sont bien appliqués en **variations relatives** : x* = x ·
   exp(v/racine(2)), avec v = (ln x₂ − ln x₁) centré. Les scénarios 1 et 2 sont déjà centrés par
   construction (bruit gaussien de moyenne 0 en log, facteur multiplicatif de médiane 1). Ils ne
   changent pas.
   Prédictions du scénario 3 recalculées (biologique) : global ET_w 1,81 → 1,80 (changement
   significatif 5,0 ; centiles 1,64 / 4,16 / 5,06) ; hépatique 1,63 → 1,60 ; rénal 1,48 → 1,47 ;
   inflammatoire 1,65 → 1,64 ; PhenoAge publié 2,07 → 2,04 ; réentraîné 1,51 → 1,49 ; métabolique
   inchangé (0,30). Complète, global : 2,23 → 2,22. Code `retest_nh3.py` : nouvelle empreinte
   `716d4d1e…` ; paramètres 2001-2002 inchangés (`aae70c0a…`).
2. **CRP à la limite de détection.** Avec 58 % de valeurs à la limite (2,1 mg/L), la CRP de ces
   personnes ne peut pas varier entre les deux examens. Le système inflammatoire et hématologique
   et les deux PhenoAge seront donc **artificiellement stables** en NHANES III. Leurs valeurs
   absolues (changement significatif, CCI, bascule) **ne sont pas comparables** à 2001-2002 ni à
   une cohorte qui dose la CRP ultrasensible. Pour ces trois scores, seule la comparaison
   simulation contre réalité (même censure des deux côtés) est interprétée.
3. **Créatinine** : l'équation 0,960 × créatinine − 0,184 est **non vérifiée à la source CDC** (note
   non ouverte ; extrait de recherche seulement).
4. **Généralisation** : sélection non aléatoire, choisie par le personnel, et seconds examens
   programmés si possible à la même heure, avec le même protocole et le même personnel. Le bruit
   mesuré ici est donc probablement **inférieur** à celui d'un suivi réel (heure, laboratoire,
   saison, état de santé différents d'une visite à l'autre). Même réserve pour 2001-2002, où le
   délai minimal était de 8 jours.

### Résultat — réplication NHANES III (2026-11-10)

Exécution du protocole pré-enregistré et amendé (`6713ba0`) ; empreintes des CV et des
paramètres 2001-2002 vérifiées par le code. Aucun écart de code. Sorties :
`reports/checkup_standard/fiabilite_nhanes3/`.

**Population.** 1 388 personnes prévues → **781** avec le sang et l'urine complets au second
examen. La cause n'était pas anticipée : l'**ACR manque au second examen pour 579 personnes** (urine
non recueillie). Pouls et tour de taille manquent pour un groupe proche. Les 781 restants
forment un sous-échantillon du sous-échantillon. Comparaison complète : 740. Délai médian
16 jours (1-48).

**Choix du scénario** (règle pré-enregistrée, 7 scores interprétés) :

| Comparaison | 1. EFLM indépendant | 2. CV + corrélation 2001-02 | 3. Vecteurs 2001-02 centrés |
|---|---|---|---|
| Biologique : perte | 0,517 | **0,299 (meilleur)** | 0,312 |
| Complète : perte | 0,414 | **0,242 (meilleur)** | 0,243 |

**Aucun scénario n'est adéquat.** Le scénario 2 est le meilleur, à peine devant le 3.

**R = ET_w observé / prédit [IC 95 %], partie biologique :**

| Score | 1. EFLM | 2. CV + corr. 2001-02 | 3. Vecteurs 2001-02 | Rapport des 95ᵉ centiles prédit/observé (2) |
|---|---|---|---|---|
| Global | 1,24 [1,16 ; 1,32] | 1,17 [1,10 ; 1,25] | 1,20 [1,12 ; 1,27] | 0,82 |
| Métabolique | 1,51 [1,35 ; 1,69] | 1,30 [1,16 ; 1,45] | 1,30 [1,16 ; 1,46] | 0,80 |
| Rénal | 1,83 [1,72 ; 1,95] | 1,36 [1,28 ; 1,45] | 1,38 [1,30 ; 1,47] | 0,72 |
| Hépatique | 1,11 [1,04 ; 1,18] | 1,10 [1,03 ; 1,17] | 1,12 [1,05 ; 1,19] | 0,87 |
| Inflammatoire (CRP censurée) | 1,16 [1,07 ; 1,25] | 1,07 [0,98 ; 1,16] | 1,03 [0,95 ; 1,12] | 0,92 |
| PhenoAge publié (CRP censurée) | 1,68 [1,39 ; 2,00] | 1,39 [1,15 ; 1,65] | 1,33 [1,11 ; 1,59] | 0,81 |
| PhenoAge réentraîné (CRP censurée) | 1,13 [1,06 ; 1,20] | 1,06 [0,99 ; 1,13] | 1,07 [1,00 ; 1,14] | 0,92 |

Médianes de |d| bien prédites (rapports 0,95 à 1,12 pour le scénario 2, sauf cardiovasculaire non
interprété), 95ᵉ centiles sous-estimés : les queues sont encore plus épaisses qu'en 2001-2002.

**Valeurs observées, partie biologique** : global ET_w 2,15 ; changement significatif gaussien
6,0 ans, empirique (95ᵉ centile) 6,2 ans ; CCI 0,91 [0,90 ; 0,93] ; bascule 15,0 %. Rénal : CCI
0,74, changement significatif 5,6 / 5,9 ans. Hépatique : CCI 0,85, 4,9 / 5,2 ans. Score complet
(tension et mensurations réellement remesurées) : global ET_w 2,41, changement significatif 6,7 /
6,9 ans, CCI 0,89 ; R = 1,07 [1,00 ; 1,13] (scénario 2). Cardiovasculaire R = 0,88 [0,82 ; 0,94] :
la simulation surestime son bruit. Pour l'inflammatoire et les PhenoAge, les valeurs absolues ne
sont pas comparables à 2001-2002 (CRP censurée, amendement 2).

**CV par marqueur** (observé / robuste / prédit EFLM / observé 2001-02, %) : ACR 88 / 59 / 40 / 57 ;
ALAT 25,4 / 18,3 / 13,0 / 18,6 ; ASAT 17,8 / 11,1 / 9,0 / 17,7 ; GGT 15,7 / 11,7 / 8,7 / 15,2 ;
TG 23,2 / 21,5 / 19,9 / 28,2 ; glucose 10,2 / 6,2 / 5,1 / 8,2 ; HDL 10,4 / 7,2 / 6,5 / 9,4 ;
plaquettes 11,0 / 6,9 / 7,8 / 8,5 ; HbA1c 3,4 / 2,1 / 2,8 / 1,9 ; albumine 4,0 / 2,9 / 2,8 / 3,4 ;
hémoglobine 2,9 / 2,8 / 2,9 / 2,7. CRP 41 % (CV robuste nul : plus de la moitié des valeurs à la
limite de détection).

**Mesures physiques** (CV observé / robuste ; littérature ; intra-visite NHANES III pour la
moyenne de 3 lectures) : PAS 2,8 / 2,3 ; 8,6 ; 2,1. PAD 3,9 / 3,2 ; 8,6 ; 3,2. Pouls 9,5 / 9,6 ;
8,0. IMC 1,4 / 0,9 ; 1,5. Tour de taille 2,5 / 1,8 ; 2,0. La tension remesurée à environ 2 semaines,
avec le même protocole et le même personnel, varie presque comme d'une lecture à l'autre dans la
même visite. C'est 3 fois moins que la variabilité entre visites au cabinet de la littérature.

**Décalage systématique** (prédiction directionnelle de 2001-2002) :
- score global : +0,12 an [−0,10 ; +0,33] → **non concluant** ;
- albumine : −0,57 % [−0,97 ; −0,14] → **confirmé** ;
- hémoglobine : −1,51 % [−1,80 ; −1,22] → **confirmé**.
Décrits : inflammatoire +0,20 [+0,03 ; +0,37] ; PhenoAge publié +0,36 [+0,10 ; +0,64] ; HDL −1,4 % ;
GGT −2,0 % ; TG +2,3 %.

**Règle CRP > 10 mg/L** (103 personnes exclues) : rapport observé [IC 95 %] contre prédit.

| Score | Observé [IC 95 %] | Prédit | Verdict |
|---|---|---|---|
| Global | 0,959 [0,921 ; 0,993] | 0,975 | compatible |
| Inflammatoire | 0,930 [0,879 ; 0,976] | 0,879 | compatible de justesse ; effet confirmé (borne haute < 1) |
| Hépatique | 0,996 [0,964 ; 1,021] | 0,982 | compatible |
| PhenoAge publié | 0,970 [0,882 ; 1,025] | 0,852 | non compatible ; effet non confirmé |
| PhenoAge réentraîné | 0,970 [0,937 ; 0,997] | 0,897 | non compatible |
| Métabolique | 0,987 [0,951 ; 1,014] | 0,875 | non compatible |
| Rénal | 0,991 [0,966 ; 1,013] | 1,018 | non compatible |

La censure de la CRP limite l'effet attendu pour les PhenoAge.

**Facteurs.** Séance : identique aux deux examens pour les 781 personnes (aucun contraste, effet
non testable). À jeun ≥ 8 h aux deux (n = 457) : global ET_w 2,09 contre 2,15 pour tous. Délai :
pas de gradient (tertiles 2,11 / 2,31 / 1,97).

**Lecture** (interprétation) :
1. La réplication indépendante ne valide **aucun** des trois modèles de bruit.
2. Le meilleur, CV et corrélations de 2001-2002, prédit bien la **médiane** des écarts mais
   sous-estime le bruit total de 6 à 39 % selon le score. Les queues sont plus épaisses qu'en
   2001-2002, surtout pour l'ACR, le rénal et le métabolique.
3. La corrélation des variations améliore nettement la prédiction : perte 0,30 contre 0,52 pour
   l'EFLM indépendant.
4. Le changement significatif réel du score global est d'environ **6 ans pour la partie
   biologique et 7 ans pour le score complet**, à environ 2 semaines et dans des conditions
   standardisées. C'est probablement une borne basse pour un suivi réel.

### Analyses finales (non pré-enregistrées, 2026-11-10) et gel des analyses

Demandées par l'auteur du projet après les résultats de NHANES III. Code :
`retest_nh3.selection_bias()` et `retest_nh3.empirical_thresholds()`.

**1. Biais de sélection lié à l'ACR manquante.** On ne reporte pas l'ACR du premier examen : cela
figerait le système rénal. On compare plutôt la fiabilité des scores sans ACR, mesures physiques
fixes, dans trois groupes : les 781 personnes avec ACR, les 1 233 personnes disponibles (sang
complet hors ACR) et les 452 personnes sans ACR. Rapport ET_w sans ACR / avec ACR [IC 95 %] :

| Score | Rapport [IC 95 %] |
|---|---|
| Métabolique | 1,03 [0,85 ; 1,27] |
| Hépatique | 0,98 [0,89 ; 1,07] |
| Inflammatoire | 0,95 [0,83 ; 1,07] |
| PhenoAge publié | 0,94 [0,75 ; 1,20] |
| PhenoAge réentraîné | 0,97 [0,88 ; 1,08] |

CCI quasi identiques entre groupes. **Aucun biais de sélection détecté** sur la fiabilité. Les
personnes sans ACR au second examen sont un peu plus âgées (49,6 contre 46,9 ans) et ont un écart
global initial plus élevé (+2,4 contre +1,9 an).

**2. Seuil empirique de changement significatif** (95ᵉ centile de |écart₂ − écart₁| ; IC 95 % par
bootstrap stratifié par source, 2 000 tirages). Scores sans mesure physique : 2001-2002 et
NHANES III regroupés. Scores avec mesures physiques (global, cardiovasculaire, métabolique) :
NHANES III seul, la seule source où tout est réellement remesuré.

| Score | Sources (n) | Tous | Sans CRP > 10 mg/L [IC 95 %] | Gaussien (sans CRP > 10) |
|---|---|---|---|---|
| Global (complet) | NHANES III (740 / 646) | 6,93 | **6,50** [5,95 ; 7,11] | 6,40 |
| Cardiovasculaire | NHANES III | 4,89 | **4,84** [4,46 ; 5,41] | 4,76 |
| Métabolique | NHANES III | 2,82 | **2,83** [2,55 ; 3,05] | 2,71 |
| Rénal | 2001-02 + NHANES III (1 169 / 1 019) | 5,51 | **5,52** [5,17 ; 6,07] | 5,20 |
| Hépatique | 2001-02 + NHANES III | 5,10 | **5,10** [4,75 ; 5,55] | 4,89 |
| Inflammatoire et hématologique | 2001-02 + NHANES III | 4,75 | **4,32** [3,92 ; 4,60] | 4,26 |

Médianes de |d| : 0,7 (métabolique) à 2,1 ans (global). Le seuil gaussien est un peu plus
étroit que le 95ᵉ centile ; c'est au-delà du 95ᵉ centile que les queues épaisses pèsent le plus.
Réserve : en NHANES III, la CRP est censurée à 2,1 mg/L, ce qui stabilise artificiellement
l'inflammatoire.

**Option `--uncertainty` remplacée.** Elle n'ajoute plus d'intervalle Monte-Carlo, mais le seuil
empirique de chaque score (`models/seuils_changement_v1.json`, version « sans CRP > 10 mg/L ») et
une colonne `alerte_crp`. Si la CRP dépasse 10 mg/L, aucun seuil n'est fourni. `score.py` ne
dépend plus de `uncertainty.py`, conservé pour le rapport `INCERTITUDE.md`, désormais historique.
Fiche du modèle : un intervalle gaussien n'est pas adapté. README mis à jour. Test ajouté.

**Gel des analyses (décision de l'auteur du projet, 2026-11-10).** Plus aucune nouvelle analyse.
La suite se limite à la rédaction (rapport PDF).

## Piste « suivi » (2026-11-10) — contexte et réserves communes

Nouvelle piste demandée par l'auteur du projet : ce qu'un produit de check-up de prévention peut
honnêtement affirmer d'un bilan à l'autre (contexte générique, aucune entreprise). Conditions
visées :
- bilan complet au départ, puis une prise de sang tous les 6 mois ;
- panel de suivi réduit, sans les urines ;
- variantes de panel et de laboratoire ;
- ni heure de prélèvement ni jeûne enregistrés ;
- **ni tension ni mensurations**, et un pouls seulement via un objet connecté optionnel.

Le gel des analyses du 2026-11-10 est levé par l'auteur du projet pour cette piste.

**Réserves communes à toutes les questions.**
1. Nos remesures sont à environ **2 semaines**, et en NHANES III à la même heure, avec le même
   protocole et le même personnel. À 6 mois, et sans contrôle de l'heure ni du jeûne, le bruit sera
   plus grand : nos chiffres sont des **bornes basses**.
2. Les données de test **ne sont pas vierges**. Les remesures de NHANES III ont déjà été analysées
   (fiabilité des scores) et la validation 2007-2010 a été consultée plusieurs fois. Les nouveaux
   indicateurs de cette piste n'y ont jamais été calculés : le pré-enregistrement garde son sens,
   mais l'évaluation n'est pas à l'aveugle.
3. Découpage : fiabilité calée sur 2001-2002 et testée sur NHANES III ; mortalité développée sur
   1999-2006 et validée sur 2007-2010.

## Suivi, étape 0 — modèle « sang seul » (pré-enregistrement, 2026-11-10)

Écrit et commité avant toute évaluation sur la validation 2007-2010. Code :
`src/aging_clock/sang_seul.py`. Panel : `config/panels/checkup_sang_seul.yaml`.

**Modèle.** Mêmes systèmes, mêmes transformations et mêmes plages que `checkup_standard`, mais
sans tension (PAS, PAD), pouls, IMC ni tour de taille (déclarés `in_model: false`). L'ACR est
gardée : le bilan de départ comprend les urines. Il reste 19 marqueurs. Le cardiovasculaire se
réduit aux lipides (cholestérol, HDL, TG) et le métabolique à la glycémie et à l'HbA1c ; le rénal,
l'hépatique et l'inflammatoire sont inchangés. Hyperparamètres figés : pénalisation 0 (valeur
retenue pour le modèle complet, pas de nouvelle sélection), nœuds appris sur le développement,
même grille d'âge.

**Analyse principale : mêmes personnes que le modèle complet.** Entraînement sur les 13 903
personnes du développement 1999-2006, validation sur les 9 276 personnes de 2007-2010. On isole
ainsi l'effet du retrait des variables. Indicateurs par score (global et 5 systèmes) :
- C [IC 95 %] et gain de C par rapport à âge + sexe ;
- HR par écart-type d'écart d'âge ;
- rapport observé/prédit et pente de calibration à 10 ans ;
- **différence de C appariée** sang seul − complet, par bootstrap (1 000 tirages, graine 42).

**Analyse secondaire : cohorte propre.** Cas complets sur les 19 marqueurs seulement, donc avec
les personnes sans mesures physiques. On donne C et calibration ; il n'y a pas de comparaison
appariée.

**Prédiction** (validation croisée « un cycle retiré » sur le développement, mêmes personnes,
`reports/checkup_sang_seul/prediction_cv_developpement.csv`). Différence de C sang seul − complet :

| Score | Prédiction (moyenne des 4 plis) |
|---|---|
| Global | −0,0032 (de −0,0037 à −0,0028 selon les plis) |
| Cardiovasculaire | −0,0060 (de −0,0082 à −0,0052) |
| Métabolique | −0,0056 (de −0,0069 à −0,0041) |
| Rénal, hépatique, inflammatoire | 0 (modèles identiques par construction) |

**Règles de lecture** (fixées maintenant) :
- la prédiction est **compatible** si elle est dans l'IC 95 % de la différence appariée observée ;
- la **perte de discrimination est jugée faible** si la borne basse de l'IC de la différence de C
  du score global est supérieure à −0,010 ;
- la **calibration est jugée acceptable** si le rapport observé/prédit est dans [0,80 ; 1,20] et
  si l'IC de la pente coupe [0,80 ; 1,20]. C'est la même règle que l'audit d'équité.

Quel que soit le résultat, l'auteur du projet a décidé que Q1 et Q2 porteraient sur le modèle
« sang seul » en analyse principale, et sur le modèle complet en secondaire.

### Résultat — étape 0, modèle « sang seul » (2026-11-10)

Exécution du protocole pré-enregistré (`484a24d`) ; aucun écart.
Sorties : `reports/checkup_sang_seul/validation_sang_seul.csv`.

**Analyse principale** : mêmes personnes (validation n = 9 276, 978 décès), C de référence âge +
sexe 0,807.

| Score | C sang seul [IC 95 %] | C complet | Différence appariée [IC 95 %] | Prédiction (CV) | Gain vs âge + sexe | HR / ET (ET de l'écart) | Obs./prédit ; pente [IC] |
|---|---|---|---|---|---|---|---|
| Global | 0,850 [0,838 ; 0,861] | 0,853 | −0,0036 [−0,0056 ; −0,0013] | −0,0032 | +0,043 | 1,91 (6,8 ans) | 0,92 ; 0,99 [0,94 ; 1,04] |
| Cardiovasculaire (lipides) | 0,810 | 0,819 | −0,0087 [−0,0118 ; −0,0055] | −0,0060 | +0,003 [0,002 ; 0,005] | 1,18 (2,0 ans) | 0,92 ; 0,95 [0,89 ; 1,01] |
| Métabolique (glycémie, HbA1c) | 0,811 | 0,819 | −0,0079 [−0,0109 ; −0,0048] | −0,0056 | +0,005 [0,002 ; 0,007] | 1,20 (2,0 ans) | 0,95 ; 0,98 [0,92 ; 1,04] |
| Rénal, hépatique, inflammatoire | identiques au modèle complet (0,820 ; 0,830 ; 0,833) | | 0 | 0 | | | 0,95-0,96 ; ≈ 1 |

**Règles pré-enregistrées.**
- Prédictions **compatibles** pour les trois scores qui changent : −0,0032, −0,0060 et −0,0056
  sont chacune dans leur IC.
- Perte de discrimination du global **faible** : borne basse −0,0056 > −0,010.
- Calibration **acceptable** pour tous les scores.

**Analyse secondaire** (cohorte propre, cas complets sur les 19 marqueurs : 14 880 personnes en
développement, 9 914 en validation, 1 087 décès) : C global 0,851 (référence 0,808), rapport
observé/prédit 0,92, pente 1,01.

**Lecture** (interprétation) :
- le score global « sang seul » perd très peu (−0,004 de C) ;
- en revanche, sans tension ni mensurations, le **cardiovasculaire** (lipides seuls) et le
  **métabolique** (glycémie, HbA1c) n'apportent presque plus rien au-delà de l'âge et du sexe
  (gain de C +0,003 et +0,005). Leur écart d'âge ne varie que de 2,0 ans (écart-type) entre
  personnes, contre 3,7 et 3,9 ans dans le modèle complet. Ces deux systèmes ne pourront pas porter
  des affirmations fortes ;
- note technique : la valeur p bootstrap affichée « 2,000 » pour les systèmes identiques est un
  artefact de la formule quand toutes les différences sont nulles ; elle se lit « sans objet ».
