#!/usr/bin/env python3
"""Read the subject catalogues declared in the curriculum references."""

from __future__ import annotations

import re
from pathlib import Path


REFERENCES = ("curriculum.md", "ai-curriculum.md")
DOMAIN_HEADING = re.compile(r"^###\s+.*?`([a-z]+)\.\*`", re.MULTILINE)
TOKEN = re.compile(r"`([a-z0-9-]+)`")


def catalogue_paths(skill_root: Path) -> list[Path]:
    return [skill_root / "references" / name for name in REFERENCES]


def subjects(skill_root: Path) -> set[str]:
    """Every subject identifier declared under a '## Subject catalogue' section."""
    known: set[str] = set()
    for path in catalogue_paths(skill_root):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        start = text.find("## Subject catalogue")
        if start < 0:
            continue
        section = text[start:]
        end = section.find("\n## ", 1)
        if end > 0:
            section = section[:end]
        headings = list(DOMAIN_HEADING.finditer(section))
        for index, heading in enumerate(headings):
            stop = headings[index + 1].start() if index + 1 < len(headings) else len(section)
            body = section[heading.end():stop]
            known.update(f"{heading.group(1)}.{token}" for token in TOKEN.findall(body))
    return known
