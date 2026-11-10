# Q4 — Agrégation en une note globale

Protocole pré-enregistré (`DECISIONS.md`, « Suivi, Q4 », commit `585f211`) ; prédictions sur le
développement et les paires de 2001-2002 ; test sur la validation 2007-2010 (9 276 personnes) et sur
les paires de NHANES III (n = 781). Modèle : « sang seul contraint ». Code : `src/aging_clock/q4.py`.
Données : `Q4_predictions.json`, `Q4_resultats.json`.

> **Borne basse** pour la fiabilité : remesures à environ 2 semaines.

**Options comparées** (en années d'écart d'âge) :
- le **score global** du modèle ;
- la **moyenne** des 5 systèmes ;
- une **moyenne pondérée par un Cox**, avec les poids cardio 0,18, métab 0,16, rénal 0,21,
  hépat 0,21 et inflam 0,24 ;
- le **pire système** ;
- un **hybride**, moyenne + λ × (pire − moyenne), avec λ = 0,1 choisi par validation croisée.

Chaque agrégat entre dans un Cox âge + sexe + agrégat ajusté sur le développement.

## Résultats

| Option | C validation [IC 95 %] | ΔC vs global [IC 95 %] | O/E ; pente | CCI NHANES III | P95 \|d\| (ans) | P95 / ET entre personnes | R1 / R2 |
|---|---|---|---|---|---|---|---|
| **Global** | **0,850** [0,838 ; 0,862] | — | 0,92 ; 0,99 | 0,873 | 6,99 | 1,04 | référence |
| Moyenne | 0,847 [0,835 ; 0,859] | −0,0029 [−0,0041 ; −0,0017] | 0,91 ; 1,00 | 0,881 | 1,90 | 0,95 | oui / oui |
| Cox | 0,848 [0,835 ; 0,859] | −0,0025 [−0,0036 ; −0,0014] | 0,92 ; 1,00 | 0,881 | 2,09 | 0,95 | oui / oui |
| Pire système | 0,838 [0,826 ; 0,850] | **−0,0119** [−0,0154 ; −0,0086] | 0,95 ; 1,02 | **0,818** | 5,54 | 1,39 | **non / non** |
| Hybride (λ = 0,1) | 0,847 [0,835 ; 0,859] | −0,0027 [−0,0041 ; −0,0015] | 0,92 ; 1,00 | 0,882 | 2,04 | 0,95 | oui / oui |

Le système désigné comme « pire » est le même aux deux examens dans 71 % des paires (même chiffre
que le système prioritaire de Q1).

## Cas « un système très défavorable, tout le reste excellent »

Il s'agit des personnes avec un seul système au-dessus de son 90ᵉ centile et tous les autres sous
leur médiane. Validation : **142 personnes, 12 décès**. Le système en cause est le cardio 56 fois,
le métab 31, le rénal 23, l'hépatique 16 et l'inflammatoire 16. Risque observé à 10 ans : 8,1 %
[4,6 ; 14,3].

| Option | Note moyenne du sous-groupe (ans) | Risque prédit | O/E [IC 95 %] |
|---|---|---|---|
| Global | **−4,9** | 6,8 % | 1,19 [0,67 ; 2,10] |
| Moyenne | −1,5 | 6,8 % | 1,19 [0,67 ; 2,09] |
| Cox | −1,6 | 6,7 % | 1,21 [0,68 ; 2,13] |
| Pire système | +4,2 | 10,5 % | 0,77 [0,43 ; 1,36] |
| Hybride | −0,9 | 7,4 % | 1,10 [0,62 ; 1,93] |

## Conclusions (règles fixées à l'avance)

- **R1 et R2** : le **pire système est écarté**. Il perd 0,012 de C et il est le moins fiable (CCI
  0,82). La moyenne, le Cox et l'hybride passent les deux règles, mais restent un peu moins
  discriminants que le global, d'environ 0,003.
- **R3** : avec 12 décès, l'IC de l'O/E du global va de 0,67 à 2,10. On **ne peut pas conclure**
  que le global sous-estime le risque de ces personnes. Il ne « masque » pas un système défavorable
  au sens de la règle.
- **Décision : on garde le score global** comme note globale. Le système défavorable s'affiche
  **à côté** du score global, pas à sa place.
- Ces conclusions avaient toutes été prédites sur le développement.

## Lecture (interprétation)

- **Le message pose problème même si le risque est bien estimé.** Dans ce sous-groupe, le score
  global dit en moyenne « 4,9 ans plus jeune » alors qu'un système est au-dessus de son 90ᵉ
  centile. Le risque de décès semble correctement prédit, mais l'IC est large. Ce qui est trompeur,
  c'est la lecture « tout va bien » : il faut afficher le système défavorable à côté du score
  global.
- **Les agrégats moyennés semblent stables en années, mais c'est un effet d'échelle.** Leur P95 est
  de 2 ans, contre 7 pour le global, mais leur dispersion entre personnes est aussi trois fois plus
  petite. Rapporté à cette dispersion, le bruit est le même (environ 1 écart-type). Un « petit »
  seuil de changement en années ne veut donc pas dire une note plus fiable.
- **Le pire système prend toujours le maximum de 5 mesures bruitées.** Il est donc biaisé vers le
  haut, et il change souvent de système d'un examen à l'autre. Cela explique probablement sa
  moindre fiabilité. C'est une interprétation, non testée ici.
