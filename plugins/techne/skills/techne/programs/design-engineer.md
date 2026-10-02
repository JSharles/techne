---
id: design-engineer
title: Design engineer UI/UX
version: 1
activity_kinds: writing, browser, code, oral
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=15
red_thread: yes
survey_ceiling: discovered
---

# Design engineer UI/UX

## Outcome and boundary

For a frontend developer who wants to become a design engineer: someone who researches, frames, designs and
tests interfaces, and also builds them. By the end the learner can run a complete design project on a real
product (research, problem definition, information architecture, flows, wireframes, visual design,
prototype, usability testing, iteration), build and document the foundations of a design system, and defend
every decision in a critique or an interview with principles and evidence rather than taste.

The program follows five levels, expressed as the order of its units, not as a second grading scale:
fundamentals (units 1–4), methods (5–10), interface design (11–19), professional practice (20–26), and a
survey of expert and research topics (27). Mastery is recorded per subject, as in every program.

The curriculum was designed from a corpus the learner assembled. Each subject is built from at least two
sources when the corpus allows it; when sources disagree, the lesson shows the disagreement instead of
picking one. Lessons are written by Techne from these sources and link to them; they never reproduce a
source's text.

Deliberately out of scope: graphic design for print, branding and logo design, illustration, 3D and motion
production beyond interface motion, design tools other than Figma, and the statistics of experimentation
beyond reading a result and its uncertainty. Service design, advanced HCI research and novel interaction
techniques are surveyed, not practised.

The program is self-contained: a stranger can follow it alone. It keeps its own evidence; nothing
demonstrated in another program counts here, including accessibility, product metrics or user interviews
taught elsewhere.

## Tools and evidence

- **Figma** (free plan) for sketches turned digital, wireframes, mockups, components and prototypes. The
  learner shares a link or exports frames into the exercise folder; Techne reads the file through the Figma
  connection or the exported images. Dev Mode is a paid feature, so handoff (unit 22) uses variables,
  annotations, exported specs and the inspect panel available on the free plan.
- **HTML/CSS** for prototypes where behaviour, focus, responsiveness or motion matter. The learner writes
  every line, as in every program.
- **Writing** for research plans, interview guides, syntheses, problem statements, rationale and case
  studies. These documents are the evidence for research and framing subjects.
- **Oral** for critique and defence of decisions. Answers arrive as speech-to-text transcripts; Techne judges
  content only (principle cited, evidence, trade-off stated, structure), never delivery.

## Research with real people

Interviews and usability tests need participants. The learner recruits three to five people for the
red-thread project. When the domain makes that impossible, the fallback is guerrilla testing: short tests
(about ten minutes) with anyone available, on tasks that need no domain expertise. A research or testing
subject reaches `independent` only on work with real participants, guerrilla included; a plan, a guide or a
simulated session alone leaves it at `assisted`.

## Red-thread project

One product carries the nine projects and the final project, so each step builds on the previous one. The
starting idea is the learner's SaaS **Diaphane**: an interface that explains a developer's work to their
client in plain terms. The product is not fixed: the learner may switch to another idea at any project
boundary. A switch keeps all evidence, and the next project starts from a short research catch-up on the new
product instead of redoing earlier projects.

| Project | Unit | Deliverable |
| --- | --- | --- |
| 1 — UX analysis | 4 | Heuristic evaluation of an existing product close to the red-thread domain, with severity ratings. |
| 2 — Research | 6 | Research plan, interview guide, three to five interviews, synthesis and insights. |
| 3 — Information architecture | 8 | Content inventory, card sort, site map, tree test and its result. |
| 4 — Wireframes | 10 | One complete journey in low fidelity, with flows and every state. |
| 5 — UI design | 19 | The journey in high fidelity, responsive and accessible, built on a grid and a type scale. |
| 6 — Prototype | 20 | Interactive prototype in Figma, and one critical screen in HTML/CSS. |
| 7 — Usability testing | 21 | Test plan, sessions, findings ranked by severity. |
| 8 — Iteration | 21 | Changes driven by the findings, with before/after and rationale. |
| 9 — Design system | 22 | Tokens, a typography and colour system, core components with states and documentation. |
| Final | 26 | The full cycle on a new feature (a dashboard or an AI feature), then a case study defended orally. |

