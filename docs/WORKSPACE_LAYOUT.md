# Workspace layout after cleanup

The repository is split into four practical layers:

- `tools/`: production and evaluation code. The workflow skill uses the native runtime (`tools/native.py`, `tools/decision_contract.py`) plus the core GEO, alignment, matrix-policy, differential-analysis, QC, enrichment, and evidence modules.
- `agent_skills/`: project skills and the LangChain agent's runtime skill folder. `agent_skills/bioinformatics-workflow/` is the source of truth for the workflow skill; `scripts/sync_skills.py` mirrors it to `.agents/skills/` (Codex) and `.claude/skills/` (Claude Code).
- `test/`: unit, smoke, validation, and historical experiment code. These remain available for regression and benchmark construction, but are not part of the skill's default tool surface.
- `data/` and `output/`: empty runtime roots recreated after cleanup. Generated runs should stay here and remain outside the skill package.

The previous runtime data and outputs were moved to the local ignored archive described by `archive/MANIFEST_20260930.json`. The archive contains the downloaded GEO data, generated results, benchmark input snapshot, the historical `0623` deliverables, and the old large reference files. It is intentionally ignored by Git so it cannot be uploaded as part of a skill.

Project-level copies are committed and discovered automatically. For a user-level install run `python scripts/sync_skills.py --install-user codex|claude|all` and rerun it after the skill changes. See `agent_skills/bioinformatics-workflow/references/setup.md`.
