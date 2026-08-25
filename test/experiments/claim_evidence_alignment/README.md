# Claim-evidence alignment experiment

Create eight annotation drafts:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe test\experiments\claim_evidence_alignment\prepare_gold.py `
  --output-dir output\claim_evidence_gold_v1\gold
```

The generated cards remain `machine_draft` and the manifest remains
`unreviewed`.  A domain reviewer must complete and approve at least six before
the scorer will run.

After three blind prediction repeats:

```powershell
.\.venv\Scripts\python.exe test\experiments\claim_evidence_alignment\score.py `
  --manifest output\claim_evidence_gold_v1\gold_manifest.json `
  --predictions-root output\claim_evidence_predictions_v1 `
  --repeats 3 `
  --output-dir output\claim_evidence_score_v1
```

Predictions are expected at
`<predictions-root>/repeat_XX/<case_id>.json`.
