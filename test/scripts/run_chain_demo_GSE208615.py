"""REAL full-chain (#7) demo on GSE208615 / PMC11076285 (exercise epigenetics paper).

This study is the one local case with BOTH halves available REAL:
  - a SUCCESSFUL GSEA (mouse-symbol leading-edge genes) from the test3 exercise cohort
  - a cached full paper text we can text-mine (#5)

It was analysed before #5 existed, so we补跑 ONE #5 call here, then run the deterministic #7 join.
Cost = 1 structured LLM call (~25k input tok, under the 30k/min limit). Everything else is local.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_chain_demo_GSE208615.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.seacdm_tools import build_reported_findings
from tools.pathway_chain_tools import build_pathway_chain

STUDY = "GSE208615"
ORG = "Mouse"
TEXT = "data/papers/ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt"
GSEA = ["output/agentA_cohort_test3_exercise_rnaseq/cohort_analysis/GSE208615/"
        "DEG_results_14-0-0_vs_0-0-0_GSEA_Hallmark.csv"]
OUT = "output/agentA_chain_demo_GSE208615"
os.makedirs(OUT, exist_ok=True)

paper_text = open(TEXT, encoding="utf-8", errors="ignore").read()[:100000]
print(f"paper: {len(paper_text)} chars (PMC11076285, exercise epigenetics)\n")

# --- step 1: #5 text-mined findings (1 LLM call) -----------------------------------------
findings_csv = os.path.join(OUT, f"{STUDY}_reported_findings.csv")
frep = {}
print("[#5] extracting reported findings (1 LLM call)...")
build_reported_findings(STUDY, paper_text, findings_csv, organism=ORG, report=frep)
fdf = pd.read_csv(findings_csv) if os.path.isfile(findings_csv) else pd.DataFrame()
print(f"[#5] {len(fdf)} findings  (unverified={frep.get('n_unverified')}, snapped={frep.get('n_snapped')})")
gene_findings = fdf[fdf["entity_type"].isin(["gene", "protein"])]["entity"].tolist() if len(fdf) else []
path_findings = fdf[fdf["entity_type"] == "pathway"]["entity"].tolist() if len(fdf) else []
print(f"      gene/protein entities: {gene_findings[:20]}")
print(f"      pathway entities:      {path_findings[:20]}\n")

# --- step 2: #7 mechanism chain (deterministic join) -------------------------------------
chain_csv = os.path.join(OUT, f"{STUDY}_pathway_chain.csv")
crep = {}
build_pathway_chain(STUDY, GSEA, findings_csv=findings_csv, out_csv=chain_csv, report=crep)
print("[#7] chain report:", crep, "\n")

ch = pd.read_csv(chain_csv).fillna("")
comp = ch[ch["source"].str.startswith("computational")]
print(f"=== computational GSEA pathways ({len(comp)}), contrast = exercise vs sedentary ===")
for _, r in comp.iterrows():
    link = f"  <-- DRIVER GENES IN PAPER: {r['genes_paper_reported']}" if r["genes_paper_reported"] else ""
    named = "  [paper names this pathway]" if r["cross_support"] else ""
    print(f"  {r['pathway']:34s} {r['direction']:4s} NES={r['nes']:>5} FDR={r['fdr']}{named}{link}")

linked = comp[comp["genes_paper_reported"] != ""]
print(f"\n=== FULL CHAIN LINKS (exercise -> pathway -> gene, all 3 real) : {len(linked)} ===")
for _, r in linked.iterrows():
    print(f"  exercise ({r['contrast']}) -> {r['pathway']} ({r['direction']}, NES={r['nes']}) "
          f"-> {r['genes_paper_reported']}")

text_rows = ch[ch["source"].str.startswith("text")]
print(f"\n=== text-claimed pathways ({len(text_rows)}) — gap analysis ===")
for _, r in text_rows.iterrows():
    print(f"  {r['pathway'][:44]:44s} {r['direction']:8s} | {r['cross_support']}")

print(f"\nArtifacts: {chain_csv}\n           {findings_csv}")
