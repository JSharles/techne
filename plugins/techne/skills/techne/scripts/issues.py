#!/usr/bin/env python3
"""The issues journal: what the learner reports about Techne itself.

Entries are append-only in spirit — they are only ever added, or marked handled
— and they are never learning evidence. They live in the state store with
everything else that is computed (ADR 0009, as amended by ADR 0011).
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path


TYPES = ("bug", "friction", "idea")
STATUSES = ("open", "applied", "dismissed")
HEADINGS = {"bug": "Bugs", "friction": "Frictions", "idea": "Ideas"}
SCHEMA_VERSION = 1
REQUIRED_KEYS = ("id", "at", "type", "text", "status")
LEGACY_FILES = ("issues.jsonl", "feedback.jsonl")


class IssueError(Exception):
    """The requested journal operation is not allowed."""


def entries(state: dict) -> list[dict]:
    recorded = state.get("issues")
    return recorded if isinstance(recorded, list) else []


def next_id(recorded: list[dict]) -> str:
    """Identify by the highest number used so far, never by list position."""
    used = []
    for entry in recorded:
        raw = str(entry.get("id", ""))
        if raw.startswith("f") and raw[1:].isdigit():
            used.append(int(raw[1:]))
    return f"f{max(used, default=0) + 1}"


def add(state: dict, kind: str, text: str, origin: dict) -> dict:
    if kind not in TYPES:
        raise IssueError(f"Unknown issue type: {kind}. Use one of {', '.join(TYPES)}.")
    if not text.strip():
        raise IssueError("The issue text is empty.")
    recorded = entries(state)
    entry = {
        "version": SCHEMA_VERSION,
        "id": next_id(recorded),
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "type": kind,
        "text": text.strip(),
        "activity": origin.get("activity"),
        "track": origin.get("track"),
        "status": "open",
    }
    state["issues"] = [*recorded, entry]
    return entry


def resolve(state: dict, entry_id: str, status: str) -> dict:
    if status not in STATUSES:
        raise IssueError(f"Unknown issue status: {status}. Use one of {', '.join(STATUSES)}.")
    for entry in entries(state):
        if entry.get("id") == entry_id:
            entry["status"] = status
            entry["resolved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            return entry
    raise IssueError(f"No issue with id {entry_id}.")


def select(state: dict, status: str | None, since: str | None) -> list[dict]:
    if status is not None and status not in STATUSES:
        raise IssueError(f"Unknown issue status: {status}. Use one of {', '.join(STATUSES)}.")
    if since is not None:
        try:
            date.fromisoformat(since)
        except ValueError as exc:
            raise IssueError(f"--since expects a date like 2026-09-19: {exc}") from exc
    selected = []
    for entry in entries(state):
        if status is not None and entry.get("status", "open") != status:
            continue
        if since is not None and str(entry.get("at", ""))[:10] < since:
            continue
        selected.append(entry)
    return selected


def export(recorded: list[dict], exported_on: date | None = None) -> str:
    """Render the journal as Markdown, grouped by type, newest first."""
    stamp = (exported_on or datetime.now().astimezone().date()).isoformat()
    lines = [f"# Techne issues — exported {stamp}", ""]
    if not recorded:
        lines.append("No issue recorded for this selection.")
        return "\n".join(lines) + "\n"
    for kind in TYPES:
        group = sorted(
            (entry for entry in recorded if entry.get("type") == kind),
            key=lambda entry: str(entry.get("at", "")),
            reverse=True,
        )
        if not group:
            continue
        lines += [f"## {HEADINGS[kind]} ({len(group)})", ""]
        for entry in group:
            context = " · ".join(str(part) for part in (entry.get("activity"), entry.get("track")) if part)
            suffix = f" — {context}" if context else ""
            status = "" if entry.get("status", "open") == "open" else f" [{entry['status']}]"
            lines.append(f"- **{entry.get('id', '?')}** · {str(entry.get('at', ''))[:10]}{suffix}{status}")
            lines.append(f"  {entry.get('text', '').strip()}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def problems(state: dict) -> list[str]:
    """Validation errors in the journal, for validate_workspace.py."""
    errors, seen = [], set()
    for position, entry in enumerate(entries(state), start=1):
        if not isinstance(entry, dict) or any(key not in entry for key in REQUIRED_KEYS):
            errors.append(f"issue {position} is missing required keys")
            continue
        if entry["type"] not in TYPES:
            errors.append(f"issue {entry['id']} has unknown type {entry['type']!r}")
        if entry["status"] not in STATUSES:
            errors.append(f"issue {entry['id']} has unknown status {entry['status']!r}")
        if entry["id"] in seen:
            errors.append(f"the journal has a duplicate issue id: {entry['id']}")
        seen.add(entry["id"])
    return errors


IMPORTED_SUFFIX = ".imported"


def read_legacy_journal(root: Path) -> tuple[list[dict], list[str]]:
    """Import entries a workspace left on disk before the storage move.

    The learner's file is kept, renamed, never deleted, and anything unreadable
    is reported rather than silently dropped.
    """
    recorded: list[dict] = []
    problems: list[str] = []
    for name in LEGACY_FILES:
        path = root / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                problems.append(f"{name} line {number} is not valid JSON and was not imported")
                continue
            if isinstance(entry, dict) and all(key in entry for key in REQUIRED_KEYS):
                recorded.append(entry)
            else:
                problems.append(f"{name} line {number} is missing required keys and was not imported")
        path.rename(path.with_suffix(path.suffix + IMPORTED_SUFFIX))
    return recorded, problems
