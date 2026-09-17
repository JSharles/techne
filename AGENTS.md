# Techne contributor guidance

Techne is one Agent Skill shared by Codex and Claude Code. Keep `plugins/techne/skills/techne/SKILL.md` and its `references/` as the single source of truth; do not create divergent agent-specific copies.

Write skill source, repository documentation, schemas, code comments, and maintenance-facing text in English. Learner-facing lessons, exercises, feedback, progress reports, and browser UI use the language the learner chose during `init`, recorded in `.techne/STATE.json`; never hard-code a learner language in skill source. Browser UI strings live in `assets/browser/assets/i18n.js` and `assets/browser/serve.py`, with English as the fallback. Techne commands stay in English. Preserve established English technical terms where they improve precision.

Before changing the skill, read `plugins/techne/skills/techne/SKILL.md` and every reference affected by the change. Preserve the separation between the morning Senior Engineer curriculum and the independent afternoon Applied AI product studio.

After changes, run:

```bash
python3 -m unittest discover -s tests
python3 plugins/techne/skills/techne/scripts/validate_workspace.py --template
claude plugin validate .
```

Also run the available Agent Skill validator against `plugins/techne/skills/techne`. Treat `.techne/` as learner runtime state, not skill source.
