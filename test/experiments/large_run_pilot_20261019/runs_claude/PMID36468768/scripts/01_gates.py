"""Gates paper_reconstruction .. threshold for GSE196147 (PMID 36468768)."""
import sys, pathlib, json, math
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import pandas as pd
from tools import native

native.enable_native_mode()
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
REL = str(RUN.relative_to(ROOT)).replace("\\", "/")
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13281843.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13281843.paper.md"
CID = "GSE196147"

run = native.RunRecorder(REL, request=(
    "Analyze GSE196147 for PMID 36468768 (Adaptation of the transcriptional response to resistance exercise over "
    "4 weeks of daily training): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[CID])
case = run.case(CID, accession="GSE196147")
paper = case.add_input(PAPER_JSON, "paper"); paper_md = case.add_input(PAPER_MD, "paper")
meta_raw = case.add_input("data/GSE196147/GSE196147_metadata.csv", "metadata")
soft = case.add_input("data/GSE196147/GSE196147_family.soft.gz", "metadata")
norm_raw = case.add_input("data/GSE196147/GSE196147_1Normalized_counts_deseq2.txt.gz", "matrix")
cnt_raw = case.add_input("data/GSE196147/GSE196147_2counts.txt.gz", "matrix")
gsa_raw = case.add_input("data/GSE196147/GSE196147_2gsa_result.txt.gz", "matrix")
mat = case.add_input(f"{REL}/inputs/GSE196147_deseq2_normalized_transcripts.csv", "matrix")
meta_keyed = case.add_input(f"{REL}/inputs/metadata_keyed.csv", "metadata")
build_log = case.add_input(f"{REL}/inputs/build_inputs_log.json", "matrix", label="build_inputs_log.json")

# ---------------------------------------------------------------- paper_reconstruction
PT = {"metric": "FDR", "adjustment": "not_reported (q-value; Partek Flow reports 'FDR step up' = BH)", "cutoff": 0.05,
      "effect_metric": None, "effect_cutoff": None, "inclusive": False,
      "source_locator": "S3.2.p1 ('identified DEGs with a cut off at (q < .05)'); FIG2"}
PAPER_COUNTS = {
    "d2_vs_ctrl": {"total": 2398, "up_pct": 71.3, "up_approx": 1710, "down_approx": 688, "locator": "S3.2.p1"},
    "d10_vs_ctrl": {"total": 2218, "up_pct": 71.3, "up_approx": 1581, "down_approx": 637, "locator": "S3.2.p1"},
    "d20_vs_ctrl": {"total": 1755, "up_pct": 54.4, "up_approx": 955, "down_approx": 800, "locator": "S3.2.p1"},
    "d30_vs_ctrl": {"total": 3312, "up": 484, "down": 2828, "locator": "S3.2.p1"},
    "common_all_timepoints": {"total": 519, "up_pct": 66.5, "locator": "S3.2.p1; FIG2 C"},
}
recon = {
    "paper_id": "PMID36468768 / PMC13281843",
    "accessions": ["GSE196147"],
    "accession_roles": {"GSE196147": "paper's own deposit (S10.p1, data availability)"},
    "assay": "bulk poly-A RNA-seq, NextSeq 550 PE150; Partek Flow, STAR to Rnor_6.0, Ensembl 99 transcript quantification (S2.6.p1, S2.7.p1)",
    "organism": "Rattus norvegicus, male Wistar, tibialis anterior (S2.1.p1, S2.5.p1)",
    "factors": [{"name": "limb", "levels": ["right contralateral control (unstimulated)", "left trained (SpillOver stimulation)"]},
                {"name": "training duration", "levels": ["2 d", "10 d", "20 d", "30 d"], "note": "sampled 1 h after last bout"}],
    "sample_inclusion": ["RNA-seq: 3 animals per training duration, both TA muscles (FIG2 B: control n = 12, each training group n = 3)"],
    "sample_exclusion": ["sham-surgery animals (n = 5) were used for morphology only; no RNA-seq libraries (S2.1.p1; FIG2 B)"],
    "primary_estimand": ("Acute (1 h post-bout) transcriptional response of trained left TA versus unexercised control TA after "
                         "2, 10, 20 and 30 days of daily resistance training, and how that response changes with training duration."),
    "planned_contrasts": ["d2_vs_ctrl", "d10_vs_ctrl", "d20_vs_ctrl", "d30_vs_ctrl"],
    "paper_control_definition": "the 12 contralateral control TAs pooled into one control group (FIG2 B; S3.2.p1 'All contralateral control samples clustered together independent of the length of training')",
    "blocking_or_covariance": {"status": "paper_not_stated",
                               "repeated_measures": "each animal contributes a trained (L) and a control (R) TA; the paper's pooled 12-vs-3 comparison does not state any animal blocking"},
    "matrix_scale": "DESeq2 median-of-ratios normalized transcript counts (S2.7.p1); raw counts not stated as deposited (S10.p1 'Processed data are provided')",
    "paper_method": "Partek Flow DESeq2 (negative binomial GLM, Wald test) per training group vs control (S2.7.p1)",
    "paper_formula": "not_reported",
    "paper_threshold": PT,
    "paper_threshold_conflict": "S2.7.p1 says significance 'set at p < .01'; S3.2.p1 and the FIG2 B counts use q < .05. The counts the paper reports are tied to q < .05, so that is taken as the paper rule; raw p < .01 is reported only as an audit.",
    "paper_reported_deg_counts": PAPER_COUNTS,
    "paper_enrichment": "KEGG (Partek) on DEG lists per timepoint, SOM clusters, HOMER motifs (S2.8.p1) - not requested here",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={k: recon[k] for k in ("accessions", "primary_estimand", "planned_contrasts", "paper_threshold",
                                         "paper_method", "paper_formula", "assay", "matrix_scale", "sample_inclusion",
                                         "sample_exclusion", "paper_control_definition", "blocking_or_covariance")},
            evidence=[paper, paper_md], paper={"locator": "S2.1.p1; S2.2.p2; S2.7.p1; S3.2.p1; FIG2; S10.p1"},
            confidence="high",
            reasoning=("Left TA trained daily by implanted stimulator for 2/10/20/30 d, right TA is the contralateral control "
                       "(S2.2.p2). RNA-seq on 3 animals per duration; each training group compared with the 12 pooled controls "
                       "with DESeq2 (FIG2 B, S2.7.p1). DEG counts are given at q < .05 (S3.2.p1). Sham animals were not sequenced."))

# ---------------------------------------------------------------- ownership
meta = pd.read_csv(ROOT / "data/GSE196147/GSE196147_metadata.csv", index_col=0)
case.decide("ownership", final={
    "accession": "GSE196147",
    "matrix_file": f"{REL}/inputs/GSE196147_deseq2_normalized_transcripts.csv (from data/GSE196147/GSE196147_1Normalized_counts_deseq2.txt.gz by scripts/00_build_inputs.py)",
    "metadata_file": "data/GSE196147/GSE196147_metadata.csv", "owned": True,
    "checks": {"series_id": "GSE196147 in metadata series_id and paper S10.p1",
               "design": "GEO overall design: stimulated left TA vs unstimulated contralateral right TA at 2/10/20/30 d, 1 h post exercise (matches S2.2.p2, S2.5.p1)",
               "samples": "24 GSMs = 4 durations x 3 animals x 2 limbs; matches FIG2 B (control n = 12, each training group n = 3)",
               "tissue_strain": "tibialis anterior, Wistar, Rattus norvegicus (matches S2.1.p1)",
               "processing": "Partek Flow, STAR, rn6, Ensembl 99 transcripts, Partek DESeq2 normalization (matches S2.7.p1; GEO says STAR 2.7.3a, paper says 'STAR 4.4.1d')",
               "matrix_rows": "20027 transcripts = the paper's '20027 different gene transcripts' (FIG2 B)",
               "other_supplementary": {
                   "GSE196147_2counts.txt.gz": "labelled 'rawcounts' in GEO but non-integer (integer fraction 0.0002), only 4635 genes, column sums ~310k: a normalized gene-level subset, not raw counts",
                   "GSE196147_2gsa_result.txt.gz": "Partek GSA result on those 4635 genes (Control vs each duration); its FDR<0.05 counts (1251/977/716/3109) do not match the paper's 2398/2218/1755/3312 - a different analysis, used only as a concordance reference"}}},
    evidence=[meta_raw, soft, norm_raw, cnt_raw, gsa_raw, paper], paper={"locator": "S10.p1; FIG2"}, confidence="high",
    reasoning="Accession, design, sample counts, and the 20027-transcript universe all match the paper.")

# ---------------------------------------------------------------- alignment
aln = native.align_to_metadata(mat["path"], meta_keyed["path"], case.dir / "aligned", key_column="lib_id")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
aligned_meta_path = aln["outputs"]["aligned_metadata"]["path"]
cond_map = {"2 Days Training": "d2", "10 Days Training": "d10", "20 Days Training": "d20", "30 Days Training": "d30"}
am = pd.read_csv(aligned_meta_path, index_col=0)
recode_tp = {v: cond_map[v.replace("  (Contralateral Control)", "").strip()] for v in am["characteristics_ch1.2.condition"].unique()}
derived = native.derive_columns(
    aligned_meta_path, case.dir / "aligned" / "design_metadata.csv",
    aliases={"tp": "characteristics_ch1.2.condition", "grp": "characteristics_ch1.2.condition",
             "limb": "side"},
    recode={"tp": recode_tp,
            "grp": {v: ("ctrl" if "Contralateral" in v else cond_map[v.strip()]) for v in am["characteristics_ch1.2.condition"].unique()},
            "limb": {"L": "trained", "R": "ctrl"}})
dm_path = case.dir / "aligned" / "design_metadata.csv"
dm = pd.read_csv(dm_path, index_col=0); dm["animal"] = "a" + dm["animal"].astype(str); dm.to_csv(dm_path)
derived["columns"]["animal"] = {"source": "description", "regex": "GC-JJ-9173-(\\d+)-?[LR]-\\d+_S\\d+", "prefix": "a"}
design_meta = case.add_output(dm_path, "design_metadata")
case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
case.decide("alignment", final={
    "method": aln["method"] + " on lib_id (= animal + side parsed from GEO description)",
    "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
    "unmatched": aln.get("unmatched", []),
    "derived_columns": {"animal": "regex on description", "side": "regex on description", "lib_id": "animal+side",
                        "tp": recode_tp, "grp": "ctrl for contralateral controls, else d2/d10/d20/d30",
                        "limb": {"L": "trained", "R": "ctrl"}},
    "consistency_check": "side R <=> title '(Contralateral Control)' for all 24 samples"},
    evidence=[mat, meta_keyed, build_log, aligned_mat, design_meta], confidence="high",
    reasoning="Matrix columns are library labels (e.g. 258R) that GEO stores in description; exact match on the parsed key, 24/24.")

# ---------------------------------------------------------------- matrix
prof = native.profile_matrix(aligned_mat["path"])
case.write_json("matrix_profile.json", prof, role="matrix_profile")
case.decide("matrix", final={
    "matrix_type": "DESeq2-normalized counts (linear, non-integer)",
    "recommended_method": "log2(x+1) then limma; count methods refused (no integer counts deposited)",
    "profile": {k: prof.get(k) for k in ("integer_fraction", "min", "max", "negative_values", "missing_values", "type_candidates") if k in prof},
    "evidence_notes": ["file name '1Normalized_counts_deseq2', GEO processing 'Partek Deseq2 normalization'",
                       "integer fraction ~0.06, values such as 0.2129 and 1e-44: not counts",
                       "every column sums to 634431 (equal library totals) - consistent with a rescaled normalized matrix",
                       "the only other matrix ('2counts', labelled rawcounts) is also non-integer and gene-subset"],
    "paper_input": "paper ran DESeq2 on raw transcript counts; those are not deposited"},
    evidence=[aligned_mat, norm_raw, cnt_raw, soft], confidence="high",
    reasoning="Normalized linear values, not integer counts; rounding normalized values to counts is not allowed.")
print("profile:", json.dumps({k: prof.get(k) for k in ("integer_fraction", "min", "max", "type_candidates")}, default=str))

# ---------------------------------------------------------------- design
rep, s_item, s_summary = case.suitability(
    matrix_type="DESeq2-normalized counts", metadata=dm, factors=["grp"], matrix_csv=aligned_mat["path"],
    organism="Rat", subject="animal", references={"grp": "ctrl"},
    planned=["grp_d2_vs_ctrl", "grp_d10_vs_ctrl", "grp_d20_vs_ctrl", "grp_d30_vs_ctrl"])
print("suitability:", s_summary, [c["name"] for c in rep["comparisons"]])
comps = rep["comparisons"]
case.write_json("comparisons.json", comps, role="comparisons")
planned = ["grp_d2_vs_ctrl", "grp_d10_vs_ctrl", "grp_d20_vs_ctrl", "grp_d30_vs_ctrl"]
case.decide("design", final={
    "analysis_type": "repeated (paired limbs within animal; one model, several levels)",
    "formula": "~ 0 + C(grp) + C(animal)",
    "design_column": "grp",
    "contrasts": planned,
    "exploratory_contrasts": [c["name"] for c in comps if c["name"] not in planned],
    "levels": {"grp": ["ctrl (12 contralateral TA)", "d2", "d10", "d20", "d30 (3 trained TA each)"]},
    "estimand_note": ("With animal blocking each dX_vs_ctrl contrast is the trained-minus-contralateral difference within the "
                      "dX animals; the 12 pooled controls set the reference level as in the paper. Between-duration "
                      "contrasts (e.g. d30 vs d2) are differences of within-animal training responses - the adaptation question."),
    "suitability": s_summary},
    evidence=[design_meta, s_item, paper], paper={"locator": "FIG2 B; S3.2.p1; S2.2.p2"}, confidence="high",
    candidates=[{"value": "~ grp (paper: pooled control, no animal term)", "reason_rejected": "treats the two limbs of one animal as independent replicates"},
                {"value": "separate 3-vs-3 paired test per duration", "reason_rejected": "refits on 6 samples and loses the shared variance estimate; one model on all 24 samples is preferred"},
                {"value": "limb x tp factorial", "reason_rejected": "tp main effect is aliased with animal under blocking; ~ animal + grp spans the same estimable effects (limb effect per duration)"}],
    reasoning=("Five-level factor grp (ctrl + four trained durations) as in FIG2 B, all 24 samples in one limma model, "
               "with animal as blocking term because every animal gives one trained and one control muscle. "
               "The four dX_vs_ctrl contrasts are the paper's; between-duration contrasts run as exploratory."))

# ---------------------------------------------------------------- covariance
pr = native.pairing_report(dm, "animal", "limb", ["ctrl", "trained"])
cr = native.confounding_report(dm, "grp", ["animal", "tp", "limb"])
dc = native.design_check(dm, ["animal", "grp"])
cov_item = case.write_json("covariance_reports.json", {"pairing": pr, "confounding": cr, "design_check": dc}, role="covariance_reports")
print("pairing:", json.dumps(pr, default=str)[:400]); print("design_check:", json.dumps(dc, default=str)[:400])
case.decide("covariance", final={
    "status": "required", "blocking_terms": ["animal"],
    "covariates": [{"name": "animal", "disposition": "included (blocking: trained and control TA from the same rat)"},
                   {"name": "tp", "disposition": "nested: training duration is constant within animal; its effect on controls is absorbed by the animal block"},
                   {"name": "limb", "disposition": "aliased by construction with grp (grp = limb x duration for trained limbs)"},
                   {"name": "sex/strain", "disposition": "excluded: single level (male Wistar)"},
                   {"name": "batch", "disposition": "excluded: not recorded in GEO or paper"}],
    "pairing": {k: pr.get(k) for k in ("n_complete", "n_incomplete", "n_duplicated", "complete_subjects") if k in pr},
    "design_rank": {k: dc.get(k) for k in ("rank", "n_columns", "full_rank", "residual_df") if k in dc}},
    evidence=[design_meta, cov_item],
    confidence="high", paper={"locator": "S2.2.p2 (contralateral limb of the same animal)"},
    candidates=[{"value": "no blocking (paper)", "reason_rejected": "12 animals each contribute a trained and a control muscle"}],
    reasoning="Complete pairing of 12 animals; ~ animal + grp is full rank with 8 residual df.")

# ---------------------------------------------------------------- method
case.decide("method", final={
    "method": "limma (moderated t, empirical Bayes) joint model",
    "matrix_type": "DESeq2-normalized counts (linear, non-integer)",
    "transform": "log2(x+1)",
    "formula": "~ 0 + C(grp) + C(animal)",
    "paper_route": {"method": "DESeq2 (Partek Flow) on raw transcript counts, Wald test, 12 pooled controls vs 3 trained", "status": "blocked",
                    "reason": "raw integer counts are not deposited in GEO (only DESeq2-normalized values and a normalized 4635-gene subset); DESeq2 cannot run on normalized values and they must not be rounded"},
    "executor": "tools.joint_contrasts:run_joint_limma (covariates=('animal',))",
    "feature_filter": "none (keeps the paper's 20027-transcript universe)"},
    evidence=[aligned_mat, norm_raw, paper], paper={"locator": "S2.7.p1"}, confidence="high",
    reasoning="Linear normalized expression -> log2(x+1) -> limma with animal block is the policy route; declared deviation from DESeq2.")

# ---------------------------------------------------------------- threshold
case.decide("threshold", final={
    "paper_threshold": PT, "threshold_source": "paper_on_deviation_route",
    "applied_threshold": {"metric": "padj", "adjustment": "BH within each contrast", "cutoff": 0.05,
                          "effect_metric": None, "effect_cutoff": None, "inclusive": False},
    "deviation_note": "paper's q-value from Partek DESeq2 (adjustment not named; Partek 'FDR step up' is BH); applied as BH-adjusted p from limma",
    "audit_threshold": {"metric": "pvalue", "cutoff": 0.01, "source": "S2.7.p1 statement 'p < .01'", "threshold_source": "audit"}},
    evidence=[paper], paper={"locator": "S3.2.p1; S2.7.p1"}, confidence="medium",
    reasoning="q < .05 is the rule behind the paper's reported counts; S2.7.p1 states p < .01, kept as an audit count.")
print("gates recorded")
