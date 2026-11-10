"""Gates 1-8 (paper_reconstruction .. threshold) for GSE267763 / PMID40577041.

Three cases, one per deposited matrix / tissue fraction, each analysed separately as in the paper:
  SM  whole red gastrocnemius tissue (primary exercise-training transcriptome; S3.3.p2, FIG2C)
  MT  RNase-purified isolated mitochondria from the same gastrocnemius (S3.6.p1, FIG4A)
  LV  left ventricle, subset of animals (S3.3.p1, FIG2A)
"""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40577041"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12204305.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12204305.paper.md"
META = "data/GSE267763/GSE267763_metadata.csv"
CASES = {
    "PMID40577041_SM": {"tissue": "SM", "matrix": "data/GSE267763/GSE267763_counts_matrix_SM.csv.gz",
                         "col_prefix": "SM_", "cpm_rule": ">1 CPM in all samples", "cpm_min": 1.0, "inclusive": False,
                         "cpm_locator": "S2.10.p1 ('> 1 CPM in all samples'); FIG2 legend '>= 1 CPM'",
                         "paper_n": "15 per group after 1 outlier per group excluded (S2.10.p1, FIG2C)",
                         "reported": {"FDR<0.05": "34 (30 up, 4 down) (S3.3.p2)", "FDR<0.2": "487 (347 up, 140 down) (S3.3.p2)"},
                         "locator": "S3.3.p2", "fig": "FIG2C"},
    "PMID40577041_MT": {"tissue": "MT", "matrix": "data/GSE267763/GSE267763_counts_matrix_MT.csv.gz",
                         "col_prefix": "Mt_", "cpm_rule": ">= 2 CPM in all samples", "cpm_min": 2.0, "inclusive": True,
                         "cpm_locator": "FIG4 legend (A) '>= 2 CPM in all samples'",
                         "paper_n": "15 per group (FIG4A)",
                         "reported": {"FDR<0.05": "0 (S3.6.p1, FIG4A)", "p<0.05": "365 (S3.6.p1)"},
                         "locator": "S3.6.p1", "fig": "FIG4"},
    "PMID40577041_LV": {"tissue": "LV", "matrix": "data/GSE267763/GSE267763_counts_matrix_LV.csv.gz",
                         "col_prefix": "LV_", "cpm_rule": ">1 CPM in all samples", "cpm_min": 1.0, "inclusive": False,
                         "cpm_locator": "S2.10.p1; FIG2 legend (A) '>= 1 CPM in all samples'",
                         "paper_n": "7 per group, subset of animals (S3.3.p1, FIG2A)",
                         "reported": {"FDR<0.05": "0 (S3.3.p1)", "p<0.01": "121 (S3.3.p1)", "p<0.05": "738 (S3.3.p1)"},
                         "locator": "S3.3.p1", "fig": "FIG2A"},
}

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE267763 for PMID 40577041 (Skeletal Muscle Mitochondria Contain Nuclear-Encoded RNA Species "
             "Prior to and Following Adaptation to Exercise Training in Rats): how exercise affects gene expression as "
             "the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=list(CASES))

paper_threshold = {"metric": "FDR", "adjustment": "not_reported (limma/Degust default BH; executor applies BH)",
                   "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False,
                   "source_locator": "S2.10.p1"}
meta_all = pd.read_csv(META, index_col=0)

for cid, cfg in CASES.items():
    t = cfg["tissue"]
    case = run.case(cid, accession="GSE267763")
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(META, "metadata")
    mat_ev = case.add_input(cfg["matrix"], "matrix")

    # ------------------------------------------------------------ 1 paper_reconstruction
    study_map = {
        "paper_id": "PMID40577041 / PMC12204305 (FASEB J 2025)",
        "accessions": ["GSE267763"], "accession_locator": "S11.p1",
        "other_accessions": {"GSE220557": "mitochondrial small-RNA (miRNA) libraries, separate series; not part of this request's accession (S11.p1)",
                             "GSE276306": "authors' prior mitoplast study, cited only for a side check (S2.11.p1)"},
        "assay": "bulk total RNA-seq, rRNA-depleted (Zymo-Seq RiboFree for SM/MT; TruSeq Ribo-Zero for LV), STAR + htseq-count on mRatBN7.2 / Ensembl 106 (S2.10.p1)",
        "this_case_fraction": {"SM": "whole red gastrocnemius tissue", "MT": "TOMM22-IP isolated, RNase-A/proteinase-K purified mitochondria from red gastrocnemius",
                               "LV": "left ventricle outer wall, subset of animals"}[t],
        "sample_inclusion": ["32 male Wistar Kyoto rats, randomised Sed (n=16) vs ExT (n=16) at 5 wk (S2.2.p1)",
                             "ExT: treadmill 5 d/wk for 4 wk, 60 min at 20 m/min in wk 2-4; Sed on stationary treadmill (S2.3.p1)",
                             "tissue collected 24 h after last session at 9 wk (S2.4.p1)",
                             f"this fraction: {cfg['paper_n']}"],
        "sample_exclusion": ["two libraries (1 animal per group) excluded as PCA outliers (S2.10.p1); GEO SM/MT deposits already hold 15+15"],
        "factors": [{"name": "grp", "levels": ["Sed", "ExT"], "type": "between-animal, randomised", "locator": "S2.2.p1"}],
        "primary_estimand": (f"Effect of 4-week moderate-intensity treadmill training (ExT) vs sedentary control (Sed) on "
                             f"gene expression in {t} ({'whole gastrocnemius' if t == 'SM' else 'isolated gastrocnemius mitochondria' if t == 'MT' else 'left ventricle'}), "
                             "24 h after the last bout; each tissue fraction analysed separately"),
        "planned_contrasts": [{"name": f"{t}_ExT_vs_Sed", "definition": "ExT vs Sed (positive log2FC = higher in ExT)", "locator": cfg["locator"]}],
        "blocking_or_covariance": {"status": "not_required", "note": "one library per animal per fraction; groups are different animals",
                                   "locator": "S2.2.p1"},
        "matrix_scale": "raw htseq-count gene counts (S2.10.p1; GEO data_processing)",
        "paper_method": "voom/limma in Degust v4.1.5 on library-size CPM (S2.10.p1)",
        "paper_gene_filter": f"{cfg['cpm_rule']} ({cfg['cpm_locator']})",
        "paper_formula": "not_reported (Degust two-group design, implied ~ group)",
        "paper_threshold": paper_threshold,
        "reported_counts": cfg["reported"],
        "enrichment": {"method": "clusterProfiler GSEA, Reactome (msigdbr 7.5.1), minGSSize 10, p<0.05 (S2.10.p1); reported for SM (FIG2D) and LV (FIG2B); none for MT",
                       "locator": "S2.10.p1"},
    }
    pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
    discrepancies = [
        {"item": "sample exclusion", "paper": "16+16 animals, 1 outlier library per group excluded (S2.10.p1)",
         "data": {"SM": "GEO deposit 15 Sed + 15 ExT", "MT": "GEO deposit 15 Sed + 15 ExT",
                  "LV": "GEO deposit 7 Sed + 7 ExT (paper: n=7 per group, subset)"}[t],
         "classification": "executable_without_change", "note": "outliers already removed before deposit; all deposited samples used"},
        {"item": "normalisation", "paper": "library-size CPM; Degust voom (TMM not mentioned)",
         "data": "repository voom executor uses lib.size = colSums (no TMM)",
         "classification": "executable_without_change", "note": "matches the stated library-size normalisation"},
        {"item": "software", "paper": "Degust v4.1.5 web front end to R limma/voom", "data": "R limma::voom via tools/limma_voom.R",
         "classification": "executable_without_change"},
        {"item": "library prep (LV)", "paper": "LV used TruSeq Ribo-Zero at Macrogen; SM/MT Zymo RiboFree", "data": "separate matrices",
         "classification": "executable_without_change", "note": "tissues are never compared to each other here"},
        {"item": "column naming", "paper": "-", "data": "MT matrix columns 'Mt_Sed_r04' vs GEO titles 'MT_Sed_r04'; MT index header misspelled 'Enemble_ID'",
         "classification": "executable_without_change", "note": "case-only prefix difference handled with a derived key column"},
        {"item": "enrichment library", "paper": "Reactome GSEA (clusterProfiler)", "data": "repository GSEA: MSigDB Hallmark only (mouse sets for rat)",
         "classification": "requires_explicit_deviation"},
    ]
    case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
    case.decide("paper_reconstruction",
                final={"accessions": ["GSE267763"], "primary_estimand": study_map["primary_estimand"],
                       "planned_contrasts": [f"{t}_ExT_vs_Sed"], "paper_threshold": paper_threshold,
                       "paper_method": study_map["paper_method"], "paper_gene_filter": study_map["paper_gene_filter"],
                       "matrix_scale": study_map["matrix_scale"], "reported_counts": cfg["reported"],
                       "fraction": t},
                evidence=[paper, pr_ev], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning=("GSE267763 is the paper's whole-transcriptome deposit (S11.p1); miRNAs are in GSE220557 and are "
                           "out of scope. Randomised two-group design Sed vs ExT (S2.2.p1). Each tissue fraction has its own "
                           f"filter and voom/limma model (S2.10.p1, {cfg['fig']}); FDR<0.05 defines DE (S2.10.p1)."))

    # ------------------------------------------------------------ 2 ownership
    sub = meta_all[meta_all.title.str.startswith(f"{t}_")].copy()
    mat_cols = [c for c in pd.read_csv(cfg["matrix"], index_col=0, nrows=2).columns if c.startswith(cfg["col_prefix"])]
    own = {"series_id": sorted(sub.series_id.astype(str).unique().tolist()), "n_samples_this_fraction": int(len(sub)),
           "n_matrix_sample_columns": len(mat_cols),
           "groups": sub["characteristics_ch1.5.treatment"].value_counts().to_dict(),
           "source": sub.source_name_ch1.unique().tolist(), "strain_sex_age": sub[["characteristics_ch1.1.strain",
           "characteristics_ch1.2.Sex", "characteristics_ch1.4.age (weeks)"]].astype(str).drop_duplicates().values.tolist(),
           "data_processing": sub.data_processing.iloc[0]}
    case.decide("ownership",
                final={"accession": "GSE267763", "matrix_file": cfg["matrix"], "metadata_file": META, "owned": True,
                       "checks": own},
                evidence=[meta_ev, mat_ev, paper], paper={"locator": "S11.p1"}, confidence="high",
                reasoning=(f"Series GSE267763 = paper accession; {len(sub)} {t} samples of male Wistar Kyoto rats, 9 wk, "
                           "Sed/ExT, STAR + HTseq on mRatBN7.2 v106, matching S2.2-S2.10. Matrix holds the same number of "
                           "sample columns."))

    # ------------------------------------------------------------ 3 alignment
    adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
    sub["mkey"] = sub.title.str.replace(r"^MT_", "Mt_", regex=True)
    sub_path = adir / "metadata_subset.csv"
    sub.to_csv(sub_path)
    case.add_output(sub_path, "metadata_subset")
    aln = native.align_to_metadata(cfg["matrix"], str(sub_path), adir, key_column="mkey")
    assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
        patterns={"grp": ("title", r"^(?:SM|MT|LV)_(Sed|ExT)_r\d+$"), "animal": ("title", r"_r(\d+)$"),
                  "grp_c": ("characteristics_ch1.5.treatment", r"\((Sed|ExT)\)$")})
    dm = pd.read_csv(derived["output"], index_col=0)
    assert (dm.grp == dm.grp_c).all()
    dm["animal"] = "r" + dm["animal"].astype(str).str.zfill(2)
    dm.to_csv(derived["output"])
    assert dm.animal.is_unique
    derived["levels"] = {"grp": dm.grp.value_counts().to_dict()}
    design_meta = case.add_output(derived["output"], "design_metadata")
    aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
    case.decide("alignment",
                final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                       "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                       "annotation_columns_dropped": aln["annotation_columns_dropped"],
                       "key_derivation": ("metadata subset to this fraction (title prefix); mkey = title with 'MT_' -> 'Mt_' "
                                          "(MT matrix uses 'Mt_' prefix); exact match on mkey"),
                       "derived_columns": {"grp": "title regex (Sed|ExT), checked equal to characteristics treatment",
                                           "animal": "title rNN (unique within fraction)"},
                       "levels": derived["levels"]},
                evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.2.p1"}, confidence="high",
                reasoning=(f"{aln['n_aligned']}/{aln['n_metadata']} exact on the GEO title key; annotation columns "
                           f"{aln['annotation_columns_dropped']} dropped; grp from title agrees with the treatment field for every sample."))

    # ------------------------------------------------------------ 4 matrix
    am_path = aln["outputs"]["aligned_matrix"]["path"]
    prof = native.profile_matrix(am_path)
    prof_short = {k: prof.get(k) for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                           "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
    am = pd.read_csv(am_path, index_col=0)
    lib = am.sum()
    prof_short["library_sizes_millions"] = [round(float(lib.min()) / 1e6, 2), round(float(lib.max()) / 1e6, 2)]
    cpm = am / lib * 1e6
    prof_short["n_genes_passing_paper_filter"] = int(((cpm >= cfg["cpm_min"]) if cfg["inclusive"] else (cpm > cfg["cpm_min"])).all(axis=1).sum())
    prof_short["feature_ids"] = native.feature_id_report(am_path)
    case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
    case.decide("matrix",
                final={"matrix_type": "raw counts", "recommended_method": "limma-voom (paper route); DESeq2/edgeR also valid",
                       "profile": prof_short, "provenance": "HTseq-count v2.0.5 gene counts, STAR 2-pass (GEO data_processing; S2.10.p1)"},
                evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning=(f"Non-negative integers (integer fraction {prof.get('integer_fraction')}), max {prof.get('max')}, "
                           f"library sizes {prof_short['library_sizes_millions']} M; GEO states raw HTseq counts. "
                           f"Paper filter ({cfg['cpm_rule']}) keeps {prof_short['n_genes_passing_paper_filter']} genes."))

    # ------------------------------------------------------------ 5 design
    planned_name = "grp_ExT_vs_Sed"
    rep, suit_item, suit_summary = case.suitability(
        matrix_type="raw counts", metadata=dm, factors=["grp"], matrix_csv=am_path, organism="Rat",
        subject=None, references={"grp": "Sed"}, planned=[planned_name])
    names = [c["name"] for c in rep["comparisons"]]
    print(cid, "suitability", json.dumps(suit_summary, default=str), names)
    assert planned_name in names, names
    case.decide("design",
                final={"analysis_type": "two-group between-animal (randomised)", "design_column": "grp",
                       "formula": "~ grp", "control": "Sed", "treatment": "ExT",
                       "contrasts": [{"name": f"{t}_ExT_vs_Sed", "suitability_name": planned_name, "role": "paper_planned"}],
                       "estimand_type": "interventional (randomised allocation, S2.2.p1)",
                       "suitability": suit_summary},
                candidates=[{"value": "pool SM, MT and LV in one model", "reason_rejected": "paper analyses each fraction separately with its own filter; different library kits for LV"},
                            {"value": "SM vs MT (mitochondrial localisation)", "reason_rejected": "not an exercise effect; the request asks how exercise affects expression"}],
                evidence=[design_meta, suit_item, paper], paper={"locator": "S2.2.p1"}, confidence="high",
                reasoning=f"Single randomised factor, Sed reference; {derived['levels']['grp']} samples; one planned contrast per fraction.")

    # ------------------------------------------------------------ 6 covariance
    cand = ["characteristics_ch1.1.strain", "characteristics_ch1.2.Sex", "characteristics_ch1.4.age (weeks)", "animal"]
    conf = native.confounding_report(derived["output"], "grp", cand)
    dc = native.design_check(derived["output"], ["grp"])
    dc_short = {k: dc.get(k) for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
    case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short}, role="covariance_reports")
    assert dc["full_rank"]
    case.decide("covariance",
                final={"status": "not_required", "blocking_terms": [],
                       "covariates": [{"name": "animal", "disposition": "nested: one library per animal within this fraction; groups are different animals, so no blocking"},
                                      {"name": "strain/sex/age", "disposition": "excluded: single level (Wistar Kyoto, male, 9 wk)"},
                                      {"name": "batch/lane", "disposition": "excluded: not reported in paper or GEO"}],
                       "design_check": dc_short},
                evidence=[design_meta, paper], paper={"locator": "S2.2.p1"}, confidence="high",
                reasoning=(f"~ grp full rank, residual df {dc.get('residual_df')}. SM and MT come from the same animals, but "
                           "they are analysed as separate cases, so no within-animal correlation enters any model."))

    # ------------------------------------------------------------ 7 method
    case.decide("method",
                final={"method": "limma-voom (R limma::voom + lmFit + eBayes, two-group ~ grp)", "matrix_type": "raw counts",
                       "executor": "tools.limma_voom_tools:run_limma_voom_analysis",
                       "filter": f"{cfg['cpm_rule']} on library-size CPM, applied before voom ({cfg['cpm_locator']})",
                       "normalisation": "library size (colSums of filtered counts), no TMM - paper states library-size CPM",
                       "paper_route": {"method": "voom/limma (Degust v4.1.5)", "status": "reproduced"}},
                evidence=[aligned_mat, paper], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning="Raw integer counts and a two-group design: the paper's voom/limma route runs as-is via R limma.")

    # ------------------------------------------------------------ 8 threshold
    audits = [{"metric": "pvalue", "cutoff": 0.05, "label": "audit: paper exploratory rule (S3.3.p1, S3.6.p1)"}]
    if t == "SM":
        audits.append({"metric": "padj", "cutoff": 0.2, "label": "audit: paper discovery rule FDR<0.2 (S3.3.p2)"})
    if t == "LV":
        audits.append({"metric": "pvalue", "cutoff": 0.01, "label": "audit: paper exploratory rule p<0.01 (S3.3.p1)"})
    case.decide("threshold",
                final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                       "applied_threshold": dict(paper_threshold), "audit_thresholds": audits},
                evidence=[paper], paper={"locator": "S2.10.p1"}, confidence="high",
                reasoning="S2.10.p1: genes with FDR < 0.05 were considered DE; no fold-change cutoff. Raw-p rules the paper reports are audits only.")
    print(cid, json.dumps({"aln": aln["n_aligned"], "filter_genes": prof_short["n_genes_passing_paper_filter"],
                           "lib": prof_short["library_sizes_millions"], "df": dc.get("residual_df")}, default=str))
