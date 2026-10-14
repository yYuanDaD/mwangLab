"""Mirror agent skills into the folders Codex and Claude Code discover.

Sources of truth:
    agent_skills/bioinformatics-workflow/          -> .agents/skills/, .claude/skills/
    .agents/skills/evaluate-bioinformatics-agent/  -> .claude/skills/

Usage:
    python scripts/sync_skills.py                        refresh the project mirrors
    python scripts/sync_skills.py --check                exit 1 if a mirror has drifted
    python scripts/sync_skills.py --install-user claude  copy to ~/.claude/skills (also: codex, all)

Copies are byte-for-byte (no symlinks), so they work on Windows checkouts.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "bioinformatics-workflow": ("agent_skills/bioinformatics-workflow",
                                [".agents/skills/bioinformatics-workflow",
                                 ".claude/skills/bioinformatics-workflow"]),
    "evaluate-bioinformatics-agent": (".agents/skills/evaluate-bioinformatics-agent",
                                      [".claude/skills/evaluate-bioinformatics-agent"]),
}
USER_DIRS = {"codex": Path.home() / ".agents" / "skills", "claude": Path.home() / ".claude" / "skills"}
IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc"}


def _files(root: Path) -> dict[str, bytes]:
    out = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_file() and not IGNORED_PARTS & set(rel.parts) and path.suffix not in IGNORED_SUFFIXES:
            out[rel.as_posix()] = path.read_bytes()
    return out


def _mirror(source: Path, target: Path) -> None:
    wanted = _files(source)
    if target.exists():
        for rel in _files(target):
            if rel not in wanted:
                (target / rel).unlink()
    for rel, data in wanted.items():
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
    for folder in sorted((p for p in target.rglob("*") if p.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()


def drift() -> list[str]:
    problems = []
    for name, (source, targets) in SKILLS.items():
        wanted = _files(ROOT / source)
        for target in targets:
            actual = _files(ROOT / target) if (ROOT / target).exists() else {}
            for rel in sorted(set(wanted) | set(actual)):
                if wanted.get(rel) != actual.get(rel):
                    problems.append(f"{target}/{rel} differs from {source}/{rel}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--install-user", choices=["codex", "claude", "all"])
    args = parser.parse_args()
    if args.check:
        problems = drift()
        print("\n".join(problems) if problems else "skill mirrors are in sync")
        return 1 if problems else 0
    if args.install_user:
        agents = list(USER_DIRS) if args.install_user == "all" else [args.install_user]
        for agent in agents:
            for name, (source, _) in SKILLS.items():
                _mirror(ROOT / source, USER_DIRS[agent] / name)
                print(f"installed {name} -> {USER_DIRS[agent] / name}")
        print(f"Set MWANGLAB_ROOT={ROOT} if the agent will run outside this repository.")
        return 0
    for name, (source, targets) in SKILLS.items():
        for target in targets:
            _mirror(ROOT / source, ROOT / target)
            print(f"synced {source} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
