# Score de vieillissement biologique par système

Un score de vieillissement biologique par système, conçu pour être appliqué à des cohortes
de check-up de prévention.

## La question

Les cohortes de prévention récentes mesurent de nombreux biomarqueurs mais n'ont pas encore
assez de recul pour observer des décès. Comment leur fournir un âge biologique **validé sur des
événements réels**, applicable tel quel à leurs données ?

Ce projet apprend un score sur une population suivie jusqu'à 20 ans, le valide sur des
participants jamais vus, le compare à la référence publiée (PhenoAge), audite son équité et sa
sensibilité aux méthodes de laboratoire, puis le fige dans un fichier autonome.

Pour chaque personne, il produit :

- un **âge biologique global** et son **écart** à l'âge chronologique ;
- un **âge biologique par système** : cardiovasculaire, métabolique, rénal, hépatique,
  inflammatoire/hématologique.

## Données

- **NHANES** (CDC), enquêtes nationales américaines 1999-2018 : biologie, tension,
  anthropométrie, questionnaires.
- **Linked Mortality Files 2019** (NCHS) : statut vital et cause de décès jusqu'au 31/12/2019
  (fichier public le plus récent).
- Adultes de 20 à 79 ans, hors grossesse, cas complets sur le panel.

| Échantillon | Cycles | n | Décès | Suivi médian |
|---|---|---|---|---|
| Développement | 1999-2006 | 13 903 | 2 796 | 16 ans |
| Validation temporelle | 2007-2010 | 9 276 | 978 | 11 ans |
| Validation secondaire | 2015-2018 | 8 421 | 164 | 3 ans |

Les données sont publiques et téléchargées automatiquement dans `data/raw/` (non versionné).

## Méthode

1. **Panel configurable.** Un fichier YAML décrit les mesures d'un check-up de prévention type (variables,
   unités, système, transformations, plages acceptées) ; un second fait la correspondance avec
   NHANES, cycle par cycle (noms de variables, conversions, recalibrations recommandées).
   Panel actuel « check-up de prévention standard » : 24 variables (`docs/specification_entrees.md`).
2. **Modèle.** Cox (âge, sexe, marqueurs ; log, splines cubiques restreintes, bornes apprises sur
   le développement) → risque de décès à 10 ans. Un Cox de référence (âge, sexe) donne le risque
   attendu à chaque âge. **L'âge biologique est l'âge auquel la référence du même sexe atteint le
   risque prédit.** Un âge par système suit la même méthode avec les seuls marqueurs du système.
3. **Validation sans fuite.** Tout est appris sur 1999-2006 puis figé ; la validation 2007-2010
   n'intervient jamais dans l'entraînement. Les choix (pénalisation, ajouts de variables) sont
   faits par validation croisée sur le développement, avec des critères **écrits avant chaque
   test** et consignés dans [`DECISIONS.md`](DECISIONS.md) ; la validation a été consultée une
   seule fois avec le panel final.
4. **Évaluation.** C de Harrell avec IC 95 % par bootstrap, gain de C par rapport à l'âge et au
   sexe, HR par écart-type de l'écart d'âge, calibration à 10 ans, analyses de sensibilité.

## Résultats clés

**Validation temporelle 2007-2010** — le score global sépare nettement mieux les décès que l'âge
et le sexe seuls, et il est bien calibré :

| Score | C (IC 95 %) | Gain de C vs âge + sexe | HR / écart-type d'écart | Obs./prédit 10 ans |
|---|---|---|---|---|
| Âge + sexe (référence) | 0,807 [0,794 ; 0,819] | — | — | — |
| **Global** | **0,853** [0,842 ; 0,865] | **+0,047** [0,040 ; 0,053] | 2,01 | 0,91 |
| Inflammatoire / hémato. | 0,833 | +0,026 | 1,67 | 0,95 |
| Hépatique | 0,830 | +0,024 | 1,59 | 0,96 |
| Métabolique | 0,819 | +0,013 | 1,47 | 0,93 |
| Rénal (créatinine + ACR) | 0,820 | +0,013 | 1,39 | 0,96 |
| Cardiovasculaire | 0,819 | +0,012 | 1,41 | 0,93 |

