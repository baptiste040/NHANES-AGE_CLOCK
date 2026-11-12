# Q1 : changement détectable à 6 mois, marqueur par marqueur

Programme « panel » : le comportement des biomarqueurs d'un check-up de prévention, sur un cas
générique (bilan large au départ, puis prise de sang tous les 6 mois, sans contrôle de l'heure ni
du jeûne). Protocole pré-enregistré dans `DECISIONS.md` (commit `76c3962`, avant tout calcul).
Code : `src/aging_clock/panel/` (`remesures.py`, `q1.py`, `q1_interventions.py`, `q1_rcv.py`,
`q1_rapport.py`). Données : `Q1_variabilite_remesures.csv`, `Q1_changement_detectable.csv`,
`Q1_interventions.csv`, `Q1_comparaison_rcv_publies.csv`.

> **Corrections d'erreurs du 2026-11-12** (audit indépendant ; détail et tableaux avant/après dans
> `DECISIONS.md`, « Corrections d'erreurs après audit ») :
> 1. la créatinine de NHANES III est maintenant recalibrée (0,960 x − 0,184 mg/dL), comme dans le
>    pipeline principal ; le DFGe en dépend ;
> 2. le jeu principal est **2001-2002** pour tous les marqueurs dont la méthode ou l'automate a changé
>    depuis NHANES III (glycémie, HbA1c, lipides, profil biochimique, numération) ; NHANES III passe en
>    sensibilité. Les tableaux ci-dessous sont régénérés depuis les CSV ;
> 3. l'effet de l'activité physique structurée sur l'HbA1c, mesuré chez des diabétiques, est rapporté
>    à une base de diabétiques (médiane des HbA1c ≥ 6,5 %, soit 7,6 %), et non à la médiane d'une
>    population surtout saine : −9 % au lieu de −13 % ;
> 4. le statut « extrapolé à 6 mois » n'est plus donné aux plaquettes : leur CV_I à long terme est
>    inférieur au CV_I à court terme, rien n'est ajouté.

## À lire avant les chiffres

- **Le changement détectable ne comprend pas la variabilité entre laboratoires.** Il suppose la
  même méthode aux deux bilans. Changer de laboratoire ajoute un décalage, étudié en Q5.
- **Les effets d'interventions sont des effets moyens.** Ils viennent de méta-analyses d'essais
  et ne disent rien de la variabilité de la réponse d'une personne à l'autre : certains répondent
  beaucoup plus, d'autres pas du tout.
- **Bornes basses.** Les remesures ont lieu à environ 2 semaines, avec le même laboratoire et le
  même protocole. À 6 mois, la variabilité est plus grande. On ne l'ajoute que lorsqu'une étude
  EFLM à long terme de bonne qualité existe (statut « extrapolé à 6 mois »). Sinon, le chiffre est
  une **borne basse**.
- **NHANES est américain**, et ses laboratoires sont centralisés : la variabilité analytique y est
  plus faible que dans un réseau de laboratoires.
- **Seuils.** Q1 n'utilise aucun seuil clinique. Dans les questions suivantes, on distinguera
  toujours les **conventions statistiques** (intervalles de référence : 95 % central d'une
  population saine) des **seuils fondés sur le risque** (recommandations de décision clinique).

## Méthode

1. **Variabilité observée** sur deux jeux de remesures, analysés séparément :
   - NHANES 2001-2002, second examen (environ 400 adultes) ;
   - NHANES III, second examen (jusqu'à 1 800 adultes).

   On garde les adultes de 20 à 79 ans, hors femmes enceintes. Avec $d = \ln x_2 - \ln x_1$ :
   - CV observé $= \sqrt{e^{\mathrm{Var}(d)/2}-1}$, en version classique et robuste ;
   - changement empirique = P95 de $|d|$ ;
   - IC par bootstrap (2 000 tirages).

   Les marqueurs qui peuvent valoir 0 (basophiles, éosinophiles en nombre, Lp(a), et certaines
   formules de NHANES III) sont sur l'échelle additive, en unités.

   **Jeu principal (corrigé le 2026-11-12).** 2001-2002 pour les marqueurs dont la méthode ou
   l'automate a changé depuis NHANES III, d'après la documentation du CDC : HbA1c (Diamat, échange
   d'ions → Primus, affinité boronate) ; profil biochimique (Hitachi 737 → Hitachi 704 en 2001, puis
   Beckman Synchron LX20 en 2002) ; numération (Coulter S-Plus JR → Coulter MAXM) ; glycémie et
   lipides ; indices dérivés de ces marqueurs. NHANES III sinon (insuline, vitamines, ferritine,
   urines, marqueurs absents de 2001-2002), ou 2001-2002 si NHANES III manque ou a plus de 20 % de
   valeurs au plancher (CRP, censurée chez 62 % des personnes). Avant la correction, NHANES III était
   principal pour tous ; son changement détectable est donné à côté, en sensibilité. Créatinine de
   NHANES III recalibrée (0,960 x − 0,184 mg/dL, Selvin 2007).
2. **Extrapolation à 6 mois** : $CV_{6m}^2 = CV_{obs}^2 + \max(0, CV_{I,LT}^2 - CV_{I,CT}^2)$.
   - CV_I,CT : méta-analyse EFLM.
   - CV_I,LT : médiane des études EFLM (BIVAC) qui réunissent ces conditions :
     - durée ≥ 6 mois ;
     - adultes en bonne santé ;
     - sérum, plasma ou sang total ;
     - note A ou B.
3. **Changement détectable** (deux mesures, 95 %) : hausse $e^{1{,}96\sqrt2\,\sigma}-1$, baisse
   $1-e^{-1{,}96\sqrt2\,\sigma}$, avec $\sigma=\sqrt{\ln(1+CV_{6m}^2)}$. L'asymétrie vient de
   l'échelle log : +100 % et −50 % correspondent au même écart.
4. **Interventions** :
   - méta-analyses d'essais trouvées avec les requêtes pré-enregistrées, et lues (résumé « R » ou
     texte complet « TC ») ;
   - effet converti en % de la médiane NHANES des 30-55 ans ;
   - ratio = |effet| / changement détectable dans le même sens.

