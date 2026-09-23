# Each program keeps its own evidence

ADR 0010 shared subjects across programs by identifier, so a subject proved in one program counted in every other that listed it. When the learner wrote a senior frontend program next to the Engineering program, that sharing made the estimates and the coverage of one program depend on progress made in the other, and the learner asked for the opposite: each course is its own, and Techne must not look elsewhere to decide what is already known.

Programs are now isolated. A domain prefix belongs to one program alone, and enrolment refuses a program that shares a prefix with one the learner follows or has followed, whatever the domain's title. Two programs may teach the same notion; the learner proves it in each, in that program's context. Nothing in the store changes: evidence is still keyed by subject identifier, and isolation comes from identifiers never crossing programs.

The survey, which was recognised by the shared prefix `survey.*`, is now any catalogue domain titled `Survey`, so each program can have its own.

## Consequences

- A notion taught by two programs is learned and proved twice; the second time is usually faster, and it is measured, not assumed.
- A program written before this decision that reuses another's prefixes must rename them before enrolling.
- The shipped programs already use disjoint prefixes, so existing evidence is untouched.
