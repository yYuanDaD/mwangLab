# Training candidate export v0

`test/scripts/export_training_dataset.py` reads existing batch `summary.csv`
and adjacent `workflow.log`, and reconstructs compact context from current
`data/<GSE>/<GSE>_metadata.csv`. It uses only Python's standard library and
never imports agent modules, invokes models, fetches data, or reruns analysis.

```powershell
python test/scripts/export_training_dataset.py
python test/unit/test_training_dataset_export.py
```

Default destination: `output/training_dataset_v0_candidates/`. Use
`--dataset-dir output/training_dataset_v0_candidates_2` for another export.
Relative arguments resolve from the repository root, regardless of shell CWD.
Existing destination directories are refused, including empty ones.

## Output

- `contrast_candidates.jsonl`: reconstructed inputs, every distinct candidate
  label, source rows, absolute paths and SHA-256 hashes. All records have
  `review_status=pending` and `training_ready=false`.
- `conflicts.jsonl`: the subset with different labels for identical inputs.
- `manifest.json`: actual coverage, counts, limitations, and label origins.
- `source_inventory.json`: processed/skipped summaries with reasons.
- `errors.json`: visible source-read/row errors; malformed sources are not silently accepted.

This is a review corpus, not a ready-to-train chat/messages dataset. No training
is started. The first task is **contrast selection**, not reproducing historical
`is_valid` decisions: the original heuristic proposal was not reliably captured.
Final contrast fields, model reasoning, matrix classification, status and output
paths are retained only in candidate labels/provenance, never in the input.

## Deduplication and limitations

Group by accession, organism, keyword sets and reconstructed metadata summary.
For each group, collapse repeated input/label pairs but retain every observation.
Different labels become explicit conflicts; a successful pipeline run does not
win automatically. Unknown intent is scoped to its source run, not equated with
other unknown requests. Summaries lacking a sibling workflow log are excluded;
these often aggregate batch runs and would double-count outcomes without intent.

Missing labels are not treated as verified refusal examples. Mechanical checks
flag absent columns/arms, identical arms, and fewer than three metadata samples
per arm. These checks do not establish biological correctness, pairing, absence
of confounding, or the counts matrix's actual aligned sample subset.

Metadata is the current local file, which may differ from what a historical run
saw; exported hashes prove export-time identity only. The exporter does not
recover exact LLM prompts, tool schemas, full messages or historical metadata
snapshots. It does not export SEA-CDM or sample-alignment training pairs yet.

Before SFT: recover source context, adjudicate labels/conflicts, link accessions
belonging to the same publication, and split by publication/cohort. Keep existing
blind benchmark cases out of training. No automatic split is claimed here.

## Future trajectory capture

A unified recorder should store one event stream per `run_id`: user request,
effective model input (system instructions, available tool schemas and state),
model response/tool call IDs and arguments, matched tool results, final answer,
errors/retries, model/config/code version, and referenced input/artifact hashes.
Record structured events incrementally so interrupted runs remain interpretable;
exclude secrets. Existing evidence/status files complement this stream but cannot
reconstruct messages that were never recorded.