## Ce que montrent les données des remesures

Les trois prédictions pré-enregistrées sur la variabilité sont **vérifiées** :

| Prédiction | Observé | Vérifiée |
|---|---|---|
| L'EFLM sous-estime le CV observé pour ≥ 2/3 des marqueurs | 35 marqueurs sur 42 (83 %) | oui |
| Queues épaisses (changement empirique > 1,10 × celui du CV robuste) pour ≥ 50 % des marqueurs | 81 % (57 sur 70 ; 56 avant la recalibration de la créatinine) | oui |
| Réplication : CV de 2001-2002 et de NHANES III à moins d'un facteur 1,5 pour ≥ 2/3 des marqueurs | 93 % (57 sur 61) | oui |

**L'EFLM à long terme est rare.** Sur 572 jeux de données EFLM de 6 mois ou plus, seuls 30
remplissent les critères. La plupart des études longues ont la note BIVAC C. Un CV_I à long terme
n'existe donc que pour la numération, l'ALAT, l'ASAT, les bicarbonates, les plaquettes et la TSH (pour
les plaquettes, il est inférieur au CV_I à court terme : rien n'est ajouté).
Ailleurs, le changement détectable reste une borne basse à 2 semaines. 81 % des jeux utilisés
dans les méta-analyses EFLM durent moins de 6 mois : le CV_I « méta-analyse » est bien un CV à
court terme.

## Changement détectable à 6 mois

