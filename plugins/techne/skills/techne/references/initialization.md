# Initialization

Use this branch only when workspace resolution fails and the learner explicitly initializes Techne.

## Create the workspace

Run `python3 scripts/init_workspace.py` with the intended learning workspace. Refuse to merge with an existing `.techne/` directory; inspect and recover it instead. The initializer registers this directory as the global active workspace in `~/.techne/config.json` so future agent sessions can resume from any directory.

Initialization creates the durable state, browser runtime, event log directory, and empty project-discovery record. It does not choose an afternoon product.

The workspace registration stores only an absolute path. The learning evidence remains inside the workspace. A workspace found in the current directory or one of its parents takes precedence over the global registration.

If a valid existing workspace needs to become active again, run `python3 scripts/resolve_workspace.py --set /absolute/workspace/path`. Do not initialize a parallel curriculum.

## Establish facts, not preferences about the syllabus

Techne ships a curriculum. Do not ask the learner to choose subjects, their order, a session duration, or when architecture begins.

Collect only facts that change the first probes:

- professional experience and strongest daily stack;
- recent examples of work completed without assistance;
- known gaps or anxiety triggers;
- language and accessibility needs;
- available local tools and ability to run a browser and VS Code;
- realistic daily availability and any hard deadline.

Update `.techne/PROFILE.md`. Treat every declaration as unverified context.

## Baseline

Run short, production-oriented probes across the morning domains. A probe is not a surprise exam on an untaught advanced concept. Prefer debugging, explanation, small implementation, and trade-off questions over trivia.

At minimum observe:

- DSA iteration, data representation, tests, and basic complexity;
- TypeScript runtime boundaries and narrowing;
- React state, rendering, effects, and component boundaries;
- Next.js server/client mental model when the learner has used it;
- JavaScript runtime and async reasoning;
- HTTP, SQL, architecture, and Product fundamentals.

Use `unassessed` rather than guessing. Store evidence and the help level in `STATE.json`; store narrative decisions in `SESSION_LOG.md`.

## Finish initialization

Initialization is complete when:

- the environment needed for the first morning activity works;
- the first diagnostic evidence is recorded without inflating it into mastery;
- `CURRENT.md` contains exactly one ready morning action;
- the afternoon track is marked `discovery_pending`;
- due-review scheduling can begin after the first successful evidence.

Do not ask the learner to define an overarching learning objective. Techne's shipped objective is the curriculum described in `curriculum.md`, with an independent Applied AI product studio described in `project-studio.md`.
