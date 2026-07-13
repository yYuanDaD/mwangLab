# Project Structure Audit

Date: 2026-06-29

This audit is intentionally non-destructive. It lists cleanup and reorganization
candidates, but no files should be deleted or moved until the owner confirms the
scope.

## Cleanup Executed

After owner approval on 2026-06-29, the following high-confidence generated/cache
artifacts were removed:

| Removed | Approx. reclaimed |
| --- | ---: |
| `__pycache__/`, `tools/__pycache__/`, `test/__pycache__/` | ~0.6 MB |
| `data/GSE123879/` | ~15.1 GB |
| `data/GSE270703/_unpacked/` | ~136 MB |
| `data/GSE316347/_unpacked/` | ~70 MB |
| `data/GSE283691/_unpacked/` | ~14 MB |
| `data/GSE302944/_unpacked/` | ~10 MB |
| `data/GSE297318/_unpacked/` | ~4 MB |
| `output/archive/cohort_history.tar.gz` | ~165 MB |
| Empty generated directories under `data/`, `output/`, and `test/output/` | negligible |

Post-cleanup size snapshot:

| Path | Before | After |
| --- | ---: | ---: |
| `data/` | ~16.1 GB | ~1.13 GB |
| `output/` | ~297 MB | ~132 MB |
| `test/` | ~77 MB | ~77 MB |
| `tools/` | ~1.06 MB including pycache | ~0.49 MB |

`test/output/` was intentionally left mostly intact because report-generation
scripts directly reference several stored validation outputs.

## Test Tree Reorganization Executed

After owner approval on 2026-06-29, Python scripts directly under `test/` were
moved into second-level categories:

| New path | Contents |
| --- | --- |
| `test/unit/` | Offline unit/regression tests named `test_*.py` plus the legacy `test.py`. |
| `test/smoke/` | Smoke tests named `smoke_test_*.py`. |
| `test/validation/` | Validation and verification scripts named `validate_*.py` / `verify_*.py`. |
| `test/scripts/` | One-off run, probe, cohort, robustness, and scan scripts. |
| `test/reports/` | Report and figure generation scripts. |
| `test/determinism/` | SEA-CDM determinism and ROUGE-L audit scripts. |

Reference updates performed:

- Updated active docs and script docstrings from `test/<script>.py` to
  `test/<category>/<script>.py`.
- Added `test/__init__.py` so test helpers can be imported as a package when
  needed.
- Rechecked moved scripts for hardcoded root assumptions. Scripts now compute
  project root as two levels above their category directory, preserving direct
  execution such as `python test/unit/test_classify_matrix.py`.

