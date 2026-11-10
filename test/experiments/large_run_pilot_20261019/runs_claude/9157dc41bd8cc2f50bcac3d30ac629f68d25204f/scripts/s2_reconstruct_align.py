import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(RUN)
case = run.case("GSE134698")
PAPER = "test/experiments/paper_screen_20261019/papers/9157dc41bd8cc2f50bcac3d30ac629f68d25204f"
paper_md = case.add_input(PAPER + ".paper.md", "paper")
paper_json = case.add_input(PAPER + ".paper.json", "paper")
meta = case.add_input("data/GSE134698/GSE134698_metadata.csv", "metadata")
mat = case.add_input("data/GSE134698/GSE134698_featureCounts_matrix.txt.gz", "matrix")

paper_threshold = {"metric": "padj", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": "not_reported", "source_locator": "S0.p46",
                   "note": "'p-values adjusted by Benjamini-Hochberg and filtered with FDR = 0.1'; Table 2 note S0.p63 'p-value adjusted = 0.1'; no fold-change cutoff stated"}
recon = {
    "accessions": ["GSE134698"],
    "assay": "3' mRNA-seq (Lexogen QuantSeq FWD), Illumina MiSeq single-end, STAR v2.5 GRCh38.p12 / GENCODE v28, featureCounts (S0.p44, S0.p45)",
    "tissue": "skeletal muscle biopsy (GEO: gastrocnemius)",
    "samples": "3 HF patients x (before, after 12-week personalized aerobic training) = 6 samples (S0.p43, S0.p47); sequenced donors match TAB1 HF1/HF4/HF5 by age/BMI (GEO P1/P4/P5)",
    "sample_inclusion": "all 6 deposited samples; S0.p47 notes HF3 and HF6 low depth, HF2 low assigned genes (not sequenced/deposited here)",
    "factors": {"time": ["before (0 weeks)", "after (12 weeks training)"], "subject": "patient (3)"},
    "primary_estimand": "within-patient change in skeletal-muscle gene expression after vs before 12-week exercise rehabilitation in HF patients",
    "planned_contrasts": [{"name": "after_vs_before", "numerator": "after", "denominator": "before", "paired_by": "patient", "locator": "S0.p46"}],
    "repeated_measure_unit": "patient (normalized in pairs per patient, S0.p46)",
    "normalization": "top 12,000 most expressed genes selected after quantile + log normalization, then DESeq2 (S0.p45-S0.p46)",
    "method": "DESeq2 (R), pairs per patient; GSEA with fgsea on GO Biological Process, pathway FDR 0.1 (S0.p46)",
    "paper_threshold": paper_threshold,
    "paper_reported_results": {"deg_total": "not_reported",
                               "table2": "curated list of 28 DEGs relevant to muscle (24 up, 4 down) at padj<=0.1 (TAB2, S0.p49)",
                               "gsea": "26 GO BP processes significant (FDR 0.1, |NES|>1.7) (S0.p50, S0.p51)"},
}
case.decide("paper_reconstruction", final=recon, evidence=[paper_md, paper_json], paper={"locator": "S0.p46"},
            reasoning="Paired pre/post design in 3 HF patients; DESeq2 with per-patient pairing; BH FDR 0.1 with no FC cutoff; Table 2 is a curated subset, total DEG count not reported.",
            confidence="high")

m = pd.read_csv(meta["path"], index_col=0)
print(m[["title", "characteristics_ch1.2.age", "characteristics_ch1.3.bmi", "characteristics_ch1.5.training period"]])

# alignment: matrix columns are GEO titles
raw = pd.read_csv(mat["path"], sep="\t", index_col=0)
print("raw matrix", raw.shape, list(raw.columns))
case_dir = case.dir
counts_only = raw.drop(columns=["Chr", "Start", "End", "Strand", "Length"])
(case_dir / "aligned").mkdir(parents=True, exist_ok=True)
counts_csv = case_dir / "aligned" / "featureCounts_counts_only.csv"
counts_only.to_csv(counts_csv)
cnt = case.add_output(str(counts_csv), "matrix")
case.decide("ownership", final={"accession": "GSE134698", "matrix_file": mat["path"], "metadata_file": meta["path"], "owned": True,
                                "checks": "series_id GSE134698 in metadata; 6 samples = 3 patients x before/after as in S0.p43/S0.p44; age/BMI of P1,P4,P5 (56/27.07, 61/32.87, 56/26.77) match TAB1 HF1, HF4, HF5; data_processing names STAR/GENCODE v28/featureCounts/DESeq2/fGSEA as in S0.p45-46; matrix columns = sample titles"},
            evidence=[meta, mat, paper_md], paper={"locator": "S0.p44"},
            reasoning="Paper deposits these 6 samples under GSE134698; GEO metadata matches donor characteristics in TAB1.", confidence="high")

aln = native.align_to_metadata(str(counts_csv), meta["path"], case_dir / "aligned", key_column="title")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case_dir / "aligned" / "design_metadata.csv",
                                patterns={"subject": ("title", r"^(P\d+)_(?:before|after)$"),
                                          "time": ("title", r"^P\d+_(before|after)$")})
dm = case.add_output(str(case_dir / "aligned" / "design_metadata.csv"), "design_metadata")
d = pd.read_csv(case_dir / "aligned" / "design_metadata.csv", index_col=0)
print(d[["title", "subject", "time", "characteristics_ch1.5.training period", "characteristics_ch1.6.treatment"]])
assert ((d["time"] == "after") == (d["characteristics_ch1.5.training period"] == "12 weeks")).all()
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                                "coverage": aln["coverage"], "key_column": "title", "derived_columns": derived,
                                "annotation_columns_removed": ["Chr", "Start", "End", "Strand", "Length"]},
            evidence=[cnt, meta, am, amd, dm], paper={"locator": "S0.p43"},
            reasoning="Exact match of matrix column names to GEO sample titles; subject/time parsed from title and cross-checked against 'training period' (0 vs 12 weeks).",
            confidence="high")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, indent=1, default=str)[:2500])
lib = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
print("library sizes", lib.sum().to_dict())
print("ERCC rows", lib.index.str.startswith("ERCC").sum(), "nonzero genes", (lib.sum(axis=1) > 0).sum())
json.dump(prof, open(case_dir / "aligned" / "matrix_profile.json", "w", encoding="utf-8"), indent=1, default=str)
