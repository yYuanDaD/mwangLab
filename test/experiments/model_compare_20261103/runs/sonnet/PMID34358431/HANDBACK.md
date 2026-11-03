# HANDBACK PMID34358431 / GSE174785 (Sonnet 5.5)

STATUS: refused (at the `design` gate)

## What ran
Skill bioinformatics-workflow, native mode (external LLM attempts: 0). Driver: `scripts/01_gates.py`. Recorded gates:
`paper_reconstruction`, `ownership`, `alignment`, `matrix` (all valid), then `design` = refused. No execution, threshold, or study record (stopped case). `validate_decision_contract.py`: VALID (5 records).

- Paper (PMC8432967, `S2.2.p2`, `S2.6.p1`, `S4.4.3`, `TAB1`, `DA.p1`): GSE174785 is the bulk RNA-seq of sorted muscle ECs, RmEC (soleus, oxidative) vs WmEC (EDL, glycolytic), WT and EC-specific Atf4 knockout (5 reps per cell, 20 samples). Method: kallisto counts into DESeq2.
- Exercise (14 d voluntary wheel running) appears in the paper only in histology and in the scRNA-seq dataset GSE158984 (`S2.5.p1`), not in GSE174785.
- GEO metadata for GSE174785: the only factors are muscle (soleus/EDL) and genotype (WT/Atf4 dEC); treatment_protocol mentions only tamoxifen. No sedentary/exercised label, no time factor.
- Ownership: valid (accession, 20 samples = 5 x 2 x 2, tissues and genotypes match the paper).
- Alignment: 20/20 exact. Matrix columns are `GSM..._koR1` etc.; the metadata index is the GSM id only, so I derived `matrix_id` from the metadata `supplementary_file_1` file name (regex, exact match, no position) and aligned on it.
- Matrix: kallisto est_counts at transcript level (ENSMUST ids), non-negative, 62% integer-valued, column sums equal est_counts sums of the per-sample files (TPM sums to 1e6, not this). Count scale, consistent with the paper's DESeq2 input; gene-level collapse would be needed before DE.
- Design: refused. Rejected candidates: WT RmEC vs WmEC (muscle-bed difference, the paper's 782 DEGs), WT vs Atf4 dEC (genotype), genotype x muscle interaction. None estimates an exercise effect, so any DEG count would answer a different estimand.

## DEG counts vs paper
None computed (refused before execution). Paper threshold: padj < 0.05 and log fold change > 1 (base not stated; log2 assumed), `S4.4.3.p2` / `S2.6.p1`. Paper counts for non-exercise contrasts: 782 DEGs WT RmEC vs WmEC (also 140 stated for the second direction/set, and 211/126 remaining after Atf4 knockout). Paper reports no bulk-RNA-seq exercise DEG count for this accession.

## Deviations
None executed. The paper's own bulk contrast (RmEC vs WmEC) was deliberately not run because it is not an exercise comparison.

## Tool problems
- `native.align_to_metadata` (`tools/native.py:287-343`) only matches the metadata index or one column; the merged-from-tar matrix uses `GSM_label` column names, which matched neither, so a derived key column was needed (`derive_columns` pattern on `supplementary_file_1` worked). Not a bug, extra step.
- `GSE174785_merged_from_tar.csv` is transcript-level (ENSMUST), not gene-level; the merge tool gives no gene collapse (relevant only if the run had continued).
- A multi-line bash heredoc containing apostrophes failed to parse in the Bash tool (harness quirk); used a file write instead.
