---
id: system-design
title: System design and software architecture
version: 1
activity_kinds: writing, browser, code, oral
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=0
red_thread: yes
survey_ceiling: discovered
---

# System design and software architecture

## Outcome and boundary

For a developer who starts from zero in system design and wants two things, in this order: pass the system
design rounds of technical interviews, then work as someone who can design, evaluate and document a real
architecture. By the end, the learner takes an unseen problem ("design a ticketing platform", "design a
chat"), clarifies requirements, estimates load, draws a high-level design, deepens the critical components,
names the trade-offs and failure modes, and writes it down as a design doc with ADRs. Later units go past the
interview: operating a system in production (SLOs, overload, cascading failures), architecture styles and
microservice patterns, and evaluating an architecture against quality attributes.

The learner declared being a complete beginner on 2026-10-02. The program therefore runs no placement test
and teaches every subject from its basics; a subject the learner already masters is compressed by the
adaptation rules, not skipped up front.

Activities are of four kinds. Writing: design docs, ADRs, estimations, written answers to design questions.
Browser: short quizzes after lessons and for reviews. Oral: interview simulations, written out in a file
(what the learner would say aloud), never asked in the chat. Code: small TypeScript labs run with
`node --test`, where the learner builds the mechanism by hand to understand it — an LRU cache, a rate
limiter, consistent hashing, a quorum read, an idempotent handler, a transactional outbox, a circuit breaker.

Only free sources are used. Cloud-specific material (Azure, AWS) is taken for its generic concepts and
patterns; no cloud account is needed and no service is deployed.

Deliberately out of scope: operating real infrastructure (Kubernetes, Terraform, a cloud account), deep
security engineering beyond authentication, authorisation and transport security, formal verification of
distributed protocols (TLA+), and vendor certification content. Some subjects are surveyed only (see the
Survey domain).

The program stands alone: a stranger can follow it without any other. It keeps its own evidence; what was
demonstrated in another program does not count here.

## Red-thread project

The learner designs one system through the whole program: **Billetterie**, a ticketing platform for concerts
and events. Users browse events, hold seats for a few minutes, pay, and receive a ticket; organisers publish
events and follow sales. The domain was chosen because it exercises nearly every unit: read-heavy browsing
(cache, CDN), write contention on the same seat (transactions, consistency, no double booking), flash sales
when a popular event opens (load, queues, rate limiting, overload), payment across services (Saga,
idempotency, outbox), notifications (messaging), and a strict availability need on sale day (SLOs, failover).

The project is a design, not a deployed product. It lives in one design doc in the workspace, `billetterie/`,
with an `adr/` folder. Each unit adds or revises a section: requirements and estimations, API, data model,
caching, scaling, replication and partitioning, consistency choices, messaging, reliability, SLOs and
monitoring, module boundaries, service decomposition, and finally a quality-attribute evaluation of the
whole design in the style of ATAM. When a lab's mechanism belongs to the project (seat hold expiry, the
payment outbox), the learner codes a minimal version of it in TypeScript inside `billetterie/labs/`.

Project sessions are bounded at 90 minutes. A section is done when it states its decisions, the
alternatives rejected and why, and at least one failure scenario with its handling.

## Sequence

### Unit 1 — The method and back-of-the-envelope estimation

- What system design is, and what an interviewer evaluates; functional and non-functional requirements.
- The interview framework: clarify, estimate, define the API, high-level design, deep dive, bottlenecks and
  trade-offs. Used on every exercise from here on.
- Latency numbers every programmer should know; powers of two; estimating QPS, storage, bandwidth and
  memory from user counts.
- Red thread: Billetterie's requirements and its estimations.

### Unit 2 — Networking fundamentals

- The path of a request: DNS resolution, TCP connection, TLS handshake, HTTP request and response.
- TCP versus UDP; the OSI and TCP/IP layers, kept to what a designer needs.
- HTTP/1.1, HTTP/2, HTTP/3 and what each changes (keep-alive, multiplexing, QUIC).
- DNS in depth: records, TTL, DNS-based routing. CDNs: push and pull, what to cache at the edge.
- Proxies: forward and reverse proxy, API gateway.

### Unit 3 — APIs and protocols

