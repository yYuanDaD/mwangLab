"""Gates paper_reconstruction -> matrix for PMID41610852 / GSE312780."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math; os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852"
CASE = "GSE312780"
REQUEST = ("Analyze GSE312780 for PMID 41610852 (Blood-flow restriction resistance training improves skeletal "
           "muscle mitochondrial capacity and cardiovascular risk factors in type 2 diabetes): how exercise "
           "affects gene expression as the paper intends.")
run = native.RunRecorder(RUN, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5) subagent", case_ids=[CASE])
case = run.case(CASE, accession="GSE312780")

paper_md = case.add_input("test/experiments/paper_screen_20261019/papers/PMC13237580.paper.md", "paper")
paper_json = case.add_input("test/experiments/paper_screen_20261019/papers/PMC13237580.paper.json", "paper")
meta_in = case.add_input("data/GSE312780/GSE312780_metadata.csv", "metadata")
mat_in = case.add_input("data/GSE312780/GSE312780_salmon.merged.gene_counts.tsv.gz", "matrix")

FC = 1.5
paper_threshold = {"metric": "padj", "adjustment": "BH (DESeq2 default; method not named)", "cutoff": 0.05,
                   "effect_metric": "log2FC (apeglm-shrunken)", "effect_cutoff": 0.585,
                   "effect_cutoff_original": "|log2FC| >= 0.585 (Methods); |FC| > 1.5 (FIG4 legend)",
                   "inclusive": "padj strict (<), effect inclusive (>=)",
                   "source_locator": "S8.3.15.p1; FIG4"}
study_map = {
    "paper_id": "PMID41610852 / PMC13237580",
    "accessions": ["GSE312780"],
    "assay": "bulk RNA-seq, human vastus lateralis biopsies (nf-core/rnaseq 3.20.0, STAR+Salmon, GENCODE v44)",
    "sample_inclusion": ["T2D participants randomized to BFRT or CREST, biopsy before (week 0) and ~72 h after "
                         "12 weeks of training (S8.3.4.p1, S2.4.p2)"],
    "sample_exclusion": ["One BFRT participant excluded after visual PCA/correlation inspection; identity not "
                         "reported (S8.3.16.p2)",
                         "Resist19 excluded from analyses for elevated hsCRP (S8.3.1.p1); not in GEO"],
    "factors": [{"name": "cohort", "levels": ["BFRT", "CREST"]},
                {"name": "timepoint", "levels": ["week 0 (before)", "week 12 (after)"]},
                {"name": "person_within_cohort", "levels": "subject nested in cohort"}],
    "primary_estimand": "within-arm training effect on muscle gene expression (after vs before) in BFRT and "
                        "in CREST, plus the difference between arms (interaction)",
    "planned_contrasts": ["BFRT week12 vs week0", "CREST week12 vs week0",
                          "interaction: (BFRT after-before) - (CREST after-before)"],
    "blocking_or_covariance": {"status": "required", "term": "cohort:person_within_cohort (subject nested in arm)"},
    "matrix_scale": "counts from tximport lengthScaledTPM of salmon quant.sf (S8.3.15.p1)",
    "paper_method": "DESeq2 1.48.2 with apeglm LFC shrinkage; genes with < 10 total counts removed",
    "paper_formula": "~ cohort + cohort:person_within_cohort + cohort:timepoint",
    "paper_threshold": paper_threshold,
    "paper_reported_deg": {"BFRT week12 vs week0": 110, "CREST week12 vs week0": 18, "interaction": "not_reported"},
    "pathway": "KEGG GSEA (clusterProfiler gseKEGG, organism='mmu' as written although data are human)",
}
pr = case.write_json("paper_reconstruction.json", study_map)
discrepancies = [
    {"item": "sample exclusion", "paper": "one BFRT participant excluded after PCA (16 subjects analysed: 8 BFRT, 8 CREST)",
     "data": "GEO has 9 BFRT + 8 CREST subjects, 34 samples; excluded subject is not identified",
     "disposition": "requires_explicit_deviation"},
    {"item": "matrix", "paper": "tximport lengthScaledTPM counts from quant.sf",
     "data": "salmon.merged.gene_counts.tsv.gz (nf-core tximport counts without length scaling, non-integer)",
     "disposition": "requires_explicit_deviation"},
    {"item": "LFC shrinkage", "paper": "apeglm-shrunken log2FC used for the |log2FC| >= 0.585 cutoff",
     "data": "repository joint DESeq2 executor reports MLE log2FC only",
     "disposition": "requires_explicit_deviation"},
    {"item": "threshold wording", "paper": "Results S2.4.p2 says 'p < 0.05 and |FC| 1.5'; Methods S8.3.15.p1 and FIG4 say adjusted p < 0.05",
     "data": "-", "disposition": "executable_without_change (Methods/legend adjusted-p rule applied; raw-p as audit)"},
    {"item": "GSEA organism", "paper": "gseKEGG organism='mmu' for human data", "data": "human gene IDs",
     "disposition": "executable_without_change (enrichment uses human sets)"},
]
dsc = case.write_json("paper_data_discrepancies.json", discrepancies)
case.decide("paper_reconstruction",
            final={"accessions": ["GSE312780"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": study_map["planned_contrasts"], "paper_threshold": paper_threshold,
                   "paper_method": study_map["paper_method"], "paper_formula": study_map["paper_formula"],
                   "sample_exclusion": study_map["sample_exclusion"],
                   "paper_reported_deg": study_map["paper_reported_deg"]},
            evidence=[paper_md, paper_json, pr, dsc], paper={"locator": "S8.3.15.p1; S8.3.16.p2; S2.4.p2; FIG4; S4.3.p1"},
            reasoning="Methods give DESeq2 nested-subject model with per-arm time effects and interaction; "
                      "threshold padj<0.05 & |log2FC|>=0.585; 110 BFRT and 18 CREST DEGs reported.",
            confidence="high")

# ownership
meta = pd.read_csv(meta_in["path"], index_col=0)
case.decide("ownership",
            final={"accession": "GSE312780", "matrix_file": mat_in["path"], "metadata_file": meta_in["path"],
                   "owned": True, "series_id": sorted(meta["series_id"].unique().tolist()),
                   "n_samples": int(len(meta)), "n_subjects": int(meta["title"].str.split("_").str[0].nunique()),
                   "arms": meta["characteristics_ch1.1.treatment"].value_counts().to_dict()},
            evidence=[meta_in, mat_in, paper_md], paper={"locator": "S4.3.p1"},
            reasoning="Paper data-availability names GSE312780; metadata series_id GSE312780; titles ResistNN_<BFRT|CREST>_<Before|After> "
                      "match the paper's participant codes (Resist19, Resist48 cited in S8.3.1); matrix file is the series supplement. "
                      "17 subjects x 2 timepoints = 34 vs paper's 16 analysed (one BFRT exclusion unidentified).",
            confidence="high")

# alignment: matrix columns S1..S34 are library names in metadata 'description'
keyed = native.derive_columns(meta_in["path"], case.dir / "aligned" / "metadata_keyed.csv",
                              patterns={"library": ("description", r"Library name: (S\d+),")})
aln = native.align_to_metadata(mat_in["path"], keyed["output"], case.dir / "aligned", key_column="library")
amat = case.add_output(aln["outputs"]["aligned_matrix"]["path"] if isinstance(aln["outputs"]["aligned_matrix"], dict)
                       else aln["outputs"]["aligned_matrix"], "aligned_matrix")
ameta_path = aln["outputs"]["aligned_metadata"]["path"] if isinstance(aln["outputs"]["aligned_metadata"], dict) else aln["outputs"]["aligned_metadata"]
derived = native.derive_columns(ameta_path, case.dir / "aligned" / "design_metadata.csv",
                                patterns={"subject": ("title", r"^(Resist\d+)_"),
                                          "arm": ("title", r"_(BFRT|CREST)_"),
                                          "time": ("title", r"_(Before|After)$")},
                                recode={"time": {"Before": "pre", "After": "post"}})
dmeta = pd.read_csv(derived["output"], index_col=0)
# consistency of title-derived labels with GEO characteristics
assert (dmeta["arm"] == dmeta["characteristics_ch1.1.treatment"]).all()
assert (dmeta["time"] == dmeta["characteristics_ch1.2.batch"].map({"Before": "pre", "After": "post"})).all()
dmeta["tcell"] = [("base" if t == "pre" else f"post_{a}") for a, t in zip(dmeta["arm"], dmeta["time"])]
dmeta["cell2"] = dmeta["arm"] + "_" + dmeta["time"]
dmeta.to_csv(derived["output"])
dm_item = case.add_output(derived["output"], "design_metadata")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched": aln.get("unmatched_matrix_columns", []),
                   "key_derivation": keyed["columns"], "derived_columns": derived["columns"],
                   "levels": derived["levels"],
                   "extra_columns": {"tcell": "base for every pre sample, post_<arm> for post samples (paper's cohort:timepoint coding)",
                                     "cell2": "arm_time"},
                   "check": "title-derived arm/time equal GEO characteristics treatment/batch for all 34 samples"},
            evidence=[mat_in, meta_in, amat, dm_item], paper={"locator": "S8.3.16.p2"},
            reasoning="Matrix columns S1..S34 equal the library names in GEO 'description'; exact match on that derived key, "
                      "no positional or substring matching.", confidence="high")

prof = native.profile_matrix(amat["path"])
print(json.dumps(prof, indent=1))
case.write_json("matrix_profile.json", prof)
run.log("01_gates done through alignment")
print(json.dumps({k: aln[k] for k in aln if k != "outputs"}, indent=1, default=str))
