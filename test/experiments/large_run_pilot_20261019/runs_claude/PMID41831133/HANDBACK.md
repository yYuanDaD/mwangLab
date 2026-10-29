# HANDBACK: PMID41831133 / GSE309619

**Outcome:** stopped at the `matrix` gate (`manual_review`). No differential expression ran.

## What ran
- `python -m tools.case_runner inspect GSE309619`: downloaded the series. The only supplementary file is `GSE309619_AR_FPKM.xls.txt.gz`, which is 1,022 bytes. An HTTP HEAD request to the GEO FTP confirmed `Content-Length: 1022`, so the download was complete.
- Paper read in full (`PMC12989000.paper.md`). The design is single-arm and longitudinal: 5 dialysis patients (GHD28/35/42/45/58), biopsied at baseline (Visit-1) and after 12 months of resistance-based therapy (Visit-2) (S2.1.p1, S2.2.p1, FIG4 legend).
- I wrote `case_spec.json` with gates `paper_reconstruction`, `ownership`, `alignment` and `matrix` (stop), then ran `execute`. Alignment: 20/20 GSMs matched exactly on the bracketed library name in `title`. Derived `subject` has 5 levels with 4 libraries each, and `time` is pre 10 / post 10. The contract validator returned 4 records and 0 errors. Route: `stopped`.

## Why it stopped
The deposited "matrix" has only **4 genes** (ACTA1, CKM, TNNC2, MT-TN) across 21 libraries. It is an excerpt of the vendor (NovoMagic) result table, not a transcriptome. No raw counts or full FPKM table are deposited (sample `supplementary_file_1 = NONE`), and none of the paper's 20 FIG4A genes (NR4A3, PRKAG3, ACO2, MT-CO3, ...) are in the file. The design would support a paired pre/post exercise contrast, with patient as the blocking factor. The missing piece is a specific file, so the decision is `manual_review`, not `refused`. To unblock: get the full FPKM or count table from the authors, or re-quantify the SRA reads (GEO BioSample links) with an alignment pipeline. This workflow does not include such a pipeline.

## DEG counts vs paper
- Paper: no DEG count and no DEG threshold. RNA-seq was analysed on the NovoMagic vendor platform with the method unstated. The results are GO terms of upregulated genes (FIG1) and a 20-gene panel (FIG4A). The only stated statistical rule is an unpaired two-tailed Student's t-test with p < 0.05, used for IHC/IF (S2.4.p1).
- Ours: none (0/1 contrasts run).

## Deviations / discrepancies recorded
- The deposited matrix is truncated to 4 genes, which blocks execution.
- GEO has 2 libraries per patient-visit (B/C or A/C; 20 GSMs), while the paper reports n = 5. The matrix has a 21st column, `EB_35_V2B`, with no GSM record; it was left unmatched. A later run would need to decide whether these libraries are technical replicates to collapse or a second blocking level.
- The paper says "unpaired" t-test, but the biopsies are pre/post from the same patients. A full matrix would call for a paired (subject-blocked) model.

## Tool problems
1. `tools/case_runner.py:91`: `MatrixGate.recommended_method: str` is required even when the gate is blocked (`manual_review`). `null` gives a spec_error, so I had to fill in placeholder text.
2. `tools/native.py:255-261` (matrix profile used by `inspect`): numeric annotation columns (`gene_chr`, `gene_start`, `gene_end`, `gene_length`) are counted as samples. Inspect reported `n_samples: 25` instead of 21, `max: 229434098` (a genomic coordinate) and `missing_values: 1` (`gene_chr = MT`). This skews the integer_fraction and the type candidates.
3. Inspect does not flag a matrix with very few features (here 4). `n_features` is the only clue; a warning in `notes` would help.
