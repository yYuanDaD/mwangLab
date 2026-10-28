"""Print the subagent prompt (PROMPT_211.md) for rows of queue_211.csv.

    python test/experiments/large_run_pilot_20261019/prompt_for.py <n> [<n> ...]
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
doc = open(os.path.join(HERE, "PROMPT_211.md"), encoding="utf-8").read()
template = doc.split("\n---\n")[1].strip()
full = re.search(r"Full text available: `(.+?)`", doc).group(1)
none = re.search(r"No full text: `(.+?)`", doc).group(1)
rows = {r["n"]: r for r in csv.DictReader(open(os.path.join(HERE, "queue_211.csv"), encoding="utf-8"))}
for n in sys.argv[1:]:
    r = rows[n]
    gses = r["gse"].split(";")
    pid = r["paper_id"]
    print(f"### n={n} paper_id={pid} gse={r['gse']}")
    print(template.format(
        paper_files=full.format(paper_md=r["paper_md"].replace("/", "\\")) if r["paper_md"] else none,
        gse_list=gses[0] if len(gses) == 1 else ", ".join(gses[:-1]) + " and " + gses[-1],
        paper_ref=f"PMID {pid[4:]}" if pid.startswith("PMID") else "the paper",
        title=r["title"], paper_id=pid))
    print()
