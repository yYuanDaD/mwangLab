"""SEA-CDM output schema for Agent A — Phase 1 design (2026-05-29 meeting decisions).

This module is the single source of truth for the shape of Agent A's SEA-CDM output.
It encodes the decisions the PhD-student meeting locked in:

  1. CONTAINER = one file per SEA-CDM table (17 tables: the original 13 + `exercise`, `gene`,
     `pathway` and `enrichment`, added so the gene/pathway<->exercise chain is a relational JOIN, not a file
     parse — see point 5). The Friday 2026-06-05 demo serializes them as CSV (one CSV per
     table); rows from many papers accumulate in the same CSV, linked by FK columns.
     (JSON-per-table is the same shape if needed.)
  2. ONTOLOGY ids are STUBBED — every `*_name_id` / `*_type_id` / `*_unit_id` column is
     OMITTED from the output entirely (not emitted as null) to prevent the LLM from
     hallucinating ontology codes. Ontology mapping is Agent B's job (cf. OMOP/Usagi,
     SEA-CDM's own Ontobee step). The `ontology` table is therefore deferred, not produced.
  3. PROVENANCE — every field EXTRACTED from paper text is a `Sourced` value: the LLM must
     supply both the value AND a verbatim `source` quote/section. On CSV flatten, a Sourced
     field `X` becomes TWO columns: `X` (value) and `X_source` (where it came from). Fields
     that are structural (ids/FKs) or machine-derived (the analysis/results rows come from
     run_batch_geo_pipeline, not the paper) are plain — no source column.
  4. MULTI-ROW — one paper -> MULTIPLE experiments, and multiple subjects/samples/groups/
     interventions/assays. Every child row carries the FK columns needed to link back up.
  5. GENE / EXERCISE / PATHWAY CHAIN (2026-06-22 extension; gene row added 2026-06-30;
     exercise node added 2026-07-01) — the scientific finding "exercise
     regulates pathway P (up/down)" used to live ONLY inside the GSEA result CSV files
     (referenced opaquely by results.file_access), so finding it meant parsing files, not
     querying rows. `gene` captures computed DEG genes from the analysis results. Paper-reported
     gene/phenotype claims stay in the reported_findings/reconciliation layer instead of filling
     the gene table directly.
     `exercise` is the explicit process node from the ontology diagram; it is derived from
     exercise-like `interventions` rows, so `gene.exercise_id` is the direct
     `Gene --is_regulated_by--> Exercise` edge while `intervention_id` remains as the protocol
     provenance / backward-compatible FK.
     `pathway` can remain empty/deferred for workflows that only need gene<->exercise.
     Two pathway tables fix this WITHOUT new computation (the facts are already on
     disk): `pathway` (the gene-set NODE, from the MSigDB/KEGG GMT) and `enrichment` (the
     pathway<->exercise EDGE, one row per significant pathway per analysis, from the GSEA
     CSV). `analysis` also gains treatment_group_id / control_group_id / contrast_label so
     the EXERCISE endpoint (which arm vs which arm) is a queryable key, not a filename.
     Result: the chain is `enrichment JOIN pathway JOIN analysis JOIN groups`, and the
     cross-study question ("pathways consistently up across N exercise studies") is a
     GROUP BY pathway_id. `pathway`/`enrichment` are machine-derived (GMT + GSEA), so all
     fields are plain; `enrichment.gsea_source` carries the result-file provenance.

ID / FK convention (so rows across the 17 CSVs join):
    study_id        = the GEO accession, e.g. "GSE279359"            (PK of study)
    experiment_id   = f"{study_id}_exp{n}"      n = 1..              (PK of experiment)
    group_id        = f"{study_id}_grp{n}"                            (PK of groups)
    subject_id      = f"{experiment_id}_subj{n}"                      (PK of subject)
    sample_id       = f"{experiment_id}_samp{n}"                      (PK of sample)
    intervention_id = f"{experiment_id}_int{n}"                       (PK of interventions)
    exercise_id     = f"{experiment_id}_exercise{n}"                  (PK of exercise)
    assay_id        = f"{experiment_id}_assay{n}"                     (PK of assay)
    material_id     = f"{study_id}_mat{n}"                            (PK of material)
    documentation_id= f"{study_id}_doc{n}"                            (PK of documentation)
    analysis_id     = f"{study_id}_analysis{n}"                       (PK of analysis)
    results_id      = f"{study_id}_res{n}"                            (PK of results)
    gene_id         = f"{study_id}_gene{n}"                           (PK of text-mined gene row)
    pathway_id      = canonical gene-set id, e.g. "HALLMARK_OXIDATIVE_PHOSPHORYLATION"
                                                                       (PK of pathway; SHARED across studies, not study-keyed)
    enrichment_id   = f"{analysis_id}_enr{n}"                         (PK of enrichment)

NOTE — linkage FKs (study_id / experiment_id) are added to some child tables even where the
upstream SEA-CDM docs did not list them explicitly; the published table defs are incomplete
on cross-links. These are flagged below and are the kind of pragmatic deviation the mentor
OK'd (WORKFLOW.md steps 2-5 are suggestions; the goal is usable relational output).

Run `python tools/sea_cdm_schema.py` to print the exact 17-CSV column layout this produces.
"""

