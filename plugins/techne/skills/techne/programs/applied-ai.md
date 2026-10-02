---
id: applied-ai
title: Applied AI
version: 2
activity_kinds: code, browser
lesson_to_practice: on-demand
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=0
red_thread: yes
survey_ceiling: discovered
---

# Applied AI

## Outcome and boundary

This program takes an experienced TypeScript developer to building, evaluating and shipping LLM applications in Python, by building one. The learner chooses a real application first, and each notion is taught when their project needs it.

The target is operational competence: design, build, evaluate and operate a realistic LLM application, and explain its trade-offs. It is not research-level machine learning; training and fine-tuning stay out of scope.

What the program covers, in the order a project usually needs it:

1. Python and FastAPI foundations;
2. LLM application fundamentals: prompts, structured outputs, tool calling;
3. retrieval and RAG with LangChain;
4. agents and stateful workflows with LangGraph;
5. evaluation, observability, and production with LangSmith.

## The project

The project is chosen and planned before any phase opens, through the ideation and the roadmap of [project.md](../references/project.md). Its frame, which is not open to discussion: Python with FastAPI, one application built across the program, worked on alone, its hard problems placed on the phases below, and no dependency on another program the learner follows.

It lives in its own repository, and `.techne/AI_LAB.md` records that path, the model provider, and where the work stands. Each phase below says what the project must exercise then; the roadmap decides which part of the application does it, and tickets derive from the roadmap one or two ahead.

## How Techne works on this program

The learner builds the product and writes every line of it. Techne holds two roles beside them:

- **product owner**: it finds the project with the learner, writes the roadmap, cuts the work into tickets one or two ahead, and says what each ticket must achieve and what the review will check;
- **lead developer**: it answers design and technical questions, reviews each pull request before it merges, and names what it would do differently and why.

Teaching happens when the learner asks for it. Before work that uses something new, Techne names in one sentence what is new and offers a lesson or a short exercise on it; the learner decides, and asking for one later costs nothing. Techne never opens a lesson they did not ask for, and never turns a ticket into a tutorial.

There is no placement test: the project shows what the learner can already do, and the mastery map is filled from the work itself, as everywhere else in Techne.

## Start of the track

In the program's first session:

1. Check Python 3.12+, `uv`, and Docker; name anything missing and install it only with the learner's consent.
2. Set up model access. Ask which provider the learner wants to use (for example Anthropic or OpenAI) and have them put the API key in the project's `.env` themselves; make sure `.env` is git-ignored, and never print, log, or store the key elsewhere. Offer a local model through Ollama when the learner has no key or wants zero cost, and state the quality trade-off. Tell the learner that exercises make paid API calls and keep them cheap: small models by default, short inputs.
3. Find the project with the learner, then build its roadmap, following [project.md](../references/project.md). No phase opens before the roadmap is committed.

## Sequence

### Weeks 1–2 — Python for a TypeScript developer

- Language: syntax, truthiness, collections, comprehensions, functions, closures, modules and packages, exceptions, context managers, iterators and generators, decorators.
- Types: type hints, `TypedDict`, `Protocol`, generics, `dataclasses`, Pydantic models and validation; static checking with Pyright or mypy.
- Async: `async`/`await`, the event loop, `asyncio.gather`, timeouts, compared with JavaScript promises.
- Tooling: `uv`, virtual environments, `pyproject.toml`, Ruff, pytest and fixtures.
- Project: a typed, tested command-line tool that reads real files and validates their content with Pydantic.

Exit evidence: idiomatic, typed Python written without translating TypeScript line by line; async code explained; tests written unaided.

### Week 3 — A service that calls a model

One week only: HTTP APIs are already the learner's daily work, so this week ports that knowledge to Python and adds the first model calls.

- FastAPI: routes, Pydantic request and response models, dependency injection, async endpoints, error handling, streaming responses, OpenAPI, tests with `TestClient`.
- Persistence: SQLModel or SQLAlchemy with SQLite, then PostgreSQL.
- Model calls: provider SDK, messages, streaming, retries and rate limits, failure handling.
- Structured outputs: JSON schema and Pydantic, validation and repair, when to reject a response.
- Cost and latency: tokens, context window, model choice, measuring a request.
- Project: an API endpoint that turns a document into validated structured data and stores it.

Exit evidence: a typed FastAPI service whose LLM call fails safely on invalid model output; the cost and latency of one request explained.

### Weeks 4–5 — Retrieval and RAG with LangChain

- Prompting: clear instructions, examples, delimiting untrusted input, prompt templates kept in code and versioned.
- Tool calling: tool schemas, the call-execute-respond loop, validating tool arguments.
- Embeddings: what they capture, similarity measures, model choice, cost.
- Retrieval pipeline: loading, chunking strategies, metadata, vector stores (pgvector), similarity and hybrid search, reranking.
- RAG: grounding, citations, handling "not found", context-window budgeting.
- LangChain: chat models, prompt templates, runnables and composition, retrievers, output parsers, tool integrations; when a direct SDK call is simpler.
- Project: a question-answering endpoint over a real document set, with citations and a "no answer" path.

Exit evidence: retrieval quality diagnosed from retrieved chunks rather than guessed; a chunking or retrieval change justified by observed results.

### Weeks 6–8 — Agents and workflows with LangGraph

