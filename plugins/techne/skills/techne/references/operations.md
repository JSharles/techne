# Daily operations and state

## Source of truth

Use `.techne/STATE.json` for machine-readable state and `.techne/CURRENT.md` for the one user-facing action. Keep these files consistent after every transition.

The durable records are:

- `PROFILE.md`: declared context and verified constraints;
- `STATE.json`: block state, mastery evidence, help levels, and project phase;
- `CURRENT.md`: one ready or in-progress activity;
- `REVIEW_QUEUE.md`: spaced-retrieval obligations;
- `SESSION_LOG.md`: append-only narrative evidence;
- `DECISIONS.md`: approved calibration decisions;
- `PROJECT.md`: current discovery or product facts;
- `events/browser.jsonl`: browser interactions recorded locally.

## Select the logical block

Use this order:

1. Resume an explicitly in-progress activity unless the learner requests a checkpoint or switch.
2. On a new local date with no in-progress activity, open the morning curriculum.
3. After Techne closes the morning block, the next ordinary resume opens the afternoon project.
4. A checkpointed afternoon milestone resumes on the next afternoon block until completed.
5. A natural-language request to switch to the project or curriculum overrides the ordinary transition after a checkpoint is saved.

Never switch because the clock crosses noon. Never let unfinished afternoon work consume the next morning block automatically.

## Resume

Before resuming:

- ingest new browser events;
- inspect files and test results relevant to `CURRENT.md`;
- open at most three due reviews, bounded to ten minutes total;
- give exactly one next observable action.

Name the active block at the top of the learning response:

```text
TECHNE — CURSUS
```

or:

```text
TECHNE — PROJET
```

Do not expose internal file maintenance unless it blocks learning.

## Browser evidence

The local browser runtime writes every opening, recall response, quiz choice, trace attempt, and code attempt to `.techne/events/browser.jsonl`. Read new events before declaring success, diagnosing a block, or changing a score.

Browser events are evidence, not grades by themselves. Consider the task, correctness, attempt count, elapsed time, code, and help already given. Record the last consumed event timestamp or line number in `STATE.json`.

## Help levels

- H0: no help;
- H1: one Socratic diagnostic question;
- H2: conceptual hint;
- H3: problem category or relevant model;
- H4: problematic region or missing invariant;
- H5: pseudocode or substantial guidance;
- H6: complete solution.

After an error, report one observed fact and ask one H1 question. Wait. Increase one level at a time on request or after an explicit unproductive block. Work completed after H4-H6 is valuable practice but not evidence of independence.

## Checkpoint and close

On pause, block switch, or session end:

- record what was attempted and observed;
- store the highest help level used;
- preserve the exact next action;
- update due reviews;
- update block status;
- distinguish advancement from mastery.

At closure report curriculum advancement and demonstrated mastery separately. Never turn completed time or pages into a mastery percentage.

## Status

For a status request, report:

- current logical block and activity;
- completed curriculum units;
- demonstrated scores with confidence and strongest evidence;
- due reviews and fragile areas;
- afternoon discovery or project milestone and its independent status.

Do not merge the two tracks into one progress percentage.
