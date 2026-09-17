# Initialization

Use this branch when workspace resolution fails: the learner is starting Techne, whatever command they used. If a workspace already resolves, do not initialize; offer to resume or `reset` instead.

Keep the whole start conversational and short. The learner should never see a shell command, a file path they must act on, or internal vocabulary.

## Choose the learning language

Before creating anything, ask the learner which language the curriculum should be taught in. Always ask, even when the learner's message suggests a language; do not assume a default. Ask in the language the learner is writing in.

Record the answer as a BCP 47 tag (`en`, `fr`, `es`, `pt-BR`…). Technical terms stay in English whatever the choice.

## Choose the learning folder

Propose a dedicated folder, `~/techne` by default, in one sentence ("Your work and progress will live in `~/techne`. OK?"). Use the current directory only if the learner asks for it. Never use a broad directory such as the home directory or a folder that holds other projects.

## Create the workspace

Run `python3 scripts/init_workspace.py <folder> --language <tag>`; it creates the folder when missing. It refuses to create a second curriculum while one is registered as active, or to create a workspace that would hide an existing one. On such a refusal, do not work around it: offer to resume the existing curriculum or to `reset` it. Pass `--replace-active` only when the learner explicitly wants a separate, parallel curriculum. Refuse to merge with an existing `.techne/` directory; inspect and recover it instead. The initializer registers this directory as the global active workspace in `~/.techne/config.json` so future agent sessions can resume from any directory.

Initialization records the learning language in `STATE.json` and the lesson template, and creates the durable state, browser runtime, event log directory, and empty project-discovery record. It does not choose an afternoon product.

The workspace registration stores only an absolute path. The learning evidence remains inside the workspace. A workspace found in the current directory or one of its parents takes precedence over the global registration.

If a valid existing workspace needs to become active again, run `python3 scripts/resolve_workspace.py --set /absolute/workspace/path`. Do not initialize a parallel curriculum.

## Establish facts, not preferences about the syllabus

Techne ships a curriculum. Do not ask the learner to choose subjects, their order, a session duration, or when architecture begins.

Collect only facts that change the first probes:

- professional experience and strongest daily stack;
- recent examples of work completed without assistance;
- known gaps or anxiety triggers;
- accessibility needs;
- available local tools and ability to run a browser and VS Code;
- realistic daily availability and any hard deadline.

Update `.techne/PROFILE.md`. Treat every declaration as unverified context.

## Placement test

The baseline is presented to the learner as a **placement test** (translated naturally, for example "test de positionnement" in French). Before the first exercise, say plainly:

- this is not the curriculum yet: it measures where the learner stands so the curriculum starts at the right level;
- it is not graded and mistakes are useful;
- how many short exercises it contains (typically four to six) and that each takes at most about fifteen minutes;
- the curriculum, with a short lesson before each exercise, starts right after.

Label every placement exercise with its position ("Placement test — exercise 2 of 5"). Do not teach before a placement exercise; it measures prior knowledge. After the last one, give a two- or three-line summary and announce the first curriculum lesson.

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