- REST: resources, verbs, status codes, versioning, pagination (offset and cursor).
- GraphQL and gRPC: what they solve, what they cost, when to choose each.
- Real-time: short polling, long polling, Server-Sent Events, WebSocket.
- Idempotency keys and safe retries; rate limiting algorithms (token bucket, leaky bucket, sliding window).
- Authentication and authorisation for APIs: sessions, tokens, JWT, OAuth 2.0 and OpenID Connect, API keys.
- Lab: a token-bucket rate limiter. Red thread: Billetterie's public API.

### Unit 4 — Databases

- Relational model, normalisation and denormalisation; SQL versus NoSQL families (key-value, document,
  wide-column, graph) and how to choose.
- Indexes; storage engines: B-tree versus LSM-tree, and what each favours.
- Transactions, ACID, isolation levels and their anomalies (dirty read, lost update, write skew); locking
  and optimistic concurrency.
- Object storage for files and media; full-text search engines and inverted indexes.
- Red thread: Billetterie's data model and how a seat is never sold twice.

### Unit 5 — Caching

- Where caches live: client, CDN, reverse proxy, application, database.
- Strategies: cache-aside, read-through, write-through, write-behind, refresh-ahead.
- Eviction policies (LRU, LFU, TTL); invalidation; cache stampede and hot keys.
- Lab: an LRU cache with TTL. Red thread: what Billetterie caches, and for how long.

### Unit 6 — Scalability and load balancing

- Performance versus scalability; latency versus throughput; percentiles (p50, p99) and tail latency.
- Vertical and horizontal scaling; stateless services and where state goes.
- Load balancers: L4 versus L7, algorithms (round robin, least connections, hashing), health checks,
  active-passive and active-active.
- Unique ID generation at scale (UUID, Snowflake-style IDs).
- First full design exercise: a URL shortener. Red thread: Billetterie's scaled high-level design.

### Unit 7 — Replication and partitioning

- Why replicate; leader-follower, multi-leader, leaderless; synchronous versus asynchronous replication.
- Replication lag and the guarantees it breaks (read-your-writes, monotonic reads).
- Partitioning by key range and by hash; consistent hashing; secondary indexes across partitions;
  rebalancing; hot partitions.
- Lab: consistent hashing with virtual nodes. Design exercise: a key-value store.
- Red thread: replicating and partitioning Billetterie's data.

### Unit 8 — Consistency and distributed systems

- The fallacies of distributed computing; partial failure; timeouts as the only failure detector.
- CAP and PACELC, read precisely; strong, eventual, causal consistency; linearizability.
- Quorums (N, R, W); conflict resolution, last-write-wins, vector clocks, CRDTs as a notion.
- Clocks: physical clocks and their drift, logical and Lamport clocks.
- Consensus: what it solves, leader election, Raft at the level of its rules; distributed locks and fencing
  tokens; the role of ZooKeeper and etcd.
- Lab: quorum reads and writes over simulated replicas. Red thread: Billetterie's consistency choices, per
  operation.

### Unit 9 — Messaging and event-driven architecture

- Why asynchronous: decoupling, load levelling, back pressure.
- Message queues versus pub/sub versus log-based streams (Kafka): ordering, partitions, consumer groups,
  retention.
- Delivery semantics: at-most-once, at-least-once, effectively-once through idempotent consumers;
  dead-letter queues; poison messages.
- Event-driven architecture: event notification, event-carried state transfer; choreography.
- Lab: an idempotent consumer with a dedup store. Design exercise: a notification system.
- Red thread: Billetterie's asynchronous flows (confirmation, tickets, waiting room).

### Unit 10 — Reliability and fault tolerance

- Availability in nines and its arithmetic in series and in parallel; failover active-passive and
  active-active; redundancy across zones and regions; RPO and RTO.
- Resilience patterns: timeouts, retries with exponential backoff and jitter, circuit breaker, bulkhead,
  fallback, graceful degradation.
- Handling overload: load shedding, admission control, queue limits; cascading failures and how they
  propagate.
- Data integrity: backups, restores, and why an untested backup is not a backup.
- Lab: a circuit breaker. Design exercise: a news feed. Red thread: Billetterie on the day a sale opens.

### Unit 11 — Observability and SRE practice

