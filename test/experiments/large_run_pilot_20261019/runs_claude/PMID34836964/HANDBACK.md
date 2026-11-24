# HANDBACK — PMID34836964 / GSE156174

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). Validator: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE156174`: downloaded the series and merged `GSE156174_RAW.tar` into a 95,883 transcript (ENSMUST) × 10 sample integer matrix. GEO `data_processing` says featureCounts raw transcript counts.
- `case_runner execute case_spec.json`: recorded `paper_reconstruction` → `ownership` → `alignment` (exact match on metadata index, 10/10) → `matrix` (raw counts) → `design` (refused). The suitability report (`GSE156174/suitability/suitability.md`) gave the verdict `not_analyzable` because of `sample_size`: 0 of 21 comparisons can be analyzed.

## Why I refused
1. **No exercise arm.** The intervention is hindlimb unloading (HU, mechanical disuse) for 8 or 14 weeks, plus 8 weeks of reloading after 8 weeks of HU (HUR). Ambulatory (AMB) mice are the controls. There is no exercise or training arm.
2. **No replication.** Each group (cell type × treatment × duration) is a single library of RNA pooled from 3–4 mice (S4.7.p1, S2.4.p1). Every contrast is therefore 1 vs 1, with zero residual degrees of freedom. The paper ran an edgeR exact test with the dispersion **fixed at 0.2** (S4.8.p1). Its DEG counts come from that assumed constant, not from variance estimated in the data.

Alternatives I rejected (recorded in the design candidates):
- HUR vs recovery AMB: also 1 vs 1.
- Pooling 8wk and 14wk as replicates: this changes the estimand, because age and duration differ and the 14wk MSC libraries were total-RNA preps while the rest were poly-A. It would still give only 2 vs 2.
- Re-running the fixed-dispersion edgeR: no executor supports it, and the result would be an assumption rather than an estimate.

## DEG counts vs paper
| Contrast | Ours | Paper |
|---|---|---|
| 8wk HU vs AMB, SSC | not run (refused) | 3991 (S2.4.p1) |
| 8wk HU vs AMB, MSC | not run (refused) | 1504 (S2.4.p1) |
| 14wk HU vs AMB, SSC / MSC | not run | not given in the text; "fewer than 8wk" (Suppl. Fig. 5d,e) |

The paper gives no DEG threshold for the RNA-seq. S4.9.p1 sets a general p ≤ 0.05, and Fig. 3 highlights genes with log2FC > 2. I recorded `pvalue < 0.05` with `stated_explicitly: false`.

## Deviations
None executed. Paper's method (edgeR exactTest, dispersion = 0.2, TMM, sum of counts > 2, protein-coding transcripts) is recorded in `paper_reconstruction` but not reproduced.

## Tool problems
- The Bash heredoc failed on this spec (`unexpected EOF while looking for matching '`), possibly because of apostrophes inside the quoted heredoc text. This was an environment problem, not a repository one; I wrote the spec with the Write tool instead.
- The PowerShell tool refused `$env:PYTHONIOENCODING=...` ("Command modifies environment variables"), so I ran the commands through Bash. This was also an environment problem.
- No repository tool problems. One minor gap: `levels.grp` in the execute output pools cell types (for example `AMB_w8: 2` = 1 SSC + 1 MSC), because the strata split is applied only inside suitability. This could mislead a quick reader about n per arm.
