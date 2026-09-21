---
id: engineering
title: T-shaped Product Engineer
version: 2
cadence: daily
activity_kinds: code, browser
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=30, review=5, project=90, placement=15
red_thread: yes
survey_ceiling: discovered
---

# T-shaped Product Engineer

## Outcome and boundary

Twelve weeks for one learner profile: a self-taught React/Node developer, bootcamp-trained rather than engineering-school-trained, who wants to stay employable as generative AI reshapes the job market. Goals, in order: be better on a React/Node job, then pass senior interviews, then be able to move roles.

The name is the shape: a deep core carried to independence, and a broad survey of what a product engineer touches around it. Depth beats coverage (see `docs/adr/0002-depth-over-breadth-core-and-survey.md`). Subjects are split in two:

- **Core**, taken to demonstrated independence: TypeScript and JavaScript, React and Next.js, NestJS and backend, SQL and data modelling, DSA up to graphs, tests and debugging, applied architecture, and the delivery flow — Git, pull requests, review, CI (see `docs/adr/0014-the-delivery-flow-joins-the-programme.md`).
- **Survey**, covered for working literacy only and grafted onto core exercises: security, performance, observability, delivery. Distributed systems and large-scale system design get a lesson and a quiz, nothing more.

Out of the programme: maths for engineering, dynamic programming and advanced DSA patterns, Product and communication as separate lanes. Python and the Applied AI frameworks belong to the afternoon curriculum in [Applied AI](applied-ai.md).

Techne controls the order from observed evidence. It may compress demonstrated material or repeat fragile material, but it preserves core coverage and prerequisite order.

## Shape of a week

