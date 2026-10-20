"""Gate 10 enrichment: ORA (Enrichr GO/KEGG, paper threshold list) and GSEA Hallmark per contrast."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40069235"
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
thr = [r for r in case.records if r["stage"] == "threshold"][-1]["final"]["applied_threshold"]
degs = sorted(native.deg_outputs(case.dir / "results"))
fid = native.feature_id_report(degs[0])
print("feature ids:", fid)
report = {}
for deg in degs:
    name = pathlib.Path(deg).stem.replace("DEG_results_", "")
    ev = case.add_output(deg, f"deg_{name}_enrichment_input")
    for kind in ("ORA", "GSEA"):
        out = case.dir / "enrichment" / name / kind.lower()
        out.mkdir(parents=True, exist_ok=True)
        if kind == "ORA":
            spec = "tools.enrichment_tools:run_enrichment_analysis"
            kwargs = dict(deg_csv=deg, organism="Human", padj_cutoff=thr["cutoff"],
                          log2fc_cutoff=thr["effect_cutoff"], direction="all", output_dir=str(out))
            final = {"method": "ORA (Enrichr, gseapy)", "gene_sets": "GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2021_Human",
                     "input_threshold": dict(thr), "input_threshold_source": "applied"}
        else:
            spec = "tools.enrichment_tools:run_gsea_analysis"
            kwargs = dict(deg_csv=deg, organism="Human", ranking_metric="stat", output_dir=str(out))
            final = {"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark h.all @ 2024.1.Hs",
                     "ranking_metric": "stat (limma moderated t)"}
        final.update({"organism": "Human", "feature_id_type": "ensembl_gene", "subset": name,
                      "id_mapping": "Ensembl gene -> symbol via MyGene.info inside the tool"})
        try:
            msg = native.call_tool(spec, **kwargs)
            files = sorted(str(p) for p in out.rglob("*.csv"))
            evs = [case.add_output(f, f"{kind.lower()}_{name}") for f in files]
            final["outputs"] = files
            case.decide("enrichment", final=final, evidence=[ev] + evs, confidence="medium",
                        execution_status="completed", paper={"locator": "S5.6.p3"},
                        reasoning=f"{kind} on {name}; paper used ORA (WebGestaltR/clusterProfiler GO) on DEG lists; "
                                  "Enrichr libraries differ from the paper's. Pathway result kept separate from DE.")
            report[f"{name}:{kind}"] = {"status": "completed", "files": files, "message": str(msg)[:1500]}
        except native.NativeToolError as error:
            final["execution_error"] = str(error)[:2000]
            case.decide("enrichment", final=final, evidence=[ev], confidence="medium",
                        execution_status="failed", paper={"locator": "S5.6.p3"}, reasoning=f"{kind} failed on {name}")
            report[f"{name}:{kind}"] = {"status": "failed", "error": str(error)[:2000]}
case.write_json("enrichment/enrichment_report.json", report, role="enrichment_report")
print(json.dumps(report, indent=1)[:12000])
