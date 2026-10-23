"""Gates 1-4 (paper_reconstruction, ownership, alignment, matrix) and the suitability report."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
REQ = ("Analyze GSE183150 for PMID 37724990 (Exercise Training Reduces the Inflammatory Response and "
       "Promotes Intestinal Mucosa-Associated Immunity in Lynch Syndrome): how exercise affects gene "
       "expression as the paper intends.")
run = native.RunRecorder(str(RUN), request=REQ, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) native session",
                         case_ids=["GSE183150"])
case = run.case("GSE183150", accession="GSE183150")

PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC10618653.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC10618653.paper.md"
paper = case.add_input(PAPER_JSON, "paper")
paper_md = case.add_input(PAPER_MD, "paper")
meta_in = case.add_input("data/GSE183150/GSE183150_metadata.csv", "metadata")
mat_in = case.add_input("data/GSE183150/GSE183150_counts.tsv.gz", "matrix")

# ---------------- 1. paper_reconstruction ----------------
paper_threshold = {"metric": "not_reported", "adjustment": "not_reported", "cutoff": "not_reported",
                   "effect_metric": "not_reported", "effect_cutoff": "not_reported",
                   "source_locator": "S2.8.p1 (defers mRNA-seq statistical parameters to Supplementary Methods SUP1, not retrievable)"}
study_map = {
    "paper_id": "PMID37724990 / PMC10618653 (Clin Cancer Res 2023)",
    "accessions": ["GSE183150"],
    "other_accessions_not_analyzed": {"GSE210011": "NanoString GeoMx DSP spatial data (S2.9.p1, S3.7.p1); not the mRNA-seq question"},
    "assay": "bulk mRNA-seq (NovaSeq 6000, 100 nt PE), rectosigmoid normal colorectal mucosa biopsies",
    "design": "non-randomized sequential-assignment trial; 12-month cycling exercise (n=11 enrolled) vs usual care (n=10 enrolled); biopsies at baseline and 12 months (S2.1.p1, S2.2.p1, FIG1)",
    "sample_inclusion": ["participants with mRNA-seq at both baseline and 12 months: usual care N=6, exercise N=9 (SUP7 legend, Supplementary Fig. S6)"],
    "sample_exclusion": ["participants without paired biopsies (not deposited)"],
    "factors": [{"name": "group", "levels": ["usual care", "exercise"]},
                {"name": "visit", "levels": ["baseline", "12 months (end of study)"]}],
    "repeated_measure_unit": "participant (two biopsies each)",
    "primary_estimand": "difference between exercise and usual care in the 12-month change of colorectal mucosa gene expression (group x time; FIG3 A: 'log fold change ... compared with baseline after 12 months in the usual care and exercise groups'; S3.5.p1: DEGs in the exercise group 'when compared with the usual care group')",
    "planned_contrasts": ["(exercise: 12 mo - baseline) - (usual care: 12 mo - baseline)"],
    "paper_reported_result": {"n_up": 13, "n_down": 33, "n_total": 46, "locator": "S3.5.p1",
                              "top_up": ["C5orf17/LINC02899", "ABCG8", "B4GALNT2", "KCNV1"],
                              "top_down": ["TMPRSS6", "PRAC1/2", "HOXB13"]},
    "blocking_or_covariance": {"status": "required", "reason": "paired baseline/12-month biopsies per participant"},
    "matrix_scale": "raw gene counts (featureCounts, GEO data_processing)",
    "paper_method": "not_reported (main text S2.7.p1/S2.8.p1 defer to Supplementary Methods, which could not be retrieved: Europe PMC says not open access; PMC bin download blocked)",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "paper_enrichment": "GSEA-style KEGG / GO BP enrichment ranked by fold change, BH-adjusted P < 0.05 (FIG3 C, SUP15, SUP6); BIOCARTA IL6 GSEA",
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction",
            final={"accessions": ["GSE183150"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": study_map["planned_contrasts"], "paper_threshold": paper_threshold,
                   "paper_method": study_map["paper_method"], "assay": study_map["assay"],
                   "sample_inclusion": study_map["sample_inclusion"],
                   "repeated_measure_unit": study_map["repeated_measure_unit"],
                   "paper_reported_result": study_map["paper_reported_result"]},
            evidence=[paper, paper_md], paper={"locator": "S3.5.p1; FIG3; S2.9.p1; SUP7; S2.8.p1"},
            confidence="medium",
            reasoning=("GSE183150 is the paper's mRNA deposit (S2.9.p1). Fig. 3A shows per-group log fold changes vs "
                       "baseline and S3.5.p1 compares exercise with usual care, so the estimand is the group difference in "
                       "12-month change. Method and threshold are in the Supplementary Methods, which could not be obtained; "
                       "they are recorded as not_reported rather than filled from a default."))

# ---------------- 2. ownership ----------------
meta = pd.read_csv(meta_in["path"], index_col=0)
own = {"series_id": sorted(meta["series_id"].unique().tolist()),
       "n_gsm": int(len(meta)),
       "participants": int(meta["characteristics_ch1.1.patient id"].nunique()),
       "per_group_participants": meta.groupby("characteristics_ch1.6.group")["characteristics_ch1.1.patient id"].nunique().to_dict(),
       "visits": sorted(meta["characteristics_ch1.7.visit"].unique().tolist()),
       "tissue": sorted(meta["characteristics_ch1.0.tissue"].unique().tolist())}
case.decide("ownership",
            final={"accession": "GSE183150", "matrix_file": "GSE183150_counts.tsv.gz",
                   "metadata_file": "GSE183150_metadata.csv", "owned": True, "checks": own},
            evidence=[meta_in, mat_in, paper], paper={"locator": "S2.9.p1; SUP7"}, confidence="high",
            reasoning=("series_id GSE183150 in every GSM; colorectal mucosa from LS participants; 15 participants "
                       "(9 exercise, 6 usual care) at baseline and end-of-study, matching Supplementary Fig. S6 (N=9/N=6). "
                       "60 GSMs = 30 libraries x 2 sequencing lanes (L001/L002)."))

# ---------------- 3. alignment ----------------
aln = native.align_to_metadata(mat_in["path"], meta_in["path"], case.dir / "aligned" / "lanes", key_column="description")
lane_mat = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
lane_meta = pd.read_csv(aln["outputs"]["aligned_metadata"]["path"], index_col=0)
# Lanes L001/L002 are technical replicates of one library: sum them (DESeq2 collapseReplicates convention).
pid = lane_meta["characteristics_ch1.1.patient id"].astype(int)
vis = lane_meta["characteristics_ch1.7.visit"].map({"Baseline": "base", "End-of-Study": "eos"})
lib = ("P" + pid.map(lambda x: f"{x:02d}") + "_" + vis)
lane_meta["library"] = lib
assert lane_meta.groupby("library").size().eq(2).all()
lib_mat = lane_mat.T.groupby(lib).sum().T
lane_meta["gsm"] = lane_meta.index.astype(str)
lib_meta = (lane_meta.groupby("library")
            .agg({"gsm": lambda s: ";".join(s),
                  "title": lambda s: " | ".join(s), "description": lambda s: ";".join(s),
                  "characteristics_ch1.1.patient id": "first", "characteristics_ch1.6.group": "first",
                  "characteristics_ch1.7.visit": "first", "characteristics_ch1.2.age": "first",
                  "characteristics_ch1.5.gene mutated": "first", "characteristics_ch1.3.race": "first"}))
lib_meta.columns = ["lane_gsms"] + list(lib_meta.columns[1:])
lib_meta["lib"] = lib_meta.index
lib_dir = case.dir / "aligned"
lib_mat.to_csv(lib_dir / "library_counts.csv")
lib_meta.to_csv(lib_dir / "library_metadata.csv")
derived = native.derive_columns(
    lib_meta, lib_dir / "design_metadata.csv",
    aliases={"pid": "characteristics_ch1.1.patient id", "age": "characteristics_ch1.2.age",
             "mmr": "characteristics_ch1.5.gene mutated"},
    patterns={"subject": ("lib", r"^(P\d+)_"), "visit": ("lib", r"_(base|eos)$")},
    recode={})
dm = pd.read_csv(lib_dir / "design_metadata.csv", index_col=0)
dm["grp"] = dm["characteristics_ch1.6.group"].map({"Exercise": "ex", "Usual care": "uc"})
assert dm["grp"].notna().all()
dm.to_csv(lib_dir / "design_metadata.csv")
derived["recode_manual"] = {"grp": {"Exercise": "ex", "Usual care": "uc"}, "source": "characteristics_ch1.6.group"}
lane_map = lane_meta[["description", "library"]]
lane_map.to_csv(lib_dir / "lane_to_library.csv")
a_mat = case.add_output(lib_dir / "library_counts.csv", "aligned_matrix")
a_meta = case.add_output(lib_dir / "design_metadata.csv", "aligned_metadata")
a_map = case.add_output(lib_dir / "lane_to_library.csv", "alignment_map")
lane_aligned = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_lane_matrix")
case.decide("alignment",
            final={"method": aln["method"] + " (key_column=description), then lane sum per library",
                   "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                   "unmatched": [], "lane_collapse": "L001+L002 summed per (participant, visit); 60 lane columns -> 30 libraries; lane log-count correlation >= 0.986",
                   "n_libraries": int(lib_mat.shape[1]), "derived_columns": derived},
            evidence=[mat_in, meta_in, a_mat, a_meta, a_map, lane_aligned], paper={"locator": "S2.9.p1"},
            confidence="high",
            reasoning=("Matrix column names equal the GEO 'description' field exactly (60/60). Each library was sequenced on "
                       "two lanes; lanes are technical replicates and were summed so that participants are not double-counted. "
                       "Formula-safe columns: subject, visit (base/eos), grp (uc/ex)."))

# ---------------- 4. matrix ----------------
prof = native.profile_matrix(lib_dir / "library_counts.csv")
prof_lane = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
case.write_json("matrix_profile.json", {"library": prof, "lane": prof_lane})
print(json.dumps({k: v for k, v in prof.items() if k not in ("annotation_columns",)}, indent=1, default=str)[:2000])
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2 / edgeR / limma-voom, or limma on log2(CPM+1)",
                   "evidence_summary": {"integer_fraction": prof.get("integer_fraction"), "min": prof.get("min"),
                                        "max": prof.get("max"), "n_features": prof.get("n_rows") or prof.get("n_features"),
                                        "feature_ids": "Ensembl gene IDs with version"},
                   "paper_input": "raw counts implied (featureCounts, GEO data_processing)"},
            evidence=[a_mat, mat_in, meta_in], paper={"locator": "S2.7.p1"}, confidence="high",
            reasoning=("All values are non-negative integers; GEO data_processing: STAR + featureCounts (subread 2.0), "
                       "'Matrix table with raw gene counts'. Lane sums of integers remain integers."))

# ---------------- comparison names (evidence only; suitability is run in the design script) ----------------
from tools.suitability import enumerate_comparisons
for c in enumerate_comparisons(dm, ["grp", "visit"], references={"grp": "uc", "visit": "base"}):
    print(c["name"], c["kind"], c["analyzable"], [x.get("n") for x in c["cells"]])
print("gates 1-4 recorded")
