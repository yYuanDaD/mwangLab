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
meta = case.add_input("data/GSE270400/GSE270400_metadata.csv", "metadata")
A = case.dir / "aligned"
amat = case.add_output(A / "aligned_matrix.csv", "aligned_matrix")
dmeta_path = A / "design_metadata.csv"
dmeta = case.add_output(dmeta_path, "design_metadata")
dm = pd.read_csv(dmeta_path, index_col=0)

# ---------------- 5. design
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"],
                                      matrix_csv=str(A / "aligned_matrix.csv"), organism="Rat",
                                      subject=None, references={"grp": "NC"}, planned=["grp_h12_vs_NC"])
assert summary["verdict"] == "analyzable", summary
case.decide("design",
            final={"analysis_type": "two_group", "design_column": "grp", "control": "NC", "treatment": "h12",
                   "contrasts": [{"name": "grp_h12_vs_NC", "control": "NC", "treatment": "h12",
                                  "description": "12 h after a single 1-h treadmill run vs naive cage control"}],
                   "formula": "~ grp", "estimand_type": "interventional (randomized between-animal)",
                   "n_per_group": {"NC": 4, "h12": 4}, "suitability": summary},
            evidence=[dmeta, item, paper], paper={"locator": "S2.4.p2; S4.1.1.p1; S4.6.p1"},
            candidates=[{"value": "0h p.r. vs NC", "reason_rejected": "0 h samples are in GSE269529, not in GSE270400"}],
            reasoning=("GSE270400 holds exactly the paper's 12 h p.r. vs NC comparison (fig. S16, S2.4.p2): 4 vs 4 independent rats, "
                       "randomized (S4.1.1.p1). One two-level factor; suitability analyzable, one male sex only."),
            confidence="high")

# ---------------- 6. covariance
conf = native.confounding_report(dm, "grp", [c for c in dm.columns if c not in ("grp", "grp_raw", "characteristics_ch1.2.treatment",
                                                                              "title", "geo_accession", "relation", "matrix_label", "rep")])
dc = native.design_check(dm, ["grp"])
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc}, role="covariance_reports")
print(json.dumps(dc, indent=1, default=str))
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [], "covariates": [
                       {"name": "subject/animal", "disposition": "excluded: one sample per animal, between-animal design"},
                       {"name": "batch/lane", "disposition": "excluded: no batch field in GEO; all technical metadata constant"},
                       {"name": "sex", "disposition": "excluded: single level (male; S4.1.p1, sex check)"}],
                   "design_check": {k: dc.get(k) for k in ("rank", "n_columns", "residual_df", "full_rank") if k in dc}},
            evidence=[dmeta, case.add_output(case.dir / "covariance_reports.json", "covariance_reports")],
            paper={"locator": "S4.1.1.p1; S4.6.p1"},
            reasoning="Independent animals, one tendon each; no pairing or batch reported; metadata covariates are constant. Design ~ grp full rank, residual df 6.",
            confidence="high")

# ---------------- 7. method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 0.5.4; Wald test, BH)", "matrix_type": "raw counts", "formula": "~ grp",
                   "paper_method": "DESeq2 v1.30.1 (R)",
                   "implementation_note": "Python port of DESeq2, not R DESeq2 1.30.1; small numeric differences expected"},
            evidence=[amat, paper], paper={"locator": "S4.6.p1"},
            reasoning="Paper used DESeq2 on featureCounts counts; deposited matrix is those raw counts, so the paper route runs directly.",
            confidence="high")

# ---------------- 8. threshold
pt = {"metric": "padj", "adjustment": "BH (FDR)", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
      "effect_cutoff_original": "fold change >= 2", "inclusive": True, "source_locator": "S4.6.p1"}
