# HANDBACK — GSE120862 / PMID 30779632

Popov et al., *Am J Physiol Endocrinol Metab* 2019, "Contractile activity-specific transcriptome response to acute endurance exercise and training in human skeletal muscle".

**Status: finished** (`run_status.json`: completed; decision-contract validator: 14 records, 0 errors).

**The comparison with the paper rests on the abstract only.** No full text was available. I used the PubMed abstract (efetch, saved as `PMID30779632_abstract.txt`) and the GEO series description (`GSE120862_series_soft.txt`). Neither gives DEG counts, a DE threshold, the DE model or the pairing, so no count-for-count comparison was possible.

## What ran
- **Design.** 7 men × {untrained, trained after 2 months of aerobic training} × {baseline, +1 h, +4 h} × {exercised leg (Ex), non-exercised leg (NE)} = 84 samples. Every subject has every cell.
- **Data source (deviation).** GEO FTP and the GEO download endpoint returned HTTP 403 for every series file from this machine on 2026-11-24. That included SOFT and the supplementary files (DESeq-normalized counts, FPKM).
  - **Metadata:** parsed from the GEO acc.cgi full sample SOFT text (`prep_GSE120862.py`).
  - **Matrix:** recount3 gene_sums for SRA project SRP163524, which GEO links from this series. The coverage sums were divided by the single-end read length and rounded to give estimated counts (recount3 `compute_read_counts` logic). SRR ids were mapped to GSM ids one-to-one. The result has 63,811 genes (GENCODE v26).
- **Alignment:** exact match on the GSM index, 84/84. Factors: `tr` (U/T), `time` (b/h1/h4), `leg` (NE/Ex), plus `subject`.
- **Model:** one joint DESeq2 (pydeseq2) model on all 84 samples, `~ subject + tr*time*leg`, with subject as a blocking term. Sequencing platform is nested in subject (S1–S4 on HiSeq 2500, S5–S7 on NextSeq 500), so the subject block absorbs it. Suitability verdict: analyzable.
- **Threshold:** `workflow_default`, BH padj < 0.05 with no fold-change rule, because the paper's threshold is unknown. Audit rule: padj < 0.05 and |FC| > 1.2.
- **Enrichment:** ORA and Hallmark GSEA for untrained +4 h Ex vs NE, and for trained vs untrained baseline (NE leg).

## DEG counts (padj < 0.05) vs paper

The paper's counts and threshold are not stated in the abstract.

| Contrast | role | n | up | down | paper |
|---|---|---|---|---|---|
| Ex vs NE, untrained +1 h | planned | 1015 | 764 | 251 | not in abstract |
| Ex vs NE, untrained +4 h | planned | 2058 | 1481 | 577 | not in abstract |
| Ex vs NE, trained +1 h | planned | 6386 | 2977 | 3409 | not in abstract |
| Ex vs NE, trained +4 h | planned | 317 | 198 | 119 | not in abstract |
| Trained vs untrained, baseline NE | planned | 8099 | 4083 | 4016 | not in abstract |
| Trained vs untrained, baseline Ex | planned | 6003 | 3038 | 2965 | not in abstract |
| Ex vs NE at baseline (U / T) | exploratory | 0 / 0 | | | |
| Time vs baseline within leg (8 tables) | exploratory | 215–3036 | | | |

### Agreement with the abstract
- **Agrees:**
  - The two legs do not differ at baseline (0 DEGs in either training state).
  - Classic contractile genes rise in the exercised leg of untrained men: NR4A3 log2FC 5.1 at +1 h and 5.8 at +4 h; PPARGC1A 2.9 at +4 h; MYC 1.8 at +1 h and 2.5 at +4 h; ATF3 up. This fits the abstract's CREB/ATF/AP1 and MYC/MAX regulation.
  - The training effect at baseline is larger than the acute untrained Ex vs NE response, as the abstract says.
  - Interferon α/γ Hallmark sets go up with training (NES about 2.46), which fits the abstract's IRF/STAT regulation.
- **Disagrees** (recorded in the study caveats):
  - Ex vs NE has many down-regulated genes, while the abstract says the response was increases only. The missing paper fold-change and threshold rules may explain part of this.
  - Trained +1 h Ex vs NE gives 6,386 DEGs, against the GEO summary's statement that trained responses "substantially decreased". The trained +1 h NE vs baseline contrast also gives 2,682 DEGs. Sample QC shows outliers in trained cells: S6 trained +1 h Ex has r = 0.91 to that subject's median, and S7 and S4 have trained cells at r = 0.95–0.96. This result is likely driven by sample quality. I excluded no samples, because I had no paper basis to do so.
  - Oxidative phosphorylation goes down with training at baseline (NES −1.83). The GEO summary reports an increase in OXPHOS proteins.

## Deviations
1. **Matrix:** recount3 (STAR, GENCODE v26) estimated counts instead of the authors' HISAT2/HTSeq counts, because the GEO files were unreachable. Counts are rounded, and the rounding is documented.
2. **Model:** subject-blocked DESeq2. The paper's exact model and pairing are unknown.
3. **Threshold:** workflow default instead of the paper's rule, which is unknown.
4. **Training at baseline:** run per leg, because the abstract does not say whether the legs were pooled.

## Tool problems
- **GEO download failure with a misleading error.**
  - `tools/geo_tools.py:42`: `download_geo_data` reported a GEOparse temp-file `[Errno 2] No such file`. The real cause was GEO FTP answering HTTP 403.
  - `tools/geo_tools.py:132`: the supplementary download also got 403. Neither call has a fallback to another endpoint.
- **Non-matrix file profiled as a matrix:** `case_runner inspect` read the SOFT text dump `_soft_full.txt` as a candidate matrix and logged a ParserError. This is harmless.
- **Comparison names silently restricted:**
  - `tools/suitability.py:200-207`: a single factor with more than 6 levels (`max_pairwise_levels=6`) is only enumerated against the reference.
  - `tools/case_runner.py:859`: this then rejected the within-cell planned names without saying why.
  - Workaround: separate `tr`/`time`/`leg` factors.