from typing import List, Optional, Type

from pydantic import BaseModel, Field, model_validator


class Sourced(BaseModel):
    """A value the LLM EXTRACTED from the paper text, paired with its evidence.

    On CSV flatten this becomes two columns: `<field>` (value) and `<field>_source`
    (a verbatim quote or section name). List-valued fields are stored as the value
    string joined by ';' (e.g. platform = "Nanopore MinION; Illumina NovaSeq").
    """
    value: Optional[str] = Field(default=None, description="the extracted value (lists joined by ';')")
    source: Optional[str] = Field(default=None, description="verbatim quote / section the value was taken from")

    @model_validator(mode="before")
    @classmethod
    def _coerce_scalar(cls, data):
        """Be lenient about the shape the LLM emits. Despite the {value, source} schema, the
        model sometimes returns a Sourced field as a bare string ('SED'), a list, or a number.
        Coerce those into {value: <str>, source: None} so one malformed field doesn't blow up the
        whole extraction (observed: GSE250122 lost entirely to a str-not-object groups field)."""
        if data is None:
            return {"value": None, "source": None}
        if isinstance(data, str):
            return {"value": data, "source": None}
        if isinstance(data, (int, float, bool)):
            return {"value": str(data), "source": None}
        if isinstance(data, (list, tuple)):
            return {"value": "; ".join(str(x) for x in data if x is not None) or None, "source": None}
        return data


# --------------------------------------------------------------------------------------
# Protocol-side tables — populated by the LLM from the paper's Methods. All descriptive
# fields are Sourced; ids / FKs / convention-set values are plain. Ontology *_id omitted.
# --------------------------------------------------------------------------------------

class Study(BaseModel):
    study_id: str = Field(description="PK = GEO accession, e.g. GSE279359")
    reference_source: str = "GEO"                       # convention
    reference_source_id: Optional[str] = None           # = study_id
    # Back-link to the parent GEO accession when this study is a per-condition SPLIT record
    # (e.g. GSE279359__2wk derived from GSE279359 by tools/study_split.py). None for a normal
    # whole-GSE study. Preserves that several split studies came from ONE paper/GSE.
    source_gse: Optional[str] = None
    study_name: Sourced = Field(default_factory=Sourced)
    study_description: Sourced = Field(default_factory=Sourced)
    study_type: Sourced = Field(default_factory=Sourced)
    study_focus: Sourced = Field(default_factory=Sourced)
    study_keywords: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Experiment(BaseModel):
    experiment_id: str = Field(description="PK = {study_id}_exp{n}")
    study_id: str = Field(description="FK -> study")
    documentation_id: Optional[str] = Field(default=None, description="FK -> documentation")
    experiment_control: Optional[str] = Field(default=None, description="'true' if this experiment is the control arm")
    experiment_type: Sourced = Field(default_factory=Sourced)
    experiment_subject: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Subject(BaseModel):
    subject_id: str = Field(description="PK = {experiment_id}_subj{n}")
    experiment_id: str = Field(description="FK -> experiment")
    group_id: Optional[str] = Field(default=None, description="FK -> groups")
    subject_type: Sourced = Field(default_factory=Sourced)        # e.g. Organism, Cell Line
    species: Sourced = Field(default_factory=Sourced)
    organism_race: Sourced = Field(default_factory=Sourced)
    subject_lineage: Sourced = Field(default_factory=Sourced)     # strain / subtype
    organism_age: Sourced = Field(default_factory=Sourced)
    organism_age_unit: Sourced = Field(default_factory=Sourced)
    organism_sex: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Sample(BaseModel):
    sample_id: str = Field(description="PK = {experiment_id}_samp{n}")
    organism_id: str = Field(description="FK -> subject.subject_id ('0' = multiple organisms)")
    group_id: Optional[str] = Field(default=None, description="FK -> groups")
    biosample_collection: Sourced = Field(default_factory=Sourced)
    biosample_type: Sourced = Field(default_factory=Sourced)      # source tissue / material
    expsample_type: Sourced = Field(default_factory=Sourced)      # final processed specimen
    comments: Sourced = Field(default_factory=Sourced)


