---
id: ai-native
title: AI-native software engineering
version: 1
activity_kinds: code, writing
lesson_to_practice: practice-heavy
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=0
red_thread: yes
survey_ceiling: discovered
---

# AI-native software engineering

## Outcome and boundary

For a TypeScript developer who wants to ship reliable software whose code is mostly written by coding agents,
without losing control of what they produce. Modelled in spirit on aienhanced.dev (research → plan → first
slice → worktrees → several agents → risk-based review → deploy → keep rules alive), on a different stack:
Next.js 16 (App Router), TypeScript strict, Effect 4, Alchemy 2, Cloudflare, Claude Code. About 15 hours.

The learner learns three gestures an agent never does for them:

1. **Decide** — product scope, architecture, module boundaries, what stays out.
2. **Constrain** — turn decisions into rules a machine enforces: strict types, typed errors with Effect,
   lint, boundary checks, tests, AGENTS.md, Claude Code permissions and hooks.
3. **Verify** — automated gates first, then a human review aimed at risk instead of every line.

The stack is the training ground, not the subject. Next.js is the thinnest layer (UI, server actions); logic
lives in Effect so it does not depend on the framework; Alchemy puts infrastructure in the same TypeScript
repository so an agent can change it and the learner reviews it like any other code.

Deliberately out of scope: teaching Next.js, React or Cloudflare from scratch; prompt collections detached
from a repository; model training; multi-tenant SaaS concerns (billing, teams, RBAC); Durable Objects and KV
unless a feature truly needs them (module 14 makes the learner justify that refusal in writing); Codex (the
learner uses Claude Code only).

The final proof: the learner hands a new feature to an agent, merges it after a targeted review, and the
architecture still holds.

## Who writes what — method exception

This program runs under the decision of 2026-10-01 in `.techne/DECISIONS.md`: the rule "the learner writes
every line" applies only when the subject of study is coding. Here the subject is directing coding agents.

- **Claude Code writes** the application code, tests, migrations and infrastructure code, in the Shelf repository.
- **The learner writes by hand** everything that directs and judges the agents: product brief, research
  questions, ADRs, architecture doc, AGENTS.md files, skills, lint and boundary rules, plans, task breakdowns,
  prompts, review verdicts, the slop report. These are the evidence.
- **Techne writes** neither the learner's code nor their rules or documents. It gives prompt skeletons
  (structure only, project content left blank), reviews the learner's artifacts, and prepares review
  exercises: copies of the learner's own pull requests with defects planted in them.
- **Agents never touch** any other repository of the learner, in particular the Engineering red-thread
  project, where "no LLM pre-review" stays in force.

Evidence for a subject comes from an artifact that actually constrained an agent (an out-of-scope edit
blocked, a wrong API refused by the compiler, a test that fails when the code is broken) or from a planted
defect the learner found unaided. An artifact that exists but changed nothing is `discovered`, not more.

## The project — Shelf

A web-page archiving app. The user pastes a URL; Shelf answers "saved" at once; in the background it fetches
the page, extracts title, text and metadata, and keeps a snapshot, so the link survives the page's
disappearance. The user tags links, searches their text, shares a collection through a public read-only link,
exports everything, and bulk-imports a browser bookmarks file.

Why this product: fetching pages from sites one does not own fails often and for real reasons (slow, 404,
PDF instead of HTML, 40 MB page, redirect loop) — exactly where Effect's typed errors matter and where agents
write `catch {}`. Tags, sharing, export and search are nearly independent, so three agents can work at once,
with one real point of friction: the database schema. The domain is banal on purpose: the learner can judge
correctness alone, so a bug is always the agent's, never a misunderstanding of the domain.

Cloudflare services and why each one is there:

| Service | Use in Shelf |
| --- | --- |
| Workers | Next.js through OpenNext, and the `capture` Worker |
| D1 | users, sessions, links, tags, collections; Better Auth's tables |
| R2 | page snapshots, export files, imported bookmark files |
| Queues | capture jobs, with retries and a dead-letter queue |
| Workflows | bulk import: long, multi-step, must resume after a failure |
| KV, Durable Objects | not used unless OpenNext caching or a feature demands it |

Repository shape, built up across modules:

