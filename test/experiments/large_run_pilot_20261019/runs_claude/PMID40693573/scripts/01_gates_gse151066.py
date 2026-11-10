"""Create the run; gates 1-8 (paper_reconstruction .. threshold) for case GSE151066 (PMID40693573)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
CASE = "GSE151066"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12248044.paper.md"
MATRIX = "data/GSE151066/GSE151066_rsem_genes_count.txt.gz"
META = "data/GSE151066/GSE151066_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE151066 and GSE279359 for PMID 40693573 (Impact of Acute Endurance Exercise on Alternative "
             "Splicing in Skeletal Muscle): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=["GSE151066", "GSE279359"])
case = run.case(CASE, accession="GSE151066")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

paper_threshold = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "inclusive": False,
                   "effect_metric": "log2FC", "effect_cutoff": 1.5, "effect_inclusive": False,
                   "effect_cutoff_original": "log2FC > 1.5 / log2FC < -1.5 (written on the log2 scale)",
                   "source_locator": "S3.1.p1",
                   "note": "S2.6.p1: DESeq2, BH-adjusted p; S3.1.p1 applies |log2FC| > 1.5 and p-adj < .05 to every human cohort"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID40693573 / PMC12248044",
    "accessions": ["GSE151066"], "accession_locator": "S2.1.p1, DA.p1",
    "other_accessions": {"GSE87749": "hsYS cohort (Pattamaprapanont) - not requested here",
                         "GSE279359": "mouse LRS cohort - separate case"},
    "assay": "bulk short-read RNA-seq, vastus lateralis biopsies (Rubenstein et al. deposit); the paper re-quantified "
             "paired-end FASTQs with RSEM-STAR on GENCODE 42 (S2.5.p1)",
    "sample_inclusion": ["older adults 65-90 y, two cohorts: active/endurance-trained (hsAA, 10: 8M 2F) and sedentary "
                         "(hsAS, 9: 7M 2F) (S2.1.p1)",
                         "single 40-min cycling bout; biopsies pre and 3 h post exercise (S2.1.p1)",
                         "only males at pre and 3 h post with paired-end FASTQ were analysed (S2.1.p1, FIG1)"],
    "sample_exclusion": ["females", "the immediate-post-exercise time point deposited in GEO ('Post')"],
    "factors": [{"name": "cohort", "levels": ["sedentary (hsAS)", "active (hsAA)"], "locator": "S2.1.p1"},
                {"name": "time", "levels": ["pre", "3 h post"], "locator": "S2.1.p1"}],
    "primary_estimand": ("Acute-exercise effect on vastus lateralis gene expression (3 h post vs pre), estimated "
                         "separately within the sedentary (hsAS) and the active (hsAA) older cohort (S3.1.p1, FIG2B,D)."),
    "planned_contrasts": [
        {"name": "AS_3pe_vs_pre", "definition": "hsAS-3pe vs hsAS-pre, males", "locator": "S3.1.p1"},
        {"name": "AA_3pe_vs_pre", "definition": "hsAA-3pe vs hsAA-pre, males", "locator": "S3.1.p1"}],
    "blocking_or_covariance": {"status": "not_reported",
                               "note": "same subjects biopsied pre and post; the paper does not state a paired design"},
    "matrix_scale": "RSEM expected counts imported with tximport (counts, abundance, length) (S2.5.p1, S2.6.p1)",
    "paper_method": "tximport (gene level) -> DESeq2, BH-adjusted p (S2.6.p1); formula not reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "reported_counts": {"AS_3pe_vs_pre": "201 up + 9 down = 210 of 14082 detected genes (S3.1.p1)",
                        "AA_3pe_vs_pre": "112 up + 4 down = 116 of 14315 detected genes (S3.1.p1)",
                        "top_genes": "up in both: PPARGC1A, NR4A3, HSPA1B; NR4A1 up in hsAA (S3.1.p1)"},
    "enrichment": {"method": "DAVID over-representation on all significantly up-regulated genes (|log2FC|>1.5, padj<.05); "
                             "hsAS 204 GO terms, hsAA 149 terms; common: skeletal muscle cell differentiation, "
                             "negative regulation of apoptotic process (S2.6.p3, S3.1.p1)"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "quantification", "paper": "own RSEM-STAR on GENCODE 42, paired-end FASTQ, tximport with lengths (S2.5.p1)",
     "data": "GEO deposit: depositor's RSEM v1.2.22 hg38 gene expected counts (Ensembl IDs plus EBV genes and ERCC/spike rows); "
             "no abundance/length matrices", "classification": "requires_explicit_deviation",
     "note": "DESeq2 on the rounded deposited expected counts with size factors only; tximport length offsets cannot be reproduced"},
    {"item": "pairing", "paper": "not stated", "data": "every subject has pre, post and 3hrPost samples",
     "classification": "executable_without_change", "note": "subject blocking used (skill rule for repeated measures)"},
    {"item": "matrix columns", "paper": "-", "data": "78 matrix columns vs 57 GEO samples; 21 extra columns not in GEO",
     "classification": "executable_without_change", "note": "extra columns dropped by exact title alignment"},
    {"item": "library prep batch", "paper": "not mentioned",
     "data": "two sequencing pools (title prefix 1-61 / 62-121); GEO protocol: 15 sedentary samples lacked rRNA/globin depletion",
     "classification": "executable_without_change",
     "note": "pool is constant within subject for every analysed male except one active subject; absorbed by the subject block"},
    {"item": "detected genes", "paper": "14082 (hsAS) and 14315 (hsAA) detected genes; filter not described",
     "data": "60725 Ensembl genes", "classification": "executable_without_change",
     "note": "no pre-filter beyond non-zero; DESeq2 independent filtering decides the tested set"},
    {"item": "threshold wording", "paper": "'log2FC > 1.5' (S3.1.p1)", "data": "-",
     "classification": "executable_without_change", "note": "taken literally as |log2FC| > 1.5 on the log2 scale"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE151066"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"],
                   "sample_inclusion": study_map["sample_inclusion"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.1.p1"}, confidence="high",
            reasoning=("GSE151066 is the Rubenstein deposit re-analysed by the paper (S2.1.p1, DA.p1). Planned: 3 h post vs "
                       "pre within each older cohort, males only. DESeq2 after tximport, |log2FC| > 1.5 and BH padj < .05."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
ct = pd.crosstab([meta["characteristics_ch1.0.cohort"], meta["characteristics_ch1.3.gender"]],
                 meta["characteristics_ch1.1.time.point"])
own = {"series_id": sorted(meta.series_id.astype(str).unique().tolist()), "n_samples": int(len(meta)),
       "cohort_sex_by_time": {f"{a}|{b}": r.to_dict() for (a, b), r in ct.iterrows()},
       "subjects": int(meta["characteristics_ch1.2.subject.id"].nunique()),
       "organism": meta.organism_ch1.unique().tolist(), "tissue": meta.source_name_ch1.unique().tolist(),
       "processing": "STAR 2.5.2b + RSEM 1.2.22, hg38 (GEO data_processing)"}
case.decide("ownership",
            final={"accession": "GSE151066", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "S2.1.p1"}, confidence="high",
            reasoning=("GEO series GSE151066 (Rubenstein, Mount Sinai) = paper's cited accession. 19 subjects: Active 8M+2F, "
                       "Sedentary 7M+2F, each with Pre/Post/3hrPost vastus lateralis - matches the cohort sizes in S2.1.p1. "
                       "The paper re-used the deposit (not its own); the counts file is the depositor's quantification."))

# ---------------------------------------------------------------- 3 alignment
aln = native.align_to_metadata(MATRIX, META, case.dir / "aligned", key_column="title")
print("alignment", {k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
assert aln["coverage"] == 1.0, aln
dpath = case.dir / "aligned" / "design_metadata.csv"
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], dpath,
    aliases={"subject": "characteristics_ch1.2.subject.id"},
    patterns={"cohort": ("characteristics_ch1.0.cohort", r"^(Sedentary|Active)$"),
              "time": ("characteristics_ch1.1.time.point", r"^(Pre|Post|3hrPost)$"),
              "sex": ("characteristics_ch1.3.gender", r"^(Male|Female)$"),
              "pool": ("title", r"^Samples-(1-61|62-121)-")},
    recode={"cohort": {"Sedentary": "sed", "Active": "act"}, "time": {"Pre": "pre", "Post": "ip", "3hrPost": "h3"},
            "sex": {"Male": "male", "Female": "female"}, "pool": {"1-61": "p1", "62-121": "p2"}})
dm = pd.read_csv(dpath, index_col=0)
design_meta = case.add_output(dpath, "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.write_json("aligned/derived_columns.json", derived, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_metadata": aln["unmatched_metadata_samples"],
                   "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "derived_columns": ["subject", "cohort", "time", "sex", "pool"],
                   "levels": {c: dm[c].astype(str).value_counts().to_dict() for c in ["cohort", "time", "sex", "pool"]}},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.1.p1"}, confidence="high",
            reasoning=("Matrix columns equal GEO titles (Samples-<pool>-<barcode>); 57/57 metadata samples matched exactly. "
                       "21 matrix columns have no GEO sample and are dropped. Not aligned by position."))

# ---------------------------------------------------------------- 4 matrix
am_path = aln["outputs"]["aligned_matrix"]["path"]
prof = native.profile_matrix(am_path)
am = pd.read_csv(am_path, index_col=0)
prof_short = {k: prof.get(k) for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                       "missing_values", "negative_values", "candidates")}
prof_short["library_sizes_millions"] = [round(float(am.sum().min()) / 1e6, 2), round(float(am.sum().max()) / 1e6, 2)]
prof_short["non_ensembl_rows"] = int((~am.index.str.startswith("ENSG")).sum())
prof_short["ercc_spike_total"] = float(am.loc[am.index.str.match(r"^(ERCC-|Spike)")].sum().sum())
prof_short["feature_ids"] = native.feature_id_report(am_path)
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
print("profile", json.dumps(prof_short, default=str)[:900])
case.decide("matrix",
            final={"matrix_type": "estimated counts", "recommended_method": "DESeq2 on rounded expected counts (paper route via tximport)",
                   "profile": prof_short, "rounding_documented": True,
                   "rounding_note": ("RSEM expected counts; the paper imported them with tximport into DESeq2 "
                                     "(S2.6.p1), whose DESeqDataSetFromTximport rounds the counts to integers. "
                                     "Rounding with round() is applied at execution; the tximport length offset is not "
                                     "available in the deposit."),
                   "provenance": "STAR 2.5.2b + RSEM 1.2.22 genes expected_count (GEO data_processing)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.6.p1"}, confidence="high",
            reasoning=(f"Non-negative, no missing values, integer fraction {prof.get('integer_fraction')}, max "
                       f"{prof.get('max')}, library sizes {prof_short['library_sizes_millions']} M: RSEM expected "
                       f"counts, not normalized. {prof_short['non_ensembl_rows']} non-Ensembl rows (EBV genes, ERCC/spike) "
                       "are not human genes and are dropped at execution."))

# ---------------------------------------------------------------- 5 design
males = dm[dm["sex"] == "male"].copy()
# sex check: give the suitability report a copy with human marker symbols in the index
markers = {"ENSG00000229807": "Xist", "ENSG00000067048": "Ddx3y", "ENSG00000183878": "Uty",
           "ENSG00000012817": "Kdm5d", "ENSG00000129824": "Rps4y1"}
sx = am.loc[am.index.str.startswith("ENSG")].rename(index=markers)
sx_path = case.dir / "aligned" / "aligned_matrix_sexmarkers.csv"
sx.to_csv(sx_path)
# full-sample sex check on all 57, then the suitability report on the paper's analysis set (males)
from tools import suitability as su
sexcheck = su.check_sex(sx_path, dm, organism="Human", out_dir=case.dir / "suitability_sex_all")
sexcheck.pop("sex_by_sample", None)
case.write_json("sex_check_all_samples.json", sexcheck, role="sex_check")
print("sex check all", json.dumps({k: sexcheck.get(k) for k in ("status", "predicted", "mismatched", "uncertain")}))
refs = {"time": "pre", "cohort": "sed"}
planned = ["time_h3_vs_pre_cohort-sed", "time_h3_vs_pre_cohort-act"]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="estimated counts", metadata=males, factors=["cohort", "time"],
    matrix_csv=str(sx_path), organism="Human", subject="subject", covariate_candidates=["pool"],
    references=refs, planned=planned)
comps = [{k: c.get(k) for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
for c in comps:
    print("  ", c["name"], c["kind"], c["analyzable"])
names = [c["name"] for c in comps]
assert all(p in names for p in planned), names
time_within = [n for n in names if n.startswith("time_") and n not in planned]
cohort_within = [n for n in names if n.startswith("cohort_")]
inter = [n for n in names if n.startswith("cohort_time") or ":" in n or "interaction" in n]
case.write_json("suitability_comparisons.json", {"comparisons": comps, "planned": planned}, role="suitability_comparisons")
LABEL = {"time_h3_vs_pre_cohort-sed": "AS_3pe_vs_pre", "time_h3_vs_pre_cohort-act": "AA_3pe_vs_pre"}
contrasts = [{"name": LABEL[p], "suitability_name": p, "role": "paper_planned",
              "fit": "per-cohort DESeq2 ~ subject + time on males, pre and h3 only (paper's per-cohort comparison)"}
             for p in planned]
contrasts += [{"name": n, "suitability_name": n, "role": "exploratory",
               "fit": "per-cohort DESeq2 ~ subject + time on males, all three time points"} for n in time_within]
contrasts += [{"name": "change_h3_sed_vs_act", "suitability_name": "cohort:time interaction (h3 vs pre)",
               "role": "exploratory",
               "fit": "limma paired_change on log2(CPM+1): (h3 - pre) per subject, ~ C(cohort)"}]
skipped = ([{"name": n, "reason": "between-cohort comparison at a fixed time is cross-sectional (associational), "
                                  "not an exercise effect; outside the request"} for n in cohort_within if n not in inter]
           + [{"name": "per-sex analyses", "reason": "paper analysed males only; females 2 per cohort (< 3), not analyzable"},
              {"name": "ip_vs_pre interaction", "reason": "not requested by the paper; h3 interaction kept as the one "
                                                          "training-status contrast"}])
case.decide("design",
            final={"analysis_type": "repeated (paired pre/post within subject), analysed per cohort",
                   "formula": "~ subject + time (per cohort)", "design_column": "time",
                   "control": "pre", "treatment": "h3",
                   "contrasts": contrasts, "skipped_comparisons": skipped,
                   "analysis_set": {"sex": "male", "n_subjects": {"sed": int(males[males.cohort == 'sed'].subject.nunique()),
                                                                   "act": int(males[males.cohort == 'act'].subject.nunique())}},
                   "estimand_type": "interventional within subject (pre vs post acute bout); cohort comparison associational",
                   "suitability": suit_summary},
            candidates=[
                {"value": "pool sedentary and active cohorts", "reason_rejected": "paper reports each cohort separately"},
                {"value": "include females", "reason_rejected": "paper restricted to males (S2.1.p1)"},
                {"value": "unpaired pre vs h3", "reason_rejected": "same subjects sampled twice; repeated measures need the subject block"},
                {"value": "one fixed model ~ subject + cohort*time", "reason_rejected": "cohort is constant within subject (aliased with subject); "
                                                                                        "training-status difference fitted by paired_change instead"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "S3.1.p1"}, confidence="high",
            reasoning=("Planned: h3 vs pre within each cohort, males (7 sedentary, 8 active subjects, complete pre/h3). "
                       "Same subject at each time point, so time is within-subject. Exploratory: other time contrasts "
                       "within each cohort and the cohort difference in the 3 h response."))

# ---------------------------------------------------------------- 6 covariance
pr = {c: native.pairing_report(males[males.cohort == c], "subject", "time", ["pre", "h3"]) for c in ["sed", "act"]}
conf = {c: native.confounding_report(males[(males.cohort == c) & males.time.isin(["pre", "h3"])], "time", ["pool", "subject"])
        for c in ["sed", "act"]}
pool_var = (males[males.time.isin(["pre", "h3"])].groupby("subject")["pool"].nunique() > 1)
dc = {c: native.design_check(males[(males.cohort == c) & males.time.isin(["pre", "h3"])], ["subject", "time"]) for c in ["sed", "act"]}
dc_short = {c: {k: d.get(k) for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df",
                                       "min_cell_size")} for c, d in dc.items()}
case.write_json("covariance_reports.json", {"pairing": pr, "confounding": conf, "design_check": dc_short,
                                            "subjects_with_pool_change_pre_h3": pool_var[pool_var].index.tolist()},
                role="covariance_reports")
print(json.dumps({"pairing": pr, "design": dc_short, "pool_varies": pool_var[pool_var].index.tolist()}, default=str)[:1500])
assert all(d["full_rank"] for d in dc.values())
case.decide("covariance",
            final={"status": "required", "blocking_terms": ["subject"],
                   "covariates": [{"name": "subject", "disposition": "included (blocking term)"},
                                  {"name": "pool", "disposition": "excluded: sequencing pool/depletion batch is constant within "
                                                                  "subject for all but one active subject, so the subject block absorbs it; "
                                                                  "not modelled by the paper"},
                                  {"name": "sex", "disposition": "excluded: analysis set is males only"},
                                  {"name": "cohort", "disposition": "nested: between-subject, analysed per cohort"}],
                   "pairing": {c: {k: v for k, v in r.items() if k in ("complete", "incomplete", "duplicated", "n_complete")}
                               for c, r in pr.items()},
                   "design_check": dc_short},
            evidence=[design_meta, paper], paper={"locator": "S2.1.p1"}, confidence="high",
            reasoning=("Each male subject has one pre and one 3 h sample; subject is a required block. ~ subject + time is "
                       f"full rank in both cohorts with residual df {[d['residual_df'] for d in dc_short.values()]}."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 Wald test, BH, independent filtering) ~ subject + time, per cohort",
                   "matrix_type": "estimated counts", "rounding_documented": True,
                   "formula": "~ subject + time",
                   "transform": "round(expected counts) to integers; Ensembl human genes only (EBV, ERCC/spike rows dropped)",
                   "executor": "tools.deseq2_tools:run_deseq2_analysis (covariate_columns='subject') on per-cohort subsets",
                   "exploratory_executors": ["tools.joint_contrasts:run_joint_deseq2 (covariates=['subject']) per cohort on pre/ip/h3",
                                             "tools.multigroup_tools:run_multigroup_analysis paired_change on log2(CPM+1) "
                                             "from preprocess_counts (transform log2(CPM+1))"],
                   "paper_route": {"method": "DESeq2 on tximport (RSEM counts with length offsets) from own GENCODE 42 quantification",
                                   "status": "blocked",
                                   "reason": "only the depositor's gene expected counts are in GEO; no length/abundance matrix"}},
            evidence=[aligned_mat, paper], paper={"locator": "S2.6.p1"}, confidence="high",
            reasoning="Paper method (DESeq2) on the deposited RSEM counts, rounded as tximport/DESeq2 does; length offsets unavailable -> declared deviation.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": dict(paper_threshold),
                   "deviation_note": "paper rule applied unchanged; route differs only in quantification input (no tximport length offsets)",
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0,
                                         "label": "audit: paper's relaxed rule used for the mouse cohort (S3.1.p2)"},
                                        {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}]},
            evidence=[paper], paper={"locator": "S3.1.p1"}, confidence="high",
            reasoning="S3.1.p1: log2FC > 1.5 (or < -1.5) and BH p-adj < .05 for each human cohort.")
print("done gates 1-8 for", CASE)
