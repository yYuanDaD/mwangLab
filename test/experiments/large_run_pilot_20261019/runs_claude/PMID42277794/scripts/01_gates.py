"""Gates 1-8 (paper_reconstruction .. threshold) for GSE263186 / PMID42277794."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import numpy as np
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42277794"
CASE = "PMID42277794"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13479974.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13479974.paper.md"
TAR = "data/GSE263186/GSE263186_RAW.tar"
MATRIX = "data/GSE263186/GSE263186_merged_from_tar.csv"
META = "data/GSE263186/GSE263186_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE263186 for PMID 42277794 (Exercise reduces hepatic pre-metastatic niche formation via TREM-1 "
             "signaling in kupffer cells): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE263186")
pre = pathlib.Path("test/experiments/large_run_pilot_20261019/preflight.json")
if pre.exists():
    (pathlib.Path(RUN) / "preflight.json").write_text(pre.read_text(encoding="utf-8"), encoding="utf-8")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
tar_ev = case.add_input(TAR, "matrix")
mat_ev = case.add_input(MATRIX, "matrix")

FC = 1.5
paper_threshold = {"metric": "FDR", "adjustment": "BH (DESeq2 default; method not named)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": math.log2(FC),
                   "effect_cutoff_original": "fold change > 1.5 (S2.15.p1); FIG4 legend: |fold-change| >= 1.5",
                   "inclusive": False, "source_locator": "S2.15.p1; FIG4"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID42277794 / PMC13479974 (BMC Medicine 2026, doi 10.1186/s12916-026-04885-x)",
    "accessions": ["GSE263186"], "accession_locator": "S2.15.p3, DA.p1",
    "assay": "bulk RNA-seq of F4/80+ MACS-isolated Kupffer cells, Illumina NextSeq 550; Trimmomatic -> STAR (mm10) read counts (S2.15.p1)",
    "sample_inclusion": ["male C57BL/6, 8-10 wk, randomised to 4 wk treadmill ExT or SED (S2.1.p1)",
                         "KCs from SED-control, EXT-control, SED-cancer-exosome and EXT-cancer-exosome mice, n = 3 per group (S2.15.p1)"],
    "sample_exclusion": ["FIG4A legend: SED-control n = 2 in the ExT-control vs SED-control volcano; which sample was dropped, and why, is not reported"],
    "factors": [{"name": "ex", "levels": ["SED", "EXT"], "type": "between-animal, randomised (S2.1.p1)"},
                {"name": "exo", "levels": ["ctrl", "exo"], "type": "between-animal: in vivo cancer-exosome pre-education vs control (S2.4, S3.4.p1)"}],
    "primary_estimand": ("Effect of 4-week treadmill exercise training on the Kupffer-cell transcriptome, (A) at baseline "
                         "(ExT-control vs SED-control) and (B) under cancer-exosome education (ExT-exosome vs SED-exosome) "
                         "(FIG4A-B, S3.4.p1). Secondary: exosome effect within SED (Fig. S5E, S3.4.p1)."),
    "planned_contrasts": [
        {"name": "A_ExTctrl_vs_SEDctrl", "definition": "EXT-control vs SED-control", "locator": "FIG4A, S3.4.p1"},
        {"name": "B_ExTexo_vs_SEDexo", "definition": "EXT-exosome vs SED-exosome", "locator": "FIG4B, S3.4.p1"},
        {"name": "C_SEDexo_vs_SEDctrl", "definition": "SED-exosome vs SED-control (IPA TREM-1 up; GSEA inflammatory)", "locator": "S3.4.p1 (Additional file 3 Fig. S5A-E)"}],
    "exploratory_contrasts": ["EXT-exosome vs EXT-control", "interaction (exercise x exosome)"],
    "blocking_or_covariance": {"status": "not_required: one KC sample per mouse, independent groups", "locator": "S2.15.p1"},
    "matrix_scale": "STAR gene read counts (S2.15.p1; GEO data_processing)",
    "paper_method": "R/Bioconductor DESeq2 (S2.15.p1); model formula and whether pairwise or joint not reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "reported_counts": {"A_ExTctrl_vs_SEDctrl": "not_reported (volcano FIG4A only, no count in text)",
                        "B_ExTexo_vs_SEDexo": "not_reported (volcano FIG4B only)",
                        "C_SEDexo_vs_SEDctrl": "not_reported"},
    "enrichment": {"GSEA": "GSEA Java v4.3.2, h.all.v2023.2.Hs, mouse->human ortholog chip, 1000 permutations, FDR q < 0.25 (S2.15.p2)",
                   "IPA": "Ingenuity on DEGs, FDR 5% (S2.15.p1)",
                   "reported": "inflammatory pathways (TNFa via NFkB, inflammatory response) up with exosome in SED, reversed by ExT; ExT reverses bile acid / xenobiotic / fatty acid metabolism / cholesterol homeostasis dysregulation (S3.4.p1, S4.p6)"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "SED-control sample set", "paper": "S2.15.p1: n = 3 per group; FIG4A: SED-control n = 2",
     "data": "GEO deposits 3 SED-control libraries (GSM8187306-08). GSM8187308 (SED-Control-3) correlates 0.86-0.91 with all other libraries vs 0.93-0.98 among the rest (log2CPM QC), the likeliest dropped sample, but the paper does not name it",
     "classification": "requires_explicit_deviation",
     "note": "Primary run keeps all 3 deposited SED-control libraries (the Methods design); a labelled audit drops GSM8187308 to approximate FIG4A. Affects contrasts A and C only."},
    {"item": "model", "paper": "DESeq2, formula not reported", "data": "2x2 between-animal design, 12 samples",
     "classification": "executable_without_change",
     "note": "one DESeq2 model ~ cell on all 12 samples (skill rule for multi-factor designs); pairwise 6-sample fits as audit"},
    {"item": "implementation", "paper": "R DESeq2", "data": "pydeseq2 (same model family; no lfcShrink stated in paper)",
     "classification": "executable_without_change"},
    {"item": "threshold wording", "paper": "S2.15.p1 'FDR = 5% and fold change > 1.5'", "data": "FIG4 legend '|fold-change| >= 1.5'",
     "classification": "executable_without_change", "note": "strict inequalities from Methods applied; >= changes nothing in practice"},
    {"item": "GSEA library", "paper": "human Hallmark h.all v2023.2 via ortholog chip, GSEA Java permutation",
     "data": "repository GSEA: gseapy prerank on MSigDB mouse Hallmark mh.all 2024.1.Mm, ranked by Wald stat",
     "classification": "requires_explicit_deviation"},
    {"item": "IPA", "paper": "Ingenuity Pathway Analysis (TREM-1 pathway)", "data": "proprietary, no executor",
     "classification": "blocks_reproduction", "note": "IPA pathway results not reproduced; TREM-1 pathway genes (Trem1, etc.) inspected directly in DE tables"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE263186"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "exploratory_contrasts": study_map["exploratory_contrasts"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"],
                   "sample_exclusion": study_map["sample_exclusion"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning=("GSE263186 is the paper's deposit (S2.15.p3, DA.p1). 2x2 between-animal design (SED/ExT x "
                       "control/cancer exosome), KC bulk RNA-seq, n=3 per group (S2.15.p1). The exercise estimand is "
                       "ExT vs SED within control (FIG4A) and within exosome (FIG4B). DESeq2, DEGs at FDR 5% and FC > 1.5. "
                       "FIG4A reports SED-control n=2 without saying which sample was dropped. No DEG counts in text."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "treatment": meta["characteristics_ch1.3.treatment"].value_counts().astype(int).to_dict(),
       "cell_type": meta["characteristics_ch1.1.cell type"].unique().tolist(),
       "organism": meta.organism_ch1.unique().tolist(), "platform": meta.platform_id.unique().tolist(),
       "instrument": meta.instrument_model.unique().tolist(), "data_processing": meta.data_processing.iloc[0],
       "contact": "Ruiqi Yang, Samer Tohme lab, Surgery, University of Pittsburgh",
       "supplementary": "GSE263186_RAW.tar: 12 GSM*_<group>-<rep>.STAR.ReadsPerGene.out.tab.gz (one per GSM)"}
case.decide("ownership",
            final={"accession": "GSE263186", "matrix_file": MATRIX, "matrix_source": TAR, "metadata_file": META,
                   "owned": True, "checks": own},
            evidence=[meta_ev, tar_ev, mat_ev, paper], paper={"locator": "S2.15.p3"}, confidence="high",
            reasoning=("Series GSE263186 = paper accession; 12 mouse Kupffer-cell libraries, 4 treatment groups x 3, "
                       "NextSeq 550, Trimmomatic/STAR/mm10 as in S2.15.p1; University of Pittsburgh, as the IACUC protocol (S2.1.p1)."))

# ---------------------------------------------------------------- 3 alignment
kpath = case.dir / "aligned" / "metadata_keyed.csv"
keyed = native.derive_columns(META, kpath, patterns={
    "mkey": ("supplementary_file_1", r"/(GSM\d+_[^/]+)\.ReadsPerGene\.out\.tab\.gz$")})
aln = native.align_to_metadata(MATRIX, str(kpath), case.dir / "aligned", key_column="mkey")
assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    patterns={"ex": ("title", r"^(SED|EXT)-"),
              "exo": ("title", r"^(?:SED|EXT)-(control|cancer exosome injection) bio"),
              "trt_ex": ("characteristics_ch1.3.treatment", r"^(Sendentary|SED|exercise)"),
              "rep": ("title", r"rep ?(\d)$")},
    recode={"exo": {"control": "ctrl", "cancer exosome injection": "exo"},
            "trt_ex": {"Sendentary": "SED", "SED": "SED", "exercise": "EXT"}})
dm = pd.read_csv(derived["output"], index_col=0)
trt_exo = dm["characteristics_ch1.3.treatment"].str.contains("exosome").map({True: "exo", False: "ctrl"})
assert (dm.ex == dm.trt_ex).all() and (dm.exo == trt_exo).all(), dm
dm["grp"] = dm.ex + "_" + dm.exo
dm.to_csv(derived["output"])
derived["levels"] = {c: dm[c].astype(str).value_counts().to_dict() for c in ["grp", "ex", "exo"]}
derived["key"] = ("matrix column 'GSM8187306_SED-Control-1.STAR' = basename of GEO supplementary_file_1 without "
                  "'.ReadsPerGene.out.tab.gz' -> metadata column mkey; ex/exo from title, cross-checked against "
                  "characteristics treatment")
design_meta = case.add_output(derived["output"], "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.write_json("aligned/derived_columns.json", {"key": keyed, "design": derived}, role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln["unmatched_matrix_columns"],
                   "key_derivation": derived["key"], "derived_columns": ["ex", "exo", "grp", "rep"],
                   "levels": derived["levels"]},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning=("Each tar member is the GSM's own supplementary file; 12/12 exact on the file-name key. "
                       "Title-derived ex/exo agree with the characteristics treatment for every sample."))

# ---------------------------------------------------------------- 4 matrix
am_path = aln["outputs"]["aligned_matrix"]["path"]
prof = native.profile_matrix(am_path)
prof_short = {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                   "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
am = pd.read_csv(am_path, index_col=0)
prof_short["library_sizes_millions"] = (am.sum() / 1e6).round(2).to_dict()
prof_short["star_strand"] = "reverse column of ReadsPerGene (forward 0.75 M vs reverse 64.4 M reads over 12 samples, ratio 86; native.merge_raw_tar)"
prof_short["feature_ids"] = native.feature_id_report(am_path)
cpm = am / am.sum() * 1e6
lc = np.log2(cpm[(cpm >= 1).sum(axis=1) >= 3] + 1)
corr = lc.corr()
prof_short["qc_mean_corr_to_others"] = ((corr.sum() - 1) / (len(corr) - 1)).round(3).to_dict()
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2 (paper route)", "profile": prof_short,
                   "provenance": "STAR --quantMode GeneCounts per-sample ReadsPerGene.out.tab (GEO supplementary; S2.15.p1)"},
            evidence=[aligned_mat, tar_ev, meta_ev, paper], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning=(f"All values integer (fraction {prof['integer_fraction']}), non-negative, max {prof['max']:.0f}; "
                       "STAR ReadsPerGene counts from a stranded (reverse) library; library sizes 3.3-7.0 M assigned reads. "
                       "Matches the paper's STAR count matrix analysed by DESeq2."))

# ---------------------------------------------------------------- 5 design
refs = {"ex": "SED", "exo": "ctrl"}
planned = ["ex_EXT_vs_SED_exo-ctrl", "ex_EXT_vs_SED_exo-exo", "exo_exo_vs_ctrl_ex-SED"]
rep, suit_item, suit_summary = case.suitability(
    matrix_type="raw counts", metadata=dm, factors=["ex", "exo"], matrix_csv=am_path, organism="Mouse",
    subject=None, references=refs, planned=planned)
comps = [{k: c[k] for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
names = {c["name"] for c in comps}
assert all(p in names for p in planned), names
exploratory = [c["name"] for c in comps if c["name"] not in planned]
case.write_json("suitability_comparisons.json", {"comparisons": comps, "planned": planned, "exploratory": exploratory},
                role="suitability_comparisons")
label = {planned[0]: "A_ExTctrl_vs_SEDctrl", planned[1]: "B_ExTexo_vs_SEDexo", planned[2]: "C_SEDexo_vs_SEDctrl"}
case.decide("design",
            final={"analysis_type": "factorial 2x2 between-animal (exercise x exosome), fitted as a 4-cell means model on all 12 samples",
                   "formula": "~ cell  (cell = ex x exo)", "design_column": "grp",
                   "contrasts": ([{"name": label[p], "suitability_name": p, "role": "paper_planned",
                                   "control": p.split("_vs_")[1].split("_")[0], "estimand_type": "interventional (randomised)"} for p in planned]
                                 + [{"name": e, "suitability_name": e, "role": "exploratory"} for e in exploratory]),
                   "primary_exercise_contrasts": ["A_ExTctrl_vs_SEDctrl", "B_ExTexo_vs_SEDexo"],
                   "suitability": suit_summary},
            candidates=[
                {"value": "pool exosome and control to ExT vs SED", "reason_rejected": "paper reports exercise effects separately within control and exosome (FIG4A-B)"},
                {"value": "drop one SED-control to match FIG4A n=2", "reason_rejected": "paper does not identify the sample; kept as a labelled audit (QC outlier GSM8187308)"},
                {"value": "separate 6-sample pairwise fits", "reason_rejected": "skill rule: one model on all samples for multi-factor designs; run as audit"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "FIG4"}, confidence="high",
            reasoning=("Four independent groups of 3 mice. Exercise was randomised (S2.1.p1). The paper's exercise "
                       "contrasts are within exosome level (FIG4A-B); the exosome effect in SED is also analysed (S3.4.p1). "
                       "Suitability: analyzable, every cell n=3."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(derived["output"], "grp", ["rep"])
dc = native.design_check(derived["output"], ["grp"])
dc_short = {k: dc[k] for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
dc2 = native.design_check(derived["output"], ["ex", "exo"], interactions=[("ex", "exo")])
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short,
                                            "design_check_factorial": {k: dc2.get(k) for k in dc_short}},
                role="covariance_reports")
assert dc["full_rank"] and dc["residual_df"] >= 4
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "rep", "disposition": "excluded: replicate number within group, not a batch or animal key shared across groups (no evidence of batch)"},
                                  {"name": "sex/age/genotype/tissue", "disposition": "excluded: single level (male WT, liver KCs)"},
                                  {"name": "library size", "disposition": "excluded: handled by DESeq2 size factors"}],
                   "design_check": dc_short},
            evidence=[design_meta, paper], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning=(f"One KC library per mouse, independent groups, no repeated measures or batch column. ~ cell "
                       f"full rank ({dc['rank']}/{dc['n_columns']}), residual df {dc['residual_df']}."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2) joint model on all 12 samples, Wald tests of cell contrasts",
                   "matrix_type": "raw counts", "formula": "~ cell", "executor": "tools.joint_contrasts:run_joint_deseq2",
                   "independent_filtering": "pydeseq2 default (alpha = 0.05)", "lfc_shrinkage": "none (not stated in paper)",
                   "audits": ["pairwise 6-sample DESeq2 per planned contrast (tools.deseq2_tools:run_deseq2_analysis)",
                              "joint model without GSM8187308 (FIG4A n=2 approximation)"]},
            evidence=[aligned_mat, paper], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning="Paper route DESeq2 on STAR counts; the deposited matrix supports it directly.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": dict(paper_threshold),
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default (no FC cutoff)"}]},
            evidence=[paper], paper={"locator": "S2.15.p1"}, confidence="high",
            reasoning="Methods: DEGs at FDR 5% and fold change > 1.5 -> padj < 0.05 and |log2FC| > log2(1.5) = 0.5849625.")
print(json.dumps({"alignment": {k: aln[k] for k in ("method", "n_aligned", "coverage")}, "design_check": dc_short,
                  "qc_corr": prof_short["qc_mean_corr_to_others"], "comparisons": [c["name"] for c in comps]},
                 indent=1, default=str))
