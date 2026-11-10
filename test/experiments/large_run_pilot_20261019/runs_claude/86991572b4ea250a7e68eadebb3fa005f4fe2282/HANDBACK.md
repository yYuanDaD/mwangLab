# HANDBACK: GSE86338 (PMC5538645, lncBATE10 / adipose browning)

## Outcome: refused at `design`

Validator: 5 records, 0 errors. Case status `stopped:design`, decision `refused`, execution `not_run`.

## What ran

1. `case_runner inspect GSE86338`: downloaded the series. Files: `GSE86338_gene_fpkm.txt.gz` (38,553 Ensembl genes x 18), `GSE86338_lncRNA_fpkm.txt.gz` (1,535 x 18), metadata.
2. Paper reconstruction from PMC5538645.paper.md:
   - Exercise arm: iWAT after a swimming program (S2.1.p1, S4.4.p1), compared with the room-temperature control iWAT. The cold (4C, 7 d) and CL316243 arms share that control.
   - Method: Cufflinks FPKM with compatible-hits-norm, then Cuffdiff (S4.3.1.p1).
   - Threshold: FDR <= 0.05 and |FC| >= 2 (S2.2.p1).
   - Paper's exercise result: 673 up and 826 down mRNAs (1,499).
3. Ownership confirmed: GSE86338 is cited in FN.p1 and S4.2.p1. GEO has 18 samples, as in the paper's PCA (S2.4.p1).
4. Alignment: matrix columns match the metadata `description` field exactly, 18 of 18. Group comes from the title (CNT/CL/COLD/SWIM). The 10 BAT samples (S3, S5) belong to separate experiments with their own controls, so they were excluded.
5. Matrix: Cufflinks FPKM, so the route would be log2(x+1) then limma. The Cuffdiff route is blocked because no alignments or counts were deposited.
6. Design: the suitability report is `not_analyzable` (sample_size: 0 of 6 comparisons have >= 3 per group).
   - Every iWAT arm has 2 libraries, and each library is a pool of 4 mice (S4.2.p1).
   - The planned exercise contrast, SWIM n=2 vs CNT n=2, cannot be recorded as valid, so the case is refused at this gate.
   - The planned route is written in the stop_reason: one limma model ~ grp over the 8 iWAT samples (residual df 4), contrast SWIM vs CNT, using the paper's threshold.

## DEG counts vs paper

- No DE was run, so there are no counts. The paper reports 673 up and 826 down mRNAs for exercise (FDR <= 0.05, |FC| >= 2).
- For context only, from the same paper: cold 1,062 / 1,201 and CL316243 837 / 681.

## Deviations / discrepancies recorded

- Paper method (Cuffdiff on alignments) is blocked because only FPKM was deposited.
- GEO labels the CL316243 iWAT samples (GSM2300497/8) as RIP-Seq / library_selection "other". The paper describes polyA RNA-seq, so this is most likely a GEO labelling error.
- GEO lists all iWAT samples as 16 weeks old. The paper says the browning cohort was 12 weeks old, and the swim protocol started at 8 weeks and ran about 3–4 weeks.
- The paper itself ran Cuffdiff with n=2 pooled libraries per condition.

## Tool problems

- **The skill text and the enforced contract disagree on small n.**
  - SKILL.md ("When to stop") and decision-contract.md:78 say "Small n alone is not a stop... label it exploratory".
  - But `tools/suitability.py:273` (`check_sample_size`) fails the check when no planned or other comparison has n >= 3 (`MIN_GROUP = 3`, suitability.py:33). `tools/decision_contract.py:171` then rejects any valid design whose verdict is `not_analyzable`.
  - Result: a study where every arm has n=2 can only be refused. The exploratory/`include` path works only when at least one comparison has n >= 3.
  - The first execute attempt, with a valid design, was rejected with this NativeToolError. It is kept in `_previous/20261110T070911Z`.
- **There is no low-expression filter for FPKM input.** `filter_low_counts` in the case spec is raw-counts only, so roughly half the genes in the FPKM matrix would go to limma at FPKM 0. This was not exercised, because the case stopped before execution.
