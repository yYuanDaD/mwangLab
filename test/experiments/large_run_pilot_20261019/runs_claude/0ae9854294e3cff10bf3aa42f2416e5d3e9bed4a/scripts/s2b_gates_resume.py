import sys, os, json; sys.path.insert(0, r"E:\agent\mwangLab_pdf"); os.chdir(r"E:\agent\mwangLab_pdf")
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/0ae9854294e3cff10bf3aa42f2416e5d3e9bed4a"
REQ = ("Use the bioinformatics-workflow skill to analyze GSE152133 for PMID 37876943 and determine how exercise "
       "affects gene expression as the paper intends.")
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
P = "test/experiments/paper_screen_20261019/papers/"
META = "data/GSE152133/GSE152133_metadata.csv"; MAT = "data/GSE152133/GSE152133_full.read.counts.tsv.gz"
meta = case.evidence_item("metadata:GSE152133_metadata.csv"); mat = case.evidence_item("matrix:GSE152133_full.read.counts.tsv.gz")
aln = native.align_to_metadata(MAT, META, case.dir / "aligned", key_column="title")
print({k: v for k, v in aln.items() if k != "outputs"})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"age_raw": "characteristics_ch1.0.age", "run_raw": "characteristics_ch1.1.type"},
    patterns={"mouse": ("title", r"^(A\d+[A-Z]?)(?:_repeat)?$")},
    recode={"age_raw": {"adult (6 months old)": "m6", "older adults (24 months old)": "m24", "elderly (28+ months old)": "m28"},
            "run_raw": {"First NextSeq550 Run": "run1", "Second NextSeq550 Run": "run2"}})
dm = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
            "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
            "unmatched_metadata_samples": aln["unmatched_metadata_samples"], "derived_columns": der},
            evidence=[mat, meta, am, amd, dm], confidence="high",
            reasoning="Matrix columns are GEO titles (A22L, A22L_repeat, ...); exact match on title.")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print({k: prof[k] for k in ["n_features", "n_samples", "min", "max", "integer_fraction", "missing_values", "candidates"]})
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "profile": {k: prof[k] for k in ["n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                             "missing_values", "negative_values", "duplicated_feature_ids"]},
            "paper_input": "STAR --quantMode GeneCounts read counts into DESeq2 (S3.1.1.p1-p2)"},
            evidence=[am, mat], confidence="high", paper={"locator": "S3.1.1.p1"},
            reasoning="All-integer non-negative values; file named full.read.counts; paper used STAR GeneCounts into DESeq2.")
d = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
print(pd.crosstab(d["age_raw"], d["run_raw"]))