| Marqueur | Jeu principal | n | CV observé (%) | **Changement détectable à 6 mois (%)**, hausse / baisse, 20-79 ans | 30-55 ans | Avec le bruit de NHANES III (sensibilité) | Statut |
|---|---|---|---|---|---|---|---|
| Leucocytes | 2001-02 | 420 | 13,4 | **+48 / −32** | +47 / −32 | +46 / −31 | extrapolé à 6 mois |
| Neutrophiles (%) | 2001-02 | 420 | 10,2 | **+37 / −27** | +34 / −25 | +43 / −30 | extrapolé à 6 mois |
| Neutrophiles (nombre) | 2001-02 | 420 | 20,3 | **+77 / −44** | +72 / −42 | — | extrapolé à 6 mois |
| Lymphocytes (%) | 2001-02 | 420 | 16,6 | **+59 / −37** | +58 / −37 | +47 / −32 | extrapolé à 6 mois |
| Lymphocytes (nombre) | 2001-02 | 420 | 15,7 | **+55 / −35** | +58 / −37 | +45 / −31 | extrapolé à 6 mois |
| Monocytes (%) | 2001-02 | 420 | 14,5 | **+57 / −36** | +60 / −38 | — | extrapolé à 6 mois |
| Monocytes (nombre) | 2001-02 | 420 | 17,4 | **+69 / −41** | +70 / −41 | — | extrapolé à 6 mois |
| Éosinophiles (%) | 2001-02 | 420 | 28,3 | **+119 / −54** | +116 / −54 | — | extrapolé à 6 mois |
| Éosinophiles (nombre) | 2001-02 | 420 | ET intra 0,07 | **± 0,20 (unités)** | ± 0,17 | — | borne basse (2 semaines), échelle additive |
| Basophiles (%) | 2001-02 | 420 | ET intra 0,30 | **± 0,82 (unités)** | ± 0,83 | — | borne basse (2 semaines), échelle additive |
| Basophiles (nombre) | — | — | — | — | — | — | non interprétable (valeurs censurées > 20 %) |
| Hématies | 2001-02 | 420 | 3,1 | **+11 / −10** | +10 / −10 | +10 / −9 | extrapolé à 6 mois |
| Hémoglobine | 2001-02 | 420 | 2,8 | **+10 / −9** | +10 / −9 | +10 / −9 | extrapolé à 6 mois |
| Hématocrite | 2001-02 | 420 | 3,2 | **+11 / −10** | +10 / −9 | +10 / −9 | extrapolé à 6 mois |
| VGM | 2001-02 | 420 | 0,8 | **+3 / −3** | +3 / −3 | +3 / −3 | extrapolé à 6 mois |
| TCMH | 2001-02 | 420 | 1,2 | **+4 / −4** | +4 / −4 | +5 / −4 | extrapolé à 6 mois |
| CCMH | 2001-02 | 420 | 1,3 | **+4 / −4** | +4 / −4 | +5 / −4 | extrapolé à 6 mois |
| RDW | 2001-02 | 420 | 1,7 | **+6 / −6** | +6 / −6 | +7 / −6 | extrapolé à 6 mois |
| Plaquettes | 2001-02 | 420 | 8,5 | **+26 / −21** | +26 / −21 | +35 / −26 | borne basse (2 semaines) |
| VPM | 2001-02 | 420 | 3,7 | **+11 / −10** | +11 / −10 | +13 / −12 | borne basse (2 semaines) |
| Glycémie à jeun (plasma) | 2001-02 | 167 | 7,7 | **+24 / −19** | +22 / −18 | +29 / −23 | borne basse (2 semaines) |
| Glucose sérique (non à jeun) | 2001-02 | 409 | 8,4 | **+26 / −21** | +24 / −20 | +33 / −25 | borne basse (2 semaines) |
| Insuline (à jeun) | NHANES III | 1182 | 28,2 | **+115 / −54** | +120 / −55 | (jeu principal) | borne basse (2 semaines) |
| HbA1c | 2001-02 | 419 | 1,9 | **+5 / −5** | +5 / −5 | +10 / −9 | borne basse (2 semaines) |
| Cholestérol total | 2001-02 | 406 | 7,1 | **+22 / −18** | +23 / −19 | +26 / −21 | borne basse (2 semaines) |
| LDL (calculé, à jeun) | 2001-02 | 147 | 11,4 | **+37 / −27** | +39 / −28 | +47 / −32 | borne basse (2 semaines) |
| HDL | 2001-02 | 406 | 9,6 | **+30 / −23** | +29 / −23 | +43 / −30 | borne basse (2 semaines) |
| Triglycérides (à jeun) | 2001-02 | 166 | 26,3 | **+105 / −51** | +107 / −52 | +111 / −53 | borne basse (2 semaines) |
| Triglycérides sériques (non à jeun) | 2001-02 | 409 | 28,3 | **+116 / −54** | +121 / −55 | +101 / −50 | borne basse (2 semaines) |
| ALAT | 2001-02 | 409 | 18,3 | **+162 / −62** | +169 / −63 | +181 / −64 | extrapolé à 6 mois |
| ASAT | 2001-02 | 409 | 17,4 | **+87 / −47** | +95 / −49 | +86 / −46 | extrapolé à 6 mois |
| GGT | 2001-02 | 409 | 15,2 | **+52 / −34** | +52 / −34 | +53 / −35 | borne basse (2 semaines) |
| PAL | 2001-02 | 409 | 7,7 | **+24 / −19** | +24 / −19 | +22 / −18 | borne basse (2 semaines) |
| Bilirubine totale | 2001-02 | 409 | 18,4 | **+66 / −40** | +68 / −41 | — | borne basse (2 semaines) |
| Albumine | 2001-02 | 409 | 3,5 | **+10 / −9** | +10 / −9 | +13 / −11 | borne basse (2 semaines) |
| Protéines totales | 2001-02 | 409 | 3,4 | **+10 / −9** | +10 / −9 | +10 / −9 | borne basse (2 semaines) |
| Créatinine | 2001-02 | 409 | 7,4 | **+23 / −19** | +24 / −20 | +26 / −21 | borne basse (2 semaines) |
| Urée | 2001-02 | 409 | 18,6 | **+67 / −40** | +72 / −42 | +68 / −40 | borne basse (2 semaines) |
| Sodium | 2001-02 | 409 | 1,3 | **+4 / −4** | +3 / −3 | +4 / −4 | borne basse (2 semaines) |
| Potassium | 2001-02 | 409 | 6,2 | **+19 / −16** | +18 / −15 | +16 / −14 | borne basse (2 semaines) |
| Chlorure | 2001-02 | 409 | 1,8 | **+5 / −5** | +5 / −5 | +6 / −6 | borne basse (2 semaines) |
| Bicarbonates | 2001-02 | 409 | 6,3 | **+20 / −17** | +19 / −16 | +38 / −27 | extrapolé à 6 mois |
| CRP | 2001-02 | 412 | 58,7 | **+351 / −78** | +397 / −80 | +206 / −67 | borne basse (2 semaines) |
| Vitamine B12 | NHANES III | 894 | 14,3 | **+48 / −33** | +58 / −37 | (jeu principal) | borne basse (2 semaines) |
| Folates érythrocytaires | NHANES III | 1176 | 9,4 | **+30 / −23** | +31 / −24 | (jeu principal) | borne basse (2 semaines) |
| 25-OH vitamine D | 2001-02 | 341 | 15,7 | **+54 / −35** | +58 / −37 | — | borne basse (2 semaines) |
| Calcium | 2001-02 | 409 | 2,4 | **+7 / −6** | +7 / −7 | +10 / −9 | borne basse (2 semaines) |
| LH | NHANES III | 275 | 67,6 | **+448 / −82** | +534 / −84 | (jeu principal) | borne basse (2 semaines) |
| FSH | 2001-02 | 86 | 43,8 | **+219 / −69** | +253 / −72 | — | borne basse (2 semaines) |
| PSA total | 2001-02 | 102 | 17,4 | **+62 / −38** | +63 / −39 | — | borne basse (2 semaines) |
| PSA libre | 2001-02 | 102 | 18,0 | **+64 / −39** | +63 / −39 | — | borne basse (2 semaines) |
| Fer sérique | 2001-02 | 409 | 31,2 | **+133 / −57** | +138 / −58 | +132 / −57 | borne basse (2 semaines) |
| Ferritine | NHANES III | 1807 | 22,3 | **+84 / −46** | +94 / −48 | (jeu principal) | borne basse (2 semaines) |
| Homocystéine | 2001-02 | 418 | 13,7 | **+46 / −32** | +44 / −31 | — | borne basse (2 semaines) |
| Acide urique | 2001-02 | 409 | 9,3 | **+29 / −23** | +29 / −22 | +30 / −23 | borne basse (2 semaines) |
| Phosphate | 2001-02 | 409 | 9,9 | **+31 / −24** | +33 / −25 | +30 / −23 | borne basse (2 semaines) |
| Albumine urinaire | NHANES III | 1196 | 107,5 | **+1034 / −91** | +1073 / −91 | (jeu principal) | borne basse (2 semaines) |
| Créatinine urinaire | NHANES III | 1196 | 56,4 | **+330 / −77** | +365 / −78 | (jeu principal) | borne basse (2 semaines) |
| HOMA-IR | 2001-02 | 160 | 31,8 | **+136 / −58** | +158 / −61 | +139 / −58 | borne basse (2 semaines) |
| QUICKI | 2001-02 | 160 | 4,4 | **+13 / −11** | +14 / −12 | +13 / −12 | borne basse (2 semaines) |
| Glycémie moyenne estimée | 2001-02 | 419 | 2,7 | **+8 / −7** | +8 / −7 | +15 / −13 | borne basse (2 semaines) |
| Indice TyG | 2001-02 | 164 | ET intra 0,27 | **± 0,76 (unités)** | ± 0,72 | — | borne basse (2 semaines), échelle additive |
| Cholestérol non-HDL | 2001-02 | 406 | 9,4 | **+30 / −23** | +31 / −24 | +36 / −27 | borne basse (2 semaines) |
| LDL/HDL | 2001-02 | 147 | 11,6 | **+38 / −27** | +40 / −29 | +70 / −41 | borne basse (2 semaines) |
| TG/HDL | 2001-02 | 166 | 30,7 | **+130 / −56** | +121 / −55 | +141 / −58 | borne basse (2 semaines) |
| Indice athérogène (log10 TG/HDL, mmol) | 2001-02 | 166 | ET intra 0,13 | **± 0,36 (unités)** | ± 0,34 | — | borne basse (2 semaines), échelle additive |
| Albumine/globulines | 2001-02 | 409 | 5,9 | **+18 / −15** | +17 / −15 | +26 / −20 | borne basse (2 semaines) |
| FIB-4 | 2001-02 | 407 | 15,2 | **+52 / −34** | +54 / −35 | +61 / −38 | borne basse (2 semaines) |
| GGT/HDL | 2001-02 | 406 | 17,7 | **+63 / −38** | +62 / −38 | +65 / −39 | borne basse (2 semaines) |
| ASAT/ALAT | 2001-02 | 409 | 14,0 | **+47 / −32** | +51 / −34 | +62 / −38 | borne basse (2 semaines) |
| Urée/créatinine | 2001-02 | 409 | 18,5 | **+66 / −40** | +72 / −42 | +69 / −41 | borne basse (2 semaines) |
| Osmolalité effective (2 Na + glucose) | 2001-02 | 409 | 1,3 | **+4 / −3** | +3 / −3 | +4 / −4 | borne basse (2 semaines) |
| Neutrophiles/lymphocytes | 2001-02 | 420 | 26,4 | **+106 / −51** | +99 / −50 | +97 / −49 | borne basse (2 semaines) |
| Indice SII | 2001-02 | 420 | 28,1 | **+115 / −53** | +105 / −51 | +119 / −54 | borne basse (2 semaines) |
| Calcium corrigé | 2001-02 | 409 | 2,0 | **+6 / −5** | +6 / −6 | +9 / −8 | borne basse (2 semaines) |
| DFGe (CKD-EPI 2021) | 2001-02 | 409 | 7,4 | **+23 / −18** | +24 / −19 | +22 / −18 | borne basse (2 semaines) |
| Granulocytes (%, automate) | NHANES III | 1742 | 9,2 | **+29 / −22** | +30 / −23 | (jeu principal) | borne basse (2 semaines) |
| Globulines | NHANES III | 1342 | 5,8 | **+18 / −15** | +18 / −15 | (jeu principal) | borne basse (2 semaines) |
| Osmolalité mesurée | NHANES III | 1342 | 1,2 | **+4 / −3** | +3 / −3 | (jeu principal) | borne basse (2 semaines) |
| ApoA1 | NHANES III | 838 | 8,5 | **+27 / −21** | +26 / −21 | (jeu principal) | borne basse (2 semaines) |
| ApoB | NHANES III | 850 | 9,9 | **+31 / −24** | +28 / −22 | (jeu principal) | borne basse (2 semaines) |
| Lp(a) | NHANES III | 952 | ET intra 7,63 | **± 21,15 (unités)** | ± 22,13 | — | borne basse (2 semaines), échelle additive |
| Capacité totale de fixation du fer | NHANES III | 1756 | 6,7 | **+21 / −17** | +21 / −17 | (jeu principal) | borne basse (2 semaines) |
| Saturation de la transferrine | NHANES III | 1756 | 31,4 | **+134 / −57** | +153 / −60 | (jeu principal) | borne basse (2 semaines) |
| Sélénium | NHANES III | 1714 | 6,8 | **+21 / −17** | +21 / −17 | (jeu principal) | borne basse (2 semaines) |
| Iode urinaire | NHANES III | 1148 | 70,9 | **+486 / −83** | +465 / −82 | (jeu principal) | borne basse (2 semaines) |

