# HANDBACK: PMID 37985354 / GSE242294

**Status: refused at `design`.** The data contain no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE242294 --data-root E:/agent/mwangLab_pdf/data` downloaded the series: one matrix (`GSE242294_raw_counts_GAS.txt.gz`, 34,714 genes x 6 samples, all integer values) and 6 GSM records.
2. Read the paper (`PMC10751421.paper.md`): S3.5.p1, FIG6, S2.1.p1, S10.p1, FIG1.
3. `python -m tools.case_runner execute case_spec.json`. Gates recorded: `paper_reconstruction`, `ownership`, `alignment` (6/6 aligned, coverage 1.0), `matrix` (raw counts) and `design` (refused). The validator found 5 records and 0 errors.

## Why it was refused
- GSE242294 is the gastrocnemius of untreated 8-week-old male WT mice (n=3) and global miR-92b knockout mice (M92KO, n=3). GEO lists the treatment as "8 weeks-old mice without treatment", and the paper (S3.5.p1, FIG6) describes this RNA-seq as WT vs M92KO only.
- The paper tests exercise only by qPCR of miR-92b in trained vs untrained mice (FIG1B-D) and by functional running tests. It also reanalyzes three external human GEO sets (GSE95735, GSE58248, GSE209880), none of them this accession. No exercise samples were sequenced.
- The effect of exercise on gene expression therefore cannot be identified from these data. The one contrast the data can support (KO vs WT; suitability verdict "analyzable") measures the genotype effect. Reporting it as an exercise effect would misstate the estimand, so it was not run.

## DEG counts vs paper
- Paper (genotype contrast, not exercise): 2165 DEGs at **P < 0.05 (raw p, no fold-change cutoff)**, 1119 up and 1046 down in M92KO vs WT (S3.5.p1, FIG6). The genes it names are Ugp2 and Slc16a3.
- Ours: none. No contrast was executed because the requested exercise estimand is absent.

## Deviations
- None from the paper. The refusal follows the request (exercise effect), not the paper's genotype aim.
- Alignment used a regex on both sides because the knockout sample stem is written `b92_8W_GAS_n` in the matrix but `92b-8W-GAS-n` in the GEO description. Both sides were reduced to `<C57|92>_<rep>`; this is cross-checked against the GSM titles and the genotype field. Confidence is medium. No positional matching was used.

## Tool problems
- None blocking.
- Minor: `inspect` reported `alignment_keys: []` and gave no hint that `description` holds the sample names. It missed them because the description uses `-` where the matrix uses `_`, and the `b92`/`92b` stems are transposed. The key had to be derived by hand with `key_patterns` and `matrix_column_pattern` (tools/case_runner.py:550-569).
- The suitability report says `analyzable` for the genotype-only design. It does not check whether the requested exercise estimand is present, which is expected since that decision belongs to the agent.
