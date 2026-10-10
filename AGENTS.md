# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

A bioinformatics AI agent built with LangChain/LangGraph that uses **DeepSeek V4 Pro** in the evaluated deployment to automate RNA-seq workflows: GEO data download → metadata inspection → preprocessing → QC/PCA/correlation → DESeq2 differential expression → GO/KEGG (ORA) + MSigDB Hallmark (GSEA) enrichment → SEA CDM (Standardized Expression Anatomy Common Data Model) extraction. **Claude Sonnet 4.6** remains the tested fallback. Also supports **keyword-driven cohort analysis**: search GEO for studies matching a keyword (e.g. "Exercise"), then batch-process the top hits with one tool call. The agent communicates in Chinese.

## Commands

```bash
# Run the agent (requires CLAUDE_API_KEY in .env)
python main.py

# Test individual tools without the LLM
python test/unit/test.py
python test/unit/test_seacdm.py
python test/smoke/smoke_test_new_tools.py        # preprocess + stats + GSEA on GSE266241
python test/scripts/probe_search_quality.py        # download + classify a few search hits
python test/scripts/probe_model_compatibility.py --provider deepseek  # live provider/tool/schema gate
python test/experiments/model_agent_ab/run_experiment.py --repeats 3  # paired Sonnet vs V4 routing A/B
python test/experiments/deepseek_seacdm_staged_ab/run_experiment.py    # DeepSeek single vs staged SEA-CDM A/B
python test/experiments/deepseek_seacdm_generalization/run_experiment.py  # routine + multifactor staged gate
python test/experiments/deepseek_seacdm_generalization/rescore_existing.py <run_dir>  # zero-call scope rescore
python test/experiments/deepseek_seacdm_blind_multicohort/run_experiment.py  # frozen unseen GSE197045/GSE198652 scope test
python test/experiments/model_e2e_ab/run_experiment.py --repeats 3    # paired cached-GEO DA A/B

# Reset workspace (wipes data/ and output/)
python clean.py
```

Test scripts include a `chdir` prelude so they work regardless of the CWD they're invoked from — they always run with the project root as CWD.

On Windows, set `PYTHONIOENCODING=utf-8` before running anything that prints emojis (the tools use them in status messages and the default GBK console encoding crashes).

## Architecture

**Agent pattern:** LangChain `create_agent` (ReAct loop) with **DeepSeek V4 Pro** selected in `.env` through its Anthropic-compatible endpoint; **Claude Sonnet 4.6** remains the fallback. `tools/model_factory.py` centralizes both paths, and its no-environment library fallback remains Anthropic. DeepSeek structured-output hooks automatically disable thinking because its thinking mode rejects the forced `tool_choice` used by `with_structured_output`, while the main ReAct agent keeps `effort=max`. The old `deepseek-chat` model previously looped on cosmetically different tool arguments; V4 Pro passed the provider gate, 7-case × 3-repeat routing A/B, and 3-case × 3-repeat cached-GEO DA A/B with zero loops or blockers. **Exception:** `seacdm_tools._get_llm()` still defaults to Sonnet via `BIOAGENT_SEACDM_LLM_PROVIDER=anthropic`. The original one-call 100k-character SEA-CDM benchmark left DeepSeek incomplete in 3/3 runs. The focused staged strategy now receives a deterministic `[TARGET GEO SCOPE]` summary and treats one GEO accession—not every cohort in the paper—as its extraction unit. The evaluator checks cross-cohort relation contamination rather than a gold experiment count. GSE208615, GSE270703, and corrected-scope GSE250122 each passed 3/3. A subsequently frozen unseen multi-accession case, GSE197045 (RRBS) in a paper that also deposits GSE198652 (RNA-seq), also passed 3/3 with no cross-accession contamination, 97.9% provenance, and an independent 100/100 audit at 65.2% applicable coverage. DeepSeek is therefore supported for staged GEO-metadata-backed accession extraction; Sonnet remains the production default and fallback for paper-wide/no-metadata extraction until routing is deliberately changed.

