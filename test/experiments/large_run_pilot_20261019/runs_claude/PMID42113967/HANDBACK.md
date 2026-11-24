# HANDBACK — PMID 42113967 / GSE310858

**Paper:** Orlova et al., *J Physiol* 2026, "Different effects of 3-week disuse on phenotype and gene expression in calf and thigh muscles".

**The comparison with the paper rests on the abstract only.** No full text was available. The study map comes from the PubMed abstract (fetched with E-utilities efetch, saved in `paper/PMID42113967_abstract.txt`) and the GEO series description (`paper/GSE310858_series.txt`). The abstract gives no DE method, no threshold, no DEG counts and no gene lists.

## What ran
- **Design:** 12 healthy men. Biopsies of the soleus (calf) and vastus lateralis (thigh) were taken before and on day 20 of a 21-day head-down bed rest. That gives 48 RNA-seq libraries.
- **Matrix:** `GSE310858_Read_counts.txt.gz`, raw Rsubread counts (all integers).
  - The deposited column names (`<subject>-<time>-<tissue>_S<n>.sorted.bam`) do not appear anywhere in the GEO metadata.
  - `prep/rename_columns.py` renames each column to its GSM id by matching subject, time point and tissue. It matches by name, never by position, and fails if any mapping is not one-to-one.
  - After renaming, all 48 of 48 samples aligned exactly.
- **Gates:** every gate is recorded in `case_spec.json`. The decision contract validator reported 0 errors.
  - Run separately per muscle (`strata: tissue`).
  - Paired by subject: DESeq2 (pydeseq2 Wald) with `~ subject + time`, comparing after vs before.
  - Suitability verdict: analyzable, with 2 of 2 comparisons analyzable.
- **Enrichment:** GSEA against the MSigDB Hallmark sets (human), ranked by the Wald statistic, for both muscles.

## DEG counts vs the paper
The threshold is the workflow default, **BH padj < 0.05 with no fold-change cutoff**, because the abstract states no threshold.

| Contrast | n DEG (up / down) | Audit rule: padj<0.05 & \|FC\|>1.25 | Paper |
|---|---|---|---|
| Soleus after vs before | 6868 (3398 / 3470) | 3856 | no count in abstract |
| Vastus lateralis after vs before | 2819 (1427 / 1392) | 1171 | no count in abstract |

- **Qualitative agreement:** the abstract says the transcriptome of the calf (soleus) changes more than that of the thigh. Soleus has about 2.4× as many DEGs, which matches.
- **GSEA:**
  - Oxidative phosphorylation is the most suppressed Hallmark set in both muscles (NES −2.76 soleus, −2.75 vastus). Fatty-acid metabolism is also down in both.
  - Inflammatory and interferon sets go up in the soleus.
  - In the vastus, G2M and E2F sets go up.
  - PPARGC1A (a mitochondrial biogenesis regulator) falls in both muscles, by log2FC −1.02 in the soleus and −0.58 in the vastus. This fits the abstract's statement that mitochondrial biogenesis is dysregulated, and more strongly in the calf.
  - These pathway results are separate from the DE counts.

## Deviations and caveats
- **No paper method or threshold to reproduce** (abstract only). I chose DESeq2 paired by subject and the workflow-default threshold myself. The audit rule (|FC| > 1.25) is labelled as audit only.
- **The estimand is disuse (bed rest), not exercise.** I treated it as the inverse of the physical-activity axis and ran it as the paper intends. Anyone who wants strictly exercise-intervention contrasts should exclude this case.
- **Pre-post design with no control group**, so time effects cannot be separated from the effect of disuse.
- **Not run:** a time × tissue interaction test. The abstract compares the size of the two responses, not a formal interaction.
- **Not in GEO:** the proteomics data that the paper also analyses.

## Tool problems
1. **`case_runner inspect` could not download the series.**
   - `tools/geo_tools.py:30`: `GEOparse.get_GEO` failed with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. It still failed when TMP pointed to a writable scratch dir.
   - `tools/geo_tools.py:58`: `https://ftp.ncbi.nlm.nih.gov/...` returned HTTP 403 for every path, including when run outside the sandbox. The 403 is on the NCBI side.
   - Workaround: the alias host `https://ftp.ncbi.nih.gov/geo/...` served both the counts file and the family SOFT file. I parsed the SOFT locally (`GEOparse.get_GEO(filepath=...)`) and wrote `data/GSE310858/GSE310858_metadata.csv` in the same `phenotype_data` format.
   - Suggestion: have `geo_tools` fall back to `ftp.ncbi.nih.gov` when `ftp.ncbi.nlm.nih.gov` returns 403.
2. **The matrix column names could not be aligned with the runner's options.**
   - The key is spread over three parts (subject, time, tissue), the `_S<n>` lane numbers repeat, and `key_patterns` joins groups only in title order (`Sol_before_1`). That order cannot be matched to `1-0-s`.
   - Workaround: a prep script (`prep/rename_columns.py`). A reorder or format option in `key_patterns`/`matrix_column_pattern` would remove the need for it.
