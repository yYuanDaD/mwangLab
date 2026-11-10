"""Gates 1-8 (paper_reconstruction .. threshold) for GSE298775 / PMID40650303."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40650303"
CASE = "PMID40650303"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12249896.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12249896.paper.md"
MATRIX = "data/GSE298775/GSE298775_raw_counts.csv.gz"
META = "data/GSE298775/GSE298775_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE298775 for PMID 40650303 (Impact of Aerobic Training on Transcriptomic Changes in Skeletal "
             "Muscle of Rats with Cardiac Cachexia): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE298775")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

paper_threshold = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "inclusive": False,
                   "effect_metric": "log2FC", "effect_cutoff": 1.0, "effect_inclusive": True,
                   "effect_cutoff_original": "log2 fold-change magnitude of 1 or greater (|log2FC| >= 1)",
                   "source_locator": "S4.6.p2",
                   "note": "'BH corrected, Wilcoxon p-test' in S4.6.p2; DESeq2 uses a Wald test, the Wilcoxon wording is unexplained"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID40650303 / PMC12249896",
    "accessions": ["GSE298775"], "accession_locator": "DA.p1",
    "assay": "bulk poly-A RNA-seq (Illumina Stranded mRNA), NextSeq 2000 PE100; Salmon 1.10.2 -> tximport gene level (S4.5.p1, S4.6.p1)",
    "sample_inclusion": ["male Wistar rats, 2x2 between-animal design: saline/monocrotaline (CC) x sedentary/4-week aerobic treadmill training (S4.1.p1, S4.2.p1)",
                         "RNA-seq on left medial gastrocnemius of six animals per group -> 24 libraries (S4.5.p1)"],
    "sample_exclusion": ["which 6 of 9-12 animals per group were sequenced is not reported (S4.5.p1)"],
    "factors": [{"name": "dis", "levels": ["Ctl (saline)", "CC (monocrotaline 60 mg/kg)"], "locator": "S4.1.p1"},
                {"name": "ex", "levels": ["Sed", "Ex (treadmill 30 min ~55% max, 5x/wk, 4 wk)"], "locator": "S4.2.p1"}],
    "primary_estimand": ("Cardiac-cachexia (monocrotaline) effect on the gastrocnemius transcriptome within sedentary "
                         "(CC-Sed vs Sed) and within trained (CC-Ex vs Ex) rats; the paper infers that aerobic training "
                         "attenuates the CC signature by comparing the two (S2.2.p1-p2, ABS). The training effect itself "
                         "(Ex vs Sed, CC-Ex vs CC-Sed) and the disease x training interaction were not tested in the paper."),
    "planned_contrasts": [
        {"name": "CC_in_Sed", "definition": "CC-Sed vs Sed (reference Sed)", "locator": "S2.2.p1"},
        {"name": "CC_in_Ex", "definition": "CC-Ex vs Ex (reference Ex)", "locator": "S2.2.p1"}],
    "exploratory_contrasts": ["Ex vs Sed within saline", "CC-Ex vs CC-Sed within CC", "interaction (CC-Ex - CC-Sed) - (Ex - Sed)"],
    "blocking_or_covariance": {"status": "not_required", "note": "one muscle sample per animal, independent groups"},
    "matrix_scale": "Salmon/tximport gene-level counts, deposited as integer 'Raw counts of Salmon mapped reads' (GEO)",
    "paper_method": "DESeq2 v1.44.0 (S4.6.p2); model/fit structure (one 4-group fit vs pairwise) not reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "reported_counts": {"CC_in_Sed": "145 DEGs: 131 up, 14 down (S2.2.p2); abstract says 114 (ABS.p1)",
                        "CC_in_Ex": "18 DEGs: 16 up, 2 down (S2.2.p2, ABS.p1)",
                        "overlap": "13 shared DEGs, gas transport (S2.2.p2, TAB2)",
                        "top_genes": "CC-Sed up Tnnc1, Tpm3, Tnni1, Myl3, Nr4a3; CC-Ex up Hbb, Hba-a1, Hba-a3, Aqp4, Prodh; CC-Ex down Nrip3, Egr1 (S2.2.p3)"},
    "enrichment": {"method": "clusterProfiler GO and KEGG ORA on DEGs, padj<0.05 BH (S4.6.p2)", "locator": "S2.3"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "CC_in_Sed DEG count", "paper": "145 (131 up + 14 down) in S2.2.p2", "data": "abstract states 114",
     "classification": "executable_without_change", "note": "both numbers kept for comparison; 145 is the itemised count"},
    {"item": "test wording", "paper": "'BH corrected, Wilcoxon p-test' (S4.6.p2)", "data": "DESeq2 performs a Wald test",
     "classification": "executable_without_change", "note": "DESeq2 Wald test used; Wilcoxon not reproducible as described"},
    {"item": "count matrix", "paper": "tximport gene-level collapse into DESeq2 (likely DESeqDataSetFromTximport with length offsets)",
     "data": "GEO deposits integer gene counts only (10,851 Ensembl genes, already filtered by the authors); no abundance/length matrix",
     "classification": "requires_explicit_deviation", "note": "DESeq2 runs on the deposited integers with size factors only; any tximport length offsets cannot be reproduced"},
    {"item": "fit structure", "paper": "two comparisons; not stated whether one 4-group DESeq2 fit or two pairwise fits",
     "data": "24 samples, 4 groups of 6", "classification": "executable_without_change",
     "note": "primary: one model ~ cell on all 24 (skill rule); audit: pairwise 12-sample fits"},
    {"item": "sample selection", "paper": "9-12 animals per group, six per group sequenced", "data": "GEO 6 per group",
     "classification": "executable_without_change"},
    {"item": "exercise estimand", "paper": "training effect inferred from smaller CC signature in trained rats",
     "data": "Ex vs Sed and interaction are estimable", "classification": "executable_without_change",
     "note": "run as exploratory contrasts from the same model"},
    {"item": "enrichment", "paper": "GO/KEGG ORA in clusterProfiler for rat",
     "data": "repository ORA/GSEA libraries are Mouse/Human only; rat needs ortholog mapping",
     "classification": "requires_explicit_deviation", "note": "enrichment not run in this case"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE298775"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [c["name"] for c in study_map["planned_contrasts"]],
                   "exploratory_contrasts": study_map["exploratory_contrasts"],
                   "paper_threshold": paper_threshold, "paper_method": study_map["paper_method"],
                   "matrix_scale": study_map["matrix_scale"], "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S4.6.p2"}, confidence="high",
            reasoning=("GSE298775 is the paper's deposit (DA.p1). 2x2 between-animal design, 6 per group sequenced. "
                       "Planned: CC-Sed vs Sed and CC-Ex vs Ex (S2.2.p1). Threshold BH padj<0.05 and |log2FC|>=1 "
                       "(S4.6.p2). The request's exercise effect is the paper's comparison of the two disease signatures; "
                       "direct training contrasts and the interaction are exploratory."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.astype(str).unique().tolist()), "n_samples": int(len(meta)),
       "title_groups": meta.title.str.replace(r"\s*replicate\s*\d+$", "", regex=True).value_counts().to_dict(),
       "organism": meta.organism_ch1.unique().tolist(), "tissue": meta["characteristics_ch1.0.tissue"].unique().tolist(),
       "instrument": meta.instrument_model.unique().tolist(),
       "data_processing_mentions": "Salmon, tximport, DESeq2 v1.44.0, padj<0.05 & |log2FC|>=1 (verbatim as S4.6)",
       "supplementary": "GSE298775_raw_counts.csv.gz (only file)"}
case.decide("ownership",
            final={"accession": "GSE298775", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("Series GSE298775 = paper accession; 24 rat gastrocnemius samples, Saline/Monocrotaline x "
                       "Sedentary/Exercised, 6 each, NextSeq 2000; processing text repeats S4.6 verbatim."))

# ---------------------------------------------------------------- 3 alignment
kpath = case.dir / "aligned" / "metadata_keyed.csv"
keyed = native.derive_columns(
    META, kpath,
    patterns={"lib": ("description", r"^Library name: (\S+)$"),
              "dis": ("title", r"^(Saline|Monocrotaline)-"),
              "ex": ("title", r"-(Sedentary|Exercised) replicate"),
              "rep": ("title", r"replicate\s*(\d+)$")},
    recode={"dis": {"Saline": "Ctl", "Monocrotaline": "CC"}, "ex": {"Sedentary": "Sed", "Exercised": "Ex"}})
aln = native.align_to_metadata(MATRIX, str(kpath), case.dir / "aligned", key_column="lib")
print("alignment", {k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")}, aln.get("unmatched_matrix_columns"))
assert aln["coverage"] == 1.0, aln
dm = pd.read_csv(aln["outputs"]["aligned_metadata"]["path"], index_col=0)
dm["grp"] = dm["dis"] + "_" + dm["ex"]
dpath = case.dir / "aligned" / "design_metadata.csv"
dm.to_csv(dpath)
levels = {c: dm[c].astype(str).value_counts().to_dict() for c in ["grp", "dis", "ex"]}
design_meta = case.add_output(dpath, "design_metadata")
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
# gene symbol map (non-sample column in the deposited file) kept for reporting
raw = pd.read_csv(MATRIX, index_col=0)
sym = raw[["gene_symbol"]]
sym_path = case.dir / "aligned" / "gene_symbols.csv"
sym.to_csv(sym_path)
case.add_output(sym_path, "gene_symbol_map")
case.write_json("aligned/derived_columns.json", {"key": keyed, "grp": "dis + '_' + ex", "levels": levels},
                role="derived_columns")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln.get("unmatched_matrix_columns"),
                   "key_derivation": "matrix column = GEO description 'Library name: <lib>' -> lib; dis/ex/rep from title",
                   "derived_columns": ["lib", "dis", "ex", "rep", "grp"], "levels": levels,
                   "non_sample_columns": ["gene_symbol (annotation, kept as gene_symbols.csv)"]},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], paper={"locator": "S4.5.p1"}, confidence="high",
            reasoning="Matrix columns are the GEO library names; 24/24 exact matches on the derived lib key. Not by position.")

# ---------------------------------------------------------------- 4 matrix
am_path = aln["outputs"]["aligned_matrix"]["path"]
prof = native.profile_matrix(am_path)
am = pd.read_csv(am_path, index_col=0)
prof_short = {k: prof.get(k) for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                       "missing_values", "negative_values", "duplicated_feature_ids", "candidates")}
prof_short["library_sizes_millions"] = [round(float(am.sum().min()) / 1e6, 2), round(float(am.sum().max()) / 1e6, 2)]
prof_short["min_row_sum"] = int(am.sum(axis=1).min())
prof_short["feature_ids"] = native.feature_id_report(am_path)
case.write_json("matrix_profile.json", prof_short, role="matrix_profile")
print("profile", json.dumps(prof_short, default=str)[:800])
case.decide("matrix",
            final={"matrix_type": "estimated counts", "recommended_method": "DESeq2 (paper route)",
                   "profile": prof_short, "rounding_documented": True,
                   "rounding_note": ("deposited by the authors as integer 'Raw counts of Salmon mapped reads' after tximport "
                                     "(GEO data_processing); the integers are the authors' own DESeq2 input, no rounding done here"),
                   "provenance": "Salmon 1.10.2 -> tximport gene level (S4.6.p1, GEO data_processing)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S4.6.p1"}, confidence="high",
            reasoning=(f"Non-negative, integer fraction {prof.get('integer_fraction')}, max {prof.get('max')}, library sizes "
                       f"{prof_short['library_sizes_millions']} M; 10,851 genes (min row sum {prof_short['min_row_sum']}), "
                       "so the authors filtered low-expression genes before deposit. Salmon/tximport estimated counts "
                       "already rounded by the depositor."))

# ---------------------------------------------------------------- 5 design
refs = {"dis": "Ctl", "ex": "Sed"}
planned = ["dis_CC_vs_Ctl_ex-Sed", "dis_CC_vs_Ctl_ex-Ex"]
# sex check needs gene symbols in the index; give suitability a symbol-indexed copy
symmat = am.join(sym).dropna(subset=["gene_symbol"]).groupby("gene_symbol").sum()
symmat_path = case.dir / "aligned" / "aligned_matrix_symbols_for_sexcheck.csv"
symmat.to_csv(symmat_path)
dm["sex"] = "male"
rep, suit_item, suit_summary = case.suitability(
    matrix_type="estimated counts", metadata=dm, factors=["dis", "ex"],
    matrix_csv=str(symmat_path), organism="Rat", subject=None, references=refs, planned=planned)
comps = [{k: c.get(k) for k in ("name", "kind", "test", "reference", "within", "analyzable")} for c in rep["comparisons"]]
print("suitability", json.dumps(suit_summary, default=str))
names = [c["name"] for c in comps]
assert all(p in names for p in planned), names
exploratory = [n for n in names if n not in planned]
case.write_json("suitability_comparisons.json", {"comparisons": comps, "planned": planned, "exploratory": exploratory},
                role="suitability_comparisons")
LABEL = {"dis_CC_vs_Ctl_ex-Sed": "CC_in_Sed", "dis_CC_vs_Ctl_ex-Ex": "CC_in_Ex",
         "ex_Ex_vs_Sed_dis-Ctl": "Ex_in_Ctl", "ex_Ex_vs_Sed_dis-CC": "Ex_in_CC",
         "dis_ex_CC_Ex_vs_Ctl_Sed": "CCxEx_interaction"}
case.decide("design",
            final={"analysis_type": "factorial 2x2 between-animal (disease x training), fitted as a 4-cell means model on all 24 samples",
                   "formula": "~ cell  (cell = dis x ex)", "design_column": "grp",
                   "contrasts": ([{"name": LABEL[p], "suitability_name": p, "role": "paper_planned"} for p in planned]
                                 + [{"name": LABEL.get(e, e), "suitability_name": e, "role": "exploratory"} for e in exploratory]),
                   "estimand_type": "interventional (randomised to injection and training, S4.1.p1)",
                   "suitability": suit_summary},
            candidates=[
                {"value": "pool sedentary and exercised to CC vs Ctl", "reason_rejected": "paper reports training-state-specific CC effects"},
                {"value": "pairwise 12-sample fits only", "reason_rejected": "fit structure not reported; skill rule uses one model on all samples; pairwise kept as audit"},
                {"value": "interaction as primary", "reason_rejected": "paper does not test it; exploratory"}],
            evidence=[design_meta, suit_item, paper], paper={"locator": "S2.2.p1"}, confidence="high",
            reasoning=("Four independent groups of 6 rats; the paper's two comparisons are simple disease effects within "
                       "each training state. The exercise question is answered by the exploratory training contrasts and "
                       "the interaction from the same model."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(str(dpath), "grp", ["rep"])
dc = native.design_check(str(dpath), ["grp"])
dc_short = {k: dc.get(k) for k in ("formula_equivalent", "n_samples", "n_columns", "rank", "full_rank", "residual_df", "min_cell_size")}
case.write_json("covariance_reports.json", {"confounding": conf, "design_check": dc_short}, role="covariance_reports")
assert dc["full_rank"]
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "animal", "disposition": "excluded: one sample per animal, no repeated measures"},
                                  {"name": "rep", "disposition": "excluded: replicate index within group, not a batch"},
                                  {"name": "sex/tissue/batch", "disposition": "excluded: single level (male, gastrocnemius, one NextSeq run per GEO)"}],
                   "design_check": dc_short},
            evidence=[design_meta, paper], paper={"locator": "S4.5.p1"}, confidence="high",
            reasoning=f"~ 0 + grp full rank ({dc_short['rank']}/{dc_short['n_columns']}), residual df {dc_short['residual_df']}; no blocking unit.")

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2, Wald test, BH, independent filtering) ~ cell on all 24 samples",
                   "matrix_type": "estimated counts", "rounding_documented": True,
                   "formula": "~ cell (dis x ex, 4 levels)",
                   "executor": "tools.joint_contrasts:run_joint_deseq2",
                   "audit": "pairwise 12-sample DESeq2 fits (tools.deseq2_tools:run_deseq2_analysis) for the two planned contrasts",
                   "paper_route_note": "paper DESeq2 v1.44.0 in R; tximport length offsets (if used) not reproducible from the deposit"},
            evidence=[aligned_mat, paper], paper={"locator": "S4.6.p2"}, confidence="high",
            reasoning="Paper method on the authors' deposited integer counts.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": dict(paper_threshold),
                   "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_metric": None, "label": "audit: workflow default"}]},
            evidence=[paper], paper={"locator": "S4.6.p2"}, confidence="high",
            reasoning="S4.6.p2: BH padj < 0.05 and |log2FC| >= 1 (inclusive effect bound).")
print(json.dumps({"design_check": dc_short, "confounding": conf}, indent=1, default=str)[:1500])
