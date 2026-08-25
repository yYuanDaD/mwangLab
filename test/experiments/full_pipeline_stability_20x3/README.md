# Full RNA-seq Pipeline Stability Benchmark (20 x 3)

This is the formal scale-up after the six-case production preflight. It executes 20 frozen GEO
studies in three independent repeats (60 full trials) using DeepSeek V4 Pro, cached acquisition,
production matrix routing, QC, sample alignment, contrast selection, DESeq2/limma, and live
Hallmark GSEA.

The set contains 12 raw-count, five linear FPKM/TPM, and three already-log-scale matrices; 17 mouse
and three human studies; single- and multi-contrast designs; and three semantic-alignment cases.
It intentionally mixes nine regression cases with eleven newly added generalization cases. It is
therefore a production stability/regression benchmark, not a claim that all 20 studies are unseen.

## Budget

Planning assumes 42 structured DeepSeek calls at $0.003/call: $0.126 at regular pricing and $0.252
with a 2x peak contingency. The hard default budget is $0.50. The runner stops between trials if the
measured regular-price estimate times 2 exceeds the hard limit. GEO, MSigDB, and MyGene endpoints do
not have a per-call charge in this project; compute, storage, and network infrastructure are outside
the token budget.

## Run

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python test/experiments/full_pipeline_stability_20x3/prepare_manifest.py --dry-run
python test/experiments/full_pipeline_stability_20x3/prepare_manifest.py
python test/experiments/full_pipeline_stability_20x3/run_experiment.py `
  --manifest output/full_pipeline_stability_20x3_inputs/frozen_manifest.json `
  --budget-usd 0.50
python .agents/skills/evaluate-bioinformatics-agent/scripts/audit_run.py `
  --run-dir output/full_pipeline_stability_20x3_<timestamp>
```

Use `--dry-run` to validate all hashes and the budget without model or analysis calls. The runner
writes each completed trial immediately and resumes it from the same output directory. Use
`--rerun` only when every trial should be recomputed.

## Outputs

- `summary.csv`: 60 trial rows.
- `case_stability.csv`: per-case cross-repeat DEG/GSEA metrics.
- `large_experiment_report.json` / `.md`: acceptance verdict and blocking findings.
- `llm_usage.json` and `budget.json`: measured token ledger, regular estimate, and peak contingency.
- `run_status.json`, `workflow.log`, and `evidence.json`: terminal state and provenance.