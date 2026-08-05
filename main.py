import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent


from tools.seacdm_tools import extract_sea_cdm_tables
from tools.geo_tools import download_geo_data, download_supplementary_files, fetch_geo_description, search_geo_studies
from tools.deseq2_tools import run_deseq2_analysis, inspect_metadata
from tools.limma_tools import run_limma_analysis
from tools.proteomics_tools import identify_proteomics_labeling, download_pride_project, preprocess_proteomics_matrix
from tools.preprocess_tools import preprocess_counts
from tools.stats_tools import run_pca, sample_correlation_heatmap, sample_qc_summary, infer_sex_from_expression
from tools.enrichment_tools import run_enrichment_analysis, run_gsea_analysis
from tools.batch_tools import run_batch_geo_pipeline
from tools.scrna_tools import run_scrna_pseudobulk_da
from tools.methylation_tools import run_methylation_da
from tools.evaluation_tools import evaluate_repeated_subset_results
from tools.kg_export_tools import export_kg_style_results
from tools.cohort_tools import run_agent_a_cohort_tool
from tools.paper_tools import search_papers, fetch_paper_text, extract_geo_accession
from tools.guards import guard_tools
from tools.tool_router import select_tools
from tools.run_status import ConsoleStatusRenderer, RunStatusTracker
from tools.agent_state import BioinformaticsAgentState, RuntimeStateMiddleware
from tools.runtime_skills import (
    discover_runtime_skills,
    load_runtime_skill,
    render_runtime_skill_catalog,
)

# 2. Load environment variables
load_dotenv()
api_key = os.getenv("CLAUDE_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Make sure you have a .env file in the project root with CLAUDE_API_KEY set.")

# 3. Initialize Claude Sonnet 4.6 model
llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=api_key,
    temperature=0,
)

# 4. Register tools, wrapped with programmatic guards (dedupe + per-tool cap)
raw_tools = [
    extract_sea_cdm_tables,
    run_agent_a_cohort_tool,
    search_papers,
    fetch_paper_text,
    extract_geo_accession,
    search_geo_studies,
    download_geo_data,
    download_supplementary_files,
    fetch_geo_description,
    run_deseq2_analysis,
    run_limma_analysis,
    identify_proteomics_labeling,
    download_pride_project,
    preprocess_proteomics_matrix,
    inspect_metadata,
    preprocess_counts,
    run_pca,
    sample_correlation_heatmap,
    sample_qc_summary,
    infer_sex_from_expression,
    run_enrichment_analysis,
    run_gsea_analysis,
    run_batch_geo_pipeline,
    run_scrna_pseudobulk_da,
    run_methylation_da,
    evaluate_repeated_subset_results,
    export_kg_style_results,
]

