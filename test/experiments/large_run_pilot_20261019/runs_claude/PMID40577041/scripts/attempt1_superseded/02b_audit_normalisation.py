"""Audit only (not the paper route): does library-size-only voom explain the MT p-value pile-up near 1?
Same filtered counts and contrast through composition-robust routes:
  - edgeR QL (TMM, tools.edger_tools)
  - DESeq2 (median-of-ratios, tools.deseq2_tools)
  - limma on TMM-scaled log2(CPM+1) (tools.de_common.tmm_factors + tools.limma_tools)
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
short = lambda d: {k: d[k] for k in ("n_significant", "n_up", "n_down")}
allout = {}
for cid in ["PMID40577041_SM", "PMID40577041_MT", "PMID40577041_LV"]:
    case = run.case(cid)
    t = cid.split("_")[-1]
    cdir = case.dir; res = cdir / "results"
    filt = res / f"GSE267763_{t}_counts_filtered.csv"
    design = cdir / "aligned" / "design_metadata.csv"
    full = pd.read_csv(cdir / "aligned" / "aligned_matrix.csv", index_col=0)
    counts = pd.read_csv(filt, index_col=0)
    ann = pd.read_csv(f"data/GSE267763/GSE267763_counts_matrix_{t}.csv.gz", index_col=0).iloc[:, 1]
    mt_rrna_frac = (full.loc[full.index.intersection(ann[ann == "Mt_rRNA"].index)].sum() / full.sum())
    nf = tmm_factors(counts)
    out = {"tmm_factor_range": [round(float(nf.min()), 3), round(float(nf.max()), 3)],
           "Mt_rRNA_fraction_of_library": [round(float(mt_rrna_frac.min()), 3), round(float(mt_rrna_frac.max()), 3)],
           "routes": {}}
    eff = counts.sum() * nf
    logcpm = np.log2(counts / eff * 1e6 + 1)
    adir = res / "audit"; adir.mkdir(parents=True, exist_ok=True)
    lp = adir / f"log2cpm_tmm_{t}.csv"; logcpm.to_csv(lp)
    routes = {
        "edgeR_QL_TMM": ("tools.edger_tools:run_edger_analysis", dict(counts_csv=str(filt))),
        "DESeq2": ("tools.deseq2_tools:run_deseq2_analysis", dict(counts_csv=str(filt))),
        "limma_TMM_log2CPM": ("tools.limma_tools:run_limma_analysis", dict(normalized_csv=str(lp))),
    }
    for name, (fn, kw) in routes.items():
        od = adir / name
        try:
            native.call_tool(fn, metadata_csv=str(design), design_column="grp", control_group="Sed",
                             treatment_group="ExT", output_dir=str(od), **kw)
            deg = [p for p in native.deg_outputs(od) if "GSEA" not in str(p)][0]
            tb = pd.read_csv(deg, index_col=0)
            out["routes"][name] = {
                "FDR<0.05": short(native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)),
                "p<0.05": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=None)),
                "p<0.01": short(native.apply_threshold(deg, metric="pvalue", cutoff=0.01, effect_cutoff=None)),
                "FDR<0.2": short(native.apply_threshold(deg, metric="padj", cutoff=0.2, effect_cutoff=None)),
                "pvalue_histogram_10bins": np.histogram(tb.pvalue.dropna(), bins=10, range=(0, 1))[0].tolist(),
                "n_tested": int(tb.pvalue.notna().sum())}
            case.add_output(deg, f"audit_{name}")
        except native.NativeToolError as e:
            out["routes"][name] = {"execution_error": str(e)[:500]}
    v = pd.read_csv(res / "voom" / "DEG_results_ExT_vs_Sed.csv", index_col=0)
    out["voom_libsize_pvalue_histogram_10bins"] = np.histogram(v.pvalue, bins=10, range=(0, 1))[0].tolist()
    case.write_json("results/audit/audit_normalisation.json", out, role="audit_normalisation")
    allout[cid] = out
print(json.dumps(allout, indent=1))
