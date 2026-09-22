# The red-thread project has its own command, and choosing it has no deadline

ADR 0018 made discovery start from a blank page, but kept goals, ideas and choice inside the first of three project mornings. The learner judged that too fast: a project carried through the whole program cannot be chosen in a morning, and the choice should grow from what drives the learner rather than from a list of domains. They asked for a dedicated command and for Matt Pocock's `wayfinder`, `grilling` and `domain-modeling` skills to shape the method.

The red-thread project now has a `project` command and two phases. Ideation has no deadline: it keeps a map of decisions in the learner's workspace, starts from questions about the learner, settles at least one decision per session, and ends when the learner chooses an idea against criteria announced in advance. Until then, project mornings run as isolated practice, so the programme keeps moving and ideation is never rushed to free the schedule. Building the roadmap then keeps the three-morning bound of ADR 0017, in four announced steps.

The method lives in `references/project.md`, not in the Engineering program: any program with a red-thread project uses it, and a program never defines the method (ADR 0010). It adapts the three skills rather than calling them. `wayfinder`, `grill-me` and `grill-with-docs` cannot be invoked by the model, `wayfinder` needs an issue tracker configured by another of those skills, and a distributed plugin cannot count on any of them being installed. Their MIT notice ships beside the skill.

## Consequences

- The learner may spend weeks on ideation without losing programme time; transfers into the project wait for it to exist.
- Each ideation session must settle or rule out at least one question, so an open-ended phase still moves.
- ADR 0018's seven steps become ideation (its goals, ideas and choice) followed by the four steps of building the roadmap.
