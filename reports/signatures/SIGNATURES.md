# Signatures d'intervention multi-marqueurs

Piste « signatures ». Protocole pré-enregistré dans `DECISIONS.md` (commit `29ba1ce`).
Code : `src/aging_clock/signatures/`. Données : fichiers `signatures_*.csv` et `.json` de ce dossier.

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
  - **6 mois** : on ajoute par **simulation** la variabilité biologique à long terme de Q1, connue
    pour 7 marqueurs sur 18 (ALAT, ASAT, leucocytes, hémoglobine, VGM, RDW, plaquettes). Pour les
    11 autres, le bruit à 6 mois reste une borne basse. L'horizon de 6 mois sert à l'interprétation.
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
   - À 6 mois, **45 % (2001-2002) à 47 % (NHANES III)** des personnes sans intervention ont au moins
     un marqueur sur 18 au-delà de son changement détectable. **7 à 8 %** en ont au moins trois.
   - Les corrélations du bruit **réduisent** la part « au moins un » (attendue à 54-55 % si les
     marqueurs étaient indépendants). Elles **doublent** la part « au moins trois » (3,6-4,0 %
     attendus) : les faux changements arrivent en grappes.
   - Seuils D1 : **40 à 51 %** des personnes ont au moins une valeur qui redevient normale (« fausse
     bonne nouvelle »). **59 à 63 %** à 6 mois en ont au moins une qui devient anormale.
2. **La signature fait mieux que le meilleur marqueur seul, pour les 5 interventions.**
   - À 6 mois et à 5 % de fausses alertes, la signature gagne de 5 à 20 points.
   - Mais elle reste **loin d'une détection fiable** : au mieux 1 personne sur 2.

   | Intervention (effet moyen, `k ~ N(1 ; 0,5²)`) | **Signature, 6 mois** | Meilleur marqueur seul, 6 mois | Test global (Mahalanobis) | Signature, 2 semaines |
   |---|---|---|---|---|
   | Alimentation méditerranéenne | **50 %** | 41 % (HbA1c) | 11 % | 72 % |
   | Perte de poids de 7 kg | **49 %** | 29 % (ALAT) | 11 % | 68 % |
   | Réduction de l'alcool (non interprétable, voir plus bas) | 29 % | 15 % (HDL) | 10 % | 30 % |
   | Arrêt du tabac | **26 %** | 11 % (leucocytes) | 10 % | 26 % |
   | Activité physique aérobie | **16 %** | 10 % (HDL) | 10 % | 16 % |

   - Le test global de Mahalanobis, qui ne vise aucune intervention, ne détecte presque rien
     (10-11 %). C'est la direction connue de l'effet qui fait le gain.
   - **Effet nécessaire pour 80 % de détection à 6 mois** : 1,75 fois l'effet moyen pour la perte de
     poids et le méditerranéen, 2,5 fois pour le tabac et l'alcool, 4 fois pour l'activité aérobie.
     Le meilleur marqueur seul demande 2,25 à 6,5 fois l'effet moyen.
3. **Le gain dépend des enzymes hépatiques pour le méditerranéen, pas pour la perte de poids.**
   - Les effets de −38 à −39 % sur l'ALAT viennent de populations avec stéatose : ils sont
     probablement surestimés pour des personnes en bonne santé.
   - En les mettant à 0, la perte de poids détecte encore 31 %, contre 14 % pour le meilleur seul
     (gain +18 points, il tient).
   - Le méditerranéen, lui, ne garde plus de gain : 42 % contre 41 %. Il repose alors sur l'HbA1c,
     marqueur dont la méthode diffère entre les deux jeux (voir la réserve sur les fausses alertes).
