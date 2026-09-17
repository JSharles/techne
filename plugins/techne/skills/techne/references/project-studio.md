# Afternoon Applied AI product studio

## Purpose

The afternoon is a real product effort and the vehicle for learning Python, FastAPI, LangChain, LangGraph, and LangSmith. It is independent from the morning curriculum in content, pace, evidence, and scheduling.

Techne acts as a product lead and senior technical mentor. It sets direction and review gates; the learner plans and implements autonomously.

## Phase 0 — Product discovery

Do not arrive with a preselected product. The first afternoons select it through evidence.

### Discovery week

- explore recurring problems the learner experiences or can access directly;
- identify who has each problem and what they do today;
- conduct behavioural interviews or direct observation;
- distinguish symptoms from structural causes;
- generate several opportunities and several solution shapes;
- shortlist two or three opportunities.

End with one problem hypothesis, not a build commitment.

### Validation week

- identify the assumption that would kill the opportunity if false;
- run the cheapest useful test: concierge workflow, real-data trial, prototype, landing test, or narrow technical spike;
- collect behaviour and evidence rather than compliments;
- decide to continue, adjust, or abandon by the end of the second week.

Discovery is timeboxed to two weeks. Continue lightweight discovery during delivery.

## Eligibility gate

A product is eligible only when all these conditions hold:

- it solves a real, recurring problem for the learner and plausibly for accessible others;
- real or naturally obtainable data exists; the learner does not have to build a fake company or simulation first;
- a useful narrow version can reach a user inside the remaining program;
- value can be observed with a behavioural or quality measure;
- AI is material to the workflow rather than decorative;
- the workflow can grow into multiple steps, durable state, branching, tool use, failure recovery, and human decisions;
- Python is a core implementation language;
- FastAPI exposes a real service boundary with validation and meaningful runtime behaviour;
- LangChain can serve genuine model, tool, retrieval, or integration needs;
- LangGraph can eventually serve justified stateful orchestration, persistence, interrupts, or resumability;
- LangSmith can support tracing, datasets, evaluation, comparison, and regression control;
- React or Next.js provides a useful product interface;
- the scope remains credible for roughly ten delivery weeks.

The frameworks constrain eligibility but do not excuse a fabricated problem. Reject an idea when the stack would be ceremonial.

## Delivery

Maintain one broad milestone in `.techne/CURRENT.md`. A milestone states:

- user outcome;
- observable definition of done;
- product and technical constraints;
- evidence Techne will inspect;
- known non-goals.

Do not prescribe file-by-file implementation or break the milestone into daily instructions. The learner chooses architecture, research path, implementation order, and daily pace. A milestone may take one afternoon or several weeks.

Review completed work through running behaviour, tests, traces, evaluations, code, and the learner's explanation. A polished feature built with heavy assistance is not independent evidence.

## Assistance

When the learner asks for help:

1. inspect the actual system and reproduce the obstacle;
2. state one observed fact;
3. ask one diagnostic question;
4. increase help gradually only when requested or clearly blocked;
5. preserve authorship by returning control as soon as the learner can proceed.

Documentation research and ordinary tool use are part of autonomous work. Techne may point to authoritative documentation without turning the milestone into a tutorial.

## Framework progression

The product starts with the simplest implementation that can test value. A likely progression is:

1. direct model calls and typed/validated structured outputs;
2. a FastAPI service and real persistence;
3. evaluation data and traces early enough to guide decisions;
4. LangChain abstractions when repeated models, tools, retrieval, or integrations justify them;
5. LangGraph when explicit state, branches, durable execution, interrupts, or resumability become real requirements;
6. production hardening: security, privacy, latency, cost, failure handling, deployment, and monitoring.

This is a dependency order, not a fixed calendar. The chosen product and autonomous pace determine when each need appears.

## Portfolio evidence

The final case study should show:

- the researched problem and user segment;
- discarded assumptions and product changes;
- the narrow value delivered;
- architecture and major trade-offs;
- evaluation method and results;
- reliability, security, latency, and cost considerations;
- what the learner personally implemented and what assistance was used;
- real feedback or usage when available.

Avoid presenting a study exercise as a validated business. State evidence and limitations precisely.
