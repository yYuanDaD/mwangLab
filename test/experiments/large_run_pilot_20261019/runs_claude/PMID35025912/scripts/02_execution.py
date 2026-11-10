"""Gate 9 execution: median-CPM filter -> log2(CPM+1) -> limma ~ 0 + cell + rin on 48 samples (joint)."""
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
aligned = cdir / "aligned" / "aligned_matrix.csv"
design = cdir / "aligned" / "design_metadata.csv"
res_dir = cdir / "results"; res_dir.mkdir(parents=True, exist_ok=True)

sc = json.loads((cdir / "suitability_comparisons.json").read_text(encoding="utf-8"))
rep = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
allc = {c["name"]: c for c in rep["comparisons"]}
run_names = sc["planned"] + sc["exploratory"]
comparisons = [allc[n] for n in run_names]
LABEL = dict(zip(sc["planned"], ["PLN_HIinLRT", "PLN_HIinHRT", "PLN_DELTA", "SOL_HIinLRT", "SOL_HIinHRT", "SOL_DELTA"]))

counts = pd.read_csv(aligned, index_col=0)
cpm = counts / counts.sum() * 1e6
keep = cpm.median(axis=1) >= 0.5
filt_csv = res_dir / "GSE159861_counts_medcpm0.5.csv"
counts.loc[keep].to_csv(filt_csv)
print("kept", int(keep.sum()), "of", len(keep))
case.add_output(filt_csv, "filtered_counts")
msg = native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(filt_csv),
                       output_dir=str(res_dir), min_count=0, min_samples=1)
print(msg)
norm = native.find_outputs(res_dir, "*_normalized.csv")[0]
nm = pd.read_csv(norm, index_col=0)
assert nm.shape[0] == int(keep.sum()), nm.shape
case.add_output(norm, "log2cpm_matrix")

out = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(norm), metadata_csv=str(design),
                       comparisons=comparisons, output_dir=str(res_dir / "joint_limma_rin"), covariates=["rin"])
out_a = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(norm), metadata_csv=str(design),
                         comparisons=comparisons, output_dir=str(res_dir / "audit_joint_limma_norin"))
# audit: per-muscle models (24 samples each), same filter, with RIN
dm = pd.read_csv(design, index_col=0)
per_tis = {}
for t in ("PLN", "SOL"):
    sub = dm[dm.tis == t]
    sp = res_dir / f"design_metadata_{t}.csv"; sub.to_csv(sp)
    ep = res_dir / f"log2cpm_{t}.csv"; nm[sub.index].to_csv(ep)
    comps_t = [c for c in comparisons if c["within"].get("tis") == t]
    per_tis[t] = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(ep), metadata_csv=str(sp),
                                  comparisons=comps_t, output_dir=str(res_dir / f"audit_limma_rin_{t}only"), covariates=["rin"])

PAPER = {"PLN_HIinLRT": {"n": 744, "pct_down": 58.5}, "PLN_HIinHRT": {"n": 251, "pct_down": 66.5},
         "SOL_HIinLRT": {"n": 294, "pct_down": 57.1}, "SOL_HIinHRT": {"n": 326, "pct_down": 57.1}}
short = lambda d: {k: d[k] for k in ("n_significant", "n_up", "n_down")}
counts_out, outputs, audit = {}, [], {"no_rin": {}, "per_muscle": {}}
sigsets = {}
for r in out["results"]:
    lab = LABEL.get(r["name"], r["name"])
    t = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0)
    counts_out[lab] = {"paper_rule": t,
                       "audit_padj0.001": short(native.apply_threshold(r["path"], metric="padj", cutoff=0.001)),
                       "audit_padj0.001_lfc1": short(native.apply_threshold(r["path"], metric="padj", cutoff=0.001, effect_cutoff=1.0)),
                       "audit_padj0.05": short(native.apply_threshold(r["path"], metric="padj", cutoff=0.05)),
                       "paper": PAPER.get(lab, "not_reported"),
                       "role": "paper_planned" if r["name"] in LABEL else "exploratory"}
    item = case.add_output(r["path"], f"deg_{lab}")
    outputs.append({"contrast": lab, "suitability_name": r["name"], "path": r["path"], "sha256": item.get("sha256")})
    tb = pd.read_csv(r["path"], index_col=0)
    sigsets[lab] = set(tb.index[(tb.padj < 0.05) & (tb.log2FoldChange.abs() > 1)])
