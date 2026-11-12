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

## Suivi, Q1 et Q2 — pré-enregistrement (2026-11-10)

Écrit et commité **avant** tout calcul de ces indicateurs sur NHANES III. Code :
`src/aging_clock/suivi.py` (`predictions()` : calage sur 2001-2002 ; `analyse()` : test sur NHANES
III). Calage figé : `reports/checkup_standard/suivi/Q1_Q2_predictions.json`, SHA-256 `c6472dd2…`
(code au moment du calage : `2172cb6b…`).

**Modèles.**
- **Principal** : « sang seul » (étape 0), ajusté sur le développement, pénalisation 0.
- **Secondaire** : modèle complet. Comme la tension et les mensurations ne sont pas remesurées en
  2001-2002, la comparaison porte sur sa partie biologique : mesures physiques figées entre les
  deux examens, et jamais candidates comme moteurs.

**Données.** Mêmes paires qu'au pré-enregistrement de la fiabilité : 2001-2002 (n = 388, calage)
et NHANES III (n = 781, test ; sang et urine complets au second examen ; CRP censurée à
2,1 mg/L). Réserve : les remesures sont à environ 2 semaines, donc les résultats sont des bornes
basses pour un suivi à 6 mois.

### Q1 — définitions

- **Seuil de changement significatif** : 95ᵉ centile de |écart₂ − écart₁| (IC 95 % par bootstrap,
  2 000 tirages), et version gaussienne, pour le global et chaque système.
- **Système prioritaire** : système dont l'écart **standardisé** est le plus défavorable. L'écart
  standardisé est le centile de l'écart d'âge du système parmi les personnes du développement de
  même sexe et de même tranche d'âge de 10 ans (20-29, …, 70-79).
- **Contribution d'un marqueur** (en années d'écart global) : écart global observé moins écart
  global quand le marqueur est remplacé par sa **valeur de référence**, c'est-à-dire la médiane du
  développement pour le même sexe et la même tranche d'âge de 10 ans.
- **Moteurs, toutes versions** : jusqu'à 3 marqueurs aux contributions positives les plus fortes,
  c'est-à-dire ceux qui vieillissent le plus le score. Si moins de 3 contributions sont
  positives, la liste est plus courte, et elle peut être vide. Les mesures physiques ne sont jamais
  candidates.
- **Moteurs actionnables** : mêmes règles, restreintes aux marqueurs de la table ci-dessous, et
  seulement quand la valeur est du côté actionnable de la référence (au-dessus pour « haut »,
  en dessous pour « bas »).
- **Indicateurs de stabilité** entre les deux examens, sans changement de santé :
  - même système prioritaire ;
  - même premier moteur (deux listes vides comptent comme identiques) ;
  - même trio de moteurs (ensembles identiques) ;
  - trio « largement stable » : indice de Jaccard ≥ 0,5, c'est-à-dire au moins 2 sur 3 en
    commun pour deux trios.

  Chaque taux est donné avec son IC 95 % (bootstrap des personnes), au total et par tertile
  d'écart global au premier examen. La distribution du nombre de moteurs est aussi rapportée.

**Table des moteurs actionnables** (fixée maintenant ; références lues en résumé, sauf mention) :

| Marqueur | Sens actionnable | Justification | Référence |
|---|---|---|---|
| Glucose, HbA1c | haut | perte de poids et activité physique réduisent l'incidence du diabète | Knowler 2002, *N Engl J Med*, doi:10.1056/nejmoa012512 |
| TG, cholestérol total | haut | mode de vie et prise en charge lipidique | Miller 2011, déclaration AHA sur les triglycérides, doi:10.1161/cir.0b013e3182160726 (métadonnées seules, pas de résumé) |
| HDL | bas | l'activité physique aérobie augmente modestement le HDL | Kodama 2007, *Arch Intern Med*, doi:10.1001/archinte.167.10.999 |
| CRP | haut | la perte de poids abaisse la CRP | Selvin 2007, *Arch Intern Med*, doi:10.1001/archinte.167.1.31 |
| ALAT, ASAT, GGT | haut | perte de poids (stéatose) et abstinence d'alcool les font baisser | Vilar-Gomez 2015, *Gastroenterology*, doi:10.1053/j.gastro.2015.04.005 ; Kravos 2010, *Alcohol Alcohol*, doi:10.1093/alcalc/agp070 |
| VGM | haut | baisse avec l'abstinence d'alcool | Kravos 2010 |
| Leucocytes | haut | l'arrêt du tabac abaisse les leucocytes | Smith 2021, *Am J Med*, doi:10.1016/j.amjmed.2020.06.014 |
| ACR | haut | contrôle tensionnel et blocage du système rénine-angiotensine (médical) | Vitiello 2026, revue, doi:10.1007/s00210-026-05140-z |

