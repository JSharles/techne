---
id: backend
title: Backend NestJS
version: 1
activity_kinds: code, browser, writing
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=15
red_thread: yes
survey_ceiling: discovered
---

# Backend NestJS

## Outcome and boundary

For a developer who knows JavaScript and TypeScript from the frontend and wants to reach an intermediate
backend level. By the end, the learner builds and operates alone a NestJS service on PostgreSQL and Redis:
a REST API and a small GraphQL API, authentication and authorisation that follow OWASP guidance, background
jobs on a queue, real-time updates over WebSockets, and a notification system that ties the three together.
The service is tested at three levels, packaged with Docker, deployed by a CI pipeline, and observable in
production. The learner can explain and defend each choice in a technical interview.

Activities are of three kinds. Code: exercises in TypeScript, tests provided, run with the project's test
runner; the learner writes every line of implementation. Browser: short quizzes after lessons and for
reviews. Writing: an API design, a security review, a design doc, ADRs.

The placement test (15 minutes) mainly compresses the HTTP and Node runtime units, which the learner may
partly master from frontend work. What was demonstrated in another program does not count here.

Sources, all free: roadmap.sh Backend as the overall skeleton, MDN HTTP, Node.js Learn, the NestJS
documentation, the PostgreSQL documentation and tutorial, Full Stack Open parts 3, 4, 9, 11 and 13 for
practical patterns (transposed from Express to NestJS and from MongoDB to PostgreSQL), the OWASP Cheat
Sheet Series, The Twelve-Factor App, the Docker documentation, the System Design Primer, and roadmap.sh
Backend Projects as isolated exercises.

Deliberately out of scope: Kubernetes and cloud-provider specifics, microservice decomposition in depth,
Kafka operation, and system design beyond a backend developer's needs (a separate, deeper program exists for
that, and this one does not rely on it). MongoDB, Kafka, gRPC, serverless and microservices are surveyed
only.

The program stands alone: a stranger can follow it without any other. It keeps its own evidence.

## Red-thread project

One backend project grows through the whole program, in its own Git repository. Its domain is chosen with
the learner after unit 4 (Git), under one constraint: it must need real-time updates and notifications, for
example something users share and watch change. The domain is never decided before that conversation.

Each unit from unit 5 on lands on the project: REST resources, the PostgreSQL schema and migrations,
authentication, the test suite, Redis cache, background jobs, a WebSocket gateway, the notification system, a
GraphQL endpoint, the Docker Compose stack, the CI pipeline and deployment, and finally a design doc for
scaling it. The project is never ahead of what was taught.

roadmap.sh Backend Projects are used as isolated exercises before a notion lands on the project: the Todo /
Notes API for REST, the URL shortener for SQL and indexes, the authentication API for auth, the caching proxy
for Redis, and the multi-container application for Docker.

Project sessions are bounded at 90 minutes. Work arrives as tickets, written in English on GitHub, like
commits and pull requests. A ticket is done when its tests pass in CI and its pull request is merged.

## Sequence

### Unit 1 — HTTP and the web

- The path of a request: DNS, TCP, TLS, HTTP request and response.
- Methods and their semantics (safe, idempotent), status codes, headers.
- Cookies and their attributes; HTTP caching (Cache-Control, ETag, conditional requests).
- CORS and the preflight request; HTTPS.
- Exercise: inspect and reproduce real exchanges with `curl`; a raw `node:http` server answering correctly.

### Unit 2 — The Node runtime (compressible by placement)

- The event loop and its phases, microtasks, what blocks it.
- ES modules and CommonJS; `package.json`, scripts, TypeScript configuration for Node.
- Errors in async code: rejected promises, unhandled rejections, `try/catch` with `await`.
- Streams and backpressure; the `fs` module; `process`, environment variables, exit codes.

### Unit 3 — NestJS foundations

- TypeScript classes and decorators, as NestJS uses them.
- Modules, controllers, providers; dependency injection and scopes; the request lifecycle.
- Pipes and validation of DTOs; exception filters; guards; interceptors; middleware.
- Configuration from the environment (Twelve-Factor, factor III).
- Exercise: the Todo / Notes API, in memory.