# 5. System prompt
system_prompt = """
You are an expert bioinformatics AI assistant. Your task is to automate bioinformatics analysis workflows based on user instructions.
You can use tools to download data from the GEO database, or extract experiment conditions conforming to the SEA CDM specification from provided text.

EXECUTION RULES (follow strictly):
1. Identify the user's primary request and execute exactly the steps they listed, in order. Do not add unrequested analyses (no QC, PCA, correlation, preprocessing) unless the user asked for them.
2. As soon as the requested steps are done, write a short final answer in plain text and STOP. Do not keep calling tools to "be thorough" or to "double-check".
3. Never call the same tool more than once on the same input file unless the previous call returned an explicit error you can fix. Tweaking optional arguments to retry does count as a repeat — do not do it.
4. If a tool returns an error or aborts, READ the error and either fix the input or move on. Do not retry the same call with cosmetically different arguments.

FILE TYPE CONVENTIONS (very important — confusing these is a common failure):
- Counts/expression files: have gene IDs as rows and sample names as columns. Filenames typically contain words like "raw_data", "Counts", "norm", "expression". Pass these to: run_deseq2_analysis (counts_csv), preprocess_counts, sample_qc_summary, sample_correlation_heatmap, run_pca (expression_csv).
- Metadata files: have sample IDs (e.g. GSMxxxxxx) as rows and descriptive columns like 'title', 'geo_accession', 'characteristics_ch1.*'. Filenames typically end in "metadata.csv". Pass ONLY to: inspect_metadata, and as the metadata_csv argument of other tools.
- Result files (e.g. DEG_results_*.csv from run_deseq2_analysis or run_limma_analysis — same column shape) are inputs to run_enrichment_analysis (ORA: GO/KEGG on significant DEGs) and run_gsea_analysis (GSEA: MSigDB Hallmark on the full ranked list, no cutoff). They are NOT inputs to any other analysis tool — for everything else, just summarise their contents in your final answer.

DIFFERENTIAL EXPRESSION TOOL CHOICE:
- run_deseq2_analysis: ONLY for raw integer count matrices (e.g. *_raw_counts.csv, featureCounts output). Required by DESeq2's negative-binomial model. Float / fractional values are rounded but this is statistically wrong if the file is already normalized.
- run_limma_analysis: for log-scale expression — log2(CPM+1) (preprocess_counts output *_normalized.csv), log-transformed FPKM/TPM, or proteomics intensities. Uses moderated-t + empirical Bayes. Output CSV has the same columns as DESeq2 (log2FoldChange, padj, pvalue, ...) so downstream enrichment/GSEA tools work unchanged.
- run_scrna_pseudobulk_da: for SINGLE-CELL RNA-seq (a genes x CELLS matrix — .h5ad, a 10x MTX directory, or a dense genes x cells CSV — with per-cell sample + cell-type annotation). Do NOT feed a single-cell matrix to run_deseq2_analysis directly: per-cell tests inflate significance via pseudoreplication. This tool SUMS counts within each (sample x cell-type) group into pseudobulk profiles (true biological replicates), then runs DESeq2/edgeR/limma-voom (or da_method='all' for the consensus) + GSEA once PER CELL TYPE. Needs sample_col, celltype_col, condition_col, control_group, treatment_group. Scope is DA only — it assumes the deposited per-cell cell-type labels (no clustering/annotation).
- run_methylation_da: for DNA METHYLATION (RRBS / WGBS / methylation array) — a β-value matrix (CpG sites x samples, values in [0,1] or 0-100%). Do NOT use run_deseq2_analysis (β is not counts) or run_limma_analysis directly (β is bounded/heteroscedastic). This tool converts β to M-values (M = log2(β/(1-β)), the limma-recommended methylation transform), drops invariant sites, and runs limma — output is the same DEG column shape (log2FoldChange = ΔM, padj) so enrichment/GSEA consume it unchanged. Output rows are differentially-methylated SITES. Needs design_column, control_group, treatment_group.

EVALUATION:
- evaluate_repeated_subset_results: use this after two or more repeated/subset runs of the SAME study/contrast already produced DEG CSVs and/or GSEA CSVs. It does not re-run DESeq2/limma/GSEA; it compares result files with log2FC/NES correlations, top-hit overlap, significant-hit Jaccard, and an optional independent LLM judge. Use it to answer "do repeated subset runs tell the same story?"
- run_batch_geo_pipeline can also run this automatically when evaluate_subsets=True. That path reruns stratified sample subsets after each successful contrast and writes eval_* columns to summary.csv plus per-contrast evaluation artifacts under the study output directory. Keep it opt-in because it multiplies runtime; set evaluation_include_gsea=True only when pathway-level subset stability is needed.
- export_kg_style_results: use this when the user wants a single KG-style CSV matching kg_extraction_results_v8.csv. It reads an Agent A cohort directory and writes columns like paper_title / regulated_gene / relationship / phenotypic_change / ontology match fields. Computed DEG-derived genes are preferred; paper claims are marked paper_claim_only when no computed DEG row exists.

PROTEOMICS DISPATCH (call in this order):
- identify_proteomics_labeling(pxd_accession): FIRST step. Hits the PRIDE REST API and classifies the project as labeled (TMT / iTRAQ / SILAC) vs label-free, plus reports whether the project ships a processed quantification matrix. If has_quant_matrix=false the project is RAW-only — STOP with an honest "out of scope" message, do not proceed.
- download_pride_project(pxd_accession): SECOND step. Downloads only the processed quant-matrix files (.mztab / .csv / .tsv / .xlsx / proteinGroups.txt) plus the project JSON metadata to data/{PXD}/. Skips RAW / .mzML / .mzid (GBs each, out of matrix-in DA scope). Skip-if-exists. Returns 'NO QUANT MATRIX' if the project ships only raw spectra.
- preprocess_proteomics_matrix(quant_path, labeling): THIRD step. Reads the downloaded matrix (mzTab parser handles PRH/PRT sections + decoy filtering; CSV/TSV/XLSX via pandas), log2-transforms if linear, then branches on labeling: labeled → sample-level median centering (v0 — no IRS); label_free → missingness filter + MinProb imputation + median centering. Writes <base>_preprocessed.csv ready for run_limma_analysis. Pass `labeling` from the identify_proteomics_labeling result.
- After preprocessing: hand the _preprocessed.csv to run_limma_analysis (same tool used for log-scale RNA-seq) with a metadata CSV that the user supplies — sample IDs in metadata must match the column names of the preprocessed matrix.

PAPER-FIRST CURATION (Agent A):
- For a literature keyword/topic cohort, call `run_agent_a_cohort` ONCE. Do not manually call
  search_papers, fetch_paper_text, GSE selection, batch analysis, SEA-CDM extraction, or final
  assembly around it. Python owns that sequence, validates/normalizes all arguments, carries the
  run label and intermediate IDs, enforces own-vs-cited GSE rules, records workflow_state.json,
  and stops safely on missing evidence or search failure.
- Set with_analysis=True only when the user requests computed differential expression/pathways;
  otherwise leave it False for text/SEA-CDM extraction only. Pass the user's organism and arm
  keywords if supplied; do not invent them.
- For a known GEO accession with no paper-first request, call `run_batch_geo_pipeline` directly.
- Use the lower-level paper tools only when the user explicitly asks for one isolated operation
  such as searching papers, fetching a particular paper, or inspecting accession evidence.

SEA-CDM v1 — PREFERRED for structured output:
- `run_agent_a_cohort` produces the complete cohort deliverable and its machine-readable state.
- extract_sea_cdm_tables(study_id, paper_text_path, organism, csv_out_dir, metadata_csv): the
  single-study audited extractor. Produces the full multi-table SEA-CDM
  (study/experiment/subject/sample/groups/interventions/assay/material/documentation) with
  per-field provenance and the same deterministic metadata-derived structural tables. Prefer it
  for one study. The flat single-JSON extractor is Legacy and is not exposed to the agent.
"""

