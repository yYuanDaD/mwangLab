import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import numpy as np, pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(RUN)
case = run.case("GSE134698")
A = case.dir / "aligned"
R = case.dir / "results"
paper = case.evidence_item("paper:9157dc41bd8cc2f50bcac3d30ac629f68d25204f.paper.md")
deg = R / "deseq2" / "DEG_results_after_vs_before.csv"
primary = native.apply_threshold(deg, metric="padj", cutoff=0.1, min_group_n=3)

# ---- audit sensitivity (not a gate): limma on quantile-normalized log2(count+1), top 12k, ~ subject + time
counts = pd.read_csv(A / "counts_top12000.csv", index_col=0)
full = pd.read_csv(A / "aligned_matrix.csv", index_col=0)
logc = np.log2(full + 1)
ranks = logc.rank(axis=0, method="first")
ref = np.sort(logc.values, axis=0).mean(axis=1)
qn = logc.copy()
for c in logc.columns:
    qn[c] = ref[(ranks[c].values - 1).astype(int)]
qn.loc[counts.index].to_csv(A / "qn_log2_top12000.csv")
aud_dir = R / "audit_limma_qnlog"
aud_dir.mkdir(parents=True, exist_ok=True)
audit = {}
try:
    native.call_tool("tools.limma_tools:run_limma_analysis", normalized_csv=str(A / "qn_log2_top12000.csv"),
                     metadata_csv=str(A / "design_metadata.csv"), design_column="time", control_group="before",
                     treatment_group="after", output_dir=str(aud_dir), covariate_columns="subject")
    adeg = [p for p in native.deg_outputs(aud_dir) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    audit = native.apply_threshold(adeg, metric="padj", cutoff=0.1, min_group_n=3)
    case.add_output(str(adeg), "audit_sensitivity")
except native.NativeToolError as e:
    audit = {"execution_error": str(e)}
print("AUDIT", audit)

# ---- concordance with paper TAB2
tab2 = pd.DataFrame([l.split("|")[1:5] for l in """|CYR61|ENSG00000142871|3.15E-05|1.745|
|RYR1|ENSG00000196218|1.97E-02|0.960|
|PLEC|ENSG00000178209|1.60E-02|1.064|
|APH1A|ENSG00000117362|5.67E-02|1.008|
|HSP90AB1|ENSG00000096384|5.67E-02|0.905|
|SYNPO2L|ENSG00000166317|5.67E-02|0.867|
|SLC25A4|ENSG00000151729|5.67E-02|-0.939|
|FLNC|ENSG00000128591|8.42E-02|0.873|
|SLC2A4|ENSG00000181856|8.42E-02|0.809|
|CRLF1|ENSG00000006016|8.42E-02|1.053|
|MPST|ENSG00000128309|8.80E-02|1.147|
|IER5|ENSG00000162783|8.80E-02|1.038|
|MT2A|ENSG00000125148|8.80E-02|1.169|
|RERE|ENSG00000142599|8.80E-02|0.955|
|HSPB7|ENSG00000173641|8.80E-02|0.812|
|CAVIN4|ENSG00000170681|8.80E-02|-0.909|
|NACA|ENSG00000196531|8.80E-02|0.857|
|KLHL40|ENSG00000157119|9.96E-02|1.034|
|GSN|ENSG00000148180|9.96E-02|0.769|
|PSMD3|ENSG00000108344|9.96E-02|0.924|
|NDUFS3|ENSG00000213619|9.96E-02|0.778|
|RN7SL2|ENSG00000274012|5.27E-02|1.592|
|BCYRN1|ENSG00000236824|6.56E-02|1.109|
|LYRM7|ENSG00000186687|9.98E-02|-1.173|
|TAPBP|ENSG00000231925|9.98E-02|1.065|
|SELENOW|ENSG00000178980|9.72E-02|-0.756|
|ND6|ENSG00000198695|5.56E-02|1.340|
|TUBA1C|ENSG00000167553|8.31E-02|1.124|""".splitlines()], columns=["symbol", "ens", "paper_padj", "paper_lfc"])
tab2[["paper_padj", "paper_lfc"]] = tab2[["paper_padj", "paper_lfc"]].astype(float)
r = pd.read_csv(deg, index_col=0); r["ens"] = r.index.str.split(".").str[0]
m = tab2.merge(r[["ens", "log2FoldChange", "pvalue", "padj"]], on="ens", how="left")
m.to_csv(R / "paper_table2_concordance.csv", index=False)
found = m["log2FoldChange"].notna()
conc = {"n_table2": len(m), "n_found_in_top12k": int(found.sum()),
        "missing": m.loc[~found, "symbol"].tolist(),
        "sign_agreement": int((np.sign(m.loc[found, "log2FoldChange"]) == np.sign(m.loc[found, "paper_lfc"])).sum()),
        "lfc_pearson_r": float(np.corrcoef(m.loc[found, "log2FoldChange"], m.loc[found, "paper_lfc"])[0, 1]),
        "n_padj_lt_0.1_ours": int((m["padj"] < 0.1).sum()),
        "median_ours_padj": float(m["padj"].median())}
print("CONC", conc)
conc_ev = case.add_output(str(R / "paper_table2_concordance.csv"), "tool_output")

# ---- enrichment: GSEA preranked (paper ran fgsea GO BP; repository GSEA uses MSigDB Hallmark)
fid = native.feature_id_report(deg)
print("FID", fid)
gs_dir = R / "gsea"
gs_dir.mkdir(parents=True, exist_ok=True)
degrec = case.add_output(str(deg), "tool_output")
efinal = {"method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark (h.all 2024.1.Hs)",
          "organism": "Human", "feature_id_type": fid["dominant_type"], "ranking_metric": "stat (DESeq2 Wald)",
          "paper_route": {"method": "fgsea on GO Biological Process, FDR 0.1, |NES|>1.7", "status": "blocked",
                          "reason": "repository GSEA executor supports only MSigDB Hallmark"},
          "significance_rule": "FDR q < 0.1 (paper's pathway FDR)"}
try:
    gmsg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Human",
                            ranking_metric="stat", output_dir=str(gs_dir))
    print(gmsg[-1800:])
    gout = [str(p) for p in gs_dir.rglob("*GSEA*.csv")]
    efinal["outputs"] = gout
    case.decide("enrichment", final=efinal, evidence=[degrec, paper], paper={"locator": "S0.p46"},
                reasoning="GSEA on full DESeq2 ranking; gene-set collection differs from paper (declared).",
                confidence="medium", execution_status="completed")
