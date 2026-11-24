# Review packet B (the analysis' decisions): GSE128651

## Mechanical flags

- none

## Stop reasons

- ownership (manual_review; claim type: other): matrix file GSE128651_gene_fpkm.txt.gz unavailable: NCBI GEO FTP returns HTTP 403 from this host; rerun when the file is placed in data/GSE128651/
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE128651"], "assay": "bulk RNA-seq (QIAseq FX Single Cell RNA Library Kit, ~800 FACS-sorted SCs/sample), Illumina HiSeq 2000 (S4.p10)", "sample_inclusion": "FACS-sorted Lin- CD34+ a7-integrin+ muscle satellite cells, n=4 mice per arm (FIG3 legend B)", "factors": {"grp": ["Con (sedentary/untrained)", "Exe (4-week treadmill training)"]}, "primary_estimand": "effect of 4-week treadmill training on the SC transcriptome: Exe vs Con (S2.3.p1, FIG3)", "planned_contrasts": ["grp_Exe_vs_Con (S2.3.p1; paper: 573 up + 1,326 down = 1,899 DEGs, >2-fold, p<0.01)"], "repeated_measure_unit": null, "paper_method": "bowtie -> HTSeq counts -> DESeq2; Cufflinks FPKM for display (S4.p10)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S2.3.p1; FIG3 legend B"}, "paper_threshold_alternative": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null, "source_locator": "S4.p10"}, "paper_results": {"up": 573, "down": 1326, "total": 1899, "named_genes": {"down": ["Igfbp4", "Igfbp5", "Igfbp6"], "up": ["Igfbp7"]}, "gsea": "up: ECM receptor interaction, cardiac muscle contraction, S phase; down: OXPHOS, ATP synthesis, PI3K-Akt, mTOR, TCA cycle (FIG3 C-K)"}}

reasoning: Paper names GSE128651 (S4.p22) as the SC RNA-seq of control vs exercise mice (S2.3.p1, FIG3A). Two arms, 4 mice each; GEO record confirms Con1-4 / Exe1-4. The DEG rule that yields the reported 573/1,326 is 'over 2-fold change, p<0.01' (S2.3.p1, FIG3B); methods state FDR<0.05 (S4.p10). Whether 'p' is raw or adjusted is not stated; taken as raw p as written.

### ownership (manual_review, not_started)

final: {"owned": null, "accession": "GSE128651", "expected_matrix_file": "GSE128651_gene_fpkm.txt.gz (GEO Series_supplementary_file; RPKM/FPKM per data_processing)", "matrix_file": null, "metadata_file": "evidence_geo/GSE128651_samples.soft.txt", "checks": {"pubmed_id_on_series": "32483463 (matches)", "samples": "8 GSM (GSM3681653-60): Con1-4 untrained, Exe1-4 trained", "matrix_retrieved": false, "download_status": "HTTP 403 Forbidden from ftp.ncbi.nlm.nih.gov (https and GEOparse), FTP 550; geo/download redirects to the same FTP host"}}

reasoning: GEO series GSE128651 carries PubMed 32483463 and 8 samples matching the paper's n=4 vs n=4 design, so the series belongs to the paper. But the only expression file (GSE128651_gene_fpkm.txt.gz) could not be retrieved: every ftp.ncbi.nlm.nih.gov request from this host returns 403 (also for unrelated series), and the metadata SOFT download via GEOparse fails the same way. Without the matrix, ownership of the file (its columns vs the 8 GSMs) and every later gate cannot be checked. A specific fact unblocks it: the deposited FPKM file. Note for resumption: the deposit is FPKM only, so the paper's DESeq2-on-counts route is blocked; the expected route is log2(FPKM+1) + limma (declared deviation) or  ... [32 more characters]


## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "S2.3.p1/FIG3B: >2-fold and p<0.01 (1,899 DEGs)",
    "data": "S4.p10 methods: P<0.05 FDR-adjusted",
    "disposition": "results rule taken as paper_threshold (it produced the reported counts); FDR rule kept as audit"
  },
  {
    "item": "deposited matrix",
    "paper": "DESeq2 on HTSeq read counts (S4.p10)",
    "data": "GEO deposits only GSE128651_gene_fpkm.txt.gz (Series_supplementary_file); data_processing says RPKM via Cufflinks",
    "disposition": "paper DESeq2 route would be blocked even with the file (no counts); FPKM->log2->limma would be a declared deviation"
  },
  {
    "item": "matrix availability",
    "paper": "-",
    "data": "NCBI GEO FTP/HTTPS returns 403 for every ftp.ncbi.nlm.nih.gov path from this host",
    "disposition": "case stopped: manual_review at ownership"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 32483463 / GSE128651

**Status: stopped. `manual_review` at the `ownership` gate.** No differential expression ran.

## What ran
- `python -m tools.case_runner inspect GSE128651 --data-root E:/agent/mwangLab_pdf/data` ran twice and failed both times. The second run had TMP/TEMP pointed at the scratchpad. The error was `no metadata ... GSE128651_metadata.csv`: the GEOparse SOFT download failed and the supplementary download got HTTP 403.
- Probes by hand (`evidence_geo/download_attempts.txt`):
  - every `https://ftp.ncbi.nlm.nih.gov/geo/...` path returns **403 Forbidden**, including unrelated series (GSE266241, GSE37525);
  - `ftp://` returns 550;
  - `geo/download/?acc=...` redirects (301) to the same FTP host.
  - `www.ncbi.nlm.nih.gov/geo/query/acc.cgi` does work. The series and sample text records are saved in `evidence_geo/`.
- The gates were recorded with the native recorder (`scripts/record_stop.py`), because the case-spec runner can't record this stop (see Tool problems).
  - `paper_reconstruction` is valid.
  - `ownership` is manual_review.
  - The decision contract validates (2 records). External-LLM attempts: 0.
- I removed the empty `data/GSE128651/` folder that the failed download created.

## Paper reconstruction (for resumption)
- **Design:** FACS-sorted muscle satellite cells (Lin⁻CD34⁺α7-integrin⁺). Con (untrained) n=4 vs Exe (4-week treadmill) n=4. GEO samples GSM3681653–60 are Con1–4 and Exe1–4. Two independent groups, no blocking.
- **Paper result** (S2.3.p1, FIG3B): 573 up and 1,326 down, 1,899 DEGs in total, at ">2-fold change, p<0.01".
  - Methods (S4.p10) instead say FDR < 0.05.
  - I took the Results rule as `paper_threshold`: pvalue < 0.01 and |log2FC| > 1. The FDR rule is recorded as the alternative.
  - Named genes: Igfbp7 up; Igfbp4, Igfbp5 and Igfbp6 down.
  - GSEA: OXPHOS, TCA, PI3K-Akt and mTOR down; ECM-receptor and S phase up.

## DEG counts vs paper
- Not computed: 0 of 1 contrasts ran. Paper: 573 up / 1,326 down (>2-fold, p<0.01).

## Deviations to expect once the file is available
- GEO deposits **only FPKM/RPKM** (`GSE128651_gene_fpkm.txt.gz`, made with Cufflinks per data_processing). The paper ran DESeq2 on HTSeq counts, so the paper's route is blocked.
- The runnable route would be log2(FPKM+1) + limma, as a declared deviation. The alternative is re-quantifying counts from SRA SRP189039.

## Tool problems
1. **Network:** NCBI GEO FTP (ftp.ncbi.nlm.nih.gov) returns HTTP 403 from this host. This blocks ... [961 more characters]