### Unit 4 — Git for a team

- Commits that tell a story; branches; merging and rebasing; resolving a conflict.
- Pull requests and review; commit conventions.
- Red thread: the project's domain is chosen, its repository created, its first tickets written.

### Unit 5 — Designing a REST API

- Resources and URLs, choosing methods and status codes, nested resources.
- Pagination (offset and cursor), filtering, sorting.
- Idempotency keys; versioning; a consistent error format (RFC 9457 problem details).
- OpenAPI with the NestJS Swagger module.
- Writing: the project's API design, reviewed before implementation.

### Unit 6 — SQL with PostgreSQL

- Relational modelling: tables, primary and foreign keys, normal forms, constraints.
- `SELECT`, joins, aggregations, `GROUP BY` and `HAVING`, subqueries and CTEs.
- Transactions and ACID; window functions; views.
- Exercise: the URL shortener's queries in raw SQL.

### Unit 7 — PostgreSQL in depth and Prisma

- Indexes (B-tree, composite, partial, unique) and reading `EXPLAIN ANALYZE`.
- Isolation levels, row locks, `SELECT ... FOR UPDATE`, lost updates.
- Prisma in NestJS: schema, client, relations, transactions; migrations and their review.
- The N+1 problem and how to detect it.
- Red thread: the project's schema and migrations.

### Unit 8 — Authentication and security

- Password storage (Argon2, bcrypt); sessions versus JWT; access and refresh tokens, rotation, revocation.
- Authorisation: roles, ownership checks, broken object-level authorisation.
- Input validation, SQL injection, mass assignment; security headers; rate limiting.
- Secrets management; security logging without leaking data (OWASP).
- Exercise: the authentication API. Writing: a security review of the project.

### Unit 9 — Testing a backend

- Unit tests of services with Jest and test doubles; what to mock and what not to.
- Integration tests on a real PostgreSQL (Testcontainers or a Compose service); isolating test data.
- End-to-end tests of the HTTP API with Supertest.
- Red thread: the project's test suite, run on every pull request.

### Unit 10 — Redis and caching

- Redis data structures and when each fits; TTL and eviction.
- Cache-aside, write-through, invalidation, stampedes.
- Rate limiting and sessions stored in Redis.
- Exercise: the caching proxy. Red thread: a cache on the project's hottest read.

### Unit 11 — Queues and events

- Why a queue: decoupling, smoothing load, slow work out of the request.
- BullMQ in NestJS: producers, workers, retries with backoff, dead-letter handling.
- Idempotent jobs; internal domain events; the transactional outbox pattern.
- Red thread: the project's first background job.

### Unit 12 — Real time

- WebSockets versus polling versus Server-Sent Events.
- NestJS gateways; rooms; authenticating at the handshake with the API's own tokens.
- Running several instances: the Redis adapter, sticky sessions.
- Red thread: live updates in the project.

### Unit 13 — A notification system

- Channels (in-app, email), templates, user preferences.
- Fan-out through the queue; delivery status, retries and deduplication.
- In-app delivery over the WebSocket gateway; unread counts.
- Red thread: the project's notification system, built from units 10, 11 and 12.

### Unit 14 — GraphQL, light

- Schema, queries, mutations, subscriptions; code-first resolvers in NestJS.
- The N+1 problem in resolvers and DataLoader; authorisation in resolvers.
- When to choose GraphQL over REST.
- Red thread: one read-heavy part of the project exposed in GraphQL.

### Unit 15 — Docker and Compose

- Images, containers, layers; a multi-stage Dockerfile for NestJS.
- Compose: the service, PostgreSQL and Redis, volumes, networks, healthchecks.
- Image security: non-root user, minimal base, no secrets in layers.
- Exercise: the multi-container application. Red thread: the project runs with one command.

### Unit 16 — CI/CD, deployment and observability

- GitHub Actions: lint, type-check, tests with services, image build.
- Deployment to a free host; migrations during deployment; environments (Twelve-Factor).
- Structured logs, health checks, basic metrics; graceful shutdown.
- Red thread: the project deployed by its pipeline.

