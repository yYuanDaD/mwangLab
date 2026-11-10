"""Start the run and record paper_reconstruction, ownership, alignment, matrix for all cases."""
import json
from common import *  # noqa: F401,F403  (sets cwd + sys.path)
from tools import native

native.enable_native_mode()
REQUEST = ("Use the bioinformatics-workflow skill to analyze GSE208639 for the paper 'Individual transcriptomic "
           "response to strength training for patients with myotonic dystrophy type 1.' (PMID 37318869). "
           "Determine how exercise affects gene expression as the paper intends.")
CASES = ["case_01", "case_02", "case_03"]
run = native.RunRecorder(RUN_DIR, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=CASES)

prof = native.profile_matrix(COUNTS)
print(json.dumps({k: v for k, v in prof.items() if k != "note"}, indent=1, default=str)[:1500])

case_desc = {
    "case_01": "Exercise effect within DM1: post- vs pre-training, paired by subject (9 pairs)",
    "case_02": "Paper grouped analysis: grouped pre-training vs controls and grouped post-training vs controls (edgeR QL), Δlog2FC",
    "case_03": "Paper individual analysis: each participant's pre and post sample (n=1) vs 6 controls",
}

for cid in CASES:
    case = run.case(cid, accession="GSE208639")
    paper = case.add_input(PAPER_JSON, "paper")
    paper_md = case.add_input(PAPER_MD, "paper")
    meta = case.add_input(META, "metadata")
    mat = case.add_input(COUNTS, "matrix")
    merge_rep = case.add_input(MERGE_REPORT, "matrix", label="star_merge_report.json")
    smap = dict(STUDY_MAP, case_scope=case_desc[cid])
    case.write_json("paper_reconstruction.json", smap)
    case.decide("paper_reconstruction",
                final={"accessions": ["GSE208639"], "primary_estimand": STUDY_MAP["primary_estimand"],
                       "planned_contrasts": STUDY_MAP["planned_contrasts"],
                       "paper_threshold": PAPER_THRESHOLD, "paper_method": STUDY_MAP["paper_method"],
                       "blocking_or_covariance": STUDY_MAP["blocking_or_covariance"],
                       "sample_inclusion": STUDY_MAP["sample_inclusion"],
                       "sample_exclusion": STUDY_MAP["sample_exclusion"], "case_scope": case_desc[cid]},
                evidence=[paper, paper_md], paper={"locator": "S4.4.p1"}, confidence="high",
                reasoning=("Methods S4.3/S4.4/S4.13 and Results S2.2.p2/S2.5.p1: 9 DM1 pre/post + 6 controls; edgeR "
                           "QL F-test of each group (grouped and per individual) vs controls; exercise effect = "
                           "Δlog2FC and % rescue; DEG rule |log2FC|>2 & raw P<0.05. GSE208639 is the own deposit "
                           "(S4.12.p1); other accessions are reanalysis/citations. No direct post-vs-pre test "
                           "and no subject blocking reported."))

    case.decide("ownership",
                final={"accession": "GSE208639", "matrix_file": "GSE208639_RAW.tar (24 STAR ReadsPerGene.out.tab.gz) "
                       "merged to GSE208639_star_counts_reverse.csv", "metadata_file": str(META), "owned": True,
                       "checks": ["GEO Series_pubmed_id = 37318869", "24 GSMs = 9 DM1 x (pre, post) + 6 controls, "
                                  "matching ABS.p1/S4.3.p1", "participant IDs in titles (907, 2005, 523, 1791, 1806, "
                                  "2002, 2019, 2110, 1242) match those named in S2.2-S2.7",
                                  "2182 and 1955 absent, as excluded in S4.4.p1",
                                  "GEO data_processing: STAR 2.7.9 --quantMode GeneCounts, hg38 (= S4.4.p1)"],
                       "alternatives": {"GSE208639_FPKM.csv.gz": "FPKM, not the paper's edgeR input; not used",
                                        "GSE208639_edgeR_output.csv": "authors' results; only the first xlsx sheet "
                                        "(grouped pre-training vs control) survived tool conversion; used only "
                                        "as a concordance reference"}},
                evidence=[meta, mat, merge_rep, paper], paper={"locator": "S4.12.p1"}, confidence="high",
                reasoning="Series is linked to PMID 37318869; sample set, IDs and processing match the Methods.")

    aln = native.align_to_metadata(COUNTS, META, case.dir / "aligned")
    aligned_m = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    aligned_md = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
        aliases={"grp": "characteristics_ch1.2.treatment"},
        patterns={"subject": ("title", r",\s*((?:Control\s+)?\d+)$")},
        recode={"grp": {"Pre-training": "pre", "Post-training": "post", "No training": "ctrl"},
                "subject": {"2019": "p2019", "907": "p907", "2110": "p2110", "2005": "p2005", "1242": "p1242",
                            "523": "p523", "1791": "p1791", "1806": "p1806", "2002": "p2002",
                            "Control 1": "c1", "Control 2": "c2", "Control 4": "c4", "Control 10": "c10",
                            "Control 11": "c11", "Control 13": "c13"}})
    design_md = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
    case.decide("alignment",
                final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                       "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                       "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                       "matrix_column_source": "GSM prefix of each tar member file name (00_merge_star_counts.py)",
                       "derived_columns": derived},
                evidence=[mat, meta, aligned_m, aligned_md, design_md], confidence="high",
                reasoning=("Each STAR file name starts with its GSM accession; columns were named by that GSM and "
                           "aligned exactly to the metadata index (24/24). subject parsed from title; grp from "
                           "characteristics treatment. Title typo 'Muslce' (GSM6356075) does not affect parsing."))

    case.decide("matrix",
                final={"matrix_type": "raw counts", "recommended_method": "edgeR / DESeq2 (raw integer counts)",
                       "profile": {k: prof.get(k) for k in ("n_rows", "n_samples", "min", "max", "median",
                                                            "integer_fraction", "candidates")},
                       "strand_column": "STAR column 4 (reverse strand); strand2/strand1 assigned-read ratio "
                                        "6.6-13.1 in all 24 samples, consistent with NEBNext Directional (S4.3.p1)",
                       "paper_input": "STAR gene counts into edgeR (S4.4.p1)"},
                evidence=[mat, merge_rep, meta, paper], paper={"locator": "S4.4.p1"}, confidence="high",
                reasoning=("Non-negative integers, STAR --quantMode GeneCounts per GEO data_processing; the 4 N_* "
                           "summary rows removed; reverse-strand column selected from the data and the library kit."))
    print(cid, "common gates recorded")