Lecture : pour l'hémoglobine, un changement de moins de +10 % ou −9 % entre deux bilans à 6 mois
n'est pas distinguable de la variabilité normale. Pour les indices dérivés (HOMA-IR, rapports,
FIB-4…), il n'existe pas d'étude EFLM à long terme : ce sont des bornes basses. Les CV_I utilisés
viennent de l'EFLM Biological Variation Database (biologicalvariation.eu, consultée le 10 novembre
2026). Ils ne sont pas reproduits ici, pour respecter la licence de la base.

**Marqueurs sans remesure** (statut « EFLM seul »). Hypothèses :
$CV = \sqrt{CV_I^2 + (0{,}5\,CV_I)^2}$ ; CV_I de la base EFLM, à long terme si une étude A/B existe (TSH), sinon à
court terme. Les CV_I eux-mêmes ne sont pas reproduits ici (licence de la base EFLM).

| Marqueur | Changement détectable (%), hausse / baisse |
|---|---|
| Thyroid stimulating hormone (TSH) | +77 / −43 |
| Testosterone | +55 / −36 |
| Sex hormone-binding globulin (SHBG) | +29 / −23 |
| Thyroxine - free (FT4) | +16 / −14 |
| DHEAS | +84 / −46 |
| Estradiol | +59 / −37 |
| Magnesium | +9 / −9 |
| Lipase | +27 / −21 |

**Trois familles se dessinent** (interprétation) :

| Variabilité | Marqueurs | Changement détectable |
|---|---|---|
| **Très stables** | VGM, TCMH, CCMH, RDW, HbA1c, sodium, chlorure, calcium, osmolalité | moins de 7 % |
| **Stables** | hémoglobine, hématocrite, hématies, protéines, albumine, VPM | environ 10 à 11 % |
| **Bruités** | CRP, insuline, triglycérides, ALAT, fer, LH, FSH, urines | souvent plus de 100 % à la hausse : une valeur isolée ne se compare presque pas |

**Deux points d'attention :**
- **Bicarbonates.** CV de 11 % dans NHANES III contre 6 % en 2001-2002 (jeu principal depuis le
  2026-11-12).
  - **Correction du 2026-11-11.** La première version de ce rapport donnait 18 % et l'attribuait à
    un artefact pré-analytique (perte de CO₂). C'était en réalité un **bug de lecture** : le code
    « 88 » (vide mais applicable) des champs à 2 chiffres de NHANES III était lu comme une valeur,
    sur 1 495 bicarbonates. Voir `DECISIONS.md`.
  - Après correction, le CV de NHANES III reste deux fois plus grand que celui de 2001-2002. Je n'en
    connais pas la cause.
- **Neutrophiles (%).** Dans NHANES III, la formule est faite à la main et ne porte que sur
  272 personnes.

## Comparaison aux RCV publiés (ajout du 2026-11-12)