class Groups(BaseModel):
    group_id: str = Field(description="PK = {study_id}_grp{n}")
    study_id: str = Field(description="FK -> study (linkage FK; not in upstream docs)")
    subject_group: Sourced = Field(default_factory=Sourced)       # e.g. 'pre-exercise', 'post-exercise'
    sample_group: Sourced = Field(default_factory=Sourced)
    group_size: Sourced = Field(default_factory=Sourced)
    min_group_age: Sourced = Field(default_factory=Sourced)
    min_age_unit: Sourced = Field(default_factory=Sourced)
    max_group_age: Sourced = Field(default_factory=Sourced)
    max_age_unit: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Interventions(BaseModel):
    intervention_id: str = Field(description="PK = {experiment_id}_int{n}")
    experiment_id: str = Field(description="FK -> experiment")
    subject_id: Optional[str] = Field(default=None, description="FK -> subject")
    material: Sourced = Field(default_factory=Sourced)            # what was administered (e.g. 'treadmill running')
    dosage: Sourced = Field(default_factory=Sourced)
    dosage_unit: Sourced = Field(default_factory=Sourced)
    intervention_type: Sourced = Field(default_factory=Sourced)
    intervention_route: Sourced = Field(default_factory=Sourced)
    t0_definition: Sourced = Field(default_factory=Sourced)
    intervention_time: Sourced = Field(default_factory=Sourced)
    time_unit: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Exercise(BaseModel):
    """The ontology-level Exercise PROCESS node.

    In the legacy schema, exercise lived only as an `interventions` row whose material/type said
    treadmill running, endurance training, wheel running, etc. This table makes the direct ontology
    relation explicit: `gene.exercise_id -> exercise.exercise_id` with
    `gene.relationship_to_exercise = is_regulated_by`. The original intervention FK is retained as
    protocol provenance.
    """
    exercise_id: str = Field(description="PK = {experiment_id}_exercise{n}")
    study_id: str = Field(description="FK -> study")
    experiment_id: str = Field(description="FK -> experiment")
    intervention_id: Optional[str] = Field(default=None, description="FK -> interventions row this exercise node was derived from")
    group_id: Optional[str] = Field(default=None, description="FK -> groups when the exercise arm is resolvable")
    exercise_name: Sourced = Field(default_factory=Sourced)
    exercise_type: Sourced = Field(default_factory=Sourced)
    exercise_parameters: Sourced = Field(default_factory=Sourced)
    t0_definition: Sourced = Field(default_factory=Sourced)
    exercise_time: Sourced = Field(default_factory=Sourced)
    time_unit: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class Assay(BaseModel):
    assay_id: str = Field(description="PK = {experiment_id}_assay{n}")
    experiment_id: str = Field(description="FK -> experiment (linkage FK; not in upstream docs)")
    documentation_id: Optional[str] = Field(default=None, description="FK -> documentation")
    organism_input: str = "true"                                  # convention: GEO RNA-seq uses a biosample
    assay_name: Sourced = Field(default_factory=Sourced)          # e.g. 'Long-read RNA-Seq'
    assay_type: Sourced = Field(default_factory=Sourced)          # Experimental Assay / Observation / Survey
    reagents: Sourced = Field(default_factory=Sourced)            # ';'-joined
    platform: Sourced = Field(default_factory=Sourced)            # ';'-joined, e.g. 'Oxford Nanopore MinION'


