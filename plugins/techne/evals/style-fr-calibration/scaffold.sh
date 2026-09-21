#!/bin/sh
set -e
here="$(cd "$(dirname "$0")" && pwd)"
sh "$here/../fixture.sh" "$here"
skill="$(cd "$here/../../skills/techne" && pwd)"
# This morning's reviews failed on both subjects: the evidence a good proposal weighs.
for subject in dsa.iteration dsa.hashing; do
  python3 "$skill/scripts/state.py" --workspace . mastery "$subject" assisted \
    --evidence "review failed: traced given code wrong, wrote correct code" --help-level H2 >/dev/null
done
