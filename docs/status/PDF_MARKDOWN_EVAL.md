# PDF → Markdown → structured paper: evaluation on real PDFs

Date: 2026-10-17. Branch `claude/project-thread-b6wrdv` (PR #4). No LLM calls were made.

## What was tested

- **10 papers with both a Europe PMC JATS copy and an open-access PDF**, taken from the
  `paper_evidence_ablation` manifest. The JATS copy (`python -m tools.paper_structure fetch`)
  is the reference. Journals: Int J Obesity, Frontiers in Cell Dev Biol, Physiological
  Reports (Wiley), BMC Physiology, Oncotarget, Frontiers in Physiology ×2, STAR Protocols,
  Molecular Metabolism, Science Advances.
- **7 PDF-only papers**, with no Europe PMC full-text XML (`fullTextXML` returns 500).
  Journals: J Neurosci, AJRCCM, Clinical Cancer Research (AACR), and four NIH author
  manuscripts (Br J Haematol, Am J Physiol, Nat Med 57 pp, Cell Metab 41 pp).
- **Backends:** `docling` 2.140 and `pymupdf4llm` 1.28.2 (with `pymupdf-layout`), in a separate
  venv (`requirements-skill.txt` + both packages).
- **Where the PDFs came from:** the PMC Open Access S3 bucket
  (`pmc-oa-opendata.s3.amazonaws.com`) and PDFs already cached in
  `archive/runtime/data_20260930/papers/`. Europe PMC's `?pdf=render` returns a Cloudflare
  challenge (403) to scripts. Publisher and Unpaywall links for the other candidates were
  blocked, so I did not use them.

Scripts and raw results are in `test/experiments/pdf_markdown_eval/`. The PDFs are not
committed.

Columns used below:
- **M R D**: the parsed paper has blocks classed as methods / results / data availability.
- **Table 1 cells / all tables cells**: the fraction of the JATS table's non-empty cells that
  appear in the best-matching PDF table, after normalising spaces and markup.
- **GSE**: every GSE accession in the JATS copy is found, and lands in the same section class.
- **Header leak / ref leak**: blocks that contain a running header or footer string (taken
  from the PDF page margins), or the title of a reference from the JATS reference list.
- **Timings**: wall-clock time on the owner's Windows PC with no GPU, excluding model
  download. The machine was busy (Unity was open), so treat them as approximate.

## Bugs found and fixed (all with regression tests, `test/unit/test_paper_structure.py` 16/16)

1. **OCR on by default, and page headers kept (`tools/pdf_markdown.py`).**
   - pymupdf4llm ≥1.27 installs `pymupdf-layout`. In that mode it OCRs every page that has a
     picture and keeps page headers and footers.
   - Docling also runs OCR by default.
   - On born-digital PDFs, OCR only reads axis labels from figures into the body, and costs a
     lot. On a 10-page paper, pymupdf4llm went from 202 s to 45 s, and docling from 117 s to
     48 s with identical output.
   - OCR is now off, and is retried only when the text layer comes back empty (scanned PDFs).
     Headers and footers are now off too.
2. **Paper title wrong on 8/10 (docling) and 6/10 (pymupdf4llm) papers.** The parser took the
   first heading, which was a publisher label: Frontiers "OPEN ACCESS" or "EDITED BY",
   Nature-style "ARTICLE", Wiley "O R I G I N A L A R T I C L E", the PMC "HHS Public Access"
   banner, Cell "HIGHLIGHTS", or the "Protocol" page banner. Front-matter headings now give the
   title as the largest one, and publisher labels are skipped. A long title that contains a
   section word ("…in Pediatric **Patients**") is no longer taken for Methods.
3. **Everything after References was dropped.** That loses Nature/Cell **Methods** and
   **data availability** printed after the reference list, and NIH author manuscripts' **tables
   and figures**. The reference list is now skipped and parsing resumes at one of those
   sections. Floats go to a `FLT` "Figures and tables" section, as in the JATS route.
4. **Science's "REFERENCES AND NOTES" heading was not recognised**, so 42 reference blocks
   leaked into the last section (PMC9451165).
5. **A Results subsection was treated as Methods.** "Anthropometric … Characteristics of
   **Participants**" opened a new Methods section, so the rest of Results was classed as
   methods (PMC7298138, both backends). Now only a heading that names methods or materials
   opens a Methods section.
6. **Table labels detached from their tables.** Docling emits "Table 2." as a heading and the
   caption as a separate paragraph. That produced an empty image-only table and left the real
   table unlabelled.
7. **Smaller fixes:**
   - Cell Press logo glyph "ll" headings are dropped.
   - Link targets and HTML tags are removed from heading text.
   - Wiley "2 | METHODS" and "K E YWO R D S" are normalised.
   - Data-availability titles left as plain lines are recognised, and Elsevier "Data
     statement" counts as data availability.
   - Docling's HTML entities (`&amp;`) and stray control characters (NUL) are cleaned.
   - pymupdf4llm "picture text" spans (words inside figures) are dropped.
   - `<sup>`, `<sub>` and `<br>` become `^`, `_` and spaces.
   - Docling's one-cell "tables" (Wiley author lines) become paragraphs.
8. **Glyph loss.**
   - On PMC7298138, docling turned every "±" (70 of them) into U+FFFD, including the
     participant table (mean ± SEM).
   - `auto` now also runs pymupdf4llm when docling's output has ≥10 U+FFFD, and keeps the
     cleaner one. On that paper it picks pymupdf4llm (0 lost, 33 "±"); on clean papers it
     stays with docling.

Effect of the parser fixes on the same converted Markdown (`compare_old.py`):

| backend | parser | titles ok (10 JATS papers) | M/R/D found vs JATS | GSE found vs JATS | tables with cells (17 papers) | of which labelled |
|---|---|---|---|---|---|---|
| docling | before (8216daa) | 2/10 | 22/23 | 36/36 | 24 | 17 |
| docling | after | 10/10 | 23/23 | 36/36 | 25 | 21 |
| pymupdf4llm | before (8216daa) | 4/10 | 21/23 | 36/36 | 19 | 16 |
| pymupdf4llm | after | 9/10 | 23/23 | 36/36 | 27 | 16 |

The "before" rows already use the OCR-off conversions. With the original defaults, the
pymupdf4llm Markdown also carried page headers and OCR'd figure text.

## Results (after the fixes)

### Totals

| backend | conversions | median s/paper (run 1 / run 2) | M/R/D found vs JATS | JATS tables with cells matched ≥0.8 | GSE found / same class | ref-leak blocks | titles ok |
|---|---|---|---|---|---|---|---|
| docling | 17/17 | 26 / 58 | 23/23 | 11/14 | 36/36 / 35/36 | 0 | 10/10 |
| pymupdf4llm | 17/17 | 33 / 40 | 23/23 | 12/14 | 36/36 / 35/36 | 0 | 9/10 |

Notes on the totals:
- The one GSE in a different section class (GSE144134 in PMC8355925) is not an error. JATS
  nests the "Data statement" under Discussion, and the PDF route now classes it as data
  availability.
- Header-leak hits (8 per backend) are all legitimate front-matter citation lines, such as
  "Front. Cell Dev. Biol. 11:1199…" or the journal/DOI line. The JATS copy of PMC9811128 scores
  4 on the same check, so these are false positives of the metric, not running headers.

### Papers with JATS (per paper)

| paper | source | sec | pages | M R D | tables (with cells) | Table 1 cells | all tables cells | GSE in JATS: found / same class | header leak | ref leak | title |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **PMC10113153** Int J Obes | JATS | – | 12 | M R D | 0 | – | – | GSE161749, GSE161750, GSE208032 (methods); GSE224310 (DA) | – | – | – |
| | docling | 57.7 | | M R D | 0 | – | – | 4/4 / 4/4 | 1 | 0 | ok |
| | pymupdf4llm | 34.8 | | M R D | 0 | – | – | 4/4 / 4/4 | 0 | 0 | ok |
| **PMC10318136** Front Cell Dev Biol | JATS | – | 13 | M R D | 0 | – | – | GSE229755 (DA) | – | – | – |
| | docling | 23.8 | | M R D | 0 | – | – | 1/1 / 1/1 | 1 | 0 | ok |
| | pymupdf4llm | 23.2 | | M R D | 0 | – | – | 1/1 / 1/1 | 1 | 0 | ok |
| **PMC10984804** Physiol Rep (Wiley) | JATS | – | 9 | M · · | 2 (2) | – | – | GSE163356 (other) | – | – | – |
| | docling | 25.7 | | M · · | 2 (2) | 0.92 | 0.81 | 1/1 / 1/1 | 0 | 0 | ok |
| | pymupdf4llm | 50.7 | | M · · | 2 (2) | 0.92 | 0.81 | 1/1 / 1/1 | 0 | 0 | ok |
| **PMC3681679** BMC Physiol | JATS | – | 11 | M R · | 6 (6) | – | – | GSE46075 (methods) | – | – | – |
| | docling | 26.5 | | M R · | 6 (6) | 0.89 | 0.97 | 1/1 / 1/1 | 0 | 0 | ok |
| | pymupdf4llm | 82.7 | | M R · | 6 (6) | 1.00 | 0.89 | 1/1 / 1/1 | 0 | 0 | ok |
| **PMC4621892** Oncotarget | JATS | – | 21 | M R · | 3 (3) | – | – | GSE64607 (methods) | – | – | – |
| | docling | 73.9 | | M R · | 3 (3) | 0.85 | 0.89 | 1/1 / 1/1 | 0 | 0 | ok |
| | pymupdf4llm | 210.0 | | M R · | 3 (3) | 0.93 | 0.92 | 1/1 / 1/1 | 0 | 0 | ok |
| **PMC7298138** Front Physiol | JATS | – | 15 | M R D | 2 (2) | – | – | GSE144627 (methods) | – | – | – |
| | docling | 58.3 | | M R D | 2 (2) | 0.50 ¹ | 0.53 ¹ | 1/1 / 1/1 | 0 | 0 | ok |
| | pymupdf4llm | 146.8 | | M R D | 2 (2) | 1.00 | 1.00 | 1/1 / 1/1 | 0 | 0 | ok |
| **PMC7868630** STAR Protocols | JATS | – | 14 | M · D | 1 (1) | – | – | GSE117161 (DA, key resources table) | – | – | – |
| | docling | 78.6 | | M · D | 1 (1) | – | 1.00 | 1/1 / 1/1 | 0 | 0 | ok |
| | pymupdf4llm | 82.9 | | M · D | 1 (1) | – | 1.00 | 1/1 / 1/1 | 0 | 0 | ok |
| **PMC8355925** Mol Metab | JATS | – | 13 | M R · | 0 | – | – | 20 GSE (19 results, 1 discussion) | – | – | – |
| | docling | 60.4 | | M R D | 0 | – | – | 20/20 / 19/20 ² | 0 | 0 | ok |
| | pymupdf4llm | 39.5 | | M R D | 0 | – | – | 20/20 / 19/20 ² | 0 | 0 | ok |
| **PMC9451165** Sci Adv | JATS | – | 14 | M R · | 0 | – | – | 5 GSE (methods/results) | – | – | – |
| | docling | 38.7 | | M R · | 0 | – | – | 5/5 / 5/5 | 0 | 0 | ok |
| | pymupdf4llm | 52.3 | | M R · | 0 | – | – | 5/5 / 5/5 | 0 | 0 ³ | ok |
| **PMC9811128** Front Physiol | JATS | – | 10 | M R D | 0 | – | – | GSE219100 (DA/methods) | 4 ⁴ | – | – |
| | docling | 36.4 | | M R D | 0 | – | – | 1/1 / 1/1 | 6 ⁴ | 0 | ok |
| | pymupdf4llm | 17.3 | | M R D | 0 | – | – | 1/1 / 1/1 | 6 ⁴ | 0 | ✗ ⁵ |

1. Docling's table structure is exactly right, but every "±" became U+FFFD. `auto` now
   switches this paper to pymupdf4llm (fix 8).
2. "Data statement" is classed as data availability in the PDF route (see Totals).
3. Before fix 4 there were 42 ref-leak blocks here.
4. False positive: the author names and journal also appear in the citation line.
5. pymupdf4llm did not mark the Frontiers title as a heading, so there is nothing to recover.

### PDF-only papers

| paper | backend | sec | pages | M R D | tables (with cells) | figures | GSE found (section class) | title |
|---|---|---|---|---|---|---|---|---|
| GSE217487 J Neurosci | docling | 79.3 | 15 | M R D | 2 (2) | 5 | GSE217487 (DA) | ok |
| | pymupdf4llm | 29.8 | 15 | M R D | 2 (2) | 5 | GSE217487 (DA) | ok |
| GSE241016 AJRCCM | docling | 88.1 | 11 | M R · | 3 (2) | 4 | none (paper cites no GSE) | ok |
| | pymupdf4llm | 22.5 | 11 | M R · | 2 (2) | 4 | none | ok |
| GSE244401 Br J Haematol (NIH AM) | docling | 122.6 | 18 | M R · | 5 (4) | 1 | GSE244401 (methods) | ok |
| | pymupdf4llm | 30.2 | 18 | M R · | 7 (5) ⁶ | 1 | GSE244401 (methods) | ok |
| GSE295777 Am J Physiol (NIH AM) | docling | 26.4 | 16 | M R D | 0 | 4 | GSE295777 (DA) | ok |
| | pymupdf4llm | 18.8 | 16 | M R D | 0 | 4 | GSE295777 (DA) | ok |
| PMC10618653 Clin Cancer Res | docling | 52.6 | 12 | M R D | 1 (1) | 5 | GSE183150, GSE210011 (DA) | ok |
| | pymupdf4llm | 25.0 | 12 | M R D | 1 (1) | 5 | GSE183150, GSE210011 (methods) ⁷ | ok |
| PMC6858591 Nat Med (NIH AM) | docling | 110.2 | 57 | M R D | 0 | 6 | GSE110639, GSE124799 (DA, methods) | ok |
| | pymupdf4llm | 126.6 | 57 | M R D | 0 | 6 | GSE110639, GSE124799 (DA, methods) | ok |
| PMC9558082 Cell Metab (NIH AM) | docling | 140.6 | 41 | M R D | 3 (2) | 6 | GSE183239, GSE183288, GSE183290 (DA) | ok |
| | pymupdf4llm | 161.0 | 41 | M R D | 3 (3) | 6 | GSE183239, GSE183288, GSE183290 (DA) | ok |

6. Three of these are prose from a landscape table page that pymupdf4llm boxed as tables.
7. Reading-order error: on this two-column page pymupdf4llm put the "Data availability"
   heading before unrelated text, so the accession sentence fell under Methods. Docling got
   the order right.

Before the fixes, both backends lost all four tables of GSE244401 (they are printed after the
references), and the Nat Med and Cell Metab methods and data-availability sections that come
after the reference list.

## What still is not handled

- **Glyphs:**
  - Both backends lose the minus sign in the AACR font. pymupdf4llm marks it with U+FFFD;
    docling silently writes "kg 1" for kg⁻¹.
  - pymupdf4llm leaves U+FFFD on 6/17 papers, mostly ©, minus and superscript daggers;
    docling on 1/17.
  - Numbers next to these symbols need checking against the PDF.
- **Tables printed as images** cannot be read without table OCR; neither backend is set to do
  it. They stay as "image only" table blocks with their caption.
- **Two-line headings** that pymupdf4llm splits into two headings leave an empty section
  (PMC7298138 "…Circulating ExomiR" / "Profiles at Baseline").
- **STAR Protocols layout** (Before you begin / Step-by-step / Troubleshooting) is classed
  methods/abstract/other; JATS classes most of it as other.
- **Timings** were measured on a busy desktop (two runs, different background load), so treat
  them as relative.

## Recommendation: keep docling as the default (`auto` = docling, then pymupdf4llm)

On section recall and GSE recall the two backends tie after the parser fixes: 23/23 sections
and 36/36 accessions each. The default should be docling because:

- **Reading order.** Docling got the two-column AACR page right; pymupdf4llm misplaced the
  data-availability heading. Where an accession sits decides which data the workflow trusts.
- **Fewer fake tables.** Docling produced no prose-as-table blocks in this set; pymupdf4llm boxed three
  landscape-page paragraphs as tables and once put a caption inside a cell. Its tables match
  JATS as well (11/14 ≥0.8 vs 12/14). The one docling miss was the "±" glyph problem, which
  `auto` now detects and routes to pymupdf4llm.
- **Titles:** 10/10 vs 9/10.
- **Licence.** Docling is MIT; pymupdf4llm is AGPL, which matters if this is ever served to
  others.
- **Speed is a wash.** About 1.5–3 s per page for both with OCR off (medians 26/58 s vs
  33/40 s per paper across the two runs). Docling adds roughly 30 s of model loading once per
  process.

The price of docling:
- a much larger install (torch);
- a Hugging Face model download on first use (on Windows without Developer Mode the cache
  falls back to copies instead of symlinks);
- slower conversion of long author manuscripts (57-page Nat Med 110 s, 41-page Cell Metab
  141 s; pymupdf4llm took 127 s and 161 s on the same machine in the same run).

pymupdf4llm stays the fallback, and is fine as the only backend on a machine where torch is
unwanted. The parser fixes above apply to both.

## Reproduce

```bash
python -m venv .venv-pdf && .venv-pdf/Scripts/python -m pip install -r requirements-skill.txt pymupdf4llm docling
python test/experiments/pdf_markdown_eval/download_pmc_oa_pdfs.py <root>/both PMC7868630 PMC9451165 ...
python test/experiments/pdf_markdown_eval/run_eval.py <root> pymupdf4llm
python test/experiments/pdf_markdown_eval/run_eval.py <root> docling
python test/experiments/pdf_markdown_eval/table.py <root>/results_pymupdf4llm.json <root>/results_docling.json
```
