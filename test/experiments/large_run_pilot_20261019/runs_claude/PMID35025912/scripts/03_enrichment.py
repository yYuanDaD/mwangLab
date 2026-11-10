"""Optional enrichment gate: preranked GSEA (Hallmark, rat via mouse symbols) on limma moderated t, planned contrasts."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35025912"
run = native.RunRecorder.open(RUN)
case = run.case("PMID35025912")
cdir = case.dir
dc = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
exe = json.loads((cdir / "decisions.json").read_text(encoding="utf-8"))
exe = [d for d in exe if d["stage"] == "execution"][-1]
paths = {o["contrast"]: o["path"] for o in exe["final"]["outputs"]}
names = ["PLN_HIinLRT", "PLN_HIinHRT", "PLN_DELTA", "SOL_HIinLRT", "SOL_HIinHRT", "SOL_DELTA"]
gdir = cdir / "results" / "gsea"
fid = native.feature_id_report(paths["PLN_HIinLRT"])
print(json.dumps(fid, indent=1, default=str))
outputs, summaries, errors = [], {}, {}
for name in names:
    od = gdir / name
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(paths[name]), organism="Rat",
                               ranking_metric="stat", top_n=10, output_dir=str(od))
        print(msg)
        for f in native.find_outputs(od, "*GSEA_Hallmark*.csv"):
            it = case.add_output(f, f"gsea_{name}")
            outputs.append({"contrast": name, "path": f, "sha256": it.get("sha256")})
            tb = pd.read_csv(f)
            sig = tb[pd.to_numeric(tb["FDR q-val"], errors="coerce") < 0.05].sort_values("NES", ascending=False)
            summaries[name] = {"n_sets": int(len(tb)), "n_fdr_lt_0.05": int(len(sig)),
                               "up": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES > 0],
                               "down": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES < 0],
                               "tool_notes": [l for l in msg.splitlines() if "mouse" in l.lower() or "mapped" in l.lower()][:4]}
    except native.NativeToolError as e:
        errors[name] = str(e)
        print("FAILED", name, e)
gs = case.write_json("results/gsea/gsea_summary.json", {"summaries": summaries, "errors": errors, "feature_ids": fid},
                     role="gsea_summary")
print(json.dumps(summaries, indent=1))
final = {"method": "GSEA preranked (gseapy.prerank via run_gsea_analysis)", "ranking_metric": "stat (limma moderated t)",
         "gene_sets": "MSigDB Hallmark mh.all v2024.1.Mm (mouse)", "organism": "Rat",
         "feature_id_type": "ensembl_gene",
         "id_mapping": "rat Ensembl gene -> symbol via MyGene.info (species=rat) inside run_gsea_analysis",
         "ortholog_mapping": "rat symbols matched to mouse Hallmark symbols by identity (no ortholog table)",
         "contrasts": names,
         "paper_enrichment": "GO BP GSEA (clusterProfiler, 10,000 permutations, size 25-500, FDR<0.05 & P<0.001) - different library; declared deviation",
         "summaries": summaries, "outputs": outputs}
status = "completed" if outputs else "failed"
if errors:
    final["execution_error"] = json.dumps(errors)
case.decide("enrichment", final=final, evidence=[gs], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning=("Paper ranks genes by t and runs GSEA (S2.2.p2, S3.6.p1). Repository offers Hallmark only; same "
                       "ranking statistic. Not term-comparable with the paper's GO BP maps."),
            execution_status=status, decision_status="valid")
