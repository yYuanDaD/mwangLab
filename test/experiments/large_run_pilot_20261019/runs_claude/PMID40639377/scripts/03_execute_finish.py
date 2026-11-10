import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import numpy as np, pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40639377"
run = native.RunRecorder.open(RUN); case = run.case("GSE294230")
A = case.dir / "aligned"; R = case.dir / "results"
paper = case.evidence_item("paper:PMC12258965.paper.md")
design_meta = str(A / "design_metadata.csv")

# rounding (value change -> done at execution, recorded in method.rounding_documented)
x = pd.read_csv(A / "aligned_matrix.csv", index_col=0)
xr = np.round(x).astype(int)
xr.to_csv(A / "aligned_counts_rounded.csv")
rounded = case.add_output(A / "aligned_counts_rounded.csv", "aligned_counts_rounded")
genes = pd.read_csv(A / "gene_annotation.csv", index_col=0)

def run_deseq(out, cov=""):
    native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(A / "aligned_counts_rounded.csv"),
                     metadata_csv=design_meta, design_column="grp", control_group="pbs", treatment_group="formate",
                     output_dir=str(out), covariate_columns=cov)
    deg = native.deg_outputs(out)[0]
    t = pd.read_csv(deg, index_col=0)
    t.insert(0, "gene_name", genes.reindex(t.index)["gene_name"])
    annotated = pathlib.Path(out) / "DEG_formate_vs_pbs_annotated.csv"
    t.to_csv(annotated)
    return deg, annotated, t

summary = {}
named = ["Shmt2", "Cth", "mt-Nd4", "Tkt", "Ripk2", "Slc39a8", "Furin", "Parp1", "Ezr", "Irf8"]
# ---------- primary execution
try:
    deg, annotated, t = run_deseq(R / "primary")
    paper_rule = native.apply_threshold(deg, metric="padj", cutoff=0.2)
    audit = native.apply_threshold(deg, metric="padj", cutoff=0.05)
    chk = t[t["gene_name"].isin(named)][["gene_name", "baseMean", "log2FoldChange", "pvalue", "padj"]]
    chk.to_csv(R / "primary" / "paper_named_genes.csv")
    o1, o2 = case.add_output(deg, "deg_table"), case.add_output(annotated, "deg_table_annotated")
    summary["primary"] = {"paper_rule": paper_rule, "audit_padj_0.05": audit, "paper_named_genes": chk.round(5).to_dict(orient="index")}
    case.decide("execution", final={"method": "DESeq2 (pydeseq2) Wald, ~ grp, rounded tximport counts", "rounding_documented": "np.round of tximport estimated counts (aligned/aligned_counts_rounded.csv), as DESeqDataSetFromTximport does", "subset": "primary_unpaired",
                                    "outputs": [deg, str(annotated)], "n_deg_applied": paper_rule["n_significant"],
                                    "n_up": paper_rule["n_up"], "n_down": paper_rule["n_down"], "rule": paper_rule["rule"],
                                    "audit_padj_lt_0.05": audit["n_significant"], "deg_sanity": paper_rule["deg_sanity"]},
                evidence=[rounded, o1, o2], confidence="high", execution_status="completed",
                reasoning="Approved route ran; counts from native.apply_threshold under the paper's BH<0.2 rule.")
    primary_ok = True
except native.NativeToolError as e:
    primary_ok = False; paper_rule = None
    case.decide("execution", final={"method": "DESeq2 (pydeseq2) Wald, ~ grp", "subset": "primary_unpaired", "execution_error": str(e)},
                evidence=[rounded], confidence="high", execution_status="failed", reasoning="executor failed")