Résultats stables sans les décès des 2 premières années, chez les personnes sans antécédent
déclaré (C 0,838) et pour chaque cause de décès. Les écarts par système sont peu corrélés
(ρ ≤ 0,32) et restent tous associés à la mortalité quand ils sont ajustés ensemble.

**Comparaison à PhenoAge** (Levine 2018) sur les mêmes participants, différences de C par
bootstrap apparié :

- score global − PhenoAge publié : **+0,022** [+0,016 ; +0,027] ;
- score global − PhenoAge réentraîné avec notre méthode : +0,016 (apport des variables) ;
- PhenoAge réentraîné − publié : +0,005 (apport de la méthode) ;
- PhenoAge publié est mal calibré sur ces données (pente 0,71) ; réentraîné, il l'est bien.

**Équité** — pas de défaut de discrimination dans les sous-groupes (sexe, groupe ethnique, âge,
revenu, études). En revanche, le **risque absolu est surestimé chez les plus favorisés** (revenu
élevé : observé/prédit 0,62 ; diplôme universitaire : 0,70) et chez les Mexicains-Américains
(0,65), alors que leur classement reste bon. Les écarts plus élevés des personnes à faible revenu
correspondent à un surcroît de mortalité réellement observé.

**Méthodes de laboratoire** — en 2015-2018, des changements d'automates (RDW en 2013-2014,
biochimie et hs-CRP en 2017-2018) déplacent l'écart d'âge moyen de −1,1 an (harmonisé) à
**+1,9 an** (brut), sans changer le classement (C 0,85 dans les deux cas). Harmonisation par
équations de pontage NHANES ou, à défaut, recalage par quantiles par strates d'âge et de sexe.

**Fiabilité réelle** — sur des remesures à quelques semaines (NHANES 2001-2002, n = 388 ; NHANES III,
n = 781, indépendant du développement), protocoles pré-enregistrés. CCI de l'écart à l'âge (plus
exigeant que le CCI de l'âge biologique, d'environ 0,98) : **0,89 pour le score complet** (NHANES III,
seule source où tension, pouls et mensurations sont aussi remesurés) ; 0,92 pour la partie biologique
seule (2001-2002, mesures physiques fixées).
Un vrai changement entre deux bilans suppose un écart d'au moins **6,5 ans** pour le score global
(95ᵉ centile observé, CRP ≤ 10 mg/L). Le bruit a des queues épaisses et des variations corrélées
entre marqueurs : un intervalle gaussien n'est pas adapté
([`FIABILITE.md`](reports/checkup_standard/fiabilite_reelle/FIABILITE.md)).

## Suivi d'un bilan à l'autre

Ce qu'un score de santé peut affirmer entre deux bilans, dans le cas d'un check-up de prévention
avec un bilan complet au départ, puis une prise de sang tous les 6 mois. Scénario étudié :
un panel plus court que le bilan de départ (ici sans urines ni mesures physiques) ; l'heure et le
jeûne ne sont pas contrôlés.
Chaque question a été pré-enregistrée dans `DECISIONS.md` avant d'être évaluée. Synthèse :
[`SYNTHESE.md`](reports/checkup_standard/suivi/SYNTHESE.md).

> **Bornes basses.** Les remesures (NHANES 2001-2002 et NHANES III) ont lieu à environ 2 semaines.
> À 6 mois, le bruit sera plus grand. Les évaluations ne sont pas aveugles : NHANES III et la
> validation 2007-2010 avaient déjà été consultés.

**Modèle « sang seul contraint »** : 19 marqueurs sanguins et urinaires, sans mesures physiques.
Une **contrainte clinique** s'y ajoute : au-delà de la limite normale, une valeur ne rend jamais le
score plus favorable que la limite.
- Discrimination : C global 0,850 [0,839 ; 0,862] sur la validation 2007-2010.
- La contrainte ne dégrade pas la discrimination : +0,0008 de C, négligeable en pratique.
- Sans contrainte, une ALAT élevée rajeunissait le score hépatique d'environ 4 ans.

