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

### B2. Estimand-aware scoring and pairing gold (in progress)

- Done: `test/validation/exergenedb_gold/estimand_annotations.json` names each series' gold axis (`acute_bout`, `training`, `habitual`), the axes its paper analyses, pairing gold per axis, and gold label corrections; `sync_covariance_annotations.py` copies the pairing gold into `covariance_annotations.csv`. `tools.contrast_gold.score_estimand_decision` scores the chosen axis separately from the labels on that axis. Rescoring the 24-series run (no new calls): every wrong call was an axis choice the paper supports or a gold error; labels on the chosen axis are 100% correct in every arm; estimand-correct is metadata 77.8%, abstract 90.3%, structured 83.3%, flat 84.7%; paper text fixes the two pairing misses of the metadata arm. See `paper_evidence_ablation/REPORT.md`.
- Next: annotate the other 15 eligible series, extend the manifest to all 39, run the four arms on the new 15 (the 24 frozen prompts are unchanged, so their calls are reused), and rescore before changing what evidence production passes to the validator.

### C. Supplementary tables

Many papers list samples and groups only in supplementary Excel files. Download them from `supplementary_download_url` (Europe PMC returns a zip), convert each `.xlsx`/`.csv` sheet to a table block (for example `SUP2.T1`), and keep the original files for provenance.

### D. Wiring and validation

- Have `validate_decision_contract.py` warn when `paper.locator` looks like a block ID but does not resolve in the case's `.paper.json`.
- Register `read_paper_section` in `main.py` and the `paper_utility` / `sea_cdm` router profiles. Deferred because it changes the evaluated LangChain backend, and `guard_tools` caps each tool at 3 unique calls per run (the tool accepts several sections per call to work within that).
- Optional PDF upgrade for non-OA papers: GROBID or Docling behind the same document schema, only if stage B shows the PDF-only cases matter.
