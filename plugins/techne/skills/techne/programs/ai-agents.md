---
id: ai-agents
title: AI agent engineering
version: 1
activity_kinds: code, browser
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=0
red_thread: yes
survey_ceiling: discovered
---

# AI agent engineering

## Outcome and boundary

For a developer who has never built anything on top of a large language model. By the end, the learner
designs, builds, evaluates and ships an AI agent on their own, in Python, with FastAPI and LangGraph: a tool
loop, memory and persistence, human approval, retrieval, MCP tools, several cooperating agents, an
evaluation suite, tracing, security guardrails and a production deployment. The learner can explain and
defend each choice in an "AI engineer" technical interview.

The target is operational competence, not research. Training models, fine-tuning, and the mathematics of
transformers stay out of scope; the model is a component the learner calls, measures and constrains.

Starting point, declared and not observed: a working developer, strongest in TypeScript, who has never called
an LLM API or written a tool-calling loop. There is no placement test: everything is taught from the start.
Python is taught here as a second language for a TypeScript developer, so the program stands alone.

Stack: Python with `uv`, Pydantic, FastAPI, LangChain's chat model layer, LangGraph, pytest. Model provider:
Anthropic's Claude API. LangGraph is the program's spine: the learner writes one agent loop by hand to see
what the framework hides, then moves to LangGraph as early as possible and stays there.

Budget: about 10 euros of API credit for the whole program. This shapes the method:

- the cheapest current Claude model (Haiku class) is the default for every exercise and for the project;
  a larger model is used only where a lesson is about choosing one, and briefly;
- a spend limit is set in the Claude Console before the first API call, and every script caps `max_tokens`;
- tests never call the real API: they use LangChain's fake chat models or recorded responses, so running a
  test suite costs nothing;
- graph logic is developed against a fake model or a local model through Ollama, and the real model is
  called only to check the final behaviour;
- prompt caching is taught early, because it is also how the budget lasts;
- tracing uses LangSmith's free developer tier, and evaluation datasets stay small.

Activities are of two kinds. Code: exercises in the editor, each checked by tests the learner runs; the
learner writes every line. Browser: short quizzes after lessons and for reviews.

Sources, all free: the Anthropic documentation (Messages API, tool use, prompt caching, building effective
agents), the LangChain and LangGraph documentation and LangChain Academy's free LangGraph course, the
FastAPI documentation, the Model Context Protocol specification and SDK documentation, the Pydantic
documentation, the LangSmith documentation, and the OWASP Top 10 for LLM Applications.

Deliberately out of scope: fine-tuning and training, building a model provider, frontend work beyond a
plain HTTP client, and certification. Other agent frameworks and SDKs, agent-to-agent protocols, computer use
and voice agents are surveyed only.

The program stands alone: a stranger can follow it without any other. It keeps its own evidence.

## Red-thread project

One agent is built across the whole program, in its own Git repository, in Python with FastAPI and
LangGraph. It is chosen with the learner after the units on calling a model and on the tool loop, so that
the choice is informed: a useful agent the learner would actually run, with at least two real tools, data
it must look up, and an action that deserves human approval. Techne never writes the agent.

From the LangGraph unit on, each unit lands on the project: the graph, the HTTP API, memory and threads, the
approval step, retrieval, MCP tools, the multi-agent split, the evaluation suite, tracing and guardrails,
and finally the deployment. The project is never ahead of what was taught.

Project sessions are bounded at 90 minutes. Work arrives as tickets, written in English, like commits and
pull requests. A ticket is done when its tests pass, without calling the real API, and its pull request is
merged.

## Sequence

### Unit 1 — Python for a TypeScript developer

- `uv`, virtual environments, project layout, running a script and a module.
- Types, collections, comprehensions, functions and keyword arguments; type hints and what they do not
  enforce at runtime.
- Classes, dataclasses and Pydantic models; validation at the boundary.
- `async` and `await` in Python compared with JavaScript; `asyncio.gather`.
- Exceptions; context managers; environment variables and secrets kept out of the repository.
- pytest: tests, fixtures, parametrisation, async tests.
- Exercise: a small typed module with Pydantic models and its pytest suite.

### Unit 2 — Calling a model

