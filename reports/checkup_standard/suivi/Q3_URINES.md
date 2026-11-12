# Q3 allégée — scénario : pas d'urines au suivi

Protocole pré-enregistré (`DECISIONS.md`, « Suivi, Q3 allégée », commit `ca1c2af`) ; calage
2001-2002 (n = 388), test sur les paires de NHANES III (n = 781) et sur la validation 2007-2010
(9 276 personnes). Modèle : « sang seul contraint ». Code : `src/aging_clock/q3.py`. Données :
`Q3_predictions.json`, `Q3_nhanes3.json`.

> **Borne basse.** Les remesures ont lieu à environ 2 semaines : aucun changement réel, tout
> changement affiché est faux. À 6 mois, sans contrôle de l'heure ni du jeûne, le bruit sera plus
> grand.

**Situation.** Le bilan 1 a l'ACR (urines), le bilan 2 ne l'a pas. Sans ACR, le système rénal se
réduit à la créatinine.

## Résultats NHANES III (paires) et validation 2007-2010

Seuils de référence T (P95 du panel complet en 2001-2002) : global 5,97 an ; rénal 4,43 an.
Marges : ±0,60 (global), ±0,44 (rénal).

| Stratégie | Score | d moyen [IC 95 %] | P95 \|d\| (rapport au complet) | Faux changement moyen [IC 95 %] | ΔC validation [IC 95 %] | Acceptable ? (a/b/c) |
|---|---|---|---|---|---|---|
| Panel complet (référence) | global | +0,15 [−0,11 ; +0,38] | 6,99 | — | — | — |
| Panel complet (référence) | rénal | +0,06 [−0,15 ; +0,26] | 5,88 | — | — | — |
| Imputation de l'ACR | global | +0,71 [+0,44 ; +0,97] | 7,41 (1,06) | **+0,56** [+0,38 ; +0,74] | −0,003 [−0,005 ; −0,001] | non (a) |
| Imputation de l'ACR | rénal | +0,87 [+0,61 ; +1,12] | 6,91 (1,18) | **+0,81** [+0,56 ; +1,07] | −0,004 [−0,006 ; −0,001] | non (a, b) |
| Marqueurs communs | global | +0,07 [−0,12 ; +0,27] | 5,60 (0,80) | −0,07 [−0,20 ; +0,07] | −0,004 [−0,006 ; −0,002] | **oui** |
| Marqueurs communs | rénal | −0,05 [−0,08 ; −0,01] | 0,95 (0,16) | −0,11 [−0,30 ; +0,10] | **−0,011** [−0,014 ; −0,008] | non (c) |
| Modèle dédié | global | +0,04 [−0,17 ; +0,26] | 6,01 (0,86) | −0,11 [−0,24 ; +0,04] | −0,003 [−0,004 ; −0,001] | oui |
| Modèle dédié | rénal | −0,09 [−0,15 ; −0,03] | 1,78 (0,30) | −0,15 [−0,34 ; +0,06] | **−0,010** [−0,013 ; −0,007] | non (c) |

Règles : (a) IC du faux changement moyen dans ±10 % de T ; (b) P95 ≤ 1,10 × celui du panel
complet ; (c) ΔC > −0,005. Le report de l'ACR du bilan 1 (sensibilité) donne exactement les mêmes
changements que les marqueurs communs.

**Deux pièges pour les stratégies 2 et 3** (P95 en années) :

| | Marqueurs communs, global | Marqueurs communs, rénal | Modèle dédié, global | Modèle dédié, rénal |
|---|---|---|---|---|
| Bilan 1 recalculé sans urines : écart moyen avec le bilan 1 complet ; P95 | −0,05 ; 4,7 | −0,07 ; 6,9 | +0,88 ; 4,8 | +0,98 ; 6,8 |
| Comparaison mixte (bilan 1 complet contre bilan 2 sans urines) : d moyen ; P95 | +0,02 ; **7,3** | −0,12 ; **7,2** | **+0,92** ; 7,6 | **+0,89** ; 7,1 |

## Conclusions (règles fixées à l'avance)

- **Score global** : « marqueurs communs » est acceptable (P95 5,60), « modèle dédié » aussi
  (6,01). On retient **les marqueurs communs**. Le prix : 0,004 de C, et un bilan 1 qu'il faut
  **recalculer sans urines** pour comparer.
- **Système rénal** : **aucune stratégie n'est acceptable**. Sans ACR, le rénal perd environ 0,01
  de C. L'imputation crée un faux vieillissement rénal d'environ 0,8 an en moyenne.
  - **Le système rénal n'est suivi qu'aux bilans avec urines.**
  - Entre deux, on affiche le dernier score rénal mesuré, daté, et on n'annonce **aucun changement
    rénal**.
- **Ce qu'il ne faut jamais faire** : comparer un bilan complet à un bilan sans urines sans
  recalculer le premier.
  - Le P95 du faux changement monte à environ 7 ans, pour le global comme pour le rénal.
  - Avec le modèle dédié, tout le monde « vieillit » en plus d'environ 0,9 an en moyenne.

**Prédictions** :
- Bien prédit : la conclusion (aucune stratégie rénale ; marqueurs communs retenus pour le global).
- Mal prédit :
  - le critère qui fait échouer le rénal : (c) seulement en NHANES III, contre (a) et (c) prévus ;
  - le biais de l'imputation, plus fort que prévu (global +0,56 contre +0,25).

## Lecture (interprétation)

- **Le rénal sans urines ne mesure plus la même chose.** La créatinine seule est stable (P95 de
  1 an), mais elle discrimine moins bien. Un score rénal « stable » au bilan sans urines n'est
  donc pas rassurant : il ignore la composante la plus variable et la plus informative.
- **L'imputation est biaisée hors de son échantillon de développement.** Elle est sans biais sur
  2007-2010, mais biaisée sur NHANES III. Une hypothèse possible, non testée : la distribution de
  l'ACR ou son dosage diffèrent entre les deux enquêtes. Les 18 marqueurs sanguins n'expliquent que
  17 % de la variance du log de l'ACR.
