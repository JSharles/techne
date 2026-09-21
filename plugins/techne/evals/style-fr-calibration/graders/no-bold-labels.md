---
type: regex
pattern: "\\*\\*[^*\\n]{1,40}?\\s*:\\s*\\*\\*|\\*\\*[^*\\n]{1,40}\\*\\*\\s*:"
match: not_contains
target: last_message
---

No bold label followed by a fragment, such as « **Terminé quand :** … » (see references/style-fr.md).
