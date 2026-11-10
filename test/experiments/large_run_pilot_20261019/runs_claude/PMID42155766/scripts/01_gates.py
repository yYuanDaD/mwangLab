"""Gates 1-8 (paper_reconstruction .. threshold) for PMID42155766 / GSE304653.
Two cases, one per sorted fraction, as the paper analyses them separately (S3.p2, S3.p4)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native
from common import RUN, PAPER_JSON, PAPER_MD, ACC, MATRIX, METADATA, PAPER_THRESHOLD, CASES, COMPARISON, REQUEST

native.enable_native_mode()
run = native.RunRecorder(RUN, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session", case_ids=list(CASES))

study_map = {
    "paper_id": "PMID42155766 / PMC13319373 (J Sport Health Sci 2026, 101146)",
    "accessions": {ACC: "bulk RNA-seq of flow-sorted Met1-iRFP tumour fractions (S8.p1, S2.4.p1)"},
    "assay": ("Met1-iRFP orthotopic tumours digested, sorted into iRFP+ (cancer) and iRFP- (TME); KAPA stranded mRNA; "
              "HiSeq 2x50; STAR mm10 + featureCounts gencode vM18 (S2.4.p1)"),
    "sample_inclusion": ["female FVB mice, Met1-iRFP grafted; voluntary wheel running vs sedentary (no wheel) from day 3 "
                         "for ~15 days (S2.1.2.p1, S2.2.p1)",
                         "TME RNA-seq: exercise n=4, control n=4 (FIG2C)",
                         "cancer-cell RNA-seq: exercise n=7, control n=8, 'from the same tumors' (S3.p4, FIG3B)"],
    "sample_exclusion": ["missed fat-pad injection, ulceration, or injury that prohibited exercise (S2.1.p1); "
                         "not identifiable at the sample level"],
    "factors": [{"name": "treatment", "levels": ["sedentary control", "voluntary wheel running"], "type": "between-mouse",
                 "locator": "S2.1.2.p1"},
                {"name": "fraction", "levels": ["iRFP- TME", "iRFP+ cancer"], "type": "analysis stratum (separate analyses)",
                 "locator": "S2.4.p1; S3.p2; S3.p4"}],
    "primary_estimand": ("Effect of voluntary wheel running vs sedentary control on gene expression of (a) the iRFP- "
                         "tumour-microenvironment fraction and (b) the iRFP+ cancer-cell fraction of Met1 tumours, "
                         "each fraction analysed separately."),
    "planned_contrasts": [{"name": f"TME: {COMPARISON}", "definition": "exercise vs control, iRFP- cells", "locator": "S3.p2; FIG2C"},
                          {"name": f"Cancer: {COMPARISON}", "definition": "exercise vs control, iRFP+ cells", "locator": "S3.p4; FIG3B"}],
    "repeated_measure_unit": "mouse; one sample per mouse per fraction; fractions from the same tumours are analysed separately",
    "normalization": "DESeq2 size factors (S2.4.p1)",
    "paper_method": "DESeq2 (Bioconductor) on featureCounts gene counts (S2.4.p1); design formula and prefilter not reported",
    "paper_threshold": PAPER_THRESHOLD,
    "reported_counts": {k: v["reported"] for k, v in CASES.items()},
    "enrichment": {"TME": "GSEA Hallmark (mouse) on all genes ranked by log2FC via genekitr; BH p_adj < 0.05 (S2.4.p1, FIG2B)",
                   "Cancer": "Reactome ORA on up/down DEGs; IPA functions (S2.4.p1, S3.p4, FIG3D)"},
}

meta_full = pd.read_csv(METADATA, index_col=0)
for case_id, cfg in CASES.items():
    case = run.case(case_id, accession=ACC)
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(METADATA, "metadata")
    mat_ev = case.add_input(MATRIX, "matrix")

    # ------------------------------------------------------------ 1 paper_reconstruction
    pr_ev = case.write_json("paper_reconstruction.json", {**study_map, "this_case": case_id,
                                                          "reported_for_this_case": cfg["reported"]},
                            role="paper_reconstruction")
    disc = [
        {"item": "DESeq2 design and prefilter", "paper": "not reported beyond 'normalized and analyzed ... using DESeq2' (S2.4.p1)",
         "data": "two groups per fraction, one sample per mouse", "classification": "executable_without_change",
         "note": "~ grp per fraction; zero-count genes dropped; DESeq2 independent filtering and Cook's handling as in pydeseq2"},
        {"item": "independent-filtering alpha", "paper": "R DESeq2 results() default alpha = 0.1 matches the paper's p_adj < 0.1 cut",
         "data": "repository executor uses pydeseq2 DeseqStats default alpha = 0.05 (not exposed)",
         "classification": "executable_without_change", "note": "may shift borderline calls near padj 0.1"},
        {"item": "GEO title typo", "paper": "-", "data": "titles read 'Sendentary'; characteristics treatment = 'Sedentary'",
         "classification": "executable_without_change", "note": "group taken from characteristics_ch1.3.treatment"},
        {"item": "sample sizes", "paper": f"{cfg['reported']['locator']}: exercise n={cfg['n']['ex']}, control n={cfg['n']['sed']}",
         "data": "GEO deposit has the same numbers", "classification": "executable_without_change"},
    ]
    case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
    case.decide("paper_reconstruction",
                final={"accessions": [ACC], "primary_estimand": study_map["primary_estimand"],
                       "planned_contrasts": [COMPARISON], "case_fraction": cfg["celltype"],
                       "paper_threshold": PAPER_THRESHOLD, "paper_method": study_map["paper_method"],
                       "paper_formula": "not_reported", "reported_counts": cfg["reported"]},
                evidence=[paper, pr_ev], paper={"locator": "S2.4.p1"}, confidence="high",
                reasoning=("GSE304653 is the paper's only RNA-seq deposit (S8.p1). Sorted iRFP- (TME) and iRFP+ (cancer) "
                           "fractions of Met1 tumours from wheel-running vs sedentary mice, each analysed with DESeq2; "
                           f"DEGs at p_adj < 0.1 (S3.p2, S3.p4). This case: {cfg['celltype']}, reported {cfg['reported']['n_deg']} DEGs."))

    # ------------------------------------------------------------ 2 ownership
    sub = meta_full[meta_full["characteristics_ch1.1.cell type"] == cfg["celltype"]]
    tab = sub["characteristics_ch1.3.treatment"].value_counts().to_dict()
    raw_cols = pd.read_csv(MATRIX, sep=None, engine="python", index_col=0, nrows=2).columns.tolist()
    own = {"series_id": sorted(meta_full.series_id.unique().tolist()), "n_samples_series": int(len(meta_full)),
           "n_samples_fraction": int(len(sub)), "treatment_counts": tab,
           "strain": meta_full["characteristics_ch1.2.strain"].unique().tolist(),
           "organism": meta_full.organism_ch1.unique().tolist(),
           "data_processing": str(meta_full.data_processing.iloc[0])[:300], "matrix_columns": raw_cols}
    assert tab == {"Sedentary": cfg["n"]["sed"], "Exercise": cfg["n"]["ex"]}, tab
    case.decide("ownership",
                final={"accession": ACC, "matrix_file": MATRIX, "metadata_file": METADATA, "owned": True, "checks": own},
                evidence=[meta_ev, mat_ev, paper], paper={"locator": "S8.p1"}, confidence="high",
                reasoning=(f"GSE304653 named in S8.p1; Met1-iRFP FVB samples, processing text matches S2.4.p1 (STAR/featureCounts); "
                           f"{cfg['celltype']} counts {tab} equal the paper's n ({cfg['reported']['locator']}). "
                           "CounTable is the series' only supplementary file; its 23 column names equal the GEO library names."))

    # ------------------------------------------------------------ 3 alignment
    adir = case.dir / "aligned"
    adir.mkdir(parents=True, exist_ok=True)
    keyed = native.derive_columns(METADATA, adir / "metadata_keyed.csv",
                                  patterns={"lib": ("description", r"^Library name: (\S+)$")})
    aln = native.align_to_metadata(MATRIX, adir / "metadata_keyed.csv", adir / "all23", key_column="lib")
    assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], adir / "all23" / "design_metadata_all.csv",
        aliases={"grp": "characteristics_ch1.3.treatment", "frac": "characteristics_ch1.1.cell type"},
        patterns={"mouse": ("title", r", (rep\d+)$")},
        recode={"grp": {"Sedentary": "sed", "Exercise": "ex"},
                "frac": {"TME cells (iRFP-)": "tme", "Cancer cells (iRFP+)": "cancer"}})
    dall = pd.read_csv(adir / "all23" / "design_metadata_all.csv", index_col=0)
    mall = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
    keep = dall.index[dall["frac"] == cfg["frac"]]
    dsub = dall.loc[keep]
    dsub.to_csv(adir / "design_metadata.csv")
    mall[keep].to_csv(adir / "aligned_matrix.csv")
    aligned_ev = case.add_output(adir / "aligned_matrix.csv", "aligned_matrix")
    dmeta_ev = case.add_output(adir / "design_metadata.csv", "design_metadata")
    case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    case.decide("alignment",
                final={"method": aln["method"] + " on 'lib' (library name parsed from GEO description)",
                       "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                       "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                       "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                       "key_derivation": keyed, "derived_columns": derived,
                       "case_subset": {"rule": f"frac == '{cfg['frac']}'", "samples": keep.tolist(),
                                       "grp_counts": dsub["grp"].value_counts().to_dict()}},
                evidence=[mat_ev, meta_ev, aligned_ev, dmeta_ev], paper={"locator": "S2.4.p1"}, confidence="high",
                reasoning=("Matrix columns (CN*/CR*/SN*/SR*) equal GEO 'Library name' values exactly; 23/23 matched, none by "
                           f"position. Subset to the {cfg['celltype']} fraction by metadata cell type. Derived grp (sed/ex), "
                           "frac, mouse (repN)."))

    # ------------------------------------------------------------ 4 matrix
    am = adir / "aligned_matrix.csv"
    prof = native.profile_matrix(am)
    fid = native.feature_id_report(am)
    case.decide("matrix",
                final={"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": prof, "feature_ids": fid,
                       "paper_input": "featureCounts gene counts, gencode vM18 (S2.4.p1)"},
                evidence=[aligned_ev, mat_ev, paper], paper={"locator": "S2.4.p1"}, confidence="high",
                reasoning=("All-integer, non-negative gene counts with gene-symbol rows; GEO data_processing and S2.4.p1 state "
                           "featureCounts per gene, which DESeq2 then normalised. Raw counts."))

    # ------------------------------------------------------------ 5 design
    rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=dsub, factors=["grp"], matrix_csv=str(am),
                                              organism="Mouse", subject=None, references={"grp": "sed"},
                                              planned=[COMPARISON])
    names = [c["name"] for c in rep["comparisons"]]
    assert COMPARISON in names, names
    dc = native.design_check(dsub, ["grp"])
    case.decide("design",
                final={"analysis_type": "two_group", "design_column": "grp", "control": "sed", "treatment": "ex",
                       "formula": "~ grp", "contrasts": [{"name": COMPARISON}], "estimand_type": "causal (randomised)",
                       "suitability": s_summary, "design_check": dc,
                       "comparisons": [{k: c.get(k) for k in ("name", "cells", "analyzable")} for c in rep["comparisons"]]},
                evidence=[dmeta_ev, s_item, paper], paper={"locator": cfg["reported"]["locator"].split(";")[0]},
                confidence="high",
                candidates=[{"value": "one model on both fractions ~ frac * grp", "reason_rejected": "paper analyses fractions separately; cell types differ completely in expression and dispersion"},
                            {"value": "paired by mouse across fractions", "reason_rejected": "only 4 TME samples share mouse reps with cancer samples; paper estimand is per fraction"}],
                reasoning=(f"Mice randomised to wheel running or sedentary (S2.1.2.p1); per fraction a two-group comparison "
                           f"exercise vs control. Suitability verdict {rep['verdict']}; full rank={dc['full_rank']}, residual df={dc['residual_df']}."))

    # ------------------------------------------------------------ 6 covariance
    conf = native.confounding_report(dsub, "grp", ["mouse"])
    covs = [{"name": "mouse", "disposition": "excluded: one sample per mouse in this fraction (no repeated measure)"},
            {"name": "sex", "disposition": "excluded: constant (all female, S2.1.2.p1)"},
            {"name": "strain", "disposition": "excluded: constant (FVB)"},
            {"name": "batch / lane", "disposition": "excluded: not recorded in GEO or paper"}]
    case.decide("covariance",
                final={"status": "not_required", "blocking_terms": [], "covariates": covs, "confounding": conf},
                evidence=[dmeta_ev, s_item, paper], paper={"locator": "S2.1.2.p1"}, confidence="high",
                reasoning="Independent mice, one library each within this fraction; no recorded batch; no covariate in paper.")

    # ------------------------------------------------------------ 7 method
    case.decide("method",
                final={"method": "DESeq2 (pydeseq2, Wald test)", "matrix_type": "raw counts", "formula": "~ grp",
                       "executor": "tools.deseq2_tools:run_deseq2_analysis",
                       "paper_method": "DESeq2 (executable)", "prefilter": "genes with zero counts in all samples of the fraction dropped (executor)"},
                evidence=[aligned_ev, paper], paper={"locator": "S2.4.p1"}, confidence="high",
                candidates=[{"value": "edgeR / limma-voom", "reason_rejected": "paper used DESeq2; counts available"},
                            {"value": "limma on log2(CPM+1)", "reason_rejected": "raw counts available; paper used DESeq2"}],
                reasoning="Paper's DESeq2 route is executable on the deposited featureCounts matrix.")

    # ------------------------------------------------------------ 8 threshold
    case.decide("threshold",
                final={"paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper", "applied_threshold": PAPER_THRESHOLD,
                       "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "label": "audit: workflow default padj<0.05"}],
                       "multiplicity": "BH within the contrast"},
                evidence=[paper], paper={"locator": "S3.p2"}, confidence="high",
                reasoning="Paper defines DEGs as BH p_adj < 0.1 with no fold-change cut (S3.p2, S3.p4, FIG3 legend).")
    print(case_id, "gates 1-8 recorded; suitability", rep["verdict"], s_summary.get("warnings"), json.dumps(s_summary, default=str)[:800])
