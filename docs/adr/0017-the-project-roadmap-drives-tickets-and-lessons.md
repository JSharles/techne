# The red-thread project's roadmap is the reference for its tickets and lessons

After picking a warehouse management system as the red-thread domain, the learner received setup tickets straight away. The first milestone, "an operator sees the stock of a location", read like a tutorial step rather than the start of a product; the product, its users and its scope had never been worked out; and tickets were written as they came, with no plan behind them. The learner lost confidence in what was being built. They want a real product that does not look junior, and to agree with Techne on the product, its scope and what each part teaches them before any code.

The Engineering program therefore opens the project with a product exploration, held in the conversation and bounded to three project mornings: the problem, the scope and the hard technical problems at its core, the teaching value of each part placed on the programme's weeks, and the architecture. Techne questions and recommends; the learner decides; Techne writes it down in the project's repository — a product document, a `CONTEXT.md` glossary, ADRs, and `docs/ROADMAP.md`. The roadmap then becomes the single reference: tickets derive from it one or two ahead, the lessons that prepare a ticket are planned from its phase, Techne rereads it before each ticket, and it changes only by an explicit decision recorded in it.

The exploration method is described in the program itself rather than delegated to installable skills. It borrows the shape of Matt Pocock's `grilling` and `domain-modeling` skills (MIT licence): a tree of decisions asked in rounds with a recommended answer each, and a glossary and decision records written as decisions crystallise. Techne is distributed as a plugin and cannot count on those skills being installed, and a method that changed with what happens to be installed would make the programme unpredictable.

## Consequences

- The exploration takes up to three of the four project mornings of weeks 1–2, so the first vertical slice may only start then.
- The weekly "Red thread" lines of the sequence become constraints the roadmap must meet, rather than the product's features.
- A learner whose project began before this decision is offered the exploration once; their open tickets are paused and rewritten from the roadmap.
- ADR 0018 replaces the exploration with a seven-step discovery that starts from a blank page.
- ADR 0008's rule is narrowed in wording to exercise questions, since the exploration is a conversation of questions the learner decides rather than finds.