## Sequence

### Unit 1 — The discipline and the process (level 1)

- What UX, UI, interaction design and HCI each cover, and how they overlap.
- Human-centred and user-centred design; design thinking (empathise, define, ideate, prototype, test) and
  the double diamond; why the process iterates.
- The design engineer role: where it sits between design and frontend engineering, and what it owns.
- Figma basics: frames, auto layout, components and instances, styles, sharing.
- Sources: OpenLearn *An Introduction to Interaction Design*; Stanford CS147; Stanford d.school *Design
  Thinking Bootleg*; IDEO design thinking resources; Encyclopedia of HCI; Figma help centre.
- Mastery: explains a real product decision in terms of the process stage it came from; builds a responsive
  card in Figma with auto layout and a component.

### Unit 2 — Perception and cognition (level 1)

- Perception, attention, working and long-term memory, cognitive load.
- Gestalt principles (proximity, similarity, closure, continuity, common region, figure/ground).
- Recognition versus recall; decision making; cognitive biases that shape interface use.
- Fitts's law and Hick's law, and their limits.
- Sensory, cognitive and physical abilities as design constraints.
- Sources: Encyclopedia of HCI; NN/g; OpenLearn; Laws of UX as an index, checked against primary sources.
- Mastery: names the perceptual or cognitive cause of a defect in an unseen interface and proposes a fix.

### Unit 3 — Principles of interaction (level 1)

