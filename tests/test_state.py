from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta
from pathlib import Path

from test_workspace import SKILL_ROOT, initializer, load_module, validator


programs = load_module("programs", SKILL_ROOT / "scripts" / "programs.py")
weekly = load_module("schedule", SKILL_ROOT / "scripts" / "schedule.py")
journal = load_module("issues", SKILL_ROOT / "scripts" / "issues.py")
store = load_module("store", SKILL_ROOT / "scripts" / "store.py")
state_script = load_module("techne_state", SKILL_ROOT / "scripts" / "state.py")


VALID_PROGRAM = """---
id: {identifier}
title: {title}
version: 1
activity_kinds: code
timeboxes: exercise=20
---

# {title}

## Sequence

### Week 1 — Start

- something to learn.

## Subject catalogue

### {domain_title} — `{prefix}.*`

`first`, `second`
"""


def write_program(directory: Path, identifier: str, **overrides) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    text = VALID_PROGRAM.format(
        identifier=identifier,
        title=overrides.get("title", identifier.title()),
        domain_title=overrides.get("domain_title", "Algorithms"),
        prefix=overrides.get("prefix", "dsa"),
    )
    for old, new in overrides.get("replace", []):
        text = text.replace(old, new)
    path = directory / f"{identifier}.md"
    path.write_text(text, encoding="utf-8")
    return path


