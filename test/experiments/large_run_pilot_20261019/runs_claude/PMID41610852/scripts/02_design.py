"""Gates matrix -> threshold for GSE312780."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852"
run = native.RunRecorder.open(RUN)
case = run.case("GSE312780")
D = case.dir
paper_md = case.evidence_item("paper:PMC13237580.paper.md")
mat_in = case.evidence_item("matrix:GSE312780_salmon.merged.gene_counts.tsv.gz")
amat = native.read_table(D / "aligned/aligned_matrix.csv")
dmeta = pd.read_csv(D / "aligned/design_metadata.csv", index_col=0)
prof_item = case.add_output(D / "matrix_profile.json", "matrix_profile")
prof = json.load(open(D / "matrix_profile.json"))

# ---- matrix
case.decide("matrix",
            final={"matrix_type": "estimated counts (salmon via nf-core tximport, gene level, not length-scaled)",
                   "recommended_method": "DESeq2 on rounded estimated counts",
                   "rounding_documented": "round half-to-even to nearest integer before DESeq2 (pandas round), "
                                          "standard practice for tximport counts; paper itself used lengthScaledTPM counts",
                   "integer_fraction": prof["integer_fraction"], "min": prof["min"], "max": prof["max"],
                   "paper_input": "tximport lengthScaledTPM counts from quant.sf (not deposited)"},
            evidence=[mat_in, prof_item, paper_md], paper={"locator": "S8.3.15.p1; S8.3.16.p2"},
            reasoning="File name salmon.merged.gene_counts (nf-core/rnaseq output), non-negative, 89% integer, max 3.8e6, "
                      "library sums ~37-54M matching the paper's 41-62M mapped reads: Salmon estimated counts. "
                      "Count methods valid after documented rounding.", confidence="high")

# ---- sample set: the paper excluded one BFRT participant after PCA without naming it
qc = pd.read_csv(D / "qc/qc_pca_scores.csv", index_col=0)
qc_item = case.add_output(D / "qc/qc_pca_scores.csv", "qc_pca_scores")
qcs_item = case.add_output(D / "qc/qc_pca_summary.json", "qc_pca_summary")
excl = {"excluded_subject": "Resist18", "excluded_samples": dmeta.index[dmeta["subject"] == "Resist18"].tolist(),
        "evidence": "Resist18_BFRT_Before (GSM9353031) alone drives PC1 (65% of variance among top-2000 variable genes, "
                    "PC1 = 171 vs |PC1| <= 21 for all others) and has mean Pearson r 0.83 to other samples vs >= 0.98 for all others; "
                    "it is a BFRT participant, matching the paper's single BFRT exclusion (S8.3.16.p2).",
        "status": "inferred from data (paper does not name the participant); both samples of the subject dropped",
        "result_n": "8 BFRT + 8 CREST subjects = 32 samples, matching the paper's 16 analysed participants"}
excl_item = case.write_json("sample_exclusion_resolution.json", excl)
keep = dmeta.index[dmeta["subject"] != "Resist18"]
sub = D / "aligned/primary_16subjects"; sub.mkdir(exist_ok=True)
dmeta.loc[keep].to_csv(sub / "design_metadata.csv")
amat.loc[:, keep].to_csv(sub / "aligned_matrix.csv")
sm_item = case.add_output(sub / "design_metadata.csv", "design_metadata_primary")
sx_item = case.add_output(sub / "aligned_matrix.csv", "aligned_matrix_primary")
pm = dmeta.loc[keep]

refs = {"time": "pre", "arm": "CREST"}
planned = ["time_post_vs_pre_arm-BFRT", "time_post_vs_pre_arm-CREST", "arm_time_BFRT_post_vs_CREST_pre"]
rep, s_item, s_summary = case.suitability(matrix_type="estimated counts", metadata=pm, factors=["arm", "time"],
                                          matrix_csv=str(sub / "aligned_matrix.csv"), organism="Human",
                                          subject="subject", references=refs, planned=planned)
print(json.dumps(s_summary, indent=1))
print([c["name"] for c in rep["comparisons"]])
print(json.dumps(rep["checks"].get("sex", {}), indent=1, default=str)[:1500])
print(json.dumps(rep["checks"].get("covariance", {}), indent=1, default=str)[:2000])
json.dump({"names": [c["name"] for c in rep["comparisons"]]}, open(D / "suitability/_names.json", "w"))
