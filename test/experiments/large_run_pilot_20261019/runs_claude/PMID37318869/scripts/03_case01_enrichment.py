"""case_01: Hallmark GSEA (full ranking) + GO/KEGG ORA (audit BH list), then study record."""
import json
from common import *  # noqa
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN_DIR)
case = run.case("case_01")
deg = str(case.dir / "results" / "deseq2_paired" / "DEG_results_post_vs_pre.csv")
deg_item = case.evidence_item("tool_output:DEG_results_post_vs_pre.csv")
ids = native.feature_id_report(deg)
print(json.dumps(ids)[:400])

gdir = case.dir / "results" / "gsea"
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Human",
                           ranking_metric="stat", top_n=15, output_dir=str(gdir))
    print(msg)
    outs = native.find_outputs(gdir, "*GSEA*.csv")
    items = [case.add_output(p, "gsea_table") for p in outs]
    case.decide("enrichment",
                final={"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
                       "organism": "Human", "feature_id_type": ids.get("id_type", "ensembl_gene"),
                       "ranking": "DESeq2 Wald stat, post vs pre (subject-blocked)", "outputs": outs,
                       "note": "Paper reports no pathway analysis; this is an added descriptive layer."},
                evidence=[deg_item] + items, confidence="medium", execution_status="completed",
                reasoning="Full ranking of the completed case_01 contrast; separate from the DE result.")
except native.NativeToolError as e:
    print("GSEA FAILED", e)
    case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark",
                                     "organism": "Human", "feature_id_type": ids.get("id_type", "ensembl_gene"),
                                     "execution_error": str(e)},
                evidence=[deg_item], confidence="medium", execution_status="failed", reasoning="GSEA failed")

odir = case.dir / "results" / "ora_audit"
try:
    msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Human",
                           padj_cutoff=0.05, log2fc_cutoff=0.0, direction="all", top_n=10, output_dir=str(odir))
    print(msg)
    outs = native.find_outputs(odir, "*.csv")
    items = [case.add_output(p, "ora_table") for p in outs]
    case.decide("enrichment",
                final={"method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "GO 2023, KEGG 2021 Human",
                       "organism": "Human", "feature_id_type": ids.get("id_type", "ensembl_gene"),
                       "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None},
                       "input_threshold_source": "audit", "outputs": outs,
                       "note": ("ORA tool filters on padj only, so the applied raw-P rule cannot be passed; the "
                                "audit BH list (166 genes) is used and labelled audit.")},
                evidence=[deg_item] + items, confidence="medium", execution_status="completed",
                reasoning="Audit-labelled ORA on BH padj<0.05 genes of the completed contrast.")
except native.NativeToolError as e:
    print("ORA FAILED", e)
    case.decide("enrichment", final={"method": "ORA (Enrichr)", "gene_sets": "GO/KEGG", "organism": "Human",
                                     "feature_id_type": ids.get("id_type", "ensembl_gene"),
                                     "input_threshold": {"metric": "padj", "cutoff": 0.05},
                                     "input_threshold_source": "audit", "execution_error": str(e)},
                evidence=[deg_item], confidence="medium", execution_status="failed", reasoning="ORA failed")

case.decide("study", final={"route": "declared_deviation",
                            "summary": "Direct subject-blocked post-vs-pre DESeq2 test; paper only derives the "
                                       "exercise effect as Δlog2FC vs controls (case_02)."},
            evidence=[deg_item], confidence="medium",
            reasoning="Paper route (edgeR QL vs controls, no direct pre/post test) is reproduced in case_02.")
cnt = json.loads((case.dir / "threshold_counts.json").read_text())["applied"]
print(case.finish(n_deg=cnt["n_significant"], deg_sanity=cnt["deg_sanity"]))
