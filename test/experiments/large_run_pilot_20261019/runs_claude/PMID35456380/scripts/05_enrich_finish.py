import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35456380"
run = native.RunRecorder.open(RUN); case = run.case("GSE164890")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC9027771.paper.md", "paper")
ex = json.load(open(case.dir / "_exec.json"))
rdir = case.dir / "results" / "deseq2_time_post_vs_pre"
deg = native.deg_outputs(rdir)[0]
degi = case.add_output(deg, "deg_table")

# ---------- enrichment: preranked GSEA, MSigDB Hallmark, full ranking by Wald stat
fid = native.feature_id_report(deg)
print(json.dumps(fid, default=str)[:600])
edir = case.dir / "results" / "gsea_hallmark"; edir.mkdir(parents=True, exist_ok=True)
base = {"method": "preranked GSEA (gseapy.prerank), ranking by DESeq2 Wald stat", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
        "organism": "Human", "feature_id_type": "Ensembl gene", "id_mapping": "Ensembl -> symbol via MyGene.info inside run_gsea_analysis",
        "paper_enrichment": "ORA (clusterProfiler) on H and CP plus fGSEA (S2.5.p1); ORA and CP not repeated here"}
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Human",
                           ranking_metric="stat", output_dir=str(edir))
    print(str(msg)[:2500])
    outs = native.find_outputs(edir, "*GSEA*.csv")
    items = [case.add_output(o, "gsea_table") for o in outs]
    top = None
    if outs:
        g = pd.read_csv(outs[0])
        fdr_col = next((c for c in g.columns if "FDR" in c), None)
        cols = [c for c in ("Term", "NES", fdr_col) if c and c in g.columns]
        top = g.sort_values(fdr_col).head(12)[cols].to_dict("records") if fdr_col else None
    case.decide("enrichment", final=dict(base, outputs=[i["path"] for i in items], top_terms=top),
        evidence=[degi] + items, paper={"locator": "S3.3.p1"}, confidence="medium", execution_status="completed",
        reasoning="Paper reports pathway results (S3.3.p1); GSEA uses the full ranking, so no DEG threshold enters.")
except native.NativeToolError as e:
    print("GSEA FAILED", e)
    case.decide("enrichment", final=dict(base, execution_error=str(e)), evidence=[degi], paper={"locator": "S3.3.p1"},
        confidence="medium", execution_status="failed", reasoning="GSEA failed; DE result unaffected.")

# ---------- study
case.decide("study", final={"route": "paper_aligned",
    "note": "DESeq2 ~ subject + time on round(RSEM counts) at padj <= 0.1 as in the paper and the authors' script; pydeseq2 instead of R DESeq2 1.18.1",
    "n_deg": ex["n_deg"], "direction": ex["split"], "paper_counts": {"up": 2516, "down": 1542, "total": 4058}},
    evidence=[paper, degi], paper={"locator": "S3.2.p2"}, confidence="high",
    reasoning="All gates valid; the paper route ran unchanged (7 per arm, residual df 6, so no exploratory label).")
case.write_json("reproduction_plan.json", {"route": "paper_aligned", "method": "DESeq2 ~ subject + time", "input": "round(RSEM expected counts, 0)",
    "contrast": "post vs pre", "threshold": "padj <= 0.1, no effect cutoff", "enrichment": "GSEA Hallmark (paper: ORA H+CP and fGSEA)"})
case.write_json("reproduction_summary.json", {"status": "completed", "n_deg": ex["n_deg"], "ours": ex["split"],
    "paper": {"up": 2516, "down": 1542, "total": 4058, "twofold_up": 104, "twofold_down": 58, "locator": "S3.2.p2"},
    "note": "pydeseq2 vs R DESeq2 1.18.1 dispersion/independent-filtering differences expected"})
print(case.finish(n_deg=ex["n_deg"], deg_sanity=ex["sanity"]))
print(run.finish())
