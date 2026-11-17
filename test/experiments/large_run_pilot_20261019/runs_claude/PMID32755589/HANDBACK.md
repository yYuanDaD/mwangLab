# HANDBACK: PMID 32755589 / GSE142678 (RGS6, voluntary running, adult-born DG neurons)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID32755589` (run label PMID32755589).
Route: case spec (`python -m tools.case_runner execute case_spec.json`). Validator: 24 records, 0 errors. No external LLM calls were made.

## Study and data
- Paper design (S2.1.p2, S4.3.7.p1, Fig 1B/E/F): RiboTag-seq on female Nes-CreERT2::RiboTag mice. There are 2 fractions (IP = adult-born neurons, IN = whole dentate gyrus input), 3 running durations (11, 18 and 27 days) and 2 arms (running, sedentary), with **2 replicates per cell**. Each replicate is a pool of 2-4 mice, so there are 24 libraries.
- Paper DE method: EBSeq inside RSEM on expected counts, called at **PPEE < 0.05** (a posterior-probability FDR) with no fold-change rule. Running and sedentary are compared within each duration, separately for IP and IN. The Fig 3A volcano colours genes at p < 0.05 and |FC| > 1.5; this is a display rule only.
- Data: the only deposited matrix is `GSE142678_nes_run_TPM.csv.gz`. It holds RSEM TPM (each column sums to 1e6) and is aligned exactly to the GEO `title` field (24/24). Expected counts are not deposited, so the EBSeq route is blocked.
- Prep: `prep_drop_ambiguous_ids.py` removed the 4 rows with Excel-mangled duplicate IDs `1-Mar` and `2-Mar`, whose true gene identity is ambiguous. Its output is `GSE142678_TPM_dedup.csv` (23302 x 24).

## Cases
1. **GSE142678_per_duration**: the paper's primary estimand. It covers 6 contrasts, running vs sedentary at 11, 18 and 27 days in IP and in IN. It **stopped at the design gate (`manual_review`)**. Suitability returned `not_analyzable` (sample_size): every cell has n = 2, so 0 of 22 comparisons reach n >= 3, and the decision contract rejects a valid design on that verdict. The paper, ownership, alignment and matrix gates were recorded.
2. **GSE142678_across_durations**: the Fig 3A / S2.3.p1 estimand, running vs sedentary "across all three time points" (Rgs6 top up, Abca8a top down). It **completed** as a declared deviation: limma on log2(TPM+1), `~ 0 + C(cell) + C(time_raw)`, fitted separately for IP and IN. Each fraction has 6 running vs 6 sedentary pools, with duration as an additive covariate and 8 residual df.

## DEG counts vs paper
Applied threshold: BH padj < 0.05 with no fold-change rule (`paper_on_deviation_route`: the paper's PPEE < 0.05 mapped to BH). Audit threshold: p < 0.05 and |log2FC| > log2(1.5) = 0.5849625, the Fig 3A display rule.

| Table | Ours (applied) | Ours (audit) | Paper |
|---|---|---|---|
| IP, running vs sedentary, across durations | 0 | 288 | not stated (Fig 3A volcano) |
| IN, running vs sedentary, across durations | 0 | 214 | not stated |
| IP 18 d / IP 27 d / IN 27 d (per duration) | not run (stopped at design) | - | 460 / 544 (508+36) / 124 (88+36) |
| IP 11 d, IN 11 d, IN 18 d | not run | - | only in the Fig 1E bar chart |

Named genes (across-duration tables):
- IP: Rgs6 log2FC +0.73 (p 1.0e-4, padj 0.33), Abca8a -0.84 (p 2.1e-4), Calb2 +1.01 (p 0.002) and Bdnf +0.45 (p 0.002).
- IN: Rgs6 -0.01 (p 0.94), Abca8a -0.37 (p 0.014) and Bdnf +0.31 (p 0.035).
- All directions agree with the paper: Rgs6 is up in IP only, and Abca8a is down in both fractions. None passes BH.

GSEA (Hallmark, ranked by t):
- IP: MYC targets V1/V2, E2F, G2M, OXPHOS and mTORC1 are positive (FDR < 0.01).
- IN: protein secretion, Hedgehog, MYC targets, UVR-DN and OXPHOS are negative.

ORA did not run because the list was empty (0 genes at the applied threshold).

## Deviations
- The method changed from EBSeq on expected counts to limma on log2(TPM+1), because counts are not deposited. The threshold metric changed from PPEE to BH padj.
- The paper's per-duration contrasts were not executed (see Tool problems). Only the across-duration Fig 3A comparison ran. Whether the paper pooled durations for Fig 3A or adjusted for them is not stated. I adjusted for duration.
- I removed the four ambiguous `1-Mar`/`2-Mar` rows. Other Excel-date IDs remain and will not map in enrichment.
- The replicate letter (`pair`, a-f) was not used as a block: the paper does not document it and did not block.

## Tool problems
1. **Small-n gate contradicts the skill.** SKILL.md and decision-contract.md say small n alone is not a stop and that planned small-n contrasts should run as exploratory. But `tools/suitability.py:259-276` (`check_sample_size`) fails when no comparison has n >= 3, `tools/suitability.py:502-504` makes that a hard `not_analyzable`, and `tools/decision_contract.py:172-174` then rejects any valid design. The `include` escape in `tools/joint_contrasts.py:174` (run_joint_limma) and `:139` (run_joint_deseq2) is therefore unreachable when every cell has n = 2. The paper's 6 per-duration contrasts (n = 2 vs 2, 6 residual df in a per-fraction joint model) could not run.
2. **Stale case directory after a rerun.** `tools/case_runner.py:426-437` (`_move_previous_attempt`) moves only the case directories named in the *new* spec. After the case IDs changed between attempts, the first attempt's `GSE142678/` stayed in the run directory. I moved it by hand to `_previous/20261117T162709Z/GSE142678_first_attempt`.
3. Minor: the bash heredoc of the long JSON spec failed in this shell with "unexpected EOF", so the spec was written with the editor tool instead. This is not a repository bug.
