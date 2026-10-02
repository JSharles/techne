---
id: product-engineer
title: Product Engineer
version: 1
activity_kinds: code, writing, oral
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=30, review=5, project=90, placement=15
red_thread: yes
survey_ceiling: discovered
---

# Product Engineer

## Outcome and boundary

For a React/Node developer with good product intuition and no method, who wants to own the role of product
engineer: carry a feature from idea to measured impact (define the problem, scope a first slice, ship it
progressively, measure whether it worked, decide what happens next), know the methods and tools behind each
step, place coding agents inside that method, and defend all of it in a product engineer interview.

The spine is the Define / Build / Ship cycle described by product.engineer, with measurement, adoption and
feedback inside Ship. The site gives the map and a handful of solid practices (problem statements, assumption
mapping, metrics, user research for engineers, written decision documents, launch). It is thin on discovery
without existing users, instrumentation and rollout implementation, and experimentation; those parts are
built from other primary sources. Statistics quoted on the site without a source are never taught as facts.

Deliberately out of scope: compensation, certifications and job listings; advanced experimentation statistics
(power analysis beyond a rule of thumb, sequential testing, CUPED); teaching React, Node or a backend
framework, which this program relies on rather than teaches; managing a team.

The program is self-contained: a stranger can follow it alone. It keeps its own evidence; nothing
demonstrated in another program counts here.

## Who writes what — method exception

This program runs under the decision of 2026-10-01T23:48:34+02:00 in `.techne/DECISIONS.md`, which extends
the decision of 2026-10-01T11:12:45+02:00: the subject here is the product engineer role, not learning to code.

- **Coding agents may write** the application code of this program's red-thread project, in its own repository.
- **The learner writes by hand** everything the role is judged on: problem statements, assumption maps,
  research notes and syntheses, one-pagers, PRFAQs, specs, tracking plans, rollout and kill criteria, review
  verdicts on agent output, ship reviews, post-mortems, interview answers. These artifacts are the evidence.
- **Techne writes** none of the learner's artifacts or code. It reviews them, gives structure-only skeletons,
  and prepares review exercises with planted defects.
- **Agents never touch** the Engineering red-thread repository, where "no LLM pre-review" stays in force.

Isolated exercises outside the project that are explicitly about code (instrumentation, flag evaluation, a
migration) are written by the learner.

## Oral work

Oral answers arrive as speech-to-text transcripts. Techne judges content only: whether the answer addresses
the question, cites numbers, states trade-offs, and has a structure. Delivery (fluency, pace, hesitation) is
never assessed and never recorded, and Techne says so when it gives feedback.

## Sequence

### Unit 1 — The role

- What a product engineer owns, and how the role differs from software engineer, full-stack engineer,
  product manager, designer and project manager.
- The Define / Build / Ship cycle and the seven skills: problem decomposition, rapid prototyping,
  measurement literacy, cross-functional communication, full-stack depth, business context, systems thinking.
- Written self-assessment against the competency map, revisited at the end of the program.

### Unit 2 — Product sense

- Observing a product with a protocol; reverse teardown of an existing product.
- Jobs-to-be-done framing.
- Hypotheses written as three competing explanations, the cheapest test that separates them, and a kill
  criterion.
- Craft: loading, empty and error states, interaction coherence; working with a designer.

### Unit 3 — Discovery without a research team

- User interviews that do not lead the answer; recruiting people to talk to; consent.
- Mining support tickets and reviews; five-minute calls; micro-surveys; do-it-yourself usability tests.
- Synthesis: from notes to patterns to a sized opportunity.
- Validating with zero users: landing page, fake door, concierge MVP, finding the first ten users.

### Unit 4 — Define and prioritise

- Problem statement: who, evidence, cost of inaction, metric, time box, confidence.
- Assumption mapping by impact and uncertainty, with a validation method for each.
- The build-worthiness test before any code; back-of-the-envelope opportunity sizing.
- Prioritisation with RICE and ICE; trade-offs; saying no.

### Unit 5 — Writing to decide

- One-pager and PRFAQ (working backwards).
- Spec with intent, acceptance criteria, edge cases, constraints and non-goals.
- Slicing: smallest shippable slice, scope cuts, layered building (hypothesis, hardening, polish).

### Unit 6 — Measure

- North star, input and guardrail metrics; leading and lagging indicators; metrics matched to product stage.
- Tracking plan: the three-event minimum, naming convention, instrumentation inside the pull request, baselines.
- Implementing events with an analytics SDK, client versus server tracking, consent and GDPR.
- Reading a funnel, a retention curve and a cohort.

