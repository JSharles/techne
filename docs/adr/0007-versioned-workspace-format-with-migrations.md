# The workspace format is versioned and migrated, never reset

Learner state is the only irreplaceable thing Techne holds: months of evidence, review schedules, and a mastery map. Early skill releases changed that format three times, and the only answer offered was `reset`, which throws the evidence away. `STATE.json` therefore carries a format `version`, and the skill ships migrations that move an older workspace forward.

On an unknown or older format, Techne says so plainly and offers the migration; it never silently rewrites state it does not understand, and never proposes a reset as a way to fix a format mismatch.

## Consequences

- Every change to the state shape now needs a migration step and a test that an older workspace survives it.
- `reset` goes back to being what it is for — starting the programme over on purpose — rather than a repair tool.
