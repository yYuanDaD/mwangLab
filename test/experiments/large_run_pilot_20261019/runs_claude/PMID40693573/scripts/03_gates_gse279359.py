"""Gates 1-8 (paper_reconstruction .. threshold) for case GSE279359 (mouse long-read, PMID40693573)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
CASE = "GSE279359"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.md"
MATRIX = "data/GSE279359/GSE279359_processed_counts.txt.gz"
META = "data/GSE279359/GSE279359_metadata.csv"

run = native.RunRecorder.open(RUN)
case = run.case(CASE, accession="GSE279359")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

paper_threshold = {"metric": "padj", "adjustment": "not_reported (executor applies BH)", "cutoff": 0.05, "inclusive": False,
                   "effect_metric": "log2FC", "effect_cutoff": 1.5, "effect_inclusive": False,
                   "effect_cutoff_original": "|log2FC| > 1.5 (log2 scale)", "source_locator": "S3.1.p2",
                   "note": "S3.1.p2 first applies |log2FC| > 1.5, p-adj < .05 and then a relaxed |log2FC| > 1.0, p-adj < .05 "
                           "for figures 2F-H; the relaxed rule is kept as a labelled audit threshold"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID40693573 / PMC12248044",
    "accessions": ["GSE279359"], "accession_locator": "DA.p1",
    "assay": "Oxford Nanopore PCR-cDNA long-read RNA-seq (MinION), minimap2 -> TranscriptClean -> TALON (S2.4.p1, S2.5.p2)",
    "sample_inclusion": ["C57BL/6-Tg(TERT) mice ~10 weeks, gastrocnemius; 30-min treadmill run at 60% max speed (S2.2.p1)",
                         "terminal sampling: pre (3M 2F), immediately post (3M 2F), 1 h post (2M 3F), 24 h post (3M 2F); "
                         "animals randomly assigned to time points, none excluded (S2.2.p1)"],
    "sample_exclusion": [],
    "factors": [{"name": "time", "levels": ["pre", "ipe", "1pe", "24pe"], "locator": "S2.2.p1"}],
    "primary_estimand": "Acute treadmill-exercise effect on gastrocnemius gene expression at each recovery time vs pre-exercise "
                        "(S3.1.p2, FIG2F-H).",
    "planned_contrasts": [
        {"name": "ipe_vs_pre", "locator": "S3.1.p2"}, {"name": "1pe_vs_pre", "locator": "S3.1.p2"},
        {"name": "24pe_vs_pre", "locator": "S3.1.p2"}],
    "blocking_or_covariance": {"status": "not_required", "note": "different animals at each time point (S2.2.p1)"},
    "matrix_scale": "TALON read counts; known genes detected in at least half of the samples (S2.6.p2)",
    "paper_method": "Swan v2.0 gene-level differential expression (log2FC + adjusted p) (S2.6.p2)",
    "paper_formula": "not_reported (Swan pairwise test vs pre)",
    "paper_threshold": paper_threshold,
    "reported_counts": {"ipe_vs_pre": "23 (17 up, 6 down) at |log2FC|>1.5; 46 (33 up, 13 down) at |log2FC|>1.0; 6323 genes detected",
                        "1pe_vs_pre": "13 (9 up, 4 down) at 1.5; 32 (24 up, 8 down) at 1.0; 5459 genes detected",
                        "24pe_vs_pre": "31 (15 up, 16 down) at 1.5; 49 (23 up, 26 down) at 1.0; 6125 genes detected",
                        "validated": "Ube2d1 up at ipe (log2FC 0.75), Fbxo32 up at 1pe (2.7), Fos down at 24pe (-3.9) (S3.1.p2)"},
    "enrichment": "none at gene level for the mouse DGE (<80 significant genes, S2.6.p3)",
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "DE method", "paper": "Swan v2.0 gene-level test (S2.6.p2)", "data": "Swan/diffxpy not installed here",
     "classification": "requires_explicit_deviation", "note": "DESeq2 on gene-summed TALON counts as a declared deviation"},
    {"item": "deposited matrix", "paper": "unfiltered TALON abundance; 5459-6323 genes detected per comparison",
     "data": "GEO 'processed counts': 8452 transcripts already filtered by the authors (TALON filter), 2974 known genes + "
             "novel antisense/intergenic loci; library sizes 77k-336k reads",
     "classification": "requires_explicit_deviation",
     "note": "gene universe smaller than the paper's; DEG counts are not expected to match exactly"},
    {"item": "gene filter", "paper": "known genes detected in at least half of the samples (S2.6.p2)",
     "data": "-", "classification": "executable_without_change",
     "note": "applied per pairwise comparison (>=5 of 10 samples with count > 0), gene_novelty == Known"},
    {"item": "sample labels", "paper": "independent animals per time point",
     "data": "GEO titles number animals 1-5 within each time point (e.g. Male1)", "classification": "executable_without_change",
     "note": "numbers are within-group replicate labels, not animal IDs across time points (S2.2.p1 random assignment)"},
    {"item": "adjustment", "paper": "p-adj, method not named for Swan", "data": "-", "classification": "executable_without_change",
     "note": "BH from DESeq2"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE279359"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S3.1.p2"}, confidence="high",
            reasoning=("GSE279359 is the paper's own mouse LRS deposit (DA.p1). Four independent groups of 5 mice; each "
                       "post-exercise time point vs pre. Swan DGE, |log2FC| > 1.5 and p-adj < .05 (relaxed 1.0 also reported)."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.astype(str).unique().tolist()), "n_samples": int(len(meta)),
       "time_by_sex": pd.crosstab(meta["characteristics_ch1.1.time"], meta["characteristics_ch1.3.Sex"]).to_dict(),
       "instrument": meta.instrument_model.unique().tolist(), "genotype": meta["characteristics_ch1.2.genotype"].unique().tolist(),
       "contact": meta.contact_name.unique().tolist(),
       "processing": "MinKNOW q>8, minimap2 2.14, SAMtools 1.13, TALON coverage 0.75 identity 0.8, GENCODE M29 (= S2.5.p2)"}
case.decide("ownership",
            final={"accession": "GSE279359", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("Paper's own deposit (Ludlow lab). 20 gastrocnemius samples, mmYS-pre/ipe/1pe/24pe x 5 with the same "
                       "sex split as S2.2.p1; MinION; processing identical to S2.5.p2."))

# ---------------------------------------------------------------- 3 alignment
aln = native.align_to_metadata(MATRIX, META, case.dir / "aligned", key_column="description")
print("alignment", {k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage", "unmatched_matrix_columns",
                                        "annotation_columns_dropped")})
assert aln["coverage"] == 1.0, aln
dpath = case.dir / "aligned" / "design_metadata.csv"
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], dpath,
    patterns={"time": ("characteristics_ch1.1.time", r"^(pre-exercise|immediately post-exercise|1 hour post-exercise|24 hours post-exercise)$"),
              "sex": ("characteristics_ch1.3.Sex", r"^(male|female)$"),
              "grp_label": ("title", r"^(mmYS-(?:pre|ipe|1pe|24pe)),")},
    recode={"time": {"pre-exercise": "pre", "immediately post-exercise": "ipe", "1 hour post-exercise": "h1",
                     "24 hours post-exercise": "h24"}})
dm = pd.read_csv(dpath, index_col=0)
assert (dm.groupby("time")["grp_label"].nunique() == 1).all()
design_meta = case.add_output(dpath, "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "derived_columns": ["time", "sex", "grp_label"],
                   "levels": {c: dm[c].astype(str).value_counts().to_dict() for c in ["time", "sex"]},
                   "row_index": "TALON gene_ID (one row per transcript; summed to genes at the matrix gate)"},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.2.p1"}, confidence="high",
            reasoning="Matrix columns equal the GEO 'description' library names (B_1M ... X24hPE_5M); 20/20 exact matches.")

# ---------------------------------------------------------------- 4 matrix
raw = pd.read_csv(MATRIX, sep="\t")
am = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
ann = raw.drop_duplicates("gene_ID").set_index("gene_ID")[["annot_gene_id", "annot_gene_name", "gene_novelty"]]
assert raw.groupby("gene_ID")["annot_gene_id"].nunique().max() == 1
gene = am.groupby(level=0).sum()
gene = gene.join(ann)
# deterministic gene-level summary (sum of transcript read counts per TALON gene), needed for the sex check and later gates
gene["ensembl"] = gene["annot_gene_id"].str.replace(r"\.\d+$", "", regex=True)
gene_counts = gene.set_index("ensembl")[dm.index.tolist()]
assert gene_counts.index.is_unique
gpath = case.dir / "aligned" / "gene_counts_all.csv"
gene_counts.to_csv(gpath)
annp = case.dir / "aligned" / "gene_annotation.csv"
gene.set_index("ensembl")[["annot_gene_id", "annot_gene_name", "gene_novelty"]].to_csv(annp)
known = gene[gene.gene_novelty == "Known"]
sym = known.set_index("annot_gene_name")[dm.index.tolist()]
sym = sym.groupby(level=0).sum()
spath = case.dir / "aligned" / "gene_counts_known_symbols.csv"
sym.to_csv(spath)
gene_ev = case.add_output(gpath, "gene_level_counts")
case.add_output(annp, "gene_annotation")
case.add_output(spath, "gene_level_counts_symbols")
prof_short = {k: prof.get(k) for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                       "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
prof_short.update({"n_transcripts": int(len(raw)), "n_genes": int(len(gene)), "n_known_genes": int(len(known)),
                   "gene_novelty": gene.gene_novelty.value_counts().to_dict(),
                   "transcript_novelty": raw.transcript_novelty.value_counts().to_dict(),
                   "library_sizes_reads": [int(am.sum().min()), int(am.sum().max())]})
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
print("profile", json.dumps(prof_short, default=str)[:1200])
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2 (paper's Swan test unavailable)",
                   "profile": prof_short, "feature_level": "transcript (TALON); summed to gene level per TALON gene",
                   "provenance": "TALON read counts per transcript, 'raw counts for each sample' (GEO data_processing, S2.5.p2)"},
            evidence=[aligned_mat, meta_ev, paper, gene_ev], paper={"locator": "S2.5.p2"}, confidence="high",
            reasoning=(f"All integers (fraction {prof.get('integer_fraction')}), non-negative, max {prof.get('max')}; GEO says raw "
                       f"counts. One row per transcript ({len(raw)}), {len(gene)} TALON genes of which {len(known)} known. "
                       "Long-read libraries are small (77k-336k reads)."))

# ---------------------------------------------------------------- 5 design
refs = {"time": "pre"}
rep0 = __import__("tools.suitability", fromlist=["x"]).enumerate_comparisons(dm, ["time"], references=refs)
names0 = [c["name"] for c in rep0]
print("comparison names", names0)
planned = [n for n in names0 if n.endswith("_vs_pre")]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="raw counts", metadata=dm, factors=["time"], matrix_csv=str(spath), organism="Mouse",
    subject=None, references=refs, planned=planned)
comps = [{k: c.get(k) for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
sexchk = rep["checks"].get("sex", {})
print("sex", json.dumps({k: sexchk.get(k) for k in ("status", "predicted", "mismatched", "uncertain", "split_plan")}, default=str)[:1500])
exploratory = [n for n in names0 if n not in planned]
LABEL = {"time_ipe_vs_pre": "ipe_vs_pre", "time_h1_vs_pre": "1pe_vs_pre", "time_h24_vs_pre": "24pe_vs_pre"}
case.write_json("suitability_comparisons.json", {"comparisons": comps, "planned": planned, "exploratory": exploratory},
                role="suitability_comparisons")
case.decide("design",
            final={"analysis_type": "multilevel (one factor, 4 independent groups)", "design_column": "time",
                   "formula": "~ time", "control": "pre",
                   "contrasts": ([{"name": LABEL.get(p, p), "suitability_name": p, "role": "paper_planned",
                                   "fit": "pairwise DESeq2 on the two groups, genes filtered per comparison (paper route)"}
                                  for p in planned]
                                 + [{"name": e, "suitability_name": e, "role": "exploratory",
                                     "fit": "joint DESeq2 ~ time on all 20 samples"} for e in exploratory]),
                   "audit": "planned contrasts also extracted from the joint 20-sample model",
                   "estimand_type": "interventional (random assignment to sampling time, S2.2.p1)",
                   "sex_split": "not run: 2-3 animals per sex per time point (< 3 in several cells)",
                   "suitability": suit_summary},
            candidates=[{"value": "pool post-exercise time points vs pre", "reason_rejected": "paper reports each time point; distinct levels are never pooled"},
                        {"value": "time as continuous", "reason_rejected": "non-monotone acute response; paper uses categorical time points"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "S3.1.p2"}, confidence="high",
            reasoning="Three planned contrasts vs pre; remaining pairwise time contrasts are exploratory from one model.")

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(dm, "time", ["sex"])
dc = native.design_check(dm, ["time"])
dc_sex = native.design_check(dm, ["time", "sex"])
dc_short = {k: dc.get(k) for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short,
                                            "design_check_with_sex": {k: dc_sex.get(k) for k in dc_short}},
                role="covariance_reports")
print(json.dumps({"conf": conf, "dc": dc_short}, default=str)[:800])
assert dc["full_rank"]
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "animal", "disposition": "excluded: one sample per animal (terminal sampling)"},
                                  {"name": "sex", "disposition": "excluded: crossed with time (2-3 per sex per group), not modelled by the paper; "
                                                                 "kept in the primary route out, noted as a limitation"}],
                   "design_check": dc_short},
            evidence=[design_meta, paper], paper={"locator": "S2.2.p1"}, confidence="high",
            reasoning=f"Independent animals; ~ time full rank, residual df {dc_short['residual_df']} (joint) and 8 per pairwise fit.")

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 Wald test, BH, independent filtering), pairwise vs pre",
                   "matrix_type": "raw counts", "formula": "~ time",
                   "transform": "transcript counts summed to TALON gene; gene_novelty == Known; per-comparison filter count > 0 in >= half of the samples",
                   "executor": "tools.deseq2_tools:run_deseq2_analysis per planned contrast",
                   "exploratory_executor": "tools.joint_contrasts:run_joint_deseq2 on all 20 (Known genes detected in >= 10 of 20)",
                   "paper_route": {"method": "Swan v2.0 gene-level differential expression", "status": "blocked",
                                   "reason": "Swan (diffxpy-based test) is not installed and has no executor here"}},
            evidence=[gene_ev, paper], paper={"locator": "S2.6.p2"}, confidence="high",
            reasoning="Raw integer read counts support DESeq2; Swan's own test cannot run -> declared deviation.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": "paper rule applied to DESeq2 instead of Swan; p-value adjustment is BH",
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
                                         "label": "audit: paper's relaxed rule (S3.1.p2)"},
                                        {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}]},
            evidence=[paper], paper={"locator": "S3.1.p2"}, confidence="high",
            reasoning="S3.1.p2: |log2FC| > 1.5 and p-adj < .05; the relaxed |log2FC| > 1.0 rule is reported as an audit count.")
print("done gates 1-8 for", CASE)