# ---------- exploratory pair-blocked sensitivity
try:
    deg2, annotated2, t2 = run_deseq(R / "sensitivity_blk", cov="blk")
    r2 = native.apply_threshold(deg2, metric="padj", cutoff=0.2)
    a2 = native.apply_threshold(deg2, metric="padj", cutoff=0.05)
    chk2 = t2[t2["gene_name"].isin(named)][["gene_name", "baseMean", "log2FoldChange", "pvalue", "padj"]]
    chk2.to_csv(R / "sensitivity_blk" / "paper_named_genes.csv")
    summary["sensitivity_blk"] = {"paper_rule": r2, "audit_padj_0.05": a2, "paper_named_genes": chk2.round(5).to_dict(orient="index"),
                                  "residual_df": 3, "exploratory_reason": "residual df 3 < 4; pairing inferred"}
    if primary_ok:
        j = t[["log2FoldChange"]].join(t2[["log2FoldChange"]], rsuffix="_blk").dropna()
        summary["sensitivity_blk"]["log2fc_pearson_vs_primary"] = float(j.corr().iloc[0, 1])
    case.decide("execution", final={"method": "DESeq2 (pydeseq2) Wald, ~ blk + grp (exploratory; blk inferred from library numbering)", "rounding_documented": "np.round of tximport estimated counts (aligned/aligned_counts_rounded.csv), as DESeqDataSetFromTximport does", 
                                    "subset": "exploratory_pair_blocked", "formula": "~ blk + grp",
                                    "outputs": [deg2, str(annotated2)], "n_deg_applied": r2["n_significant"], "rule": r2["rule"],
                                    "audit_padj_lt_0.05": a2["n_significant"]},
                evidence=[rounded, case.add_output(deg2, "deg_table_sensitivity")], confidence="medium", execution_status="completed",
                reasoning="Sensitivity analysis only: the pairing is inferred, not documented, so this is not the primary result.")
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 ~ blk + grp (exploratory)", "subset": "exploratory_pair_blocked", "execution_error": str(e)},
                evidence=[rounded], confidence="medium", execution_status="failed", reasoning="executor failed")

case.write_json("reproduction_plan.json", {
    "paper_route": "Kallisto + Sleuth, PBS vs 2 mM formate, q < 0.2 (S5.2.19.p1): blocked (no Sleuth executor, no bootstraps deposited)",
    "declared_deviation": "DESeq2 ~ grp on rounded tximport gene-level counts, BH padj < 0.2",
    "exploratory": "DESeq2 ~ blk + grp, blk = putative mouse pair from library numbering",
    "estimand_note": "formate is the paper's exercise-induced microbiota metabolite; no exercise samples were sequenced"})
case.write_json("reproduction_summary.json", {"results": summary,
    "paper_count": "not available (Table S3 not retrievable; text gives no count)",
    "validation": "alignment 8/8 exact; suitability analyzable; 4 vs 4"})

# ---------- enrichment: not requested by the user; paper used ChEA3 TFEA (web tool, no executor)
case.decide("enrichment", final={"method": "ChEA3 TFEA (paper) / Hallmark GSEA", "gene_sets": "ENCODE ChIP-seq TF targets (paper)", "organism": "Mouse",
                                 "feature_id_type": "ensembl_gene", "reason_not_run": "not requested; the paper's enrichment is the ChEA3 web tool (no executor here)"},
            evidence=[paper], paper={"locator": "S5.2.20.p1"}, confidence="high", execution_status="not_run",
            reasoning="Request asks for gene expression changes only.")

case.decide("study", final={"route": "declared_deviation",
                            "deviation": "Sleuth -> DESeq2 on rounded tximport counts; estimand is formate (exercise mediator) in vitro, not exercise itself",
                            "exploratory_items": ["pair-blocked sensitivity (blk inferred; residual df 3)"],
                            "exploratory_reason": "sensitivity fit ~ blk + grp has residual df 3 (< 4) and an inferred block; primary 4 vs 4 has residual df 6"},
            evidence=[paper], confidence="medium", execution_status="completed" if primary_ok else "failed",
            reasoning="Paper-defined contrast run via a declared alternative method under the paper's threshold.")
print(json.dumps(summary, indent=1, default=str))
case.finish(n_deg=paper_rule["n_significant"] if paper_rule else None, deg_sanity=paper_rule["deg_sanity"] if paper_rule else None)
run.finish()
