# HANDBACK: PMID40000838 / GSE280656

## What ran
- Route: case spec (`case_spec.json`, built by `prep/build_spec.py`; cartilage stop applied by `prep/stop_cartilage.py`). `python -m tools.case_runner execute` finished with status completed and 21 records, 0 validator errors.
- Prep: `prep/drop_nan_rows.py` removed 57 gene rows that are NaN in every sample, in both deposited RSEM matrices. No other values were changed.
- Two cases, one per tissue. The tissues come as separate matrices, and the paper analyses them separately (Fig 3 synovium, Fig 4 cartilage).
  - **GSE280656_synovium** (paper_aligned, completed). There are 15 samples, n=3 in each of Control, S1, S4, S24 and R24. Alignment is exact on `title`. Matrix: RSEM expected counts. The method is one joint pydeseq2 model, `~ grp`, on all 15 samples, which is how iDEP works. Counts were rounded, and the filter kept genes with CPM >= 0.5 in at least 1 sample (the assumed iDEP default). That filter kept 17,315 genes against the paper's 17,316 (S4.4.p3). All 7 planned pairwise contrasts ran. Enrichment: Enrichr ORA up and down plus Hallmark GSEA, for S1 vs control and R24 vs control.
  - **GSE280656_cartilage** (stopped at `design`, `manual_review`). Control has n=3, but each exercise arm has n=2. Because no planned comparison has n >= 3 per arm, the suitability report fails `sample_size` and returns `not_analyzable`, and the contract then refuses to record the design as valid. Nothing was run for cartilage.

## DEG counts (paper threshold: FDR < 0.1 and fold change > 2, i.e. padj < 0.1 and |log2FC| > 1; S4.4.p2, iDEP defaults)
Synovium, our results (up/down). The audit column is padj < 0.05 with no fold-change cutoff.

| Comparison | n (up/down) | audit n |
|---|---|---|
| S1 vs Control | 1104 (598/506) | 4896 |
| S4 vs Control | 412 (180/232) | 1776 |
| S24 vs Control | 171 (83/88) | 500 |
| R24 vs Control | 1844 (1008/836) | 6568 |
| S4 vs S1 | 1373 (626/747) | 5114 |
| S24 vs S4 | 639 (365/274) | 2510 |
| R24 vs S24 | 1377 (699/678) | 5261 |

- The paper gives its DEG counts only as a figure (Fig 2b), and the numbers are not in the text, so no exact count comparison was possible.
- The qualitative pattern matches the paper:
  - S24 vs control has the fewest DEGs in synovium (S2.2.p1).
  - R24 vs control has far more DEGs than S24 vs control (S2.5.p1).
- Named genes match in direction:
  - Nr4a3 is up at S1 (log2FC 4.8) and down from S4 to S24.
  - Inhba is up at S1, at R24 and in R24 vs S24.
  - Saa3, Clec4d, Calca and Ecel1 are up at S1, S4 and S24.
  - Il1b is up at S1 and at R24, where it passes narrowly (padj 0.083 against the 0.1 cutoff, log2FC 1.18).
- Overlaps are larger than the paper's:
  - S1 and S4 share 102 DEGs (paper 52).
  - S4 and S24 share 42 (paper 9).
  - 8 DEGs are common to all three (paper 4).
  - The paper probably used other gene-set restrictions; for example its follow-up analyses keep protein-coding genes only (S4.4.p3).
- GO BP results agree in direction: S1 down is muscle contraction terms (the paper's "muscle system process"), and R24 up is immune and phagocytosis terms.
- Cartilage: not run (stopped), so there are no counts.

## Deviations
- pydeseq2 Wald test instead of iDEP's R DESeq2.
- RSEM expected counts rounded to integers before DESeq2.
- The iDEP low-count prefilter is assumed (CPM 0.5 in at least 1 sample); the paper does not state it, but the kept-gene count matches.
- DESeq2 independent filtering uses alpha = 0.1, the paper's FDR.
- Enrichment uses Enrichr GO 2023, not Metascape, and is limited to S1 and R24 vs control.

## Tool problems
- The skill and the tools contradict each other on small n. The skill says "Small n alone is not a reason to stop" and points to the exploratory label (decision-contract.md). But `tools/suitability.py:259-277` (`check_sample_size`) fails the whole design when no comparison has n >= 3 per arm, `tools/suitability.py:502-505` makes that a hard `not_analyzable`, and `tools/decision_contract.py:172-173` rejects a valid design under that verdict. The `include` argument of `run_joint_deseq2` (`tools/joint_contrasts.py:128`) can never be used when every comparison is small, because the case is rejected before execution. As a result the cartilage case (n=3 vs n=2, the same design the paper ran) could only be recorded as manual_review.
- The deposited matrices have 57 all-NaN rows. I removed them in a prep script before the first run, so a crash was never observed. Without that step, `tools/joint_contrasts.py:106` (`.round().astype(int)`) would probably fail on NaN. The runner and inspect do report the missing values, but they do not drop them.
