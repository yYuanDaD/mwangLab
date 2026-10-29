"""Gates 1-8 (paper_reconstruction .. threshold) for GSE153100 / PMID33257951."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json, re
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33257951"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC8087275.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC8087275.paper.md"
MATRIX_RAW = "data/GSE153100/GSE153100_counts.csv"
XLSX = "data/GSE153100/GSE153100_counts.xlsx"
META = "data/GSE153100/GSE153100_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE153100 for PMID 33257951 (Healthy Aging Interventions Reduce Repetitive Element "
             "Transcripts): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=["PMID33257951"])
case = run.case("PMID33257951", accession="GSE153100")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
xlsx_ev = case.add_input(XLSX, "matrix")
mat_ev = case.add_input(MATRIX_RAW, "matrix")

paper_threshold = {"metric": "FDR", "adjustment": "Benjamini-Hochberg (DESeq2 default padj)", "cutoff": 0.1,
                   "effect_metric": None, "effect_cutoff": None, "inclusive": False,
                   "source_locator": "FIG4"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID33257951 / PMC8087275 (bioRxiv 10.1101/2020.06.25.172023 preprint copy)",
    "accessions": ["GSE153100"],
    "accession_locator": "S3.1.p1 ('GSE153100 (human exercise)'); other GSEs are mouse re-analyses",
    "assay": "bulk total RNA-seq (Ribo-Zero), PBMC, NovaSeq 6000 SE150; STAR + TEtranscripts gene and RE counts",
    "sample_inclusion": ["young sedentary n=5 (2 m), older sedentary n=5 (2 m), older habitually exercising n=4 (1 m) (S3.3.p1)"],
    "sample_exclusion": ["not_reported"],
    "factors": [{"name": "group (age x exercise, 3 cells)", "levels": ["Y (young sedentary)", "O (older sedentary)",
                                                                  "OEX (older habitually exercising >=5 y)"],
                 "type": "between-subject, cross-sectional", "locator": "S3.3.p1"}],
    "primary_estimand": ("Associational: whether long-term habitual aerobic exercise in older adults is associated "
                         "with attenuation of age-related PBMC gene/RE expression changes; shown as O vs Y and "
                         "O-EX vs Y DESeq2 MA plots (FIG4A genes, FIG4B RE; S2.p6). Cross-sectional, not a "
                         "randomized intervention."),
    "planned_contrasts": [
        {"name": "O_vs_Y", "locator": "FIG4 (A,B); S2.p6", "role": "paper planned (aging reference)"},
        {"name": "OEX_vs_Y", "locator": "FIG4 (A,B); S2.p6", "role": "paper planned (exercise attenuation)"},
    ],
    "exploratory_contrasts": [
        {"name": "OEX_vs_O", "reason": "direct exercise-status comparison within older adults; implied by "
                                       "'changes largely attenuated in exercising older adults' (S2.p6) but no "
                                       "MA plot or count reported"}],
    "blocking_or_covariance": {"status": "not_required", "reason": "one sample per subject; groups matched by design (S3.3.p1); no covariates stated"},
    "matrix_scale": "raw gene + RE counts (STAR + TEtranscripts) (S3.2.p1; GEO data_processing)",
    "paper_method": "DESeq2 with size factors (S3.2.p1, S3.4.p1)",
    "paper_formula": "not_reported (presumably ~ group)",
    "paper_threshold": paper_threshold,
    "reported_counts": {
        "O_vs_Y_genes": "~2500 transcripts significantly increased/decreased with aging (FDR<0.1), 'largely reversed with exercise' (FIG4A legend); exact count and up/down not reported",
        "OEX_vs_Y_genes": "not_reported (described qualitatively as attenuated)",
        "RE": "'numerous' RE increased with aging (FDR<0.1) (FIG4B); counts not reported",
        "OEX_vs_O": "not_reported"},
    "other_analyses_not_reproduced": ["VO2max vs composite RE count correlation (FIG4C)", "WGCNA/GOrilla (mouse data only)"],
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "sample count", "paper": "S3.3.p1 says 'twelve healthy young and older adults' but lists 5+5+4=14",
     "data": "GEO has 14 samples (5 O, 4 T, 5 Y)", "classification": "executable_without_change",
     "note": "the group listing (14) matches GEO; 'twelve' is a text error"},
    {"item": "genome build", "paper": "Hg38 (S3.2.p1)", "data": "GEO data_processing: hg19",
     "classification": "executable_without_change"},
    {"item": "library kit", "paper": "Illumina Ribo-Zero total RNA (S3.3.p1)",
     "data": "GEO extract protocol mentions 'polyA RNA-seq' and TruSeq Ribo-Zero", "classification": "executable_without_change"},
    {"item": "gene identifiers", "paper": "-",
     "data": "deposited xlsx stores 28 gene symbols as Excel dates (MARCH1-11, MARC1/2, SEPT1-15, DEC1); MARCH1/MARC1 and MARCH2/MARC2 collide",
     "classification": "executable_without_change",
     "note": "rows restored to MARCHn/SEPTn/DEC1; the 2 colliding pairs kept as separate ambiguous rows"},
    {"item": "DE unit", "paper": "FIG4A genes and FIG4B RE shown separately; unclear whether one DESeq2 fit on the combined TEtranscripts table or separate fits",
     "data": "one combined gene+RE count table deposited", "classification": "executable_without_change",
     "note": "one DESeq2 fit on the combined table (TEtranscripts default); counts reported separately for genes and RE"},
    {"item": "threshold for OEX_vs_O", "paper": "not reported (no such plot)", "data": "-",
     "classification": "executable_without_change", "note": "paper FDR<0.1 rule applied to the exploratory contrast as well"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE153100"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": ["O_vs_Y", "OEX_vs_Y"], "exploratory_contrasts": ["OEX_vs_O"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "blocking": "not_required (one sample per subject)",
                   "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "FIG4"}, confidence="high",
            reasoning=("GSE153100 is the paper's own human exercise deposit (S3.1.p1). Cross-sectional PBMC study, "
                       "3 groups Y/O/OEX (S3.3.p1). Fig 4 shows DESeq2 O vs Y and OEX vs Y at FDR<0.1 for genes and RE; "
                       "the exercise claim is that age changes are attenuated in OEX. OEX vs O is the direct exercise "
                       "comparison but was not reported, so it is exploratory."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "title_groups": meta.title.str.split(",").str[0].value_counts().to_dict(),
       "sex_by_group": pd.crosstab(meta.title.str.split(",").str[0], meta["characteristics_ch1.0.Sex"]).to_dict(),
       "age_range_by_group": meta.groupby(meta.title.str.split(",").str[0])["characteristics_ch1.1.age"].agg(["min", "max"]).to_dict(),
       "data_processing": meta.data_processing.iloc[0]}
case.decide("ownership",
            final={"accession": "GSE153100", "matrix_file": XLSX, "matrix_file_converted": MATRIX_RAW,
                   "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, xlsx_ev, mat_ev, paper], paper={"locator": "S3.1.p1"}, confidence="high",
            reasoning=("series_id GSE153100 = the paper's human exercise accession; 14 PBMC samples: Y 5 (2 m, age 18-22), "
                       "O 5 (2 m, 62-74), T 4 (1 m) exactly as S3.3.p1; data_processing STAR + TEtranscripts raw gene "
                       "and RE counts. The only supplementary file is GSE153100_counts.xlsx (converted to CSV by the "
                       "download tool)."))

# ---------------------------------------------------------------- 3 alignment (with ID repair)
raw = pd.read_csv(MATRIX_RAW, index_col=0)
ids = raw.index.astype(str).tolist()
repair, seen = {}, {}
fixed = []
for i, g in enumerate(ids):
    m = re.match(r"^2020-(\d\d)-(\d\d) 00:00:00$", g)
    if m:
        mon, day = int(m.group(1)), int(m.group(2))
        base = {3: f"MARCH{day}", 9: f"SEPT{day}", 12: f"DEC{day}"}[mon]
        if mon == 3 and day in (1, 2) and ids.count(g) > 1:
            k = seen.get(g, 0); seen[g] = k + 1
            new = f"MARCH{day}_or_MARC{day}_row{k + 1}"
        else:
            new = base
        repair[f"row{i}:{g}"] = new
        fixed.append(new)
    else:
        fixed.append(g)
raw.index = fixed
raw.index.name = "feature"
assert not raw.index.duplicated().any()
fixed_dir = case.dir / "aligned"; fixed_dir.mkdir(parents=True, exist_ok=True)
fixed_csv = fixed_dir / "GSE153100_counts_idfixed.csv"
raw.to_csv(fixed_csv)
fixed_ev = case.add_output(fixed_csv, "matrix_id_repaired")
case.write_json("aligned/id_repair.json", {"n_repaired": len(repair), "mapping": repair}, role="id_repair")

aln = native.align_to_metadata(fixed_csv, META, case.dir / "aligned", key_column="description")
assert aln["coverage"] == 1.0, aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"sex": "characteristics_ch1.0.Sex", "age": "characteristics_ch1.1.age",
             "exstat": "characteristics_ch1.2.exercise status"},
    patterns={"grp": ("description", r"^([OTY])\d$")},
    recode={"grp": {"O": "O", "T": "OEX", "Y": "Y"}, "exstat": {"sedentary": "sed", "habitually exercising": "ex"}})
dm = pd.read_csv(derived["output"], index_col=0)
# consistency: title / exercise-status / age agree with grp
assert ((dm.grp == "OEX") == (dm.exstat == "ex")).all()
assert (dm.loc[dm.grp == "Y", "age"] <= 22).all() and (dm.loc[dm.grp != "Y", "age"] >= 62).all()
derived["levels"] = {c: dm[c].astype(str).value_counts().to_dict() for c in ["grp", "sex", "exstat"]}
design_meta = case.add_output(derived["output"], "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                   "derived_columns": derived["columns"], "levels": derived["levels"],
                   "feature_id_repair": {"n_rows": len(repair),
                                         "rule": "Excel-date row IDs 2020-03-dd -> MARCHdd, 2020-09-dd -> SEPTdd, 2020-12-01 -> DEC1; two MARCH/MARC collisions kept as separate rows"}},
            evidence=[fixed_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S3.3.p1"}, confidence="high",
            reasoning=("All 14 matrix columns (O1-5, T1-4, Y1-5) match GEO 'description' exactly; grp derived from the "
                       "label letter and cross-checked against exercise status and age. 28 feature IDs had been turned "
                       "into dates in the submitter's xlsx; they were renamed before alignment (no values changed)."))

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_short = {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                   "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
n_re = int(pd.Index(fixed).str.contains(":").sum())
prof_short["n_RE_features"] = n_re
prof_short["n_gene_features"] = len(fixed) - n_re
prof_short["library_sizes"] = raw.sum().astype(int).to_dict()
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "profile": prof_short,
                   "content": f"{len(fixed) - n_re} gene rows + {n_re} RE rows (name:family:class, TEtranscripts)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S3.2.p1"}, confidence="high",
            reasoning=("Integer fraction 1.0, min 0, max in the millions, library sizes 19.6-33.9 M; GEO says 'Raw gene "
                       "and repetitive element counts'; paper used DESeq2 on these counts. Raw counts -> DESeq2 matches "
                       "the paper route."))

# ---------------------------------------------------------------- 5 design
rep, suit_item, suit_summary = case.suitability(
    matrix_type="raw counts", metadata=dm, factors=["grp"], matrix_csv=aln["outputs"]["aligned_matrix"]["path"],
    organism="Human", subject=None, references={"grp": "Y"}, planned=["grp_O_vs_Y", "grp_OEX_vs_Y"])
print("suitability", json.dumps(suit_summary, default=str))
print(json.dumps([{k: c[k] for k in ("name", "factor", "test", "reference", "analyzable")} for c in rep["comparisons"]], indent=1))
print(json.dumps(rep["checks"].get("sex"), default=str)[:1500])
case.decide("design",
            final={"analysis_type": "multilevel (one factor, 3 levels, between-subject)", "formula": "~ grp",
                   "design_column": "grp",
                   "contrasts": [{"name": "O_vs_Y", "test": "O", "reference": "Y", "role": "paper_planned"},
                                 {"name": "OEX_vs_Y", "test": "OEX", "reference": "Y", "role": "paper_planned"},
                                 {"name": "OEX_vs_O", "test": "OEX", "reference": "O", "role": "exploratory"}],
                   "estimand_type": "associational",
                   "per_sex_exploratory": {"female": "same 3 contrasts on the 9 female samples (3 per group), one ~ grp model",
                                           "male": "not analyzable (2/2/1 per group)"},
                   "suitability": suit_summary},
            candidates=[
                {"value": "pairwise two-arm DESeq2 fits on 9-10 samples", "reason_rejected": "one model on all 14 samples, as one DESeq2 dataset in the paper; pooled dispersion"},
                {"value": "pool O and Y sedentary vs OEX", "reason_rejected": "mixes age with exercise; age is the larger effect"},
                {"value": "age as continuous covariate", "reason_rejected": "age is nested in the group structure (Y 18-22 vs older 62-74); not in the paper"},
                {"value": "VO2max regression (FIG4C)", "reason_rejected": "VO2max not deposited in GEO; composite-RE correlation, not DE"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "FIG4"}, confidence="high",
            reasoning=("Three independent groups of different people; exercise is habitual and self-selected, so all "
                       "contrasts are associational. Paper contrasts O vs Y and OEX vs Y (FIG4); OEX vs O added as the "
                       "direct exercise comparison (exploratory). All from one ~ grp model."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(derived["output"], "grp", ["sex", "age"])
dc = native.design_check(derived["output"], ["grp"])
dc_short = {k: dc[k] for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short}, role="covariance_reports")
assert dc["full_rank"] and dc["residual_df"] >= 4
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "sex", "disposition": "excluded: crossed with grp (M 2/5, 2/5, 1/4), groups matched by design and the paper did not adjust; male n too small to stratify"},
                                  {"name": "age", "disposition": "nested: defines Y vs older; within-older ages overlap (O 62-74, OEX 63-69)"},
                                  {"name": "subject", "disposition": "excluded: one sample per subject"}],
                   "design_check": dc_short, "confounding": conf},
            evidence=[design_meta, paper], paper={"locator": "S3.3.p1"}, confidence="high",
            reasoning=(f"Independent subjects; ~ grp is full rank ({dc['rank']}/{dc['n_columns']}), residual df "
                       f"{dc['residual_df']}. Sex is crossed with group and not modelled by the paper."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2, joint model on all 14 samples, Wald contrasts)",
                   "matrix_type": "raw counts", "formula": "~ grp",
                   "executor": "tools.joint_contrasts:run_joint_deseq2", "alpha_independent_filtering": 0.1,
                   "notes": "pydeseq2 rather than R DESeq2; one fit on the combined gene+RE table; no LFC shrinkage (paper did not mention it)"},
            evidence=[aligned_mat, paper], paper={"locator": "S3.4.p1"}, confidence="high",
            reasoning="Raw counts and the paper used DESeq2 with size factors; same route.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": dict(paper_threshold),
                   "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow-default comparison"}},
            evidence=[paper], paper={"locator": "FIG4"}, confidence="high",
            reasoning="FIG4 legend: significant at FDR<0.1 identified with DESeq2; no fold-change cutoff stated.")
print(json.dumps({"alignment": {k: aln[k] for k in ("method", "n_aligned", "coverage")},
                  "design_check": dc_short, "confounding": conf, "n_repair": len(repair)}, indent=1, default=str))
