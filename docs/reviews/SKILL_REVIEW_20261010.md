# bioinformatics-workflow skill review (2026-10-10)

Scope: `agent_skills/bioinformatics-workflow` at `0c90ba1`, its references and validator, the tools it names, and its companion `evaluate-bioinformatics-agent` skill. Goal: one skill that drives the same agent workflow in Codex and Claude Code.

## Verdict

The decision policy is strong. Two fresh Claude Code sessions, given only the skill and five frozen cases with traps, made every scored decision correctly (10/10 case-runs, 0 external LLM calls, no DE claims from an invalid plan).

It is not yet a portable workflow. Both sessions succeeded only after writing 1,232 and 1,375 lines of their own glue code (import stubs, an external-LLM guard, record writers, design checks). They produced two different output layouts. The project's own auditor scored both runs `insufficient_evidence` (coverage 4.3% and 31.5%). The contract validator accepted records containing four injected scientific errors. The skill describes the policy well, but the repository does not give an agent a native runtime to carry it out reproducibly.

## How it was tested

- Five synthetic GEO-like cases: `test/experiments/skill_forward_test_20261010/`. Answer keys stayed outside the tested workspaces.
- Two independent sessions, each in a clean checkout, with the skill copied to `.claude/skills/bioinformatics-workflow/`. Each was asked to analyze the exercise effect "as intended by the paper", with no hints about the traps.
- Environment: no network. pydeseq2, patsy, inmoose and langchain could not be installed because PyPI is blocked by the sandbox egress policy. Model fitting therefore failed at import, and the sessions recorded that as execution failure. **This test covers decisions, not numerical execution.**
- Scoring: `score_run.py` (layout-independent). Negative control: a copy of a passing run with four injected errors.

| Case | Trap | Session A | Session B |
|---|---|---|---|
| case_01 | pre/post in the same 8 subjects; matrix columns are shuffled titles | DESeq2 `~ subject + time`, 16/16 title-to-GSM correct, no FC cutoff | same |
| case_02 | sequencing run identical to exercise arm; paper silent | stop at covariance (`manual_review`) | stop at covariance (`refused`) |
| case_03 | only FPKM deposited; paper used DESeq2 | DESeq2 refused; limma on log2(FPKM+1) as a declared deviation | same |
| case_04 | control + 0/6/24 h, different animals; FC > 1.5 | one 4-level limma model, 3 contrasts, no blocking, abs(log2FC) > 0.585 | same |
| case_05 | genotype-only RNA-seq | refused: no exercise contrast | same |

| Check | Result |
|---|---|
| Scorer, sessions A and B | 5/5 and 5/5 |
| Scorer, negative control | 4/4 injected errors caught |
| `validate_decision_contract.py` on the negative control | 4/4 reported `VALID` |
| `audit_run.py` on sessions A and B | `insufficient_evidence`; coverage 4.3% and 31.5% |
| External LLM calls | 0 and 0 (each session wrote its own guard) |

Codex was not available in this sandbox. Codex compatibility below is a static review against the Codex skill documentation. Codex behavior itself was covered by the earlier forward tests listed in `docs/CLAUDE_HANDOFF_20261009.md`.

## Findings

### P0: required for one workflow on both platforms

**1. The skill is not where either platform looks for it.**
- Claude Code discovers project skills in `.claude/skills/<name>/SKILL.md`.
- Codex scans `.agents/skills/` from the working directory up to the repository root, plus `$HOME/.agents/skills`.
- The skill lives in `agent_skills/`, which neither platform scans. `.gitignore` excludes `.claude/` and every `.agents/skills/*` entry except the evaluator.
- `tool-map.md:28` says the installed copy is under `~/.codex/skills`, which the current Codex documentation does not list.
- Both platforms follow the Agent Skills standard and accept `name` and `description` frontmatter, so the files themselves are compatible.

Recommendation:
- Make `.agents/skills/bioinformatics-workflow/` the canonical copy.
- Add `scripts/sync_skills.py` to mirror it to `.claude/skills/`, and a unit test that fails when the copies differ. Both platforms follow symlinks, but symlinks in Git checkouts on Windows are unreliable.