```text
shelf/
  AGENTS.md            rules every agent reads first; CLAUDE.md only imports it
  alchemy.run.ts       all infrastructure, per stage
  apps/web/            Next.js: UI and server actions, no direct D1/R2 access
  apps/capture/        Worker: queue consumer and import Workflow
  packages/domain/     Effect services, Schema, typed errors, business rules
  packages/db/         Drizzle schema and D1 migrations
  docs/                product.md, architecture.md, adr/, research/, effect4.md, plans/
  .claude/             settings.json (permissions, hooks), skills/
  tests/e2e/           Playwright
  .github/workflows/   gates, previews per PR, prod deploy
```

The founding rule: `apps/web` never touches D1 or R2 directly. It calls `packages/domain`, which receives its
dependencies as Effect Layers. Tests swap infrastructure without hand-made mocks, and dependency-cruiser checks
the boundary on every commit — not an agent's goodwill.

## How Techne works on this program

Techne is product owner and tech lead. Each module opens with a lesson of at most ten minutes, then the
learner works on Shelf. The module's deliverable is a merged pull request on Shelf, and Techne reviews it
against the module's validation criteria. Questions tied to an exercise are answered in files, never in the
chat (decision of 2026-09-18, clarified 2026-09-21).

Every module, when opened, gives the learner these eleven parts, in the learning language: objective,
concepts, estimated time, minimal theory, practical exercise, deliverable, commands, prompt skeletons,
validation criteria, frequent mistakes with AI agents, what to understand before moving on. The sequence below
holds them in condensed form. Each module also states the split of responsibility:

- what the human decides; what the agent may decide; what is automated; what the human must verify;
- which documents the agent receives and how much context; how scope is enforced; how drift is spotted early.

Prompt skeletons are structure, not content. The learner fills the project-specific parts; the filled prompt
is evidence.

## Start of the track

1. Check Node 22+, pnpm, git, Claude Code, a GitHub account, and a Cloudflare account (free plan first; name it
   if a service in use needs the paid Workers plan before anything is deployed). Install nothing without consent.
2. The learner creates the empty public repository `shelf` on GitHub themselves.
3. Version watch (see "Keeping content current") runs once, before module 0.

## Sequence

### Module 0 — Effect 4, fast (45 min)

- **Objective:** read and direct Effect 4 code: generators, typed errors, services and Layers, Schema.
- **Concepts:** `Effect<A, E, R>`; `Effect.gen`; tagged errors; services and Layers; `Schema` decoding at the
  edge; `Effect.runPromise` only at the boundary.
- **Theory:** an Effect is a description of work whose type lists what it returns, how it fails and what it
  needs. The `E` channel is why an agent cannot silently swallow an error: removing a failure forces a change
  the compiler sees. Agents were trained mostly on Effect 3; Effect 4 moved platform modules into core.
- **Exercise:** in a scratch folder, ask Claude Code for a `fetchTitle(url)` effect with three tagged errors
  (timeout, not HTML, HTTP status). Compile it against the pinned version. Log every API the agent used that
  does not exist in Effect 4.
- **Deliverable:** `docs/effect4.md` in the Shelf repo, written by the learner: the ten APIs Shelf will use,
  each with a correct one-line example from the official docs, and the wrong Effect 3 forms the agent produced.
- **Commands:** `pnpm init`, `pnpm add -E effect`, `pnpm add -D -E typescript`, `pnpm tsc --noEmit`.
- **Prompt skeleton (coding, constrained):** "Context: <file to read>. Task: <one function>. Constraints: Effect
  version <x>, only APIs listed in <doc>; errors as tagged classes; no `any`, no `try/catch`. Done when: <command>
  passes. Stop and ask if an API you need is not in the doc."
- **Split:** human picks the APIs Shelf needs; agent writes the kata; compiler judges; human reads every line
  here (the only module where that is expected).
- **Validation:** `docs/effect4.md` cites the official source for each API; the kata compiles with zero `any`.
- **Frequent mistakes with agents:** invented APIs stated with confidence; `Effect.runPromise` scattered in
  business code; errors typed as `unknown` or `Error`; a wrapper "helper" around every Effect call.
- **Before moving on:** why the `E` type makes silent errors visible, and why the agent needs a written source
  of truth for a library newer than its training.

### Module 1 — Alchemy and Cloudflare, fast (30 min)

