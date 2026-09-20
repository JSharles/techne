# Techne contributor guidance

Techne is one Agent Skill shared by Codex and Claude Code. Keep `plugins/techne/skills/techne/SKILL.md` and its `references/` as the single source of truth; do not create divergent agent-specific copies.

Write skill source, repository documentation, schemas, code comments, and maintenance-facing text in English. Learner-facing lessons, exercises, feedback, progress reports, and browser UI use the language the learner chose during `init`, recorded in `.techne/STATE.json`; never hard-code a learner language in skill source. Browser UI strings live in `assets/browser/assets/i18n.js` and `assets/browser/serve.py`, with English as the fallback. Techne commands stay in English. Preserve established English technical terms where they improve precision.

Techne commands are defined in the skill's `SKILL.md`. Each one also has a thin Claude Code slash command in `plugins/techne/commands/<name>.md` that only forwards to the skill; keep both in sync and never put behaviour in the command files.

`CONTEXT.md` is the project glossary and `docs/adr/` holds the decisions behind the curriculum's shape; read both before changing the method or the programme, and add an ADR when a new hard-to-reverse decision is made.

Before changing the skill, read `plugins/techne/skills/techne/SKILL.md` and every reference affected by the change. Preserve the separation between the morning Senior Engineer curriculum and the independent afternoon Applied AI curriculum.

`plugins/techne/skills/techne/scripts/state.py` is the only writer of `.techne/STATE.json`, `feedback.py` the only writer of `.techne/feedback.jsonl`, and `catalogue.py` the only reader of the subject catalogues; keep it that way, and add a test in `tests/test_state.py` for every new transition.

Every change that ships to learners (anything under `plugins/techne/`) must bump `version` in both `plugins/techne/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Claude Code caches installed plugins by version, so a change pushed without a bump never reaches existing installations.

After changes, run:

```bash
python3 -m unittest discover -s tests
python3 plugins/techne/skills/techne/scripts/validate_workspace.py --template
claude plugin validate .
```

Also run the available Agent Skill validator against `plugins/techne/skills/techne`. Treat `.techne/` as learner runtime state, not skill source.
