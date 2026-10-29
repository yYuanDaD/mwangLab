import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
C = pathlib.Path(RUN) / "GSE179302"; DMD = str(C / "aligned" / "design_metadata.csv")
FC = str(C / "aligned" / "counts_filtered_paper30pct.csv"); fco = case.evidence_item("tool_output:counts_filtered_paper30pct.csv")
TH = dict(metric="padj", cutoff=0.1, effect_cutoff=None)
res = {}
for name, covs in [("audit_deseq2_unadjusted", ""), ("audit_deseq2_sex_hisp", "sex,hisp")]:
    D = C / "results" / name; D.mkdir(parents=True, exist_ok=True)
    meth = "DESeq2 ~ " + " + ".join([c for c in covs.split(",") if c] + ["tert"])
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=FC, metadata_csv=DMD, design_column="tert",
            control_group="inactive", treatment_group="active", output_dir=str(D), covariate_columns=covs)
        deg = [p for p in native.deg_outputs(D) if pathlib.Path(p).name.startswith("DEG_results_")][0]
        cnt = native.apply_threshold(deg, **TH); res[name] = cnt
        print(name, {k: cnt[k] for k in ("n_significant", "n_up", "n_down")})
        case.decide("execution", final={"method": meth, "subset": name, "outputs": [str(deg)], "counts": cnt,
            "role": "audit only (not the planned estimand): omits paper covariates; shows how adjustment set drives DEG counts"},
            evidence=[fco, case.add_output(deg, "deg_table_audit")], confidence="high", execution_status="completed",
            reasoning="Audit model to explain the gap to the paper's 767 DEGs.")
    except native.NativeToolError as e:
        print(name, "FAIL", e)
        case.decide("execution", final={"method": meth, "subset": name, "execution_error": str(e)}, evidence=[fco],
            confidence="high", execution_status="failed", reasoning="audit executor failed")

# GSEA on primary (limma full) and secondary (DESeq2 no age)
for unit, sub in [("primary_limma_full_covariates", "limma_full"), ("secondary_deseq2_without_age", "deseq2_no_age")]:
    D = C / "results" / sub; deg = str(D / "DEG_results_active_vs_inactive.csv")
    fid = native.feature_id_report(deg); print(unit, fid["dominant_type"], fid.get("gene_set_ready"))
    G = D / "gsea"; G.mkdir(exist_ok=True)
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Human", ranking_metric="stat", output_dir=str(G))
        outs = [str(p) for p in G.glob("*GSEA*")]
        top = pd.read_csv(outs[0]) if outs else None
        if top is not None:
            cols = [c for c in top.columns if c.lower() in ("term", "nes", "fdr q-val", "fdr_q-val", "fdr")]
            print(top[cols].head(8).to_string())
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank), ranking=stat", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
            "organism": "Human", "feature_id_type": fid["dominant_type"], "subset": unit, "outputs": outs,
            "paper_enrichment": "IPA on DEGs (proprietary; not reproduced)"},
            evidence=[case.add_output(outs[0], "gsea_table")] if outs else [fco], confidence="medium", execution_status="completed",
            reasoning="Full-ranking GSEA as an open substitute for the paper's IPA pathway analysis.")
    except native.NativeToolError as e:
        print("GSEA FAIL", e)
        case.decide("enrichment", final={"method": "GSEA preranked", "gene_sets": "MSigDB Hallmark", "organism": "Human",
            "feature_id_type": fid["dominant_type"], "subset": unit, "execution_error": str(e)}, evidence=[fco],
            confidence="medium", execution_status="failed", reasoning="GSEA failed")
