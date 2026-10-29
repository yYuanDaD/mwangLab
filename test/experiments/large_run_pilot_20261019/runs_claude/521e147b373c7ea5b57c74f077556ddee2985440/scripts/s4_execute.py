import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE164798")
recon = json.load(open(case.dir / "paper_reconstruction.json", encoding="utf-8"))
aligned = case.dir / "aligned" / "aligned_matrix.csv"
DM = case.dir / "aligned" / "design_metadata.csv"
x = pd.read_csv(aligned, index_col=0)
drop = ["Psen1", "App", "Thy1"]
present = [g for g in drop if g in x.index]
x = x.drop(index=present)
counts = case.dir / "aligned" / "counts_no_transgene_markers.csv"
x.to_csv(counts)
print("counts after marker removal:", x.shape, "removed", present)
cin = case.add_output(counts, "counts_for_deseq2")
results = {}
for c in recon["planned_contrasts"]:
    out = case.dir / "results" / c["name"]
    out.mkdir(parents=True, exist_ok=True)
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(counts), metadata_csv=str(DM),
                         design_column="grp", control_group=c["control"], treatment_group=c["treatment"], output_dir=str(out))
    except native.NativeToolError as error:
        case.decide("execution", final={"method": "DESeq2", "subset": c["name"], "execution_error": str(error)[:2000]},
                    evidence=[cin], reasoning="DESeq2 call failed", confidence="high", execution_status="failed")
        results[c["name"]] = {"error": str(error)[:300]}
        continue
    deg = [p for p in native.deg_outputs(out) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    cnt = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None, min_group_n=4)
    t = pd.read_csv(deg, index_col=0)
    sig = t[t["padj"] < 0.05].sort_values("padj")
    cnt["top"] = sig.head(5)[["log2FoldChange", "padj"]].round(4).reset_index().values.tolist()
    if "Chgb" in t.index:
        cnt["Chgb"] = t.loc["Chgb", ["log2FoldChange", "padj"]].round(4).tolist()
    cnt["paper_n_deg"] = c["paper_n_deg"]
    results[c["name"]] = cnt
    o = case.add_output(deg, f"deg_{c['name']}")
    case.decide("execution", final={"method": "DESeq2", "subset": c["name"], "formula": "~ grp",
                "contrast": f"{c['treatment']} vs {c['control']}", "outputs": [o["path"]],
                "counts_under_applied_threshold": {k: cnt[k] for k in ("rule", "n_tested", "n_significant", "n_up", "n_down", "deg_sanity")}},
                evidence=[cin, o], reasoning="Paper route DESeq2 on the 8 samples of the two groups.", confidence="high",
                execution_status="completed")
    print(c["name"], {k: cnt[k] for k in ("n_tested", "n_significant", "n_up", "n_down", "deg_sanity", "paper_n_deg")}, "Chgb", cnt.get("Chgb"))
case.write_json("reproduction_summary.json", results)
