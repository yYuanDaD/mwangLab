import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
C = pathlib.Path(RUN) / "GSE179302"; DMD = str(C / "aligned" / "design_metadata.csv")
x = pd.read_csv(C / "aligned" / "counts_filtered_paper30pct.csv", index_col=0)
d = pd.read_csv(DMD, index_col=0)
lib = x.sum(); ercc = x[x.index.str.startswith("ERCC")].sum() / lib
ercc_by = ercc.groupby(d.loc[x.columns, "tert"].values).median().round(3).to_dict()
FC = C / "aligned" / "counts_filtered_paper30pct_noERCC.csv"; x[~x.index.str.startswith("ERCC")].to_csv(FC)
fco = case.add_output(FC, "filtered_counts_noERCC")
note = (f"Execution-time refinement: ERCC spike-ins are 41-70% of assigned reads (median fraction by tertile {ercc_by}); "
        "total-count CPM including them produced a global +0.44 median log2FC shift in the first limma run, so the 89 ERCC rows are "
        "removed before normalization (19,171 endogenous genes). The earlier primary_limma_full_covariates/secondary_deseq2_without_age units are superseded.")
print(note)
TH = dict(metric="padj", cutoff=0.1, effect_cutoff=None)
out = {}
def gsea(unit, deg, G):
    fid = native.feature_id_report(deg); G.mkdir(exist_ok=True)
    try:
        native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Human", ranking_metric="stat", output_dir=str(G))
        o = sorted(str(p) for p in G.glob("*GSEA*.csv")); t = pd.read_csv(o[0]).sort_values("NES")
        sig = t[t["FDR q-val"] < 0.05]
        summ = {"n_sets": len(t), "fdr05_up": int((sig.NES > 0).sum()), "fdr05_down": int((sig.NES < 0).sum()),
                "down_fdr05": sig[sig.NES < 0].Term.tolist(), "up_fdr05": sig[sig.NES > 0].Term.tolist(),
                "ifn": t[t.Term.str.contains("INTERFERON|INFLAMMATORY|IL6|TNFA")][["Term", "NES", "FDR q-val"]].round(4).values.tolist()}
        print(unit, json.dumps(summ)[:1500])
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank), ranking=stat", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
            "organism": "Human", "feature_id_type": fid["dominant_type"], "subset": unit, "outputs": o, "summary": summ,
            "paper_enrichment": "IPA on DEGs (proprietary; not reproduced)"},
            evidence=[case.add_output(o[0], "gsea_table")], confidence="medium", execution_status="completed",
            reasoning="Full-ranking GSEA as an open substitute for the paper's IPA.")
    except native.NativeToolError as e:
        print("GSEA FAIL", e)
        case.decide("enrichment", final={"method": "GSEA preranked", "gene_sets": "MSigDB Hallmark", "organism": "Human",
            "feature_id_type": fid["dominant_type"], "subset": unit, "execution_error": str(e)}, evidence=[fco],
            confidence="medium", execution_status="failed", reasoning="GSEA failed")

L = C / "results" / "limma_full_noERCC"; L.mkdir(parents=True, exist_ok=True)
native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(FC), output_dir=str(L / "prep"), min_count=1, min_samples=1)
norm = native.find_outputs(L / "prep", "*_normalized.csv")[0]
native.call_tool("tools.limma_tools:run_limma_analysis", normalized_csv=str(norm), metadata_csv=DMD, design_column="tert",
      control_group="inactive", treatment_group="active", output_dir=str(L), design_formula="~ Treatment + C(sex) + age + C(race)", coefficient="Treatment")
deg = L / "DEG_results_active_vs_inactive.csv"; cnt = native.apply_threshold(deg, **TH); out["limma"] = cnt
t = pd.read_csv(deg, index_col=0); print("limma", {k: cnt[k] for k in ("n_tested", "n_significant", "n_up", "n_down")}, "median lfc", round(t.log2FoldChange.median(), 3), "p<0.05 frac", round((t.pvalue < 0.05).mean(), 3))
case.decide("execution", final={"method": "limma (log2(CPM+1), eBayes trend=False as implemented in tools/limma_tools.py:162) ~ sex + age + race + tert",
    "subset": "primary_limma_full_covariates_noERCC", "transform": "log2(CPM+1)", "outputs": [str(deg)], "counts": cnt, "n_samples": 21, "n_features": int(t.shape[0]),
    "refinement_note": note}, evidence=[fco, case.add_output(norm, "normalized_noERCC"), case.add_output(deg, "deg_table")],
    confidence="medium", execution_status="completed", reasoning="Primary declared-deviation route rerun on endogenous genes.")
gsea("primary_limma_full_covariates_noERCC", deg, L / "gsea")

D = C / "results" / "deseq2_no_age_noERCC"; D.mkdir(parents=True, exist_ok=True)
native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(FC), metadata_csv=DMD, design_column="tert",
      control_group="inactive", treatment_group="active", output_dir=str(D), covariate_columns="sex,race")
deg = D / "DEG_results_active_vs_inactive.csv"; cnt = native.apply_threshold(deg, **TH); out["deseq2"] = cnt
t = pd.read_csv(deg, index_col=0); print("deseq2", {k: cnt[k] for k in ("n_tested", "n_significant", "n_up", "n_down")}, "median lfc", round(t.log2FoldChange.median(), 3), "p<0.05 frac", round((t.pvalue < 0.05).mean(), 3))
case.decide("execution", final={"method": "DESeq2 ~ sex + race + tert", "subset": "secondary_deseq2_without_age_noERCC", "outputs": [str(deg)], "counts": cnt,
    "refinement_note": note}, evidence=[fco, case.add_output(deg, "deg_table")], confidence="high", execution_status="completed",
    reasoning="Secondary sensitivity route rerun on endogenous genes.")
gsea("secondary_deseq2_without_age_noERCC", deg, D / "gsea")
json.dump(out, open(C / "results" / "final_threshold_counts.json", "w", encoding="utf-8"), indent=1, default=str)
