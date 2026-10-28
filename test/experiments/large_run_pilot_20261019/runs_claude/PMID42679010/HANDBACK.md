# HANDBACK: PMID42679010 / GSE344550

**Status: refused at `design`. There is no exercise contrast.**

## What ran
- I skipped preflight, as instructed.
- I ran `python -m tools.case_runner inspect GSE344550`. GEO downloaded the series into `data/GSE344550`: one matrix (`GSE344550_macrophage_counts_rpkm.txt.gz`, 36,591 features x 30 samples) and the metadata.
- I read the paper (PMC13557500). It is about fluconazole-resistant *Candida parapsilosis* outbreak isolates. GSE344550 is the RNA-seq of human macrophages infected ex vivo with LBP isolates (29T, 49B) and BP isolates (1T, 35B) at 3 h and 24 h, plus uninfected controls (FN.p1, S2.7.p1, S4.13.p1).
- I ran `python -m tools.case_runner execute case_spec.json` with the gates paper_reconstruction, ownership, alignment, matrix and design. Design was `refused`.
  - The validator returned 5 records and 0 errors.
  - Alignment matched exactly on `Library name` from `description`, 30/30.
  - The case route is `stopped`.
- No DE execution and no enrichment ran.

## Why it was refused
The only factors are fungal isolate (BP/LBP) and hours post-infection. No exercise, training or physical-activity arm exists in the paper or in GEO, so the requested estimand cannot be identified. I did not substitute the paper's BP-vs-LBP contrast, which is about infection isolates.

## DEG counts vs the paper
- Not applicable. No contrast was run.
- Paper threshold: only `|log2FC| > 1`, with no p-value or FDR rule (S4.13.p1).
- The paper reports no macrophage DEG count in its text; it reports GSEA results (Fig 5, S4 Fig).

## Deviations and caveats (recorded; they do not change the outcome)
- The paper used edgeR on raw counts (`~0 + group:time`). GEO holds only RPKM (data_processing: "RPKM normalized transcripts"; integer fraction 0.55). The paper's route could therefore not be reproduced exactly, even for the paper's own question.
- Uninfected controls sit in three time labels: Control (3), 3 hour (2) and 24 hour (3). Infected groups at 3 h have n=2 for 1T and for 35B.

## Tool problems
None that blocked the run.
- Minor: `inspect` lists the matrix as "linear_normalized ... or estimated_counts". It does not use the `RPKM` statement in data_processing or the file name to narrow this down. I decided the type by hand.