**Entry point:** `main.py` — initializes the LLM, registers tools (wrapped with programmatic guards), defines the English system prompt, and streams the agent's tool calls / responses. `recursion_limit=25`.

**Tools** (in `tools/`):

*Single-study workflow:*
- `geo_tools.py` — `download_geo_data`, `download_supplementary_files`, `fetch_geo_description`, **`search_geo_studies`** (NCBI E-utilities keyword search, returns a curated GEO series list). Saves expression matrix and metadata as CSV to `./data/{accession}/`, auto-converts supplementary `.xlsx` → `.csv`. `download_supplementary_files` does NOT auto-unpack `_RAW.tar` archives (the batch pipeline handles that — see `batch_tools.py`).
- `seacdm_tools.py` — `extract_sea_cdm_tables` is current. `extract_sea_cdm_conditions` is **Legacy**, retained only for old scripts.
- `preprocess_tools.py` — `preprocess_counts`. Drops all-NaN annotation columns, filters low-expression genes, log2(CPM+1) normalization. Reads CSV/TSV/.gz transparently via pandas separator sniffing (see "TSV silent-failure fix" below). Outputs `<base>_filtered.csv` and `<base>_normalized.csv`.
- `stats_tools.py` — `run_pca`, `sample_correlation_heatmap`, `sample_qc_summary`. Each tool accepts an optional `metadata_csv` so it can intersect against true sample IDs and ignore annotation columns. All tools call `_reject_if_metadata` at entry to refuse a metadata CSV passed where a counts CSV was expected.
- `deseq2_tools.py` — `run_deseq2_analysis`, `inspect_metadata`. Uses the shared `align_samples()` cascade (see `sample_align.py`) when counts/metadata sample IDs don't match exactly.
- `limma_tools.py` — `run_limma_analysis`. limma moderated-t + empirical Bayes (via `inmoose.limma`, pure-Python port of R/Bioconductor limma). For **log-scale** matrices: log2(CPM+1), log-FPKM/TPM, proteomics intensities. Output CSV is column-compatible with DESeq2 (`log2FoldChange` / `padj` / `pvalue` / `lfcSE` / `stat`) so `enrichment_tools` and GSEA consume it unchanged. Patsy gotcha: must pass `patsy.DesignMatrix` (default `dmatrix(formula, data)` return), NOT `return_type='dataframe'` — inmoose drops the column names on DataFrame→DesignMatrix conversion, breaking `topTable(coef="Treatment", ...)`.
- `proteomics_tools.py` — PRIDE labeling/download/preprocessing plus `aggregate_peptide_to_protein` for peptide-level exports. Linear peptide abundances default to summed protein abundance; log2 input must use mean/median/top-N mean. Shared peptides and decoys are excluded by default, with a JSON manifest for provenance.
- `scrna_tools.py` — pseudobulk single-cell DA per cell type; `paired=True` keeps complete donor pairs and uses donor-blocked limma (`~ C(sample) + Treatment`).
- `enrichment_tools.py` — `run_enrichment_analysis` (ORA against Enrichr GO BP/MF/CC + KEGG) and **`run_gsea_analysis`** (preranked GSEA against MSigDB Hallmark via `gseapy.prerank` + `gp.Msigdb().get_gmt`). Auto-detects Ensembl IDs and converts to gene symbols via MyGene.info. Mouse uses `mh.all @ 2024.1.Mm`; Human uses `h.all @ 2024.1.Hs`.

