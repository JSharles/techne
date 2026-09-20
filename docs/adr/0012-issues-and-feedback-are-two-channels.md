# Issues go to Techne's developer, feedback goes to Techne the teacher

One command was carrying two conversations. Reporting that an exercise is broken is a defect report for whoever maintains Techne; saying that lessons are too long is a learner talking to their teacher about the programme in progress. Merging them meant product defects ended up in a pedagogical discussion, and pedagogical requests ended up in a list of tickets.

`issue <text>` records a defect or an improvement for the developer, with the activity it came from, and `extract-issues` exports the journal for the repository. `feedback <text>` stays pedagogical: a preference is applied at once and kept in the profile, a change touching evidence, the programme or assessment goes through calibration and is recorded as a decision.

## Consequences

- The journal is a product backlog, never learning evidence: nothing in it moves the mastery map.
- A learner who reports a broken exercise gets it recorded and their activity voided, without being dragged into a discussion about method.
- The 0.8.0 wiring, where `feedback` wrote to the journal and `report` exported it, is undone; `report` and `help` disappear with it.