class Material(BaseModel):
    material_id: str = Field(description="PK = {study_id}_mat{n}")
    reference_source: Optional[str] = Field(default=None, description="source type of the reference id")
    material_name: Sourced = Field(default_factory=Sourced)
    organization: Sourced = Field(default_factory=Sourced)


class Documentation(BaseModel):
    documentation_id: str = Field(description="PK = {study_id}_doc{n}")
    study_id: str = Field(description="FK -> study")
    documentation_file_access: Optional[str] = Field(default=None, description="URL/path to the document")
    reference_source: Optional[str] = Field(default=None, description="e.g. 'PubMed', 'GEO'")
    reference_source_id: Optional[str] = Field(default=None, description="e.g. the PMCID / GSE")
    document_name: Sourced = Field(default_factory=Sourced)
    documentation_type: Sourced = Field(default_factory=Sourced)  # protocol / paper / results
    citation: Sourced = Field(default_factory=Sourced)
    creator_role: Sourced = Field(default_factory=Sourced)


# --------------------------------------------------------------------------------------
# Result-side tables — populated from run_batch_geo_pipeline artifacts (summary.csv /
# decisions.json), NOT from paper text. Plain fields: their provenance is the cohort run,
# so no per-field `_source` (the meeting's source requirement is for text-extracted fields).
# --------------------------------------------------------------------------------------

class Analysis(BaseModel):
    analysis_id: str = Field(description="PK = {study_id}_analysis{n}")
    study_id: str = Field(description="linkage FK -> study")
    group_id: Optional[str] = Field(default=None, description="FK -> groups (legacy single-group link; kept for back-compat)")
    # The EXERCISE endpoint of the pathway<->exercise chain: this analysis' contrast as a pair of
    # group FKs (lifted out of the DEG filename) so 'which analysis is exercise-treat vs control'
    # is a queryable JOIN key. groups.subject_group then says whether an arm is exercise/sedentary.
    treatment_group_id: Optional[str] = Field(default=None, description="FK -> groups: the treated / exercise arm of this analysis' contrast")
    control_group_id: Optional[str] = Field(default=None, description="FK -> groups: the control / baseline arm of this analysis' contrast")
    contrast_label: Optional[str] = Field(default=None, description="human-readable contrast, e.g. '14-0-0 vs 0-0-0' (the DEG-file contrast as a value)")
    documentation_id: Optional[str] = None
    input_data: Optional[str] = Field(default=None, description="data type used, e.g. 'Raw RNA-seq integer counts'")
    input_data_id: Optional[str] = None
    file_access: Optional[str] = Field(default=None, description="download URL for the input data")
    analysis_name: Optional[str] = Field(default=None, description="e.g. 'Differential expression analysis'")
    da_method: Optional[str] = Field(default=None, description="tool the LLM/pipeline chose: deseq2 / limma / limma-voom / edger")
    n_deg: Optional[str] = Field(default=None, description="DEG count at the pipeline cutoff")
    reference_source: Optional[str] = None
    reference_source_id: Optional[str] = None


class Results(BaseModel):
    results_id: str = Field(description="PK = {study_id}_res{n}")
    experiment_id: Optional[str] = Field(default=None, description="FK -> experiment")
    group_id: Optional[str] = Field(default=None, description="FK -> groups")
    sample_id: Optional[str] = Field(default=None, description="FK -> sample ('1' = group-level)")
    subject_id: Optional[str] = Field(default=None, description="FK -> subject ('1' = group-level)")
    documentation_id: Optional[str] = None
    analysis_type: Optional[str] = Field(default=None, description="method that produced the result")
    original_assay_type: Optional[str] = "experimental assay"
    datatype: Optional[str] = Field(default=None, description="e.g. Spreadsheet, Image")
    dataset_size: Optional[str] = None
    file_access: Optional[str] = Field(default=None, description="path/URL of the result file")
    file_type: Optional[str] = None


# --------------------------------------------------------------------------------------
# Gene<->exercise table (computed from DEG result files). Pathway is intentionally optional here:
# pathway membership / enrichment is represented by pathway + enrichment tables.
# --------------------------------------------------------------------------------------