Verification after move:

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m py_compile <all moved test scripts>
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_cost_timing.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/determinism/determinism_analyze.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_classify_matrix.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_enrichment_loader.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_metadata_structural.py
```

All verification commands passed. A post-move `rg` scan found no remaining active
references to the old `test/<script>.py` command paths outside generated
`test/output/`.

## Current Top-Level Shape

| Path | Role | Size | Notes |
| --- | --- | ---: | --- |
| `tools/` | Agent-callable tools and shared pipeline utilities | ~1 MB | Active code. No obvious dead module from import scan. |
| `test/` | Smoke tests, validation scripts, one-off run harnesses, generated test outputs | ~77 MB | Code is small; `test/output/` is most of the size. |
| `data/` | GEO/PRIDE/raw validation caches | ~16.1 GB | Main cleanup target. |
| `output/` | Analysis outputs and historical runs | ~297 MB | Mostly historical cohort artifacts. |
| `0623/` | Frozen deliverable snapshot | ~34 MB | Keep as release artifact unless superseded. |
| `docs/` | Design/schema docs | small | Good place for audit and structure docs. |
| `new_deg3.zip` | Exercise DEG reference archive | ~376 MB | Referenced in docs/history; derived slices are in `data/_validation/`. |

## Data Cleanup Candidates

### Highest-Impact Candidate

| Path | Size | Recommendation | Reason |
| --- | ---: | --- | --- |
| `data/GSE123879/` | ~15.1 GB | Delete or move to external archive | Contains huge `GSE123879_RAW.tar` plus `_unpacked/` bedGraph/ATAC-style files. This is outside the RNA-seq expression-matrix happy path and dominates disk usage. |

If keeping the study, do not keep both forms:

| Redundant Pair | Reclaim |
| --- | ---: |
| `data/GSE123879/_unpacked/` only | ~7.54 GB |
| `data/GSE123879/GSE123879_RAW.tar` only | ~7.54 GB |
| whole `data/GSE123879/` | ~15.1 GB |

### General Raw-Tar Duplication

These studies keep both a `*_RAW.tar` and `_unpacked/`. The pipeline can recreate
`_unpacked/` from the tar when needed, so `_unpacked/` is usually a safe cache to
delete after downstream merged matrices are produced.

| Study | Raw tar | `_unpacked/` | Recommendation |
| --- | ---: | ---: | --- |
| `GSE123879` | 7538.91 MB | 7538.86 MB | Delete whole study or at least `_unpacked/`. |
| `GSE270703` | 136.14 MB | 136.07 MB | Delete `_unpacked/`; keep tar if reruns matter. |
| `GSE316347` | 70.20 MB | 70.18 MB | Delete `_unpacked/`; keep tar if reruns matter. |
| `GSE283691` | 13.79 MB | 13.75 MB | Delete `_unpacked/`; derived merged matrix exists. |
| `GSE302944` | 9.98 MB | 9.97 MB | Delete `_unpacked/`; derived merged matrix exists. |
| `GSE297318` | 4.51 MB | 4.49 MB | Delete `_unpacked/`; derived merged matrix exists. |

### Keep By Default

| Path | Reason |
| --- | --- |
| `data/_validation/` | Used by validation scripts and deliverable report generation. |
| `data/_validation/ref_GSE*.csv` | Small reference slices derived from `new_deg3`; useful without loading the large archive. |
| `data/papers/` | Cached paper texts for SEA-CDM extraction and determinism checks. |
| Small GSE metadata + matrix directories | Useful as local smoke-test fixtures; cheap compared with `GSE123879`. |

### Review Before Deleting

| Path | Size | Note |
| --- | ---: | --- |
| `new_deg3.zip` | ~376 MB | Historical/source DEG reference. If `data/_validation/ref_*.csv` is enough, archive externally. If validation must regenerate slices, keep. |
| `data/scrna_demo` | ~36.6 MB | Likely needed for scRNA demo. Keep if demos matter. |
| `data/PXD*` | ~29 MB total | Proteomics smoke/demo inputs. Keep if proteomics tests remain active. |

## Output Cleanup Candidates

| Path | Size | Recommendation |
| --- | ---: | --- |
| `output/archive/cohort_history.tar.gz` | ~165 MB | Keep only if historical rerun evidence matters; otherwise move outside repo. |
| `output/agentA_cohort_rerun_0622/` | ~16.5 MB | Historical run; archive/delete if superseded by `0623/` or `agentA_cohort_recon_min_0626`. |
| `output/agentA_cohort_split_live_0623/` | ~22.5 MB | Historical run; keep only if used for demo comparison. |
| `output/cohort_proof_0623/` | ~29.2 MB | Proof artifact. Keep if cited in reports; otherwise archive. |
| `output/GSE266241/` | ~15.7 MB | Single-study output; can be regenerated if source data remains. |
| `output/scrna_demo_kang/` | ~14.8 MB | Demo output. Keep if demo is current. |
| `output/_determinism_check/` | ~0.35 MB | Keep; now used for ROUGE-L determinism audit. |
| `output/deliverables/` | ~0.44 MB | Keep; polished report artifact. |

Recommended policy:

- `output/current/` or `output/runs/<run_label>/` for active runs.
- `output/deliverables/` for curated report/demo artifacts.
- `output/scratch/` for disposable experiments.
- `output/archive/` should live outside the repo/workspace if it grows.

## Test Directory Assessment

The test directory mixes four kinds of files:

| Category | Examples | Recommendation |
| --- | --- | --- |
| Unit/regression tests | `test_classify_matrix.py`, `test_cost_caches.py`, `test_metadata_structural.py` | Keep under `test/unit/` or `test/regression/`. |
| Smoke tests | `smoke_test_new_tools.py`, `smoke_test_limma.py` | Move to `test/smoke/`. |
| Live/probe/one-off scripts | `probe_one_pass_live.py`, `run_overnight_0623.py`, `run_audit8_0623.py` | Move to `test/scripts/` or `scripts/experiments/`. |
| Validation/report builders | `validate_*.py`, `gen_deliverables_report.py`, `make_req_diagrams.py` | Move to `test/validation/` or `scripts/reports/`. |

Main cleanup target in `test/` is not Python code, but generated artifacts:

| Path | Size | Recommendation |
| --- | ---: | --- |
| `test/output/smoke_test/` | ~69.6 MB | Keep only curated fixtures required by report generation; delete/regenerate the rest. |
| `test/__pycache__/` | tiny | Safe to delete. |
| `test/output/*.log` | small | Delete unless needed for audit history. |

Files that are likely historical one-offs and can be archived after confirmation:

- `run_cohort_v2.py`
- `run_cohort_v3_diabetes.py`
- `run_cohort_test2.py`
- `run_cohort_test3.py`
- `run_overnight_0623.py`
- `run_audit8_0623.py`
- `rerun_cohort_0622.py`
- `robustness_keywords_0622.py`
- `robustness_keywords2_0623.py`
- `robustness_batch_cached_0623.py`
- `scan_strata.py`
- `pick_cohort.py`

Do not delete these before deciding whether old cohort experiments need to remain
reproducible.

## Tools Directory Assessment

Import scan did not find a clearly unused `tools/*.py` module. Most modules are
referenced by `main.py`, another tool module, or tests.

Suggested second-level organization:

```text
tools/
  core/
    guards.py
    cost_timing.py
    determinism_similarity.py
  io/
    geo_tools.py
    paper_tools.py
  expression/
    preprocess_tools.py
    stats_tools.py
    sample_align.py
    deseq2_tools.py
    limma_tools.py
    edger_tools.py
    limma_voom_tools.py
    limma_voom.R
  enrichment/
    enrichment_tools.py
    enrichment_loader.py
    pathway_chain_tools.py
    agreement_tools.py
  seacdm/
    sea_cdm_schema.py
    seacdm_tools.py
    metadata_structural.py
    study_split.py
    cohort_tools.py
    batch_tools.py
  modalities/
    scrna_tools.py
    methylation_tools.py
    proteomics_tools.py
  llm/
    llm_helpers.py
```

Migration warning: moving `tools/` modules requires updating many imports in
`main.py`, `tools/*.py`, and `test/*.py`. A lower-risk first step is to keep file
locations as-is and add package-level docs or wrapper modules. Move modules only
after tests are grouped and import paths are covered by regression checks.

## Proposed Target Structure

```text
project root/
  main.py
  clean.py
  AGENTS.md
  README.md
  docs/
    SEACDM_SCHEMA.md
    PROJECT_STRUCTURE_AUDIT.md
  tools/
    ...active tool modules...
  test/
    unit/
    regression/
    smoke/
    validation/
    scripts/
    fixtures/
    output/              # gitignored/generated only
  data/
    fixtures/            # small stable local fixtures
    papers/              # cached full text
    validation/          # ref slices and validation metadata
    cache/geo/           # large downloadable GEO cache
    cache/pride/         # large downloadable PRIDE cache
  output/
    current/
    runs/
    scratch/
    deliverables/
```

## Recommended Cleanup Order

1. Delete Python caches: `__pycache__/`, `tools/__pycache__/`, `test/__pycache__/`.
2. Remove or external-archive `data/GSE123879/`.
3. Delete `_unpacked/` directories where the corresponding `*_RAW.tar` is kept.
4. Move `output/archive/cohort_history.tar.gz` outside the workspace if not needed.
5. Prune `test/output/smoke_test/` down to files explicitly referenced by report
   scripts.
6. Group `test/` scripts into second-level directories.
7. Only then consider reorganizing `tools/` into packages.
