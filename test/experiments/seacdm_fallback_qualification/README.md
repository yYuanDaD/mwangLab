# SEA-CDM Opus 5 fallback qualification

This bounded experiment reuses the frozen `exercise` A/B inputs and permits exactly two paid
`claude-opus-5` structured-output calls. It tests one known DeepSeek design-stage failure, one
complex-design shadow case, and one zero-cost negative routing control.

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe test\experiments\seacdm_fallback_qualification\run.py `
  --source-experiment output\seacdm_exercise10_ab_20260818_1730 `
  --output-dir output\seacdm_fallback_qualification_<timestamp>
```

The independent concept rubric is stored in the runner and is not included in model prompts.