Changement détectable à 6 mois de dix marqueurs, avant et après la correction, rapporté au RCV
publié (Westgard 2014 : $CV = \sqrt{CV_I^2 + I^2}$ ; EFLM : $CV_A = 0{,}5\,CV_I$). Valeurs publiées
reprises de l'audit ; fichier `Q1_comparaison_rcv_publies.csv`. Un RCV publié est à court terme :
un rapport un peu supérieur à 1 est attendu (variabilité à 6 mois, laboratoires réels).

| Marqueur | Avant (NHANES III) | **Après (2001-2002)** | RCV Westgard 2014 | Rapport Westgard avant → **après** (hausse) | Rapport Westgard après (baisse) | RCV EFLM | Rapport EFLM après (hausse / baisse) |
|---|---|---|---|---|---|---|---|
| Glycémie à jeun (plasma) | +29 / −23 | **+24 / −19** | +19 / −16 | 1,53 → **1,25** | 1,20 | +16 / −14 | 1,49 / 1,38 |
| HbA1c | +10 / −9 | **+5 / −5** | +6 / −6 | 1,67 → **0,91** | 0,87 | +4 / −4 | 1,37 / 1,30 |
| Cholestérol total | +26 / −21 | **+22 / −18** | +20 / −17 | 1,30 → **1,09** | 1,06 | +18 / −15 | 1,21 / 1,20 |
| LDL (calculé, à jeun) | +47 / −32 | **+37 / −27** | +27 / −21 | 1,74 → **1,37** | 1,28 | +27 / −21 | 1,37 / 1,28 |
| HDL | +43 / −30 | **+30 / −23** | +25 / −20 | 1,72 → **1,21** | 1,16 | +19 / −16 | 1,59 / 1,45 |
| Triglycérides (à jeun) | +111 / −53 | **+105 / −51** | +84 / −46 | 1,32 → **1,25** | 1,11 | +83 / −45 | 1,26 / 1,14 |
| ALAT | +181 / −64 | **+162 / −62** | +81 / −45 | 2,23 → **2,00** | 1,37 | +47 / −32 | 3,45 / 1,93 |
| GGT | +53 / −35 | **+52 / −34** | +51 / −34 | 1,04 → **1,02** | 1,01 | +29 / −22 | 1,80 / 1,56 |
| Créatinine | +21 / −17 | **+23 / −19** | +20 / −17 | 1,05 → **1,14** | 1,09 | +15 / −13 | 1,52 / 1,43 |
| CRP | +351 / −78 | **+351 / −78** | +246 / −71 | 1,43 → **1,43** | 1,10 | +182 / −65 | 1,93 / 1,20 |

- **Avec les méthodes de 2001-2002, les écarts à Westgard se resserrent** : de 1,04-2,23 à
  0,91-2,00 (hausse). L'HbA1c passe sous 1 (0,91) ; HDL, LDL, glycémie et triglycérides
  descendent à 1,2-1,4.
- **L'ALAT reste à 2,0.** Ce n'est pas le jeu : c'est l'ajout à long terme, tiré de 3 études EFLM
  notées A/B (CV_I 33 %). Avec toutes les études longues (notes A, B et C, n = 8 : CV_I 22 %), le
  changement détectable est de **+100 %**, soit 1,24 fois le RCV de Westgard. Le chiffre de +162 %
  est donc à lire avec cette sensibilité (colonne `cd6m_hausse_sens_noteC`).
- **La créatinine monte un peu** (1,05 → 1,14) : la recalibration affine de NHANES III et le passage
  à 2001-2002 relèvent légèrement le bruit relatif.

## Effets d'interventions rapportés au changement détectable

| Intervention | Marqueur | Effet moyen | Changement détectable à 6 mois | **Ratio**, 20-79 ans | Ratio, 30-55 ans | Ratio avec le bruit de NHANES III | Conclusion | Source (lecture) ; population |
|---|---|---|---|---|---|---|---|---|
| Activité physique (toutes formes) | Cholestérol total | −3 % | 18 % | **0,16** | 0,16 | 0,14 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | HDL | +4 % | 30 % | **0,15** | 0,15 | 0,11 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | LDL (calculé, à jeun) | −6 % | 27 % | **0,22** | 0,21 | 0,19 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique (toutes formes) | Triglycérides (à jeun) | −7 % | 51 % | **0,13** | 0,13 | 0,13 | visible seulement en moyenne de groupe | Smart 2025 (R) ; 148 ECR, adultes |
| Activité physique structurée | HbA1c | −9 % | 5 % | **1,70** | 1,76 | 0,94 | détectable chez une personne | Umpierre 2011 (R) ; diabète de type 2 |
| Activité physique aérobie | Glycémie à jeun (plasma) | −3 % | 19 % | **0,15** | 0,16 | 0,12 | visible seulement en moyenne de groupe | Wewege 2018 (R) ; syndrome métabolique |
| Activité physique (toutes formes) | Insuline (à jeun) | −20 % | 54 % | **0,37** | 0,36 | 0,37 | visible seulement en moyenne de groupe | Smart 2018 (R) ; surpoids ou stéatose |
| Alimentation méditerranéenne | Glycémie à jeun (plasma) | −3 % | 19 % | **0,16** | 0,17 | 0,14 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes, 57 essais contrôlés |
| Alimentation méditerranéenne | Insuline (à jeun) | −10 % | 54 % | **0,18** | 0,18 | 0,18 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HOMA-IR | −17 % | 58 % | **0,29** | 0,28 | 0,29 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HbA1c | −3 % | 5 % | **0,54** | 0,56 | 0,30 | limite | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | Cholestérol total | −3 % | 18 % | **0,16** | 0,15 | 0,14 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | LDL (calculé, à jeun) | −7 % | 27 % | **0,25** | 0,24 | 0,21 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | HDL | +3 % | 30 % | **0,09** | 0,09 | 0,06 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | Triglycérides (à jeun) | −10 % | 51 % | **0,20** | 0,20 | 0,19 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | ALAT | −25 % | 62 % | **0,40** | 0,39 | 0,38 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | GGT | −10 % | 34 % | **0,31** | 0,31 | 0,30 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Alimentation méditerranéenne | CRP | −29 % | 78 % | **0,37** | 0,36 | 0,42 | visible seulement en moyenne de groupe | Papadaki 2020 (TC) ; adultes |
| Perte de poids de 5 kg | ALAT | −18 % | 62 % | **0,29** | 0,29 | 0,28 | visible seulement en moyenne de groupe | Koutoukidis 2021 (R) ; stéatose (NAFLD) |
| Perte de poids de 5 kg | ASAT | −13 % | 47 % | **0,27** | 0,26 | 0,27 | visible seulement en moyenne de groupe | Koutoukidis 2021 (R) ; stéatose (NAFLD) |
| Perte de poids de 5 kg (poids stabilisé) | HDL | +4 % | 30 % | **0,12** | 0,13 | 0,09 | visible seulement en moyenne de groupe | Dattilo 1992 (R) ; 70 études |
| Vitamine D3, 25 µg/j | 25-OH vitamine D | +98 % | 54 % | **1,80** | 1,67 | — | détectable chez une personne | Autier 2012 (R) ; plus de 50 ans, sans calcium |
| Oméga-3 (EPA + DHA), 2 g/j | Triglycérides (à jeun) | −35 % | 51 % | **0,68** | 0,68 | 0,67 | limite | Wang 2023 (TC) ; 90 ECR, surtout hyperlipidémiques |
| Acide folique 0,8 mg/j | Homocystéine | −23 % | 32 % | **0,73** | 0,75 | — | limite | Homocysteine Lowering Trialists' Collaboration 2005 (R) ; 25 ECR |
| Fer oral (femmes réglées) | Hémoglobine | +4 % | 10 % | **0,38** | 0,38 | 0,36 | visible seulement en moyenne de groupe | Low 2016 (R) ; femmes réglées |

