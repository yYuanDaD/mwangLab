"""Reproducibility harness: run the SAME-keyword Agent A cohort N times and score determinism.

Goal — answer "同一个关键词多跑几次效果如何 + 之前那几条达没达标":
  * #3 determinism: which SEA-CDM tables are BYTE-IDENTICAL across reps (expected: the
    metadata-derived structural tables subject/sample/groups/assay; the LLM-text tables
    study/experiment/interventions/material are expected to vary in wording).
  * #7/#7b chain: is chain_view (the pathway<->exercise chain) identical run-to-run
    (GSEA seed=42 + deterministic loader => should be).
  * #5/#6/#8 + DA: are reported-findings count, agreement tallies, DEG counts and the
    search top-hit stable.

Label-bearing file PATHS (gsea_source / file_access contain the run label) are normalized out
before hashing, so only TRUE content differences count as non-determinism — not the label.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/repro_cohort_0622.py
"""
import os
import sys
import glob
import hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

N_REPS = 3
KEYWORD = "voluntary wheel running mouse skeletal muscle RNA sequencing"
PARAMS = dict(
    keyword=KEYWORD, max_papers=1, organism="Mouse", with_analysis=True,
    treatment_keywords=["exercise", "training", "trained", "post", "run", "HIIT", "endurance"],
    control_keywords=["sedentary", "control", "pre", "rest", "sham", "untrained"],
    raw_da_method="all", require_pdf=True, search_pool=25,
    output_base="./output", max_chars=24000, extract_findings=True,
)


def _norm(text: str, label: str) -> str:
    """Strip the run label so label-bearing paths don't masquerade as non-determinism."""
    return text.replace(label, "REP").replace(label.replace("_", "-"), "REP")


def _hash_table(csv_path: str, label: str):
    if not os.path.isfile(csv_path):
        return None, 0
    with open(csv_path, encoding="utf-8") as f:
        raw = f.read()
    norm = _norm(raw, label)
    nrows = max(0, raw.count("\n") - 1)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12], nrows


def _chain_set(csv_path: str, label: str):
    """The chain_view as a label-normalized set of chain strings (order-independent)."""
    if not os.path.isfile(csv_path):
        return set()
    d = pd.read_csv(csv_path).fillna("")
    col = "chain" if "chain" in d.columns else d.columns[0]
    return {_norm(str(s), label) for s in d[col]}


# the BIOLOGICAL core of a chain — independent of the human-readable `exercise` descriptor, which
# is built from interventions (an LLM-text table) and so inherits that table's wording variance.
_CHAIN_CORE = ["contrast_label", "pathway_id", "direction", "nes", "fdr"]


def _chain_core_set(csv_path: str):
    if not os.path.isfile(csv_path):
        return set()
    d = pd.read_csv(csv_path).fillna("")
    cols = [c for c in _CHAIN_CORE if c in d.columns]
    return {tuple(str(v) for v in row) for row in d[cols].itertuples(index=False, name=None)}


# ---------------- run N reps (one process => shared GMT/MyGene cache) ----------------
labels, dirs = [], []
for r in range(1, N_REPS + 1):
    label = f"repro_r{r}"
    print("=" * 80)
    print(f"REP {r}/{N_REPS}  label={label}")
    print("=" * 80)
    rep = run_agent_a_cohort(run_label=label, **PARAMS)
    print(rep.splitlines()[0] if rep else "(no report)")
    labels.append(label)
    dirs.append(os.path.join("output", f"agentA_cohort_{label}", "csv"))

# ---------------- determinism scorecard ----------------
TABLES = ["study", "subject", "sample", "groups", "assay", "experiment", "interventions",
          "material", "analysis", "results", "pathway", "enrichment", "chain_view"]
STRUCTURAL = {"subject", "sample", "groups", "assay"}          # expected byte-identical (#3)

print("\n" + "=" * 80)
print(f"DETERMINISM SCORECARD  ({N_REPS} reps, same keyword)  — label-paths normalized out")
print("=" * 80)
print(f"{'table':14s} {'rows':>5s}  {'identical?':11s}  distinct-hashes")
ident_struct, varied = [], []
for t in TABLES:
    hashes, rows = [], []
    for lbl, d in zip(labels, dirs):
        h, n = _hash_table(os.path.join(d, f"{t}.csv"), lbl)
        hashes.append(h); rows.append(n)
    present = [h for h in hashes if h is not None]
    if not present:
        continue
    distinct = sorted(set(present))
    same = len(distinct) == 1 and len(present) == N_REPS
    tag = "IDENTICAL" if same else "VARIES"
    print(f"{t:14s} {rows[0]:>5d}  {tag:11s}  {distinct}")
    if t in STRUCTURAL and same:
        ident_struct.append(t)
    if not same and t in STRUCTURAL:
        varied.append(t)

# chain (#7b) — separate the BIOLOGICAL core (contrast->pathway->NES/FDR/dir) from the full
# string. The core is what relational queries use; the full string also embeds the LLM-text
# `exercise` descriptor, so it can vary purely from interventions wording (not a chain defect).
cores = [_chain_core_set(os.path.join(d, "chain_view.csv")) for d in dirs]
core_same = all(c == cores[0] for c in cores) and len(cores[0]) > 0
csets = [_chain_set(os.path.join(d, "chain_view.csv"), lbl) for lbl, d in zip(labels, dirs)]
str_same = all(c == csets[0] for c in csets) and len(csets[0]) > 0
print(f"\n#7b chain_view: {[len(c) for c in cores]} chains/rep")
print(f"   CORE (contrast,pathway,dir,NES,FDR): {'IDENTICAL' if core_same else 'DIFFERS'}")
print(f"   full string (core + exercise descriptor): {'IDENTICAL' if str_same else 'DIFFERS'}")
if core_same and not str_same:
    descs = [sorted({r.split(' | ')[0] for r in c}) for c in csets]
    print("   -> divergence is ONLY the LLM-text descriptor (interventions), e.g.:")
    for r, dlist in enumerate(descs, 1):
        print(f"      rep{r}: {dlist}")

# DA / #5 / #6 stability from results+analysis
print("\nDA / #5 / #6 stability:")
for lbl, d in zip(labels, dirs):
    res = os.path.join(d, "results.csv")
    n_res = len(pd.read_csv(res)) if os.path.isfile(res) else 0
    anal = os.path.join(d, "analysis.csv")
    a = pd.read_csv(anal) if os.path.isfile(anal) else pd.DataFrame()
    txt = int((a.get("da_method") == "text-mining").sum()) if "da_method" in a else 0
    print(f"   {lbl}: results={n_res} rows, analysis={len(a)} rows ({txt} text-mining)")

print("\n" + "=" * 80)
print("VERDICT")
print(f"  #3 structural determinism: {sorted(ident_struct)} byte-identical"
      + (f"; VARIED(unexpected): {varied}" if varied else "  (all 4 as expected)"))
print(f"  DA+GSEA tables (analysis/results/pathway/enrichment): see scorecard above")
print(f"  #7b chain CORE reproducibility: {'PASS — identical biology' if core_same else 'CHECK — core differs'}"
      + ("" if str_same else "  (full string varies ONLY via the LLM-text exercise descriptor)"))
print("  (study/experiment/interventions/material varying = expected LLM-text paraphrase, not a defect)")
print("=" * 80)
