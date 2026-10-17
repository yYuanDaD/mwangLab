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
- Tests: `test/unit/test_paper_structure.py` (11 cases, offline, four real Europe PMC fixtures in `test/fixtures/papers/`).
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

### PDF input (2026-10-16)

About 31 of 70 evaluated papers have no Europe PMC XML, so the PDF is their only source. `tools/pdf_markdown.py` converts a PDF to Markdown with an existing open-source converter and `paper_structure.parse_markdown` turns that Markdown into the same document schema as the JATS route.

| Backend | Licence | What it gives | Install |
|---|---|---|---|
| Docling (default when installed) | MIT | layout model and TableFormer: reading order on two-column pages, real table cells; downloads models from Hugging Face on first use | `pip install docling` |
| pymupdf4llm | AGPL | no models, fast, offline; tables from PyMuPDF's table finder | `pip install pymupdf4llm` |
| pypdf (existing fallback) | BSD | plain text, heuristic headings, no tables | core dependency |

`parse_markdown` handles converters that emit every heading at one level (numbering such as `2.1.` sets nesting; unnumbered subheadings nest under the current main section), attaches `Table N` captions to the following pipe table, makes `Figure N` paragraphs figure blocks, removes running headers and page numbers, rejoins paragraphs split by a page break, and stops at References. `structure_quality` is `pdf_markdown:docling` or `pdf_markdown:pymupdf4llm`. `fetch_paper_text` uses it automatically for PDF downloads, and also writes `<id>.converted.md`.

Tests: three new cases in `test/unit/test_paper_structure.py` (Docling-shaped Markdown, numbered headings, and both backends on `test/fixtures/papers/synthetic_two_column.pdf`). Not yet checked on real PDFs: run `python -m tools.pdf_markdown <pdfs> --out <dir>` on the PDF-only papers and compare against the JATS copies of papers that have both.

## Remaining stages

### B2. Estimand-aware scoring and pairing gold (next)

- Add an estimand axis (acute bout, training, cross-sectional) to the gold and score the axis separately from sample labels.
- Fill `covariance_annotations.csv` for the 24 frozen series and score the pairing calls.
- Rerun on all 39 eligible series before changing what evidence production passes to the validator.

### C. Supplementary tables

Many papers list samples and groups only in supplementary Excel files. Download them from `supplementary_download_url` (Europe PMC returns a zip), convert each `.xlsx`/`.csv` sheet to a table block (for example `SUP2.T1`), and keep the original files for provenance.

### D. Wiring and validation

- Have `validate_decision_contract.py` warn when `paper.locator` looks like a block ID but does not resolve in the case's `.paper.json`.
- Register `read_paper_section` in `main.py` and the `paper_utility` / `sea_cdm` router profiles. Deferred because it changes the evaluated LangChain backend, and `guard_tools` caps each tool at 3 unique calls per run (the tool accepts several sections per call to work within that).
- Optional PDF upgrade for non-OA papers: GROBID or Docling behind the same document schema, only if stage B shows the PDF-only cases matter.
