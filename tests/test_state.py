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

    def test_cli_writes_state_and_reports_errors(self):
        self.assertEqual(self.run_cli("mastery", "ts.generics", "assisted", "--evidence", "helped", "--help-level", "H3"), 0)
        written = json.loads((self.workspace / ".techne" / "STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(written["mastery"]["ts.generics"]["state"], "assisted")
        self.assertEqual(self.run_cli("mastery", "ts.generics", "independent", "--help-level", "H4"), 1)


if __name__ == "__main__":
    unittest.main()