**Non actionnables** :
- ALAT basse et albumine basse : marqueurs de fragilité (décision de l'auteur du projet) ;
- créatinine, PAL, RDW, lymphocytes %, hémoglobine, plaquettes : orientation médicale, pas
  d'action de mode de vie identifiable dans le produit.

### Q1 — prédictions (calage 2001-2002) et règles

| Indicateur (sang seul) | 2001-2002 [IC 95 %] |
|---|---|
| Seuil P95 global ; cardio ; métab ; rénal ; hépat ; inflam (ans) | 5,99 [5,45 ; 6,50] ; 2,69 ; 0,93 ; 4,43 ; 4,95 ; 4,49 |
| Même système prioritaire | 64,2 % [59,5 ; 69,1] |
| Même premier moteur (tous / actionnables) | 62,4 % / 61,1 % |
| Même trio (tous / actionnables) | 27,8 % / 29,4 % |
| Trio largement stable, Jaccard ≥ 0,5 (tous / actionnables) | 82,2 % [78,4 ; 86,1] / 81,4 % [77,6 ; 85,3] |

Modèle complet (partie biologique) : seuil global 5,29 ; même système 72,2 % ; premier moteur
62,9 % / 63,9 % ; trio identique 25,8 % / 32,5 % ; trio largement stable 84,0 % / 81,7 %.
Nombre de moteurs au premier examen (sang seul) : 3 pour 384 personnes sur 388 ; 3 moteurs
actionnables pour 332.

**Règles de lecture.**
- **Compatibilité** : la valeur de 2001-2002 est dans l'IC 95 % de NHANES III (seuils et taux).
- **Règle des 80 %** (validée) : un élément est **affichable** si son taux de stabilité observé en
  NHANES III est ≥ 80 %, et **affichable avec confiance** si la borne basse de l'IC est ≥ 80 %. Elle
  s'applique au système prioritaire, au premier moteur et au trio (critère : largement stable).

### Q2 — définitions

- **Seuils « anormal »** (validés) :

| Marqueur | Seuil |
|---|---|
| Glucose | ≥ 5,6 mmol/L |
| HbA1c | ≥ 5,7 % |
| Cholestérol total | ≥ 5,2 mmol/L |
| HDL | < 1,0 (H) / < 1,3 (F) mmol/L |
| TG | ≥ 1,7 mmol/L |
| ALAT, ASAT | > 40 U/L |
| GGT | > 60 (H) / > 40 (F) U/L |
| PAL | > 120 U/L |
| Albumine | < 35 g/L |
| Créatinine | > 106 (H) / > 89 (F) µmol/L |
| ACR | ≥ 3 mg/mmol |
| CRP | > 3 mg/L |
| Leucocytes | < 4 ou > 10 G/L |
| Lymphocytes | < 20 ou > 40 % |
| RDW | > 14,5 % |
| VGM | < 80 ou > 100 fL |
| Hémoglobine | < 13 (H) / < 12 (F) g/dL |
| Plaquettes | < 150 ou > 400 G/L |

  **Sensibilité** : seuils tirés des données, aux centiles 10 et 90 du développement par sexe,
  du côté ou des côtés de chaque seuil clinique.
- **Second bilan** :
  - remesure complète (toutes les valeurs du second examen) ;
  - remesure sélective : seuls les marqueurs anormaux au premier bilan sont remesurés, les
    autres gardent leur première valeur.
- **Amélioration apparente** : moyenne de (écart₂ − écart₁) chez les personnes ayant au moins un
  marqueur anormal (pour un système, dans ses marqueurs ; pour le global, n'importe lequel) ; une
  valeur négative signifie un rajeunissement. Même calcul chez les 20 % de personnes au plus
  grand écart global au premier bilan (sélection sur le score).
- **Correction principale, marqueur par marqueur** (demandée) : valeur attendue au second bilan
  sans changement réel, exp(μ + ρ (ln x₁ − μ)).
  - ρ est le CCI(A,1) du log du marqueur en 2001-2002 : glucose 0,80 ; HbA1c 0,97 ;
    cholestérol 0,88 ; HDL 0,89 ; TG 0,76 ; ALAT 0,84 ; ASAT 0,74 ; GGT 0,94 ; PAL 0,94 ;
    albumine 0,77 ; créatinine 0,92 ; ACR 0,75 ; CRP 0,82 ; leucocytes 0,78 ; lymphocytes 0,66 ;
    RDW 0,96 ; VGM 0,99 ; hémoglobine 0,92 ; plaquettes 0,89.
  - μ est la moyenne du log dans le développement, même sexe et même tranche d'âge de 10 ans.
  - Changement corrigé : écart₂ observé − écart₂ attendu, les marqueurs non remesurés gardant
    leur valeur.
  - Sensibilité : μ calculé sur le premier examen de l'échantillon testé lui-même.
- **Correction secondaire, au niveau du score** (ajoutée **pendant le calage**, après avoir vu
  qu'en 2001-2002 la correction marqueur par marqueur surcorrige la sélection sur le score) :
  écart₂ attendu = μ_s + ρ_s (écart₁ − μ_s).
  - μ_s est l'écart moyen du développement, même sexe et même tranche d'âge.
  - ρ_s est le CCI(A,1) du score en 2001-2002 ; sang seul : global 0,89, cardio 0,80, métab
    0,95, rénal 0,82, hépat 0,82, inflam 0,89.
  - Elle ne s'applique qu'à la remesure complète.

### Q2 — prédictions (calage 2001-2002, sang seul) et règles

Moyennes de (écart₂ − écart₁) en années, avec n :

| Groupe | n | Complète | Sélective | Corrigée complète (marqueurs) | Corrigée sélective | Corrigée complète (score) |
|---|---|---|---|---|---|---|
| Global, ≥ 1 marqueur anormal | 357 | +0,29 | −0,24 | +0,59 | +0,05 | +0,25 |
| Cardiovasculaire | 271 | +0,10 | +0,03 | +0,34 | +0,17 | +0,07 |
| Métabolique | 91 | −0,13 | −0,20 | +0,01 | −0,05 | −0,06 |
| Rénal | 69 | −0,81 | −0,83 | +0,07 | +0,19 | −0,00 |
| Hépatique | 69 | +0,33 | −0,01 | +0,83 | +0,36 | +0,67 |
| Inflammatoire | 247 | −0,02 | −0,38 | +0,21 | −0,13 | +0,11 |
| Sélection sur le score (20 % les plus « vieux ») | 78 | −0,54 | — | +0,88 | — | +0,42 |

Taux de normalisation spontanée au second examen (marqueurs anormaux au premier) : de 15 %
(HbA1c) à 46 % (leucocytes) ; CRP 20 %, ACR 32 %, glucose 34 %
(`Q2_marqueurs_2001_sang.csv`). Rappel : en 2001-2002, le second examen « vieillit » en moyenne
tout le monde d'environ +0,3 an (décalage systématique), ce qui se mélange à la régression vers la
moyenne.

**Règles de lecture.** Le seuil de référence est le P95 de 2001-2002 du même modèle et du même
score (sang seul : global 5,99 ; cardio 2,69 ; métab 0,93 ; rénal 4,43 ; hépat 4,95 ;
inflam 4,49).
- **Compatibilité** : la moyenne de 2001-2002 est dans l'IC 95 % de NHANES III (complète,
  sélective, chaque groupe).
- **Correction validée**, pour chaque correction : l'IC 95 % du changement corrigé moyen en
  NHANES III est **entièrement dans ±10 % du seuil** (marge d'équivalence), pour le global **et**
  au moins 4 des 5 systèmes.
- **Remesure sélective trompeuse** : son amélioration apparente moyenne (−moyenne de
  écart₂ − écart₁) dépasse 25 % du seuil, pour le global ou pour un système.

Le modèle complet (secondaire) et les sensibilités (seuils par centiles, μ interne) sont rapportés
sans règle de décision.

### Amendement au pré-enregistrement Q1-Q2 (2026-11-10, avant toute analyse sur NHANES III)

Demandé par l'auteur du projet après relecture. Le calage sur 2001-2002 a été relancé avec ces
amendements : nouveau calage `Q1_Q2_predictions.json`, SHA-256 `8c52de01…` ; code `suivi.py`
`7a5010bf…`. Il remplace le précédent (`c6472dd2…`).

**1. Cohérence entre le sens du modèle et le sens clinique** (`suivi.coherence()`, sur la
validation 2007-2010, n = 9 276 ; ce ne sont pas les données de test de Q1-Q2).

Pour chaque marqueur et chaque côté anormal (seuils cliniques de Q2), on calcule chez les
personnes au-delà du seuil la contribution du marqueur au score global et au score de son système
(observé − valeur de référence).

*Règle (pré-enregistrée)* : un marqueur au-delà de son seuil clinique dont la contribution au
score global ou à son système est négative, c'est-à-dire que le modèle le récompense, est
signalé **« à revoir par le médecin »**. Il n'est **jamais présenté comme favorable** et ne compte
jamais comme moteur actionnable.

*Constat*, modèle sang seul, médianes chez les personnes au-delà du seuil (en années) :

| Marqueur, côté anormal | n (% de la validation) | Contribution au global | Contribution au système | % récompensés |
|---|---|---|---|---|
| **ALAT > 40** | 1 020 (11,0 %) | −4,07 | **hépatique −3,98** | 100 % |
| **VGM < 80** | 475 (5,1 %) | −7,45 | −7,75 | 100 % |
| **Leucocytes < 4** | 239 (2,6 %) | −2,63 | −3,72 | 100 % |
| **Lymphocytes > 40 %** | 1 198 (12,9 %) | −1,30 | −1,00 | 100 % |
| **Cholestérol total ≥ 5,2** | 3 918 (42,2 %) | 0,00 | cardiovasculaire −0,20 | 73 % |
| Hémoglobine basse | 671 (7,2 %) | +0,14 | +2,62 | 9 % (modèle complet : global −0,27, 100 %) |
| Créatinine haute | 869 (9,4 %) | +1,01 | +2,48 | 7 % |

Tous les autres côtés anormaux sont aggravants, comme le veut le sens clinique.

- **Contradictions franches** (médiane négative) : ALAT élevée, VGM bas, leucocytes bas,
  lymphocytes % élevés, cholestérol total élevé (effet faible). Dans le modèle complet, s'y ajoute
  l'hémoglobine basse.
- **Personnes signalées** (au moins un marqueur concerné) : 4 724 sur 9 276 (51 %) avec le modèle
  sang seul, dont la plupart par le seul cholestérol ; 5 075 (55 %) avec le modèle complet.
- **Pour un produit**, une ALAT cliniquement élevée **rajeunit le score hépatique d'environ
  4 ans**. Afficher ce score sans la règle reviendrait à présenter comme favorable une anomalie
  hépatique. Ces contradictions viennent de l'apprentissage sur la mortalité : une ALAT basse ou un
  VGM bas accompagnent la fragilité ou la carence (interprétation, section ALAT de `FIABILITE.md`).

Sorties : `coherence_sens_clinique.csv`, `coherence_signalements.json`.

**2. Troisième catégorie de marqueurs.** VGM et leucocytes sont retirés des actionnables et classés
**« à interpréter par le médecin »** : ils ne sont jamais moteurs actionnables. Les taux de
stabilité des moteurs actionnables ont été recalculés (2001-2002, sang seul) :
- même premier moteur actionnable : 58,5 % ;
- même trio actionnable : 28,6 % ;
- trio actionnable largement stable : 74,7 %.

Les autres prédictions de Q1 sont inchangées.

**3. Référence pour les triglycérides.** Miller 2011 (métadonnées seules) est remplacé par
Dattilo et Kris-Etherton 1992, *Am J Clin Nutr*, doi:10.1093/ajcn/56.2.320. Résumé lu :
méta-analyse de 70 études ; la perte de poids par le régime abaisse les TG et le cholestérol total.

**4. Correction au niveau du score** : **validée en secondaire** par l'auteur du projet, déclarée
comme ajoutée après le calage. La même règle d'équivalence (±10 % du seuil) lui est appliquée,
avec le statut secondaire.

**5. Analyse avec groupe contrôle — méthode recommandée** pour évaluer l'effet d'un protocole.
Effet = changement moyen du groupe sélectionné − changement moyen de **toute** la population
remesurée (remesure complète). L'IC 95 % vient d'un bootstrap des personnes, avec le groupe et la
population tirés ensemble. On soustrait ainsi le décalage systématique entre examens, et il ne
reste que la régression vers la moyenne, plus l'effet éventuel de la remesure sélective. Elle est
calculée pour la remesure complète et pour la remesure sélective (dans ce cas, changement
sélectif du groupe moins changement complet de la population).

Prédictions (2001-2002, sang seul), en années :

| Groupe | n | Changement brut (complète) | Contrôle, complète [IC 95 %] | Contrôle, sélective [IC 95 %] |
|---|---|---|---|---|
| Global, ≥ 1 anormal | 357 | +0,29 | −0,04 [−0,13 ; +0,05] | −0,57 [−0,84 ; −0,30] |
| Cardiovasculaire | 271 | +0,10 | −0,13 [−0,22 ; −0,04] | −0,20 [−0,30 ; −0,08] |
| Métabolique | 91 | −0,13 | −0,14 [−0,25 ; −0,02] | −0,21 [−0,30 ; −0,12] |
| Rénal | 69 | −0,81 | −0,59 [−1,13 ; −0,05] | −0,61 [−1,08 ; −0,16] |
| Hépatique | 69 | +0,33 | −0,22 [−0,79 ; +0,42] | −0,56 [−0,95 ; −0,18] |
| Inflammatoire | 247 | −0,02 | −0,22 [−0,40 ; −0,05] | −0,58 [−0,79 ; −0,38] |
| Sélection sur le score (20 %) | 78 | −0,54 | −0,87 [−1,50 ; −0,26] | — |

*Règle* : même compatibilité que les autres indicateurs (valeur de 2001-2002 dans l'IC de NHANES
III). Elle est rapportée en tête de la synthèse de Q2 comme méthode recommandée.

### Résultat — Q1 et Q2 sur NHANES III (2026-11-10)

Exécution du protocole amendé (`c32a6ba`), sans écart. n = 781. Rapports :
`reports/checkup_standard/suivi/Q1_MOTEURS.md` et `Q2_REGRESSION_MOYENNE.md`.

**Q1 (sang seul).**
- Seuils P95 : global 7,14 [6,47 ; 7,54] (prédit 5,99, non compatible) ; cardiovasculaire 2,27 ;
  métabolique 1,11 ; rénal 5,88 ; hépatique 5,19 (compatible) ; inflammatoire 4,79 (compatible).
- Stabilité :
  - système prioritaire 70,4 % ;
  - premier moteur 74,3 % (tous) et 61,1 % (actionnables) ;
  - trio largement stable 89,6 % (tous, **affichable avec confiance**) et 79,9 % (actionnables,
    juste sous la règle des 80 %).
- Les indicateurs actionnables sont compatibles avec 2001-2002 ; les indicateurs « tous » sont
  plus stables que prévu (CRP censurée en NHANES III, interprétation).

**Q2 (sang seul).**
- Analyse avec groupe contrôle : remesure sélective du global −0,42 [−0,63 ; −0,18] ; inflammatoire
  −0,53 ; sélection sur le score −0,88 [−1,39 ; −0,34] ; remesure complète du global −0,02.
- Remesure sélective **trompeuse pour le rénal** (amélioration apparente de 1,15 an, plus de 25 %
  du seuil de 4,43).
- **Aucune correction validée.** La correction marqueur par marqueur échoue pour le global en
  remesure complète (+0,73 [+0,48 ; +0,98], marge ±0,60), et en remesure sélective seuls 3 systèmes
  sur 5 passent. La correction au niveau du score échoue aussi (global +0,61). Les deux
  surcorrigent.

## Suivi, étape 1 — variante « sang seul contrainte » (pré-enregistrement, 2026-11-10)

Demandée par l'auteur du projet après la vérification de cohérence (une ALAT élevée rajeunissait le
score hépatique d'environ 4 ans). Écrit et commité avant toute évaluation sur la validation
2007-2010. Code : `src/aging_clock/contrainte.py`.

**Contrainte clinique.** Une valeur anormale ne doit jamais rendre le score plus favorable.
- Pour chaque marqueur doté d'un seuil (les 19 seuils de Q2) et chaque côté anormal, si la valeur
  est au-delà de la limite de la zone normale, le terme du marqueur dans le prédicteur linéaire de
  **chaque** modèle (global et systèmes) devient le moins favorable des deux : terme à la valeur
  observée, ou terme à la valeur limite.
- Une valeur au-delà de la limite, dans le sens que le modèle récompense, compte donc comme la
  valeur limite. Une valeur au-delà dans le sens aggravant n'est pas modifiée.
- La règle s'applique à tous les marqueurs, ce qui inclut ceux demandés (ALAT, ASAT, VGM,
  leucocytes, lymphocytes, cholestérol, hémoglobine) et tous ceux repérés par la vérification de
  cohérence.
- Pas de réentraînement : mêmes coefficients que le modèle « sang seul ».
- Par construction, l'écart d'âge contraint est toujours ≥ l'écart non contraint.

**Évaluation** sur la validation 2007-2010, mêmes personnes (9 276), pour le global et les 5
systèmes :
- C [IC 95 %] ;
- gain de C par rapport à âge + sexe ;
- HR par écart-type ;
- calibration (rapport observé/prédit, pente) ;
- **différence de C appariée contrainte − non contrainte** (bootstrap, 1 000 tirages, graine 42) ;
- nombre de personnes dont le score change, avec la médiane, le 90ᵉ centile et le maximum du
  changement.

**Règle de décision** (fixée par l'auteur du projet) : on **adopte** la variante contrainte si
elle perd **moins de 0,005 de C sur le score global**, c'est-à-dire si l'estimation ponctuelle de la
différence appariée est > −0,005. L'IC est rapporté.

**Règle de signalement révisée** : « à revoir par le médecin » seulement si la récompense indue
dépasse un **seuil matériel de 1 an sur le score du système** du marqueur. La récompense indue est
l'écart du système avec la valeur observée moins l'écart avec la valeur limite ; le signalement
se déclenche si elle est < −1 an. On calcule le pourcentage de personnes signalées sans et avec
la contrainte ; avec la contrainte, il vaut 0 par construction.

**Prédiction** (développement, apparent, n = 13 903 ;
`reports/checkup_sang_seul/contrainte/prediction_developpement.json`) :
- différence de C : global +0,0001 ; cardiovasculaire −0,0001 ; hépatique +0,0001 ;
  inflammatoire +0,0000 ; métabolique et rénal 0 ;
- écarts modifiés : global 46,6 % des personnes (médiane +0,16 an ; 90ᵉ centile +1,93 ;
  maximum +9,5) ; cardiovasculaire 38,7 % (+0,34) ; hépatique 10,9 % (+0,68 ; 90ᵉ centile +2,0) ;
  inflammatoire 17,3 % (+0,44 ; 90ᵉ centile +3,1) ; métabolique et rénal : aucun.

Si la variante est adoptée, elle devient le modèle principal de Q3 allégée et de Q4. Q1 et Q2
gardent leurs résultats pré-enregistrés ; leur reprise avec la variante contrainte serait une
analyse distincte.

### Résultat — étape 1, variante contrainte (2026-11-10)

Exécution du protocole (`e886322`), sans écart. Validation 2007-2010 : C global contraint 0,8504
[0,839 ; 0,862] contre 0,8496 ; différence appariée **+0,0008 [+0,0001 ; +0,0016]**. Hépatique
+0,0005 ; inflammatoire +0,0002 ; cardiovasculaire −0,0001 ; métabolique et rénal 0. Calibration :
global 0,90 ; pente 0,99. Règle : perte < 0,005 → **variante adoptée** ; elle devient le modèle
principal de Q3 allégée et de Q4.

Écarts modifiés : global 46,0 % des personnes (médiane +0,22 an ; 90ᵉ centile +2,1 ; maximum +8,0) ;
hépatique 11,0 % (+0,72) ; inflammatoire 18,6 % (+0,46 ; 90ᵉ centile +3,4) ; cardiovasculaire 35,7 %
(+0,33).

Signalement avec le seuil matériel de 1 an : 823 personnes (8,9 %) sans contrainte (ALAT 375, VGM
330, lymphocytes 78, leucocytes 59) ; 0 avec contrainte. Rapport :
`reports/checkup_standard/suivi/ETAPE1_CONTRAINTE.md`.

Note ajoutée aux rapports à la demande de l'auteur du projet : la mortalité toutes causes à 10 ans
sous-estime les facteurs de risque cardiovasculaire (lipides, glycémie). Les systèmes cardio et
métab « sang seul » ne doivent pas être présentés comme inutiles.

## Suivi — reprise de Q1 et Q2 avec le modèle « sang seul contraint » (analyse secondaire, pré-enregistrement, 2026-11-10)

Demandée par l'auteur du projet après l'adoption de la variante contrainte (étape 1). Écrit et
commité avant de relancer NHANES III. Code : `src/aging_clock/suivi_contraint.py`.

**Statut.** Analyse **secondaire**. NHANES III a déjà été consulté pour Q1-Q2 avec le modèle non
contraint : l'évaluation **n'est pas aveugle**. Les résultats pré-enregistrés (modèle non
contraint) restent dans les rapports, inchangés.

**Ce qui change** : seulement le modèle. Le modèle « sang seul contraint » est appliqué à chaque
prédiction, y compris aux contributions des moteurs et aux centiles du système prioritaire
(référence : écarts contraints du développement).

**Ce qui ne change pas** : définitions de Q1 et Q2 et leur amendement, table des moteurs
actionnables, seuils « anormal », CCI des marqueurs de 2001-2002, règles de lecture
(compatibilité, règle des 80 %, correction validée à ±10 % du seuil, remesure sélective trompeuse à
25 % du seuil). Le seuil de référence des règles de Q2 est le P95 de 2001-2002 **du modèle
contraint**. Les CCI du score (correction secondaire) sont recalculés sur 2001-2002 avec le modèle
contraint.

**Prédictions (2001-2002, n = 388 ; `Q1_Q2_contraint_predictions.json`).**

| Indicateur | Non contraint (pré-enregistré) | Contraint |
|---|---|---|
| Seuil P95 global [IC 95 %] | 5,99 | 5,97 [5,46 ; 6,57] |
| Seuil P95 cardio ; métab ; rénal ; hépat ; inflam | 2,69 ; 0,93 ; 4,43 ; 4,95 ; 4,49 | 2,61 ; 0,93 ; 4,43 ; 4,95 ; 4,43 |
| Même système prioritaire | 64,2 % | 64,9 % |
| Même premier moteur (tous / actionnables) | 62,4 % / 58,5 % | 62,4 % / 58,2 % |
| Même trio (tous / actionnables) | 27,8 % / 28,6 % | 27,8 % / 28,9 % |
| Trio largement stable (tous / actionnables) | 82,2 % / 74,7 % | 82,5 % / 74,0 % |

Q2, modèle contraint, moyennes de (écart₂ − écart₁) en années :

| Groupe | Complète | Sélective | Corr. complète | Corr. sélective | Corr. score | Contrôle complète | Contrôle sélective |
|---|---|---|---|---|---|---|---|
| Global | +0,28 | −0,31 | +0,70 | +0,10 | +0,24 | −0,05 | −0,64 |
| Cardio | +0,08 | 0,00 | +0,32 | +0,14 | +0,06 | −0,14 | −0,22 |
| Métab | −0,13 | −0,20 | +0,01 | −0,05 | −0,06 | −0,14 | −0,21 |
| Rénal | −0,81 | −0,83 | +0,07 | +0,19 | −0,00 | −0,59 | −0,60 |
| Hépatique | +0,28 | −0,13 | +0,93 | +0,39 | +0,70 | −0,27 | −0,68 |
| Inflam | −0,04 | −0,43 | +0,30 | −0,07 | +0,08 | −0,24 | −0,63 |
| Sélection sur le score | −0,39 | — | +1,13 | — | +0,56 | −0,72 | — |

**Attendu qualitatif** : le modèle contraint change peu les seuils et la stabilité (au plus 1 point
de pourcentage pour les taux, 0,1 an pour les seuils). Les conclusions de Q1 et Q2 ne devraient pas
changer.

### Résultat — reprise de Q1 et Q2 avec le modèle contraint (2026-11-10, non aveugle)

Exécution du protocole (`33cb504`), sans écart. NHANES III, n = 781.
- **Q1** : taux de stabilité inchangés à moins d'un point près (système prioritaire 71,1 % ; trio
  largement stable 89,6 %, affichable avec confiance ; trio actionnable largement stable 79,6 %,
  non affichable). Seuils P95 : global 6,99 [6,64 ; 7,54] (contre 7,14), cardio 2,21, métab 1,11,
  rénal 5,88, hépat 5,14, inflam 4,71. Compatibilité avec 2001-2002 : même profil.
- **Attendu qualitatif** : vérifié pour les taux ; **pas tout à fait pour les seuils** (le global baisse
  de 0,15 an, au-delà des 0,1 an attendus).
- **Q2** : remesure sélective trompeuse pour le rénal (1,15 > 1,11), contrôle sélectif global −0,48
  [−0,69 ; −0,24] ; aucune correction validée (marqueurs : global complète +0,87 ; sélective 3/5
  systèmes ; score : +0,62).
- **Conclusion** : la contrainte ne change aucune conclusion de Q1 ni de Q2. Rapports : section
  « Analyse secondaire » de `Q1_MOTEURS.md` et `Q2_REGRESSION_MOYENNE.md`.

## Suivi, Q3 allégée — urines absentes au second bilan (pré-enregistrement, 2026-11-10)

Demandée par l'auteur du projet : au suivi, seules les urines manquent. Écrit et commité avant de
toucher aux paires de NHANES III et à la validation 2007-2010 pour cette question. Code :
`src/aging_clock/q3.py` ; modèle dédié : `config/panels/checkup_sang_sans_urines.yaml`. Modèle de
référence : « sang seul contraint » (étape 1). Évaluation non aveugle au sens des réserves communes.

**Situation.** Bilan 1 avec ACR, bilan 2 sans ACR. Sur des paires de remesures à environ 2
semaines, il n'y a pas de changement réel : **tout changement affiché est un faux changement**.
Scores étudiés : global et rénal (le rénal sans ACR se réduit à la créatinine).

**Stratégies** (plan validé) :
1. **imputation** : ACR prédite par régression linéaire du log de l'ACR sur les 18 autres
   marqueurs (log pour les marqueurs transformés en log), l'âge et le sexe, ajustée sur le
   développement (R² = 0,165) ; bilan 1 avec l'ACR mesurée ;
2. **marqueurs communs** : ACR mise à la valeur de référence (médiane du développement, même sexe,
   même tranche d'âge) **aux deux bilans** ; le bilan 1 est recalculé ;
3. **modèle dédié** : Cox « sang seul, sans urines » (même pipeline, mêmes hyperparamètres, ACR
   hors modèle), contraint, appliqué **aux deux bilans**.
- Sensibilité, non prévue au plan : **report** de l'ACR du bilan 1. Elle donne le même changement
  que les marqueurs communs : l'ACR entre de façon additive dans le prédicteur et ne change pas
  entre les bilans.
- Référence : **panel complet**, ACR mesurée aux deux bilans.

**Indicateurs** (global et rénal) :
- sur les paires :
  - changement moyen d = écart₂ − écart₁ [IC 95 %] ;
  - P95 de |d| [IC 95 %] et rapport au P95 du panel complet sur les mêmes paires ;
  - **faux changement dû à l'absence d'urines** = d(stratégie) − d(panel complet), moyenne [IC]
    et P95 de sa valeur absolue ;
- pour les stratégies 2 et 3 :
  - écart d'affichage du bilan 1 recalculé sans urines par rapport au bilan 1 complet ;
  - **comparaison mixte** : bilan 1 complet affiché tel quel, bilan 2 avec la stratégie ;
- validation 2007-2010, un seul bilan sans urines :
  - C de la stratégie et différence de C appariée avec le panel complet (bootstrap, 1 000
    tirages) ;
  - biais de l'écart par rapport au panel complet.

**Règles de décision.** Le seuil de référence T est le P95 du panel complet contraint en 2001-2002
(global 5,97 ; rénal 4,43). Une stratégie est **acceptable** pour un score si, à la fois :
- (a) l'IC 95 % du faux changement moyen en NHANES III est entièrement dans ±10 % de T ;
- (b) le P95 de |d| en NHANES III ne dépasse pas 1,10 fois celui du panel complet ;
- (c) la différence de C sur la validation est > −0,005 (estimation ponctuelle).

Si plusieurs stratégies sont acceptables, on retient celle au P95 le plus bas.

Limite connue de (a) : d(panel complet) contient la variation propre de l'ACR entre les deux
examens. Une stratégie sans ACR ne la reproduit pas. La sensibilité « report » sépare les deux
effets.

**Conclusion sur le suivi rénal, fixée à l'avance.**
- Si une stratégie est acceptable pour le rénal, le score rénal est suivi au bilan sans urines
  avec cette stratégie.
- Sinon, le système rénal **n'est suivi qu'aux bilans avec urines**. Entre deux, on affiche le
  dernier score rénal mesuré, daté, et on n'annonce aucun changement rénal.
- Même règle pour le global, sauf qu'en l'absence de stratégie acceptable, le global est donné
  sans comparaison au bilan complet.

**Prédictions (paires 2001-2002, n = 388 ; développement apparent pour C ;
`Q3_predictions.json`).**

| Stratégie | Score | d moyen [IC] | P95 \|d\| [IC] (rapport) | Faux changement moyen [IC] | ΔC dév. | (a) / (b) / (c) |
|---|---|---|---|---|---|---|
| Complet | global | +0,33 [+0,02 ; +0,62] | 5,97 [5,46 ; 6,57] | — | — | — |
| Complet | rénal | −0,23 [−0,44 ; −0,00] | 4,43 [3,96 ; 4,79] | — | — | — |
| Imputation | global | +0,58 | 7,24 (1,21) | +0,25 [+0,06 ; +0,43] | −0,0028 | oui / non / oui |
| Imputation | rénal | +0,14 | 5,96 (1,34) | +0,36 [+0,08 ; +0,62] | −0,0031 | non / non / oui |
| Communs | global | +0,52 | 5,52 (0,92) | +0,19 [+0,04 ; +0,33] | −0,0035 | oui / oui / oui |
| Communs | rénal | +0,04 | 1,04 (0,23) | +0,27 [+0,05 ; +0,47] | −0,0089 | non / oui / non |
| Dédié | global | +0,56 | 5,86 (0,98) | +0,24 [+0,08 ; +0,38] | −0,0027 | oui / oui / oui |
| Dédié | rénal | +0,06 | 1,67 (0,38) | +0,29 [+0,07 ; +0,49] | −0,0083 | non / oui / non |

- Bilan 1 recalculé sans urines (P95 de l'écart d'affichage) : communs, global 4,6 et rénal 6,7 ;
  dédié, global 3,9 et rénal 5,7.
- Comparaison mixte (P95 de |d|) : communs, global 7,0 et rénal 7,0 ; dédié, global 7,5 et rénal
  6,2.

**Prédiction de la conclusion.**
- Rénal : aucune stratégie acceptable, donc le système rénal n'est suivi qu'aux bilans avec urines.
- Global : « marqueurs communs » retenue (P95 5,52), « dédié » également acceptable.
- La comparaison mixte (bilan complet contre bilan sans urines, sans recalcul) produit les plus
  grands faux changements.

### Résultat — Q3 allégée (2026-11-10)

Exécution du protocole (`ca1c2af`), sans écart. Paires NHANES III n = 781 ; validation n = 9 276.
- **Global.** Acceptable : « marqueurs communs » et « modèle dédié ». Avec « marqueurs communs » :
  P95 5,60, soit 0,80 fois le panel complet ; faux changement −0,07 [−0,20 ; +0,07] ; ΔC −0,0039.
  Avec « modèle dédié » : P95 6,01 ; ΔC −0,0027. **Retenue : marqueurs communs.** L'imputation
  échoue sur (a), avec un faux changement de +0,56 [+0,38 ; +0,74].
- **Rénal.** **Aucune stratégie acceptable.**
  - Marqueurs communs : ΔC −0,0108 [−0,014 ; −0,008] ; échec sur (c).
  - Modèle dédié : ΔC −0,0102 ; échec sur (c).
  - Imputation : faux changement +0,81 et rapport 1,18 ; échec sur (a) et (b).
  - Application de la conclusion fixée à l'avance : le système rénal n'est suivi qu'aux bilans
    avec urines.
- **Comparaison mixte** (bilan 1 complet, bilan 2 sans urines, sans recalcul) : P95 7,3 (global)
  et 7,2 (rénal) avec les marqueurs communs ; avec le modèle dédié, d moyen +0,92 (global).
- **Prédictions.** Conclusion bien prédite. Le rénal échoue sur (c) seul, et non sur (a) et (c)
  comme prévu. Le biais de l'imputation est plus fort que prévu (+0,56 contre +0,25).
- Rapport : `reports/checkup_standard/suivi/Q3_URINES.md`.

## Suivi, Q4 — agrégation en une note globale (pré-enregistrement, 2026-11-10)

Plan validé par l'auteur du projet. Écrit et commité avant toute évaluation sur la validation
2007-2010 et sur les paires de NHANES III pour cette question. Code : `src/aging_clock/q4.py`.
Modèle : « sang seul contraint ». Évaluation non aveugle au sens des réserves communes.

**Options** (toutes en années d'écart d'âge) :
- **global** : score global du modèle (référence) ;
- **moyenne** : moyenne des 5 écarts de système ;
- **Cox** : moyenne pondérée des 5 écarts. Poids = coefficients d'un Cox âge + sexe + 5 écarts
  ajusté sur le développement, normalisés à une somme de 1 : cardio 0,175 ; métab 0,160 ;
  rénal 0,210 ; hépat 0,212 ; inflam 0,243 ;
- **pire système** : écart du système prioritaire (centile standardisé le plus élevé, comme en Q1) ;
- **hybride** : moyenne + λ × (pire − moyenne). λ est choisi par validation croisée à 5 plis sur le
  développement, dans {0 ; 0,1 ; … ; 1 ; 1,5 ; 2}, en maximisant le C du Cox âge + sexe + agrégat.
  Résultat : **λ = 0,1**, avec un C de CV de 0,8466 pour λ = 0 comme pour λ = 0,1. Le C baisse
  ensuite de façon monotone.

Chaque agrégat entre dans un Cox âge + sexe + agrégat ajusté sur le développement. Ce modèle donne
le risque à 10 ans.

**Mesures.**
- Validation 2007-2010 :
  - C [IC 95 %] ;
  - différence de C appariée avec l'option « global » (bootstrap, 1 000 tirages) ;
  - calibration (rapport observé/prédit, pente).
- Fiabilité sur les paires de NHANES III :
  - CCI(A,1) de l'agrégat ;
  - P95 de |d| ;
  - P95 rapporté à l'écart-type entre personnes du développement.
- **Cas « un système très défavorable, tout le reste excellent »** : un seul système au-dessus de
  son 90ᵉ centile standardisé, tous les autres sous leur médiane. Dans ce sous-groupe de la
  validation, on compare le risque observé à 10 ans (Kaplan-Meier) au risque prédit moyen de chaque
  option, par le rapport O/E et son IC (IC de Kaplan-Meier rapporté au risque prédit moyen).

**Règles de décision.**
- R1, discrimination : une option est écartée si sa différence de C avec « global » est < −0,005
  (estimation ponctuelle), comme à l'étape 1.
- R2, fiabilité : une option est écartée si son CCI en NHANES III est inférieur de plus de 0,02 à
  celui de « global ».
- R3, cas d'un seul système très défavorable : on dit que « global » **masque** un système
  défavorable si la borne basse de l'IC de son O/E dans le sous-groupe est > 1.
  - Si « global » masque et qu'une option non écartée par R1-R2 a un IC d'O/E contenant 1, on
    recommande cette option (la plus fiable si plusieurs).
  - Sinon, on **garde « global »**. Une autre option n'est pas adoptée si elle n'apporte rien sur
    R3.

**Prédictions (développement, apparent ; fiabilité sur 2001-2002 ; `Q4_predictions.json`).**

| Option | C dév. | ΔC vs global | CCI 2001-02 | P95 \|d\| (ans) | P95 / ET | O/E cas un système [IC] |
|---|---|---|---|---|---|---|
| Global | 0,848 | — | 0,891 | 5,97 | 0,89 | 1,13 [0,71 ; 1,78] |
| Moyenne | 0,847 | −0,0015 | 0,901 | 1,70 | 0,84 | 1,15 [0,73 ; 1,81] |
| Cox | 0,847 | −0,0014 | 0,903 | 1,81 | 0,83 | 1,16 [0,73 ; 1,83] |
| Pire système | 0,840 | **−0,0081** | 0,809 | 4,47 | 1,12 | 0,70 [0,44 ; 1,10] |
| Hybride (λ = 0,1) | 0,847 | −0,0015 | 0,897 | 1,79 | 0,84 | 1,05 [0,66 ; 1,66] |

- Calibration : O/E de 1,00 à 1,01 et pente de 1,00 pour toutes les options (apparent).
- Cas d'un seul système défavorable (développement) : 257 personnes, 42 décès ; le système en
  cause est le cardio dans 92 cas.
  - Le score global moyen de ce sous-groupe est de **−4,4 ans** : le score global dit « plus
    jeune » alors qu'un système est au-dessus de son 90ᵉ centile.
  - Le risque observé (6,6 %) est un peu au-dessus du risque prédit (5,8 %), mais l'IC est large.
- **Prédiction de la conclusion.**
  - Le pire système est écarté (R1, et R2 avec un CCI inférieur de 0,08).
  - La moyenne, le Cox et l'hybride passent R1 et R2.
  - « Global » ne masque pas le système défavorable au sens de R3 (borne basse 0,71). On **garde
    « global »**.
  - Le pire système doit s'afficher à côté du score global, pas à sa place.

### Résultat — Q4 (2026-11-10)

Exécution du protocole (`585f211`), sans écart.

Validation (n = 9 276), C et différence avec « global » :
- global : C 0,850 ;
- moyenne : ΔC −0,0029 [−0,0041 ; −0,0017] ;
- Cox : ΔC −0,0025 ;
- hybride (λ = 0,1) : ΔC −0,0027 ;
- pire système : ΔC **−0,0119** [−0,0154 ; −0,0086].

Fiabilité sur les paires de NHANES III, en CCI :
- global 0,873 ;
- moyenne 0,881 ;
- Cox 0,881 ;
- hybride 0,882 ;
- pire système 0,818.

Cas d'un seul système défavorable : 142 personnes, 12 décès. O/E du global 1,19 [0,67 ; 2,10]. La
note globale moyenne de ce groupe est de −4,9 ans.

Application des règles :
- R1 et R2 écartent le pire système ;
- R3 : le global ne masque pas le système défavorable ;
- **on garde le score global**, avec le système défavorable affiché à côté.

Conclusion prédite correctement. Rapport : `reports/checkup_standard/suivi/Q4_AGREGATION.md`.

## Gel des analyses de la piste « suivi » (2026-11-10)

À la demande de l'auteur du projet, après Q4 : les analyses de la piste « suivi » sont **gelées**.
- Synthèse : `reports/checkup_standard/suivi/SYNTHESE.md`.
- Q5 (marqueurs manquants dans un système) reste en attente.
- Toute nouvelle analyse demandera une levée du gel datée ici, et un pré-enregistrement.

### Erratum — Q4 (2026-11-10)

Arrondi corrigé : la note globale moyenne du sous-groupe « un seul système très défavorable » vaut
−4,848 ans (`Q4_resultats.json`), soit **−4,8 ans** et non −4,9 comme écrit dans le résultat de Q4,
`Q4_AGREGATION.md` et `SYNTHESE.md`. Aucune conclusion ne change.

## Programme « panel » : comportement des biomarqueurs d'un check-up (2026-11-10)

**Levée du gel.** L'auteur du projet lève le gel des analyses pour ce seul programme (branche
`panel`, créée depuis `suivi`). La piste « suivi » reste gelée.

**Nature.** Programme de recherche sur le comportement des biomarqueurs et des populations,
pas un produit. Contexte générique :
- bilan large au départ, puis un panel de suivi tous les 6 mois ;
- ni heure ni jeûne enregistrés ;
- plusieurs laboratoires ;
- adultes surtout de 30 à 55 ans, plus favorisés et en meilleure santé que la moyenne, dont des
  athlètes.

Aucune entreprise n'est nommée. La correspondance avec un panel précis reste hors du dépôt.

**Inventaire** (étape 1, sans analyse de valeurs) :
- 78 marqueurs mesurés et 21 indices dérivés ;
- 67 marqueurs présents dans NHANES 1999-2018 avec mortalité, 51 avec une remesure en 2001-2002,
  54 dans NHANES III (examen principal et second examen) ;
- 9 marqueurs absents de toutes les sources.

**Questions, dans l'ordre validé** :
1. Q1 : changement détectable à 6 mois ;
2. Q4 : normalisation spontanée ;
3. Q2 : jeûne et heure du prélèvement ;
4. Q5 : changements de méthode de laboratoire ;
5. Q3 : populations particulières.

Q6 (zones fondées sur le risque) sera décidée après Q3.

### Décisions communes (validées par l'auteur du projet)

- **D1, seuils « usuels ».** Une table, chaque ligne indiquant **son type et sa source lue** :
  - **seuil de décision clinique** quand il existe (glycémie, HbA1c, lipides, hs-CRP, DFGe, ACR,
    vitamine D) : recommandations européennes de préférence (ESC/EAS pour les lipides), sinon
    internationales (ADA, OMS, KDIGO). Pour la vitamine D, le seuil est débattu (20 ou 30 ng/mL) :
    analyse de sensibilité ;
  - **intervalle de référence statistique** sinon : intervalles harmonisés nordiques (NORIP), ou à
    défaut une autre source européenne publiée.

  La distinction « convention statistique » contre « seuil fondé sur le risque » apparaît dans
  tous les rapports. La table est figée dans le pré-enregistrement de Q4.
- **D2, population.** Adultes de 20 à 79 ans, sans les femmes enceintes. Les 30-55 ans sont
  rapportés en plus pour Q1, et en analyse principale pour Q3.
- **D3, poids d'enquête.** Pondéré pour les descriptions de population ; non pondéré pour la
  variabilité et les comparaisons internes.
- **D4, échelle.** Log pour les marqueurs strictement positifs ; règle pour les valeurs nulles
  ci-dessous.
- **D5, horizon.** 6 mois. Tout chiffre tiré des remesures à 2 semaines porte le statut
  « borne basse ».
- **D6, littérature.**
  - Ne citer que ce qui a été ouvert, en précisant texte complet ou résumé.
  - Écrire « rien trouvé avec ces requêtes ».

## Programme « panel », Q1 : changement détectable à 6 mois (pré-enregistrement, 2026-11-10)

Écrit et commité avant tout calcul sur les remesures. Code prévu : `src/aging_clock/panel/`.
Rapport : `reports/panel/Q1_CHANGEMENT_DETECTABLE.md`.

### Données

- **Remesures NHANES 2001-2002.** Adultes de 20 à 79 ans, non enceintes, avec une valeur aux deux
  examens (fichiers `*_2_B`, délai médian d'environ 2 semaines).
- **Remesures NHANES III.** Mêmes critères (fichier `labse`).

Les deux jeux sont analysés **séparément**, sans mise en commun : le second sert de réplication.

Marqueurs : ceux de l'inventaire présents dans au moins un jeu de remesures (environ 40 du suivi
et 11 du départ), plus les indices dérivés calculables sur les paires. Unités SI. Mêmes plages de
plausibilité que le projet pour les marqueurs déjà connus ; pour les autres, on exclut seulement
les codes de valeur manquante.

### Valeurs nulles, négatives ou censurées (D4)

- **Échelle additive** (unités, pas %) pour les marqueurs qui peuvent valoir 0 ou dont plus de
  1 % des valeurs sont au plancher de résolution : basophiles et éosinophiles (% et nombre), et
  monocytes en nombre s'ils remplissent le critère. Le changement détectable y est donné en unités.
- **Valeurs sous la limite de détection.** Remplacées par la valeur publiée par NHANES (limite / √2).
  La part de valeurs censurées est rapportée. Au-delà de 20 % de valeurs censurées dans un jeu,
  le résultat est marqué « non interprétable » pour ce jeu (cas attendu : CRP dans NHANES III).
- **Indices qui peuvent être négatifs ou nuls** : sur l'échelle additive (cas attendu : indice
  athérogène, déjà en log). Les autres indices dérivés (HOMA-IR, TyG, FIB-4, NLR, SII, rapports)
  sont sur l'échelle log.

### Indicateurs

Pour chaque marqueur et chaque jeu de remesures, avec $d = \ln x_2 - \ln x_1$ :
- **CV observé** $CV_{obs} = \sqrt{e^{\mathrm{Var}(d)/2}-1}$, version classique et version robuste
  (écart absolu médian × 1,4826) ;
- **décalage moyen** entre examens (moyenne de $d$) ;
- **changement détectable empirique** : P95 de $|d - \bar d|$, exprimé en % (hausse $e^{q}-1$,
  baisse $1-e^{-q}$) ;
- IC 95 % par bootstrap des personnes (2 000 tirages, graine 2026).

Rapportés pour tous les adultes et pour les **30-55 ans**.

### Variabilité à 6 mois

- **CV_I,CT** : CV_I de la méta-analyse EFLM (consultée le 2026-11-10). On vérifie, en lisant les
  études incluses, qu'il vient surtout d'études courtes.
- **CV_I,LT** : études BIVAC de la base EFLM, retenues si elles remplissent toutes ces conditions :
  - adultes en bonne santé ;
  - durée totale de prélèvement ≥ 6 mois ;
  - note BIVAC A ou B.

  S'il y en a plusieurs, on prend la médiane de leurs CV_I. S'il n'y en a aucune, CV_I,LT est
  « non disponible ».
- **Combinaison**, sur l'échelle log : $CV_{6m}^2 = CV_{obs}^2 + \max(0,\ CV_{I,LT}^2 - CV_{I,CT}^2)$.
  - Analyse principale : CV_obs de NHANES III (le plus grand échantillon).
  - Sensibilité : CV_obs de 2001-2002, et version robuste.
- **Statut** de chaque marqueur :
  - « extrapolé à 6 mois » si CV_I,LT existe ;
  - « borne basse (2 semaines) » sinon ;
  - « EFLM seul » pour un marqueur sans remesure, avec $\sqrt{CV_A^2 + CV_{I,LT\ ou\ CT}^2}$.
    CV_A vient des fiches de contrôle qualité NHANES, sinon de la spécification EFLM
    (0,5 × CV_I) ;
  - « non disponible » sans aucune source.
- **Changement détectable à 6 mois** (2 mesures, 95 %) : hausse $e^{1{,}96\sqrt2\,\sigma}-1$,
  baisse $1-e^{-1{,}96\sqrt2\,\sigma}$, avec $\sigma = \sqrt{\ln(1+CV_{6m}^2)}$.

### Effets d'interventions

Interventions et marqueurs, fixés à l'avance :

| Intervention | Marqueurs |
|---|---|
| Activité physique (aérobie, résistance) | HbA1c, glycémie, insuline ou HOMA-IR, TG, HDL, LDL, cholestérol total, CRP, ALAT |
| Alimentation de type méditerranéen | LDL, cholestérol total, TG, HDL, CRP, glycémie, HbA1c |
| Perte de poids | TG, HDL, LDL, ALAT, GGT, insuline, glycémie, HbA1c, CRP, acide urique |
| Réduction de l'alcool | GGT, HDL, TG, VGM |
| Supplémentation en vitamine D | 25-OH vitamine D |
| Supplémentation en oméga-3 | TG |
| Supplémentation en B12 ou folates | B12, folates, homocystéine |
| Supplémentation en fer | ferritine, hémoglobine |

**Recherche** : PubMed, requêtes « `<intervention>` AND `<marqueur>` AND meta-analysis AND
randomized ». Pour chaque couple, on retient la méta-analyse d'essais randomisés chez l'adulte la
plus récente et la plus large qui a été **ouverte** (texte complet ou résumé, précisé).

**Extraction** : effet moyen et IC, converti en % de la valeur de départ (moyenne de départ de la
méta-analyse, ou à défaut la médiane NHANES des 30-55 ans), durée et dose.

**Ratio** = |effet| / changement détectable à 6 mois, du côté de l'effet (hausse ou baisse) :

| Ratio | Conclusion |
|---|---|
| ≥ 1 | un effet moyen est **détectable chez une personne** |
| 0,5 à 1 | **limite** |
| < 0,5 | **visible seulement en moyenne de groupe** |

La règle s'applique au changement détectable principal, avec en sensibilité le changement
empirique.

### Ce que le rapport doit dire explicitement (demandé par l'auteur du projet)

- La **variabilité entre laboratoires n'est pas incluse** dans le changement détectable : elle
  relève de Q5.
- Les effets des méta-analyses sont des **effets moyens**. Ils ne disent rien de la variabilité de
  la réponse d'une personne à l'autre.
- Remesures à 2 semaines ; NHANES est américain et ses laboratoires sont centralisés.

### Prédictions

Fichier `private/panel/Q1_predictions_eflm.csv` (hors dépôt, licence EFLM ; SHA-256
`d65fabbc89b0465cfdd4b0267f025d859c125fa279ba0efd11cc2615890c168c`). Pour 67 marqueurs, il donne
le CV attendu à 2 semaines, $\sqrt{CV_I^2 + (0{,}5\,CV_I)^2}$, avec le CV_I de la méta-analyse EFLM.

1. **Directionnelle** (d'après le projet précédent, où l'EFLM sous-estimait presque tous les CV
   observés) : dans NHANES III, le CV observé classique **dépasse** le CV attendu pour au moins
   deux tiers des marqueurs remesurés.
2. **Queues épaisses** : pour au moins la moitié des marqueurs, le changement détectable
   empirique dépasse de plus de 10 % celui qu'on déduirait du CV robuste.
3. **Réplication** : pour au moins deux tiers des marqueurs présents dans les deux jeux, les CV
   observés de 2001-2002 et de NHANES III diffèrent de moins d'un facteur 1,5.
4. **Interventions** (attendu qualitatif) :
   - ratio ≥ 1 pour la 25-OH vitamine D sous supplémentation, et pour les TG sous oméga-3 à forte
     dose ;
   - ratio < 0,5 pour la plupart des effets de l'activité physique sur les lipides et l'HbA1c.

Ces prédictions sont vérifiées et rapportées ; elles ne conditionnent aucune décision.

### Résultat — programme « panel », Q1 (2026-11-10)

Exécution du protocole (`76c3962`). Rapport : `reports/panel/Q1_CHANGEMENT_DETECTABLE.md`. Les CV_I
EFLM bruts restent hors du dépôt (`private/panel/`), à la demande de l'auteur du projet (licence) ;
les fichiers publics ne donnent que les résultats dérivés.

**Variabilité.** 70 marqueurs et indices sur les remesures (NHANES III jusqu'à 1 821 adultes ;
2001-2002, environ 410).
- Prédiction 1 vérifiée : le CV observé dépasse le CV attendu d'après l'EFLM pour 35 marqueurs sur
  42 (83 %).
- Prédiction 2 vérifiée : queues épaisses pour 80 % des marqueurs.
- Prédiction 3 vérifiée : réplication entre les deux jeux pour 93 % des marqueurs.

**CV_I à long terme EFLM (note A/B, ≥ 6 mois).** Disponible seulement pour la numération, l'ALAT,
l'ASAT, les bicarbonates, les plaquettes et la TSH. 30 jeux sur 572 jeux de 6 mois ou plus ; la
plupart des études longues ont la note C. Ailleurs, le changement détectable est une borne basse.

**Changement détectable à 6 mois** (hausse / baisse, 20-79 ans) :
- VGM ±3 % ; hémoglobine +10/−9 % ; HbA1c +10/−9 % ;
- cholestérol total +26/−21 % ; HDL +43/−30 % ; TG +111/−53 % ;
- ALAT +181/−64 % (extrapolé à 6 mois) ; CRP +351/−78 %.

**Interventions** (25 couples, méta-analyses lues) :
- 2 détectables chez une personne : vitamine D3 25 µg/j (ratio 1,8) ; HbA1c sous activité
  physique structurée chez des diabétiques (1,3) ;
- 3 limites : ALAT sous alimentation méditerranéenne, TG sous oméga-3 2 g/j, homocystéine sous
  acide folique ;
- 20 visibles seulement en moyenne de groupe.

Prédiction 4 en partie fausse : oméga-3 à 0,7 et non ≥ 1 ; HbA1c sous activité physique à 1,3 et
non < 0,5.

**Écarts.**
- CV_A des marqueurs sans remesure : spécification EFLM (0,5 × CV_I) pour tous ; les fiches NHANES
  n'ont pas été lues.
- Filtre de matrice ajouté (sérum, plasma, sang total) pour le CV_I à long terme.
- Sensibilité non pré-enregistrée incluant les études EFLM de note C.

### Analyse secondaire — Q1 (2026-11-11, déclarée après les résultats)

À la demande de l'auteur du projet, sans nouvelle donnée NHANES (`q1_secondaire.py`,
`Q1_secondaire_moyenner.csv`) :
1. **Population.** Elle est indiquée pour chaque couple.
   - HbA1c sous activité physique chez des non-diabétiques : rien trouvé avec ces requêtes.
   - L'effet de 1,3 vient de diabétiques.
