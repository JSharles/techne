from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "plugins" / "techne" / "skills" / "techne"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(SKILL_ROOT / "scripts"))
registry = load_module("workspace_registry", SKILL_ROOT / "scripts" / "workspace_registry.py")
initializer = load_module("techne_initializer", SKILL_ROOT / "scripts" / "init_workspace.py")
store = load_module("store", SKILL_ROOT / "scripts" / "store.py")
validator = load_module("techne_validator", SKILL_ROOT / "scripts" / "validate_workspace.py")
resetter = load_module("techne_resetter", SKILL_ROOT / "scripts" / "reset_workspace.py")


class WorkspaceTests(unittest.TestCase):
    def test_initializes_and_validates_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / "registry" / "config.json"
            state_root = initializer.initialize(workspace, "fr", config)

            self.assertEqual(state_root, (workspace / ".techne").resolve())
            self.assertEqual(validator.validate(state_root), [])
            self.assertTrue((state_root / "browser" / "lessons").is_dir())
            self.assertEqual(store.load(workspace)["workspace"], str(workspace.resolve()))
            self.assertEqual(registry.load_active_workspace(config), workspace.resolve())

    def test_records_learning_language_in_state_and_lesson_template(self):
        with tempfile.TemporaryDirectory() as directory:
            state_root = initializer.initialize(Path(directory), "PT-br")

            state = store.load(Path(directory))
            template = (state_root / "browser" / "lesson-template.html").read_text(encoding="utf-8")
            self.assertEqual(state["language"], "pt-br")
            self.assertIn('<html lang="pt-br">', template)
            self.assertNotIn("__LANG__", template)

    def test_rejects_invalid_language(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            with self.assertRaises(ValueError):
                initializer.initialize(workspace, "")
            self.assertFalse((workspace / ".techne").exists())

    def test_validator_requires_language_in_initialized_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            initializer.initialize(Path(directory), "fr")
            state = store.load(Path(directory))
            state["language"] = None
            store.save(Path(directory), state)
            state_root = Path(directory) / ".techne"

            self.assertIn("STATE.json language must record the learner's chosen language", validator.validate(state_root))

    def test_refuses_second_curriculum_while_one_is_active(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.json"
            initializer.initialize(root / "first", "fr", config)

            with self.assertRaises(initializer.WorkspaceConflictError):
                initializer.initialize(root / "second", "fr", config)
            self.assertFalse((root / "second" / ".techne").exists())

            initializer.initialize(root / "second", "fr", config, replace_active=True)
            self.assertEqual(registry.load_active_workspace(config), (root / "second").resolve())

    def test_refuses_to_hide_active_workspace_from_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.json"
            initializer.initialize(root / "dev" / "techne", "fr", config)

            with self.assertRaises(initializer.WorkspaceConflictError):
                initializer.initialize(root / "dev", "en", config, replace_active=True)
            self.assertFalse((root / "dev" / ".techne").exists())

    def test_refuses_to_nest_inside_existing_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initializer.initialize(root, "fr")
            with self.assertRaises(initializer.WorkspaceConflictError):
                initializer.initialize(root / "exercises", "fr")

    def test_reset_archives_state_and_allows_a_fresh_init(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "learning"
            config = root / "config.json"
            initializer.initialize(workspace, "fr", config)
            (workspace / "exercises").mkdir()

            archive = resetter.reset(workspace, config)

            self.assertTrue((archive / "techne.db").is_file())
            self.assertFalse((workspace / ".techne").exists())
            self.assertTrue((workspace / "exercises").is_dir())
            self.assertIsNone(registry.load_active_workspace(config))
            initializer.initialize(workspace, "en", config)
            self.assertEqual(registry.load_active_workspace(config), workspace.resolve())

    def test_reset_can_delete_state(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / "config.json"
            initializer.initialize(workspace, "fr", config)

            self.assertIsNone(resetter.reset(workspace, config, delete=True))
            self.assertFalse((workspace / ".techne").exists())
            self.assertEqual(list(workspace.glob(".techne-archive-*")), [])
            self.assertFalse(config.exists())

    def test_refuses_to_overwrite_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            initializer.initialize(workspace, "fr")
            with self.assertRaises(FileExistsError):
                initializer.initialize(workspace, "fr")

    def test_resolves_local_workspace_before_registered_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registered = root / "registered"
            local = root / "local"
            registered.mkdir()
            local.mkdir()
            config = root / "config.json"
            initializer.initialize(registered, "en", config)
            initializer.initialize(local, "fr")

            nested = local / "project" / "src"
            nested.mkdir(parents=True)
            self.assertEqual(registry.resolve_workspace(nested, config), local.resolve())

    def test_resolves_registered_workspace_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "learning"
            elsewhere = root / "elsewhere"
            workspace.mkdir()
            elsewhere.mkdir()
            config = root / "config.json"
            initializer.initialize(workspace, "en", config)

            self.assertEqual(registry.resolve_workspace(elsewhere, config), workspace.resolve())

    def test_distribution_manifests_reference_the_canonical_skill(self):
        plugin = json.loads(
            (ROOT / "plugins" / "techne" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

        self.assertEqual(plugin["name"], "techne")
        self.assertEqual(marketplace["plugins"][0]["name"], "techne")
        self.assertEqual(marketplace["plugins"][0]["source"], "./plugins/techne")
        self.assertEqual(marketplace["plugins"][0]["version"], plugin["version"])
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())

    def test_shipped_changes_bump_the_plugin_version(self):
        # Claude Code caches plugins by version: plugin changes since the last
        # upstream commit must come with a version different from upstream's.
        def git(*args):
            return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)

        if git("rev-parse", "--verify", "--quiet", "origin/main").returncode != 0:
            self.skipTest("no origin/main to compare against")
        changed = git("diff", "--name-only", "origin/main", "--", "plugins/techne").stdout.split()
        if not changed:
            return
        upstream = git("show", "origin/main:plugins/techne/.claude-plugin/plugin.json")
        if upstream.returncode != 0:
            self.skipTest("plugin manifest not on origin/main")
        current = json.loads((ROOT / "plugins" / "techne" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertNotEqual(
            json.loads(upstream.stdout)["version"],
            current["version"],
            f"plugin files changed ({', '.join(changed)}) without a version bump",
        )

    def test_every_documented_command_has_a_claude_slash_command(self):
        commands_dir = ROOT / "plugins" / "techne" / "commands"
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in ("init", "resume", "hint", "ask", "issue", "extract-issues", "status", "programs", "switch", "enroll", "leave", "pause", "end", "feedback", "reset", "uninstall"):
            self.assertIn(f"`{name}", skill)
            command = (commands_dir / f"{name}.md").read_text(encoding="utf-8")
            self.assertTrue(command.startswith("---\ndescription: "), name)
            self.assertIn(f"Techne `{name}` command", command)
        self.assertFalse((commands_dir / "lost.md").exists(), "lost was replaced by ask")


if __name__ == "__main__":
    unittest.main()
