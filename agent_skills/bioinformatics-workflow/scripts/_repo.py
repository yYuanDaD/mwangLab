"""Locate the mwangLab repository that provides this skill's tools.

Search order: the MWANGLAB_ROOT environment variable, the current directory
and its parents, then the directories above this script (a project-level
install lives inside the repository).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

MARKERS = ("tools/native.py", "tools/decision_contract.py")


def _is_repo(path: Path) -> bool:
    return all((path / marker).is_file() for marker in MARKERS)


def find_repo() -> Path | None:
    env = os.environ.get("MWANGLAB_ROOT")
    candidates = [Path(env).expanduser()] if env else []
    cwd = Path.cwd().resolve()
    candidates += [cwd, *cwd.parents]
    here = Path(__file__).resolve().parent
    candidates += list(here.parents)
    for path in candidates:
        if _is_repo(path):
            return path
    return None


def import_repo() -> Path:
    root = find_repo()
    if root is None:
        raise SystemExit(
            "mwangLab repository not found. Run from inside the repository, or set "
            "MWANGLAB_ROOT to its path (see references/setup.md)."
        )
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root
