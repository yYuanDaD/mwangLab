import sys, pathlib, json, math; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))  # repository root
from tools import native
native.enable_native_mode()
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41314005"
run = native.RunRecorder.open(REL)
case = run.case("GSE308674")
plan = json.loads((case.dir / "reproduction_plan.json").read_text(encoding="utf-8"))
PT = plan["threshold"]
counts_csv, meta_csv = plan["counts_csv"], plan["metadata_csv"]
am = case.evidence_item("tool_output:aligned_matrix.csv"); dm = case.evidence_item("tool_output:design_metadata.csv")
results = {}
for c in plan["contrasts"]:
    name = c["name"]; out = case.dir / "results" / name
    cov = plan["covariates"].get(name, "")
    formula = "~ batch + grp" if cov else "~ grp"
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=counts_csv, metadata_csv=meta_csv,
                               design_column="grp", control_group="C", treatment_group=c["treatment"],
                               output_dir=str(out), covariate_columns=cov)
        deg = native.deg_outputs(out)[0]
        th = native.apply_threshold(deg, metric="padj", cutoff=PT["cutoff"], effect_cutoff=PT["effect_cutoff"])
        item = case.add_output(deg, f"deg_table_{name}")
        (out / "tool_message.txt").write_text(str(msg), encoding="utf-8")
        results[name] = {"deg_csv": deg, "threshold": th, "paper": c["paper_n_deg"], "formula": formula}
        case.decide("execution", final={"method": "DESeq2 (pydeseq2 Wald)", "subset": name, "formula": formula,
                    "samples": f"C (n=4) + {c['treatment']} (n=6)", "outputs": [deg],
                    "n_tested": th["n_tested"], "n_deg": th["n_significant"], "n_up": th["n_up"], "n_down": th["n_down"],
                    "rule": th["rule"], "paper_n_deg": c["paper_n_deg"], "deg_sanity": th["deg_sanity"]},
                    evidence=[am, dm, item], paper={"locator": "S3.3.p1"}, confidence="high",
                    execution_status="completed",
                    reasoning=f"Ran {formula} on the C and {c['treatment']} samples; counted DEGs under the paper rule with apply_threshold.")
    except native.NativeToolError as error:
        results[name] = {"error": str(error)}
        case.decide("execution", final={"method": "DESeq2 (pydeseq2 Wald)", "subset": name, "formula": formula,
                    "execution_error": str(error)}, evidence=[am, dm], paper={"locator": "S3.3.p1"},
                    confidence="high", execution_status="failed", reasoning="executor failed")
(case.dir / "execution_results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
for k, v in results.items():
    print(k, v.get("threshold", v.get("error")), v.get("paper"))
