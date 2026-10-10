# Core tool map

Use the smallest tool surface that satisfies the request.

This is an implementation inventory, not a list to execute blindly. Native Codex execution uses deterministic readers, validators, and calculation tools. `llm_helpers`, `model_factory`, `main.build_agent`, and the automatic batch runner belong to the external-agent backend; consult `native-codex.md` before using any tool that may invoke them. Preserve these backend modules in the repository without treating them as required Codex decision tools.

| Workflow stage | Core tools/modules |
|---|---|
| GEO search/download | `tools/geo_tools.py` |
| Candidate matrix discovery and batch orchestration | `tools/batch_tools.py` |
| Sample alignment | `tools/sample_align.py`, `tools/llm_helpers.py` |
| Design and method gates | `tools/analysis_policy.py`, `tools/multifactor_design.py`, `tools/batch_tools.py`, `tools/llm_helpers.py` |
| Raw-count preprocessing and QC | `tools/preprocess_tools.py`, `tools/stats_tools.py` |
| Differential analysis | `tools/deseq2_tools.py`, `tools/edger_tools.py`, `tools/limma_voom_tools.py`, `tools/limma_tools.py` |
| Enrichment | `tools/enrichment_tools.py` |
| Evidence and run status | `tools/evidence.py`, `tools/run_status.py`, `tools/guards.py` |
| Routing and model configuration | `tools/tool_router.py`, `tools/model_factory.py`, `tools/agent_state.py` |
| Paper-driven tests | `tools/paper_tools.py`, `tools/evaluation_tools.py` |

Load modality-specific tools only when required:

- SEA-CDM: `seacdm_tools.py`, `sea_cdm_schema.py`, `metadata_structural.py`
- scRNA-seq: `scrna_tools.py`
- proteomics: `proteomics_tools.py`
- methylation: `methylation_tools.py`
- cohort/result graph extensions: `cohort_tools.py`, `agreement_tools.py`, `pathway_chain_tools.py`, `study_split.py`, `kg_export_tools.py`

The project source of this map is `agent_skills/bioinformatics-workflow/`; the installed Codex copy is under the user's `.codex/skills` directory. Keep the tool files in the repository as the single implementation source.
