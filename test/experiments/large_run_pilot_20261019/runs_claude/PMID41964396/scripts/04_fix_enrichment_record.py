"""03_resume_execution.py wrote the GSE276889 enrichment (not_run) record with input_threshold = {paper, applied};
case.finish rejected it (ORA input_threshold must equal the applied rule). The recorder has no amend call, so this
patches that one field in decisions.json in place: input_threshold -> the applied rule; the paper's ORA input rule
moves to paper_input_rule. Nothing else changes."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from common import RUN, PAPER_THRESHOLD

p = pathlib.Path(RUN) / "GSE276889_mRNA" / "decisions.json"
recs = json.loads(p.read_text(encoding="utf-8"))
n = 0
for r in recs:
    if r["stage"] == "enrichment" and isinstance(r["final"].get("input_threshold"), dict) and "applied" in r["final"]["input_threshold"]:
        r["final"]["paper_input_rule"] = r["final"]["input_threshold"]["paper"]
        r["final"]["input_threshold"] = PAPER_THRESHOLD
        r["final"]["record_patch"] = "input_threshold field patched by scripts/04_fix_enrichment_record.py"
        n += 1
assert n == 1, n
p.write_text(json.dumps(recs, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
print("patched", n, [r["stage"] for r in recs])
