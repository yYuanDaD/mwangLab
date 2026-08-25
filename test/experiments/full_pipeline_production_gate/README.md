# Full RNA-seq Pipeline Production Gate

This experiment validates the cached-input scientific core of the complete bulk RNA-seq
workflow before the larger 20-study x 3-repeat production gate.

The six-case preflight covers:

- raw integer counts routed to DESeq2;
- linear FPKM routed through log2(x+1) to limma;
- an already log-scale matrix routed directly to limma;
- prefix-collision sample names (`Sample_1` versus `Sample_10`);
- a multi-level treatment producing two control-versus-treatment contrasts;
- semantic sample-name abbreviations that require the LLM alignment fallback.

GEO acquisition is intentionally frozen to local cached files. Main-path GSEA remains live,
so the preflight also exercises MSigDB/MyGene integration. The later production gate must add
uncached GEO acquisition and three repeats per case.

## Run

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python test/experiments/full_pipeline_production_gate/prepare_manifest.py
python test/experiments/full_pipeline_production_gate/run_experiment.py `
  --manifest output/full_pipeline_production_gate_inputs/frozen_preflight_manifest.json
python .agents/skills/evaluate-bioinformatics-agent/scripts/audit_run.py `
  --run-dir output/full_pipeline_preflight_<timestamp>
```

Use `--dry-run` on either experiment script to validate inputs without model, network, or DA
calls. `run_experiment.py` resumes completed case-result JSON files in the same output directory;
pass `--rerun` to force recomputation.

## Cost and provenance

Every structured LLM hook retains the provider response usage. The root experiment writes
`llm_usage.json`, while each cohort writes `llm_calls` and `estimated_cost_usd` to
`run_status.json`. DeepSeek V4 estimates use the public regular-time cache-hit, cache-miss, and
output token rates; budget planning should retain a 2x contingency for the announced peak-price
policy. Semantic sample alignment is cached only within one independent batch run, avoiding
repeated QC/design calls while preserving independent live calls across experimental repeats.

Decision-log artifact paths are canonicalized to existing files and stored with SHA-256 hashes.
The independent audit must report zero missing artifacts and zero hash mismatches before the run
is accepted.