### Unit 17 — System design for a backend developer

- Stateless services and horizontal scaling; load balancing.
- Read replicas, connection pooling, cache layers, a queue to absorb load peaks.
- Availability and failure: timeouts, retries, circuit breakers, kept to the essentials.
- Writing: a design doc for scaling the project tenfold, with its ADRs.

## Subject catalogue

### HTTP and the web — `bkhttp.*`

`request-path`, `methods`, `status-codes`, `headers`, `cookies`, `caching`, `cors`, `https`

### Node runtime — `bknode.*`

`event-loop`, `modules`, `async-errors`, `streams`, `filesystem`, `process-env`

### NestJS — `bknest.*`

`decorators`, `modules`, `controllers`, `providers-di`, `lifecycle`, `pipes-validation`, `exception-filters`,
`guards`, `interceptors`, `middleware`, `configuration`

### Git — `bkgit.*`

`commits`, `branches`, `merge-rebase`, `conflicts`, `pull-requests`, `conventions`

### API design — `bkapi.*`

`resources`, `pagination`, `filtering`, `idempotency`, `versioning`, `error-format`, `openapi`

### SQL — `bksql.*`

`modelling`, `constraints`, `select`, `joins`, `aggregations`, `subqueries-cte`, `transactions`,
`window-functions`, `views`

### PostgreSQL and ORM — `bkpg.*`

`indexes`, `explain`, `isolation`, `locking`, `prisma`, `migrations`, `n-plus-one`

### Security — `bksec.*`

`password-storage`, `sessions-jwt`, `refresh-tokens`, `authorisation`, `input-validation`,
`injection`, `security-headers`, `rate-limiting`, `secrets`, `security-logging`

### Testing — `bktest.*`

`unit`, `test-doubles`, `integration-db`, `e2e-http`

### Redis and caching — `bkcache.*`

`redis-structures`, `ttl-eviction`, `cache-aside`, `invalidation`, `stampede`, `redis-rate-limit`

### Queues and events — `bkqueue.*`

`why-queues`, `bullmq`, `retries-backoff`, `dead-letter`, `idempotent-jobs`, `domain-events`, `outbox`

### Real time — `bkrt.*`

`transports`, `gateways`, `rooms`, `handshake-auth`, `multi-instance`, `sse`

### Notifications — `bknotif.*`

`channels`, `preferences`, `fan-out`, `delivery-tracking`, `in-app`

### GraphQL — `bkgql.*`

`schema`, `resolvers`, `subscriptions`, `dataloader`, `resolver-auth`, `graphql-vs-rest`

### Docker — `bkdocker.*`

`images-containers`, `dockerfile`, `compose`, `volumes-networks`, `healthchecks`, `image-security`

### Delivery and operations — `bkops.*`

`ci-pipeline`, `deployment`, `deploy-migrations`, `twelve-factor`, `structured-logs`, `health-metrics`,
`graceful-shutdown`

### System design — `bksd.*`

`stateless-scaling`, `load-balancing`, `read-replicas`, `connection-pooling`, `cache-layers`,
`load-levelling`, `resilience`, `design-doc`

### Survey — `bksurvey.*`

`mongodb`, `kafka`, `grpc`, `serverless`, `microservices`

## Adaptation rules

- A new notion is taught in a 10-minute lesson, checked by a short quiz, practised on an isolated exercise,
  then applied to the project. The project never receives a notion that has not been practised in isolation.
- Units 1 and 2 compress to their unproven subjects when the placement test shows the rest.
- Exercises are one mechanism at a time, with tests provided; the learner writes the implementation.
  Difficulty rises by removing scaffolding, then by combining two earlier mechanisms.
- A subject already demonstrated in this program goes straight to a harder use inside the project.
- Transfer is the unannounced reuse of an earlier mechanism in a later ticket (a cache invalidated by a job,
  a WebSocket authenticated with the API's token). Used correctly without help, it counts as transferred.
- Survey subjects attach to the lessons of neighbouring units and never get a unit of their own.
