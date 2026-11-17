# HANDBACK: PMID 39747575 / GSE269053

**Status: refused at the `design` gate.** No exercise contrast exists in the sequenced samples.

## What ran
- `python -m tools.case_runner inspect GSE269053`: downloaded the series into `E:/agent/mwangLab_pdf/data/GSE269053`. It holds an FPKM `data_matrix.tsv.gz`, a `_RAW.tar` with 21 per-sample Salmon count files, and metadata for 21 samples.
- I read the paper (`PMC11696687.paper.md`). The RNA-seq (S2.4.p1, FIG4, S4.9.p1) covers left-ventricle samples from four groups: chow null (4), chow AAV8-Renin (6), HFD null (6) and HFD Renin (5). Exercise appears only as a phenotyping readout, a treadmill test to exhaustion (S2.2.p4, S2.2.p5, S4.5.p1, FIG2H, FIG5F). No sequenced animal was assigned an exercise or sedentary condition, and no per-sample exercise-capacity value is deposited.
- `python -m tools.case_runner execute case_spec.json` recorded these gates:
  - `paper_reconstruction`
  - `ownership`: owned. DA.p1 names the accession, and the GEO data_processing text matches S4.9.p1.
  - `alignment`: the `_RAW.tar` was merged, giving GSM columns. Exact index match, 21/21.
  - `matrix`: Salmon estimated counts.
  - `design`: refused. The suitability report itself was "analyzable" for the diet × renin comparisons. That only shows those comparisons can be computed; they are not exercise comparisons.
- The validator returned 5 records with 0 errors. Executions and enrichment were deliberately left out.

## DEG counts vs paper
Nothing was run, so I have no counts of my own. For reference, the paper's threshold is FDR < 0.05 and at least a 1.2-fold change (|log2FC| >= 0.2630344), from S4.9.p1. Results paragraph S2.4.p1 quotes adjusted p < 0.01 for the DIO count. The paper reports these DEG counts, none of which measures an exercise effect:
- HFD null vs chow null: 839 down
- chow Renin vs chow null: 927 up
- HFD Renin vs chow null: 498 up and 472 down

## Deviations
- None in execution, because nothing ran.
- Rejected design alternatives, recorded in the design `candidates`:
  - HFpEF vs control
  - HFD vs chow. The paper says diet dominates exercise capacity (S3.p3), but a diet contrast is still not an exercise effect.
  - An expression–performance association. This is impossible because no per-sample exercise data exists.

## Tool problems / observations
1. `tools/native.py:539` `merge_raw_tar`: the per-sample `*_raw_counts.tsv.gz` files are Salmon **transcript-level** counts (ENSMUST IDs, 119,215 rows). The merge writes them under a `gene_id` header with no transcript-to-gene summarization. The paper summarized to gene level before DESeq2 (S4.9.p1), so a run on this matrix would test transcripts, not genes, and no gate flags it. This did not affect the result here.
2. `inspect` on `GSE269053_data_matrix.tsv.gz` returned empty type `candidates`. The file mixes FPKM sample columns, negative values (min −21.2) and non-sample analysis columns (`outlier`, `HFD+virus log2FoldChange`, `HFD+virus padj`), which are counted in `n_samples` = 24, while the metadata has 21. Its 23 real sample columns use group/animal codes (`cn_A147`, …) that match the animal IDs in the tar member names, not anything in the metadata, so `alignment_keys` is empty. There is no file:line for this.
3. `merge_raw_tar` writes `GSE269053_merged_from_tar.csv` into the shared data cache (`data/GSE269053/`) as well as the run directory. This is a side effect outside the run directory.
