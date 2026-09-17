#!/usr/bin/env python3
"""Resolve and register the active Techne learning workspace."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def default_config_path() -> Path:
    techne_home = os.environ.get("TECHNE_HOME")
    base = Path(techne_home).expanduser() if techne_home else Path.home() / ".techne"
    return base / "config.json"


def is_workspace(path: Path) -> bool:
    return (path / ".techne" / "STATE.json").is_file()


def find_local_workspace(start: Path) -> Path | None:
    current = start.expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if is_workspace(candidate):
            return candidate
    return None


def load_active_workspace(config_path: Path | None = None) -> Path | None:
    path = (config_path or default_config_path()).expanduser()
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid Techne registry: {path}")
    raw_workspace = data.get("active_workspace")
    if not isinstance(raw_workspace, str) or not raw_workspace:
        raise ValueError(f"Invalid Techne registry: {path}")
    workspace = Path(raw_workspace).expanduser().resolve()
    if not is_workspace(workspace):
        raise FileNotFoundError(f"Registered Techne workspace is unavailable: {workspace}")
    return workspace


def resolve_workspace(start: Path, config_path: Path | None = None) -> Path:
    local = find_local_workspace(start)
    if local is not None:
        return local
    registered = load_active_workspace(config_path)
    if registered is not None:
        return registered
    raise FileNotFoundError("No Techne workspace found. Run 'techne init' to initialize one.")


def unregister_workspace(workspace: Path, config_path: Path | None = None) -> bool:
    """Remove the registry entry when it points at workspace. Return True if removed."""
    path = (config_path or default_config_path()).expanduser()
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return False
    raw_workspace = data.get("active_workspace") if isinstance(data, dict) else None
    if not isinstance(raw_workspace, str):
        return False
    if Path(raw_workspace).expanduser().resolve() != workspace.expanduser().resolve():
        return False
    path.unlink()
    return True


def register_workspace(workspace: Path, config_path: Path | None = None) -> Path:
    resolved = workspace.expanduser().resolve()
    if not is_workspace(resolved):
        raise FileNotFoundError(f"Not a Techne workspace: {resolved}")

    path = (config_path or default_config_path()).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "active_workspace": str(resolved),
    }
    descriptor, temporary_name = tempfile.mkstemp(prefix="config.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=True, indent=2)
            stream.write("\n")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return path
