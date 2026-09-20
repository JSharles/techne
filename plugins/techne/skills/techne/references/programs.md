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
| `survey_ceiling` | a mastery state | how far a survey subject may go |

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

Subjects are global: `dsa.bfs` is the same subject wherever it is taught, and carries one mastery entry. Reuse an existing identifier when you mean the same thing — that is how a new program credits what the learner already proved. Two programs that give the same prefix different meanings are refused at enrolment.

## The wizard

`new` creates a program by interview, in the conversation. This is one of the operational exchanges ADR 0008 allows: nothing here has a right answer the host could leak.

Run it as rounds of numbered questions, each with your recommended answer, and wait for the learner between rounds — the same shape as the design sessions that built Techne. Show pedagogical judgement: name what is missing, what is out of order, what is too large for one unit.

**Mode one — the learner brings the subjects.** They already know what they want to study.

1. Collect their list as given, without adding to it.
2. Group it into units and propose the grouping.
3. Mint the identifiers, one domain prefix for the program's own material, reusing existing identifiers wherever a subject is genuinely the same.
4. Name the prerequisites their list implies but does not contain, and ask whether to add them or treat them as already known. Never add one silently.
5. Propose an order, from what depends on what.
6. Propose the five settings from how they described working.

**Mode two — the learner brings an objective.** "Hold a meeting in Spanish", "understand our Kubernetes setup".

1. Establish the outcome, the starting point, and the boundary in a few questions.
2. Design units, catalogue and settings yourself, and submit the whole program for approval.
3. Say what you deliberately left out, and why.

Either way, write the file to `.techne/programs/<id>.md`, run `state.py programs` to confirm it is usable, and fix what is reported before offering to enrol. The file is the learner's from then on: say that they can edit it by hand whenever they want.

## Changing a program

Editing a program the learner follows is ordinary work: change the file. Their evidence is addressed by subject identifier, so it survives. A subject dropped from the catalogue keeps its mastery entry and is reported as no longer taught rather than deleted.
