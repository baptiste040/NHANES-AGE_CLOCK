# Fiabilité test-retest réelle — remesures NHANES 2001-2002

Protocole pré-enregistré dans `DECISIONS.md` (commit `1795991`), avant toute lecture des valeurs
du second examen. Les résultats ci-dessous intègrent la correction du bug de lecture des zéros
(2026-11-10). Code : `src/aging_clock/retest.py` (analyse) et `retest_explore.py`
(exploratoire).

## Données

- 388 adultes de 20 à 79 ans, cohorte de développement (cycle 2001-2002). Ils ont été reprélevés
  3 à 47 jours plus tard, avec un délai médian de 17 jours.
- Les participants ont été recrutés de façon **non aléatoire** (Lacher et al. 2010, NHSR 21) :
  sexes et âges équilibrés de 16 à 69 ans, environ 5 % des personnes prélevées, second prélèvement
  au moins 8 jours après le premier.
- Ces personnes ont servi à ajuster le modèle (premier examen) ; le second examen ne l'a jamais été.
- Seuls les marqueurs sanguins et urinaires ont été remesurés. Tension, pouls, IMC et tour de
  taille sont fixes dans la comparaison principale (« partie biologique du score »). Le système
  cardiovasculaire n'y est donc pas interprété.

## Résultats pré-enregistrés (partie biologique, simulation principale : CV de l'EFLM)

R = écart-type intra-individuel observé / prédit. L'IC 95 % vient d'un bootstrap des personnes.

| Score | R [IC 95 %] | Lecture | Chgt significatif obs. / prédit (ans) | CCI obs. [IC] / prédit | Biais moyen (ans) [IC] | Bascule obs. / prédit |
|---|---|---|---|---|---|---|
| Global | 1,05 [0,96 ; 1,14] | compatible | 5,2 / 4,9 | 0,92 [0,90 ; 0,94] / 0,93 | +0,31 [+0,05 ; +0,57] | 13,9 % / 10,7 % |
| Métabolique | 1,21 [1,05 ; 1,39] | bruit sous-estimé | 0,9 / 0,7 | 0,993 / 0,995 | +0,01 | 2,8 % / 2,6 % |
| Rénal | 1,34 [1,19 ; 1,48] | bruit sous-estimé | 4,3 / 3,2 | 0,82 [0,73 ; 0,88] / 0,90 | −0,23 [−0,44 ; 0,00] | 21,6 % / 15,6 % |
| Hépatique | 1,04 [0,93 ; 1,17] | compatible | 4,9 / 4,7 | 0,82 [0,77 ; 0,87] / 0,84 | +0,55 [+0,31 ; +0,80] | 19,3 % / 17,8 % |
| Inflammatoire et hématologique | 1,15 [1,02 ; 1,27] | bruit sous-estimé | 4,6 / 4,0 | 0,89 [0,85 ; 0,91] / 0,92 | +0,20 | 13,7 % / 12,5 % |
| PhenoAge publié | 1,28 [1,13 ; 1,43] | bruit sous-estimé | 5,7 / 4,4 | 0,91 [0,87 ; 0,93] / 0,94 | +0,42 [+0,13 ; +0,71] | 12,1 % / 10,8 % |
| PhenoAge réentraîné | 1,07 [0,96 ; 1,17] | compatible | 4,2 / 3,9 | 0,92 [0,90 ; 0,94] / 0,93 | +0,39 [+0,18 ; +0,60] | 11,9 % / 11,0 % |

Score complet, version corrigée non pré-enregistrée (bruit physique simulé sur les deux examens) :
global R = 1,03, changement significatif 6,3 ans. Délai : aucune relation avec |d|.

## Analyse exploratoire (non pré-enregistrée)

- **Les variations des marqueurs sont corrélées.**
  - Dilution ou posture : albumine-protéines 0,70, hémoglobine-protéines 0,58,
    albumine-hémoglobine 0,51.
  - Foie : ALAT-ASAT 0,64.
  - Avec les CV observés et cette corrélation, la simulation retrouve le bruit réel de tous les
    scores (R de 0,98 à 1,05). Avec un bruit indépendant, elle surestime celui du global (R = 0,82)
    et de l'hépatique (0,72).
  - Le « compatible » pré-enregistré du score global combine donc deux erreurs qui se compensent :
    des CV EFLM trop bas et l'hypothèse d'indépendance.
- **Les queues de distribution sont épaisses.** Les CV robustes (écart absolu médian) rejoignent
  les valeurs de référence : CRP 35 % contre 60 % en CV classique ; ACR 40 % contre 57 %. Cinq
  personnes portent 15 à 27 % de la variance des écarts. Sans les 47 personnes dont la CRP dépasse
  10 mg/L à un examen, l'écart-type intra-individuel de PhenoAge publié passe de 2,04 à 1,74.
- Conséquence : le changement significatif gaussien (1,96 × racine(2) × écart-type) est trop large
  pour la plupart des personnes et trop étroit pour celles qui traversent un épisode aigu.

## Note : relation inverse entre l'ALAT et l'âge biologique

Dans le modèle, une ALAT plus élevée **rajeunit** l'âge biologique : +10 % d'ALAT donne −0,8 an
d'âge global (médiane), alors que +10 % d'ASAT donne +0,5 an. Ce n'est pas une anomalie du
modèle : la littérature décrit une association entre ALAT basse et mortalité plus élevée. Une ALAT
basse est interprétée comme un marqueur de faible masse musculaire (sarcopénie), de fragilité et
de carence en vitamine B6 (cofacteur de l'enzyme).
- Elinav et al. 2006, *J Am Geriatr Soc* (doi:10.1111/j.1532-5415.2006.00921.x) : à 70 ans, une
  ALAT basse est associée à une mortalité plus élevée sur 12 ans.
- Vespasiani-Gentilucci et al. 2018, *J Gerontol A* (doi:10.1093/gerona/glx126) : dans InCHIANTI,
  une ALAT basse est liée à la fragilité, à l'incapacité, à la sarcopénie et à une survie réduite.
- Peltz-Sinvani et al. 2016, *J Gen Intern Med* (doi:10.1007/s11606-015-3480-6) : une ALAT basse est
  associée à la mortalité à 22 ans chez des coronariens.
- Yamazaki et al. 2019, *J Gastroenterol Hepatol* (doi:10.1111/jgh.14631) : une ALAT basse,
  indicateur d'une carence en vitamine B6, est associée à la perte d'autonomie ou au décès chez des
  personnes âgées.
- Li et Lan 2025, *Sci Rep* (doi:10.1038/s41598-025-93184-1) : un rapport ASAT/ALAT élevé
  (De Ritis) est associé à la mortalité (NHANES, insuffisance rénale chronique).

Pour la fiabilité, cela a une conséquence. L'ALAT et l'ASAT varient ensemble d'un prélèvement à
l'autre (ρ = 0,64), alors que leurs effets sont de sens opposés. Leurs variations se compensent en
partie dans l'âge hépatique et dans l'âge global. Résumés lus pour ces cinq articles, pas les
textes complets. Le modèle n'a pas de terme explicite de rapport ASAT/ALAT : la relation vient
des splines de chaque enzyme, ajustées sur les autres marqueurs.

## Réplication indépendante — second examen de NHANES III

Protocole pré-enregistré et amendé (`DECISIONS.md`), code `retest_nh3.py`, sorties `reports/checkup_standard/fiabilite_nhanes3/`. Résultats détaillés dans `DECISIONS.md` (« Résultat — réplication NHANES III »).
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
