# Signatures d'intervention multi-marqueurs

Piste « signatures ». Protocole pré-enregistré dans `DECISIONS.md` (commit `29ba1ce`).
Code : `src/aging_clock/signatures/`. Données : fichiers `signatures_*.csv` et `.json` de ce dossier.

> **Corrections d'erreurs du 2026-11-12** (audit indépendant ; section dédiée en fin de rapport et
> `DECISIONS.md`). L'analyse principale à 6 mois ajoute désormais un bruit à long terme à **tous** les
> marqueurs (toutes les études longues EFLM, notes A, B et C) ; l'ancienne version, où seules l'ALAT et
> l'ASAT en recevaient un notable, devient une **borne optimiste**. Les effets absolus sont convertis en %
> avec les médianes de 2001-2002 (comme Q1 corrigé), la créatinine de NHANES III est recalibrée, et les
> seuils « naïfs » de la partie A suivent la même hypothèse de bruit. Tous les chiffres ci-dessous sont
> ceux d'après correction.

**Question.** Un marqueur seul ne détecte pas, chez une personne, l'effet d'une intervention d'hygiène
de vie en 6 mois (programme « panel », Q1). Une combinaison de marqueurs y arrive-t-elle, avec un taux
de fausses alertes contrôlé ? Elle peut exploiter la forme de l'effet et la structure corrélée du
bruit.

## À lire avant les chiffres

- **Données.** Paires de remesures NHANES : les mêmes personnes, à environ 2 semaines.
  - **Calibration** : NHANES 2001-2002, 403 paires complètes. Elle fixe la covariance du bruit et les
    seuils.
  - **Évaluation** : NHANES III, 1 292 paires complètes, indépendant (autres laboratoires, autre
    époque).