- Metrics, logs, traces; the four golden signals; RED and USE methods.
- SLI, SLO, SLA, error budgets, and implementing an SLO from a user journey.
- Alerting on symptoms and burn rate rather than causes; on-call and toil as notions.
- Release safety: canary releases, progressive rollout, feature flags, configuration as a risk.
- Non-abstract large system design: turning a design into machine counts and capacity.
- Design exercise: a chat system, ending with its SLOs. Red thread: Billetterie's SLOs and dashboards.
- From here, every full design exercise is run as a timed interview simulation.

### Unit 12 — Software architecture foundations

- What architecture is: the decisions that are hard to change; architecture versus design.
- Modularity, cohesion and coupling; information hiding; dependency direction.
- Architecture styles: layered, hexagonal (ports and adapters), modular monolith, event-driven,
  microservices, serverless as a notion; their trade-offs.
- Evolutionary architecture and fitness functions; technical debt as a design decision.
- Architecture Decision Records: when to write one, what goes in it.
- Red thread: Billetterie as a modular monolith, with its first ADRs.

### Unit 13 — Microservices and distributed data patterns

- Monolith versus microservices, and when not to split; decomposition by business capability and by
  subdomain (bounded contexts).
- Database per service and its consequences; API composition; API gateway and backend-for-frontend.
- Saga (orchestration and choreography) and compensating actions; transactional outbox; CQRS; Event Sourcing.
- Migrating a legacy system: strangler fig, anti-corruption layer.
- Deployment and resilience patterns at service level; service discovery.
- Lab: a transactional outbox. Red thread: splitting Billetterie, and its payment Saga.

### Unit 14 — Evaluating and documenting an architecture

- Quality attributes (performance, availability, modifiability, security, testability, usability…) and
  quality attribute scenarios.
- Well-Architected pillars as an evaluation grid: operational excellence, security, reliability,
  performance efficiency, cost optimisation, sustainability.
- Cloud design patterns and anti-patterns as a catalogue; technology selection.
- ATAM: utility tree, sensitivity points, trade-off points, risks.
- Documenting an architecture: views and beyond, the C4 model, the design doc.
- Red thread: the ATAM-style evaluation of Billetterie.

### Unit 15 — Case studies and foundational papers

- AOSA case studies, read for their components, interactions, decisions and problems met.
- Foundational papers, read for the problem they solve and the trade-off they make: Dynamo, GFS,
  MapReduce, Bigtable, Spanner, Kafka, ZooKeeper, Raft.
- Engineering articles from real companies, read with the same grid.
- Capstone: an unseen full design, timed, written as a design doc with ADRs.

## Subject catalogue

### Method and estimation — `sdmeth.*`

`requirements`, `interview-framework`, `latency-numbers`, `back-of-envelope`, `high-level-design`,
`deep-dive`, `trade-off-reasoning`

### Networking — `sdnet.*`

`request-path`, `tcp-udp`, `http-versions`, `tls`, `dns`, `cdn`, `proxies`, `api-gateway`

### APIs and protocols — `sdapi.*`

`rest`, `pagination`, `graphql`, `grpc`, `realtime-transports`, `idempotency`, `rate-limiting`,
`authentication`, `authorisation`

### Databases — `sddb.*`

`relational-model`, `sql-vs-nosql`, `indexes`, `storage-engines`, `transactions-acid`, `isolation-levels`,
`concurrency-control`, `object-storage`, `search-engines`

### Caching — `sdcache.*`

`cache-layers`, `cache-strategies`, `eviction`, `invalidation`, `stampede-hot-keys`

### Scalability and load balancing — `sdscale.*`

`latency-throughput`, `percentiles`, `vertical-horizontal`, `statelessness`, `load-balancers`,
`lb-algorithms`, `unique-ids`

### Replication and partitioning — `sdrepl.*`

`replication-topologies`, `sync-async-replication`, `replication-lag`, `partitioning`,
`consistent-hashing`, `rebalancing`, `hot-partitions`

### Distributed systems and consistency — `sddist.*`

`partial-failure`, `cap-pacelc`, `consistency-models`, `quorums`, `conflict-resolution`, `clocks`,
`consensus`, `distributed-locks`, `coordination-services`

