# HANDBACK: GSE110507 / PMC7475200 (VDR overexpression induces skeletal muscle hypertrophy)

## What ran
- `tools.case_runner inspect GSE110507`: downloaded the series and merged `GSE110507_RAW.tar` into 32,883 Ensembl rat genes x 28 samples, all integer raw counts.
- `tools.case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment (exact on GSM index, 28/28), matrix (raw counts) and design. The case was **refused at design**. The validator found 5 records and 0 errors.
- No differential expression or enrichment was run.

## Why refused
- The request asks how exercise affects gene expression. GSE110507 contains only sedentary male Wistar rats in which the tibialis anterior was electroporated:
  - VDR-OE (pCAGGS-mVDR, right leg) vs empty pCAGGS (left leg), 7 animals;
  - VDR shRNA knock-down vs scramble, 7 animals. The paper does not report this arm.
- There is no exercise arm.
- The paper's exercise component is the human 20-week resistance exercise training cohort. It is a separate series, GSE47881 (S2.8.p1), and the paper uses it only to correlate VDR mRNA with gains in lean mass and 1-RM (S3.4.p1, FIG7).
- The rat RNA-seq contrast (VDR-OE vs contralateral control, paired) is a genetic gain-of-function estimand, so I did not run it as a stand-in for exercise.

## DEG counts vs paper
- Paper (S3.2.p1): 3,330 genes at P < 0.05 (raw p, no fold-change rule) for VDR-OE vs control. Method: edgeR with CPM filter at a count of 10, TMM, and glmFit paired by animal (S2.7.p1). Also 310 gene sets at FDR < 5%.
- Ours: none. The case stopped at design and no exercise contrast exists in the data.

## Deviations / notes
- Ownership: the paper names no accession for its rat RNA-seq. I matched GSE110507 on several points:
  - protocol: IVE with pCAGGS-mVDR vs empty vector in the TA;
  - HiSeq 4000 with TruSeq libraries;
  - n = 7;
  - the GEO contact is I. Gallagher, who is IJG, the bioinformatician in S5.p1.
- Of the 28 samples, only the 14 knock-in samples (animals 416-422) belong to this paper.

## Tool problems
- None in repository tools.
- My first spec had a JSON escape error: the shell heredoc collapsed `\d` to `\d`. I removed the unneeded `matrix_column_pattern`, because a raw_tar merge already names columns by GSM.