- What an LLM call is: messages, roles, the system prompt, tokens, the context window, `max_tokens`.
- The Anthropic Messages API in Python; reading usage and computing the cost of a call.
- Setting a spend limit before the first call; choosing a model by price, speed and capability.
- Temperature and determinism; why the same prompt can answer differently.
- Prompt design for an agent: role, instructions, examples, output format.
- Structured output with Pydantic; validating and retrying a malformed answer.
- Streaming; prompt caching and what it saves.
- Exercise: a script that extracts a typed object from free text, with its cost printed per call.

### Unit 3 — Tool calling and the agent loop by hand

- What a tool is for a model: a name, a description, a JSON schema.
- The tool-use round trip: the model asks, the code runs the tool, the result goes back.
- The agent loop: repeat until the model stops asking for tools; stop conditions and an iteration cap.
- Tool errors returned to the model instead of raised; parallel tool calls.
- Workflows versus agents: when a fixed chain beats a loop.
- Exercise: a two-tool agent loop written without any framework, tested with a fake model.
- Red thread: the project is chosen and its first tickets are written.

### Unit 4 — LangGraph foundations

- LangChain chat models and tool binding, as much as LangGraph needs.
- `StateGraph`: state as a typed dict, nodes as functions, edges, `START` and `END`.
- Conditional edges and routing; reducers and how a node's return merges into the state.
- `ToolNode` and `tools_condition`; the prebuilt ReAct agent and what it builds.
- Compiling, invoking and streaming a graph; drawing it; the recursion limit.
- Testing a graph with a fake chat model.
- Exercise: the hand-written loop of the previous unit rebuilt as a graph.
- Red thread: the project's first graph, with its tools.

### Unit 5 — Serving an agent with FastAPI

- Routes, path and query parameters, request and response models with Pydantic.
- Dependency injection for the model, the graph and settings.
- Async endpoints; streaming the agent's output with server-sent events.
- Errors, timeouts and cancellation when a model call is slow.
- Testing endpoints with the test client and a fake model.
- Red thread: the agent reachable over HTTP, streaming its answer.

### Unit 6 — Memory and persistence

- Short-term memory: checkpointers, threads, resuming a conversation.
- Persisting checkpoints in SQLite, then PostgreSQL.
- Managing the context window: trimming, summarising, keeping what matters.
- Long-term memory across threads with a store; what to remember and what to forget.
- Red thread: conversations survive a restart, and the agent remembers the user across threads.

### Unit 7 — Human in the loop and control

- Interrupts: pausing a graph before a sensitive tool, resuming with a decision.
- Approving, editing or rejecting a tool call; `Command` to resume and to route.
- Inspecting and replaying state: history, time travel, forking.
- Red thread: the project's risky action waits for a human approval exposed by the API.

### Unit 8 — Retrieval for agents

- Embeddings and similarity; chunking documents; metadata.
- A vector store, local first (Chroma or pgvector); indexing and querying.
- Retrieval as a tool the agent decides to call; agentic RAG with query rewriting and grading.
- Citing sources; what to do when nothing relevant is found.
- Red thread: the agent looks up the project's own data before answering.

### Unit 9 — Model Context Protocol

- What MCP standardises: servers, clients, tools, resources, prompts; transports.
- Writing an MCP server in Python and testing it with the inspector.
- Consuming MCP tools from a LangGraph agent with the LangChain MCP adapters.
- Trust: what an MCP server can do on the agent's behalf.
- Red thread: one of the project's tools moved behind an MCP server.

### Unit 10 — Multi-agent patterns

- Subgraphs and how state passes in and out.
- Router, supervisor and handoffs; a team of specialised agents.
- Plan-and-execute; reflection and self-critique; map-reduce over many items.
- When several agents cost more than they bring: latency, tokens, debugging.
- Red thread: the project split into at least two cooperating agents, or a written decision not to.

### Unit 11 — Evaluating agents

- Why tests alone are not enough; a dataset of inputs and expected behaviour.
- Deterministic checks first, then LLM-as-judge with a rubric, and its own biases.
- Evaluating the final answer, a single step, and the whole trajectory of tool calls.
- Regression runs before each change; comparing two prompts or two models on the same dataset.
- Red thread: an evaluation suite that runs before every merge, on a small budget.