2. **Références.**
   - Statine (atorvastatine 10 mg/j) : LDL −40 %, ratio 1,25 (Law 2003).
   - Perte de poids de 5 % chez des obèses non diabétiques (Magkos 2016, essai unique,
     n = 19 contre 14) : TG −38 % (ratio 0,72) ; glycémie −4 % (0,18) ; ALAT −17 % (0,26) ; HDL et
     CRP inchangés.
   - Aucune méta-analyse de perte de poids de 5-10 % sans médicament chez des non-diabétiques n'a
     été trouvée avec ces requêtes.
3. **Nombre de mesures pour atteindre un ratio de 1.**
   - Une seule mesure suffit pour la vitamine D, les statines et l'HbA1c chez des diabétiques.
   - Environ 3 mesures de part et d'autre pour les TG (oméga-3, perte de poids) et l'homocystéine.
   - Des dizaines pour les lipides et la glycémie sous activité physique ou alimentation.
   - Impossible par des prélèvements rapprochés pour l'ALAT et l'hémoglobine (variation à long
     terme supérieure à l'effet).

### Complément Q1 (2026-11-11, analyse secondaire)

Perte de poids : méta-analyses ajoutées sur un scénario de 7 kg (5-10 %).
- Lipides : Hasan 2020 (73 ECR, surpoids ou obésité ; par kg après une intervention sur le mode de
  vie : TG −4,0, LDL −1,28, HDL +0,46 mg/dL).
- ALAT : Koutoukidis 2021.

Ratios : TG 0,45, LDL 0,23, HDL 0,16, ALAT 0,60. Magkos 2016 est gardé en appui, comme petit
essai unique.

## Programme « panel » : table D1 figée, et pré-enregistrement de Q4 (2026-11-11)

Décisions de l'auteur du projet (2026-11-11) :
- **Intervalles statistiques** : calculés sur NHANES selon le CLSI EP28. NORIP sert seulement de
  comparaison, si les articles sont fournis. Aucune page de laboratoire privé.
- **Seuils cliniques** : sources européennes ou OMS accessibles. Quand les organismes divergent,
  on enregistre les deux seuils et Q4 tourne avec chacun. Le désaccord est présenté comme un
  résultat (exemple de seuil conventionnel).
- **Marqueurs sans seuil lu** : exclus de l'analyse principale, listés avec leur raison.

### Table D1 (figée)

**Seuils de décision clinique (type R)** : `reports/panel/D1_seuils_cliniques.csv`.
- Glycémie à jeun : ≥ 6,1 mmol/L (OMS 2006 ; ESC 2023 diabète, tableau 6) **et** ≥ 5,6 mmol/L
  (ADA, rapporté par ESC 2023).
- HbA1c : ≥ 6,0 % (OMS, rapporté par ESC 2023) **et** ≥ 5,7 % (ADA, rapporté par ESC 2023).
- LDL : ≥ 3,0 mmol/L, objectif du risque faible (ESC/EAS 2019).
- Cholestérol non-HDL : ≥ 3,4 mmol/L, objectif secondaire du risque modéré, faute d'objectif pour
  le risque faible (ESC/EAS 2019).
- TG, à jeun et non à jeun : ≥ 1,7 mmol/L (ESC/EAS 2019).
- DFGe : < 60 (KDIGO 2024). Rapport albumine/créatinine : ≥ 3 mg/mmol, soit 30 mg/g (KDIGO 2024).
- 25-OH vitamine D : < 20 ng/mL, avec < 30 ng/mL en sensibilité (Endocrine Society 2011). Le
  seuil est débattu.

Sources lues : ESC 2023 et ESC/EAS 2019 en texte intégral (extraits exacts), OMS 2006 et KDIGO
2024 en PDF, Endocrine Society 2011 en texte intégral.

**Intervalles de référence statistiques (type S)** : `reports/panel/D1_intervalles_statistiques.csv`,
code `src/aging_clock/panel/intervalles.py` (CLSI EP28).
- **Population de référence** : NHANES 2003-2010, cycles distincts des jeux de test de Q4. Adultes
  de 20 à 79 ans, avec les critères suivants :
  - non-fumeurs (cotinine < 3 ng/mL, Benowitz 2009) ;
  - IMC de 18,5 à 30, femmes non enceintes ;
  - sans diabète, maladie cardiovasculaire, hépatique, rénale ni cancer déclarés ;
  - sans traitement antidiabétique, antihypertenseur ni hypolipémiant déclaré.

  Résultat : 4 769 adultes.
- **Méthode** : 2,5ᵉ et 97,5ᵉ centiles non paramétriques, par sexe, avec un IC 90 % des bornes par
  bootstrap.
- **Partition par âge** (20-39, 40-59, 60-79 ans) : si une tranche a moins de 1 % ou plus de 5 % de
  ses valeurs au-delà d'une borne commune, et si chaque tranche compte au moins 120 personnes.
  L'idée vient de Harris et Boyd (décrite par Lahti 2004) ; les seuils de 1 % et 5 % sont choisis
  ici.
- **Cycles** : 2003-2010, sauf B12 et folates érythrocytaires (2003-2006), à cause de changements de
  méthode documentés.
- **Limite connue** : les jeux de test (2001-2002, NHANES III) ont d'autres méthodes de laboratoire.
  Les valeurs entières (électrolytes) font déclencher la partition par âge à cause des ex aequo.
- Ferritine, capacité de fixation et saturation : femmes seulement (sous-échantillon NHANES).
- La hs-CRP n'a pas de seuil de risque lu (AHA/CDC 2003 inaccessible) : intervalle statistique
  seulement.

**Exclus de l'analyse principale de Q4**, avec leur raison (`D1_population_reference.json`) :
- Lp(a), ApoA1, sélénium, iode urinaire ;
- LH, FSH, PSA ;
- concentrations urinaires brutes ;
- glucose sérique non à jeun ;
- indices dérivés sans seuil lu.

### Q4 : protocole

Données, indicateurs et règles : voir le brouillon validé, avec ces précisions.
- **Paires** : celles de Q1 (2001-2002 et NHANES III), analysées séparément.
- **Anormal** :
  - type R : au-delà du seuil (≥ pour un seuil haut, < pour un seuil bas) ;
  - type S : hors de l'intervalle du sexe et de la tranche d'âge.
- **Indicateurs** :
  - taux de normalisation au second examen, avec IC de Wilson ;
  - même taux pour les anomalies limites (à moins d'un changement détectable empirique de Q1 au-delà
    du seuil) et pour les anomalies nettes ;
  - taux d'apparition ;
  - normalisation attendue sous le seul bruit (modèle binormal conditionnel, échelle log si
    possible).
- **Prédiction** : les taux de 2001-2002 (`Q4_normalisation_2001.csv`, empreintes dans
  `Q4_predictions_2001.json`). Ils sont compatibles s'ils tombent dans l'IC de NHANES III.
- **Règles** (calculées sur le plus petit des deux taux quand les deux jeux ont au moins
  20 anomalies) :

  | Normalisation | Conclusion |
  |---|---|
  | ≥ 30 % | confirmer avant de signaler |
  | ≥ 50 % | anomalie isolée peu informative |

  - Avec un seul jeu disponible, la conclusion porte le statut « un seul jeu ».
  - Avec moins de 20 anomalies dans un jeu, aucune conclusion pour ce jeu.
- **Glycémie et HbA1c** : Q4 tourne avec les seuils OMS et ADA. Le désaccord est rapporté comme un
  résultat.

**Aperçu des prédictions (2001-2002)** :
- normalisation ≥ 50 % pour bilirubine, calcium, chlorure, bicarbonates, potassium, protéines,
  lymphocytes, neutrophiles, sodium, phosphate, fer, MPV, HDL, homocystéine, leucocytes,
  éosinophiles et urée ;
- 30 à 50 % pour la plupart des enzymes, la CRP, la créatinine, l'hématocrite et le LDL ;
- < 30 % pour la ferritine, le VGM, la TCMH, les folates, l'HbA1c (OMS 10 %, ADA 16 %), le non-HDL
  (13 %), le DFGe (12 %), la vitamine D (11 %), la glycémie OMS (19 %) et l'ACR (28 %).

**Réserves.**
- Remesures à 2 semaines.
- Évaluation non aveugle pour les 19 marqueurs déjà vus dans la piste « suivi ».
- CRP de NHANES III censurée.
- Les intervalles statistiques classent anormaux, par construction, 5 % des personnes en bonne
  santé de la population de référence.

### Résultat — programme « panel », Q4 (2026-11-11)

Exécution du protocole (`ce82907`). Rapport : `reports/panel/Q4_NORMALISATION.md`. 57 couples
marqueur-seuil.

**Conclusions de la règle.**
- Anomalie isolée peu informative (≥ 50 %) : 14 couples, dont 9 dans les deux jeux (électrolytes,
  protéines, phosphate, urée, fer).
- Confirmer avant de signaler (≥ 30 %) : 18, dont 13 dans les deux jeux.
- Normalisation < 30 % : 25, dont 18 dans les deux jeux. Tous les seuils de risque en font partie.

**Prédiction** (taux de 2001-2002 dans l'IC de NHANES III) : 13 couples sur 40.

**Faits saillants.**
- La normalisation observée est à moins de 10 points de celle attendue sous le seul bruit pour
  81 % des couples dans NHANES III.
- Anomalies limites : 41 % de normalisation ; anomalies nettes : 8 % (médianes).
- Désaccord OMS / ADA : part d'anormaux de 17 % contre 30 % (glycémie) et de 18 % contre 32 %
  (HbA1c) dans NHANES III.
- Intervalles statistiques non transposables à NHANES III pour 11 marqueurs (plus de 15 %
  d'anormaux).

**Écart.** La signalisation des intervalles non transposables (plus de 15 % d'anormaux) n'était pas
pré-enregistrée ; c'est une aide à la lecture.

### Faiblesse du pré-enregistrement de Q4, et règle pour la suite (2026-11-11)

Le pré-enregistrement de Q4 (`ce82907`) renvoyait, pour le détail des indicateurs, à un brouillon
non versionné (`private/panel/Q4_prereg_brouillon.md`). Son contenu ne peut donc pas être vérifié
depuis le dépôt. Les indicateurs calculés sont ceux décrits dans le rapport et dans le résultat de
Q4, mais rien ne prouve qu'ils n'ont pas changé entre le brouillon et l'analyse.

**Règle (auteur du projet), applicable dès Q2** : chaque pré-enregistrement est complet au moment du
commit, sans renvoi à un document non versionné. Un détail qui doit rester privé est représenté par
son empreinte SHA-256 dans le pré-enregistrement.

CRP : les seuils AHA/CDC 2003 seront ajoutés si l'auteur du projet fournit le texte ; en attendant,
l'intervalle statistique suffit.

## Programme « panel », Q2 : jeûne et heure du prélèvement (pré-enregistrement, 2026-11-11)

Texte complet, validé par l'auteur du projet avec ses modifications. Écrit avant toute lecture de
valeurs de marqueurs pour cette question. Code : `src/aging_clock/panel/q2.py`. Rapport :
`reports/panel/Q2_JEUNE_HEURE.md`.

**Question.** De combien le jeûne, puis l'heure du prélèvement, déplacent-ils chaque marqueur et
indice, par rapport au changement détectable à 6 mois de Q1 ? Quels marqueurs exigent un
prélèvement à jeun ou un horaire fixe pour qu'un suivi ait un sens ? Analyse principale : le
**jeûne**, plus important dans la situation visée (prélèvements surtout le matin, jeûne non
contrôlé). L'heure vient en second.

### Données et faisabilité

Comptages faits avant l'analyse, sans aucune valeur de marqueur.

**NHANES III, paires des deux examens** (fichiers `lab` et `labse`). Adultes de 20 à 79 ans, hors
femmes enceintes (`MAPF12R`) : 2 008 personnes.
- Durée de jeûne (`PHPFAST`, `PHRFAST`, en heures) connue aux deux examens pour **1 206** personnes.
- Croisement des classes de jeûne (examen 1 en lignes, examen 2 en colonnes : < 4 h, 4-8 h,
  ≥ 8 h) : 29, 16, 20 / 21, 247, 42 / 28, 70, 733.
- **48 personnes** sont non à jeun (< 4 h) à un examen et à jeun (≥ 8 h) à l'autre.
- La séance (`MXPSESSR`, `MXRSESSR`) est identique aux deux examens pour tous.
- L'heure exacte du prélèvement (`PHPBEST`, `PHRBEST`, au format HH:MM) est connue aux deux examens
  pour 1 207 personnes ; 51 ont plus de 2 h d'écart.

**NHANES 1999-2018, examen principal.** Durée de jeûne `PHAFSTHR` et séance `PHDSESN` (1 matin,
2 après-midi, 3 soir), dans les fichiers PH, PH_B, PH_C et FASTQX_D à J. Covariables :
- `RIDRETH1` et `INDFMPIR` (DEMO) ;
- `BMXBMI` (BMX) ;
- `DIQ010` (DIQ ; diabète = 1).

Adultes de 20 à 79 ans, hors femmes enceintes. Marqueurs mesurés quelle que soit la séance :
- numération ;
- biochimie, dont la glycémie et les TG sériques non à jeun `LBXSGL` et `LBXSTR`, et la CK
  (2011-2018) ;
- HbA1c, cholestérol total, HDL ;
- CRP standard (1999-2010) ;
- B12, folates érythrocytaires (1999-2006), 25-OH vitamine D, ferritine ;
- TSH (1999-2002 et 2007-2012).

Mêmes fichiers et variables que l'inventaire du programme.

**Indices dérivés** (NHANES III seulement : ils demandent la glycémie à jeun, l'insuline ou les TG
du plasma, mesurés à toutes les séances dans NHANES III) :
- HOMA-IR = glucose (mg/dL) × insuline (µU/mL) / 405 ;
- QUICKI = 1 / (log₁₀ insuline + log₁₀ glucose) ;
- TyG = ln(TG × glucose / 2), en mg/dL, sur l'échelle additive ;
- LDL calculé :
  - **Friedewald** : CT − HDL − TG/5 (mg/dL), si TG < 400 mg/dL ;
  - **Martin-Hopkins** : CT − HDL − TG / facteur, avec le tableau de facteurs de Martin et al.
    (JAMA 2013), lu dans la source. Si ce tableau ne peut pas être lu, l'indice est déclaré « non
    estimable ».

### Analyse A : jeûne chez une même personne (NHANES III), analyse principale

- **Modèle principal**, sur les paires avec le jeûne connu aux deux examens :
  $\ln x_2 - \ln x_1 = \alpha + \beta\,(F_2 - F_1) + \varepsilon$.
  - $F$ est la durée de jeûne en heures, plafonnée à 24 h.
  - L'ordonnée à l'origine $\alpha$ absorbe le décalage systématique entre examens.
  - Les marqueurs sur l'échelle additive dans Q1 (et le TyG) utilisent $x_2 - x_1$.
- **Effet rapporté** : le contraste « moins de 4 h contre 10 h », calculé à 2 h contre 10 h :
  $e^{\beta(2-10)} - 1$ en %, ou $\beta \times (2-10)$ sur l'échelle additive.
  - IC 95 % par bootstrap des personnes (2 000 tirages, graine 2026).
  - Estimable si au moins 30 paires ont un écart de jeûne d'au moins 4 h.
- **Sensibilité en classes** : même modèle, avec à la place de $F_2 - F_1$ les différences
  d'indicatrices des classes < 4 h et 4-8 h (référence ≥ 8 h). Effet rapporté : < 4 h contre ≥ 8 h.
- **Contraste direct, en appui** : chez les personnes discordantes (< 4 h à un examen, ≥ 8 h à
  l'autre), moyenne de $\ln x_{\text{non à jeun}} - \ln x_{\text{à jeun}}$, moins le décalage
  moyen orienté de la même façon chez les personnes de même classe aux deux examens. IC par
  bootstrap. **Estimable si au moins 30 paires discordantes** ; sinon « non estimable ».

### Analyse B : associations entre personnes

Ces résultats sont présentés comme des **associations**, à confronter à la physiologie connue : les
personnes vues l'après-midi ou non à jeun diffèrent des autres (âge, santé, emploi).

- **NHANES 1999-2018.** Régression linéaire de $\ln x$ (ou $x$ sur l'échelle additive) sur :
  - la durée de jeûne en classes (< 2, 2-4, 4-8, 8-12, ≥ 12 h ; référence 8-12 h) ;
  - la séance (référence : matin) ;
  - les covariables d'ajustement : âge (spline cubique naturelle, 4 degrés de liberté), sexe,
    IMC, groupe ethnique (`RIDRETH1`), rapport revenu / seuil de pauvreté, diabète déclaré et
    cycle.

  Contrastes rapportés :
  - non à jeun (moyenne des coefficients < 2 h et 2-4 h, pondérée par les effectifs) contre
    8-12 h ;
  - après-midi contre matin ; soir contre matin.

  IC par bootstrap des personnes (500 tirages), non pondéré.
- **NHANES III, examen principal.** Même modèle, avec l'**heure exacte** du prélèvement (spline
  cubique naturelle, 4 degrés de liberté) à la place de la séance. Covariables :
  - âge, sexe ;
  - IMC (`BMPBMI`), groupe ethnique (`DMARETHN`) ;
  - rapport revenu / seuil de pauvreté (`DMPPIR`) ;
  - diabète déclaré (`HAD1`).

  Contrastes d'heure, dans cet ordre : **11 h contre 8 h** (prélèvement du matin réaliste), puis
  16 h contre 9 h. Contraste de jeûne : < 4 h contre 8-12 h.
- **Heure chez une même personne** (NHANES III, 51 personnes avec plus de 2 h d'écart), en
  secondaire : régression de $\ln x_2 - \ln x_1$ sur la différence d'heure, avec ordonnée à
  l'origine. Effet rapporté par heure, avec l'effectif.

### Comparaison au changement détectable et règles

Ratio = |effet| / changement détectable à 6 mois de Q1, du côté de l'effet (20-79 ans, valeur
principale). Pour les indices dérivés sans valeur dans Q1 (LDL Martin-Hopkins), on reprend celui du
LDL Friedewald.

| Ratio | Conclusion |
|---|---|
| ≥ 1 | **comparaison impossible sans standardiser** |
| 0,5 à 1 | **à enregistrer et à corriger** |
| < 0,5 | négligeable |

**Décisions.**
- **Jeûne** : analyse A, modèle principal, contraste 2 h contre 10 h. Pour un marqueur absent des
  paires de NHANES III : analyse B (NHANES 1999-2018, non à jeun contre 8-12 h), avec le statut
  « association ».
- **Heure** : analyse B. NHANES III, 11 h contre 8 h, pour la décision principale. Si ce contraste
  n'est pas disponible : NHANES 1999-2018, après-midi contre matin. Le contraste 16 h contre 9 h est
  rapporté. S'il est ≥ 1, il ajoute la mention « horaire fixe requis si prélèvements
  l'après-midi ».

### Tableau final

Pour chaque marqueur et indice : effet du jeûne et de l'heure, leurs IC, le ratio au changement
détectable, et une **catégorie** :
- **à jeun requis** : ratio du jeûne ≥ 1 ;
- **horaire fixe requis** : ratio de l'heure ≥ 1 ;
- **à enregistrer et corriger** : un ratio de 0,5 à 1 ;
- **indifférent** : ratios < 0,5 ;
- **non estimable** : aucune estimation disponible.

Si plusieurs catégories s'appliquent, on les rapporte toutes.

### Attentes a priori (physiologie connue, données par l'auteur du projet)

| Marqueur | Attente | Situation |
|---|---|---|
| TG, glycémie, insuline (et HOMA-IR, TyG) | hausse | non à jeun |
| QUICKI | baisse | non à jeun |
| Fer | baisse dans la journée | heure plus tardive |
| TSH | baisse | après-midi contre matin |
| Phosphate | hausse | après-midi |
| Leucocytes | hausse | après-midi ou soir |

Une attente est **confirmée** si l'effet a le signe attendu et que son IC exclut 0.

### Réserves

- Les discordances de jeûne sont rares dans NHANES III (48 paires < 4 h / ≥ 8 h) : les IC seront
  larges.
- La séance ne varie jamais chez une même personne.
- NHANES est américain ; NHANES III date de 1988-1994.
- L'effet d'un repas dépend de sa composition, inconnue ici.
- Le changement détectable de Q1 est une borne basse pour la plupart des marqueurs.
- Le modèle linéaire en heures de jeûne suppose un effet proportionnel au temps écoulé ; la
  sensibilité en classes le vérifie.

### Correction de bug — lecture de NHANES III, code « 88 » des champs à 2 chiffres (2026-11-11)

**Découverte** : en Q2, les basophiles de NHANES III donnaient un effet de l'heure de 4,5 points de
pourcentage pour une valeur moyenne d'environ 0,5 %, ce qui est impossible.

**Cause** : `nhanes3.read_fixed` ne traitait comme manquants que les codes faits de 8 ou de 9 sur au
moins 3 chiffres. Dans les champs à 2 chiffres, « 88 » (vide mais applicable) était lu comme une
valeur.

**Portée**, mesurée sur toutes les variables NHANES III du programme :
- examen principal : formule leucocytaire manuelle (monocytes, éosinophiles, basophiles ;
  2 276 valeurs « 88 » chacun) et **bicarbonates** (1 495 valeurs) ;
- second examen : formule manuelle (27 valeurs).

Les seules autres variables à 2 chiffres lues sont l'âge et le délai entre examens, pour lesquels
88 est une valeur réelle. Elles ne changent pas, et **les analyses gelées des pistes précédentes
ne sont pas touchées**.

**Correction** : liste explicite `TWO_DIGIT_BLANK` dans `nhanes3.py` (formule manuelle et
bicarbonates), avec un test (`test_two_digit_blank_code`). Q1, Q4 et Q2 ont été relancées.

**Avant / après**

| Analyse | Avant | Après |
|---|---|---|
| Q1, bicarbonates NHANES III : CV observé | 18,1 % (n = 1 812) | 11,4 % (n = 1 757) |
| Q1, bicarbonates : changement détectable à 6 mois | +65 / −39 % | +38 / −27 % |
| Q1, formule manuelle NHANES III (écart-type intra, unités) | monocytes 8,6 ; éosinophiles 8,6 ; basophiles 10,4 | 2,6 ; 1,8 ; 0,9 (pas le jeu principal : aucun changement détectable modifié) |
| Q1, prédictions 1 à 3 | vérifiées (83 %, 80 %, 93 %) | inchangées |
| Q4, conclusions de la règle | — | inchangées (57 couples) |
| Q4, écart observé − attendu < 10 points | 81 % des couples | 87 % |
| Q4, normalisation des anomalies nettes (médiane) | 8 % | 5 % |
| Q2 | première exécution non interprétée | relancée après correction |

L'explication « artefact pré-analytique (perte de CO₂) » donnée dans le rapport de Q1 pour les
bicarbonates est **retirée** : c'était ce bug. Après correction, le CV de NHANES III reste deux fois
celui de 2001-2002, sans explication connue.

### Écart — Q2, codage de la séance (2026-11-11)

Le pré-enregistrement de Q2 indiquait `PHDSESN` codé 1, 2 et 3 (matin, après-midi, soir). La
documentation NHANES (FASTQX_D, lue) code 0 matin, 1 après-midi, 2 soir.
- La première exécution excluait donc les personnes vues le matin.
- Son contraste « après-midi contre matin » était en réalité soir contre après-midi.

Corrigé selon la documentation avant toute interprétation, sans autre changement d'analyse.

### Résultat — programme « panel », Q2 (2026-11-11)

Exécution du protocole (`6404a61`), avec les deux corrections ci-dessus. Rapport :
`reports/panel/Q2_JEUNE_HEURE.md`.

**Règle pré-enregistrée.** Aucun marqueur n'exige un prélèvement à jeun ou un horaire fixe : tous les
ratios sont < 0,5. Seule la CK est non estimable (pas de changement détectable dans Q1).

**Jeûne, chez une même personne** (NHANES III ; modèle principal, 2 h contre 10 h) :
- insuline +11 % [+4 ; +19] ; HOMA-IR +12 % ;
- TG −0,2 % ; glycémie +1 %.

En classes ou en contraste direct (34 à 44 paires discordantes) : TG +8 %, insuline +18 à +25 %.

**Jeûne, entre personnes (associations)** :
- TG +23 à +25 %, glycémie +5 à +10 %, insuline +77 %, HOMA-IR +94 %.
- Avec ces associations, insuline, HOMA-IR et QUICKI passeraient « à enregistrer et corriger »
  (ratios 0,66 à 0,71).

**Heure** : 11 h contre 8 h, aucun effet ≥ 0,5. Après-midi contre matin : TSH −16 %, leucocytes
+9 %, phosphate +2 %. Le soir : fer −17 %, leucocytes +16 %.

**Attentes physiologiques** :
- confirmées : insuline, HOMA-IR, QUICKI, TSH, phosphate, leucocytes ;
- non confirmées chez une même personne : TG, glycémie, TyG (confirmées entre personnes) ;
- fer : baisse le soir seulement.

**LDL Martin-Hopkins** : non estimable, comme prévu (tableau de facteurs publié en figure).

### Analyses secondaires — programme « panel », Q2, NON pré-enregistrées (2026-11-11)

Demandées par l'auteur du projet **après** lecture des résultats, parce que la conclusion
pré-enregistrée est fragile (modèle linéaire en heures de jeûne). La conclusion pré-enregistrée
reste inchangée dans le rapport. Code : `src/aging_clock/panel/q2_secondaire.py`.

1. **Jeûne par morceaux chez une même personne** (NHANES III, mêmes paires ; nœuds à 4 et 8 h,
   durée plafonnée à 24 h ; 2 h contre 10 h ; IC bootstrap, 2 000 tirages, graine 2026) :
   TG +14,9 % [+4,0 ; +27,5] (linéaire : −0,2 %) ; insuline +21,9 % ; HOMA-IR +23,2 % ;
   glycémie +3,4 % ; QUICKI −2,8 % ; cholestérol total, HDL, LDL : moins de 2 %. Ratios au
   changement détectable toujours < 0,2 : catégories inchangées.
2. **Nordestgaard et al., Eur Heart J 2016** (déclaration EAS/EFLM, texte complet lu) : TG +26 mg/dL
   (+24 % de la médiane à jeun de NHANES III), cholestérol total et LDL −8 mg/dL (−4 % et −7 %),
   HDL inchangé ; aucun changement moyen donné pour la glycémie. Accord avec les associations entre
   personnes (TG +23 %, LDL calculé −6 %) plus qu'avec les estimations chez une même personne.
3. **Classification** (personnes à jeun ≥ 8 h de NHANES III ; effet multiplicatif appliqué) :
   personnes qui passeraient au-dessus du seuil si le prélèvement était non à jeun, selon la
   fourchette d'effets (même personne → entre personnes) : glycémie OMS +1 à +16 points, ADA +3 à
   +31 points, TG 1,7 mmol/L jusqu'à +13 points, HOMA-IR (75ᵉ centile, valeur illustrative sans
   source) +6 à +39 points.

**Note clinique ajoutée au rapport** : HOMA-IR et QUICKI sont définis à jeun et ne sont pas valides
sur un prélèvement non à jeun, quel que soit le ratio ; même chose pour une « glycémie à jeun » dont
le jeûne n'est pas vérifié.

### Q2 : synthèse en deux temps (2026-11-11)

À la demande de l'auteur du projet, la synthèse du rapport de Q2 est formulée en deux temps : le jeûne
pèse peu pour suivre une personne (effet petit devant le bruit), mais beaucoup pour la classer
(jusqu'à +31 points au seuil ADA de la glycémie). Conséquence pratique : enregistrer le statut de
jeûne, et ne pas calculer les indices définis à jeun (HOMA-IR, QUICKI) quand il est inconnu. La
règle pré-enregistrée et sa conclusion restent inchangées.

### Pré-enregistrement — programme « panel », Q5 : changements de méthode de laboratoire (2026-11-11)

**Question.** De combien un changement de méthode, d'instrument ou de laboratoire déplace-t-il
chaque marqueur, comparé au changement détectable à 6 mois (Q1) ? Quels marqueurs ne peuvent pas
être comparés d'un laboratoire à l'autre sans équation de passage ? Et, comme pour le jeûne (Q2),
combien de personnes changent de classe autour d'un seuil ?

Ce texte est complet : il ne renvoie à aucun brouillon. Toutes les équations ci-dessous viennent de
la documentation NHANES et de la note analytique du NCHS sur la vitamine D (pages publiques du NCHS, lues et extraites avant ce pré-enregistrement ;
aucun résultat calculé).

#### Données et population

- NHANES 1999-2018, adultes de 20 à 79 ans, femmes enceintes exclues (D2). Non pondéré (D3), sauf
  pour la vérification V1 (qui reproduit un chiffre pondéré du NCHS).
- Fichiers : ceux de Q2 (`q2.G`), plus glycémie et insuline à jeun (`L10AM`, `GLU`, `INS`), TG à
  jeun (`L13AM`, `TRIGLY`), urines (`LAB16`, `L16`, `ALB_CR`), CRP ultrasensible (`HSCRP`), folates
  sériques et érythrocytaires (`LAB06`, `L06_B`, `L06NB_C`, `FOLATE`), ApoB (`ApoB`, `APOB`),
  testostérone (`TST`), thyroïde (`LAB18T4`, `L40T4_B`, `THYROD`), homocystéine (`LAB06`, `L06_B`,
  `L06MH_C`, `HCY`).
- Changement détectable : celui de Q1, groupe 20-79 ans (`cd6m_hausse` si le décalage est positif,
  `cd6m_baisse` s'il est négatif, `cd6m_unites` sur l'échelle additive). Sensibilité : changement
  empirique de Q1 (`cd6m_hausse_robuste`, et son pendant en baisse quand il existe).

#### Table des événements (figée)

« Nouvelle = f(ancienne) ». Type : L = laboratoire, I = instrument, M = méthode, K = lot ou réactif,
E = étalonnage par rapport à une méthode de référence. « Diffusion ajustée » : le NCHS a déjà
corrigé les données publiées, d'après sa documentation.

| # | Marqueur | Transition | Type | Équation ou décalage publié | Source | Diffusion ajustée |
|---|---|---|---|---|---|---|
| 1 | Créatinine sérique | 1999-2000 (laboratoire NHANES → référence) | E | réf = 1,013·x + 0,147 mg/dL | LAB18 | non |
| 2 | Créatinine sérique | 2005-2006 (laboratoire NHANES → référence) | E | réf = 0,978·x − 0,016 mg/dL | BIOPRO_D | non |
| 3 | Créatinine sérique | 2007 → 2008 (LX-20 → DxC800) | I | nouvelle − ancienne ≈ −0,08 mg/dL (moyenne) | BIOPRO_E | oui |
| 4 | Biochimie : PAL, créatinine, LDH, phosphore, bilirubine | 2001 → 2002 (changement de laboratoire) | L | équations non publiées dans la page lue | L40_B | oui |
| 5 | Bilan biochimique (21 analytes) | 2015-2016 → 2017-2018 (Beckman DxC 660i → Roche Cobas 6000) | L, I, M | voir table 5 ci-dessous | BIOPRO_J | non |
| 6 | Glycémie à jeun | 2003-2004 → 2005-2006 (Cobas Mira → Hitachi 911) | I | 0,9815·x + 3,5707 mg/dL | GLU_D | non |
| 7 | Glycémie à jeun | 2005-2006 → 2007-2008 (Hitachi 911 → Modular P) | I | x + 1,148 mg/dL | GLU_E | non |
| 8 | Glycémie à jeun | 2013-2014 → 2015-2016 (Cobas C501 → C311) | I | 1,023·x − 0,5108 mg/dL | GLU_I | données 2015-2016 mises à l'échelle C311 ; pas de correction vers 2013-2014 |
| 9 | Insuline | 1999-2002 → 2003-2004 (Pharmacia → Tosoh) | M | 1,0027·x − 2,2934 µU/mL | L10AM_C | non |
| 10 | Insuline | 2003-2004 → 2005-2006 (Tosoh → Mercodia) | M | 0,9501·x + 1,4890 µU/mL | GLU_D | non |
| 11 | Insuline | 2009-2010 → 2011-2012 (Mercodia → Roche) | M | 0,8868·x + 0,0011·x² − 0,0744 µU/mL | GLU_G | 2010 ajusté vers Mercodia ; 2011-2012 non |
| 12 | Insuline | 2011-2012 → 2013-2014 (Roche → Tosoh) | M | 10^(1,024·log₁₀x − 0,0802) | INS_H | non |
| 13 | HDL | 2005-2006 → 2007-2008 (nouveau laboratoire, autre instrument) | L, I | biais par rapport au CDC : +2,0 % → −0,5 %, soit −2,45 % | HDL_D, HDL_E | non |
| 14 | HDL | 2001-2002 → 2003-2004 (méthode directe) | M | non chiffré | l13_c | 1999-2002 et 2005-2006 corrigés sur contrôles |
| 15 | Cholestérol total, TG à jeun | 2005-2006 → 2007-2008 (nouveau laboratoire, Modular P) | L, I | non chiffré : « aucun ajustement nécessaire » | TCHOL_E, TRIGLY_E | non |
| 16 | HbA1c | 2005-2006 → 2007-2008 (glissement vers le haut inexpliqué) | inconnu | non chiffré (équation de 2005 retirée par le NCHS) | GHB_D | non |
| 17 | NFS (dont RDW, hématocrite, leucocytes) | 2011-2012 → 2013-2014 (Coulter HMX → DxH, en 2012) | I | non chiffré ; moyennes pondérées publiées : RDW 12,84 → 13,55 % ; hématocrite 40,57 → 41,22 % | CBC_H | non |
| 18 | Ferritine | 2007-2008 → 2009-2010 (Hitachi 912 → E170) | I | 10^(0,989·log₁₀x + 0,049) ng/mL | FERTIN_F | non |
| 19 | Ferritine | 2009-2010 → 2015-2016 (E170 → e601) | I | 1,079·x + 0,2243 ng/mL | FERTIN_I | données 2015-2016 mises à l'échelle e601 |
| 20 | Vitamine B12 | 2005-2006 → 2011-2012 (Bio-Rad → Roche) | M | 10^(0,97·log₁₀x + 0,14) pg/mL | VITB12_G | non |
| 21 | Vitamine B12 | 2013-2014 (dérive de lots) | K | non chiffré | VITB12_H | oui |
| 22 | Folates érythrocytaires | 1999-2006 → 2007-2008 (radio-essai Bio-Rad → microbiologique) | M | algorithme en 4 étapes (ci-dessous) | FOLATE_E | non |
| 23a | Vitamine D (25-OH) | 2001-2002 (RIA → LC-MS/MS standardisée) | M, E | 0,95212·x + 6,43435 nmol/L | note analytique NCHS sur la vitamine D | oui (LBDVIDMS) |
| 23b | Vitamine D (25-OH) | 2003-2004 (RIA → LC-MS/MS standardisée) | M, E | 0,98284·x + 1,72786 nmol/L | idem | oui |
| 23c | Vitamine D (25-OH) | 2005-2006 → 2007-2008 (RIA DiaSorin → LC-MS/MS) | M, E | 0,97012·x + 8,36753 nmol/L | idem ; VID_E | oui |
| 24 | CRP ultrasensible | 2015-2016 → 2017-2018 (DxC 660i → Cobas 6000) | L, I, M | 0,8695·x + 0,2954 mg/L (x ≤ 23 mg/L) | HSCRP_J | non |
| 25 | ApoB | 2005-2006 → 2007-2008 (BN100 → ProSpec, autre laboratoire) | L, I | 0,923·x mg/dL | ApoB_E | non |
| 26 | ApoB | 2013-2014 → 2015-2016 (ProSpec → Cobas 6000, turbidimétrie) | I, M | 1,001·x + 2,883 mg/dL | APOB_I | non |
| 27 | Testostérone totale | 2011-2012 → 2013-2014 (LC-MS/MS TST → TST + estradiol) | M | +3,9 % en moyenne ; équation 1,021·x + 0,182 (unité de l'ordonnée à l'origine ambiguë : ng/mL dans le texte, variable en ng/dL) | TST_H | début 2013 mis à l'échelle nouvelle |
| 28 | T4 libre, TSH | 2009 → 2010 (changement de laboratoire) | L | T4 totale +5 % (corrigée) ; T4 libre et TSH non chiffrées | THYROD_F, THYROD_G | T4 totale seulement |
| 29 | Homocystéine | 2002 (Abbott IMX → AxSym) | I | 10^(0,983·log₁₀x + 0,0418) µmol/L | LAB06, L06MH_C | non précisé |
| 30 | Homocystéine | 2005-2006 (réactif reformulé, ≈ +13 %) | K | non publié | HCY_D | oui |
| 31 | Créatinine urinaire (et donc ACR) | 2005-2006 → 2007-2008 (Modular P → CX3) | I, M | par morceaux : x < 75 : (1,02·√x − 0,36)² ; 75-250 : (1,05·√x − 0,74)² ; ≥ 250 : (1,01·√x − 0,10)² mg/dL | ALB_CR_E | non |
| 32 | Fer, CTF | 2001 → 2002 (changement de laboratoire) | L | non publié ; CTF corrigée | L40FE_B | CTF seulement |

**Table 5 : bilan biochimique 2017** (BIOPRO_J ; nouvelle = Cobas 6000, ancienne = DxC 660i ;
« % » = différence moyenne publiée).

| Analyte | Équation (nouvelle = f(ancienne)) | % publié |
|---|---|---|
| Albumine (g/dL) | 0,9581·x − 0,0108 | −4,42 |
| PAL (U/L) | log₁₀ y = 0,9986·log₁₀x + 0,04288 | +9,74 |
| ASAT (U/L) | 0,9822·x − 3,695 | −18,03 |
| ALAT (U/L) | 0,9869·x − 2,653 | −15,46 |
| Urée (mg/dL) | 0,9992·x − 0,4484 | −3,36 |
| Bicarbonates | ajustement non recommandé | +1,74 |
| Calcium | ajustement non recommandé | −2,12 |
| Cholestérol (bilan) | 0,9556·x + 2,105 | −3,21 |
| CK (U/L) | 1,068·x − 1,131 | +5,91 |
| Chlore | ajustement non recommandé | −1,44 |
| Créatinine (mg/dL) | 0,9515·x + 0,06608 | +3,35 |
| Glucose sérique | ajustement non recommandé | +2,41 |
| GGT (U/L) | 1,243·x − 2,938 | +7,70 |
| Fer (µg/dL) | 1,023·x + 4,597 | +10,01 |
| Potassium | ajustement non recommandé | −1,40 |
| LDH (U/L) | 1,167·x − 2,407 | +14,86 |
| Sodium | ajustement non recommandé | +0,80 |
| Phosphore | ajustement non recommandé | −1,80 |
| Bilirubine totale | ajustement non recommandé | −3,19 |
| Protéines totales | ajustement non recommandé | +0,36 |
| TG (bilan, non à jeun) | 1,036·x + 7,271 | +13,44 |
| Acide urique (mg/dL) | 1,073·x − 0,2495 | +2,37 |

Globuline et osmolalité sont calculées : leur décalage se déduit de ceux des analytes qui les
composent, comme les dérivés (rapports, DFG, FIB-4, etc.), recalculés à partir des valeurs
transformées.

**Événement 22 (folates érythrocytaires), algorithme du NCHS**, avec l'hématocrite (HCT, %) et les
folates sériques (FOL, nmol/L) de la même personne :
1. sang total : WBF = RBF·HCT/100 + FOL·(1 − HCT/100) ;
2. WBF ajusté = 10^(0,2204 + 1,017·log₁₀WBF) ;
3. FOL ajusté = 10^(0,0188·X³ − 2,7109·X^(−1/2) + 3,8276), avec X = log₁₀FOL ;
4. RBF ajusté = [WBF ajusté − FOL ajusté·(1 − HCT/100)] / (HCT/100).

**Événements 23a-c (vitamine D).**
- Source : note analytique du NCHS, « Analytical Note for 25-Hydroxyvitamin D Data Analysis using
  NHANES III (1988-1994), NHANES 2001-2006, and NHANES 2007-2010 ». Page publique wwwn.cdc.gov, lue
  en texte complet le 2026-11-11. Étude de passage sur 1 448 sérums réanalysés en LC-MS/MS.
- 2003-2006 : seules les valeurs converties (LBDVIDMS) sont diffusées. On retrouve la valeur RIA
  d'origine en inversant l'équation du cycle. C'est exact, puisque la conversion est linéaire.
- 2001-2002 : les deux variables sont diffusées (LBXVID en ng/mL, valeur RIA ; LBDVIDMS), d'où la
  vérification V3.
- L'équation par morceaux de NHANES III n'est pas utilisée : le fichier de laboratoire NHANES III du
  dépôt ne contient pas la vitamine D.

**Correction de l'inventaire.** L'inventaire indiquait pour la TSH « 2011 : kit reformulé ». La
documentation (THYROD_G) parle en fait des anticorps anti-thyroglobuline. Aucune reformulation
n'est documentée pour la TSH.

#### Partie (a) : équations de passage publiées

- Pour chaque événement chiffré, on applique l'équation aux valeurs des adultes du **cycle
  précédant** le changement (ancienne méthode), telles que diffusées.
- **Décalage** en % (échelle log) ou en unités (échelle additive, D4), aux centiles 10, 25, 50, 75
  et 90.
  - Mesure principale : décalage au **centile 50**.
  - Sensibilité : plus grand décalage, en valeur absolue, entre les centiles 10 et 90.
- Quand seule une différence moyenne est publiée (« ajustement non recommandé », événements 3,
  13 et 27), ce décalage s'applique à tous les centiles. Pour l'événement 3, c'est −0,08 mg/dL
  converti en % à chaque centile.
- Événement 27 : décalage principal = +3,9 %. Sensibilité : l'équation, avec l'ordonnée à l'origine
  lue en ng/dL, puis en ng/mL (×100). Résultats par sexe.
- Dérivés : on recalcule l'indice à partir des analytes transformés, chez les mêmes personnes, et
  on prend le décalage au centile 50 de l'indice.
- Événements non chiffrés (4, 14, 15, 16, 17, 21, 23, 28 sauf T4 totale, 30, 32) : « (a) non
  estimable », partie (b) seulement.

#### Partie (b) : décalage empirique (différence de différences)

- Pour chaque marqueur : régression de ln(x), ou de x sur l'échelle additive, sur des indicatrices
  de cycle, ajustée sur l'âge (spline cubique restreinte, 4 ddl, `features.rcs_basis`), le sexe et
  le groupe ethnique (RIDRETH1).
- **Saut** J_k = différence entre les coefficients de deux cycles successifs où le marqueur est
  mesuré.
- **Saut de référence** : moyenne des sauts aux transitions sans aucun événement de la table pour
  ce marqueur. Il faut au moins 2 transitions sans événement, sinon la partie (b) est non
  estimable (le saut brut est rapporté pour information).
- **Décalage empirique** = J_k − saut de référence. Si le changement tombe en milieu de cycle
  (événements 3, 11, 17, 29), on compare le cycle d'avant et celui d'après, et on retire deux fois
  le saut de référence.
- IC 95 % par bootstrap des personnes dans chaque cycle (500 tirages, graine 2026).
- **Sensibilité** : ajustement supplémentaire sur l'IMC et le rapport revenu/pauvreté.
- **Écart au plan** : le plan parlait de médianes standardisées. On prend des moyennes géométriques
  ajustées, plus stables et faciles à ajuster. La médiane (régression quantile, sans IC) est
  rapportée en sensibilité.
- **Lecture** :
  - si la diffusion est ajustée, (b) mesure le décalage **résiduel**, attendu proche de 0 ; c'est un
    contrôle ;
  - sinon, (b) est une estimation indépendante de (a).

#### Règles de décision

Ratio r = |décalage| / changement détectable à 6 mois (Q1), comme dans Q2.

| r | Catégorie de l'événement |
|---|---|
| ≥ 1 | **comparaison impossible sans équation de passage** |
| 0,5 à 1 | **un changement de laboratoire peut créer un faux changement** |
| < 0,5 | **négligeable au regard du bruit** |
| — | **non estimable** (pas de changement détectable dans Q1, ou ni (a) ni (b)) |

- Pour l'événement, on prend le ratio de (a) au centile 50. Si (a) n'est pas estimable, on prend
  (b), en le signalant « empirique ».
- **Catégorie du marqueur** = la plus défavorable de ses événements. On la rapporte aussi par type
  d'événement, car un changement de laboratoire et un changement de lot de réactif ne se
  présentent pas de la même façon dans un suivi.
- (a) et (b) sont dites « discordantes » si l'une donne r ≥ 0,5 et l'autre r < 0,5 (événements non
  ajustés dans la diffusion seulement).
- **Taux de faux changement** (indicateur complémentaire, pas une règle). C'est la probabilité
  qu'une personne sans changement réel franchisse le changement détectable à cause du décalage δ.
  - Formule : Φ(−1,96 + δ/s) + Φ(−1,96 − δ/s), sur l'échelle log, avec s = ln(1 + cd6m_hausse)/1,96.
  - Sans décalage, ce taux vaut 5 %.

#### Effet sur la classification

- Seuils : la table D1 figée (`D1_seuils_cliniques.csv`, seuils R et S). Pour les marqueurs qui
  n'ont que l'intervalle statistique, ce sont ses limites (`D1_intervalles_statistiques.csv`), par
  sexe quand il en dépend.
- Pour chaque événement chiffré de (a) : on transforme les valeurs du cycle précédent. On rapporte
  la part au-dessus (ou en dessous) du seuil, avant et après, et l'écart en points. Non pondéré,
  20-79 ans.
- Glycémie : seuils OMS et ADA, comme dans Q4.

#### Vérifications de l'implémentation (avant toute lecture des résultats)

- **V1** (GLU_I) : on applique l'équation inverse, C501 = 0,9776·x + 0,4994, aux glycémies à jeun
  de 2015-2016. Population : non enceintes, 18 ans et plus, sans diabète diagnostiqué (DIQ010 ≠ 1),
  pondération WTSAF2YR.
  - Attendu : part 100-125 mg/dL de 53,7 % → 41,5 % ; part ≥ 126 de 5,5 % → 3,4 %.
  - Tolérance : ±1,5 point.
- **V3** (vitamine D, 2001-2002) : 0,95212·(2,4959·LBXVID) + 6,43435 doit redonner LBDVIDMS.
  Tolérance : écart absolu médian < 0,5 nmol/L.
- **V2** (INS_H) : on applique l'équation inverse, 10^(0,9765·log₁₀x + 0,07832), à l'insuline de
  2013-2014. Moyenne géométrique pondérée (poids à jeun) attendue : 9,20 → 10,46 µU/mL, à ±0,15
  près.
- Si une vérification échoue : on cherche l'erreur et on la corrige avant l'analyse, puis on la
  documente. Si elle reste inexpliquée, l'écart est rapporté, sans changer le protocole.

#### Prédictions (a priori, sans calcul)

- **P1.** Les ratios les plus élevés viendront des analytes **à faible variabilité**, et non des
  enzymes, même si les enzymes ont les décalages en % les plus grands (ASAT −18 %, ALAT −15 % en
  2017). Vérifiée si :
  - au moins 3 des 5 ratios (a) les plus élevés appartiennent à {albumine, protéines, calcium,
    sodium, chlore, bicarbonates, créatinine, HbA1c, glycémie à jeun, cholestérol total, HDL} ;
  - et aucune enzyme (ALAT, ASAT, GGT, PAL, CK) n'atteint r ≥ 1.
- **P2.** Pour les événements non ajustés dans la diffusion où |décalage (a)| ≥ 3 %, (b) a le même
  signe que (a) dans au moins 75 % des cas.

#### Partie (c) : écarts entre laboratoires de routine (littérature)

Les changements de NHANES ont lieu entre des laboratoires de référence très contrôlés. La population
cible passe par plusieurs laboratoires de routine, dont les écarts sont probablement plus grands.

**Marqueurs concernés** : ceux du panel de suivi.
- Hématologie : leucocytes et formule, hématies, hémoglobine, hématocrite, VGM, TCMH, CCMH, RDW,
  plaquettes, VPM.
- Glycémie : glycémie à jeun, insuline, HbA1c.
- Lipides : cholestérol total, LDL, HDL, TG.
- Foie : ALAT, ASAT, GGT, PAL, bilirubine totale et conjuguée, albumine, protéines totales,
  globulines.
- Autres : lipase, créatinine, urée, sodium, potassium, chlore, bicarbonates, osmolalité,
  CRP ultrasensible, vitamine B12, folates érythrocytaires, vitamine D (25-OH), calcium, magnésium.

**Critères de sélection des études** (fixés ici) :
1. Évaluation externe de la qualité (EEQ) ou programme d'harmonisation, publiés dans une revue
   indexée.
2. Résultat chiffré par marqueur : CV entre laboratoires (CV_inter), ou biais entre laboratoires
   ou entre méthodes, sur un marqueur du panel de suivi.
3. Laboratoires de routine : au moins 20, ou un programme national.
4. Laboratoires européens de préférence. Une étude non européenne n'est retenue que si aucune
   étude européenne ne couvre le marqueur.
5. Matériaux commutables de préférence. Avec des matériaux non commutables, l'étude est retenue
   mais signalée (les effets de matrice gonflent les écarts).
6. Publiée en 2005 ou après, et lue : texte complet si accessible, sinon résumé, avec la mention TC
   ou R. Un résumé n'est retenu que s'il donne le chiffre. Pas de page de laboratoire privé.

**Requêtes PubMed** (D6) :
1. `("external quality assessment"[tiab] OR "proficiency testing"[tiab]) AND ("between-laboratory"[tiab] OR interlaboratory[tiab] OR "inter-laboratory"[tiab]) AND commutable[tiab]`
2. `("external quality assessment"[tiab] OR EQA[tiab]) AND harmonization[tiab] AND (Europe[tiab] OR European[tiab])`
3. `(HbA1c[tiab] OR "glycated hemoglobin"[tiab]) AND ("external quality assessment"[tiab] OR EurA1c[tiab]) AND (laboratories[tiab] OR "between-laboratory"[tiab])`
4. `("external quality assessment"[tiab] OR "proficiency testing"[tiab]) AND (enzymes[tiab] OR ALT[tiab] OR GGT[tiab] OR creatinine[tiab] OR "25-hydroxyvitamin D"[tiab] OR "vitamin B12"[tiab] OR "C-reactive protein"[tiab]) AND ("between-laboratory"[tiab] OR interlaboratory[tiab] OR "inter-laboratory"[tiab])`
5. `("external quality assessment"[tiab] OR "proficiency testing"[tiab]) AND ("complete blood count"[tiab] OR hematology[tiab] OR haematology[tiab]) AND (laboratories[tiab] OR interlaboratory[tiab])`

**Lecture.**
- Pour chaque requête : les 20 premiers résultats (tri par pertinence), lus sur titre et résumé.
  Le texte complet est lu pour les études qui satisfont les critères.
- Au plus 15 études retenues en tout.
- **Par marqueur** : l'étude européenne la plus récente sur matériau commutable. À défaut,
  l'étude la plus récente qui satisfait les critères.
- Marqueur sans étude : « rien trouvé avec ces requêtes ».
- Seules les valeurs dérivées et la référence entrent dans le rapport public. Les valeurs extraites
  (CV_inter) et le détail de la sélection vont dans `private/panel/Q5_litterature/`. Le rapport
  public donne, par marqueur, le changement détectable entre deux laboratoires, son rapport à
  celui de Q1 et la référence.

**Calcul** (échelle log, CV converti en σ = √ln(1 + CV²)) :
- décalage typique entre deux laboratoires : δ_lab = √2·CV_inter ;
- **changement détectable entre deux laboratoires différents** :
  hausse = e^{1,96·√2·√(σ_6m² + σ_inter²)} − 1, et la baisse de même. On le compare au changement
  détectable de Q1 (même laboratoire), par le rapport des deux.
- Si l'étude ne donne qu'un biais entre méthodes (pas de CV_inter), ce biais est traité comme un
  décalage δ, avec les règles de la partie (a).
- Mêmes règles de décision : δ_lab rapporté au changement détectable de Q1.

#### Partie (d) : un changement de laboratoire peut-il imiter ou masquer une intervention ?

- **Effets d'intervention** : ceux de Q1 (`Q1_interventions.csv` et `Q1_secondaire_moyenner.csv`,
  groupe 20-79 ans), en %.
- **Décalages** : ceux des parties (a) ou, à défaut, (b), et le δ_lab de (c), en %.
- Un décalage mesuré sur l'analyte du bilan biochimique (TG, cholestérol, glucose sériques) sert de
  décalage pour le même analyte : c'est le même dosage, fait dans un autre laboratoire. On le
  signale.
- **Rapport** ρ = |décalage| / |effet de l'intervention|, pour chaque couple (marqueur,
  intervention), avec le plus grand décalage du marqueur et aussi événement par événement.
- **Signalement** :
  - **peut imiter** l'intervention : ρ ≥ 0,5 et décalage de même signe que l'effet ;
  - **peut masquer** l'intervention : ρ ≥ 0,5 et signe opposé ;
  - ρ ≥ 1 : le changement de laboratoire **suffit** à produire (ou à annuler) l'effet moyen de
    l'intervention.
- Pour δ_lab, dont le signe est inconnu (deux laboratoires au hasard), on signale « peut imiter ou
  masquer ».
- C'est une comparaison d'effets moyens, sur la même échelle. Le bruit individuel est traité
  ailleurs, dans le ratio au changement détectable.

#### Prédiction sur la partie (d)

- **P3.** Elle est formulée en connaissant les différences moyennes publiées dans la table des
  événements, mais sans avoir calculé aucun rapport ρ. Elle est vérifiée si les deux conditions
  sont remplies :
  - pour les **TG**, l'**ALAT** et la **vitamine D**, au moins un changement de laboratoire ou de
    méthode des parties (a) ou (c) atteint ρ ≥ 0,5 face à au moins une intervention de Q1 ;
  - au moins la moitié des marqueurs qui ont à la fois un décalage estimé et un effet
    d'intervention dans Q1 ont un ρ ≥ 0,5.

#### Limites (à écrire dans le rapport)

- Les méthodes de NHANES ne sont pas celles des laboratoires de la population cible. On obtient un
  **ordre de grandeur** des décalages possibles.
- Les équations de passage sont estimées sur 92 à 773 échantillons ; leur IC n'est pas propagé.
- La partie (b) ne retire qu'en partie la tendance séculaire et les changements de composition de
  l'échantillon.
- Les changements détectables de Q1 sont des bornes basses (remesures à environ 2 semaines).
- NHANES est américain.
- Pas de seuil fondé sur le risque propre à Q5 : les seuils viennent de D1 (R ou S, signalés comme
  tels).

#### Livrables

- Rapport : `reports/panel/Q5_METHODES.md`.
- Données : `Q5_evenements.csv` (table ci-dessus), `Q5_passage.csv` (a), `Q5_empirique.csv` (b),
  `Q5_classification.csv`, `Q5_entre_laboratoires.csv` (c), `Q5_interventions.csv` (d),
  `Q5_synthese.csv`, `Q5_verifications.json`, `Q5_predictions.json`.
- Code : `src/aging_clock/panel/q5.py`.

Décisions de l'auteur du projet intégrées avant le commit : partie (c) retenue, avec ses critères de
sélection ; moyennes géométriques ajustées, médiane en sensibilité ; vitamine D traitée en (a) avec
l'équation de la note NCHS ; partie (d) et prédiction P3 ajoutées.

### Résultat — programme « panel », Q5 (2026-11-11)

Exécution du protocole (`22c38f5`). Rapport : `reports/panel/Q5_METHODES.md`.

**Vérifications.** V2 et V3 réussies. V1 en échec partiel : les valeurs après correction du NCHS
sont retrouvées exactement (41,5 % et 3,4 %), mais pas les valeurs avant (48,3 % contre 53,7 %).
À la demande de l'auteur du projet, 36 variantes ont été testées sans changer l'analyse : poids
WTSAF2YR ou WTMEC2YR, âge minimal 18 ou 20 ans, exclusion des diabétiques connus, jeûne ≥ 8 h.
Aucune n'explique l'écart, qui reste inexpliqué.
Effet sur la classification (part de 100-125 mg/dL) : +6,8 points dans nos calculs, contre +12,2
dans le texte du NCHS. Hypothèse : version antérieure du fichier GLU_I.

**Règle pré-enregistrée (suivi).**
- Ratio ≥ 1 : folates érythrocytaires 2007 (+85 %) ; créatinine 1999-2000 (+22 %).
- Ratio de 0,5 à 1 :
  - créatinine 2007, DFGe et urée/créatinine 1999, albumine/globulines 2017 ;
  - en empirique : PAL et bilirubine 1999-2003, RDW et VPM (2012), insuline 2003.
- Tous les autres marqueurs : < 0,5.

**Classification.** Passage Beckman → Roche en 2017 (bilan biochimique) : +26 points sous la limite basse de l'ASAT,
+10 à +14 pour l'ALAT, le chlore, le calcium et la bilirubine (S). Glycémie : +4 à +5 points au
seuil ADA à chaque changement d'instrument (R). Vitamine D, RIA → LC-MS/MS : −10 points sous
50 nmol/L.

**(c)** Trois études européennes retenues (EEQ espagnole 2019, EurA1c 2026, INSTAND 2019), deux en
sensibilité (RfB 2021, Equalis 2019). Le changement détectable entre deux laboratoires vaut 1,02 à
1,49 fois celui d'un même laboratoire : calcium ×1,49 (ratio 0,53), PAL ×1,30, HbA1c ×1,27. Pour
les lipides, la NFS, les vitamines et l'insuline, rien trouvé avec ces requêtes : l'écart entre
laboratoires de routine y reste inconnu.

**(d)** ρ ≥ 0,5 pour 11 marqueurs sur 15 : TG, insuline, HOMA-IR, cholestérol total, HDL,
glycémie, HbA1c, GGT, ALAT, ASAT et CRP. Pas pour la vitamine D (ρ ≤ 0,15), ni pour le LDL sous
statine.

**Lien avec Q1, ajouté à la synthèse à la demande de l'auteur du projet.** Les effets d'hygiène de vie
ne sont visibles qu'en moyenne de groupe. Or un changement de laboratoire peut les imiter ou les
masquer pour 11 marqueurs sur 15. Toute évaluation de l'effet d'un protocole à l'échelle d'une
cohorte doit donc enregistrer le laboratoire de chaque prélèvement et en tenir compte : comparaisons
à laboratoire identique, ou laboratoire en covariable.

**Noms de fabricants** : conservés. La règle de neutralité ne vise que l'entreprise du panel cible.

**Prédictions.** P1 non vérifiée (2 analytes à faible variabilité parmi les 5 premiers ; aucune
enzyme ≥ 1). P2 vérifiée (20 sur 24). P3 non vérifiée (vitamine D).

**Écarts.**
- Régression médiane : moindres carrés repondérés itératifs au lieu de la programmation linéaire,
  arrêtée faute de temps de calcul, avant toute lecture.
- Corrigés avant la lecture des ratios :
  - échelle log (bilirubine, LDL, LDL/HDL) ;
  - unités des folates dans la classification ;
  - osmolalité exclue de la classification.
- Créatinine 2005-2006 : convention de sens opposée entre (a) et (b), signalée dans le rapport.

### Pré-enregistrement — programme « panel », Q3 : populations particulières (2026-11-11)

**Question.** Chez des groupes proches de la population cible, les marqueurs sont-ils décalés ?
Les seuils usuels (D1) donnent-ils trop de faux signaux chez les personnes en bonne santé ? De combien
un centile « population générale » flatte-t-il une population favorisée et en bonne santé ?

Ce texte est complet : il ne renvoie à aucun brouillon. Les effectifs ci-dessous ont été comptés à
partir des questionnaires, des ordonnances et de l'accéléromètre seulement
(`q3.run(only_groups=True)`, fichier `reports/panel/Q3_groupes.json`). Aucune valeur de marqueur
n'a été lue. Version validée par l'auteur du projet avec six modifications (voir la fin).

#### Cycles et marqueurs

- **NHANES 2003-2010** : ce sont les cycles et donc les méthodes de laboratoire des intervalles
  statistiques D1. Q5 a montré qu'un intervalle n'est valable que pour la méthode qui l'a produit.
  Accéléromètre : 2003-2006. Chaque marqueur est restreint aux cycles de son intervalle D1 (folates
  érythrocytaires et B12 : 2003-2006).
- **Marqueurs** :
  - pour les taux hors seuil : ceux de la table D1 (intervalles S, seuils R) ;
  - pour les décalages : les mêmes, plus la CK, l'HbA1c, la vitamine D, la glycémie et les TG à jeun
    et les indices dérivés de Q1 (DFGe CKD-EPI 2021, non-HDL, LDL, RAC, HOMA-IR, QUICKI, TyG, TG/HDL,
    indice athérogène, LDL/HDL, albumine/globulines, FIB-4, GGT/HDL, ASAT/ALAT, urée/créatinine,
    NLR, SII, calcium corrigé, glycémie moyenne estimée).
  - Les marqueurs à jeun (glycémie, insuline, TG, LDL et leurs indices) sont analysés dans le
    sous-échantillon à jeun (poids WTSAF2YR > 0).
- **Changement détectable** : celui de Q1, groupe 30-55 ans (`cd6m_hausse` ou `cd6m_baisse` selon le
  sens du décalage ; `cd6m_unites` sur l'échelle additive). Si un marqueur manque dans le groupe
  30-55 ans, on prend le groupe 20-79 ans, et on l'indique. Même échelle (log ou additive) que Q1.

#### Groupes (effectifs comptés avant analyse)

« Sains » : membres de la population de référence D1 (`intervalles.reference_population`), critères
appliqués tels quels :
- non enceinte ;
- cotinine < 3 ng/mL ;
- IMC de 18,5 à 30 ;
- sans diabète ni antidiabétique ;
- sans maladie cardiovasculaire, hépatique, rénale ni cancer déclarés ;
- sans antihypertenseur ni hypolipémiant.

| Groupe | Définition | Comparaison | Effectif (dont sains) | Comparaison (n) |
|---|---|---|---|---|
| **Très actifs** (principal) | 30-55 ans, accéléromètre 2003-2006 fiable (PAXSTAT = PAXCAL = 1), au moins 4 jours valides : **5 % les plus actifs au sein de chaque sexe** en minutes d'activité modérée à vigoureuse par jour (seuils : 72 min/jour chez les hommes, 43 chez les femmes) | les autres 30-55 ans **du même sexe** avec accéléromètre valide | 166 (92) ; H 83 (44), F 83 (48) | H 1 573, F 1 555 |
| Très actifs, sensibilité 1 | 5 % les plus actifs, **seuil global** (59 min/jour) | les autres 30-55 ans avec accéléromètre valide | 168 (81) ; H 136 (63), F 32 (18) | 3 126 |
| Très actifs, sensibilité 2 | 30-55 ans, 2003-2010, activité vigoureuse de loisir ≥ 300 min/semaine (questionnaire) | les autres 30-55 ans | 521 (204) ; H 334, F 187 | 8 739 |
| **Pilule** (principal) | femmes de 20 à 49 ans, non enceintes, pilule actuelle (RHD442 = 1), sans injectable (RHQ520 ≠ 1) ni patch ou anneau sur ordonnance | femmes de 20 à 49 ans non enceintes, réglées dans l'année (RHQ031 = 1), sans pilule, injectable ni contraceptif hormonal sur ordonnance | 546 (294) | 3 236 |
| Pilule œstroprogestative | pilule + ordonnance orale d'éthinylestradiol (ou de mestranol) dans le fichier des médicaments (RXQ_RX) | idem | 344 (187) | 3 236 |
| Pilule progestative seule | pilule + ordonnance de noréthindrone ou de norgestrel seuls, sans éthinylestradiol | idem | 13 (9) : non estimable, rapporté par transparence | 3 236 |
| **Injectable** (analyse séparée) | injectable actuel (RHQ520 = 1 ; acétate de médroxyprogestérone, progestatif seul), sans pilule | idem | 103 (37) | 3 236 |
| **Après la ménopause** | femmes de 45 à 59 ans, sans règles depuis 12 mois pour cause de ménopause (RHQ031 = 2, RHD042 = 7), sans hystérectomie (RHD280 ≠ 1), sans traitement hormonal actuel (RHQ558, RHQ566, RHQ574, RHQ584, RHQ600 ≠ 1, et aucune ordonnance d'œstrogène ou de progestatif) | femmes de 45 à 59 ans réglées dans l'année (RHQ031 = 1), sans pilule ni hormone sur ordonnance | 687 (144) | 780 |
| Ménopause sous traitement hormonal | idem, avec traitement hormonal actuel | idem | 55 (20) : rapporté à part, sans règle | 780 |
| **Favorisée** | 30-55 ans, revenu ≥ 3,5 fois le seuil de pauvreté (INDFMPIR), diplôme universitaire (DMDEDUC2 = 5), non-fumeur actuel (SMQ020 = 2 ou SMQ040 = 3) et cotinine < 10 ng/mL | les autres 30-55 ans | 1 075 (607) ; H 509 (279), F 566 (328) | 8 191 |

- **Le seuil d'activité décrit des personnes actives, pas des athlètes de compétition.** 72 minutes
  par jour chez les hommes et 43 chez les femmes, cela correspond à des personnes très actives au
  quotidien. L'accéléromètre porté à la hanche capte mal le vélo et la natation, et ne capte pas la
  musculation.
- **Le questionnaire RHQ ne dit pas quel type de pilule.** La distinction entre pilule
  œstroprogestative et pilule progestative seule vient du fichier des médicaments sur ordonnance des
  30 derniers jours (RXQ_RX, noms de molécules).
  - Une femme sous pilule sans ordonnance retrouvée reste dans le groupe « pilule » mais n'entre dans
    aucun des deux sous-groupes.
  - La noréthindrone seule peut aussi être prescrite à dose gynécologique (la dose n'est pas lue).
  - Les variables RHQ562-RHQ566 portent sur les hormones de la ménopause : elles excluent la
    contraception.
- **Corrections par rapport à la version présentée** (avant toute lecture de marqueur) :
  - le traitement hormonal de la ménopause comptait RHQ580 (« a déjà utilisé » un patch). Il est
    remplacé par les usages actuels, plus l'ordonnance. La ménopause passe de 700 à 687 femmes ;
  - la comparaison de la contraception excluait les femmes n'ayant jamais pris la pilule
    (RHD442 manquant). Elle les inclut désormais.
- RHD042 = 7 code « ménopause ou hystérectomie » : l'hystérectomie est exclue par RHD280.

**Accéléromètre** (`src/aging_clock/panel/accelerometre.py`, règles de Troiano et al., Med Sci Sports
Exerc 2008) :
- non-port : au moins 60 minutes consécutives à 0 coup, avec au plus 2 minutes consécutives entre
  1 et 100 coups ;
- jour valide : au moins 600 minutes de port ; personne retenue : au moins 4 jours valides ;
- activité modérée à vigoureuse : minutes à 2 020 coups/minute ou plus ; moyenne sur les jours
  valides.

#### Mesures

1. **Décalage.**
   - Régression médiane (moindres carrés repondérés itératifs, comme Q5) de ln(x), ou de x sur
     l'échelle additive, sur l'indicatrice du groupe. Ajustement sur l'âge (spline cubique
     restreinte, 4 ddl, nœuds aux centiles 5, 27,5, 50, 72,5 et 95), et sur le sexe quand les deux
     sexes sont présents.
   - **Très actifs** : analyse principale **par sexe**, chaque sexe contre son comparateur du même
     sexe. L'estimation commune (deux sexes, ajustée sur le sexe) sert aux attentes physiologiques.
   - **Ménopause** : l'ajustement sur l'âge est indispensable, car les ménopausées sont plus âgées
     que les femmes réglées du même intervalle 45-59 ans. Il est fait par la même spline, dans
     l'intervalle 45-59 ans.
   - Effet en % (ou en unités). IC 95 % par bootstrap des personnes, stratifié groupe/comparaison
     (500 tirages, graine 2026).
   - Sensibilité : moindres carrés (moyenne géométrique).
   - Toutes les strates (deux sexes, puis chaque sexe) sont produites pour les groupes mixtes.
2. **Taux hors seuil chez les sains du groupe** (« faux signaux »), par sexe et par côté :
   - pour les intervalles S, sous la limite basse et au-dessus de la limite haute, limites de D1
     appliquées par sexe et par tranche d'âge ;
   - pour les seuils R, dans le sens du seuil ;
   - non pondéré (D3, comparaison interne).
3. **Taux de référence** : le même taux dans la population de référence D1, restreinte au même
   sexe et aux mêmes âges que le groupe (par exemple les femmes de 20 à 49 ans pour la
   contraception).
4. **Centile « population générale » (groupe favorisé)** :
   - pour chaque marqueur et chaque sexe, médiane du groupe favorisé ;
   - puis son centile dans la population générale de 30 à 55 ans (non enceintes, favorisés compris)
     du même sexe, pondéré par les poids d'examen (WTMEC2YR ; WTSAF2YR pour les marqueurs à jeun).
   - Principal : groupe favorisé **et sain**. Rapportés aussi : tout le groupe favorisé, et le centile
     non pondéré.
   - Écart = centile − 50, en points. Il mesure de combien un centile « population générale » situe
     une personne favorisée et en bonne santé loin du milieu.
   - Mesure descriptive. On signale un écart d'au moins 10 points, sans règle de décision.

#### Règles de décision (par groupe, sexe, marqueur et côté)

Les seuils usuels sont **inadaptés** au groupe si :
- |décalage| ≥ changement détectable à 6 mois (Q1, 30-55 ans), **ou**
- le taux hors seuil chez les sains du groupe est au moins **2 fois** le taux de référence **et**
  au moins **10 %**.

Autres catégories :
- **décalé, sous le changement détectable** : l'IC du décalage exclut 0, mais |décalage| est
  inférieur au changement détectable ;
- **sans différence** : sinon ;
- **non estimable** : moins de 50 personnes mesurées dans le groupe pour le décalage, ou moins de
  30 sains mesurés pour le taux.

Analyses principales :
- très actifs par sexe (5 % au sein de chaque sexe) ;
- pilule ;
- injectable ;
- ménopause sans traitement ;
- favorisée.

Les sensibilités sont rapportées sans règle propre :
- seuil global et questionnaire pour les très actifs ;
- pilule œstroprogestative confirmée par ordonnance.

On note si elles confirment l'analyse principale.

#### Attentes physiologiques (validées par l'auteur du projet)

- **Règle de confirmation.** Une attente est confirmée si le décalage a le signe attendu et que son
  IC exclut 0. Elle est contredite si l'IC exclut 0 dans l'autre sens.
- **Sources.** Ce sont des revues ouvertes et lues (texte intégral PMC, conservé dans
  `private/panel/Q3_litterature/`). Une attente sans source lue est marquée **« sans source lue »**.

| Groupe | Attente | Source lue |
|---|---|---|
| Très actifs | TG ↓, cholestérol total ↓ | Lee 2017 : l'utilisation des graisses à l'effort réduit le cholestérol total et les TG de repos |
| | glycémie à jeun ↓ | Lee 2017 |
| | ferritine ↓ | Lee 2017 (sportifs d'endurance, surtout les femmes, sujets à la carence en fer) ; Solberg 2023 (prévalence élevée de la carence en fer chez les sportifs d'endurance) |
| | CK ↑ | Lee 2017 (la CK culmine environ 24 h après un effort lésant, élevée jusqu'à 7 jours) |
| | hémoglobine et hématocrite ↓ | Mairbäurl 2013 (hématocrite plus bas chez les sportifs, « anémie du sportif » ; l'hémoglobine et l'hématocrite dépendent du volume plasmatique) |
| | HDL ↑ ; créatinine ↑ (masse musculaire), donc DFGe ↓ ; ASAT ↑ ; leucocytes ↓ ; CRP ↓ ; insuline ↓ | **sans source lue** |
| Pilule (et pilule œstroprogestative) | TG ↑, HDL ↑ | Regidor 2023 (éthinylestradiol + drospirénone : TG +42 à +74 %, HDL +13 à +26 % selon les essais) |
| | ferritine ↑ | Fischer 2021 (la pilule réduit les pertes menstruelles ; ferritine plus haute chez les utilisatrices dans une étude citée) |
| | CRP ↑ ; CTF (capacité totale de fixation du fer) ↑ ; albumine ↓ ; vitamine B12 ↓ | **sans source lue** |
| Pilule progestative seule | lipides neutres | Regidor 2023 (drospirénone seule : effet sur les lipides jugé neutre) ; groupe non estimable |
| Injectable | pas d'attente de signe sur un marqueur du bilan | Glisic 2018 (méta-analyse des progestatifs seuls) : prise de poids modeste, surtout sous médroxyprogestérone injectable ; selon une revue antérieure citée, pas d’effet sur la glycémie chez les femmes minces tolérantes au glucose |
| Après la ménopause | cholestérol total ↑, LDL ↑, TG ↑, ApoB ↑, HDL ↓ | Fasero 2025 (« increased levels of total cholesterol, LDL-cholesterol, triglycerides and apolipoprotein B ; decreased HDL ») |
| | PAL ↑ | Bhattoa 2025 : hausse des marqueurs du remodelage osseux, dont la PAL osseuse, en fin de périménopause et en début de postménopause. Lien **indirect** : NHANES mesure la PAL totale |
| | ferritine ↑ ; hémoglobine ↑ ; acide urique ↑ | **sans source lue** |
| Favorisée | pas d'attente de signe ; taux de faux signaux proches du taux de référence | sans objet |

Revues lues (toutes en texte intégral) :
- Lee EC et al., J Strength Cond Res 2017, doi:10.1519/JSC.0000000000002122 (PMC5640004) ;
- Solberg A et al., Life 2023, doi:10.3390/life13102007 (PMC10608302) ;
- Mairbäurl H, Front Physiol 2013, doi:10.3389/fphys.2013.00332 (PMC3824146) ;
- Regidor PA et al., Womens Health 2023, doi:10.1177/17455057221147388 (PMC9905034) ;
- Fischer JAJ et al., Nutrients 2021, doi:10.3390/nu13072340 (PMC8308850) ;
- Glisic M et al., Eur J Prev Cardiol 2018, doi:10.1177/2047487318774847 (PMC6039863) ;
- Fasero M et al., J Clin Med 2025, doi:10.3390/jcm14113663 (PMC12156203) ;
- Bhattoa HP et al., Osteoporos Int 2025, doi:10.1007/s00198-025-07422-3 (PMC12064614).

Recherches PubMed (filtre « pubmed pmc », revues et méta-analyses) :
- sur les sportifs (biomarqueurs, fer, hématologie, créatinine) ;
- sur la pilule (lipides, CRP, fer, B12, transferrine, albumine) ;
- sur l'injectable ;
- sur la ménopause (lipides, fer, ferritine, PAL, acide urique).

**Rien trouvé avec ces requêtes** :
- une revue lue appuyant la créatinine, l'ASAT, les leucocytes, la CRP ou l'insuline chez les
  sportifs ;
- la CRP, la CTF, l'albumine ou la B12 sous pilule ;
- la ferritine, l'hémoglobine ou l'acide urique après la ménopause.

#### Prédiction

- **P1.** Au moins un couple (groupe, marqueur) est classé « inadapté » chez les très actifs
  (analyse principale, l'un ou l'autre sexe), par la règle du taux (faux signaux) :
  - créatinine (limite haute S) ;
  - DFGe (< 60) ;
  - ASAT (limite haute S) ;
  - hémoglobine (limite basse S).

  Formulée sans avoir lu aucune valeur de marqueur.

#### Limites (à écrire dans le rapport)

- Les proxys restent imparfaits :
  - « très actif » n'est pas « athlète de compétition » ; l'accéléromètre de hanche capte mal le vélo
    et la natation ;
  - la contraception et la ménopause sont déclarées ;
  - le type de pilule vient des ordonnances, qui ne sont pas toujours retrouvées.
- Les effectifs de sains sont petits : très actifs 44 hommes et 48 femmes, injectable 37, ménopause
  144.
- L'accéléromètre de 2011-2014 (prévu au plan) n'est pas utilisé. Ses mesures (MIMS) n'ont pas les
  mêmes unités, et les méthodes de laboratoire de ces cycles diffèrent de celles de D1.
- Hormones exclues (testostérone, estradiol, SHBG, FSH) : elles ne sont pas mesurées en 2003-2010
  chez tous les adultes. Or l'éthinylestradiol augmente fortement la SHBG (Regidor 2023), ce qui
  est un faux signal classique sous pilule. L'indice d'androgènes libres (testostérone/SHBG) en
  dépend : un bilan hormonal sous pilule ne s'interprète pas avec des seuils généraux. Q3 ne peut
  pas le chiffrer.
- Étude transversale, sur des Américains, cycles 2003-2010 : les méthodes de laboratoire ont changé
  depuis (Q5).
- Les changements détectables de Q1 sont des bornes basses (remesures à environ 2 semaines).
- Convention statistique (S) contre seuil fondé sur le risque (R) : un taux « hors S » élevé chez des
  sains signale un intervalle mal adapté, pas un risque.

#### Livrables

- Rapport : `reports/panel/Q3_POPULATIONS.md`.
- Données :
  - `Q3_groupes.json` (effectifs, déjà produit) ;
  - `Q3_decalages.csv`, `Q3_faux_signaux.csv`, `Q3_centiles_favorisee.csv`, `Q3_synthese.csv` ;
  - `Q3_attentes.json`, `Q3_predictions.json`.
- Code : `src/aging_clock/panel/q3.py`, `src/aging_clock/panel/accelerometre.py`.

#### Décisions de l'auteur du projet (validation du 2026-11-11)

1. **Très actifs.** Le groupe à seuil global est masculin à 80 %. L'analyse principale devient donc
   celle des 5 % les plus actifs au sein de chaque sexe, avec un comparateur de même sexe ; le seuil
   global passe en sensibilité. Le rapport précise que ces personnes sont actives, pas des athlètes
   de compétition, et que l'accéléromètre capte mal le vélo et la natation.
2. **Contraception.**
   - Pilule en analyse principale, injectables en analyse séparée (effets différents, progestatif
     seul).
   - La pilule œstroprogestative et la pilule progestative seule sont distinguées par les ordonnances.
     La seconde (13 femmes) est non estimable.
3. **Attentes.** Ferritine plus basse chez les très actifs, plus haute sous pilule. Chaque groupe
   s'appuie sur au moins une revue lue. Les attentes sans source sont marquées comme telles.
4. **Ménopause** : ajustement sur l'âge explicite.
5. **Population favorisée** : ajout du centile « population générale » de la personne médiane du
   groupe.
6. **Accéléromètre et hormones.** Abandon de l'accéléromètre 2011-2014 validé. Exclusion des hormones
   validée, avec la limite de la SHBG sous pilule écrite dans le rapport.

### Résultat — programme « panel », Q3 (2026-11-12)

Rapport : `reports/panel/Q3_POPULATIONS.md`. Pré-enregistrement : commit `daba713`.

- **« Inadapté »** :
  - ferritine après la ménopause (+196 %, 2,1 fois le changement détectable ; femmes de 45 à
    49 ans seulement) ;
  - glycémie à jeun ≥ 6,1 mmol/L après la ménopause (11,8 % contre 5,1 %) ;
  - protéines totales et globulines basses chez les femmes très actives (5 et 6 femmes sur 48).
- **Ailleurs, les décalages restent sous le changement détectable**, souvent entre 0,3 et 0,9 fois.
  Les plus forts : pilule (CRP ×2, vitamine D +46 %, TG +27 %) ; très actifs (CRP, GGT, insuline) ;
  favorisée (GGT, CRP, TG/HDL, HOMA-IR).
- **P1 non vérifiée.** Chez les très actifs, aucun excès de faux signaux pour la créatinine, le
  DFGe, l'ASAT ou l'hémoglobine.
- **Centile « population générale »** : la personne médiane du groupe favorisé et sain est à au
  moins 10 points du 50e centile pour 56 couples (marqueur, sexe) sur 133, et jusqu'à 26 points.
- **Attentes confirmées** : pilule 7/7 ; ménopause 6/9 ; très actifs 5/14 (2 non estimables,
  2 contredites sous réserve de la créatinine arrondie).
- **Écarts** :
  - seuils de vitamine D convertis en nmol/L (erreur d'unité repérée à la lecture des premiers
    résultats, taux recalculés ; décalages inchangés) ;
  - relance sur 4 processus après un arrêt pour manque de mémoire ;
  - régression médiane peu fiable pour la créatinine arrondie à 0,1 mg/dL (lecture par les
    moindres carrés) ;
  - ferritine mesurée seulement chez les femmes de moins de 50 ans, CK absente en 2003-2010 ;
  - analyses non pré-enregistrées signalées dans le rapport.

### Amendement d'interprétation — programme « panel », Q3 (2026-11-12)

Décision de l'auteur du projet, après lecture des résultats.

- **Portée de la règle.** La règle des faux signaux n'a de sens que pour les intervalles de
  référence statistiques (S).
- **Seuils fondés sur le risque (R).** Pour un seuil de décision clinique comme la glycémie à jeun
  ≥ 6,1 mmol/L, dépasser le seuil n'est pas un faux signal, même chez une personne « saine » :
  c'est un risque réel.
- **Glycémie à jeun après la ménopause.** Le classement « inadapté » est requalifié en « risque
  réellement plus élevé, seuil à conserver ».
- **Ferritine après la ménopause.** Elle reste « inadaptée », car c'est un intervalle statistique.
- **Conséquence pour la suite.** Toute règle de faux signaux appliquée à un seuil R sera désormais
  lue ainsi.
- **Données.** Les fichiers de données gardent la sortie brute de la règle pré-enregistrée.
- **Ajouts au rapport :**
  - contraception : un début ou un arrêt entre deux bilans fait bouger les marqueurs comme une
    intervention, et une CRP doublée peut mimer une inflammation. Le statut contraceptif doit être
    enregistré à chaque bilan et servir à interpréter les changements ;
  - très actifs : le groupe décrit des personnes actives, pas des athlètes de compétition ; la
    question reste ouverte pour eux.

### Pré-enregistrement — programme « panel », Q6 : zones fondées sur le risque (2026-11-12)

**Question.** Pour chaque marqueur, comment le risque de mortalité varie-t-il selon sa valeur ? Cette
relation correspond-elle aux bornes usuelles (table D1) ? Les zones décrivent un **risque associé**,
pas des cibles thérapeutiques.

Ce texte est complet : il ne renvoie à aucun brouillon. Les effectifs de décès par marqueur ont été
comptés avant toute analyse, sans relier un marqueur à la survie. Aucun modèle n'a été ajusté sur les
données NHANES : le modèle de Cox n'a été vérifié que sur des données simulées
(`tests/test_q6_cox.py`).

#### Données

- **Source.** NHANES 1999-2010, relié aux Linked Mortality Files 2019 (décès jusqu'au 31/12/2019).
- **Population.** Adultes de 20 à 79 ans (comme le score : l'âge est plafonné à 85 puis à 80 ans
  selon les cycles), non enceintes, éligibles au couplage (ELIGSTAT = 1), suivi connu.
  - Effectif : 27 175 personnes.
- **Découpage** (comme le score) :
  - développement : cycles 1999-2006 ;
  - validation : cycles 2007-2010.
- **Suivi principal tronqué à 10 ans** (120 mois après l'examen, horizon du score).
  - Le suivi médian complet est de 192 mois en développement contre 128 en validation. Sans
    troncature, les deux périodes ne seraient pas comparables, et l'hypothèse de risques
    proportionnels serait plus fragile sur 20 ans.
  - Décès à 10 ans : 1 842 en développement, 1 117 en validation.
  - Le suivi complet est une sensibilité (n° 6).
- **Issues.**
  - Principale : décès toutes causes.
  - Secondaires : décès cardiovasculaires (UCOD_LEADING 1 ou 5, comme le score) et par cancer
    (UCOD_LEADING 2), modèles par cause, les autres décès étant censurés.
    - Ils sont ajustés pour **tous** les marqueurs retenus. Le rapport les commente au moins pour
      les lipides, la glycémie, l'HbA1c, la CRP et le rein.
    - Même critère de réplication des côtés de risque, sans IC bootstrap des seuils. Décès à 10 ans :
    cardiovasculaires 544 et 290, cancers 497 et 323 (développement et validation).

#### Changements de méthode (règle de Q5, fixée par marqueur)

Pour chaque événement de Q5 situé entre 1999 et 2010, la règle est la suivante :
1. une équation publiée existe et les données diffusées ne sont pas déjà corrigées : on l'applique
   aux cycles antérieurs, en enchaînant jusqu'à la méthode de 2009-2010 ;
2. sinon, si le décalage empirique de Q5 (b) atteint au moins 0,5 changement détectable : on
   restreint aux cycles postérieurs ;
3. sinon : pas de correction.

| Marqueur | Événement Q5 | Choix |
|---|---|---|
| Créatinine (et DFGe, urée/créatinine) | 1 (1999), 2 (2005) | équations appliquées à 1999-2000 et à 2005-2006 ; l'événement 3 est déjà corrigé dans les données diffusées |
| Glycémie à jeun (et HOMA-IR, QUICKI, TyG) | 6, 7 | équations enchaînées : 1999-2004 (6 puis 7), 2005-2006 (7) |
| Insuline | 9, 10 | équations enchaînées : 1999-2002 (9 puis 10), 2003-2004 (10) |
| HDL (et rapports) | 13 | −2,45 % appliqué à 1999-2006 ; l'événement 14 vaut 0,07 changement détectable, pas de correction |
| Folates érythrocytaires | 22 | algorithme du NCHS (radio-essai → méthode microbiologique) sur 1999-2006 ; valeurs sans folates sériques ou sans hématocrite retirées |
| Créatinine urinaire (RAC) | 31 | équation appliquée à 1999-2006 |
| PAL, bilirubine | 4 (pas d'équation ; 0,77 et 0,90 changement détectable) | restriction à 2003-2010 |
| Phosphore | 4 (0,40) | pas de correction |
| Cholestérol total, TG | 15 (0,01) | pas de correction |
| HbA1c | 16 (0,16) | pas de correction |
| Vitamine D | 23a-c | valeurs diffusées, déjà exprimées en équivalent LC-MS/MS (2001-2010 ; absente en 1999-2000) |
| Autres marqueurs | aucun événement entre 1999 et 2010 | pas de correction |

Le journal des corrections (marqueur, événement, cycles, n) est écrit dans `Q6_methodes.json`.

#### Marqueurs (liste fixée avant analyse)

- **Règle.**
  - On part des marqueurs du panel (liste de Q1).
  - On exclut les hormones sexuelles et les PSA (exclues de D1 : elles dépendent du sexe, du cycle
    ou de l'âge).
  - On garde les marqueurs présents en 1999-2010 avec **au moins 1 000 décès à 10 ans**.
  - La **réplication** demande en plus au moins 250 décès dans chaque période.
- **Indices redondants retirés.** La glycémie moyenne estimée est une fonction affine de l'HbA1c ;
  l'indice athérogène est le log de TG/HDL. Avec une spline sur l'échelle log, leurs courbes seraient
  identiques à celles de l'HbA1c et de TG/HDL.
- **Raw urinaires remplacés.** L'albumine et la créatinine urinaires brutes sont remplacées par leur
  rapport (RAC), comme dans D1.

**Retenus avec réplication (68 marqueurs ; décès à 10 ans, développement / validation)** :
- **Numération (20)**, 1 705 / 1 016 décès :
  - leucocytes ;
  - neutrophiles, lymphocytes, monocytes, éosinophiles, basophiles (% et nombre) ;
  - hématies, hémoglobine, hématocrite ;
  - VGM, TCMH, CCMH, RDW ;
  - plaquettes, VPM.
- **Glycémie (4)** : glycémie à jeun (707 / 452), glycémie sérique, insuline à jeun (692 / 445),
  HbA1c.
- **Lipides (6)** : cholestérol total, LDL (691 / 445), HDL, TG à jeun (691 / 445), TG sériques,
  non-HDL.
- **Foie et protéines (8)** :
  - ALAT, ASAT, GGT ;
  - PAL et bilirubine (799 / 1 002, cycles 2003-2010) ;
  - albumine, protéines totales, globulines.
- **Rein et électrolytes (11)** :
  - créatinine, urée, DFGe (CKD-EPI 2021), RAC ;
  - sodium, potassium, chlorure, bicarbonates, calcium, phosphore ;
  - osmolalité calculée.
- **Autres (5)** : CRP, acide urique, fer sérique, folates érythrocytaires, vitamine D
  (1 238 / 931).
- **Indices dérivés (14)** :
  - glycémie et lipides : HOMA-IR, QUICKI, TyG, LDL/HDL, TG/HDL ;
  - foie : FIB-4, GGT/HDL, ASAT/ALAT ;
  - protéines et rein : albumine/globulines, urée/créatinine ;
  - électrolytes : osmolalité effective, calcium corrigé ;
  - numération : NLR, SII.

**Développement seulement, sans réplication possible** (pas de mesure en 2007-2010) : vitamine B12
(1 665 décès) et homocystéine (1 251). Leurs courbes sont rapportées comme **non répliquées** ; leur
catégorie D1 est « non estimable ».

**Exclus** :
- moins de 1 000 décès à 10 ans :
  - ferritine (936 ; femmes de moins de 50 ans seulement en 2005-2010) ;
  - CTF (935) et saturation de la transferrine (504) ;
  - TSH (963 ; laboratoires différents entre 1999-2002 et 2007-2010) ;
  - T4 libre (685, validation seulement) ;
  - ApoB (672) ;
- absents en 1999-2010 : Lp(a), ApoA1, sélénium, iode urinaire, magnésium, lipase.

#### Modèle

- **Type de modèle.** Cox, temps depuis l'examen, ex aequo de Breslow. Le code est en numpy,
  identique à lifelines sans ex aequo (test unitaire).
- **Marqueur.**
  - Spline cubique restreinte à **4 nœuds, aux centiles 5, 35, 65 et 95** du développement
    (3 ddl).
  - Échelle log si Q1 utilise l'échelle log et que toutes les valeurs du développement sont
    positives ; sinon échelle additive.
  - Valeurs tronquées aux centiles 0,5 et 99,5 du développement.
- **Ajustement.** Âge (spline, 4 nœuds aux mêmes centiles) et sexe.
- **Marqueurs à jeun.** Sous-échantillon à jeun (WTSAF2YR > 0).
- **Courbe.**
  - HR par rapport au point de risque minimal, IC 95 % par la méthode delta. **Le minimum n'est
    cherché qu'entre les centiles 5 et 95** du marqueur (développement).
  - Chaque courbe est aussi rapportée **par rapport à la médiane** du marqueur (développement).
  - Tracée sur l'échelle de la variable, entre les centiles 1 et 99 du développement (grille de
    200 points).
  - Le point minimal est traité comme fixe : c'est une limite.
- **Interaction avec le sexe.**
  - Test du rapport de vraisemblance (3 ddl : spline × sexe), en développement puis en validation.
  - « Répliquée » si p < 0,01 en développement et p < 0,05 en validation. Les courbes par sexe sont
    alors rapportées en complément ; les catégories restent celles du modèle commun.
- **Interaction avec l'âge.**
  - Même test (spline × âge centré, linéaire), en développement puis en validation.
  - **Analyse secondaire : courbes séparées pour les 20-59 ans et les 60-79 ans.** Le nombre de
    décès est rapporté dans chaque tranche.
    - Ajustement sur 1999-2010 réunis, avec les nœuds et la grille du développement (tous âges).
    - **Non estimable sous 150 décès à 10 ans** dans la tranche.
    - Formes et seuils sont rapportés pour chaque tranche, sans réplication.
  - Le modèle est aussi ajusté chez les **30-55 ans** (population visée), sur 1999-2010 réunis
    (549 décès à 10 ans). C'est descriptif et non répliqué, avec le même minimum de 150 décès.

#### Définitions fixées à l'avance

- **Point de risque minimal** : valeur de la grille, **entre les centiles 5 et 95**, où le log-HR
  est le plus bas.
  - Pour une forme montante ou descendante, on indique si le minimum tombe sur une borne (5e ou 95e
    centile) : le risque continue alors probablement de baisser au-delà.
- **Référence médiane** : HR de chaque point par rapport à la médiane du marqueur, avec son IC
  delta. C'est une lecture complémentaire, qui ne sert pas aux définitions.
- **Zone de risque minimal** : valeurs contiguës au minimum où la borne basse de l'IC 95 % du HR
  reste sous 1,1.
- **Seuils de risque** : de chaque côté du minimum (restreint aux centiles 5-95), première valeur (en s'éloignant du minimum) où le
  HR (estimation ponctuelle) atteint 1,2, puis 1,5. Interpolation linéaire sur la grille. Pas de
  seuil si le HR n'atteint pas le niveau entre les centiles 1 et 99.
- **Formes** :
  - **plate** : aucun seuil 1,2 ;
  - **montante** : seuil 1,2 du côté haut seulement ;
  - **descendante** : seuil 1,2 du côté bas seulement ;
  - **en U** : seuil 1,2 des deux côtés, et 1,5 des deux côtés ou d'aucun ;
  - **en J** : seuil 1,2 des deux côtés, 1,5 d'un seul côté.
  - Relation en U au sens de la question : un seuil 1,2 existe des deux côtés (U ou J).
- **IC des seuils** : bootstrap des personnes en développement, **500 tirages** (calcul parallélisé),
  graine 2026. Si le temps de calcul ne le permet pas, on passe à 200 tirages et on le signale. Percentiles
  2,5 et 97,5 parmi les tirages où le seuil existe (au moins 20 tirages). La part des tirages où il
  existe est rapportée.

#### Réplication (critères fixés à l'avance)

On garde la forme du développement (nœuds, troncature, grille), et on ajuste le même modèle en
validation.

1. **Association retenue** si p global (3 ddl) < 0,05 en développement **et** en validation.
2. **Côté de risque retenu** si le seuil 1,2 existe de ce côté en développement **et** en validation,
   et que l'association est retenue.
3. **Relation en U retenue** si les deux côtés sont retenus.
4. **Valeur de seuil retenue** si le seuil 1,2 de validation tombe dans l'IC 95 % bootstrap du seuil
   de développement.
5. **Forme retenue** : celle qui découle des côtés retenus. Sans association retenue : « non
   répliquée ».

Tous les marqueurs sont rapportés, retenus ou non.

#### Catégories (comparaison aux bornes D1)

- **Bornes.**
  - Intervalles S de D1 par sexe. Si D1 a partitionné par âge, on prend la tranche 40-59 ans, au
    centre de la population visée.
  - Seuils R de D1 dans le sens du seuil : glycémie à jeun 100 (ADA) et 110 (OMS) mg/dL ; HbA1c 5,7
    et 6,0 % ; LDL 116 ; non-HDL 130 ; TG à jeun 150 mg/dL ; DFGe 60 ; RAC 30 mg/g ; vitamine D 20
    et 30 ng/mL, convertis en nmol/L (×2,4959).
- **Seuils utilisés.** Seuls comptent les seuils 1,2 retenus en validation. On prend leur estimation
  de développement et son IC bootstrap.
- **Catégorie par côté**, pour une borne b de D1 :
  - **conforme au risque** : b est dans l'IC 95 % du seuil 1,2 ;
  - **intervalle trop large** : l'IC du seuil 1,2 est entièrement du côté normal de b. Des valeurs
    jugées normales sont déjà associées à un HR ≥ 1,2 ;
  - **intervalle trop strict** : l'IC du seuil 1,2 est entièrement au-delà de b, ou aucun seuil n'est
    retenu de ce côté alors que b est entre les centiles 1 et 99. Des valeurs signalées anormales
    n'ont pas de HR ≥ 1,2 ;
  - **non estimable** : b est hors des centiles 1 à 99, marqueur sans réplication, ou méthode
    différente de celle de D1.
    - C'est le cas des folates érythrocytaires : D1 est en radio-essai 2003-2006 et en ng/mL, alors
      que Q6 est harmonisé vers la méthode microbiologique.
- **Catégorie du marqueur** :
  - **« relation en U non signalée »** si la relation en U est retenue mais que la référence D1 n'a
    qu'un côté (seuil R) ;
  - sinon, la liste des catégories par côté et par sexe, par exemple « trop large (haut, H et F) ;
    trop strict (bas, F) ».
- **Indices dérivés sans borne D1.** Seules la courbe et les zones sont rapportées.

#### Sensibilités (contre la causalité inverse et la confusion)

Chaque sensibilité est ajustée sur le développement et comparée à l'analyse principale de
développement.

1. Exclusion des décès des 3 premières années (36 mois).
2. Population sans maladie connue : critères complets de la population de référence D1.
   - Cotinine < 3 ng/mL et IMC de 18,5 à 30.
   - Sans diabète, maladie cardiovasculaire, hépatique, rénale ni cancer déclarés.
   - Sans antidiabétique, antihypertenseur ni hypolipémiant.
3. Ajustement supplémentaire :
   - tabac (jamais, ancien, actuel, inconnu ; SMQ020 et SMQ040) ;
   - IMC (spline, 4 nœuds) ;
   - diabète déclaré (DIQ010) ;
   - revenu (INDFMPIR, avec indicatrice de donnée manquante).
4. Lipides et glycémie seulement : ajustement sur les traitements déclarés.
   - Hypolipémiant (BPQ100D), antihypertenseur (BPQ050A), antidiabétique (DIQ050 ou DIQ070).
   - Marqueurs concernés : cholestérol total, LDL, HDL, TG, non-HDL, LDL/HDL, TG/HDL, TyG, glycémies,
     HbA1c, insuline, HOMA-IR, QUICKI.
5. Poids d'enquête : WTMEC2YR, ou WTSAF2YR pour les marqueurs à jeun. Estimations ponctuelles
   seulement.
6. Suivi complet (jusqu'à 2019), sans troncature à 10 ans.

- **Ce qu'on appelle un changement net de forme.** Par rapport à l'analyse principale de
  développement :
  - un côté de risque (seuil 1,2) apparaît ou disparaît ;
  - ou le seuil 1,2 sort de l'IC 95 % bootstrap principal.
- **Interprétation pré-enregistrée.** Un marqueur dont la forme change nettement aux sensibilités 1 ou
  2 est signalé comme **marqueur de maladie probable plutôt que facteur de risque**. Sa zone reflète
  alors au moins en partie des maladies présentes à l'examen.

#### Prédictions (formes attendues, d'après des sources lues)

- **Ce qui est lu.** La colonne « Base » le dit pour chaque prédiction :
  - **« résumé seulement »** : seul le résumé a été lu, même quand le texte intégral a été
    téléchargé ;
  - **« texte intégral, passages »** : des passages du texte intégral ont été lus.

  Toutes les prédictions reposent sur un résumé seulement, sauf celle des lymphocytes (Zidar 2019).
- **Recherches.** Les requêtes PubMed sont dans `private/panel/Q6_litterature/recherches.json` (40
  requêtes, une ou plusieurs par marqueur).
- **Marqueurs sans source.** Un marqueur sans source lue n'a pas de prédiction.
- **Vérification.** Une prédiction est vérifiée si les côtés de risque **retenus en validation**
  correspondent aux côtés prévus. Elle est aussi rapportée sur le développement seul.

| Marqueur | Forme attendue (côtés de risque) | Source lue | Base |
|---|---|---|---|
| ALAT | descendante (ALAT basse) | Liu 2014, méta-analyse : ALAT basse associée à une mortalité plus élevée chez les plus âgés ; association jugée incohérente | résumé seulement |
| GGT | montante | Cho 2023, Corée, 9,7 millions | résumé seulement |
| PAL | montante | Yan 2023, NHANES 1999-2014 ; Li 2014, méta-analyse | résumé seulement |
| Bilirubine | montante | Chen 2021, NHANES 1999-2014 : association positive, linéaire, avec la mortalité toutes causes | résumé seulement |
| Albumine | descendante | Di Castelnuovo 2024, Moli-sani : association inverse, nette seulement à 65 ans et plus | résumé seulement |
| HDL | en U | Huang 2020 : risque aux deux extrêmes (≤ 30 et > 70 mg/dL) | résumé seulement |
| LDL | en U | Johannesen 2020, Copenhague | résumé seulement |
| Cholestérol total | en U | Yi 2019, Corée, 12,8 millions | résumé seulement |
| TG à jeun | plate | Fang 2022, NHANES : pas d'association chez les personnes à jeun | résumé seulement |
| TG sériques (non à jeun) | montante | Fang 2022 | résumé seulement |
| RDW | montante | Patel 2010, méta-analyse de personnes âgées | résumé seulement |
| VGM, TCMH | en U | Li 2024, NHANES 1999-2008 | résumé seulement |
| CCMH | descendante | Li 2024 : courbe en L | résumé seulement |
| Leucocytes | montante | Wang 2018, Guangzhou | résumé seulement |
| NLR | montante | Song 2021, NHANES | résumé seulement |
| Lymphocytes (nombre) | descendante | Zidar 2019, NHANES | texte intégral, passages |
| Sodium | en U | Mohan 2013, NHANES 1999-2004 ; côté bas aussi chez Zhang 2026 | résumé seulement |
| Potassium | montante | Zhang 2026, NHANES ; Liu 2021, Chine | résumé seulement |
| Chlorure | descendante | Mavragani 2023, NHANES : courbe en L | résumé seulement |
| DFGe | descendante | Matsushita 2010, méta-analyse CKD-PC : risque plat entre 75 et 105, croissant en dessous | résumé seulement |
| RAC | montante | Matsushita 2010 | résumé seulement |
| Acide urique | en U | Zhao 2025, NHANES 1999-2010 | résumé seulement |
| Glycémie à jeun | en U ou en J | Zhou 2019, Chine | résumé seulement |
| HbA1c | en U ou en J | Li 2019, HRS ; Inoue 2021, NHANES, pour le côté bas | résumé seulement |
| Insuline à jeun | plate | Zhang 2017, méta-analyse : RR 1,13, non significatif | résumé seulement |
| HOMA-IR | montante | Zhang 2017 | résumé seulement |
| CRP | montante | Emerging Risk Factors Collaboration 2010 | résumé seulement |
| Vitamine D | descendante | Garland 2014, méta-analyse | résumé seulement |
| Phosphore | montante | Li 2014 | résumé seulement |
| Bicarbonates | descendante | Raphael 2013, NHANES III : risque sous 22 mmol/L | résumé seulement |
| Urée | montante | Hong 2023, NHANES 1999-2006 | résumé seulement |
| Urée/créatinine | en U | Shen 2022, NHANES | résumé seulement |
| FIB-4 | montante | Anstee 2024, personnes obèses ou diabétiques : indirect | résumé seulement |
| Homocystéine (développement seulement) | montante | Fan 2017, méta-analyse | résumé seulement |

- **Sans source lue, donc sans prédiction** :
  - numération : neutrophiles (% et nombre), lymphocytes (%), monocytes, éosinophiles, basophiles,
    hématies, hématocrite, VPM, SII ;
  - glycémie et lipides : glycémie sérique, non-HDL, QUICKI, TyG, LDL/HDL, TG/HDL ;
  - foie et protéines : ASAT, protéines totales, globulines, albumine/globulines, GGT/HDL, ASAT/ALAT ;
  - rein et électrolytes : créatinine, calcium, calcium corrigé, osmolalités ;
  - autres : fer, folates érythrocytaires, B12.
- **Rien trouvé avec ces requêtes** pour l'hémoglobine et les plaquettes en population générale :
  les études trouvées portaient sur des patients.
- **Écart avec les exemples de l'auteur.** Il citait le potassium en U ; les sources lues ne décrivent
  que le côté haut. La prédiction suit les sources.

Références (DOI) :
- Liu 2014, 10.1371/journal.pone.0091410 ;
- Jensen 2020, 10.2147/CLEP.S241292 (lu, non utilisé : issues de morbidité) ;
- Cho 2023, 10.1038/s41598-022-25970-0 ;
- Yan 2023, 10.3389/fendo.2023.1217369 ;
- Li 2014, 10.1371/journal.pone.0102276 ;
- Chen 2021, 10.3389/fcvm.2021.670768 ;
- Di Castelnuovo 2024, 10.1016/j.eclinm.2024.102627 ;
- Huang 2020, 10.2147/CIA.S271528 ;
- Johannesen 2020, 10.1136/bmj.m4266 ;
- Yi 2019, 10.1038/s41598-018-38461-y ;
- Fang 2022, 10.1002/hsr2.642 ;
- Patel 2010, 10.1093/gerona/glp163 ;
- Li 2024, 10.1371/journal.pone.0307609 ;
- Wang 2018, 10.1186/s12889-018-6073-6 ;
- Song 2021, 10.1038/s41598-020-79431-7 ;
- Zidar 2019, 10.1001/jamanetworkopen.2019.16526 ;
- Mohan 2013, 10.1016/j.amjmed.2013.07.021 ;
- Zhang 2026, 10.1002/cdt3.70041 ;
- Liu 2021, 10.1007/s11606-021-07111-x ;
- Mavragani 2023, 10.2196/49291 ;
- Matsushita 2010, 10.1016/S0140-6736(10)60674-5 ;
- Zhao 2025, 10.3389/fnut.2025.1569798 ;
- Zhou 2019, 10.1016/j.cdtm.2018.08.001 ;
- Li 2019, 10.1210/jc.2018-02536 ;
- Inoue 2021, 10.1093/ije/dyaa263 ;
- Zhang 2017, 10.1042/BSR20170947 ;
- Emerging Risk Factors Collaboration 2010, 10.1016/S0140-6736(09)61717-7 ;
- Garland 2014, 10.2105/AJPH.2014.302034 ;
- Raphael 2013, 10.1093/ndt/gfs609 ;
- Hong 2023, 10.3390/nu15020461 ;
- Shen 2022, 10.1080/0886022X.2022.2030359 ;
- Anstee 2024, 10.1016/j.lanepe.2023.100780 ;
- Fan 2017, 10.1038/s41598-017-05205-3 ;
- Stack 2014, 10.1093/qjmed/hcu045 (lu ; saturation de la transferrine, marqueur exclu) ;
- Xu 2023, 10.1016/S2213-8587(23)00227-9 (lu ; TSH, marqueur exclu).

#### Livrables

- Rapport : `reports/panel/Q6_ZONES.md`, avec une figure par marqueur dans `reports/panel/figures_q6/`.
  Chaque figure montre :
  - la courbe de HR de développement (IC 95 %) et la courbe de validation ;
  - les intervalles S de D1 par sexe et les seuils R ;
  - les lignes HR = 1,2 et 1,5.
- Données :
  - `Q6_marqueurs.csv` (liste, décès, échelle, choix de méthode) et `Q6_methodes.json` ;
  - `Q6_courbes.csv` (HR et IC sur la grille, développement et validation) ;
  - `Q6_zones.csv` (minimum, zone, seuils, IC bootstrap, forme, réplication, catégories D1,
    interactions) ;
  - `Q6_causes.csv` (cardiovasculaire, cancer) ;
  - `Q6_sensibilites.csv` (6 sensibilités, changement net de forme) ;
  - `Q6_30_55.csv` ;
  - `Q6_predictions.json`.
- Ajout des résultats à `resultats_par_marqueur.csv` et aux fiches (livrables finaux).
- Code : `src/aging_clock/panel/q6.py` (données, méthodes, analyses) et
  `src/aging_clock/panel/q6_modele.py` (Cox, courbes, seuils).

#### Limites (section du rapport)

- **Association, pas causalité.** Une zone ne dit pas qu'amener un marqueur dans la zone réduit le
  risque. Les sensibilités 1 à 4 ne corrigent qu'en partie la causalité inverse et la confusion.
- **Mortalité seule.** Pas de morbidité, de qualité de vie ni d'événements non mortels.
- **Population américaine**, mesurée en 1999-2010, aux méthodes de laboratoire de l'époque. Les
  traitements ont changé depuis, notamment les statines plus répandues.
- **Traitements.** Les personnes traitées ont des valeurs modifiées par leur traitement. La
  sensibilité 4 ne s'applique qu'aux lipides et à la glycémie, et les traitements sont déclarés.
- **Une mesure unique.** Le bruit de mesure (Q1) atténue les pentes et élargit les zones.
- **Nombre de tests.** Les seuils p sont fixés, mais 68 marqueurs et plusieurs issues multiplient
  les tests : la réplication en validation sert de garde-fou.
- **Point minimal.** Il est traité comme fixe dans l'IC delta ; le bootstrap des seuils en tient
  compte. Sa recherche est limitée aux centiles 5-95 : hors de cette plage, la courbe est trop
  incertaine pour servir de référence.
- **Effectifs.** Les marqueurs à jeun ont moitié moins de décès. L'analyse des 30-55 ans
  (549 décès) est descriptive.

#### Décisions de l'auteur du projet (validation du 2026-11-12)

1. **Ajouts validés.** Troncature à 10 ans ; 1 000 décès à 10 ans et 250 par période ;
   interaction avec le sexe ; comparaison aux bornes D1 des 40-59 ans.
2. **Point de référence.** Le minimum est cherché entre les centiles 5 et 95. Les courbes sont aussi
   rapportées par rapport à la médiane. On signale un minimum tombé sur une borne pour les formes
   montantes ou descendantes.
3. **Âge.** Courbes 20-59 et 60-79 ans en analyse secondaire, avec le nombre de décès ; non estimable
   sous 150 décès.
4. **Causes.** Mortalité cardiovasculaire et par cancer en analyse secondaire, au moins pour les
   lipides, la glycémie, l'HbA1c, la CRP et le rein (ici : tous les marqueurs).
5. **Bootstrap.** 500 tirages, parallélisés ; 200 en repli signalé.
6. **Prédictions.** Celles qui reposent sur un résumé seulement sont marquées.

### Résultat — programme « panel », Q6 (2026-11-12)

Rapport : `reports/panel/Q6_ZONES.md`. Pré-enregistrement : commit `705e3d7`.

- **Formes.** 68 marqueurs testables. Après réplication :
  - 37 en U ou en J ;
  - 14 montants ;
  - 11 descendants ;
  - 6 non répliqués : basophiles (% et nombre), VPM, TG à jeun, TG sériques, TG/HDL.
- **Comparaison aux bornes D1** (179 comparaisons par sexe et par côté) :
  - 90 « trop larges » ;
  - 42 « trop strictes » ;
  - 22 « conformes » ;
  - 22 « non estimables » ;
  - 3 relations en U non signalées : DFGe, HbA1c, non-HDL.
- **Seuils R.**
  - Conformes : glycémie à jeun 110 mg/dL (OMS), HbA1c 5,7 et 6,0 %, vitamine D 20 ng/mL.
  - Trop stricts pour la mortalité : glycémie à jeun 100 mg/dL (ADA), LDL 116, non-HDL 130, TG 150,
    vitamine D 30 ng/mL.
  - Trop large : RAC 30 mg/g (risque dès 4,7 mg/g).
- **Prédictions.** 17 sur 34 vérifiées.
- **Marqueurs de maladie probables** (sensibilité 1) : côtés bas des leucocytes, des neutrophiles,
  de la CRP, du phosphore et du calcium corrigé ; côtés hauts de la bilirubine, du chlorure et des
  bicarbonates.
- **Écarts.**
  - Minimum de 100 décès (sensibilité 2 et causes) fixé dans le code mais absent du texte
    pré-enregistré.
  - La sensibilité 2 (138 décès) manque de puissance : la règle signale 54 marqueurs sur 58. Ce
    signal n'est pas utilisé pour classer (interprétation non pré-enregistrée).
  - Figures redessinées après analyse (présentation seulement).
  - Le bootstrap de 500 tirages a été fait.
