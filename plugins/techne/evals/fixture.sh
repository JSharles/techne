#!/bin/sh
# Build a Techne workspace taught in French in the eval's working directory,
# then lay the calling case's own files over it: `workspace/` is copied as is,
# and `workspace/state/` goes into `.techne/` (a `.techne/` directory could not
# be committed: the repository ignores it). HOME is the eval's sandbox, so the
# registry written here never touches a real learner's workspace.
set -e
case_dir="$1"
skill="$(cd "$case_dir/../../skills/techne" && pwd)"
state() { python3 "$skill/scripts/state.py" --workspace . "$@" >/dev/null; }

python3 "$skill/scripts/init_workspace.py" . --language fr --registry "$HOME/.techne/config.json" >/dev/null
state enroll engineering
state enroll applied-ai
state switch engineering
if [ -d "$case_dir/workspace" ]; then
  (cd "$case_dir/workspace" && find . -path ./state -prune -o -type f -print) | while read -r file; do
    mkdir -p "$(dirname "$file")"
    cp "$case_dir/workspace/$file" "$file"
  done
fi
if [ -d "$case_dir/workspace/state" ]; then
  cp -R "$case_dir/workspace/state/." .techne/
fi
