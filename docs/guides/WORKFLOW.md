# Exercise Database Construction — Agent Workflow Specification

> This document is the **single source of truth** for the AI-agent-assisted
> workflow that builds the Exercise Database. All code must conform to
> the contracts defined here. When in doubt, update this document first,
> then the code.

---

## 0. System Overview

This system ingests heterogeneous study documentation (papers, protocols,
public-repository data) and produces an **ontology-annotated, SEA-CDM-formatted
exercise database** ready for downstream Exercise-KG construction.

The system is composed of three sequential agents plus a human review step:

```
Inputs ──► [A] Study Curation ──► [B] Ontology Mapping ──► [C] Review ──► Human Expert ──► Final DB
                  │
                  └── (if secondary results needed) ──► [Analysis Agent ↔ Coding Agent] sub-loop
```

---

## 1. Inputs

The system accepts the following input types per study:

| Input            | Format            | Source                                  | Required |
| ---------------- | ----------------- | --------------------------------------- | -------- |
| Articles / PDFs  | `.pdf`            | User upload                             | Yes      |
| Protocols & Supp | `.pdf`, `.docx`   | User upload                             | No       |
| Public repo data | GEO/PRIDE IDs     | NCBI GEO, EBI PRIDE, ...                | No       |
| Study metadata   | `.json` / `.yaml` | User-provided                           | Yes      |
| Web & guidelines | URL list          | User-provided                           | No       |

<!-- TODO: confirm exact accepted file types and any size limits -->

---

## 2. Core Data Models

All inter-agent communication uses these Pydantic v2 models.
Defined in `src/models/`.

### 2.1 `StudyDocumentation`
Raw bundle of everything we know about a study before processing.

```python
class StudyDocumentation(BaseModel):
    study_id: str
    pdfs: list[Path]
    protocols: list[Path]
    repo_accessions: list[str]   # e.g. ["GSE123456"]
    metadata: dict
    urls: list[HttpUrl]
```

### 2.2 `SEACDMRecord`
The structured study record. <!-- TODO: paste the actual SEA-CDM schema here.
This is the most important contract in the whole system. Without it nothing
downstream is well-defined. -->

```python
class SEACDMRecord(BaseModel):
    study_id: str
    sea_a_process: SEAProcess          # extracted in Step 3
    protocol_classes: list[SEACDMClass] # extracted in Step 4
    result_classes: list[SEACDMClass]   # extracted in Step 5
    secondary_results: SecondaryResults | None  # from Analysis sub-loop
    provenance: Provenance              # who/what produced each field
```

### 2.3 `OntologyMapping`
A single term-to-ontology-entity mapping with evidence.

```python
class OntologyMapping(BaseModel):
    source_term: str
    ontology: Literal["EXAO", "EXMO", "OPE", "GO", "MONDO",
                      "Reactome", "HPO", "DRON", "DrugBank",
                      "FOODON", "ONS", "OBI", "OPMI"]
    ontology_id: str          # e.g. "GO:0008150"
    label: str
    confidence: float         # 0.0–1.0
    evidence: str             # why we believe this match
    method: Literal["exact", "synonym", "semantic", "manual"]
```

### 2.4 `AnnotatedSEACDMRecord`
SEA-CDM record after Agent B finishes.

```python
class AnnotatedSEACDMRecord(SEACDMRecord):
    mappings: list[OntologyMapping]
```

### 2.5 `ReviewReport`
Output of Agent C.

```python
class ReviewReport(BaseModel):
    record_id: str
    missing_fields: list[str]
    inconsistencies: list[Issue]
    uncertain_mappings: list[OntologyMapping]   # below confidence threshold
    quality_warnings: list[Warning]
    passed_checks: list[str]
    overall_status: Literal["ready_for_human", "needs_rework"]
```

<!-- TODO: define `SEAProcess`, `SEACDMClass`, `Provenance`, `Issue`, `Warning`. -->