- **Deux horizons.**
  - **2 semaines** : les paires réelles.
  - **6 mois** : on ajoute par **simulation** une variabilité biologique à long terme, tirée de toutes
    les études longues EFLM (notes A, B et C). Elle existe et dépasse le CV_I à court terme pour 16
    marqueurs sur 18 (pas pour l'urée ni les plaquettes). Avec les seules études A/B, 6 marqueurs
    seulement recevaient un ajout (et non 7 comme écrit avant : pour les plaquettes, l'ajout est nul),
    et il n'était notable que pour l'ALAT et l'ASAT. L'horizon de 6 mois sert à l'interprétation.
- **Effets d'intervention.** Ce sont des **moyennes de méta-analyses**, souvent chez des personnes
  malades (obésité, stéatose, syndrome métabolique), et souvent assemblées à partir de plusieurs
  études (`signatures_vecteurs_sources.csv`). La sensibilité suppose que chaque personne reçoit une
  part aléatoire de l'effet moyen : `k ~ N(1 ; 0,5²)`.
- **Panel.** 18 marqueurs mesurables sans jeûne. La CRP est exclue du panel principal : dans
  NHANES III, 62 % de ses valeurs sont à la limite de détection. Elle est testée en sensibilité, dans
  2001-2002 seulement.

## Revue (étape 0) : ce qui existe, ce qui manque

- **Les changements de référence (RCV) sont univariés.** Toute la littérature de la variation
  biologique les calcule analyte par analyte : `RCV = √2 · z · √(CV_A² + CV_I²)`. Les intervalles de
  référence personnalisés prolongent cette logique (Coskun 2022, R ; Sandberg 2023, R).
- **Le CV annuel est plus grand que le CV à court terme** pour 11 analytes sur 18 (Wang 2022, R).
  Cela confirme que les changements détectables à 2 semaines sont des bornes basses.
- **Les approches multivariées servent à repérer des erreurs**, pas des effets : delta checks
  (Randell 2019, R), distance de Mahalanobis entre deux bilans d'un patient (Furutani 1984, R).
- **La structure corrélée des bilans est décrite dans la population, pas dans le bruit
  intra-individuel.** Un « axe bien-être » réunit TG, insuline, LDL, leucocytes et HOMA-IR (Nat
  Commun 2021, TC).
- **Rien trouvé avec nos requêtes** sur :
  - une signature multi-marqueurs d'intervention d'hygiène de vie ;
  - un taux de fausses alertes multivarié calé sur de vraies paires ;
  - la covariance du bruit intra-individuel d'un panel de routine ;
  - la robustesse d'un détecteur aux pièges.

### L'analogie : le passeport biologique de l'athlète

- **Le principe** (revue de 2024, TC ; Sottas 2011, R ; Eleftheriou 2025, R). L'antidopage cherche,
  dans un profil de plusieurs marqueurs répétés chez une même personne, un effet de forme connue :
  l'EPO ou la transfusion.
  - Il combine les marqueurs en scores : l'OFF-score (hémoglobine et réticulocytes), et l'ABPS, qui
    réunit 7 paramètres et prédit le dopage « mieux que chaque paramètre seul ».
  - Il fixe des seuils personnels par un modèle bayésien adaptatif, avec une spécificité d'au moins
    99 %.
- **C'est exactement l'idée testée ici.** Mais notre cas est beaucoup plus difficile :

| | Passeport biologique | Suivi d'hygiène de vie |
|---|---|---|
| Taille de l'effet | grande, très directionnelle | petite : quelques % à 20 % sur quelques marqueurs |
| Prélèvements | nombreux, réguliers | deux bilans espacés de 6 mois |
| Laboratoires | un seul laboratoire accrédité par échantillon | plusieurs laboratoires, changements de méthode |
| Conditions | contrôlées (heure, hydratation, altitude notées) | jeûne et heure non enregistrés |
| Spécificité visée | ≥ 99 % | 95 % ici |
| Connaissance de l'effet | pharmacologie étudiée chez l'athlète | moyennes de méta-analyses, souvent chez des malades |

## Ce qu'il faut retenir

1. **Le problème est réel : sans changement, beaucoup de personnes ont des marqueurs « significatifs ».**
   - À 6 mois, **53 % (2001-2002) à 60 % (NHANES III)** des personnes sans intervention ont au moins
     un marqueur sur 18 au-delà de son changement détectable. **10 à 11 %** en ont au moins trois.
     (Avant la correction : 45 à 47 %, et 7 à 8 %.)
   - Les corrélations du bruit **réduisent** la part « au moins un » (attendue à 61-67 % si les
     marqueurs étaient indépendants). Elles **augmentent** la part « au moins trois » (6,1-8,6 %
     attendus) : les faux changements arrivent en grappes.
   - Seuils D1 : **40 à 51 %** des personnes ont au moins une valeur qui redevient normale (« fausse
     bonne nouvelle »). **60 à 65 %** à 6 mois en ont au moins une qui devient anormale.
2. **La signature fait mieux que le meilleur marqueur seul, pour les 5 interventions.**
   - À 6 mois et à 5 % de fausses alertes, la signature gagne de 4 à 18 points, avec des IC qui
     excluent 0 pour les cinq (aérobie : +4 [+1 ; +7]).
   - Mais elle reste **loin d'une détection fiable** : au mieux **2 personnes sur 5** (avant la
     correction : 1 sur 2).
   - **Les IC à 95 % intègrent l'incertitude du calage** : chaque tirage bootstrap (500) rééchantillonne
     les 403 paires de calibration, réestime la covariance, recale les seuils, puis rééchantillonne
     les personnes d'évaluation (`signatures_ic_recalage.csv`).

   | Intervention (effet moyen, `k ~ N(1 ; 0,5²)`) | **Signature, 6 mois [IC 95 %]** | Meilleur marqueur seul [IC 95 %] | Gain [IC 95 %] | Test global (Mahalanobis) | Signature, 2 semaines [IC 95 %] |
   |---|---|---|---|---|---|
   | Perte de poids de 7 kg | **41 % [37 ; 45]** | 23 % [20 ; 25] (ALAT) | +18 [+15 ; +21] | 11 % | 51 % [46 ; 59] |
   | Alimentation méditerranéenne | **40 % [37 ; 45]** | 22 % [20 ; 25] (ALAT) | +18 [+14 ; +22] | 11 % | 55 % [48 ; 65] |
   | Arrêt du tabac | **20 % [16 ; 26]** | 10 % [6 ; 16] (leucocytes) | +10 [+6 ; +14] | 10 % | 25 % [21 ; 37] |
   | Réduction de l'alcool (non interprétable, voir plus bas) | 19 % [15 ; 23] | 13 % [9 ; 17] (HDL) | +6 [+4 ; +8] | 9 % | 30 % [22 ; 44] |
   | Activité physique aérobie | **13 % [11 ; 16]** | 9 % [7 ; 11] (HDL) | +4 [+1 ; +7] | 9 % | 16 % [12 ; 23] |

   - Le test global de Mahalanobis, qui ne vise aucune intervention, ne détecte presque rien
     (9-11 %). C'est la direction connue de l'effet qui fait le gain.
   - **Effet nécessaire pour 80 % de détection à 6 mois** : 2 à 2,25 fois l'effet moyen pour la perte
     de poids et le méditerranéen, 3 fois pour le tabac, 3,75 fois pour l'alcool, 5,25 fois pour
     l'activité aérobie. Le meilleur marqueur seul demande 3,25 à 8,75 fois l'effet moyen.
   - **Le gain dépend de l'hypothèse de bruit à 6 mois** (fourchette demandée après l'audit) :

     | Gain de la signature, 6 mois (points) | Bruit A/B (borne optimiste) | **Bruit A/B/C (principal)** | Long terme corrélé |
     |---|---|---|---|
     | Perte de poids | +25 (41 / 17, ASAT) | **+18** (41 / 23, ALAT) | +17 (39 / 23) |
     | Méditerranéen | +3 (44 / 41, HbA1c) | **+18** (40 / 22, ALAT) | +22 (44 / 22) |
     | Arrêt du tabac | +15 (26 / 10) | **+10** (20 / 10) | +10 (21 / 11) |
     | Aérobie | +5 (15 / 11) | **+4** (13 / 9) | +5 (14 / 9) |

     Pour la perte de poids, le gain va donc de **+17 à +25 points** selon l'hypothèse de bruit. Avec
     les anciens vecteurs (médianes de NHANES III), il allait de +12 (A/B/C, chiffre de l'audit) à
     +21 (A/B, ancien chiffre publié). Le sens tient toujours : la signature fait mieux ; l'ampleur
     dépend du bruit supposé de l'ALAT et des marqueurs lipidiques, mal connu à 6 mois.
3. **Le gain dépend des enzymes hépatiques pour le méditerranéen, moins pour la perte de poids.**
   - Les effets de −25 % sur l'ALAT (−38 à −39 % avant la conversion par les médianes de 2001-2002)
     viennent de populations avec stéatose : ils sont probablement surestimés pour des personnes en
     bonne santé.
   - En les mettant à 0, la perte de poids détecte encore 25 %, contre 14 % pour le meilleur seul
     (gain +11 points, il tient).
   - Le méditerranéen ne garde presque plus de gain : 30 % contre 27 % (+3 points). Il repose alors
     sur l'HbA1c.
4. **Usage ciblé, oui ; usage global, non.**
   - Quand on ne teste que la signature du protocole prescrit, les fausses alertes observées dans
     NHANES III sont de **4 à 6 %**, sauf pour le méditerranéen (9,7 %). IC avec recalage : de [2 ; 6]
     (tabac) à [8 ; 12] (méditerranéen).
   - Quand on teste les 5 signatures à la fois, **25 %** [23 ; 29] des personnes sans intervention
     déclenchent au moins une alerte.
5. **Les signatures se recouvrent, et certains pièges les déclenchent.**
   - **Déclenchements croisés.** Une perte de poids déclenche la signature de l'activité aérobie
     dans 23 % des cas et celle du méditerranéen dans 24 %.
   - **Pilule.**
     - Le **début d'une pilule** déclenche la signature du méditerranéen dans 15 % des cas, celles
       de l'arrêt du tabac et de l'activité aérobie dans 9 % (15-16 % avant la correction).
     - Son **arrêt** déclenche celle de la réduction de l'alcool dans **21 %** des cas (34 % avant).
   - **Changement de laboratoire de biochimie** (Beckman → Roche) : il déclenche la signature de la
     perte de poids dans 14 % des cas, par l'ALAT et l'ASAT, et celle du méditerranéen dans 10 %.
   - **Prélèvement non à jeun** (effet chez une même personne) : peu d'effet, 3 à 11 %.
   - **Correction.** Une signature contrainte, rendue insensible aux directions de pièges, ne coûte
     presque rien en sensibilité (alcool : de 19 % à 17 %). La meilleure protection reste
     opérationnelle : **enregistrer le laboratoire et la contraception**.
6. **Plusieurs bilans.** Modèle gaussien, fixé à l'avance.
   - Avec des bilans à 6 et 12 mois et un seul bilan de départ, la perte de poids passe de 44 % à
     51 % et le méditerranéen de 40 % à 47 %.
   - **Avec un seul bilan de départ, aucune signature n'atteint 80 %**, quel que soit le nombre de
     bilans de suivi. Les plafonds vont de 19 % (activité aérobie) à 62 % (perte de poids), car le
     bruit du bilan de départ reste.
   - **Avec autant de bilans avant qu'après**, 80 % sont atteints en 5 bilans de chaque côté pour la
     perte de poids, 6 pour le méditerranéen, 11 pour le tabac, jamais pour l'alcool ni l'activité
     aérobie (jusqu'à 20). Le meilleur marqueur seul demande 14 à 19 bilans.
7. **Réduire l'alcool fait baisser le HDL.**
   - La signature de la réduction de l'alcool repose à 93 % sur une **baisse** du HDL.
   - Un affichage naïf présenterait donc un marqueur « dégradé » après une intervention bénéfique.
   - Cette signature n'est pas interprétable comme test de la réduction de l'alcool. Aucune source
     lue ne chiffre l'effet d'une réduction sur la GGT, et un essai chez des volontaires sains ne
     voit pas la GGT distinguer une consommation modérée de l'abstinence (Kechagias 2015, R).
   - Avec une GGT illustrative à −15 % (non sourcée), elle détecterait 27 %.

## Partie A : le problème, sur de vraies personnes sans changement

Seuil : changement détectable à 6 mois de Q1 (20-79 ans), avec la même hypothèse de bruit que
l'horizon de 6 mois (notes A, B et C ; correction du 2026-11-12), le même aux deux horizons. Paires
complètes sur les 18 marqueurs.

| Jeu | Horizon | Paires | Marqueurs au-delà (moyenne) | ≥ 1 marqueur | ≥ 1 si indépendants | ≥ 3 marqueurs | ≥ 3 si indépendants |
|---|---|---|---|---|---|---|---|
| 2001-2002 | 2 semaines | 403 | 0,56 | 34,5 % | 43,5 % | 5,2 % | 1,7 % |
| 2001-2002 | 6 mois | 403 | 0,92 | 52,8 % | 61,1 % | 9,9 % | 6,1 % |
| NHANES III | 2 semaines | 1 292 | 0,69 | 43,3 % | 50,8 % | 6,2 % | 2,9 % |
| NHANES III | 6 mois | 1 292 | 1,07 | 60,2 % | 66,9 % | 11,4 % | 8,6 % |

- **Avec la CRP** (2001-2002, 19 marqueurs) : 54,3 % au moins 1 et 11,0 % au moins 3, à 6 mois.
- **Transitions autour des seuils D1** (S, plus les seuils R de l'HbA1c et des TG) :

| Jeu | Horizon | Au moins une fausse bonne nouvelle (anormal → normal) | Au moins une valeur qui devient anormale |
|---|---|---|---|
| 2001-2002 | 2 semaines | 40,2 % | 43,2 % |
| 2001-2002 | 6 mois | 40,0 % | 60,1 % |
| NHANES III | 2 semaines | 47,5 % | 49,5 % |
| NHANES III | 6 mois | 50,8 % | 64,7 % |

Dans NHANES III, une partie de ces transitions vient d'intervalles D1 non transposables à ses
méthodes (ALAT, ASAT : voir Q4). La créatinine n'en fait plus partie depuis sa recalibration.

## Partie B : les signatures

### Bruit : covariance des variations chez une même personne

- **Estimation.** 2001-2002, 403 paires. Estimation robuste (écart absolu médian, corrélations de
  Spearman converties), puis rétrécissement de Ledoit-Wolf (coefficient 0,17).
- **Corrélations les plus fortes.** ALAT-ASAT 0,53 ; albumine-hémoglobine 0,44 ; cholestérol
  total-albumine 0,33 ; ALAT-GGT 0,31 ; cholestérol total-HDL 0,28 ; HDL-TG −0,25
  (`signatures_correlation_bruit.csv`).
- **Elles sont modestes, mais elles comptent.** La signature retire du bruit en combinant des
  marqueurs qui varient ensemble par hasard. C'est pourquoi elle dépasse les prédictions a priori,
  faites sous hypothèse d'indépendance.

### Contributions : ce qui porte chaque signature (6 mois)

Part de chaque marqueur dans le signal attendu (`signatures_contributions.csv`). Les marqueurs absents
du tableau pèsent moins de 1 %.

| Signature | Marqueurs principaux |
|---|---|
| Perte de poids | ALAT 31 %, ASAT 25 %, TG 15 %, cholestérol total 13 %, HDL 10 %, glycémie 5 % |
| Méditerranéen | ALAT 43 %, HbA1c 37 %, GGT 8 %, cholestérol total 4 %, glycémie 3 %, TG 3 % |
| Activité aérobie | HDL 40 %, cholestérol total 34 %, glycémie 21 %, TG 4 % |
| Réduction de l'alcool | HDL 93 %, TG 7 % |
| Arrêt du tabac | leucocytes 65 %, HDL 35 % |

À 2 semaines, l'ALAT porte 38 % (perte de poids) et 57 % (méditerranéen) du signal (71 % et 81 %
avant la conversion par les médianes de 2001-2002). À 6 mois, sa variabilité à long terme réduit sa
part pour la perte de poids ; pour le méditerranéen, l'HbA1c reçoit aussi un bruit à long terme et
l'ALAT reste en tête.

### Sensibilités

| Variante (6 mois) | Perte de poids : signature / meilleur seul | Méditerranéen | Aérobie | Tabac |
|---|---|---|---|---|
| **Principal (bruit A/B/C)** | 41 % / 23 % | 40 % / 22 % | 13 % / 9 % | 20 % / 10 % |
| Bruit A/B (ancienne analyse principale, borne optimiste) | 41 % / 17 % | 44 % / 41 % | 15 % / 11 % | 26 % / 10 % |
| Enzymes × 0,5 | 28 % / 14 % | 32 % / 27 % | 13 % / 9 % | 20 % / 11 % |
| Enzymes à 0 | 25 % / 14 % | 30 % / 27 % | 13 % / 9 % | 20 % / 11 % |
| Covariance non robuste | 40 % / 23 % | 40 % / 27 % | 12 % / 9 % | 20 % / 11 % |
| Long terme corrélé | 39 % / 23 % | 44 % / 22 % | 14 % / 9 % | 21 % / 11 % |
| Avec CRP (2001-2002, plis 1 / 2) | 36 % / 22 % ; 49 % / 24 % | 30 % / 21 % ; 50 % / 24 % | 12 % / 9 % ; 18 % / 11 % | 25 % / 13 % ; 21 % / 14 % |

- Les conclusions tiennent aux choix de covariance.
- Avec la CRP, les résultats sont du même ordre, mais très instables d'un pli à l'autre (200 paires
  par pli).

### Recouvrement entre signatures et pièges

- **Ce qui est mesuré.** La similarité (cosinus) dans la métrique du bruit à 6 mois.
- **Lecture.** Une valeur proche de 1 veut dire que les deux directions sont presque
  indiscernables ; une valeur négative, qu'elles vont en sens opposé.

| | Perte de poids | Aérobie | Méditerranéen | Alcool | Tabac |
|---|---|---|---|---|---|
| Perte de poids | 1 | 0,61 | 0,52 | −0,24 | 0,17 |
| Aérobie | 0,61 | 1 | 0,33 | −0,59 | 0,40 |
| Méditerranéen | 0,52 | 0,33 | 1 | −0,13 | 0,06 |
| Laboratoire, biochimie | 0,33 | −0,03 | 0,03 | −0,11 | 0,05 |
| Pilule | 0,03 | 0,13 | 0,14 | −0,34 | 0,23 |
| Non à jeun (même personne) | 0,35 | −0,02 | 0,27 | 0,07 | −0,16 |

- **Le recouvrement le plus fort** relie l'activité aérobie à la perte de poids (0,61), à l'arrêt du
  tabac (0,40), et en sens opposé à la réduction de l'alcool (−0,59), parce que toutes passent par le
  HDL.
- **Déclenchements croisés** (`signatures_declenchements_croises.csv`) :
  - une perte de poids déclenche la signature de l'activité aérobie dans 23 % des cas et celle du
    méditerranéen dans 24 % ;
  - un régime méditerranéen déclenche la perte de poids dans 18 % des cas.
  - **Une signature dit qu'il y a eu un changement compatible, pas lequel.**

### Pièges et correction

- **Pièges.** Taux de déclenchement à 6 mois, sur des personnes sans intervention, piège ajouté
  (`signatures_pieges.csv`). À comparer aux fausses alertes de base (4 à 10 %).
  - **Laboratoire de biochimie +** : perte de poids 14 %, méditerranéen 10 %, autres 4 à 5 %.
  - **Numération** : 3 à 10 %, sans effet net au-delà du niveau de base.
  - **Pilule, début** : aérobie 9 %, tabac 9 %, méditerranéen 15 %.
  - **Pilule, arrêt** : alcool 21 %.
  - **Non à jeun** : 3 à 11 %. Seul le méditerranéen est au-dessus de 10 %, mais il part de 9,7 %
    de fausses alertes de base.
- **Correction.** La signature contrainte est rendue insensible aux pièges qui la déclenchent au-delà
  de 10 % (`signatures_correction.csv`). Elle garde sa sensibilité :
  - perte de poids 40 % (contre 41 %) ;
  - méditerranéen 40 % (contre 40 %) ;
  - alcool 17 % (contre 19 %) ;
  - le tabac et l'aérobie ne sont plus déclenchés au-delà de 10 % par un piège à 6 mois : pas de
    correction.

## Levier du bilan de départ (recommandation de conception)

Amendement du 2026-11-12, demandé après les résultats (`signatures_levier_depart.csv`).

- **Modèle gaussien, effet maintenu, 5 % de fausses alertes.** Chaque mesure est la vraie valeur, plus
  une composante à long terme propre à la période, plus un bruit à court terme indépendant.
  - Les prélèvements rapprochés du départ partagent la composante à long terme.
  - Les bilans de suivi ont chacun la leur.
  - `Cov(Δ) = Σ_ct (1/b + 1/f) + (Ω/2)(1 + 1/f)`, avec `Σ_ct = Σ_2sem / 2`.
- **Les valeurs sont comparables entre elles**, pas avec le tableau principal (empirique).

| Prélèvements au départ | Bilans de suivi | Perte de poids | Méditerranéen | Arrêt du tabac | Aérobie |
|---|---|---|---|---|---|
| 1 | 1 (6 mois) | 44 % | 40 % | 28 % | 14 % |
| 2 | 1 | 48 % | 43 % | 32 % | 15 % |
| 3 | 1 | 50 % | 44 % | 34 % | 15 % |
| 1 | 2 (6 et 12 mois) | 52 % | 47 % | 34 % | 16 % |
| 2 | 2 | 57 % | 51 % | 40 % | 17 % |
| 3 | 2 | 60 % | 53 % | 43 % | 18 % |

**Recommandation (corrigée le 2026-11-12).**
- **Un deuxième prélèvement au départ** (quelques semaines avant le début du programme) apporte
  **+3 à +4 points** de détection (aérobie +1). **Un deuxième bilan de suivi en apporte davantage :
  +5 à +7 points** (aérobie +2). Le rapport disait avant « +5 à +6 points, autant qu'un deuxième
  bilan de suivi » ; c'était déjà un peu flatteur (perte de poids : +5 contre +7), et l'écart grandit
  avec un bruit à long terme pour tous les marqueurs. Des prélèvements rapprochés partagent la
  même variation à long terme, que seul un bilan espacé dans le temps moyenne.
- Le deuxième prélèvement au départ reste utile quand on ne peut pas attendre 12 mois.
- **Les deux ensemble** donnent +11 à +13 points pour la perte de poids, le méditerranéen et le tabac.
- **Un troisième prélèvement au départ** n'apporte plus que +1 à +2 points.

## Prédictions pré-enregistrées

| | Énoncé (résumé) | Observé (après correction) | Vérifiée | Avant la correction |
|---|---|---|---|---|
| P1 | Signature > meilleur seul pour au moins 4 interventions sur 5 (6 mois) | 5 sur 5 avec les IC qui intègrent le calage (aérobie : [+1 ; +7]) | **oui** | oui (4 sur 5) |
| P2 | Aucune signature à 80 % (6 mois) | maximum 41 % | **oui** | oui |
| P3 | Perte de poids et méditerranéen en tête, aérobie dernière | 41 %, 40 % ; aérobie 13 % | **oui** | oui |
| P4 | Fausses alertes ciblées entre 3 et 10 % pour au moins 4 sur 5 ; plus de 15 % avec les 5 | 5 sur 5 (méditerranéen 9,7 %) ; 25 % | **oui** | oui |
| P5 | Labo de biochimie : perte de poids et méditerranéen au-delà de 10 % | 14,2 % ; 10,3 % | **oui** | non (9,7 %) |
| P6 | Pilule : tabac au-delà de 10 % au début ; alcool au-delà de 10 % à l'arrêt | 9,3 % ; 21 % | non (de justesse) | oui (15 % ; 34 %) |
| P7 | Perte de poids et méditerranéen : cosinus > 0,7 et croisés > 30 % | 0,52 ; 24 % et 18 % | non | non |
| P8 | Non à jeun : moins de 10 % pour chaque signature | méditerranéen 11,2 % | non (de justesse) | non |
| P9 | Sans enzymes : le gain survit pour les deux ; sensibilités < 25 % | gain : perte de poids +11, méditerranéen +3 ; 25 % et 30 % | non | non |
| P10 | ALAT > 40 % du signal | 6 mois : 31 % et 43 % | non (méditerranéen seulement) | non |
| P11 | Un seul départ : jamais 80 % ; plan symétrique : perte de poids en 6 bilans au plus | plafonds de 19 à 62 % ; 5 bilans | **oui** | oui (4 bilans) |
| P12 | Alcool : pas de prédiction | — | — | — |

- **Prédictions a priori** (indépendance, CV de Q1) contre observé à 6 mois, signature (après
  correction ; avant entre parenthèses) :
  - perte de poids 46 % → 41 % (49 %) ;
  - méditerranéen 37 % → 40 % (50 %) ;
  - tabac 20 % → 20 % (26 %) ;
  - alcool 14 % → 19 % (29 %) ;
  - aérobie 12 % → 13 % (16 %).
- **Pourquoi l'observé était plus élevé avant la correction.** Les échelles robustes du bruit (écart absolu médian, 2001-2002)
  valent 0,55 à 0,88 fois celles tirées des CV de Q1 pour 14 marqueurs sur 18 : HDL 0,60, HbA1c 0,55,
  albumine 0,56. Les CV de Q1 sont gonflés par les queues épaisses. Les corrélations aident aussi la
  signature. Les seuils, eux, restent calés empiriquement : les fausses alertes ne sont pas sous-estimées
  pour autant.

## Conséquences pour un produit de suivi

1. **Un tableau de 18 marqueurs comparés un à un à leur seuil produit des faux changements chez plus
   d'une personne sur deux en 6 mois.** Afficher des flèches de tendance marqueur par marqueur
   induit en erreur.
2. **Quand on sait quel protocole la personne suit, une signature fait mieux qu'un marqueur seul.**
   Elle double environ la détection pour la perte de poids, le méditerranéen et le tabac. Mais elle ne
   détecte que 2 personnes sur 5 au mieux, avec une réponse moyenne.
   - **Il faut le dire ainsi** : « compatible avec l'effet attendu » ou « pas de changement
     détectable », jamais « votre programme n'a pas marché ».
3. **Pour une détection fiable (80 %), il faut des bilans répétés avant et après** l'intervention :
   5 de chaque côté pour la perte de poids. Deux bilans espacés de 6 mois ne suffisent pas. À coût
   égal, un bilan de suivi supplémentaire aide plus qu'un prélèvement supplémentaire au départ.
4. **Ne pas tester toutes les signatures à la fois** : 25 % de fausses alertes.
5. **Enregistrer le laboratoire et la contraception.** Le début ou l'arrêt d'une pilule et un
   changement de laboratoire imitent des signatures.
6. **Le HDL baisse quand on réduit l'alcool.** Une interface qui colore les marqueurs en
   « mieux / moins bien » pénaliserait un changement bénéfique.

## Limites

- **Horizon simulé.** Les 6 mois sont simulés. La variabilité à long terme vient de toutes les études
  longues EFLM (notes A, B et C), de qualité inégale et parfois peu nombreuses (GGT : 3 études). La
  version sans les études de note C est une borne optimiste ; la vraie valeur pour un laboratoire de
  routine peut être plus grande encore.
- **Fausses alertes à 6 mois en partie simulées.** La composante à long terme est tirée du même
  modèle en calage et en évaluation : à 6 mois, le contrôle des fausses alertes est en partie vrai
  par construction, ce n'est pas une validation indépendante sur NHANES III.
- **Vecteurs d'effet.**
  - Ce sont des moyennes, souvent chez des malades, souvent assemblées à partir d'études
    différentes.
  - Plusieurs composantes sont à 0 faute de chiffre lu (GGT et VGM pour l'alcool ; hémoglobine et VGM
    pour le tabac).
  - L'effet sur l'ALAT est probablement surestimé pour des personnes en bonne santé (voir les
    sensibilités).
  - Les effets absolus sont convertis en % par une médiane de population : le résultat dépend de
    l'enquête de référence (ALAT : 15 U/L dans NHANES III, 23 U/L en 2001-2002).
- **Hétérogénéité de réponse.** Elle est postulée, pas mesurée.
- **Taille et précision de la calibration.**
  - 403 paires pour une covariance à 18 dimensions.
  - Les IC du rapport intègrent maintenant l'incertitude du calage (amendement du 2026-11-12). Ils
    sont 2 à 5 fois plus larges que les IC initiaux, qui ne rééchantillonnaient que les personnes
    d'évaluation.
  - Les IC des sections « Sensibilités » et « Pièges » restent ceux de la version initiale : ils
    sont trop étroits.
- **Méthodes différentes entre les deux jeux.** C'est voulu pour l'indépendance, mais cela crée des
  écarts. Les fausses alertes un peu élevées du méditerranéen (9,7 %) en viennent probablement
  (HbA1c : Diamat dans NHANES III, Primus en 2001-2002).
- **CRP absente du panel principal** (censure dans NHANES III), alors qu'elle porte une partie de
  l'effet de l'alimentation et de l'activité.
- **Pièges.** Ce sont des effets moyens de NHANES. Les vrais écarts entre laboratoires de routine
  sont inconnus pour les lipides et la numération (Q5).

## Amendement du 2026-11-12 (demandé après les résultats)

1. **IC qui intègrent le calage.** Ils remplacent les IC initiaux du tableau principal et des fausses
   alertes.
2. **Levier du bilan de départ** (section dédiée).
3. **Repli technique.** Dans la covariance robuste, si l'écart absolu médian d'un marqueur vaut 0
   (valeurs arrondies, tirages bootstrap), on se replie sur l'écart interquartile, puis sur l'écart
   type. Le cas ne se produit pas dans l'analyse principale : ses résultats sont inchangés.

## Corrections d'erreurs du 2026-11-12 (audit indépendant)

1. **Bruit à 6 mois de tous les marqueurs (analyse principale).** Avant, l'ajout à long terme venait
   des seules études EFLM notées A/B : il était notable pour l'ALAT et l'ASAT, négligeable ou nul
   ailleurs. Le meilleur marqueur seul de la perte de poids (ALAT) était donc pénalisé, alors que la
   signature se reportait sur des marqueurs dont le bruit était sous-estimé : le gain était gonflé.
   Désormais : toutes les études longues (A, B et C) pour tous les marqueurs. L'ancienne version est
   rapportée comme borne optimiste (variante « bruit 6 mois A/B »).
2. **« 7 marqueurs extrapolés » corrigé en 6** (pour les plaquettes, le CV_I à long terme est plus
   petit qu'à court terme : rien n'est ajouté). Avec la nouvelle hypothèse : 16 sur 18.
3. **Conversion des effets absolus en %** avec les médianes des 30-55 ans de 2001-2002, comme Q1
   corrigé (jeu principal pour les méthodes changées depuis NHANES III). Ancien et nouveau vecteur
   (`signatures_vecteurs_avant_apres.csv`) :

   | Intervention | Marqueur | Avant (médianes NHANES III) | Après (médianes 2001-2002) |
   |---|---|---|---|
   | Perte de poids | ALAT | −38,7 % (médiane 15 U/L) | **−25,3 %** (23 U/L) |
   | Perte de poids | ASAT | −20,6 % (19 U/L) | **−17,8 %** (22 U/L) |
   | Perte de poids | TG | −23,7 % (118 mg/dL) | −23,0 % (122 mg/dL) |
   | Perte de poids | HDL | +6,7 % (48 mg/dL) | +6,9 % (47 mg/dL) |
   | Méditerranéen | ALAT | −37,7 % | **−24,6 %** |
   | Méditerranéen | GGT | −10,9 % | −10,5 % |
   | Méditerranéen | TG ; glycémie ; HDL | −10,4 % ; −3,2 % ; +2,7 % | −10,1 % ; −3,1 % ; +2,8 % |
   | Aérobie | HDL ; TG ; glycémie | +4,4 % ; −6,8 % ; −2,9 % | +4,5 % ; −6,6 % ; −2,8 % |
   | Arrêt du tabac | HDL ; leucocytes | +8,1 % ; −11,6 % | +8,2 % ; −11,3 % |
   | Réduction de l'alcool | HDL ; TG | −8,3 % ; −4,8 % | −8,5 % ; −4,7 % |

   Les composantes déjà en % dans les sources (glycémie de la perte de poids, HbA1c et cholestérol
   total du méditerranéen, CRP) ne changent pas.
4. **HbA1c.** Le bruit de l'HbA1c suit Q1 corrigé (méthode moderne de 2001-2002) dans les seuils naïfs
   de la partie A et dans l'ajout à long terme.
5. **Créatinine de NHANES III recalibrée** (0,960 x − 0,184) dans les paires d'évaluation.

**Décomposition** (`signatures_decomposition_corrections.csv`, même graine) :

| 6 mois, perte de poids / méditerranéen | Anciens vecteurs | Nouveaux vecteurs |
|---|---|---|
| Bruit A/B | 49 / 28 (+21) ; 50 / 41 (+9) — ancienne publication | 41 / 17 (+25) ; 44 / 41 (+3) |
| Bruit A/B/C | 53 / 41 (+12) ; 53 / 40 (+13) — recalcul de l'audit | **40 / 23 (+17) ; 40 / 22 (+18)** — principal |

Les deux corrections tirent en sens opposés pour le gain de la perte de poids : le bruit de tous les
marqueurs le réduit (+21 → +12), la conversion par les médianes de 2001-2002 le relève (+12 → +17),
parce qu'elle réduit surtout l'effet sur l'ALAT, donc la force du meilleur marqueur seul. Les
sensibilités absolues baissent dans tous les cas.

**Conclusions qui changent** : détection au mieux de 2 personnes sur 5 (et non 1 sur 2) ; gain
significatif pour les 5 interventions ; un deuxième bilan de suivi aide plus qu'un deuxième
prélèvement au départ ; P5 devient vérifiée, P6 ne l'est plus.

## Écarts au pré-enregistrement

- **Effectif d'évaluation.** 1 292 paires complètes dans NHANES III, contre 1 288 annoncées dans le
  pré-enregistrement. Le compte préalable incluait la CRP (19 marqueurs) ; le panel principal en a 18.
- **Meilleur marqueur seul du méditerranéen.** Avant la correction, à 6 mois, c'était l'HbA1c ; avec
  le bruit à long terme de tous les marqueurs, c'est l'ALAT, comme dans la prédiction a priori. Le
  pré-enregistrement le fait choisir sur 2001-2002, ce qui a été respecté.
- **Aucun autre écart.**
