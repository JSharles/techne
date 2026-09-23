# Techne

Techne is one Agent Skill that runs an intensive twelve-week bootcamp for a single learner persona: a self-taught React/Node developer, bootcamp-trained rather than engineering-school-trained, who wants to stay employable as generative AI reshapes the job market. This glossary fixes the words used across the skill, its references, and learner-facing text.

## Language

**Learner**:
The single person a workspace belongs to.
_Avoid_: student, user

**Program**:
A Markdown file that defines what is taught: its units, its subject catalogue, and five settings the method leaves open. Techne ships some; the learner writes others. A program never redefines the method.
_Avoid_: curriculum, track, course

**Enrolment**:
The learner's commitment to a program. Several run at once, each progressing on its own evidence.
_Avoid_: subscription

**Coverage**:
How much of a program's catalogue has been taught and demonstrated. Reaching full coverage is what ends a program; time never does.

**Session**:
One stretch of work on one program, whenever and for however long the learner chooses; the state script calls it a block. Techne keeps no schedule: the learner organises their own time, and a program advances in sessions, not in calendar days.
_Avoid_: slot, morning, afternoon, working day

**Activity**:
One unit of learner work inside a block: a lesson, an exercise, a review, or a placement probe. At most one evaluated activity is open at a time.

**Lesson**:
A short browser page that teaches a concept before practice: the problem, a mental model, a worked example, and quick checks.

**Exercise**:
Practice the learner writes by hand. Techne never supplies the implementation; hand-writing the code is the point of the programme.

**Placement test**:
The short, ungraded sequence of probes that finds a starting level, climbing from easy until the learner hits real difficulty. Each track has its own.
_Avoid_: baseline, diagnostic, exam

**Help level**:
How much assistance a piece of work received: H0 none, H1 a Socratic question, H2 a conceptual hint, H3 a precise lead, H4 the solution explained. Independence stops at H1.

**Evidence**:
One dated observation of work the learner did, naming the task, the help level, and the result. It is what moves a subject's state; declarations never do.
_Avoid_: score, grade

**Due review**:
A scheduled retrieval attempt on a subject already demonstrated, at J+2, J+7 and J+21 in calendar days. Reviews overdue by more than twice their interval are dropped and the subject steps down.

**Transfer deadline**:
The scheduled moment when an `independent` subject is to be reinvested in the red-thread project or the AI lab, which is what earns `transferred`.

**Ideation**:
The first phase of the red-thread project: finding, from what drives the learner, an idea they want to build. It has no deadline and runs on a map of decisions settled one per session, in `.techne/project/MAP.md`, opened with the `project` command. Techne questions; the learner decides.
_Avoid_: brainstorm, discovery

**Building the roadmap**:
The second phase of the red-thread project, three project sessions at most: problem, scope, teaching value, architecture and roadmap, ending in the learner's commitment to the roadmap.
_Avoid_: exploration

**Roadmap**:
The red-thread project's `docs/ROADMAP.md`, written while building the roadmap: the single reference from which tickets and the lessons that prepare them derive. It changes only by an explicit, recorded decision.
_Avoid_: backlog, plan

**Core**:
The set of subjects a program takes to demonstrated independence, for the T-shaped Product Engineer program: TypeScript and JavaScript, React and Next.js, NestJS and backend, SQL and data modelling, DSA up to graphs, tests and debugging, applied architecture, and the delivery flow (Git, pull requests, review, CI).
_Avoid_: priority lane, must-have

**Survey**:
A subject the programme covers for working literacy only, with no mastery required: distributed systems, large-scale system design, and the day-to-day level of security, performance, observability, and delivery.
_Avoid_: optional, nice-to-have

**Mastery map**:
The per-subject record of demonstrated level, its date, and the evidence behind it, including subjects not yet started. A subject is `not_started`, `discovered`, `assisted`, `independent`, `transferred`, or `blocked` after three failures. Shown in the browser and through `status`.
_Avoid_: score, progress percentage

**Calibration**:
The conversation that changes how Techne teaches. A preference — lesson length, more theory, pace — is applied at once and kept in the learner profile; a change touching evidence, the programme, or assessment goes through discussion, approval, and a recorded decision.

**Weekly assessment**:
The blunt review written after every six sessions of a program: what moved, what stalled, what is fragile, and the learner's real pace. After sessions 20, 40 and 60 it also compares the mastery map to what a senior React/Node developer is expected to know.
_Avoid_: progress report, recap

**Issue**:
A defect or an improvement the learner reports about Techne itself, recorded with the activity it came from and exported for whoever maintains the skill. Never learning evidence.
_Avoid_: bug report, complaint

**Feedback**:
What the learner tells Techne about the programme in progress: a preference, applied at once and kept in the profile, or a request to change the method, which goes through calibration.
_Avoid_: issue, report

**Light session**:
A session of reviews and reading only, with no new subject, which Techne proposes, never imposes, when results degrade.
_Avoid_: rest day, day off

**AI lab**:
The single Python repository that grows through the Applied AI track and becomes the capstone.
_Avoid_: project, studio
