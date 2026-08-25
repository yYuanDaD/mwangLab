# Few-shot paper case A/B experiment

Purpose: measure whether one curated paper-to-workflow example improves structured extraction and
workflow planning on the **same unseen target paper**.

Controlled variables:

- Model: `claude-sonnet-4-6`
- Temperature: `0`
- Target: PMC10776189 (`data/papers/e75202...txt`)
- Output schema: `PaperWorkflowExtraction`
- Baseline instructions: identical
- Only independent variable: condition B includes `example_case.json`; condition A does not

The target is deliberately different from the example. The example is an exercise mouse RNA-seq
study (GSE279359); the target is a human AML multi-dataset bulk + scRNA study (GSE71014,
GSE116256). This tests generalization and makes copied example identifiers measurable.

Run:

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe test\experiments\fewshot_case_ab\run_experiment.py
```

Outputs land under `output/fewshot_case_ab_<timestamp>/`:

- `condition_a_no_example.json`
- `condition_b_with_example.json`
- `scores.json`
- `comparison.md`
- `run_status.json`

Primary metric is the score delta `B - A`. Component metrics cover accession F1, modalities,
organism, groups, reported methods, workflow safety, evidence grounding, and copied/hallucinated
accessions. One run is a smoke experiment, not a statistical conclusion; use `--repeats 3` or more
for a more reliable estimate.

If scoring logic changes, rescore an existing run without another model call:

```powershell
.\.venv\Scripts\python.exe test\experiments\fewshot_case_ab\rescore_existing.py output\fewshot_case_ab_<timestamp>
```

To evaluate the repository runtime skill instead of injecting the legacy example directly:

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe test\experiments\fewshot_case_ab\run_experiment.py `
  --condition-b runtime-skill --skill-name paper-workflow-safety --repeats 3
```