**2. There is no native runtime, so every session rebuilds one.**
- `tools/__init__.py` imports `geo_tools` (GEOparse) and `seacdm_tools`. As a result, even pure-pandas modules such as `analysis_policy`, `sample_align` and `evidence` cannot be imported without the full stack. Both sessions had to register a stub package.
- Every DE and QC module imports `langchain_core` at the top (`deseq2_tools.py:7`, `limma_tools.py:5`, `stats_tools.py:8`, `preprocess_tools.py:5`, `edger_tools.py:27`, `limma_voom_tools.py:23`).
- The executors are LangChain `@tool` objects. They return strings such as `FATAL ERROR` and `POLICY BLOCKED` instead of raising, and the skill does not document how to call them.
- `native-codex.md:21` asks for a fail-closed guard around external LLM entry points but provides none. Each session wrote a different import hook.

Recommendation:
- Make `tools/__init__.py` lazy.
- Add plain-function entry points that raise on policy violations (for example `tools/native.py` wrapping alignment, matrix profiling, design validation, DESeq2, limma and the multigroup executor).
- Honor `BIOAGENT_DISABLE_EXTERNAL_LLM=1` in `llm_helpers._get_validation_llm` and `align_samples_with_llm_fallback`, recording attempted calls.
- Add `scripts/skill_preflight.py`, which reports which gates are executable in the current environment.
- Document the calling convention in one reference file.

**3. The contract validator checks structure, not the invariants that matter.** It accepted four records with scientific errors:
- case_01 with blocking removed;
- case_02 proceeding despite the confound, with execution `completed`;
- case_03 with DESeq2 on FPKM;
- case_04 with an invented abs(log2FC) > 1.

It also accepts a `covariance` record with an empty `final` and evidence given as a bare string. These are exactly the "p-value ran but the method was wrong" cases from the meeting.

Recommendation:
- Require stage-specific `final` fields: `matrix_type`, `method`, `status`, `blocking_terms`, `n_aligned`/`coverage`, and contrasts.
- Require each evidence item to carry an `id` and a `kind`.
- Add case-level invariants:
  - no `completed` execution if any gate is `unresolved`, `manual_review` or `refused`;
  - covariance `required` must have blocking terms that appear in the executed formula;
  - a raw-count method requires `matrix_type` raw counts;
  - `effect_cutoff` must equal the paper's value, or `audit_threshold` must be labelled.
- The scorer here shows these checks can be deterministic.

**4. There is no shared output layout, so runs cannot be audited.**
- Session A wrote `decisions/01..09_*.json`; session B wrote one `decision_records.json`.
- The skill names only the four paper-reconstruction files (`paper-reconstruction.md:73-78`).
- `audit_run.py` expects batch-pipeline files (`summary.csv`, `workflow.log`, root `run_status.json`), so it cannot assess either run.

Recommendation: define one run layout in the skill and teach `audit_run.py` to read it:
- `run_status.json`
- `summary.csv`
- per case: `decisions.json`, `evidence.json` and the four paper files

### P1: safety gaps in the execution layer the skill relies on

**5. Matrix-method gates are missing on two paths.**
- `multigroup_tools._read_matrix` (line 65) never calls `enforce_method_matrix_compatibility`. A native caller can fit limma on raw counts or linear FPKM, and the batch path avoids this only because it substitutes a log-CPM sidecar first.
- `enforce_method_matrix_compatibility(method="limma")` rejects only raw-count-like matrices; session A confirmed that linear FPKM passes.
- `_paired_change` (line 130) silently skips subjects without exactly one baseline and one follow-up sample (line 147) and does not report them. The skill requires the subject mapping to be "complete and unique".

**6. Executors report a threshold the skill forbids.**
- `deseq2_tools.py:197` and `limma_tools.py:189` print summaries at `padj < 0.05, |log2FC| > 1`.
- `multigroup_tools` counts at `padj < 0.05` only.
- No executor takes a threshold argument.

The skill should say explicitly: apply `paper_threshold` to the full results table and ignore tool `n_deg` summaries. Better still, pass the threshold in.

