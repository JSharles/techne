from __future__ import annotations

import importlib.util
import json
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
validator = load_module("techne_validator", SKILL_ROOT / "scripts" / "validate_workspace.py")


class WorkspaceTests(unittest.TestCase):
    def test_initializes_and_validates_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            config = workspace / "registry" / "config.json"
            state_root = initializer.initialize(workspace, config)

            self.assertEqual(state_root, (workspace / ".techne").resolve())
            self.assertEqual(validator.validate(state_root), [])
            self.assertTrue((state_root / "browser" / "lessons").is_dir())
            self.assertIn(str(workspace), (state_root / "STATE.json").read_text(encoding="utf-8"))
            self.assertEqual(registry.load_active_workspace(config), workspace.resolve())

    def test_refuses_to_overwrite_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            initializer.initialize(workspace)
            with self.assertRaises(FileExistsError):
                initializer.initialize(workspace)

    def test_resolves_local_workspace_before_registered_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registered = root / "registered"
            local = root / "local"
            registered.mkdir()
            local.mkdir()
            config = root / "config.json"
            initializer.initialize(registered, config)
            initializer.initialize(local)

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
            initializer.initialize(workspace, config)

            self.assertEqual(registry.resolve_workspace(elsewhere, config), workspace.resolve())

    def test_distribution_manifests_reference_the_canonical_skill(self):
        plugin = json.loads(
            (ROOT / "plugins" / "techne" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

        self.assertEqual(plugin["name"], "techne")
        self.assertEqual(marketplace["plugins"][0]["name"], "techne")
        self.assertEqual(marketplace["plugins"][0]["source"], "./plugins/techne")
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