---

## 3. Agent A — Study Curation Agent

**Goal:** Turn a `StudyDocumentation` into a `SEACDMRecord`.

**Steps (from the diagram):**

1. **Collect documentation** — gather all materials about the study.
2. **Identify protocols & results** — locate the protocol sections and the
   results sections within the documents.
3. **Extract SEA-A process** from protocols.
4. **Identify SEA-CDM classes** present in the experiment protocol.
5. **Characterize SEA-CDM classes** listed in results.

**Sub-loop trigger (Step 2 → Analysis Agent):**
If Step 2 determines that secondary analysis is needed (e.g. the paper
references raw GEO data that must be re-analyzed to populate result fields),
invoke the Analysis + Coding sub-agents (Section 6).

**Interface:**

```python
class StudyCurationAgent:
    def run(self, docs: StudyDocumentation) -> SEACDMRecord: ...
```

**Quality bar:**
- Every extracted field must carry provenance (which document, which page/section).
- If a required SEA-CDM field cannot be filled, leave it `None` and log it —
  do **not** hallucinate.

<!-- TODO: which LLM? Same model across all steps, or step-specific? -->
<!-- TODO: do we want few-shot examples per step? -->

---

## 4. Agent B — Ontology Mapping Agent

**Goal:** Turn a `SEACDMRecord` into an `AnnotatedSEACDMRecord`.

**Step 6 has two phases:**

### 4.1 Phase 1 — Select appropriate ontologies
Choose from:

- Exercise/Physical Activity: EXAO, EXMO, OPE
- Gene: GO
- Disease: MONDO
- Pathway: Reactome
- Phenotype: HPO
- Drug: DRON, DrugBank
- Diet/Nutrition: FOODON, ONS
- Other domain: OBI, OPMI

<!-- TODO: ontology source — local OWL files? OLS API? BioPortal? -->

### 4.2 Phase 2 — Map terms to ontology entities
For each candidate term in the SEA-CDM record:

1. **Entity recognition & normalization**
2. **Synonym expansion**
3. **Semantic similarity matching** (embedding-based)
4. **Assign ontology ID**
5. **Record mapping evidence & confidence**

**Interface:**

```python
class OntologyMappingAgent:
    def run(self, record: SEACDMRecord) -> AnnotatedSEACDMRecord: ...
```

**Confidence policy:**
- `≥ 0.85` → auto-accept
- `0.60–0.85` → flag as uncertain, send to Agent C
- `< 0.60` → leave unmapped, log as missing

<!-- TODO: confirm thresholds with domain expert -->
<!-- TODO: which embedding model? local (e.g. BioBERT) or hosted? -->

---

## 5. Agent C — Review Agent

**Goal:** Produce a `ReviewReport` and decide whether the record is ready
for human review.

**Step 7 — Characterize remaining documentation:**
- Extract missing information from any docs not yet processed
- Capture notes & comments
- Link additional files to the record

**Step 8 — Verify no missing information:**
Run these checks against the AnnotatedSEACDMRecord:

| Check                      | Description                                              |
| -------------------------- | -------------------------------------------------------- |
| Completeness               | All required SEA-CDM fields populated                    |
| Consistency & logic        | No contradictory values (e.g. duration > total study)    |
| Ontology mapping validation| Mapped IDs exist, of expected type, not deprecated       |
| Provenance & reproducibility| Every value traceable; secondary results re-runnable    |
| Duplicate & conflict       | No duplicate entities, no conflicting mappings           |

**Interface:**

```python
class ReviewAgent:
    def run(self, record: AnnotatedSEACDMRecord) -> ReviewReport: ...
```

---

## 6. Sub-agents: Analysis + Coding

Triggered from Agent A Step 2 when primary documentation lacks needed
result data and re-analysis of public-repo data is required.

### 6.1 Analysis Agent
- Determines what analysis is required
- Defines data sources & methods
- Generates an **analysis plan** (structured object, see below)

