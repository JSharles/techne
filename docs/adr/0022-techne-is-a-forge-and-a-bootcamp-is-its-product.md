# Techne is a forge: a bootcamp is a skill it produces

Techne writes a lesson, an exercise or a recall for one learner, serves it from their workspace, and forgets it. The wording the learner had corrected, the test that was missing, the question that had two defensible answers: all of it improves one session and nothing else. Meanwhile the programs themselves became the valuable part — ten courses, written and sharpened over weeks — and they teach nothing on their own, because the material that makes them teachable is regenerated from scratch for every learner.

So Techne becomes two things. It stays the course a learner follows. It also becomes the workshop where a bootcamp is built: the author follows their own programme, reviews each piece of material as it is produced, and what they accept is kept in the programme itself. Once the material is reviewed, `forge` turns a selection of programmes into a standalone skill that only teaches — another repository, another plugin, which anyone can install.

## What a programme holds

A programme keeps its course and its material side by side:

```text
programs/frontend-senior.md              the course: outcome, sequence, catalogue, adaptation rules
programs/frontend-senior/
  fejs.closures/
    intent.md                            what this material must cover: the goal, the pitfalls to hit,
                                         the success criteria, what must already be known
    lesson.html                          the page served to the learner
    recall.md                            recall prompts and their model answers, quiz items
    exercise/
      BRIEF.md                           the statement, in the programme's language
      files/                             the starting files, with their tests
      solution/                          the reference implementation, never copied into a learner folder
```

Every file carries `status: draft` or `status: reviewed` in its front matter, with `reviewed_at` and the Techne version that produced it. `scripts/content.py` is the only module that reads or writes this material, as `state.py` is for evidence and `programs.py` for the course.

A subject with no folder is normal: Techne generates the material, saves it as `draft`, and the author's "this is good" is what marks it `reviewed`. Nothing else changes for a learner who is not an author.

## Which material a learner gets

Both, as the author chose: the reviewed file is served as it stands, and `intent.md` sits beside it so the agent can rewrite or translate the page when a learner asks, without touching what is stored. A draft is served the same way and improved in place as the author reviews it.

## The forge

`forge` is the command that makes a bootcamp, and it is an interview:

1. **The name.** What the bootcamp is called, from which its plugin identifier is derived — "Product Engineer" gives `techne-product-engineer`.
2. **The repository.** Where it is written: a local path, and the remote it will be pushed to. Techne creates the directory, initialises the repository and sets the remote; pushing stays the author's act.
3. **The programmes.** Which of the programmes available here compose it, chosen from a list that states, for each, how much of its material is reviewed. A programme whose material is mostly draft is named as such before it is picked, never silently excluded.

The interview then shows what will ship — the programmes, the number of subjects with reviewed material, what is left behind — and writes nothing until the author agrees.

What `forge` writes is a draft. The bootcamp exists as a repository on the author's machine, with a `forge.json` recording its name, its programmes, the Techne commit it was built from, and the version last published, if any. Running `forge` again on the same bootcamp brings it up to date in place: material newly reviewed joins it, the repository's history is kept, and nothing is published.

Underneath it is a script the author can also run alone:

```bash
python3 scripts/export_bootcamp.py --name "<name>" --into <directory> <program-id>...
```

It writes a plugin that teaches those programmes and nothing else:

- their course files and the `reviewed` material, drafts left behind;
- the method: `pedagogy.md`, `exercises.md`, `operations.md`, the language style files, and `project.md` when the programme carries a project;
- the engine: `state.py`, `store.py`, `programs.py`, `content.py`, `issues.py`, the workspace scripts, and the browser runtime;
- five commands — `init`, `start`, `status`, `assessment`, `ask` — where `init` enrols in every programme the bootcamp ships and opens one, and `start` with no argument lists them, so the learner is in the course as soon as they arrive;
- a `plugin.json` naming the Techne version and commit it was built from, and a seeded `CHANGELOG.md`.

It does not write `new`, `forge`, `publish`, the creation interview or the content workshop: a bootcamp teaches, it does not forge.

The steps of both live in `references/forge.md`, beside the other method references, and `commands/forge.md` and `commands/publish.md` expose them as `/techne:forge` and `/techne:publish`.

## Publishing

`publish` releases a version of a bootcamp:

1. It shows what changed since the last published version: programmes added, subjects whose material was reviewed or rewritten, method files that moved.
2. It asks for the version, proposing the next one, and writes it into `plugin.json` and the bootcamp's own `CHANGELOG.md`, in the terms its learners read.
3. It commits, tags `v<version>`, and pushes to the remote the forge recorded.

Between two publications the bootcamp stays a draft the author keeps working on, in Techne, by following the course and reviewing its material. A learner who installs it gets the last published version, never the work in progress.

## Consequences

- The author's first run through a programme is also its review: following the course is what produces the product, with no separate authoring pass.
- A bootcamp carries the pedagogy of the day it was published, so it does not change under its learners; bringing it a method improvement means forging and publishing again, which the recorded version makes a deliberate act.
- Reviewed material is written in one language and pinned to the level the author had that day. The agent can translate or re-level it on request, from `intent.md`, but what ships is what the author read.
- A bootcamp ships no `issue` command, so its learners have no channel back to its author. Adding one is a decision for whoever forges it, not a default.
- A bootcamp made of several programmes keeps them isolated, as everywhere else: a learner proves a subject in each, and the bootcamp is covered when all of them are.
- Programmes grow heavy: material lives in the repository beside the course, and a full bootcamp is megabytes rather than kilobytes.