*Shared utilities:*
- `sample_align.py` — `align_samples(counts_cols, metadata_df)` cascade: **exact** → **substring** → **token-overlap** (Jaccard-like on alphanumeric tokens with ≥3-token threshold). Used by both `deseq2_tools` and `stats_tools`. **No position-based fallback** — silently aligning by row order risks producing biologically wrong DESeq2 results when ordering differs.
- `guards.py` — `guard_tools(tools, max_calls_per_tool=3)`. Per-run isolated, thread-safe dedupe and unique-execution cap; duplicate arguments reuse cached/in-flight results without consuming budget. `main.build_agent()` creates a fresh guarded set for every request.
- `tool_router.py` — deterministic per-request capability routing. `main.build_agent(query)` exposes only the matched modality/workflow tools and creates fresh guarded wrappers for that request; ambiguous queries fall back to the full registry.
- `analysis_policy.py` — code-enforced scientific invariants shared by DA tools: numeric matrix validation, raw-count vs log-scale method compatibility, two-arm design validity, minimum replication, and per-arm alignment coverage.
- `evidence.py` — unified provenance schema and recorder for sources, claims, decisions, and artifacts. Batch runs emit per-study `evidence.json`; legacy `decisions.json` remains for compatibility and links to the evidence bundle.
- `run_status.py` — persistent run control/status model plus optional one-line terminal renderer. CLI agent runs write `output/agent_<timestamp>/run_status.json`; batch runs write `output/cohort_<label>/run_status.json` with study/stage counters, elapsed time, warnings/failures, usage fields, and evidence pointers.
- `agent_state.py` — custom `BioinformaticsAgentState` (`messages` plus separate analysis request, run status, artifacts, evidence IDs, and execution budget) and `RuntimeStateMiddleware`. Before each model call it synchronizes the tracker and temporarily augments the system message with a compact decision-relevant state projection; it never appends status updates to ReAct message history.

*Cohort/batch workflow:*
- `batch_tools.py` — **`run_batch_geo_pipeline`** orchestrates multi-study runs from a list of accessions:
  - For each study: download → `_find_expression_file` (heuristic matrix detection, excludes `*_metadata.csv`, accepts raw_counts / log_transformed / fpkm_or_tpm; prefers raw_counts when multiple types are present) → `_unpack_and_merge_geo_tar` fallback for `_RAW.tar` studies → **matrix-type dispatch**: raw_counts → preprocess_counts (CPM+log2 side artifact) + QC + DESeq2; log_transformed → QC + limma on file as-is; fpkm_or_tpm → `_log2_transform_matrix` (writes `<base>_log2.csv`) + QC + limma → `_auto_detect_design` (scoring-based) → **LLM contrast validation** → DA (DESeq2 or limma) → GSEA. Summary CSV records `matrix_type` and `da_method` per study.
  - Per-study failures are caught and logged to `failures.log`; the batch continues.
  - Captures full stdout/stderr (including pydeseq2 / gseapy logging) to `workflow.log` via an in-process Tee.
  - Optional `source_search_csv` param: when provided, snapshots the matching rows from the search CSV at the top of `workflow.log` for full provenance.

- `llm_helpers.py` — LLM fallback utilities. Two hooks:
  - **`validate_contrast_with_llm`** (Priority A) — called from `batch_tools` once per study after `_auto_detect_design`. Returns a `ContrastValidationResult` Pydantic model with `is_valid`, optional override `(col, ctrl, treat)`, and reasoning.
  - **`align_samples_with_llm_fallback`** (Priority B) — drop-in wrapper for `tools.sample_align.align_samples`. When the 3 string strategies (exact / substring / token-overlap) all fail, asks Codex to decode the abbreviation pattern and returns a `{metadata_id → counts_col}` mapping. Used by `deseq2_tools` and `stats_tools`. Returned method string is `llm (k/n)` on success, `no_match` / `no_match_llm_too_few (k/n)` on failure.
  - Both use `ChatAnthropic.with_structured_output()` for deterministic JSON. Per-call cost ≈ $0.001-0.005. If the call fails (no API key, network, schema), the caller falls back to the Python heuristic's original answer — never blocks.
- `multigroup_tools.py` — explicit multi-level/factorial/paired-change executor used by
  `run_batch_geo_pipeline` when a plan declares `analysis_type` as `multigroup`, `multilevel`,
  `factorial`, or `paired_change`. Validates exact metadata coverage, duplicate feature IDs,
  full-rank patsy formulas, residual degrees of freedom, and named limma contrasts. Paired-change
  plans compute within-subject follow-up minus baseline deltas before fitting group contrasts.

