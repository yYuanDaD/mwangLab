"""Gate 9 execution: paper CPM filter -> R limma-voom ExT vs Sed, per fraction."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40577041"
run = native.RunRecorder.open(RUN)
CFG = {"PMID40577041_SM": (1.0, False, ">1 CPM in all samples"),
       "PMID40577041_MT": (2.0, True, ">=2 CPM in all samples"),
       "PMID40577041_LV": (1.0, False, ">1 CPM in all samples")}
PAPER = {"PMID40577041_SM": {"FDR<0.05": 34, "FDR<0.05_up": 30, "FDR<0.05_down": 4, "FDR<0.2": 487, "FDR<0.2_up": 347, "FDR<0.2_down": 140},
         "PMID40577041_MT": {"FDR<0.05": 0, "p<0.05": 365},
         "PMID40577041_LV": {"FDR<0.05": 0, "p<0.01": 121, "p<0.05": 738}}
short = lambda d: {k: d[k] for k in ("n_significant", "n_up", "n_down")}
GOI = {"ENSRNOG00000013915": None}  # placeholder, replaced by symbol lookup below

for cid, (cmin, incl, rule) in CFG.items():
    case = run.case(cid)
    cdir = case.dir
    t = cid.split("_")[-1]
    aligned = cdir / "aligned" / "aligned_matrix.csv"
    design = cdir / "aligned" / "design_metadata.csv"
    res = cdir / "results"; res.mkdir(parents=True, exist_ok=True)
    counts = pd.read_csv(aligned, index_col=0)
    cpm = counts / counts.sum() * 1e6
    keep = ((cpm >= cmin) if incl else (cpm > cmin)).all(axis=1)
    filt = res / f"GSE267763_{t}_counts_filtered.csv"
    counts.loc[keep].to_csv(filt)
    case.add_output(filt, "filtered_counts")
    out_dir = res / "voom"
    try:
        msg = native.call_tool("tools.limma_voom_tools:run_limma_voom_analysis", counts_csv=str(filt),
                               metadata_csv=str(design), design_column="grp", control_group="Sed",
                               treatment_group="ExT", output_dir=str(out_dir))
        print(cid, msg)
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "limma-voom", "execution_error": str(e)},
                    evidence=[case.add_output(filt, "filtered_counts")], reasoning="voom executor failed",
                    confidence="high", execution_status="failed")
        print(cid, "FAILED", e)
        continue
    deg = [p for p in native.deg_outputs(out_dir) if "GSEA" not in str(p)][0]
    item = case.add_output(deg, f"deg_{t}_ExT_vs_Sed")
    applied = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
    audit = {"pvalue<0.05": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=None)),
             "pvalue<0.01": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.01, effect_cutoff=None)),
             "padj<0.2": short(native.apply_threshold(deg, metric="padj", cutoff=0.2, effect_cutoff=None)),
             "padj<0.1": short(native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=None))}
    tb = pd.read_csv(deg, index_col=0)
    ann = pd.read_csv(f"data/GSE267763/GSE267763_counts_matrix_{t}.csv.gz", index_col=0).iloc[:, :2]
    ann.columns = ["symbol", "biotype"]
    tb = tb.join(ann)
    sig = tb[tb.padj < 0.05].sort_values("pvalue")
    top = [{"gene": g, "symbol": r.symbol, "biotype": r.biotype, "log2FC": round(float(r.log2FoldChange), 3),
            "padj": float(r.padj)} for g, r in sig.head(40).iterrows()]
    goi_syms = ["Cox7a1", "Myh7", "Myh4", "Myh1", "Myl1", "Tnni2", "Tnnt3", "Ppargc1a", "Mt-co1"]
    goi = {s: {"log2FC": round(float(r.log2FoldChange), 3), "pvalue": float(r.pvalue), "padj": float(r.padj)}
           for s in goi_syms for g, r in tb[tb.symbol == s].iterrows()}
    summary = {"filter": rule, "n_genes_tested": int(keep.sum()), "n_samples": int(counts.shape[1]),
               "applied_FDR<0.05": applied, "audit": audit, "paper": PAPER[cid], "top_sig": top, "genes_of_interest": goi}
    sp = case.write_json("results/deg_counts.json", summary, role="deg_counts")
    print(cid, json.dumps({"tested": int(keep.sum()), "applied": short(applied), "audit": audit, "paper": PAPER[cid],
                           "goi": goi}, indent=1))
    case.decide("execution",
                final={"method": "limma-voom (R limma::voom, lmFit, eBayes; ~ grp; BH)", "filter": rule,
                       "n_genes_tested": int(keep.sum()),
                       "outputs": [{"contrast": f"{t}_ExT_vs_Sed", "path": str(deg), "sha256": item.get("sha256")}],
                       "deg_counts_applied": short(applied), "deg_sanity": applied.get("deg_sanity"),
                       "audit_counts": audit, "paper_counts": PAPER[cid]},
                evidence=[sp, item], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning=f"voom on {int(keep.sum())} genes passing {rule}; FDR<0.05 applied with native.apply_threshold.",
                execution_status="completed")
