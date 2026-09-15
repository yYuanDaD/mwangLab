# mwangLab Bioinformatics Agent

An agent-assisted bioinformatics workflow for GEO studies and related omics data. It combines LangChain/LangGraph with Python analysis tools and supports interactive requests and reproducible batch runs.

## What it does

- Finds and downloads GEO studies and supplementary files.
- Runs preprocessing, QC, PCA, sample correlation, differential analysis, and pathway analysis.
- Uses DESeq2 for raw counts and limma for log-scale expression, FPKM/TPM, and proteomics matrices.
- Supports bulk RNA-seq, scRNA-seq pseudobulk, DNA methylation, and matrix-based proteomics workflows.
- Extracts paper and experiment metadata into SEA-CDM-style tables with source and artifact provenance.
- Provides paper-first cohort analysis, contrast validation, sample-alignment fallback, and repeat/subset stability checks.
- Records run status, failures, decisions, evidence, and output paths for later review.

The agent can use Claude Sonnet or DeepSeek V4 through the Anthropic-compatible client. Tool routing and per-tool call limits are enforced in Python.

## Quick start

The project is tested with Python 3.12+ and a local virtual environment.

```powershell
$env:BIOAGENT_LLM_PROVIDER = "deepseek"   # or "anthropic"
$env:DEEPSEEK_API_KEY = "..."             # or CLAUDE_API_KEY
python main.py
```

Copy `.env.example` to `.env` and set the provider and API key instead of exporting them in the shell. GEO, Europe PMC, Enrichr, MSigDB, and MyGene requests require network access.

## Examples

```powershell
python test/unit/test.py
python test/unit/test_seacdm.py
python test/smoke/smoke_test_new_tools.py
python test/scripts/probe_model_compatibility.py --provider deepseek
```

Results are written under `output/`. GEO downloads are stored under `data/`. Batch runs create a `cohort_<label>` directory containing a summary table, workflow log, failure log, evidence bundle, and per-study artifacts.

## Project layout

```text
main.py                 CLI entry point
tools/                  GEO, statistics, enrichment, paper, and evidence tools
data/                   downloaded and cached inputs
output/                 analysis artifacts and run status
test/                   unit, smoke, and evaluation tests
agent_skills/           optional runtime workflow skills
```

See [AGENTS.md](AGENTS.md) for the detailed architecture and development notes.

## Scope and limitations

The pipeline requires a usable expression or quantitative matrix and metadata with enough information to define the comparison. FPKM/TPM-only studies cannot be analyzed with DESeq2. Complex multifactor designs and paper-wide extraction still require explicit review.

## License

No license has been added yet.
