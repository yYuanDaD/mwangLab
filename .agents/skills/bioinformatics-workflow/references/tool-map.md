# Tool map

Use the smallest tool surface that answers the request. This is an inventory, not a list to execute.

| Workflow stage | Modules |
|---|---|
| Native runtime: native mode, evidence helpers, run layout | `tools/native.py`, `tools/decision_contract.py` |
| GEO search and download | `tools/geo_tools.py` |
| Sample alignment | `tools.native.align_to_metadata` (exact only); `tools/sample_align.py` is used inside executors |
| Design and method gates | `tools/analysis_policy.py`, `tools/multifactor_design.py` |
| Raw-count preprocessing and QC | `tools/preprocess_tools.py`, `tools/stats_tools.py` |
| Two-arm differential analysis | `tools/deseq2_tools.py`, `tools/edger_tools.py`, `tools/limma_voom_tools.py`, `tools/limma_tools.py` |
| Multi-level, factorial, paired-change limma | `tools/multigroup_tools.py` |
| Enrichment | `tools/enrichment_tools.py` |
| Evidence and run status | `tools/evidence.py`, `tools/run_status.py` |

Load modality-specific modules only when needed:

| Modality | Modules |
|---|---|
| Single cell | `scrna_tools.py` (donor-level pseudobulk, `paired=True` for donor blocking) |
| Proteomics | `proteomics_tools.py` (PRIDE download, peptide-to-protein roll-up, preprocessing) |
| Methylation | `methylation_tools.py` |
| SEA-CDM extraction | `seacdm_tools.py`, `sea_cdm_schema.py`, `metadata_structural.py` |

These modules belong to the external-agent backend; use them only when the user asks for that backend: `main.py`, `tools/batch_tools.run_batch_geo_pipeline`, `tools/llm_helpers.py`, `tools/model_factory.py`, `tools/guards.py`, `tools/tool_router.py`, `tools/agent_state.py`, `tools/runtime_skills.py`.

## Skill copies

The source of truth is `agent_skills/bioinformatics-workflow/`, which is also the LangChain agent's runtime skill folder. `scripts/sync_skills.py` mirrors it to `.agents/skills/` (Codex) and `.claude/skills/` (Claude Code). Never edit the mirrors directly.
