# HANDBACK: PMID34526402 / GSE166322

## What ran
- Case-spec route (`case_spec.json`), `tools.case_runner execute`. Status completed. The validator passed with 10 records and 0 errors.
- Input: `GSE166322_merged_from_tar.csv`, merged from the 21 per-sample RNA-seq files in `_RAW.tar`. GEO `data_processing` says these files hold TPM.
- Samples: the 9 libraries at 8 weeks (8w), n = 3 each:
  - Control_8w (Ctrl)
  - MDZ_8w (MDZ, early-life midazolam)
  - RUN_MDZ_8w (RunMDZ, MDZ mice given a running wheel)
- Excluded, with reasons recorded: 6 P10 RNA-seq libraries and 6 in vitro Egr1/Ctrl NSC libraries. The ATAC-seq and ChIP-seq samples are not in the matrix.
- Model: one limma model, `~ 0 + grp`, on log2(TPM+1), after a filter keeping TPM >= 1 in >= 3 samples (14,759 of 24,657 genes kept). It gives three contrasts:
  - primary: RunMDZ vs MDZ (paper Fig. 7B)
  - secondary: Ctrl vs MDZ (sign reversed relative to the paper's Fig. 3E)
  - exploratory: RunMDZ vs Ctrl
- Enrichment: not run, because the paper reports no pathway result for the running contrast.

## DEGs vs paper
Threshold is the paper's rule (Fig. 7B legend): q < 0.05 and FC > 1.5, i.e. padj < 0.05 and |log2FC| > 0.5849625. It is applied on the deviation route.

| Contrast | Ours | Paper |
|---|---|---|
| MDZ+RW vs MDZ (primary, exercise) | 328 (237 up, 91 down) | no total reported |
| MDZ vs Ctrl, 8w | 1972 (1671 up, 301 down in MDZ) | 1477 (604 up, 873 down) |
| Fig. 7B overlap: MDZ-up and reversed down by running | 80 | 42 |
| Fig. 7B overlap: MDZ-down and reversed up by running | 16 | 76 |
| RunMDZ vs Ctrl (exploratory) | 2753 | not reported |

- Both overlaps are significant, as in the paper (hypergeometric P = 5e-64 and 3e-5).
- The up/down balance is inverted relative to the paper. This is recorded in the study caveats.
- Notch2 moves in the paper's direction (up in MDZ, down with running) but is not significant here: padj 0.069 for MDZ vs Ctrl and 0.48 for RunMDZ vs MDZ.
- The audit rule (padj < 0.05, no FC cutoff) gives the same counts. With n = 3, every gene at padj < 0.05 already has |log2FC| > 0.585.

## Deviations
- The paper used DESeq2 on featureCounts raw counts, but GEO has only TPM. The paper route is blocked, and limma on log2(TPM+1) ran as a declared deviation.
- I added a low-expression filter (TPM >= 1 in >= 3 samples). The paper states no filter.
- No Ctrl+RW RNA-seq exists, so the running effect can only be estimated in MDZ-exposed mice. No interaction term is possible.
- The RUN_MDZ libraries have later GSM ids, which suggests a separate sequencing batch. No batch variable is recorded, so it cannot be modelled; this is listed as a caveat.

## Tool problems
- None blocking.
- The inspect profile labels the TPM matrix only as "linear_normalized or estimated_counts" (integer fraction 0.36, driven by zeros). The type was settled from `data_processing`.
- The Bash heredoc for writing the spec failed in this shell (quote parsing), so I wrote the spec with the Write tool. This was an environment issue, not a repository issue.
