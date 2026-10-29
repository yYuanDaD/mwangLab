"""Gates 1-8 (paper_reconstruction .. threshold) for GSE328094 / PMID42363191."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native
from tools import suitability as su

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42363191"
CASE = "PMID42363191"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13591731.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13591731.paper.md"
MATRIX = "data/GSE328094/GSE328094_counts.txt.gz"
FPKM = "data/GSE328094/GSE328094_fpkm.txt.gz"
META = "data/GSE328094/GSE328094_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE328094 for PMID 42363191 (Aerobic exercise is associated with alleviation of skeletal muscle "
             "atrophy in CT26 tumor-bearing mice: insights from transcriptomic and weighted gene co-expression network "
             "analysis): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE328094")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")
fpkm_ev = case.add_input(FPKM, "matrix")

LOG2_2 = math.log2(2.0)  # = 1.0 exactly
paper_threshold = {"metric": "qvalue", "adjustment": "not_reported (DESeq2 q value; executor applies BH)",
                   "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": LOG2_2,
                   "effect_cutoff_original": "fold change > 2 or < 0.5 (|log2FC| > 1)",
                   "inclusive": False, "source_locator": "S2.7.p2"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID42363191 / PMC13591731 (BMC Musculoskelet Disord 2026, doi 10.1186/s12891-026-10131-5)",
    "accessions": ["GSE328094"], "accession_locator": "S11.p1",
    "assay": "bulk RNA-seq, gastrocnemius, Illumina NovaSeq 6000 PE150; fastp -> HISAT2 (GRCm39) -> HTSeq-count; FPKM also computed (S2.6.p1, S2.7.p1)",
    "sample_inclusion": ["48 male BALB/c mice, 4 groups x 12: C (control), E (exercise), T (CT26 tumor-bearing), TE (tumor + exercise) (S2.1.p2)",
                         "RNA-seq on 4 randomly selected mice per group, n=16 (S2.6.p1, S3.3.p1, FIG2)"],
    "sample_exclusion": ["not_reported for RNA-seq (one TE mouse missing from phenotype figure, FIG1; n=4/group sequenced)"],
    "factors": [
        {"name": "tumor", "levels": ["no", "yes"], "type": "between-animal; CT26 s.c. inoculation vs saline", "locator": "S2.2.p3"},
        {"name": "ex", "levels": ["sed", "ex"], "type": "between-animal; 4-wk treadmill 14 m/min 60 min/d 6 d/wk vs stationary treadmill", "locator": "S2.3.p1"}],
    "design": "2x2 factorial, one gastrocnemius sample per mouse, independent animals",
    "primary_estimand": ("Effect of aerobic exercise on the gastrocnemius transcriptome of tumor-bearing mice (TE vs T), "
                         "interpreted against the tumor effect (T vs C) that exercise is said to partially reverse."),
    "planned_contrasts": [
        {"name": "T_vs_C", "definition": "tumor-bearing vs control (sedentary)", "reported": "486 DEGs (273 up, 213 down)", "locator": "S3.3.p3, FIG2F"},
        {"name": "TE_vs_T", "definition": "tumor+exercise vs tumor-bearing (exercise effect under tumor burden)", "reported": "270 DEGs (165 up, 105 down)", "locator": "S3.3.p3, FIG2G"}],
    "not_reported_contrasts": ["E vs C (exercise in healthy mice), TE vs E, tumor x exercise interaction: no DE results reported; run as exploratory"],
    "blocking_or_covariance": {"status": "not_required", "reason": "one sample per independent animal; single batch (GEO batch=1)", "locator": "S2.1.p2, S2.6.p1"},
    "matrix_scale": "HTSeq-count raw read counts (GEO counts.xls) plus FPKM (S2.7.p1)",
    "paper_method": "DESeq2 (S2.7.p2); formula and pairwise vs joint fitting not reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "enrichment": {"ORA": "clusterProfiler GO/KEGG on DEGs, p<0.05 (S2.8.p1)",
                   "GSEA": "GSEA software, GO gene sets (S2.7.p2, S3.4.p2)",
                   "WGCNA": "top 2000 variable genes (S2.7.p2, S2.9)"},
}
case.write_json("paper_reconstruction.json", study_map, "paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE328094"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": study_map["planned_contrasts"], "paper_threshold": paper_threshold,
                   "factors": study_map["factors"], "paper_method": study_map["paper_method"],
                   "sample_inclusion": study_map["sample_inclusion"]},
            evidence=[paper], paper={"locator": "S2.1.p2; S2.6.p1; S2.7.p2; S3.3.p3; S11.p1"},
            reasoning=("2x2 tumor x exercise design, n=4 mice/group sequenced. The paper reports DESeq2 DEGs for T vs C "
                       "and TE vs T only, with q<0.05 and FC>2 or <0.5. The exercise question is TE vs T; E vs C and the "
                       "interaction are not reported and are exploratory."),
            confidence="high")

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
counts_raw = native.read_table(MATRIX)
own = {"accession": "GSE328094", "matrix_file": MATRIX, "metadata_file": META, "owned": True,
       "series_id": sorted(meta["series_id"].astype(str).unique()),
       "n_metadata_samples": int(len(meta)), "n_matrix_columns": int(counts_raw.shape[1]),
       "groups_in_metadata": meta["characteristics_ch1.2.treatment"].value_counts().to_dict(),
       "matrix_columns": list(map(str, counts_raw.columns)),
       "other_file": {"path": FPKM, "use": "not used for DE (counts deposited)"}}
case.decide("ownership", final=own, evidence=[meta_ev, mat_ev, fpkm_ev, paper],
            paper={"locator": "S11.p1; S2.6.p1"},
            reasoning=("Series GSE328094 is the paper's deposit (S11.p1). 16 gastrocnemius samples, 4 groups x 4 "
                       "(control, exercise, tumor-bearing, tumor-bearing + exercise) match the n=4/group RNA-seq. "
                       "GEO data_processing repeats the paper's pipeline and threshold. Matrix columns are the library names."),
            confidence="high")

# ---------------------------------------------------------------- 3 alignment
keyed = native.derive_columns(META, case.dir / "aligned" / "metadata_keyed.csv",
                              patterns={"lib": ("title", r"^sample (\S+)$")})
aln = native.align_to_metadata(MATRIX, case.dir / "aligned" / "metadata_keyed.csv", case.dir / "aligned", key_column="lib")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
aligned_meta_ev = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"trt": "characteristics_ch1.2.treatment"},
    patterns={"grp": ("lib", r"^(N-A|NC|TSA|TS)\d$"), "tumor": ("characteristics_ch1.2.treatment", r"^(\S+)"),
              "ex": ("characteristics_ch1.2.treatment", r"^(.*)$")},
    recode={"grp": {"NC": "C", "N-A": "E", "TS": "T", "TSA": "TE"},
            "tumor": {"control": "no", "exercise": "no", "tumor-bearing": "yes"},
            "ex": {"control": "sed", "exercise": "ex", "tumor-bearing": "sed", "tumor-bearing + exercise": "ex"}})
design_csv = case.dir / "aligned" / "design_metadata.csv"
design_ev = case.add_output(design_csv, "design_metadata")
dm = pd.read_csv(design_csv, index_col=0)
# cross-check library prefix group against GEO treatment label
xt = pd.crosstab(dm["grp"], dm["trt"])
assert all((xt > 0).sum(axis=1) == 1), xt
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln.get("unmatched", []),
                   "key_derivation": keyed, "derived_columns": derived,
                   "group_check": {k: {kk: int(vv) for kk, vv in v.items() if vv} for k, v in xt.to_dict(orient="index").items()}},
            evidence=[mat_ev, meta_ev, aligned_mat, aligned_meta_ev, amap, design_ev],
            reasoning=("Matrix columns (N-A1..TSA4) equal the GEO title after the 'sample ' prefix; an exact key 'lib' was "
                       "derived by regex and used for exact alignment (16/16). Library prefixes (NC, N-A, TS, TSA) agree "
                       "one-to-one with the GEO treatment characteristic. Derived formula-safe columns grp (C/E/T/TE), "
                       "tumor (no/yes), ex (sed/ex)."),
            confidence="high")

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
case.write_json("matrix_profile.json", prof, "matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": prof,
                   "source": "HTSeq-count gene-level read counts (GEO data_processing; S2.7.p1)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.7.p1"},
            reasoning=("All values non-negative integers (profile), file named counts, GEO processing says HTSeq-count raw "
                       "read counts; the paper ran DESeq2 on these counts."),
            confidence="high")
print("profile:", json.dumps(prof, default=str)[:800])

# ---------------------------------------------------------------- 5 design
refs = {"tumor": "no", "ex": "sed"}
comps = su.enumerate_comparisons(dm, ["tumor", "ex"], references=refs)
for c in comps:
    print("COMP", c["name"], c["kind"], c.get("within"), c["analyzable"])
names = {c["name"]: c for c in comps}
T_vs_C = next(c["name"] for c in comps if c["kind"] == "simple" and c["factor"] == "tumor" and c["within"].get("ex") == "sed")
TE_vs_T = next(c["name"] for c in comps if c["kind"] == "simple" and c["factor"] == "ex" and c["within"].get("tumor") == "yes")
planned = [T_vs_C, TE_vs_T]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="raw counts", metadata=dm, factors=["tumor", "ex"], matrix_csv=aln["outputs"]["aligned_matrix"]["path"],
    organism="Mouse", subject=None, references=refs, planned=planned)
print("SUITABILITY", json.dumps(suit_summary))
contrasts = []
for c in rep["comparisons"]:
    role = "planned" if c["name"] in planned else "exploratory"
    label = {T_vs_C: "T_vs_C (paper)", TE_vs_T: "TE_vs_T (paper; exercise effect under tumor)"}.get(c["name"], "")
    contrasts.append({"name": c["name"], "kind": c["kind"], "within": c.get("within"), "role": role,
                      "paper_label": label, "analyzable": c["analyzable"]})
case.decide("design",
            final={"analysis_type": "factorial 2x2 (tumor x exercise), independent animals",
                   "formula": "~ cell (cell = tumor:ex, 4 levels), one DESeq2 model on all 16 samples",
                   "contrasts": contrasts, "planned": planned, "references": refs,
                   "estimand_type": "causal (randomised groups, S2.1.p2)",
                   "suitability": suit_summary},
            evidence=[design_ev, suit_item, paper], paper={"locator": "S2.1.p2; S3.3.p3"},
            candidates=[{"value": "pool E+TE vs C+T (exercise main effect)", "reason_rejected": "paper's question is exercise within tumor-bearing mice; pooling hides the interaction"},
                        {"value": "only the two pairwise subsets", "reason_rejected": "skill policy: one model on all samples for a factorial; pairwise subset fit kept as sensitivity audit"}],
            reasoning=("Randomised 2x2 design with n=4 per cell. Paper-planned: T vs C (tumor effect, sedentary) and TE vs T "
                       "(exercise effect under tumor). Exploratory: E vs C, TE vs E, and the tumor x exercise interaction. "
                       "All from one model with four cell means."),
            confidence="high")

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(dm, "grp", ["characteristics_ch1.3.batch", "characteristics_ch1.0.tissue",
                                             "characteristics_ch1.1.genotype"])
dc = native.design_check(dm, ["grp"], [])
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc}, "covariance_reports")
sex = rep["checks"].get("sex", {})
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "batch", "disposition": "excluded: single level (batch=1)"},
                                  {"name": "tissue", "disposition": "excluded: single level (skeletal muscle)"},
                                  {"name": "genotype", "disposition": "excluded: single level (wild type)"},
                                  {"name": "sex", "disposition": "excluded: all male (S2.1.p1); sex check status " + str(sex.get("status"))},
                                  {"name": "animal", "disposition": "nested: one sample per animal, no repeated measures"}],
                   "confounding": conf, "design_check": dc},
            evidence=[design_ev, suit_item, paper], paper={"locator": "S2.1.p1; S2.6.p1"},
            reasoning="Independent animals, one muscle sample each; batch, tissue, genotype and sex are constant. No blocking.",
            confidence="high")

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 0.5.4) joint model ~ cell on all 16 samples, Wald contrasts per comparison",
                   "matrix_type": "raw counts", "formula": "~ cell", "independent_filtering_alpha": 0.05,
                   "lfc_shrinkage": "none (unshrunk MLE log2FC, as DESeq2 results())",
                   "paper_route": {"method": "DESeq2 (R; per-pair vs joint not reported)", "status": "reproduced_with_python_port"},
                   "sensitivity": "pairwise two-group DESeq2 fits for the two planned contrasts (audit)"},
            evidence=[aligned_mat, design_ev, paper], paper={"locator": "S2.7.p2"},
            reasoning=("Paper used DESeq2 on HTSeq counts; counts deposited, so the paper route runs. The pairwise vs joint "
                       "choice is not reported; one joint model is the factorial policy, and pairwise fits are an audit."),
            confidence="medium")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": dict(paper_threshold),
                   "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "label": "workflow_default audit"}},
            evidence=[paper], paper={"locator": "S2.7.p2"},
            reasoning="Paper: q<0.05 and FC>2 or <0.5, i.e. padj<0.05 and |log2FC|>1 strict. Applied unchanged; a padj-only count is an audit.",
            confidence="high")
json.dump({"planned": planned, "refs": refs, "design_csv": str(design_csv),
           "aligned_matrix": aln["outputs"]["aligned_matrix"]["path"]},
          open(case.dir / "plan_state.json", "w"), indent=2)
print("planned:", planned)
