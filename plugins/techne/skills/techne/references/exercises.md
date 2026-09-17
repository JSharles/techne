# Exercise standard

Read this file before creating, opening, resuming, or revising any morning lesson, exercise, or review.

## Preflight

Before presenting an exercise, verify that:

- the scenario is understandable without hidden project context;
- every necessary ambiguous term is defined;
- a concrete example shows expected behaviour without revealing the solution;
- the action, editable files, and completion evidence are explicit;
- every provided command terminates and yields useful output;
- the normal browser, VS Code, test, and debugger loop works;
- the difficulty fits observed evidence rather than years of experience;
- every evaluated formal concept serves the engineering problem.

Keep the activity closed until preflight passes.

## Brief outside the timebox

Present, in order:

1. the situation;
2. why it matters in production;
3. indispensable vocabulary;
4. one distinct example;
5. the exact mission and definition of done.

Clarification consumes neither time nor help level. Start the timebox only after the learner confirms the context and action are clear.

## One action

Give one observable action at a time. Name the file or browser activity, the action, the evidence to report or inspect, and the bound for that step. Wait for the result before opening the next action.

Do not ask the learner to maintain pedagogical documents or copy terminal output that the agent can inspect.

## Debugging

Use this order:

1. reproduce;
2. state one failing behaviour from actual output;
3. let the learner inspect and explain;
4. collect one additional fact or make one minimal change;
5. verify and generalize.

Request a prediction before execution only when it reduces uncertainty and its purpose has been explained.

## Ambiguity

When Techne's wording causes confusion, stop the timebox, consume no help level, draw no mastery conclusion, fix the statement, and investigate a systemic cause when repeated.

## Browser or repository

Choose browser practice for short recall, mental tracing, quizzes, and isolated algorithms. Generate the lesson under `.techne/browser/lessons/` from `.techne/browser/lesson-template.html`, which already carries the learning language, use the bundled assets, start `.techne/browser/serve.py`, and inspect the local event log before feedback.

Choose a real repository for TypeScript, React, Next.js, backend, multi-file debugging, architecture, performance, and production work. Scaffold only what removes irrelevant setup; leave the reasoning and target implementation to the learner.

At the end of a timebox, checkpoint the work even when incomplete.
