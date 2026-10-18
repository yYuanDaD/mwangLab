# Paper screen, 2026-10-18: rescreen, spot-check and fixes

These are the same 200 papers as `../paper_screen_20261017/` (query
`"exercise gene expression"`, up to 2026). The rescreen reused that run's HTTP cache and
the full text it had already fetched. No LLM calls were made.

There are three runs:
- **10-17**: commit 69621f4, the first run.
- **947de40**: blocked PDFs count as no full text; the wording around each accession
  decides ownership; reused series are flagged `shared_gse`.
- **final**: commit ae98e5f, with the fixes below. `screen.csv` and `screen_summary.md` here
  are from this run.

## Summary

| Verdict | 10-17 | 947de40 | final |
|---|---:|---:|---:|
| analyzable | 7 | 4 | **3** |
| needs_inspection | 27 | 7 | **4** |
| excluded | 166 | 189 | **193** |

| Excluded because | 10-17 | 947de40 | final |
|---|---:|---:|---:|
| no_full_text | 50 | 73 | 73 |
| no_own_deposit | 81 | 83 | 88 (6 of them `:reuses_public_gse`) |
| data_on_request | 14 | 15 | 14 |
| unsupported_data_type | 14 | 13 | 13 |
| non_geo_repository | 4 | 3 | 3 |
| normalized_only | 3 | 2 | 2 |

| Needs inspection because | 10-17 | 947de40 | final |
|---|---:|---:|---:|
| error (publisher PDF 403) | 23 | 0 | 0 |
| matrix_raw_tar | 4 | 4 | 4 |
| shared_gse | – | 3 | 0 |

**Analyzable in the final run:**

| Paper | Series | Design |
|---|---|---|
| Cardiovasc Res 2019 (PDF route, docling) | GSE129962 | mouse, raw featureCounts, 15 vs 15 |
| PMID40650303 | GSE298775 | rat, raw counts, 4 groups × 6 |
| PMID33071237 | GSE157585 | human, MASTERS raw counts, groups 63/52/21 |

**Needs inspection in the final run.** These four have only a `_RAW.tar`:
- GSE195585
- GSE242358 (MoTrPAC, two papers)
- GSE208639

## Spot-check (21 papers, checked against the paper text and GEO)

Evidence is a block ID in the paper's structure file, or the GEO series record and its file list.

| # | Paper | Final verdict / reason | Correct? | Evidence | 10-17 | 947de40 |
|---|---|---|---|---|---|---|
| 1 | aeab5224 CVR 2019 | analyzable GSE129962 | yes | DA states own deposit; GEO `GSE129962_DSP.combined.RAW.featureCounts.txt.gz`; genotype 15/15 | ok | ok |
| 2 | PMID40650303 | analyzable GSE298775 | yes | `GSE298775_raw_counts.csv.gz`; Saline/MCT × Sed/Ex, 6 each | ok | ok |
| 3 | PMID33071237 | analyzable GSE157585 | yes | DA S4.6.p1 "raw RNA-Seq and count data from this experiment"; raw-count txt | ok | ok |
| 4 | 080ab719 AD portrait (PMC9561721) | no_own_deposit:reuses_public_gse | yes | 36 series, all in results tables; analyzable GSE81672 was a ketamine study | **wrong**: analyzable GSE81672 | **wrong**: same |
| 5 | PMID31980607 MetaMEx | no_own_deposit:reuses_public_gse | yes | Methods S4.1.p1 "Repositories were screened…"; DA "Original studies… publicly available" | **wrong**: analyzable GSE113165/GSE97084 | **wrong**: shared_gse |
| 6 | PMID40613684 | no_own_deposit:reuses_public_gse | yes | S2.4.p1 "We compiled … RNA-seq data (GSE97084)"; "GESTALT cohort^6 (GSE129643)" | **wrong**: analyzable GSE97084 | **wrong**: shared_gse |
| 7 | PMID37318869 DM1 strength training | needs_inspection matrix_raw_tar GSE208639 | yes | DA "deposited … at GSE208639"; "Data from the Amar et al. … GSE59088 and GSE97084"; GEO has FPKM + `_RAW.tar` | **wrong**: analyzable GSE97084 | reason wrong (shared_gse) |
| 8 | 2dc6a814 collagen peptides | needs_inspection matrix_raw_tar GSE195585 | yes | Methods S2.8.p1 "deposited … GSE195585"; GEO has only `_RAW.tar` | ok | ok |
| 9 | PMID38693412 MoTrPAC | needs_inspection matrix_raw_tar GSE242358 | yes | DA "deposited … GEO … GSE242358"; GEO has `_RAW.tar` + README; 1747 samples | ok | ok |
| 10 | PMID41862462 MoTrPAC TF programs | needs_inspection matrix_raw_tar GSE242358 | yes | Same consortium deposit, DA says "deposited" | ok | ok |
| 11 | 1a8eb7eb electroacupuncture PCOS | no_own_deposit:reuses_public_gse | yes | Methods S1.8.p1 "we performed a meta-analysis including 3 studies (GSE43219, GSE71972 and GSE28422)" | **wrong**: raw_tar | **wrong**: raw_tar |
| 12 | ca29b773 WAT adipogenic genes | no_own_deposit | yes | RT-PCR only; no accession | ok | ok |
| 13 | PMID29263116 Sestrin2 | no_own_deposit | yes | Western blots only | ok | ok |
| 14 | PMID29671347 adipose genomic response | no_own_deposit:reuses_public_gse | verdict yes, reason partly | Own RNA-seq/RRBS described but no accession given; GSE36952 "downloaded" (macrophage reference) | reason wrong (normalized_only on GSE36952) | ok |
| 15 | db39ca83 HIIT muscle | unsupported_data_type:microarray | yes | "microarray data … GSE109657"; Affymetrix CEL | ok | ok |
| 16 | PMID35855056 diabetes biomarkers | no_own_deposit:reuses_public_gse | yes | Abstract "We downloaded the GSE101931 dataset" | reason wrong (microarray, as own) | reason imprecise (data_on_request) |
| 17 | PMID38439070 aging lens | non_geo_repository:sra | yes | DA "deposited in the NCBI SRA … PRJNA1072988" | ok | ok |
| 18 | ddb8851a Per2 contraction | data_on_request | yes | DA "available from the corresponding author upon reasonable request" | ok | ok |
| 19 | 419a2daa 24-h landscape | normalized_only GSE252357 | yes | GEO has only `normalized_counts_protein_coding.csv.gz` + DE tables; GSE214544 is "data from Lovrić et al", now cited | reason ok, ownership wrong (GSE214544 own) | same |
| 20 | PMID40725470 GTEx network | no_own_deposit | yes | Only phs000424 (GTEx), reused | reason wrong (non_geo:dbgap) | ok |
| 21 | PMID23459753 protein timing | no_full_text | yes, given sources | Europe PMC fullTextXML returns 500; no OA PDF URL | ok | ok |