- Mental models and conceptual models; the gulfs of execution and evaluation.
- Affordances and signifiers; feedback; constraints; mapping; consistency and standards (Jakob's law).
- Direct manipulation; interaction cost; response time limits.
- Sources: Encyclopedia of HCI; NN/g; CMU interaction techniques short course; OpenLearn.
- Mastery: diagnoses a confusing control in terms of signifier, feedback or mapping, and redesigns it.

### Unit 4 — Usability and heuristics (level 1)

- Usability components: learnability, efficiency, memorability, errors, satisfaction.
- Nielsen's ten heuristics; heuristic evaluation; cognitive walkthrough; expert review; severity ratings.
- First critique practice: describing a problem without prescribing a solution.
- Sources: NN/g; 18F Methods (heuristic evaluation, cognitive walkthrough); Stanford CS147.
- Project 1.
- Mastery: an evaluation of an unseen product that finds the major issues, ties each to a heuristic, and
  ranks them by severity with a reason.

### Unit 5 — User research (1): plan and conduct (level 2)

- Research strategy across the product life (discovery, alpha, beta, live); research questions versus
  interview questions.
- Choosing a method: qualitative and quantitative, attitudinal and behavioural.
- Research plans; recruitment and sampling; informed consent and research ethics.
- Interviews that do not lead the answer; observation; contextual inquiry; note-taking.
- Sources: GOV.UK Service Manual (user research); 18F UX guide; 18F Methods; Digital.gov human-centred
  design; d.school Bootleg.
- Mastery: a plan whose questions can be answered by its method, and an interview transcript without leading
  or closed questions where open ones were needed.

### Unit 6 — User research (2): make sense and report (level 2)

- Debriefs; synthesis; affinity mapping and the KJ method; from observations to insights.
- Surveys: when they fit, writing questions, bias; diary studies.
- Reporting findings so a team acts on them; research repositories.
- Sources: GOV.UK; 18F UX guide; 18F Methods; NN/g.
- Project 2.
- Mastery: insights that each trace back to several observations and say something a team can act on.

### Unit 7 — Problem framing (level 2)

- User needs and business needs; problem statements; jobs to be done.
- Personas, proto-personas and their misuse; empathy maps.
- Journey maps, experience maps, opportunity mapping.
- How Might We questions; prioritisation of problems before solutions.
- Sources: 18F Methods; d.school Bootleg; NN/g; GOV.UK.
- Mastery: a problem statement grounded in project 2 evidence, with no solution in it, and a prioritised set
  of opportunities with reasons.

### Unit 8 — Information architecture (level 2)

- Organisation schemes, taxonomies, classification, content hierarchy.
- Navigation systems, labelling, wayfinding.
- Card sorting (open, closed) and tree testing.
- Search: information seeking, query intent, results pages, information scent, filtering and faceted
  navigation.
- Sources: Web Style Guide; Hearst *Search User Interfaces*; NN/g; GOV.UK Design System navigation patterns.
- Project 3.
- Mastery: a structure justified by card-sort and tree-test results, with labels taken from users' words.

### Unit 9 — Flows and states (level 2)

- User flows and task flows; happy path and edge cases.
- State design: empty, loading, partial, error, success; progressive disclosure.
- Interaction patterns and when to reuse rather than invent; microinteractions.
- Sources: NN/g; GOV.UK Design System; Atlassian Design System; Encyclopedia of HCI.
- Mastery: a flow that covers every state and failure of an unseen task, with no dead end.

### Unit 10 — Sketching, wireframes and fidelity (level 2)

- Sketching and divergence (crazy eights, several alternatives before choosing).
- Paper prototypes; low- and mid-fidelity wireframes; choosing fidelity for the question being asked.
- Sources: d.school Bootleg; Stanford CS147; OpenLearn; 18F Methods.
- Project 4.
- Mastery: several distinct alternatives for one screen, a reasoned choice, and wireframes that answer the
  question they were made for.

### Unit 11 — Visual fundamentals (level 3)

- Visual elements (point, line, shape) and visual language.
- Composition, balance, rhythm, repetition, alignment, proximity, contrast, scale, proportion.
- Visual hierarchy and scannability; white space.
- Sources: *Graphic Design and Print Production Fundamentals*; CMU OLI Visual Design; Web Style Guide;
  NN/g.
- Mastery: reworks an unseen cluttered screen so its hierarchy reads in the intended order, and names the
  principle behind each change.

### Unit 12 — Grids, layout and responsiveness (level 3)

- Column grids, baseline and spacing scales; layout patterns.
- Responsive principles, mobile first, breakpoints, fluid layouts; adaptive interfaces.
- Density for data-heavy B2B screens; touch targets; mobile navigation; desktop versus mobile behaviour.
- Sources: *Graphic Design and Print Production Fundamentals*; Web Style Guide; Atlassian Design System;
  W3C WAI designing tips.
- Mastery: one screen on a grid at three widths, written in HTML/CSS for one of them, with consistent
  spacing tokens.

### Unit 13 — Typography (level 3)

- Typeface anatomy and classification; choosing a typeface for an interface.
- Legibility and readability; size, line height, line length, tracking, kerning, paragraph spacing.
- Type scales and typographic hierarchy; responsive typography.
- Sources: Butterick's *Practical Typography*; *Graphic Design and Print Production Fundamentals*; Web Style
  Guide; Atlassian typography foundations.
- Mastery: a type scale with stated ratios and line heights, applied to an unseen screen with a readable
  hierarchy.

### Unit 14 — Colour (level 3)

- Colour models (RGB, HSL, OKLCH); hue, saturation, lightness; harmony.
- Contrast and its measurement; colour never as the only signal.
- Semantic colour; colour systems and palettes with steps; dark mode.
- Sources: Atlassian colour foundations; W3C WAI; WCAG 2.2; *Graphic Design and Print Production
  Fundamentals*.
- Mastery: a palette with semantic roles that passes contrast in light and dark mode, with the measures.

### Unit 15 — Iconography, imagery and motion (level 3)

- Icons: when they help, when a label is needed, consistency of a set.
- Images and illustration in interfaces; their content role.
- Motion: purpose (orientation, feedback, continuity), duration and easing, reduced motion.
- Sources: Atlassian iconography and motion foundations; Material Design motion; W3C WAI; Web Style Guide.
- Mastery: a transition specified with its purpose, duration and easing, implemented in CSS with a
  reduced-motion alternative.

### Unit 16 — Components and patterns (level 3)

- Buttons, inputs, checkboxes, radios, selects; navigation, tabs, modals, tooltips.
- Tables, cards, lists; search and filters; pagination; notifications, alerts and toasts; empty states.
- Choosing between patterns: modal or page, tabs or sections, toast or inline message.
- Sources: GOV.UK Design System; Atlassian Design System; NN/g.
- Mastery: chooses between two patterns for an unseen case and justifies it with user and context, not
  habit.

### Unit 17 — Forms (level 3)

- Form structure, labels, help text, grouping; one question per page versus one long form.
- Validation timing; error prevention and error recovery; error messages in place.
- Multi-step forms; checkout flows; authentication, passwords, autofill.
- Sources: GOV.UK Design System; NN/g; W3C WAI forms tutorial; Atlassian.
- Mastery: redesigns an unseen faulty form so that every error is prevented or recoverable, and builds it
  in accessible HTML.

### Unit 18 — UX writing and content design (level 3)

- Content design; microcopy; buttons, labels, instructions, link text.
- Error, empty-state and confirmation messages.
- Voice and tone; plain language; writing for scanning; inclusive language; localisation.
- Sources: GOV.UK content design; Atlassian content design; NN/g.
- Mastery: rewrites the copy of an unseen screen so each message says what happened and what to do next,
  in plain language.

### Unit 19 — Accessibility and inclusive design (level 3)

- Disability models; assistive technologies; WCAG principles (perceivable, operable, understandable,
  robust) and levels.
- Visual, motor and cognitive accessibility; screen readers; keyboard navigation; focus management.
- Accessible content and forms; testing with tools and by hand, and the limits of tools.
- Inclusive design beyond compliance.
- Sources: W3C WAI resources, designing tips and tutorials; WCAG 2.2; GOV.UK Service Manual.
- Project 5.
- Mastery: an audit of an unseen screen that finds the failures a tool misses, mapped to success criteria,
  and fixes them.

### Unit 20 — Interactive prototyping (level 4)

- Prototypes as questions; Figma prototyping (flows, interactions, variables, conditional states).
- When to switch to HTML/CSS: real focus, real responsiveness, real data.
- Sources: Stanford CS147; d.school Bootleg; Figma help centre; 18F Methods.
- Project 6.
- Mastery: a prototype whose fidelity matches the question asked, and a critical screen in HTML/CSS that
  works with keyboard and at every width.

### Unit 21 — Usability testing (level 4)

- Test plans; research questions; tasks and scenarios that do not give the answer.
- Recruitment; moderation; think-aloud; remote testing; guerrilla testing.
- Observation and note-taking; severity ratings; analysis; reporting.
- Iteration from findings.
- Sources: GOV.UK; 18F UX guide; NN/g; Stanford CS147; Digital.gov.
- Projects 7 and 8.
- Mastery: a moderated session that does not lead, findings ranked by severity and tied to observations,
  and changes that address them.

### Unit 22 — Design systems (level 4)

- What a design system is, and when it is worth it.
- Foundations; design tokens; colour, typography, spacing and grid systems.
- Components, variants and states; component documentation.
- Governance, contribution, consistency and scale.
- Handoff to developers: variables, annotations, specs, and tokens shared between Figma and CSS.
- Sources: GOV.UK Design System; Atlassian Design System; Carbon (for data components).
- Project 9.
- Mastery: tokens defined once and used in both Figma and CSS, and components whose states and usage rules
  are documented well enough for another person to use them.

### Unit 23 — Data visualisation for B2B products (level 4)

- Choosing a chart from the relationship to show (comparison, distribution, part-to-whole, change over time,
  correlation).
- Encoding, scales and axes; colour in charts; annotation; misleading charts.
- Dashboards: questions first, layout, density, drill-down; data tables at scale (sorting, filtering,
  column choice, numeric alignment).
- Accessible charts.
- Sources: Claus Wilke *Fundamentals of Data Visualization*; Financial Times *Visual Vocabulary*; Carbon data
  visualisation guidelines; NN/g; W3C WAI.
- Mastery: a dashboard for a stated set of user questions, where each chart type is justified and nothing
  misleads.

### Unit 24 — AI and conversational interfaces (level 4)

- Setting expectations about what the system can do; showing uncertainty and sources.
- Errors, correction and graceful failure; user control, undo and override; trust calibration.
- Conversational interfaces: turn taking, prompts and suggestions, when chat is the wrong interface.
- Durable principles over current patterns: the lesson dates every example.
- Sources: Google *People + AI Guidebook*; Microsoft *Guidelines for Human-AI Interaction* (Amershi et al.,
  CHI 2019); NN/g AI articles.
- Mastery: an AI feature designed so a wrong output is visible, correctable and never silently applied.

### Unit 25 — Design in the product (level 4)

- Product discovery; user value and business value; constraints.
- Hypotheses, MVP, experimentation; prioritisation.
- UX metrics; behavioural analytics; funnels, conversion, retention; A/B testing and reading a result;
  triangulating qualitative and quantitative evidence.
- Ethics: persuasive design, dark patterns, consent.
- Sources: NN/g; GOV.UK Service Manual; Encyclopedia of HCI (persuasive design); Stanford HCI courses;
  Deceptive Design.
- Mastery: a design change stated as a hypothesis with a metric, a guardrail and a threshold, and a review
  of an unseen flow that names its dark patterns.

### Unit 26 — Critique, case study and portfolio (level 4)

- Giving and receiving critique; evaluating an interface; design rationale.
- Defending decisions; naming trade-offs; comparing alternatives.
- Case study structure: problem, research, process, iterations, failures, decisions, results.
- Portfolio storytelling; presenting a project.
- Sources: Frank Chimero *The Shape of Design*; Stanford CS147; NN/g.
- Final project.
- Mastery: an oral defence of the final project that answers challenges with evidence and states what the
  learner would do differently.

### Unit 27 — Beyond the interface (level 5)

- Service design: touchpoints, stakeholder and ecosystem maps, customer journeys, service blueprints
  (frontstage, backstage), service prototyping.
- Advanced HCI: seminal papers, experimental design, research through design.
- Interaction techniques: input and output devices, gestures, text entry, VR and ubiquitous computing.
- Sources: Service Design Toolkit; Stanford HCI courses; CMU interaction techniques short course;
  Encyclopedia of HCI.

## Subject catalogue

### Discipline and process — `defound.*`

`ux-ui-hci`, `human-centred-design`, `design-thinking`, `double-diamond`, `iteration`, `design-engineer-role`

### Figma — `defigma.*`

`frames-auto-layout`, `components-instances`, `styles-variables`, `prototyping`, `handoff`

### Perception and cognition — `depsy.*`

`perception`, `attention`, `memory`, `cognitive-load`, `gestalt`, `recognition-recall`, `decision-making`,
`cognitive-biases`, `fitts-law`, `hicks-law`, `human-abilities`

### Interaction principles — `deixd.*`

`mental-models`, `gulfs`, `affordances-signifiers`, `feedback`, `constraints`, `mapping`, `consistency`,
`direct-manipulation`, `interaction-cost`, `response-time`

### Usability — `deusab.*`

`usability-components`, `nielsen-heuristics`, `heuristic-evaluation`, `cognitive-walkthrough`,
`expert-review`, `severity-ratings`

### User research — `deres.*`

`research-strategy`, `research-questions`, `method-choice`, `research-plan`, `recruitment-sampling`,
`consent-ethics`, `interviews`, `observation`, `contextual-inquiry`, `note-taking`, `surveys`,
`diary-studies`, `synthesis`, `affinity-mapping`, `insights`, `reporting`

### Problem framing — `deframe.*`

`user-business-needs`, `problem-statements`, `jobs-to-be-done`, `personas`, `empathy-maps`,
`journey-maps`, `opportunity-mapping`, `how-might-we`, `prioritisation`

### Information architecture — `deia.*`

`organisation-schemes`, `taxonomies`, `content-hierarchy`, `navigation-systems`, `labelling`, `wayfinding`,
`card-sorting`, `tree-testing`, `search-ux`, `filtering-facets`, `information-scent`

### Flows and states — `deflow.*`

`user-flows`, `task-flows`, `edge-cases`, `state-design`, `empty-states`, `loading-states`, `error-states`,
`progressive-disclosure`, `interaction-patterns`, `microinteractions`

### Sketching and wireframes — `dewire.*`

`sketching`, `divergence`, `paper-prototypes`, `wireframes`, `fidelity-choice`

### Visual design — `devis.*`

`visual-language`, `composition`, `balance-rhythm`, `alignment-proximity`, `contrast`, `scale-proportion`,
`visual-hierarchy`, `white-space`

### Layout — `delayout.*`

`grids`, `spacing-scales`, `layout-patterns`, `responsive-principles`, `breakpoints-fluid`, `density`,
`touch-targets`, `mobile-navigation`

### Typography — `detype.*`

`anatomy-classification`, `typeface-choice`, `legibility-readability`, `size-leading-measure`,
`tracking-kerning`, `type-scales`, `typographic-hierarchy`, `responsive-type`

### Colour — `decolor.*`

`colour-models`, `harmony`, `contrast-measurement`, `colour-not-alone`, `semantic-colour`, `palettes`,
`dark-mode`

### Iconography, imagery and motion — `demedia.*`

`icons`, `imagery`, `motion-purpose`, `duration-easing`, `reduced-motion`

### Components — `decomp.*`

`buttons`, `inputs-choices`, `navigation-components`, `tabs`, `modals`, `tooltips`, `tables`,
`cards-lists`, `search-filters`, `pagination`, `notifications-alerts`, `pattern-choice`

### Forms — `deform.*`

`form-structure`, `labels-help`, `validation`, `error-prevention-recovery`, `multi-step`, `checkout`,
`authentication-passwords`, `autofill`

### Content design — `dewrite.*`

`content-design`, `microcopy`, `messages`, `voice-tone`, `plain-language`, `scanning`, `inclusive-language`,
`localisation`

### Accessibility — `dea11y.*`

`disability-models`, `assistive-tech`, `wcag`, `visual-a11y`, `motor-a11y`, `cognitive-a11y`,
`screen-readers`, `keyboard-focus`, `accessible-forms`, `a11y-testing`, `inclusive-design`

### Prototyping — `deproto.*`

`prototype-as-question`, `figma-prototype`, `code-prototype`

### Usability testing — `detest.*`

`test-plan`, `tasks-scenarios`, `moderation-think-aloud`, `remote-guerrilla`, `test-analysis`,
`test-reporting`, `iteration-from-findings`

### Design systems — `desys.*`

`ds-fundamentals`, `tokens`, `foundation-systems`, `components-variants`, `documentation`, `governance`,
`design-code-sync`

### Data visualisation — `dedataviz.*`

`chart-choice`, `encoding-scales`, `chart-colour`, `annotation`, `misleading-charts`, `dashboards`,
`data-tables`, `accessible-charts`

### AI interfaces — `deai.*`

`expectations`, `uncertainty-sources`, `error-correction`, `user-control`, `trust-calibration`,
`conversational-design`

### Product and measurement — `deprod.*`

`discovery-value`, `hypotheses-mvp`, `ux-metrics`, `analytics-funnels`, `ab-testing`, `triangulation`,
`ethics-dark-patterns`

### Critique and portfolio — `decrit.*`

`giving-critique`, `receiving-critique`, `design-rationale`, `trade-offs`, `case-study`, `presentation`

### Survey — beyond the interface — `desurvey.*`

`service-design`, `service-blueprints`, `stakeholder-ecosystem-maps`, `hci-research`,
`experimental-design`, `research-through-design`, `interaction-techniques`, `emerging-platforms`

## Sources

| Source | URL |
| --- | --- |
| OpenLearn — An Introduction to Interaction Design | https://www.open.edu/openlearn/science-maths-technology/an-introduction-interaction-design |
| Encyclopedia of Human-Computer Interaction, 2nd ed. | https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed |
| Stanford CS147 (autumn 2026) | https://hci.stanford.edu/courses/cs147/2026/au/index.html |
| Web Style Guide | https://webstyleguide.com/ |
| Nielsen Norman Group | https://www.nngroup.com/articles/ |
| GOV.UK Service Manual | https://www.gov.uk/service-manual |
| 18F UX guide (archived; 18F was dissolved in 2025) | https://github.com/18F/ux-guide |
| 18F Methods (archived, CC0) | https://github.com/18F/methods |
| Digital.gov — Human-centered design | https://digital.gov/topics/human-centered-design/ |
| Stanford d.school — Design Thinking Bootleg | https://dschool.stanford.edu/tools/design-thinking-bootleg |
| IDEO — Design thinking resources | https://designthinking.ideo.com/resources |
| Hearst — Search User Interfaces | https://searchuserinterfaces.com/book/ |
| Graphic Design and Print Production Fundamentals | https://opentextbc.ca/graphicdesign/ |
| Butterick's Practical Typography | https://practicaltypography.com/ |
| CMU OLI — Visual Design | https://oli.cmu.edu/courses/visual-design-open-free/ |
| Frank Chimero — The Shape of Design | https://shapeofdesignbook.com/ |
| W3C WAI resources, designing tips, tutorials | https://www.w3.org/WAI/resources/ |
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ |
| Atlassian Design System and content design | https://atlassian.design/design-system |
| GOV.UK Design System | https://design-system.service.gov.uk/ |
| Service Design Toolkit | https://www.servicedesigntoolkit.org/downloads.html |
| Stanford HCI courses | https://hci.stanford.edu/courses/ |
| CMU — Interaction techniques short course | https://www.cs.cmu.edu/~bam/ixtshortcourse/index.html |
| Claus Wilke — Fundamentals of Data Visualization | https://clauswilke.com/dataviz/ |
| Financial Times — Visual Vocabulary | https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary |
| Carbon — Data visualisation | https://carbondesignsystem.com/data-visualization/getting-started/ |
| Google — People + AI Guidebook | https://pair.withgoogle.com/guidebook/ |
| Microsoft — Guidelines for Human-AI Interaction | https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ |
| Material Design — Motion | https://m3.material.io/styles/motion/overview |
| Deceptive Design | https://www.deceptive.design/ |
| Laws of UX (index only) | https://lawsofux.com/ |
| Figma help centre | https://help.figma.com/hc/en-us |

Gaps the corpus does not fill, built from the added sources above: Figma practice, Fitts's and Hick's laws,
motion, iconography and imagery, data visualisation, AI interfaces, ethics and dark patterns, and handoff.

## Adaptation rules

- Placement (15 minutes) runs three short probes: a critique of an unseen screen (heuristics and visual
  hierarchy), a hierarchy fix on a cluttered card, and a research question to turn into a plan. Frontend
  experience is never assumed to cover visual design or research; each area is proved here.
- Every lesson follows the corpus module brief: objectives, concepts, sources, theory, an example and a
  counter-example, frequent mistakes, then practice. Exercises rotate between analysis, reproduction,
  transformation, design, research and critique, and every unit from unit 4 on includes at least one critique.
- Exercises use the red-thread product when the subject prepares project work, and unseen interfaces for
  transfer and reviews.
- Difficulty rises from naming a principle, to applying it on a given screen, to choosing between methods or
  patterns and stating the trade-off.
- A unit compresses when its subjects are demonstrated cold on a different day: the learner goes straight to
  the unit's project step.
- Research and testing subjects need real participants to reach `independent` (see Research with real people).
- When the learner changes the red-thread product, the next project opens with a research catch-up on the new
  product.
- Survey subjects get a lesson and a short recall, never a graded exercise.
