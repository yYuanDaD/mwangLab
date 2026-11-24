# HANDBACK — PMID39639402 / GSE228869

**Outcome: refused at `design`.** No differential-expression model was run.

## What ran
- `python -m tools.case_runner inspect GSE228869` downloaded the series into `data/GSE228869`. It found one count table: `GSE228869_Row_counts_table_faps.txt.gz`, 32,622 rat Ensembl genes × 12 samples, all integers, from featureCounts.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment, matrix and design (refused). Alignment was exact on `source_name_ch1` and matched 12/12 samples. The contract validator returned 0 errors on 5 records. The case status is `stopped:design`.

## Why it was refused
1. **There is no exercise contrast.** The study only reduces muscle use. Its groups are a vivarium control, 7 days of hindlimb suspension (HS7) and 14 days (HS14) (S2.1.p2). There is no exercise, training or reloading arm. Exercise comes up only as cited background (S1.p2, S3.2.p1, S4.p1). The requested exercise effect cannot be estimated from these data.
2. **There is only one biological unit per group.** The paper says that at each time point, FAPs from the 8 animals were combined before in vitro expansion (S2.2.p4). So `rep1` and `rep2` are culture replicates of one pool, and any group effect is aliased with that group's isolation and expansion batch. The design is also 3 groups × 2 differentiation days × 2 replicates. The suitability report (`GSE228869/suitability/suitability.md`) therefore finds 0 of 11 comparisons with at least 3 samples per group (`not_analyzable`, failing on sample size).

## DEG counts vs the paper
- **Paper:** DESeq2 likelihood-ratio test across Contr/HS7/HS14, DEGs at **p.adj < 0.01** with no fold-change cutoff (S2.8.p1). The paper reports five degPatterns clusters of at least 30 genes each, but gives no total DEG count or per-contrast count.
- **Ours:** none, because the case stopped at design. There are 0 executed contrasts to compare.

## Deviations and discrepancies (recorded in the spec)
- **Differentiation day:** GEO includes day-0 and day-3 adipogenic-differentiation samples. The paper's RNA-seq methods describe only second-passage FAPs and do not say whether differentiation day was in the LRT model.
- **Reference genome:** the paper says STAR v2.604a with mRatBN7.2. GEO `data_processing` says STAR 2.7 with Rnor_6.0 (Ensembl 104).
- **Replication:** pooled animals, so the replicates are technical (see above).

## Tool problems
- **None blocking.** Minor: the suitability report splits comparisons by every listed factor, here `diff`. As a result, all simple grp contrasts show cells of n=2, even though grp alone has n=4 per level. That is correct for a factorial design, but the report has no pooled-over-`diff` view. This did not affect the decision.
- **Minor:** GEO `data_processing` contains mojibake (`fgsea 懈 clusterProfiler`, `1 渭M`). It comes from the GEO SOFT encoding, not the repository.