case.decide("threshold",
            final={"paper_threshold": pt, "threshold_source": "paper", "applied_threshold": dict(pt),
                   "inclusive_note": "paper: 'fold change >= 2' and 'adjusted P value < 0.05'; applied as |log2FC| >= 1 and padj <= 0.05 (inclusive); the boundary padj == 0.05 does not occur in practice"},
            evidence=[paper], paper={"locator": "S4.6.p1; S2.4.p1"},
            reasoning="Paper states FC >= 2 and FDR-adjusted P < 0.05; log2(2) = 1 exactly.",
            confidence="high")

# ---------------- 9. execution
out = case.dir / "results"
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(A / "aligned_matrix.csv"),
                           metadata_csv=str(dmeta_path), design_column="grp", control_group="NC",
                           treatment_group="h12", output_dir=str(out))
    print(msg)
    deg = native.deg_outputs(out)[0]
    t = pd.read_csv(deg, index_col=0)
    # strict paper rule: padj < 0.05 and |log2FC| >= 1
    p = t["padj"]; l = t["log2FoldChange"]
    sig = (p < 0.05) & (l.abs() >= 1)
    cnt = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=1.0, inclusive=True, min_group_n=4)
    cnt["strict_padj_lt_0.05_and_abs_lfc_ge_1"] = int(sig.sum())
    # protein-coding scope (paper counts protein-coding genes) using the authors' annotation
    ann = pd.read_csv("data/GSE270400/GSE270400_Expression.All.fpkm.anno.txt.gz", sep="\t", index_col=0)
    biot = None
    for c in ann.columns:
        if "biotype" in c.lower():
            biot = ann[c]
    if biot is None:
        auth = pd.read_csv("data/GSE270400/GSE270400_DifGene.12hVSNC.All.fpkm.anno.txt.gz", sep="\t", index_col=0)
        biot = auth["gene_biotype"]
    pc = t.index.isin(biot[biot == "protein_coding"].index)
    cnt["protein_coding_scope"] = {"n_significant": int((sig & pc).sum()), "n_up": int((sig & pc & (l > 0)).sum()),
                                   "n_down": int((sig & pc & (l < 0)).sum()), "biotype_source": "authors' FPKM annotation file"}
    # authors' own DESeq2 table, same rule (reference only)
    auth = pd.read_csv("data/GSE270400/GSE270400_DifGene.12hVSNC.All.fpkm.anno.txt.gz", sep="\t", index_col=0)
    asig = (auth["padj"] < 0.05) & (auth["log2FoldChange"].abs() >= 1)
    apc = auth["gene_biotype"] == "protein_coding"
    cnt["authors_deposited_table_same_rule"] = {"all": int(asig.sum()), "protein_coding": int((asig & apc).sum()),
                                                "protein_coding_up": int((asig & apc & (auth["log2FoldChange"] > 0)).sum()),
                                                "protein_coding_down": int((asig & apc & (auth["log2FoldChange"] < 0)).sum())}
    common = t.index.intersection(auth.index)
    cnt["concordance_with_authors_table"] = {
        "n_common": int(len(common)),
        "log2fc_pearson_r": float(t.loc[common, "log2FoldChange"].corr(auth.loc[common, "log2FoldChange"])),
        "deg_overlap": int((sig.reindex(common, fill_value=False) & asig.reindex(common, fill_value=False)).sum())}
    print(json.dumps(cnt, indent=1))
    case.write_json("threshold_counts.json", cnt, role="threshold_counts")
    dego = case.add_output(deg, "deg_table")
    case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "outputs": [deg], "counts": cnt},
                evidence=[dego, amat, dmeta], reasoning="DESeq2 ~ grp, h12 vs NC; counts under the paper threshold via apply_threshold.",
                confidence="high", execution_status="completed")
    executed = True
except native.NativeToolError as e:
    cnt = None
    case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "execution_error": str(e)}, evidence=[amat, dmeta],
                reasoning="executor failed", confidence="high", execution_status="failed")
    executed = False
json.dump({"executed": executed, "counts": cnt}, open(case.dir / "_exec_state.json", "w"), indent=1, default=str)
