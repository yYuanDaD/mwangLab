# HANDBACK: PMID 25484259 (Lindholm et al. 2014, Epigenetics; PMC4622000)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID25484259` (run label PMID25484259)
Spec: `case_spec.json` (built from a scratch script, not a driver). Runner: `python -m tools.case_runner execute`.
Validator: 28 records, 0 errors. Evaluator `audit_run.py --no-write`: verdict pass, score 100, coverage 90.2, no blocking findings.

## Paper (what it intends)
- Design: 23 sedentary young adults (12 M, 11 F) did 3 months of supervised one-legged knee-extension endurance training. Vastus lateralis biopsies were taken from both legs before (T1/U1) and 24 h after the last session (T2) (S3.1.p1, S5.1.p1).
- RNA-seq DE (S5.4.p2): edgeR on gene counts, with group (T2 vs T1, trained leg), library preparation and individual as covariates. Threshold **FDR < 0.05, no fold-change cutoff**. Result: **4076 DEGs** (S3.1.p2, S4.p2).
- Data (S5.6.p1): GSE58608 and GSE60590 are the expression series; GSE60655 is methylation and was not requested. GSE60591 is the GEO SuperSeries of the two expression series.

## Data facts
- All three series deposit only Cufflinks `genes.fpkm_tracking` files per sample (TopHat 2.0.4 + Cufflinks 2.0.2). There are **no read counts**, and there is no library-preparation annotation.
- GSE58608 (24 samples): 12 subjects x {T1, U1}, all taken before training.
- GSE60590 (33 samples): 22 T2 samples, plus 11 T1 samples from the 11 other subjects.
- GSE60591 (57 samples) = GSE58608 + GSE60590. It has T1 for 23 subjects and T2 for 22; subject 13 has no T2.
- Subject, arm (T1/T2/U1) and series batch were parsed from the per-sample file name in `supplementary_file_1` (`<subject><T|U><1|2>.fpkm`). This file name equals `original sample id`.

## What ran

| Case | Gate outcome | Model | Samples | DEGs at the paper's rule (padj<0.05) | Up / down | Paper |
|---|---|---|---|---|---|---|
| GSE58608 | **refused at design**: baseline only (T1/U1), no post-training sample | - | - | - | - | - |
| GSE60591 (primary) | declared deviation | limma on log2(FPKM+1), `~ Treatment + C(subject) + C(batch)` | 23 T1 + 22 T2 | **1608** | 1069 / 539 | 4076 |
| GSE60591 (sensitivity, no batch term) | declared deviation | limma, `~ Treatment + C(subject)` | 23 T1 + 22 T2 | **2576** | 1583 / 993 | 4076 |
| GSE60590 (sensitivity, pairs within the series) | declared deviation | limma, `~ Treatment + C(subject)`, complete pairs | 11 pairs | **1428** | 899 / 529 | 4076 |

- Gene filter: FPKM >= 1 in at least as many samples as the smaller arm (22, or 11 for GSE60590), leaving about 12.4k of 61,779 genes.
- Audit rule (padj<0.05 and |log2FC|>log2(1.5)), a labelled comparison only: 205 / 72 / 203 DEGs.
- The primary model's log2FCs are identical to those from the 11 within-series pairs. This is expected: with a subject block, the series-batch term absorbs the 11 cross-series pairs, so the training effect comes only from subjects that have both T1 and T2 in GSE60590. The no-batch model uses all pairs but assumes there is no library-prep or series effect.

### Named genes from the paper (primary model)
- Every gene the paper names as up has positive log2FC and padj<0.05: COL4A1 1.60, COL4A2 1.61, A2M, THBS4, PDGFRB, LAMA4, CS, SDHA, HADHA, COX7A2, MDH1, NDUFA8 and KDR.
- ATP5B (ENSG00000110955) is also up: log2FC 0.33, padj 0.0027. I looked it up by hand because the runner's symbol lookup returned null.
- Every gene the paper names as down has negative log2FC. No direction contradicts the paper.
  - padj<0.05: UACA, CUL3, TRDN and RYR1.
  - Not significant: MDM2, ZNF638, PPP1R12A, MEF2A, MYH3, TNNT2 and SH3GLB1. In the no-batch sensitivity MYH3 and RYR1 are strongly significant; MDM2, ZNF638, MEF2A and TNNT2 remain >0.05.

### Enrichment (primary table only, kept separate from the DE result)
- ORA: the top KEGG terms are oxidative phosphorylation and thermogenesis.
- GSEA Hallmark, most positive NES: oxidative phosphorylation (NES 3.28), EMT/ECM, fatty-acid metabolism, adipogenesis, coagulation and angiogenesis.
- GSEA Hallmark, negative NES: only G2M checkpoint and E2F targets (FDR > 0.05).
- These match the paper's themes (S3.5.p1): OXPHOS up, ECM and blood-vessel development up, cell cycle and DNA replication down.

## Deviations (declared in the records)
1. **Method:** limma on log2(FPKM+1) instead of edgeR on counts. The paper route is recorded as blocked because no counts were deposited, and the threshold source is `paper_on_deviation_route`. FPKM was not rounded into counts.
2. **Library-preparation covariate:** not deposited. The sub-series (GSE58608 = b1, GSE60590 = b2) was used as a proxy, and a sensitivity run without it is reported. The true library-prep layout is unknown, which is the main reason our counts differ from 4076 (along with FPKM vs counts and gene filtering).
3. **U1 (untrained-leg baseline) samples** were excluded from GSE60591, because the paper's RNA-seq DE is T2 vs T1 only.
4. **Metadata conflict, subject 7:** GSE58608 gives 7T1 as "right leg", but its publication id is 8L and GSE60590 gives 7T2 as "left leg". The arm was taken from the T/U code, so this has no effect on the design.
5. Sex pooled as in the paper (sex is constant within subject and absorbed by the subject block). No separate per-sex analyses were run.

## Tool problems
- `tools/case_runner.py:478-486`: the paper-gene lookup maps Ensembl IDs to *current* MyGene symbols, so retired symbols used in the paper (ATP5B -> ATP5F1B) come back `null` even though the gene is in the table and significant. Minor: the lookup should also try aliases.
- GSE58608, refused at design: the runner still ran the suitability report and gave `not_analyzable` / `sample_size` with 0 comparisons, although T1 and U1 each have n=12. This is harmless here because the case was refused for the estimand, but the reported reason is misleading.
- `tools/geo_tar.py:121`: Cufflinks files repeat some gene_ids (about 120 per sample, split loci). The FPKM merge sums them. This is reasonable but not logged. Note only.
- No executor failures. Network enrichment (Enrichr, MSigDB) completed.
