# Techne

Techne is an intensive, adaptive bootcamp delivered as one Agent Skill for Codex, Claude Code, and compatible coding agents. It is designed for developers with a TypeScript/frontend background who want to reach a senior level and build LLM applications.

It runs two independent curricula over twelve weeks, about three hours each per day, with the same method (a short lesson, then hands-on practice, starting easy):

- **morning — Engineering:** a core taken to independence (TypeScript and JavaScript, React and Next.js, NestJS and backend, SQL, algorithms up to graphs, tests and debugging, architecture), plus a red-thread Next.js/NestJS application built two mornings a week and presentable at the end;
- **afternoon — Applied AI:** Python, FastAPI, LLM applications, RAG with LangChain, agents with LangGraph, evaluation with LangSmith, and a final capstone.

You write every line of every exercise: Techne scaffolds and reviews, but never writes your implementation, and never teaches you to delegate it to an AI.

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

Then start Techne with `/techne:init` (type `/techne:` to see every command). Natural language also works; Techne maps it to the matching command (see [Commands](#commands)).

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
- runs a short **placement test**, about an hour: each area starts with an easy exercise and gets harder only while you succeed, so the curriculum starts at the right level;
- starts the curriculum, where each exercise is preceded by a short lesson in your browser.

The whole start takes two questions and under five minutes before the first exercise.

### Where to run it

Anywhere Claude Code runs, but a terminal inside your editor (VS Code, or iTerm next to it) is the smoothest: the code, the tests, and Techne share one window, and Techne resolves your workspace from the current folder. Run one Techne session at a time; concurrent sessions are detected and warned about, not merged.

The rhythm is six full days and one light day per week, and the programme advances in working days, so missing a day delays nothing. Your progress is tracked subject by subject — not started, discovered, with help, independent, transferred, blocked — and shown on the "My progress" page in your browser.

Techne does not flatter: it names what you demonstrated and what you did not, gives a blunt assessment every six working days, and compares your map to what is expected of a senior React/Node developer on working days 20, 40 and 60.

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
| `init` | Asks your learning language, sets up your learning folder, and runs the placement test. | Once, the first time you use Techne. |
| `resume` | Picks up where you left off and gives you exactly one next action. Typing the entry point alone does the same. | To start the day or come back after a break, from any folder or a new conversation. |
| `hint` | Gives one more step of help on the current exercise, from a guiding question up to the solution explained. | When you are stuck on the exercise itself. Each call gives a little more help; work done with help counts as practice, not as proof of mastery. |
| `ask <question>` | Answers any question: where you are, why this subject, what a word means, how a tool works. Costs you nothing and leaves no trace. | Whenever you wonder anything. It declines only the answer to the exercise you have open — that is what `hint` is for. |
| `status` | Shows the current activity, your mastery map subject by subject, due reviews, and Applied AI progress, with the two curricula kept separate. | When you want to know where you stand. |
| `programs` | Lists the programs you can follow, the ones you are enrolled in, and your coverage in each. | To see what you are carrying. |
| `switch <id>` | Saves your progress and opens another program you follow. | Whenever you want to change course. |
| `schedule` | Shows your weekly schedule and offers to change it, or writes a first one from your enrolments. | When your week changes shape. |
| `enroll <id>` / `leave <id>` | Follow a program, or stop following it without losing what you proved. | When your goals change. |
| `new` | Creates a program with you, by interview: you bring the subjects and Techne structures them, or you give an objective and Techne designs the course. | When you want to learn something Techne does not ship. |
| `pause` | Saves your progress and keeps the day open; `resume` continues exactly where you stopped. | Before a short break. |
| `end` | Saves your progress, closes the session, and gives you four closing lines. | At the end of your working session. |
| `feedback <text>` | Talks about the teaching: a preference is applied at once, a bigger change is discussed and recorded. | When the method or the content does not suit you. |
| `issue <text>` | Records a defect or an idea about Techne itself, with the activity it came from. | The moment the tool misbehaves, without losing your thread. |
| `extract-issues` | Exports everything you reported, grouped and dated, ready to paste into the Techne repository. | When you sit down to improve Techne itself. |
| `reset` | After you confirm, puts your progress aside (archived, not deleted unless you ask) so Techne starts again from `init`. Your exercise files stay unless you ask to remove them. | To start the whole curriculum over. Updating Techne never needs it: an older workspace is migrated, not reset. |
| `uninstall` | After you confirm, removes Techne from your agent, optionally after a `reset`, and tells you how to reinstall. | When you no longer want Techne, or to retest installation. |

### Natural language

You can also just talk to the agent, in any language: "on reprend", "I'm stuck", "où en suis-je ?". The agent maps a clear request to the matching command and runs it. If your intent is ambiguous, it asks which command you mean. Inside an active Techne workspace, you can often skip the invocation entirely.

## Resume from another directory or a new conversation

The conversation transcript is not the source of truth. Techne reconstructs the learning session from persisted files.

It resolves the workspace in this order:

1. `.techne/STATE.json` in the current directory or one of its parents;
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

Restart your agent after an update. If a new version changes how progress is stored, Techne says so and offers to migrate your workspace; your evidence is preserved, and you never need a `reset` to update.

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

The learning experience is delivered in the language you choose during `init`: lessons, exercise prompts, feedback, progress reports, and browser UI. The choice is stored in `.techne/STATE.json`; ask Techne to switch language at any time. Established technical terms remain in English when that is clearer.

The browser UI ships with English and French strings (`assets/browser/assets/i18n.js`); other languages fall back to English in the browser while the lessons themselves are written in your language.

## Repository structure

The repository contains one canonical skill and two distribution adapters:

```text
.claude-plugin/marketplace.json              Claude Code marketplace
plugins/techne/.claude-plugin/plugin.json    Claude Code plugin manifest
plugins/techne/commands/                     Claude Code slash commands (thin wrappers)
plugins/techne/skills/techne/                Canonical Agent Skill
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

For local Claude Code testing, add this checkout as a marketplace:

```bash
claude plugin marketplace add .
claude plugin install techne@jsharles
```

For local `skills` discovery without publishing to GitHub:

```bash
npx skills@latest add . --skill techne --agent codex
```

Python, FastAPI, LangChain, LangGraph, and LangSmith are taught in the afternoon Applied AI curriculum. They are not runtime dependencies of the Techne skill itself. The Applied AI track makes model API calls with the learner's own key (or a local model), so it can incur small provider costs.
