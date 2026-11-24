# HANDBACK: PMID32969079 / GSE146336

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE146336` (data cached): 1 matrix, `GSE146336_counts.csv.gz`, 55,487 Ensembl genes × 22 samples, all integers (featureCounts). The metadata has two grouping columns: genotype (WT 11 / TRa1 KO 11) and treatment (T3 13 / vehicle 9). All samples are male soleus.
- `case_spec.json` was executed. Gates recorded: paper_reconstruction, ownership, alignment (exact key from the title prefix, 22/22), matrix (raw counts), and design (refused). The validator passed with 0 errors and 5 records. No DE executions or enrichment ran.

## Why refused
The RNA-seq design is genotype (WT vs muscle TRα1 L400R loss-of-function) × T3 vs vehicle, given for 7 days (S2.6.p1, S3.3.p1, FIG3). Exercise (treadmill to exhaustion, 6-week voluntary wheel running; S2.4, S3.1.p1, FIG1E/F) was only measured as a phenotype in separate cohorts that were not sequenced. The data therefore contain no exercise effect on gene expression to estimate. I rejected the T3 contrast because it is a pharmacological treatment, and the genotype contrast because it is not exercise.

## DEG counts vs paper
- Paper threshold: FDR-adjusted P (S2.11.p1). The cutoff is taken as 0.05 from the paper's general P < .05 rule, with no fold-change rule.
- Paper: 788 DEGs for KO vs WT under vehicle (S3.3.p1). There is no exercise contrast in the paper's RNA-seq.
- Ours: none run (refused). 0/0 exercise contrasts.

## Deviations
- None executed. The GEO group sizes (vehicle 9, T3 13) differ slightly from FIG3 (vehicle n=5-6/4-6, T3 n=5-6/7). This was recorded as a discrepancy and not evaluated.

## Tool problems
- Minor: when the design gate is refused without `factors`, the runner still runs the suitability report. It returns `not_analyzable` with `failed: ["sample_size"]` and 0 comparisons, which is misleading because the actual stop reason is the absence of an exercise factor, not sample size. See `GSE146336/suitability/suitability.md`. The suitability check should be skipped, or labelled as `no factors given`, when design is refused.
- Inspect: the GEO metadata spellings "T3 treatmant" and "vechicle" are kept verbatim. This caused no problem here.
