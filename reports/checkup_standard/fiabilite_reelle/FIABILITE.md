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
