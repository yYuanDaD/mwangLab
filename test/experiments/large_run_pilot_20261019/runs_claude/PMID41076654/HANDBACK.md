# HANDBACK: PMID41076654 / GSE303983

Paper: Molecular responses in abdominal subcutaneous adipose tissue after a session of endurance exercise: effects of exercise intensity (PMC12645526).
Design in the paper: 45 regular exercisers, each did one session of LOW, MOD or HIGH intensity (n=15 per group). Adipose biopsies were taken Pre and 1.5 h Post (90 RNA-seq libraries). DESeq2 `~ group + group:ID + group:condition`, Wald tests, BH adjusted P < 0.05, no fold-change cutoff (S2.6.2.1.p1).

## What ran

- `inspect` on GSE303983. The deposited `GSE303983_genes.counts.csv.gz` holds integer raw counts (62,700 genes x 90 samples).
- `prep_counts.py`:
  - strips the `_S<n>.counts` suffix so the columns equal the GEO `title` (90/90 exact);
  - turns ` ENSG...|SYMBOL` IDs into symbols (28 rows that share a symbol keep `SYMBOL|ENSG`);
  - applies the paper's low-count filter (>= 10 counts in >= 15 samples). It keeps exactly **17,466 genes, matching S3.3.p1**.
- `case_spec.json` has two cases:
  1. **GSE303983_by_intensity**, the paper's six planned contrasts. This case is **stopped at `design` as `manual_review`**. GEO does not record each participant's intensity group:
     - `treatment` is the constant "Exercise(high, moderate, or low intensity)";
     - the titles are `3X-<id>_PRE/POST`;
     - groups were assigned by counterbalancing (S2.3.p1), so the IDs do not encode them.
     DA.p1 says the metadata is on GitHub (github.com/ahnchi/3X-Study). I did not download it, because download permission covered GEO only. A subject-to-group table would unblock all six contrasts.
  2. **GSE303983_pooled**, an exploratory analysis. It runs a paired Post vs Pre contrast over all 45 subjects with pydeseq2 `~ subject + time`, which is the subject blocking the paper uses. Subject is nested in group, so this estimates the equal-weight average of the three intensity effects. That matches the paper's hypothesis 1 (S1.p3), but the paper reports no count for it. ORA and Hallmark GSEA were also run.
- The contract validator passed: 17 records, 0 errors.

## DEG counts vs the paper (BH adjusted P < 0.05, no fold-change rule; paper's rule)

| Contrast | Ours | Paper |
|---|---|---|
| LOW Post vs Pre | not run (no group labels) | 1003 (397 up / 606 down) |
| MOD Post vs Pre | not run | 1979 (773 / 1206) |
| HIGH Post vs Pre | not run | 759 (452 / 307) |
| HIGH vs MOD change | not run | 734 |
| HIGH vs LOW change | not run | 183 |
| MOD vs LOW change | not run | 0 |
| Pooled Post vs Pre (exploratory, not in paper) | 2878 (1318 up / 1560 down); 39 with an added \|log2FC\| > 1 | none reported |

Named genes from S3.4.p1, checked on the pooled contrast, all agree in direction:

- **Down after exercise, as the paper says:**
  - NR1D1: log2FC -1.56, padj ~ 0
  - CIART: -1.51
  - DBP: -0.95
  - PER1: -0.60
- **Up, as the paper says:** NAMPT, log2FC +0.47, padj ~ 0.
- **Unchanged, as the paper says:**
  - BMAL1: padj 0.19. GENCODE v44 calls it BMAL1, so the runner's lookup under `ARNTL` returned null.
  - CLOCK: padj 0.85.

Pooled Hallmark GSEA:

- Up: inflammatory response, TNFA/NFKB, IL6/JAK/STAT3, MYC targets.
- Down: adipogenesis (FDR 0.036).

This fits the paper's pathway themes qualitatively, but it is not a reproduction, because the paper used CAMERA on separate intensity groups.

## Deviations

- The per-intensity paper route is blocked because the group labels are missing. Only a pooled paired contrast ran, and it is labelled exploratory.
- The low-count filter was applied in the prep script, because the case runner has no prefilter option.
- pydeseq2 was used instead of R DESeq2.
- Enrichment used gseapy prerank on Hallmark plus Enrichr ORA, not the paper's CAMERA on GO/KEGG/Hallmark.

## Tool problems

- `tools/case_runner.py` (`Execution` model, around lines 114-127, and `MethodGate`, lines 109-111) has no option for a low-count prefilter. The paper's filter had to go into a prep script, although the skill says filters are method decisions made at execution.
- The runner's paper-gene lookup is an exact symbol match, so `ARNTL` returned null while the matrix uses the GENCODE v44 name `BMAL1`. There is no alias resolution.
- Deposited matrix column names (`<title>_S<n>.counts`) cannot be matched with `key_patterns`, which only derives keys from metadata. A prep script was needed to rename the matrix columns.
