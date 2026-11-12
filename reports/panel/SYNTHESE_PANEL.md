# Programme « panel » : synthèse

**Contexte.** Les marqueurs d'un bilan de check-up sont suivis tous les 6 mois, dans plusieurs
laboratoires, sans contrôle du jeûne ni de l'heure, chez des adultes de 30 à 55 ans souvent
favorisés. Six questions ont été traitées sur NHANES (États-Unis, 1988-2018), chacune avec un
pré-enregistrement dans `DECISIONS.md` et un rapport :
- Q1 : bruit et changement détectable ;
- Q2 : jeûne et heure ;
- Q3 : populations particulières ;
- Q4 : normalisation spontanée ;
- Q5 : méthodes et laboratoires ;
- Q6 : zones de risque.

Résultats par marqueur : `resultats_par_marqueur.csv` et `fiches/`.

**Niveau de preuve**, indiqué pour chaque résultat :
- **pré-enregistré** ou non : protocole et règles de décision fixés avant de lire les données ;
- **répliqué** ou non : retrouvé dans un second jeu indépendant (NHANES III et NHANES 2001-2002,
  ou développement et validation), ou appuyé seulement sur la littérature lue.

## Les 10 résultats principaux

### 1. Le bruit d'un marqueur entre deux bilans est grand

- **Chiffre clé.** Un changement n'est détectable chez une personne, en 6 mois, qu'au-delà de ces
  valeurs (30-55 ans, hausse / baisse) :
  - HbA1c : +11 / −10 % ;
  - créatinine : +21 / −17 % ;
  - glycémie à jeun : +24 / −19 % ;
  - cholestérol total : +26 / −21 % ;
  - HDL : +41 / −29 % ;
  - LDL : +57 / −36 % ;
  - TG : +115 / −54 % ;
  - insuline : +120 / −55 % ;
  - ALAT : +186 / −65 % ;
  - CRP : +397 / −80 %.
- **Ce sont des bornes basses.** Elles viennent de remesures à environ 2 semaines. Un CV à long
  terme n'existe que pour quelques marqueurs.
- **Niveau de preuve : pré-enregistré, répliqué.** Les CV de NHANES III et de 2001-2002 sont à moins
  d'un facteur 1,5 pour 93 % des marqueurs. Les spécifications EFLM sous-estiment le CV observé pour
  83 % d'entre eux.
- **Conséquence pratique.**
  - Une variation entre deux bilans n'est un changement que si elle dépasse ce seuil.
  - Il faut afficher ce seuil, ou un intervalle autour de chaque valeur, plutôt qu'une flèche de
    tendance.

### 2. Les interventions d'hygiène de vie ne sont visibles qu'en moyenne de groupe

- **Chiffre clé.** Chez les 30-55 ans :
  - sur 25 couples (intervention, marqueur) tirés de méta-analyses, 20 ne sont visibles qu'en
    moyenne de groupe, 3 sont limites, et 2 seulement sont détectables chez une personne ;
  - les deux détectables : la vitamine D sous supplémentation (ratio 1,7) et l'HbA1c sous activité
    physique, **chez des diabétiques** (1,3) ;
  - l'effet de l'activité physique sur le cholestérol total vaut 0,14 fois le changement
    détectable : il faudrait environ 60 bilans avant et après pour le voir chez une personne.
- **Niveau de preuve : pré-enregistré, non répliqué** (effets tirés de la littérature lue, souvent
  des résumés, chez des populations souvent malades).
- **Conséquence pratique.**
  - Ne pas promettre à une personne de « voir » l'effet de son hygiène de vie sur ses marqueurs en
    6 mois.
  - Un effet de programme se démontre sur une cohorte, pas sur une personne.

### 3. Le jeûne pèse peu pour suivre une personne, beaucoup pour la classer

- **Chiffre clé.**
  - Pour suivre : chez une même personne, l'effet d'un repas vaut moins de 0,5 fois le changement
    détectable pour tous les marqueurs (TG +15 % au plus, pour un seuil de +111 %).
  - Pour classer : jusqu'à **+31 points** de personnes au-dessus du seuil glycémique de l'ADA, +13
    pour les TG, +39 pour un seuil de HOMA-IR.
