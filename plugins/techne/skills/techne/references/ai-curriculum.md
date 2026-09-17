# Afternoon Applied AI curriculum

## Outcome and boundary

The afternoon is a guided twelve-week curriculum that takes an experienced TypeScript developer to building, evaluating, and shipping LLM applications in Python. It is independent from the morning Senior Engineer curriculum in content, pace, evidence, and scheduling; both follow the same method ([pedagogy.md](pedagogy.md), [exercises.md](exercises.md)): a short lesson, then practice, easy first.

The target is operational competence: the learner can design, build, evaluate, and operate a realistic LLM application and explain its trade-offs. It is not research-level machine learning; model training and fine-tuning stay out of scope.

Priority lanes:

1. Python and FastAPI foundations;
2. LLM application fundamentals: prompts, structured outputs, tool calling;
3. retrieval and RAG with LangChain;
4. agents and stateful workflows with LangGraph;
5. evaluation, observability, and production with LangSmith.

## The AI lab

All afternoon practice happens in one Python repository, `ai-lab/` inside the learning workspace, that grows week after week. Each unit adds a feature or a small service to it, so later units reuse earlier work and the capstone starts from real code. Record its path and the provider setup in `.techne/AI_LAB.md`.

Guidance fades over the twelve weeks:

- weeks 1–4: a lesson, then small guided steps with tests provided;
- weeks 5–10: a lesson, then a feature described by its outcome and acceptance tests; the learner designs the implementation;
- weeks 11–12: an autonomous capstone with milestones only.

## Start of the track

On the first afternoon:

1. Check Python 3.12+, `uv`, and Docker; name anything missing and install it only with the learner's consent.
2. Set up model access. Ask which provider the learner wants to use (for example Anthropic or OpenAI) and have them put the API key in `ai-lab/.env` themselves; make sure `.env` is git-ignored, and never print, log, or store the key elsewhere. Offer a local model through Ollama when the learner has no key or wants zero cost, and state the quality trade-off. Tell the learner that exercises make paid API calls and keep them cheap: small models by default, short inputs.
3. Run a short placement test for this track, climbing from easy as in [initialization.md](initialization.md#placement-test): Python basics, HTTP APIs, and one LLM concept question. It sets the starting point inside weeks 1–4.

## Sequence

### Weeks 1–2 — Python for a TypeScript developer

- Language: syntax, truthiness, collections, comprehensions, functions, closures, modules and packages, exceptions, context managers, iterators and generators, decorators.
- Types: type hints, `TypedDict`, `Protocol`, generics, `dataclasses`, Pydantic models and validation; static checking with Pyright or mypy.
- Async: `async`/`await`, the event loop, `asyncio.gather`, timeouts, compared with JavaScript promises.
- Tooling: `uv`, virtual environments, `pyproject.toml`, Ruff, pytest and fixtures.
- Lab: a typed, tested command-line tool that reads real files and validates their content with Pydantic.

Exit evidence: idiomatic, typed Python written without translating TypeScript line by line; async code explained; tests written unaided.

### Weeks 3–4 — LLM fundamentals and FastAPI

- LLM model: tokens, context window, sampling and temperature, system and user messages, non-determinism, cost and latency.
- Provider SDK: calls, streaming, retries and rate limits, error handling.
- Prompting: clear instructions, examples, delimiting untrusted input, prompt templates kept in code.
- Structured outputs: JSON schema and Pydantic, validation and repair, when to reject.
- Tool calling: tool schemas, the call-execute-respond loop, validating tool arguments.
- FastAPI: routes, Pydantic request and response models, dependency injection, async endpoints, error handling, streaming responses, OpenAPI, tests with `TestClient`.
- Persistence: SQLModel or SQLAlchemy with SQLite, then PostgreSQL.
- Lab: an API that extracts structured data from documents with an LLM, validates it, stores it, and exposes it.

Exit evidence: a typed FastAPI service with an LLM call that fails safely on invalid model output; cost and latency of a request explained.

### Weeks 5–6 — Retrieval and LangChain

- Embeddings: what they capture, similarity measures, model choice, cost.
- Retrieval pipeline: loading, chunking strategies, metadata, vector stores (pgvector), similarity and hybrid search, reranking.
- RAG: grounding, citations, handling "not found", context-window budgeting.
- LangChain: chat models, prompt templates, runnables and composition, retrievers, output parsers, tool integrations; when a direct SDK call is simpler.
- Lab: a question-answering service over a real document set, with citations and a "no answer" path.

Exit evidence: retrieval quality diagnosed from retrieved chunks rather than guessed; a chunking or retrieval change justified by observed results.

### Weeks 7–8 — Agents and workflows with LangGraph

- Agent loop: model, tools, observations, stopping conditions, when not to use an agent.
- LangGraph: state, nodes, edges, conditional routing, reducers, subgraphs.
- Durability: checkpointers, persistence, resuming after failure, thread and memory handling.
- Human in the loop: interrupts, approval steps, editing state.
- Reliability: tool errors, retries, loops and budgets, timeouts.
- Multi-agent patterns only where a single graph is demonstrably insufficient.
- Lab: a multi-step workflow over the lab's documents and tools, with an approval step and resumable state, exposed through FastAPI.

Exit evidence: a graph whose state and branches the learner can draw and defend; a failure mid-run recovered from a checkpoint.

### Weeks 9–10 — Evaluation, observability, and production

- LangSmith: tracing, inspecting runs, datasets, evaluators (exact checks, heuristics, LLM-as-judge and its limits), experiments and comparison, prompt versioning.
- Regression control: an evaluation suite run before merging changes.
- Security: prompt injection, data exfiltration through tools, secrets, least privilege for tools, output handling.
- Cost and latency: model choice, caching, batching, streaming, token budgets.
- Operations: Docker, configuration, health checks, structured logs, rate limiting, deployment to a simple cloud target, monitoring.
- Lab: tracing and an evaluation dataset for the RAG and agent features; a measured improvement; a deployable container.

Exit evidence: a change accepted or rejected from evaluation results; a prompt-injection risk demonstrated and mitigated; cost per request measured.

### Weeks 11–12 — Capstone

A small but real LLM application, built autonomously in the lab from the previous units.

- Choose the problem in one or two afternoons: a recurring problem the learner has or can observe directly, with real or naturally available data. Reject ideas where AI would be decorative.
- Scope it to ship within the two weeks: FastAPI backend, at least one LangChain or LangGraph workflow justified by the problem, LangSmith evaluation, and a React or Next.js interface.
- Run it through milestones (see below), not daily instructions.

Exit evidence: a working application, an evaluation report, and a short case study.

## Milestones and assistance in the capstone

A milestone states the user outcome, an observable definition of done, constraints, the evidence Techne will inspect, and non-goals. Keep the current milestone in `.techne/CURRENT.md`. The learner chooses architecture, implementation order, and pace.

When the learner asks for help, inspect the actual system, state one observed fact, ask one diagnostic question, and increase help one level at a time. Documentation research is part of the work; point to official documentation rather than turning the milestone into a tutorial.

The case study shows the problem, the scope delivered, the architecture and main trade-offs, the evaluation method and results, security, cost, and latency considerations, and what the learner implemented personally versus with assistance. Present it as a learning project, not a validated business.

## Keeping content current

LangChain, LangGraph, LangSmith, and provider SDKs change quickly. Before writing a lesson or exercise that uses their APIs, check the current official documentation and use current, non-deprecated interfaces. Pin package versions in the lab so exercises stay reproducible.

## Adaptation rules

Apply the morning rules in [curriculum.md](curriculum.md#adaptation-rules): every topic starts easy, difficulty moves one step at a time from observed results, and demonstrated material may be compressed while prerequisite order is preserved.