Three weeks, the densest part of the track.

- Agent loop: model, tools, observations, stopping conditions, and when not to use an agent.
- LangGraph: state, nodes, edges, conditional routing, reducers, subgraphs.
- Durability: checkpointers, persistence, resuming after failure, threads and memory.
- Human in the loop: interrupts, approval steps, editing state.
- Reliability: tool errors, retries, loop and cost budgets, timeouts.
- Multi-agent patterns only where a single graph is demonstrably insufficient.
- Project: a multi-step workflow over the project's documents and tools, with an approval step and resumable state, exposed through FastAPI.

Exit evidence: a graph whose state and branches the learner can draw and defend; a run recovered from a checkpoint after a failure.

### Weeks 9–10 — Evaluation, observability, and production

- LangSmith: tracing, inspecting runs, datasets, evaluators (exact checks, heuristics, LLM-as-judge and its limits), experiments and comparison, prompt versioning.
- Regression control: an evaluation suite run before accepting a change.
- Security: prompt injection, data exfiltration through tools, secrets, least privilege for tools, output handling.
- Cost and latency: model choice, caching, batching, streaming, token budgets.
- Operations: Docker, configuration, health checks, structured logs, rate limiting, deployment to a simple cloud target, monitoring.
- Project: tracing and an evaluation dataset for the RAG and agent features; a measured improvement; a deployable container.

Exit evidence: a change accepted or rejected on evaluation results; a prompt-injection risk demonstrated and mitigated; cost per request measured.

### Weeks 11–12 — Finishing and presenting

The application is finished, deployed, documented and presented, from the roadmap's last phases.

- Run it through milestones, not daily instructions.
- Close what the roadmap left open, or record explicitly what ships unfinished, and why.

Exit evidence: a working application, an evaluation report, and a short case study.

## Subject catalogue

Stable identifiers for the mastery map: every lesson and exercise declares the subjects it teaches or evaluates, and Techne never invents one outside this list.

### Python — `py.*`

`syntax`, `collections`, `comprehensions`, `functions-closures`, `modules-packages`, `exceptions`, `context-managers`, `iterators-generators`, `decorators`, `type-hints`, `protocols-generics`, `dataclasses`, `pydantic`, `static-checking`, `async`, `uv-packaging`, `pytest`

### Services — `svc.*`

`fastapi-routing`, `request-models`, `dependency-injection`, `async-endpoints`, `error-handling`, `streaming`, `openapi`, `api-tests`, `persistence`, `migrations`

### LLM applications — `llm.*`

`tokens-context`, `model-calls`, `streaming-calls`, `retries-rate-limits`, `prompting`, `prompt-versioning`, `structured-outputs`, `output-validation`, `tool-calling`, `cost-latency`

### Retrieval — `rag.*`

`embeddings`, `chunking`, `metadata`, `vector-stores`, `similarity-search`, `hybrid-search`, `reranking`, `grounding-citations`, `no-answer-path`, `context-budgeting`, `langchain-runnables`, `langchain-retrievers`, `when-not-langchain`

### Agents — `agent.*`

`agent-loop`, `when-not-agent`, `graph-state`, `nodes-edges`, `conditional-routing`, `reducers`, `subgraphs`, `checkpointers`, `resumability`, `memory`, `human-in-the-loop`, `tool-errors`, `loop-budgets`, `multi-agent`

### Evaluation and operations — `eval.*`

`tracing`, `datasets`, `heuristic-evaluators`, `llm-as-judge`, `experiments`, `regression-suite`, `prompt-injection`, `tool-least-privilege`, `output-handling`, `caching`, `token-budgets`, `containerization`, `deployment`, `monitoring`

## Milestones and assistance

A milestone states the user outcome, an observable definition of done, constraints, the evidence Techne will inspect, and non-goals. Keep the current milestone in `.techne/CURRENT.md`; it comes from the roadmap. The learner chooses architecture, implementation order, and pace.

When the learner asks for help, inspect the actual system, state one observed fact, ask one diagnostic question, and increase help one level at a time. Documentation research is part of the work; point to official documentation rather than turning the milestone into a tutorial.

The case study shows the problem, the scope delivered, the architecture and main trade-offs, the evaluation method and results, security, cost, and latency considerations, and what the learner implemented personally versus with assistance. Present it as a learning project, not a validated business.

## Keeping content current

LangChain, LangGraph, LangSmith, and provider SDKs change quickly. Before writing a lesson or exercise that uses their APIs, check the current official documentation and use current, non-deprecated interfaces. Pin package versions in the lab so exercises stay reproducible.

## Adaptation rules

Every subject starts easy. Raise the difficulty one step after an unassisted success; lower it one step after a failure, with a short explanation first. Declared experience never sets a level.

- The roadmap decides the order. When a phase of the project needs a notion, its unit opens then, even if the sequence above places it later; the sequence is the default whenever the roadmap is silent.
- A notion the project never needs stays in the catalogue and is offered, not imposed: name it when a phase would have used it, and teach it if the learner wants it. A subject they decline stays `not_started`, and the program says so rather than pretending otherwise.
- Failed recall or repeated assisted work: reduce novelty and schedule a smaller attempt within two sessions.
- Independent success: schedule transfer into the project.
- Survey subjects are grafted onto project work whenever possible, and never expand into a phase of their own.
