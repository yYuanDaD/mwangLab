# HANDBACK: PMID37059838 / GSE228901

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE228901`: the data were already cached. There are 15 female liver samples (A1-A5 Adult 6 mo vehicle, O1-O5 Old 22 mo vehicle, P1-P5 Old PDX). The matrix `GSE228901_counts.txt.gz` holds integer featureCounts counts, 55,450 Ensembl genes. There is also a derived VST file, which was not used.
- `python -m tools.case_runner execute case_spec.json` recorded these gates in order:
  - `paper_reconstruction`
  - `ownership`: owned (S2.9.p3 names GSE228901)
  - `alignment`: exact match on `title`, 15/15 samples
  - `matrix`: raw counts
  - `design`: refused
- The validator returned 0 errors. Suitability ran on the 3 groups and called it "analyzable", but the design was refused on the estimand, not on the data.
- No DE executions and no enrichment were run.

## Why refused
The paper is about aging and Protectin DX. Its arms are Adult vehicle, Old vehicle and Old PDX gavage for 9 weeks. Treadmill exhaustion and the 4-day voluntary wheel test are fitness assessments given to every animal in every group (S2.2.p1, S2.4.p1-p9). No group was exercise-trained or kept sedentary, and the words "exercise" and "training" never appear in the article.

The metadata columns for treadmill distance and wheel km/d are per-animal outcome readouts, and they are confounded with age. The paper's planned contrasts are Old vs Adult (aging) and PDX vs Old (drug). Neither one estimates an exercise effect.

## DEG counts vs the paper (paper threshold: FDR q < 0.05, no fold-change cutoff, S3.7.p2)
- Old vs Adult: paper reports 1,621 DEGs. Not run (not an exercise contrast).
- PDX vs Old: paper reports 0 genes at FDR < 0.25. Not run.
- No exercise contrast exists, so 0/0 contrasts were run.

## Deviations
None. The case was stopped before the method gate.

## Tool problems
None blocking. One minor point: the `treatment_protocol_ch1` and `growth_protocol_ch1` strings show mojibake (for example `渭L`, `庐`) in inspect's output. This is a UTF-8 file being decoded as GBK when the metadata CSV is read or written. It is cosmetic and did not affect any decision.