Six full mornings and one light day (see [pedagogy.md](../references/pedagogy.md#rhythm)):

- **four mornings** of isolated work: one web activity (TypeScript, JavaScript, React, Next.js, or NestJS), one DSA activity, and due reviews;
- **two mornings** on the red-thread project;
- **the light day**: reviews and reading only.

A subject is first learned on an isolated exercise, then reinvested in the red-thread project one or two weeks later. That reinvestment is what earns `transferred` in the mastery map.

## The red-thread project

One Next.js + NestJS + database application, built across the twelve weeks and presentable at the end (see `docs/adr/0003-red-thread-project-as-the-place-of-transfer.md`).

- In week 1, offer two or three simple, concrete domains and let the learner pick one. Keep the domain small enough that no week is spent on business rules.
- Techne sets the milestone for each project morning: the user-visible outcome, the constraints, and what evidence it will inspect. The learner designs and writes the implementation.
- From weeks 3–4, every change reaches the main branch through a pull request the learner opens and Techne reviews, following [operations.md](../references/operations.md#reviewing-a-pull-request).
- Survey subjects are grafted here: structured logs, a latency budget, an authorization boundary, a deployment step, on code the learner wrote.
- From week 9 the project also carries production concerns; in weeks 11–12 it is finished and presented.

## Sequence

### Weeks 1–2 — Foundations and the first slice

- DSA: iteration gestures, hand tracing, arrays, strings, `Map`, `Set`, frequency counting, Big-O intuition.
- TypeScript: inference, widening, narrowing, `unknown`, `never`, discriminated unions, runtime validation, strict configuration.
- JavaScript: values and references, closures, call stack, event loop, promises, errors, modules.
- React: render model, component identity, local and derived state, controlled inputs, effects and their alternatives.
- Tests: what to test, arrange-act-assert, testing behaviour rather than implementation.
- Flow: slicing a ticket into changes small enough to review, one branch per ticket, small commits following a commit convention.
- Red thread: pick the domain, scaffold the app in its own repository, ship one vertical slice with a typed contract, sliced into tickets.

Exit evidence: unfamiliar Easy iteration and hash problems solved independently; a runtime boundary secured with validation; a React state bug diagnosed from behaviour; a feature sliced into tickets and delivered as a readable history.

### Weeks 3–4 — Data, APIs, and frontend depth

- DSA: two pointers, sliding window, stack, queue, binary search, recursion.
- SQL and data modelling: relational modelling, keys, constraints, joins, indexes, query plans, transactions and isolation intuition.
- NestJS: modules, controllers, providers and dependency injection, DTO validation pipes, exception filters, configuration.
- TypeScript: generics with constraints, `keyof`, indexed access, type predicates, domain modelling, public API design.
- React: reconciliation, keys, composition, async UI states, forms, accessibility.
- Flow: opening a pull request a reviewer can follow, reviewing someone else's, merge versus rebase, resolving conflicts by understanding both sides.
- Red thread: real persistence behind the API, with a data model the learner defends; from here every change goes through a pull request.

Exit evidence: a data model defended under constraints; a query investigated with a query plan; a NestJS endpoint that validates and fails correctly; a pull request reviewed with its real defects found; a conflict resolved without losing either side's intent.

### Weeks 5–6 — Next.js, deeper backend, and structures

- DSA: linked structures where useful, trees, BSTs, heaps.
- Next.js: App Router, layouts, Server and Client Components, request boundaries, error and loading states, data fetching, caching and invalidation, rendering strategies.
- NestJS: authentication vs authorization with guards, interceptors, error taxonomy, unit and e2e tests with the Nest testing module.
- Testing: unit, integration, contract and end-to-end boundaries; test doubles and failure-focused cases.
- Debugging: reproducing, bisecting, reading stack traces, the VS Code debugger, logs as evidence.
- Flow: a CI pipeline, written by the learner, that runs lint, type checking and tests on every pull request and blocks the merge when red.
- Red thread: authentication, authorization boundaries, and a test suite that catches regressions before they merge.

Exit evidence: a caching or rendering choice justified with measurements; a multi-file bug diagnosed with the debugger; a tree problem solved without pattern announcement; a regression stopped by the pipeline.

### Weeks 7–8 — Graphs, architecture, and concurrency

- DSA: graph representation, BFS, DFS, topological reasoning.
- Architecture: deep modules, cohesion, coupling, dependency direction, ports and adapters, NestJS modules as boundaries, evolutionary design.
- Concurrency: races, idempotency, retries, cancellation, backpressure, partial failure.
- JavaScript and Node runtime: async reasoning under load, streams where relevant, memory.
- Survey: distributed systems (consistency, delivery semantics, queues, caches) as a lesson and a quiz.
- Flow: recovering history — `revert`, `reset`, `reflog`, finding when a change went wrong.
- Red thread: a refactor that moves a boundary, defended with tests; one asynchronous or failure-prone path made safe.

Exit evidence: a race or partial failure reproduced and protected; an architecture change explained with its alternatives and consequences; a lost or broken step recovered from history without help.

### Weeks 9–10 — Production behaviour

- Survey grafted onto the project: security (hostile input, authorization boundaries, OWASP-relevant risks, secrets), performance (profiling before optimizing, latency budgets, database and frontend bottlenecks), observability (structured logs, metrics, traces, actionable alerts), delivery (containers, deployment, rollback, configuration).
- TypeScript and tooling: ESM/CJS, module resolution, declaration files, builds, compiler diagnosis.
- Next.js production: caching correctness, hydration, bundle and runtime analysis, resilience.
- DSA: mixed retrieval across every pattern learned, under time constraints.
- Red thread: the application is deployed, observable, and measured before and after one optimization.

Exit evidence: a bottleneck measured before and after; a threat modelled and mitigated; a reproducible deployment and rollback.

### Weeks 11–12 — Consolidation and employability

- Cumulative cold recall and reassessment across the core.
- Mixed DSA under interview-like time constraints.
- Cross-layer debugging across browser, frontend, API, and database.
- Survey: bounded system design exercises, defended orally.
- About half of these mornings: mock interviews (timed DSA, technical questions, explaining an architecture decision) and portfolio work on both projects, with a written account of choices and trade-offs.
- Red thread: finished, deployed, documented, and presented.

Exit evidence: an independent problem-solving loop; a design defended orally; an honest mastery map and a prioritized plan for what comes next.

## Subject catalogue

Stable identifiers for the mastery map. Every lesson and exercise declares the subjects it teaches or evaluates; Techne never invents an identifier outside this list. Detail (objectives, misconceptions, reference exercises) is written week by week, not upfront.

### TypeScript — `ts.*`

`inference`, `widening`, `narrowing`, `unknown-never`, `discriminated-unions`, `runtime-validation`, `strict-config`, `generics`, `keyof-indexed`, `type-predicates`, `domain-modelling`, `api-design`, `modules-resolution`, `declaration-files`, `compiler-diagnosis`

### JavaScript and the runtime — `js.*`

`values-references`, `closures`, `call-stack`, `event-loop`, `promises`, `errors`, `modules`, `async-under-load`, `streams`, `memory`

### React — `react.*`

`render-model`, `component-identity`, `state-local-derived`, `controlled-inputs`, `effects-and-alternatives`, `reconciliation-keys`, `composition`, `async-ui-states`, `forms`, `accessibility`, `behaviour-tests`, `render-performance`

### Next.js — `next.*`

`app-router`, `layouts`, `server-client-components`, `request-boundaries`, `error-loading-states`, `data-fetching`, `caching-invalidation`, `rendering-strategies`, `metadata`, `middleware`, `hydration`, `bundle-analysis`, `production-resilience`

### NestJS and backend — `nest.*`

`modules`, `controllers`, `providers-di`, `dto-validation`, `exception-filters`, `configuration`, `guards-authz`, `interceptors`, `error-taxonomy`, `persistence`, `unit-tests`, `e2e-tests`, `module-boundaries`, `health-and-shutdown`

### SQL and data — `sql.*`

`relational-modelling`, `keys-constraints`, `joins`, `indexes`, `query-plans`, `transactions`, `isolation`, `migrations`

### DSA — `dsa.*`

`iteration`, `hand-tracing`, `arrays`, `strings`, `hashing`, `frequency-counting`, `big-o`, `two-pointers`, `sliding-window`, `stack`, `queue`, `binary-search`, `recursion`, `linked-structures`, `trees`, `bst`, `heaps`, `graph-representation`, `bfs`, `dfs`, `topological-order`

### Tests and debugging — `test.*`

`what-to-test`, `behaviour-vs-implementation`, `unit`, `integration`, `contract`, `end-to-end`, `test-doubles`, `failure-cases`, `reproduce`, `bisect`, `stack-traces`, `debugger`, `logs-as-evidence`

### Delivery flow — `flow.*`

`commits`, `branches`, `pull-requests`, `review`, `commit-conventions`, `merge-rebase`, `conflicts`, `history-recovery`, `ci-pipeline`, `ticket-slicing`

### Architecture and concurrency — `arch.*`

`deep-modules`, `cohesion-coupling`, `dependency-direction`, `ports-adapters`, `evolutionary-design`, `races`, `idempotency`, `retries`, `cancellation`, `backpressure`, `partial-failure`

### Survey — `survey.*`

`security-input`, `security-authz`, `secrets`, `profiling`, `latency-budgets`, `db-bottlenecks`, `frontend-bottlenecks`, `structured-logs`, `metrics`, `traces`, `alerts`, `containers`, `deployment-rollback`, `configuration`, `distributed-systems`, `system-design`

Survey subjects never reach `independent` or `transferred` in the mastery map; `discovered` is their ceiling.

## DSA problem bank

Free LeetCode problems to base DSA exercises on, at `https://leetcode.com/problems/<slug>/`. All slugs were verified to exist and not be paid-only on 2026-09-17. Pick by topic and observed level; the bank is a starting point, not an exhaustive list or a fixed order.

| Topic | Easy | Medium |
| --- | --- | --- |
| Arrays, iteration | `move-zeroes`, `majority-element`, `best-time-to-buy-and-sell-stock` | `merge-intervals` |
| Hashing, `Map`/`Set`, frequency counting | `two-sum`, `contains-duplicate`, `valid-anagram`, `first-unique-character-in-a-string` | `group-anagrams`, `top-k-frequent-elements` |
| Strings | `valid-palindrome`, `find-the-index-of-the-first-occurrence-in-a-string` | `longest-substring-without-repeating-characters` |
| Two pointers | `valid-palindrome`, `move-zeroes` | `two-sum-ii-input-array-is-sorted`, `container-with-most-water` |
| Sliding window | `maximum-average-subarray-i` | `minimum-size-subarray-sum`, `longest-substring-without-repeating-characters` |
| Stack, queue | `valid-parentheses`, `implement-queue-using-stacks` | `min-stack`, `daily-temperatures` |
| Binary search | `binary-search`, `sqrtx` | `search-in-rotated-sorted-array` |
| Recursion | `fibonacci-number`, `climbing-stairs` | — |
| Linked lists | `reverse-linked-list`, `merge-two-sorted-lists` | — |
| Trees, BST | `maximum-depth-of-binary-tree`, `invert-binary-tree` | `validate-binary-search-tree`, `lowest-common-ancestor-of-a-binary-search-tree`, `binary-tree-level-order-traversal` |
| Heaps | `kth-largest-element-in-a-stream`, `last-stone-weight` | `kth-largest-element-in-an-array` |
| Graphs, BFS/DFS | — | `number-of-islands`, `clone-graph` |
| Topological order | — | `course-schedule`, `course-schedule-ii` |

## Adaptation rules

Every new subject starts easy. Raise the difficulty one step after an unassisted success; lower it one step after a failure, with a short explanation first. Never start a subject at Medium because of job tenure or declared experience.

- Failed recall or repeated assisted work: reduce novelty and schedule a smaller attempt within two mornings.
- Independent success: schedule transfer into the red-thread project.
- Transferred subject: compress explanation and increase constraints, design, and teaching-back.
- Two activities without usable evidence: reduce scope and improve instrumentation.
- Survey subjects are grafted onto core exercises whenever possible, and never expand into their own week.
