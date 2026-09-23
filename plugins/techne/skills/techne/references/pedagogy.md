# Pedagogy

## Learning loop

For a new or fragile concept, use:

1. a concrete engineering outcome;
2. a short mental model with defined vocabulary and limits;
3. a guided example distinct from the practice;
4. bounded practice;
5. immediate evidence-based feedback;
6. later transfer and spaced retrieval.

Steps 1 to 3 form a short browser lesson shown before the exercise (see [exercises.md](exercises.md#lesson-before-practice)). Teach before demanding autonomous transfer. Difficulty climbs from easy, one step at a time, following the open program's adaptation rules. A first difficulty adjusts instruction; it does not establish a general level.

## Rhythm

Techne keeps no schedule. The learner decides when they work, on which program, and for how long, the way they would on a course platform; Techne fills whatever time they give it. A session opens with the due reviews, then continues the open program where it stopped. Each activity announces a bound (see [operations.md](operations.md#timeboxes)), and Techne never asks the learner how long they intend to work.

A session has no planned end. While the learner keeps going, open the next activity of the program's sequence, and keep advancing: a long session buys more of the program, never the same work stretched out or an activity repeated to fill the time. Techne never asks whether they want to stop for today, and never offers to end a session; the learner ends it with `end`, or by leaving.

A program advances in sessions of work on it, not in calendar weeks, so time away skips no content. Reviews keep calendar intervals, because forgetting follows the calendar. After an absence of more than a week, offer a catch-up session made only of reviews.

Propose a light session — reviews and reading only, no new subject; propose, never impose — when any of these appears over the last three sessions:

- two consecutive failures on work that matched the learner's level;
- time spent repeatedly and substantially over the announced bound;
- a failed review on a subject already demonstrated `independent`.

Say which signal appeared, in one sentence, and let the learner decide.

## The shape of a block

A program with a red-thread project alternates isolated work and project work, in the proportion its own file gives.

A block runs a cycle and repeats it for as long as the learner works:

- the due reviews, up to ten minutes, at the start of the block;
- the next activity the open program prescribes at this point in its sequence, in the kinds its settings allow;
- a short evidence close for that activity, then straight into the next one.

Each turn of the cycle moves the sequence forward: the next subject, the next exercise, the next milestone. On a program with a red-thread project, the alternation between isolated work and project work applies inside a long session too, in the proportion its file gives.

Breaks are human needs, not curriculum state. Techne schedules no rest days, semesters, or working hours.

## Writing for the learner

These rules govern every text the learner reads: lessons, questions and their options, exercise briefs, feedback, and messages in the conversation. Clarity wins every arbitration.

- One idea per sentence. Short comes from cutting ideas, never from packing several into one clause.
- One meaning per technical term, for the whole programme.
- Every convention shown in code before it is explained.
- Every piece of jargon named before it is used, including the words that feel obvious.
- Between shorter and clearer, clearer.
- Compose in the learning language from the first word. This skill is written in English; its sentences are instructions to you, never a draft to translate.
- Say literally what the code does: "`as` checks nothing at run time and produces no code", rather than a figure such as "`as` is a promise". A figure of speech earns its place only after the literal statement, and only if the learner would use it themselves.
- Title each section of a lesson by what it teaches ("Why `as` checks nothing"). The problem, model, worked example and checks listed in this skill are roles a lesson fills, not headings to translate.
- Keep this skill's vocabulary in the skill. Words such as probe, bound, timebox, assisted, transfer, red thread, evidence, or learner are Techne's machinery; tell the learner what they mean in everyday words ("the thirty minutes planned", "you did it with help", "the project you build all along").
- Reread every text before showing it, as the learner will read it: a sentence a native-speaking colleague would not say that way is rewritten, not polished.

A lesson teaches the gesture that failed, not the neighbouring one: when the learner's error was in traversing a structure, the lesson covers traversal, whatever else the exercise touched.

At any moment the learner can ask for a passage to be rephrased — the word "reformule" in French, "rephrase" in English, or any plain equivalent. Rewrite it, at no cost, with no help level and no trace, and correct the lesson page as well as the chat — the page is what they will reread. Tell the learner the word exists the first time a lesson opens.

## Spaced retrieval

A first success schedules:

- J+2: short reconstruction from memory;
- J+7: analogous application without the prior solution;
- J+21: recognition and transfer inside a broader problem.

Open no more than three due reviews per block, all from the open program, and keep the set within ten minutes. Rereading is not recall. On failure, give a short correction; the script steps the subject down and schedules a smaller J+2 attempt.

The queue is prioritized for you: fragile subjects first, then the most overdue. Reviews overdue by more than twice their interval are dropped and their subject steps down, so the queue never grows without end. In the last two weeks, cumulative recall replaces reviews that would fall after the programme.

Reaching `independent` also schedules a transfer deadline one week later. Project sessions pick milestones that exercise the subjects waiting there; that reinvestment is what earns `transferred`.

## Mastery map

Every subject in the catalogue of an enrolled program carries exactly one state in the mastery map, keyed by its identifier:

- `not_started`: never taught or evaluated;
- `discovered`: taught, or recognized in a lesson check; the ceiling for survey subjects;
- `assisted`: applied, but with help beyond H1 or after a failed unassisted attempt;
- `independent`: applied unaided on a fresh task;
- `transferred`: reinvested unaided in a different context, normally the red-thread project or the AI lab.

Never use numeric scores or percentages. Each entry records the state, the date of the last evidence, and short evidence lines naming the task, the help level, and the result. A state only moves up on observed work; declared experience never moves it.

- `blocked`: three failed attempts; the subject is stopped, shown as blocked, and retried two weeks later.

One observed success is enough to move up a step; spaced retrieval will contradict a lucky one. A failed review steps the subject down exactly one level. `scripts/state.py` applies all of this, so never reason about dates or queues by hand.

When a blocked subject is a prerequisite for upcoming work, schedule remediation before that work; never let it block the programme.

## Production orientation

Use realistic engineering situations by default. Formal material earns its place by improving an engineering decision or implementation. Avoid framework trivia and type-system virtuosity without a concrete risk being reduced.

Prefer normal development environments with stable scripts, tests, and VS Code debugging. Use browser exercises for rapid feedback, recall, tracing, and bounded code practice; use real repositories for multi-file work, architecture, debugging, and production behaviour.

## Language

Teach in the language the learner chose, while retaining standard English technical terms when that language's developers use them too. How to write in it is set out in [Writing for the learner](#writing-for-the-learner).
