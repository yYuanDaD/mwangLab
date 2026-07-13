# SEA-CDM Schema Reference (13 tables)

**Source:** `https://sea-cdm.github.io/SEA-CDM/sea-cdm_documentation/` — pulled 2026-05-27.

**Purpose:** Single reference for the v0 → v1 Agent A alignment work (`docs/reviews/REVIEW_NOTES_AGENT_A.md` Sprint 1+2). All field names below are LITERAL from the upstream docs — typos and inconsistencies preserved (see §Notes-on-upstream-docs at the bottom).

**SEA** = **S**tudy / **E**xperiment / **A**ssay — the three central nouns. The 13 tables form a relational graph; most non-central tables FK into one or more of `study` / `experiment` / `documentation`.

---

## Table inventory

| # | Table | Purpose (one line) |
|---|---|---|
| 1 | `study` | Top-level scientific investigation answering one question |
| 2 | `experiment` | A controlled / observational unit within a study; central node of the model |
| 3 | `assay` | A process that takes sample(s) and produces data |
| 4 | `analysis` | A planned process that transforms a data result into another data result |
| 5 | `results` | Data items generated from an assay or analysis |
| 6 | `subject` | An organism participating in an experiment |
| 7 | `sample` | A biosample or experimental sample derived from a subject |
| 8 | `groups` | A collection of subjects/samples sharing experimental characteristics |
| 9 | `interventions` | Records of an organism being exposed to a material entity |
| 10 | `material` | A material entity used in an experiment (non-organism) |
| 11 | `occurence` | Events affecting an organism (disease, pregnancy, adverse event). [sic — spelled `occurence` upstream] |
| 12 | `documentation` | Registry of all study-related documents (papers, protocols, results files) |
| 13 | `ontology` | Repository of ontologies referenced by `*_name_id` columns across the model |

---

## FK graph (informal)

```
                       documentation ── ontology
                              │
                              ├──── study ──── experiment ──── subject
                              │                  │                │
                              │                  │              sample
                              │                  │                │
                              │                  ├──── groups ────┤
                              │                  │                │
                              │                  ├──── interventions (→ subject, → experiment)
                              │                  │
                              │                  ├──── assay (→ documentation)
                              │                  │
                              │                  └──── analysis (→ group, → documentation)
                              │                              │
                              └──── results (→ experiment, sample, subject, documentation)
                                                 │
                                            (datatype, file_access...)

  occurence → subject
  material  → (referenced by interventions.material_name_id and assay.reagents/platform lists)
```

Notes:
- `documentation` is a sink for almost every table — most tables can cite a protocol document.
- `analysis.group_id` references `groups`; `analysis.input_data_id` is a string id of the input data (not strictly a typed FK in the upstream docs).
- `results` carries FKs to `experiment`, `sample`, `subject`, `documentation`.
- Several tables have ontology stub fields (`*_name_id`, `*_type_id`, `*_unit_id`) that point at terms registered in the `ontology` table.

---

## 1. `study`

**DEFINITION:** A planned process intended to answer a scientific question through multiple experiments or observational studies.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| study_id | String | Primary key | — |
| study_name | String | Name of the study | — |
| study_description | String | Short description (≤500 chars) of the key scientific question | — |
| study_type | String | Category (e.g. Clinical Investigation, Experimental Study) | — |
| study_type_id | String (Ontology) | Ontology identifier for study type | — |
| study_focus | String | Intended focus (e.g. Immune Response, Vaccine Response) | — |
| study_focus_id | String (Ontology) | Ontology identifier for study focus | — |
| study_keywords | String | Keywords for diseases/qualities relevant to the study | — |
| study_keyword_id | String (Ontology) | Ontology identifier for study keywords | — |
| reference_source_id | String | External ID from another system | — |
| reference_source | String | Name of external reference (e.g. ImmPort) | — |
| comments | String | Free-text notes | — |

---

## 2. `experiment`

