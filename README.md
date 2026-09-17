# Techne

Techne is an intensive, adaptive engineering academy delivered as one Agent Skill for Codex, Claude Code, and compatible coding agents.

It runs two independent tracks over a maximum of twelve weeks:

- a morning curriculum for Senior Engineer foundations, led and sequenced by Techne;
- an afternoon Applied AI product studio, guided by product and technical milestones.

Techne stores progress outside the installed skill, records answers from browser exercises, scaffolds real coding environments, and adapts from observed evidence rather than self-assessment alone.

## Installation (30-second setup)

There are two distribution paths for two agent ecosystems. Claude Code receives Techne as a managed plugin. Codex and other compatible agents receive the same canonical skill through the open `skills` installer.

Install Techne only once per agent. If the Claude plugin is installed, do not also target Claude Code with `npx skills`; doing so creates duplicate skills.

### Claude Code

Until Techne is listed in Claude Code's official marketplace, add the repository marketplace once and install the plugin:

```bash
claude plugin marketplace add JSharles/techne
claude plugin install techne@jsharles
```

The same operations are available from inside Claude Code:

```text
/plugin marketplace add JSharles/techne
/plugin install techne@jsharles
```

When Techne becomes available in the official marketplace, installation can become a single command:

```bash
claude plugin install techne
```

Claude Code invokes plugin skills with a namespace:

```text
/techne:techne init
/techne:techne
```

Natural language such as `Techne init` or `On reprend` also works.

### Codex

Install Techne globally for Codex from GitHub:

```bash
npx skills@latest add JSharles/techne --skill techne --agent codex --global
```

Then invoke it with:

```text
$techne init
$techne
```

### Other compatible agents

Run the interactive installer and choose the target agents and installation scope:

```bash
npx skills@latest add JSharles/techne --skill techne
```

Do not select Claude Code when the Claude plugin is already installed.

## Start a curriculum

Installation makes the teaching method available. Initialization creates your personal curriculum state. These are separate operations.

1. Open the folder that should hold your learning work and progress.
2. Start Codex or Claude Code in that folder.
3. Invoke Techne with `init`:

```text
# Codex
$techne init

# Claude Code plugin
/techne:techne init
```

You can also say `Techne init` in natural language.

Techne then:

- creates `.techne/` in the learning workspace;
- registers that workspace in `~/.techne/config.json`;
- collects only facts needed to calibrate the first diagnostic activities;
- begins the baseline without asking you to design the syllabus.

Do not commit `.techne/`: it contains personal progress, evidence, and local exercise events.

## Daily use

Techne uses a deliberately small interface. Natural language is preferred over configuration commands.

| Intent | Codex | Claude Code | Natural language example |
| --- | --- | --- | --- |
| Resume | `$techne` | `/techne:techne` | `On reprend` |
| Request help | `$techne` | `/techne:techne` | `Indice` |
| Check progress | `$techne` | `/techne:techne` | `Où en suis-je ?` |
| Switch to the studio | `$techne` | `/techne:techne` | `On passe au projet` |
| Return to the curriculum | `$techne` | `/techne:techne` | `Je reprends le cursus` |
| Save a checkpoint | `$techne` | `/techne:techne` | `Pause` or `Fin de session` |
| Discuss the method | `$techne` | `/techne:techne` | Describe the problem in ordinary language |

Techne chooses the next subject, due reviews, difficulty, and activity format. The learner does not choose when to study architecture, DSA, React, Product, or another curriculum domain.

## Resume from another directory or a new conversation

The conversation transcript is not the source of truth. Techne reconstructs the learning session from persisted files.

It resolves the workspace in this order:

1. `.techne/STATE.json` in the current directory or one of its parents;
2. the active workspace recorded in `~/.techne/config.json`.

This allows a new agent conversation to locate the current curriculum from another directory. The host agent may still request filesystem permission before writing outside its current project sandbox.

Updating or uninstalling Techne does not remove learner progress. Progress remains in the learning workspace until the learner explicitly deletes it.

## Update

### Claude Code

Refresh the marketplace and update the plugin:

```bash
claude plugin marketplace update jsharles
claude plugin update techne@jsharles
```

### Codex and other `skills` installations

```bash
npx skills@latest update techne --global
```

## Uninstall

### Claude Code

```bash
claude plugin uninstall techne@jsharles
```

### Codex

```bash
npx skills@latest remove techne --agent codex --global --yes
```

Uninstallation removes the teaching package, not `.techne/` or `~/.techne/config.json`.

## Language policy

Techne's source, agent instructions, repository documentation, schemas, and code comments are written in English. The learning experience is delivered in French by default: lessons, exercise prompts, feedback, progress reports, and browser UI. Established technical terms remain in English when that is clearer.

## Repository structure

The repository contains one canonical skill and two distribution adapters:

```text
.claude-plugin/marketplace.json              Claude Code marketplace
plugins/techne/.claude-plugin/plugin.json    Claude Code plugin manifest
plugins/techne/skills/techne/                Canonical Agent Skill
```

Claude Code and `npx skills` install the same `plugins/techne/skills/techne` source. There are no agent-specific copies of the curriculum.

## Development and validation

Run the test suite, workspace-template validator, skill validator, and Claude plugin validator before release:

```bash
python3 -m unittest discover -s tests
python3 plugins/techne/skills/techne/scripts/validate_workspace.py --template
python3 /path/to/skill-creator/scripts/quick_validate.py plugins/techne/skills/techne
claude plugin validate .
```

For local Claude Code testing, add this checkout as a marketplace:

```bash
claude plugin marketplace add .
claude plugin install techne@jsharles
```

For local `skills` discovery without publishing to GitHub:

```bash
npx skills@latest add . --skill techne --agent codex
```

Python, FastAPI, LangChain, LangGraph, and LangSmith are curriculum technologies for the afternoon product studio. They are not runtime dependencies of the Techne skill itself.
