# Suivi, étape 0 — modèle « sang seul »

Protocole et prédiction : `DECISIONS.md` (pré-enregistrement « Suivi, étape 0 »). Code : `src/aging_clock/sang_seul.py` ; panel : `config/panels/checkup_sang_seul.yaml` ; sorties détaillées : `reports/checkup_sang_seul/`.

**Réserve commune à la piste « suivi »** : nos remesures sont à environ 2 semaines ; à 6 mois et sans contrôle de l'heure ni du jeûne, le bruit sera plus grand. Les chiffres de fiabilité de cette piste sont des bornes basses.
**Analyse principale** : mêmes personnes (validation n = 9 276, 978 décès), C de référence âge +
sexe 0,807.

| Score | C sang seul [IC 95 %] | C complet | Différence appariée [IC 95 %] | Prédiction (CV) | Gain vs âge + sexe | HR / ET (ET de l'écart) | Obs./prédit ; pente [IC] |
|---|---|---|---|---|---|---|---|
| Global | 0,850 [0,838 ; 0,861] | 0,853 | −0,0036 [−0,0056 ; −0,0013] | −0,0032 | +0,043 | 1,91 (6,8 ans) | 0,92 ; 0,99 [0,94 ; 1,04] |
| Cardiovasculaire (lipides) | 0,810 | 0,819 | −0,0087 [−0,0118 ; −0,0055] | −0,0060 | +0,003 [0,002 ; 0,005] | 1,18 (2,0 ans) | 0,92 ; 0,95 [0,89 ; 1,01] |
| Métabolique (glycémie, HbA1c) | 0,811 | 0,819 | −0,0079 [−0,0109 ; −0,0048] | −0,0056 | +0,005 [0,002 ; 0,007] | 1,20 (2,0 ans) | 0,95 ; 0,98 [0,92 ; 1,04] |
| Rénal, hépatique, inflammatoire | identiques au modèle complet (0,820 ; 0,830 ; 0,833) | | 0 | 0 | | | 0,95-0,96 ; ≈ 1 |

**Règles pré-enregistrées.**
- Prédictions **compatibles** pour les trois scores qui changent : −0,0032, −0,0060 et −0,0056
  sont chacune dans leur IC.
- Perte de discrimination du global **faible** : borne basse −0,0056 > −0,010.
- Calibration **acceptable** pour tous les scores.

**Analyse secondaire** (cohorte propre, cas complets sur les 19 marqueurs : 14 880 personnes en
développement, 9 914 en validation, 1 087 décès) : C global 0,851 (référence 0,808), rapport
observé/prédit 0,92, pente 1,01.

**Lecture** (interprétation) :
- le score global « sang seul » perd très peu (−0,004 de C) ;
- en revanche, sans tension ni mensurations, le **cardiovasculaire** (lipides seuls) et le
  **métabolique** (glycémie, HbA1c) n'apportent presque plus rien au-delà de l'âge et du sexe
  (gain de C +0,003 et +0,005). Leur écart d'âge ne varie que de 2,0 ans (écart-type) entre
  personnes, contre 3,7 et 3,9 ans dans le modèle complet. Ces deux systèmes ne pourront pas porter
  des affirmations fortes ;
- note technique : la valeur p bootstrap affichée « 2,000 » pour les systèmes identiques est un
  artefact de la formule quand toutes les différences sont nulles ; elle se lit « sans objet ».
