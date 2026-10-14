# Structured paper full text plan

Goal: give the paper-first workflow section-level access to the article (Methods, tables, figure legends, data availability) with citable block IDs, then measure whether that evidence makes the control/treatment and covariance decisions more accurate. The plan is split into stages that each fit in one usage window.

## Why

`paper_tools.fetch_paper_text` already downloads Europe PMC JATS XML. It then flattens the XML with `" ".join(root.itertext())`, which removes section boundaries, table cells, and figure legends. Sample groups, pairing, and thresholds usually live in exactly those places. Each paper is 10k–30k tokens, so it fits in context whole; the problem was missing structure, not missing retrieval. Section-level reading is used instead of vector top-k so a Methods paragraph or a sample table is never returned half-cut.

## Done

### A. Structured parser and section reader (2026-10-14)

- `tools/paper_structure.py`: JATS parser (standard library only) producing sections with a class (`abstract`, `introduction`, `methods`, `results`, `discussion`, `conclusion`, `data_availability`, `supplementary`, `other`) and blocks with stable IDs (`S2.4.p1`, `TAB1`, `FIG2`, `SUP1`, `DA.p1`). Tables become Markdown with rowspan/colspan expanded. Handles structured abstracts, floats nested in paragraphs, `<floats-group>`, data availability in `<back><notes>`, references inside `<body>`, and the Europe PMC "Associated Data" duplicate. A PDF fallback marks its output `pdf_heuristic` (headings approximate, no tables).
- Reading API and CLI: `outline`, `read_section` (class, section ID, or title words; comma-separated), `find`, `get_blocks`, `resolve_locator`, `fetch`, `parse`.
- `fetch_paper_text` now also writes `<id>.paper.json`, `<id>.paper.md`, and `<id>.jats.xml`, and reports where each GSE is mentioned. The `.txt` is byte-identical to before.
- `paper_tools.read_paper_section` LangChain tool (not yet registered in `main.py`; see stage D).
- Skill references: `paper-reconstruction.md` gains "Reading the paper"; `decision-contract.md` uses block IDs as `paper.locator`; `tool-map.md` lists the module.
- Tests: `test/unit/test_paper_structure.py` (8 cases, offline, four real Europe PMC fixtures in `test/fixtures/papers/`).
- Live sweep over the first 25 PMCIDs of `native_codex_paper_first_20_20261001_` manifest: 23 open access, 23 parsed, 0 errors; Methods found in 23/23, Results in 21/23 (the other two are Data in Brief articles), data-availability statement in 18/23.

### B. Evidence ablation on ExerGeneDB (2026-10-14)

`test/experiments/paper_evidence_ablation/` (`build_manifest.py`, `run_arms.py`, `REPORT.md`). 24 frozen series, 4 arms (metadata, abstract, structured, flat) x 3 repeats on DeepSeek V4 Pro, 288 calls, about $1 in total.

| arm | correct | wrong | refused | locators that resolve | mean input tokens |
|---|---|---|---|---|---|
| metadata | 68.1% | 9.7% | 22.2% | n/a | 1,757 |
| abstract | 77.8% | 12.5% | 9.7% | 100% | 2,212 |
| structured | 70.8% | 12.5% | 16.7% | 100% | 6,890 |
| flat | 68.1% | 16.7% | 15.3% | 70.2% | 17,178 |

Conclusions: at this size, full text does not clearly improve the contrast choice; the abstract gives most of the gain. Structure matters for auditability (flat-text locators are 30% invented) and cost. Some "mixed" verdicts come from the gold's acute-bout definition of exercise, which penalises a paper-aligned cross-sectional contrast. Details and per-series cases are in `REPORT.md`.

## Remaining stages

### B2. Estimand-aware scoring and pairing gold (2026-10-14)

- `test/validation/exergenedb_gold/estimand_annotations.json` names each series' gold axis (`acute_bout`, `training`, `habitual`), the axes its paper analyses, pairing gold per axis, and gold label corrections (8 GSE202295 samples). `sync_covariance_annotations.py` copies the pairing gold into `covariance_annotations.csv`. `tools.contrast_gold.score_estimand_decision` scores the chosen axis separately from the labels on it, flags contrasts with an unlabelled arm, and scores pairing against the chosen axis.
- The ablation now covers all 38 scorable eligible series (39 eligible; GSE158984 has no gold overlap): 456 calls, about $1.60 in total.

| arm | estimand-correct | refused | pairing correct | mean input tokens |
|---|---|---|---|---|
| metadata | 75.4% | 22.8% | 88.2% | 1,711 |
| abstract | 88.6% | 11.4% | 95.9% | 2,151 |
| structured | 84.2% | 15.8% | 100% | 7,770 |
| flat | 85.1% | 14.9% | 100% | 18,214 |

Conclusions: labels on the chosen axis are always right (one confounded metadata call aside); the earlier "wrong" calls were paper-supported axes or gold errors. Abstract is best for the contrast; Methods text is what makes pairing fully right. The remaining errors are in the metadata summary, not the evidence: subject-ID columns with many subjects are dropped, and arms embedded in per-sample titles are never exposed (four series refused in every arm). Details in `paper_evidence_ablation/REPORT.md`.

### B2b. Codex decision-model comparison (paused)

- `run_arms.py --backend codex-cli` sends the same prompts to the local Codex CLI (ChatGPT plan quota, `gpt-6.1-sol`). Low effort is complete (456 calls). Over 38 series it is 86.0% estimand-correct on metadata and 89.5% with any paper text, against DeepSeek 75.4% and 84–89%.
- Ultra effort is paused at 239/456 calls (metadata complete; the paper arms cover 14 series). Resume mark and command are in `paper_evidence_ablation/REPORT.md` ("Codex as the decision model"). On the 13 matched series, ultra so far gives no gain over low at 3–7 times the time.

### B3. Metadata summary fixes (next)

- `summarize_metadata_for_llm`: keep subject-like columns (name, subject count, whether IDs recur across groups) and expose arm tokens embedded in per-sample titles or descriptions (GSE1832, GSE53598, GSE92719, GSE115645).
- Then pass title + abstract by default and Methods for design/pairing in production, and rerun the 38-series ablation as the regression check.

### C. Supplementary tables

Many papers list samples and groups only in supplementary Excel files. Download them from `supplementary_download_url` (Europe PMC returns a zip), convert each `.xlsx`/`.csv` sheet to a table block (for example `SUP2.T1`), and keep the original files for provenance.

### D. Wiring and validation

- Have `validate_decision_contract.py` warn when `paper.locator` looks like a block ID but does not resolve in the case's `.paper.json`.
- Register `read_paper_section` in `main.py` and the `paper_utility` / `sea_cdm` router profiles. Deferred because it changes the evaluated LangChain backend, and `guard_tools` caps each tool at 3 unique calls per run (the tool accepts several sections per call to work within that).
- Optional PDF upgrade for non-OA papers: GROBID or Docling behind the same document schema, only if stage B shows the PDF-only cases matter.
