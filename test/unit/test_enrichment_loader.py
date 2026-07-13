"""Minimal executable unit for tools/enrichment_loader — zero LLM, zero network (local GSEA CSV).

Proves: (1) every written row matches csv_columns(table) exactly; (2) pathway is deduped/shared;
(3) FK integrity (enrichment.pathway_id ∈ pathway, enrichment.analysis_id ∈ analysis, analysis'
treatment/control group ids ∈ groups); (4) the chain JOIN returns the expected GSE208615 pathways
with the FDR filter holding.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_enrichment_loader.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.sea_cdm_schema import csv_columns
from tools.enrichment_loader import load_enrichment_tables, query_chain

OUT = os.path.join("test", "output", "test_enrichment_loader")

STUDIES = [
    ("GSE208615",
     "output/agentA_cohort_test3_exercise_rnaseq/cohort_analysis/GSE208615/"
     "DEG_results_14-0-0_vs_0-0-0_GSEA_Hallmark.csv", "mh.all@2024.1.Mm"),
]

rep = {}
written = load_enrichment_tables(STUDIES, OUT, fdr_cutoff=0.25, report=rep)
print("loaded rows:", rep)

# (1) every written row matches csv_columns(table) exactly
for table in ("analysis", "groups", "pathway", "enrichment"):
    df = pd.read_csv(os.path.join(OUT, f"{table}.csv"))
    assert list(df.columns) == csv_columns(table), f"{table}.csv columns != csv_columns({table})"
print("[1] all 4 CSVs have exactly their csv_columns() header")

A = pd.read_csv(os.path.join(OUT, "analysis.csv"))
G = pd.read_csv(os.path.join(OUT, "groups.csv"))
P = pd.read_csv(os.path.join(OUT, "pathway.csv"))
E = pd.read_csv(os.path.join(OUT, "enrichment.csv"))

# (2) pathway deduped (one row per distinct id) and shared key is unique
assert P["pathway_id"].is_unique, "pathway_id must be unique (deduped node)"
assert len(E) >= len(P), "should be >=1 enrichment edge per pathway"
print(f"[2] pathway deduped: {len(P)} distinct nodes for {len(E)} edges")

# (3) FK integrity
assert set(E["pathway_id"]) <= set(P["pathway_id"]), "enrichment.pathway_id must FK into pathway"
assert set(E["analysis_id"]) <= set(A["analysis_id"]), "enrichment.analysis_id must FK into analysis"
gids = set(G["group_id"])
assert set(A["treatment_group_id"]) <= gids and set(A["control_group_id"]) <= gids, \
    "analysis treatment/control group ids must FK into groups"
assert E["enrichment_id"].is_unique, "enrichment_id PK must be unique"
print("[3] FK integrity: enrichment->pathway, enrichment->analysis, analysis->groups all close")

# (4) the chain JOIN
chain = query_chain(OUT, study_id="GSE208615")
assert (chain["fdr"] < 0.25).all(), "FDR filter must hold in the JOIN output"
assert (chain["t_subject_group"] == "14-0-0").all(), "treatment arm must be the exercise arm"
assert (chain["c_subject_group"] == "0-0-0").all(), "control arm must be sedentary"
top = chain.reindex(chain["nes"].abs().sort_values(ascending=False).index)
assert top.iloc[0]["pathway_name"] == "Protein Secretion", top.iloc[0]["pathway_name"]
print(f"[4] chain JOIN: {len(chain)} pathways for the 14-0-0 vs 0-0-0 exercise contrast")
print(top[["pathway_name", "direction", "nes", "fdr"]].head(5).to_string(index=False))

# (5) raw_da_method='all' filenames carry a '__<method>' suffix — it must NOT leak into the
#     control arm, else the enrichment->groups FK breaks (regression: GSE279359 rerun 2026-06-22
#     left control_group_id null for all 3 contrasts because ctrl parsed as 'pre-exercise  deseq2').
from tools.pathway_chain_tools import _parse_gsea_contrast
from tools.enrichment_loader import _rows_for_gsea

assert _parse_gsea_contrast("DEG_results_a_vs_b_GSEA_Hallmark.csv") == "a vs b"
for meth in ("deseq2", "edger", "limma-voom", "limma"):
    got = _parse_gsea_contrast(
        f"DEG_results_immediately_post-exercise_vs_pre-exercise__{meth}_GSEA_Hallmark.csv")
    assert got == "immediately post-exercise vs pre-exercise", (meth, got)
print("[5] _parse_gsea_contrast strips the '__<method>' suffix (single- and multi-method names)")

# cohort-mode FK resolution: a '__deseq2' GSEA file must still resolve BOTH arms to real groups.
glut = {"immediately post-exercise": "G_treat", "pre-exercise": "G_ctrl"}
fake_gsea = STUDIES[0][1].replace("14-0-0_vs_0-0-0",
                                  "immediately_post-exercise_vs_pre-exercise__deseq2")
# the file at fake_gsea path doesn't exist; only the contrast parse (filename) drives FK resolution,
# and _rows_for_gsea reads pathway rows from the file — so point it at the real GSEA CSV's rows by
# parsing the contrast from a synthesized name while reading bodies from the real file.
import shutil
_tmp = os.path.join(OUT, os.path.basename(fake_gsea))
shutil.copy(STUDIES[0][1], _tmp)
a, g, p, e = _rows_for_gsea("GSE279359", _tmp, "mh.all@2024.1.Mm", 1, 0.25, groups_lookup=glut)
assert a["treatment_group_id"] == "G_treat" and a["control_group_id"] == "G_ctrl", a
assert a["contrast_label"] == "immediately post-exercise vs pre-exercise", a["contrast_label"]
print("[6] cohort-mode FK: a '__deseq2' GSEA file resolves BOTH arms to real groups (0 unresolved)")

print("\nPASS — enrichment_loader: GSEA -> schema-conformant pathway/enrichment/analysis/groups "
      "rows, FK-closed, the pathway<->exercise chain is a working JOIN, and the multi-method "
      "'__<method>' filename suffix no longer breaks contrast-arm -> groups FK resolution.")
