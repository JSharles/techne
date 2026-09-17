#!/usr/bin/env python3
"""Initialize a Techne learner workspace without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from workspace_registry import default_config_path, register_workspace


SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_TEMPLATE = SKILL_ROOT / "assets" / "workspace"
BROWSER_TEMPLATE = SKILL_ROOT / "assets" / "browser"
LANGUAGE_TAG = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")


def normalize_language(language: str) -> str:
    """Return a lowercase-primary BCP 47 tag such as "fr" or "pt-BR"."""
    tag = language.strip()
    primary, _, rest = tag.partition("-")
    tag = primary.lower() + ("-" + rest if rest else "")
    if not LANGUAGE_TAG.match(tag):
        raise ValueError(f"Invalid language tag: {language!r} (expected e.g. 'en', 'fr', 'pt-BR')")
    return tag


def initialize(workspace: Path, language: str, registry_path: Path | None = None) -> Path:
    language = normalize_language(language)
    workspace = workspace.expanduser().resolve()
    state_root = workspace / ".techne"
    if state_root.exists():
        raise FileExistsError(f"Techne workspace already exists: {state_root}")
    if not workspace.exists() or not workspace.is_dir():
        raise FileNotFoundError(f"Workspace directory does not exist: {workspace}")

    shutil.copytree(WORKSPACE_TEMPLATE, state_root)
    shutil.copytree(BROWSER_TEMPLATE, state_root / "browser")
    (state_root / "browser" / "lessons").mkdir()

    template_path = state_root / "browser" / "lesson-template.html"
    template = template_path.read_text(encoding="utf-8")
    template_path.write_text(template.replace("__LANG__", language), encoding="utf-8")

    state_path = state_root / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    state["initialized_at"] = now
    state["workspace"] = str(workspace)
    state["language"] = language
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (state_root / "SESSION_LOG.md").open("a", encoding="utf-8") as stream:
        stream.write(f"\n## {now} — Workspace initialized\n\n")
        stream.write("- Status: diagnostic pending\n")
        stream.write(f"- Learning language: {language}\n")
        stream.write("- Next action: collect learner facts and open the first baseline probe.\n")

    if registry_path is not None:
        register_workspace(workspace, registry_path)

    return state_root


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize local Techne learning state.")
    parser.add_argument("workspace", nargs="?", default=".", help="Learning workspace (default: current directory)")
    parser.add_argument(
        "--language",
        required=True,
        help="Language the learner chose for the curriculum, as a BCP 47 tag (e.g. en, fr, pt-BR)",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=default_config_path(),
        help="Global workspace registry (default: ~/.techne/config.json)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        state_root = initialize(Path(args.workspace), args.language, args.registry)
    except (FileExistsError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"Techne initialization failed: {exc}", file=sys.stderr)
        return 1
    print(f"Techne workspace initialized: {state_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