class Gene(BaseModel):
    """A computed DEG gene that was regulated in an exercise contrast.

    This is not filled from paper text. Rows are selected from DEG result CSVs, with the DEG file
    path recorded in the Sourced provenance columns. Paper gene/phenotype statements are stored in
    reported_findings.csv and reconciliation result rows.
    """
    gene_id: str = Field(description="PK = {study_id}_gene{n}")
    study_id: str = Field(description="FK -> study")
    experiment_id: Optional[str] = Field(default=None, description="FK -> experiment")
    intervention_id: Optional[str] = Field(default=None, description="FK -> interventions; the exercise stimulus when resolvable")
    exercise_id: Optional[str] = Field(default=None, description="FK -> exercise; direct Gene --is_regulated_by--> Exercise edge")
    group_id: Optional[str] = Field(default=None, description="FK -> groups when the paper maps the gene to one arm")
    pathway_id: Optional[str] = Field(default=None, description="Optional FK -> pathway; left null until pathway modeling is enabled")
    gene_symbol: Sourced = Field(default_factory=Sourced)
    gene_name: Sourced = Field(default_factory=Sourced)
    organism: Optional[str] = None
    comparison: Sourced = Field(default_factory=Sourced)
    regulation_direction: Optional[str] = Field(default=None, description="up / down / changed / unchanged / n/a")
    magnitude: Sourced = Field(default_factory=Sourced)
    relationship_to_exercise: Optional[str] = Field(default="is_regulated_by", description="Edge label for gene -> exercise")
    reference_source: Optional[str] = Field(default="paper")
    reference_source_id: Optional[str] = None


# --------------------------------------------------------------------------------------
# Pathway<->exercise chain tables (2026-06-22). Machine-derived — `pathway` from the MSigDB/
# KEGG GMT used for GSEA, `enrichment` from the GSEA result CSV — so ALL fields are plain (no
# `_source`); enrichment.gsea_source records the result file the numbers came from. Together
# they turn 'which pathways does exercise regulate' from a file parse into a relational JOIN.
# --------------------------------------------------------------------------------------

class Pathway(BaseModel):
    """A gene-set / pathway NODE — the canonical dimension behind enrichment edges. SHARED across
    studies (pathway_id is the gene-set's OWN id, not study-keyed), so each set appears once and
    many studies' enrichment rows point at it — that shared key is what makes cross-study
    aggregation ('pathways up across N exercise studies') a GROUP BY."""
    pathway_id: str = Field(description="PK = canonical gene-set id, e.g. HALLMARK_OXIDATIVE_PHOSPHORYLATION")
    pathway_name: Optional[str] = Field(default=None, description="readable name, e.g. 'Oxidative Phosphorylation'")
    library: Optional[str] = Field(default=None, description="source collection, e.g. 'MSigDB Hallmark' / 'KEGG' / 'Reactome'")
    collection_version: Optional[str] = Field(default=None, description="exact collection tag for reproducibility, e.g. 'h.all@2024.1.Hs'")
    n_genes: Optional[str] = Field(default=None, description="number of genes in the set")


class Enrichment(BaseModel):
    """The pathway<->exercise EDGE: one row per SIGNIFICANT pathway in one analysis' contrast.
    Its analysis_id FK carries the exercise endpoint (via analysis.treatment_group_id /
    control_group_id); its pathway_id FK is a clean equi-join to the canonical pathway node —
    no token-overlap name matching. This is the finer-grained result-side table that the old
    file-pointer `results` row could not express."""
    enrichment_id: str = Field(description="PK = {analysis_id}_enr{n}")
    analysis_id: str = Field(description="FK -> analysis (the exercise contrast lives there as treatment/control group FKs)")
    pathway_id: str = Field(description="FK -> pathway")
    direction: Optional[str] = Field(default=None, description="'up' / 'down' (sign of NES)")
    nes: Optional[str] = Field(default=None, description="normalized enrichment score")
    fdr: Optional[str] = Field(default=None, description="FDR q-value at which this pathway is significant")
    leading_edge_genes: Optional[str] = Field(default=None, description="';'-joined leading-edge gene symbols driving the enrichment")
    paper_named: Optional[str] = Field(default=None, description="'true' if the paper text also names this pathway as exercise-changed (text cross-confirmation; left empty in the zero-LLM v1)")
    paper_named_source: Optional[str] = Field(default=None, description="verbatim paper sentence backing paper_named, when populated")
    gsea_source: Optional[str] = Field(default=None, description="path of the GSEA result file these numbers came from (computational provenance)")


