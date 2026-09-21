#!/bin/sh
set -e
here="$(cd "$(dirname "$0")" && pwd)"
sh "$here/../fixture.sh" "$here"
