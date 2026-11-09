# Score de vieillissement biologique par système

Un score de vieillissement biologique par système, conçu pour être appliqué à
des cohortes de check-up de prévention.

Le score est appris sur des **décès réels** : enquêtes NHANES (CDC) chaînées aux
Linked Mortality Files du NCHS, jusqu'à 20 ans de suivi. Il peut ainsi être
appliqué tel quel à des cohortes récentes qui n'ont pas encore accumulé
d'événements. Il produit :

- un **âge biologique global** et son écart à l'âge chronologique ;
- un **âge biologique par système** : cardiovasculaire, métabolique, rénal,
  hépatique, inflammatoire/hématologique.

## Méthode

1. Un modèle de Cox (âge, sexe, marqueurs du panel) prédit le risque de décès à 10 ans.
2. Un modèle de référence (âge, sexe) donne le risque attendu à chaque âge.
3. L'âge biologique est l'âge qui, sur la courbe de référence du même sexe, donne le
   même risque. Un âge par système suit la même méthode avec les seuls marqueurs du système.

Tout est entraîné sur les cycles 1999-2006 puis **figé**. La validation porte sur des
cycles jamais vus (2007-2010). Les transformations (plancher de détection, log,
splines cubiques restreintes, winsorisation) sont apprises sur le développement et
font partie du modèle.

## Panels configurables

Un panel décrit ce que mesure la cohorte cible : variables, unités, système,
transformations, plages acceptées. Il est indépendant de la source de données.

```
config/
  panels/checkup_standard.yaml   # panel « check-up de prévention standard »
  sources/nhanes.yaml            # correspondance NHANES -> variables canoniques, par cycle
  study.yaml                     # découpage, horizon, bootstrap, sensibilités
```

Pour ajouter un panel, il suffit d'écrire un nouveau YAML dans `config/panels/`
avec le même schéma (voir l'en-tête de `checkup_standard.yaml`), puis de lancer
le pipeline avec `--panel <nom>`.

## Utilisation

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # Windows
pip install -e .
python -m aging_clock validate --panel checkup_standard   # télécharge NHANES au premier lancement
pytest
```

Les résultats sont écrits dans `reports/<panel>/` : `RESULTATS.md`, tables CSV et figures.

## État

- **Jalon 1 (fait)** : panels YAML, harmonisation NHANES 1999-2010, validation
  temporelle (C avec IC bootstrap, gain de C, HR par écart-type, calibration à 10 ans),
  indépendance des écarts par système, sensibilités (décès précoces, antécédents,
  causes de décès).
- **Jalon 2** : analyses pondérées, imputation multiple, tranches d'âge, AUC
  dépendante du temps, benchmark PhenoAge, validation secondaire 2015-2018 (hs-CRP),
  audit d'équité, puis modèle figé exportable (JSON + module de calcul autonome).

## Données

NHANES et les Linked Mortality Files sont des données publiques du CDC/NCHS.
Elles sont téléchargées automatiquement dans `data/raw/` (non versionné).
