# Preregistered Protocol: Full Pipeline Stability 20 x 3

## Objective and evaluation unit

The primary unit is one frozen GEO study processed once by the production batch pipeline. Twenty
studies are each run in three independent repeats, for 60 trials. The objective is to measure task
success, scientific routing, semantic-decision repeatability, DEG/GSEA stability, provenance, time,
and token cost.

## Frozen design

Before execution, the manifest freezes each accession, selected matrix filename, matrix and metadata
SHA-256, organism, expected matrix type and DA method, design column, control, treatment set, contrast
count, minimum alignment, and any required semantic-alignment path. The exact case set is:

GSE117161, GSE130401, GSE132520, GSE163356, GSE164798, GSE194193, GSE208615, GSE266241,
GSE270703, GSE279359, GSE282641, GSE294305, GSE297707, GSE302944, GSE308674, GSE315612,
GSE315678, GSE316347, GSE317978, and GSE326587.

Acquisition is frozen to cached inputs so repeated results test analysis/model stability rather than
GEO server variance. LLM datatype cross-checking is enabled and Hallmark GSEA remains live. The
within-run semantic-alignment cache is reset at the start of every independent case run: QC/design
reuse is free, but repeat 1 cannot supply an LLM answer to repeats 2 or 3.

## Trial hard gates

A trial fails if any of the following occurs:

- an input hash changes or the selected expression matrix differs from the manifest;
- matrix type or DA route differs from the biologically valid frozen expectation;
- the design column, control, treatment set, or contrast count differs;
- sample alignment fails, falls below the frozen minimum, or misses a required LLM path;
- pipeline status is not `deg_gsea_ok`, DEG sanity is not `ok`, or the run is non-terminal;
- expected DEG, GSEA, QC, decision, status, or evidence artifacts are absent.

## Cross-repeat stability gates

For every case, all three trials must pass. Every expected contrast must yield all three pairwise
repeat comparisons. Minimum pairwise thresholds are:

- DEG full-ranking log2FC Pearson correlation >= 0.99;
- GSEA full-ranking NES Pearson correlation >= 0.99;
- significant DEG Jaccard >= 0.95;
- significant Hallmark pathway Jaccard >= 0.95.

Thresholded overlaps are interpreted alongside full rankings, but this deterministic repeated-input
benchmark requires both. Any missing metric is a failure, not silently omitted coverage.

## Cost and stopping rule

The pre-run plan assumes 42 structured calls, $0.126 regular-price cost, and $0.252 under a 2x peak
contingency. The hard token budget is $0.50. After every trial the runner records actual provider
usage; it stops before the next trial if 2x measured estimated spend exceeds the hard limit. Every
executed call must have measurable token usage and a recognized price.

## Acceptance

The experiment passes only when all 60 trials execute and pass, all 20 cases satisfy repeat-stability
thresholds, all input hashes match, all LLM calls are measured and priced, the peak-contingency spend
is within budget, and the independent audit reports no blocking findings. Audit score and coverage
must be reported separately; subset-stability coverage is supplied by `case_stability.csv`.