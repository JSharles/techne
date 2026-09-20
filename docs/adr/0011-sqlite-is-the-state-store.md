# SQLite holds what is computed; Markdown holds what is read

The skill requires the agent to read the whole learner state at the start of every turn. With per-subject mastery, review and transfer queues, several enrolled programs and a journal, that file heads for a hundred kilobytes — roughly twenty thousand tokens a turn to retrieve three useful facts. State therefore moves into a single SQLite database in the workspace, queried through `state.py`, which asks only for what it needs.

Everything written for a human stays Markdown in the workspace: lessons, the current activity, the session log, decisions, the profile, the schedule, and the learner's own programs. The workspace stays navigable in an editor or in Obsidian, and the database is never the only trace of what happened.

Alternatives were weighed: plain JSON is what we are leaving; TinyDB, shelve and pickle add no atomicity or constraints; DuckDB targets analytics; LMDB and RocksDB are binary key-value stores with native dependencies; a server would break offline use. SQLite ships with Python, is transactional, and is a single file to copy.

## Consequences

- `state.py show` renders a readable state and `state.py export` writes a JSON backup, so nothing is locked behind a binary format.
- Migration from the JSON formats is automatic and preserves evidence by subject identifier, as ADR 0007 requires.
- Concurrent sessions become a database concern rather than a race between whole-file rewrites.