4. **Usage ciblé, oui ; usage global, non.**
   - Quand on ne teste que la signature du protocole prescrit, les fausses alertes observées dans
     NHANES III sont de **4 à 7 %**, sauf pour le méditerranéen (10,4 %, porté par l'HbA1c).
   - Quand on teste les 5 signatures à la fois, **25 %** des personnes sans intervention déclenchent
     au moins une alerte.
5. **Les signatures se recouvrent, et certains pièges les déclenchent.**
   - **Déclenchements croisés.** Une perte de poids déclenche la signature de l'activité aérobie et
     celle du méditerranéen dans 28 % des cas.
   - **Pilule.**
     - Le **début d'une pilule** déclenche les signatures de l'arrêt du tabac, de l'activité aérobie
       et du méditerranéen dans 15 à 16 % des cas, par le HDL.
     - Son **arrêt** déclenche celle de la réduction de l'alcool dans **34 %** des cas.
   - **Changement de laboratoire de biochimie** (Beckman → Roche) : il déclenche la signature de la
     perte de poids dans 14 % des cas, par l'ALAT et l'ASAT.
   - **Prélèvement non à jeun** (effet chez une même personne) : peu d'effet, 4 à 12 %.
   - **Correction.** Une signature contrainte, rendue insensible aux directions de pièges, ne coûte
     presque rien en sensibilité, sauf pour l'alcool (de 29 % à 23 %). La meilleure protection
     reste opérationnelle : **enregistrer le laboratoire et la contraception**.
6. **Plusieurs bilans.** Modèle gaussien, fixé à l'avance.
   - Avec des bilans à 6 et 12 mois et un seul bilan de départ, la perte de poids passe de 54 % à
     61 % et le méditerranéen de 51 % à 59 %.
   - **Avec un seul bilan de départ, aucune signature n'atteint 80 %**, quel que soit le nombre de
     bilans de suivi. Les plafonds vont de 28 % (activité aérobie) à 71 % (perte de poids), car le
     bruit du bilan de départ reste.
   - **Avec autant de bilans avant qu'après**, 80 % sont atteints en 4 bilans de chaque côté pour la
     perte de poids et le méditerranéen, 8 pour le tabac, 12 pour l'alcool, jamais pour l'activité
     aérobie (jusqu'à 20). Le meilleur marqueur seul demande 10 à 19 bilans.
7. **Réduire l'alcool fait baisser le HDL.**
   - La signature de la réduction de l'alcool repose à 93 % sur une **baisse** du HDL.
   - Un affichage naïf présenterait donc un marqueur « dégradé » après une intervention bénéfique.
   - Cette signature n'est pas interprétable comme test de la réduction de l'alcool. Aucune source
     lue ne chiffre l'effet d'une réduction sur la GGT, et un essai chez des volontaires sains ne
     voit pas la GGT distinguer une consommation modérée de l'abstinence (Kechagias 2015, R).
   - Avec une GGT illustrative à −15 % (non sourcée), elle détecterait 42 %.

## Partie A : le problème, sur de vraies personnes sans changement

Seuil : changement détectable à 6 mois de Q1 (20-79 ans), le même aux deux horizons. Paires
complètes sur les 18 marqueurs.

| Jeu | Horizon | Paires | Marqueurs au-delà (moyenne) | ≥ 1 marqueur | ≥ 1 si indépendants | ≥ 3 marqueurs | ≥ 3 si indépendants |
|---|---|---|---|---|---|---|---|
| 2001-2002 | 2 semaines | 403 | 0,61 | 37,0 % | 46,6 % | 6,5 % | 2,1 % |
| 2001-2002 | 6 mois | 403 | 0,75 | 44,6 % | 53,7 % | 7,9 % | 3,6 % |
| NHANES III | 2 semaines | 1 292 | 0,63 | 39,7 % | 47,6 % | 5,9 % | 2,4 % |
| NHANES III | 6 mois | 1 292 | 0,78 | 47,1 % | 54,7 % | 7,4 % | 4,0 % |

- **Avec la CRP** (2001-2002, 19 marqueurs) : 47,0 % au moins 1 et 8,8 % au moins 3, à 6 mois.
- **Transitions autour des seuils D1** (S, plus les seuils R de l'HbA1c et des TG) :

| Jeu | Horizon | Au moins une fausse bonne nouvelle (anormal → normal) | Au moins une valeur qui devient anormale |
|---|---|---|---|
| 2001-2002 | 2 semaines | 40,2 % | 43,2 % |
| 2001-2002 | 6 mois | 40,1 % | 58,5 % |
| NHANES III | 2 semaines | 48,3 % | 51,6 % |
| NHANES III | 6 mois | 50,6 % | 62,7 % |

Dans NHANES III, une partie de ces transitions vient d'intervalles D1 non transposables à ses
méthodes (ALAT, ASAT, créatinine : voir Q4).

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
| Perte de poids | ALAT 32 %, ASAT 22 %, cholestérol total 15 %, HDL 14 %, TG 10 %, glycémie 7 % |
| Méditerranéen | HbA1c 38 %, ALAT 34 %, GGT 15 %, glycémie 4 % |
| Activité aérobie | HDL 46 %, cholestérol total 32 %, glycémie 24 % |
| Réduction de l'alcool | HDL 93 %, TG 7 % |
| Arrêt du tabac | HDL 51 %, leucocytes 49 % |

À 2 semaines, l'ALAT porte 71 % (perte de poids) et 81 % (méditerranéen) du signal. À 6 mois, sa
variabilité à long terme réduit sa part.

### Sensibilités

| Variante (6 mois) | Perte de poids : signature / meilleur seul | Méditerranéen | Aérobie | Tabac |
|---|---|---|---|---|
| Principal | 49 % / 29 % | 50 % / 41 % | 16 % / 10 % | 26 % / 11 % |
| Enzymes × 0,5 | 36 % / 14 % | 43 % / 41 % | 16 % / 10 % | 26 % / 11 % |
| Enzymes à 0 | 31 % / 14 % | 42 % / 41 % (gain non significatif) | 16 % / 10 % | 26 % / 11 % |
| Covariance non robuste | 49 % / 28 % | 51 % / 41 % | 17 % / 10 % | 26 % / 11 % |
| Long terme corrélé | 45 % / 28 % | 55 % / 41 % | 16 % / 10 % | 26 % / 11 % |
| Avec CRP (2001-2002, plis 1 / 2) | 48 % / 30 % ; 56 % / 28 % | 44 % / 28 % ; 51 % / 39 % | 12 % / 4 % ; 25 % / 13 % | 27 % / 7 % ; 31 % / 21 % |

- Les conclusions tiennent aux choix de covariance.
- Avec la CRP, les résultats sont du même ordre, mais très instables d'un pli à l'autre (200 paires
  par pli).

### Recouvrement entre signatures et pièges

- **Ce qui est mesuré.** La similarité (cosinus) dans la métrique du bruit à 6 mois.
- **Lecture.** Une valeur proche de 1 veut dire que les deux directions sont presque
  indiscernables ; une valeur négative, qu'elles vont en sens opposé.

| | Perte de poids | Aérobie | Méditerranéen | Alcool | Tabac |
|---|---|---|---|---|---|
| Perte de poids | 1 | 0,63 | 0,49 | −0,31 | 0,26 |
| Aérobie | 0,63 | 1 | 0,33 | −0,66 | 0,53 |
| Méditerranéen | 0,49 | 0,33 | 1 | −0,17 | 0,10 |
| Laboratoire, biochimie | 0,26 | 0,04 | −0,03 | −0,14 | 0,11 |
| Pilule | 0,08 | 0,22 | 0,12 | −0,38 | 0,29 |
| Non à jeun (même personne) | 0,22 | −0,08 | 0,21 | 0,06 | −0,15 |

- **Le recouvrement le plus fort** relie l'activité aérobie à la perte de poids (0,63), à l'arrêt du
  tabac (0,53), et en sens opposé à la réduction de l'alcool (−0,66), parce que toutes passent par le
  HDL.
- **Déclenchements croisés** (`signatures_declenchements_croises.csv`) :
  - une perte de poids déclenche la signature de l'activité aérobie dans 28 % des cas et celle du
    méditerranéen dans 28 % ;
  - un régime méditerranéen déclenche la perte de poids dans 20 % des cas.
  - **Une signature dit qu'il y a eu un changement compatible, pas lequel.**

### Pièges et correction

- **Pièges.** Taux de déclenchement à 6 mois, sur des personnes sans intervention, piège ajouté
  (`signatures_pieges.csv`). À comparer aux fausses alertes de base (4 à 10 %).
  - **Laboratoire de biochimie +** : perte de poids 14 %, méditerranéen 10 %, autres 5 à 6 %.
  - **Numération** : 3 à 11 %, sans effet net au-delà du niveau de base.
  - **Pilule, début** : aérobie 15 %, tabac 15 %, méditerranéen 16 %.
  - **Pilule, arrêt** : alcool 34 %.
  - **Non à jeun** : 4 à 12 %. Seul le méditerranéen est au-dessus de 10 %, mais il part de 10,4 %
    de fausses alertes de base.
- **Correction.** La signature contrainte est rendue insensible aux pièges qui la déclenchent au-delà
  de 10 % (`signatures_correction.csv`). Elle garde sa sensibilité :
  - perte de poids 49 % (contre 49 %) ;
  - méditerranéen 50 % (contre 50 %) ;
  - tabac 24 % (contre 26 %) ;
  - alcool 23 % (contre 29 %).

## Prédictions pré-enregistrées

| | Énoncé (résumé) | Observé | Vérifiée |
|---|---|---|---|
| P1 | Signature > meilleur seul pour au moins 4 interventions sur 5 (6 mois) | 5 sur 5 | **oui** |
| P2 | Aucune signature à 80 % (6 mois) | maximum 50 % | **oui** |
| P3 | Perte de poids et méditerranéen en tête, aérobie dernière | 49 %, 50 % ; aérobie 16 % | **oui** |
| P4 | Fausses alertes ciblées entre 3 et 10 % pour au moins 4 sur 5 ; plus de 15 % avec les 5 | 4 sur 5 (méditerranéen 10,4 %) ; 25 % | **oui** |
| P5 | Labo de biochimie : perte de poids et méditerranéen au-delà de 10 % | 14 % ; 9,7 % | non (perte de poids seulement) |
| P6 | Pilule : tabac au-delà de 10 % au début ; alcool au-delà de 10 % à l'arrêt | 15 % ; 34 % | **oui** |
| P7 | Perte de poids et méditerranéen : cosinus > 0,7 et croisés > 30 % | 0,49 ; 28 % et 20 % | non |
| P8 | Non à jeun : moins de 10 % pour chaque signature | méditerranéen 11,7 % | non (de justesse) |
| P9 | Sans enzymes : le gain survit pour les deux ; sensibilités < 25 % | gain : perte de poids oui, méditerranéen non ; 31 % et 42 % | non |
| P10 | ALAT > 40 % du signal | 6 mois : 32 % et 34 % ; 2 semaines : 71 % et 81 % | non à 6 mois |
| P11 | Un seul départ : jamais 80 % ; plan symétrique : perte de poids en 6 bilans au plus | plafonds de 28 à 71 % ; 4 bilans | **oui** |
| P12 | Alcool : pas de prédiction | — | — |

- **Prédictions a priori** (indépendance, CV de Q1) contre observé à 6 mois, signature :
  - perte de poids 46 % → 49 % ;
  - méditerranéen 37 % → 50 % ;
  - tabac 20 % → 26 % ;
  - alcool 14 % → 29 % ;
  - aérobie 12 % → 16 %.
- **Pourquoi l'observé est plus élevé.** Les échelles robustes du bruit (écart absolu médian, 2001-2002)
  valent 0,55 à 0,88 fois celles tirées des CV de Q1 pour 14 marqueurs sur 18 : HDL 0,60, HbA1c 0,55,
  albumine 0,56. Les CV de Q1 sont gonflés par les queues épaisses. Les corrélations aident aussi la
  signature. Les seuils, eux, restent calés empiriquement : les fausses alertes ne sont pas sous-estimées
  pour autant.

## Conséquences pour un produit de suivi

1. **Un tableau de 18 marqueurs comparés un à un à leur seuil produit des faux changements chez près
   d'une personne sur deux en 6 mois.** Afficher des flèches de tendance marqueur par marqueur
   induit en erreur.
2. **Quand on sait quel protocole la personne suit, une signature fait mieux qu'un marqueur seul.**
   Elle double environ la détection pour la perte de poids et le tabac. Mais elle ne détecte qu'une
   personne sur deux au mieux, avec une réponse moyenne.
   - **Il faut le dire ainsi** : « compatible avec l'effet attendu » ou « pas de changement
     détectable », jamais « votre programme n'a pas marché ».
3. **Pour une détection fiable (80 %), il faut des bilans répétés avant et après** l'intervention :
   4 de chaque côté pour la perte de poids. Deux bilans espacés de 6 mois ne suffisent pas.
4. **Ne pas tester toutes les signatures à la fois** : 25 % de fausses alertes.
5. **Enregistrer le laboratoire et la contraception.** Le début ou l'arrêt d'une pilule et un
   changement de laboratoire imitent des signatures.
6. **Le HDL baisse quand on réduit l'alcool.** Une interface qui colore les marqueurs en
   « mieux / moins bien » pénaliserait un changement bénéfique.

## Limites

- **Horizon simulé.** Les 6 mois sont simulés, avec une variabilité à long terme connue pour
  7 marqueurs sur 18 ; ailleurs, le bruit est une borne basse. Les sensibilités à 6 mois sont donc
  probablement **optimistes**.
- **Vecteurs d'effet.**
  - Ce sont des moyennes, souvent chez des malades, souvent assemblées à partir d'études
    différentes.
  - Plusieurs composantes sont à 0 faute de chiffre lu (GGT et VGM pour l'alcool ; hémoglobine et VGM
    pour le tabac).
  - L'effet sur l'ALAT est probablement surestimé pour des personnes en bonne santé (voir les
    sensibilités).
- **Hétérogénéité de réponse.** Elle est postulée, pas mesurée.
- **Taille et précision de la calibration.**
  - 403 paires pour une covariance à 18 dimensions.
  - **Les IC bootstrap des sensibilités ne tiennent pas compte de l'incertitude des seuils** calés
    sur 403 paires : ils sont trop étroits.
  - Les fausses alertes observées dans NHANES III (4 à 10 %) donnent l'ordre de grandeur réel de
    cette incertitude.
- **Méthodes différentes entre les deux jeux.** C'est voulu pour l'indépendance, mais cela crée des
  écarts. Les fausses alertes du méditerranéen et du meilleur marqueur seul (HbA1c, 12,5 %) en
  viennent probablement.
- **CRP absente du panel principal** (censure dans NHANES III), alors qu'elle porte une partie de
  l'effet de l'alimentation et de l'activité.
- **Pièges.** Ce sont des effets moyens de NHANES. Les vrais écarts entre laboratoires de routine
  sont inconnus pour les lipides et la numération (Q5).

## Écarts au pré-enregistrement

- **Effectif d'évaluation.** 1 292 paires complètes dans NHANES III, contre 1 288 annoncées dans le
  pré-enregistrement. Le compte préalable incluait la CRP (19 marqueurs) ; le panel principal en a 18.
- **Meilleur marqueur seul du méditerranéen.** À 6 mois, c'est l'HbA1c, et non l'ALAT comme dans la
  prédiction a priori. Le pré-enregistrement le fait choisir sur 2001-2002, ce qui a été respecté.
- **Aucun autre écart.**
