# Workspace layout after cleanup

The repository is split into four practical layers:

- `tools/`: production and evaluation code. The first Codex skill uses the core GEO, alignment, matrix-policy, differential-analysis, QC, enrichment, guard, routing, evidence, and runtime modules.
- `agent_skills/`: portable project skills. `agent_skills/bioinformatics-workflow/` is the source copy of the Codex workflow skill.
- `test/`: unit, smoke, validation, and historical experiment code. These remain available for regression and benchmark construction, but are not part of the skill's default tool surface.
- `data/` and `output/`: empty runtime roots recreated after cleanup. Generated runs should stay here and remain outside the skill package.

The previous runtime data and outputs were moved to the local ignored archive described by `archive/MANIFEST_20260930.json`. The archive contains the downloaded GEO data, generated results, benchmark input snapshot, the historical `0623` deliverables, and the old large reference files. It is intentionally ignored by Git so it cannot be uploaded as part of the Codex skill.

The installed user-level copy is at `C:\Users\34198\.codex\skills\bioinformatics-workflow`. Keep the project copy and installed copy synchronized when the skill changes.