Règle pré-enregistrée :
- **≥ 1** : un effet moyen est détectable chez une personne ;
- **0,5 à 1** : limite ;
- **< 0,5** : visible seulement en moyenne de groupe.

**Non trouvé ou non chiffré** (`Q1_interventions_non_trouvees.csv`) :
- **CRP sous activité physique**, et **ALAT sous activité physique** : les résumés lus ne donnent
  pas d'estimation chiffrée ;
- **TG, LDL et cholestérol par kg perdu** : absents du résumé de Dattilo 1992 ;
- **glucose, HbA1c, insuline, CRP et acide urique sous perte de poids sans médicament** : rien
  trouvé avec ces requêtes ;
- **réduction de l'alcool** (GGT, HDL, TG, VGM) : rien trouvé avec ces requêtes ;
- **ferritine sous fer chez les sportifs** : différence standardisée seulement.

**Résultat (corrigé le 2026-11-12).** Sur 25 couples intervention-marqueur, chez les 20-79 ans :
- **2 sont détectables chez une personne** :
  - 25-OH vitamine D sous supplémentation (ratio 1,8) ;
  - HbA1c sous activité physique structurée (ratio 1,7 ; 0,9 avec le bruit de NHANES III), mais chez
    des diabétiques de type 2, dont l'HbA1c baisse plus que celle de personnes en bonne santé ;
- **3 sont limites** : **HbA1c sous alimentation méditerranéenne (0,5 ; 0,3 avec le bruit de NHANES
  III)**, TG sous oméga-3 à 2 g/j (0,7), homocystéine sous acide folique (0,7) ;
- **20 ne sont visibles qu'en moyenne de groupe**, dont tous les effets de l'activité physique et
  de l'alimentation méditerranéenne sur les lipides et la glycémie (ratios de 0,09 à 0,25).

Deux conclusions changent par rapport à la version d'avant les corrections :
- **HbA1c sous alimentation méditerranéenne** : « visible seulement en moyenne de groupe » (0,30)
  devient **« limite » (0,54)**, parce que le bruit de l'HbA1c de 2001-2002 est moitié moindre ;
- **ALAT sous alimentation méditerranéenne** : « limite » (0,59) devient **« visible seulement en
  moyenne de groupe » (0,40)**. Le bruit change peu ; c'est l'effet en % qui baisse, parce que
  l'ALAT médiane de 2001-2002 (23 U/L) est plus haute que celle de NHANES III (15 U/L, automate
  Hitachi 737). Le même effet absolu (−5,66 U/L) fait −25 % au lieu de −38 %.

Les conclusions sont les mêmes chez les 30-55 ans.

**Prédiction 4 (qualitative)** : **en partie fausse**.
- Bien prédit :
  - vitamine D ≥ 1 ;
  - activité physique sur les lipides < 0,5.
- Mal prédit :
  - TG sous oméga-3 à 2 g/j : 0,7, et non ≥ 1 ;
  - HbA1c sous activité physique : 1,7 (1,3 avant les corrections), et non < 0,5. Mais l'effet vient
    de diabétiques.

## Lecture (interprétation)

1. **La plupart des interventions réalistes ne produisent pas, en moyenne, un changement
   détectable chez une personne en 6 mois.** C'est vrai même avec des seuils qui sont des bornes
   basses, et la conclusion tient avec le bruit des méthodes modernes (2001-2002), plus faible. Les
   lipides et la glycémie sont l'exemple le plus net : leur effet moyen représente 9 à 25 % du
   changement détectable (6 à 21 % avec le bruit de NHANES III). **Exception nouvelle depuis la
   correction : l'HbA1c**, marqueur très stable avec une méthode moderne (changement détectable de
   5 %), devient « limite » sous alimentation méditerranéenne. Avec un analyseur aussi précis que
   celui de 2001-2002, une baisse moyenne de 3 % commence à se voir chez une personne.
