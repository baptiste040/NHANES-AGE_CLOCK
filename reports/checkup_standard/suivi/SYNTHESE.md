# Ce qu'un score de santé peut affirmer d'un bilan à l'autre

Synthèse de la piste « suivi ». Contexte générique : un check-up de prévention fait un bilan
complet au départ, puis une prise de sang tous les 6 mois. Le panel est réduit, sans urines, sans
tension ni mensurations, et on ne contrôle ni l'heure ni le jeûne. Les protocoles, prédictions et
résultats sont datés dans `DECISIONS.md`. Le détail est dans les rapports de chaque étape (liste
en fin de document).

## Trois réserves à garder en tête

1. **Bornes basses.** Nos remesures ont lieu à environ 2 semaines, et en NHANES III à la même
   heure, avec le même protocole. Entre deux bilans à 6 mois, le bruit sera plus grand. Tous les
   seuils ci-dessous sont des **minimums**.
2. **Évaluations non aveugles.** NHANES III et la validation 2007-2010 avaient déjà été consultés.
   Chaque question a été pré-enregistrée avant le calcul de ses propres indicateurs. La reprise de
   Q1-Q2 avec le modèle contraint est une analyse secondaire.
3. **Le critère est la mortalité toutes causes à 10 ans.** Il sous-estime les facteurs de risque
   cardiovasculaire (lipides, glycémie), qui sont souvent traités et causaux à plus long terme. Les
   systèmes cardio et métab « sang seul » ne doivent pas être présentés comme inutiles.

## Le modèle retenu

**« Sang seul contraint »** : 19 marqueurs sanguins et urinaires, sans mesures physiques, avec
une contrainte clinique. Une valeur au-delà de la limite normale ne peut jamais rendre le score
plus favorable que la valeur limite.

