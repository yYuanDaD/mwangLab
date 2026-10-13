"""Validate decision-contract records: per-record fields and per-case invariants.

Usage (run with the Python environment that has the repository installed):
    python <skill_dir>/scripts/validate_decision_contract.py <run_dir or decisions.json> [...]
    python <skill_dir>/scripts/validate_decision_contract.py --legacy <old records>

A directory argument is searched for every decisions.json below it.
--legacy skips the stage-field checks for records written before contract v2;
case invariants still apply.

Checks structure and internal consistency only. It cannot tell whether a
decision matches the paper; that needs evidence review or a gold set.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _repo import import_repo  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--legacy", action="store_true")
    args = parser.parse_args()
    import_repo()
    from tools.decision_contract import validate

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("decisions.json")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"skipping missing path: {path}")
    if not files:
        print("INVALID\nno decision record files found")
        return 1
    count, errors = validate(files, legacy=args.legacy)
    if errors:
        print("INVALID")
        print("\n".join(errors))
        return 1
    print(f"VALID ({count} decision records in {len(files)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