- **Niveau de preuve.**
  - Suivi : pré-enregistré.
  - Classification : analyse secondaire non pré-enregistrée.
  - Effet chez une même personne : NHANES III seul. Les associations entre personnes sont 3 à 8 fois
    plus fortes.
- **Conséquence pratique.**
  - Enregistrer le statut de jeûne (heures depuis le dernier repas) à chaque prélèvement.
  - Ne pas calculer le HOMA-IR ni le QUICKI quand le jeûne est inconnu.
  - Ne pas appliquer les seuils glycémiques à un prélèvement non vérifié.

### 4. Une anomalie limite disparaît souvent seule : c'est la mesure, pas une guérison

- **Chiffre clé.**
  - En 2 semaines, les anomalies limites (à moins d'un changement détectable du seuil) redeviennent
    normales dans 41 % des cas, les anomalies nettes dans 5 %.
  - Le bruit de mesure seul explique la normalisation observée, à 10 points près, pour 87 % des
    couples (marqueur, seuil).
- **Niveau de preuve : pré-enregistré, répliqué** (NHANES III et 2001-2002, 73 % des couples dans le
  second jeu).
- **Conséquence pratique.**
  - Confirmer une anomalie limite et isolée avant de la signaler.
  - Ne pas attribuer à une intervention le retour à la normale d'une valeur limite.

### 5. Un changement de laboratoire compte peu pour suivre, beaucoup pour classer, et peut imiter une intervention

- **Chiffre clé.**
  - Pour suivre, la plupart des changements de méthode de NHANES valent moins de 0,5 fois le
    changement détectable. Deux exceptions : folates érythrocytaires +85 % (2007) et créatinine
    +22 % (1999-2000).
  - Pour classer : passage Beckman → Roche en 2017 :
    - +26 points de personnes sous la limite basse de l'ASAT ;
    - +14 pour la bilirubine.
  - Pour classer, glycémie au seuil de l'ADA : +4 à +7 points à chaque changement d'instrument.
  - Un changement de laboratoire peut **imiter ou masquer** l'effet moyen d'une intervention
    réaliste pour 11 marqueurs sur 15 : TG, insuline, cholestérol, HDL, transaminases.
- **Niveau de preuve.**
  - Pré-enregistré.
  - Vérification de l'implémentation : partielle. Nous trouvons +6,8 points sur la glycémie, contre
    +12,2 points dans le texte du NCHS.
  - Prédictions : 1 sur 3 vérifiée.
- **Conséquence pratique.**
  - Enregistrer le laboratoire et la méthode à chaque prélèvement.
  - Pour évaluer un protocole sur une cohorte, comparer à laboratoire identique ou mettre le
    laboratoire en covariable.
  - N'appliquer un intervalle de référence qu'à la méthode qui l'a produit.

### 6. L'écart entre laboratoires de routine est inconnu pour la plupart des marqueurs

- **Chiffre clé.**
  - Quand l'écart est publié (évaluations externes de la qualité), le changement détectable entre
    deux laboratoires est 1,02 à 1,49 fois celui d'un même laboratoire :
    - calcium : ×1,49 ;
    - PAL : ×1,30 ;
    - HbA1c : ×1,27 ;
    - enzymes : ×1,02 à ×1,04.
  - **Rien trouvé** pour les lipides, la numération, les vitamines et l'insuline.
- **Niveau de preuve : pré-enregistré, littérature seule** (études lues, CV mesurés au sein des
  groupes de méthode : bornes basses).
- **Conséquence pratique.** Cet écart ne pourra être mesuré que sur des données réelles venant de
  plusieurs laboratoires (voir les questions en fin de document).

### 7. Les seuils usuels conviennent à la plupart des groupes particuliers, mais la contraception et la ménopause déplacent des marqueurs

- **Chiffre clé.**
  - **Pilule** :
    - CRP ×2 ;
    - vitamine D +46 % ;
    - TG +27 % ;
    - B12 −19 % ;
    - ferritine +31 %.
  - **Après la ménopause** : ferritine +196 % (45-49 ans), seul seuil « inadapté » par décalage.
    Glycémie à jeun au-delà du seuil de l'OMS chez 11,8 % des femmes saines, contre 5,1 % : c'est
    un risque réel, et le seuil est à conserver.
  - **Personnes très actives** (5 % les plus actives, accéléromètre) : pas d'excès de faux signaux
    pour la créatinine, le DFGe, l'ASAT ou l'hémoglobine. La prédiction contraire n'est pas
    vérifiée.
- **Niveau de preuve : pré-enregistré.** 7 attentes sur 7 confirmées sous pilule. Les groupes
  reposent sur des déclarations et des ordonnances. Les très actifs ne sont pas des athlètes de
  compétition.
- **Conséquence pratique.**
  - Enregistrer le statut contraceptif à chaque bilan. Un début ou un arrêt de pilule fait bouger
    les marqueurs comme une intervention, et une CRP doublée peut mimer une inflammation.
  - Prévoir des repères distincts avant et après la ménopause (ferritine, PAL, glycémie).

### 8. Un centile « population générale » flatte une population favorisée et en bonne santé

- **Chiffre clé.**
  - La personne médiane du groupe favorisé et sain est à au moins 10 points du 50e centile de la
    population générale des 30-55 ans pour **56 couples (marqueur, sexe) sur 133**. L'écart va
    jusqu'à 26 points : TG/HDL des femmes au 24e centile, HDL au 72e.
  - C'est surtout l'effet du filtre « sain » : pour tout le groupe favorisé, sains ou non, seuls
    22 couples dépassent 10 points.
- **Niveau de preuve : pré-enregistré** (mesure descriptive), **non répliqué**.
- **Conséquence pratique.**
  - Ne pas présenter le 50e centile général comme une norme à une population sélectionnée.
  - Pour le métabolisme, le foie et l'inflammation, la personne médiane d'une population favorisée
    et saine est vers le 30e centile général.

### 9. Le risque de mortalité commence souvent à l'intérieur de l'intervalle usuel, et la plupart des relations sont en U

- **Chiffre clé.**
  - Sur 68 marqueurs, après réplication : 37 relations en U ou en J, 14 montantes,
    11 descendantes, 6 non répliquées.
  - Sur 179 comparaisons aux intervalles de référence, 90 sont « trop larges ». Le risque (HR 1,2)
    commence à l'intérieur de l'intervalle usuel, par exemple :
    - leucocytes au-dessus de 8,1 G/L ;
    - RDW au-dessus de 12,4 % ;
    - GGT au-dessus de 31 U/L ;
    - CRP au-dessus de 2,4 mg/L ;
    - albumine sous 4,55 g/dL ;
    - HDL sous 43 et au-dessus de 71 mg/dL.
  - Ces seuils tiennent après ajustement sur le tabac, l'alcool (déclaré), l'IMC, le diabète et le
    revenu : 38 côtés inchangés, 9 atténués, 1 mixte selon le sexe. Un seul devient un **marqueur
    de risque** expliqué par ces facteurs : le côté bas de la bilirubine.
  - L'alcool ne change presque rien, y compris pour la GGT, l'ALAT, l'ASAT et le VGM.
  - Exclure les décès précoces montre que certains côtés sont des **marqueurs de maladie** : côté bas
    des leucocytes et de la CRP, côté haut de la bilirubine.
- **Niveau de preuve : pré-enregistré, répliqué** (développement 1999-2006 et validation 2007-2010).
  Ce sont des **associations**, pas des cibles.
- **Conséquence pratique.**
  - Un intervalle de laboratoire n'est pas une « zone de santé ».
  - Un produit peut signaler qu'une valeur normale est associée à un risque plus élevé, sans en
    faire une cible thérapeutique.

### 10. Mais à 45 ans, un HR de 1,2 est une petite différence, et les seuils cliniques ne doivent pas être assouplis

- **Chiffre clé.**
  - Au seuil HR 1,2, le risque de décès à 10 ans d'une personne de 45 ans augmente de **+0,8 point
    chez les hommes** (de 4,4 %) et de **+0,5 point chez les femmes** (de 2,7 %).
  - En moyenne, 20 % des 30-55 ans dépassent un seuil de ce type.
  - **Un seuil franchi par la majorité des 30-55 ans décrit une pente de risque, pas un signal à
    afficher** : albumine 78 %, RAC 64 %, DFGe élevé 53 %.
  - **Le risque au-dessus d'un DFGe de 101 traduit probablement une faible masse musculaire**
    (créatinine basse, marqueur de fragilité) plutôt qu'un risque rénal. C'est une hypothèse, non
    testée.
- **Seuils cliniques.** Les seuils jugés « trop stricts » pour la mortalité (LDL, non-HDL, TG,
  glycémie à jeun 100 mg/dL, vitamine D 30 ng/mL) visent les événements cardiovasculaires ou le
  diabète. La mortalité à 10 ans est un mauvais juge pour eux.
- **Niveau de preuve.** Risque absolu : analyse secondaire non pré-enregistrée. Seuils cliniques et
  DFGe élevé : interprétation.
- **Conséquence pratique.**
  - Montrer le risque absolu, pas seulement le risque relatif.
  - Ne pas faire d'alerte individuelle à partir d'un seuil franchi par une personne sur cinq.
  - Garder les seuils cliniques fondés sur les événements.

## Limites communes

- **NHANES est américain.** Ses laboratoires sont centralisés et très contrôlés. Ses méthodes ont
  changé au fil des cycles (Q5), et ses traitements datent des années 2000.
- **Les remesures sont à environ 2 semaines.** Les changements détectables à 6 mois sont des bornes
  basses, sauf pour les quelques marqueurs à CV connu à long terme.
- **La population cible n'est pas celle de NHANES.** Elle est plus jeune, plus favorisée, et compte
  des athlètes et des femmes sous contraception hormonale. Q3 n'en donne que des proxys.
- **Neuf marqueurs du panel n'existent dans aucune source** utilisée.
- **Q6 décrit des associations avec la mortalité seule**, et une mesure unique. Les sensibilités ne
  corrigent qu'en partie la causalité inverse ; celle sur la population saine manque de puissance.
- **Littérature.** Les sources ont été lues, souvent en résumé seulement (signalé dans chaque
  rapport). Les effets d'intervention viennent souvent de populations malades.

## Ce que seules des données réelles multi-laboratoires à 6 mois peuvent trancher

1. **La vraie variabilité à 6 mois** de chaque marqueur dans la population cible. Les changements
   détectables de Q1 sont des bornes basses tirées de remesures à 2 semaines.
2. **L'écart entre laboratoires de routine** pour les lipides, la numération, les vitamines et
   l'insuline, aujourd'hui inconnu. Il faut les mêmes personnes, ou les mêmes échantillons, mesurés
   dans plusieurs laboratoires.
3. **L'effet réel du jeûne et de l'heure dans les conditions de prélèvement de la cohorte**, et la
   part des prélèvements non à jeun.
4. **La dispersion des réponses individuelles** aux interventions : qui change au-delà du seuil, et
   combien de personnes. Les méta-analyses ne donnent que des moyennes.
5. **Le taux de normalisation des anomalies limites à 6 mois**, et non plus à 2 semaines.
6. **Les intervalles et les centiles propres à la population cible** : affluente, athlètes,
   contraception hormonale. Ils sont nécessaires pour cesser de la comparer à une population
   générale américaine.
7. **L'effet d'un changement de laboratoire chez une même personne**, pour bâtir des équations de
   passage propres à la cohorte.
8. **Les zones de risque** ne peuvent pas être validées sur la cohorte sans événements cliniques
   (morbidité, événements cardiovasculaires) ni suivi long. À défaut, on peut seulement vérifier
   que la distribution de la cohorte autour des seuils de Q6 ressemble à celle de NHANES.
