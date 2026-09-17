# Daily operations and state

## Source of truth

Use `.techne/STATE.json` for machine-readable state and `.techne/CURRENT.md` for the one user-facing action. Keep these files consistent after every transition.

The durable records are:

- `PROFILE.md`: declared context and verified constraints;
- `STATE.json`: block state, mastery evidence, help levels, and Applied AI track progress;
- `CURRENT.md`: one ready or in-progress activity;
- `REVIEW_QUEUE.md`: spaced-retrieval obligations;
- `SESSION_LOG.md`: append-only narrative evidence;
- `DECISIONS.md`: approved calibration decisions;
- `AI_LAB.md`: Applied AI lab repository, model provider, and capstone facts;
- `events/browser.jsonl`: browser interactions recorded locally.

## Select the logical block

Use this order:

1. Resume an explicitly in-progress activity unless the learner requests a checkpoint or switch.
2. On a new local date with no in-progress activity, open the morning Senior Engineer block.
3. After Techne closes the morning block, the next ordinary resume opens the afternoon Applied AI block.
4. A checkpointed afternoon activity or capstone milestone resumes on the next afternoon block.
5. An `engineering` or `ai` command (or the equivalent natural-language request) overrides the ordinary transition after a checkpoint is saved.

Never switch because the clock crosses noon. Never let unfinished afternoon work consume the next morning block automatically.

## Resume

Before resuming:

- ingest new browser events;
- inspect files and test results relevant to `CURRENT.md`;
- open at most three due reviews, bounded to ten minutes total;
- give exactly one next observable action.

Name the active block at the top of the learning response, translated into the learning language:

```text
TECHNE — ENGINEERING
```

or:

```text
TECHNE — APPLIED AI
```

For example, a French learner sees `TECHNE — INGÉNIERIE` and `TECHNE — IA APPLIQUÉE`.

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

A `hint` command raises the help level by exactly one step from the current level; it never jumps to a solution.

After an error, report one observed fact and ask one H1 question. Wait. Increase one level at a time on request or after an explicit unproductive block. Work completed after H4-H6 is valuable practice but not evidence of independence.

## Checkpoint and close

On `pause`, a block switch (`engineering`, `ai`), or `end`:

- record what was attempted and observed;
- store the highest help level used;
- preserve the exact next action;
- update due reviews;
- update block status;
- distinguish advancement from mastery.

Tell the learner in plain words that their work is saved; do not name the files. `pause` keeps the day open so the next `resume` continues the same block. `end` closes the session. At closure report advancement and demonstrated mastery separately, for each curriculum. Never turn completed time or pages into a mastery percentage.

## Status

For a `status` command, report:

- current logical block and activity;
- completed units in each curriculum;
- demonstrated scores with confidence and strongest evidence;
- due reviews and fragile areas;
- the Applied AI week, lab progress, and capstone milestone when started.

Do not merge the two curricula into one progress percentage.

## Reset

`reset` lets the learner start Techne over, for example to retry installation and initialization from the beginning.

1. Say in one or two sentences what will happen: saved progress is put aside (archived in the workspace, not deleted) and the next start begins from zero with the language question; Techne will not reuse anything from it. Exercise files the learner wrote stay where they are.
2. Ask for an explicit yes. Offer permanent deletion only if the learner asks for it.
3. Run `python3 <this-skill-directory>/scripts/reset_workspace.py <workspace> --confirm` (add `--delete` only when the learner asked for deletion).
4. Ask whether to also remove exercise folders Techne created in the workspace; remove them only on an explicit yes.
5. Offer to start again now; if the learner agrees, follow [initialization.md](initialization.md).

## Uninstall

`uninstall` removes the Techne skill from the host agent. It never deletes learner progress unless the learner also asks for `reset`.

1. Ask whether the learner also wants to reset their progress first; if so, run the reset procedure above.
2. Ask for an explicit yes, then run the command for the host, or give it to the learner when the host cannot run it:
   - Claude Code plugin: `claude plugin uninstall techne@jsharles`, then `claude plugin marketplace remove jsharles` if the learner wants a completely clean slate;
   - `skills` installation (Codex and others): `npx skills@latest remove techne --global --yes`.
3. Give the reinstallation commands from the repository README (https://github.com/JSharles/techne#installation-30-second-setup) and say a new session is needed after reinstalling.
