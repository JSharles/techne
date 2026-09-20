#!/usr/bin/env python3
"""Apply every Techne state transition, so the agent never edits STATE.json.

See docs/adr/0004-state-transitions-belong-to-a-script.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import feedback as journal
from catalogue import subjects
from workspace_registry import default_config_path, resolve_workspace


SKILL_ROOT = Path(__file__).resolve().parents[1]
FORMAT_VERSION = 2
RECENT_SESSION_HOURS = 12
STATES = ("not_started", "discovered", "assisted", "independent", "transferred", "blocked")
LADDER = ("not_started", "discovered", "assisted", "independent", "transferred")
HELP_LEVELS = tuple(f"H{level}" for level in range(5))
REVIEW_STEPS = (2, 7, 21)
TRANSFER_DELAY_DAYS = 7
BLOCKED_RETRY_DAYS = 14
FAILURES_BEFORE_BLOCKED = 3
EVIDENCE_KEPT = 5
BLOCKS = ("engineering", "ai")


class StateError(Exception):
    """The requested transition is not allowed."""


def today() -> date:
    return datetime.now().astimezone().date()


def now_stamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(workspace: Path, allow_old_format: bool = False) -> tuple[Path, dict]:
    path = workspace / ".techne" / "STATE.json"
    if not path.is_file():
        raise StateError(f"No Techne state at {path}")
    state = json.loads(path.read_text(encoding="utf-8"))
    version = state.get("version")
    if not allow_old_format and version != FORMAT_VERSION:
        if isinstance(version, int) and version < FORMAT_VERSION:
            raise StateError(
                f"This workspace uses state format {version}, the skill expects {FORMAT_VERSION}. "
                "Run 'state.py migrate' to bring it forward; the learner's evidence is preserved."
            )
        raise StateError(f"Unknown state format: {version!r}. Update Techne rather than editing state by hand.")
    return path, state


def migrate(state: dict) -> list[str]:
    """Bring an older workspace forward without losing learner evidence."""
    version = state.get("version")
    if version == FORMAT_VERSION:
        return []
    if not isinstance(version, int) or version > FORMAT_VERSION:
        raise StateError(f"Unknown state format: {version!r}.")
    applied = []
    if version < 2:
        day = state.setdefault("day", {})
        if "curriculum" in day:
            day["engineering"] = day.pop("curriculum")
        if "project" in day:
            day["ai"] = day.pop("project")
        if "project" in state:
            state["ai"] = state.pop("project")
        state.pop("reviews", None)
        state.setdefault("reviews_due", [])
        state.setdefault("transfers_due", [])
        state.setdefault("progress", {"engineering_days": 0, "ai_days": 0})
        state.setdefault("red_thread", {"domain": None, "repository": None, "milestone": None})
        state.setdefault("ai", {"phase": "not_started", "week": None, "lab_repository": None, "provider": None, "capstone": None})
        mastery = state.get("mastery")
        if isinstance(mastery, dict):
            # Old entries were per domain with a score or a level, not per subject,
            # so they cannot become subject states. Keep them as history.
            legacy = {
                key: entry
                for key, entry in mastery.items()
                if "." not in key or not (isinstance(entry, dict) and entry.get("state") in STATES)
            }
            if legacy:
                state["legacy_mastery"] = {**state.get("legacy_mastery", {}), **legacy}
                state["mastery"] = {key: entry for key, entry in mastery.items() if key not in legacy}
                applied.append(f"kept {len(legacy)} old per-domain entries as legacy_mastery")
        if state.get("current", {}).get("help_level") in ("H5", "H6"):
            state["current"]["help_level"] = "H4"
            applied.append("clamped help level to H4")
        applied.append("migrated state from format 1 to 2")
    state["version"] = FORMAT_VERSION
    return applied


def note_session(state: dict, session: str | None) -> str | None:
    """Record which agent session is writing, and warn when another one was active."""
    if not session:
        return None
    previous = state.get("session") or {}
    warning = None
    if previous.get("id") and previous["id"] != session:
        try:
            seen = datetime.fromisoformat(previous["seen_at"])
            hours = (datetime.now().astimezone() - seen).total_seconds() / 3600
        except (KeyError, ValueError):
            hours = None
        if hours is not None and hours < RECENT_SESSION_HOURS:
            warning = "Another Techne session wrote this workspace recently; re-read the state before continuing."
    state["session"] = {"id": session, "seen_at": now_stamp()}
    return warning


def save(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def entry_for(state: dict, subject: str) -> dict:
    mastery = state.setdefault("mastery", {})
    return mastery.setdefault(subject, {"state": "not_started", "last_evidence_at": None, "failures": 0, "evidence": []})


def queue(state: dict, name: str) -> list:
    return state.setdefault(name, [])


def drop_from_queue(state: dict, name: str, subject: str) -> None:
    state[name] = [item for item in queue(state, name) if item["subject"] != subject]


def schedule_reviews(state: dict, subject: str, start: date) -> None:
    drop_from_queue(state, "reviews_due", subject)
    for interval in REVIEW_STEPS:
        queue(state, "reviews_due").append(
            {"subject": subject, "due_on": (start + timedelta(days=interval)).isoformat(), "interval_days": interval}
        )


def schedule_transfer(state: dict, subject: str, start: date) -> None:
    drop_from_queue(state, "transfers_due", subject)
    queue(state, "transfers_due").append(
        {"subject": subject, "due_on": (start + timedelta(days=TRANSFER_DELAY_DAYS)).isoformat()}
    )


def set_mastery(state: dict, subject: str, target: str, evidence: str | None, help_level: str | None, known: set[str]) -> dict:
    if subject not in known:
        raise StateError(f"Unknown subject identifier: {subject}. Use one from the curriculum catalogues.")
    if target not in STATES:
        raise StateError(f"Unknown mastery state: {target}. Use one of {', '.join(STATES)}.")
    if help_level is not None and help_level not in HELP_LEVELS:
        raise StateError(f"Unknown help level: {help_level}. Use one of {', '.join(HELP_LEVELS)}.")
    if target in ("independent", "transferred") and help_level in ("H2", "H3", "H4"):
        raise StateError(f"Work helped at {help_level} cannot be {target}; record it as assisted.")

    entry = entry_for(state, subject)
    entry["state"] = target
    entry["last_evidence_at"] = now_stamp()
    if evidence:
        line = f"{today().isoformat()} · {help_level or 'H0'} · {evidence}"
        entry["evidence"] = ([*entry.get("evidence", []), line])[-EVIDENCE_KEPT:]

    if target == "independent":
        entry["failures"] = 0
        schedule_reviews(state, subject, today())
        schedule_transfer(state, subject, today())
    elif target == "transferred":
        entry["failures"] = 0
        drop_from_queue(state, "transfers_due", subject)
    elif target in ("not_started", "discovered", "assisted"):
        drop_from_queue(state, "transfers_due", subject)
    return entry


def step_down(state: dict, subject: str, reason: str) -> dict:
    entry = entry_for(state, subject)
    current = entry.get("state", "not_started")
    if current in LADDER:
        entry["state"] = LADDER[max(LADDER.index(current) - 1, 0)]
    entry["last_evidence_at"] = now_stamp()
    entry["evidence"] = ([*entry.get("evidence", []), f"{today().isoformat()} · {reason}"])[-EVIDENCE_KEPT:]
    drop_from_queue(state, "transfers_due", subject)
    return entry


def record_failure(state: dict, subject: str, known: set[str]) -> dict:
    if subject not in known:
        raise StateError(f"Unknown subject identifier: {subject}.")
    entry = entry_for(state, subject)
    entry["failures"] = int(entry.get("failures", 0)) + 1
    entry["last_evidence_at"] = now_stamp()
    if entry["failures"] >= FAILURES_BEFORE_BLOCKED:
        entry["state"] = "blocked"
        drop_from_queue(state, "reviews_due", subject)
        drop_from_queue(state, "transfers_due", subject)
        queue(state, "reviews_due").append(
            {
                "subject": subject,
                "due_on": (today() + timedelta(days=BLOCKED_RETRY_DAYS)).isoformat(),
                "interval_days": BLOCKED_RETRY_DAYS,
                "reason": "blocked-retry",
            }
        )
    return entry


def due_reviews(state: dict, limit: int | None) -> tuple[list[dict], list[dict]]:
    """Return (due, dropped). Reviews overdue by more than twice their interval are dropped."""
    current = today()
    due, kept, dropped = [], [], []
    for item in queue(state, "reviews_due"):
        due_on = date.fromisoformat(item["due_on"])
        if due_on > current:
            kept.append(item)
            continue
        if (current - due_on).days > 2 * int(item.get("interval_days", 2)):
            dropped.append(item)
            continue
        due.append(item)

    fragile = {"assisted", "discovered"}
    due.sort(key=lambda item: (state.get("mastery", {}).get(item["subject"], {}).get("state") not in fragile, item["due_on"]))
    for subject in dict.fromkeys(item["subject"] for item in dropped):
        # One step down per subject, however many of its reviews went stale.
        step_down(state, subject, "révision abandonnée (trop en retard)")
    state["reviews_due"] = kept + due
    return (due if limit is None else due[:limit]), dropped


def due_transfers(state: dict) -> list[dict]:
    current = today()
    return [item for item in queue(state, "transfers_due") if date.fromisoformat(item["due_on"]) <= current]


def record_review(state: dict, subject: str, passed: bool, known: set[str]) -> dict:
    if subject not in known:
        raise StateError(f"Unknown subject identifier: {subject}.")
    entry = entry_for(state, subject)
    done = [item for item in queue(state, "reviews_due") if item["subject"] == subject]
    if passed:
        if done:
            first = min(done, key=lambda item: item["due_on"])
            state["reviews_due"] = [item for item in queue(state, "reviews_due") if item is not first]
        entry["last_evidence_at"] = now_stamp()
        entry["evidence"] = ([*entry.get("evidence", []), f"{today().isoformat()} · révision réussie"])[-EVIDENCE_KEPT:]
        return entry
    drop_from_queue(state, "reviews_due", subject)
    entry = step_down(state, subject, "révision ratée")
    queue(state, "reviews_due").append(
        {"subject": subject, "due_on": (today() + timedelta(days=2)).isoformat(), "interval_days": 2}
    )
    return entry


def checkpoint(state: dict, note: str | None, help_level: str | None, status: str) -> dict:
    current = state.setdefault("current", {})
    current["status"] = status
    current["checkpointed_at"] = now_stamp()
    if help_level:
        if help_level not in HELP_LEVELS:
            raise StateError(f"Unknown help level: {help_level}.")
        current["help_level"] = help_level
    if note:
        current["checkpoint_note"] = note
    if status == "closed":
        block = state.get("day", {}).get("active_block")
        if block in BLOCKS:
            progress = state.setdefault("progress", {"engineering_days": 0, "ai_days": 0})
            key = f"{block}_days"
            progress[key] = int(progress.get(key, 0)) + 1
            state.setdefault("day", {})[block] = "closed"
    return current


def switch_block(state: dict, block: str) -> dict:
    if block not in BLOCKS:
        raise StateError(f"Unknown block: {block}. Use one of {', '.join(BLOCKS)}.")
    day = state.setdefault("day", {})
    day["active_block"] = block
    day.setdefault(block, "in_progress")
    if day.get(block) == "pending":
        day[block] = "in_progress"
    return day


def ingest_events(state: dict, workspace: Path, known: set[str]) -> dict:
    """Apply mechanical browser evidence; hand everything else back to the agent."""
    path = workspace / ".techne" / "events" / "browser.jsonl"
    consumed = int(state.setdefault("browser", {}).get("last_event_line", 0))
    applied, for_agent = [], []
    if path.is_file():
        lines = path.read_text(encoding="utf-8").splitlines()
        for line in lines[consumed:]:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            subject = event.get("subject")
            if event.get("kind") == "quiz" and event.get("correct") and subject in known:
                entry = entry_for(state, subject)
                if entry.get("state", "not_started") == "not_started":
                    set_mastery(state, subject, "discovered", "question de leçon réussie", "H0", known)
                    applied.append(subject)
                    continue
            for_agent.append(event)
        state["browser"]["last_event_line"] = len(lines)
    return {"applied": applied, "for_agent": for_agent}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply a Techne state transition.")
    parser.add_argument("--workspace", type=Path, help="Learning workspace (default: resolved like the skill does)")
    parser.add_argument("--config", type=Path, default=default_config_path(), help="Global workspace registry")
    parser.add_argument("--session", help="Opaque identifier of the agent session, to detect concurrent sessions")
    sub = parser.add_subparsers(dest="command", required=True)

    mastery = sub.add_parser("mastery", help="Record a mastery state for one subject")
    mastery.add_argument("subject")
    mastery.add_argument("state", choices=STATES)
    mastery.add_argument("--evidence")
    mastery.add_argument("--help-level", choices=HELP_LEVELS)

    fail = sub.add_parser("fail", help="Record a failed attempt; three failures block the subject")
    fail.add_argument("subject")

    review = sub.add_parser("review", help="List or record due reviews")
    review.add_argument("--due", action="store_true")
    review.add_argument("--limit", type=int, default=3)
    review.add_argument("--record", metavar="SUBJECT")
    review.add_argument("--result", choices=("pass", "fail"))

    transfer = sub.add_parser("transfer", help="List subjects due for transfer into a project")
    transfer.add_argument("--due", action="store_true")

    check = sub.add_parser("checkpoint", help="Checkpoint the current activity")
    check.add_argument("--note")
    check.add_argument("--help-level", choices=HELP_LEVELS)

    close = sub.add_parser("close", help="Close the current block and count a working day")
    close.add_argument("--note")

    block = sub.add_parser("block", help="Switch the active block")
    block.add_argument("name", choices=BLOCKS)

    feedback = sub.add_parser("feedback", help="Record, list, resolve or export learner feedback")
    actions = feedback.add_subparsers(dest="action", required=True)

    record = actions.add_parser("add", help="Record a new entry")
    record.add_argument("--type", choices=journal.TYPES, required=True)
    record.add_argument("--text", required=True)
    record.add_argument("--activity", help="Activity the entry came from (default: the current activity)")
    record.add_argument("--track", help="Track the entry came from (default: the current track)")

    listing = actions.add_parser("list", help="List entries as JSON")
    listing.add_argument("--status", choices=journal.STATUSES)
    listing.add_argument("--since", metavar="DATE")

    exporting = actions.add_parser("export", help="Print the entries as Markdown grouped by type")
    exporting.add_argument("--status", choices=journal.STATUSES, default="open")
    exporting.add_argument("--since", metavar="DATE")

    resolving = actions.add_parser("resolve", help="Mark an entry applied or dismissed")
    resolving.add_argument("id")
    resolving.add_argument("--status", choices=journal.STATUSES, default="applied")

    sub.add_parser("ingest-events", help="Apply mechanical browser evidence")
    sub.add_parser("migrate", help="Bring an older workspace forward to the current state format")
    sub.add_parser("show", help="Print the current state as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    try:
        workspace = args.workspace.expanduser().resolve() if args.workspace else resolve_workspace(Path("."), args.config)
        path, state = load(workspace, allow_old_format=args.command == "migrate")
        known = subjects(SKILL_ROOT)
        warning = note_session(state, args.session)
        result: object = None

        if args.command == "mastery":
            result = set_mastery(state, args.subject, args.state, args.evidence, args.help_level, known)
        elif args.command == "fail":
            result = record_failure(state, args.subject, known)
        elif args.command == "review":
            if args.record:
                if args.result is None:
                    raise StateError("--record requires --result pass|fail")
                result = record_review(state, args.record, args.result == "pass", known)
            else:
                due, dropped = due_reviews(state, args.limit)
                result = {"due": due, "dropped": dropped}
        elif args.command == "transfer":
            result = {"due": due_transfers(state)}
        elif args.command == "checkpoint":
            result = checkpoint(state, args.note, args.help_level, "checkpointed")
        elif args.command == "close":
            result = checkpoint(state, args.note, None, "closed")
        elif args.command == "block":
            result = switch_block(state, args.name)
        elif args.command == "feedback":
            if args.action == "add":
                current = state.get("current", {})
                origin = {
                    "activity": args.activity or current.get("id"),
                    "track": args.track or current.get("track"),
                }
                result = journal.add(workspace, args.type, args.text, origin)
            elif args.action == "resolve":
                result = journal.resolve(workspace, args.id, args.status)
            elif args.action == "export":
                # A report reads; it never writes state.
                print(journal.export(journal.select(workspace, args.status, args.since)), end="")
                return 0
            else:
                result = {"entries": journal.select(workspace, args.status, args.since)}
        elif args.command == "ingest-events":
            result = ingest_events(state, workspace, known)
        elif args.command == "migrate":
            result = {"applied": migrate(state), "version": state["version"]}
        elif args.command == "show":
            result = state

        save(path, state)
        if warning:
            print(warning, file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (StateError, journal.FeedbackError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"Techne state transition failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
