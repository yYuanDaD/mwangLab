"""Deliverables report generator (OFFLINE — recomputes concordance from already-saved
DEG outputs + reference slices; runs NO differential-expression analysis).

Inputs (all on disk):
  RNA-seq  our  : test/output/smoke_test/val132520_{WT_only,pooled}/DEG_*.csv  (limma-trend)
                  test/output/smoke_test/val117161_{deseq2,edger,limma_voom}/DEG_*.csv
  RNA-seq  ref  : data/_validation/ref_GSE132520.csv , ref_GSE117161.csv  (limma DEG ground-truth)
  Prot     our  : test/output/smoke_test/motrpac_prot/DEG_results_8W_vs_SED.csv  (limma)
  Prot     ref  : data/_validation/motrpac/PROT_DA_trained_vs_SED.csv  (MoTrPAC limma DEA)

Outputs:
  output/deliverables/master_concordance.csv
  output/deliverables/internal_consistency.csv
  output/deliverables/component_inventory.csv
  output/deliverables/plots/<study>_<method>.png   (our logFC vs ref logFC; ref-sig highlighted)

The concordance formulas are copied verbatim from test/validation/validate_gse117161.py /
validate_gse132520.py / validate_motrpac_prot.py so the numbers reproduce the validated results.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/reports/gen_deliverables_report.py
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)

OUT = "output/deliverables"
PLOTS = os.path.join(OUT, "plots")
os.makedirs(PLOTS, exist_ok=True)


# ---------------------------------------------------------------- concordance core
def concord(our_deg, ref_df, *, lfc="logFC", padj="adj.P.Value"):
    """ref_df already filtered + collapsed + indexed by the join key (gene symbol / feature_ID).
    our_deg = path to our DEG CSV (index_col=0, cols log2FoldChange / padj)."""
    our = pd.read_csv(our_deg, index_col=0)
    our.index = our.index.astype(str)
    common = our.index.intersection(ref_df.index)
    j = pd.DataFrame({
        "our_lfc": our.loc[common, "log2FoldChange"], "our_padj": our.loc[common, "padj"],
        "ref_lfc": ref_df.loc[common, lfc], "ref_padj": ref_df.loc[common, padj],
    }).dropna(subset=["our_lfc", "ref_lfc"])

    pear = j["our_lfc"].corr(j["ref_lfc"])
    spear = j["our_lfc"].corr(j["ref_lfc"], method="spearman")
    nz = j[(j["our_lfc"] != 0) & (j["ref_lfc"] != 0)]
    sign = (np.sign(nz["our_lfc"]) == np.sign(nz["ref_lfc"])).mean()
    ref_sig = set(j.index[j["ref_padj"] < 0.05])
    our_sig = set(j.index[j["our_padj"] < 0.05])
    recov = sum(1 for g in ref_sig
                if g in our_sig and np.sign(j.at[g, "our_lfc"]) == np.sign(j.at[g, "ref_lfc"]))
    recov_frac = recov / len(ref_sig) if ref_sig else float("nan")
    sj = j.loc[[g for g in ref_sig if g in j.index]]
    pear_sig = sj["our_lfc"].corr(sj["ref_lfc"]) if len(sj) > 2 else float("nan")
    return {
        "n_common": len(j), "pearson": pear, "spearman": spear, "sign_pct": sign * 100,
        "ref_sig": len(ref_sig), "our_sig": len(our_sig),
        "recovery_pct": recov_frac * 100, "pearson_on_refsig": pear_sig,
        "_join": j, "_ref_sig": ref_sig,
    }


def scatter(tag, study, method, contrast, res):
    j = res["_join"]; ref_sig = res["_ref_sig"]
    sig_mask = j.index.isin(ref_sig)
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.scatter(j.loc[~sig_mask, "ref_lfc"], j.loc[~sig_mask, "our_lfc"],
               s=6, c="#c9ced6", alpha=0.45, linewidths=0, label=f"other (n={(~sig_mask).sum()})")
    ax.scatter(j.loc[sig_mask, "ref_lfc"], j.loc[sig_mask, "our_lfc"],
               s=12, c="#d6604d", alpha=0.75, linewidths=0,
               label=f"ref-significant (n={sig_mask.sum()})")
    lo = float(np.nanmin([j["ref_lfc"].min(), j["our_lfc"].min()]))
    hi = float(np.nanmax([j["ref_lfc"].max(), j["our_lfc"].max()]))
    ax.plot([lo, hi], [lo, hi], "--", c="#888", lw=1, label="y = x")
    ax.set_xlabel("reference logFC")
    ax.set_ylabel("our logFC")
    ax.set_title(f"{study}  |  {method}\n{contrast}", fontsize=10)
    ax.text(0.04, 0.96,
            f"Pearson r = {res['pearson']:.3f}\n"
            f"r on ref-sig = {res['pearson_on_refsig']:.3f}\n"
            f"sign agree = {res['sign_pct']:.0f}%\n"
            f"recovery = {res['recovery_pct']:.0f}%",
            transform=ax.transAxes, va="top", ha="left", fontsize=8.5,
            bbox=dict(boxstyle="round", fc="white", ec="#bbb", alpha=0.85))
    ax.legend(loc="lower right", fontsize=7.5, framealpha=0.85)
    ax.grid(True, ls=":", lw=0.5, alpha=0.5)
    fig.tight_layout()
    path = os.path.join(PLOTS, f"{tag}.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- reference loaders
def ref_gse132520():
    r = pd.read_csv("data/_validation/ref_GSE132520.csv")
    r = r.dropna(subset=["Gene_Symbol", "logFC"]).copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    return r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol", keep="first").set_index("Gene_Symbol")


def ref_gse117161():
    r = pd.read_csv("data/_validation/ref_GSE117161.csv")
    r = r[(r["Health_condition"].astype(str) == "Health(ZT14)") &
          (r["Exe_Intensity"].astype(str) == "High intensity")].copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    r = r.dropna(subset=["Gene_Symbol", "logFC"])
    return r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol", keep="first").set_index("Gene_Symbol")


def ref_motrpac():
    r = pd.read_csv("data/_validation/motrpac/PROT_DA_trained_vs_SED.csv")
    r = r[r["contrast"] == "M_8W - M_SED"].copy()
    r["feature_ID"] = r["feature_ID"].astype(str)
    return r.dropna(subset=["feature_ID", "logFC"]).drop_duplicates("feature_ID").set_index("feature_ID")


# ---------------------------------------------------------------- run
JOBS = [
    # tag, study, modality, matrix_type, method, contrast, our_deg, ref_loader, lfc, padj
    ("GSE132520_limma_WTonly", "GSE132520", "RNA-seq", "FPKM", "limma-trend",
     "WT exercised vs sedentary (4v4)",
     "test/output/smoke_test/val132520_WT_only/DEG_results_exercised_vs_sedentary.csv",
     ref_gse132520, "logFC", "adj.P.Value"),
    ("GSE132520_limma_pooled", "GSE132520", "RNA-seq", "FPKM", "limma-trend",
     "pooled exercised vs sedentary (8v8)",
     "test/output/smoke_test/val132520_pooled/DEG_results_exercised_vs_sedentary.csv",
     ref_gse132520, "logFC", "adj.P.Value"),
    ("GSE117161_deseq2", "GSE117161", "RNA-seq", "raw counts", "DESeq2",
     "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_deseq2/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "logFC", "adj.P.Value"),
    ("GSE117161_edger", "GSE117161", "RNA-seq", "raw counts", "edgeR",
     "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_edger/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "logFC", "adj.P.Value"),
    ("GSE117161_limmavoom", "GSE117161", "RNA-seq", "raw counts", "limma-voom",
     "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_limma_voom/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "logFC", "adj.P.Value"),
    ("WAT_prot_limma", "MoTrPAC-WAT", "proteomics", "norm. intensity", "limma",
     "Male 8wk-trained vs SED (6v6)",
     "test/output/smoke_test/motrpac_prot/DEG_results_8W_vs_SED.csv",
     ref_motrpac, "logFC", "adj.P.Val"),
]

rows = []
for tag, study, modality, mtype, method, contrast, our_deg, ref_loader, lfc, padj in JOBS:
    if not os.path.exists(our_deg):
        print(f"!! MISSING our DEG: {our_deg} — skipping {tag}")
        continue
    res = concord(our_deg, ref_loader(), lfc=lfc, padj=padj)
    png = scatter(tag, study, method, contrast, res)
    rows.append({
        "study": study, "modality": modality, "matrix_type": mtype, "method": method,
        "contrast": contrast, "n_common": res["n_common"],
        "pearson": round(res["pearson"], 3), "spearman": round(res["spearman"], 3),
        "sign_agree_pct": round(res["sign_pct"], 1),
        "ref_sig": res["ref_sig"], "our_sig": res["our_sig"],
        "recovery_pct": round(res["recovery_pct"], 1),
        "pearson_on_refsig": round(res["pearson_on_refsig"], 3),
        "plot": os.path.relpath(png, OUT).replace("\\", "/"),
    })
    print(f"[{tag}] n={res['n_common']} pearson={res['pearson']:.3f} "
          f"r_refsig={res['pearson_on_refsig']:.3f} sign={res['sign_pct']:.0f}% "
          f"recov={res['recovery_pct']:.0f}% refsig={res['ref_sig']} -> {png}")

master = pd.DataFrame(rows)
master.to_csv(os.path.join(OUT, "master_concordance.csv"), index=False)
print(f"\nwrote {OUT}/master_concordance.csv ({len(master)} rows)")

# -------------------------------------------------- internal consistency (GSE117161 3 methods)
ic_files = {
    "DESeq2": "test/output/smoke_test/val117161_deseq2/DEG_results_High_vs_Basal.csv",
    "edgeR": "test/output/smoke_test/val117161_edger/DEG_results_High_vs_Basal.csv",
    "limma-voom": "test/output/smoke_test/val117161_limma_voom/DEG_results_High_vs_Basal.csv",
}
L = {}
for name, p in ic_files.items():
    d = pd.read_csv(p, index_col=0); d.index = d.index.astype(str)
    L[name] = d["log2FoldChange"]
ic_rows = []
names = list(L)
for i in range(len(names)):
    for k in range(i + 1, len(names)):
        a, b = L[names[i]].align(L[names[k]], join="inner")
        r = a.corr(b)
        ic_rows.append({"method_a": names[i], "method_b": names[k],
                        "n_common": len(a), "pearson_logFC": round(r, 3)})
        print(f"[internal] {names[i]} vs {names[k]}: r={r:.3f} (n={len(a)})")
pd.DataFrame(ic_rows).to_csv(os.path.join(OUT, "internal_consistency.csv"), index=False)
print(f"wrote {OUT}/internal_consistency.csv ({len(ic_rows)} rows)")

# -------------------------------------------------- component inventory
INV = [
    ("1. Agent A keyword->13-CSV pipeline", "Phase 1: SEA-CDM 13-table schema + Sourced provenance + ID/FK convention",
     "tools/sea_cdm_schema.py", "13 tables; <field>+<field>_source columns; ontology *_name_id omitted", "shipped"),
    ("1. Agent A keyword->13-CSV pipeline", "Phase 2: grouped multi-table/multi-experiment extraction (3 flat LLM calls)",
     "tools/seacdm_tools.py::extract_tables_from_text", "deterministic ID/FK assignment; LLM never invents IDs", "shipped"),
    ("1. Agent A keyword->13-CSV pipeline", "Phase 3: deterministic cohort orchestrator + own-vs-cited GSE classifier",
     "tools/cohort_tools.py::run_agent_a_cohort", "PMCID fallback when no own-GSE; 13 shared CSVs", "shipped"),
    ("1. Agent A keyword->13-CSV pipeline", "Phase 4: demo cohort (Friday 2026-06-05 deliverable)",
     "output/agentA_cohort_demo/", "5 papers->4 text-extracted, 3 analyzed; 13 FK-linked CSVs", "shipped"),
    ("1. Agent A keyword->13-CSV pipeline", "2nd live keyword cohort (provenance verifier first real-LLM run)",
     "output/agentA_cohort_test2_exercise_rnaseq/", "3/3 text_ok; 322/358 source quotes verbatim-verified", "shipped"),
    ("2. DA method matrix", "edgeR (inmoose, pure-Python)",
     "tools/edger_tools.py::run_edger_analysis", "DESeq2-compatible columns; NB GLM QL F-test", "shipped"),
    ("2. DA method matrix", "limma-voom (R limma::voom via Rscript; inmoose has no voom)",
     "tools/limma_voom_tools.py + tools/limma_voom.R", "voom->lmFit->eBayes; DESeq2-compatible CSV", "shipped"),
    ("2. DA method matrix", "LLM 'auto' method picker + per-study relative reasoning",
     "tools/llm_helpers.py::choose_raw_da_method_with_llm", "fills analysis.da_method + da_method_reason in summary/papers.csv", "shipped"),
    ("3. Correctness validation", "RNA-seq limma-trend vs new_deg3 (FPKM path)",
     "test/validation/validate_gse132520.py", "logFC Pearson on ref-sig = 0.95 (GSE132520)", "validated"),
    ("3. Correctness validation", "RNA-seq raw-counts methods vs new_deg3",
     "test/validation/validate_gse117161.py", "DESeq2/edgeR/limma-voom r = 0.977/0.977/0.978 (GSE117161)", "validated"),
    ("3. Correctness validation", "Proteomics limma vs MoTrPAC ground-truth",
     "test/validation/validate_motrpac_prot.py", "logFC r=0.986 overall / 0.997 on ref-sig (M_8W vs SED)", "validated"),
    ("4. Proteomics pipeline", "identify -> download -> preprocess (matrix-in, limma DA)",
     "tools/proteomics_tools.py", "PRIDE labeled/label-free dispatch; concordance-validated", "shipped"),
    ("5. Bugs + anti-hallucination", "10 reproduce-verified bug fixes (6 validation, 1 demo-safety-check, 3 code-scan)",
     "test/validation/verify_bugfixes.py", "10/10 PASS (offline; Bug3 runs real DESeq2 on spaced-column study)", "verified"),
    ("5. Bugs + anti-hallucination", "Programmatic provenance verification + stitched-quote fragment check",
     "tools/seacdm_tools.py::verify_provenance", "non-verbatim quotes marked [UNVERIFIED]; faithful stitched quotes pass; test_provenance.py PASS", "shipped"),
    ("5. Bugs + anti-hallucination", "Structured-output JSON-string coercion (extraction crash guard)",
     "tools/seacdm_tools.py::_CoerceJSONContainer", "tolerates LLM serializing a list field/object as a JSON string", "shipped"),
    ("5. Bugs + anti-hallucination", "Live demo safety check (keys/fetch/extract/provenance/R/S2/artifacts)",
     "test/scripts/demo_safety_check.py", "8/8 PASS; caught the extraction-crash bug before Friday", "shipped"),
    # ---- 6. SEA-CDM meeting requirements (#1-#8), 2026-06 ----
    ("6. Meeting requirements (#1-#8)", "#1 raw-counts DA picker = deterministic rule (no per-study LLM)",
     "tools/llm_helpers.py::choose_raw_da_method_rule", "'auto'->DESeq2 rule, zero result change in common case; pure cost cut", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#2 single-cell RNA-seq via pseudobulk (sum raw counts per sample x cell-type)",
     "tools/scrna_tools.py::run_scrna_pseudobulk_da", "per-cell-type bulk DA+GSEA; REAL Kang2018 demo: CD14 Mono 3428 DEG, GSEA top=IFN (NES 2.61); paired-design fix", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#3 determinism: subject/sample/groups/assay from GEO metadata CSV (not LLM)",
     "tools/metadata_structural.py::build_structural_tables", "4 structural tables BYTE-IDENTICAL across runs; sample [2,7,7]->[70,70,70], groups [6,6,21]->[6,6,6]; field stability 68%->90%", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#4 extraction-input reduction: lean 1-call when GEO metadata present",
     "tools/seacdm_tools.py::_extract_lean", "3-call->1-call (full text sent once not 3x) when metadata supplies structural tables; measured savings in output/_extraction_profile/profile.json", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#5 result-from-text: mine the paper's reported findings (verbatim-checked)",
     "tools/seacdm_tools.py::build_reported_findings", "fills results for non-computable studies; verbatim rate tightened 47%->0-2% via snap", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#6 computed-vs-reported agreement annotation (gene-level verdicts)",
     "tools/agreement_tools.py::build_agreement_report", "confirmed/contradicted/not_detected per finding; gene-ID->symbol bridge 5%->100% on GSE279359", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#7 exercise->pathway->gene mechanism chain (GSEA leading-edge x paper genes)",
     "tools/pathway_chain_tools.py::build_pathway_chain", "REAL GSE208615: EMT (NES 1.48) -> BDNF; REAL scRNA Kang IFN leading-edge = ISGs (IFITM2/OASL/IRF7)", "shipped"),
    ("6. Meeting requirements (#1-#8)", "#8 split design column into one contrast per treatment level",
     "tools/batch_tools.py::_auto_detect_contrasts", "GSE242358->4, GSE279359->3 contrasts; each its own DEG+GSEA; SEA-CDM 1 experiment + durations as groups", "shipped"),
    ("6. Meeting requirements (#1-#8)", "v1 SEA-CDM stack registered into the interactive agent",
     "main.py + tools/cohort_tools.py::run_agent_a_cohort_tool", "run_agent_a_cohort + extract_sea_cdm_tables now agent-reachable tools (26 guarded tools)", "shipped"),
]
inv = pd.DataFrame(INV, columns=["component", "item", "file_path", "headline_result", "status"])
inv.to_csv(os.path.join(OUT, "component_inventory.csv"), index=False)
print(f"wrote {OUT}/component_inventory.csv ({len(inv)} rows)")

print("\n=== DONE ===")
