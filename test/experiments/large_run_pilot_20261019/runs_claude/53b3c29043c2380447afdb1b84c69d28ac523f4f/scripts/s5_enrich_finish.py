import sys, os, json, pathlib, glob
ROOT = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
from tools import native
native.enable_native_mode()

RUN = str(pathlib.Path(__file__).resolve().parents[1].relative_to(ROOT))
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
paper = case.evidence_item("paper:PMC10614785.paper.md")
res = json.load(open(case.dir / "results" / "deg_counts.json", encoding="utf-8"))
qc = case.add_output(case.dir / "results" / "qc_diagnostics.json", "qc_diagnostics")

summary = {}
for name, r in res.items():
    deg = r["deg"]
    degev = case.add_output(deg, f"deg_input_{name}")
    fid = native.feature_id_report(deg)["dominant_type"]
    out = case.dir / "results" / name / "enrichment"
    # GSEA (full ranking)
    try:
        native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                         ranking_metric="stat", output_dir=str(out))
        files = sorted(glob.glob(str(out / "*GSEA*.csv")))
        outs = [case.add_output(f, f"gsea_{name}")["path"] for f in files]
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy)", "subset": name,
                    "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "organism": "Mouse", "feature_id_type": fid,
                    "ranking": "DESeq2 Wald stat", "outputs": outs}, evidence=[degev], confidence="medium",
                    execution_status="completed", paper={"locator": "FIG1"},
                    reasoning="Full-ranking pathway view of the exercise response; paper used ORA on Reactome/KEGG/GO.")
        summary[f"gsea_{name}"] = outs
    except native.NativeToolError as e:
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy)", "subset": name,
                    "gene_sets": "MSigDB Hallmark", "organism": "Mouse", "feature_id_type": fid,
                    "execution_error": str(e)}, evidence=[degev], confidence="medium", execution_status="failed",
                    reasoning="GSEA failed.")
        summary[f"gsea_{name}"] = "failed: " + str(e)[:300]
    # ORA on the applied-threshold DEG list (padj<0.05, no effect cutoff)
    try:
        native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Mouse",
                         padj_cutoff=0.05, log2fc_cutoff=0.0, direction="all", output_dir=str(out))
        files = sorted(set(glob.glob(str(out / "*.csv"))) - set(glob.glob(str(out / "*GSEA*.csv"))))
        outs = [case.add_output(f, f"ora_{name}_{pathlib.Path(f).stem[-20:]}")["path"] for f in files]
        case.decide("enrichment", final={"method": "ORA (Enrichr)", "subset": name,
                    "gene_sets": "GO BP/MF/CC 2023 + KEGG 2019 Mouse", "organism": "Mouse", "feature_id_type": fid,
                    "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None},
                    "input_threshold_source": "applied", "n_input_genes": r["n_significant"], "outputs": outs},
                    evidence=[degev], confidence="medium", execution_status="completed", paper={"locator": "FIG1"},
                    reasoning="Paper ran pathway ORA on exercise DEG lists (FIG1E-H).")
        summary[f"ora_{name}"] = outs
    except native.NativeToolError as e:
        case.decide("enrichment", final={"method": "ORA (Enrichr)", "subset": name,
                    "gene_sets": "GO BP/MF/CC 2023 + KEGG 2019 Mouse", "organism": "Mouse", "feature_id_type": fid,
                    "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None},
                    "input_threshold_source": "applied", "execution_error": str(e)},
                    evidence=[degev], confidence="medium", execution_status="failed", reasoning="ORA failed.")
        summary[f"ora_{name}"] = "failed: " + str(e)[:300]
print(json.dumps(summary, indent=1))

v, k = res["vehicle_ex_vs_ctrl"], res["ko_ex_vs_ctrl"]
case.decide("study", final={"route": "paper_aligned",
            "comparison_to_paper": {
                "vehicle_ex_vs_ctrl": {"ours": {"total": v["n_significant"], "up": v["n_up"], "down": v["n_down"]},
                                       "paper": {"total": 989, "up": 600, "down": 389}},
                "ko_ex_vs_ctrl": {"ours": {"total": k["n_significant"], "up": k["n_up"], "down": k["n_down"]},
                                  "paper": {"total": 517, "up": 250, "down": 267}}},
            "discrepancy_note": "Counts are far below the paper's. QC: labels are biologically consistent (Dbp ~2.5 log2 lower "
                                "in all KO samples; Nr4a3/Nr4a1/Per1 higher after exercise), but PC1 (42% of variance) is a "
                                "nuisance axis crossing all four groups, so within-group variance is high. Partek Flow's DESeq2 "
                                "settings (joint 20-sample fit, filtering) are not reported and may explain the gap. "
                                "Direction matches the paper: Vehicle response larger than KO; Fosb/Per1/Nfil3 up in Vehicle; "
                                "Nr4a3 and Ppargc1a respond nominally in Vehicle (p=0.005, 0.022) but not at FDR.",
            "evidence_qc": qc["path"]},
            evidence=[qc, paper], confidence="medium", paper={"locator": "S3.1.p1"},
            reasoning="Paper route (DESeq2 Wald, q<0.05, within genotype) reproduced on deposited raw counts; "
                      "counts differ from the paper.")
case.finish(n_deg=v["n_significant"] + k["n_significant"], deg_sanity="ok")
run.finish()