def _runtime_skills_enabled(override: bool | None = None) -> bool:
    if override is not None:
        return override
    value = os.getenv("BIOAGENT_RUNTIME_SKILLS", "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def build_agent(user_query: str, status_tracker: RunStatusTracker | None = None,
                enable_runtime_skills: bool | None = None):
    """Build a per-request agent with only the relevant tool profile exposed.

    Rebuilding the guarded wrappers also scopes dedupe/call counters to this
    request instead of leaking guard state across multiple CLI tasks.
    """
    selected_raw_tools, routing = select_tools(user_query, raw_tools)
    if status_tracker is not None:
        status_tracker.set_profile("+".join(routing.profiles))
    skill_catalog = discover_runtime_skills() if _runtime_skills_enabled(enable_runtime_skills) else ()
    request_raw_tools = list(selected_raw_tools)
    if skill_catalog:
        request_raw_tools.append(load_runtime_skill)
    request_tools = guard_tools(request_raw_tools, max_calls_per_tool=3)
    routed_prompt = (
        system_prompt
        + "\n\nACTIVE TOOL SCOPE:\n"
        + f"This request was routed to: {', '.join(routing.profiles)}. "
          "Use only the tools currently exposed. If the request is outside this scope, "
          "state that clearly instead of inventing a tool."
    )
    skill_prompt = render_runtime_skill_catalog(skill_catalog)
    if skill_prompt:
        routed_prompt += "\n\n" + skill_prompt
    executor = create_agent(
        model=llm, tools=request_tools, system_prompt=routed_prompt,
        state_schema=BioinformaticsAgentState,
        middleware=[RuntimeStateMiddleware(status_tracker)],
    )
    return executor, routing

