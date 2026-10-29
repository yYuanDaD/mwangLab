import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import json, os
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39356750"
run = native.RunRecorder.open(RUN)
case = run.case("GSE270400_12h_vs_NC")
paper = case.add_input("test/experiments/paper_screen_20261019/papers/PMC11446262.paper.json", "paper")
authdeg = case.add_input("data/GSE270400/GSE270400_DifGene.12hVSNC.All.fpkm.anno.txt.gz", "matrix")
deg = str(case.dir / "results" / "DEG_results_h12_vs_NC.csv")
dego = case.add_output(deg, "deg_table")
cnt = json.load(open(case.dir / "_exec_state.json"))["counts"]

# ---------------- audit: padj < 0.05 without fold-change cutoff (the rule that reproduces the paper's 51/42)
t = pd.read_csv(deg, index_col=0)
a = pd.read_csv(authdeg["path"], sep="\t", index_col=0)
pc_ids = set(a.index[a["gene_biotype"] == "protein_coding"])
ann = pd.read_csv("data/GSE270400/GSE270400_Expression.All.fpkm.anno.txt.gz", sep="\t", index_col=0)
bt_col = next((c for c in ann.columns if "biotype" in c.lower()), None)
if bt_col:
    pc_ids |= set(ann.index[ann[bt_col] == "protein_coding"])
pc = t.index.isin(pc_ids)
aud = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
s = (t["padj"] < 0.05)
audit = {"rule": "padj < 0.05, no fold-change cutoff (audit; reproduces the paper's reported 12 h counts in the authors' own table)",
         "threshold_source": "audit",
         "ours_all_genes": {k: aud[k] for k in ("n_significant", "n_up", "n_down")},
         "ours_protein_coding": {"n": int((s & pc).sum()), "up": int((s & pc & (t.log2FoldChange > 0)).sum()),
                                 "down": int((s & pc & (t.log2FoldChange < 0)).sum())},
         "authors_table_protein_coding": {"n": int(((a.padj < 0.05) & (a.gene_biotype == "protein_coding")).sum()),
                                          "up": int(((a.padj < 0.05) & (a.gene_biotype == "protein_coding") & (a.log2FoldChange > 0)).sum()),
                                          "down": int(((a.padj < 0.05) & (a.gene_biotype == "protein_coding") & (a.log2FoldChange < 0)).sum())},
         "paper_reported": {"up": 51, "down": 42, "total": 93, "locator": "S2.4.p2"}}
print(json.dumps(audit, indent=1))
case.write_json("audit_threshold_counts.json", audit, role="audit_threshold_counts")

# ---------------- 10. enrichment (paper: GO BP ORA, clusterProfiler, all DEGs; fig. S16B, table S4)
fid = native.feature_id_report(deg)
print(json.dumps(fid, indent=1, default=str))
applied = {"metric": "padj", "adjustment": "BH (FDR)", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
           "effect_cutoff_original": "fold change >= 2", "inclusive": True, "source_locator": "S4.6.p1"}
eout = case.dir / "enrichment"
base = {"method": "ORA (Enrichr; GO BP/MF/CC 2023 + KEGG_2019_Mouse) via run_enrichment_analysis",
        "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2019_Mouse",
        "organism": "Rat", "feature_id_type": "ensembl_gene",
        "ortholog_mapping": "rat Ensembl -> rat symbol (MyGene.info, species=rat), then matched to mouse Enrichr libraries by identical symbol (tools/enrichment_tools.py:31-35)",
        "input_threshold": applied, "input_threshold_source": "applied", "direction": "all",
        "paper_method": "clusterProfiler v3.6.0 enrichGO BP, hypergeometric, BH (S4.6.p1)",
        "deviation_note": ("Enrichr (library background, mouse libraries by symbol) instead of clusterProfiler with rat GO; "
                           "tool filter is strict |log2FC| > 1 (enrichment_tools.py:222); no gene sits at exactly 1, so the list equals the applied rule")}