- **Objective:** deploy and destroy infrastructure from TypeScript, per stage.
- **Concepts:** stack, resource, typed binding, stage, state store; `alchemy dev`, `deploy`, `destroy`.
- **Theory:** infrastructure as code in the same repo means an agent's infra change is a diff like any other.
  A stage is a full disposable copy of the infra; previews per pull request are stages.
- **Exercise:** have the agent write `alchemy.run.ts` with one Worker bound to one D1 database; deploy to stage
  `sandbox-<name>`; call the Worker; destroy the stage; check the Cloudflare dashboard is clean.
- **Deliverable:** the smoke stack committed, and `docs/research/alchemy.md` written by the learner: the
  commands, how stages and state work, and three API differences between what the agent first wrote and the
  current docs.
- **Commands:** `pnpm add -E alchemy`, `pnpm alchemy --help`, `pnpm alchemy deploy --stage sandbox-<name>`,
  `pnpm alchemy destroy --stage sandbox-<name>` (check exact flags with `--help`; Alchemy 2 is in beta).
- **Prompt skeleton (infrastructure):** "Read <alchemy doc file>. Add <resource> bound to <worker>. Do not
  touch other resources. Show the plan of created/changed/deleted resources before deploying. Never deploy to
  `prod`."
- **Split:** human chooses stage names and who may deploy where; agent writes resources; human verifies the
  resource diff before every deploy.
- **Validation:** a deploy and a destroy both ran; nothing left behind.
- **Frequent mistakes with agents:** Alchemy 0.x syntax; secrets written in code; deploying to the wrong stage;
  adding resources "for later".
- **Before moving on:** what a stage is, and why an infra diff deserves the same review as code.

### Module 2 — Product framing and research (45 min)

- **Objective:** decide what Shelf is and is not before any agent writes code.
- **Concepts:** problem, users, scope, non-goals, hard parts, research with primary sources.
- **Theory:** an upfront giant spec drifts; a short brief plus research on the hard parts stays alive.
  Research is the one phase where the agent may roam wide, read-only.
- **Exercise:** write `docs/product.md` (one page: problem, the five features, non-goals, the three hard parts).
  Then ask Claude Code, read-only, to research the hard parts (OpenNext limits on Workers, Better Auth on D1,
  Queues retry semantics) and write notes with sources.
- **Deliverable:** `docs/product.md` (learner) and `docs/research/*.md` (agent, every claim sourced, reviewed by
  the learner who marks each claim verified or not).
- **Commands:** `git init`, first commit, push to GitHub.
- **Prompt skeleton (research):** "Question: <precise question>. Sources allowed: official docs, release notes,
  repositories. For each claim give the URL and the version it applies to. Say what you could not verify.
  Do not write code. Do not propose architecture."
- **Split:** human decides scope and non-goals; agent may decide nothing about the product; research is
  automated; human verifies two sourced claims by hand.
- **Validation:** non-goals exist and are specific; every research claim has a source and a version.
- **Frequent mistakes with agents:** research that slides into architecture; unsourced confident claims;
  feature creep proposed as "nice to have".
- **Before moving on:** why non-goals protect against agents more than goals do.

### Module 3 — Architecture and decisions (45 min)

- **Objective:** fix the boundaries agents will work inside.
- **Concepts:** layers (web, domain, db, capture), the dependency rule, error taxonomy, ADRs.
- **Theory:** an agent left free invents an architecture per task; consistency comes from a written one. An
  ADR records a decision, its rejected alternative and its cost, so the next agent does not reopen it.
- **Exercise:** write `docs/architecture.md` (the diagram, the dependency rule, which package owns what) and
  four ADRs: monorepo layout, Effect at the domain boundary, Better Auth on D1, Drizzle for schema and
  migrations. Then ask the agent to critique the architecture, not rewrite it.
- **Deliverable:** `docs/architecture.md` and `docs/adr/0001…0004` written by the learner.
- **Prompt skeleton (architecture review):** "Read <docs>. Find contradictions, missing decisions, and places
  where an agent would have to guess. Do not propose new layers or abstractions. Answer as a numbered list."
- **Split:** human decides every boundary; agent critiques; human accepts or rejects each point in writing.
- **Validation:** for any file path a feature will need, the doc says which package it belongs to.
- **Frequent mistakes with agents:** over-architecture (repositories, factories, "ports and adapters" for a
  15-hour app); abstractions with one implementation; the agent's critique silently becoming a redesign.
