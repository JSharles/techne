# Exercise standard

Read this file before creating, opening, resuming, or revising any lesson, exercise, or review, in either curriculum.

## Preflight

Before presenting an exercise, verify that:

- the scenario is understandable without hidden project context;
- every necessary ambiguous term is defined;
- a concrete example shows expected behaviour without revealing the solution;
- the action, editable files, and completion evidence are explicit;
- every provided command terminates and yields useful output;
- the normal browser, VS Code, test, and debugger loop works;
- the difficulty follows the easy-first ladder and observed evidence, never years of experience;
- every evaluated formal concept serves the engineering problem.

Keep the activity closed until preflight passes.

## Lesson before practice

Every activity in either curriculum starts with a short lesson, except placement-test exercises, due reviews, transfer work on an already demonstrated skill, and capstone milestones.

- Generate it as a browser page (see "Browser or repository"), readable in five to ten minutes: the engineering problem, a mental model with its vocabulary, one worked example distinct from the exercise, and one or two quick checks (quiz or recall).
- Serve and open it yourself, then tell the learner to read it and to say when they are done.
- Open the coding exercise only after the lesson. The exercise brief then refers back to the lesson instead of repeating it.

## Brief outside the timebox

Present, in order:

1. the situation;
2. why it matters in production;
3. indispensable vocabulary;
4. one distinct example;
5. the exact mission and definition of done.

Clarification consumes neither time nor help level. Start the timebox only after the learner confirms the context and action are clear.

## DSA exercises and LeetCode

Base every DSA exercise on a free LeetCode problem whenever one fits, preferring the problems listed for the current topic in [curriculum.md](curriculum.md#dsa-problem-bank).

- The learner solves it locally, in TypeScript, in a small exercise folder with tests that Techne can run and read.
- Write the statement yourself in the learning language; never copy LeetCode's text.
- Give the link `https://leetcode.com/problems/<slug>/` in the brief as the original problem, and suggest submitting there once the local tests pass.
- Link only problems from the problem bank or problems you have verified exist and are not paid-only. Without a verified match, write an original exercise and give no link.

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

Use the browser for lessons, short recall, mental tracing, and quizzes. Generate the lesson under `.techne/browser/lessons/` from `.techne/browser/lesson-template.html`, which already carries the learning language, use the bundled assets, start `.techne/browser/serve.py`, and inspect the local event log before feedback.

Use a local exercise folder or real repository for coding: the Applied AI lab, DSA, TypeScript, React, Next.js, NestJS and backend, multi-file debugging, architecture, performance, and production work. Scaffold only what removes irrelevant setup; leave the reasoning and target implementation to the learner.

At the end of a timebox, checkpoint the work even when incomplete.
