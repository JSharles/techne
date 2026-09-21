"""Keep the French style file and the style eval suite in agreement.

The eval suite (`plugins/techne/evals/style-fr-*`) runs real agent sessions and
costs money, so it runs before a release, not here. These tests are the cheap
half: the regex graders must flag the wording learners reported and must never
flag the natural versions the style file recommends, and every case must build
a valid French workspace.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_workspace import ROOT as REPO_ROOT, SKILL_ROOT, validator


EVALS = REPO_ROOT / "plugins" / "techne" / "evals"
STYLE_FR = SKILL_ROOT / "references" / "style-fr.md"

# Rows whose pattern a regex can see; the others are left to the LLM grader.
# « preuve » and « borne » also have plain meanings (« bornes incluses »), so a
# regex would flag correct French: only the LLM grader judges them.
DETECTABLE = ("Bold label", "Machinery word", "Anglicism")
JUDGED_ONLY = ("« preuve »",)


def style_rows() -> list[tuple[str, str, str]]:
    rows = []
    for line in STYLE_FR.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] not in ("Pattern", "---"):
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    header = text.split("---", 2)[1]
    fields = {}
    for line in header.strip().splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def regex_graders() -> dict[Path, re.Pattern]:
    graders = {}
    for path in sorted(EVALS.glob("*/graders/*.md")):
        fields = frontmatter(path)
        if fields.get("type") != "regex":
            continue
        pattern = json.loads(fields["pattern"])
        flags = re.IGNORECASE if "i" in fields.get("flags", "") else 0
        graders[path] = re.compile(pattern, flags)
    return graders


class StyleSuiteTests(unittest.TestCase):
    def test_the_style_file_holds_a_dozen_pairs(self):
        self.assertGreaterEqual(len(style_rows()), 12)

    def test_natural_versions_pass_every_regex_grader(self):
        graders = regex_graders()
        self.assertTrue(graders)
        for _, _, natural in style_rows():
            for path, pattern in graders.items():
                self.assertIsNone(pattern.search(natural), f"{path.parent.parent.name}/{path.name} flags: {natural}")

    def test_reported_wording_is_caught(self):
        patterns = list({grader.pattern: grader for grader in regex_graders().values()}.values())
        for kind, avoid, _ in style_rows():
            if kind.startswith(DETECTABLE) and not any(word in kind for word in JUDGED_ONLY):
                self.assertTrue(any(pattern.search(avoid) for pattern in patterns), f"no grader catches: {avoid}")

    def test_every_case_uses_the_same_regex_graders(self):
        by_name: dict[str, set[str]] = {}
        for path in EVALS.glob("*/graders/*.md"):
            if frontmatter(path).get("type") == "regex":
                by_name.setdefault(path.name, set()).add(path.read_text(encoding="utf-8"))
        for name, versions in by_name.items():
            self.assertEqual(len(versions), 1, f"{name} differs between cases")

    def test_every_case_builds_a_valid_french_workspace(self):
        for scaffold in sorted(EVALS.glob("*/scaffold.sh")):
            with tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary) / "home"
                cwd = Path(temporary) / "cwd"
                home.mkdir()
                cwd.mkdir()
                subprocess.run(
                    ["sh", str(scaffold)],
                    cwd=cwd,
                    env={**os.environ, "HOME": str(home), "TECHNE_HOME": str(home / ".techne")},
                    check=True,
                    capture_output=True,
                )
                self.assertEqual(validator.validate(cwd / ".techne"), [], scaffold.parent.name)
                state = json.loads(
                    subprocess.run(
                        ["python3", str(SKILL_ROOT / "scripts" / "state.py"), "--workspace", str(cwd), "brief"],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout
                )
                self.assertEqual(state["language"], "fr")


if __name__ == "__main__":
    unittest.main()