### Unit 12 — Observability, security and guardrails

- Tracing every run with LangSmith; reading a trace to find a wrong decision.
- Cost and latency per run; budgets enforced in code.
- Prompt injection, direct and through tool results; data exfiltration through tools.
- Least privilege for tools; input and output validation; refusing out-of-scope requests.
- Red thread: traces on, a spend cap in code, and an injection test in the suite.

### Unit 13 — Shipping an agent

- Configuration and secrets per environment; a Docker image for the API.
- Retries with backoff, rate limits, fallback to another model, idempotent tools.
- Running long tasks in the background; durable execution and resuming after a crash.
- Deploying on a free tier, or keeping it local when no free tier fits.
- Red thread: the agent deployed and usable, with a README that explains its design and its limits.

## Subject catalogue

### Python for agents — `agpy.*`

`tooling-uv`, `types-collections`, `functions`, `type-hints`, `classes-dataclasses`, `pydantic`, `async`,
`exceptions`, `context-managers`, `env-secrets`, `pytest`

### Calling a model — `agllm.*`

`messages-roles`, `tokens-context`, `api-call`, `cost-usage`, `model-choice`, `sampling`, `prompt-design`,
`structured-output`, `streaming`, `prompt-caching`

### The agent loop — `agloop.*`

`tool-schema`, `tool-round-trip`, `agent-loop`, `stop-conditions`, `tool-errors`, `parallel-tools`,
`workflow-vs-agent`

### LangGraph — `aglg.*`

`chat-models`, `state-graph`, `nodes-edges`, `conditional-edges`, `reducers`, `tool-node`, `prebuilt-agent`,
`stream-invoke`, `recursion-limit`, `graph-testing`

### Serving with FastAPI — `agapi.*`

`routes`, `pydantic-io`, `dependencies`, `async-endpoints`, `sse-streaming`, `errors-timeouts`,
`endpoint-testing`

### Memory — `agmem.*`

`checkpointers`, `threads`, `persistent-checkpoints`, `context-trimming`, `summarisation`, `long-term-store`

### Human in the loop — `aghitl.*`

`interrupts`, `approval`, `command`, `state-history`, `time-travel`

### Retrieval — `agrag.*`

`embeddings`, `chunking`, `vector-store`, `retrieval-tool`, `agentic-rag`, `citations`

### MCP — `agmcp.*`

`protocol`, `server`, `inspector`, `client-adapters`, `trust`

### Multi-agent patterns — `agmulti.*`

`subgraphs`, `router`, `supervisor`, `handoffs`, `plan-execute`, `reflection`, `map-reduce`, `trade-offs`

### Evaluation — `ageval.*`

`datasets`, `deterministic-checks`, `llm-judge`, `trajectory-eval`, `regression`, `comparison`

### Observability and security — `agops.*`

`tracing`, `cost-latency`, `prompt-injection`, `tool-permissions`, `guardrails`

### Shipping — `agprod.*`

`config`, `docker`, `retries-fallbacks`, `rate-limits`, `background-runs`, `durable-execution`, `deploy`

### Survey — `agsurvey.*`

`claude-agent-sdk`, `openai-agents-sdk`, `other-frameworks`, `agent-to-agent`, `computer-use`,
`voice-agents`, `fine-tuning`

## Adaptation rules

- No placement test: the learner declared no experience with LLM APIs. Every unit is taught. The Python
  unit compresses on observed work only: a subject the learner shows independently on the first exercise
  moves on without a lesson.
- LangGraph comes as early as possible: the hand-written loop is one exercise, not a unit of several days.
  If the loop is understood on the first attempt, LangGraph opens right after it.
- Every exercise test runs against a fake model or a recorded response. A real API call is a separate,
  announced step with its expected cost, never part of a test run.
- When the remaining API credit falls under a third of the starting amount, project work switches to a local
  model through Ollama for development, and the real model is kept for final checks and evaluation runs.
- A failed subject comes back as a smaller exercise on the same notion, never as the same exercise again.
- Multi-agent, retrieval and MCP are taught on the project's own needs: if the project has no reason for one
  of them, the exercise still runs, and the project records why it does not use it.
- Survey subjects stop at discovered: one short lesson and a quiz, no exercise.
