---
id: git-mastery
title: Git, en profondeur
version: 1
activity_kinds: code, browser
lesson_to_practice: practice-heavy
timeboxes: lesson=10, exercise=25, review=5, placement=20
red_thread: no
survey_ceiling: discovered
---

# Git, en profondeur

## Outcome and boundary

For a developer who already uses Git at an intermediate level in a team: branches, pull requests, rebase,
code review. The goal is to become solid rather than to learn the basics. By the end, the learner predicts
what every common command will do before running it, because they reason from Git's model (objects, refs,
`HEAD`, the index). They shape a clean history before a pull request, resolve any conflict calmly, recover
from any broken state with `reflog` and `reset`, investigate history with `log`, `blame` and `bisect`,
work across forks and remotes without fear of `push --force`, and set up the guard rails a team relies on:
hooks, conventions, protected branches, and a first GitHub Actions workflow that runs tests on a pull
request.

Activities are mostly terminal work. Techne prepares a real repository in a precise state (a conflict in
progress, a messy history, a lost commit, a diverged remote) and the learner brings it to the requested
state with Git commands only. Techne then checks the resulting repository directly: commit graph, trees,
refs, working tree. Short browser quizzes serve recall and reviews. Every new notion opens with a 10-minute
lesson.

The placement test (20 minutes) runs a few repository scenarios across the units, and compresses what the
learner already does without help. What was demonstrated in another program does not count here.

Sources, all free: the Pro Git book (git-scm.com/book), the official Git reference documentation, the
GitHub Docs (pull requests, protected branches, Actions), Conventional Commits, and Semantic Versioning.

Deliberately out of scope: Git internals below the object model (packfile format, low-level plumbing beyond
`cat-file`, `rev-parse` and `ls-files`), administering a Git server, large-scale monorepo tooling, and CI
beyond a first test workflow on pull requests. Submodules, subtrees, Git LFS, sparse checkout and packfiles
are surveyed only.

The program stands alone: a stranger can follow it without any other. It keeps its own evidence.

## Sequence

### Unit 1 — Git's model

- Blobs, trees, commits and tags as content-addressed objects; reading them with `git cat-file`.
- Refs, branches as movable pointers, `HEAD`, detached `HEAD`.
- The three trees: `HEAD`, the index, the working tree; what `add`, `commit` and `checkout` move.
- Revision syntax: `HEAD~2`, `HEAD^2`, `@{u}`, `main..feature`, `main...feature`.

### Unit 2 — Committing well

- Atomic commits; staging hunks with `git add -p`, unstaging with `git restore --staged`.
- Commit messages: subject and body, Conventional Commits.
- `commit --amend` and `commit --fixup`.

### Unit 3 — Branches, merge and conflicts

- Merge base; fast-forward against three-way merge; `--no-ff`.
- Reading a conflict: markers, `ours` and `theirs`, the `diff3` / `zdiff3` conflict style.
- Resolving with `git checkout --ours/--theirs`, a merge tool, and aborting cleanly.
- `rerere` for conflicts that come back.

### Unit 4 — Rebase in depth

- What rebase replays, and why commit hashes change.
- Interactive rebase: reorder, squash, fixup, reword, edit, drop; splitting a commit.
- `--autosquash` with fixup commits; `rebase --onto` to move a range.
- Conflicts during a rebase; `--continue`, `--skip`, `--abort`.
- When to rebase and when to merge: the team policy and the shared-history rule.

### Unit 5 — Undoing and recovering

- `restore`, `reset --soft/--mixed/--hard`, `revert`, including reverting a merge.
- `reflog`: recovering a lost commit, a deleted branch, a bad rebase or reset.
- `stash`: push with a message, partial stash, `pop` against `apply`, stash conflicts.
- `git clean` and what it destroys.

### Unit 6 — Remotes and collaboration

- `fetch` against `pull`; remote-tracking branches; upstream configuration.
- `pull --rebase` and `pull.rebase`; diverged branches.
- `push --force-with-lease` against `--force`; what happens to a teammate's work.
- Fork workflow: `origin` and `upstream`, keeping a fork in sync.

### Unit 7 — Investigating history

- `log` filters: by author, path, date, `--grep`, `--graph`, `--first-parent`.
- `diff` between commits, branches and the index; `--stat`, `--word-diff`.
- `blame` with `-w`, `-C`, and `--ignore-rev`; the pickaxe `log -S` and `log -G`.
- `bisect`, manual and with `bisect run` on a test.

