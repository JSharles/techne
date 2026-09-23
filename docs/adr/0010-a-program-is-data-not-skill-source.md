# A program is data the learner owns, not skill source

Techne started with two curricula written into its own references, which made every new course a change to the skill. The engine and the course are now separate: Techne owns the method — lesson then practice, easy first, evidence, graded help, spaced retrieval, lucid feedback — and a **program** is a Markdown file that owns the content.

A program declares its identity, its units, its subject catalogue, and exactly five settings: the activity kinds it uses, its lesson-to-practice balance, its default timeboxes, whether it has a red-thread project, and the mastery ceiling for its survey subjects. The set is closed: a sixth setting is refused, the way an unknown subject identifier already is. Programs shipped with the skill live beside it; the learner's own live in the workspace and win on an identifier clash.

Subjects were shared by identifier across programs, so `dsa.bfs` was one subject with one mastery entry whatever taught it; ADR 0020 reversed this, and each program now keeps its own evidence. A program ends when its catalogue is covered, never after a fixed number of weeks.

A program is also self-contained: its catalogue and sequence describe everything it teaches, including what another program covers, so a stranger can follow it alone. Shared identifiers let evidence count across programs, but they never justify removing content from one because another has it.

## Consequences

- Any number of programs can run at once, driven by a weekly schedule the learner owns; the fixed morning/afternoon blocks and their `engineering` and `ai` commands disappear. ADR 0021 removed the schedule: the learner organises their own time.
- Two programs declaring the same subject must mean the same thing; the validator checks it, and enrolment refuses an invalid program without disturbing the others.
- The method's guarantees survive a new course, because a program cannot redefine evidence, help levels, or review scheduling.