| | Global, validation 2007-2010 |
|---|---|
| C [IC 95 %] | 0,850 [0,839 ; 0,862] |
| Gain sur âge + sexe | +0,044 |
| Contre le modèle complet (avec tension et mensurations) | −0,004 de C (étape 0) |
| Contre le modèle sans contrainte | +0,0008 : la contrainte ne dégrade pas la discrimination (différence détectable grâce à l'appariement, négligeable en pratique) |
| Calibration | O/E 0,90 ; pente 0,99 |

- **Sans contrainte**, le modèle récompensait des valeurs anormales. Une ALAT élevée, par exemple,
  rajeunissait le score hépatique d'environ 4 ans. Avec un seuil matériel de 1 an, 8,9 % des
  personnes auraient dû être signalées « à revoir par le médecin ».
- **Avec la contrainte**, plus aucune ne l'est.

## Ce qu'on peut affirmer, et ce qu'on ne peut pas

### 1. Un changement de score n'est réel qu'au-delà d'un seuil (Q1)

Le seuil est le P95 du changement sans aucun effet réel (NHANES III, modèle contraint).

| Score | Seuil minimal de changement |
|---|---|
| Global | **7,0 ans** |
| Rénal | 5,9 ans |
| Hépatique | 5,1 ans |
| Inflammatoire / hémato | 4,7 ans |
| Cardio (lipides) | 2,2 ans |
| Métab (glycémie, HbA1c) | 1,1 an |

- La version gaussienne ne convient pas : les queues sont lourdes.
- Les seuils cardio et métab sont petits en années, parce que ces systèmes varient peu entre
  personnes. Ce n'est pas le signe d'une plus grande fiabilité (voir Q4).
- **À affirmer** : « votre score a changé de plus que ce que la variabilité de mesure explique »,
  seulement au-delà de ces seuils.
- **À ne pas affirmer** : un changement plus petit, présenté comme une amélioration ou une
  dégradation.

### 2. Les moteurs : afficher un groupe, pas un classement (Q1)

Stabilité entre deux prises de sang à 2 semaines, sans aucun changement de santé :

| Élément affiché | Stable dans… | Règle des 80 % |
|---|---|---|
| Système prioritaire | 71 % des paires | non affichable comme fait stable |
| Premier moteur | 74 % (tous) ; 61 % (actionnables) | non affichable |
| Trio largement stable (au moins 2 sur 3 en commun), tous marqueurs | **90 %** | **affichable avec confiance** |
| Trio largement stable, marqueurs actionnables | 80 % | juste sous la limite |

- **À afficher** : un **groupe de 3 marqueurs** qui pèsent sur le score, sans ordre.
- **À ne pas afficher** :
  - « votre système le plus âgé est X » comme un fait stable ;
  - « votre premier facteur est Y ».
- Le VGM et les leucocytes sont « à interpréter par le médecin », jamais des moteurs actionnables.

### 3. Remesurer seulement les anomalies fabrique une amélioration (Q2)

Sans aucun effet réel, après retrait du décalage entre examens :

| Situation | Amélioration apparente |
|---|---|
| Remesure des seuls marqueurs anormaux, score global | 0,4 à 0,5 an |
| Même chose, système inflammatoire | environ 0,5 an |
| Système rénal chez les personnes à ACR anormale | **1,2 an** |
| Sélection des 20 % les plus « vieux » sur le score | **0,9 an** |

- Aucune correction statistique simple n'a passé le test : ni marqueur par marqueur, ni au niveau
  du score.
- **À affirmer** : une amélioration, seulement par **comparaison à un groupe contrôle**, ou au
  minimum par la remesure complète du panel avec soustraction du changement moyen de la population.
- **À ne pas affirmer** : « vos marqueurs anormaux se sont améliorés » après une remesure ciblée,
  comme preuve d'un effet du programme.

### 4. Les urines au suivi (Q3)

- **Score global** :
  - mettre l'ACR à la valeur de référence **aux deux bilans** (marqueurs communs) est
    acceptable : le bruit n'augmente pas et le C baisse de 0,004 ;
  - il faut **recalculer le bilan 1 sans urines** pour comparer.
- **Système rénal** : **aucune stratégie n'est acceptable**.
  - Sans ACR, le rénal perd environ 0,01 de C.
  - L'imputation de l'ACR crée un faux vieillissement d'environ 0,8 an.
  - **Le rénal n'est suivi qu'aux bilans avec urines.** Entre deux, on affiche le dernier score
    rénal mesuré, daté, et on n'annonce aucun changement rénal.
- **Interdit** : comparer un bilan complet à un bilan sans urines sans recalcul. Le faux
  changement atteint 7 ans au P95.

### 5. La note globale (Q4)

- **On garde le score global du modèle.** La moyenne des systèmes, la moyenne pondérée et
  l'hybride perdent environ 0,003 de C sans rien apporter. Le « pire système » perd 0,012 de C et
  il est le moins fiable.
- **À afficher à côté du score global** : le système défavorable.
  - Une personne dont un seul système dépasse son 90ᵉ centile, alors que tous les autres sont
    bons, a en moyenne un score global de « 4,9 ans plus jeune ».
  - Le risque semble correctement estimé, avec seulement 12 décès et un IC large. C'est la lecture
    « tout va bien » qui est trompeuse.

### 6. Données manquantes dans un système (Q5)

**En attente.** Elle n'a pas été traitée.

## Récapitulatif pour un produit de check-up

| Affirmation | Statut |
|---|---|
| Score global et âge par système au bilan complet | oui, avec la contrainte clinique |
| « Votre score a changé » | seulement au-delà du seuil (global ≥ 7 ans, borne basse) |
| « Votre système le plus âgé est X » | non, comme fait stable (71 %) |
| « Les marqueurs qui pèsent le plus sont A, B, C » (sans ordre) | oui (90 %) |
| « Vos anomalies se sont améliorées » après remesure ciblée | non, sans groupe contrôle |
| Suivi du système rénal sans urines | non |
| Score global au bilan sans urines | oui, avec le bilan 1 recalculé sans urines |
| Note globale | le score global du modèle, avec le système défavorable affiché à côté |
| Cardio et métab « sang seul » | ne pas les présenter comme inutiles : le critère de mortalité les sous-estime |

## Rapports de la piste

- `ETAPE0_SANG_SEUL.md` : modèle sans mesures physiques ;
- `ETAPE1_CONTRAINTE.md` : contrainte clinique et règle de signalement ;
- `Q1_MOTEURS.md` : seuils de changement et stabilité des moteurs, y compris l'analyse secondaire
  avec le modèle contraint ;
- `Q2_REGRESSION_MOYENNE.md` : régression vers la moyenne et groupe contrôle, y compris l'analyse
  secondaire ;
- `Q3_URINES.md` : urines absentes au second bilan ;
- `Q4_AGREGATION.md` : agrégation en une note globale.

Gel des analyses : 2026-11-10 (`DECISIONS.md`).