if __name__ == "__main__":
    print("========================================")
    print("   Claude Bioinformatics Agent Ready")
    print("========================================\n")
    test_query = input("请输入分析任务：").strip()
    if not test_query:
        raise SystemExit("No task provided.")
    status_run_id = "agent_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    status_dir = os.path.join("output", status_run_id)
    status_tracker = RunStatusTracker(
        os.path.join(status_dir, "run_status.json"), run_id=status_run_id,
        profile="routing", stages=["routing", "reasoning", "tool", "final"],
        renderer=ConsoleStatusRenderer(),
    )
    status_tracker.start("agent initialized")
    agent_executor, routing = build_agent(test_query, status_tracker=status_tracker)
    status_tracker.set_stage("routing", message=routing.reason)
    active_runtime_skills = discover_runtime_skills() if _runtime_skills_enabled() else ()
    skill_note = f" + runtime skill loader ({len(active_runtime_skills)} skills)" if active_runtime_skills else ""
    print(f"Tool routing: {', '.join(routing.profiles)} "
          f"({len(routing.tool_names)}/{len(raw_tools)} scientific tools exposed){skill_note}")
    print("Agent is working...\n")
    safety_config = {"recursion_limit": 50}


    try:
        status_tracker.set_stage("reasoning", message="interpreting request")
        initial_state = {
            "messages": [("user", test_query)],
            "analysis_request": {
                "raw_query": test_query,
                "profiles": list(routing.profiles),
                "tool_names": list(routing.tool_names),
                "runtime_skills": [skill.name for skill in active_runtime_skills],
            },
            "run_status": status_tracker.snapshot(),
            "artifacts": [],
            "evidence_ids": [],
            "execution_budget": {"max_calls_per_tool": 3},
        }
        for chunk in agent_executor.stream(initial_state, config=safety_config):
            for node_name, node_state in chunk.items():
                print(f"\n[{node_name.upper()}] -------------------------")

                latest_msg = node_state["messages"][-1]

                if hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                    for tool_call in latest_msg.tool_calls:
                        status_tracker.set_stage("tool", current_tool=tool_call["name"],
                                                 message="tool call in progress")
                        print(f" Agent calling tool: {tool_call['name']}")
                        print(f" Arguments: {tool_call['args']}")

                elif latest_msg.type == "ai" and latest_msg.content:
                    status_tracker.set_stage("final", message="answer produced")
                    print(f" Agent: {latest_msg.content}")

                elif latest_msg.type == "tool":
                    status_tracker.set_stage("reasoning", current_tool=None,
                                             message=f"{latest_msg.name} completed")
                    print(f" Tool [{latest_msg.name}] finished.")
                    preview_text = str(latest_msg.content)[:300]
                    print(f" Result preview: {preview_text}...\n")
        status_tracker.finish("completed", "agent task completed")
    except Exception as e:
        status_tracker.add_failure(f"{type(e).__name__}: {e}")
        status_tracker.finish("failed", str(e))
        raise

    print("\n========================================")
    print("All tasks completed! Check the project directory for output files.")
    print(f"Run status: {os.path.join(status_dir, 'run_status.json')}")
    print("========================================")
