"""The workflow skill is a valid Agent Skill for Codex and Claude Code, and its copies are in sync."""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

SOURCES = [ROOT / "agent_skills/bioinformatics-workflow", ROOT / ".agents/skills/evaluate-bioinformatics-agent"]
COPIES = [ROOT / ".agents/skills/bioinformatics-workflow", ROOT / ".claude/skills/bioinformatics-workflow",
          ROOT / ".claude/skills/evaluate-bioinformatics-agent"]
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def frontmatter(skill_dir: Path) -> dict:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    assert match, f"{skill_dir}: SKILL.md must start with --- frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"\'')
    return fields


class SkillPackageTests(unittest.TestCase):
    def test_copies_are_in_sync(self):
        from scripts.sync_skills import drift

        self.assertEqual(drift(), [])

    def test_frontmatter_follows_agent_skills_spec(self):
        for skill in SOURCES + COPIES:
            fields = frontmatter(skill)
            self.assertEqual(fields.get("name"), skill.name, skill)
            self.assertRegex(fields["name"], r"^[a-z0-9-]{1,64}$")
            self.assertTrue(0 < len(fields.get("description", "")) <= 1024, skill)

    def test_relative_links_resolve(self):
        for skill in SOURCES:
            for doc in [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]:
                for target in LINK.findall(doc.read_text(encoding="utf-8")):
                    if "://" in target or target.startswith("<"):
                        continue
                    self.assertTrue((doc.parent / target).exists(), f"{doc}: broken link {target}")

    def test_no_machine_specific_paths(self):
        pattern = re.compile(r"[A-Z]:[\\\\/]Users[\\\\/]\w|/home/\w+/|/Users/\w+/")
        for skill in SOURCES:
            for path in skill.rglob("*"):
                if path.suffix in {".md", ".py", ".yaml"}:
                    self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")), path)

    def test_validator_script_runs_outside_the_repo(self):
        script = ROOT / ".claude/skills/bioinformatics-workflow/scripts/validate_decision_contract.py"
        result = subprocess.run([sys.executable, str(script), str(ROOT / "nonexistent")],
                                cwd=Path.home(), capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no decision record files found", result.stdout)


if __name__ == "__main__":
    unittest.main()
