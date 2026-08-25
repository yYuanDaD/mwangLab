# Large-scale SEA-CDM Production Gate v1

This experiment freezes 30 GEO-backed exercise-response papers and runs the same
DeepSeek staged SEA-CDM workflow three times per target accession.

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe test\experiments\seacdm_production_gate\prepare_manifest.py `
  --output-dir output\seacdm_production_gate_v1_inputs

.\.venv\Scripts\python.exe test\experiments\seacdm_production_gate\run_experiment.py `
  --manifest output\seacdm_production_gate_v1_inputs\frozen_manifest.json `
  --output-dir output\seacdm_production_gate_v1_run `
  --dry-run

# One paid call before the frozen full run:
.\.venv\Scripts\python.exe test\experiments\seacdm_production_gate\run_experiment.py `
  --manifest output\seacdm_production_gate_v1_inputs\frozen_manifest.json `
  --output-dir output\seacdm_production_gate_v1_run `
  --max-runs 1

# Resume and finish all remaining runs under the same USD 4.50 cap:
.\.venv\Scripts\python.exe test\experiments\seacdm_production_gate\run_experiment.py `
  --manifest output\seacdm_production_gate_v1_inputs\frozen_manifest.json `
  --output-dir output\seacdm_production_gate_v1_run
```

The runner is resumable and refuses a changed manifest. Residual failures are written to
the fallback queue in `production_gate_report.json`; Opus is not called during the
DeepSeek phase.

