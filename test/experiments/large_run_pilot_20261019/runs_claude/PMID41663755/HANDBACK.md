# HANDBACK — PMID41663755 / GSE200283

**Status: refused at the `matrix` gate (both tissues).** No differential expression or enrichment was run.

## What ran
- `python -m tools.case_runner inspect GSE200283` (the series downloaded into `data/GSE200283`): two supplementary matrices, `GSE200283_synovium.csv.gz` (1178 genes × 18) and `GSE200283_cartilage.csv.gz` (1606 genes × 14). Both are non-integer values with a minimum of about 1. GEO `data_processing` says "FPKM values".
- Prep scripts (they do not change any values):
  - `prep/rename_control.py` renames the matrix prefix `cont_` to `Control_`.
  - `prep/split_metadata.py` writes the metadata separately for each tissue.
- `case_spec.json` has two cases, `GSE200283_synovium` and `GSE200283_cartilage`. For each, the gates `paper_reconstruction`, `ownership`, `alignment` and `matrix` are recorded, and the case stops at `matrix` with `decision_status: refused`.
- Alignment matched 18/18 synovium samples and 14/14 cartilage samples exactly on a key built from the title (normalized) — not by position. Groups:
  - synovium: CON, D3, D7, D14, R1, R2, with n=3 each
  - cartilage: the same groups plus D28, with n=2 each
- The contract validator checked 8 records and found 0 errors.

## Why refused
1. **The deposited features were selected on the outcome.** S4.8.p2 says the synovium matrix holds the genes with FPKM>1 and fold change MMS D14/control <0.67 or >1.5, which gives exactly 1,178 genes. The cartilage matrix uses MMS D28/control the same way and gives exactly 1,606 genes. Both row counts match the files.
   - Any DE test on these subsets is circular.
   - The BH/FDR correction is applied over a gene set that was itself selected, so it is invalid.
   - FPKM cannot be used in the count model the paper's PoissonDis test needs.
   - No genome-wide matrix is deposited. The only way to get one would be to re-process the SRA reads, which this run does not do.
2. **There is no exercise arm.** This is a disuse model (knee immobilization plus tail-suspension unloading). The closest to "exercise" are the remobilization arm R1 and the remobilization plus reloading arm R2. The paper reports no DE result for R1 or R2, only heatmaps and modules.

## DEG counts vs paper
- Paper threshold (S4.7.p1): fold change ≥ 2.0 and FDR ≤ 0.001, from the PoissonDis test run by BGI. Inclusive, this is |log2FC| ≥ 1 and FDR ≤ 0.001.
- **The paper reports no DEG counts.** Its results are module heatmaps and named genes:
  - Synovium, up: Spp1, Col1a1, Postn, Mmp9, Mmp13, Il1b, Osm and others.
  - Cartilage, down: Col2a1, Acan, Sox9, Prg4 and others.
- We produced no DEGs (0 contrasts run), so there is nothing to compare.

## Deviations
- None in the analysis, since nothing was executed.
- The data were split into one case per tissue because GEO holds the two tissues in separate matrices.

## Tool problems
- `tools/case_runner.py:577`: the `normalize_keys` collision check runs on the **whole** metadata before `exclude_samples` is applied (line 588). If the derived keys repeat across strata (here, tissues), the run fails with "keys collide", so the metadata had to be pre-split with a prep script. It would be better to apply `exclude_samples` (or a subset) before the collision check.
- `summary.csv` / finish record: when the case stops at `matrix`, the `matrix_type` field stays empty even though the matrix gate recorded `FPKM (feature-selected subset)`.
- Inspect flagged Excel-date gene IDs (`7-Mar` and `1-Mar`). They are left as they are, since nothing was executed.
