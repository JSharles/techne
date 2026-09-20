#!/usr/bin/env python3
"""Validate Techne's bundled template or an initialized learner workspace."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import issues as journal
import schedule as weekly
import store


SKILL_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "CURRENT.md",
    "PROFILE.md",
    "SESSION_LOG.md",
    "DECISIONS.md",
    "AI_LAB.md",
)
REQUIRED_STATE_KEYS = (
    "version", "status", "language", "mode", "day", "progress", "current",
    "mastery", "reviews_due", "transfers_due", "enrolments", "issues", "browser",
)
MASTERY_STATES = ("not_started", "discovered", "assisted", "independent", "transferred", "blocked")
BROWSER_FILES = ("serve.py", "lesson-template.html", "assets/i18n.js", "assets/progress.js", "assets/exercise.js")
SCRIPTS = ("state.py", "programs.py", "store.py", "issues.py", "schedule.py", "init_workspace.py", "reset_workspace.py", "resolve_workspace.py", "workspace_registry.py")


def validate(state_root: Path, require_browser: bool = True, template: bool = False) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = state_root / name
        if not path.is_file():
            errors.append(f"missing {path}")

    if not store.exists_at(state_root):
        errors.append(f"missing Techne state in {state_root}")
    else:
        try:
            state = store.load_at(state_root)
        except store.StoreError as exc:
            errors.append(str(exc))
        else:
            for key in REQUIRED_STATE_KEYS:
                if key not in state:
                    errors.append(f"state missing key: {key}")
            if state.get("version") != 3:
                errors.append("state version must be 3; run state.py migrate on an older workspace")
            if state.get("current", {}).get("help_level") not in {f"H{value}" for value in range(5)}:
                errors.append("current.help_level must be H0 through H4")
            language = state.get("language")
            if template and language is not None:
                errors.append("the seed language must be null until initialization")
            if not template and not (isinstance(language, str) and language):
                errors.append("state language must record the learner's chosen language")

            mastery = state.get("mastery")
            if not isinstance(mastery, dict):
                errors.append("mastery must be an object keyed by subject id")
            else:
                for subject, entry in mastery.items():
                    entry_state = entry.get("state") if isinstance(entry, dict) else None
                    if entry_state not in MASTERY_STATES:
                        errors.append(f"mastery.{subject}.state must be one of {', '.join(MASTERY_STATES)}")

            errors.extend(journal.problems(state))
            _, unreadable = weekly.read(state_root.parent)
            errors.extend(f"SCHEDULE.md {problem}" for problem in unreadable)

    if require_browser:
        browser = state_root / "browser"
        for relative in BROWSER_FILES:
            if not (browser / relative).is_file():
                errors.append(f"missing browser runtime file: {browser / relative}")

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Techne learner state.")
    parser.add_argument("workspace", nargs="?", default=".", help="Learning workspace (default: current directory)")
    parser.add_argument("--template", action="store_true", help="Validate the bundled templates instead")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.template:
        state_root = SKILL_ROOT / "assets" / "workspace"
        errors = validate(state_root, require_browser=False, template=True)
        browser = SKILL_ROOT / "assets" / "browser"
        for relative in BROWSER_FILES:
            if not (browser / relative).is_file():
                errors.append(f"missing browser template file: {browser / relative}")
    else:
        state_root = Path(args.workspace).expanduser().resolve() / ".techne"
        errors = validate(state_root)

    if errors:
        print("Techne validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Techne validation passed: {state_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
