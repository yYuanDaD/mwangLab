"""Execution and study gates for GSE196147: log2(x+1) -> limma ~ 0 + C(grp) + C(animal), all 10 comparisons."""
import sys, pathlib, json, math
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import numpy as np
import pandas as pd
from tools import native

native.enable_native_mode()
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
REL = str(RUN.relative_to(ROOT)).replace("\\", "/")
run = native.RunRecorder.open(REL)
case = run.case("GSE196147")
cdir = case.dir
PLANNED = ["grp_d2_vs_ctrl", "grp_d10_vs_ctrl", "grp_d20_vs_ctrl", "grp_d30_vs_ctrl"]
PAPER = {"grp_d2_vs_ctrl": 2398, "grp_d10_vs_ctrl": 2218, "grp_d20_vs_ctrl": 1755, "grp_d30_vs_ctrl": 3312}

aligned = cdir / "aligned" / "aligned_matrix.csv"
design_meta = cdir / "aligned" / "design_metadata.csv"
comps = json.loads((cdir / "comparisons.json").read_text(encoding="utf-8"))
res_dir = cdir / "results"; res_dir.mkdir(exist_ok=True)

lt = native.log_transform(aligned, res_dir / "log2_norm_plus1.csv")
log_item = case.add_output(res_dir / "log2_norm_plus1.csv", "log2_matrix")
method = "limma joint model ~ 0 + C(grp) + C(animal) on log2(DESeq2-normalized + 1)"
try:
    out = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(res_dir / "log2_norm_plus1.csv"),
                           metadata_csv=str(design_meta), comparisons=comps, output_dir=str(res_dir / "joint_limma"),
                           covariates=("animal",))
except native.NativeToolError as e:
    case.decide("execution", final={"method": method, "execution_error": str(e)}, evidence=[log_item],
                reasoning="executor failed", confidence="high", execution_status="failed")
    case.decide("study", final={"route": "declared_deviation"}, evidence=[log_item], reasoning="planned route recorded",
                confidence="high", execution_status="failed")
    case.finish(); run.finish(); raise SystemExit(str(e))

(res_dir / "joint_limma_return.json").write_text(json.dumps(out, indent=2, default=str))
degs = native.deg_outputs(res_dir / "joint_limma")
print("outputs:", [p.name for p in map(pathlib.Path, degs)])

# concordance reference: GEO Partek GSA result (4635 genes; Log2(Ratio) is Control/Trained -> sign flipped)
gsa = pd.read_csv(ROOT / "data/GSE196147/GSE196147_2gsa_result.txt.gz", sep="\t", index_col=0)
tmap = pd.read_csv(RUN / "inputs/transcript_gene_map.csv")
gsa_lab = {"grp_d2_vs_ctrl": "2 Days", "grp_d10_vs_ctrl": "10 Days", "grp_d20_vs_ctrl": "20 Days", "grp_d30_vs_ctrl": "30 Days"}

results, outputs, counts_all, deg_items = {}, [], {}, []
for comp in comps:
    name = comp["name"]
    hit = [p for p in degs if pathlib.Path(p).name == f"DEG_results_{name}.csv"]
    if not hit:
        results[name] = {"status": "no output file"}; continue
    f = pathlib.Path(hit[0])
    item = case.add_output(f, f"deg_{name}"); deg_items.append(item)
    outputs.append(str(f).replace("\\", "/"))
    c = native.apply_threshold(f, metric="padj", cutoff=0.05)
    a = native.apply_threshold(f, metric="pvalue", cutoff=0.01)
    t = pd.read_csv(f, index_col=0)
    r = {"route": "paper" if name in PLANNED else "exploratory",
         "n_deg": c["n_significant"], "up": c.get("n_up"), "down": c.get("n_down"), "deg_sanity": c["deg_sanity"],
         "audit_p_lt_0.01": a["n_significant"], "paper_n_deg_q_lt_0.05": PAPER.get(name)}
    if name in gsa_lab:
        lab = gsa_lab[name]
        sym = tmap.set_index("Transcript")["Gene Symbol"]
        t2 = t.assign(sym=sym.reindex(t.index).values).dropna(subset=["sym"])
        t2 = t2.loc[t2.groupby("sym")["AveExpr" if "AveExpr" in t2 else "log2FoldChange"].idxmax()] if "AveExpr" in t2 else t2.drop_duplicates("sym")
        t2 = t2.set_index("sym")
        common = t2.index.intersection(gsa.index)
        ref = -gsa.loc[common, f"Log2(Ratio) (Control vs. {lab})"]
        ours = t2.loc[common, "log2FoldChange"]
        sig = gsa.loc[common, f"FDR step up (Control vs. {lab})"] < 0.05
        r["concordance_vs_geo_gsa"] = {"n_genes": int(len(common)),
                                       "pearson_logfc": round(float(np.corrcoef(ours, ref)[0, 1]), 3),
                                       "pearson_logfc_on_gsa_sig": round(float(np.corrcoef(ours[sig], ref[sig])[0, 1]), 3),
                                       "sign_agreement_on_gsa_sig": round(float((np.sign(ours[sig]) == np.sign(ref[sig])).mean()), 3),
                                       "gsa_fdr05": int(sig.sum())}
    results[name] = r
    counts_all[name] = c
print(json.dumps(results, indent=1, default=str))

# common DEGs across the four planned contrasts
sets = {}
for name in PLANNED:
    f = [p for p in degs if pathlib.Path(p).name == f"DEG_results_{name}.csv"][0]
    t = pd.read_csv(f, index_col=0); sets[name] = set(t.index[t["padj"] < 0.05])
common4 = set.intersection(*sets.values())

case.decide("execution", final={
    "method": method, "formula": "~ 0 + C(grp) + C(animal)", "transform": "log2(x+1)",
    "executor": "tools.joint_contrasts:run_joint_limma", "outputs": outputs,
    "n_features": int(pd.read_csv(res_dir / "log2_norm_plus1.csv", index_col=0).shape[0]),
    "skipped": out.get("skipped"), "applied_threshold": "BH padj < 0.05, no effect cutoff",
    "per_contrast": results, "common_deg_all_4_planned": len(common4)},
    evidence=[log_item] + deg_items,
    reasoning="Executor completed on all 24 samples; counts from native.apply_threshold.", confidence="high",
    execution_status="completed")

summary = {"planned": {n: results[n] for n in PLANNED}, "exploratory": {n: v for n, v in results.items() if n not in PLANNED},
           "common_deg_all_4_planned": len(common4), "paper_common": 519,
           "threshold": "BH padj < 0.05 (paper q < .05 on deviation route)"}
case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
case.decide("study", final={
    "route": "declared_deviation",
    "deviation": "limma on log2(DESeq2-normalized + 1) with animal blocking instead of DESeq2 on raw counts with pooled unblocked controls",
    "exploratory": [n for n in results if n not in PLANNED],
    "exploratory_reason": "between-duration contrasts are not tested by the paper (it compares durations only via SOM/Venn of per-duration DEGs)"},
    evidence=[log_item] + deg_items, reasoning="Paper route blocked by missing raw counts; planned contrasts kept.", confidence="high",
    execution_status="completed")
tot = sum(results[n]["n_deg"] for n in PLANNED)
case.finish(n_deg=tot, deg_sanity="; ".join(f"{n}:{results[n]['deg_sanity']}" for n in PLANNED))
run.finish()
print("common4", len(common4))
