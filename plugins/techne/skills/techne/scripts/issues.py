#!/usr/bin/env python3
"""The issues journal: an append-only record of Techne's own defects.

See docs/adr/0009-feedback-journal-is-an-append-only-workspace-file.md.
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


class IssueError(Exception):
    """The requested journal operation is not allowed."""


def journal_path(workspace: Path) -> Path:
    path = workspace / ".techne" / "issues.jsonl"
    if not path.is_file():
        # Workspaces created before the split kept the same journal here.
        legacy = workspace / ".techne" / "feedback.jsonl"
        if legacy.is_file():
            return legacy
    return path


def read(workspace: Path) -> list[dict]:
    """Return the journal's entries, ignoring lines that are not entries."""
    path = journal_path(workspace)
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and all(key in entry for key in REQUIRED_KEYS):
            entries.append(entry)
    return entries


def write(workspace: Path, entries: list[dict]) -> None:
    path = journal_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries), encoding="utf-8")


def next_id(entries: list[dict]) -> str:
    """Identify by the highest number used so far, never by list position."""
    used = []
    for entry in entries:
        raw = str(entry.get("id", ""))
        if raw.startswith("f") and raw[1:].isdigit():
            used.append(int(raw[1:]))
    return f"f{max(used, default=0) + 1}"


def add(workspace: Path, kind: str, text: str, origin: dict) -> dict:
    if kind not in TYPES:
        raise IssueError(f"Unknown issue type: {kind}. Use one of {', '.join(TYPES)}.")
    if not text.strip():
        raise IssueError("The issue text is empty.")
    entries = read(workspace)
    entry = {
        "version": SCHEMA_VERSION,
        "id": next_id(entries),
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "type": kind,
        "text": text.strip(),
        "activity": origin.get("activity"),
        "track": origin.get("track"),
        "status": "open",
    }
    write(workspace, [*entries, entry])
    return entry


def resolve(workspace: Path, entry_id: str, status: str) -> dict:
    if status not in STATUSES:
        raise IssueError(f"Unknown issue status: {status}. Use one of {', '.join(STATUSES)}.")
    entries = read(workspace)
    for entry in entries:
        if entry.get("id") == entry_id:
            entry["status"] = status
            entry["resolved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            write(workspace, entries)
            return entry
    raise IssueError(f"No issue with id {entry_id}.")


def select(workspace: Path, status: str | None, since: str | None) -> list[dict]:
    if status is not None and status not in STATUSES:
        raise IssueError(f"Unknown issue status: {status}. Use one of {', '.join(STATUSES)}.")
    if since is not None:
        try:
            date.fromisoformat(since)
        except ValueError as exc:
            raise IssueError(f"--since expects a date like 2026-09-19: {exc}") from exc
    selected = []
    for entry in read(workspace):
        if status is not None and entry.get("status", "open") != status:
            continue
        if since is not None and str(entry.get("at", ""))[:10] < since:
            continue
        selected.append(entry)
    return selected


def export(entries: list[dict], exported_on: date | None = None) -> str:
    """Render the journal as Markdown, grouped by type, newest first."""
    stamp = (exported_on or datetime.now().astimezone().date()).isoformat()
    lines = [f"# Techne issues — exported {stamp}", ""]
    if not entries:
        lines.append("No issue recorded for this selection.")
        return "\n".join(lines) + "\n"
    for kind in TYPES:
        group = sorted(
            (entry for entry in entries if entry.get("type") == kind),
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


def problems(workspace: Path) -> list[str]:
    """Validation errors in the journal, for validate_workspace.py."""
    path = journal_path(workspace)
    if not path.is_file():
        return []
    errors, seen = [], set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except ValueError:
            errors.append(f"issues.jsonl line {number} is not valid JSON")
            continue
        if not isinstance(entry, dict) or any(key not in entry for key in REQUIRED_KEYS):
            errors.append(f"issues.jsonl line {number} is missing required keys")
            continue
        if entry["type"] not in TYPES:
            errors.append(f"issues.jsonl line {number} has unknown type {entry['type']!r}")
        if entry["status"] not in STATUSES:
            errors.append(f"issues.jsonl line {number} has unknown status {entry['status']!r}")
        if entry["id"] in seen:
            errors.append(f"issues.jsonl has a duplicate id: {entry['id']}")
        seen.add(entry["id"])
    return errors
