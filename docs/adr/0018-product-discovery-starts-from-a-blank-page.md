# Product discovery starts from a blank page, and a restart sets earlier ideas aside

ADR 0017 opened the red-thread project with a product exploration, but it assumed the domain was already chosen, and week 1 still had Techne offer two or three domains. When the learner asked to start over from nothing, Techne kept the warehouse system recorded as a decision in `DECISIONS.md` and opened the first round of questions on warehouses. The same day it told the learner a choice had been made "this morning" when it dated from another day: the records carried a date at most, and the date came from the conversation.

Discovery now starts from a blank page and runs in seven announced steps — goals and frame, ideas, choice, problem, scope, teaching value, architecture and roadmap — each with what must be settled to move on and what gets written. The learner lists their ideas before Techne offers any, and ideas are sorted against criteria announced before the sort. The repository and the project's name come only after the choice. The three-morning bound holds: steps 1–3, then 4–5, then 6–7.

When the learner starts over, earlier ideas and domain choices are moved into `.techne/archive/`, which Techne never reads unless asked, rather than deleted. They are the learner's records, deleting them cannot be undone, and the learner may want an idea back; what made them harmful was being reread at every turn, and the archive ends that. Product decisions no longer go into `DECISIONS.md`, which holds method decisions only, so a restart has one discovery record to move instead of entries scattered among method decisions.

Every entry Techne writes in its records carries a full ISO 8601 timestamp from the system clock (`state.py now`, also in `state.py brief`), and relative times are computed from those stamps.

## Consequences

- The first project morning goes to goals, ideas and choice; code starts after the third.
- ADR 0019 gives ideation its own command and no deadline; building the roadmap keeps the three-morning bound.
- An archived idea stays on disk and can be restored by the learner; Techne never reopens it on its own.
- Entries written before this decision carry dates only; their time cannot be recovered and is not guessed.
