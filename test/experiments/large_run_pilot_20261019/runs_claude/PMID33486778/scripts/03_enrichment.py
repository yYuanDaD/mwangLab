"""Optional enrichment gate: preranked GSEA (Hallmark, rat via mouse symbols) on limma moderated t."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33486778"
run = native.RunRecorder.open(RUN)
case = run.case("PMID33486778")
res = case.dir / "results" / "limma_rin"
gdir = case.dir / "results" / "gsea"

fid = native.feature_id_report(res / "DEG_results_FOinLRT.csv")
print(json.dumps(fid, indent=1, default=str))
outputs, summaries, errors = [], {}, {}
for name in ("FOinLRT", "FOinHRT", "DELTA"):
    deg = res / f"DEG_results_{name}.csv"
    od = gdir / name
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Rat",
                               ranking_metric="stat", top_n=10, output_dir=str(od))
        print(msg)
        files = native.find_outputs(od, "*GSEA_Hallmark*.csv")
        for f in files:
            it = case.add_output(f, f"gsea_{name}")
            outputs.append({"contrast": name, "path": f, "sha256": it.get("sha256")})
            tb = pd.read_csv(f)
            fdr_col = next(c for c in tb.columns if c.lower() in ("fdr q-val", "fdr", "fdr_q-val"))
            nes_col = next(c for c in tb.columns if c.upper() == "NES")
            term_col = next(c for c in tb.columns if c.lower() in ("term", "name"))
            sig = tb[pd.to_numeric(tb[fdr_col], errors="coerce") < 0.05]
            summaries[name] = {"n_sets": int(len(tb)), "n_fdr_lt_0.05": int(len(sig)),
                               "up": sig[pd.to_numeric(sig[nes_col]) > 0][term_col].tolist(),
                               "down": sig[pd.to_numeric(sig[nes_col]) < 0][term_col].tolist(),
                               "overlap_note": [l for l in msg.splitlines() if "matched to mouse" in l]}
    except native.NativeToolError as e:
        errors[name] = str(e)
        print("FAILED", name, e)
case.write_json("results/gsea/gsea_summary.json", {"summaries": summaries, "errors": errors, "feature_ids": fid},
                role="gsea_summary")
print(json.dumps(summaries, indent=1))
final = {"method": "GSEA preranked (gseapy.prerank via run_gsea_analysis)", "ranking_metric": "stat (limma moderated t)",
         "gene_sets": "MSigDB Hallmark mh.all v2024.1.Mm (mouse)", "organism": "Rat",
         "feature_id_type": "ensembl_gene",
         "id_mapping": "rat Ensembl gene -> symbol via MyGene.info (species=rat) inside run_gsea_analysis",
         "ortholog_mapping": "rat symbols matched to mouse Hallmark symbols by identity (no ortholog table); overlap reported by the tool",
         "contrasts": ["FOinLRT", "FOinHRT", "DELTA"],
         "paper_enrichment": "GO biological process GSEA (clusterProfiler, 10,000 permutations, size 25-500) - different library; declared deviation",
         "summaries": summaries}
if outputs and not errors:
    final["outputs"] = outputs
    status = "completed"
else:
    final["outputs"] = outputs
    final["execution_error"] = json.dumps(errors)
    status = "failed" if not outputs else "completed"
case.decide("enrichment", final=final,
            evidence=[case.add_output(case.dir / "results" / "gsea" / "gsea_summary.json", "gsea_summary_json")],
            paper={"locator": "S2.5.p3"}, confidence="medium",
            reasoning=("Paper reports GSEA ranked by limma moderated t (S2.5.p3, S3.6.p1). Repository has Hallmark only; "
                       "same ranking statistic used. Not comparable term-by-term with the paper's GO BP results."),
            execution_status=status, decision_status="valid")
