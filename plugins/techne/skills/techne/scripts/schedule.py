#!/usr/bin/env python3
"""The learner's weekly intention: which program each slot belongs to.

The schedule is Markdown in the workspace because it is an intention, not a
calculation: the learner writes it, edits it on a Sunday evening, and Techne
follows it. It is a suggestion — deviating from it is recorded, never refused.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


FILENAME = "SCHEDULE.md"
ROW = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|\s*$")

DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DAY_NAMES = {
    "monday": "monday", "lundi": "monday",
    "tuesday": "tuesday", "mardi": "tuesday",
    "wednesday": "wednesday", "mercredi": "wednesday",
    "thursday": "thursday", "jeudi": "thursday",
    "friday": "friday", "vendredi": "friday",
    "saturday": "saturday", "samedi": "saturday",
    "sunday": "sunday", "dimanche": "sunday",
}
SLOTS = ("morning", "afternoon", "evening")
SLOT_NAMES = {
    "morning": "morning", "matin": "morning",
    "afternoon": "afternoon", "après-midi": "afternoon", "apres-midi": "afternoon",
    "evening": "evening", "soir": "evening",
    "light": "light", "léger": "light", "leger": "light",
}
LIGHT = "light"
NONE_MARKERS = ("—", "-", "–", "none", "aucun", "")


def schedule_path(workspace: Path) -> Path:
    return workspace / ".techne" / FILENAME


def slot_for(when: datetime) -> str:
    hour = when.hour
    if hour < 12:
        return "morning"
    if hour < 18:
        return "afternoon"
    return "evening"


def parse(text: str) -> tuple[list[dict], list[str]]:
    """Read the table rows; return the entries and what could not be understood."""
    entries: list[dict] = []
    problems: list[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = ROW.match(line.strip())
        if not match:
            continue
        day_cell, slot_cell, program_cell = (cell.strip() for cell in match.groups())
        day = DAY_NAMES.get(day_cell.casefold())
        slot = SLOT_NAMES.get(slot_cell.casefold())
        if day is None or slot is None:
            if day_cell.casefold() not in ("day", "jour") and set(day_cell) <= set("-: "):
                continue
            if day_cell.casefold() in ("day", "jour"):
                continue
            problems.append(f"line {number}: cannot read day {day_cell!r} or slot {slot_cell!r}")
            continue
        program = program_cell.strip()
        entries.append(
            {
                "day": day,
                "slot": slot,
                "program": None if program.casefold() in NONE_MARKERS else program,
            }
        )
    return entries, problems


def read(workspace: Path) -> tuple[list[dict], list[str]]:
    path = schedule_path(workspace)
    if not path.is_file():
        return [], []
    return parse(path.read_text(encoding="utf-8"))


def expected(entries: list[dict], when: datetime) -> dict | None:
    """What the schedule expects at this moment, if anything."""
    day = DAYS[when.weekday()]
    slot = slot_for(when)
    for entry in entries:
        if entry["day"] == day and entry["slot"] == slot:
            return entry
    for entry in entries:
        if entry["day"] == day and entry["slot"] == LIGHT:
            return entry
    return None


def render(rows: list[tuple[str, str, str]], title: str = "My week") -> str:
    lines = [
        f"# {title}",
        "",
        "Techne opens the program this table expects. Edit it whenever your week changes:",
        "working on something else is always allowed and costs nothing.",
        "",
        "| Day | Slot | Program |",
        "| --- | --- | --- |",
    ]
    lines += [f"| {day} | {slot} | {program} |" for day, slot, program in rows]
    return "\n".join(lines) + "\n"


def propose(program_ids: list[str], light_day: str = "sunday") -> str:
    """A first schedule from what the learner follows: one slot each, a light day."""
    rows: list[tuple[str, str, str]] = []
    for day in DAYS:
        if day == light_day:
            rows.append((day, LIGHT, "—"))
            continue
        for slot, program in zip(SLOTS, program_ids):
            rows.append((day, slot, program))
    return render(rows)


def write(workspace: Path, text: str) -> Path:
    path = schedule_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def record_deviation(state: dict, planned: dict | None, opened: str, when: datetime) -> None:
    """Remember that the learner worked elsewhere, so drift can be noticed later.

    A light day counts: working through it is exactly the kind of drift worth
    noticing, and noticing is all Techne does with it.
    """
    if planned is None:
        return
    expected_program = planned["program"] or LIGHT
    if expected_program == opened:
        return
    drift = state.setdefault("schedule_drift", [])
    drift.append({"at": when.isoformat(timespec="seconds"), "expected": expected_program, "opened": opened})
    del drift[:-60]


def drifting(state: dict, when: datetime, days: int = 14, threshold: int = 6) -> bool:
    """Has the schedule been systematically wrong for a fortnight?"""
    recent = [
        item
        for item in state.get("schedule_drift", [])
        if (when - datetime.fromisoformat(item["at"])).days <= days
    ]
    return len(recent) >= threshold
