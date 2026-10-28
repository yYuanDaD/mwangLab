"""Record one finished paper of the 211-paper run: progress.csv row (via record_run.py) + PROBLEMS.md section.

    python test/experiments/large_run_pilot_20261019/finish_paper.py <paper_id> <gse> <minutes> <tokens> <status> "<vs_paper>" "<problems>"
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
paper_id, gse, minutes, tokens, status, note, problems = sys.argv[1:8]
subprocess.run([sys.executable, os.path.join(HERE, "record_run.py"), paper_id, gse, minutes, tokens, status, note],
               check=True)
if problems.strip() and problems.strip().lower() != "none":
    with open(os.path.join(HERE, "runs_claude", "PROBLEMS.md"), "a", encoding="utf-8") as f:
        f.write(f"\n## {paper_id} ({gse})\n\n- {problems.strip()} Details: `{paper_id}/HANDBACK.md`.\n")
