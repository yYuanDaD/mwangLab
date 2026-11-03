import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
import pandas as pd, numpy as np
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
meta = case.evidence_item("metadata:GSE164890_metadata.csv"); mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
am = case.dir/"aligned"/"aligned_matrix.csv"
prof = native.profile_matrix(am)
ev_prof = case.write_json("matrix_profile.json", prof, "matrix_profile")
x = pd.read_csv(am, index_col=0)
frac = x.values - np.rint(x.values)
print("fractional entries:", int((np.abs(frac)>1e-8).sum()), "max abs frac dev", np.abs(frac).max(), "col sums", x.sum().min(), x.sum().max())
case.decide("matrix", final={"matrix_type": "estimated counts (RSEM expected counts, per gene)", "recommended_method": "DESeq2 on rounded expected counts",
    "integer_fraction": prof["integer_fraction"], "max": prof["max"], "min": prof["min"],
    "evidence": "file name 'rsem.genes.counts'; GEO data_processing: RSEM v1.2.31 'expression table of raw read counts per gene'; 94.5% integer-valued, remainder fractional expected counts (non-negative); library sizes 9.7-35M; a separate TPM file exists and was not used; paper S2.4.p1/S2.5.p1 fed RSEM per-gene table to DESeq2",
    "rounding_recipe": "round half-to-even to nearest integer (numpy.rint) of RSEM expected counts; no other change"},
  evidence=[mat, ev_prof], paper={"locator": "S2.5.p1"}, confidence="high",
  reasoning="RSEM expected counts are estimated counts, not raw integers; the paper's own route is DESeq2 on this table, so rounding is a documented preparation step, not a substitution.")
