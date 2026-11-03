import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
DATA = "E:/agent/mwangLab_pdf/data/GSE164890"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
meta = case.evidence_item("metadata:GSE164890_metadata.csv"); mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
import pandas as pd
m = pd.read_csv(f"{DATA}/GSE164890_metadata.csv", index_col=0)
print(m["series_id"].unique(), len(m), m["organism_ch1"].unique(), m["library_strategy"].unique())
case.decide("ownership", final={"accession": "GSE164890", "matrix_file": f"{DATA}/GSE164890_rsem.genes.counts.tsv.gz",
    "metadata_file": f"{DATA}/GSE164890_metadata.csv", "owned": True,
    "checks": "metadata series_id=GSE164890; 14 samples = 7 skaters x before/after exactly as S2.3.p1; whole blood globin-depleted, Homo sapiens, RNA-seq; matrix columns 1before..7after match metadata 'description'; data_processing names STAR/RSEM/GENCODE v26 as in S2.4.p1; matrix is the supplementary 'raw read counts per gene' file"},
  evidence=[meta, mat], paper={"locator": "S2.3.p1"}, confidence="high",
  reasoning="Accession, sample count, tissue and processing all agree with the paper.")
aln = native.align_to_metadata(f"{DATA}/GSE164890_rsem.genes.counts.tsv.gz", f"{DATA}/GSE164890_metadata.csv", case.dir/"aligned", key_column="description")
print({k:v for k,v in aln.items() if k!='outputs'})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir/"aligned"/"design_metadata.csv",
   aliases={"time_raw": "characteristics_ch1.1.time point"},
   patterns={"subject": ("title", r"Skater (\d+) - "), "ex": ("characteristics_ch1.1.time point", r"(before|after) exercise")},
   )
print(json.dumps(derived, indent=1, default=str)[:1500])
dm = pd.read_csv(case.dir/"aligned"/"design_metadata.csv", index_col=0); print(dm[["title","subject","ex","time_raw"]])
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
   "coverage": aln["coverage"], "unmatched": {"matrix": aln["unmatched_matrix_columns"], "metadata": aln["unmatched_metadata_samples"]},
   "annotation_columns_dropped": aln["annotation_columns_dropped"], "feature_ids": "Ensembl gene IDs (Gene_id index; Symbol column dropped)",
   "derived_columns": derived},
  evidence=[meta, mat, am, amd], confidence="high",
  reasoning="Exact match of matrix column labels (1before...) to metadata 'description'; all 14 matched, no positional alignment. Derived subject and ex columns by regex from title and time point.")
