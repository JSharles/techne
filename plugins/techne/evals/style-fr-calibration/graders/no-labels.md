---
type: regex
pattern: "\\*\\*[^*\\n]{1,40}?\\s*:\\s*\\*\\*|\\*\\*[^*\\n]{1,40}\\*\\*\\s*:|^\\s*(maintenant|terminé quand|fini quand|ce que ça [^:\\n]{1,30}|voulu|pas voulu|prochaine étape|objectif|contexte|résultat attendu|critères?|hors périmètre|taille|décidé|à toi de décider|bénéfice|coût|impact)\\s?:"
flags: im
match: not_contains
target: last_message
---

No label followed by a fragment, bold or not, such as « **Terminé quand :** … » or « Ce que ça coûte : … » at the start of a line (see references/style-fr.md).
