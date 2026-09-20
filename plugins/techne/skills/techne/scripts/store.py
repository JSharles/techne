#!/usr/bin/env python3
"""The one place learner state is read from and written to.

State lives in one SQLite database in the workspace; `state.py` applies every
transition through this module, the validator and the initializer read and seed
it, and the browser reads the progress view rendered here. Everything written
for a human stays Markdown beside it.
See docs/adr/0011-sqlite-is-the-state-store.md.

Functions come in pairs: those taking a workspace (the learner's directory) and
those taking a state root (the `.techne` directory inside it), because the
bundled seed is validated as a state root with no workspace around it.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path


DATABASE = "techne.db"
SEED_FILE = "STATE.json"
LEGACY_JOURNAL = "feedback.jsonl"
PROGRESS_VIEW = ("browser", "progress.json")

# These have tables of their own; every other key is kept as a document, so a
# new field never goes missing just because the store had not heard of it.
TABLE_KEYS = ("mastery", "reviews_due", "transfers_due", "enrolments", "issues")

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS mastery (
    subject TEXT PRIMARY KEY,
    state TEXT NOT NULL,
    last_evidence_at TEXT,
    failures INTEGER NOT NULL DEFAULT 0,
    evidence TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS reviews_due (
    position INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    due_on TEXT NOT NULL,
    interval_days INTEGER NOT NULL,
    reason TEXT
);
CREATE TABLE IF NOT EXISTS transfers_due (subject TEXT PRIMARY KEY, due_on TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS enrolments (
    program TEXT PRIMARY KEY,
    enrolled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    data TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS issues (
    id TEXT PRIMARY KEY,
    at TEXT NOT NULL,
    type TEXT NOT NULL,
    text TEXT NOT NULL,
    activity TEXT,
    track TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    resolved_at TEXT,
    version INTEGER NOT NULL DEFAULT 1
);
"""

class StoreError(Exception):
    """The store is missing or unreadable."""


def state_root(workspace: Path) -> Path:
    return workspace / ".techne"


def database_path(root: Path) -> Path:
    return root / DATABASE


def seed_path(root: Path) -> Path:
    return root / SEED_FILE


def exists_at(root: Path) -> bool:
    return database_path(root).is_file() or seed_path(root).is_file()


def exists(workspace: Path) -> bool:
    return exists_at(state_root(workspace))


def connect(root: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path(root))
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def read_seed(root: Path) -> dict | None:
    """The JSON document a workspace was seeded from, or left by an older Techne."""
    path = seed_path(root)
    if not path.is_file():
        return None
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise StoreError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise StoreError(f"Invalid Techne state in {path}")
    return document


def load_at(root: Path) -> dict:
    if not database_path(root).is_file():
        seed = read_seed(root)
        if seed is None:
            raise StoreError(f"No Techne state at {database_path(root)}")
        return seed

    state: dict = {}
    with closing(connect(root)) as connection:
        for row in connection.execute("SELECT key, value FROM documents"):
            state[row["key"]] = json.loads(row["value"])
        state["mastery"] = {
            row["subject"]: {
                "state": row["state"],
                "last_evidence_at": row["last_evidence_at"],
                "failures": row["failures"],
                "evidence": json.loads(row["evidence"]),
            }
            for row in connection.execute("SELECT * FROM mastery ORDER BY subject")
        }
        state["reviews_due"] = [
            {
                key: row[key]
                for key in ("subject", "due_on", "interval_days", "reason")
                if not (key == "reason" and row[key] is None)
            }
            for row in connection.execute("SELECT * FROM reviews_due ORDER BY position")
        ]
        state["transfers_due"] = [
            {"subject": row["subject"], "due_on": row["due_on"]}
            for row in connection.execute("SELECT * FROM transfers_due ORDER BY due_on, subject")
        ]
        state["enrolments"] = [
            {
                **json.loads(row["data"]),
                "program": row["program"],
                "enrolled_at": row["enrolled_at"],
                "status": row["status"],
            }
            for row in connection.execute("SELECT * FROM enrolments ORDER BY enrolled_at, program")
        ]
        state["issues"] = [
            {key: row[key] for key in row.keys() if row[key] is not None}
            for row in connection.execute("SELECT * FROM issues ORDER BY at, id")
        ]
    return state


