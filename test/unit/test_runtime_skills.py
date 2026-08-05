"""Offline tests for runtime skill discovery and bounded loading."""

from pathlib import Path
import tempfile
import unittest

from tools.runtime_skills import (
    discover_runtime_skills,
    load_runtime_skill_bundle,
    render_runtime_skill_catalog,
)


class RuntimeSkillTests(unittest.TestCase):
    def test_discovers_project_skill_and_renders_metadata_only(self):
        skills = discover_runtime_skills()
        selected = next(skill for skill in skills if skill.name == "paper-workflow-safety")
        catalog = render_runtime_skill_catalog(skills)
        self.assertIn(selected.description, catalog)
        self.assertNotIn("GSE279359", catalog)

    def test_loads_instructions_and_safe_references(self):
        bundle = load_runtime_skill_bundle("paper-workflow-safety")
        self.assertIn("RUNTIME SKILL LOADED: paper-workflow-safety", bundle)
        self.assertIn("curated-example.json", bundle)
        self.assertIn("GSE279359", bundle)
        self.assertIn("Never use DESeq2 or limma-voom on FPKM/TPM", bundle)

    def test_unknown_skill_does_not_become_a_path(self):
        with self.assertRaises(ValueError):
            load_runtime_skill_bundle("../../.env")

    def test_duplicate_names_fail_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ("a", "b"):
                path = root / folder
                path.mkdir()
                (path / "SKILL.md").write_text(
                    "---\nname: duplicate\ndescription: test\n---\nDo work.\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                discover_runtime_skills(root)


if __name__ == "__main__":
    unittest.main()
