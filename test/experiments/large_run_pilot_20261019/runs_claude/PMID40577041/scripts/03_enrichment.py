"""Optional enrichment gate (SM and LV, where the paper reports GSEA): preranked Hallmark GSEA on limma moderated t."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40577041"
run = native.RunRecorder.open(RUN)
PAPER_TERMS = {"PMID40577041_SM": "Reactome up in ExT: Citric acid cycle, Fatty acid metabolism, Aerobic respiration (S3.3.p2, FIG2D)",
               "PMID40577041_LV": "Reactome: Citric acid cycle TCA cycle, Pyruvate metabolism, Mitochondrial translation, Aerobic respiration and respiratory electron transport (S3.3.p1, FIG2B)"}
for cid in PAPER_TERMS:
    case = run.case(cid)
    cdir = case.dir
    t = cid.split("_")[-1]
    exe = [d for d in json.loads((cdir / "decisions.json").read_text(encoding="utf-8")) if d["stage"] == "execution"][-1]
    deg = exe["final"]["outputs"][0]["path"]
    fid = native.feature_id_report(deg)
    od = cdir / "results" / "gsea"
    final = {"method": "GSEA preranked (gseapy.prerank via run_gsea_analysis)", "ranking_metric": "stat (limma moderated t)",
             "gene_sets": "MSigDB Hallmark mh.all v2024.1.Mm (mouse)", "organism": "Rat", "feature_id_type": "ensembl_gene",
             "id_mapping": "rat Ensembl gene -> symbol via MyGene.info (species=rat) inside run_gsea_analysis",
             "ortholog_mapping": "rat symbols matched to mouse Hallmark symbols by identity (no ortholog table)",
             "paper_enrichment": "clusterProfiler GSEA on Reactome (msigdbr 7.5.1), minGSSize 10, p<0.05 - different library; declared deviation",
             "paper_terms": PAPER_TERMS[cid], "feature_id_report": fid}
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Rat",
                               ranking_metric="stat", top_n=10, output_dir=str(od))
        print(msg)
        files = native.find_outputs(od, "*GSEA_Hallmark*.csv")
        outs = []
        for f in files:
            it = case.add_output(f, f"gsea_{t}")
            outs.append({"path": str(f), "sha256": it.get("sha256")})
        tb = pd.read_csv(files[0])
        q = pd.to_numeric(tb["FDR q-val"], errors="coerce")
        sig = tb[q < 0.05].sort_values("NES", ascending=False)
        final.update({"outputs": outs, "n_sets": int(len(tb)), "n_fdr_lt_0.05": int(len(sig)),
                      "up_in_ExT": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES > 0],
                      "down_in_ExT": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES < 0]})
        status = "completed"
    except native.NativeToolError as e:
        final["execution_error"] = str(e)[:800]
        status = "failed"
    gs = case.write_json("results/gsea/gsea_summary.json", final, role="gsea_summary")
    print(cid, status, json.dumps({k: final.get(k) for k in ("n_fdr_lt_0.05", "up_in_ExT", "down_in_ExT", "execution_error")}, indent=1))
    case.decide("enrichment", final=final, evidence=[gs], paper={"locator": "S2.10.p1"}, confidence="medium",
                reasoning="Paper runs GSEA on the full ranked list (S2.10.p1). Repository offers Hallmark only; not term-comparable with Reactome.",
                execution_status=status, decision_status="valid")
