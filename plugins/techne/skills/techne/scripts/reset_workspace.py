#!/usr/bin/env python3
"""Archive or delete a Techne learner workspace so the learner can start over."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

from workspace_registry import default_config_path, is_workspace, unregister_workspace


def reset(workspace: Path, registry_path: Path | None = None, delete: bool = False) -> Path | None:
    """Move `.techne/` aside (or delete it) and drop the matching registry entry.

    Return the archive path, or None when the state was deleted. Learner files
    outside `.techne/` are never touched.
    """
    workspace = workspace.expanduser().resolve()
    if not is_workspace(workspace):
        raise FileNotFoundError(f"Not a Techne workspace: {workspace}")
    state_root = workspace / ".techne"

    archive: Path | None = None
    if delete:
        shutil.rmtree(state_root)
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive = workspace / f".techne-archive-{stamp}"
        state_root.rename(archive)

    if registry_path is not None:
        unregister_workspace(workspace, registry_path)
    return archive


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset a Techne learning workspace.")
    parser.add_argument("workspace", type=Path, help="Learning workspace to reset")
    parser.add_argument("--confirm", action="store_true", required=True, help="Required: the learner confirmed the reset")
    parser.add_argument("--delete", action="store_true", help="Delete learner state instead of archiving it")
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
        archive = reset(args.workspace, args.registry, args.delete)
    except (FileNotFoundError, OSError) as exc:
        print(f"Techne reset failed: {exc}", file=sys.stderr)
        return 1
    print(f"Techne state archived: {archive}" if archive else "Techne state deleted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
