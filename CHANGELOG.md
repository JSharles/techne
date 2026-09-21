# Changelog

Learner-visible changes, newest first. Versions match `plugins/techne/.claude-plugin/plugin.json`.

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
