# HANDBACK: PMID28273480 / GSE97084

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Status: completed, validator 21 records, 0 errors.
- Prep: `prep_merge_counts.py` merged the two deposited count files (`GSE97084_GeneCount_raw.tsv.gz`, 63 samples; `_raw_2.tsv.gz`, 40 samples) on Ensembl GeneID, giving 57,773 x 103 (`GSE97084_merged_counts.csv`). Columns were renamed to the sample code at the start of each GEO title (`s_18a-180_GeneCount` -> `18A`).
- Alignment: exact match on the key from the title, 103/103. Derived `subject` (the participant number), `time` (Pre/Post), `age`, `mode` (HIIT/RT/CT), `batch` (count file B1/B2) and `cohort` (age_mode).
- Matrix: raw integer counts (MapRSeq "raw reads per gene"), analysed with DESeq2.
- Design: paired post vs pre within each age x mode stratum, `~ subject + time` (pydeseq2 Wald), one fit per stratum. All subjects are complete pairs except Young CT subject 27 (pre only), which was dropped through a subject subset.
- Secondary: baseline Old vs Young on the 52 pre-training biopsies, labelled associational. A sensitivity fit adds `batch`.
- Enrichment: ORA (Enrichr GO/KEGG) and GSEA (Hallmark) on Old HIIT and Young HIIT. Both completed.

## Threshold
The paper's rule (S4.4.1.p1, FIG4) is FDR <= 0.05 and |log2FC| >= 0.5, inclusive. It is applied here as written. The audit rule is padj < 0.05 only.

## DEG counts vs paper (paper rule; up / down / total)
| contrast | ours up | ours down | ours total | paper |
|---|---|---|---|---|
| Young HIIT | 1020 | 243 | 1263 | up not stated in the text (FIG4A) |
| Old HIIT | 983 | 142 | 1125 | **553 up** (S2.4.p2, S2.6.p5) |
| Young RT | 554 | 97 | 651 | up 35% below young HIIT |
| Old RT | 239 | 77 | 316 | up 70% below old HIIT (~166) |
| Young CT | 380 | 47 | 427 | up 28% below young HIIT |
| Old CT | 149 | 142 | 291 | up 84% below old HIIT (~88) |
| Baseline Old vs Young | 1704 | 359 | 2063 | 166 higher / 267 lower in old = 433 |
| same, with batch covariate | 1713 | 354 | 2067 | |

- Our up counts are about 1.8x the paper's for Old HIIT. The relative pattern across modes in the old group matches the paper: RT is 24% and CT 15% of HIIT, against 30% and 16% in the paper. In the young group the pattern is weaker (RT 54% and CT 37% of HIIT, against 65% and 72% in the paper).
- In Old HIIT, all six mitochondrial genes the paper names (MT-RNR1, MT-RNR2, MT-TL1, MT-TV, MT-TR, MT-TG) are up with padj < 0.05 and log2FC 0.54-0.80. They pass the paper's rule.
- Baseline age DEGs are about 5x the paper's 433, and the direction is reversed: ours are mostly higher in old, while the paper has more lower in old. The batch covariate does not change this. The paper's baseline sample set and method are not stated; for example, CT participants may have used the pre-SED biopsy, which is not deposited. This comparison is not reproduced.

## Deviations
- The paper does not name its DE software ("as previously described", Lanza 2012, MapRSeq). DESeq2 with subject blocking was used, so the route is `declared_deviation`.
- Only complete pairs were used (Young CT subject 27 dropped). The paper may have used a different sample handling.
- CT pre-training = the post-SED biopsy (B). The pre-SED biopsy and the SED-period comparison are not deposited.
- `deseq2_tools` runs lfc_shrink (tools/deseq2_tools.py:175-180). The |log2FC| cutoff may therefore apply to shrunk LFCs, while the paper's are presumably unshrunk.

## Tool problems
- tools/case_runner.py:634 passes subject, condition and levels positionally to `native.complete_pairs_subset` (tools/native.py:688). That function takes them keyword-only, so any execution with `complete_pairs` crashes (TypeError). Workaround here: an explicit `subset` on subject.
- `covariate_columns` must be a comma-separated string (tools/deseq2_tools.py:28,105). A list fails with "'list' object has no attribute 'strip'". The case-spec docs show a string, but the spec schema does not reject a list.
- tools/native.py:338: SyntaxWarning, invalid escape sequence '\d' in a docstring (cosmetic).
- pydeseq2 gives overflow RuntimeWarnings in utils.py:1088 during the fits (did not stop them).