| Affirmation | Statut |
|---|---|
| « Votre score a changé » | seulement au-delà du seuil : **7,0 ans** pour le global (P95, NHANES III) |
| « Votre système le plus âgé est X » | non, comme fait stable : il change une fois sur trois en 2 semaines |
| « Les marqueurs qui pèsent le plus sont A, B, C » (sans ordre) | oui : au moins 2 sur 3 en commun dans 90 % des remesures |
| « Vos anomalies se sont améliorées » après une remesure ciblée | non sans groupe contrôle : 0,4 an d'amélioration fabriquée (global), 1,2 an (rénal) |
| Suivi du système rénal sans urines | non : aucune stratégie acceptable ; afficher le dernier score rénal, daté |
| Score global au bilan sans urines | oui, en recalculant le bilan 1 sans urines (C −0,004) |
| Note globale | le score global du modèle, avec le système le plus défavorable affiché à côté |

Les systèmes cardiovasculaire et métabolique « sang seul » apportent peu au-delà de l'âge pour la
mortalité à 10 ans. Ce critère sous-estime toutefois les lipides et la glycémie : ils ne doivent
pas être présentés comme inutiles.

Rapports : [`ETAPE0_SANG_SEUL.md`](reports/checkup_standard/suivi/ETAPE0_SANG_SEUL.md),
[`ETAPE1_CONTRAINTE.md`](reports/checkup_standard/suivi/ETAPE1_CONTRAINTE.md),
[`Q1_MOTEURS.md`](reports/checkup_standard/suivi/Q1_MOTEURS.md),
[`Q2_REGRESSION_MOYENNE.md`](reports/checkup_standard/suivi/Q2_REGRESSION_MOYENNE.md),
[`Q3_URINES.md`](reports/checkup_standard/suivi/Q3_URINES.md),
[`Q4_AGREGATION.md`](reports/checkup_standard/suivi/Q4_AGREGATION.md). Les marqueurs manquants
dans un système (Q5) n'ont pas été traités.

## Limites

- **Dosages** : un âge biologique absolu n'est interprétable que si les dosages de la cohorte
  sont comparables à ceux du développement (méthodes listées dans le modèle JSON) ou harmonisés.
- **Recalibrage** : une cohorte de check-up, souvent plus favorisée que la population générale,
  aura probablement un âge biologique surestimé sans recalibrage local ; le classement des
  personnes devrait rester valide.
- **Population** : adultes américains, 1999-2006 ; glycémie et triglycérides non à jeun ;
  domaine 20-79 ans ; analyses non pondérées.
- **Interprétation** : le score décrit un risque de mortalité toutes causes ; les âges par
  système ne sont pas des diagnostics d'organe ; les traitements (testés, non retenus) ne sont
  pas dans le modèle.
