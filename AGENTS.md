# Techne contributor guidance

Techne is one Agent Skill shared by Codex and Claude Code. Keep `plugins/techne/skills/techne/SKILL.md` and its `references/` as the single source of truth; do not create divergent agent-specific copies.

Write skill source, repository documentation, schemas, code comments, and maintenance-facing text in English. Learner-facing lessons, exercises, feedback, progress reports, and browser UI use the language the learner chose during `init`, carried in the state store; never hard-code a learner language in skill source, except in a `references/style-<language>.md` file, which holds that language's examples and is read only when the learner chose it. Browser UI strings live in `assets/browser/assets/i18n.js` and `assets/browser/serve.py`, with English as the fallback. Techne commands stay in English. Preserve established English technical terms where they improve precision.

Techne commands are defined in the skill's `SKILL.md`. Each one also has a thin Claude Code slash command in `plugins/techne/commands/<name>.md` that only forwards to the skill; keep both in sync and never put behaviour in the command files.

`CONTEXT.md` is the project glossary and `docs/adr/` holds the decisions behind the curriculum's shape; read both before changing the method or the programme, and add an ADR when a new hard-to-reverse decision is made.

Before changing the skill, read `plugins/techne/skills/techne/SKILL.md` and every reference affected by the change. Programs under `plugins/techne/skills/techne/programs/` are content, not engine: keep the method in the skill and never let a program redefine it.

`store.py` is the only module that opens the state store, `state.py` the only one that applies transitions, `issues.py` the only writer of the issues journal, and `programs.py` the only reader of program files; keep it that way, and add a test in `tests/test_state.py` for every new transition.

Every change that ships to learners (anything under `plugins/techne/`) must bump `version` in both `plugins/techne/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, and add what it changes for the learner, in their terms, to `plugins/techne/skills/techne/CHANGELOG.md`. Techne reads that file to tell the learner what changed after an update, so it ships inside the skill rather than at the repository root. Claude Code caches installed plugins by version, so a change pushed without a bump never reaches existing installations.

After changes, run:

```bash
python3 -m unittest discover -s tests
python3 plugins/techne/skills/techne/scripts/validate_workspace.py --template
claude plugin validate .
```

Also run the available Agent Skill validator against `plugins/techne/skills/techne`. Treat `.techne/` as learner runtime state, not skill source.

Before releasing a change to learner-facing wording (message rules, `pedagogy.md`, a `style-<language>.md` file), run the style eval suite; it makes real model calls, so it is not part of the routine checks:

```bash
claude plugin eval plugins/techne --tag style-fr --scaffold --allow-tools Bash Write Edit --trust-plugin
```

While iterating, add `--runs 1 --ablation none`: one run per case and no baseline arm, about a sixth of the cost of a full pass.