**Data flow:**

*Single study:* User query (Chinese) → Codex → tool selection → guarded tool execution → per-study CSV/JSON output → Chinese summary response.

*Cohort:* User keyword → `search_geo_studies` → list of accessions → `run_batch_geo_pipeline(accessions, treatment_keywords, control_keywords, source_search_csv)` → per-study outputs + cohort-level `summary.csv` + `workflow.log`.

**Key design choice — programmatic guardrails:** System prompts asking the LLM "do not loop" are insufficient on their own. `guard_tools` enforces dedupe + cap in Python so loops are structurally impossible. Both Sonnet 4.6 and DeepSeek V4 Pro completed the paired evaluations without loops, while the guards still cap the worst-case bill at ~30 tool calls per run.

**Key design choice — structured tool outputs via Pydantic:** Current extraction uses validated Pydantic output; Python assigns IDs/FKs and writes relational tables.

**Key design choice — fail loudly, not silently.** `align_samples` deliberately omits a position-based fallback (would corrupt biology silently); `_find_raw_counts_file` skips with explicit reason codes instead of best-effort matching; `_classify_matrix` rejects FPKM/TPM rather than feeding them to DESeq2 (statistical model assumes integer counts).

## Directory Layout

```
project root/
├── main.py, clean.py, README.md, AGENTS.md, .env
├── data/                                 # GEO downloads (mirrors GSE accession structure)
│   └── {GSE_accession}/
│       ├── {accession}_metadata.csv      # GEOparse phenotype_data
│       ├── {accession}_*.tsv.gz / .csv.gz / .txt.gz   # raw counts (read directly via pandas)
│       ├── {accession}_RAW.tar           # per-sample archive (unpacked on demand by batch tool)
│       ├── _unpacked/                    # tar extract dir (created on demand)
│       └── {accession}_merged_from_tar.csv   # synthesized when tar is unpacked
├── tools/                                # all @tool definitions + shared helpers
├── output/
│   ├── search_{keyword}.csv              # search results from search_geo_studies
│   ├── {GSE_accession}/                  # single-study outputs (flat per-GSE, mirrors data/)
│   │   ├── *_filtered.csv, *_normalized.csv
│   │   ├── *_pca.png, *_pca_scores.csv
│   │   ├── *_corr_{method}.csv, *_corr_{method}.png
│   │   ├── *_sample_qc.tsv
│   │   ├── DEG_results_{treatment}_vs_{control}.csv
│   │   ├── *_GSEA_Hallmark.csv
│   │   ├── <deg_basename>_GO_Biological_Process_2023.csv  (and MF/CC, KEGG)
│   │   └── seacdm.json
│   └── cohort_{run_label}/               # batch-run outputs (isolated per-cohort)
│       ├── summary.csv                   # one row per accession, machine-readable status table
│       ├── failures.log                  # explicit exceptions / DEG failures
│       ├── workflow.log                  # full stdout/stderr including pydeseq2/gseapy logs
│       └── {GSE_accession}/              # per-study artifacts (same layout as output/{GSE_accession})
└── test/
    ├── test.py, test_seacdm.py, smoke_test_new_tools.py, probe_search_quality.py
    ├── WORKFLOW_REPORT.md                # historical end-to-end run trace
    └── output/smoke_test/                # smoke-test artifacts (kept isolated from real runs)
```

Cohort directory naming: `output/cohort_{run_label}/`. Each batch run is isolated so two cohorts sharing a GSE don't overwrite each other. The `run_batch_geo_pipeline` default for `output_base` is `./output`; the `cohort_` prefix is added automatically from `run_label`.

## Important Engineering Decisions From This Codebase's History

