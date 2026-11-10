"""Execution, enrichment, study record and run finish for GSE282942 / PMID41933175."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import numpy as np
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41933175"
CASE = "PMID41933175"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
cdir = case.dir

# ---------------------------------------------------------------- 9 execution
mat = pd.read_csv(cdir / "aligned" / "aligned_matrix.csv", index_col=0)
keep = mat.sum(axis=1) >= 15
filt_path = cdir / "aligned" / "aligned_matrix_min15reads.csv"
mat.loc[keep].to_csv(filt_path)
filt_ev = case.add_output(filt_path, "filtered_matrix")
print(f"read filter: kept {int(keep.sum())} of {len(mat)} genes")

res_dir = cdir / "results" / "deseq2_irisin_vs_pbs"
method = "DESeq2 (pyDESeq2 Wald test, MLE log2FC)"
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis",
                           counts_csv=str(filt_path), metadata_csv=str(cdir / "aligned" / "design_metadata.csv"),
                           design_column="grp", control_group="pbs", treatment_group="irisin",
                           output_dir=str(res_dir))
    print(msg)
except native.NativeToolError as error:
    case.decide("execution", final={"method": method, "execution_error": str(error)},
                evidence=[filt_ev], decision_status="valid", execution_status="failed", confidence="high",
                reasoning="DESeq2 failed on the approved plan.")
    raise

deg = native.deg_outputs(res_dir)[0]
deg_ev = case.add_output(deg, "deg_table")
primary = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=1.0, inclusive=False, min_group_n=3)
audit_wt = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=1.0, inclusive=True, min_group_n=3)
audit_def = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None, min_group_n=3)
print("primary", primary); print("audit whole-tissue", audit_wt); print("audit default", audit_def)

tab = pd.read_csv(deg, index_col=0)
genes = ["Il33", "Il6", "Fgf23", "Ccl2", "Ccl7", "Cxcl5", "Fabp4", "Adipoq", "Cd36", "Pparg"]
gene_check = {g: ({"log2FC": round(float(tab.loc[g, "log2FoldChange"]), 3),
                   "fold": round(float(2 ** tab.loc[g, "log2FoldChange"]), 2),
                   "pvalue": float(tab.loc[g, "pvalue"]), "padj": float(tab.loc[g, "padj"])}
                  if g in tab.index else "not tested") for g in genes}
print(json.dumps(gene_check, indent=1))

case.decide("execution",
            final={"method": method, "formula": "~ grp", "contrast": "irisin vs pbs",
                   "n_genes_input": int(len(mat)), "n_genes_after_read_filter": int(keep.sum()),
                   "outputs": [deg], "primary_count": primary,
                   "audit_counts": {"whole_tissue_rule padj<=0.05 & |log2FC|>=1": audit_wt,
                                    "workflow_default padj<0.05": audit_def},
                   "paper_gene_check": gene_check},
            evidence=[filt_ev, deg_ev], decision_status="valid", execution_status="completed", confidence="high",
            reasoning="DESeq2 ran on the paper-filtered raw counts; counts via native.apply_threshold.")

# ---------------------------------------------------------------- 10 enrichment (GSEA Hallmark)
fid = native.feature_id_report(deg)
print("feature ids:", {k: fid[k] for k in fid if k in ("id_type", "usable_for_gene_sets", "note")})
gsea_dir = cdir / "results" / "gsea_hallmark"
gsea_final = {"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
              "organism": "Mouse", "feature_id_type": "gene_symbol", "ranking_metric": "stat (DESeq2 Wald)",
              "paper_comparison": ("paper: 147/195 adipogenesis-up signature genes attenuated (chi-squared); "
                                   "compare HALLMARK_ADIPOGENESIS direction")}
try:
    gmsg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Mouse",
                            ranking_metric="stat", output_dir=str(gsea_dir))
    print(gmsg[:1500])
    outs = native.find_outputs(gsea_dir, "*GSEA*.csv")
    g = pd.read_csv(outs[0])
    term_col = "Term"
    adip = g[g[term_col].astype(str).str.contains("ADIPOGENESIS", case=False)]
    adip_row = adip.iloc[0].to_dict() if len(adip) else "not in results"
    sig_cols = [c for c in g.columns if "fdr" in c.lower()]
    top = g.sort_values(sig_cols[0]).head(10)[[term_col, "NES", sig_cols[0]]].to_dict("records") if sig_cols else []
    # Leading-edge-free check of the paper's 75% figure: Hallmark adipogenesis genes with log2FC < 0.
    gmt = __import__("tools.enrichment_tools", fromlist=["_get_hallmark_gmt"])._get_hallmark_gmt("mh.all", "2024.1.Mm")
    members = [x for x in gmt.get("HALLMARK_ADIPOGENESIS", []) if x in tab.index]
    frac_down = float((tab.loc[members, "log2FoldChange"] < 0).mean()) if members else None
    gsea_final.update({"outputs": [str(p) for p in outs], "adipogenesis": adip_row,
                       "adipogenesis_members_tested": len(members), "adipogenesis_fraction_log2FC_below_0": frac_down,
                       "top10_by_fdr": top})
    for p in outs:
        case.add_output(p, "gsea_table")
    case.decide("enrichment", final=gsea_final, evidence=[deg_ev], decision_status="valid",
                execution_status="completed", confidence="medium",
                reasoning=("Paper reports attenuation of a GSEA-derived adipogenesis-up signature (S2.3.p5, S4.9.p4); "
                           "Hallmark GSEA on the full Wald ranking is the closest available gene-set test."))
    print("adipogenesis:", adip_row, "members", len(members), "frac down", frac_down)
except Exception as error:  # network or tool failure does not stop the case
    gsea_final["execution_error"] = f"{type(error).__name__}: {error}"
    case.decide("enrichment", final=gsea_final, evidence=[deg_ev], decision_status="valid",
                execution_status="failed", confidence="medium", reasoning="GSEA failed; DE result unaffected.")
    print("GSEA failed:", error)

# ---------------------------------------------------------------- 11 study
plan = {"paper_route": "DESeq2 normalisation + Multiplot Studio comparison (blocked: tool/test not available)",
        "run_route": "DESeq2 Wald ~ grp on raw counts, genes with >= 15 total reads",
        "threshold": "raw pvalue < 0.05 and |log2FC| > 1 (paper FIG3 g) on the deviation route"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summary = {"contrast": "irisin/HSP90a vs PBS, IL-33- eWAT mSCs (exercise-mimetic proxy, no exercise arm)",
           "primary": primary, "audits": {"whole_tissue_rule": audit_wt, "workflow_default": audit_def},
           "paper_n_deg": "not_reported in text", "paper_gene_check": gene_check,
           "enrichment": {k: gsea_final.get(k) for k in ("adipogenesis", "adipogenesis_fraction_log2FC_below_0",
                                                         "adipogenesis_members_tested", "execution_error") if k in gsea_final}}
case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
case.decide("study",
            final={"route": "declared_deviation",
                   "deviation": "DESeq2 Wald test replaces the unnamed Multiplot Studio comparison; CV>0.30 filter not applied",
                   "estimand_note": "irisin (exercise-induced myokine) treatment in vitro; not an exercise effect",
                   "n_deg": primary["n_significant"], "threshold_source": "paper_on_deviation_route"},
            evidence=[deg_ev], decision_status="valid", execution_status="completed", confidence="medium",
            reasoning="Paper's planned contrast executed on a declared deviation route; 3 vs 3, residual df 4 (not exploratory by rule).")
case.finish(n_deg=primary["n_significant"], deg_sanity=primary["deg_sanity"])
run.finish()
print("finished")
