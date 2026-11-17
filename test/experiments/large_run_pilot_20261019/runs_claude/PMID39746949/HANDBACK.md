# HANDBACK: PMID 39746949 / GSE273694

**Status: refused at `design`.**

## What ran
- `python -m tools.case_runner inspect GSE273694`: downloaded the series. Files: `GSE273694_gene_count_matrix.csv` (56,847 genes x 14 samples, all integers, IDs `ENSMUSG...|Symbol`) and the metadata.
- I read the paper (PMC11695632.paper.md) and wrote `case_spec.json` with these gates: paper_reconstruction, ownership, alignment, matrix, design (refused).
- `python -m tools.case_runner execute case_spec.json` completed. The validator wrote 5 records with 0 errors. Alignment was exact on `description` for 14/14 samples. Route: `stopped`.

## Why it was refused
- GSE273694 is resting gastrocnemius from male PanK4 WT (n=8) and PanK4 mKO (n=6) mice. All of them were fasted for 4 h and injected with glucose 40 min before euthanasia (S4.1.1.4.p1). The GEO `treatment` value is the same for all 14 samples.
- The only factor is genotype. There is no exercise or sedentary arm.
- The paper's exercise data were never sequenced. They are:
  - human p-PanK4 Ser63 phosphoproteomics and Western blots (Fig. 1A–C);
  - mouse treadmill glucose uptake and metabolite measurements (Fig. 4E–H, Fig. S7).
- The genotype contrast (mKO vs WT, DESeq2, used for the BCAA-gene check in S2.6.p5 and Fig. S9) is a valid comparison. But it does not estimate an exercise effect, so I did not run it in place of the exercise question.

## DEG counts vs the paper
- The paper gives no DEG count for this RNA-seq. It says only that BCAA-catabolism genes showed "no significant alterations" (S2.6.p5).
- The paper states no threshold. It names only DESeq2 v1.34.0 (S4.1.1.4.p1).
- No executions were run, so this run has no DEG counts.

## Deviations and discrepancies
- **Matrix quantification:** the paper says abundance was expressed as FPKM, but the GEO file holds integer prepDE.py read counts. This is consistent with the paper using DESeq2 and would not have blocked a genotype analysis.
- No other deviations: nothing was executed.

## Tool problems
None blocked the run. One observation: the suitability report returned `analyzable` (1 comparison) for genotype (it tests whether the given factors can be analyzed, not whether an exercise contrast exists) when `planned` was empty. Deciding that this is not an exercise contrast was left to the agent, which is by design.
