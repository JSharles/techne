# Techne

Techne is an intensive, adaptive bootcamp delivered as one Agent Skill for Codex, Claude Code, and compatible coding agents. It is designed for developers with a TypeScript/frontend background who want to reach a senior level and build LLM applications.

Techne teaches **programs**: Markdown files describing what to learn. One ships with it, and you write or generate the others — a program never changes the method, only the content.

- **Applied AI:** Python, FastAPI, LLM applications, RAG with LangChain, agents with LangGraph, evaluation with LangSmith — built around one real application you choose, with Techne as your product owner and lead developer.

Everything else you write yourself with `new`, or bring from elsewhere: a frontend course, a DSA course, a design course. Techne teaches whatever its programs describe.

You follow as many programs as you like, and organise your time as you wish: enrol in a program and start it at once, open any of them whenever you want, for as long as you want.

You write every line of every exercise: Techne scaffolds and reviews, but never writes your implementation, and never teaches you to delegate it to an AI.

Techne stores progress outside the installed skill — a small database beside your Markdown files — records answers from browser exercises, scaffolds real coding environments, and adapts from observed evidence rather than self-assessment alone.

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

Then set Techne up with `/techne:init` (type `/techne:` to see every command). Natural language also works; Techne maps it to the matching command (see [Commands](#commands)).

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

Installation makes the teaching method available; `init` creates your personal curriculum state. Start Techne from any folder:

```text
/techne:init     # Claude Code
$techne init     # Codex
```

Techne then:

- asks which language you want to learn in (English, French, or any other language); commands and technical terms stay in English;
- proposes a dedicated folder for your work and progress (`~/techne` by default), creates `.techne/` there, and remembers it so you can resume from anywhere;
- checks your tools (and asks before installing anything missing);
- asks which program you want to start with, and enrols you in it;
- runs a short **placement test**, about an hour: each area starts with an easy exercise and gets harder only while you succeed, so teaching starts at the right level;
- starts teaching, where each exercise is preceded by a short lesson in your browser.

The whole start takes two questions and under five minutes before the first exercise.

### Where to run it

Anywhere Claude Code runs, but a terminal inside your editor (VS Code, or iTerm next to it) is the smoothest: the code, the tests, and Techne share one window, and Techne resolves your workspace from the current folder. Run one Techne session at a time; concurrent sessions are detected and warned about, not merged.

There is no timetable: you work when you want and for as long as you want, and Techne picks up wherever you left off, starting each session with your due reviews. A program ends when its subjects are covered, never after a fixed number of weeks. Your progress is tracked subject by subject — not started, discovered, with help, independent, transferred, blocked — and shown on the "My progress" page in your browser.

Techne does not flatter: it names what you demonstrated and what you did not, and gives a blunt assessment after every six sessions of a program.

Techne refuses to start a second curriculum while one is in progress; use `reset` to start over.

Do not commit `.techne/`: it contains personal progress, evidence, and local exercise events.

## Daily use

Each command is typed after the Techne entry point:

```text
/techne:<command>          # Claude Code, e.g. /techne:hint
$techne <command>          # Codex, e.g. $techne hint
```

In Claude Code, type `/techne:` and pick a command from the menu. Commands are the same whatever language you learn in.

Techne decides what comes next: the subject, due reviews, difficulty, and activity format. You never pick when to study architecture, DSA, React, Product, or any other curriculum domain.

### Commands

| Command | What it does | When to use it |
| --- | --- | --- |
| `init` | Sets Techne up on this machine: your learning folder and its Git repository, your learning language, and a check of your tools. | Once, the first time you use Techne. |
| `resume` | Picks up the program this conversation has open and gives you exactly one next action. Typing the entry point alone does the same. | To start working, or to come back after a break. |
| `start <id>` | Opens a program in this conversation, enrolling you if you did not follow it yet. | To begin a program, or to work on another one in a second window. |
| `ask <question>` | Answers any question: where you are, why this subject, what a word means, how a tool works. Costs you nothing and leaves no trace. | Whenever you wonder anything. It declines only the answer to the exercise you have open. |
| `status` | Where the open program stands: its progress, what is open, what is due. | When you want to know where you are. |
| `programs` | Lists the programs you can follow, the ones you are enrolled in, and your coverage in each. | To see what you are carrying. |
| `assessment` | A blunt assessment of what moved, what stalled and what is fragile in the open program, with your skills radar. | Every week or two. |
| `assessment-all` | The same radar across every program you follow: the state of your skills as a whole. | When you want the whole picture. |
| `new` | Creates a program with you, by interview: you bring the subjects and Techne structures them, or you give an objective and Techne designs the course. | When you want to learn something Techne does not ship. |
| `issue <text>` | Notes anything about Techne itself, with the activity it came from. | The moment the tool misbehaves. |
| `issues-export` | Prints everything you noted, grouped and dated, then offers to empty the journal. | When you sit down to improve Techne. |
| `reset` | After you confirm, puts your progress aside (archived, not deleted unless you ask) so Techne starts again from `init`. | To start over. Updating Techne never needs it. |
| `uninstall` | After you confirm, removes Techne from your agent, optionally after a `reset`, and tells you how to reinstall. | When you no longer want Techne. |

Everything else you simply ask for, in plain words: a step of help on the exercise you have open, opening your project, setting a program aside, or changing how Techne teaches you.

## Several programs at once

Each Claude Code window works on one program. Open a second window, run `start` or `resume` there, and the two advance in parallel: each keeps its own program, its own activity and its own due reviews. Only one of them writes at a time, so nothing is lost. Techne warns you only if two windows open the same program, where both would record evidence for the same subjects.

### Natural language

You can also just talk to the agent, in any language: "on reprend", "I'm stuck", "où en suis-je ?". The agent maps a clear request to the matching command and runs it. If your intent is ambiguous, it asks which command you mean. Inside an active Techne workspace, you can often skip the invocation entirely.

## Learning something else

A new subject is a **program**, not a second Techne: `new` writes one with you, and `start` opens it beside the ones you already follow. Everything stays in one workspace, and each program keeps its own evidence: what you proved in one never counts in another.

One workspace holds your whole learning life, and `reset` is only for starting that life over. To try Techne out without touching it — a new version, a program you are unsure about — give the session its own registry:

```bash
mkdir -p /tmp/techne-trial && cd /tmp/techne-trial
TECHNE_HOME=/tmp/techne-trial/registry claude
```

## Resume from another directory or a new conversation

The conversation transcript is not the source of truth. Techne reconstructs the learning session from persisted files.

It resolves the workspace in this order:

1. a Techne workspace in the current directory or one of its parents;
2. the active workspace recorded in `~/.techne/config.json`.

This allows a new agent conversation to locate the current curriculum from another directory. The host agent may still request filesystem permission before writing outside its current project sandbox.

Updating or uninstalling Techne does not remove learner progress. Progress remains in the learning workspace until the learner explicitly deletes it.

## Start over from scratch

To retest the whole journey (installation, initialization, placement test):

1. In a Techne session, run `reset`, then `uninstall` (or run the commands below yourself).
2. Start a new session and follow [Installation](#installation-30-second-setup) again.

Manual equivalent for Claude Code:

```bash
claude plugin uninstall techne@jsharles
claude plugin marketplace remove jsharles
mv <learning-folder>/.techne <learning-folder>/.techne-archive   # or delete it
rm -f ~/.techne/config.json
```

Then reinstall with the two commands from [Claude Code](#claude-code) and run `/techne:init` in a new session.

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

Restart your agent after an update. When you come back, Techne tells you in a sentence or two what changed for you, once. If a new version changes how progress is stored, Techne says so and offers to migrate your workspace; your evidence is preserved, and you never need a `reset` to update.

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

Techne's source, agent instructions, repository documentation, schemas, code comments, and commands are written in English.

The learning experience is delivered in the language you choose during `init`: lessons, exercise prompts, feedback, progress reports, and browser UI. Ask Techne to switch language at any time. Established technical terms remain in English when that is clearer.

The browser UI ships with English and French strings (`assets/browser/assets/i18n.js`); other languages fall back to English in the browser while the lessons themselves are written in your language.

## Repository structure

The repository contains one canonical skill and two distribution adapters:

```text
.claude-plugin/marketplace.json              Claude Code marketplace
plugins/techne/.claude-plugin/plugin.json    Claude Code plugin manifest
plugins/techne/commands/                     Claude Code slash commands (thin wrappers)
plugins/techne/skills/techne/                Canonical Agent Skill
plugins/techne/skills/techne/programs/       Programs Techne ships
plugins/techne/skills/techne/CHANGELOG.md    What each version changed, read by Techne
tests/                                       Workspace, state and catalogue tests
CONTEXT.md                                   Project glossary
docs/adr/                                    Decisions behind the programme's shape
```

Claude Code and `npx skills` install the same `plugins/techne/skills/techne` source. There are no agent-specific copies of the curriculum; the Claude Code slash commands only forward to the skill.

## Development and validation

Run the test suite, workspace-template validator, skill validator, and Claude plugin validator before release:

```bash
python3 -m unittest discover -s tests
python3 plugins/techne/skills/techne/scripts/validate_workspace.py --template
uvx --from skills-ref agentskills validate plugins/techne/skills/techne
claude plugin validate .
```

Before releasing a change to learner-facing wording, run the style eval suite. It runs Techne on three reference situations in French and fails when a reported turn of phrase comes back; it makes real model calls:

```bash
claude plugin eval plugins/techne --tag style-fr --scaffold --allow-tools Bash Write Edit --trust-plugin
```

While iterating, add `--runs 1 --ablation none`: one run per case and no baseline arm, about a sixth of the cost of a full pass.

For local Claude Code testing, add this checkout as a marketplace:

```bash
claude plugin marketplace add .
claude plugin install techne@jsharles
```

For local `skills` discovery without publishing to GitHub:

```bash
npx skills@latest add . --skill techne --agent codex
```

Python, FastAPI, LangChain, LangGraph, and LangSmith are taught in the Applied AI program. They are not runtime dependencies of the Techne skill itself. The Applied AI track makes model API calls with the learner's own key (or a local model), so it can incur small provider costs.
