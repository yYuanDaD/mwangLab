# HANDBACK — PMID39141732 / GSE263912

**Status: refused at `design`** (no exercise contrast in the sequenced samples).

## What ran
- `case_runner inspect GSE263912`. The first attempt hung for more than 10 minutes with no output while it fetched the supplementary file over HTTPS. I stopped it, fetched `GSE263912_NormCounts.txt.gz` over `ftp://` with curl, put it in `data/GSE263912/` and re-ran inspect.
- `case_runner execute case_spec.json`: gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design` were recorded. The case stops at `design` with `refused`. The validator reported 0 errors.
  - Alignment: exact match on a key taken from `title`, 9 of 9 samples.
  - Groups: HN = p38αMCK-KO, COW = p38α/γMCK-KO, KIC = control, 3 libraries each.
  - Matrix: the deposited file is TMM-normalized CPM (non-integer, already filtered to genes with CPM ≥ 1 in ≥ 3 samples). Raw or RSEM expected counts are not deposited.
  - Suitability: all three genotype comparisons are analyzable.
- Executions: none. Enrichment: none.

## Why it was refused
- The paper's only RNA-seq experiment (S4.22.p1–p2, FIG5 A–C) is gastrocnemius from sedentary mice fed a high-fat diet for 6 weeks and fasted overnight.
- It compares three genotypes: p38αMCK-KO vs control, p38α/γMCK-KO vs control, and p38αMCK-KO vs p38α/γMCK-KO.
- Exercise appears only in experiments that were not sequenced: plasma IL-15 after treadmill running (FIG5E), human biopsies (FIG1A), and wheel/treadmill behaviour (FIG4).
- No metadata column codes exercise, training or time after exercise.
- Calling the knockout contrast an "exercise effect" would misstate the estimand, so it was rejected as a candidate.

## DEG counts vs the paper
- Paper threshold: BH FDR < 0.05, no fold-change cutoff (S4.22.p2). The secreted-protein candidate list used raw P < 0.05 before the SignalP/SecretomeP/TargetP filter (S4.24.p1).
- Paper counts:
  - 15 secreted-protein DEGs in p38αMCK-KO.
  - Il15 is up in p38αMCK-KO but not in p38α/γMCK-KO.
  - Total FDR DEG counts are not reported.
- Ours: none, because the case was refused before any model ran.

## Deviations and discrepancies
- The paper names no GEO accession (S5.4.p1). Ownership rests on matching content: tissue, diet, genotypes, CNIC pipeline and CPM filter. Confidence: medium.
- Paper vs GEO:
  - Reference: GRCm38.76 vs GRCm38.91.
  - Sequencer: HiSeq2500 vs MiSeq.
  - Input: the paper ran limma on expected counts; GEO has only TMM-normalized CPM.

## Tool problems
- `tools/geo_tools.py:60` calls `requests.get(ftp_url)` with no timeout, and `:93` (`urllib.request.urlretrieve`) has no timeout either. When HTTPS to ftp.ncbi.nlm.nih.gov stalls, `inspect` hangs with no output and an empty log, and there is no FTP fallback. `ftp://` worked from this machine.
- Spec usability: `alignment.aliases` maps `{new_name: source_column}`. I first wrote it the other way round, and the error message (`alias source column 'geno' not in metadata`, `tools/native.py:381`) was clear enough to fix it.