**DEFINITION:** Central node of the SEA model. An experiment can include clinical visits or experimental controls.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| experiment_id | string | Primary key | — |
| study_id | string | Study this experiment belongs to | study |
| documentation_id | string | Document describing the experiment protocol | documentation |
| experiment_control | boolean | True if this row represents a control | — |
| experiment_type | string | Type of experiment performed | — |
| experiment_type_id | string | Ontology id matching `experiment_type` | — |
| experiment_subject | string | Type of subject used in the experiment | — |
| experiment_subject_id | string | Ontology id matching `experiment_subject` [field name inferred — upstream docs duplicate `experiment_subject` for the id row] | — |
| reference_source_id | string | External id from another system | — |
| reference_source | string | Name of the external system | — |
| comments | string | Free-text notes | — |

---

## 3. `assay` (this is the "A" in SEA / "SEA-A")

**DEFINITION:** A defined process that accepts one or more samples as input and produces measurable data as output.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| assay_id | String | Primary key | — |
| documentation_id | String | Document describing the assay process | documentation |
| assay_name | String | General name (e.g. `"RNA-Microarray"`, `"Bulk RNA-Seq"`) | — |
| assay_name_id | String | OBI ontology identifier | — |
| assay_type | String | Category: experimental / observational / survey | — |
| organism_input | Boolean | True if the assay requires an organism specimen | — |
| reagents | List\<String\> | `material_id`s consumed during the assay | material |
| platform | List\<String\> | `material_id`s used but not consumed (e.g. GPL5263) | material |

---

## 4. `analysis`

**DEFINITION:** A planned process that transforms a data result into another data result via computational/statistical means. Each analysis is derived from an assay.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| analysis_id | String | Primary key | — |
| group_id | String | Group this analysis concerns | groups |
| documentation_id | String | Document describing the analysis protocol | documentation |
| input_data | String | Data type(s) used as input | — |
| input_data_id | String | Unique identifier for the input data | — |
| file_access | String | Download URL for the input data | — |
| analysis_name | String | Type of analysis (e.g. `"Differential expression"`) | — |
| analysis_name_id | String | Ontology id for the analysis name | — |
| reference_source_id | String | External reference id | — |
| reference_source | String | Source system for the reference | — |

---

## 5. `results`

**DEFINITION:** Data items generated from an assay or from analysis of an assay.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| results_id | string | Primary key | — |
| experiment_id | string | Experiment containing this result | experiment |
| group_id | string | Group this result concerns | groups |
| sample_id | string | Sample id; use `"1"` placeholder for group-level results | sample |
| subject_id | string | Subject (organism) id; use `"1"` placeholder for group-level results | subject |
| documenation_id | string | Document associated with the result [sic — `documenation_id` is the literal field name; upstream typo] | documentation |
| analysis_type | string | Analysis method that produced the result | — |
| original_assay_type | string | Original assay type (always "experimental assay") | — |
| original_assay_type_ID | string | Ontology id for the assay type | — |
| datatype | string | Data result type (e.g. Image, Spreadsheet) | — |
| datatype_ID | string | Ontology id for `datatype` | — |
| dataset_size | string | Size of the result (string to fit matrix/hierarchical shapes) | — |
| file_access | string | URL/path where the result file is accessible | — |
| file_type | string | File extension | — |
| replications | integer | Count of repeated analyses generating this data | — |

---

## 6. `subject`

**DEFINITION:** Registry of all study subjects (organisms) within an experiment.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| subject_id | string | Primary key | — |
| experiment_id | string | Experiment this subject belongs to | experiment |
| group_id | string | Group this subject belongs to (singletons use `1`) | groups |
| subject_type | string | General classification (e.g. Organism, Cell Line) | — |
| subject_type_id | string | Ontology id for `subject_type` | — |
| species | string | Species (cell lines list original species) | — |
| species_id | string | Ontology id for species | — |
| organism_race | string | Race / population grouping (humans only) | — |
| organism_race_id | string | Ontology id for `organism_race` | — |
| subject_lineage | string | Subtype classification | — |
| subject_lineage_id | string | Ontology id for `subject_lineage` | — |
| organism_age | double | Lowest age value (requires paired unit fields) | — |
| organism_age_unit | string | Unit for `organism_age` | — |
| organism_age_unit_id | string | Ontology id for the age unit | — |
| organism_sex | string | Biological sex | — |
| organism_sex_id | string | Ontology id for sex | — |
| reference_source_id | string | External id | — |
| reference_source | string | External source name | — |
| comments | string | Free-text notes | — |

