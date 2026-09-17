#!/usr/bin/env python3
"""Validate Techne's bundled template or an initialized learner workspace."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "STATE.json",
    "CURRENT.md",
    "PROFILE.md",
    "REVIEW_QUEUE.md",
    "SESSION_LOG.md",
    "DECISIONS.md",
    "PROJECT.md",
)
REQUIRED_STATE_KEYS = ("version", "status", "mode", "day", "current", "mastery", "project", "browser")


def validate(state_root: Path, require_browser: bool = True) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = state_root / name
        if not path.is_file():
            errors.append(f"missing {path}")

    state_path = state_root / "STATE.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {state_path}: {exc}")
        else:
            for key in REQUIRED_STATE_KEYS:
                if key not in state:
                    errors.append(f"STATE.json missing key: {key}")
            if state.get("version") != 1:
                errors.append("STATE.json version must be 1")
            if state.get("current", {}).get("help_level") not in {f"H{value}" for value in range(7)}:
                errors.append("current.help_level must be H0 through H6")

    if require_browser:
        browser = state_root / "browser"
        for relative in ("serve.py", "lesson-template.html", "assets/progress.js", "assets/exercise.js"):
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
        errors = validate(state_root, require_browser=False)
        browser = SKILL_ROOT / "assets" / "browser"
        for relative in ("serve.py", "lesson-template.html", "assets/progress.js", "assets/exercise.js"):
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
