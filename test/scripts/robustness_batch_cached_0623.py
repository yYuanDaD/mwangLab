"""Robustness complement (near-zero LLM): stress the ANALYSIS-LAYER validations across MANY
distinct CACHED studies, bypassing search/paper-extraction. Directly exercises:
  * matrix-type classification + routing (raw_counts->DESeq2/edgeR/limma-voom 'all';
    fpkm_or_tpm->limma; log_transformed->limma; non-counts files -> rejected),
  * tar-merge fallback (_merged_from_tar studies),
  * contrast auto-detection + the gated LLM contrast validation,
  * GSEA incl. the integer-ID -> symbol sidecar fix,
  * graceful skip when no clean 2-group design is found (fail-soft, not crash).

Only LLM cost = the small gated per-study contrast validation (~$0.005 each); the expensive
extraction/#5 calls are skipped entirely. Organisms are split into two batches so GSEA's
species Hallmark library matches. Outputs under output/_kw_robustness/.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/robustness_batch_cached_0623.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.batch_tools import run_batch_geo_pipeline as _rbg_tool

# run_batch_geo_pipeline is a @tool (StructuredTool) -> call the underlying function directly
run_batch_geo_pipeline = getattr(_rbg_tool, "func", _rbg_tool)

OUT_BASE = "./output/_kw_robustness"

# diverse cached studies spanning matrix types + edge cases (organism-grouped for GSEA)
MOUSE = ["GSE117161", "GSE164798", "GSE282641", "GSE297707",   # raw counts (various)
         "GSE132520", "GSE283234", "GSE302944",                # fpkm / tpm / log
         "GSE283691",                                          # merged-from-tar
         "GSE317978",                                          # known classify edge (fpkm+diffexp cols)
         "GSE315612"]                                          # DE-result tables (should be rejected, not crash)
HUMAN = ["GSE163356", "GSE202295", "GSE130401"]                # counts+logCPM / counts / FPKM

# BROAD keywords (not exercise-only) so the contrast detector finds a 2-group split in more studies
TK = ["exercise", "training", "treated", "treatment", "ko", "knockout", "mutant", "model",
      "disease", "stim", "stimulated", "hfd", "aged", "old", "post", "run", "tumor", "infected"]
CK = ["control", "sedentary", "wt", "wildtype", "wild-type", "vehicle", "sham", "healthy",
      "normal", "baseline", "young", "chow", "untreated", "naive", "pre", "rest"]


def _run(accessions, organism, label):
    print("=" * 80)
    print(f"BATCH {label}: {len(accessions)} {organism} studies")
    print("=" * 80)
    try:
        msg = run_batch_geo_pipeline(accessions, organism=organism,
                                     treatment_keywords=TK, control_keywords=CK,
                                     output_base=OUT_BASE, run_label=label, raw_da_method="all")
        print(msg[:400])
    except Exception as e:
        print(f"!! batch raised: {type(e).__name__}: {e}")
    summ = os.path.join(OUT_BASE, f"cohort_{label}", "summary.csv")
    df = pd.read_csv(summ) if os.path.isfile(summ) else pd.DataFrame()
    if not df.empty:
        df["organism"] = organism
    return df


m = _run(MOUSE, "Mouse", "batch_mouse")
h = _run(HUMAN, "Human", "batch_human")
df = pd.concat([m, h], ignore_index=True) if not (m.empty and h.empty) else pd.DataFrame()

print("\n" + "=" * 110)
print("ANALYSIS-LAYER ROBUSTNESS — across distinct cached studies")
print("=" * 110)
if df.empty:
    print("no summary rows produced.")
    sys.exit(0)

cols = [c for c in ["accession", "organism", "matrix_type", "da_method", "n_contrasts",
                    "n_deg", "n_gsea_sig", "llm_validated", "status"] if c in df.columns]
with pd.option_context("display.max_colwidth", 22, "display.width", 240):
    print(df[cols].to_string(index=False))

# coverage histogram
print("\n--- matrix-type coverage (classification routing) ---")
if "matrix_type" in df:
    print(df["matrix_type"].fillna("(none/skipped)").value_counts().to_string())
print("\n--- status distribution (did it complete / skip gracefully / crash) ---")
if "status" in df:
    print(df["status"].fillna("(none)").value_counts().to_string())

# GSEA + DA outcomes
def _num(s):
    return pd.to_numeric(s, errors="coerce")

n = len(df)
ran_da = int((_num(df.get("n_deg")).notna()).sum()) if "n_deg" in df else 0
ran_gsea = int((_num(df.get("n_gsea_sig")).notna()).sum()) if "n_gsea_sig" in df else 0
print("\n--- verdict ---")
print(f"  studies processed: {n}")
print(f"  reached DA (a 2-group contrast was found): {ran_da}/{n}")
print(f"  reached GSEA (sig count recorded): {ran_gsea}/{n}")
print(f"  matrix types classified: {sorted(df['matrix_type'].dropna().unique()) if 'matrix_type' in df else '?'}")
# anything that looks like a hard failure vs a graceful skip
hard = df[df["status"].astype(str).str.contains("error|exception|crash", case=False, na=False)] if "status" in df else pd.DataFrame()
print(f"  hard failures (crash/exception in status): {len(hard)}")
print("  (statuses like preprocess_ok_no_design / deg_ok_gsea_failed are GRACEFUL skips, not crashes)")
print("=" * 110)
df.to_csv(os.path.join(OUT_BASE, "robustness_batch_summary.csv"), index=False)
print("saved:", os.path.join(OUT_BASE, "robustness_batch_summary.csv"))