for r in out_a["results"]:
    audit["no_rin"][LABEL.get(r["name"], r["name"])] = short(native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0))
    case.add_output(r["path"], f"audit_norin_{r['name']}")
for t, o in per_tis.items():
    for r in o["results"]:
        audit["per_muscle"][LABEL.get(r["name"], r["name"])] = short(native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0))
        case.add_output(r["path"], f"audit_permuscle_{r['name']}")
four = ["PLN_HIinLRT", "PLN_HIinHRT", "SOL_HIinLRT", "SOL_HIinHRT"]
common4 = len(set.intersection(*[sigsets[k] for k in four]))

# atrogene / gene-of-interest logFCs (paper S3.7.p1); symbols via MyGene (rat)
goi = {}
try:
    import mygene
    hits = mygene.MyGeneInfo().querymany(["Trim63", "Fbxo32", "Hdac4", "Mtor", "Ubr5"], scopes="symbol",
                                         fields="ensembl.gene", species="rat", verbose=False)
    ens = {}
    for h in hits:
        e = h.get("ensembl")
        if e:
            e = e if isinstance(e, list) else [e]
            ens[h["query"]] = [x["gene"] for x in e]
    for lab in four:
        path = next(o["path"] for o in outputs if o["contrast"] == lab)
        tb = pd.read_csv(path, index_col=0)
        goi[lab] = {s: {"log2FC": round(float(tb.loc[g, "log2FoldChange"]), 2), "padj": float(tb.loc[g, "padj"])}
                    for s, gl in ens.items() for g in gl if g in tb.index}
except Exception as e:  # network / mapping failure only affects this side check
    goi = {"error": str(e)}
paper_goi = {"PLN_HIinHRT": {"Trim63": 1.41, "Fbxo32": 1.62, "Hdac4": 2.14, "Mtor": 0.49, "Ubr5": 0.32},
             "PLN_HIinLRT": {"Trim63": 2.55, "Fbxo32": 2.74, "Hdac4": 2.89, "Mtor": 0.65, "Ubr5": 0.54},
             "SOL_HIinHRT": {"Hdac4": 1.85, "Mtor": 0.32}, "SOL_HIinLRT": {"Hdac4": 2.21, "Mtor": 0.59}}

summary = {"n_genes_tested": int(keep.sum()), "formula": "~ 0 + C(cell) + rin (continuous)",
           "design_rank": out.get("design_rank"), "residual_df": out.get("residual_df"), "cells": out.get("cells"),
           "counts": counts_out, "common_all_four_HI_contrasts": common4, "paper_common": 40,
           "audit_paper_rule": audit, "genes_of_interest": goi, "paper_genes_of_interest": paper_goi}
case.write_json("results/deg_counts.json", summary, role="deg_counts")
print(json.dumps({k: {"ours": short(v["paper_rule"]), "paper": v["paper"]} for k, v in counts_out.items()}, indent=1))
print(json.dumps({"common4": common4, "audit": audit, "goi": goi, "rank": out.get("design_rank"), "df": out.get("residual_df")}, indent=1, default=str))

case.decide("execution",
            final={"method": "limma (inmoose) on log2(CPM+1), ~ 0 + cell + rin on 48 samples, contrasts.fit + eBayes, BH per contrast",
                   "outputs": outputs, "n_genes_tested": int(keep.sum()), "design_rank": out.get("design_rank"),
                   "residual_df": out.get("residual_df"),
                   "deg_counts_paper_rule": {k: short(v["paper_rule"]) for k, v in counts_out.items()},
                   "deg_sanity": {k: v["paper_rule"].get("deg_sanity") for k, v in counts_out.items()},
                   "audit": audit, "common_all_four_HI_contrasts": common4},
            evidence=[case.add_output(cdir / "results" / "deg_counts.json", "deg_counts_summary")],
            reasoning="Approved route ran on all 48 samples; counts from native.apply_threshold under the paper rule (FDR<0.05 & |log2FC|>1).",
            confidence="high", execution_status="completed", decision_status="valid")
