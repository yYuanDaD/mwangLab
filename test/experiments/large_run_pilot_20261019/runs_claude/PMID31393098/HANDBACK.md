# HANDBACK — PMID31393098 / GSE129612

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). Validator: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE129612` (cached data) → `inspect_GSE129612.json`.
- `case_runner execute case_spec.json`: gates paper_reconstruction → ownership → alignment → matrix → design (refused). Alignment exact on the title suffix (`runNNNN: <name>`), 6/6 samples; grp CON 3 / KO 3. Suitability verdict `analyzable` for the genetic contrast, which I refused as off-estimand.

## Why refused
- The paper's only RNA-seq (S2.8.p2, S4.12.p1) is FACS-sorted EGFP+ cardiac myofibroblasts 4 weeks after TAC, **Hsp47-deleted vs control** (Postn-MCM). n = 3 + 3.
- Exercise appears only as a forced downhill treadmill performance test in Sgcd-null dystrophic mice (S2.5.p1, S4.15.p1, Fig. 4G). It was not sequenced.
- GEO metadata vary only by genotype, so no exercise contrast exists. Running KO vs CON would produce a genetic result labelled as exercise.

## DEG counts vs paper
- None computed (stopped before execution).
- The paper reports no DEG count, only Supplemental Table 1 categories and qPCR genes.
- Paper threshold: the paper states none. GEO data_processing gives AltAnalyze moderated t, raw p < 0.05 with fold > 2. That rule is recorded in paper_reconstruction for reference only.

## Deviations / notes
- Matrix chosen: `GSE129612_Khalil_et_al_All_gene_list.csv` (AltAnalyze output, log2-TPM scale; it mixes 6 sample columns with avg/fold/p columns). This was recorded only: no executor read it.
- Sequencing-run confound: 2 controls are in run1739; 1 control and all 3 KO are in run2675. I recorded this as a discrepancy. It would matter for any genetic analysis.

## Tool problems
- `inspect` reports the AltAnalyze statistic columns (`avg-Mutant`, `log_fold-…`, `fold-…`) as `sample_columns`, and gives `n_samples: 15` for files that hold 6 real samples. The candidate `type` list is empty, so there is no matrix-type hint for log-TPM. These are minor and did not block the run.
- No other problems.
