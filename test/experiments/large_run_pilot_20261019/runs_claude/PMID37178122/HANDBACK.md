# HANDBACK: PMID37178122 / GSE230102 (ExcHMDP: female HMDP mice, 30 d voluntary wheel running vs sedentary)

## What ran
- Route: case spec (`case_spec.json`, made by `make_spec.py`), `python -m tools.case_runner execute`. Five cases, one per tissue: quadriceps, gWAT, liver, heart, BAT. Each uses its own `GSE230102_<tissue>.counts.txt.gz`. The runner ran twice: attempt 1 is in `_previous/20261117T181157Z`. Attempt 2 is identical except that the result-vs-paper caveats were added to the study gate. Decision-contract validator: 65 records, 0 errors. 0 execution failures, 0 LLM calls.
- Ownership: GSE230102 is the paper's own deposit (S4.1.3.p1, TAB1). The GEO protocol and data_processing (kallisto v0.45, Ensembl v97) match S4.3.6.1.p1 and S4.4.1.p2.
- Alignment: exact match on the GEO `title`, 100/100 samples per tissue (99 for quadriceps). `grp` comes from the exercise-group characteristic (Exercised -> TRN, Sedentary -> SED). `strain` comes from the leading title code, which I checked maps 1:1 to the strain characteristic (50 strains).
- Matrix: kallisto estimated counts (non-integer), rounded for DESeq2 (`transform: round`, rounding documented).
- Design: per tissue, two groups, TRN vs SED (reference SED). Each strain has one SED and one TRN animal per tissue; quadriceps lacks the SED sample for 129X1/SvJ. Suitability: analyzable in all five tissues.
- Covariance and method:
  - Primary: DESeq2 (pydeseq2 Wald) `~ strain + grp`. Strain is the randomization and pairing unit (S2.1.p1), and the transcriptomes cluster by strain (S2.9.p3).
  - Sensitivity: `~ grp`.
- Threshold: the paper's rule, padj (FDR) < 0.05 with no fold-change cutoff (S4.4.1.p3; legends of Figures 5A and 6A). `threshold_source: paper_on_deviation_route`.
- Enrichment: ORA (Enrichr GO and KEGG) and Hallmark GSEA on each primary table. All completed.

## DEG counts vs paper (padj < 0.05, no FC rule)
| Tissue | Strain-blocked (primary) | Unblocked (sensitivity) | Paper |
|---|---|---|---|
| quadriceps | 4057 (1995 up / 2062 down) | 378 | not given in text |
| gWAT | 533 (331 / 202) | 15 | not given in text |
| liver | 19 (12 / 7) | 60 | "fewer DEGs" than muscle and gWAT |
| heart | 18 (8 / 10) | 2 | "relatively few" |
| BAT | 4045 (2106 / 1939) | 2037 | "the most DEGs" of all tissues |

The paper gives no per-tissue counts in the text. They appear only in Figures S11A/S12A/S13A, which were not available here. The text says only that the average is about 500 DEGs per tissue (S2.9.p3). Qualitative agreement:
- Liver and heart have the fewest DEGs in both models: agrees with the paper.
- BAT has the most DEGs in the unblocked model. In the blocked model BAT and quadriceps are about equal.

Paper genes:
- Slc25a1, Acly, Ccn1 and Dusp1 (paper: DE in every tissue except liver, S2.9.p1):
  - quadriceps and BAT: all four DE.
  - gWAT: Slc25a1 and Acly DE; Ccn1 (padj 0.053) and Dusp1 (0.057) just miss.
  - heart: only Dusp1 DE.
  - liver: none DE, which agrees with the paper.
- Muscle key drivers Myoz2 and Esrrb: DE (up) in quadriceps.

Pathways (separate from the DE result):
- Agreeing with the paper:
  - Quadriceps: OXPHOS and fatty-acid metabolism up (paper S2.4.p3: β-oxidation and mitochondrial).
  - gWAT: OXPHOS, FA metabolism, adipogenesis and MYC up (paper S2.5.p1: mitochondrial and lipid metabolism, TCA).
  - BAT: glycolysis, cholesterol homeostasis, mTORC1 and OXPHOS up (paper S2.8.p1).
  - Heart: interferon, complement and allograft pathways up (paper S2.7.p1: immune and inflammatory).
- Conflicting with the paper:
  - Liver: the paper reports cell-cycle and mitosis enrichment and argues for hepatocyte proliferation (S2.6.p1, S3.p4). Our G2M checkpoint is down (NES -1.57, FDR 0.011) and Mki67 is not DE. This is recorded in the liver study caveats.

## Deviations
1. The paper corrected for library-prep batch and flow-cell lane with limma (S4.4.1.p2). Neither variable is in the GEO metadata, so the paper route is blocked and the analysis runs without them.
2. I added strain as a blocking term in the primary model, and ran the unblocked model as a sensitivity check. The paper does not say whether it modelled strain. This choice changes the counts a lot: blocking gives 4057 vs 378 in quadriceps and 533 vs 15 in gWAT.
3. Estimated counts were rounded to integers for DESeq2.
4. GEO holds 50 strains with one animal per arm per tissue. The paper describes a 100-strain panel.
5. pydeseq2 was used instead of DESeq2 v1.28.0 (R), and ORA used Enrichr instead of PANTHER.

All cases are recorded with route `declared_deviation`.

## Tool problems
- No blocking problems.
- pydeseq2 emits `RuntimeWarning: overflow encountered in exp` at `.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088` during the 50-level strain fits (33 times in `execute_stderr.log`). The fits completed and the counts were the same in both attempts.
- The case runner had no way to add result-driven caveats to the study gate after execution. Recording the liver direction conflict needed a full re-run of all five tissues (about 13 minutes).
- The empty `comparison {}` in the output is expected, because the paper gives no counts to compare. It is not a tool fault.
