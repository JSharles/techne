# A learning language may carry its own style file, and message structure is an intention

A French learner kept finding Techne's messages translated rather than written: stacked nouns, verbless fragments, bold labels followed by fragments (« **Terminé quand :** … »), the skill's own words (« sonde », « learner ») leaking into the prose. The general rules in `pedagogy.md` already asked for native, composed prose, and did not stop it. Two causes were found. The skill described every message as a template — three parts, then an orientation line, then "four lines" for closings and returns — and the model filled the template literally, one bold label per part. And rules stated in the abstract, in English, gave the model no French to imitate.

The message rules now describe what a message must achieve, and say that it is written as a colleague would on Slack, in sentences; the parts are never labels. A learning language may have a `references/style-<language>.md` file of paired examples, sentences to avoid and their natural version, taken from what learners reported. It adds no rule: it shows the general rules at work in that language. It is read only when the learner chose that language, which is the one place skill source may hold learner-language text.

A suite of eval cases (`plugins/techne/evals/style-fr-*`) runs Techne on three reference situations — a brief, feedback on a failed quiz, a calibration proposal — and grades the replies with regex graders for the reported patterns and an LLM grader against a reference version. The regex graders are kept consistent with the style file by the unit tests.

## Consequences

- Another language gets its style file when a learner of that language reports the same drift; until then the general rules apply alone.
- The eval suite costs real model calls, so it runs before a release that touches learner-facing wording, not on every change.
- A pattern a regex cannot see reliably (passive voice, stacked nouns, words with a plain meaning such as « preuve ») is judged only by the LLM grader.