- **Before moving on:** the dependency rule in one sentence, and where each kind of error is handled.

### Module 4 — The AI-friendly repository (75 min)

- **Objective:** a repo that rejects bad code before the learner sees it.
- **Concepts:** pnpm workspace; `tsconfig` strict plus `noUncheckedIndexedAccess`; typescript-eslint
  strict-type-checked; `max-lines` and `max-lines-per-function`; no floating promises; Prettier;
  dependency-cruiser for boundaries; knip for dead code; husky pre-commit; one `pnpm check` command; CI.
- **Theory:** every element exists to catch one kind of slop mechanically: types catch lies, lint catches
  sloppiness, boundaries catch architecture drift, knip catches generated-but-unused code, `max-lines` catches
  giant files. One `check` command gives the agent and CI the same definition of done.
- **Exercise:** the learner writes the rules (which lint rules, which limits, which boundaries); the agent
  scaffolds the workspace and the Next.js app to satisfy them. Then the learner plants three violations
  (a cross-boundary import, an unused export, a floating promise) and checks each is caught.
- **Deliverable:** `pnpm check` green locally and in GitHub Actions; the three planted violations caught.
- **Commands:** `pnpm create next-app@latest apps/web`, `pnpm add -D -E eslint typescript-eslint prettier
  dependency-cruiser knip husky lint-staged`, `pnpm check`.
- **Prompt skeleton (setup):** "Set up <tool> to enforce exactly these rules: <list>. Do not add rules I did
  not list. Do not disable a rule to make code pass; report the violation instead."
- **Split:** human decides every rule and limit; agent configures; CI automates; human verifies with planted
  violations, not by reading config.
- **Validation:** each planted violation fails `pnpm check` with a readable message.
- **Frequent mistakes with agents:** `eslint-disable` sprinkled to get green; rules relaxed silently;
  ten dev dependencies nobody asked for; a gate that passes because it checks nothing.
- **Before moving on:** which gate catches which slop, and that a gate is proven only by making it fail.

### Module 5 — Rules for agents (60 min)

- **Objective:** an agent that knows the project's rules and cannot leave its scope.
- **Concepts:** root and per-package `AGENTS.md`; `CLAUDE.md` importing it; a Claude Code skill pointing at
  `docs/effect4.md`; `.claude/settings.json` permissions (deny edits to `alchemy.run.ts`, migrations, CI unless
  the task says so); a hook running `pnpm check` after edits.
- **Theory:** write constraints, not micro-instructions. An instruction the machine can enforce goes in a gate;
  only what it cannot enforce goes in AGENTS.md. Short rules are read; long ones are skimmed.
- **Exercise:** write the AGENTS.md files (under 80 lines at the root). Run three probes: ask the agent to add
  a feature that would need a forbidden import, to "quickly fix" CI, and to use an Effect 3 API. Record what
  stopped each one.
- **Deliverable:** AGENTS.md files, `.claude/settings.json`, one skill; a probe log with the three outcomes.
- **Commands:** `claude`, then `/memory` and `/permissions` inside Claude Code to inspect what it loaded.
- **Prompt skeleton (documentation for agents):** "Read AGENTS.md and list every rule you would find ambiguous
  or could satisfy in two contradictory ways. Do not edit the file."
- **Split:** human writes every rule; agent only reports ambiguity; permissions and hooks automate scope;
  human verifies with the probes.
- **Validation:** all three probes stopped by a rule, a permission or a gate — not by luck.
- **Frequent mistakes with agents:** a 500-line AGENTS.md; rules duplicating lint; contradictory rules between
  root and package files; architecture invented by the agent because the rule was vague.
- **Before moving on:** what goes in a gate, what goes in AGENTS.md, what goes nowhere.

### Module 6 — First vertical slice, one agent (90 min)

- **Objective:** sign in and save a link, deployed on a preview stage, with one agent end to end.
- **Concepts:** thin slice through every layer; plan file; plan review before code; small commits; preview
  stage per pull request.
- **Theory:** the first slice proves the architecture before features pile up. A plan reviewed before code is
  the cheapest place to catch a wrong direction.