- Hypothèses non testées sur la surestimation chez les Mexicains-Américains (paradoxe hispanique,
  décès non retrouvés après un retour à l'étranger).
- **Suivi** : les seuils et taux de stabilité viennent de remesures à environ 2 semaines. Ce sont
  des bornes basses pour un suivi à 6 mois. Les évaluations de cette piste ne sont pas aveugles.
- **Limite connue : créatinine de 2005-2006 non recalibrée dans la table D1.** La table des seuils
  D1 (intervalles statistiques, NHANES 2003-2010, `intervalles.py`) n'applique pas la recalibration
  recommandée de la créatinine de 2005-2006 (0,978 x − 0,016 mg/dL), alors que le pipeline principal
  l'applique. L'effet est limité à la créatinine et au DFGe, dans les questions qui utilisent D1
  (Q3, Q4, Q6). Signalée par l'audit indépendant du 2026-11-12, non corrigée (analyses gelées).
- **Seuil de changement du score rénal.** Le seuil publié (**5,52 ans**, 2001-2002 et NHANES III
  regroupés) inclut les 388 personnes de 2001-2002 dont le premier examen a servi au développement.
  L'estimation indépendante de l'audit (NHANES III seul, sans CRP > 10 mg/L) est de **6,0 ans**. Les
  deux valeurs sont données ; la valeur du modèle (`models/seuils_changement_v1.json`) reste 5,52.
- Non fait à ce stade : analyses pondérées, imputation multiple, transposition à une cohorte non
  américaine (recalibrage, alignement des distributions), fiabilité à 6 mois, marqueurs manquants
  dans un système (Q5).

## Utiliser le modèle figé

```bash
python -m aging_clock score --input examples/exemple_entree_synthetique.csv [--uncertainty]
```

- `--uncertainty` ajoute, pour chaque score, le seuil empirique de changement significatif
  (`models/seuils_changement_v1.json`) et une alerte si la CRP dépasse 10 mg/L.

- Modèle : [`models/checkup_standard_v1.json`](models/checkup_standard_v1.json) (coefficients,
  transformations, survie de base, méthodes de dosage de référence, avertissements).
- Entrées : [`docs/specification_entrees.md`](docs/specification_entrees.md) ; exemple
  **entièrement synthétique** dans `examples/`.
- Le module de calcul (`src/aging_clock/score.py`) ne dépend que de NumPy et pandas.
- Fiche du modèle : [`docs/fiche_modele.md`](docs/fiche_modele.md).

## Reproduire

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # Windows
pip install -e .
git config core.hooksPath .githooks          # pre-commit : bloque le commit si pytest échoue
python -m aging_clock validate               # validation 2007-2010 (télécharge NHANES)
python -m aging_clock benchmark              # PhenoAge
python -m aging_clock equite                 # audit d'équité
python -m aging_clock secondaire             # validation 2015-2018
python -m aging_clock export                 # modèle JSON, spécification, exemple
pytest
```

Piste « suivi » (avec `PYTHONPATH=src`) :

```python
from aging_clock import sang_seul, suivi, contrainte, suivi_contraint, q3, q4
sang_seul.predictions(); sang_seul.run()                 # étape 0 : modèle sang seul
suivi.coherence(); suivi.predictions(); suivi.analyse()  # cohérence clinique ; Q1-Q2
contrainte.predictions(); contrainte.run()               # étape 1 : contrainte clinique
suivi_contraint.predictions(); suivi_contraint.analyse() # Q1-Q2 avec le modèle contraint
q3.predictions(); q3.analyse()                           # Q3 : urines absentes au second bilan
q4.predictions(); q4.analyse()                           # Q4 : agrégation en une note globale
```

| Dossier | Contenu |
|---|---|
| `config/` | panels, correspondance NHANES, harmonisation des dosages, paramètres d'étude |
| `src/aging_clock/` | pipeline (données, modèle, validation) et module de calcul autonome |
| `reports/checkup_standard/` | rapports : `RESULTATS.md`, `benchmark_phenoage/`, `equite/`, `secondaire/`, sélection de variables, `fiabilite_reelle/`, `fiabilite_nhanes3/`, `suivi/` |
| `reports/checkup_sang_seul/` | modèle « sang seul » (étape 0) et contrainte clinique (`contrainte/`) |
| `DECISIONS.md` | journal des décisions : critères pré-enregistrés, résultats, déviations |
| `models/`, `docs/`, `examples/` | modèle figé, fiche du modèle, spécification, exemple synthétique |

## Références

- Levine ME et al. An epigenetic biomarker of aging for lifespan and healthspan. *Aging* 2018.
  doi:10.18632/aging.101414
- Liu Z et al. A new aging measure captures morbidity and mortality risk across diverse
  subpopulations from NHANES IV. *PLoS Med* 2018 ; correction 2019, doi:10.1371/journal.pmed.1002760
- NCHS. Public-use Linked Mortality Files (2019).
