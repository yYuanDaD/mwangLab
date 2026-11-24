# HANDBACK — PMID41229364 (PMC12612635)

Paper: *Fast Myosin Binding Protein-C Is a Vital Regulator in Young and Aged Fast Skeletal Muscle Homeostasis* (J Cachexia Sarcopenia Muscle 2025).

## Outcome: refused (all 3 cases), at the `design` gate

The request asked for the effect of exercise on gene expression. All three RNA-seq series in this paper compare Mybpc2-knockout (C2-/-) mice with wild-type (WT) mice. None of the series has a training, running or acute-exercise arm (S2.11.p1, S3.5.p1, S3.7.p1). The only contraction intervention in the paper, eccentric-contraction injury (S2.3.p1), was measured by Western blot and ELISA in C57BL/6 mice and was never sequenced. So none of the data can answer an exercise question. I did not run the knockout comparison in its place, and I ran no DE model.

## What ran

- `python -m tools.case_runner inspect` for each series (`inspect_<GSE>.json`).
- `python -m tools.case_runner execute case_spec.json` recorded the gates paper_reconstruction → ownership → alignment → matrix → design (refused). The validator passed: 15 records, 0 errors.

| Case | Samples / alignment | Matrix decision | Paper's contrast (not run) |
|---|---|---|---|
| GSE285405 (aged TA, 22 mo) | 8/8 exact on `Library name` key (WT 4, KO 4) | `read_count_*` columns = estimated counts (94% integer, fractional values present) | C2-/-Old vs WT-Old: 310 DEGs (226 up / 84 down) |
| GSE302562 (young TA, 5–6 mo) | 7/7 exact (WT 4, KO 3) | `log2_TMM.csv.gz` = log2 TMM-CPM → limma | C2-/-Young vs WT-Young: only the overlap with aged is reported (45 up / 14 down shared) |
| GSE160827 (young single EDL fibres) | 47/47 exact on GSM (WT 27, C2KO 20) | Merged featureCounts counts from the tar = raw counts | C2-/- vs WT: 956 DEGs (621 up / 335 down), n=10/group |

The paper's threshold (S2.11.p1) is |fold change| > 1.5 (|log2FC| > 0.5849625) with adjusted p < 0.05, using limma/voom after edgeR TMM normalisation. The FIG8 legend instead says "log-transformed fold change cut off of 0.5". I applied no threshold because nothing was executed.

## DEG counts vs paper

None of ours to compare: 0 contrasts ran. The paper's knockout DEG counts are listed above for reference only.

## Deviations and discrepancies (recorded in the spec)

- GSE285405: GEO data_processing says Bowtie2 + DESeq2, and the table carries BGI DESeq2 columns. The paper says featureCounts + limma/voom. The growth protocol says "grown upto 2 months", but the age field says 22 months.
- GSE160827: GEO has 27 WT and 20 KO fibres, but the paper analysed n=10 per group and does not say which fibres it used. The fibres come from 3 WT and 2 KO mice, so any future genotype analysis would have to block by donor mouse.

## Tool problems

No blocking problems. Minor issues:
- `inspect` gave GSE285405's mixed BGI core table (fpkm_/tpm_/read_count_/diffexp_ columns in one file) no type candidates (`candidates: []`) and found no `alignment_keys`. The library names sit inside the prefixed column names, so I had to write `matrix_column_pattern` and `key_patterns` by hand. This is the known mixed-FPKM+diffexp classification gap; see `_contained_keys` in `tools/case_runner.py:332`, which only matches bare column names.
- `GSE302562_log2_TMM.csv.gz` is tab-separated despite its `.csv` name. The runner's sniffer handled it, but plain `pd.read_csv` reads it as one column.
- The suitability report says `analyzable` for the genotype comparison. That is correct for genotype, but the report cannot flag a missing exercise factor, so the refusal is a manual decision only.