2. **Les exceptions ont un point commun** : un effet direct sur le marqueur lui-même
   (supplémentation en vitamine D, acide folique) ou une population de départ très anormale
   (HbA1c de diabétiques, TG d'hyperlipidémiques).
3. **Pour une personne, un changement au-delà du seuil reste possible** si elle répond plus que la
   moyenne. Ces effets moyens ne disent rien de la dispersion des réponses individuelles.
4. **Montrer un effet moyen demande un groupe** : un groupe d'environ 100 personnes, par exemple,
   suffirait à voir des effets que personne ne peut voir seul (non calculé ici).

## Écarts et compléments au protocole

- **CV_A des marqueurs sans remesure.** Le protocole prévoyait les fiches de contrôle qualité
  NHANES, sinon la spécification EFLM. Les fiches n'ont pas été lues ; la spécification EFLM
  (0,5 × CV_I) a été utilisée pour tous.
- **Filtre de matrice ajouté** (sérum, plasma, sang total) pour le CV_I à long terme. Il ne change
  rien aux études A/B. Il écarte des études urinaires de note C, qui donnaient des CV aberrants
  pour le sodium et le potassium.
- **Sensibilité non pré-enregistrée** : CV_I à long terme avec les études de note C
  (colonne `cd6m_hausse_sens_noteC`). Elle relève les seuils, par exemple :
  - triglycérides : +125 % au lieu de +111 % ;
  - GGT : +77 % au lieu de +53 % ;
  - B12 : +69 % au lieu de +48 %.
- **Médiane de départ** pour convertir les effets en % : médiane NHANES des 30-55 ans, issue du jeu
  principal (2001-2002 depuis la correction du 2026-11-12 pour les marqueurs dont la méthode a changé ;
  NHANES III pour les autres). Exception, depuis la même date : un effet mesuré chez des diabétiques
  (HbA1c sous activité structurée) est rapporté à la médiane des HbA1c ≥ 6,5 % (7,6 %). La vitamine D
  de 2001-2002 a été dosée avant la standardisation LC-MS/MS.

## Limites

- Remesures à 2 semaines. Une extrapolation à 6 mois n'existe que pour quelques marqueurs.
- NHANES est américain, avec des laboratoires centralisés. Les données de NHANES III datent de
  1988-1994.
- Les effets d'interventions viennent souvent de populations malades (diabète, stéatose,
  hyperlipidémie). Chez des personnes en bonne santé, ils sont probablement plus faibles.
- Plusieurs effets ne viennent que de résumés. Les essais diffèrent en durée et en dose.

## Analyse secondaire (déclarée après les résultats, à la demande de l'auteur du projet)

Trois compléments, sans nouvelle donnée NHANES. Fichier : `Q1_secondaire_moyenner.csv` ; code : `q1_secondaire.py`.

**1. Population des méta-analyses.** Elle figure pour chaque couple dans le tableau ci-dessous. Beaucoup d'effets viennent de populations malades ou à risque : diabétiques, syndrome métabolique, stéatose, obésité, hyperlipidémie. Chez des adultes en bonne santé, ils sont probablement plus petits.
- **HbA1c sous activité physique** : ratio 1,7 chez des diabétiques de type 2 (Umpierre 2011 ; effet
  rapporté à une base de diabétiques depuis le 2026-11-12). Chez des **non-diabétiques**, rien trouvé avec ces requêtes : aucune méta-analyse d'activité physique sur l'HbA1c hors diabète. On ne peut donc pas dire si l'effet serait détectable chez une personne non diabétique.
- **Oméga-3** : sans hyperlipidémie, l'effet plafonne vers −40 mg/dL (Wang 2023, TC), soit le même ordre de grandeur que l'effet global.

**2. Deux références.**
- **Statine** (atorvastatine 10 mg/j ou équivalent) : −40 % de LDL (Law 2003, BMJ, résumé). C'est un effet **clairement détectable** chez une personne : ratio 1,48 (1,25 avec le bruit de NHANES III).
- **Perte de poids de 5-10 %**, d'après deux méta-analyses, sur un scénario de 7 kg :
  - lipides : Hasan 2020 (73 ECR, surpoids ou obésité, IMC moyen 36), par kg perdu après une intervention sur le mode de vie : TG −4,0 mg/dL, LDL −1,28, HDL +0,46 ;
  - ALAT : Koutoukidis 2021, −0,83 U/L par kg, chez des personnes avec stéatose.
  - L'article de Dattilo 1992, également lu, ne donne dans son résumé que la pente du HDL.
- **En appui seulement** : Magkos 2016 (Cell Metab, texte complet), un **petit essai unique** (19 personnes contre 14), chez des obèses non diabétiques. Il donne les seuls chiffres trouvés pour la glycémie, l'insuline et la CRP hors diabète. Ses effets sont estimés grossièrement, par la différence des variations des médianes.
- **Non trouvé avec ces requêtes** : une méta-analyse de l'effet d'une perte de poids sans médicament sur la glycémie, l'HbA1c ou la CRP chez des non-diabétiques. Look AHEAD (Wing 2011) ne porte que sur des diabétiques et ne donne que des rapports de cotes.

**3. Combien de mesures faudrait-il ?** Deux façons de réduire le bruit :
- **A, prélèvements rapprochés** : k prises de sang à quelques jours d'intervalle autour de chaque bilan, moyennées. Elles réduisent le bruit à court terme, mais pas la variation biologique à long terme. Si celle-ci dépasse à elle seule l'effet, c'est **impossible** ;
- **B, tendance** : m bilans espacés avant l'intervention et m après, moyennés. Tout le bruit à 6 mois se divise par m.

