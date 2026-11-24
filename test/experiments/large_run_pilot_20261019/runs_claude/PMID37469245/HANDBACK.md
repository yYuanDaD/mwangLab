# HANDBACK — PMID37469245 / GSE216408

**Status: refused at `design`. No exercise contrast in the data.**

## What ran
- `case_runner inspect GSE216408`: downloaded to `data/GSE216408`. One matrix, `GSE216408_exp_all.csv.gz`, with 21,487 genes × 7 samples (WT-1..3, KO-1..4). 92% of values are integers and the maximum is 3.25e6. GEO says STAR + RSEM, then DESeq2, so I read it as RSEM expected counts.
- `case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors. The case is `stopped:design` with route `stopped`.
  - Alignment: the key comes from the title (`GAS WT repN` / `GAS MPARK7KO repN`) and is matched to the matrix columns ignoring separators. All 7 of 7 samples aligned.

## Why refused
- The paper's RNA-seq (S2.16.p1, S3.6.p1, Fig. 5) covers GAS muscle from **immobilized** MDKO (DJ-1/Park7 knockout) mice (n=4) and immobilized Flox mice (n=3).
- In GEO, `treatment` is the same for every sample ("immobilization-induced muscle atrophy"). The only factor that varies is genotype.
- Exercise appears in the paper only as phenotyping: treadmill exhaustion, rotarod, grip and ladder tests (S2.11, S3.2). No exercised or sedentary-vs-exercise animals were sequenced.
- So the exercise effect on gene expression cannot be estimated from these data. I rejected the genotype contrast (KO vs WT under disuse) as a stand-in, because it is not an exercise estimand.

## DEG counts vs paper
- Paper: 1113 DEGs for MDKO vs Flox (763 down, so 350 up). The threshold comes from GEO data_processing: DESeq2 adjusted P < 0.05 and |FC| > 1.5, i.e. |log2FC| > 0.5849625. The paper text itself states no DEG threshold.
- Ours: none. Nothing was executed because the case was refused, so there was no comparison to make.

## Deviations
- None, since nothing was executed. The paper threshold is taken from the GEO record, not the article.

## Tool problems
- **Suitability report with no design factors** (`tools/suitability.py:332-358`): I refused at design without giving any `factors`. The report then said `not_analyzable` because of `sample_size` ("0/0 comparisons"). It also listed constant columns (`data_processing`, `library_selection`, `library_source`, `library_strategy`) as `candidate_covariate`, "crossed with the design factors". With an empty factor list the loop never runs, so `worst` stays `"crossed"`. Constant columns should be dropped before that loop. This did not change the outcome.
- **Matrix quirks**: the matrix has 2 duplicated gene symbols and Excel-mangled IDs (`1-Mar`, `11-Mar`, ...), which inspect flagged. They did not matter here, but a rerun of the genotype contrast would need a prep script.
- **Spec authoring**: a `\d` regex inside a Bash heredoc reached the JSON as an invalid escape, so I used `[0-9]` instead. The runner's error was a raw JSONDecodeError traceback (`tools/case_runner.py:1115`) rather than a `spec_error`.
