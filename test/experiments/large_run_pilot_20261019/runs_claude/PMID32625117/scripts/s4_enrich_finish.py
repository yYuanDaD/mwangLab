import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()

RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID32625117"
run = native.RunRecorder.open(RUN)
case = run.case("PMID32625117")
st = json.loads((case.dir / "stage3_state.json").read_text(encoding="utf-8"))
deg = st["deg"]; main = st["main"]
deg_ev = case.evidence_item("tool_output:DEG_results_post_vs_pre.csv")
paper = case.evidence_item("paper:PMC7311784.paper.md")
fid = native.feature_id_report(deg)
print("fid", json.dumps(fid, default=str)[:500])
ftype = fid["dominant_type"]
res = case.dir / "results"

# GSEA (full ranking)
g = {"method": "GSEA preranked (gseapy.prerank), ranking = limma moderated t", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
     "organism": "Human", "feature_id_type": ftype}
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Human", ranking_metric="stat",
                           output_dir=str(res / "gsea"))
    print(msg[:1500])
    outs = native.find_outputs(res / "gsea", "*GSEA*.csv")
    g["outputs"] = [case.add_output(o, "gsea_table")["path"] for o in outs]
    case.decide("enrichment", final=g, evidence=[deg_ev], confidence="medium", execution_status="completed",
                reasoning="Exploratory pathway view; paper annotated gene functions descriptively (S3.1.p1), no formal GSEA.")
except native.NativeToolError as e:
    print("GSEA FAILED", e); g["execution_error"] = str(e)
    case.decide("enrichment", final=g, evidence=[deg_ev], confidence="medium", execution_status="failed", reasoning="GSEA failed")

# ORA on applied threshold (padj<0.05, no effect cutoff)
o = {"method": "ORA (Enrichr) GO BP/MF/CC + KEGG", "gene_sets": "GO_2023 + KEGG_2021_Human", "organism": "Human", "feature_id_type": ftype,
     "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}, "input_threshold_source": "applied"}
try:
    msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Human", padj_cutoff=0.05,
                           log2fc_cutoff=0.0, output_dir=str(res / "ora"))
    print(msg[:1500])
    outs = native.find_outputs(res / "ora", "*.csv")
    o["outputs"] = [case.add_output(p, "ora_table")["path"] for p in outs]
    case.decide("enrichment", final=o, evidence=[deg_ev], confidence="medium", execution_status="completed",
                reasoning="ORA on the applied DEG list (padj<0.05, no FC cutoff).")
except native.NativeToolError as e:
    print("ORA FAILED", e); o["execution_error"] = str(e)
    case.decide("enrichment", final=o, evidence=[deg_ev], confidence="medium", execution_status="failed", reasoning="ORA failed")

case.decide("study", final={"route": "declared_deviation", "exploratory_reason": "n=5 subjects per arm, residual df = 4 (paired)",
                            "deviation": "limma on log2(CPM+1) with subject block instead of paired limma-voom (executor limits; fractional counts)",
                            "paper_vs_ours": {"paper_FDR05": {"up": 304, "down": 402}, "ours_FDR05": {"up": main["n_up"], "down": main["n_down"]},
                                              "paper_FDR05_FC2": {"up": 42, "down": "29/31"}, "ours_FDR05_FC2": {"up": st["audit"]["n_up"], "down": st["audit"]["n_down"]}}},
            evidence=[deg_ev, paper], confidence="medium", paper={"locator": "S3.1.p1"},
            reasoning="Paired post-vs-pre RT contrast executed on the closest available route; residual df 4 makes it exploratory by contract rule.")
case.finish(n_deg=main["n_significant"], deg_sanity=main["deg_sanity"])
run.finish()
print("done")
