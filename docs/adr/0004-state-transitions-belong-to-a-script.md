# State transitions belong to a script, not to the agent

Techne's method depends on bookkeeping an agent is bad at: about 130 subjects, each with a state and evidence, spaced reviews at J+2, J+7 and J+21, transfer deadlines, block switches, and browser events. Letting the model edit `STATE.json` free-hand already produced a workspace stuck in calibration mode after one session. Every state transition therefore goes through `state.py` — mastery, reviews, transfers, checkpoints, block switches, event ingestion — and the agent never writes `STATE.json` itself.

The script owns what is mechanical and verifiable: it computes dates, refuses unknown subject identifiers and invalid states, schedules reviews and transfers, prunes overdue reviews, and applies `discovered` when a lesson check passes. Judgement stays with the agent: how many attempts a solution took, whether an explanation was convincing, whether a subject is genuinely independent.

## Consequences

- Narrative files (`SESSION_LOG.md`, `CURRENT.md`) stay hand-written: they are text for the learner, not state.
- `REVIEW_QUEUE.md` is deleted; the queue lives in `STATE.json` and is shown on the browser progress page. Two sources of one truth eventually means one wrong source.
- The subject catalogues in the curriculum references become load-bearing: an identifier that is not in them cannot be recorded.