- **Exercise:** the agent writes `docs/plans/001-first-slice.md` (files touched, order, tests, risks); the
  learner amends and approves it; the agent implements on a branch; the learner stops it at the first sign of
  drift. Better Auth on D1, a `links` table, a domain `saveLink` service, a server action, a page.
- **Deliverable:** merged PR; preview URL working; plan file kept in `docs/plans/`.
- **Commands:** `git switch -c feat/first-slice`, `pnpm check`, `pnpm alchemy deploy --stage pr-<n>`.
- **Prompt skeleton (implementation plan):** "Read <docs>. Write a plan for <slice>: files to create or change,
  in order; what each test proves; what you will not touch; open questions. No code yet."
- **Prompt skeleton (coding):** "Implement step <k> of <plan>. Stay inside <paths>. Run `pnpm check` and stop
  when it passes. If the plan is wrong, stop and say why instead of improvising."
- **Split:** human approves the plan and every deviation; agent decides local implementation details; gates
  automate correctness checks; human verifies auth and the data written to D1.
- **Validation:** the plan's "won't touch" list held; `apps/web` imports nothing from `packages/db`.
- **Frequent mistakes with agents:** skipping the plan; one giant commit; auth code copied from an old tutorial;
  code generated for future features; comments narrating what the code does.
- **Before moving on:** how to spot drift from the diff stat and the plan, before reading code.

### Module 7 — Planning and atomic tasks (45 min)

- **Objective:** turn the remaining features into tasks an agent can finish alone.
- **Concepts:** atomic task (one outcome, one owner, verifiable), dependency graph, shared-file hotspots,
  issue template.
- **Theory:** a task is atomic when its done condition is a command and it touches no file another parallel
  task touches. The schema is the usual hotspot: migrations serialize.
- **Exercise:** the learner breaks tags, export, sharing, search and capture into about eight GitHub issues,
  each with outcome, acceptance criteria, paths in scope, and dependencies; draws the graph; marks which can
  run in parallel.
- **Deliverable:** the issues and `docs/plans/backlog.md` with the graph.
- **Prompt skeleton (planning critique):** "Read these issues. For each pair, say whether they touch a common
  file or table. Flag any issue whose done condition is not a command."
- **Split:** human decides the cut and the order; agent detects overlaps; human verifies the graph.
- **Validation:** no two tasks marked parallel share a migration or a file.
- **Frequent mistakes with agents:** tasks that are really epics; vague done conditions; hidden dependency on an
  unmerged schema change.
- **Before moving on:** what makes two tasks safe to run at the same time.

### Module 8 — Tests that matter (60 min)

- **Objective:** tests that fail when the code is wrong, not tests that restate it.
- **Concepts:** domain unit tests with test Layers and `@effect/vitest`; integration on local D1; one
  Playwright end-to-end path; the "break it" check.
- **Theory:** a test that mirrors the implementation passes whatever the code does. The learner decides what
  must be proven; the agent writes the test; breaking the code proves the test.
- **Exercise:** write `docs/testing.md` (what each level proves, what is not tested). Ask the agent for tests on
  `saveLink` and auth. Then break the code three ways by hand and keep only tests that caught something.
- **Deliverable:** `docs/testing.md`, the tests, a short note of what each break revealed.
- **Commands:** `pnpm add -D -E vitest @effect/vitest @playwright/test`, `pnpm test`, `pnpm e2e`.
- **Prompt skeleton (test generation):** "Write tests proving these behaviours: <list>. Use the test Layer, not
  mocks of internal functions. Do not assert on implementation details. For each test, name the bug it catches."
- **Split:** human decides behaviours to prove; agent writes tests; CI runs them; human verifies by breaking.
- **Validation:** every kept test failed at least once against a deliberate break.
- **Frequent mistakes with agents:** snapshot tests of everything; mocks of the unit under test; tests that
  assert the mock was called; 40 tests for one function.
- **Before moving on:** how to know a test is useful without reading it closely.

### Module 9 — Async jobs and resilience (75 min)

- **Objective:** capture pages in the background, reliably.
- **Concepts:** Queue producer and consumer; Effect `retry` with `Schedule`, `timeout`, tagged errors per
  failure cause; idempotency key; dead-letter queue; snapshot to R2; size limits.
- **Theory:** each failure cause gets a decision: retry, give up, or mark the link. Effect makes the decision
  visible in types; an agent's generic retry-everything loop shows up as a type that lies.
