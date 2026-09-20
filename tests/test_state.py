from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

from test_workspace import SKILL_ROOT, initializer, load_module, validator


catalogue = load_module("techne_catalogue", SKILL_ROOT / "scripts" / "catalogue.py")
journal = load_module("feedback", SKILL_ROOT / "scripts" / "feedback.py")
state_script = load_module("techne_state", SKILL_ROOT / "scripts" / "state.py")


class CatalogueTests(unittest.TestCase):
    def test_reads_both_curricula(self):
        subjects = catalogue.subjects(SKILL_ROOT)

        self.assertIn("ts.narrowing", subjects)
        self.assertIn("dsa.bfs", subjects)
        self.assertIn("agent.checkpointers", subjects)
        self.assertNotIn("ts.bogus", subjects)
        self.assertGreater(len(subjects), 150)


class StateTransitionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.workspace = Path(self.directory.name)
        initializer.initialize(self.workspace, "fr")
        self.path, self.state = state_script.load(self.workspace)
        self.known = catalogue.subjects(SKILL_ROOT)

    def run_cli(self, *args) -> int:
        return state_script.main(["--workspace", str(self.workspace), *args])

    def test_refuses_unknown_subject_and_helped_independence(self):
        with self.assertRaises(state_script.StateError):
            state_script.set_mastery(self.state, "ts.bogus", "independent", None, None, self.known)
        with self.assertRaises(state_script.StateError):
            state_script.set_mastery(self.state, "ts.narrowing", "independent", None, "H3", self.known)

    def test_independence_schedules_reviews_and_a_transfer(self):
        state_script.set_mastery(self.state, "ts.narrowing", "independent", "9/9", "H1", self.known)

        due_dates = [item["due_on"] for item in self.state["reviews_due"]]
        expected = [(date.today() + timedelta(days=days)).isoformat() for days in (2, 7, 21)]
        self.assertEqual(due_dates, expected)
        self.assertEqual(self.state["transfers_due"][0]["subject"], "ts.narrowing")

        state_script.set_mastery(self.state, "ts.narrowing", "transferred", "red thread", "H0", self.known)
        self.assertEqual(self.state["transfers_due"], [])

    def test_failed_review_steps_down_and_reschedules(self):
        state_script.set_mastery(self.state, "dsa.hashing", "independent", "two-sum", "H0", self.known)
        state_script.record_review(self.state, "dsa.hashing", False, self.known)

        self.assertEqual(self.state["mastery"]["dsa.hashing"]["state"], "assisted")
        self.assertEqual(
            [item["due_on"] for item in self.state["reviews_due"]],
            [(date.today() + timedelta(days=2)).isoformat()],
        )

    def test_overdue_reviews_are_dropped_and_step_the_subject_down(self):
        state_script.set_mastery(self.state, "react.effects-and-alternatives", "independent", "ok", "H0", self.known)
        long_gone = (date.today() - timedelta(days=30)).isoformat()
        for item in self.state["reviews_due"]:
            item["due_on"] = long_gone

        due, dropped = state_script.due_reviews(self.state, None)

        # J+2 and J+7 are stale beyond twice their interval; J+21 is still due.
        self.assertEqual([item["interval_days"] for item in dropped], [2, 7])
        self.assertEqual([item["interval_days"] for item in due], [21])
        # One step down, not one per dropped review.
        self.assertEqual(self.state["mastery"]["react.effects-and-alternatives"]["state"], "assisted")

    def test_fragile_subjects_come_first_in_the_due_queue(self):
        state_script.set_mastery(self.state, "dsa.hashing", "independent", "ok", "H0", self.known)
        state_script.set_mastery(self.state, "sql.indexes", "assisted", "helped", "H3", self.known)
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        self.state["reviews_due"] = [
            {"subject": "dsa.hashing", "due_on": yesterday, "interval_days": 2},
            {"subject": "sql.indexes", "due_on": date.today().isoformat(), "interval_days": 2},
        ]

        due, _ = state_script.due_reviews(self.state, None)

        self.assertEqual([item["subject"] for item in due], ["sql.indexes", "dsa.hashing"])

    def test_three_failures_block_the_subject_and_schedule_a_retry(self):
        for _ in range(3):
            state_script.record_failure(self.state, "dsa.bfs", self.known)

        self.assertEqual(self.state["mastery"]["dsa.bfs"]["state"], "blocked")
        self.assertEqual(
            self.state["reviews_due"][0]["due_on"],
            (date.today() + timedelta(days=14)).isoformat(),
        )

    def test_closing_a_block_counts_one_working_day(self):
        state_script.switch_block(self.state, "engineering")
        state_script.checkpoint(self.state, "done", None, "closed")

        self.assertEqual(self.state["progress"]["engineering_days"], 1)
        self.assertEqual(self.state["day"]["engineering"], "closed")

    def test_ingesting_events_applies_only_mechanical_evidence(self):
        events = self.workspace / ".techne" / "events" / "browser.jsonl"
        events.write_text(
            json.dumps({"kind": "quiz", "subject": "react.forms", "correct": True}) + "\n"
            + json.dumps({"kind": "exercise", "subject": "react.forms", "passed": 3, "total": 9}) + "\n",
            encoding="utf-8",
        )

        report = state_script.ingest_events(self.state, self.workspace, self.known)

        self.assertEqual(report["applied"], ["react.forms"])
        self.assertEqual(len(report["for_agent"]), 1)
        self.assertEqual(self.state["mastery"]["react.forms"]["state"], "discovered")
        self.assertEqual(self.state["browser"]["last_event_line"], 2)

    def test_migrates_an_old_workspace_without_losing_evidence(self):
        old = {
            "version": 1,
            "status": "diagnostic_in_progress",
            "language": "fr",
            "mode": "curriculum",
            "day": {"date": "2026-09-17", "curriculum": "in_progress", "project": "discovery_pending", "active_block": "morning"},
            "current": {"id": "s01", "track": "curriculum", "status": "ready", "help_level": "H6"},
            "mastery": {
                "dsa": {"level": "unassessed", "evidence": [{"task": "placement"}]},
                "typescript": {"score": None, "status": "unassessed"},
            },
            "reviews": {"last_opened_at": None, "due_count": 0},
            "project": {"phase": "discovery_pending"},
            "browser": {"last_event_line": 3},
        }
        path = self.workspace / ".techne" / "STATE.json"
        path.write_text(json.dumps(old), encoding="utf-8")

        with self.assertRaises(state_script.StateError):
            state_script.load(self.workspace)
        self.assertEqual(self.run_cli("migrate"), 0)

        migrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["version"], state_script.FORMAT_VERSION)
        self.assertEqual(migrated["day"]["engineering"], "in_progress")
        self.assertEqual(migrated["ai"]["phase"], "discovery_pending")
        self.assertEqual(migrated["current"]["help_level"], "H4")
        self.assertEqual(migrated["mastery"], {})
        self.assertEqual(sorted(migrated["legacy_mastery"]), ["dsa", "typescript"])
        self.assertEqual(migrated["legacy_mastery"]["dsa"]["evidence"], [{"task": "placement"}])
        self.assertEqual(migrated["browser"]["last_event_line"], 3)
        self.assertEqual(migrated["reviews_due"], [])
        self.assertEqual(self.run_cli("mastery", "dsa.hashing", "discovered"), 0)

    def test_warns_when_another_session_wrote_recently(self):
        self.assertIsNone(state_script.note_session(self.state, "session-a"))
        self.assertIsNone(state_script.note_session(self.state, "session-a"))
        warning = state_script.note_session(self.state, "session-b")

        self.assertIsNotNone(warning)
        self.assertEqual(self.state["session"]["id"], "session-b")

    def test_cli_records_feedback_with_its_context(self):
        self.state["current"] = {"id": "l04-dicts", "track": "engineering"}
        state_script.save(self.path, self.state)

        self.assertEqual(self.run_cli("feedback", "add", "--type", "bug", "--text", "  la trace refuse mes réponses  "), 0)

        entries = journal.read(self.workspace)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["id"], "f1")
        self.assertEqual(entries[0]["text"], "la trace refuse mes réponses")
        self.assertEqual((entries[0]["activity"], entries[0]["track"]), ("l04-dicts", "engineering"))
        self.assertEqual(entries[0]["status"], "open")

    def test_cli_refuses_an_unknown_type_or_empty_text(self):
        self.assertEqual(self.run_cli("feedback", "add", "--type", "bug", "--text", "   "), 1)
        with self.assertRaises(SystemExit):
            self.run_cli("feedback", "add", "--type", "rant", "--text", "x")
        self.assertFalse(journal.journal_path(self.workspace).exists())

    def test_cli_export_groups_by_type_and_hides_resolved_entries(self):
        for kind, text in (("bug", "trace cassée"), ("friction", "sortie bruyante"), ("idea", "un raccourci")):
            self.run_cli("feedback", "add", "--type", kind, "--text", text, "--activity", "l04", "--track", "engineering")
        self.assertEqual(self.run_cli("feedback", "resolve", "f3", "--status", "applied"), 0)

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("feedback", "export"), 0)
        export = printed.getvalue()

        self.assertIn("## Bugs (1)", export)
        self.assertIn("## Frictions (1)", export)
        self.assertNotIn("## Ideas", export)
        self.assertIn("l04 · engineering", export)

    def test_cli_export_leaves_the_state_untouched(self):
        self.run_cli("feedback", "add", "--type", "bug", "--text", "trace cassée")
        before = (self.workspace / ".techne" / "STATE.json").read_text(encoding="utf-8")

        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.run_cli("feedback", "export"), 0)

        self.assertEqual((self.workspace / ".techne" / "STATE.json").read_text(encoding="utf-8"), before)

    def test_cli_export_without_a_journal_is_empty_not_an_error(self):
        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("feedback", "export"), 0)

        self.assertIn("No feedback recorded", printed.getvalue())

    def test_cli_list_narrows_by_date_and_status(self):
        self.run_cli("feedback", "add", "--type", "bug", "--text", "vieux")
        entries = journal.read(self.workspace)
        entries[0]["at"] = "2026-01-05T09:00:00+01:00"
        journal.write(self.workspace, entries)
        self.run_cli("feedback", "add", "--type", "bug", "--text", "récent")

        recent = journal.select(self.workspace, None, date.today().isoformat())
        self.assertEqual([entry["text"] for entry in recent], ["récent"])

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("feedback", "list", "--since", date.today().isoformat()), 0)
        self.assertIn("récent", printed.getvalue())
        self.assertNotIn("vieux", printed.getvalue())
        self.assertEqual(self.run_cli("feedback", "list", "--since", "hier"), 1)

    def test_ids_survive_a_damaged_journal(self):
        self.run_cli("feedback", "add", "--type", "bug", "--text", "première")
        path = journal.journal_path(self.workspace)
        path.write_text(path.read_text(encoding="utf-8") + "{ not json\n", encoding="utf-8")

        self.run_cli("feedback", "add", "--type", "idea", "--text", "seconde")

        self.assertEqual([entry["id"] for entry in journal.read(self.workspace)], ["f1", "f2"])

    def test_validator_reports_a_damaged_journal(self):
        journal.journal_path(self.workspace).write_text(
            json.dumps({"id": "f1", "at": "2026-09-20T09:00:00+02:00", "type": "rant", "text": "x", "status": "open"}) + "\n",
            encoding="utf-8",
        )

        self.assertTrue(any("unknown type" in error for error in validator.validate(self.workspace / ".techne")))

    def test_cli_writes_state_and_reports_errors(self):
        self.assertEqual(self.run_cli("mastery", "ts.generics", "assisted", "--evidence", "helped", "--help-level", "H3"), 0)
        written = json.loads((self.workspace / ".techne" / "STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(written["mastery"]["ts.generics"]["state"], "assisted")
        self.assertEqual(self.run_cli("mastery", "ts.generics", "independent", "--help-level", "H4"), 1)


if __name__ == "__main__":
    unittest.main()