---

## 7. `sample`

**DEFINITION:** Experimental data collected from an organism — both the initial biosample (tissue or cell culture) and any further processed expsample derivatives used in assays.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| sample_id | string | Primary key | — |
| organism_id | string | Subject this sample came from; `'0'` indicates multiple organisms | subject |
| group_id | string | Group of subjects this sample originated from | groups |
| biosample_collection | string | Method used to collect the sample | — |
| biosample_collection_id | string | Ontology id for the collection method | — |
| collection_date | string | Date of collection | — |
| collection_datetime | string | Datetime of collection | — |
| biosample_type | string | Source tissue / material | — |
| biosample_type_id | string | Ontology id for `biosample_type` | — |
| biosample_reference_source | string | Documentation source for the biosample | — |
| biosample_reference_source_id | string | Source-specific identifier for the biosample | — |
| expsample_type | string | Final processed specimen type used in the assay | — |
| expsample_type_id | string | Ontology id for `expsample_type` | — |
| expsample_reference_source | string | Documentation source for expsample ontology | — |
| expsample_reference_source_id | string | Source-specific id for the experimental sample | — |
| comments | string | Free-text notes | — |

---

## 8. `groups`

**DEFINITION:** A collection of subjects/samples sharing common experimental characteristics — may span multiple organisms (for observations) or samples (for assays).

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| group_id | string | Primary key | — |
| subject_group | string | Original set of subjects used as a group | — |
| subject_group_type_id | string | Ontology id for the subject set | — |
| sample_group | string | Sample types derived from organisms in the group | — |
| sample_group_type_id | string | Ontology id for the sample group classification | — |
| group_size | integer | Count of organisms in the group | — |
| min_group_age | double | Youngest age in the group | — |
| min_age_unit | string | Unit for `min_group_age` (e.g. Day, Year) | — |
| min_age_unit_id | string | Ontology id for the min-age unit | — |
| max_group_age | double | Oldest age in the group | — |
| max_age_unit | string | Unit for `max_group_age` | — |
| max_age_unit_id | string | Ontology id for the max-age unit | — |
| reference_source | string | External source name | — |
| reference_source_id | string | External id for the group | — |
| comments | string | Free-text notes | — |

---

## 9. `interventions`

**DEFINITION:** Records of an experimental exposure — one organism being exposed to one material entity (with dosage, route, timing).

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| intervention_id | string | Primary key | — |
| experiment_id | string | Experiment this intervention belongs to | experiment |
| subject_id | string | Subject receiving the intervention | subject |
| material | string | Name of the material administered | — |
| material_name_id | string | Ontology id for the material | material |
| dosage | decimal | Quantity of material administered | — |
| dosage_unit | string | Unit for `dosage` | — |
| dosage_unit_id | string | Ontology id for the dosage unit | — |
| intervention_type | string | Intervention category | — |
| intervention_type_id | string | Ontology id for `intervention_type` | — |
| intervention_route | string | Administration pathway | — |
| intervention_route_id | string | Ontology id for the route | — |
| t0_definition | string | Definition of the baseline time point | — |
| intervention_time | decimal | Duration after T0 when the intervention occurred | — |
| time_unit | string | Unit for `intervention_time` | — |
| time_unit_id | string | Ontology id for the time unit | — |
| reference_source_id | string | External reference id | — |
| reference_source | string | Source system | — |
| comments | string | Free-text notes | — |

---

## 10. `material`

**DEFINITION:** Any material entity used in an experiment / assay (with an associated dose) that doesn't fit the organism classification.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| material_id | String | Primary key | — |
| material_name | String | Descriptive name of the material | — |
| material_name_id | String | Ontology id for the material name | — |
| organization | String | Organization responsible for creation / refinement | — |
| reference_source_id | String | External reference id | — |
| reference_source | String | Source type of the reference id | — |

---

## 11. `occurence`