- **Exercise:** the learner writes the failure table (cause → retry? how often? final state). The agent
  implements the `capture` Worker and the infra in Alchemy following it, inside a plan.
- **Deliverable:** merged PR; a test per failure cause; a link to a 404 page ends in a clear final state.
- **Prompt skeleton (coding with failure table):** "Implement <consumer> following exactly this failure table:
  <table>. Every row is a tagged error. No catch-all. Retries only where the table says."
- **Prompt skeleton (infrastructure):** as module 1, plus "show the resource diff for the Queue and DLQ".
- **Split:** human decides every failure policy; agent implements; tests automate; human verifies the infra
  diff and the idempotency.
- **Validation:** the same message delivered twice produces one snapshot.
- **Frequent mistakes with agents:** `catch (e) { console.log(e) }`; retries on 404; no timeout; unbounded
  page size; error types widened to `unknown`.
- **Before moving on:** why the failure policy is a human decision.

### Module 10 — Agents in parallel (90 min)

- **Objective:** three features delivered by three agents at once, without breaking each other.
- **Concepts:** `git worktree`; one agent per worktree; serialized migrations; merge order; rebase after each
  merge; handoff notes that survive the end of a session; the cost of parallelism.
- **Theory:** parallelism pays only when tasks are truly independent. Past three agents, the learner's review
  becomes the bottleneck.
- **Exercise:** tags, export and public sharing, from the module 7 graph. Migrations merged first. Each agent
  gets its issue, its paths, and a handoff file it must update.
- **Deliverable:** three merged PRs; `docs/plans/parallel-log.md` (what collided, what the learner did).
- **Commands:** `git worktree add ../shelf-tags -b feat/tags`, one `claude` session per worktree,
  `git worktree remove ../shelf-tags` after merge.
- **Prompt skeleton (parallel task):** "You work only in <paths> for issue <n>. Another agent works on <other
  paths>; never edit them. Update <handoff file> before stopping."
- **Split:** human decides what runs in parallel and the merge order; agents decide local code; gates run per
  PR; human verifies schema and shared files.
- **Validation:** no agent edited another's paths; `main` stayed green after every merge.
- **Frequent mistakes with agents:** agents contradicting each other (two date helpers, two error styles);
  duplicated utilities; a fourth agent "to go faster"; merging out of dependency order.
- **Before moving on:** the limit of parallelism and where it comes from.

### Module 11 — Risk-based review (60 min)

- **Objective:** review without reading every line, and still catch what matters.
- **Concepts:** gates first; an automated review pass (Claude Code in a separate session, or the Claude Code
  GitHub Action) told the risks to look for; risk triage (auth, data, migrations, infra, secrets, money, deletion);
  PR template with a risk section.
- **Theory:** reading effort follows risk, not diff size. A reviewer agent must not be the agent that wrote the
  code, and receives the rules, not the author's reasoning.
- **Exercise:** write `REVIEW.md` (risk categories and what to check in each) and the PR template. Then review
  three Techne-prepared copies of the learner's own PRs, each with planted defects, in a file, unaided.
- **Deliverable:** `REVIEW.md`, PR template, review files with findings.
- **Prompt skeleton (review):** "Review this diff against <AGENTS.md>, <architecture.md>, <REVIEW.md>. Report
  only findings with a concrete failure scenario. No style comments. Rank by risk."
- **Split:** human decides the risk categories and the final verdict; agent does the first pass; human reads
  fully only the high-risk files.
- **Validation:** planted defects found in high-risk areas; time spent per PR noted.
- **Frequent mistakes with agents:** a reviewer flooding style nits; the author reviewing itself; approving
  because the reviewer agent said "looks good".
- **Before moving on:** what the learner always reads, and what they never read.

### Module 12 — Deploy, observe, debug (75 min)

- **Objective:** Shelf in production, observable, and a bug found from its traces.
- **Concepts:** `prod` stage deployed from `main`; preview per PR and destroy on close (Alchemy GitHub action);
  secrets in CI; Workers Logs and traces; Effect logging and `withSpan`; structured logs.
- **Theory:** an agent debugs well from evidence and badly from guesses. Observability is what turns a bug
  report into evidence.
