# A project ticket may bring something new, if a lesson comes first

ADR 0003 made the red-thread project the place of transfer: a subject is first learned on an isolated exercise, then reinvested in the project. The first ticket of a real project broke that silently. It asked the learner to set up a pnpm workspace holding a Next.js and a NestJS application, a monorepo they had never built and Techne had never taught. A project cannot always wait for every subject to pass through an isolated exercise first: its first ticket already needs a repository layout, and later ones need tools the catalogue does not isolate well.

Techne therefore teaches before the ticket. Before opening one, it lists the catalogue subjects the ticket mobilises and gives a lesson of about ten minutes on each one still `not_started`: the notion and how one goes about it, never a ready-made setup to copy. ADR 0003 still holds for everything else: the project remains where `transferred` is earned, and a subject met first in a ticket is only `discovered` or `assisted` there until later work shows more.

The same incident showed tickets that said what to do and never why. The program's ticket format now carries the reason for the ticket and for each imposed choice, what is known and what is new, a size in mornings, what is decided and what is the learner's, and every exclusion as a sentence. That format belongs to the program; the lesson rule and the slicing review belong to the method, since they touch evidence and help levels (ADR 0010).

## Consequences

- Some project mornings start with a short lesson, so a ticket can take longer than its code alone.
- A block on something neither the ticket nor a lesson covered makes the ticket void, like any activity Techne broke, and is recorded as an issue.
- Review signal: during a ticket, the learner never gets stuck on something that neither the ticket nor its lessons covered. Each recorded issue of that kind reopens this decision.