**DEFINITION:** An event affecting an organism throughout its existence — disease, pregnancy, adverse events (lethal or otherwise).

[Spelled `occurence` (one r) in table-name and file-name; field names use BOTH `occurrence_*` and `occurence_*` — preserved as-is below.]

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| occurrence_id | string | Primary key [sic — table is `occurence`, key is `occurrence_id`] | — |
| subject_id | string | Subject the event concerns | subject |
| occurrence_name | string | Reported summary of the event | — |
| occurrence_name_id | string | Ontology id for the event | — |
| occurrence_severity | integer | CTCAE-like 0–5 severity (0 = benign) | — |
| occurence_onset_date | string | Onset date [sic] | — |
| occurence_onset_datetime | string | Onset datetime [sic] | — |
| occurrence_end_date | string | End date | — |
| occurence_end_datetime | string | End datetime; blank if ongoing [sic] | — |
| occurence_ongoing | boolean | True if chronic / persistent [sic] | — |
| reference_source_id | string | Event id in another dataset | — |
| reference_source | string | Source system | — |
| comments | string | Free-text notes | — |

---

## 12. `documentation`

**DEFINITION:** Comprehensive registry for all study-related materials — data types, protocols, papers, results files. Each row is linked to its parent study.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| documentation_id | string | Primary key | — |
| study_id | string | Study this document belongs to | study |
| document_name | string | Title / name of the document | — |
| documentation_type | string | Category (protocol, paper, results, etc.) | — |
| documentation_type_id | string | Ontology id for `documentation_type` | — |
| documentation_file_access | string | URL or file path to the document | — |
| reference_source | string | Origin system / database (e.g. PubMed) | — |
| reference_source_id | string | External id paired with `reference_source` | — |
| citation | string | Full bibliographic citation | — |
| citation_style | string | Citation format standard (e.g. NLM) | — |
| creator_id | string | Identifier for the creator's role | — |
| creator_id_type | string | Type of identifier used to identify the person/org | — |
| creator_role | string | Role designation (author, reporting agent, etc.) | — |
| creator_role_id | string | OBI ontology code for the creator role | — |

---

## 13. `ontology`

**DEFINITION:** Repository of ontologies referenced elsewhere in the model via `*_name_id` / `*_type_id` columns. Enables direct querying to associate identifiers with knowledge graphs.

| field_name | data_type | description | foreign_key_target |
|---|---|---|---|
| ontology_id | String | Primary key | — |
| documentation_id | String | Linked documentation | documentation |
| ontology_name | String | Common name (e.g. "Ontology of Biomedical Investigations") | — |
| ontology_iri | String | IRI string identifying ontology terms (e.g. `http://purl.obolibrary.org/obo/OBI`) | — |

---

## Notes on upstream docs

The published SEA-CDM docs (as of 2026-05-27) have several internal inconsistencies preserved above for fidelity. When we eventually instantiate Pydantic models for v1, we should:

1. **`occurence` vs `occurrence`** — table and file are `occurence` (one r), but several field names use `occurrence_*` (correct spelling) while others use `occurence_*` (matching the typo). Mentor question: pick one normalized form for our Python models?
2. **`results.documenation_id`** (missing one "t") — almost certainly a doc typo; our model should call it `documentation_id` for cross-table consistency, with a renamer if SEA-CDM exporters expect the literal field.
3. **`experiment.experiment_subject` appears twice** — once as the string field, once (incorrectly) as the ontology id field. The second is almost certainly meant to be `experiment_subject_id`.
4. **`results` table FK named `subject_id`** but the column description says "organism" — `subject_id` is the right name (matches `subject` table key).
5. **Ontology stub fields are pervasive** — virtually every `*_name`, `*_type`, `*_unit` field has a paired `*_id` ontology pointer. For v1 we likely emit `None` for these and queue them as TODO unless ontology lookup is implemented (see REVIEW_NOTES §4 question 4).
6. **No required/optional markers in the docs** — every field's nullability is unspecified. Mentor question (informal): is every field optional except primary keys + FKs?

These are the items to fold into mentor sync §4. SCHEMA.md will be re-pulled and reconciled with any v0.5+ docs release.
