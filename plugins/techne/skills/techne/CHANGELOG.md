# Changelog

Learner-visible changes, newest first. Versions match `plugins/techne/.claude-plugin/plugin.json`.

## 0.14.0

- Every technical concept keeps its English name — `call stack`, `task queue`, `event loop`, `closure`, `scope`, `hoisting`, `rest parameter`, `click handler`, `strict mode` — and only the sentence around it is in your language, headings included. You learn the notion and the word you will need with an English-speaking colleague at the same time.
- A lesson or an exercise never uses syntax the programme has not taught you yet. When it would have to, Techne rewrites the activity instead of explaining the accident.
- When you design a function's signature, the brief prints how it is called and what it returns, including the edge case the tests check.
- Exercise folders ship a working editor setup, so your editor does not report errors on code that runs.
- After two explanations of the same notion that do not land, Techne changes support instead of rephrasing: first a file you run and watch, then an exercise where that notion is the only blank. It also prefers the shape you already work in — a class before a method in an object literal.
- An exercise never leans on a subject you have only seen once; that subject is taught or practised first.
- Words from the product or the browser — click handler, panel, strict mode — are defined the first time they appear, like the language ones.
- When the programme you have open has nothing due, Techne carries on with it instead of offering another programme's reviews.
- Every lesson, exercise, brief and question is reread before you see it, against five checks: relevance, prerequisites, contract, code actually run, and teaching quality. What fails is rewritten, not patched after you stumble.

## 0.13.1

- Techne tells you what changed after an update, once, when you come back.
- A session lasts as long as you want it to. Techne no longer asks whether you want to stop for today: when you finish an activity, it opens the next one in the programme's sequence, so working longer takes you further instead of repeating the same work.

## 0.13.0

- Each program keeps its own evidence: what you prove in one never counts in another, even when both teach the same notion. Enrolling in a program that shares a domain with one you follow is refused.
- A survey domain is any catalogue domain titled `Survey`, so each program can have its own.
- Reviews and transfers stay inside the program you have open: opening one never brings you another program's recall. A review left behind still goes stale, because forgetting does not wait.
- No more timetable: enrol in a program and it opens at once, open any program whenever you want, for as long as you want. Techne picks up where you left off and never says you lack the time. The `schedule` command and `SCHEDULE.md` are gone, and programs advance in sessions rather than mornings and afternoons.
- The first start asks which program you want to begin with, instead of enrolling you in every shipped program.

## 0.12.1

- The T-shaped Product Engineer program no longer counts three phantom subjects read from a sentence of its catalogue, which kept it from ever being covered.
- A program's domain may be named with digits, such as `a11y.*`; a catalogue heading that names no domain is refused with its reason instead of merging its subjects into the domain above.

## 0.12.0

- A `project` command opens your red-thread project wherever it stands, whenever you want, outside the schedule.
- Choosing the project is now an ideation with no deadline. It starts from what drives you — work you have done, people and trades you know, problems you have lived — and settles one decision per session on a map kept in your workspace. Techne offers ideas of its own only if you ask.
- Until the project is chosen, project mornings become isolated practice, so the programme keeps moving.
- Once you choose, building the roadmap takes four announced steps over three project mornings at most: problem, scope, teaching value, architecture and roadmap.
- The method follows Matt Pocock's `wayfinder`, `grilling` and `domain-modeling` skills, adapted inside Techne so it works without them installed.

## 0.11.0

- Product discovery starts from a blank page and runs in seven announced steps: goals and frame, your ideas, the choice against criteria stated in advance, the problem, the scope, the teaching value, and the architecture with the roadmap. Techne tells you which step you are on and what must be settled to move on.
- Your ideas come first; Techne offers its own only when you ask. The project's repository and name are created only once you have chosen.
- Starting discovery over sets every earlier idea aside in an archive Techne never reads, and Techne no longer brings them up.
- Everything Techne records carries a full date, time and time zone from the system clock, and Techne no longer says "this morning" or "yesterday" without computing it.

## 0.10.0

- Before the first ticket of the red-thread project, Techne holds a product exploration with you in the conversation, three project mornings at most: the problem, the scope and its hard technical problems, what each part will teach you, and the architecture. You decide; Techne questions and writes it down.
- The exploration produces a product document, a `CONTEXT.md`, ADRs and a `docs/ROADMAP.md` in the project. The roadmap is the single reference: tickets and the lessons that prepare them derive from it, and it changes only by a decision you take and that is recorded.
- Lessons that prepare a ticket take their examples from your project, not from an imaginary one.
- Only questions that belong to an exercise stay out of the conversation; product, scope, planning and calibration questions are asked there normally.
- If your project started without an exploration, Techne offers one once, pauses the open tickets, and rewrites them from the roadmap.

## 0.9.9

- A proposal to change the method is argued in sentences, not laid out under labels such as « Ce que ça coûte : ».

## 0.9.8

- Before a project ticket, every subject it needs that you have never studied gets a ten-minute lesson first. A ticket no longer asks you for something Techne never taught.
- Tickets say why they exist and why each imposed choice, what you already know and what is new, how many mornings they take, what is decided and what is yours to decide, and what is out of scope in plain sentences.
- You write how you will slice a ticket before coding, and Techne reviews it in five minutes; the slicing counts as evidence for `flow.ticket-slicing`.
- Tickets are written one or two ahead, never the whole backlog at once.

## 0.9.7

- Messages in French read like a colleague writing on Slack: complete sentences, no bold labels followed by fragments. The rules no longer describe a message as a template to fill.
- A French style reference (`references/style-fr.md`) pairs the wording learners reported with its natural version; it is read only when the learning language is French.
- A style eval suite (`plugins/techne/evals/style-fr-*`) checks a brief, a failed-quiz feedback and a calibration proposal against those patterns.
