import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent


from tools.seacdm_tools import extract_sea_cdm_conditions, extract_sea_cdm_tables
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
from tools.paper_tools import search_papers, fetch_paper_text, extract_geo_accession, assemble_agent_a_record
from tools.guards import guard_tools

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
    extract_sea_cdm_conditions,
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
    assemble_agent_a_record,
]
tools = guard_tools(raw_tools, max_calls_per_tool=3)

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

PAPER-FIRST CURATION WORKFLOW (Agent A):
When the user starts from the literature — a topic/keyword, a paper title, or a DOI/PDF URL — rather than a known GEO accession, run this chain to find and analyze the paper's data:
1. search_papers(keyword): get a triage list of open-access papers (saved to a CSV). Prefer candidates that already expose a GEO id in the abstract (geo_in_abstract), then those flagged [seq-signal].
2. fetch_paper_text on a promising candidate: pass search_index=N — the [#N] rank from the search_papers list. The tool resolves that hit's exact PMCID/PDF for you. Do NOT retype a PMCID into the call (mistyping the digits silently fetches an unrelated paper); just pass the index. It returns the GEO/SRA/ArrayExpress accessions with a context snippet. If a fetch fails or finds no accession, move on to the NEXT candidate (a different index); do not retry the same input.
3. Decide which accession is the paper's OWN deposited data vs. a citation of another study — read the context snippet (look for "deposited", "data availability", "available at", "GEO accession"). You may also run extract_geo_accession on the saved .txt path to re-list accessions.
4. Hand the chosen GSE to the analysis backend via run_batch_geo_pipeline(accessions=[GSE], organism=..., treatment_keywords=..., control_keywords=..., run_label=...) — even for a single study. It runs download -> contrast auto-detection (+ LLM validation) -> DESeq2 -> GSEA and writes a decision log; this is the hardened path and avoids you having to pick the contrast by hand. REMEMBER the run_label you used — step 6 needs it.
5. Call extract_sea_cdm_conditions on the paper text to capture study- and assay-level structured info from the paper (it writes output/{study_id}_seacdm.json). Use chosen_gse as study_id.
6. Call assemble_agent_a_record LAST to produce the FINAL Agent A deliverable — a single JSON file at output/agentA/{stem}.json. Pass:
   - paper_id (the literal 'paperId' from the search_papers row; pass "" if you started from a known PMCID)
   - pmcid (same one you passed to fetch_paper_text)
   - chosen_gse (the OWN GSE)
   - chosen_reason (a short tag, e.g. "deposition language: 'are deposited'")
   - rejected_gses (list of {"gse": "...", "reason": "..."} dicts for EVERY other GSE the text contained; pass [] if none)
   - cohort_run_label (exactly what you passed to run_batch_geo_pipeline)
   - paper_title, paper_year, paper_doi, paper_pmid, organism (all from the search_papers row + what you used)
   This tool re-reads everything from disk and writes the single artifact the mentor reviews per paper.
7. In your final answer, reference the path returned by assemble_agent_a_record plus a one-paragraph human summary.

(If the user gave you a known accession directly — no paper — skip steps 1-3, 5, 6 and just run the analysis backend.)

PAPER-FIRST GUARDRAILS (critical — every bullet is a hard rule, not a suggestion):
- To read a search hit, pass search_index=N to fetch_paper_text — NEVER retype its PMCID. The tool looks up the exact id; a hand-typed PMCID that isn't in the search results is rejected. NEVER construct, guess, or derive a PMCID from a GSE number or training memory — a wrong id silently fetches a completely unrelated paper.
- The chosen_gse you hand to run_batch_geo_pipeline and assemble_agent_a_record MUST appear LITERALLY in the text returned by fetch_paper_text or extract_geo_accession for a candidate you actually fetched. NEVER use a GSE number from your training memory, from search_geo_studies, or from any other source. assemble_agent_a_record cross-checks this and will flag a CRITICAL issue if the GSE is not in the paper text — that means the record is publicly broken.
- If after fetching 2-3 candidate papers NONE of them contains a GSE in its fetched text, STOP. Call assemble_agent_a_record with chosen_gse="" and chosen_reason describing the situation (e.g. "no GSE accession found in 3 fetched candidates; data may be in supplementary tables or another repository — manual review needed"). Do NOT then call run_batch_geo_pipeline (there is no valid GSE to analyze), do NOT fall back to search_geo_studies, do NOT invent a GSE. An honest "no-data" record is correct output; a fabricated chosen_gse is a serious integrity failure.
- If search_papers is unavailable (e.g. it returns a 429 rate-limit message), do NOT improvise: do not switch to search_geo_studies, and do not invent accessions or PMCIDs. State plainly that the paper search was rate-limited and stop.
- Do not call search_papers more than twice. If it is rate-limited, immediate retries will also fail — stop and report rather than churning through tool calls.

SEA-CDM v1 — PREFERRED for structured output (use these instead of the older flat extractor):
- run_agent_a_cohort(keyword, ...): the ONE-CALL full Agent A pipeline. Turns a keyword into the
  13 SEA-CDM CSVs from the top hits, running internally: own-vs-cited GSE disambiguation; the 9
  text tables with per-field provenance; subject/sample/groups/assay derived DETERMINISTICALLY
  from each study's GEO metadata CSV (re-runs give byte-identical structural tables); the paper's
  text-mined findings; and the pathway->gene->exercise mechanism chain. Pass with_analysis=True
  (plus treatment_keywords/control_keywords) to also compute DESeq2/edgeR/limma-voom + GSEA on
  strictly-own GSEs and the computed-vs-reported agreement. Use this when the user wants the whole
  keyword->SEA-CDM cohort deliverable; you do NOT need to hand-orchestrate steps 1-7 above.
- extract_sea_cdm_tables(study_id, paper_text_path, organism, csv_out_dir, metadata_csv): the
  SINGLE-STUDY v1 successor to extract_sea_cdm_conditions. Produces the full multi-table SEA-CDM
  (study/experiment/subject/sample/groups/interventions/assay/material/documentation) with
  per-field provenance and the same deterministic metadata-derived structural tables. Prefer it
  over extract_sea_cdm_conditions for step 5 when you want the relational 13-table output for one
  study. (extract_sea_cdm_conditions remains only for the legacy flat single-JSON output.)
"""

# 6. Create Agent via langchain
agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

# ==========================================
# 7. Test Agent
# ==========================================
if __name__ == "__main__":
    print("========================================")
    print("   Claude Bioinformatics Agent Ready")
    print("========================================\n")


    # Full keyword-driven paper-first chain (search -> fetch -> disambiguate -> analyze
    # -> extract -> assemble). Requires a working Semantic Scholar (S2_API_KEY in .env)
    # AND a candidate paper that exposes its GSE in main text — for some keywords most
    # 2024+ papers put accessions in supplementary tables only, in which case the
    # GUARDRAILS will (correctly) make the agent stop with an honest "no-data" record.
    # Swap names with `test_query` below to use this as the active run.
    test_query_keyword_driven = """
  Run the paper-first Agent A workflow end-to-end on a real exercise skeletal-muscle study
  and produce the final Agent A deliverable JSON.

  Steps:
  1) search_papers with keyword "exercise skeletal muscle transcriptome". Remember the row
     fields of whichever candidate you pick (paperId, title, year, pmcid, pmid, doi).
  2) Pick a candidate that looks like it generated RNA-seq data (a GEO id in the abstract, or a
     [seq-signal] flag, and a PMCID rather than pdf-only). Call fetch_paper_text(search_index=N)
     using that hit's [#N] number — do NOT type its PMCID. If a fetch finds no accession, move on
     to the NEXT candidate (a different index) — do not retry the same input. Try at most 3 before stopping.
  3) From the extracted text, identify the GEO GSE accession that THIS paper DEPOSITED — use
     the context snippets the tool returned to distinguish the paper's own data (phrasing
     like "deposited", "data availability") from data it merely reused ("downloaded from",
     "obtained from"). Only use a GSE that literally appears in the tool output.
  4) Hand that single GSE to run_batch_geo_pipeline:
     - accessions: [the OWN GSE]
     - organism: the study's species — "Human" or "Mouse" — based on the context snippet
       (most "exercise skeletal muscle" studies are Human; mouse studies say "mouse" in the
       snippet). Getting this right matters: GSEA uses species-specific Hallmark gene sets.
     - treatment_keywords: ["exercise", "training", "treadmill", "endurance", "trained",
         "voluntary wheel", "run", "aerobic", "exe", "acute"]
     - control_keywords: ["sedentary", "sham", "control", "sed", "rest", "untrained",
         "inactive", "baseline", "pre", "basal"]
     - run_label: "paperA_exercise"  (remember this exact value — step 6 needs it)
  5) After the batch returns, call extract_sea_cdm_conditions to capture study- and
     assay-level structured info from the paper text. Use the chosen GSE as study_id.
  6) Call assemble_agent_a_record LAST with everything you accumulated:
       paper_id        = the paperId from the search row
       pmcid           = the PMCID you passed to fetch_paper_text
       chosen_gse      = the OWN GSE
       chosen_reason   = short tag, e.g. "deposition language: 'are deposited'"
       rejected_gses   = list of {"gse": "...", "reason": "..."} for EVERY other GSE found
                         in the text (e.g. cited prior datasets); pass [] if none
       cohort_run_label= "paperA_exercise"
       paper_title, paper_year, paper_doi, paper_pmid, organism = all from the search row + what you used
     This writes output/agentA/{stem}.json — the final deliverable.
  7) Final answer (English): one paragraph summarizing the paper / chosen GSE / contrast /
     n_DEG / top pathways, and reference the agentA JSON path returned by step 6.
  """

    # ACTIVE — seeded query. Known-good demo for the mentor: PMC12248044 has mixed
    # own/cited GSEs (deposit GSE279359, cited GSE87749 + GSE151066) so it directly
    # exercises the own-vs-cited disambiguation guardrail and produces a clean record.
    # Decoupled from Semantic Scholar (skips search_papers).
    test_query = """
  Validate the paper-first analysis chain starting from a KNOWN open-access paper. This run
  intentionally SKIPS search_papers, so do NOT call search_papers or search_geo_studies.
  The paper is PubMed Central PMC12248044 ("Impact of Acute Endurance Exercise on
  Alternative Splicing in Skeletal Muscle").

  Steps:
  1) fetch_paper_text with pmcid="PMC12248044" (no pdf_url needed — it uses Europe PMC full text).
  2) From the reported accessions and their context snippets, identify the single GEO GSE that
     THIS paper DEPOSITED itself. Distinguish the paper's OWN data (phrasing like "deposited",
     "data availability") from data it merely REUSED ("downloaded from", "obtained from").
     Only use a GSE that literally appears in the tool output — never invent or alter an id.
  3) Hand that single OWN GSE to run_batch_geo_pipeline:
     - accessions: [the OWN GSE]
     - organism: set to that dataset's species (Human or Mouse) based on the context snippet.
     - treatment_keywords: ["exercise", "training", "treadmill", "endurance", "trained",
         "voluntary wheel", "run", "aerobic", "exe", "acute"]
     - control_keywords: ["sedentary", "sham", "control", "sed", "rest", "untrained",
         "inactive", "baseline", "pre", "basal"]
     - run_label: "paperA_seed"
  4) Call extract_sea_cdm_conditions (study_id = the OWN GSE).
  5) Call assemble_agent_a_record(paper_id="", pmcid="PMC12248044", chosen_gse=..., chosen_reason=...,
     rejected_gses=[...], cohort_run_label="paperA_seed", organism=...).
  6) Summarize:
     - The GSE you chose and WHY it is the paper's own data (quote the snippet).
     - Which GSE(s) you rejected as cited/reused data.
     - The organism you used.
     - How far the analysis got: the status, n_deg and top pathways if it ran, or the
       explicit fail-loud reason if the study was skipped (e.g. no raw counts).

  Respond in English.
  """
    


    print("Agent is working...\n")
    safety_config = {"recursion_limit": 50}


    for chunk in agent_executor.stream({"messages": [("user", test_query)]}, config=safety_config):
        for node_name, node_state in chunk.items():
            print(f"\n[{node_name.upper()}] -------------------------")

            latest_msg = node_state["messages"][-1]

            if hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                for tool_call in latest_msg.tool_calls:
                    print(f" Agent calling tool: {tool_call['name']}")
                    print(f" Arguments: {tool_call['args']}")

            elif latest_msg.type == "ai" and latest_msg.content:
                print(f" Agent: {latest_msg.content}")

            elif latest_msg.type == "tool":
                print(f" Tool [{latest_msg.name}] finished.")
                preview_text = str(latest_msg.content)[:300]
                print(f" Result preview: {preview_text}...\n")

    print("\n========================================")
    print("All tasks completed! Check the project directory for output files.")
    print("========================================")