- **Exercise:** wire the CI deploy; then the learner injects a bug in capture on a branch, deploys a preview,
  and has an agent find it from logs and traces only, following a debugging protocol.
- **Deliverable:** prod URL; CI deploying previews; `docs/runbook.md`; the debugging transcript summarized.
- **Commands:** `pnpm alchemy deploy --stage prod` (only through CI after the first time).
- **Prompt skeleton (debugging):** "Symptom: <observed>. Evidence: <logs, trace ids>. Form hypotheses, rank
  them, and propose the experiment that discriminates them. Do not change code until one is confirmed."
- **Prompt skeleton (migration):** "Write a forward-only migration for <change>. Show the SQL. Say what happens
  to existing rows. No destructive change without my approval."
- **Split:** human owns prod access and secrets; agent may deploy previews only; human verifies every infra diff
  touching prod.
- **Validation:** the injected bug found from traces; no secret in the repository.
- **Frequent mistakes with agents:** fixing the symptom; adding logs everywhere instead of spans; deploying
  prod from a laptop; secrets in `alchemy.run.ts`.
- **Before moving on:** what a good bug report gives an agent.

### Module 13 — Slop and refactoring (45 min)

- **Objective:** find what drifted and turn each finding into a rule.
- **Concepts:** slop catalogue (duplication, premature abstraction, giant files, dead code, useless comments,
  hidden dependencies, out-of-scope edits); knip and dependency-cruiser reports; refactoring under green tests.
- **Theory:** cleanup without a new rule recurs. Each finding ends in a gate, an AGENTS.md line, or an accepted
  exception.
- **Exercise:** have an agent produce a slop inventory; the learner triages it, writes `docs/slop-report.md`, and
  directs two refactors; then updates rules.
- **Deliverable:** slop report, two refactor PRs, rules updated.
- **Prompt skeleton (refactoring):** "Refactor <area> to <target shape>. Behaviour must not change: tests stay
  green without editing them. No new abstraction unless it removes at least two duplications."
- **Split:** human decides what is slop and what is fine; agent refactors; tests guard; human verifies tests were
  not edited.
- **Validation:** each finding mapped to a rule or an accepted exception.
- **Frequent mistakes with agents:** refactors that also change behaviour; editing tests to pass; a new
  abstraction replacing duplication with indirection.
- **Before moving on:** the loop finding → rule.

### Module 14 — Maintenance and a late feature (45 min)

- **Objective:** add bulk import without degrading the architecture, and keep rules and docs alive.
- **Concepts:** Cloudflare Workflow for a long resumable job; ADR for a new service; version watch as a task;
  doc and rule rot.
- **Theory:** the test of the whole setup is a feature that arrives late and pushes on every layer.
- **Exercise:** write ADR 0005 (Workflows for import; KV and Durable Objects refused, with reasons); plan,
  implement and review the import with the full process; run a dependency upgrade as an agent task.
- **Deliverable:** import merged and deployed; ADR 0005; docs and AGENTS.md updated; upgrade PR.
- **Prompt skeleton (documentation maintenance):** "Compare <docs> with the code. List statements that are no
  longer true. Do not edit; I decide."
- **Split:** human decides the new service and accepts doc changes; agent proposes; gates verify.
- **Validation:** the final proof: the import merged after a targeted review, and `pnpm check` plus the
  boundary rules unchanged and green.
- **Frequent mistakes with agents:** a new service adopted "because it exists"; docs updated by the agent with no
  human check; rules growing without pruning.
- **Before moving on:** this is the end — the learner can explain how they would onboard a new agent onto Shelf.

## Coverage of the 32 steps asked by the learner

| Steps | Module |
| --- | --- |
| 1 framing, 2 research | 2 |
| 3 architecture, 4 technology decisions, 7 architecture docs | 3 |
| 5 AI-friendly repo, 16 type checking, 17 linting, 18 formatting | 4 |
| 6 project rules, 8 AGENTS.md, 11 using Claude Code | 5 |
| 15 code generation, 20 integration tests (first) | 6 |
| 9 feature planning, 10 atomic tasks, 14 task dependencies | 7 |
| 19 unit, 20 integration, 21 end-to-end tests | 8 |
| 26 infrastructure as code (Queues, R2) | 1, 9 |
| 12 branches and worktrees, 13 parallel agents, 25 merge | 10 |
| 22 automated review, 23 risk-based human review, 24 fixing issues | 11 |
| 27 deployment, 28 observability, 29 debugging | 12 |
| 30 refactoring | 13 |
| 31 maintaining rules and docs, 32 new features without degrading | 14 |

