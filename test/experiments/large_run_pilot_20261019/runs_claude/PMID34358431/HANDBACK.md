# HANDBACK: PMID34358431 / GSE174785

**Status:** refused at the `design` gate. No exercise comparison exists in this accession.

## What ran
- `python -m tools.case_runner inspect GSE174785`: used the cached data. The `_RAW.tar` was merged into 129,439 ENSMUST transcripts x 20 samples. I checked that the merge took the kallisto `est_counts` column and not `tpm`: the GSM5328123 column sum is 1.411e7, while TPM would sum to 1e6.
- `python -m tools.case_runner execute case_spec.json`: recorded the paper_reconstruction, ownership, alignment, matrix and design gates. The design gate is `refused`. The validator reported 5 records and 0 errors. No DE executor ran.

## Why it was refused
- GSE174785 contains 2 muscle EC subtypes x 2 genotypes x 5 replicates, all from unexercised mice:
  - muscle EC subtypes: RmEC from soleus, WmEC from EDL;
  - genotypes: WT and Atf4 EC-KO.
- The paper studies exercise (14-day voluntary wheel running, S2.5.p1) with histology, EdU, flow cytometry and scRNA-seq. The scRNA-seq is GSE158984, not this accession.
- Neither muscle subtype nor genotype is an exercise effect. The suitability report did find 5 analyzable non-exercise comparisons, but none of them answers the exercise question.

## DEG counts vs paper
- Paper threshold: padj < 0.05 and log fold change > 1 (S2.6.p1, Fig6C legend, S4.4.3.p2).
- Paper counts: 782 DEGs for WT RmEC vs WmEC. The paper says 211 of them "remained" in Atf4-KO RmEC vs WmEC; it also mentions 140 WmEC DEGs, but the wording is ambiguous.
- Our counts: none. Nothing was run, because the requested estimand (exercise) is absent.

## Deviations and notes
- The paper says Smart-seq2 libraries (S4.4.3.p1), but GEO `extract_protocol` says TruSeq stranded mRNA. This was recorded and does not block the case.
- The matrix is transcript-level estimated counts. A paper-aligned rerun of the subtype contrasts would first need a transcript-to-gene summary.

## Tool problems
- None blocking.
- Minor: inspect labels the merged matrix "linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts" and does not say which kallisto column the tar merge used. I had to check this by hand.
