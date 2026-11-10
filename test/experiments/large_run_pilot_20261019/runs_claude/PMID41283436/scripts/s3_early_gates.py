import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436"
CASES = ["fatigued_pbmt_vs_ctrl", "sedentary_pbmt_vs_ctrl", "exercise_vs_sedentary_ctrl"]
run = native.RunRecorder(RUN, request="Analyze GSE297318 for PMID 41283436 (830 nm PBMT, acute exercise); determine how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) agent session", case_ids=CASES)
PJ = "test/experiments/paper_screen_20261019/papers/PMC12641718.paper.json"
PM = "test/experiments/paper_screen_20261019/papers/PMC12641718.paper.md"
META = "data/GSE297318/GSE297318_metadata.csv"
MAT = "data/GSE297318/GSE297318_merged_from_tar.csv"
TAR = "data/GSE297318/GSE297318_RAW.tar"

# derive formula-safe columns once (shared file per case below)
full = pd.read_csv(META, index_col=0)
grp_map = {"Fatigue": "fatctl", "PBM Fatigue": "fatpbm", "Sedentary": "sedctl", "PBM Sedentary": "sedpbm"}
paper_thr = {"metric": "padj", "adjustment": "not_reported", "cutoff": 0.05, "effect_metric": None,
             "effect_cutoff": None, "inclusive": False, "source_locator": "S4.9.p1"}
study_map = {
    "paper_id": "PMID41283436 / PMC12641718",
    "accessions": ["GSE297318"],
    "assay": "bulk RNA-seq (mRNA, NovaSeq 150PE), mouse tibialis anterior",
    "sample_inclusion": ["6 fatigued controls + 6 fatigued PBMT (Admera project 23263-01) [S4.6.p1]",
                         "6 sedentary controls + 6 sedentary PBMT (Admera project 23263-02) [S4.6.p1]"],
    "sample_exclusion": [],
    "factors": [{"name": "PBMT", "levels": ["control (anesthesia, no light)", "830 nm PBMT"], "locator": "S4.2.p1,S4.2.p2"},
                {"name": "exercise", "levels": ["sedentary", "treadmill run to exhaustion 24 h post-PBMT"], "locator": "S4.3.p1,S4.5.p1"}],
    "primary_estimand": "Effect of 830 nm PBMT pretreatment on TA transcriptome in acutely exercised (fatigued) muscle [S2.3.p1, FIG4]; secondary: PBMT effect in sedentary muscle [S2.1.p1, FIG1]",
    "planned_contrasts": [
        {"name": "fatigued PBMT vs fatigued control", "locator": "S2.3.p1", "paper_counts": {"up": 302, "down": 156}},
        {"name": "sedentary PBMT vs sedentary control", "locator": "S2.1.p1", "paper_counts": {"up": "~586", "down": "~802"}}],
    "not_planned": "No transcriptomic exercise-vs-sedentary contrast is reported; the two arms were sequenced as separate Admera projects [S4.6.p1]",
    "blocking_or_covariance": {"status": "not_required", "note": "independent mice per group [S4.3.p1]; no pairing"},
    "matrix_scale": "not_reported (GEO: featureCounts/HTSeq gene counts)",
    "paper_method": "DESeq2 (stated version 1.4.1) [S4.9.p1]",
    "paper_formula": "not_reported (two-group per project implied by S4.6.p1)",
    "paper_threshold": paper_thr,
    "enrichment": "clusterProfiler GO BP/CC/MF + KEGG ORA [S4.9.p1]",
}
for cid in CASES:
    case = run.case(cid, accession="GSE297318")
    paper = case.add_input(PJ, "paper"); case.add_input(PM, "paper", label="PMC12641718.paper.md")
    meta = case.add_input(META, "metadata"); mat = case.add_input(MAT, "matrix"); tar = case.add_input(TAR, "matrix", label="GSE297318_RAW.tar")
    case.write_json("paper_reconstruction.json", study_map)
    case.decide("paper_reconstruction", final={k: study_map[k] for k in ("accessions", "primary_estimand", "planned_contrasts", "paper_threshold")} | {"paper_method": study_map["paper_method"], "not_planned": study_map["not_planned"]},
                evidence=[paper], paper={"locator": "S4.6.p1"}, confidence="high",
                reasoning="Abstract/S2.1/S2.3/S4.6/S4.9/S10 read. Paper reports PBMT-vs-control DESeq2 within fatigued (302 up/156 down) and within sedentary (~586 up/~802 down) TA, adjusted p<0.05, no fold-change cutoff. Exercise enters as the context (fatigued muscle), not as a sequenced contrast.")
    case.decide("ownership", final={"accession": "GSE297318", "matrix_file": MAT, "metadata_file": META, "owned": True,
                                     "checks": ["GSE297318 named in data availability S10.p1", "24 samples = 4 groups x 6 as in S4.6.p1",
                                                "library names 23263XR-01-* (fatigue) and -02-* (sedentary) match Admera project IDs 23263-01/-02",
                                                "matrix merged from GSE297318_RAW.tar (24/24 per-sample count files)"]},
                evidence=[paper, meta, tar, mat], paper={"locator": "S10.p1"}, confidence="high",
                reasoning="Accession, sample counts, group labels and Admera project IDs all match the paper.")
    keep = {"fatigued_pbmt_vs_ctrl": ["Fatigue", "PBM Fatigue"], "sedentary_pbmt_vs_ctrl": ["Sedentary", "PBM Sedentary"],
            "exercise_vs_sedentary_ctrl": ["Fatigue", "Sedentary"]}[cid]
    lab = full["title"].str.extract(r"^TA Muscle, (.+), \d+$")[0]
    sub = full[lab.isin(keep)]
    (case.dir / "aligned").mkdir(exist_ok=True)
    subp = case.dir / "aligned" / "metadata_subset.csv"; sub.to_csv(subp)
    derived = native.derive_columns(subp, case.dir / "aligned" / "derived_metadata.csv",
        patterns={"matrix_col": ("supplementary_file_1", r"/suppl/(GSM\d+_[^/]+_count)\.txt\.gz$"),
                  "grp": ("title", r"^TA Muscle, (.+), \d+$"),
                  "project": ("description", r"^Library name: 23263XR-(\d+)-\d+$")},
        recode={"grp": {k: v for k, v in grp_map.items() if k in keep}, "project": {"01": "p01", "02": "p02"}})
    aln = native.align_to_metadata(MAT, case.dir / "aligned" / "derived_metadata.csv", case.dir / "aligned", key_column="matrix_col")
    am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
    case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                                    "coverage": aln["coverage"], "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                                    "matrix_columns_outside_case": len(aln["unmatched_matrix_columns"]),
                                    "derived_columns": derived},
                evidence=[mat, meta, am, amd], paper={"locator": "S4.6.p1"}, confidence="high",
                reasoning=f"Metadata subset to the case's groups {keep}; matrix column names (GSM_library_count) reproduced exactly from each sample's supplementary_file_1 name; exact alignment, no position matching. Other matrix columns belong to the other project.")
    prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
    print(cid, aln["n_aligned"], aln["coverage"], {k: prof[k] for k in prof if k not in ("annotation_columns",)})
    print(pd.read_csv(case.dir / "aligned" / "derived_metadata.csv", index_col=0)[["grp", "project"]].value_counts().to_dict())
    case.write_json("matrix_profile.json", prof)
    run.log(f"{cid} early gates done")
