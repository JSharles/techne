# The delivery flow joins the T-shaped Product Engineer program

ADR 0002 left Git and code review out of the programme because the learner practised them daily at work. That premise no longer holds: the learner is now looking for work, so no job exercises these skills for them. The program was also renamed T-shaped Product Engineer: an engineer who ships a product end to end, for whom Git, pull requests, review and a pipeline are how every change reaches production, and what a hiring team sees on the first day.

The program therefore gains a core domain, `flow.*`, of ten subjects: commits, branches, pull requests, review, commit conventions, merge and rebase, conflicts, history recovery, the CI pipeline, and slicing a ticket. Each subject enters the sequence in the phase where the red-thread project first needs it. `survey.ci` is removed, since `flow.ci-pipeline` covers it at core depth; deployment, containers and rollback stay in the survey.

How Techne reviews the learner's pull requests is written in the method, in `references/operations.md`, not in the program file: review comments are help, and help levels belong to the method, which a program never redefines (ADR 0010).

The program keeps its identifier `engineering`, so enrolments, working days and schedules carry over; only its title and its content change.

## Consequences

- From weeks 3–4, every change to the red-thread project reaches the main branch through a pull request, which is where `flow.*` subjects earn `transferred`.
- Ten core subjects are added, so the program takes longer to cover; most of the practice happens on project work the learner is doing anyway.
- Any evidence already recorded on `survey.ci` becomes off-programme and stays visible as such.