except native.NativeToolError as e:
    print("GSEA FAILED", e)
    efinal["execution_error"] = str(e)
    case.decide("enrichment", final=efinal, evidence=[degrec, paper], paper={"locator": "S0.p46"},
                reasoning="GSEA failed to execute.", confidence="medium", execution_status="failed")

disc = [{"item": "DEG significance", "paper": "Table 2 lists 28 genes with BH padj < 0.1 (curated subset; total not reported)",
         "data": f"paired DESeq2 on top-12k genes: {primary['n_significant']} gene padj<0.1 (CYR61); TAB2 log2FC reproduced (r={conc['lfc_pearson_r']:.3f}, sign {conc['sign_agreement']}/{conc['n_found_in_top12k']}) but padj much larger",
         "impact": "effect sizes reproduce; significance does not. Paper p-values imply smaller dispersion than R/py DESeq2 on these counts; exact paper pipeline (phantasus, quantile-normalized input) cannot be reconstructed from the text",
         "audit_limma_qnlog": audit},
        {"item": "GSEA gene sets", "paper": "fgsea GO BP", "data": "Hallmark only in repository executor", "impact": "pathway results not directly comparable"},
        {"item": "sample labels", "paper": "HF1/HF4/HF5 (TAB1)", "data": "P1/P4/P5 in GEO", "impact": "none; matched by age/BMI"}]
json.dump(disc, open(case.dir / "paper_data_discrepancies.json", "w", encoding="utf-8"), indent=1, default=str)

case.decide("study", final={"route": "paper_aligned", "exploratory": True,
                            "exploratory_reason": "3 subjects per arm; residual df = 2 (< 4) for ~ subject + time",
                            "paper_threshold_counts": primary, "paper_table2_concordance": conc,
                            "audit_limma_qnlog_counts": audit,
                            "deviations": ["pydeseq2 instead of R DESeq2", "GSEA on Hallmark instead of GO BP"]},
            evidence=[degrec, conc_ev, paper], paper={"locator": "S0.p46"},
            reasoning="Paper route (paired DESeq2, top-12k genes, BH FDR 0.1) executed; effect sizes match TAB2 closely but only CYR61 passes FDR 0.1.",
            confidence="medium")
case.finish(n_deg=primary["n_significant"], deg_sanity=primary["deg_sanity"])
run.finish()
print("PRIMARY", primary)
