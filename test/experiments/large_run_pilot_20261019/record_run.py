"""Append one finished paper to runs_claude/progress.csv (runs the decision-contract validator).

    python test/experiments/large_run_pilot_20261019/record_run.py <paper_id> <gse> <minutes> <tokens> <status> "<comparison note>"
"""
import csv
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
paper_id, gse, minutes, tokens, status, note = sys.argv[1:7]
run_dir = os.path.join(HERE, "runs_claude", paper_id)
validator = os.path.join(ROOT, ".agents", "skills", "bioinformatics-workflow", "scripts", "validate_decision_contract.py")
proc = subprocess.run([sys.executable, validator, run_dir], capture_output=True, text=True,
                      encoding="utf-8", errors="replace", cwd=ROOT,
                      env={**os.environ, "PYTHONIOENCODING": "utf-8"})
lines = [ln for ln in (proc.stdout + proc.stderr).strip().splitlines() if ln.strip()]
result = lines[-1][:200] if lines else f"exit {proc.returncode}"
path = os.path.join(HERE, "runs_claude", "progress.csv")
new = not os.path.exists(path)
with open(path, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["paper_id", "gse", "wall_minutes", "subagent_tokens", "status", "validator", "vs_paper"])
    w.writerow([paper_id, gse, minutes, tokens, status, result, note])
print(result)
