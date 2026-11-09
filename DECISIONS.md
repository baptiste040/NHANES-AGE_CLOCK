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
- Constantes publiées retenues (0,09165 ; 141,50). Plusieurs implémentations publiques, dont
  le prototype de ce dépôt, utilisaient 0,090165 et 141,50225 : écart documenté ; le C n'en
  dépend pas (PhenoAge est une fonction croissante de M).
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