### Unit 7 — Ship and launch

- Feature flags: server-side evaluation, sticky bucketing, kill switch, flag hygiene.
- Staged and percentage rollouts with explicit gates, canary thresholds, rollback plan.
- Expand / contract database migrations that survive a rollback.
- Launch: distribution, onboarding, activation, changelog.

### Unit 8 — Conclude and learn

- A/B test basics: primary and guardrail metrics, rough sample size, confounders, and when traffic is too low
  for a test to mean anything.
- Ship review: baseline, current, target, verdict (keep, kill, iterate), next action; presenting results.
- Root cause analysis with five whys; blameless post-mortems.

### Unit 9 — AI in the method

- Where agents fit in Define, Build and Ship; agent maturity levels.
- Spec-driven work: a spec an agent can execute and a human can check.
- Bounded autonomy: classifying actions by reversibility and blast radius, permissions outside the model.
- Reviewing agent output on three layers: spec conformance, systemic integrity, product judgment.
- Measuring what AI tooling actually returns: acceptance and revert rates, cycle time, change failure rate.

### Unit 10 — The role in interviews

- Impact portfolio and outcome-first storytelling.
- Product sense interview: problem framing, metrics, trade-offs, out loud.
- The product angle in a system design interview; pitching expanded ownership.
- Mock interviews on the learner's own project.

## Red-thread project

The project has its own repository, separate from every other program's, and real users even if few. Each unit
lands on it: unit 3's discovery chooses or reshapes it, unit 4 and 5 artifacts define its first slice, unit 6
instruments it, unit 7 ships it behind a flag, unit 8 reviews it, unit 9 governs how agents build it, unit 10
turns it into interview material. The idea is chosen with the learner, after unit 2.

## Subject catalogue

### The role — `perole.*`

`ownership`, `role-boundaries`, `define-build-ship`, `seven-skills`, `self-assessment`

### Product sense — `pesense.*`

`observation`, `teardown`, `jobs-to-be-done`, `hypotheses`, `kill-criteria`, `craft-states`,
`designer-collaboration`

### Discovery — `pedisc.*`

`interviews`, `recruiting`, `ticket-mining`, `micro-surveys`, `usability-tests`, `synthesis`,
`zero-user-validation`, `first-users`

### Define and prioritise — `pedef.*`

`problem-statement`, `assumption-mapping`, `build-worthiness`, `opportunity-sizing`, `rice-ice`,
`trade-offs`, `saying-no`

### Writing to decide — `pedoc.*`

`one-pager`, `prfaq`, `spec`, `non-goals`, `slicing`, `layered-building`

### Measure — `pemeas.*`

`north-star`, `input-guardrail-metrics`, `stage-metrics`, `tracking-plan`, `event-implementation`,
`consent-privacy`, `funnels`, `retention-cohorts`

### Ship and launch — `peship.*`

`feature-flags`, `kill-switch`, `staged-rollout`, `canary`, `expand-contract`, `flag-hygiene`, `launch`,
`onboarding-activation`, `changelog`

### Conclude and learn — `pelearn.*`

`ab-basics`, `low-traffic`, `ship-review`, `presenting-results`, `five-whys`, `post-mortem`

### AI in the method — `peai.*`

`agents-in-cycle`, `maturity-levels`, `spec-driven`, `bounded-autonomy`, `reviewing-agent-output`,
`ai-roi`

### Interviews — `peint.*`

`impact-portfolio`, `outcome-storytelling`, `product-sense-interview`, `system-design-product`,
`pitching-ownership`

## Adaptation rules

- The learner arrives with intuition and no method. The placement test checks which reflexes already exist
  (framing a problem, choosing a metric, cutting scope); a demonstrated reflex compresses its lesson to the
  vocabulary and the template, never skips the practice.
- Every method is practised first on a small given case, then on the red-thread project. A subject reaches
  `transferred` only from project evidence.
- Writing artifacts are judged against explicit criteria given before the work (for example: a problem
  statement names who, the evidence, and a number). A vague artifact that meets the template's shape but
  commits to nothing stays `discovered`.
- Agent-built project code is never evidence. Evidence comes from the learner's artifacts and from planted
  defects found unaided in review exercises.
- Units 1 and 2 come first; units 3 to 8 follow the cycle; unit 9 may be pulled forward as soon as agents
  start building the project; unit 10 draws on everything and can run alongside units 7 and 8.