**7. Executors call an external LLM silently.** `deseq2_tools`, `limma_tools`, `edger_tools`, `limma_voom_tools`, `stats_tools` and `batch_tools` all call `align_samples_with_llm_fallback` when fewer than half the IDs match exactly. Both sessions avoided this only by writing exact-ID aligned files first. Finding 2's switch would close this.

**8. The decision contract does not match the gates.**
- No `stage` exists for gate 2 (file and accession ownership) or for the final study record.
- Rank and residual df are required in `method` (gate 6), but blocking terms are only decided in `covariance` (gate 7).
- There is no field for an execution error on a valid decision.
- A completely aliased confound may be `manual_review` or `refused` (`decision-contract.md:52`): session A chose one and session B the other.
- A deviation route (case_03) has no `threshold_source` value. "Repository default" threshold is undefined.
- "Small study" has no size rule, and the multiplicity family for multi-level contrasts is ambiguous.

**9. The references are behind the code.**
- `tools/multigroup_tools.py`, the only executor that fits a k-level model, is missing from SKILL.md and `tool-map.md`.
- Its plan schema (`analysis_type`, `formula`, `contrasts[{name, coefficients}]`, `subject_column`, `time_column`, `baseline_level`, `followup_levels`, `derived_columns`) is documented only in `main.py`'s system prompt.
- `multigroup-longitudinal.md:23` and `multifactor-design.md:38` still say no such executor exists.
- `multifactor-design.md:3` routes plans through `run_batch_geo_pipeline`, which `native-codex.md:16` forbids in native mode.
- SKILL.md gate 4 (line 25) asks for "structured LLM review", which in native mode means the forbidden external validator.

### P2: wording and hygiene

10. **Platform-specific wording.** "Codex" appears 13 times (for example SKILL.md:10, "The current Codex conversation is the scientific decision-maker"). Use "the agent session running this skill (Codex or Claude Code)", and rename `native-codex.md` to `native-execution.md`.
11. **Ambiguous validator path.** SKILL.md:18 says to run `scripts/validate_decision_contract.py`, but a session at the repository root resolves that to the repo's own `scripts/`, where the file does not exist. Make the path explicitly skill-relative (`${CLAUDE_SKILL_DIR}/scripts/...` in Claude Code).
12. **Project context files don't mention the skill.** Neither `CLAUDE.md` (read by Claude Code) nor `AGENTS.md` (read by Codex) says the skill exists. `CLAUDE.md` is also stale: it says "No requirements.txt" although one exists, and it gives `recursion_limit=25` while `main.py` uses 50.
13. **Overlapping second skill.** `agent_skills/paper-workflow-safety/` overlaps the main skill and is neither installed nor referenced. Merge it into a reference file.
14. **Windows-only evaluator command.** `evaluate-bioinformatics-agent/SKILL.md:18` uses a Windows-only command (`.\.venv\Scripts\python.exe`). Give a platform-neutral form.

## What to keep

- Paper-first reconstruction.
- Exact threshold semantics.
- The separation of decision status from execution status.
- The covariance gate.
- Explicit refusal paths.

Both sessions applied all of these correctly on every trap, and both recorded the case_03 paper route as blocked rather than calling the limma result a reproduction. The fixes above are about making that behavior reproducible, auditable and executable, not about changing the policy.

## Proposed layout

```text
.agents/skills/bioinformatics-workflow/   canonical (Codex)
  SKILL.md                                platform-neutral wording
  agents/openai.yaml
  references/native-execution.md          calling convention, guard, run layout
  references/...                          updated to the current executors
  scripts/validate_decision_contract.py   stage fields + case invariants
  scripts/preflight.py
.claude/skills/bioinformatics-workflow/   generated mirror (Claude Code)
tools/native.py                           plain functions, raise on violation
scripts/sync_skills.py                    mirror + drift check
CLAUDE.md, AGENTS.md                      one line pointing to the skill
```

## Sources

- Claude Code skills: https://code.claude.com/docs/en/skills
- Codex skills: https://learn.chatgpt.com/docs/build-skills (redirected from https://developers.openai.com/codex/skills)
- Agent Skills standard: https://agentskills.io