**TSV silent-failure fix.** Originally `pd.read_csv(path, index_col=0)` was used without specifying `sep`. For `.tsv.gz` inputs this read the whole row as one column, `pd.to_numeric` then coerced everything to NaN, and the "drop all-NaN columns" cleanup silently dropped every sample → preprocessing reported "N genes x 0 samples" with no error. **All four affected read points** (`preprocess_tools:29`, `stats_tools:31`, `stats_tools:44`, `deseq2_tools:32`) now use `sep=None, engine="python"` to let csv.Sniffer auto-detect the delimiter. Metadata read points were intentionally left at the default since GEOparse output is reliably CSV.

**Sample alignment cascade (`align_samples`).** The original inline alignment was a greedy substring match: for each metadata row, iterate counts columns and break on first substring hit. This silently corrupted alignments when sample names had prefix-collision patterns like `Sample_1` (substring of `Sample_10`, `Sample_11`, ...) — the substring would prematurely match the wrong column, then `~duplicated(keep="first")` would discard the right one. GSE297707 (64 samples) was getting reduced to 9 aligned samples → 1 DEG. The new cascade tracks `used` columns to prevent double-assignment and adds token-overlap as a third strategy when both exact and substring fail.

**Metadata-as-counts misidentification.** Before the metadata-name exclusion, `_find_raw_counts_file` would pick `{accession}_metadata.csv` as the counts matrix when no other file existed — some metadata columns (e.g. `data_row_count`) are large integers that pass the "looks like raw counts" heuristic. Filenames containing `metadata` are now excluded from the candidate list at scan time.

**Tar archive unpacking.** GEO submissions often distribute per-sample counts as `{accession}_RAW.tar` containing one `GSM*_label.txt.gz` per sample. `_unpack_and_merge_geo_tar` extracts these to `data/{accession}/_unpacked/`, reads each (auto-detecting separator, skipping `#`-prefixed comment lines for featureCounts output), takes the rightmost numeric column as the count, and merges by gene_id into a synthesized `{accession}_merged_from_tar.csv`. The result is then re-classified — sometimes the per-sample files contain FPKM/TPM and the synthesized matrix is rejected at that stage.

**Scoring-based contrast detection (`_auto_detect_design`).** First-match was too brittle when multiple metadata columns could potentially split into 2 groups. Now scores each candidate column: +1 base, +1 if column name contains "treatment"/"condition", +1 if both groups have ≥3 samples. A value is counted as a control candidate only if it matches a control keyword AND NOT a treatment keyword (avoids ambiguous strings like "sedentary control").

**LLM contrast validation (Priority A fallback).** `_auto_detect_design` uses keyword matching that fails when (a) the relevant keywords aren't in the user's list (PBS, Vehicle, AEX) or (b) multiple columns could split into 2 groups and the heuristic picks the wrong one. After each `_auto_detect_design` call — success or failure — `validate_contrast_with_llm` (in `tools/llm_helpers.py`) sends Codex the user's intent + a compact summary of candidate metadata columns + the Python pick, and gets back a `ContrastValidationResult` Pydantic model. Three outcomes: confirm (`is_valid=True`), override with a better `(col, ctrl, treat)`, or refuse (`is_valid=False` + all-null fields → study skipped from DEG with `status=preprocess_ok_no_design`). The result is recorded in `summary.csv` (new columns: `llm_validated`, `llm_overrode`, `llm_reasoning`) and printed to `workflow.log`. Smoke test: `python test/unit/test_llm_contrast.py`.

**LLM sample-alignment fallback (Priority B fallback).** `align_samples` is purely string-based — when counts use sequencer/lab abbreviations like `HC_F1_TL_S54_L003` and metadata uses full words like `HomeCage1_Female1_TotalLysate`, exact/substring/token-overlap all return empty because the vocabularies don't share tokens. `align_samples_with_llm_fallback` (in `tools/llm_helpers.py`) wraps `align_samples` and, on `no_match`, asks Codex to decode the abbreviation pattern. The LLM mapping is validated against the input lists (drops unknown IDs/cols and duplicates) before being accepted. Both `deseq2_tools.run_deseq2_analysis` and `stats_tools._align_metadata` now use the wrapper, so the fallback automatically benefits the single-study path and (transitively) the batch path. Smoke test: `python test/unit/test_llm_align.py`.