```python
class AnalysisPlan(BaseModel):
    objective: str
    inputs: list[DataSource]      # e.g. GEO accessions
    methods: list[AnalysisStep]   # ordered pipeline
    expected_outputs: list[str]   # table/figure descriptions
```

### 6.2 Coding Agent
Executes the plan:
- Downloads data from GEO (or other repo)
- Runs analysis as **reproducible code** (script + pinned env)
- Generates tables/figures
- Returns `SecondaryResults`

```python
class SecondaryResults(BaseModel):
    code_artifact: Path           # the script that produced this
    environment: Path             # requirements.txt / lockfile
    tables: list[Path]
    figures: list[Path]
    summary: str
```

**Loop control:**
- Analysis ↔ Coding may iterate up to `MAX_SUBLOOP_ITERATIONS` (default: 3)
- On failure after max iterations, mark the field as "requires human analyst"
  and continue

<!-- TODO: sandbox/execution environment for Coding Agent.
     Options: local subprocess, Docker, Anthropic code execution tool, E2B. -->

---

## 7. Human Expert Review

Final step. Curator:
- Reviews the `ReviewReport`
- Confirms or edits the `AnnotatedSEACDMRecord`
- Approves final entry into the database

<!-- TODO: interaction surface. Options:
     (a) CLI that prints report and accepts y/n + edits
     (b) Web UI (Streamlit / FastAPI + React)
     (c) Out-of-band: export to spreadsheet, import edits back
     Recommend (a) for v1, (b) later. -->

---

## 8. Orchestration & Control Flow

Top-level pipeline (`src/pipeline.py`):

```python
def process_study(docs: StudyDocumentation) -> FinalRecord:
    record       = study_curation_agent.run(docs)
    annotated    = ontology_mapping_agent.run(record)
    review       = review_agent.run(annotated)
    if review.overall_status == "needs_rework":
        # route back to A or B depending on the issue category
        ...
    final = human_review(annotated, review)
    database.insert(final)
    return final
```

**Concurrency:** studies are processed independently and may be parallelized
at the pipeline level. Within a study, the pipeline is sequential.

**State persistence:** every agent's input and output is persisted before
the next agent starts, so failures can be resumed.

<!-- TODO: persistence layer. Recommend SQLite + JSON blob columns for v1. -->

---

## 9. Non-Functional Requirements

- **Language:** Python 3.11+
- **LLM SDK:** Anthropic Python SDK (no heavy framework like LangGraph/CrewAI in v1)
- **Validation:** Pydantic v2 everywhere at agent boundaries
- **Logging:** structured logs (one record per agent invocation) to `logs/`
- **Testing:** each agent has unit tests using fixture documents in `tests/fixtures/`
- **Reproducibility:** every LLM call records model name, prompt hash,
  temperature, and a seed where supported

---

## 10. Out of Scope (v1)

- Real-time/streaming processing
- Multi-curator collaborative review
- Automatic re-curation when ontologies update
- Web UI (CLI only in v1)

<!-- TODO: confirm this list with stakeholder -->

---

## 11. Open Questions

Tracked here until resolved, then folded into the relevant section above.

1. Exact SEA-CDM schema — need authoritative reference.
2. Which embedding model for semantic mapping?
3. Sandbox choice for the Coding Agent.
4. Source of ontology data (local vs API).
5. How does the human reviewer interact with the system in v1?
6. Confidence thresholds for ontology mapping — defaults given, need expert validation.

---

## 12. Glossary

- **SEA-CDM** — Standardized Exercise Activity Common Data Model.
  <!-- TODO: fill in authoritative definition + link -->
- **SEA-A** — <!-- TODO -->
- **Exercise-KG** — Exercise Knowledge Graph; the downstream consumer.
- **GEO / PRIDE** — public omics repositories (NCBI GEO; EBI PRIDE).