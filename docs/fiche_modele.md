# Fiche du modèle — panel `checkup_standard`

Modèle figé : `models/checkup_standard_v1.json` (coefficients, transformations apprises,
survie de base, méthodes de dosage de référence). Calcul : `python -m aging_clock score
--input fichier.csv` (NumPy et pandas uniquement). Entrées : `docs/specification_entrees.md`.

## Données d'entraînement

NHANES 1999-2006 chaînées aux Linked Mortality Files 2019 (NCHS) : 13 903 adultes de 20 à
79 ans, 2 796 décès, suivi médian 16 ans. Décisions de modélisation : `DECISIONS.md`.

## Performances (validation temporelle 2007-2010, n = 9 276, 978 décès)

| Score | C (IC 95 %) | Gain de C vs âge + sexe | HR par écart-type d'écart | Obs./prédit 10 ans |
|---|---|---|---|---|
| Global | 0,853 [0,842 ; 0,865] | +0,047 | 2,01 | 0,91 |
| Cardiovasculaire | 0,819 | +0,012 | 1,41 | 0,93 |
| Métabolique | 0,819 | +0,013 | 1,47 | 0,93 |
| Rénal | 0,820 | +0,013 | 1,39 | 0,96 |
| Hépatique | 0,830 | +0,024 | 1,59 | 0,96 |
| Inflammatoire / hémato. | 0,833 | +0,026 | 1,67 | 0,95 |

Détails : `reports/checkup_standard/` (validation, benchmark PhenoAge, équité, 2015-2018).

## Usage prévu

Estimer, pour un adulte de 20 à 79 ans vu en check-up de prévention, un âge biologique
global et par système, défini comme l'âge auquel le risque de décès à 10 ans de la
population de référence (même sexe) égale le risque prédit pour cette personne.

## Notes d'interprétation

- **Le score décrit un risque de mortalité, pas un état de santé « idéal ».** Un écart
  positif signifie un risque de décès supérieur à celui attendu pour l'âge et le sexe.
- **Traitements.** Dans la version actuelle, les traitements antihypertenseur et
  hypolipémiant ont été testés et **ne sont pas dans le modèle** (apport insuffisant en
  validation croisée, voir `DECISIONS.md`). Si des variables de traitement (antihypertenseur, hypolipémiant)
  figurent dans le modèle, elles signalent une maladie connue : elles augmentent le
  risque prédit, donc l'âge biologique, des personnes traitées. Le score **ne mesure pas
  l'effet protecteur des traitements** et ne doit pas être lu comme une incitation à les
  arrêter. À marqueurs égaux, une personne traitée a un risque plus élevé parce que sa
  maladie sous-jacente existe, pas parce que le traitement est nocif.
- Les âges par système décomposent le risque par groupe de marqueurs ; ils ne sont pas
  des diagnostics d'organe.

## Précision individuelle : changement significatif entre deux bilans

Mesurée sur des remesures réelles à quelques semaines d'intervalle : NHANES 2001-2002
(n = 388) et NHANES III (n = 781, indépendant du développement). Voir
`reports/checkup_standard/fiabilite_reelle/FIABILITE.md`.

- **Un intervalle gaussien (± 1,96 écart-type) n'est pas adapté.** Le bruit de mesure a des
  queues épaisses : la plupart des personnes varient peu, une minorité (épisode aigu, CRP
  élevée) varie beaucoup. Les variations des marqueurs sont en outre corrélées entre elles
  (dilution, posture, enzymes hépatiques). Aucun modèle de bruit simulé n'a reproduit la
  variabilité observée dans la réplication.
- **Seuils empiriques** (`models/seuils_changement_v1.json`, option `--uncertainty`) : un écart
  entre deux bilans est un vrai changement s'il dépasse le 95ᵉ centile des écarts observés.
  Valeurs, CRP ≤ 10 mg/L aux deux bilans : **global 6,5 ans** [IC 95 % 6,0 ; 7,1] ;
  cardiovasculaire 4,8 ; métabolique 2,8 ; rénal 5,5 ; hépatique 5,1 ; inflammatoire et
  hématologique 4,3. Les seuils rénal, hépatique et inflammatoire regroupent 2001-2002 et NHANES III :
  ils incluent les 388 personnes de 2001-2002 dont le premier examen a servi au développement. Seule
  estimation indépendante pour le rénal (NHANES III seul) : 6,0 ans sans CRP > 10 mg/L. Les deux
  valeurs sont à lire ensemble : 5,52 ans (publié, regroupé) et 6,0 ans (indépendant).
- **CRP > 10 mg/L à l'un des deux bilans** : pas de seuil fourni ; refaire le bilan avant de
  comparer. Toutes personnes confondues, le seuil global serait de 6,9 ans.
- Ce sont des **bornes basses** : remesures à 1-48 jours, même protocole, même personnel, même
  heure, échantillons non aléatoires. Entre deux check-ups espacés d'un an, avec un autre
  laboratoire ou une autre saison, le bruit sera plus grand.
- Fiabilité (CCI) observée du score global : 0,91 (partie biologique) et 0,89 (score complet).

## Limites

- **Dosages.** Un âge biologique absolu n'est interprétable que si les dosages sont comparables
  à ceux du développement ou harmonisés : en 2015-2018, des changements d'automates (RDW,
  biochimie) décalaient l'âge biologique moyen de près de 3 ans sans changer le classement.
- **Population d'entraînement** : adultes américains (NHANES), 1999-2006 ; glycémie non à jeun ;
  domaine de validité 20-79 ans.
- **Surestimation du risque absolu des groupes favorisés.** En validation (2007-2010), le modèle
  surestime la mortalité à 10 ans des personnes au revenu élevé (rapport observé/prédit 0,62
  pour un revenu ≥ 3,5 fois le seuil de pauvreté) et des diplômés de l'université (0,70), alors
  que leur classement reste bon (gain de C positif, pente de calibration proche de 1). Les
  biomarqueurs ne captent qu'une partie de l'avantage social.
- **Conséquence pour les cohortes de check-up de prévention.** Ces cohortes étant souvent plus
  favorisées que la population générale, l'âge biologique y sera probablement **surestimé sans
  recalibrage local** ; le classement relatif des personnes devrait rester valide.
- **Mexicains-Américains** : risque surestimé (observé/prédit 0,65). Les explications avancées
  (« paradoxe hispanique » de mortalité, décès non retrouvés après un retour à l'étranger) sont
  des **hypothèses non testées**.
- Détails : `reports/checkup_standard/equite/` (EQUITE.md, INTERPRETATION.md).
