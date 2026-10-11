# Setup on a new machine

The skill drives code in the mwangLab repository. A machine needs three things:
- a clone of the repository;
- a Python environment with its requirements;
- the skill installed where the agent looks for skills.

These steps work on Windows, macOS, and Linux, with Codex or Claude Code.

## 1. Repository and Python environment

Python 3.12 or newer is recommended; 3.10 is the minimum for the native runtime.

`requirements-skill.txt` installs what native skill sessions use. `requirements.txt` adds the LangChain packages that the external-agent backend (`main.py`) needs. Install one or both.

macOS / Linux:

```bash
git clone https://github.com/yYuanDaD/mwangLab.git
cd mwangLab
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-skill.txt
```

Windows (PowerShell):

```powershell
git clone https://github.com/yYuanDaD/mwangLab.git
cd mwangLab
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-skill.txt
```

Optional:
- **R with the `limma` package**, only for limma-voom. If `Rscript` is not on `PATH`, set `BIOAGENT_RSCRIPT` to its full path.
- **Network access**, only for GEO download, Europe PMC paper fetch, PRIDE, MSigDB, Enrichr, and MyGene. Local files need none.

No API key is needed for native skill runs. `.env` keys are used only by the external-agent backend.

## 2. Install the skill

The repository carries ready-to-use copies of the skill:

| Agent | Project install (already in the clone) | User-level install |
|---|---|---|
| Codex | `.agents/skills/bioinformatics-workflow/` | `python scripts/sync_skills.py --install-user codex` copies to `~/.agents/skills/` |
| Claude Code | `.claude/skills/bioinformatics-workflow/` | `python scripts/sync_skills.py --install-user claude` copies to `~/.claude/skills/` |

Both agents discover the project copy when they start inside the repository. Restart the agent after installing; in Claude Code, `/reload-skills` also works.

Invoke the skill:
- **Codex:** mention `$bioinformatics-workflow`, or describe the task and let Codex select it.
- **Claude Code:** type `/bioinformatics-workflow`, or describe the task.

Platform notes:

- **Codex sandbox and network.** The default `workspace-write` sandbox has no network access. For runs that download from GEO or call enrichment services, add this to `~/.codex/config.toml`:

  ```toml
  [sandbox_workspace_write]
  network_access = true
  ```

  For a single run, use `codex -c 'sandbox_workspace_write.network_access=true'` instead. Runs on local files work without network.

- **Claude Code permissions.** Claude Code asks before running shell commands. To pre-approve the skill's Python commands, add `"Bash(python *)"` to `permissions.allow` in `.claude/settings.local.json`.

A user-level install still needs the repository. The skill scripts find it in this order:
1. the `MWANGLAB_ROOT` environment variable;
2. the current directory and its parents;
3. the folders above the script.

The source of truth is `agent_skills/bioinformatics-workflow/`. After editing it:
- run `python scripts/sync_skills.py` to refresh both project copies;
- `python scripts/sync_skills.py --check` fails when the copies have drifted, and the unit tests run this check.

## 3. Check the environment

```bash
python .agents/skills/bioinformatics-workflow/scripts/preflight.py --out output/preflight.json --network
```

For each capability, the report gives the missing packages or import errors:
- `native_runtime`
- `deseq2`, `limma_two_group`, `limma_multigroup`, `edger`, `limma_voom`
- `preprocess_and_qc`, `methylation`, `proteomics_preprocess`
- `single_cell_aggregation`, `single_cell_de_tool`
- `gsea_and_ora`, `geo_download`, `paper_fetch`

It also reports:
- installed package versions;
- whether the external-LLM block works;
- with `--network`, whether the hosts each capability needs are reachable.

Exit code 1 means the native runtime cannot load. Fix that before running a study.

## 4. Self-test

```bash
python scripts/skill_selftest.py            # add --network to include GSEA and ORA
```

The self-test runs a small native run on synthetic data with planted effects through each route:
- DESeq2 with subject blocking;
- limma on log2 FPKM;
- one multilevel limma model;
- methylation beta-to-M;
- label-free proteomics;
- paired single-cell pseudobulk.

For each route it checks that the planted genes are recovered with the right sign. It then validates every decision record and audits the run.

Routes whose packages are missing show `SKIP` with the reason. Add `--require-all` to make a skip count as a failure, for example when you check a machine that should run everything. The report is written to `output/skill_selftest_<time>/selftest_report.json`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `mwangLab repository not found` | Start the agent inside the clone, or set `MWANGLAB_ROOT` |
| `NativeToolError: cannot import ...` | Activate the environment and run `python -m pip install -r requirements-skill.txt` |
| `UnicodeEncodeError` on Windows outside a native run | Set `PYTHONIOENCODING=utf-8`. `native.enable_native_mode()` already does this inside a run |
| limma-voom unavailable | Install R and the `limma` package, or set `BIOAGENT_RSCRIPT`; or use DESeq2 or edgeR for raw counts |
| GEO download or enrichment fails in Codex | Enable network for the sandbox (see above) |
| `NativeToolError: ... tried to call an external LLM` | A tool needed an input you had not resolved, usually sample IDs. Align with `native.align_to_metadata` first |
