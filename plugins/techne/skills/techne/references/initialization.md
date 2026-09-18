# Initialization

Use this branch when workspace resolution fails: the learner is starting Techne, whatever command they used. If a workspace already resolves, do not initialize; offer to resume or `reset` instead.

This is always a fresh start. Never read or reuse `.techne-archive-*` folders left by a `reset`, and never refer to a previous start.

Keep the start short: two questions — the language, then the folder — and under five minutes before the first placement exercise. Check the environment silently while asking. The learner should never see a shell command, a file path they must act on, or internal vocabulary.

Everything else waits until it is useful: the learner profile fills itself from observed work, the red-thread project domain is chosen in week 1, and the AI lab is set up on the first afternoon.

## Choose the learning language

Before creating anything, ask the learner which language the curriculum should be taught in. Always ask, even when the learner's message suggests a language; do not assume a default. Ask in the language the learner is writing in.

Record the answer as a BCP 47 tag (`en`, `fr`, `es`, `pt-BR`…). Technical terms stay in English whatever the choice.

## Choose the learning folder

Propose a dedicated folder, `~/techne` by default, in one sentence ("Your work and progress will live in `~/techne`. OK?"). Use the current directory only if the learner asks for it. Never use a broad directory such as the home directory or a folder that holds other projects.

## Create the workspace

Run `python3 scripts/init_workspace.py <folder> --language <tag>`; it creates the folder when missing. It refuses to create a second curriculum while one is registered as active, or to create a workspace that would hide an existing one. On such a refusal, do not work around it: offer to resume the existing curriculum or to `reset` it. Pass `--replace-active` only when the learner explicitly wants a separate, parallel curriculum. Refuse to merge with an existing `.techne/` directory; inspect and recover it instead. The initializer registers this directory as the global active workspace in `~/.techne/config.json` so future agent sessions can resume from any directory.

Initialization records the learning language in `STATE.json` and the lesson template, and creates the durable state, browser runtime, event log directory, and an empty Applied AI lab record. The Applied AI track is set up on its first afternoon (see [ai-curriculum.md](ai-curriculum.md#start-of-the-track)).

The workspace registration stores only an absolute path. The learning evidence remains inside the workspace. A workspace found in the current directory or one of its parents takes precedence over the global registration.

If a valid existing workspace needs to become active again, run `python3 scripts/resolve_workspace.py --set /absolute/workspace/path`. Do not initialize a parallel curriculum.

## Establish facts, not self-assessment

Techne ships a fixed twelve-week program and measures the learner's level by observation. After the language and folder, ask nothing else: no subjects, order, session duration, availability, deadline, experience, stack, or weaknesses.

State the rhythm instead, in one sentence: twelve weeks, about three hours on the Senior Engineer curriculum in the morning and three hours on Applied AI in the afternoon, at the learner's pace within each block.

Check the environment yourself: Node.js, a package manager, Git, VS Code, a browser, and Python for the lesson server. When something is missing, say what and why, and install it only after the learner agrees.

Record the verified environment in `.techne/PROFILE.md`.

## Placement test

The baseline is presented to the learner as a **placement test** (translated naturally, for example "test de positionnement" in French). Before the first exercise, say plainly:

- this is not the curriculum yet: it measures where the learner stands so the curriculum starts at the right level;
- it is not graded and mistakes are useful;
- that each area starts with an easy exercise and gets harder only while the learner succeeds, so it stays short (about an hour in total, each exercise at most fifteen minutes);
- the curriculum, with a short lesson before each exercise, starts right after.

Label every placement exercise with its area and position ("Placement test — algorithms, exercise 2"). Do not teach before a placement exercise; it measures prior knowledge. After the last one, give a two- or three-line summary and announce the first curriculum lesson.

Run short, production-oriented probes across the morning domains. The Applied AI track has its own short placement test on its first afternoon. Prefer debugging, explanation, small implementation, and trade-off questions over trivia.

For each area, climb a difficulty ladder:

1. start with an easy probe;
2. after an unassisted success, give a harder probe in the same area;
3. stop the area at the first real difficulty, or after the hardest probe the curriculum needs at this stage; the last success sets the starting level.

A failed probe is information, not a grade: say so briefly, give no correction yet, and move on.

At minimum observe:

- DSA iteration, data representation, tests, and basic complexity;
- TypeScript runtime boundaries and narrowing;
- React state, rendering, effects, and component boundaries;
- Next.js server/client mental model;
- Node.js backend with NestJS: modules, controllers, providers, and validation;
- JavaScript runtime and async reasoning;
- HTTP, SQL, architecture, and Product fundamentals.

Never guess a state: a subject nobody probed stays `not_started`. Record every probe result with `python3 scripts/state.py mastery <subject> <state> --evidence "…" --help-level H0`, never by editing `STATE.json`; store narrative decisions in `SESSION_LOG.md`. Pick the red-thread project domain with the learner during week 1, not during initialization.

## Finish initialization

Initialization is complete when:

- the environment needed for the first morning activity works;
- the subjects probed carry a mastery state from the catalogue, and every other subject stays `not_started`;
- `CURRENT.md` contains exactly one ready morning action;
- the Applied AI track is marked `not_started`;
- due-review scheduling can begin after the first successful evidence.

Do not ask the learner to define an overarching learning objective. Techne's shipped objective is the Senior Engineer curriculum in `curriculum.md` and the Applied AI curriculum in `ai-curriculum.md`.