### Unit 8 — Moving changes around

- `cherry-pick`, including a range and a backport onto a release branch.
- `range-diff` to compare two versions of a rebased branch.
- `worktree` to work on two branches at once.

### Unit 9 — Team workflows on GitHub

- Trunk-based development against GitFlow; short-lived branches; pull request size.
- Stacked pull requests, and updating a stack after the base changes.
- Reviewing on GitHub: suggestions, requesting changes, re-reviewing after a force push.
- Protected branches, required reviews and checks, `CODEOWNERS`.
- Releases: annotated tags, Semantic Versioning, changelogs from commits.

### Unit 10 — Configuration and guard rails

- Configuration levels (system, global, local, `includeIf`); useful aliases.
- `.gitignore`, `.gitattributes`, line endings.
- Hooks: `pre-commit` and `commit-msg`, and how a team shares them.
- Signing commits and tags.

### Unit 11 — A first CI workflow

- GitHub Actions: workflow file, trigger on `pull_request`, a job that installs and runs tests.
- Making the check required on the protected branch.
- Reading a failed run and fixing it from the branch.

### Unit 12 — Repository hygiene

- Removing a secret or a large file from history with `git filter-repo`, and what it means for clones.
- `gc`, `fsck` and dangling objects, in relation to the reflog.

### Unit 13 — Breakage drills

- Composite scenarios that mix earlier units without saying which: a rebase gone wrong on a shared branch,
  a force push that erased a teammate's commits, a regression to locate and revert on a release branch.
  The learner diagnoses the state first, then repairs it.

## Subject catalogue

### Model — `gitmodel.*`

`objects`, `refs-head`, `three-trees`, `revision-syntax`

### Commits — `gitcommit.*`

`atomic-commits`, `partial-staging`, `commit-messages`, `conventional-commits`, `amend-fixup`

### Merge and conflicts — `gitmerge.*`

`merge-base`, `fast-forward`, `conflict-reading`, `conflict-resolution`, `rerere`

### Rebase — `gitrebase.*`

`rebase-replay`, `interactive-rebase`, `split-commit`, `autosquash`, `rebase-onto`, `rebase-conflicts`,
`rebase-vs-merge`

### Undo and recovery — `gitundo.*`

`restore-reset`, `revert`, `revert-merge`, `reflog-recovery`, `stash`, `clean`

### Remotes — `gitremote.*`

`fetch-pull`, `tracking-branches`, `pull-rebase`, `force-with-lease`, `fork-workflow`

### History — `githist.*`

`log-filters`, `diff-ranges`, `blame`, `pickaxe`, `bisect`

### Moving changes — `gitmove.*`

`cherry-pick`, `range-diff`, `worktree`

### Team workflows — `gitteam.*`

`branching-models`, `pr-size`, `stacked-prs`, `github-review`, `branch-protection`, `releases-tags`

### Configuration and guard rails — `gitconf.*`

`config-levels`, `ignore-attributes`, `hooks`, `signing`

### CI — `gitci.*`

`actions-workflow`, `required-checks`, `failed-run`

### Hygiene — `githyg.*`

`history-rewrite-secrets`, `gc-fsck`

### Survey — `gitsurvey.*`

`submodules`, `subtree`, `lfs`, `sparse-checkout`, `packfiles`

## Adaptation rules

- A new notion is taught in a 10-minute lesson, then practised at once on a prepared repository. The
  exercise is done when the repository reaches the requested state, checked by Techne from the graph, refs
  and trees; the commands the learner ran are not the criterion, the result is.
- Before running a command in an exercise, the learner may be asked to predict its effect on the graph in a
  file; the prediction is evidence about the model, the repository about the skill.
- The placement test compresses any unit whose scenarios the learner solves without help; those subjects go
  straight to a harder scenario rather than a lesson.
- Difficulty rises by removing hints from the scenario, then by hiding which notion applies, then by
  combining two earlier notions.
- Transfer is an earlier notion reused unannounced in a later scenario, above all in the breakage drills.
  Used correctly without help, it counts as transferred.
- Survey subjects attach to the lessons of neighbouring units and never get a unit of their own.
- Recall and reviews run as short browser quizzes, never as questions in the chat.
