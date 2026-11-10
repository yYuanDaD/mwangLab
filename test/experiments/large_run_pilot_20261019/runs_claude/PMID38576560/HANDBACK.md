# HANDBACK: PMID38576560 / GSE256152

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator: 18 records, 0 errors; status completed, route `paper_aligned`.
- Prep: `prep/extract_read_counts.py` keeps the 12 HTSeq `:read count` columns of `GSE256152_Gene_exp_with_symbol.txt.gz` (drops the paired `:fpkm` and annotation columns). It renames the columns by name to the GEO titles (`Tnm_swim1` -> `Tnm-swim-1`, `Tnm_union1` -> `Tnm+union-1`). It checks for integer counts, no NaN and unique IDs. Alignment is exact on `title`: 12/12.
- Design: there is one factor, `grp` (Tnm, swim, cur, union; n=3 each). Tnm is the reference. There is no blocking, because the tumours come from independent randomized mice.
- Method: pydeseq2 Wald. Each of the paper's contrasts was fit as a two-group subset, the way the paper's pairwise DESeq2 is set up. A joint `~ grp` model on all 12 samples was run as a sensitivity check.
- Threshold (paper, S2.3.p1): raw P < 0.05 and |log2FC| > 1. Audit threshold: padj < 0.05, with no fold-change rule.
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA for swim vs Tnm and for union vs Tnm.

## DEG counts vs paper (P < 0.05 & |log2FC| > 1)
| Contrast | Role | Ours (up/down) | Paper (up/down, S3.2.p3) | Audit padj<0.05 |
|---|---|---|---|---|
| swim vs Tnm (exercise) | primary | 211 (73/138) | 134 (79/55) | 47 |
| union (cur+swim) vs Tnm | secondary | 523 (286/237) | 445 (154/291) | 908 |
| cur vs Tnm (non-exercise) | secondary | 164 (110/54) | 107 (28/79) | 45 |
| union vs cur (exercise on curcumin) | exploratory | 481 (153/328) | not reported | 2156 |
| joint model swim vs Tnm | sensitivity | 312 (97/215) | | 304 |
| joint model union vs Tnm | sensitivity | 563 (292/271) | | 1629 |

Our counts are 1.2 to 1.6 times the paper's. The paper's up/down balance does not match ours in any contrast, and no single sign flip reconciles all three; this is recorded in the study caveats. The paper's genes in union vs Tnm: Wnt5a (log2FC 1.21, p≈0), Il6 (log2FC 1.29, p=0.003) and Camk1g (log2FC 1.19, p=0.031) all pass the paper rule. In the KEGG ORA for union vs Tnm, IL-17 signalling is the top term (adj p 0.031). Wnt (raw p 0.06) and calcium signalling (raw p 0.12) are not significant, whereas the paper reports them as enriched (it used GSEA for KEGG).

## Deviations
- pydeseq2 was used instead of R DESeq2. GEO data_processing names DESeq 1.30.0, while the paper says DESeq2. Either can shift raw-p DEG counts.
- The paper says groups of 6 mice and GEO says 5. Either way, 3 tumours per group were sequenced.
- KEGG enrichment was run as Enrichr ORA, not the paper's GSEA-on-KEGG. GSEA here uses Hallmark gene sets.

## Tool problems
- During the fits, pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`). The runs still completed.
- The case runner's `alignment.key_patterns` and `patterns` (`tools/native.py`, `derive_columns`) reject optional regex groups: an unmatched group becomes NaN and the row fails. Only `matrix_column_pattern` (`tools/case_runner.py:515`) skips empty groups. Titles of the form `Tnm-1` / `Tnm-swim-1` / `Tnm+union-1` could therefore not be keyed against `Tnm1` / `Tnm_swim1` without a prep script that renames the columns by name.
- `inspect` treats the combined `:read count` + `:fpkm` file as one matrix (integer fraction 0.69, type "linear_normalized or estimated_counts", no alignment keys). It does not split the paired count and FPKM columns.
