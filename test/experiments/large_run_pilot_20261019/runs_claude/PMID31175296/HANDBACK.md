# HANDBACK: PMID 31175296 / GSE125630

Status: **refused at the `design` gate**. Contract validator: 0 errors. Route: `stopped`.

## What ran
- `python -m tools.case_runner inspect GSE125630`: the series was already cached (`data/GSE125630`). It holds one matrix, `GSE125630_GeneMatrix_RawCounts_InjuryActivity.txt.gz`: 24,613 Ensembl rat genes x 24 samples, integer raw HTSeq counts.
- `python -m tools.case_runner execute case_spec.json`, with these gates recorded:
  - `paper_reconstruction`
  - `ownership`
  - `alignment`: 24/24 samples matched by a key derived from the GSM title and from the matrix column name, compared case-insensitively. No positional alignment.
  - `matrix`: raw counts, DESeq2 route.
  - `design`: refused.
- No executions or enrichment ran.
- Earlier attempts are kept in `_previous/`. The first attempt marked the design `valid` and refused at `covariance`. The runner rejected it because the suitability verdict was `not_analyzable`, so the refusal moved to `design`.
- Evidence for the decision: an ad-hoc read-only PCA on log2 CPM of the 500 most variable genes. It was not saved as an artifact; the numbers are recorded in the design `stop_reason`.

## The paper
- The paper is a Scientific Data *Data Descriptor*. It reports no differential-expression analysis, no DEG counts, no DE genes and no threshold.
- It defines an exercise comparison set (S4.2.p1): CONT SCI (n=6) vs CONT SCI + SWIM (n=5) and CONT SCI + SWW (n=5). The planned contrasts were therefore `grp_SWIM_vs_CONT` and `grp_SWW_vs_CONT`, from a single five-level `grp` model.

## Why it was refused
Exercise is completely aliased with the time of sacrifice and the tissue-collection session:
- Every SWIM and SWW animal was sacrificed at 13.5 weeks post-surgery.
- Every sedentary CONT SCI animal (and every No SCI animal) was sacrificed at 11.5 weeks.
- TX SCI animals were sacrificed at 8.5 weeks.
- Sources: GEO `weeks after injury`, S2.3.p1, S4.3.p1, FIG2.

No sedentary contused animal shares the exercised animals' collection time, so the 2-week, age and collection-session difference cannot be adjusted out of the exercise contrast.

The data show this confound dominates. PC1 explains 57% of the variance (the paper's Fig 3b reports 66%). Mean PC1 score by group:

| Group | Weeks post-surgery at sacrifice | Mean PC1 |
|---|---|---|
| No SCI | 11.5 | -14.3 |
| CONT SCI | 11.5 | -14.6 |
| CONT SCI + SWIM | 13.5 | +9.9 |
| CONT SCI + SWW | 13.5 | +10.5 |
| TX SCI | 8.5 | +10.7 |

PC1 splits the 11.5-week collection from the other collection times. It does not separate exercise from injury biology: complete transection lands in the same place as mild swimming or wading, while contusion vs no injury shows no shift at all.

The paper argues that batch effects are low (S4.3.p1). That is an assumption, not a design control.

The runner's suitability check independently failed covariance: `wpi: primary_nested_in_candidate`.

Alternatives considered and rejected:
- SWIM vs SWW (same collection time) compares two exercise modalities, not exercise vs no exercise.
- Pooling the two exercise groups would combine two distinct exercise levels.

## DEG counts vs paper
Not applicable. The paper reports no DEGs and no threshold; the case stopped before execution, so we have no counts either. Had it run, the threshold would have been `workflow_default` (BH padj < 0.05, no fold-change cutoff).

## Deviations
None executed.

## Tool problems
- **Skill reference and runner disagree on where an aliased covariate stops the case.** `references/decision-gates.md` (Covariate gate section) says to refuse at `covariance` with `status: unresolved`. But the runner always runs suitability at `design`, and `tools/decision_contract.py:174` rejects a `valid` design when suitability is `not_analyzable`. So an aliased covariate can only be refused at `design`.
- **The sex check cannot run on Rnor_6.0 Ensembl 93 counts.** `xist_signal` is 0 for all 24 female samples and the Y signal is near 0, so the result is `no_markers` (`tools/suitability.py:435`, via `tools/stats_tools.py:309` `infer_sex_from_expression`). Rat Xist is probably absent from this annotation. This did not affect the decision; the study is female-only (S2.1.p1).
- **Inspect could not offer an alignment key** (`alignment_keys: []`). The matrix column names use different words from the GSM titles ("Uninjured" vs "No SCI"). I solved this with `key_patterns`, `matrix_column_pattern` and `normalize_keys`. As a result, the naive animals are keyed by replicate number alone ("1" to "4"); the keys are unique but not self-describing.
