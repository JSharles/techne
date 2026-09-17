# Techne Claude Code plugin

This plugin packages the canonical Techne Agent Skill for Claude Code. It contains one skill, `techne`, a set of thin slash commands that call it, and no hooks, subagents, or external service integrations.

Install and usage instructions live in the [repository README](https://github.com/JSharles/techne#readme). Type `/techne:` in Claude Code to see the commands (`/techne:init`, `/techne:hint`, `/techne:feedback`…). Each file in `commands/` only forwards to the skill; the behaviour lives in `skills/techne/`. Natural language also works.

Learner state is stored outside the plugin in the initialized learning workspace. Updating or uninstalling the plugin does not delete curriculum progress.
