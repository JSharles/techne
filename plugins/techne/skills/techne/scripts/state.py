#!/usr/bin/env python3
"""Apply every Techne state transition, so the agent never edits the state store.

See docs/adr/0004-state-transitions-belong-to-a-script.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import issues as journal
import programs
import store
from workspace_registry import default_config_path, resolve_workspace


SKILL_ROOT = Path(__file__).resolve().parents[1]
FORMAT_VERSION = 3
RECENT_SESSION_HOURS = 12
STATES = ("not_started", "discovered", "assisted", "independent", "transferred", "blocked")
LADDER = ("not_started", "discovered", "assisted", "independent", "transferred")
HELP_LEVELS = tuple(f"H{level}" for level in range(5))
REVIEW_STEPS = (2, 7, 21)
TRANSFER_DELAY_DAYS = 7
BLOCKED_RETRY_DAYS = 14
FAILURES_BEFORE_BLOCKED = 3
EVIDENCE_KEPT = 5
SHIPPED_AT_MIGRATION = ("engineering", "applied-ai")


class StateError(Exception):
    """The requested transition is not allowed."""


def today() -> date:
    return datetime.now().astimezone().date()


def now_stamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load(workspace: Path, allow_old_format: bool = False) -> dict:
    try:
        state = store.load(workspace)
    except store.StoreError as exc:
        raise StateError(str(exc)) from exc
    version = state.get("version")
    if not allow_old_format and version != FORMAT_VERSION:
        if isinstance(version, int) and version < FORMAT_VERSION:
            raise StateError(
                f"This workspace uses state format {version}, the skill expects {FORMAT_VERSION}. "
                "Run 'state.py migrate' to bring it forward; the learner's evidence is preserved."
            )
        raise StateError(f"Unknown state format: {version!r}. Update Techne rather than editing state by hand.")
    return state


def migrate(state: dict) -> list[str]:
    """Bring an older workspace forward without losing learner evidence."""
    version = state.get("version")
    if version == FORMAT_VERSION:
        return []
    if version is None:
        # A document written before the format was numbered.
        version = 1
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
    if version < 3:
        state.setdefault("issues", [])
        day = state.setdefault("day", {})
        blocks = {}
        for old_key, program in (("engineering", "engineering"), ("ai", "applied-ai")):
            if old_key in day:
                blocks[program] = day.pop(old_key)
        if blocks:
            day["blocks"] = {**day.get("blocks", {}), **blocks}
        if day.get("active_block") in ("engineering", "ai", "morning", "afternoon"):
            day["active_block"] = "applied-ai" if day["active_block"] in ("ai", "afternoon") else "engineering"
        progress = state.get("progress", {})
        if "engineering_days" in progress or "ai_days" in progress:
            state["progress"] = {
                "days": {
                    "engineering": int(progress.get("engineering_days", 0)),
                    "applied-ai": int(progress.get("ai_days", 0)),
                }
            }
        if not state.get("enrolments"):
            stamp = now_stamp()
            state["enrolments"] = [
                {"program": program, "enrolled_at": stamp, "status": "active"} for program in SHIPPED_AT_MIGRATION
            ]
            applied.append("enrolled in the shipped programs")
        applied.append("migrated state from format 2 to 3")
    state["version"] = FORMAT_VERSION
    return applied


CHANGELOG = SKILL_ROOT / "CHANGELOG.md"
RELEASE = re.compile(r"^## (\d+\.\d+\.\d+)\s*$")


def released() -> list[dict]:
    """The changelog, newest first: what each version changed for the learner."""
    entries: list[dict] = []
    try:
        lines = CHANGELOG.read_text(encoding="utf-8").splitlines()
    except OSError:
        return entries
    for line in lines:
        heading = RELEASE.match(line)
        if heading:
            entries.append({"version": heading.group(1), "changes": []})
        elif line.startswith("- ") and entries:
            entries[-1]["changes"].append(line[2:].strip())
    return entries


def whats_new(state: dict) -> dict:
    """What changed since this workspace last heard, and remember that it heard.

    A workspace that has never been told is brought up to date silently: the
    learner opened Techne to learn, not to read a history of the tool.
    """
    entries = released()
    current = entries[0]["version"] if entries else None
    seen = state.setdefault("techne", {}).get("seen_version")
    fresh = []
    if seen and current:
        for entry in entries:
            if entry["version"] == seen:
                break
            fresh.append(entry)
    state["techne"]["seen_version"] = current
    return {"version": current, "changes": fresh}


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


def program_subjects(state: dict, workspace: Path, identifier: str | None) -> set[str] | None:
    """The subjects of one program, or None when no program is open."""
    if not identifier:
        return None
    return programs.subjects(SKILL_ROOT, workspace, [identifier])


def due_reviews(state: dict, limit: int | None, here: set[str] | None = None) -> tuple[list[dict], list[dict]]:
    """Return (due, dropped), for the open program when `here` names its subjects.

    Programs are isolated (ADR 0020), so the learner is only ever offered the
    reviews of the program they have open. Staleness is not: a review left
    behind in another program still goes stale, and its subject still steps
    down, because forgetting does not wait for the learner to come back.
    """
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
        step_down(state, subject, "review dropped (too overdue)")
    state["reviews_due"] = kept + due
    # The queue keeps every program's reviews; only what is offered is narrowed.
    offered = [item for item in due if here is None or item["subject"] in here]
    return (offered if limit is None else offered[:limit]), dropped


def due_transfers(state: dict, here: set[str] | None = None) -> list[dict]:
    current = today()
    return [
        item
        for item in queue(state, "transfers_due")
        if date.fromisoformat(item["due_on"]) <= current and (here is None or item["subject"] in here)
    ]


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
        entry["evidence"] = ([*entry.get("evidence", []), f"{today().isoformat()} · review passed"])[-EVIDENCE_KEPT:]
        return entry
    drop_from_queue(state, "reviews_due", subject)
    entry = step_down(state, subject, "review failed")
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
        if block:
            days = state.setdefault("progress", {}).setdefault("days", {})
            days[block] = int(days.get(block, 0)) + 1
            state.setdefault("day", {}).setdefault("blocks", {})[block] = "closed"
    return current


def switch_block(state: dict, program: str) -> dict:
    if program not in enrolled(state):
        following = ", ".join(enrolled(state)) or "none"
        raise StateError(f"You are not enrolled in {program}. You follow: {following}.")
    day = state.setdefault("day", {})
    day["active_block"] = program
    for item in state.get("enrolments", []):
        if item["program"] == program:
            item["last_opened_at"] = now_stamp()
    blocks = day.setdefault("blocks", {})
    if blocks.get(program) in (None, "pending", "closed"):
        blocks[program] = "in_progress"
    return day


def open_program(state: dict) -> str | None:
    """The program the learner has open, which is the only one they are offered work in."""
    return state.get("day", {}).get("active_block")


def enrolled(state: dict) -> list[str]:
    return [item["program"] for item in state.get("enrolments", []) if item.get("status") == "active"]


def known_subjects(state: dict, workspace: Path) -> set[str]:
    """Subjects the learner can be measured on: those of the programs they follow."""
    active = enrolled(state)
    return programs.subjects(SKILL_ROOT, workspace, active or None)


DEMONSTRATED = ("independent", "transferred")


def is_covered(name: str, ceiling: str, survey: bool) -> bool:
    """A core subject is covered once demonstrated; a survey one once at its ceiling."""
    if survey:
        return name in LADDER and LADDER.index(name) >= LADDER.index(ceiling)
    return name in DEMONSTRATED


def off_programme(state: dict, workspace: Path) -> list[str]:
    """Subjects with evidence that no enrolled program teaches any more.

    Their evidence is kept — it was earned — and named, so a dropped subject is
    visible rather than silently gone.
    """
    known = known_subjects(state, workspace)
    return sorted(
        subject
        for subject, entry in state.get("mastery", {}).items()
        if subject not in known and entry.get("state", "not_started") != "not_started"
    )


def coverage(state: dict, program: programs.Program) -> dict:
    """How much of a program has been taught, and how much is demonstrated.

    A program is covered when its subjects are demonstrated, not merely seen:
    `discovered` means taught, `blocked` means stuck, and neither finishes a
    program. A survey subject is covered at its ceiling, since it is never
    meant to go further, but it is never counted as demonstrated (ADR 0002).
    `share` is what completion is measured against.
    """
    mastery = state.get("mastery", {})
    ceiling = program.settings.get("survey_ceiling", "discovered")
    survey = programs.survey_prefixes(program)
    counted = {"not_started": 0, "discovered": 0, "assisted": 0, "independent": 0, "transferred": 0, "blocked": 0}
    covered = 0
    for subject in program.subjects:
        name = mastery.get(subject, {}).get("state", "not_started")
        counted[name] = counted.get(name, 0) + 1
        covered += is_covered(name, ceiling, subject.partition(".")[0] in survey)
    total = len(program.subjects)
    started = total - counted["not_started"]
    demonstrated = sum(
        1
        for subject in program.subjects
        if subject.partition(".")[0] not in survey
        and mastery.get(subject, {}).get("state", "not_started") in DEMONSTRATED
    )
    return {
        "subjects": total,
        "started": started,
        "demonstrated": demonstrated,
        "covered": covered,
        "states": counted,
        "share": round(covered / total, 3) if total else 0.0,
        "survey_ceiling": ceiling,
    }


def settle_completions(state: dict, workspace: Path) -> list[str]:
    """Move a program to maintenance once its catalogue is covered.

    Coverage ends a program, never elapsed time (ADR 0010). The others carry on.
    """
    found, _ = programs.discover(SKILL_ROOT, workspace)
    completed = []
    for item in state.get("enrolments", []):
        program = found.get(item["program"])
        if item.get("status") != "active" or program is None:
            continue
        if coverage(state, program)["share"] >= 1.0:
            item["status"] = "maintenance"
            item["completed_at"] = now_stamp()
            completed.append(item["program"])
    return completed


def enroll(state: dict, workspace: Path, identifier: str) -> dict:
    found, rejected = programs.discover(SKILL_ROOT, workspace)
    if identifier not in found:
        # A broken file never hides a program that works: only say a file is
        # unusable when nothing usable answers to that name.
        reason = rejected.get(identifier)
        if reason:
            raise StateError(f"{identifier} cannot be used: {reason}")
        available = ", ".join(sorted(found)) or "none"
        raise StateError(f"No program called {identifier}. Available: {available}.")

    program = found[identifier]
    # Check against every program they have followed, not only the active ones:
    # the evidence of a program they left is still stored under its prefixes.
    ever = [item["program"] for item in state.get("enrolments", [])]
    others = [found[other] for other in ever if other in found and other != identifier]
    shared = programs.overlaps(program, others)
    if shared:
        raise StateError(f"{identifier} shares a domain with a program you follow: {'; '.join(shared)}")

    enrolments = state.setdefault("enrolments", [])
    for item in enrolments:
        if item["program"] == identifier:
            item["status"] = "active"
            return item
    entry = {"program": identifier, "enrolled_at": now_stamp(), "status": "active"}
    enrolments.append(entry)
    return entry


def leave(state: dict, identifier: str) -> dict:
    for item in state.get("enrolments", []):
        if item["program"] == identifier:
            item["status"] = "left"
            item["left_at"] = now_stamp()
            return item
    raise StateError(f"You are not enrolled in {identifier}.")


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
                    set_mastery(state, subject, "discovered", "lesson question answered", "H0", known)
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
    review.add_argument("--everywhere", action="store_true", help="Include the programs that are not open")

    transfer = sub.add_parser("transfer", help="List subjects due for transfer into a project")
    transfer.add_argument("--due", action="store_true")
    transfer.add_argument("--everywhere", action="store_true", help="Include the programs that are not open")

    check = sub.add_parser("checkpoint", help="Checkpoint the current activity")
    check.add_argument("--note")
    check.add_argument("--help-level", choices=HELP_LEVELS)

    close = sub.add_parser("close", help="Close the current block and count a working day")
    close.add_argument("--note")

    switch = sub.add_parser("switch", help="Open an enrolled program")
    switch.add_argument("program")


    enrolling = sub.add_parser("enroll", help="Enrol in a program and open it")
    enrolling.add_argument("program")

    leaving = sub.add_parser("leave", help="Leave a program without losing its evidence")
    leaving.add_argument("program")

    issues = sub.add_parser("issue", help="Record, list, resolve or export reported issues")
    actions = issues.add_subparsers(dest="action", required=True)

    record = actions.add_parser("add", help="Record a new issue")
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
    sub.add_parser("programs", help="List the programs available to this learner")
    sub.add_parser("brief", help="Print the short state an agent needs to start a turn, with the current time")
    sub.add_parser("now", help="Print the current date, time and UTC offset, to stamp a record")
    sub.add_parser("whats-new", help="What Techne changed since this workspace last heard, once")
    export_state = sub.add_parser("export", help="Print the whole state as JSON, for backup")
    export_state.add_argument("--out", type=Path, help="Write to this file instead of standard output")
    sub.add_parser("show", help="Print the current state as JSON")
    return parser


def read_only(args: argparse.Namespace) -> bool:
    """Commands that only look at the state, and so must leave it alone."""
    return args.command in ("programs", "show")


def days_line(summary: dict) -> str:
    days = (summary.get("progress") or {}).get("days") or {}
    return " · ".join(f"{program} {count}" for program, count in days.items()) or "none yet"


def readable(state: dict) -> str:
    """The state as a person would want to read it, since it now lives in a database."""
    summary = store.brief(state)
    lines = [
        f"Status        {summary['status']} · mode {summary['mode']}",
        f"Language      {summary['language']}",
        f"Open          {(summary.get('current') or {}).get('id') or 'nothing'}"
        f" ({(summary.get('current') or {}).get('status', 'none')})",
        f"Programs      {', '.join(summary['enrolments']) or 'none'}",
        f"Working days  {days_line(summary)}",
        f"Due           {summary['reviews_due']} reviews · {summary['transfers_due']} transfers",
        f"Open issues   {summary['open_issues']}",
        "",
        "Mastery",
    ]
    counts = summary["mastery_counts"]
    for name in ("transferred", "independent", "assisted", "discovered", "blocked"):
        if counts.get(name):
            lines.append(f"  {name:<13} {counts[name]}")
    if not counts:
        lines.append("  nothing recorded yet")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    if args.command == "now":
        # The system clock, never the conversation, dates what Techne records.
        print(now_stamp())
        return 0
    try:
        workspace = args.workspace.expanduser().resolve() if args.workspace else resolve_workspace(Path("."), args.config)
        state = load(workspace, allow_old_format=args.command == "migrate")
        known = known_subjects(state, workspace)
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
                here = None if args.everywhere else program_subjects(state, workspace, open_program(state))
                due, dropped = due_reviews(state, args.limit, here)
                result = {"due": due, "dropped": dropped, "program": open_program(state)}
        elif args.command == "transfer":
            here = None if args.everywhere else program_subjects(state, workspace, open_program(state))
            result = {"due": due_transfers(state, here), "program": open_program(state)}
        elif args.command == "checkpoint":
            result = checkpoint(state, args.note, args.help_level, "checkpointed")
        elif args.command == "close":
            result = checkpoint(state, args.note, None, "closed")
        elif args.command == "switch":
            checkpoint(state, f"switching to {args.program}", None, "checkpointed")
            result = switch_block(state, args.program)
        elif args.command == "enroll":
            # Enrol, then start: the learner organises their own time, so a new
            # program opens at once rather than waiting for a slot.
            result = enroll(state, workspace, args.program)
            if state.get("current", {}).get("id"):
                checkpoint(state, f"enrolling in {args.program}", None, "checkpointed")
            switch_block(state, args.program)
        elif args.command == "leave":
            result = leave(state, args.program)
        elif args.command == "issue":
            if args.action == "add":
                current = state.get("current", {})
                origin = {
                    "activity": args.activity or current.get("id"),
                    "track": args.track or current.get("track"),
                }
                result = journal.add(state, args.type, args.text, origin)
            elif args.action == "resolve":
                result = journal.resolve(state, args.id, args.status)
            elif args.action == "export":
                # An export reads; it never writes state.
                print(journal.export(journal.select(state, args.status, args.since)), end="")
                return 0
            else:
                result = {"entries": journal.select(state, args.status, args.since)}
        elif args.command == "whats-new":
            result = whats_new(state)
        elif args.command == "ingest-events":
            result = ingest_events(state, workspace, known)
        elif args.command == "programs":
            found, rejected = programs.discover(SKILL_ROOT, workspace)
            following = enrolled(state)
            result = {
                "available": [
                    {
                        "id": program.identifier,
                        "title": program.title,
                        "source": program.source,
                        "enrolled": program.identifier in following,
                        "open": state.get("day", {}).get("active_block") == program.identifier,
                        "units": len(program.units),
                        "coverage": coverage(state, program),
                        "settings": program.settings,
                    }
                    for program in sorted(found.values(), key=lambda item: item.identifier)
                ],
                "rejected": rejected,
                "off_programme": off_programme(state, workspace),
            }
        elif args.command == "migrate":
            applied = migrate(state)
            legacy, unreadable = journal.read_legacy_journal(workspace / ".techne")
            if legacy:
                state["issues"] = [*journal.entries(state), *legacy]
                applied.append(f"moved {len(legacy)} journal entries into the store")
            for problem in unreadable:
                print(problem, file=sys.stderr)
            result = {"applied": applied, "version": state["version"]}
        elif args.command == "brief":
            print(json.dumps({**store.brief(state), "now": now_stamp()}, ensure_ascii=False, indent=2))
            return 0
        elif args.command == "export":
            document = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
            if args.out:
                args.out.write_text(document, encoding="utf-8")
                result = {"written": str(args.out)}
            else:
                print(document, end="")
                return 0
        elif args.command == "show":
            print(readable(state), end="")
            return 0

        if read_only(args):
            # Listing or reading must not end a program, nor touch the store.
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        completed = settle_completions(state, workspace)
        store.save(workspace, state)
        if completed:
            print(
                "Covered, and now in maintenance: " + ", ".join(completed) + ". Write the closing assessment.",
                file=sys.stderr,
            )
        if warning:
            print(warning, file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (StateError, journal.IssueError, programs.ProgramError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"Techne state transition failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
