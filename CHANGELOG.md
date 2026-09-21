# Changelog

Learner-visible changes, newest first. Versions match `plugins/techne/.claude-plugin/plugin.json`.

## 0.9.7

- Messages in French read like a colleague writing on Slack: complete sentences, no bold labels followed by fragments. The rules no longer describe a message as a template to fill.
- A French style reference (`references/style-fr.md`) pairs the wording learners reported with its natural version; it is read only when the learning language is French.
- A style eval suite (`plugins/techne/evals/style-fr-*`) checks a brief, a failed-quiz feedback and a calibration proposal against those patterns.
