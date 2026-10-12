# Workflow skill portability plan

Goal: the `bioinformatics-workflow` skill runs on any machine (Windows, macOS, Linux) under Codex or Claude Code, from a repository clone plus `requirements-skill.txt`. The plan is split into stages that each fit in one usage window.

Branch: `zoutongfei/skill-portability` on GitHub (pushed 2026-10-11).

## How to resume in a new session

1. Check out `zoutongfei/skill-portability`.
2. Start the session with: "Continue the skill portability plan at stage <X>. Read `docs/status/SKILL_PORTABILITY_PLAN.md` first."
3. When a stage finishes, update its status line here and commit.

Budget notes:
- One blind-test session costs about 250k subagent tokens and 12 minutes for five cases.
- Run one blind session per window, not two in parallel.
- Keep the scorer-side files (`test/experiments/skill_forward_test_*`, `docs/reviews/SKILL_REVIEW_*`) out of tested checkouts.

## Done

| Stage | Commit | Result |
|---|---|---|
| A. Review and round-1 blind test | `282382b` | Decisions 10/10 correct in 2 sessions. Validator accepted 4/4 injected errors; auditor coverage 4–31%; each session wrote about 1,300 lines of glue code |
| B. Portability foundation and round-2 fixes | `4b4086d`, `6ef1b37` | Skill copies in `.agents/skills` and `.claude/skills` with drift check; `tools/native.py`; contract v2 with case invariants; external-LLM block; native runs auditable. Round 2: 5/5 in both sessions |
| C. All modalities and machine self-test | `fbca852` | Enrichment gate; single-cell, proteomics, and methylation routes; LangChain-optional tools; `requirements-skill.txt`; preflight per capability with `--network`; `scripts/skill_selftest.py` |
| D. Round-3 blind test (9 cases, both skill locations) and fixes | `029fb50` | 9/9 in both sessions; validator and scorer caught all injected modality errors. Fixed the integer check (large LFQ intensities counted as raw counts), threshold metric names and adjustment changes, planned-but-not-run enrichment, observational wording, and the gene-collapse and complete-pair helpers |

## Remaining stages

### E. Verify the round-3 fixes (done 2026-10-11)

Result: cases 01 and 06 (first attempt) and 07, 08, 09 (second session, `.claude/skills`) all pass the scorer; the contract check is `VALID`; the audit reports `incomplete_environment` with no blocking findings. Helper code written by the session fell from about 1,300 lines to 245. Its four documentation notes were fixed. The `.agents/skills` copy is byte-identical (checked by `sync_skills.py --check`), so a separate Codex-location rerun is deferred to stage G.

- Scope: cases 07, 08, and 09, in one session for the `.claude/skills` location. In the next window, run the same cases for the `.agents/skills` location.
- Setup: create a checkout at commit `029fb50` or later and remove the scorer-side files. Then run `python test/experiments/skill_forward_test_20261011/make_cases.py <checkout>/cases` and trim the manifest to the three cases.
- Exit:
  - `score_run.py` passes;
  - `validate_decision_contract.py` reports `VALID`;
  - the audit reports `incomplete_environment` with no blocking findings;
  - the usability notes are triaged into fixes or "won't fix".

### F. Real execution on a full environment

First run (2026-10-11, Windows 11, Python 3.12.4, commit `165bea5`): preflight fully available (`de_capable: true`, every network host reachable, R limma found). Five of seven self-test routes passed (DESeq2 with blocking, limma on FPKM, methylation, paired single-cell, GSEA and ORA). Multilevel limma and label-free proteomics failed with `KeyError: -2`, an inmoose 0.9.1 eBayes bug: when residual variances are near-homogeneous, squeezeVar returns `df_prior = inf` as a Python float and `~True == -2` is used as a column key. Fixed by `tools/limma_compat.ebayes`, used by `limma_tools` and `multigroup_tools`; regression test `test/unit/test_limma_compat.py`. With inmoose loaded in the cloud workspace, all limma routes then pass.

Second run (2026-10-11, Windows, commit `f9eb082`): **done**. All 7 routes `PASS` (sensitivity 1.0 except paired single-cell 0.9; null false-positive rate at most 0.006; sign agreement 1.0). Decision contract: 60 records, 0 errors. Audit: `pass`, score 100. External LLM attempts: 0.

This is the stage that proves the skill runs on another device. It cannot run in the cloud sandbox, where PyPI, GEO, and enrichment services are blocked. Run it on your computer, or on any machine with network:

```bash
git fetch origin && git checkout <branch>
python -m venv .venv && . .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-skill.txt
python .agents/skills/bioinformatics-workflow/scripts/preflight.py --network --out output/preflight.json
python scripts/skill_selftest.py --network --require-all
```

Exit:
- every self-test route is `PASS`: DESeq2 with blocking, limma on FPKM, multilevel limma, methylation, proteomics, paired single-cell, GSEA and ORA;
- preflight reports `de_capable: true`.

Send back `output/preflight.json` and `output/skill_selftest_*/selftest_report.json`. A failing route becomes the first task of the next stage. If possible, repeat on a second OS.

### G. Live Codex run

Status (2026-10-11): verified by the user on Codex; not scored here. A blind checkout is at `output/stage_g/repo` (9 cases) if a scored run is wanted later.

Run the Codex CLI in a clean checkout with network enabled:

```bash
codex -c 'sandbox_workspace_write.network_access=true'
```

Give it the request: "Use $bioinformatics-workflow to analyze the studies in cases/manifest.json. For each study, determine how exercise affects the measured molecules as the paper intends. Where the paper reports pathway results, also run the pathway analysis."

Score the run directory with `score_run.py`, `validate_decision_contract.py`, and `audit_run.py`.

Exit: every case passes, the record is `VALID`, and the audit verdict is `pass`, with real DE tables this time.

### H. One real study end to end

Run one GEO study with a trusted reference (a BO benchmark contrast, or GSE132520) through the skill with execution. Compare logFC, direction, and DEG overlap with the reference.

Exit: the agreement metrics are reported, and any difference is explained by a recorded decision.

Setup (2026-10-11): study GSE195482 (HFpEF diet vs chow in WT cardiomyocytes, female `WMF_vs_WCF` and male `WMM_vs_WCM`, 3 vs 3 raw counts). Reference: Bo's R DESeq2 tables in `F:\RNAseqData4Testing\GSE195482`. Blind workspace: `output/stage_h/repo` with `cases/GSE195482/` (two matrices, metadata, `paper.md` from the published article); Bo's results and scripts withheld, and the 2026-10-09 handoff note (which lists earlier DEG counts) removed. Scoring: `test/experiments/stage_h_bo_reference/compare_to_reference.py` against `*.allgene.DEseq2.txt`.

### I. Wrap-up

- Add the stage D–H results to `docs/reviews/SKILL_REVIEW_20261010.md`, or a follow-up review.
- Open a PR to `main`, and keep `sync_skills.py --check` in the test run.

## Known limits

- Cloud sandbox: no PyPI, GEO, ExerGeneDB, or enrichment hosts, so stages F–H run on a full machine.
- Not implemented:
  - IRS correction for multi-plex TMT;
  - an omnibus F-test;
  - a per-group proteomics missingness filter;
  - permutation FDR.

  Each is recorded as a declared deviation when a paper needs it.
