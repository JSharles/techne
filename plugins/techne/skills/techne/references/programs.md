# Programs and the creation wizard

Read this before listing, creating, or changing a program.

## What a program is

A program is a Markdown file that says what is taught: a metadata header, a sequence of units, a subject catalogue, and adaptation notes. It never changes the method — the lesson-then-practice loop, the evidence rules, the help ladder, the review intervals all stay in the engine (`docs/adr/0010-a-program-is-data-not-skill-source.md`).

Techne ships programs beside the skill; the learner's own live in `.techne/programs/`, and win an identifier clash. `state.py programs` lists what is usable, with coverage, and why anything was rejected.

## The five settings

A header declares exactly these, and nothing else:

| Setting | Values | What it changes |
| --- | --- | --- |
| `activity_kinds` | `code`, `browser`, `oral`, `writing` | what an activity may be |
| `lesson_to_practice` | `lesson-heavy`, `balanced`, `practice-heavy` | how much teaching precedes practice |
| `timeboxes` | `lesson=`, `exercise=`, `review=`, `project=`, `placement=`, in minutes | the bounds announced before work |
| `red_thread` | `yes`, `no` | whether the program carries a running project |
| `survey_ceiling` | a mastery state | how far a survey subject — any under the `survey.*` prefix — may go |

A sixth setting is refused, so a program cannot quietly invent its own rules.

## The file

```text
---
id: frontend-interviews
title: Frontend interviews
version: 1
cadence: three-times-weekly
activity_kinds: code, oral
lesson_to_practice: practice-heavy
timeboxes: lesson=10, exercise=20, review=5, placement=15
red_thread: no
survey_ceiling: discovered
---

# Frontend interviews

## Outcome and boundary

Who it is for, what it takes them to, and what it deliberately leaves out.

## Sequence

### Unit 1 — <name>

- what is taught here.

## Subject catalogue

### <Domain title> — `<prefix>.*`

`first-subject`, `second-subject`

## Adaptation rules

How difficulty moves, and what compresses when a subject is already demonstrated.
```

## A program is complete on its own

Write every program as if a stranger were about to follow it, one who has never taken any other program. Its catalogue lists everything it teaches, including subjects another program already covers, and its sequence stands without reading anywhere else.

This is not negotiable, and it overrides any wish to avoid repetition:

- never drop a subject because the learner demonstrated it elsewhere;
- never fold a new program into an existing one, or present it as an extension of it;
- never let another program's content decide what this one contains.

Subjects are still global: `dsa.bfs` is the same subject wherever it is taught, and carries one mastery entry. Reuse an identifier when it is genuinely the same skill demonstrated the same way — the learner then starts this program with real coverage instead of zero. When a program trains the same theme in a different mode — under time, out loud, at interview pace — that is not the same subject: mint an identifier under this program's own prefix.

Shared evidence is a consequence, never a reason to cut content. Two programs that give the same prefix different meanings are refused at enrolment.

## The wizard

`new` creates a program by interview, in the conversation. This is one of the operational exchanges ADR 0008 allows: nothing here has a right answer the host could leak.

Run it as rounds of numbered questions, each with your recommended answer, and wait for the learner between rounds — the same shape as the design sessions that built Techne. Show pedagogical judgement: name what is missing, what is out of order, what is too large for one unit.

**Mode one — the learner brings the subjects.** They already know what they want to study.

1. Collect their list as given, without adding to it and without removing anything that exists elsewhere.
2. Group it into units and propose the grouping.
3. Mint the identifiers: this program's own prefix for what it trains its own way, an existing identifier only where the skill and the way it is demonstrated are genuinely the same.
4. Name the prerequisites their list implies but does not contain, and ask whether to add them to this program or leave them out. Never add one silently, and never leave one out merely because another program teaches it — a stranger following this program would then hit a hole.
5. Propose an order, from what depends on what, inside this program alone.
6. Propose the five settings from how they described working.

Creating a program is not scheduling it. Write and validate the file first; where it fits in the week is a separate conversation, after the learner has approved the program.

**Mode two — the learner brings an objective.** "Hold a meeting in Spanish", "understand our Kubernetes setup".

1. Establish the outcome, the starting point, and the boundary in a few questions.
2. Design units, catalogue and settings yourself, and submit the whole program for approval.
3. Say what you deliberately left out, and why.

Either way, write the file to `.techne/programs/<id>.md`, run `state.py programs` to confirm it is usable, and fix what is reported before offering to enrol. The file is the learner's from then on: say that they can edit it by hand whenever they want.

## Changing a program

Editing a program the learner follows is ordinary work: change the file. Their evidence is addressed by subject identifier, so it survives. A subject dropped from the catalogue keeps its mastery entry and is reported as no longer taught rather than deleted.