## Subject catalogue

### Framing — `aiprod.*`

`product-brief`, `non-goals`, `hard-parts`, `research-with-sources`

### Architecture — `aiarch.*`

`layer-boundaries`, `dependency-rule`, `error-taxonomy`, `adr-writing`, `rejecting-over-architecture`

### Effect — `aieff.*`

`effect-type`, `generators`, `tagged-errors`, `services-layers`, `schema-validation`, `config`, `retry-schedule`,
`timeout`, `concurrency`, `runtime-boundary`, `test-layers`

### Repository and gates — `airepo.*`

`strict-typescript`, `lint-rules`, `formatting`, `boundary-checks`, `dead-code-detection`, `file-size-limits`,
`single-check-command`, `pre-commit-hooks`, `ci-gates`, `proving-a-gate`

### Agent rules — `airules.*`

`agents-md`, `constraints-over-instructions`, `skills`, `permissions-scope`, `agent-hooks`,
`library-source-of-truth`, `scope-probes`

### Planning and prompting — `aiplan.*`

`implementation-plan`, `plan-review`, `atomic-tasks`, `dependency-graph`, `prompt-research`, `prompt-architecture`,
`prompt-coding`, `prompt-debugging`, `prompt-review`, `prompt-refactoring`, `prompt-tests`, `prompt-docs`,
`prompt-migration`, `prompt-infra`, `early-drift-detection`

### Testing — `aitest.*`

`testing-strategy`, `behaviour-tests`, `integration-d1`, `end-to-end`, `break-it-check`, `rejecting-mirror-tests`

### Parallel agents — `aiflow.*`

`worktrees`, `parallel-limits`, `migration-serialization`, `merge-order`, `handoff-notes`, `agent-conflicts`

### Review — `aireview.*`

`automated-first-pass`, `risk-triage`, `review-checklist`, `pr-template`, `planted-defect-finding`,
`independent-reviewer`

### Infrastructure and operations — `aiinfra.*`

`alchemy-stacks`, `stages-previews`, `typed-bindings`, `d1-migrations`, `r2-storage`, `queues-dlq`, `workflows`,
`nextjs-on-workers`, `auth-on-d1`, `secrets`, `ci-deploy`, `observability`, `evidence-based-debugging`,
`service-refusal`

### Maintenance — `aimaint.*`

`slop-detection`, `finding-to-rule`, `safe-refactoring`, `doc-rot`, `version-watch`, `late-feature`

## Keeping content current

The stack moves fast, and this program pins the newest versions on purpose (decision with the learner,
2026-10-01). As verified on 2026-10-01: Effect 4.0.0 (GA that day), Alchemy 2.0.0-beta (alpha, built on Effect
4, breaking changes expected), @opennextjs/cloudflare 1.20 (Node runtime only, no edge runtime), Next.js 16.3,
Better Auth 1.7 (native D1), Drizzle 0.45 with a 1.0 beta.

- Versions are pinned exactly in Shelf. Nothing upgrades silently.
- At the opening of every module, Techne checks the npm registry and release notes for Effect, Alchemy,
  OpenNext, Next.js, Better Auth and Drizzle. A new version becomes an explicit upgrade task, run by an agent
  and reviewed by the learner; a breaking change that blocks a module is fixed before the module opens.
- When the agent's knowledge and the pinned version disagree, `docs/effect4.md` and `docs/research/` win, and
  the gap is recorded there.

## Adaptation rules

- 20 % theory, 80 % practice: the lesson never exceeds ten minutes; the rest of a module is work on Shelf.
- If a module's validation fails, the learner repeats the failing part on Shelf, smaller, before the next module
  opens. Modules are not skipped: each produces something the next reuses.
- If an artifact did not constrain the agent in practice, the subject stays `discovered`, whatever its quality.
- A subject the learner already shows in the first module that uses it is recorded and the module's exercise is
  shortened, never the deliverable.
- If Alchemy 2 breaks a module beyond a short fix, fall back for that module to the last working version and
  record it in `docs/research/alchemy.md`; do not switch the whole program to Alchemy 0.x without the learner.
