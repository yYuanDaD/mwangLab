"""Fill the two changes lacking a surviving real example:
  #1  raw_da_method='auto' deterministic rule  -> GSE282641 (raw counts): rule picks DESeq2, recorded
  deg_sanity guard                              -> GSE317978 (fpkm->limma, 2v2): 66% DEG => flagged
One batch run (both cached, near-zero LLM). Prints the proofs from summary.csv + decisions.json.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_proof_0623.py
"""
import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.batch_tools import run_batch_geo_pipeline as _t
rbg = getattr(_t, "func", _t)

LABEL = "proof_0623"
OUT = f"output/cohort_{LABEL}"
TK = ["exercise", "training", "treated", "ko", "knockout", "mutant", "model", "disease"]
CK = ["control", "sedentary", "wt", "wildtype", "vehicle", "sham", "healthy", "normal", "pbs"]

print("running batch: GSE282641 (raw->auto rule) + GSE317978 (fpkm 2v2 -> deg_sanity), raw_da_method='auto'")
rbg(["GSE282641", "GSE317978"], organism="Mouse", treatment_keywords=TK, control_keywords=CK,
    output_base="./output", run_label=LABEL, raw_da_method="auto")

summ = pd.read_csv(os.path.join(OUT, "summary.csv"))
print("\n===== summary.csv (key cols) =====")
cols = [c for c in ["accession", "matrix_type", "da_method", "n_deg", "deg_sanity", "status"] if c in summ.columns]
print(summ[cols].to_string(index=False))


def _decisions(gse):
    p = os.path.join(OUT, gse, "decisions.json")
    d = json.load(open(p, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("decisions", [])

print("\n===== PROOF #1 — raw_da_method='auto' deterministic rule (GSE282641) =====")
for r in _decisions("GSE282641"):
    if r.get("step") == "da_method_select":
        print(f"  da_method_select decision='{r.get('decision')}'  reason={str(r.get('reason'))[:90]}")
print("  summary da_method:", summ[summ['accession'] == 'GSE282641']['da_method'].iloc[0])

print("\n===== PROOF — deg_sanity guard (GSE317978, 2v2) =====")
ds = summ[summ['accession'] == 'GSE317978']['deg_sanity']
print("  summary deg_sanity:", ds.iloc[0] if len(ds) else "(none)")
for r in _decisions("GSE317978"):
    if r.get("step") in ("limma", "deseq2") and ("sanity" in str(r.get("status", "")) or r.get("flags")):
        print(f"  decision sanity_warning: flags={r.get('flags')}")

print("\n===== BONUS — gap-3 DA decision reasons present in this fresh run =====")
for r in _decisions("GSE282641"):
    if r.get("step") in ("deseq2", "gsea", "da_method_comparison") and r.get("reason"):
        print(f"  [{r['step']}] {str(r['reason'])[:88]}")
        break
print("\nDONE.")
