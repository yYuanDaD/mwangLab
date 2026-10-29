import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE164798")
paper = case.evidence_item("paper:PMC8004053.paper.json")
summary = {}
for name in ["wt_acute_vs_wt_sed", "wt_acute_vs_wt_chronic"]:
    rdir = case.dir / "results" / name
    deg = [p for p in native.deg_outputs(rdir) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    ev = case.evidence_item(f"tool_output:{pathlib.Path(deg).name}")
    fid = native.feature_id_report(deg)["dominant_type"]
    # GSEA
    gdir = case.dir / "enrichment" / name / "gsea"; gdir.mkdir(parents=True, exist_ok=True)
    base = {"organism": "Mouse", "feature_id_type": fid, "subset": name}
    try:
        native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse", ranking_metric="stat", output_dir=str(gdir))
        outs = [str(p) for p in gdir.glob("*.csv")]
        for p in outs: case.add_output(p, f"gsea_{name}")
        g = pd.read_csv([p for p in outs if "GSEA" in p][0])
        cols = [c for c in g.columns if c.lower() in ("term", "nes", "fdr q-val")]
        summary[f"{name}:gsea"] = g.sort_values(cols[-1] if cols else g.columns[0]).head(6)[cols].values.tolist() if cols else g.shape
        case.decide("enrichment", final={**base, "method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
                    "ranking_metric": "stat", "outputs": outs, "paper_comparison": "paper used ORA (clusterProfiler GO/KEGG), not GSEA; supplementary only"},
                    evidence=[ev], reasoning="Full ranking by Wald stat.", confidence="high", execution_status="completed")
    except native.NativeToolError as e:
        summary[f"{name}:gsea"] = str(e)[:300]
        case.decide("enrichment", final={**base, "method": "GSEA preranked", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "execution_error": str(e)[:1500]},
                    evidence=[ev], reasoning="GSEA failed", confidence="high", execution_status="failed")
    # ORA up / down at applied threshold
    for direction in ("up", "down"):
        odir = case.dir / "enrichment" / name / f"ora_{direction}"; odir.mkdir(parents=True, exist_ok=True)
        orab = {**base, "method": f"ORA Enrichr ({direction}-regulated)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2019_Mouse",
                "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "direction": direction},
                "input_threshold_source": "applied",
                "deviation_note": "paper used clusterProfiler with the tested genes as universe and acute-specific gene subsets; Enrichr uses its own background and the full per-contrast DEG list"}
        try:
            native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Mouse", padj_cutoff=0.05,
                             log2fc_cutoff=0.0, direction=direction, output_dir=str(odir))
            outs = [str(p) for p in odir.glob("*.csv")]
            for p in outs: case.add_output(p, f"ora_{name}_{direction}")
            bp = [p for p in outs if "Biological_Process" in p]
            if bp:
                t = pd.read_csv(bp[0]); summary[f"{name}:ora_{direction}:GO_BP"] = t.head(5)[["Term", "Adjusted P-value"]].values.tolist() if "Term" in t else t.shape
            case.decide("enrichment", final={**orab, "outputs": outs}, evidence=[ev], reasoning="ORA on applied-threshold DEGs split by direction, as in S3.3.2.",
                        confidence="medium", execution_status="completed", paper={"locator": "S2.5.p3; S3.3.2.p2"})
        except native.NativeToolError as e:
            summary[f"{name}:ora_{direction}"] = str(e)[:300]
            case.decide("enrichment", final={**orab, "execution_error": str(e)[:1500]}, evidence=[ev], reasoning="ORA failed",
                        confidence="medium", execution_status="failed", paper={"locator": "S2.5.p3"})
case.write_json("enrichment_summary.json", summary)
for k, v in summary.items(): print(k, str(v)[:400])
