from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from test_workspace import SKILL_ROOT, initializer, load_module


catalogue = load_module("techne_catalogue", SKILL_ROOT / "scripts" / "catalogue.py")
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

    def test_feedback_is_recorded_with_its_context(self):
        self.state["current"] = {"id": "l04-dicts", "track": "engineering"}
        entry = state_script.add_feedback(self.state, self.workspace, "bug", "  la trace refuse mes réponses  ", None, None)

        self.assertEqual(entry["id"], "f1")
        self.assertEqual(entry["type"], "bug")
        self.assertEqual(entry["text"], "la trace refuse mes réponses")
        self.assertEqual((entry["activity"], entry["track"]), ("l04-dicts", "engineering"))
        self.assertEqual(entry["status"], "open")
        self.assertEqual(state_script.read_feedback(self.workspace), [entry])

    def test_feedback_refuses_an_unknown_type_or_empty_text(self):
        with self.assertRaises(state_script.StateError):
            state_script.add_feedback(self.state, self.workspace, "rant", "x", None, None)
        with self.assertRaises(state_script.StateError):
            state_script.add_feedback(self.state, self.workspace, "bug", "   ", None, None)
        self.assertFalse(state_script.feedback_path(self.workspace).exists())

    def test_resolved_feedback_leaves_the_default_export(self):
        state_script.add_feedback(self.state, self.workspace, "bug", "trace cassée", "l04", "engineering")
        state_script.add_feedback(self.state, self.workspace, "idea", "un raccourci pour les tests", "l04", "engineering")
        state_script.resolve_feedback(self.workspace, "f1", "applied")

        open_entries = state_script.select_feedback(self.workspace, "open", None)
        self.assertEqual([entry["id"] for entry in open_entries], ["f2"])
        self.assertEqual(len(state_script.select_feedback(self.workspace, None, None)), 2)

    def test_export_groups_by_type_and_names_the_activity(self):
        state_script.add_feedback(self.state, self.workspace, "bug", "trace cassée", "l04", "engineering")
        state_script.add_feedback(self.state, self.workspace, "friction", "sortie de test bruyante", "e07", "engineering")

        export = state_script.export_feedback(state_script.select_feedback(self.workspace, "open", None))

        self.assertIn("## Bugs (1)", export)
        self.assertIn("## Frictions (1)", export)
        self.assertIn("l04 · engineering", export)
        self.assertNotIn("## Ideas", export)

    def test_export_without_a_journal_is_empty_not_an_error(self):
        self.assertEqual(state_script.select_feedback(self.workspace, "open", None), [])
        self.assertIn("No feedback recorded", state_script.export_feedback([]))
        self.assertEqual(self.run_cli("feedback", "--export"), 0)

    def test_export_can_be_narrowed_by_date(self):
        state_script.add_feedback(self.state, self.workspace, "bug", "vieux", None, None)
        entries = state_script.read_feedback(self.workspace)
        entries[0]["at"] = "2026-01-05T09:00:00+01:00"
        state_script.write_feedback(self.workspace, entries)
        state_script.add_feedback(self.state, self.workspace, "bug", "récent", None, None)

        recent = state_script.select_feedback(self.workspace, None, date.today().isoformat())

        self.assertEqual([entry["text"] for entry in recent], ["récent"])
        with self.assertRaises(state_script.StateError):
            state_script.select_feedback(self.workspace, None, "hier")

    def test_cli_records_and_exports_feedback(self):
        self.assertEqual(self.run_cli("feedback", "--add", "le placeholder divulgue", "--type", "bug"), 0)
        self.assertEqual(self.run_cli("feedback", "--add", "sans type"), 1)
        self.assertEqual(len(state_script.read_feedback(self.workspace)), 1)
        self.assertEqual(self.run_cli("feedback", "--resolve", "f1", "--status", "dismissed"), 0)
        self.assertEqual(state_script.read_feedback(self.workspace)[0]["status"], "dismissed")

    def test_cli_writes_state_and_reports_errors(self):
        self.assertEqual(self.run_cli("mastery", "ts.generics", "assisted", "--evidence", "helped", "--help-level", "H3"), 0)
        written = json.loads((self.workspace / ".techne" / "STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(written["mastery"]["ts.generics"]["state"], "assisted")
        self.assertEqual(self.run_cli("mastery", "ts.generics", "independent", "--help-level", "H4"), 1)


if __name__ == "__main__":
    unittest.main()
