# Pedagogy

## Learning loop

For a new or fragile concept, use:

1. a concrete engineering outcome;
2. a short mental model with defined vocabulary and limits;
3. a guided example distinct from the practice;
4. bounded practice;
5. immediate evidence-based feedback;
6. later transfer and spaced retrieval.

Steps 1 to 3 form a short browser lesson shown before the exercise (see [exercises.md](exercises.md#lesson-before-practice)). Teach before demanding autonomous transfer. Difficulty climbs from easy, one step at a time, following [curriculum.md](curriculum.md#adaptation-rules). A first difficulty adjusts instruction; it does not establish a general level.

## Rhythm

Six full days and one light day per week, over twelve weeks. A full day is about three hours of morning curriculum and three hours of afternoon Applied AI. The light day is about ninety minutes of reviews and reading, with no new subject; it also absorbs what a busy week pushed back.

Techne never asks the learner to set a session duration. It decides the content and stops when the day's planned evidence is collected. Each activity announces a bound (see [operations.md](operations.md#timeboxes)).

The programme advances in working days — sixty morning and sixty afternoon blocks — not in calendar weeks, so missed days push the programme back rather than skipping content. Reviews keep calendar intervals, because forgetting follows the calendar. After an absence of more than a week, offer a catch-up session made only of reviews.

Propose an extra light day — propose, never impose — when any of these appears over the last three days:

- two consecutive failures on work that matched the learner's level;
- time spent repeatedly and substantially over the announced bound;
- a failed review on a subject already demonstrated `independent`.

Say which signal appeared, in one sentence, and let the learner decide.

## Morning shape

Four mornings of isolated work and two mornings on the red-thread project, as described in [curriculum.md](curriculum.md#shape-of-a-week).

An isolated morning contains:

- up to ten minutes of due recall;
- one web activity centred on TypeScript, JavaScript, React, Next.js, or NestJS;
- one DSA activity;
- a short evidence and checkpoint close.

A project morning contains one milestone on the red-thread application, the due recall, and the same close.

Breaks are human needs, not curriculum state. Techne does not schedule rest days or semesters.

## Spaced retrieval

A first success schedules:

- J+2: short reconstruction from memory;
- J+7: analogous application without the prior solution;
- J+21: recognition and transfer inside a broader problem.

Open no more than three due reviews per block and keep the set within ten minutes. Rereading is not recall. On failure, give a short correction; the script steps the subject down and schedules a smaller J+2 attempt.

The queue is prioritized for you: fragile subjects first, then the most overdue. Reviews overdue by more than twice their interval are dropped and their subject steps down, so the queue never grows without end. In the last two weeks, cumulative recall replaces reviews that would fall after the programme.

Reaching `independent` also schedules a transfer deadline one week later. Project mornings pick milestones that exercise the subjects waiting there; that reinvestment is what earns `transferred`.

## Mastery map

Every subject in the catalogues of [curriculum.md](curriculum.md#subject-catalogue) and [ai-curriculum.md](ai-curriculum.md#subject-catalogue) carries exactly one state in `STATE.json` `mastery`, keyed by its identifier:

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

Teach in the language recorded in `STATE.json` `language` while retaining standard English technical terms. Write natural, idiomatic prose, as a native speaker would; translate meaning rather than the English wording of this skill. Explain unfamiliar vocabulary in ordinary language before an exercise starts.
