---
type: regex
pattern: "pile d['’]appels|files? des? t[âa]ches|files? des? microt[âa]ches|boucle d['’][ée]v[ée]nements|gestionnaires? de clic|param[èe]tres? du reste|\\b[ée]talement\\b|fermeture lexicale|mode strict|portée lexicale"
flags: i
match: not_contains
target: last_message
---

A technical concept keeps its English name — `call stack`, `task queue`, `microtask queue`, `event loop`, `click handler`, `rest parameter`, `spread`, `closure`, `scope`, `strict mode` — with the prose around it in the learner's language (see references/style-fr.md).
