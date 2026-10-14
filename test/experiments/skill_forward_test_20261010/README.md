# Blind skill forward test (2026-10-10)

Tests whether a fresh agent session, given only the `bioinformatics-workflow` skill and frozen inputs, makes the scientific decisions correctly. Findings are in [docs/reviews/SKILL_REVIEW_20261010.md](../../../docs/reviews/SKILL_REVIEW_20261010.md).

## Files

| File | Purpose |
|---|---|
| `make_cases.py` | Writes five synthetic GEO-like cases (paper text, GEO-style metadata, matrix, manifest) |
| `answer_key.json` | Scorer-side expectations. Never copy into a tested workspace |
| `score_run.py` | Scores one or more `runs/` directories against the answer key; layout-independent |
| `results.json` | Scores from the 2026-10-10 Claude Code run, negative control, audit and validator results |

## Cases

| Case | Design | What a wrong decision would look like |
|---|---|---|
| case_01 | 8 subjects, pre and 3 h post, raw counts; matrix columns are shuffled sample titles | Unpaired model; positional alignment; added fold-change cutoff |
| case_02 | 4 vs 4 mice; sequencing run identical to the exercise arm; paper silent | Running DE as if the effect were estimable |
| case_03 | Only FPKM deposited; paper used DESeq2 on counts | DESeq2 on rounded FPKM; calling a limma deviation an exact reproduction |
| case_04 | Control plus 0 h, 6 h, 24 h groups of different animals; FC > 1.5 | Pooling time points; blocking on unique animal IDs; using abs(log2FC) > 1.5 or > 1 |
| case_05 | Genotype-only RNA-seq; exercise tested in a separate cohort | Substituting the knockout contrast for an exercise contrast |

## Protocol

1. Create a clean checkout, copy the skill into the platform's skill directory (`.claude/skills/` for Claude Code, `.agents/skills/` for Codex), and run `python make_cases.py <workspace>/cases`.
2. Start a new session in that workspace with this request: "Use the bioinformatics-workflow skill to analyze the five studies listed in cases/manifest.json. For each study, determine how exercise affects gene expression as intended by the paper, following the skill's workflow." State the environment limits (no network, available packages) and ask for outputs under `runs/<case_id>/`.
3. Score: `python score_run.py <workspace>/runs`.
4. Keep a negative control: edit a copy of a passing run to inject known errors and confirm the scorer fails it.

The scorer checks decisions only. It does not check numerical results, because execution was not available in the sandbox where this test was first run.
