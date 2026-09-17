# Morning Senior Engineer curriculum

## Outcome and boundary

This is an intensive twelve-week ceiling for an experienced developer with a frontend/TypeScript background and uneven fundamentals. Techne controls the order from observed evidence. It may accelerate demonstrated material, repeat fragile material, or substitute an equivalent exercise, but it preserves the domain coverage and prerequisite order.

The morning does not teach Python, FastAPI, LangChain, LangGraph, or LangSmith. Those belong to the independent afternoon studio. The morning may teach general backend, architecture, distributed-systems, mathematics, and Product principles without tying them to the afternoon project's current needs.

Priority lanes:

1. DSA and problem solving;
2. TypeScript and JavaScript depth;
3. React and Next.js depth;
4. CS and mathematics for engineering;
5. backend, data, architecture, production, system design, and Product foundations.

## Sequence

### Weeks 1–2 — Observe the foundations

- DSA: iteration gestures, hand tracing, neutral values, arrays, strings, `Map`, `Set`, frequency counting, Big-O intuition.
- TypeScript: inference, widening, narrowing, `unknown`, `never`, discriminated unions, runtime validation, strict configuration.
- JavaScript: values and references, closures, call stack, event loop, promises, errors, modules.
- React: render model, component identity, local and derived state, controlled inputs, effects and their alternatives.
- CS/math: representations, linear/quadratic/exponential growth, logarithm intuition, stack/heap as useful models.
- Product: problem, user, current alternative, outcome, risky assumption.

Exit evidence: unfamiliar Easy-level iteration and hash problems completed independently; runtime boundary explained and secured; React state/effect bugs diagnosed from behaviour.

### Weeks 3–4 — Patterns and frontend depth

- DSA: two pointers, sliding window, stack, queue, binary search, recursion introduction.
- TypeScript: generics with constraints, `keyof`, indexed access, type predicates, domain modelling, public API design.
- React: reconciliation, keys, composition, async UI states, forms, accessibility, behaviour tests, rendering performance.
- Next.js: App Router, layouts, routing, Server and Client Components, request boundaries, error and loading states.
- Browser/network: DOM events, critical rendering path, HTTP request lifecycle, DNS/TCP/TLS at an engineering level.
- Mathematics: invariants, sets, simple combinatorics and probability only where they improve reasoning.

Exit evidence: pattern choice explained rather than guessed; a React/Next behaviour task debugged with tests; a generic or domain model defended for readability and safety.

### Weeks 5–6 — Data structures, Next.js, backend, and data

- DSA: linked structures where useful, trees, BSTs, heaps, BFS, DFS, graph representation.
- Next.js: data fetching, caching and invalidation, rendering strategies, metadata, middleware when justified, profiling.
- Backend: HTTP API contracts, validation, error taxonomy, authentication vs authorization, modular service boundaries.
- SQL/data: relational modelling, keys, constraints, joins, indexes, query plans, transactions and isolation intuition.
- Testing: unit, integration, contract and end-to-end boundaries; test doubles and failure-focused cases.
- CS: processes, threads, concurrency, memory, file systems and I/O models.

Exit evidence: a data model and API defended under constraints; a query investigated with evidence; a tree or graph problem solved without pattern announcement.

### Weeks 7–8 — Reliability and software architecture

- DSA: topological reasoning, greedy patterns, backtracking, dynamic programming only after prerequisites are demonstrated.
- Concurrency: races, idempotency, retries, cancellation, backpressure and partial failure.
- Architecture: deep modules, cohesion, coupling, boundaries, dependency direction, ports/adapters, domain modelling, evolutionary design.
- Distributed systems: consistency, availability, delivery semantics, clocks, queues, caches and failure modes without empty formalism.
- System design: requirements, estimates, API, data model, data flow, bottlenecks, trade-offs and failure handling.
- Product: discovery evidence, prioritization, instrumentation, adoption and outcome metrics.

Exit evidence: race or partial failure reproduced and protected; architecture choice documented with alternatives and consequences; bounded system design defended orally.

### Weeks 9–10 — Production engineering

- Security: hostile input, authorization boundaries, OWASP-relevant risks, secrets, dependency and supply-chain awareness.
- Performance: profiling before optimization, latency budgets, memory, network, database and frontend bottlenecks.
- Observability: structured logs, metrics, traces, correlation, actionable alerts, SLI/SLO fundamentals.
- Delivery: Linux essentials, processes, containers, CI/CD, deployment strategies, rollback, configuration and cloud fundamentals.
- TypeScript/tooling: ESM/CJS, module resolution, declaration files, monorepos, builds, type tests and compiler diagnosis.
- Next.js production: caching correctness, hydration, bundle and runtime analysis, accessibility and resilience.

Exit evidence: bottleneck measured before/after; threat model produces verified controls; deployment or rollback path is reproducible at available scale.

### Weeks 11–12 — Integration and transfer

- cumulative cold recall and reassessment;
- mixed DSA under interview-like constraints, progressing toward Medium only when Easy patterns are independent;
- cross-layer debugging across browser, frontend, API, SQL, concurrency, and network;
- frontend and backend system-design exercises;
- architecture review of an unfamiliar system;
- Product reasoning under technical and business constraints;
- communication: explain a bug, design, trade-off, incident, and decision to technical and non-technical audiences.

Exit evidence: independent problem-solving loop, defended system design, cross-layer diagnosis, honest mastery matrix, and a prioritized post-Techne plan.

## Adaptation rules

- Score 0–1 or failed recall: reduce novelty and schedule a smaller attempt within two mornings.
- Score 2: provide an analogous attempt without reusing the previous solution.
- Score 3: schedule transfer or debugging.
- Score 4–5: compress explanation and increase design, constraints, and teaching-back.
- Two activities without usable evidence: reduce scope and improve instrumentation.
- Progress toward Medium DSA follows independent Easy evidence, never job tenure.
- Advanced math, framework trivia, and exotic patterns remain outside the core unless a demonstrated prerequisite or target requires them.
