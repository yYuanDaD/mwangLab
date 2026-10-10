# Setup on a new machine

The skill drives code in the mwangLab repository. A machine needs a clone of the repository, a Python environment with its requirements, and the skill installed where the agent looks for skills.

## 1. Repository and Python environment

Python 3.12 or newer is recommended (3.10 is the minimum for the native runtime).

macOS / Linux:

```bash
git clone https://github.com/yYuanDaD/mwangLab.git
cd mwangLab
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
git clone https://github.com/yYuanDaD/mwangLab.git
cd mwangLab
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONIOENCODING = "utf-8"   # some tools print non-ASCII status text
```

Optional:
- R with the `limma` package on `PATH`, only for limma-voom.
- Network access, only for GEO download, Europe PMC, MSigDB, Enrichr, and MyGene.

No API key is needed for native skill runs. `.env` keys are used only by the external-agent backend (`main.py`).

## 2. Install the skill

The repository carries ready-to-use copies:

| Agent | Project install (already in the clone) | User-level install |
|---|---|---|
| Codex | `.agents/skills/bioinformatics-workflow/` | `python scripts/sync_skills.py --install-user codex` copies to `~/.agents/skills/` |
| Claude Code | `.claude/skills/bioinformatics-workflow/` | `python scripts/sync_skills.py --install-user claude` copies to `~/.claude/skills/` |

Both agents discover the project copy when started inside the repository. Restart the agent, or reload its skills, after installing.

A user-level install still needs the repository. The skill scripts find it in this order:
1. the `MWANGLAB_ROOT` environment variable;
2. the current directory and its parents;
3. the folders above the script.

The source of truth is `agent_skills/bioinformatics-workflow/`. After editing it, run `python scripts/sync_skills.py` to refresh both project copies. `python scripts/sync_skills.py --check` fails when the copies have drifted; the unit tests run this check.

## 3. Check the environment

```bash
python .agents/skills/bioinformatics-workflow/scripts/preflight.py --out output/preflight.json
```

The report lists every capability: `native_runtime`, `deseq2`, `limma_two_group`, `limma_multigroup`, `edger`, `limma_voom`, `preprocess_and_qc`, `gsea_and_ora`, `geo_download`, and `single_cell_pseudobulk`. For each one it gives the missing packages or import errors, and it confirms that the external-LLM block works.

Exit code 1 means the native runtime cannot load. Fix that before running a study.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `mwangLab repository not found` | Start the agent inside the clone, or set `MWANGLAB_ROOT` |
| `ModuleNotFoundError` from a repository tool | Activate the environment and run `python -m pip install -r requirements.txt` |
| `UnicodeEncodeError` on Windows | Set `PYTHONIOENCODING=utf-8` |
| limma-voom unavailable | Install R and the `limma` package, or use DESeq2 or edgeR for raw counts |
| `NativeToolError: ... tried to call an external LLM` | A tool needed an input you had not resolved (usually sample IDs). Align with `native.align_to_metadata` first |