# --------------------------------------------------------------------------------------
# Rarely / not populated for RNA-seq exercise studies — present for schema completeness.
# --------------------------------------------------------------------------------------

class Occurence(BaseModel):
    """Events affecting an organism (disease, pregnancy, adverse event). Usually EMPTY for
    a basic exercise RNA-seq study — the CSV exists but typically has 0 rows."""
    occurrence_id: str = Field(description="PK")
    subject_id: str = Field(description="FK -> subject")
    occurrence_name: Sourced = Field(default_factory=Sourced)
    occurrence_severity: Optional[str] = None
    comments: Sourced = Field(default_factory=Sourced)


# --------------------------------------------------------------------------------------
# Table registry: name -> (model, csv filename, how it gets filled). Drives Phase 3's
# 13-CSV writer and tells the LLM which tables to populate from text vs which come from
# the pipeline vs which to leave for Agent B.
# --------------------------------------------------------------------------------------

# fillable_from: "text" = LLM extracts from the paper; "pipeline" = from run_batch_geo_pipeline;
#                "reference" = authoritative external data (the MSigDB/KEGG GMT, no paper, no LLM);
#                "rare" = schema-complete but usually 0 rows; "deferred" = Agent B (ontology mapping).
SEA_TABLES = {
    "study":         {"model": Study,         "csv": "study.csv",         "fillable_from": "text"},
    "experiment":    {"model": Experiment,    "csv": "experiment.csv",    "fillable_from": "text"},
    "subject":       {"model": Subject,       "csv": "subject.csv",       "fillable_from": "text"},
    "sample":        {"model": Sample,        "csv": "sample.csv",        "fillable_from": "text"},
    "groups":        {"model": Groups,        "csv": "groups.csv",        "fillable_from": "text"},
    "interventions": {"model": Interventions, "csv": "interventions.csv", "fillable_from": "text"},
    "exercise":      {"model": Exercise,      "csv": "exercise.csv",      "fillable_from": "derived"},
    "assay":         {"model": Assay,         "csv": "assay.csv",         "fillable_from": "text"},
    "material":      {"model": Material,      "csv": "material.csv",      "fillable_from": "text"},
    "documentation": {"model": Documentation, "csv": "documentation.csv", "fillable_from": "text"},
    "analysis":      {"model": Analysis,      "csv": "analysis.csv",      "fillable_from": "pipeline"},
    "results":       {"model": Results,       "csv": "results.csv",       "fillable_from": "pipeline"},
    "gene":          {"model": Gene,          "csv": "gene.csv",          "fillable_from": "pipeline"},
    "pathway":       {"model": Pathway,       "csv": "pathway.csv",       "fillable_from": "reference"},
    "enrichment":    {"model": Enrichment,    "csv": "enrichment.csv",    "fillable_from": "pipeline"},
    "occurence":     {"model": Occurence,     "csv": "occurence.csv",     "fillable_from": "rare"},
    "ontology":      {"model": None,          "csv": "ontology.csv",      "fillable_from": "deferred"},
}


def is_sourced_field(model: Type[BaseModel], field_name: str) -> bool:
    """True if `field_name` is a Sourced (text-extracted) field on `model`."""
    ann = model.model_fields[field_name].annotation
    return ann is Sourced


def csv_columns(table_name: str) -> List[str]:
    """Ordered CSV column list for a table: a Sourced field X -> [X, X_source];
    a plain field -> [X]. This IS the on-disk column spec for that table's CSV."""
    entry = SEA_TABLES[table_name]
    model = entry["model"]
    if model is None:
        return []  # deferred (ontology) — no columns produced by Agent A
    cols: List[str] = []
    for name, info in model.model_fields.items():
        if info.annotation is Sourced:
            cols.extend([name, f"{name}_source"])
        else:
            cols.append(name)
    return cols


if __name__ == "__main__":
    print("SEA-CDM 17-CSV output layout (Agent A — +exercise/+gene/+pathway/+enrichment)\n")
    for name, entry in SEA_TABLES.items():
        cols = csv_columns(name)
        ncol = len(cols)
        tag = entry["fillable_from"]
        print(f"=== {entry['csv']:<20} [{tag}] {ncol} cols ===")
        if cols:
            print("    " + ", ".join(cols))
        else:
            print("    (deferred to Agent B — ontology mapping; Agent A emits no rows)")
        print()
