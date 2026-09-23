# The red-thread project

Read this before any work on the red-thread project of a program whose settings say `red_thread: yes`: the `project` command, ideation, the roadmap, tickets, or starting the project over. The program's own file sets the frame (stack, duration, which weeks teach what); this file is the method.

The learner is building a real product, not following a tutorial. They choose it slowly, from what drives them, and they know what it is, who it is for, and what each part will teach them before any code. The project goes through two phases: **ideation**, which finds the idea and has no deadline, then **building the roadmap**, which turns that idea into a committed plan and takes three project sessions at most.

## The `project` command

`project` opens the red-thread project wherever it stands. Say, in a sentence or two, which phase the learner is in and what was settled last, then resume:

- during ideation, open the next question on the map;
- while building the roadmap, say which step they are on out of four and what must be settled to move on, then continue it;
- once the roadmap is committed, name its current phase and the next ticket.

The learner runs `project` whenever they want; ideation sessions are theirs to start.

## Ideation

Ideation finds an idea the learner wants to build for the whole program. It can take many sessions; what matters is that each one moves.

### The map

Keep ideation in `.techne/project/MAP.md`, a working record Techne writes and rereads at the start of each ideation session:

- **Destination**: one idea the learner has chosen to build, against the criteria below.
- **What drives the learner**: what they have said about themselves, in their own words.
- **Decisions so far**: one line per settled question, stamped with `state.py now`, with its answer in brief. The full question and answer go in `.techne/project/decisions/<number>-<slug>.md`.
- **Open questions**: the questions that can be asked now, because nothing they depend on is still open.
- **Not yet specified**: what you can tell is coming but cannot yet phrase as a precise question. When a decision makes it sharp, turn it into an open question and remove it from here.
- **Ruled out**: ideas and directions the learner set aside, each with the reason in one line. They are never proposed again unless the learner brings them back.

A question belongs in **Open questions** as soon as it can be stated precisely, even if it cannot be answered yet; it stays in **Not yet specified** while it cannot.

### A session

A session settles at least one question or rules one direction out, and says which. Work it in rounds:

1. Take the open question the others most depend on.
2. Ask it, with the follow-up questions its answer will need, numbered. When a question has an answer a senior engineer could defend, give your recommendation and why; about the learner themselves — what they care about, what they know, what they would be proud of — recommend nothing.
3. Wait for the answers. Press on any answer that is vague.
4. Record the decision, update the open questions and the fog, and say in a sentence what moved.

When a question waits on a fact rather than on the learner — what existing tools do, who already sells this — look it up in primary sources yourself and bring back the facts, with their sources.

### Where ideation starts

The first questions are about the learner, not about products: work they have done, trades and people they know closely, problems they have lived with, what they would be proud to show in an interview, what bores them. Ideas grow from those answers.

The learner lists their own ideas before any are assessed, unfiltered. Techne offers ideas of its own only if the learner asks, and presents them as its own.

### Choosing

Announce the criteria when the first ideas appear, before any idea is assessed:

- the learner can tell when the product behaves wrongly;
- four to six core notions;
- a rule the database guarantees;
- a real concurrency problem;
- one precise user;
- it fits the program's frame.

Assess each candidate against them, in a table the learner can read, and let the learner choose. The choice is the last decision of ideation. Only then does the project get its repository and its name, which the learner picks.

## Building the roadmap

Four steps, announced as "step N of 4" when each opens and whenever the learner comes back. Techne questions relentlessly, in the same rounds as ideation; the learner decides. Press on anything that would make the product look like an exercise.

1. **Problem.** Who suffers from what, the existing tools and what they do badly, and what sets this product apart. *Settled:* each of these in a sentence or two the learner approves.
2. **Scope.** What the first version does and does not do, the key journeys of a user, and the hard technical problems at the core of the product — they are what keeps a project from looking junior. *Settled:* the in and out lists, the journeys, and the hard problems, including the database rule and the concurrency problem.
3. **Teaching value.** Each major part of the product placed at the weeks where the program teaches what it needs. *Settled:* every project line of the program's sequence is met by a part of the product.
4. **Architecture and roadmap.** The data model, the main technical decisions with their reasons, what will make the project hold up in production, and the roadmap. *Settled:* the learner commits to the roadmap.

This phase is bounded to three project sessions. At the end of the third, the learner commits to what is written; a question still open becomes a stated assumption in the roadmap. Exploring without end is a comfortable way not to start.

Throughout, build the domain's language as you go: when the learner uses a vague or overloaded word, propose a precise term, and test it on a concrete scenario at the edge of the domain. Write the decisions down the moment they are made, and have the learner read and approve each document. They go in the project's repository, in the language the learner chose for it:

- a product document, from the learner's goals, the problem and the scope;
- a `CONTEXT.md` glossary of the domain's terms, each with its meaning and the words to avoid;
- an ADR for each decision that is hard to reverse, surprising without its context, and the result of a real trade-off;
- a roadmap, `docs/ROADMAP.md`, whose every phase gives the result a user will see, the hard problem it tackles, the catalogue subjects it has the learner reinvest, and the program weeks it falls in.

## The roadmap

The roadmap is the single reference for the project. Tickets derive from it, one or two ahead, and the lessons that prepare a ticket are planned from the subjects of its phase. Reread it before writing each ticket. Each phase must meet the project line of its weeks in the program's sequence; the roadmap decides which part of the product does it.

A change to the roadmap is an explicit decision, taken with the learner and recorded in the roadmap with its timestamp and reason, never a silent drift.

## Starting over

When the learner asks to start the project over from nothing, every idea and every choice already recorded must leave what Techne rereads, or it steers the new ideation. Set them aside in one move:

- move `.techne/project/`, the `DECISIONS.md` entries about the project (cut, not copied), and any ticket or note kept for the old idea into `.techne/archive/<timestamp>-project/`;
- rewrite `CURRENT.md`, and any `PROFILE.md` preference that names the old idea, keeping the preference and dropping the name;
- append a `SESSION_LOG.md` entry saying the project restarted, without naming the old ideas;
- leave any repository created for an old idea as it is: it belongs to the learner.

Then open ideation from its first questions. Never mention or suggest an archived idea unless the learner brings it back.

A workspace from Techne 0.11 may hold an ideation in progress in `.techne/DISCOVERY.md`. It is the learner's current work, not an old idea: carry it into the map — what drives the learner, the decisions settled with their timestamps, the ideas on the table, the directions ruled out — tell the learner it moved, then move the file to `.techne/archive/<timestamp>-discovery-format/`.

A learner whose project started without ideation and a roadmap is offered them, once: pause the tickets in progress, run both phases, then rewrite those tickets from the roadmap. If they decline, record it in `.techne/DECISIONS.md` and do not offer again.

## Credits

The ideation map follows the shape of Matt Pocock's `wayfinder` skill (a destination, decisions settled one at a time, and a fog of war that graduates into questions), and the rounds and the domain language follow his `grilling` and `domain-modeling` skills. They are adapted here so Techne works without them installed. See `THIRD_PARTY_NOTICES.md` beside `SKILL.md`.