class ProgramTests(unittest.TestCase):
    def test_reads_the_shipped_programs(self):
        found, rejected = programs.discover(SKILL_ROOT)

        self.assertEqual(rejected, {})
        self.assertEqual(sorted(found), ["applied-ai", "engineering"])
        self.assertTrue(found["engineering"].settings["red_thread"])
        self.assertEqual(found["engineering"].settings["timeboxes"]["exercise"], 30)
        self.assertGreater(len(found["engineering"].units), 3)

        subjects = programs.subjects(SKILL_ROOT)
        self.assertIn("ts.narrowing", subjects)
        self.assertIn("agent.checkpointers", subjects)
        self.assertNotIn("ts.bogus", subjects)
        self.assertGreater(len(subjects), 150)

    def test_the_learners_program_wins_an_identifier_clash(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_program(programs.workspace_dir(workspace), "engineering", title="My Engineering")

            found, _ = programs.discover(SKILL_ROOT, workspace)

            self.assertEqual(found["engineering"].title, "My Engineering")
            self.assertEqual(found["engineering"].source, "workspace")

    def test_an_unusable_program_is_rejected_with_its_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            folder = programs.workspace_dir(workspace)
            write_program(folder, "no-settings", replace=[("activity_kinds: code", "pace: fast")])
            write_program(folder, "no-units", replace=[("### Week 1 — Start", "Nothing here")])
            write_program(folder, "no-catalogue", replace=[("### Algorithms — `dsa.*`", "Nothing")])
            write_program(folder, "bad-kind", replace=[("activity_kinds: code", "activity_kinds: telepathy")])
            write_program(folder, "fine")

            found, rejected = programs.discover(SKILL_ROOT, workspace)

            self.assertIn("fine", found)
            self.assertIn("unknown setting(s): pace", rejected["no-settings"])
            self.assertIn("at least one unit", rejected["no-units"])
            self.assertIn("subject catalogue", rejected["no-catalogue"])
            self.assertIn("unknown activity kind: telepathy", rejected["bad-kind"])

    def test_programs_disagreeing_about_a_domain_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            folder = programs.workspace_dir(workspace)
            write_program(folder, "interviews", domain_title="Algorithms", prefix="dsa")
            write_program(folder, "gardening", domain_title="Digging", prefix="dsa")

            found, _ = programs.discover(SKILL_ROOT, workspace)
            problems = programs.contradictions(found["gardening"], list(found.values()))

            self.assertTrue(any("`dsa.*`" in problem for problem in problems))
            self.assertEqual(programs.contradictions(found["interviews"], [found["interviews"]]), [])


class StateTransitionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.workspace = Path(self.directory.name)
        initializer.initialize(self.workspace, "fr")
        self.state = state_script.load(self.workspace)
        self.known = programs.subjects(SKILL_ROOT, self.workspace)

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
        state_script.enroll(self.state, self.workspace, "engineering")
        state_script.switch_block(self.state, "engineering")
        state_script.checkpoint(self.state, "done", None, "closed")

        self.assertEqual(self.state["progress"]["days"]["engineering"], 1)
        self.assertEqual(self.state["day"]["blocks"]["engineering"], "closed")

    def test_enrolment_gates_switching_and_keeps_evidence_on_leaving(self):
        with self.assertRaises(state_script.StateError):
            state_script.switch_block(self.state, "engineering")

        state_script.enroll(self.state, self.workspace, "engineering")
        state_script.set_mastery(self.state, "dsa.hashing", "independent", "two-sum", "H0", self.known)
        state_script.leave(self.state, "engineering")

        self.assertEqual(state_script.enrolled(self.state), [])
        self.assertEqual(self.state["mastery"]["dsa.hashing"]["state"], "independent")
        state_script.enroll(self.state, self.workspace, "engineering")
        self.assertEqual(state_script.enrolled(self.state), ["engineering"])

    def test_enrolment_refuses_what_it_cannot_use(self):
        with self.assertRaises(state_script.StateError) as unknown:
            state_script.enroll(self.state, self.workspace, "gardening")
        self.assertIn("No program called gardening", str(unknown.exception))

        folder = programs.workspace_dir(self.workspace)
        write_program(folder, "broken", replace=[("activity_kinds: code", "pace: fast")])
        with self.assertRaises(state_script.StateError) as broken:
            state_script.enroll(self.state, self.workspace, "broken")
        self.assertIn("unknown setting(s): pace", str(broken.exception))

    def test_a_broken_file_never_hides_a_working_program(self):
        write_program(
            programs.workspace_dir(self.workspace), "engineering", replace=[("activity_kinds: code", "pace: fast")]
        )

        state_script.enroll(self.state, self.workspace, "engineering")

        self.assertEqual(state_script.enrolled(self.state), ["engineering"])

    def test_enrolment_refuses_a_program_that_disagrees_about_a_domain(self):
        state_script.enroll(self.state, self.workspace, "engineering")
        write_program(programs.workspace_dir(self.workspace), "gardening", domain_title="Digging", prefix="dsa")

        with self.assertRaises(state_script.StateError) as clash:
            state_script.enroll(self.state, self.workspace, "gardening")

        self.assertIn("disagrees with a program you follow", str(clash.exception))

    def test_measurable_subjects_follow_the_learners_enrolments(self):
        state_script.enroll(self.state, self.workspace, "applied-ai")

        known = state_script.known_subjects(self.state, self.workspace)

        self.assertIn("py.async", known)
        self.assertNotIn("dsa.bfs", known)

    def test_the_schedule_reads_both_languages_and_says_what_is_expected(self):
        weekly.write(
            self.workspace,
            "| Jour | Créneau | Programme |\n| --- | --- | --- |\n"
            "| lundi | matin | engineering |\n| monday | afternoon | applied-ai |\n| dimanche | léger | — |\n",
        )

        entries, problems = weekly.read(self.workspace)

        self.assertEqual(problems, [])
        self.assertEqual(len(entries), 3)
        monday_morning = weekly.expected(entries, datetime(2026, 9, 21, 9, 30))
        monday_afternoon = weekly.expected(entries, datetime(2026, 9, 21, 15, 0))
        sunday = weekly.expected(entries, datetime(2026, 9, 20, 10, 0))
        self.assertEqual(monday_morning["program"], "engineering")
        self.assertEqual(monday_afternoon["program"], "applied-ai")
        self.assertEqual((sunday["slot"], sunday["program"]), ("light", None))

    def test_an_unreadable_schedule_row_is_reported(self):
        weekly.write(self.workspace, "| Day | Slot | Program |\n| --- | --- | --- |\n| someday | morning | engineering |\n")

        entries, problems = weekly.read(self.workspace)

        self.assertEqual(entries, [])
        self.assertTrue(any("someday" in problem for problem in problems))
        self.assertTrue(any("SCHEDULE.md" in error for error in validator.validate(self.workspace / ".techne")))

    def test_working_elsewhere_is_obeyed_and_recorded_as_drift(self):
        state_script.enroll(self.state, self.workspace, "engineering")
        state_script.enroll(self.state, self.workspace, "applied-ai")
        store.save(self.workspace, self.state)
        weekly.write(self.workspace, weekly.propose(["engineering", "applied-ai"]))

        self.assertEqual(self.run_cli("switch", "applied-ai"), 0)

        after = self.reload()
        self.assertEqual(after["day"]["active_block"], "applied-ai")
        drift = after.get("schedule_drift", [])
        expected_now = weekly.expected(weekly.read(self.workspace)[0], datetime.now().astimezone())
        if expected_now and (expected_now["program"] or "light") != "applied-ai":
            self.assertEqual(drift[-1]["opened"], "applied-ai")
            self.assertEqual(drift[-1]["expected"], expected_now["program"] or "light")
        else:
            self.assertEqual(drift, [])

    def test_a_proposed_schedule_gives_each_program_a_slot_and_keeps_a_light_day(self):
        text = weekly.propose(["engineering", "applied-ai"], light_day="sunday")
        entries, problems = weekly.parse(text)

        self.assertEqual(problems, [])
        self.assertEqual(sum(1 for entry in entries if entry["slot"] == "light"), 1)
        self.assertEqual(sum(1 for entry in entries if entry["program"] == "engineering"), 6)
        self.assertEqual(sum(1 for entry in entries if entry["program"] == "applied-ai"), 6)

    def test_drifting_needs_a_fortnight_of_deviations(self):
        now = datetime(2026, 9, 20, 10, 0)
        state = {}
        planned = {"day": "monday", "slot": "morning", "program": "engineering"}
        state["schedule_drift"] = [
            weekly.deviation(planned, "applied-ai", datetime(2026, 9, 15 + index % 5, 9, 0)) for index in range(5)
        ]
        self.assertFalse(weekly.drifting(state, now))
        self.assertIsNone(weekly.deviation(planned, "engineering", now), "following the schedule is not drift")

        state["schedule_drift"].append(weekly.deviation(planned, "applied-ai", datetime(2026, 9, 19, 9, 0)))
        self.assertTrue(weekly.drifting(state, now))

    def test_evidence_survives_a_subject_leaving_a_program(self):
        write_program(programs.workspace_dir(self.workspace), "sprint", prefix="int", domain_title="Interviews")
        state_script.enroll(self.state, self.workspace, "sprint")
        known = state_script.known_subjects(self.state, self.workspace)
        state_script.set_mastery(self.state, "int.first", "independent", "fait", "H0", known)

        write_program(
            programs.workspace_dir(self.workspace),
            "sprint",
            prefix="int",
            domain_title="Interviews",
            replace=[("`first`, `second`", "`second`")],
        )

        self.assertEqual(state_script.off_programme(self.state, self.workspace), ["int.first"])
        self.assertEqual(self.state["mastery"]["int.first"]["state"], "independent")

    def test_an_unscheduled_program_is_named_with_the_one_to_propose(self):
        state_script.enroll(self.state, self.workspace, "engineering")
        state_script.enroll(self.state, self.workspace, "applied-ai")
        state_script.switch_block(self.state, "engineering")
        store.save(self.workspace, self.state)
        weekly.write(
            self.workspace,
            "| Day | Slot | Program |\n| --- | --- | --- |\n| monday | morning | engineering |\n",
        )

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("schedule"), 0)
        reported = json.loads(printed.getvalue())

        self.assertEqual(reported["unscheduled"], ["applied-ai"])
        self.assertEqual(reported["least_recent"], "applied-ai", "the one worked on longest ago")

    def test_a_proposal_never_overwrites_a_schedule_without_being_told(self):
        state_script.enroll(self.state, self.workspace, "engineering")
        store.save(self.workspace, self.state)
        weekly.write(self.workspace, "| Day | Slot | Program |\n| --- | --- | --- |\n| monday | morning | engineering |\n")
        mine = weekly.schedule_path(self.workspace).read_text(encoding="utf-8")

        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.run_cli("schedule", "--propose"), 1)
        self.assertEqual(weekly.schedule_path(self.workspace).read_text(encoding="utf-8"), mine)

        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.run_cli("schedule", "--propose", "--replace"), 0)
        self.assertNotEqual(weekly.schedule_path(self.workspace).read_text(encoding="utf-8"), mine)

    def test_a_proposal_follows_each_programs_cadence(self):
        text = weekly.propose(["sprint"], cadences={"sprint": "three-times-weekly"})
        entries, _ = weekly.parse(text)

        days = sorted({entry["day"] for entry in entries if entry["program"] == "sprint"})
        self.assertEqual(days, ["friday", "monday", "wednesday"])

    def test_reading_the_state_never_changes_it(self):
        write_program(programs.workspace_dir(self.workspace), "sprint", prefix="int", domain_title="Interviews")
        state_script.enroll(self.state, self.workspace, "sprint")
        known = state_script.known_subjects(self.state, self.workspace)
        for subject in ("int.first", "int.second"):
            state_script.set_mastery(self.state, subject, "independent", "fait", "H0", known)
        store.save(self.workspace, self.state)
        database = store.database_path(self.workspace / ".techne")
        before = database.read_bytes()

        with redirect_stdout(io.StringIO()):
            for command in (["programs"], ["show"], ["schedule"]):
                self.assertEqual(self.run_cli(*command), 0)

        self.assertEqual(database.read_bytes(), before, "listing must not end a program")
        statuses = {item["program"]: item["status"] for item in self.reload()["enrolments"]}
        self.assertEqual(statuses["sprint"], "active")

    def test_a_readable_state_is_available_beside_the_json(self):
        state_script.enroll(self.state, self.workspace, "engineering")
        store.save(self.workspace, self.state)

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("show"), 0)
        rendered = printed.getvalue()

        self.assertIn("Programs", rendered)
        self.assertIn("engineering", rendered)
        self.assertNotIn("{", rendered, "show renders for a person; export is the JSON")

    def test_a_covered_program_moves_to_maintenance_alone(self):
        write_program(programs.workspace_dir(self.workspace), "sprint", prefix="int", domain_title="Interviews")
        state_script.enroll(self.state, self.workspace, "sprint")
        state_script.enroll(self.state, self.workspace, "engineering")
        known = state_script.known_subjects(self.state, self.workspace)

        state_script.set_mastery(self.state, "int.first", "discovered", "lu", "H0", known)
        state_script.set_mastery(self.state, "int.second", "independent", "fait", "H0", known)
        self.assertEqual(
            state_script.settle_completions(self.state, self.workspace),
            [],
            "a subject only taught does not finish a program",
        )

        state_script.set_mastery(self.state, "int.first", "independent", "fait aussi", "H0", known)
        completed = state_script.settle_completions(self.state, self.workspace)

        self.assertEqual(completed, ["sprint"])
        store.save(self.workspace, self.state)
        kept = {item["program"]: item for item in self.reload()["enrolments"]}
        self.assertIn("completed_at", kept["sprint"], "a stored enrolment keeps its own fields")
        statuses = {item["program"]: item["status"] for item in self.state["enrolments"]}
        self.assertEqual(statuses["sprint"], "maintenance")
        self.assertEqual(statuses["engineering"], "active")

    def test_now_prints_a_full_timestamp_from_the_system_clock(self):
        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(state_script.main(["now"]), 0)
        stamp = datetime.fromisoformat(printed.getvalue().strip())

        self.assertIsNotNone(stamp.tzinfo, "a record's time carries its UTC offset")
        self.assertLess(abs((datetime.now().astimezone() - stamp).total_seconds()), 5)

    def test_the_brief_carries_the_current_time(self):
        store.save(self.workspace, self.state)
        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("brief"), 0)

        self.assertIsNotNone(datetime.fromisoformat(json.loads(printed.getvalue())["now"]).tzinfo)

    def test_a_survey_subject_at_its_ceiling_covers_the_program(self):
        write_program(
            programs.workspace_dir(self.workspace),
            "sprint",
            prefix="int",
            domain_title="Interviews",
            replace=[("`first`, `second`\n", "`first`, `second`\n\n### Survey — `survey.*`\n\n`logs`\n")],
        )
        state_script.enroll(self.state, self.workspace, "sprint")
        known = state_script.known_subjects(self.state, self.workspace)
        state_script.set_mastery(self.state, "int.first", "independent", "fait", "H0", known)
        state_script.set_mastery(self.state, "int.second", "transferred", "fait", "H0", known)
        self.assertEqual(
            state_script.settle_completions(self.state, self.workspace),
            [],
            "a survey subject never taught leaves the program open",
        )

        state_script.set_mastery(self.state, "survey.logs", "discovered", "lu", "H0", known)
        found, _ = programs.discover(SKILL_ROOT, self.workspace)
        measured = state_script.coverage(self.state, found["sprint"])

        self.assertEqual(measured["demonstrated"], 2, "a survey subject is literacy, never mastery")
        self.assertEqual(measured["share"], 1.0)
        self.assertEqual(state_script.settle_completions(self.state, self.workspace), ["sprint"])

    def test_the_shipped_engineering_program_can_be_covered(self):
        found, _ = programs.discover(SKILL_ROOT, self.workspace)
        engineering = found["engineering"]
        ceiling = engineering.settings["survey_ceiling"]
        self.state["mastery"] = {
            subject: {"state": ceiling if subject.startswith("survey.") else "transferred"}
            for subject in engineering.subjects
        }

        self.assertEqual(state_script.coverage(self.state, engineering)["share"], 1.0)

    def test_coverage_counts_started_subjects(self):
        found, _ = programs.discover(SKILL_ROOT, self.workspace)
        state_script.enroll(self.state, self.workspace, "engineering")
        state_script.set_mastery(self.state, "dsa.hashing", "independent", "two-sum", "H0", self.known)

        measured = state_script.coverage(self.state, found["engineering"])

        self.assertEqual(measured["started"], 1)
        self.assertEqual(measured["demonstrated"], 1)
        self.assertEqual(measured["states"]["independent"], 1)
        self.assertLess(measured["share"], 0.05)

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
            "day": {"date": "2026-09-17", "engineering": "in_progress", "ai": "discovery_pending", "active_block": "morning"},
            "current": {"id": "s01", "track": "curriculum", "status": "ready", "help_level": "H6"},
            "mastery": {
                "dsa": {"level": "unassessed", "evidence": [{"task": "placement"}]},
                "typescript": {"score": None, "status": "unassessed"},
            },
            "reviews": {"last_opened_at": None, "due_count": 0},
            "project": {"phase": "discovery_pending"},
            "browser": {"last_event_line": 3},
        }
        store.database_path(self.workspace / ".techne").unlink()
        store.seed_path(self.workspace / ".techne").write_text(json.dumps(old), encoding="utf-8")

        with self.assertRaises(state_script.StateError):
            state_script.load(self.workspace)
        self.assertEqual(self.run_cli("migrate"), 0)

        migrated = store.load(self.workspace)
        self.assertEqual(migrated["version"], state_script.FORMAT_VERSION)
        self.assertEqual(migrated["day"]["blocks"]["engineering"], "in_progress")
        self.assertEqual(migrated["day"]["active_block"], "engineering")
        self.assertEqual(sorted(state_script.enrolled(migrated)), ["applied-ai", "engineering"])
        self.assertEqual(migrated["ai"]["phase"], "discovery_pending")
        self.assertEqual(migrated["current"]["help_level"], "H4")
        self.assertEqual(migrated["mastery"], {})
        self.assertEqual(sorted(migrated["legacy_mastery"]), ["dsa", "typescript"])
        self.assertEqual(migrated["legacy_mastery"]["dsa"]["evidence"], [{"task": "placement"}])
        self.assertEqual(migrated["browser"]["last_event_line"], 3)
        self.assertEqual(migrated["reviews_due"], [])
        self.assertEqual(self.run_cli("mastery", "dsa.hashing", "discovered"), 0)

    def test_migrates_a_second_format_workspace_with_its_queues_and_journal(self):
        root = self.workspace / ".techne"
        store.database_path(root).unlink()
        store.seed_path(root).write_text(
            json.dumps(
                {
                    "version": 2,
                    "status": "curriculum",
                    "language": "fr",
                    "mode": "curriculum",
                    "day": {"date": "2026-09-19", "engineering": "closed", "ai": "in_progress", "active_block": "ai"},
                    "progress": {"engineering_days": 4, "ai_days": 3},
                    "current": {"id": "e07", "track": "ai", "status": "ready", "help_level": "H1"},
                    "mastery": {
                        "dsa.hashing": {
                            "state": "independent",
                            "last_evidence_at": "2026-09-18T09:00:00+02:00",
                            "failures": 0,
                            "evidence": ["2026-09-18 · H0 · two-sum"],
                        }
                    },
                    "reviews_due": [{"subject": "dsa.hashing", "due_on": "2026-09-25", "interval_days": 7}],
                    "transfers_due": [{"subject": "dsa.hashing", "due_on": "2026-09-25"}],
                    "red_thread": {"domain": "bookshelf", "repository": None, "milestone": None},
                    "ai": {"phase": "week-3", "week": 3, "lab_repository": "ai-lab", "provider": "anthropic", "capstone": None},
                    "browser": {"last_event_line": 12},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (root / "feedback.jsonl").write_text(
            json.dumps(
                {"id": "f1", "at": "2026-09-19T10:00:00+02:00", "type": "bug", "text": "trace cassée", "status": "open"}
            )
            + "\n{ not json\n",
            encoding="utf-8",
        )

        self.assertEqual(self.run_cli("migrate"), 0)

        migrated = store.load(self.workspace)
        self.assertEqual(migrated["version"], state_script.FORMAT_VERSION)
        self.assertEqual(migrated["mastery"]["dsa.hashing"]["evidence"], ["2026-09-18 · H0 · two-sum"])
        self.assertEqual(migrated["reviews_due"][0]["interval_days"], 7)
        self.assertEqual(migrated["transfers_due"][0]["subject"], "dsa.hashing")
        self.assertEqual(migrated["browser"]["last_event_line"], 12)
        self.assertEqual(migrated["progress"]["days"], {"engineering": 4, "applied-ai": 3})
        self.assertEqual(migrated["day"]["blocks"], {"engineering": "closed", "applied-ai": "in_progress"})
        self.assertEqual(state_script.enrolled(migrated), ["engineering", "applied-ai"])
        self.assertEqual([entry["id"] for entry in journal.entries(migrated)], ["f1"])
        self.assertTrue((root / "feedback.jsonl.imported").is_file(), "the learner's journal is kept, not deleted")
        self.assertTrue(weekly.schedule_path(self.workspace).is_file(), "migration writes a first schedule")
        entries, problems = weekly.read(self.workspace)
        self.assertEqual(problems, [])
        morning = [entry["program"] for entry in entries if entry["slot"] == "morning"]
        self.assertEqual(set(morning), {"engineering"}, "mornings stay what they were")

    def test_warns_when_another_session_wrote_recently(self):
        self.assertIsNone(state_script.note_session(self.state, "session-a"))
        self.assertIsNone(state_script.note_session(self.state, "session-a"))
        warning = state_script.note_session(self.state, "session-b")

        self.assertIsNotNone(warning)
        self.assertEqual(self.state["session"]["id"], "session-b")

    def test_the_browser_reads_a_rendered_view_not_the_store(self):
        view_path = store.progress_path(self.workspace / ".techne")
        self.assertTrue(view_path.is_file(), "initialization seeds the view")

        self.run_cli("mastery", "dsa.hashing", "independent", "--evidence", "two-sum", "--help-level", "H0")

        view = json.loads(view_path.read_text(encoding="utf-8"))
        self.assertEqual(view["language"], "fr")
        self.assertEqual(view["mastery"]["dsa.hashing"]["state"], "independent")
        self.assertEqual(len(view["reviews_due"]), 3)
        self.assertNotIn("current", view, "the view carries only what the browser shows")

    def reload(self) -> dict:
        return state_script.load(self.workspace)

    def test_cli_records_an_issue_with_its_context(self):
        self.state["current"] = {"id": "l04-dicts", "track": "engineering"}
        store.save(self.workspace, self.state)

        self.assertEqual(self.run_cli("issue", "add", "--type", "bug", "--text", "  la trace refuse mes réponses  "), 0)

        recorded = journal.entries(self.reload())
        self.assertEqual(len(recorded), 1)
        self.assertEqual(recorded[0]["id"], "f1")
        self.assertEqual(recorded[0]["text"], "la trace refuse mes réponses")
        self.assertEqual((recorded[0]["activity"], recorded[0]["track"]), ("l04-dicts", "engineering"))
        self.assertEqual(recorded[0]["status"], "open")

    def test_cli_refuses_an_unknown_issue_type_or_empty_text(self):
        self.assertEqual(self.run_cli("issue", "add", "--type", "bug", "--text", "   "), 1)
        with self.assertRaises(SystemExit):
            self.run_cli("issue", "add", "--type", "rant", "--text", "x")
        self.assertEqual(journal.entries(self.reload()), [])

    def test_cli_export_groups_by_type_and_hides_resolved_entries(self):
        for kind, text in (("bug", "trace cassée"), ("friction", "sortie bruyante"), ("idea", "un raccourci")):
            self.run_cli("issue", "add", "--type", kind, "--text", text, "--activity", "l04", "--track", "engineering")
        self.assertEqual(self.run_cli("issue", "resolve", "f3", "--status", "applied"), 0)

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("issue", "export"), 0)
        export = printed.getvalue()

        self.assertIn("## Bugs (1)", export)
        self.assertIn("## Frictions (1)", export)
        self.assertNotIn("## Ideas", export)
        self.assertIn("l04 · engineering", export)

    def test_cli_export_leaves_the_store_untouched(self):
        self.run_cli("issue", "add", "--type", "bug", "--text", "trace cassée")
        database = store.database_path(self.workspace / ".techne")
        before = database.read_bytes()

        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.run_cli("issue", "export"), 0)

        self.assertEqual(database.read_bytes(), before)

    def test_cli_export_without_a_journal_is_empty_not_an_error(self):
        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("issue", "export"), 0)

        self.assertIn("No issue recorded", printed.getvalue())

    def test_cli_list_narrows_by_date_and_status(self):
        self.run_cli("issue", "add", "--type", "bug", "--text", "vieux")
        aged = self.reload()
        aged["issues"][0]["at"] = "2026-01-05T09:00:00+01:00"
        store.save(self.workspace, aged)
        self.run_cli("issue", "add", "--type", "bug", "--text", "récent")

        recent = journal.select(self.reload(), None, date.today().isoformat())
        self.assertEqual([entry["text"] for entry in recent], ["récent"])

        with redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.run_cli("issue", "list", "--since", date.today().isoformat()), 0)
        self.assertIn("récent", printed.getvalue())
        self.assertNotIn("vieux", printed.getvalue())
        self.assertEqual(self.run_cli("issue", "list", "--since", "hier"), 1)

    def test_ids_never_come_from_list_position(self):
        self.run_cli("issue", "add", "--type", "bug", "--text", "première")
        recorded = self.reload()
        recorded["issues"].append({**recorded["issues"][0], "id": "hand-written", "text": "collée à la main"})
        store.save(self.workspace, recorded)

        self.run_cli("issue", "add", "--type", "idea", "--text", "seconde")

        self.assertEqual(sorted(entry["id"] for entry in journal.entries(self.reload())), ["f1", "f2", "hand-written"])

    def test_validator_reports_a_damaged_journal(self):
        damaged = self.reload()
        damaged["issues"] = [
            {"id": "f1", "at": "2026-09-20T09:00:00+02:00", "type": "rant", "text": "x", "status": "open"}
        ]
        store.save(self.workspace, damaged)

        self.assertTrue(any("unknown type" in error for error in validator.validate(self.workspace / ".techne")))

    def test_cli_writes_state_and_reports_errors(self):
        self.assertEqual(self.run_cli("mastery", "ts.generics", "assisted", "--evidence", "helped", "--help-level", "H3"), 0)
        written = store.load(self.workspace)
        self.assertEqual(written["mastery"]["ts.generics"]["state"], "assisted")
        self.assertEqual(self.run_cli("mastery", "ts.generics", "independent", "--help-level", "H4"), 1)


if __name__ == "__main__":
    unittest.main()