## Known Limitations (Hardening Backlog)

1. ~~**Semantic abbreviation mismatch**~~ — **mitigated by LLM sample-alignment fallback** (see Architecture). When string-based alignment returns `no_match`, Codex decodes the abbreviation pattern and emits a validated mapping. Remaining gap: if the metadata itself doesn't contain enough descriptive context (e.g. only GSM IDs and `data_processing` columns are present), the LLM has nothing to pattern-match against and will still fail.
2. ~~**Keyword coverage gap**~~ — **partially mitigated by LLM contrast validation** (see Architecture). Biological synonyms like `PBS`/`Vehicle`/`AEX` that don't appear in the user's keyword list can still derail `_auto_detect_design`, but the LLM fallback now catches and overrides these picks based on the user's stated intent. Remaining issue: the LLM call only sees keyword lists, not full free-text intent — for studies with truly novel terminology a more descriptive intent string would help.
3. **FPKM/TPM-only studies** — when authors upload only normalized expression matrices (no raw counts in supplementary or in SRA-accessible form), DESeq2 cannot be run. The pipeline correctly skips these but the underlying data problem is unfixable at this layer.
4. **Multi-factor designs** — studies with genotype × stimulus × time × tissue 3-4 axis designs
   require either an LLM-produced or user-supplied explicit formula/contrast plan. The main batch
   path now executes validated `multigroup`/`factorial`/`paired_change` plans; it still refuses to
   invent a design when no plan is available.
5. ~~**`download_supplementary_files` always re-downloads**~~ — **FIXED 2026-06-22 (mechanical cost pass)**. Skip-if-exists added in two places: `download_supplementary_files` skips any file whose target (or converted `.csv` sibling) already exists, and `download_geo_data` short-circuits when `{accession}_metadata.csv` is present (skipping the SOFT download + parse + rewrite). Companion deterministic cost cuts shipped the same pass: process-level **MSigDB GMT cache** (`enrichment_tools._get_hallmark_gmt`, N same-species GSEA runs → 1 fetch), **MyGene Ensembl→symbol cache** (`enrichment_tools._query_symbols`, per `(id, species)`), and a **confidence gate on the per-study LLM contrast validation** (`batch_tools._python_pick_is_confident` — skips the LLM call only when the Python pick is unambiguous: both arms keyword-grounded with ≥3 samples AND exactly one viable design column; ambiguous/no-design studies still go to the LLM). Tests: `test/unit/test_cost_caches.py`, `test/unit/test_cost_gate_45.py`.

## Environment

- Python 3.12+ with virtual environment in `.venv`
- API keys loaded from `.env` via `python-dotenv`: the evaluated deployment uses `DEEPSEEK_API_KEY` + `DEEPSEEK_BASE_URL`; set `BIOAGENT_LLM_PROVIDER=anthropic` to use the `CLAUDE_API_KEY` fallback
- No `requirements.txt` or `pyproject.toml` — dependencies are only tracked in the venv. Key packages: `langchain`, `langchain-anthropic`, `langgraph`, `pandas`, `geoparse`, `pydeseq2`, `inmoose` (limma/edgeR pure-Python port), `patsy`, `scikit-learn`, `matplotlib`, `seaborn`, `gseapy`, `mygene`, `lxml`.
- **`lxml` is required for `gseapy.Msigdb`** (used by `run_gsea_analysis`) — without it, MSigDB Hallmark library fetching fails with `ImportError: Missing optional dependency 'lxml'`.
- External APIs used at runtime (require network): NCBI E-utilities (`search_geo_studies`), GEO FTP (`download_supplementary_files`), Enrichr (`run_enrichment_analysis`), MSigDB (`run_gsea_analysis` via `gp.Msigdb`), MyGene.info (Ensembl→symbol conversion in both enrichment tools).
