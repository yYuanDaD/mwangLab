# Agent A — Implementation Review & SEA-CDM Alignment Plan

**Purpose:** Discussion doc for the mentor sync. Spells out where the current
implementation sits relative to (a) `WORKFLOW.md §3 Agent A` and (b) the
authoritative [SEA-CDM documentation](https://sea-cdm.github.io/SEA-CDM/sea-cdm_documentation/index.html),
and proposes a concrete v0 → v1 alignment path.

**Status (2026-05-27):** **v0.1** — Sprint 1 (cheap wins) shipped. End-to-end
runnable; produces one JSON record per paper at `output/agentA/{stem}.json`.
The `secondary_analysis.analysis` block and `study_extracted.study` +
`study_extracted.assays[]` blocks now use real SEA-CDM field names from
`docs/SEACDM_SCHEMA.md`; pipeline-internal metadata is segregated into clearly
labeled non-SEA-CDM subsections; Sprint 2 multi-table rewrite is still pending.

---

## 1. Authoritative sources

| Source | Location | Used for |
|---|---|---|
| Mentor's design spec | `WORKFLOW.md §3` (lines 116-145) | Agent A goal & 5-step decomposition |
| Real schema | `https://sea-cdm.github.io/SEA-CDM/sea-cdm_documentation/` | Table names + field definitions |
| Publication | `https://www.nature.com/articles/s41597-026-06558-z` | (paywall — not consulted) |
| GitHub | `https://github.com/sea-cdm/SEA-CDM` | File enumeration |

---

## 2. SEA-CDM schema reality — 13 tables

SEA = **Study / Experiment / Assay**. The data model is **relational**, not a
single nested object. The 13 tables (one HTML page per table on the docs site):

```
study          experiment    assay         analysis      results
subject        sample        groups        interventions material
occurence      documentation ontology
```

### Field details pulled so far

**`assay`** — "a process that takes one or more samples and generates data"
*(this is mentor's "SEA-A")*

| field | type | meaning |
|---|---|---|
| `assay_id` | str | primary key |
| `documentation_id` | str (FK→documentation) | protocol source |
| `assay_name` | str | e.g. `"RNA-Microarray"` |
| `assay_name_id` | str | OBI ontology id (e.g. `ECO_0000097`) |
| `assay_type` | str | `Experimental Assay` / `Observation` / `Survey` |
| `organism_input` | bool | needs biological sample? |
| `reagents` | list | consumed inputs |
| `platform` | list | non-consumed inputs (e.g. `["GPL5263"]`) |

**`analysis`** — "a planned process which transforms a data result into another data result"
*(maps directly to our `run_batch_geo_pipeline` output)*

| field | type | meaning |
|---|---|---|
| `analysis_id` | str | primary key |
| `group_id` | str (FK→groups) | which group it analyzes |
| `documentation_id` | str (FK→documentation) | protocol |
| `input_data` | str | data type used |
| `input_data_id` | str | unique id for the input |
| `file_access` | str | URL/download link |
| `analysis_name` | str | e.g. `"Differential expression"` |
| `analysis_name_id` | str | ontology id |
| `reference_source` | str | e.g. `"PMID"` |
| `reference_source_id` | str | the id value |

The other 11 tables (`study`, `experiment`, `results`, `subject`, `sample`,
`groups`, `interventions`, `material`, `occurence`, `documentation`, `ontology`)
have not been field-mapped yet — to be pulled before v1.

### Important resolutions vs mentor's WORKFLOW.md

| Mentor's term (`WORKFLOW.md`) | What it really maps to in SEA-CDM |
|---|---|
| `SEACDMRecord` (single Pydantic) | A **set of rows across 13 tables** linked by FKs |
| `sea_a_process` field | One or more `assay` rows |
| `protocol_classes: list[SEACDMClass]` | Rows in `study`/`subject`/`sample`/`groups`/`interventions`/`material`/`assay` populated from the methods section |
| `result_classes: list[SEACDMClass]` | Rows in `results` and `analysis` populated from the results section |
| `secondary_results: SecondaryResults` | Specifically `analysis` rows when GEO re-analysis was run |
| **SEA-A** (undefined in WORKFLOW.md L354) | = `assay` (the **A** in S-E-A) |
| **SEACDMClass** (undefined L113) | = any of the 13 table row types |
| **SEAProcess** (undefined L113) | likely = an `assay` row (a process taking sample → data) |

---

## 3. Current implementation = Agent A v0

### Runtime flow (what executes today)

```
keyword
  → search_papers          (Semantic Scholar; needs S2_API_KEY)
  → fetch_paper_text       (Europe PMC full-text XML; PDF fallback)
  → agent disambiguates    (OWN GSE vs cited, with snippet quoting)
  → run_batch_geo_pipeline (download → contrast detect + LLM-A → DESeq2 → GSEA → decisions.json)
  → extract_sea_cdm_conditions (study + assay-level extraction from paper text)
  → assemble_agent_a_record    (writes output/agentA/{stem}.json)
```

### Deliverable artifact

A single JSON per paper. Structure:

```json
{
  "version": "v0 — subset of SEA-CDM …",
  "paper": { "paperId", "title", "year", "pmcid", "pmid", "doi" },
  "organism": "Human" | "Mouse",
  "data_discovery": {
    "chosen_gse": "GSE…",
    "chosen_reason": "agent's tag",
    "chosen_snippet_verified": "re-derived from paper text by the tool",
    "rejected_gses": [ { "gse", "reason", "snippet_verified" } ]
  },
  "study_extracted": { /* extract_sea_cdm_conditions output */ },
  "secondary_analysis": { /* status, n_deg, design, LLM-A reasoning, deg_csv, gsea_failure */ },
  "provenance": { /* file paths for paper_text / metadata / decisions_log / summary_csv / study_seacdm */ },
  "sea_cdm_alignment_notes": "…",
  "issues": [ /* fail-loud list of anything missing */ ]
}
```

### What it covers (mapped to mentor's 5 steps)

| WORKFLOW.md §3 step | v0 coverage |
|---|---|
| 1 — Collect documentation | ✅ paper text via Europe PMC + GSE pointer |
| 2 — Identify protocols & results sections | ❌ not done (full text is one blob) |
| 3 — Extract SEA-A process | ⚠️ partial: `extract_sea_cdm_conditions` captures `assay_type` + `platform` but NOT the OBI ontology id, FK to documentation, reagents, organism_input |
| 4 — SEA-CDM classes in protocol | ⚠️ flat: `ExperimentInfo` conflates subject/groups/interventions/material into one shape |
| 5 — SEA-CDM classes in results | ❌ no `results` rows |
| Sub-loop — Analysis Agent | ✅ runs (`run_batch_geo_pipeline`), and the result is captured as `secondary_analysis` ≈ one informal `analysis` row |

### What v0 explicitly does NOT do

- Generate one row per SEA-CDM table; no FK enforcement
- OBI / EDAM / GO ontology lookups for any `*_name_id` field
- Section-level provenance (which page / which paragraph each field came from)
- Multiple `assay` rows per study (mentor's `protocol_classes: list`)
- Populating the `results` table

---

## 4. Open mentor questions

WORKFLOW.md has these TODOs that block parts of the v0 → v1 work:

| WORKFLOW.md ref | TODO | Resolution from real SEA-CDM |
|---|---|---|
| L113 | define `SEAProcess` | likely = `assay` row (or all rows in a study?) — **needs mentor confirm** |
| L113 | define `SEACDMClass` | = any of the 13 SEA-CDM table row types |
| L113 | define `Provenance`, `Issue`, `Warning` | not defined in SEA-CDM either — these are our internal concerns; **propose a shape** |
| L342 #1 | exact SEA-CDM schema | resolved — the GitHub site IS the authoritative schema |
| L354 | define **SEA-A** | = `assay` (the A in S-E-A); **needs mentor confirm** |

### Questions to ask the mentor

1. **Confirm SEA-A = `assay`** (the SEA-CDM `assay` table). Yes/no.
2. **Confirm `SEACDMClass` = "any SEA-CDM table row type"** — used as the polymorphic
   element type when listing protocol/result classes.
3. **Output container shape for v1**: do we serialize to JSON-per-table (a folder of
   13 JSON files per study), one combined JSON with 13 named arrays, or a SQLite DB
   per study? **Preference?**
4. **Ontology lookups**: which service / ontology versions to use for `*_name_id`
   fields (OBI for assays; EDAM/MeSH for analyses; etc.)? Is a stub acceptable for v1?
5. **Section identification**: is splitting the paper into "Methods" vs "Results"
   sections required for v1, or is end-of-paper holistic extraction acceptable?

---

## 5. Alignment plan: v0 → v1

Ranked by ROI (effort vs. demo-value):

### Sprint 1 — Cheap wins (≤ 1 day) — DONE 2026-05-27

- [x] **Pull all 13 table field definitions** from the SEA-CDM docs site →
      `docs/SEACDM_SCHEMA.md`. Includes the full field roster per table, an FK
      graph, and a §Notes-on-upstream-docs section flagging real inconsistencies
      I found (`occurence` vs `occurrence` spelling drift; `results.documenation_id`
      typo; `experiment.experiment_subject` field name appearing twice for both
      the string and ontology-id rows).
- [x] **Reshape `secondary_analysis` → real `analysis` row(s)** — done in
      `assemble_agent_a_record`. New shape: `secondary_analysis.analysis` carries
      the 10 SEA-CDM `analysis` fields (`analysis_id`, `input_data`, `input_data_id`,
      `file_access`, `analysis_name`, `reference_source`, `reference_source_id`,
      etc.); pipeline-internal data is split into `contrast` (design column + ctrl
      + treat), `outcome` (status / matrix_type / da_method / n_deg / n_gsea_sig /
      file paths / gsea_failure), and `decisions` (LLM-A reasoning + sex_mismatch).
      Backward-compat note: existing demo `PMC12248044.json` was re-generated;
      `input_data` / `da_method` are null because the underlying `summary.csv` was
      written before the matrix-type dispatch shipped — fresh cohorts populate them.
- [x] **Reshape `study_extracted` → real `study` + `assay` rows** — done in
      `assemble_agent_a_record`. `study_extracted.study` has the 12-field
      SEA-CDM `study` row (study_description ← objective; reference_source = "GEO");
      `study_extracted.assays[]` are 8-field SEA-CDM `assay` rows (`assay_name`,
      `assay_type=Experimental Assay`, `organism_input=true`, `platform` as a list).
      Did NOT touch the extraction tool (`extract_sea_cdm_conditions`); the
      reshape happens at assembly time, and `_extraction_source` preserves the raw
      v0 flat shape so Sprint 2's multi-table rewrite has the source intact.
      `_unmapped_fields` is an explicit list of v0 fields that belong to OTHER
      SEA-CDM tables (subject / sample / groups / interventions) — Sprint 2 will
      route them.

### Sprint 2 — Schema-faithful extraction (~ 1 week)

- [ ] Rewrite `seacdm_tools.py`: 13 Pydantic models (one per table) + 4-5
      extraction tools (`extract_study_table`, `extract_subjects_samples`,
      `extract_groups_interventions`, `extract_assays`, `extract_results`),
      each driven by `args_schema` so the LLM produces validated rows
- [ ] Add a `documentation` row per source file (paper PDF/XML, supplementary)
- [ ] Output container per mentor's preference (JSON-per-table folder /
      combined JSON / SQLite)

### Sprint 3 — Ontology + provenance (~ 1 week)

- [ ] OBI / EDAM / MeSH lookups (or stubbed `*_name_id` with TODO markers)
- [ ] Section-level provenance (which paragraph each field came from)
- [ ] Validation pass: every required SEA-CDM field present or explicitly None
      with a log entry (per mentor's L143-145 rule: "do not hallucinate")

### Out of scope for Agent A (handed off elsewhere)

- Agent B (ontology mapping → `AnnotatedSEACDMRecord`)
- Agent C (review report)
- Human review / DB ingestion

---

## 6. Demo readiness summary

| Question | Answer |
|---|---|
| Can a mentor reviewer see what Agent A does on one paper? | **Yes** — one JSON file per paper at `output/agentA/{stem}.json` |
| Does it call the Analysis sub-agent when the paper points to raw GEO data? | **Yes** — via `run_batch_geo_pipeline` |
| Does it distinguish the paper's own data from cited data? | **Yes** — with re-verified snippet quotes |
| Does the output JSON match the real SEA-CDM schema? | **No** — v0 is a subset with non-canonical field names |
| Is the gap clearly labeled? | **Yes** — `version` field + `sea_cdm_alignment_notes` field + `issues` list |

**Recommendation:** demo v0 to mentor, get answers to §4 questions, then proceed
with Sprint 1 (cheap wins) before Sprint 2 (full schema rewrite).
