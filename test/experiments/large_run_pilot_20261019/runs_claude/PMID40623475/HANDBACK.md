# HANDBACK: PMID40623475 / GSE302911

Status: finished (case `completed`, route `declared_deviation`; validator 15 records, 0 errors).

## What ran
- `inspect` on GSE302911. One supplementary matrix exists: `GSE302911_RNA-seq_Count_Matrix_TPM_allconditions.tsv.gz` (salmon TPM, 53,738 genes x 21 samples). No raw or estimated counts are deposited.
- Prep script `prep/prep_matrix.py`: reads the whitespace-separated file, renames the columns by a name rule (`Untrained_0h1` -> `Untrained_0h_1`, checked against the GEO "Library name" values) and writes `prep/GSE302911_TPM_renamed.csv`. The values are unchanged.
- Alignment: exact match on `libkey`, extracted from GEO `description` ("Library name: X,RNASeq"), 21/21. Groups come from `characteristics_ch1.3.treatment`, recoded to SED, U0, U6, U72, T0, T6, T72.
- **Excluded GSM9113520 (Untrained_0h_1) and GSM9113529 (Trained_0h_1).** The two deposited columns are byte-identical across all 53,738 genes (library sum 997,304 in both), so one library was deposited twice and its true group cannot be known. After the exclusion U0 and T0 have n=2.
- Matrix: TPM. The method is limma on log2(TPM+1) with the cell-means model `~ grp` on 19 samples (36,627 genes with nonzero values; no extra low-expression filter).
  - `joint` (tools.joint_contrasts:run_joint_limma): the paper's six contrasts, each exercised condition vs sedentary. U0 and T0 were added via `include` and labelled exploratory because n=2.
  - `training_state` (tools.multigroup_tools:run_multigroup_analysis, exploratory): trained vs untrained at 0h, 6h and 72h.
- GSEA (MSigDB Hallmark, preranked on limma t) for U0, U6, T0 and T6 vs SED: all completed.

## DEG counts (applied rule = paper FIG4: BH FDR < 0.05 and |log2FC| > 0.585)
| Contrast | DEGs (up/down) | Audit FDR<0.05 only |
|---|---|---|
| U0 vs SED (n=2 vs 3, exploratory) | 351 (314/37) | 858 |
| U6 vs SED | 386 (336/50) | 1072 |
| U72 vs SED | 0 | 4 |
| T0 vs SED (n=2 vs 3, exploratory) | 372 (358/14) | 960 |
| T6 vs SED | 303 (214/89) | 1179 |
| T72 vs SED | 9 (5/4) | 39 |
| T0 vs U0 (exploratory) | 6 (2/4) | 22 |
| T6 vs U6 (exploratory) | 161 (42/119) | 517 |
| T72 vs U72 (exploratory) | 18 (6/12) | 66 |

The paper gives no numeric per-contrast DEG counts. Figure 4A shows bars only, and only for the ATAC-derived myonuclear gene subset (23% of genes, which needs the GSE302910 peaks). The text gives only a union of 1,848 subset genes across all conditions. **No numeric count comparison is therefore possible.**

The qualitative claims in S3.4.p1 do match:
- There are more DEGs at 0h in trained than in untrained muscle (372 vs 351).
- Upregulated counts at 6h are of similar size (214 vs 336). Trained muscle has more downregulated genes at 6h (89 vs 50).
- There are very few changes at 72h (0 and 9).

Named genes:
- Klf5 is up in U6 (log2FC 1.28, padj 8e-4) and flat in T6.
- Esrrg is up in T6 (log2FC 1.31, padj 1e-4) and flat in U6. Both match the training-state dependency in FIG4 C.
- The immediate early genes Fos, Jun, Egr1, Atf3 and Nr4a1 are strongly up at 0h in both training states.

## Deviations
1. The paper's method is DESeq2 (GEO data_processing). That route is blocked because only TPM was deposited. I ran limma on log2(TPM+1) instead, with the paper's threshold applied (`paper_on_deviation_route`).
2. The two duplicated 0h libraries were excluded, so the 0h contrasts are 2 vs 3 and exploratory. The paper presumably used all 21 columns.
3. The effect cutoff is the paper's stated 0.585, not log2(1.5)=0.5849625. The paper writes the log2 value directly.
4. The genome-wide DEG universe is not the paper's myonuclear-subset universe.
5. The training-state contrasts (T vs U per time point) are additions and exploratory.

## Tool problems
- There is no duplicate-sample-column check. `inspect`/`profile_matrix` report `duplicated_feature_ids` (tools/native.py:246; tools/case_runner.py:346) but never compare columns. The identical Untrained_0h1/Trained_0h1 pair went unflagged by every tool, including suitability; I found it by hand.
- `inspect` returned `alignment_keys: []` (tools/case_runner.py:351). The matrix names differ from the GEO library names only by an underscore. `key_patterns` accepts only one regex capture group (tools/native.py:345-351, `str.extract(..., expand=False)`), so it cannot drop a character. I had to write a prep script to rename the columns.
- `comparisons: "all"` for a single 7-level factor lists only the comparisons against the reference (tools/case_runner.py:671 / suitability). Trained-vs-untrained per time point needed a separate multigroup plan execution.
- The case `finish` summary reports `n_deg=351` and `deg_sanity=tiny_n_per_group=2` from the first table only. That summary does not represent a multi-contrast case.
