"""Write prompts/<paper_id>.txt from prompt_for.py with the experiment's edits."""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BS = chr(92)
MC = os.path.join("E:" + BS, "agent", "mwangLab_mc")
PDF = os.path.join("E:" + BS, "agent", "mwangLab_pdf")
ROWS = ["24", "2", "27", "18", "8", "13"]
RUNS = BS.join(["test", "experiments", "large_run_pilot_20261019", "runs_claude"])
FORBID = (f"Do not read anything under {RUNS}, {BS.join(['test', 'experiments', 'case_runner_*'])}, or "
          f"{BS.join(['test', 'experiments', 'model_compare_20261103'])} outside your own run directory, "
          "in either checkout. Do not edit any code.")

out = subprocess.run([sys.executable, os.path.join(MC, "test", "experiments", "large_run_pilot_20261019", "prompt_for.py"), *ROWS],
                     capture_output=True, text=True, encoding="utf-8", check=True).stdout
for block in re.split(r"(?m)^### ", out)[1:]:
    head, body = block.split("\n", 1)
    pid = re.search(r"paper_id=(\S+)", head).group(1)
    md = body.split("Paper files: " + PDF + BS)[1].split(" and the ")[0]
    root = MC if os.path.exists(os.path.join(MC, md)) else PDF
    body = body.replace("Paper files: " + PDF + BS + md, "Paper files: " + root + BS + md)
    body = body.replace("repository checkout " + PDF, "repository checkout " + MC)
    body = body.replace("Run every command from " + PDF + " with", "Run every command from " + MC + " with")
    body = body.replace(PDF + BS + ".claude", MC + BS + ".claude")
    body = body.replace(f"test/experiments/large_run_pilot_20261019/runs_claude/{pid}",
                        f"test/experiments/model_compare_20261103/runs/<model>/{pid}")
    old = f"Do not open other papers' folders under {RUNS}."
    assert old in body
    body = body.replace(old, FORBID)
    with open(os.path.join(HERE, "prompts", pid + ".txt"), "w", encoding="utf-8") as f:
        f.write(body.strip() + "\n")