### Messaging and events — `sdmsg.*`

`async-motivation`, `queues-pubsub-logs`, `kafka-model`, `delivery-semantics`, `idempotent-consumers`,
`dead-letter`, `back-pressure`, `event-driven-styles`

### Reliability — `sdrel.*`

`availability-math`, `failover-redundancy`, `rpo-rto`, `timeouts-retries`, `circuit-breaker`, `bulkhead`,
`graceful-degradation`, `overload`, `cascading-failures`, `backups-integrity`

### Observability and SRE — `sdobs.*`

`telemetry`, `golden-signals`, `sli-slo-sla`, `error-budgets`, `alerting`, `canary-releases`,
`configuration-risk`, `capacity-planning`

### Software architecture — `sdarch.*`

`architecture-definition`, `modularity-coupling`, `architecture-styles`, `hexagonal`, `modular-monolith`,
`evolutionary-architecture`, `adr`

### Microservices and distributed patterns — `sdms.*`

`monolith-vs-microservices`, `decomposition`, `database-per-service`, `api-composition`, `bff`, `saga`,
`outbox`, `cqrs`, `event-sourcing`, `strangler-fig`, `service-discovery`

### Architecture evaluation and documentation — `sdeval.*`

`quality-attributes`, `qa-scenarios`, `well-architected`, `cloud-design-patterns`, `technology-selection`,
`atam`, `c4-model`, `design-doc`

### Case studies and full designs — `sdcase.*`

`reading-case-studies`, `dynamo`, `gfs-mapreduce`, `bigtable-spanner`, `kafka-paper`, `zookeeper-raft`,
`url-shortener`, `key-value-store`, `notification-system`, `news-feed`, `chat-system`, `capstone`

### Survey — `sdsurvey.*`

`service-mesh`, `serverless`, `crdts`, `geo-distribution`, `sustainability`, `cost-modelling`,
`data-pipelines`

## Sources

Taken in this order of priority. All are free.

| Source | Role |
| --- | --- |
| https://github.com/donnemartin/system-design-primer | spine of units 1 to 10; full design exercises and their solutions |
| https://github.com/ByteByteGoHq/system-design-101 | intuitive introductions before each lesson, especially networking, APIs, databases, caching |
| https://sre.google/sre-book/table-of-contents/ | units 10 and 11: SLOs, monitoring, overload, cascading failures, consensus, data integrity |
| https://sre.google/workbook/table-of-contents/ | units 10 and 11 in practice: implementing SLOs, alerting, canaries, non-abstract design |
| https://martinfowler.com/architecture/ | unit 12 and part of 13: modularity, coupling, evolutionary architecture, migration |
| https://microservices.io/patterns/ | unit 13: decomposition, Saga, CQRS, Event Sourcing, outbox, API composition |
| https://aosabook.org/ | unit 15 case studies |
| https://learn.microsoft.com/en-us/azure/architecture/ | architecture styles, cloud design patterns, anti-patterns (generic concepts only) |
| https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | unit 14: the evaluation grid |
| https://www.sei.cmu.edu/library/software-architecture-publications/ | unit 14: quality attributes, ATAM, documentation |
| https://github.com/ashishps1/awesome-system-design-resources | index of further reading, engineering articles and papers for every unit |

## Adaptation rules

- Every unit opens with a lesson that introduces its concepts intuitively, then a quiz, then written or
  coded practice. A full design exercise is only opened once the units it depends on have been taught.
- Every design answer, from unit 1 on, follows the interview framework and ends with its trade-offs and at
  least one failure scenario. An answer without trade-offs is not complete.
- Labs are small: one mechanism, one file, tests provided. The learner writes the implementation.
- Interview simulations are written in a file, in the order the learner would speak, under a timebox
  (45 minutes). From unit 11 on, every full design exercise is a simulation.
- A subject already demonstrated in this program goes straight to a harder design that uses it.
- Transfer is the unannounced reuse: a mechanism from an earlier unit is needed in a later design without
  being named. Used correctly without help, it counts as transferred.
- The red thread advances after each unit, with the section that unit enables; it is never ahead of what
  was taught.
- Survey subjects attach to the lessons of neighbouring units and never get a unit of their own.
