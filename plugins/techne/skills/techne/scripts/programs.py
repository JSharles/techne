#!/usr/bin/env python3
"""Read the programs available to a learner.

A program is a Markdown file: a metadata header, a sequence of units, and a
subject catalogue. Techne ships some beside the skill; the learner keeps their
own in the workspace, where an identifier clash goes to the learner.
See docs/adr/0010-a-program-is-data-not-skill-source.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


SHIPPED_DIR = "programs"
WORKSPACE_DIR = (".techne", "programs")

ACTIVITY_KINDS = ("code", "browser", "oral", "writing")
BALANCES = ("lesson-heavy", "balanced", "practice-heavy")
TIMEBOX_KEYS = ("lesson", "exercise", "review", "project", "placement")
CEILINGS = ("discovered", "assisted", "independent", "transferred")
SETTING_KEYS = ("activity_kinds", "lesson_to_practice", "timeboxes", "red_thread", "survey_ceiling")
# `cadence` fed a weekly schedule Techne no longer keeps; older files that declare it still load.
HEADER_KEYS = ("id", "title", "version", "cadence", *SETTING_KEYS)

IDENTIFIER = re.compile(r"^[a-z][a-z0-9-]*$")
PREFIX = r"[a-z][a-z0-9]*"
SUBJECT_DOMAIN = re.compile(rf"^###\s+(.+?)\s+—\s+`({PREFIX})\.\*`", re.MULTILINE)
SUBJECT_TOKEN = re.compile(r"`([a-z0-9-]+)`")
# A line of subjects holds nothing but them: prose under a domain may quote words in backticks.
SUBJECT_LINE = re.compile(r"^\s*`[a-z0-9-]+`(\s*,\s*`[a-z0-9-]+`)*\s*,?\s*$")
UNIT_HEADING = re.compile(r"^###\s+(.+)$", re.MULTILINE)


class ProgramError(Exception):
    """A program file cannot be used, and why."""


@dataclass
class Program:
    identifier: str
    title: str
    version: int
    path: Path
    source: str
    settings: dict = field(default_factory=dict)
    units: list[str] = field(default_factory=list)
    subjects: set[str] = field(default_factory=set)
    domains: dict = field(default_factory=dict)


def split_header(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ProgramError("missing metadata header")
    end = text.find("\n---", 4)
    if end < 0:
        raise ProgramError("unterminated metadata header")
    header: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ProgramError(f"header line is not `key: value`: {line.strip()!r}")
        header[key.strip()] = value.strip()
    return header, text[end + 4 :]


def parse_settings(header: dict) -> dict:
    unknown = sorted(key for key in header if key not in HEADER_KEYS)
    if unknown:
        raise ProgramError(f"unknown setting(s): {', '.join(unknown)}")

    kinds = [kind.strip() for kind in header.get("activity_kinds", "").split(",") if kind.strip()]
    for kind in kinds:
        if kind not in ACTIVITY_KINDS:
            raise ProgramError(f"unknown activity kind: {kind}")
    if not kinds:
        raise ProgramError("activity_kinds is required")

    balance = header.get("lesson_to_practice", "balanced")
    if balance not in BALANCES:
        raise ProgramError(f"lesson_to_practice must be one of {', '.join(BALANCES)}")

    timeboxes = {}
    for pair in header.get("timeboxes", "").split(","):
        if not pair.strip():
            continue
        name, separator, minutes = pair.partition("=")
        if not separator or name.strip() not in TIMEBOX_KEYS or not minutes.strip().isdigit():
            raise ProgramError(f"timeboxes entry is not `name=minutes`: {pair.strip()!r}")
        timeboxes[name.strip()] = int(minutes)

    red_thread = header.get("red_thread", "no").lower()
    if red_thread not in ("yes", "no"):
        raise ProgramError("red_thread must be yes or no")

    ceiling = header.get("survey_ceiling", "discovered")
    if ceiling not in CEILINGS:
        raise ProgramError(f"survey_ceiling must be one of {', '.join(CEILINGS)}")

    return {
        "activity_kinds": kinds,
        "lesson_to_practice": balance,
        "timeboxes": timeboxes,
        "red_thread": red_thread == "yes",
        "survey_ceiling": ceiling,
    }


def parse_catalogue(body: str) -> tuple[set[str], dict[str, str]]:
    """Return the subjects, and what each domain prefix is called here."""
    start = body.find("## Subject catalogue")
    if start < 0:
        return set(), {}
    section = body[start:]
    end = section.find("\n## ", 1)
    if end > 0:
        section = section[:end]
    subjects: set[str] = set()
    domains: dict[str, str] = {}
    for line in section.splitlines():
        if line.startswith("###") and not SUBJECT_DOMAIN.match(line):
            # Otherwise its subjects would silently join the domain above it.
            raise ProgramError(f"catalogue heading names no domain as `prefix.*`: {line.strip()!r}")
    headings = list(SUBJECT_DOMAIN.finditer(section))
    for index, heading in enumerate(headings):
        title, prefix = heading.group(1).strip(), heading.group(2)
        domains[prefix] = title
        stop = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        for line in section[heading.end() : stop].splitlines():
            if SUBJECT_LINE.match(line):
                subjects.update(f"{prefix}.{token}" for token in SUBJECT_TOKEN.findall(line))
    return subjects, domains


def parse_units(body: str) -> list[str]:
    start = body.find("## Sequence")
    if start < 0:
        return []
    section = body[start:]
    end = section.find("\n## ", 1)
    if end > 0:
        section = section[:end]
    return [heading.strip() for heading in UNIT_HEADING.findall(section)]


def read(path: Path, source: str = "workspace") -> Program:
    """Parse one program file, raising ProgramError with the reason it cannot be used."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProgramError(str(exc)) from exc

    header, body = split_header(text)
    identifier = header.get("id", "")
    if not IDENTIFIER.match(identifier):
        raise ProgramError("id is missing or not a lowercase slug")
    if not header.get("title"):
        raise ProgramError("title is required")
    if not header.get("version", "").isdigit():
        raise ProgramError("version must be a whole number")

    settings = parse_settings(header)
    units = parse_units(body)
    if not units:
        raise ProgramError("a program needs at least one unit under its sequence")
    subjects, domains = parse_catalogue(body)
    if not subjects:
        raise ProgramError("a program needs a subject catalogue")
    malformed = sorted(subject for subject in subjects if not re.match(rf"^{PREFIX}\.[a-z0-9-]+$", subject))
    if malformed:
        raise ProgramError(f"malformed subject identifier(s): {', '.join(malformed)}")

    return Program(
        identifier=identifier,
        title=header["title"],
        version=int(header["version"]),
        path=path,
        source=source,
        settings=settings,
        units=units,
        subjects=subjects,
        domains=domains,
    )