def load(workspace: Path) -> dict:
    return load_at(state_root(workspace))


def save_at(root: Path, state: dict) -> None:
    root.mkdir(parents=True, exist_ok=True)
    with closing(connect(root)) as connection:
        with connection:
            connection.execute("DELETE FROM documents")
            connection.executemany(
                "INSERT INTO documents (key, value) VALUES (?, ?)",
                [
                    (key, json.dumps(value, ensure_ascii=False))
                    for key, value in state.items()
                    if key not in TABLE_KEYS
                ],
            )

            connection.execute("DELETE FROM mastery")
            connection.executemany(
                "INSERT INTO mastery (subject, state, last_evidence_at, failures, evidence) VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        subject,
                        entry.get("state", "not_started"),
                        entry.get("last_evidence_at"),
                        int(entry.get("failures", 0)),
                        json.dumps(entry.get("evidence", []), ensure_ascii=False),
                    )
                    for subject, entry in state.get("mastery", {}).items()
                ],
            )

            connection.execute("DELETE FROM reviews_due")
            connection.executemany(
                "INSERT INTO reviews_due (subject, due_on, interval_days, reason) VALUES (?, ?, ?, ?)",
                [
                    (item["subject"], item["due_on"], int(item.get("interval_days", 2)), item.get("reason"))
                    for item in state.get("reviews_due", [])
                ],
            )

            connection.execute("DELETE FROM transfers_due")
            connection.executemany(
                "INSERT INTO transfers_due (subject, due_on) VALUES (?, ?)",
                [(item["subject"], item["due_on"]) for item in state.get("transfers_due", [])],
            )

            connection.execute("DELETE FROM enrolments")
            connection.executemany(
                "INSERT INTO enrolments (program, enrolled_at, status, data) VALUES (?, ?, ?, ?)",
                [
                    (
                        item["program"],
                        item.get("enrolled_at", ""),
                        item.get("status", "active"),
                        json.dumps(
                            {key: value for key, value in item.items() if key not in ("program", "enrolled_at", "status")},
                            ensure_ascii=False,
                        ),
                    )
                    for item in state.get("enrolments", [])
                ],
            )

            connection.execute("DELETE FROM issues")
            connection.executemany(
                "INSERT INTO issues (id, at, type, text, activity, track, status, resolved_at, version)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        item["id"],
                        item["at"],
                        item["type"],
                        item["text"],
                        item.get("activity"),
                        item.get("track"),
                        item.get("status", "open"),
                        item.get("resolved_at"),
                        int(item.get("version", 1)),
                    )
                    for item in state.get("issues", [])
                ],
            )

    seed = seed_path(root)
    if seed.is_file():
        # The seed document has done its job; the database is the state now.
        seed.unlink()
    write_progress_view(root, state)


def save(workspace: Path, state: dict) -> None:
    save_at(state_root(workspace), state)


def brief(state: dict) -> dict:
    """What an agent needs at the start of a turn, instead of the whole state."""
    mastery = state.get("mastery", {})
    counted: dict[str, int] = {}
    for entry in mastery.values():
        name = entry.get("state", "not_started")
        counted[name] = counted.get(name, 0) + 1
    return {
        "status": state.get("status"),
        "language": state.get("language"),
        "mode": state.get("mode"),
        "day": state.get("day"),
        "progress": state.get("progress"),
        "current": state.get("current"),
        "enrolments": [item["program"] for item in state.get("enrolments", [])],
        "mastery_counts": counted,
        "reviews_due": len(state.get("reviews_due", [])),
        "transfers_due": len(state.get("transfers_due", [])),
        "open_issues": sum(1 for item in state.get("issues", []) if item.get("status", "open") == "open"),
    }


def progress_path(root: Path) -> Path:
    return root.joinpath(*PROGRESS_VIEW)


def write_progress_view(root: Path, state: dict) -> None:
    """Render what the browser needs, so it never reads the store itself."""
    path = progress_path(root)
    if not path.parent.is_dir():
        return
    view = {
        "language": state.get("language"),
        "mastery": state.get("mastery", {}),
        "reviews_due": state.get("reviews_due", []),
    }
    path.write_text(json.dumps(view, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_progress_view(root: Path) -> dict:
    path = progress_path(root)
    if not path.is_file():
        return {}
    try:
        view = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return {}
    return view if isinstance(view, dict) else {}
