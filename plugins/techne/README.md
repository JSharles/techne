# Techne Claude Code plugin

This plugin packages the canonical Techne Agent Skill for Claude Code. It contains one skill, `techne`, and no hooks, subagents, or external service integrations.

Install and usage instructions live in the [repository README](https://github.com/JSharles/techne#readme). Claude Code invokes the installed skill as `/techne:techne`; natural-language invocation remains available through the skill description.

Learner state is stored outside the plugin in the initialized learning workspace. Updating or uninstalling the plugin does not delete curriculum progress.
