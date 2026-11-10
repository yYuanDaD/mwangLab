"""Execute the rebuilt specs and compare DEG counts with the original large-run numbers.

    python test/experiments/case_runner_validation_20261028/make_specs.py --pdf-root E:/agent/mwangLab_pdf
    python test/experiments/case_runner_validation_20261028/run_validation.py

Writes runs/comparison.json and prints one line per result table.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def main() -> int:
    expected = json.loads((RUNS / "expected.json").read_text(encoding="utf-8"))
    rows, ok = [], True
    for paper, want in expected.items():
        spec = RUNS / paper / "case_spec.json"
        start = time.time()
        proc = subprocess.run([sys.executable, "-m", "tools.case_runner", "execute", str(spec)],
                              capture_output=True, text=True, encoding="utf-8")
        seconds = round(time.time() - start, 1)
        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError:
            rows.append({"paper": paper, "error": (proc.stdout + proc.stderr)[-2000:]})
            ok = False
            continue
        case = result["cases"][0]
        got = {}
        for runs in (case.get("executions") or {}).values():
            for name, value in runs.items():
                got[name] = value.get("n")
        for name, n_old in want.items():
            rows.append({"paper": paper, "table": name, "original": n_old, "case_runner": got.get(name),
                         "same": got.get(name) == n_old})
            ok &= got.get(name) == n_old
        rows.append({"paper": paper, "seconds": seconds, "validator_errors": result["validator"]["errors"],
                     "case_error": case.get("error"), "enrichment": case.get("enrichment"),
                     "suitability": (case.get("suitability") or {}).get("verdict")})
        ok &= not result["validator"]["errors"] and "error" not in case
    (RUNS / "comparison.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    for r in rows:
        print(json.dumps(r, ensure_ascii=False, default=str)[:600])
    print("ALL SAME" if ok else "DIFFERENCES OR ERRORS (see runs/comparison.json)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
