# HANDBACK: PMID39056292 / GSE246428

**Status: refused at `design`.** The data cannot answer the exercise question.

## What ran
- `python -m tools.case_runner inspect GSE246428`: downloaded the series into `data/GSE246428` (it was not cached). Found two files: `GSE246428_Spag7_raw_counts.txt.gz` (9 samples, all integers) and `GSE246428_Spag7_norm_counts_and_DE_results.txt.gz` (DESeq2-normalized counts plus the authors' DE columns).
- `python -m tools.case_runner execute case_spec.json`: recorded the gates `paper_reconstruction`, `ownership`, `alignment` (exact match on `description`, 9 of 9 samples), `matrix` (Salmon/tximport estimated counts, rounded) and `design` (refused). The contract validator found 0 errors, and no external LLM call was attempted. The suitability report rated the only comparison, genotype KO vs WT, as analyzable. We did not run it, because it is not the estimand that was requested.

## Why it was refused
- The paper sequenced gastrocnemius muscle from sedentary female WT and germline SPAG7 KO mice (S4.17.p1, S2.3.p2, Fig 3K).
- GEO has one grouping column, genotype: WT 5, Spag7 KO 4.
- The paper's only exercise content is a treadmill endurance test, used as a phenotype readout (S2.3.p1, S4.12.p1, Fig 3A–B). No exercised animals were sequenced.
- So the data contain no exercise contrast. Presenting KO vs WT as an exercise effect would change the estimand.

## DEG counts compared with the paper
- **Ours:** none. No contrast was run.
- **Paper:** KO vs WT had 1,848 genes up and 2,291 down, 4,139 in total (S2.3.p2). This is a genotype contrast, not an exercise one. The most downregulated gene was Hsd17b10, and the downregulated GO terms were mitochondrial.
- **Paper's threshold:** not stated. The text only says "significantly", and the methods give no cutoff. It is recorded as `not_reported`.

## Deviations and discrepancies
- **Sample count:** the paper gives n=7 and says two samples were removed (one for a batch effect, one for a label mismatch, S4.19.p1). GEO deposits 9 samples and does not say which ones were removed. This did not matter here because the case was refused.

## Tool problems
- **Garbled text in the metadata:** the metadata CSV written at download shows mojibake in `extract_protocol_ch1` (`manufacturer鈥檚`, which should be "manufacturer's"). A UTF-8 curly apostrophe appears to have been decoded as GBK somewhere in the GEO download and metadata write path. I did not locate the line. It is cosmetic and did not affect this case.
- **Inflated sample count in inspect:** inspect profiled the norm-counts/DE-results file as a candidate matrix with `n_samples: 19`, although the series has only 9 samples. Non-sample columns are being counted as samples. It is harmless here, since that file was rejected as an input matrix.
- No other problems.
