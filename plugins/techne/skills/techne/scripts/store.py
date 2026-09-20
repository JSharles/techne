#!/usr/bin/env python3
"""The one place learner state is read from and written to.

Nothing else opens the store: `state.py` applies transitions through it, the
validator and the initializer read and seed it, and the browser reads the
progress view this module renders. See docs/adr/0011-sqlite-is-the-state-store.md.

Functions come in pairs: those taking a workspace (the learner's directory) and
those taking a state root (the `.techne` directory inside it), because the
bundled template is validated as a state root with no workspace around it.
"""

from __future__ import annotations

import json
from pathlib import Path


STATE_FILE = "STATE.json"
PROGRESS_VIEW = ("browser", "progress.json")


class StoreError(Exception):
    """The store is missing or unreadable."""


def state_root(workspace: Path) -> Path:
    return workspace / ".techne"


def state_file(root: Path) -> Path:
    return root / STATE_FILE


def exists_at(root: Path) -> bool:
    return state_file(root).is_file()


def exists(workspace: Path) -> bool:
    return exists_at(state_root(workspace))


def load_at(root: Path) -> dict:
    path = state_file(root)
    if not path.is_file():
        raise StoreError(f"No Techne state at {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise StoreError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(state, dict):
        raise StoreError(f"Invalid Techne state in {path}")
    return state


def load(workspace: Path) -> dict:
    return load_at(state_root(workspace))


def save_at(root: Path, state: dict) -> None:
    state_file(root).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_progress_view(root, state)


def save(workspace: Path, state: dict) -> None:
    save_at(state_root(workspace), state)


def progress_path(root: Path) -> Path:
    return root.joinpath(*PROGRESS_VIEW)


def write_progress_view(root: Path, state: dict) -> None:
    """Render what the browser needs, so it never reads the store itself."""
    path = progress_path(root)
    if not path.parent.is_dir():
        return
    view = {
        "language": state.get("language"),
        "mastery": state.get("mastery", {}),
        "reviews_due": state.get("reviews_due", []),
    }
    path.write_text(json.dumps(view, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_progress_view(root: Path) -> dict:
    path = progress_path(root)
    if not path.is_file():
        return {}
    try:
        view = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return {}
    return view if isinstance(view, dict) else {}