Hypothèses : erreurs indépendantes, effet stable dans le temps, même laboratoire. Quand le seuil est une borne basse (pas d'étude à long terme), A et B donnent le même chiffre, **optimiste**. Calcul : $k = \sigma_{obs}^2 / (\sigma^{*2} - \sigma_{LT}^2)$ et $m = \sigma_{6m}^2 / \sigma^{*2}$, avec $\sigma^* = |\ln(1+\text{effet})| / (1{,}96\sqrt2)$.

| Intervention | Marqueur | Population | Effet moyen | Ratio | **A : prises de sang par bilan** | **B : bilans avant et après** | 30-55 ans (A / B) | Source (lecture) |
|---|---|---|---|---|---|---|---|---|
| Activité physique (toutes formes) | Cholestérol total | 148 ECR, adultes | −3 % | 0,16 | **45** | **45** | 49 / 49 | Smart 2025 (R) |
| Activité physique (toutes formes) | HDL | 148 ECR, adultes | +4 % | 0,15 | **37** | **37** | 35 / 35 | Smart 2025 (R) |
| Activité physique (toutes formes) | LDL (calculé, à jeun) | 148 ECR, adultes | −6 % | 0,22 | **27** | **27** | 29 / 29 | Smart 2025 (R) |
| Activité physique (toutes formes) | Triglycérides (à jeun) | 148 ECR, adultes | −7 % | 0,13 | **> 100** | **> 100** | > 100 / > 100 | Smart 2025 (R) |
| Activité physique structurée | HbA1c | diabète de type 2 | −9 % | 1,70 | **1** | **1** | 1 / 1 | Umpierre 2011 (R) |
| Activité physique aérobie | Glycémie à jeun (plasma) | syndrome métabolique | −3 % | 0,15 | **57** | **57** | 50 / 50 | Wewege 2018 (R) |
| Activité physique (toutes formes) | Insuline (à jeun) | surpoids ou stéatose | −20 % | 0,37 | **13** | **13** | 13 / 13 | Smart 2018 (R) |
| Alimentation méditerranéenne | Glycémie à jeun (plasma) | adultes, 57 essais contrôlés | −3 % | 0,16 | **47** | **47** | 41 / 41 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Insuline (à jeun) | adultes | −10 % | 0,18 | **55** | **55** | 58 / 58 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HOMA-IR | adultes | −17 % | 0,29 | **22** | **22** | 26 / 26 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HbA1c | adultes | −3 % | 0,54 | **4** | **4** | 4 / 4 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Cholestérol total | adultes | −3 % | 0,16 | **49** | **49** | 52 / 52 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | LDL (calculé, à jeun) | adultes | −7 % | 0,25 | **20** | **20** | 22 / 22 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | HDL | adultes | +3 % | 0,09 | **94** | **94** | 90 / 90 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | Triglycérides (à jeun) | adultes | −10 % | 0,20 | **46** | **46** | 47 / 47 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | ALAT | adultes | −25 % | 0,40 | **impossible** | **12** | impossible / 13 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | GGT | adultes | −10 % | 0,31 | **15** | **15** | 15 / 15 | Papadaki 2020 (TC) |
| Alimentation méditerranéenne | CRP | adultes | −29 % | 0,37 | **21** | **21** | 23 / 23 | Papadaki 2020 (TC) |
| Perte de poids de 5 kg | ALAT | stéatose (NAFLD) | −18 % | 0,29 | **impossible** | **24** | impossible / 25 | Koutoukidis 2021 (R) |
| Perte de poids de 5 kg | ASAT | stéatose (NAFLD) | −13 % | 0,27 | **impossible** | **22** | impossible / 25 | Koutoukidis 2021 (R) |
| Perte de poids de 5 kg (poids stabilisé) | HDL | 70 études | +4 % | 0,12 | **53** | **53** | 51 / 51 | Dattilo 1992 (R) |
| Vitamine D3, 25 µg/j | 25-OH vitamine D | plus de 50 ans, sans calcium | +98 % | 1,80 | **1** | **1** | 1 / 1 | Autier 2012 (R) |
| Oméga-3 (EPA + DHA), 2 g/j | Triglycérides (à jeun) | 90 ECR, surtout hyperlipidémiques | −35 % | 0,68 | **3** | **3** | 3 / 3 | Wang 2023 (TC) |
| Acide folique 0,8 mg/j | Homocystéine | 25 ECR | −23 % | 0,73 | **3** | **3** | 2 / 2 | Homocysteine Lowering Trialists' Collaboration 2005 (R) |
| Fer oral (femmes réglées) | Hémoglobine | femmes réglées | +4 % | 0,38 | **impossible** | **7** | impossible / 7 | Low 2016 (R) |
| Statine (atorvastatine 10 mg/j ou équivalent) | LDL (calculé, à jeun) | 164 essais contre placebo | −40 % | 1,48 | **1** | **1** | 1 / 1 | Law 2003 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | Triglycérides (à jeun) | 73 ECR, surpoids ou obésité (IMC moyen 36) | −23 % | 0,45 | **8** | **8** | 8 / 8 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | LDL (calculé, à jeun) | 73 ECR, surpoids ou obésité | −7 % | 0,27 | **17** | **17** | 19 / 19 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | HDL | 73 ECR, surpoids ou obésité | +7 % | 0,23 | **16** | **16** | 16 / 16 | Hasan 2020 (R) |
| Perte de poids de 7 kg (≈ 5-10 %), méta-analyse | ALAT | stéatose (NAFLD) | −25 % | 0,41 | **impossible** | **11** | impossible / 12 | Koutoukidis 2021 (R) |
| Perte de poids de 5 % (essai unique, petite taille) | Glycémie à jeun (plasma) | obèses non diabétiques, n = 19 contre 14 | −4 % | 0,21 | **27** | **27** | 23 / 23 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | Insuline (à jeun) | obèses non diabétiques | −14 % | 0,25 | **28** | **28** | 30 / 30 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | Triglycérides (à jeun) | obèses non diabétiques | −38 % | 0,74 | **3** | **3** | 3 / 3 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | HDL | obèses non diabétiques | +0 % | 0,01 | **> 100** | **> 100** | > 100 / > 100 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | ALAT | obèses non diabétiques | −17 % | 0,27 | **impossible** | **28** | impossible / 30 | Magkos 2016 (TC) |
| Perte de poids de 5 % (essai unique, petite taille) | CRP | obèses non diabétiques | +5 % | 0,01 | **> 100** | **> 100** | > 100 / > 100 | Magkos 2016 (TC) |

**Lecture pratique** (interprétation) :
- **Une seule mesure suffit** quand l'effet est direct et fort : vitamine D sous supplémentation, LDL sous statine, et HbA1c chez des diabétiques.
- **Environ 3 à 8 mesures de part et d'autre** pour les TG sous oméga-3 ou sous perte de poids, l'homocystéine sous acide folique, et l'HbA1c sous alimentation méditerranéenne (avec le bruit de 2001-2002).
- **Des dizaines de mesures** pour les lipides et la glycémie sous activité physique, alimentation ou perte de poids modérée : en pratique, ce n'est jamais faisable pour une personne.
- **Impossible par des prélèvements rapprochés** pour l'ALAT et l'hémoglobine : la variation à long terme dépasse déjà l'effet. Seule une tendance sur plusieurs bilans peut alors le montrer.
- Ces nombres supposent le même laboratoire. Un changement de laboratoire (Q5) les augmente.
