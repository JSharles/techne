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

import store
from workspace_registry import default_config_path, is_workspace, load_active_workspace, register_workspace


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


class WorkspaceConflictError(Exception):
    """Initialization would create a second curriculum or hide an existing one."""


def check_conflicts(workspace: Path, registry_path: Path | None, replace_active: bool) -> None:
    try:
        active = load_active_workspace(registry_path) if registry_path is not None else None
    except (FileNotFoundError, ValueError):
        active = None
    if active is None or active == workspace:
        return
    if workspace in active.parents:
        # A workspace in a parent directory takes precedence over the registry,
        # so it would silently hide the learner's existing curriculum.
        raise WorkspaceConflictError(
            f"{workspace} contains the active Techne workspace {active}; "
            "initializing here would hide it. Choose another directory."
        )
    if not replace_active:
        raise WorkspaceConflictError(
            f"An active Techne workspace already exists: {active}. "
            "Resume it, reset it, or pass --replace-active to start a separate curriculum."
        )


def initialize(
    workspace: Path,
    language: str,
    registry_path: Path | None = None,
    replace_active: bool = False,
) -> Path:
    language = normalize_language(language)
    workspace = workspace.expanduser().resolve()
    state_root = workspace / ".techne"
    if state_root.exists():
        raise FileExistsError(f"Techne workspace already exists: {state_root}")
    if workspace.exists() and not workspace.is_dir():
        raise FileNotFoundError(f"Workspace path is not a directory: {workspace}")
    ancestor = next((parent for parent in workspace.parents if is_workspace(parent)), None)
    if ancestor is not None:
        raise WorkspaceConflictError(f"{workspace} is inside the existing Techne workspace {ancestor}.")
    check_conflicts(workspace, registry_path, replace_active)
    workspace.mkdir(parents=True, exist_ok=True)

    shutil.copytree(WORKSPACE_TEMPLATE, state_root)
    shutil.copytree(BROWSER_TEMPLATE, state_root / "browser")
    (state_root / "browser" / "lessons").mkdir()

    template_path = state_root / "browser" / "lesson-template.html"
    template = template_path.read_text(encoding="utf-8")
    template_path.write_text(template.replace("__LANG__", language), encoding="utf-8")

    state = store.load(workspace)
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    state["initialized_at"] = now
    state["workspace"] = str(workspace)
    state["language"] = language
    store.save(workspace, state)

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
        "--replace-active",
        action="store_true",
        help="Start a new curriculum even though another workspace is registered as active",
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
        state_root = initialize(Path(args.workspace), args.language, args.registry, args.replace_active)
    except (FileExistsError, FileNotFoundError, OSError, ValueError, WorkspaceConflictError) as exc:
        print(f"Techne initialization failed: {exc}", file=sys.stderr)
        return 1
    print(f"Techne workspace initialized: {state_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
