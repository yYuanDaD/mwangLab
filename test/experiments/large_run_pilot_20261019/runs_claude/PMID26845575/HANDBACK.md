# HANDBACK: PMID26845575 / GSE69699

## Outcome

The case stopped at the `design` gate with `manual_review`. Nothing was executed, so there are no DEG counts.

## What ran

1. `tools.case_runner inspect GSE69699`. It downloaded the series and merged `GSE69699_RAW.tar`: 21302 Ensembl genes x 8 samples. The values are RPM (`data_processing`: "Read counts were converted to RPM"; each column sums to 1e6).
2. `prep_counts.py` reconstructed read counts from the RPM values.
   - Within each sample, every value is an exact multiple of that sample's smallest non-zero RPM (one read), so count = round(RPM / min_nonzero_RPM).
   - Library sizes come out at 324k-1.15M reads. The reconstructed column sums match within 4 reads, and the largest rounding residual is 0.31 read.
   - The script also applied the paper's 125 RPM gene filter. The rule "mean RPM > 125 in at least one assay x condition group" gives exactly the paper's 1011 genes.
   - Outputs are in `prep/`.
   - Slc25a25 (ENSMUSG00000026819) passes the filter. Its RPM is about 4x higher with exercise in mRNA and about 18x higher in RPF, which matches FIG4.
3. `tools.case_runner execute case_spec.json`. Five records were written, and the contract validator reported no errors.
   - Gates `paper_reconstruction`, `ownership`, `alignment` (exact match on GSM ids, coverage 1.0) and `matrix` (raw counts reconstructed from RPM) are valid.
   - `design` is `manual_review`.

## Paper vs data

- **Paper plan** (S2.7.p1, S3.p4, SUP3): edgeR with TMM on the 1011 genes > 125 RPM, comparing exercise with no exercise separately for each assay. The DEG rule is raw P < 0.01 with no fold-change cutoff.
  - Paper counts: 26 DEGs at the transcription level (mRNA-Seq) and 37 at the translation level (RPF).
- **Data**: n = 2 biological replicates per arm per assay. Each replicate is a pool of 3 mice (S2.3.p1). Only the no-exercise and immediately-after-exercise groups were sequenced. The 1h/2h/4h groups were used for qPCR and western blot only (S2.2.p1, S4.p1).
- **Our DEG counts**: none (not executed). Compared with the paper: 0/2 contrasts run, paper 26/37.

## Why it stopped (tool problem)

The two rules below contradict each other:

- The skill and decision contract say small n alone is not a stop (`references/decision-contract.md:78`, `SKILL.md:84`). They say to run such a contrast and label it exploratory.
- The runner's suitability check fails any planned comparison with fewer than 3 samples per group (`tools/suitability.py:259` `check_sample_size`, `MIN_GROUP`; verdict set at `tools/suitability.py:502-505`). The validator then rejects a valid design that carries that verdict (`tools/decision_contract.py:172`).

The case spec offers no override for this:

- `run_joint_deseq2`'s `include` (`tools/joint_contrasts.py:139`) works only at execution.
- Even with `include`, the suitability check still needs at least one planned comparison that passes.

I rejected one workaround: adding a pooled 4-vs-4 grp comparison across assays only to pass the gate. It would be an estimand the paper never tested.

The first attempt, recorded as a valid design, is kept in `case_spec_attempt1_valid_design.json` and `_previous/`. It names the intended executions:

- edgeR per assay, primary;
- DESeq2 per assay, sensitivity;
- ORA on the edgeR tables.

## Deviations that would have been declared

- Counts reconstructed from RPM.
- The 125 RPM filter applied in the prep script. The runner's `filter_low_counts` cannot express a group-mean rule, so edgeR library sizes would be sums over the 1011 retained genes.
- The repository edgeR executor uses the QL F-test (`tools/edger_tools.py:124`). The paper does not name its edgeR test; it was most likely the classic exactTest.

## Other tool notes

- The sex check reports `no_markers` on this matrix. The 1011-gene filter removed the sex-marker genes, and all mice are male (S2.2.p1). This is not a problem for this case.
