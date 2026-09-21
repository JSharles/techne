---
type: regex
pattern: "\\blearners?\\b|\\bsondes?\\b|\\bassisté|\\bprobes?\\b|\\btimebox|\\bcheckpoint|\\bH[0-4]\\b|\\bfai[a-z]* sens\\b|\\badress(er|é|ons|ez)"
flags: i
match: not_contains
target: last_message
---

None of Techne's machinery words or of the calques listed in references/style-fr.md.
