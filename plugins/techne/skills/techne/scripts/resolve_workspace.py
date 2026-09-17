#!/usr/bin/env python3
"""Print the Techne workspace that applies to the current agent session."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workspace_registry import register_workspace, resolve_workspace


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve or activate a Techne learning workspace.")
    parser.add_argument("start", nargs="?", default=".", help="Directory used for local workspace discovery")
    parser.add_argument("--config", type=Path, help="Override the global registry path")
    parser.add_argument("--set", dest="workspace", type=Path, help="Register a workspace as globally active")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.workspace is not None:
            register_workspace(args.workspace, args.config)
            workspace = args.workspace.expanduser().resolve()
        else:
            workspace = resolve_workspace(Path(args.start), args.config)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Techne workspace resolution failed: {exc}", file=sys.stderr)
        return 1
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
