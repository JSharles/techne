# The feedback journal is an append-only file beside the state, not part of it

Learner reports are evidence about Techne, not about the learner, and they accumulate without bound: hundreds of lines over a programme, each interesting long after the activity that produced it. Keeping them in `STATE.json` would grow the file the agent reads on every turn and mix two lifetimes in one document. They live instead in `.techne/feedback.jsonl`, one JSON object per line, appended and never rewritten except to mark an entry handled.

Each entry carries its own schema version, an identifier derived from the highest one already used, the moment it was recorded, its type, its text, the activity and track it came from, and a status. `feedback.py` owns every read and write, as `state.py` owns `STATE.json` (ADR 0004), and the workspace validator checks the journal's entries.

## Consequences

- The file is created on the first entry, so existing workspaces need no migration and the state format is untouched.
- A damaged line is skipped on read and reported by the validator, rather than failing the session or recycling an identifier.
- Nothing here is learning evidence: a report never moves the mastery map.
