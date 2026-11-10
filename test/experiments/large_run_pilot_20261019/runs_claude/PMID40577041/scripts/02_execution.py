"""Gate 9 execution, per fraction:
primary  limma (inmoose) on log2(TMM-CPM+1) after the paper CPM filter
audits   R limma-voom lib.size only (repository executor), edgeR QL (TMM), DESeq2
"""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import numpy as np, pandas as pd
from tools import native
from tools.de_common import tmm_factors

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40577041"
run = native.RunRecorder.open(RUN)
CFG = {"PMID40577041_SM": (1.0, False, ">1 CPM in all samples"),
       "PMID40577041_MT": (2.0, True, ">=2 CPM in all samples"),
       "PMID40577041_LV": (1.0, False, ">1 CPM in all samples")}
PAPER = {"PMID40577041_SM": {"FDR<0.05": "34 (30 up, 4 down)", "FDR<0.2": "487 (347 up, 140 down)"},
         "PMID40577041_MT": {"FDR<0.05": "0", "p<0.05": "365"},
         "PMID40577041_LV": {"FDR<0.05": "0", "p<0.01": "121", "p<0.05": "738"}}
short = lambda d: {k: d[k] for k in ("n_significant", "n_up", "n_down")}
GOI = ["Cox7a1", "Myh7", "Myh2", "Myh4", "Myh1", "Myl1", "Mylpf", "Tnni2", "Tnnt3", "Ppargc1a", "Mt-co1"]


def rules(deg):
    tb = pd.read_csv(deg, index_col=0)
    return {"FDR<0.05": short(native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)),
            "FDR<0.2": short(native.apply_threshold(deg, metric="padj", cutoff=0.2, effect_cutoff=None)),
            "p<0.05": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=None)),
            "p<0.01": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.01, effect_cutoff=None)),
            "pvalue_histogram_10bins": np.histogram(tb.pvalue.dropna(), bins=10, range=(0, 1))[0].tolist()}


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
    fc = counts.loc[keep]
    filt = res / f"GSE267763_{t}_counts_filtered.csv"
    fc.to_csv(filt)
    filt_ev = case.add_output(filt, "filtered_counts")
    nf = tmm_factors(fc)
    eff = fc.sum() * nf
    logcpm = np.log2(fc / eff * 1e6 + 1)
    lp = res / f"GSE267763_{t}_log2cpm_tmm.csv"
    logcpm.to_csv(lp)
    lp_ev = case.add_output(lp, "log2cpm_tmm_matrix")
    case.write_json("results/tmm_factors.json", nf.round(5).to_dict(), role="tmm_factors")

    ann = pd.read_csv(f"data/GSE267763/GSE267763_counts_matrix_{t}.csv.gz", index_col=0).iloc[:, :2]
    ann.columns = ["symbol", "biotype"]
    try:
        native.call_tool("tools.limma_tools:run_limma_analysis", normalized_csv=str(lp), metadata_csv=str(design),
                         design_column="grp", control_group="Sed", treatment_group="ExT", output_dir=str(res / "limma_tmm"))
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "limma on log2(TMM-CPM+1)", "execution_error": str(e)},
                    evidence=[lp_ev], reasoning="limma executor failed", confidence="high",
                    execution_status="failed", paper={"locator": "S2.10.p1"})
        print(cid, "FAILED", e)
        continue
    deg = [p for p in native.deg_outputs(res / "limma_tmm") if "GSEA" not in str(p)][0]
    item = case.add_output(deg, f"deg_{t}_ExT_vs_Sed")
    applied = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
    primary = rules(deg)
    tb = pd.read_csv(deg, index_col=0).join(ann)
    sig = tb[tb.padj < 0.05].sort_values("pvalue")
    top = [{"gene": g, "symbol": r.symbol, "biotype": r.biotype, "log2FC": round(float(r.log2FoldChange), 3),
            "padj": float(r.padj)} for g, r in sig.head(50).iterrows()]
    goi = {s: {"log2FC": round(float(r.log2FoldChange), 3), "pvalue": float(r.pvalue), "padj": float(r.padj)}
           for s in GOI for g, r in tb[tb.symbol == s].iterrows()}

    audits = {}
    for name, fn, kw in [("voom_libsize_R", "tools.limma_voom_tools:run_limma_voom_analysis", {"counts_csv": str(filt)}),
                         ("edgeR_QL_TMM", "tools.edger_tools:run_edger_analysis", {"counts_csv": str(filt)}),
                         ("DESeq2", "tools.deseq2_tools:run_deseq2_analysis", {"counts_csv": str(filt)})]:
        od = res / "audit" / name
        try:
            native.call_tool(fn, metadata_csv=str(design), design_column="grp", control_group="Sed",
                             treatment_group="ExT", output_dir=str(od), **kw)
            ad = [p for p in native.deg_outputs(od) if "GSEA" not in str(p)][0]
            audits[name] = rules(ad)
            at = pd.read_csv(ad, index_col=0)
            common = tb.index.intersection(at.index)
            audits[name]["log2FC_pearson_vs_primary"] = round(float(np.corrcoef(tb.loc[common, "log2FoldChange"], at.loc[common, "log2FoldChange"])[0, 1]), 4)
            audits[name]["overlap_FDR<0.05_with_primary"] = int(len(set(sig.index) & set(at.index[at.padj < 0.05])))
            case.add_output(ad, f"audit_{name}")
        except native.NativeToolError as e:
            audits[name] = {"execution_error": str(e)[:500]}
    summary = {"filter": rule, "n_genes_tested": int(keep.sum()), "n_samples": int(counts.shape[1]),
               "tmm_factor_range": [round(float(nf.min()), 3), round(float(nf.max()), 3)],
               "primary_limma_tmm": primary, "applied_FDR<0.05": applied, "audits": audits, "paper": PAPER[cid],
               "top_sig": top, "genes_of_interest": goi}
    sp = case.write_json("results/deg_counts.json", summary, role="deg_counts")
    print(cid, json.dumps({"tested": int(keep.sum()), "primary": {k: v for k, v in primary.items()},
                           "audits": {k: {kk: v.get(kk) for kk in ("FDR<0.05", "p<0.05", "log2FC_pearson_vs_primary")} for k, v in audits.items()},
                           "paper": PAPER[cid], "goi": goi, "top": [(x["symbol"], x["log2FC"]) for x in top[:40]]}, indent=None, default=str))
    case.decide("execution",
                final={"method": "limma (inmoose lmFit + eBayes, ~ grp, BH) on log2(TMM-CPM+1)", "filter": rule,
                       "n_genes_tested": int(keep.sum()),
                       "outputs": [{"contrast": f"{t}_ExT_vs_Sed", "path": str(deg), "sha256": item.get("sha256")}],
                       "deg_counts_applied": short(applied), "deg_sanity": applied.get("deg_sanity"),
                       "other_rules": {k: v for k, v in primary.items() if k != "FDR<0.05"},
                       "audit_routes": {k: {kk: v.get(kk) for kk in ("FDR<0.05", "p<0.05", "p<0.01", "FDR<0.2", "log2FC_pearson_vs_primary", "overlap_FDR<0.05_with_primary", "execution_error") if kk in v} for k, v in audits.items()},
                       "paper_counts": PAPER[cid]},
                evidence=[sp, item, filt_ev, lp_ev], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning=f"limma on TMM log2-CPM for {int(keep.sum())} genes passing {rule}; FDR<0.05 counted with native.apply_threshold; three audit routes on the same filtered counts.",
                execution_status="completed")