### Accuracy

| Run | Verdict correct | Verdict and reason correct |
|---|---:|---:|
| 10-17 | 16/21 | 13/21 |
| 947de40 | 17/21 | 15/21 |
| final | **21/21** | **20/21** |

The miss in the final run is #14. The paper describes its own RNA-seq but never gives an
accession, so it is excluded correctly, but the reason is labelled as reuse. This spot-check
also drove the fixes, so treat the final figure as an upper bound. The next query's sample
should be checked fresh.

## Bugs found and fixed

All fixes are in ae98e5f and covered by `test/unit/test_paper_screen.py` (15/15).

1. **Meta-analyses claimed dozens of series.** MetaMEx listed 58 series and the AD portrait
   36, mostly in tables or Methods with no deposit wording. When more than 8 GEO series would
   count as the paper's own, only those with deposit wording ("deposited", "generated in this
   study") are kept.
2. **List items lost the reuse wording.** In "Data from the Amar et al. … are accessible at
   GSE59088 and GSE97084", the second accession's context window stopped at GSE59088. The
   wording before the first item of a separator-joined list now covers every item.
3. **More reuse wording.**
   - "meta-analysis";
   - "compiled";
   - "data from (the) <Name> et al";
   - a reference marker right before the accession ("cohort^6 (GSE129643)").
4. **Reason for reuse-only papers.** A paper whose only GEO series are reused was labelled
   `data_on_request` whenever it also had an "upon request" line. It is now
   `no_own_deposit:reuses_public_gse`.
5. **Raw-count files with "Counts" between underscores were missed.** For example
   `GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx`: `\b` does not split on `_`.
   It is now detected as raw counts.

Already fixed in 947de40 (verified on this run):
- 23 publisher-PDF 403s now count as `no_full_text`;
- reuse wording now overrides the section a mention appears in;
- `shared_gse` flags reused series. All three `shared_gse` rows were reuse, and the final
  ownership rules now exclude them directly.

## Remaining limitations

- **No full text for 73/200 (37%).** 36 of them have a PMCID, but Europe PMC returns 500 for
  PMC papers outside its open-access XML set. 26 of them have a PDF URL, but the publisher
  blocks scripted download (403). The PMC OA S3 bucket (used in the PDF evaluation) and the
  publisher's own OA route are not tried yet.
- **Deposit ownership is inferred from wording.** It can still fail on:
  - an own deposit described only as "available in GEO (GSExxx)" when that series also
    appears in a citation-like context;
  - consortium papers reusing their own consortium's series (MoTrPAC; treated as own here,
    which is defensible).
- **`_RAW.tar` always needs inspection.** The screen does not open the archive to check
  whether its members are counts or FPKM.
- **Only bulk RNA-seq is routed.** Microarray (13 papers) is excluded as an unsupported data
  type, even though the workflow can run limma on arrays. Widen with `--routes`.
- **Slow first pass when Europe PMC fails.** Its 500 responses are not cached, so every run
  retries them with backoff (about 30 s each). A cached run still took about 35 min.
- **PDF conversion crash.** When the `screen` process itself converts PDFs, docling can kill
  it. `../paper_screen_20261017/prefetch_full_text.py` converts each paper in its own process.
  It was not needed for this run: everything was already cached, or blocked by 403.

## Reproduce

```bash
python -m tools.paper_screen screen output/screen_20261018/papers.csv --out output/screen_20261018
```

Use the same `papers.csv` as `../paper_screen_20261017/`. To avoid downloading again, copy
`_http_cache/` and `papers/` from the 10-17 output directory.
