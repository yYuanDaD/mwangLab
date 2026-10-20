import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
c = json.load(open(pathlib.Path(RUN) / "GSE179302/results/final_threshold_counts.json", encoding="utf-8"))
case.decide("study", final={"route": "declared_deviation",
    "primary_unit": "primary_limma_full_covariates_noERCC",
    "deviations": ["limma on log2(CPM+1) instead of DESeq2 (DESeq2 executor cannot take continuous age)",
                   "no sva surrogate variable (sva unavailable)", "BH instead of IHW at padj<0.1",
                   "ethnicity represented by race (exactly aliased with race 'dk' in the 21 samples)",
                   "ERCC spike-ins removed before normalization (41-70% of reads)"],
    "results": {"primary_limma": {k: c["limma"][k] for k in ("n_significant", "n_up", "n_down")},
                "secondary_deseq2_no_age": {k: c["deseq2"][k] for k in ("n_significant", "n_up", "n_down")},
                "audit_deseq2_unadjusted_with_ERCC": "85 (2 up / 83 down)", "audit_deseq2_sex_hisp_with_ERCC": "2 (0/2)",
                "paper": "767 (365 up / 402 down in active), IHW padj<0.1"},
    "superseded_units": ["primary_limma_full_covariates", "secondary_deseq2_without_age"],
    "interpretation": "Associational, not causal. Not reproduced: under the paper's covariate set the active-vs-inactive contrast gives ~0-5 DEGs; signal (mainly interferon-gene downregulation in active, e.g. IFI44L) appears only without race adjustment. Race 'dk' (=Hispanic) is 8/13 active vs 1/8 inactive, so race/ethnicity adjustment absorbs most of the contrast; the paper's sva SV and IHW may explain part of the gap."},
    evidence=[case.evidence_item("paper:PMC9722583.paper.md")], confidence="medium",
    reasoning="Planned route ran as a declared deviation; arms 13 vs 8, residual df 13, so not exploratory.")
case.finish(n_deg=c["limma"]["n_significant"], deg_sanity=c["limma"]["deg_sanity"])
print(run.finish())