try:
    msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Rat",
                           padj_cutoff=0.05, log2fc_cutoff=1.0, direction="all", top_n=10, output_dir=str(eout))
    print(msg)
    outs = sorted(str(p) for p in eout.glob("*.csv"))
    items = [case.add_output(p, "enrichment_table") for p in outs]
    case.decide("enrichment", final=dict(base, outputs=outs), evidence=[dego] + items,
                paper={"locator": "S4.6.p1; S2.4.p2"}, confidence="medium", execution_status="completed",
                reasoning="Paper ran GO over-representation on all 12 h DEGs (fig. S16B, table S4); same gene list rule as the applied threshold.")
except native.NativeToolError as e:
    print("ENRICH FAIL", e)
    case.decide("enrichment", final=dict(base, execution_error=str(e)), evidence=[dego],
                paper={"locator": "S4.6.p1"}, confidence="medium", execution_status="failed",
                reasoning="Enrichment tool failed; DE result unaffected.")

# ---------------- discrepancies / plan / summary
disc = [
    {"item": "threshold", "paper_methods": "FC >= 2 and FDR < 0.05 (S4.6.p1)",
     "paper_reported_12h": "51 up / 42 down protein-coding (S2.4.p2)",
     "data": ("authors' own deposited DESeq2 table (GSE270400_DifGene.12hVSNC) gives 12 up / 16 down protein-coding under FC>=2 & padj<0.05, "
              "and exactly 51 / 42 under padj<0.05 with no fold-change cutoff"),
     "disposition": "executable_without_change",
     "note": "The reported 12 h count appears to omit the stated fold-change cutoff. Paper rule applied as stated; padj-only reported as audit."},
    {"item": "group size", "paper": "n = 6 per group in the one-time running study (S4.1.1.p1)", "data": "GEO: 4 per group",
     "disposition": "executable_without_change", "note": "RNA-seq n not stated in the paper; GEO subset used as deposited"},
    {"item": "implementation", "paper": "R DESeq2 1.30.1", "data": "pydeseq2 0.5.4",
     "disposition": "executable_without_change", "note": "log2FC Pearson r = 0.9999999 vs the authors' table"},
    {"item": "accession scope", "paper": "0 h vs NC in GSE269529 (Fig. 4, 358/281 DEGs)", "data": "GSE270400 holds only 12 h vs NC",
     "disposition": "executable_without_change", "note": "0 h contrast out of scope for this request"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
case.write_json("reproduction_plan.json", {"route": "paper_aligned", "accession": "GSE270400", "contrast": "h12 vs NC",
                                            "method": "DESeq2 ~ grp", "threshold": applied,
                                            "audit": "padj < 0.05 without FC cutoff"}, role="reproduction_plan")
case.write_json("reproduction_summary.json", {
    "paper_aligned": {"threshold": applied, "n_deg_all": cnt["n_significant"], "up": cnt["n_up"], "down": cnt["n_down"],
                      "protein_coding": cnt["protein_coding_scope"]},
    "authors_table_same_rule": cnt["authors_deposited_table_same_rule"],
    "concordance_with_authors_table": cnt["concordance_with_authors_table"],
    "audit_padj_only": audit,
    "paper_reported": {"up": 51, "down": 42, "scope": "protein-coding", "locator": "S2.4.p2"},
    "conclusion": ("DESeq2 reproduces the authors' deposited results almost exactly (log2FC r ~ 1). The paper's stated rule gives 30 "
                   "protein-coding DEGs (13 up / 17 down); the paper's 93 (51/42) matches padj<0.05 without the FC cutoff, "
                   "where we get the audit counts above.")}, role="reproduction_summary")

# ---------------- 11. study
case.decide("study", final={"route": "paper_aligned", "exploratory_reason": None,
                            "notes": "n = 4 vs 4 (>= 3 per arm, residual df 6): not exploratory by the contract rule"},
            evidence=[dego, paper], paper={"locator": "S2.4.p2; S4.6.p1"}, confidence="high",
            reasoning="Paper's DESeq2 route and stated threshold ran on the deposited counts for the paper's 12 h vs NC contrast.")
case.finish(n_deg=cnt["n_significant"], deg_sanity=cnt["deg_sanity"])
print(run.finish())
