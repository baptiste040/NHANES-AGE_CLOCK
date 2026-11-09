# Fiche du modèle — panel `checkup_standard`

Fiche complétée au fil du projet. Version complète (coefficients figés, domaine de
validité, performances) au moment de l'export du modèle.

## Usage prévu

Estimer, pour un adulte de 20 à 79 ans vu en check-up de prévention, un âge biologique
global et par système, défini comme l'âge auquel le risque de décès à 10 ans de la
population de référence (même sexe) égale le risque prédit pour cette personne.

## Notes d'interprétation

- **Le score décrit un risque de mortalité, pas un état de santé « idéal ».** Un écart
  positif signifie un risque de décès supérieur à celui attendu pour l'âge et le sexe.
- **Traitements.** Si des variables de traitement (antihypertenseur, hypolipémiant)
  figurent dans le modèle, elles signalent une maladie connue : elles augmentent le
  risque prédit, donc l'âge biologique, des personnes traitées. Le score **ne mesure pas
  l'effet protecteur des traitements** et ne doit pas être lu comme une incitation à les
  arrêter. À marqueurs égaux, une personne traitée a un risque plus élevé parce que sa
  maladie sous-jacente existe, pas parce que le traitement est nocif.
- Les âges par système décomposent le risque par groupe de marqueurs ; ils ne sont pas
  des diagnostics d'organe.