def shipped_dir(skill_root: Path) -> Path:
    return skill_root / SHIPPED_DIR


def workspace_dir(workspace: Path) -> Path:
    return workspace.joinpath(*WORKSPACE_DIR)


def discover(skill_root: Path, workspace: Path | None = None) -> tuple[dict[str, Program], dict[str, str]]:
    """Return the usable programs by identifier, and the reason each unusable one was rejected."""
    found: dict[str, Program] = {}
    rejected: dict[str, str] = {}
    sources = [(shipped_dir(skill_root), "shipped")]
    if workspace is not None:
        sources.append((workspace_dir(workspace), "workspace"))

    for directory, source in sources:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            try:
                program = read(path, source)
            except ProgramError as exc:
                rejected[path.stem] = str(exc)
                continue
            # The learner's own program wins an identifier clash with a shipped one.
            found[program.identifier] = program
    return found, rejected


def subjects(skill_root: Path, workspace: Path | None = None, identifiers: list[str] | None = None) -> set[str]:
    """The subjects declared by the given programs, or by every usable one."""
    found, _ = discover(skill_root, workspace)
    chosen = found.values() if identifiers is None else [found[key] for key in identifiers if key in found]
    known: set[str] = set()
    for program in chosen:
        known.update(program.subjects)
    return known


def overlaps(program: Program, others: list[Program]) -> list[str]:
    """The domain prefixes this program shares with others.

    Programs are isolated: each keeps its own evidence, so a domain prefix
    belongs to one program alone. A shared prefix would let evidence earned in
    one program count in another (ADR 0020).
    """
    problems = []
    for other in others:
        if other.identifier == program.identifier:
            continue
        for prefix in sorted(set(program.domains) & set(other.domains)):
            problems.append(f"`{prefix}.*` is also a domain of {other.identifier}")
    return problems


def survey_prefixes(program: Program) -> set[str]:
    """The prefixes of the domains titled Survey, whose subjects stop at the survey ceiling."""
    return {prefix for prefix, title in program.domains.items() if title.casefold() == "survey"}
