# Workflow skill review, stages D to H (2026-10-13)

Follow-up to [SKILL_REVIEW_20261010.md](SKILL_REVIEW_20261010.md). The goal of the work was a
`bioinformatics-workflow` skill that runs on any machine, under Codex or Claude Code, from a
repository clone plus `requirements-skill.txt`. The staged plan and per-stage notes are in
[docs/status/SKILL_PORTABILITY_PLAN.md](../status/SKILL_PORTABILITY_PLAN.md).

## Verdict

The skill is portable and its decisions are reliable on every case set tried. It ran on a
Windows machine under Codex, made correct paper-aligned decisions on a real study, and
reproduced a trusted R DESeq2 analysis gene for gene in fold change. What is not yet shown:
a scored blind run under Codex, a strictly blind real-data run, and scale beyond tens of cases.

## Evidence by stage

| Stage | What was tested | Result |
|---|---|---|
| D | Round-3 blind test: 9 synthetic cases with planted traps (paired design, batch aliased with the arm, FPKM only, multilevel, no exercise arm, single-cell, LFQ proteomics, paired methylation, probe-level GSEA), both skill locations | 9/9 decisions correct in both sessions; validator and scorer caught every injected error |
| E | Fixes from round 3, cases 07 to 09 | All pass; record `VALID`; helper code written by the session fell from about 1,300 to 245 lines |
| F | Real execution on Windows 11, Python 3.12 | Preflight fully available (network, R limma). First self-test 5/7: an inmoose 0.9.1 eBayes bug (`KeyError: -2` when the prior df is infinite) broke multilevel limma and proteomics. After `tools/limma_compat.py`: 7/7 routes pass, 60 records with 0 errors, audit `pass` (100) |
| G | Live Codex run | Verified by the user on Codex; not scored |
| H | Real study GSE195482 against Bo's R DESeq2 tables | All 24 records `VALID` and correct; log2FC Pearson 1.000 over about 17,000 genes, direction 100%, DEG Jaccard 0.910 (female) and 0.904 (male) |

## Stage H in detail

Codex read the published article and analysed the two supplied contrasts (HFpEF diet against
chow in wild-type cardiomyocytes, female and male, 3 against 3). Its decisions:

- two sex-stratified pairwise contrasts, as in the paper, not pooled;
- raw counts with DESeq2, `~ condition`, no blocking (independent animals);
- the paper's threshold, BH-adjusted P < 0.05 with no fold-change cutoff;
- a declared deviation: PyDESeq2 instead of edgeR scaling plus DESeq2 1.16.1.

| Contrast | Bo DEG | Skill DEG | Overlap | Jaccard | Bo DEG recovered, same direction |
|---|---:|---:|---:|---:|---:|
| WMF vs WCF | 1,360 | 1,379 | 1,305 | 0.910 | 96.0% |
| WMM vs WCM | 131 | 128 | 123 | 0.904 | 93.9% |

Every discordant gene lies at the significance boundary (padj 0.04 to 0.06 in both tables).
The main cause is the low-count pre-filter: Bo keeps genes with a total count of at least 10
(about 17,000 genes), the skill's DESeq2 tool kept every gene that was not all zero (23,500),
so different gene sets entered the BH adjustment. PyDESeq2 standard errors are also about 2%
larger. The pre-filter was not a recorded decision; `run_deseq2_analysis` now takes
`min_total_count`, and the method decision records it as `prefilter`.

Caveats: Codex ran from the main repository, which holds an older note with these contrasts'
DEG counts, so the run was not strictly blind; nothing in its outputs refers to the note, and
the counts come from PyDESeq2 directly. The run predates trace recording.

Details: [test/experiments/stage_h_bo_reference/RESULTS.md](../../test/experiments/stage_h_bo_reference/RESULTS.md).

## Decision traces

Native runs now write `trace.jsonl`: every helper and tool call with duration and outcome,
every decision with its revision number and the fields that changed, and records the contract
rejected. `scripts/analyze_traces.py` aggregates runs into stops, hesitation signals, tool
failures, and a review sheet with reviewer columns modelled on a two-reviewer binary audit.

Applied to the decision records of 33 earlier blind-test cases, the gates most often recorded
below high confidence were:

- `ownership` (30%): case metadata carried no accession column, so ownership rested on file
  names and content;
- `method` (20%): the paper's own method had no executor in the repository (for example
  Perseus with permutation FDR), so the agent declared an alternative.

Both point to fixable causes rather than model weakness.

## Changes in this branch

- Portable skill copies in `.agents/skills` (Codex) and `.claude/skills` (Claude Code) from one
  source, with a drift check (`scripts/sync_skills.py --check`).
- Native runtime `tools/native.py`: exact alignment, design, confounding and pairing checks,
  run recorder, external-LLM block, decision trace.
- Decision contract v2 with cross-record invariants and `validate_decision_contract.py`.
- Modalities: single-cell pseudobulk, proteomics, methylation, and an enrichment gate.
- LangChain-optional tools and `requirements-skill.txt`; per-capability preflight;
  `scripts/skill_selftest.py`.
- `tools/limma_compat.py` (inmoose eBayes fix); DESeq2 `min_total_count`.
- ExerGeneDB gold export and contrast scoring; blind forward-test case sets and scorers;
  Bo-reference comparison for stage H.

Unit tests: no test module that passes on `main` fails on this branch; 15 of 62 modules pass in
a sandbox without pydeseq2, inmoose, patsy, or GEOparse (1 of 55 on `main` in the same sandbox).
The full self-test passes on a complete environment.

## Open items

1. Rerun stage H from the clean checkout with `min_total_count=10`, to get a strictly blind run
   with a trace and to confirm the remaining gap is PyDESeq2 against R.
2. Score a blind Codex run on the nine-case set (`output/stage_g/repo`).
3. Expert review: two reviewers fill `review_sheet.csv` for a random sample of real runs.
4. Scale: run ExerGeneDB-labelled studies to measure control/treatment accuracy and trace
   statistics over many studies.
5. Not implemented, recorded as declared deviations when a paper needs them: IRS correction
   for multi-plex TMT, an omnibus F-test, a per-group proteomics missingness filter,
   permutation FDR.
