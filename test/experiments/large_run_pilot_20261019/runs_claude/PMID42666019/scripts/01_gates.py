"""Gates 1-8 (paper_reconstruction .. threshold) for GSE326247 / PMID42666019."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42666019"
CASE = "PMID42666019"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13525339.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13525339.paper.md"
MATRIX = "data/GSE326247/GSE326247_COUNTs_all_Samples.csv"
MATRIX_XLSX = "data/GSE326247/GSE326247_COUNTs_all_Samples.xlsx"
FPKM = "data/GSE326247/GSE326247_FPKMs_all_Samples.csv"
META = "data/GSE326247/GSE326247_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE326247 for PMID 42666019 (Skeletal Muscle-Derived Extracellular Vesicles During Eccentric "
             "and Concentric Exercise Promote Muscle Regeneration After Injury): how exercise affects gene expression "
             "as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE326247")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")
xlsx_ev = case.add_input(MATRIX_XLSX, "matrix")
fpkm_ev = case.add_input(FPKM, "matrix")

LFC = 1.0
paper_threshold = {"metric": "padj", "adjustment": "not_reported (DESeq2 default BH)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": LFC,
                   "effect_cutoff_original": "|log2FoldChange| > 1", "inclusive": False,
                   "source_locator": "S2.16.p1 (also GEO data_processing)"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID42666019 / PMC13525339",
    "accessions": ["GSE326247"], "accession_locator": "S10.p1",
    "assay": "bulk poly(A) RNA-seq, Illumina PE (S2.16.p1); GEO: NovaSeq X Plus PE150, HISAT2 + StringTie2, mm10",
    "sample_inclusion": [
        "C2C12 myoblasts treated 24 h with mEVs isolated from TA muscle of SED, CE (uphill) or EE (downhill) "
        "trained mice (6 wk, S2.5.p1); N = 3 per group (S3.8.p1, FIG8 legend)"],
    "sample_exclusion": ["not_reported (none)"],
    "factors": [{"name": "grp (EV source)", "levels": ["SED", "CE", "EE"],
                 "type": "between-well, in vitro treatment; exercise acts through the EV donor muscle",
                 "locator": "S3.8.p1, S2.5.p1"}],
    "primary_estimand": ("Transcriptomic effect on C2C12 myoblasts of muscle-derived EVs from exercised mice "
                         "(concentric CE, eccentric EE) versus EVs from sedentary mice, and EE- versus CE-derived EVs. "
                         "Exercise is the treatment of the EV-donor mice; the sequenced cells were not exercised."),
    "planned_contrasts": [
        {"name": "grp_CE_vs_SED", "definition": "CE-mEV vs SED-mEV (volcano 'SED and CE', FIG8b left)", "locator": "FIG8"},
        {"name": "grp_EE_vs_CE", "definition": "EE-mEV vs CE-mEV (volcano 'CE and EE', FIG8b right)", "locator": "FIG8"}],
    "exploratory_contrasts": ["grp_EE_vs_SED (not shown in the paper)"],
    "direction_note": "FIG8c overlaps genes up in CE vs SED and up in EE vs CE ('sequential increase', S3.8.p1)",
    "blocking_or_covariance": {"status": "not_required", "note": "independent culture replicates; no batch/pairing reported"},
    "matrix_scale": "gene-level read counts from StringTie2 (GEO data_processing); FPKM/TPM also deposited",
    "paper_method": "DESeq2 (S2.16.p1; GEO: DESeq2 v1.38.3)",
    "paper_formula": "not_reported (vendor pairwise DESeq2 comparisons implied)",
    "paper_threshold": paper_threshold,
    "reported_counts": {"grp_CE_vs_SED": "not_reported (volcano only, FIG8b)",
                        "grp_EE_vs_CE": "not_reported (volcano only, FIG8b)",
                        "overlap_up": "nine fatty-acid-metabolism genes increase sequentially SED<CE<EE (S3.8.p1), incl. Prkag3, Cox7a1, Cox6a2, Cox8b"},
    "enrichment": {"method": "GO and KEGG enrichment of DEGs (S2.16.p1, FIG8a)", "locator": "S2.16.p1, FIG8"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "exercise estimand", "paper": "exercise effect is studied through EVs from exercised muscle",
     "data": "sequenced samples are C2C12 cells treated with EVs; no exercised tissue was sequenced",
     "classification": "executable_without_change",
     "note": "the contrasts answer 'effect of exercise-conditioned mEVs on myoblast expression', not a direct tissue exercise effect"},
    {"item": "treatment duration", "paper": "S2.6.p1: mEVs 20 ug/mL for 48 h before experiments",
     "data": "S3.8.p1 and GEO titles: 24 h treatment for RNA-seq", "classification": "executable_without_change",
     "note": "the RNA-seq samples are the 24 h treatment"},
    {"item": "matrix file", "paper": "not described",
     "data": "COUNT xlsx: 15,488 rows incl. one blank spreadsheet row (row 7147, no gene ID, no values); 15,487 genes, only 1 all-zero (deposited gene set appears pre-filtered)",
     "classification": "executable_without_change", "note": "blank row dropped as a parsing artifact before alignment"},
    {"item": "model", "paper": "DESeq2, pairwise comparisons implied by the volcanoes",
     "data": "3 groups x 3 replicates", "classification": "requires_explicit_deviation",
     "note": "one DESeq2 model ~ grp on all 9 samples (skill rule for one factor with several levels); dispersion pooled over 9 samples rather than refit per pair"},
    {"item": "gene identifiers", "paper": "gene symbols in figures", "data": "IDs carry a StringTie 'gene-' / 'rna-' prefix",
     "classification": "executable_without_change", "note": "prefix stripped only for enrichment input"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE326247"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "exploratory_contrasts": study_map["exploratory_contrasts"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.16.p1"}, confidence="high",
            reasoning=("GSE326247 is the paper's only deposit (S10.p1). RNA-seq = C2C12 treated 24 h with SED-, CE- or "
                       "EE-mEVs, n=3 (S3.8.p1, FIG8). FIG8b shows DEGs for SED vs CE and CE vs EE; up-regulated sets are "
                       "overlapped (FIG8c), so tests are CE vs SED and EE vs CE. DESeq2 with |log2FC|>1 and adjusted "
                       "p<0.05 (S2.16.p1). No DEG counts are given in the text."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "treatment_counts": meta["characteristics_ch1.1.treatment"].value_counts().to_dict(),
       "organism": meta.organism_ch1.unique().tolist(), "cell": meta.source_name_ch1.unique().tolist(),
       "titles": meta.title.tolist(), "data_processing": meta.data_processing.iloc[0]}
case.decide("ownership",
            final={"accession": "GSE326247", "matrix_file": MATRIX, "metadata_file": META, "owned": True,
                   "checks": own, "source_file": MATRIX_XLSX + " (converted to CSV by download_supplementary_files)"},
            evidence=[meta_ev, mat_ev, xlsx_ev, paper], paper={"locator": "S10.p1"}, confidence="high",
            reasoning=("Series GSE326247 = paper accession; 9 C2C12 samples treated 24 h with SED/CE/EE-mEVs, 3 each, "
                       "matching S3.8.p1/FIG8 (N=3). GEO processing names DESeq2 with |log2FC|>1, padj<0.05, as S2.16.p1."))

# ---------------------------------------------------------------- 3 alignment
clean = case.dir / "aligned" / "counts_no_blank_row.csv"
clean.parent.mkdir(parents=True, exist_ok=True)
raw = pd.read_csv(MATRIX, index_col=0)
blank = raw.index.isna() & raw.isna().all(axis=1)
assert blank.sum() == 1 and not raw.loc[~blank].isna().any().any()
raw.loc[~blank].to_csv(clean)
clean_ev = case.add_output(clean, "counts_without_blank_spreadsheet_row")

k1 = case.dir / "aligned" / "metadata_lib.csv"
d1 = native.derive_columns(META, k1, patterns={"lib": ("description", r"^Library name: (\w+)$")})
k2 = case.dir / "aligned" / "metadata_keyed.csv"
libs = pd.read_csv(k1, index_col=0)["lib"].tolist()
d2 = native.derive_columns(k1, k2, aliases={"mcol": "lib"}, recode={"mcol": {l: f"{l}.COUNT" for l in libs}})
aln = native.align_to_metadata(str(clean), str(k2), case.dir / "aligned", key_column="mcol")
assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"grp": "characteristics_ch1.1.treatment"},
    recode={"grp": {"SED-mEVs": "SED", "CE-mEVs": "CE", "EE-mEVs": "EE"}})
dm = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
consistent = bool((dm["lib"].str.replace(r"\d+$", "", regex=True) == dm["grp"]).all())
assert consistent
DESIGN = str(case.dir / "aligned" / "design_metadata.csv")
ALIGNED = aln["outputs"]["aligned_matrix"]["path"]
al_mat = case.add_output(ALIGNED, "aligned_matrix")
al_meta = case.add_output(DESIGN, "design_metadata")
al_map = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.decide("alignment",
            final={"method": aln["method"] + " (metadata description 'Library name: X' -> matrix column 'X.COUNT')",
                   "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                   "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "derived_key": {"lib": d1["columns"], "mcol": d2["columns"]},
                   "derived_columns": derived["columns"], "levels": derived["levels"],
                   "label_consistency_lib_vs_treatment": consistent,
                   "parse_fix": "dropped one blank spreadsheet row (no gene ID, all values missing) from the COUNT file"},
            evidence=[mat_ev, meta_ev, clean_ev, al_mat, al_meta, al_map], confidence="high",
            reasoning=("Matrix columns SED1.COUNT..EE3.COUNT match GEO 'Library name' SED1..EE3 one-to-one (exact, via "
                       "an explicit recode). Library prefix agrees with characteristics treatment for all 9 samples. "
                       "Coverage 9/9."))

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(ALIGNED)
fp = native.profile_matrix(FPKM)
prof_ev = case.write_json("matrix_profile.json", {"counts": prof, "fpkm": fp}, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "profile": {k: prof[k] for k in ("n_features", "n_samples", "integer_fraction", "min", "max",
                                                    "median", "missing_values", "negative_values", "duplicated_feature_ids")},
                   "library_sizes": pd.read_csv(ALIGNED, index_col=0).sum().astype(int).to_dict(),
                   "alternative_file": "FPKM matrix (linear, non-integer) not used",
                   "paper_input": "DESeq2 on counts (S2.16.p1)"},
            evidence=[al_mat, prof_ev, meta_ev, fpkm_ev], paper={"locator": "S2.16.p1"}, confidence="high",
            reasoning=("File named COUNT, 100% integers, 0..748513, library sizes 31-42 M, no negatives or missing "
                       "values after the blank row; GEO: HISAT2/StringTie2 quantification with DESeq2 downstream; the "
                       "companion FPKM file is separate. Raw read counts match the paper's DESeq2 input."))

# ---------------------------------------------------------------- 5 design
rep, sitem, ssum = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"], matrix_csv=ALIGNED,
                                    organism="Mouse", subject=None, references={"grp": "SED"},
                                    planned=["grp_CE_vs_SED", "grp_EE_vs_CE"])
comps = rep["comparisons"]
names = [c["name"] for c in comps]
print("suitability:", rep["verdict"], names, rep["warnings"])
assert "grp_CE_vs_SED" in names and "grp_EE_vs_CE" in names, names
case.write_json("comparisons.json", comps, role="comparisons")
case.decide("design",
            final={"analysis_type": "multilevel (one factor, three levels, one model)", "formula": "~ grp",
                   "design_column": "grp", "reference": "SED",
                   "contrasts": [{"name": "grp_CE_vs_SED", "test": "CE", "reference": "SED", "role": "planned"},
                                 {"name": "grp_EE_vs_CE", "test": "EE", "reference": "CE", "role": "planned"},
                                 {"name": "grp_EE_vs_SED", "test": "EE", "reference": "SED", "role": "exploratory"}],
                   "estimand_type": "interventional (in vitro EV treatment; exercise acts on the EV donor mice)",
                   "suitability": ssum},
            evidence=[al_meta, sitem, paper], paper={"locator": "FIG8"}, confidence="high",
            candidates=[{"value": "pool CE+EE vs SED", "reason_rejected": "pools distinct exercise modalities"},
                        {"value": "three separate two-group DESeq2 fits", "reason_rejected":
                         "skill rule: one model on all samples for a k-level factor; kept as the paper's likely vendor route only"}],
            reasoning=("Single factor grp (SED/CE/EE), 3 replicates each. Planned contrasts follow FIG8b/c "
                       "(CE vs SED; EE vs CE, up = higher in the later group). EE vs SED is the remaining analyzable "
                       f"pair, exploratory. Suitability verdict {rep['verdict']}."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(dm, "grp", ["characteristics_ch1.0.cell line", "source_name_ch1",
                                             "instrument_model", "molecule_ch1"])
dchk = native.design_check(dm, ["grp"])
cov_ev = case.write_json("covariance_checks.json", {"confounding": conf, "design_check": dchk}, role="covariance_checks")
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "cell line / source / instrument / molecule", "disposition": "excluded: single level"},
                                  {"name": "batch / culture plate", "disposition": "excluded: not reported in paper or GEO"}],
                   "design_check": dchk},
            evidence=[al_meta, cov_ev], confidence="high",
            reasoning=("Independent C2C12 culture replicates, one sample per well; no subject, pairing or batch key in "
                       "paper or GEO. All annotation columns besides treatment have a single level. Design ~ grp is full "
                       "rank with 6 residual df."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2, joint model on all 9 samples, Wald tests per contrast)",
                   "matrix_type": "raw counts", "formula": "~ grp", "executor": "tools.joint_contrasts:run_joint_deseq2",
                   "alpha": 0.05,
                   "paper_route": {"method": "DESeq2 (R v1.38.3), pairwise group comparisons", "status": "reproduced_with_model_choice",
                                   "note": "same method and input; dispersion estimated from all 9 samples instead of per pair"}},
            evidence=[al_mat, prof_ev, paper], paper={"locator": "S2.16.p1"}, confidence="high",
            reasoning="Paper route is DESeq2 on raw counts and the deposited matrix supports it; pydeseq2 is the executor.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": dict(paper_threshold),
                   "multiplicity": "BH within each contrast (DESeq2 default)"},
            evidence=[paper], paper={"locator": "S2.16.p1"}, confidence="high",
            reasoning="Paper states DESeq2 with |log2FoldChange| > 1 and adjusted p < 0.05; applied unchanged to every contrast.")
print("gates 1-8 recorded")
