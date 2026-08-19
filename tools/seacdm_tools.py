"""Audited SEA-CDM extraction plus compatibility-only Legacy extractors."""

import os
import re
import json
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from langchain_core.tools import tool

from tools.sea_cdm_schema import Sourced, SEA_TABLES, csv_columns
from tools.metadata_structural import (
    build_structural_tables,
    META_SOURCE_PREFIX,
    summarize_geo_scope,
)


# LEGACY: flat v0 compatibility API. Do not use for new workflows.

class AssayInfo(BaseModel):
    assay_type: str = Field(description="Assay type, e.g. RNA-Seq")
    platform: str = Field(description="Sequencing platform, e.g. Illumina NovaSeq 6000")


class ExperimentInfo(BaseModel):
    subject_species: str = Field(description="Species, e.g. Homo sapiens, Mus musculus")
    treatment_group: str = Field(description="Description of the treatment group")
    control_group: str = Field(description="Description of the control group")
    tissue_or_cell: str = Field(description="Tissue or cell type")


class SEACDM_Record(BaseModel):
    study_id: str = Field(description="Study ID or GEO Accession ID")
    study_objective: str = Field(description="Summary of the study's primary scientific objective")
    experiments: List[ExperimentInfo] = Field(description="Detailed grouping and condition info for experimental subjects")
    assays: List[AssayInfo] = Field(description="Sequencing technologies and assay methods used")


@tool(args_schema=SEACDM_Record)
def extract_sea_cdm_conditions(study_id: str, study_objective: str, experiments: list, assays: list) -> str:
    """LEGACY: write the deprecated flat SEA-CDM v0 JSON. Use extract_sea_cdm_tables."""
    os.makedirs("./output", exist_ok=True)
    dict_experiments = [exp.model_dump() if hasattr(exp, 'model_dump') else exp for exp in experiments]
    dict_assays = [assay.model_dump() if hasattr(assay, 'model_dump') else assay for assay in assays]
    record = {
        "study_id": study_id,
        "study_objective": study_objective,
        "experiments": dict_experiments,
        "assays": dict_assays,
    }
    save_path = f"./output/{study_id}_seacdm.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=4, ensure_ascii=False)
    return f"LEGACY flat SEA-CDM record saved to: {save_path}"


# Current extraction models omit IDs/FKs; Python assigns them deterministically.

class StudyExtract(BaseModel):
    study_name: Sourced = Field(default_factory=Sourced, description="The study's title / name")
    study_description: Sourced = Field(default_factory=Sourced, description="One-paragraph objective of the study")
    study_type: Sourced = Field(default_factory=Sourced, description="e.g. 'transcriptomics', 'observational'")
    study_focus: Sourced = Field(default_factory=Sourced, description="primary biological focus")
    study_keywords: Sourced = Field(default_factory=Sourced, description="keywords, ';'-joined if several")
    comments: Sourced = Field(default_factory=Sourced)


class DocumentationExtract(BaseModel):
    document_name: Sourced = Field(default_factory=Sourced, description="title of the paper / protocol document")
    documentation_type: Sourced = Field(default_factory=Sourced, description="'paper' / 'protocol' / 'results'")
    citation: Sourced = Field(default_factory=Sourced, description="full citation if stated")
    creator_role: Sourced = Field(default_factory=Sourced, description="e.g. 'authors', 'consortium'")
    documentation_file_access: Optional[str] = Field(default=None, description="DOI / URL of the document if stated")
    reference_source: Optional[str] = Field(default=None, description="e.g. 'PubMed', 'GEO', 'DOI'")
    reference_source_id: Optional[str] = Field(default=None, description="the PMCID / PMID / DOI value")

    @model_validator(mode="before")
    @classmethod
    def _coerce_plain_reference_fields(cls, data):
        """Some providers apply the global {value, source} convention to plain ID fields too."""
        if not isinstance(data, dict):
            return data
        out = dict(data)
        for field in ("documentation_file_access", "reference_source", "reference_source_id"):
            value = out.get(field)
            if isinstance(value, dict) and "value" in value:
                out[field] = value.get("value")
        return out


class MaterialExtract(BaseModel):
    material_name: Sourced = Field(default_factory=Sourced, description="a reagent / kit / instrument / antibody used")
    organization: Sourced = Field(default_factory=Sourced, description="vendor / manufacturer / supplier")
    reference_source: Optional[str] = Field(default=None, description="catalog/RRID source type if stated")


class ExperimentLite(BaseModel):
    """One experiment, top-level fields only (children attach via experiment_index)."""
    experiment_type: Sourced = Field(default_factory=Sourced, description="what this experiment does, e.g. 'acute exercise time-course RNA-seq'")
    experiment_subject: Sourced = Field(default_factory=Sourced, description="who/what is studied in this experiment, e.g. 'mouse gastrocnemius'")
    experiment_control: Optional[str] = Field(default=None, description="'true' if this whole experiment IS the control arm; else null")
    comments: Sourced = Field(default_factory=Sourced)

    @model_validator(mode="before")
    @classmethod
    def _coerce_sourced_plain_control(cls, data):
        """Claude 5 may apply the global Sourced convention to this legacy plain field."""
        if not isinstance(data, dict):
            return data
        out = dict(data)
        value = out.get("experiment_control")
        if isinstance(value, dict) and "value" in value:
            out["experiment_control"] = value.get("value")
        return out


class SubjectExtract(BaseModel):
    experiment_index: int = Field(default=1, description="1-based index into the experiments list this subject belongs to (use 1 for a single-experiment paper)")
    subject_type: Sourced = Field(default_factory=Sourced, description="e.g. 'Organism', 'Cell Line'")
    species: Sourced = Field(default_factory=Sourced, description="e.g. 'Mus musculus'")
    organism_race: Sourced = Field(default_factory=Sourced, description="breed / population if stated")
    subject_lineage: Sourced = Field(default_factory=Sourced, description="strain / genotype, e.g. 'C57BL/6J'")
    organism_age: Sourced = Field(default_factory=Sourced)
    organism_age_unit: Sourced = Field(default_factory=Sourced, description="e.g. 'weeks', 'years'")
    organism_sex: Sourced = Field(default_factory=Sourced)
    group_label: Optional[str] = Field(default=None, description="natural-language name of the group this subject belongs to (used only to link to a groups row; leave null if it spans all groups)")
    comments: Sourced = Field(default_factory=Sourced)


class SampleExtract(BaseModel):
    experiment_index: int = Field(default=1, description="1-based index into the experiments list this sample belongs to")
    biosample_collection: Sourced = Field(default_factory=Sourced, description="how/when the specimen was collected")
    biosample_type: Sourced = Field(default_factory=Sourced, description="source tissue / material, e.g. 'gastrocnemius muscle'")
    expsample_type: Sourced = Field(default_factory=Sourced, description="final processed specimen, e.g. 'total RNA'")
    group_label: Optional[str] = Field(default=None, description="natural-language name of the group this sample belongs to; null if it spans all groups")
    comments: Sourced = Field(default_factory=Sourced)


class GroupExtract(BaseModel):
    experiment_index: int = Field(default=1, description="1-based index into the experiments list this group belongs to")
    subject_group: Sourced = Field(default_factory=Sourced, description="the arm name, e.g. 'pre-exercise', 'post-exercise', 'control'")
    sample_group: Sourced = Field(default_factory=Sourced, description="sample-level group label if different from subject_group")
    group_size: Sourced = Field(default_factory=Sourced, description="n per group")
    min_group_age: Sourced = Field(default_factory=Sourced)
    min_age_unit: Sourced = Field(default_factory=Sourced)
    max_group_age: Sourced = Field(default_factory=Sourced)
    max_age_unit: Sourced = Field(default_factory=Sourced)
    comments: Sourced = Field(default_factory=Sourced)


class InterventionExtract(BaseModel):
    experiment_index: int = Field(default=1, description="1-based index into the experiments list this intervention belongs to")
    material: Sourced = Field(default_factory=Sourced, description="what was administered/applied, e.g. 'treadmill running', 'PBS'")
    dosage: Sourced = Field(default_factory=Sourced)
    dosage_unit: Sourced = Field(default_factory=Sourced)
    intervention_type: Sourced = Field(default_factory=Sourced, description="e.g. 'exercise', 'drug', 'diet'")
    intervention_route: Sourced = Field(default_factory=Sourced, description="e.g. 'oral', 'i.p.', 'n/a'")
    t0_definition: Sourced = Field(default_factory=Sourced, description="what defines time zero, e.g. 'end of exercise bout'")
    intervention_time: Sourced = Field(default_factory=Sourced, description="duration / timepoint, e.g. '30', '1/3/6/24'")
    time_unit: Sourced = Field(default_factory=Sourced, description="e.g. 'minutes', 'hours'")
    comments: Sourced = Field(default_factory=Sourced)


class AssayExtract(BaseModel):
    experiment_index: int = Field(default=1, description="1-based index into the experiments list this assay belongs to")
    assay_name: Sourced = Field(default_factory=Sourced, description="e.g. 'Long-read RNA-Seq', 'bulk RNA-Seq'")
    assay_type: Sourced = Field(default_factory=Sourced, description="'Experimental Assay' / 'Observation' / 'Survey'")
    reagents: Sourced = Field(default_factory=Sourced, description="library prep kits etc., ';'-joined")
    platform: Sourced = Field(default_factory=Sourced, description="sequencer(s), ';'-joined")


class _CoerceJSONContainer(BaseModel):
    """Base for the three group containers. Tolerates a real structured-output failure mode:
    Sonnet sometimes serializes a list-typed field (e.g. `assays`) — or the whole object — as a
    JSON *string* ('[{...}]') instead of an actual list/dict, which strict pydantic rejects and
    which would crash the entire extraction. Here a mode='before' validator json.loads() any such
    stringified array/object back into a real structure before field validation. Same fail-soft
    philosophy as Sourced's scalar coercion. Nested Sourced/Extract validators handle the rest."""

    @model_validator(mode="before")
    @classmethod
    def _coerce_stringified_json(cls, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except (ValueError, TypeError):
                return data
        if not isinstance(data, dict):
            return data
        out = dict(data)
        for k, v in out.items():
            if isinstance(v, str):
                s = v.strip()
                if s[:1] in ("[", "{") and s[-1:] in ("]", "}"):
                    try:
                        out[k] = json.loads(s)
                    except (ValueError, TypeError):
                        pass
        return out


class StudyLevelExtraction(_CoerceJSONContainer):
    """Group 1 container — study-scoped tables."""
    study: StudyExtract = Field(default_factory=StudyExtract)
    documentation: List[DocumentationExtract] = Field(default_factory=list)
    material: List[MaterialExtract] = Field(default_factory=list)


class DesignExtraction(_CoerceJSONContainer):
    """Group 2 container — experiments and who/what/arms (flat lists)."""
    experiments: List[ExperimentLite] = Field(default_factory=list)
    subjects: List[SubjectExtract] = Field(default_factory=list)
    groups: List[GroupExtract] = Field(default_factory=list)


class MethodsExtraction(_CoerceJSONContainer):
    """Group 3 container — specimens / interventions / assays (flat lists)."""
    samples: List[SampleExtract] = Field(default_factory=list)
    interventions: List[InterventionExtract] = Field(default_factory=list)
    assays: List[AssayExtract] = Field(default_factory=list)


class StudyDocumentationExtraction(_CoerceJSONContainer):
    """Small staged schema for study identity and publication provenance."""
    study: StudyExtract = Field(default_factory=StudyExtract)
    documentation: List[DocumentationExtract] = Field(default_factory=list)


class StudyOnlyExtraction(_CoerceJSONContainer):
    """One-table staged schema; avoids providers silently omitting later schema fields."""
    study: StudyExtract = Field(default_factory=StudyExtract)


class DocumentationOnlyExtraction(_CoerceJSONContainer):
    """One-table staged schema for the source publication."""
    documentation: List[DocumentationExtract] = Field(default_factory=list)


class ExperimentInterventionExtraction(_CoerceJSONContainer):
    """Small staged schema for designs and the treatments applied to them."""
    experiments: List[ExperimentLite] = Field(default_factory=list)
    interventions: List[InterventionExtract] = Field(default_factory=list)


class MaterialExtraction(_CoerceJSONContainer):
    """Small staged schema for named reagents, instruments, kits, and software."""
    material: List[MaterialExtract] = Field(default_factory=list)


class LeanExtraction(_CoerceJSONContainer):
    """Single-call extraction used when GEO metadata supplies structural tables."""
    study: StudyExtract = Field(default_factory=StudyExtract)
    documentation: List[DocumentationExtract] = Field(default_factory=list)
    material: List[MaterialExtract] = Field(default_factory=list)
    experiments: List[ExperimentLite] = Field(default_factory=list)
    interventions: List[InterventionExtract] = Field(default_factory=list)
    reported_findings: List["ReportedFinding"] = Field(default_factory=list)


# Paper-reported findings used when computed results are unavailable.

class ReportedFinding(BaseModel):
    entity: str = Field(description="the molecule/gene/protein/metabolite/lipid/phenotype that "
                                    "CHANGED with the intervention, e.g. 'PGC-1alpha', 'IL-6', 'VO2max'")
    entity_type: str = Field(description="one of: gene, protein, metabolite, lipid, phenotype, other")
    direction: str = Field(description="one of: up, down, changed, unchanged, n/a (relative to control/baseline)")
    magnitude: Optional[str] = Field(default=None, description="fold-change / percent / p-value / qualifier "
                                                              "if the paper states one, else null")
    comparison: Optional[str] = Field(default=None, description="the contrast this refers to, e.g. "
                                                              "'trained vs sedentary', '24h post vs pre-exercise'")
    source: str = Field(description="a SHORT VERBATIM quote copied EXACTLY from the paper text stating this finding")


class ReportedFindingsExtraction(_CoerceJSONContainer):
    """Container for the paper's explicitly-reported findings (text-mined results)."""
    findings: List[ReportedFinding] = Field(default_factory=list)


LeanExtraction.model_rebuild()


# --- LLM plumbing ----------------------------------------------------------------------

def _get_llm():
    """SEA-CDM provider, pinned to Sonnet unless explicitly overridden.

    DeepSeek V4 Pro is suitable for the main agent and DA routing, but the
    paired 100k-character paper benchmark returned silently incomplete
    ``LeanExtraction`` objects in 3/3 trials. Keep this high-recall extraction
    path on Sonnet until a dedicated prompt/schema change passes the same gate.
    """
    from tools.model_factory import create_structured_chat_model, resolve_model_config
    provider = os.environ.get("BIOAGENT_SEACDM_LLM_PROVIDER", "anthropic")
    config = resolve_model_config(provider=provider)
    return create_structured_chat_model(config, required=False)


class _UsageCapturingStructured:
    """Wraps a with_structured_output(..., include_raw=True) runnable so each extraction call
    records token use and termination metadata into a shared ``usage`` list. A parse failure is
    raised instead of being converted into an all-empty default object; otherwise an incomplete
    response is indistinguishable from a paper that genuinely contains no records."""

    def __init__(self, llm, schema, usage):
        self._runnable = llm.with_structured_output(schema, include_raw=True)
        self._schema = schema
        self._usage = usage

    def invoke(self, prompt):
        res = self._runnable.invoke(prompt)
        raw = res.get("raw") if isinstance(res, dict) else None
        um = getattr(raw, "usage_metadata", None) or {}
        response_meta = getattr(raw, "response_metadata", None) or {}
        parsed = res.get("parsed") if isinstance(res, dict) else res
        parsing_error = res.get("parsing_error") if isinstance(res, dict) else None
        self._usage.append({
            "call": self._schema.__name__,
            "input_tokens": um.get("input_tokens"),
            "output_tokens": um.get("output_tokens"),
            "stop_reason": response_meta.get("stop_reason") or response_meta.get("finish_reason"),
            "model": response_meta.get("model") or response_meta.get("model_name"),
            "parsed": parsed is not None,
            "parsing_error": str(parsing_error) if parsing_error else None,
        })
        if parsed is None:
            detail = f": {parsing_error}" if parsing_error else ""
            raise ValueError(f"Structured output did not parse for {self._schema.__name__}{detail}")
        return parsed


def _structured_runnable(llm, schema, usage=None):
    """A structured-output runnable for `schema`. When `usage` is a list, wrap it to capture token
    usage (uses include_raw); otherwise the plain runnable (identical production behavior)."""
    if usage is None:
        return llm.with_structured_output(schema)
    return _UsageCapturingStructured(llm, schema, usage)


_PROVENANCE_RULES = (
    "Provenance rules (STRICT):\n"
    "- Every descriptive field is an object {value, source}.\n"
    "- `value`: the extracted content (join lists with ';'). Use null when the paper does not state it — DO NOT guess.\n"
    "- `source`: a SHORT VERBATIM quote (a sentence or phrase) copied EXACTLY from the paper text where you found the value.\n"
    "  The source MUST be an actual substring of the provided text. If value is null, source is null too.\n"
    "- Never invent ontology codes, IDs, accession numbers, or citations that are not in the text."
)


def _extract_study_level(paper_text: str, study_id: str, organism: str, usage=None) -> StudyLevelExtraction:
    """LEGACY FULL-mode group; retained when GEO metadata is unavailable."""
    llm = _get_llm()
    if llm is None:
        return StudyLevelExtraction()
    structured = _structured_runnable(llm, StudyLevelExtraction, usage)
    prompt = f"""You are extracting STUDY-LEVEL metadata for the SEA-CDM (Study-Experiment-Assay Common Data Model).

Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}

Extract THREE things from the paper text below:
1. `study`     — one study record (title, objective/description, type, focus, keywords).
2. `documentation` — the paper itself (and any explicitly named protocol/results documents). For the
   paper, set documentation_type='paper', and fill reference_source/reference_source_id with the
   PMCID/PMID/DOI ONLY if they literally appear in the text.
3. `material`  — reagents, kits, instruments, antibodies, software explicitly named in Methods
   (one row each; vendor/manufacturer -> organization). Skip generic mentions with no name.

{_PROVENANCE_RULES}

------- PAPER TEXT START -------
{paper_text}
------- PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_design(paper_text: str, study_id: str, organism: str, usage=None) -> DesignExtraction:
    """LEGACY FULL-mode group; retained when GEO metadata is unavailable."""
    llm = _get_llm()
    if llm is None:
        return DesignExtraction()
    structured = _structured_runnable(llm, DesignExtraction, usage)
    prompt = f"""You are extracting the EXPERIMENTAL DESIGN for the SEA-CDM (Study-Experiment-Assay Common Data Model).

Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}

Return THREE FLAT lists:
1. `experiments` — ONE entry per DISTINCT experimental design. You MUST return at least ONE experiment.
   Most papers tied to a single GEO accession have exactly ONE experiment (return one); create several
   ONLY when the paper clearly describes separate designs (e.g. a mouse RNA-seq experiment AND a
   separate human cohort, or two tissues under different protocols). Do NOT over-split a time-course
   (a single time-course with several timepoints is ONE experiment).
2. `subjects` — the organism(s)/cell line(s) studied (species, strain/lineage, age, sex).
3. `groups`   — the comparison arms (e.g. 'pre-exercise', 'immediately post-exercise', 'control'),
   with n-per-group in group_size. These are the rows a differential analysis contrasts.

For every subject and group, set `experiment_index` to the 1-based position of its experiment in the
`experiments` list (use 1 if there is a single experiment). For each subject, if it clearly belongs to
ONE named group put that group's name verbatim in `group_label`; if it spans all groups, leave it null.

{_PROVENANCE_RULES}

------- PAPER TEXT START -------
{paper_text}
------- PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_methods(paper_text: str, study_id: str, organism: str, usage=None) -> MethodsExtraction:
    """LEGACY FULL-mode group; retained when GEO metadata is unavailable."""
    llm = _get_llm()
    if llm is None:
        return MethodsExtraction()
    structured = _structured_runnable(llm, MethodsExtraction, usage)
    prompt = f"""You are extracting MATERIALS & METHODS for the SEA-CDM (Study-Experiment-Assay Common Data Model).

Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}

Return THREE FLAT lists:
1. `samples`       — the biospecimen(s) assayed (source tissue -> biosample_type; processed form,
   e.g. 'total RNA' / 'cDNA library' -> expsample_type; collection method -> biosample_collection).
2. `interventions` — what was done to the treated arm(s) (e.g. 'treadmill running' / 'PBS injection'),
   with dosage, route, timepoint(s) and the t0 definition.
3. `assays`        — the measurement technique(s): assay_name (e.g. 'Long-read RNA-Seq'), platform /
   sequencer, and library-prep kits as reagents.

For every row, set `experiment_index` to the 1-based position of its experiment (use 1 if the paper has
a single experiment). For each sample, if it clearly belongs to ONE named group put that group's name
verbatim in `group_label`; otherwise leave it null.

{_PROVENANCE_RULES}

------- PAPER TEXT START -------
{paper_text}
------- PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_lean(paper_text: str, study_id: str, organism: str, usage=None) -> LeanExtraction:
    """Extract descriptive fields not supplied by GEO metadata."""
    llm = _get_llm()
    if llm is None:
        return LeanExtraction()
    structured = _structured_runnable(llm, LeanExtraction, usage)
    prompt = f"""You are extracting SEA-CDM (Study-Experiment-Assay Common Data Model) records from a
paper's full text. The study's per-sample structural data (subjects, samples, groups, assays) is
taken from a separate structured GEO metadata table, so DO NOT extract those here — extract ONLY
these five descriptive parts:

Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}

1. `study`         — one study record (title, objective/description, type, focus, keywords).
2. `documentation` — the paper itself (documentation_type='paper') and any explicitly named
   protocol/results documents; fill reference_source/reference_source_id with the PMCID/PMID/DOI
   ONLY if they literally appear in the text.
3. `material`      — reagents, kits, instruments, antibodies, software explicitly named in Methods
   (one row each; vendor/manufacturer -> organization). Skip generic mentions with no name.
4. `experiments`   — ONE entry per DISTINCT experimental design. Return at least ONE. Most papers
   tied to a single GEO accession have exactly ONE experiment (return one); do NOT over-split a
   time-course into many.
5. `interventions` — what was done to the treated arm(s) (e.g. 'treadmill running' / 'PBS
   injection'), with dosage, route, timepoint(s) and the t0 definition.
6. `reported_findings` — the SPECIFIC gene/phenotype changes the paper REPORTS (which
   gene/protein/metabolite/lipid/phenotype changed and in which direction). ONE entry per
   concrete reported change: entity, entity_type (gene/protein/metabolite/lipid/phenotype/other),
   direction (up/down/changed/unchanged/n/a), magnitude (fold/percent/p-value if stated, else null),
   comparison (the contrast, e.g. 'trained vs sedentary'), and `source`. Do NOT extract
   pathway/process names here; pathway tables are computed from GSEA/enrichment results. Extract
   ONLY changes the paper EXPLICITLY states (Abstract/Results/Discussion) — do NOT infer or invent.
   If the paper reports no concrete changes, return an empty list.

   THE `source` RULE FOR reported_findings (most important): `source` is a CONTIGUOUS, CHARACTER-
   FOR-CHARACTER copy of paper text (findable by Ctrl-F) — the SHORTEST exact run of words that
   names the entity and its change (a 6-12 word fragment is ideal). Do NOT rephrase, merge clauses,
   add/drop words, expand abbreviations, or change a gene's case/species prefix (keep 'mHnrnpa3' as
   'mHnrnpa3'). Put your interpretation in entity/direction/comparison; `source` stays a raw quote.
   You MAY join two exact fragments with ' ... ' (each >=8 chars, each an exact copy). Drop a finding
   only if no exact phrase mentioning the entity exists.

{_PROVENANCE_RULES}

------- PAPER TEXT START -------
{paper_text}
------- PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_study_documentation(paper_text: str, study_id: str, organism: str,
                                 usage=None) -> StudyDocumentationExtraction:
    llm = _get_llm()
    if llm is None:
        return StudyDocumentationExtraction()
    structured = _structured_runnable(llm, StudyDocumentationExtraction, usage)
    prompt = f"""Extract only study identity and publication metadata for SEA-CDM from the supplied
paper excerpt. Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}.

Return JSON matching the schema with exactly these parts:
1. `study`: title, one-paragraph objective, study type, biological focus, and keywords.
2. `documentation`: at least the paper itself (`documentation_type='paper'`). Include DOI/PMCID/
   PMID only when literally present. Do not extract experiments, materials, or findings in this step.

Completion rule: do not return until the title and paper documentation record have been populated.
{_PROVENANCE_RULES}

------- RELEVANT PAPER TEXT START -------
{paper_text}
------- RELEVANT PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_study_only(paper_text: str, study_id: str, organism: str,
                        usage=None) -> StudyOnlyExtraction:
    llm = _get_llm()
    if llm is None:
        return StudyOnlyExtraction()
    structured = _structured_runnable(llm, StudyOnlyExtraction, usage)
    prompt = f"""Extract exactly ONE SEA-CDM `study` record from this paper header/abstract.
Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}.
Populate title, objective, study type, biological focus, keywords, and comments when stated.
Do not return documentation, experiments, materials, interventions, or findings.
Completion rule: `study_name.value` must contain the paper title.
{_PROVENANCE_RULES}

------- PAPER HEADER/ABSTRACT START -------
{paper_text}
------- PAPER HEADER/ABSTRACT END -------
"""
    return structured.invoke(prompt)


def _extract_documentation_only(paper_text: str, study_id: str, organism: str,
                                usage=None) -> DocumentationOnlyExtraction:
    llm = _get_llm()
    if llm is None:
        return DocumentationOnlyExtraction()
    structured = _structured_runnable(llm, DocumentationOnlyExtraction, usage)
    prompt = f"""Extract exactly the source publication as ONE SEA-CDM `documentation` record.
Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}.

Required:
- `document_name`: the paper title copied from the text.
- `documentation_type`: `paper`.
- `citation` and creator role when stated.
- DOI/PMCID/PMID in reference_source/reference_source_id only when literally present.
- documentation_file_access may contain the literal DOI or URL.
Do not return study, experiments, materials, interventions, or findings.
Completion rule: return exactly one documentation row; never return an empty list when a paper
header is supplied.
{_PROVENANCE_RULES}

------- PAPER HEADER/IDENTIFIERS START -------
{paper_text}
------- PAPER HEADER/IDENTIFIERS END -------
"""
    return structured.invoke(prompt)


def _extract_experiment_interventions(paper_text: str, study_id: str, organism: str,
                                      usage=None) -> ExperimentInterventionExtraction:
    llm = _get_llm()
    if llm is None:
        return ExperimentInterventionExtraction()
    structured = _structured_runnable(llm, ExperimentInterventionExtraction, usage)
    prompt = f"""Extract only the target GEO accession's experimental design and interventions for
SEA-CDM from the supplied scope block and paper excerpts. Target GEO study: {study_id}{f' (organism: {organism})' if organism else ''}.

HARD SCOPE RULES:
- The extraction unit is the target GEO accession, not every experiment reported in the paper.
- Return exactly one experiment representing the samples described in `[TARGET GEO SCOPE]`.
- Extract only interventions actually applied to those GEO samples.
- Exclude independent validation cohorts, follow-up training cohorts, and assays that appear only
  in the paper but are not represented in `[TARGET GEO SCOPE]`.
- A pre-existing subject attribute such as "trained" or "untrained" is a cohort characteristic,
  not a longitudinal training intervention, unless the GEO scope explicitly contains samples
  collected during that training intervention.
- Several timepoints from the same subjects and protocol remain one experiment.
- Cover every experimental axis represented by the target GEO samples. If GEO sample titles or
  characteristics contain an exercise/training arm (including MICT or HIIT), return a distinct
  exercise intervention for that arm; never return only its control diet or sedentary arm.

Return JSON matching the schema:
1. `experiments`: exactly one row describing the GEO-linked design.
2. `interventions`: what was done to each treated arm, including exercise/drug/viral manipulation,
   dosage, route, timing, and t0 when stated. Link each row with 1-based `experiment_index`.

Completion rule: if the text describes an exercise or treatment protocol, `interventions` must not
be empty. Do not return subjects, samples, groups, assays, materials, or reported findings.
{_PROVENANCE_RULES}

------- RELEVANT PAPER TEXT START -------
{paper_text}
------- RELEVANT PAPER TEXT END -------
"""
    return structured.invoke(prompt)


def _extract_materials(paper_text: str, study_id: str, organism: str,
                       usage=None) -> MaterialExtraction:
    llm = _get_llm()
    if llm is None:
        return MaterialExtraction()
    structured = _structured_runnable(llm, MaterialExtraction, usage)
    prompt = f"""Extract only named materials for SEA-CDM from this Methods excerpt. Target GEO
study: {study_id}{f' (organism: {organism})' if organism else ''}.

Return one `material` row per explicitly named reagent, kit, instrument, antibody, sequencer, or
software package. Put vendor/manufacturer in `organization`. Skip generic unnamed supplies and do
not extract experiments, interventions, or scientific findings. Deduplicate within this excerpt.
{_PROVENANCE_RULES}

------- METHODS EXCERPT START -------
{paper_text}
------- METHODS EXCERPT END -------
"""
    return structured.invoke(prompt)


# --- Flattener: extraction lists -> SEA-CDM table rows ----------------------------------

def _emit(row: dict, name: str, s: Optional[Sourced]) -> None:
    """Write a Sourced field as two row keys: name (value) + name_source (quote)."""
    if s is None:
        row[name] = None
        row[f"{name}_source"] = None
    else:
        row[name] = s.value
        row[f"{name}_source"] = s.source


def _order_row(table: str, row: dict) -> dict:
    """Reindex a row dict to the exact csv_columns order for `table`, filling gaps with None."""
    return {col: row.get(col) for col in csv_columns(table)}


def _norm_label(x: Optional[str]) -> str:
    return (x or "").strip().lower()


def flatten_extraction(
    study_id: str,
    study_level: StudyLevelExtraction,
    design: DesignExtraction,
    methods: MethodsExtraction,
    metadata_csv: Optional[str] = None,
) -> dict:
    """Walk the three extraction containers and produce {table_name: [row, ...]} with all
    IDs/FKs assigned per tools/sea_cdm_schema.py's convention. Only the 9 text tables are
    produced here; analysis/results/occurence/ontology are left to other stages.

    Child rows attach to an experiment by their 1-based `experiment_index`. If the model
    returns children but no experiments, a single default experiment (exp1) is synthesized
    so nothing is orphaned.

    When `metadata_csv` points to a readable GEO metadata CSV, the four
    per-sample STRUCTURAL tables (subject / sample / groups / assay) are REPLACED with rows
    derived deterministically from that CSV (tools/metadata_structural.build_structural_tables)
    instead of the run-to-run-varying LLM lists. The LLM still fills the descriptive tables
    (study/experiment/documentation/material/interventions). Falls back to the LLM tables if
    the metadata is missing or unreadable."""
    tables: dict[str, list] = {name: [] for name in SEA_TABLES}

    # ---- study (1 row) ----
    s = study_level.study
    srow = {"study_id": study_id, "reference_source": "GEO", "reference_source_id": study_id}
    _emit(srow, "study_name", s.study_name)
    _emit(srow, "study_description", s.study_description)
    _emit(srow, "study_type", s.study_type)
    _emit(srow, "study_focus", s.study_focus)
    _emit(srow, "study_keywords", s.study_keywords)
    _emit(srow, "comments", s.comments)
    tables["study"].append(_order_row("study", srow))

    # ---- documentation ----
    for i, d in enumerate(study_level.documentation, 1):
        drow = {
            "documentation_id": f"{study_id}_doc{i}",
            "study_id": study_id,
            "documentation_file_access": d.documentation_file_access,
            "reference_source": d.reference_source,
            "reference_source_id": d.reference_source_id,
        }
        _emit(drow, "document_name", d.document_name)
        _emit(drow, "documentation_type", d.documentation_type)
        _emit(drow, "citation", d.citation)
        _emit(drow, "creator_role", d.creator_role)
        tables["documentation"].append(_order_row("documentation", drow))

    # ---- material ----
    for i, m in enumerate(study_level.material, 1):
        mrow = {"material_id": f"{study_id}_mat{i}", "reference_source": m.reference_source}
        _emit(mrow, "material_name", m.material_name)
        _emit(mrow, "organization", m.organization)
        tables["material"].append(_order_row("material", mrow))

    # One experiment per study; arms and timepoints remain groups/contrasts.
    # The LLM's experiment COUNT is non-deterministic (1 vs 6 on the same paper — see the
    # determinism check). Time/duration arms are captured as `groups` and split per-contrast in the
    # analysis layer, so we pin a single experiment here and attach every child to it (ei is forced
    # to 1 below). This removes the structural over-split that made the table shape vary run-to-run.
    # (Note: per-condition study SPLITTING — turning 0wk/2wk/… into separate study records with
    # cross-study pairwise comparisons — is handled separately by tools/study_split.py, NOT by
    # multiplying experiments here.)
    experiments = list(design.experiments)
    has_children = bool(design.subjects or design.groups or methods.samples
                        or methods.interventions or methods.assays)
    if experiments:
        experiments = experiments[:1]        # collapse any over-split to the first experiment
    elif has_children:
        experiments = [ExperimentLite()]     # defensive default so children link to exp1
    exp_id_by_index: dict[int, str] = {}
    for ei, exp in enumerate(experiments, 1):
        experiment_id = f"{study_id}_exp{ei}"
        exp_id_by_index[ei] = experiment_id
        erow = {
            "experiment_id": experiment_id,
            "study_id": study_id,
            "documentation_id": None,
            "experiment_control": exp.experiment_control,
        }
        _emit(erow, "experiment_type", exp.experiment_type)
        _emit(erow, "experiment_subject", exp.experiment_subject)
        _emit(erow, "comments", exp.comments)
        tables["experiment"].append(_order_row("experiment", erow))

    def _exp_id(idx) -> str:
        """Resolve a child's experiment_index to an experiment_id (clamp to exp1)."""
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            idx = 1
        return exp_id_by_index.get(idx, exp_id_by_index.get(1, f"{study_id}_exp1"))

    # ---- groups (study-scoped ids), de-duplicated by normalized arm label ----
    # An over-split repeats the same arm across phantom experiments; dedup collapses those to one
    # row per real arm. All groups belong to the single experiment, so the label -> group_id map is
    # keyed by label alone (no experiment_index).
    grp_counter = 0
    label_to_gid: dict[str, str] = {}
    seen_group_keys: set = set()
    for g in design.groups:
        gk = _norm_label(g.subject_group.value) or _norm_label(g.sample_group.value)
        if gk and gk in seen_group_keys:
            continue  # dedup repeated arm
        if gk:
            seen_group_keys.add(gk)
        grp_counter += 1
        group_id = f"{study_id}_grp{grp_counter}"
        grow = {"group_id": group_id, "study_id": study_id}
        _emit(grow, "subject_group", g.subject_group)
        _emit(grow, "sample_group", g.sample_group)
        _emit(grow, "group_size", g.group_size)
        _emit(grow, "min_group_age", g.min_group_age)
        _emit(grow, "min_age_unit", g.min_age_unit)
        _emit(grow, "max_group_age", g.max_group_age)
        _emit(grow, "max_age_unit", g.max_age_unit)
        _emit(grow, "comments", g.comments)
        tables["groups"].append(_order_row("groups", grow))
        for lbl in (_norm_label(g.subject_group.value), _norm_label(g.sample_group.value)):
            if lbl:
                label_to_gid.setdefault(lbl, group_id)

    def _gid_for(label) -> Optional[str]:
        return label_to_gid.get(_norm_label(label))

    # ---- subjects, de-duplicated by normalized (species, lineage, sex, age, type) ----
    # An over-split repeats the same organism per phantom experiment; dedup collapses those.
    experiment_id = _exp_id(1)
    subj_counter = 0
    all_subject_ids: list = []
    seen_subject_keys: set = set()
    for subj in design.subjects:
        skey = (_norm_label(subj.species.value), _norm_label(subj.subject_lineage.value),
                _norm_label(subj.organism_sex.value), _norm_label(subj.organism_age.value),
                _norm_label(subj.subject_type.value))
        if any(skey) and skey in seen_subject_keys:
            continue  # dedup the same organism repeated by an over-split
        if any(skey):
            seen_subject_keys.add(skey)
        subj_counter += 1
        subject_id = f"{experiment_id}_subj{subj_counter}"
        all_subject_ids.append(subject_id)
        subrow = {
            "subject_id": subject_id,
            "experiment_id": experiment_id,
            "group_id": _gid_for(subj.group_label),
        }
        _emit(subrow, "subject_type", subj.subject_type)
        _emit(subrow, "species", subj.species)
        _emit(subrow, "organism_race", subj.organism_race)
        _emit(subrow, "subject_lineage", subj.subject_lineage)
        _emit(subrow, "organism_age", subj.organism_age)
        _emit(subrow, "organism_age_unit", subj.organism_age_unit)
        _emit(subrow, "organism_sex", subj.organism_sex)
        _emit(subrow, "comments", subj.comments)
        tables["subject"].append(_order_row("subject", subrow))

    # ---- samples; organism_id = the lone subject if exactly one, else '0' ----
    organism_fk = all_subject_ids[0] if len(all_subject_ids) == 1 else "0"
    samp_counter = 0
    for samp in methods.samples:
        samp_counter += 1
        samprow = {
            "sample_id": f"{experiment_id}_samp{samp_counter}",
            "organism_id": organism_fk,
            "group_id": _gid_for(samp.group_label),
        }
        _emit(samprow, "biosample_collection", samp.biosample_collection)
        _emit(samprow, "biosample_type", samp.biosample_type)
        _emit(samprow, "expsample_type", samp.expsample_type)
        _emit(samprow, "comments", samp.comments)
        tables["sample"].append(_order_row("sample", samprow))

    # ---- interventions (all under the single experiment) ----
    int_counter = 0
    for iv in methods.interventions:
        int_counter += 1
        ivrow = {
            "intervention_id": f"{experiment_id}_int{int_counter}",
            "experiment_id": experiment_id,
            "subject_id": None,
        }
        _emit(ivrow, "material", iv.material)
        _emit(ivrow, "dosage", iv.dosage)
        _emit(ivrow, "dosage_unit", iv.dosage_unit)
        _emit(ivrow, "intervention_type", iv.intervention_type)
        _emit(ivrow, "intervention_route", iv.intervention_route)
        _emit(ivrow, "t0_definition", iv.t0_definition)
        _emit(ivrow, "intervention_time", iv.intervention_time)
        _emit(ivrow, "time_unit", iv.time_unit)
        _emit(ivrow, "comments", iv.comments)
        tables["interventions"].append(_order_row("interventions", ivrow))

    tables["exercise"].extend(exercise_rows_from_interventions(study_id, tables))

    # ---- assays (all under the single experiment) ----
    assay_counter = 0
    for asy in methods.assays:
        assay_counter += 1
        arow = {
            "assay_id": f"{experiment_id}_assay{assay_counter}",
            "experiment_id": experiment_id,
            "documentation_id": None,
            "organism_input": "true",
        }
        _emit(arow, "assay_name", asy.assay_name)
        _emit(arow, "assay_type", asy.assay_type)
        _emit(arow, "reagents", asy.reagents)
        _emit(arow, "platform", asy.platform)
        tables["assay"].append(_order_row("assay", arow))

    # Override structural tables with a deterministic read of the
    # GEO metadata CSV (one row per real sample, distinct organisms, distinct design-column arms,
    # distinct platforms). This is what makes the structural table SHAPE reproducible run-to-run; the
    # experiment table is already pinned to one row above. Fail-soft: keep the LLM tables on error.
    if metadata_csv and os.path.exists(metadata_csv):
        try:
            struct = build_structural_tables(study_id, _exp_id(1), metadata_csv)
            for t in ("subject", "sample", "groups", "assay"):
                tables[t] = struct[t]
        except Exception as e:
            print(f"      [flatten] metadata-structural derivation failed, keeping LLM "
                  f"subject/sample/groups/assay: {type(e).__name__}: {e}")

    return tables


def _first_exercise_intervention_id(tables: Optional[dict]) -> Optional[str]:
    """Best-effort FK from a text-mined gene to the exercise intervention row.

    The schema's "Exercise" node is represented in this codebase by `interventions`.
    Prefer an intervention whose extracted material/type mentions exercise/training/running;
    otherwise use the first intervention row when one exists.
    """
    rows = (tables or {}).get("interventions") or []
    if not rows:
        return None
    for row in rows:
        if _is_exercise_like_intervention(row):
            return row.get("intervention_id")
    return None


_EXERCISE_TERMS = (
    "exercise",
    "treadmill",
    "wheel running",
    "voluntary wheel",
    "endurance exercise",
    "endurance training",
    "resistance exercise",
    "resistance training",
    "aerobic exercise",
    "aerobic training",
    "sprint exercise",
    "sprint training",
    "hiit",
    "mict",
)


def _is_exercise_like_intervention(row: dict) -> bool:
    # Only the intervention's semantic identity may create an Exercise node. Comments often
    # contain contrast text such as "control group, no exercise intervention"; treating that as
    # positive evidence silently turns a diet/control row into exercise.
    hay = " ".join(str(row.get(c) or "") for c in ("material", "intervention_type")).lower()
    return any(t in hay for t in _EXERCISE_TERMS)


def _has_exercise_terms(*vals) -> bool:
    hay = " ".join(_clean_text(v).lower() for v in vals)
    return any(t in hay for t in _EXERCISE_TERMS)


def _tables_have_exercise_context(tables: Optional[dict]) -> bool:
    if not tables:
        return False
    for row in tables.get("exercise") or []:
        if _has_exercise_terms(
            row.get("exercise_name"), row.get("exercise_type"),
            row.get("exercise_parameters"), row.get("comments"),
        ):
            return True
    for row in tables.get("interventions") or []:
        if _is_exercise_like_intervention(row):
            return True
    for table in ("study", "experiment", "groups"):
        for row in tables.get(table) or []:
            if _has_exercise_terms(*row.values()):
                return True
    return False


def _findings_have_exercise_context(findings: list) -> bool:
    for f in findings or []:
        if _has_exercise_terms(f.get("comparison"), f.get("source")):
            return True
    return False


def _source_for_flat_field(row: dict, field: str) -> Optional[str]:
    return row.get(f"{field}_source")


def _clean_text(val) -> str:
    if val is None:
        return ""
    text = str(val).strip()
    if not text or text.lower() in {"nan", "none", "<na>"}:
        return ""
    return text


def _first_nonempty(*vals) -> Optional[str]:
    for val in vals:
        text = _clean_text(val)
        if text:
            return text
    return None


def _exercise_row_from_intervention(study_id: str, intervention: dict, ordinal: int) -> dict:
    experiment_id = intervention.get("experiment_id") or f"{study_id}_exp1"
    intervention_id = intervention.get("intervention_id")
    source = _first_nonempty(
        _source_for_flat_field(intervention, "material"),
        _source_for_flat_field(intervention, "intervention_type"),
        _source_for_flat_field(intervention, "comments"),
        "derived from exercise-like intervention row",
    )

    duration = " ".join(
        v for v in [
            _clean_text(intervention.get("intervention_time")),
            _clean_text(intervention.get("time_unit")),
        ] if v
    ) or None
    dose = " ".join(
        v for v in [
            _clean_text(intervention.get("dosage")),
            _clean_text(intervention.get("dosage_unit")),
        ] if v
    ) or None
    params = "; ".join(v for v in (dose, duration) if v) or None

    row = {
        "exercise_id": f"{experiment_id}_exercise{ordinal}",
        "study_id": study_id,
        "experiment_id": experiment_id,
        "intervention_id": intervention_id,
        "group_id": None,
        "exercise_name": _first_nonempty(intervention.get("material"), intervention.get("intervention_type"), "exercise"),
        "exercise_name_source": source,
        "exercise_type": _first_nonempty(intervention.get("intervention_type"), intervention.get("material"), "exercise"),
        "exercise_type_source": _first_nonempty(_source_for_flat_field(intervention, "intervention_type"), source),
        "exercise_parameters": params,
        "exercise_parameters_source": _first_nonempty(
            _source_for_flat_field(intervention, "dosage"),
            _source_for_flat_field(intervention, "intervention_time"),
            source if params else None,
        ),
        "t0_definition": intervention.get("t0_definition"),
        "t0_definition_source": _source_for_flat_field(intervention, "t0_definition"),
        "exercise_time": intervention.get("intervention_time"),
        "exercise_time_source": _source_for_flat_field(intervention, "intervention_time"),
        "time_unit": intervention.get("time_unit"),
        "time_unit_source": _source_for_flat_field(intervention, "time_unit"),
        "comments": "explicit exercise process node derived from intervention",
        "comments_source": source,
    }
    return _order_row("exercise", row)


def exercise_rows_from_interventions(study_id: str, tables: Optional[dict]) -> list[dict]:
    """Derive ontology-level `exercise` rows from exercise-like intervention rows.

    This keeps the LLM surface stable: interventions are still extracted once, and the direct
    Exercise node is a deterministic projection used by gene.exercise_id.
    """
    if tables is None:
        return []
    out = []
    existing_intervention_ids = {
        row.get("intervention_id") for row in (tables.get("exercise") or []) if row.get("intervention_id")
    }
    n = len(tables.get("exercise") or [])
    for intervention in tables.get("interventions") or []:
        iid = intervention.get("intervention_id")
        if iid and iid in existing_intervention_ids:
            continue
        if not _is_exercise_like_intervention(intervention):
            continue
        n += 1
        out.append(_exercise_row_from_intervention(study_id, intervention, n))
    return out


def _first_exercise_id(tables: Optional[dict], intervention_id: Optional[str] = None) -> Optional[str]:
    rows = (tables or {}).get("exercise") or []
    if intervention_id:
        for row in rows:
            if row.get("intervention_id") == intervention_id:
                return row.get("exercise_id")
    for row in rows:
        if row.get("exercise_id"):
            return row.get("exercise_id")
    return None


def _exercise_source_from_tables(tables: Optional[dict]) -> Optional[str]:
    """Find a compact provenance hint for a derived exercise intervention."""
    for row in (tables or {}).get("groups") or []:
        for col in ("subject_group_source", "sample_group_source", "comments_source"):
            val = row.get(col)
            if val and "exercise" in str(val).lower():
                return str(val)
    return "derived from paper-reported exercise gene findings"


def ensure_gene_exercise_scaffold(
    study_id: str,
    tables: Optional[dict],
    scaffold_rows: Optional[dict] = None,
    allow_create: bool = True,
) -> tuple[str, Optional[str], Optional[str]]:
    """Ensure text-mined gene rows have experiment + exercise-intervention FKs.

    Metadata-structural extraction can replace LLM design rows with deterministic
    subject/sample/groups/assay rows, leaving no intervention row even when group labels
    encode exercise parameters. For the gene table, create a minimal exercise intervention
    only when none exists; callers can collect the added rows into their own append batch.
    """
    experiment_id = None
    if tables and tables.get("experiment"):
        experiment_id = tables["experiment"][0].get("experiment_id")
    experiment_id = experiment_id or f"{study_id}_exp1"

    if tables is not None and not tables.get("experiment"):
        exp = _order_row("experiment", {
            "experiment_id": experiment_id,
            "study_id": study_id,
            "documentation_id": None,
            "experiment_control": None,
            "experiment_type": "exercise-associated reported gene comparison",
            "experiment_type_source": "derived from paper-reported gene findings",
            "experiment_subject": None,
            "experiment_subject_source": None,
            "comments": "minimal scaffold for gene-to-exercise foreign keys",
            "comments_source": "derived from paper-reported gene findings",
        })
        tables.setdefault("experiment", []).append(exp)
        if scaffold_rows is not None:
            scaffold_rows.setdefault("experiment", []).append(exp)

    intervention_id = _first_exercise_intervention_id(tables)
    if not intervention_id and not allow_create:
        return experiment_id, None, None
    if tables is not None and not intervention_id:
        n = len(tables.get("interventions") or []) + 1
        source = _exercise_source_from_tables(tables)
        intervention = _order_row("interventions", {
            "intervention_id": f"{experiment_id}_int{n}",
            "experiment_id": experiment_id,
            "subject_id": None,
            "material": "exercise",
            "material_source": source,
            "dosage": None,
            "dosage_source": None,
            "dosage_unit": None,
            "dosage_unit_source": None,
            "intervention_type": "exercise",
            "intervention_type_source": source,
            "intervention_route": None,
            "intervention_route_source": None,
            "t0_definition": None,
            "t0_definition_source": None,
            "intervention_time": None,
            "intervention_time_source": None,
            "time_unit": None,
            "time_unit_source": None,
            "comments": "minimal scaffold for gene-to-exercise foreign keys",
            "comments_source": "derived from paper-reported gene findings",
        })
        tables.setdefault("interventions", []).append(intervention)
        intervention_id = intervention["intervention_id"]
        if scaffold_rows is not None:
            scaffold_rows.setdefault("interventions", []).append(intervention)

    exercise_id = _first_exercise_id(tables, intervention_id)
    if tables is not None and intervention_id and not exercise_id:
        intervention = None
        for row in tables.get("interventions") or []:
            if row.get("intervention_id") == intervention_id:
                intervention = row
                break
        if intervention is not None:
            n = len(tables.get("exercise") or []) + 1
            exercise = _exercise_row_from_intervention(study_id, intervention, n)
            tables.setdefault("exercise", []).append(exercise)
            exercise_id = exercise["exercise_id"]
            if scaffold_rows is not None:
                scaffold_rows.setdefault("exercise", []).append(exercise)

    return experiment_id, intervention_id, exercise_id


def gene_rows_from_reported_findings(
    study_id: str,
    findings: list,
    organism: str = "",
    tables: Optional[dict] = None,
    scaffold_rows: Optional[dict] = None,
) -> list[dict]:
    """Convert paper-reported gene findings into schema-conformant `gene` rows.

    Scope is intentionally text evidence: named genes the paper explicitly compared/reported,
    not every row in a DEG matrix. Each row keeps the exact paper quote as provenance via the
    Sourced columns. `pathway_id` is left null so pathway modeling can be added later.
    """
    out = []
    seen = set()
    has_exercise_context = (
        _tables_have_exercise_context(tables) or _findings_have_exercise_context(findings)
    )
    if not has_exercise_context:
        return out
    experiment_id, intervention_id, exercise_id = ensure_gene_exercise_scaffold(
        study_id, tables, scaffold_rows=scaffold_rows, allow_create=True
    )

    for f in findings or []:
        entity_type = str(f.get("entity_type") or "").strip().lower()
        if "gene" not in entity_type:
            continue
        symbol = str(f.get("entity") or "").strip()
        if not symbol or symbol.lower() in {"gene", "genes", "multiple genes", "several genes"}:
            continue
        source = (f.get("source") or "").strip() or None
        comparison = f.get("comparison")
        direction = f.get("direction")
        magnitude = f.get("magnitude")
        key = (symbol.lower(), str(comparison or "").lower(), str(direction or "").lower())
        if key in seen:
            continue
        seen.add(key)
        n = len(out) + 1
        row = {
            "gene_id": f"{study_id}_gene{n}",
            "study_id": study_id,
            "experiment_id": experiment_id,
            "intervention_id": intervention_id,
            "exercise_id": exercise_id,
            "group_id": None,
            "pathway_id": None,
            "gene_symbol": symbol,
            "gene_symbol_source": source,
            "gene_name": None,
            "gene_name_source": None,
            "organism": organism or None,
            "comparison": comparison,
            "comparison_source": source if comparison else None,
            "regulation_direction": direction,
            "magnitude": magnitude,
            "magnitude_source": source if magnitude else None,
            "relationship_to_exercise": "is_regulated_by",
            "reference_source": "paper",
            "reference_source_id": study_id,
        }
        out.append(_order_row("gene", row))
    return out


def pathway_rows_from_reported_findings(study_id: str, findings: list) -> list[dict]:
    """Convert paper-reported pathway/process findings into descriptive pathway nodes.

    These are intentionally not standardized pathway IDs. They preserve the paper's own
    wording as a text-derived node so ontology/normalization can happen later.
    """
    out = []
    seen = set()
    for f in findings or []:
        entity_type = str(f.get("entity_type") or "").strip().lower()
        if "pathway" not in entity_type:
            continue
        name = str(f.get("entity") or "").strip()
        if not name or name.lower() in {"pathway", "pathways", "signaling pathway"}:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        n = len(out) + 1
        row = {
            "pathway_id": f"{study_id}_pathway_text{n}",
            "pathway_name": name,
            "library": "paper_text",
            "collection_version": study_id,
            "n_genes": None,
        }
        out.append(_order_row("pathway", row))
    return out


# --- IO --------------------------------------------------------------------------------

def write_study_tables_json(study_id: str, tables: dict, out_dir: str = "./output") -> str:
    study_dir = os.path.join(out_dir, study_id)
    os.makedirs(study_dir, exist_ok=True)
    path = os.path.join(study_dir, "seacdm_tables.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)
    return path


def append_tables_to_csvs(tables: dict, out_dir: str) -> list[str]:
    """Append each table's rows to its cohort CSV (creating with header if absent).
    Used both for single-study demo output and Phase 3 cohort aggregation."""
    import csv
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for table, rows in tables.items():
        cols = csv_columns(table)
        if not cols:  # deferred (ontology) — never written
            continue
        path = os.path.join(out_dir, SEA_TABLES[table]["csv"])
        new_file = not os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            if new_file:
                w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c) for c in cols})
        if rows:
            written.append(path)
    return written


# --- Provenance verification: each `_source` quote must be a real substring of the text ----

_UNVERIFIED = "[UNVERIFIED]"
_WS = re.compile(r"\s+")
# Normalize punctuation the LLM commonly re-renders (curly quotes, dashes) so a faithful
# quote isn't flagged just because it straightened a quote mark.
_PUNCT_MAP = str.maketrans({
    "‘": "'", "’": "'", "‛": "'",       # curly single quotes / apostrophes
    "“": '"', "”": '"',                       # curly double quotes
    "–": "-", "—": "-", "−": "-",        # en/em dash, minus
})


def _norm_quote(s: str) -> str:
    """Lowercase, fold common punctuation variants, and collapse all whitespace (incl.
    newlines from PDF/XML line-wrapping) to single spaces — so substring matching compares
    content, not formatting. Returns '' for None/blank."""
    if not s:
        return ""
    return _WS.sub(" ", s.translate(_PUNCT_MAP)).strip().lower()


# Ellipsis variants the LLM uses to STITCH a quote from non-adjacent spans ('A ... B'). A
# stitched quote is faithful if every fragment is itself verbatim, so we verify per-fragment
# rather than flagging the whole thing — this is the main source of false [UNVERIFIED] flags.
_ELLIPSIS = re.compile(r"\.\s*\.\s*\.+|…+")


def _quote_is_verbatim(raw: str, norm_text: str) -> bool:
    """True if the quote is a verbatim substring of the paper text — OR if it is a faithful
    STITCHED quote: split on ellipsis, every non-trivial fragment (>=8 normalized chars) is a
    verbatim substring, and there are >=2 such fragments."""
    nq = _norm_quote(raw)
    if not nq:
        return True  # blank handled upstream
    if nq in norm_text:
        return True
    frags = [f for f in (_norm_quote(p) for p in _ELLIPSIS.split(raw)) if len(f) >= 8]
    return len(frags) >= 2 and all(f in norm_text for f in frags)


def _snap_to_verbatim(source: str, paper_text: str, norm_text: str, min_chars: int = 24) -> str:
    """Snap a near-verbatim quote DOWN to its real core: return the longest CONTIGUOUS run of words
    from `source` that is an actual substring of the paper (>= min_chars normalized), recovered in
    the paper's ORIGINAL casing/spacing. '' if no run is long enough.

    Deterministic safety net for #5: the model sometimes lightly rephrases a quote (drops a word,
    merges clauses). Rather than flag the whole thing [UNVERIFIED], we keep the genuine verbatim
    fragment it was built around as the source anchor; the structured entity/direction/comparison
    fields carry the interpretation. Fully fabricated quotes (no run >= min_chars) still get flagged."""
    words = (source or "").split()
    n = len(words)
    if n < 2:
        return ""
    for size in range(n, 1, -1):                 # try the longest windows first
        for i in range(n - size + 1):
            window = words[i:i + size]
            normw = _norm_quote(" ".join(window))
            if len(normw) >= min_chars and normw in norm_text:
                pat = re.compile(r"\s+".join(re.escape(w) for w in window), re.IGNORECASE)
                m = pat.search(paper_text)
                return m.group(0) if m else " ".join(window)
    return ""


def _provenance_source_cols(table: str) -> set:
    """The set of `<field>_source` columns for `table` that are genuine provenance companions
    of a Sourced field — EXCLUDING plain data fields that merely end in '_source'
    (e.g. documentation.reference_source = 'PubMed', which must NOT be checked against the text)."""
    model = SEA_TABLES[table]["model"]
    if model is None:
        return set()
    return {f"{name}_source" for name, info in model.model_fields.items() if info.annotation is Sourced}


def verify_provenance(tables: dict, paper_text: str) -> dict:
    """Programmatically enforce the provenance contract that the prompts only *ask* for:
    every Sourced `<field>_source` quote MUST be a verbatim substring of the paper text.
    Quotes that are not found are prefixed in-place with '[UNVERIFIED] ' (so a fabricated /
    paraphrased citation is visible in both the JSON and the CSVs — fail-loud, consistent with
    the GSE literal-presence cross-check), and the value is left intact for human review.

    Mutates `tables` in place. Returns a summary {n_total, n_verified, n_unverified, items[]}
    where each item = {table, field, value, claimed_source}."""
    norm_text = _norm_quote(paper_text)
    items, n_total, n_unverified = [], 0, 0
    for table, rows in tables.items():
        src_cols = _provenance_source_cols(table)
        if not src_cols:
            continue
        for row in rows:
            for col in src_cols:
                raw = row.get(col)
                if not raw or not str(raw).strip():
                    continue
                if str(raw).startswith(_UNVERIFIED):  # idempotent: don't double-mark
                    n_total += 1
                    n_unverified += 1
                    continue
                n_total += 1
                # Metadata column references are structured provenance, not paper quotes.
                if str(raw).startswith(META_SOURCE_PREFIX):
                    continue
                if _quote_is_verbatim(str(raw), norm_text):
                    continue
                n_unverified += 1
                value_col = col[: -len("_source")]
                items.append({
                    "table": table, "field": value_col,
                    "value": row.get(value_col), "claimed_source": raw,
                })
                row[col] = f"{_UNVERIFIED} {raw}"
    return {
        "n_total": n_total,
        "n_verified": n_total - n_unverified,
        "n_unverified": n_unverified,
        "items": items,
    }


def _paper_regions(paper_text: str) -> dict[str, str]:
    """Return coarse article regions without depending on line breaks in PMC plain text."""
    references = paper_text.find(" References ")
    body = paper_text[:references] if references > 0 else paper_text
    discussion = body.find(" Discussion ")
    methods = body.find(" Methods ", max(0, discussion))
    data_availability = body.find(" Data availability ", max(0, methods))
    results = body.find(" Results ")
    return {
        "body": body,
        "results_discussion": body[max(0, results):methods if methods > 0 else len(body)],
        "methods": body[methods:data_availability if data_availability > methods else len(body)]
        if methods > 0 else body,
        "data_availability": body[data_availability:data_availability + 5000]
        if data_availability > 0 else "",
    }


def _ranked_chunks(text: str, terms: tuple[str, ...], *, chunk_size: int = 14000,
                   overlap: int = 1400, max_chunks: int = 3) -> list[str]:
    if not text:
        return []
    ranked = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        low = chunk.lower()
        score = sum(low.count(term.lower()) for term in terms)
        ranked.append((score, start, chunk))
        if start + chunk_size >= len(text):
            break
    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected = [chunk for score, _, chunk in ranked[:max_chunks] if score > 0]
    return selected or [text[:chunk_size]]


def _sourced_value(item, field: str) -> str:
    value = getattr(item, field, None)
    if hasattr(value, "value"):
        value = value.value
    return re.sub(r"\W+", " ", str(value or "").lower()).strip()


def _dedupe_models(items: list, key_fields: tuple[str, ...]) -> list:
    kept = []
    seen = set()
    for item in items:
        key = tuple(_sourced_value(item, field) for field in key_fields)
        if not any(key) or key in seen:
            continue
        seen.add(key)
        kept.append(item)
    return kept


def _extract_staged_lean(study_id: str, paper_text: str, organism: str, *, usage=None,
                         report: Optional[dict] = None, max_retries: int = 1,
                         metadata_csv: Optional[str] = None):
    """DeepSeek-oriented map/reduce extraction with deterministic completion gates.

    Each call owns a small schema and a focused paper region. Required empty outputs are retried;
    every attempt is recorded in ``decision_trace`` so a syntactically valid but incomplete object
    can no longer pass silently.
    """
    regions = _paper_regions(paper_text)
    body = regions["body"]
    trace: list[dict] = []
    errors: dict[str, str] = {}

    def run_stage(name, contexts, fn, complete, count):
        last = None
        attempts = min(len(contexts), max_retries + 1)
        for index, context in enumerate(contexts[:attempts], start=1):
            before = len(usage) if usage is not None else 0
            event = {"stage": name, "attempt": index, "input_chars": len(context)}
            try:
                last = fn(context, study_id, organism, usage=usage)
                event["record_count"] = count(last)
                event["status"] = "complete" if complete(last) else "incomplete"
            except Exception as exc:
                event["status"] = "error"
                event["error"] = f"{type(exc).__name__}: {exc}"
            if usage is not None and len(usage) > before:
                event["llm"] = usage[-1]
            trace.append(event)
            if last is not None and complete(last):
                return last
        errors[name] = trace[-1].get("error") or "completion gate failed"
        return last

    study_primary = body[:18000].strip()
    study_retry = body[:30000].strip()
    study_only = run_stage(
        "study", [study_primary, study_retry], _extract_study_only,
        lambda x: bool(_sourced_value(x.study, "study_name")), lambda x: 1,
    ) or StudyOnlyExtraction()
    documentation_primary = (body[:7000] + "\n" + regions["data_availability"]).strip()
    documentation_retry = (body[:14000] + "\n" + regions["data_availability"]).strip()
    documentation_only = run_stage(
        "documentation", [documentation_primary, documentation_retry],
        _extract_documentation_only, lambda x: len(x.documentation) == 1,
        lambda x: len(x.documentation),
    ) or DocumentationOnlyExtraction()
    if (not _sourced_value(study_only.study, "study_name") and
            documentation_only.documentation and
            _sourced_value(documentation_only.documentation[0], "document_name")):
        # Title is the same fact in both SEA-CDM tables. DeepSeek occasionally fills the
        # documentation title but omits study_name; reuse the independently grounded value instead
        # of spending another nondeterministic call or accepting an empty required field.
        study_only.study.study_name = documentation_only.documentation[0].document_name.model_copy(
            deep=True
        )
        errors.pop("study", None)
        trace.append({
            "stage": "repair_study_name",
            "attempt": 0,
            "status": "complete",
            "record_count": 1,
            "method": "copied grounded documentation.document_name",
        })

    design_terms = (
        "exercise protocol", "wheel-running", "running wheel", "experimental design",
        "viral", "injection", "treatment", "sedentary", "mice were", "days of exercise",
    )
    design_chunks = _ranked_chunks(body, design_terms, max_chunks=4)
    scope_context = ""
    if metadata_csv:
        try:
            scope_context = summarize_geo_scope(metadata_csv)
        except Exception as exc:
            trace.append({
                "stage": "geo_scope_context", "attempt": 0, "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
            })
    scope_prefix = (
        f"[TARGET GEO SCOPE]\n{scope_context}\n[END TARGET GEO SCOPE]\n\n"
        if scope_context else ""
    )
    design_primary = scope_prefix + "\n\n[EXCERPT]\n".join(design_chunks[:3])
    design_retry = scope_prefix + "\n\n[EXCERPT]\n".join(design_chunks)
    scope_requires_exercise = _has_exercise_terms(scope_context)

    def design_complete(extraction):
        basic = bool(
            len(extraction.experiments) == 1
            and extraction.interventions
            and all(iv.experiment_index == 1 for iv in extraction.interventions)
        )
        if not basic or not scope_requires_exercise:
            return basic
        return any(_has_exercise_terms(
            _sourced_value(iv, "material"), _sourced_value(iv, "intervention_type")
        ) for iv in extraction.interventions)

    design = run_stage(
        "experiment_interventions", [design_primary, design_retry],
        _extract_experiment_interventions,
        design_complete,
        lambda x: len(x.experiments) + len(x.interventions),
    ) or ExperimentInterventionExtraction()

    material_terms = (
        "antibody", "kit", "software", "microscope", "sequenc", "instrument",
        "manufacturer", "purchased", "catalog", "rrid", "version", "aav",
    )
    material_chunks = _ranked_chunks(regions["methods"], material_terms, max_chunks=4)
    materials = []
    for chunk_index, chunk in enumerate(material_chunks, start=1):
        ext = run_stage(
            f"materials_chunk_{chunk_index}", [chunk, chunk], _extract_materials,
            lambda x: bool(x.material), lambda x: len(x.material),
        )
        if ext is not None:
            materials.extend(ext.material)
    materials = _dedupe_models(materials, ("material_name", "organization"))
    if materials:
        for key in list(errors):
            if key.startswith("materials_chunk_"):
                errors.pop(key, None)

    finding_chunks = _finding_chunks(regions["results_discussion"], max_chunks=4)
    findings = []
    for chunk_index, chunk in enumerate(finding_chunks, start=1):
        ext = run_stage(
            f"findings_chunk_{chunk_index}", [chunk, chunk], _extract_reported_findings,
            lambda x: bool(x.findings), lambda x: len(x.findings),
        )
        if ext is not None:
            findings.extend(ext.findings)
    findings = _dedupe_models(findings, ("entity", "direction", "comparison"))
    if findings:
        for key in list(errors):
            if key.startswith("findings_chunk_"):
                errors.pop(key, None)

    if report is not None:
        report["decision_trace"] = trace
        report["stage_errors"] = errors
        report["staged_regions"] = {name: len(text) for name, text in regions.items()}
        report["geo_scope_policy"] = "target_accession" if scope_context else "paper_only"
        report["geo_scope_context"] = scope_context
    return (
        StudyLevelExtraction(study=study_only.study,
                             documentation=documentation_only.documentation,
                             material=materials),
        DesignExtraction(experiments=design.experiments, subjects=[], groups=[]),
        MethodsExtraction(samples=[], interventions=design.interventions, assays=[]),
        [finding.model_dump() for finding in findings],
        errors,
    )


def extract_tables_from_text(
    study_id: str,
    paper_text: str,
    organism: str = "",
    verify: bool = True,
    report: Optional[dict] = None,
    metadata_csv: Optional[str] = None,
    lean: Optional[bool] = None,
    usage: Optional[list] = None,
    strategy: str = "single",
    max_stage_retries: int = 1,
) -> dict:
    """Extract SEA-CDM tables without writing files.

    ``strategy='single'`` preserves the original one-call LEAN extraction. ``strategy='staged'``
    uses focused small-schema calls with deterministic completion gates and targeted retries.
    The three-call FULL fallback is Legacy and runs only when metadata is unavailable or explicitly
    requested with ``lean=False``. Source quotes are verified by default.
    """
    if metadata_csv is None:
        _cand = os.path.join("data", study_id, f"{study_id}_metadata.csv")
        if os.path.exists(_cand):
            metadata_csv = _cand
    have_meta = bool(metadata_csv and os.path.exists(metadata_csv))
    use_lean = (have_meta if lean is None else bool(lean)) and have_meta

    group_errors = {}
    lean_findings = []

    def _safe(fn, empty, name):
        try:
            return fn(paper_text, study_id, organism, usage=usage)
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            group_errors[name] = msg
            print(f"      [extract] group '{name}' failed, using empty container: {msg.splitlines()[0][:200]}")
            return empty

    if strategy not in {"single", "staged"}:
        raise ValueError("strategy must be 'single' or 'staged'")

    if use_lean and strategy == "staged":
        study_level, design, methods, lean_findings, staged_errors = _extract_staged_lean(
            study_id, paper_text, organism, usage=usage, report=report,
            max_retries=max_stage_retries, metadata_csv=metadata_csv,
        )
        group_errors.update(staged_errors)
        if verify and lean_findings:
            frep = verify_findings_provenance(lean_findings, paper_text)
            if report is not None:
                report["findings_verify"] = frep
        if report is not None:
            report["reported_findings"] = lean_findings
    elif use_lean:
        lean_ext = _safe(_extract_lean, LeanExtraction(), "lean")
        study_level = StudyLevelExtraction(study=lean_ext.study,
                                           documentation=lean_ext.documentation,
                                           material=lean_ext.material)
        design = DesignExtraction(experiments=lean_ext.experiments, subjects=[], groups=[])
        methods = MethodsExtraction(samples=[], interventions=lean_ext.interventions, assays=[])
        lean_findings = [f.model_dump() for f in lean_ext.reported_findings]
        if verify and lean_findings:
            frep = verify_findings_provenance(lean_findings, paper_text)
            if report is not None:
                report["findings_verify"] = frep
        if report is not None:
            report["reported_findings"] = lean_findings
    else:
        # LEGACY fallback: three full-text calls. Kept for papers without GEO metadata.
        study_level = _safe(_extract_study_level, StudyLevelExtraction(), "study_level")
        design = _safe(_extract_design, DesignExtraction(), "design")
        methods = _safe(_extract_methods, MethodsExtraction(), "methods")

    tables = flatten_extraction(study_id, study_level, design, methods, metadata_csv=metadata_csv)
    if report is not None:
        report["metadata_structural"] = have_meta
        report["extraction_mode"] = (
            "lean(staged)" if use_lean and strategy == "staged" else
            "lean(1-call)" if use_lean else "full(3-call)"
        )
        report["legacy_mode"] = not use_lean
        if metadata_csv:
            report["metadata_csv"] = metadata_csv
    if report is not None and group_errors:
        report["group_errors"] = group_errors
    if verify:
        rep = verify_provenance(tables, paper_text)
        if report is not None:
            report.update(rep)
    return tables


# Reported-findings extraction and result rows.

_FINDINGS_COLUMNS = ["entity", "entity_type", "direction", "magnitude", "comparison", "source"]


def _extract_reported_findings(paper_text: str, study_id: str, organism: str,
                               usage=None) -> ReportedFindingsExtraction:
    llm = _get_llm()
    if llm is None:
        return ReportedFindingsExtraction()
    structured = _structured_runnable(llm, ReportedFindingsExtraction, usage)
    prompt = f"""You are extracting the SPECIFIC GENE/PHENOTYPE FINDINGS this paper REPORTS — i.e.
which named genes/proteins or physiological measurements CHANGED as a result of the intervention.
This is the article-evidence layer used for later reconciliation against computed DEG results.

Target study: {study_id}{f' (organism: {organism})' if organism else ''}

Return a flat list `findings`. ONE entry per concrete reported change:
- `entity`: the gene / protein / metabolite / lipid / phenotype/measurement that changed
  (e.g. 'PGC-1alpha', 'IL-6', 'VO2max', 'grip strength'). Do NOT extract pathway/process names
  such as 'AMPK signaling pathway' or 'mitochondrial biogenesis' here; pathways are computed from
  GSEA/enrichment data.
- `entity_type`: gene / protein / metabolite / lipid / phenotype / other. Do NOT use pathway.
- `direction`: up / down / changed / unchanged / n/a (relative to the control or baseline).
- `magnitude`: the fold-change / percent / p-value / qualifier IF the paper states one, else null.
- `comparison`: the contrast it refers to (e.g. 'trained vs sedentary', '24h post vs pre-exercise').
- `source`: a CONTIGUOUS, CHARACTER-FOR-CHARACTER copy of text from the paper (a real substring).

THE `source` RULE IS THE MOST IMPORTANT ONE — follow it literally:
- COPY, don't rephrase. `source` must be text you can find by Ctrl-F in the paper. Pick the SHORTEST
  exact run of words that names the entity and its change. A 6-12 word exact fragment is ideal.
- Do NOT, under any circumstances: merge two clauses into one, drop or add words, expand or contract
  abbreviations, fix grammar/spelling, or re-order anything. Write every gene/protein name EXACTLY as
  the paper prints it — do not add OR remove a species/case prefix (if the paper writes "mHnrnpa3"
  keep "mHnrnpa3"; if it writes "Hnrnpa3" keep "Hnrnpa3"). Putting the structured interpretation in
  entity/direction/comparison is your job — `source` stays a raw quote.
- The interpretation can be broader than the quote. The quote only has to PROVE the change is stated;
  entity/direction/comparison hold your reading of it.
- If the statement is split across the text, you MAY join TWO exact fragments with ' ... ' (space dot
  dot dot space); EACH fragment must itself be an exact copy (>=8 chars). Never write words between
  them that aren't in the paper.
- SELF-CHECK before returning each finding: re-read your `source` and confirm those exact characters
  appear in the paper above. If they don't, SHORTEN `source` to the longest run you CAN copy exactly
  (even just the entity name plus one or two surrounding words). Only drop the finding if no exact
  phrase mentioning the entity exists at all.

GOOD source: paper says "Hnrnpa3 showed a 28.5% shift at 24 h post-exercise" -> entity 'Hnrnpa3',
  direction 'changed', magnitude '28.5%', source "Hnrnpa3 showed a 28.5% shift".
BAD source (paraphrase — will be rejected): "61 RBPs, including mHnrnpa3 (28.5% at 24pe)" when the
  paper never wrote that exact string. BAD: "the expression of 5 genes ... were observed to be
  downregulated" when you reconstructed the sentence instead of copying a real run of words.

Other rules (STRICT):
- Extract ONLY findings the paper EXPLICITLY states (Abstract / Results / Discussion). DO NOT infer,
  summarize loosely, or invent entities, numbers, or directions.
- Prefer specific named entities over vague statements. Skip pure methods/background sentences.
- If the paper reports no concrete molecular/physiological changes, return an empty list.

------- PAPER TEXT START -------
{paper_text}
------- PAPER TEXT END -------
"""
    return structured.invoke(prompt)


_FINDINGS_CHUNK_TERMS = (
    "gene", "genes", "mrna", "rna-seq", "rnaseq", "transcript", "expression",
    "differential", "deg", "up-regulated", "upregulated", "down-regulated",
    "downregulated", "increased", "decreased", "exercise", "training",
)


def _finding_chunks(paper_text: str, chunk_size: int = 12000, overlap: int = 1200,
                    max_chunks: int = 4) -> list[str]:
    """Pick compact chunks most likely to contain reported molecular findings."""
    if not paper_text:
        return []
    chunks = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(paper_text), step):
        chunk = paper_text[start:start + chunk_size]
        low = chunk.lower()
        score = sum(low.count(t) for t in _FINDINGS_CHUNK_TERMS)
        chunks.append((score, start, chunk))
        if start + chunk_size >= len(paper_text):
            break
    chunks.sort(key=lambda x: (-x[0], x[1]))
    return [c for score, _, c in chunks[:max_chunks] if score > 0]


def extract_reported_findings_chunked(study_id: str, paper_text: str, organism: str = "",
                                      verify: bool = True, report: Optional[dict] = None,
                                      usage=None) -> list:
    """Fallback for long papers whose single structured findings call hits output caps."""
    findings = []
    seen = set()
    n_chunks = 0
    for chunk in _finding_chunks(paper_text):
        n_chunks += 1
        try:
            ext = _extract_reported_findings(chunk, study_id, organism, usage=usage)
        except Exception:
            continue
        for item in [f.model_dump() for f in ext.findings]:
            key = (
                str(item.get("entity") or "").strip().lower(),
                str(item.get("entity_type") or "").strip().lower(),
                str(item.get("comparison") or "").strip().lower(),
                str(item.get("direction") or "").strip().lower(),
            )
            if not key[0] or key in seen:
                continue
            seen.add(key)
            findings.append(item)
    if verify and findings:
        rep = verify_findings_provenance(findings, paper_text)
        if report is not None:
            report.update(rep)
    if report is not None:
        report["n_findings"] = len(findings)
        report["findings_chunked_fallback"] = True
        report["findings_chunks"] = n_chunks
    return findings


def verify_findings_provenance(findings: list, paper_text: str) -> dict:
    """Same verbatim-quote contract as verify_provenance, but for the flat `source` field of each
    reported finding. Mutates findings in place (prefixes unverifiable quotes with [UNVERIFIED]).
    Returns {n_total, n_verified, n_unverified}."""
    norm_text = _norm_quote(paper_text)
    n_total = n_unver = n_snapped = 0
    for f in findings:
        src = (f.get("source") or "").strip()
        if not src:
            continue
        n_total += 1
        if str(src).startswith(_UNVERIFIED):
            n_unver += 1
            continue
        if _quote_is_verbatim(str(src), norm_text):
            continue
        # Before flagging, try to SNAP the quote down to its genuine verbatim core (a lightly
        # rephrased quote usually wraps a real fragment). Only flag if nothing long enough survives.
        snap = _snap_to_verbatim(str(src), paper_text, norm_text)
        if snap and _quote_is_verbatim(snap, norm_text):
            f["source"] = snap
            n_snapped += 1
            continue
        n_unver += 1
        f["source"] = f"{_UNVERIFIED} {src}"
    return {"n_total": n_total, "n_verified": n_total - n_unver,
            "n_unverified": n_unver, "n_snapped": n_snapped}


def extract_reported_findings(study_id: str, paper_text: str, organism: str = "",
                              verify: bool = True, report: Optional[dict] = None,
                              usage=None) -> list:
    """Run the single findings call and return a list of finding dicts. Pure (no disk writes).
    When `verify`, each `source` quote is checked verbatim against paper_text. If `report` is
    passed it is updated with {n_total, n_verified, n_unverified, n_findings}. `usage` (a list)
    captures the call's token counts for the cost profiler."""
    if len(paper_text or "") > 30000:
        if report is not None:
            report["findings_chunked_fallback"] = False
            report["findings_chunked_mode"] = "long_text"
        return extract_reported_findings_chunked(
            study_id, paper_text, organism, verify=verify, report=report, usage=usage
        )
    ext = _extract_reported_findings(paper_text, study_id, organism, usage=usage)
    findings = [f.model_dump() for f in ext.findings]
    if not findings and len(paper_text or "") > 30000:
        findings = extract_reported_findings_chunked(
            study_id, paper_text, organism, verify=verify, report=report, usage=usage
        )
        return findings
    if verify:
        rep = verify_findings_provenance(findings, paper_text)
        if report is not None:
            report.update(rep)
    if report is not None:
        report["n_findings"] = len(findings)
    return findings


def build_reported_findings(study_id: str, paper_text: str, findings_csv_path: str,
                            organism: str = "", verify: bool = True,
                            report: Optional[dict] = None,
                            prefetched_findings: Optional[list] = None,
                            existing_tables: Optional[dict] = None,
                            usage=None) -> dict:
    """Extract reported findings, write them to findings_csv_path,
    and return {'analysis': [row], 'results': [row]} contributions for the SEA-CDM model so a study
    with no computable data still has non-empty results. Returns empty lists when no findings.

    IDs are text-specific ('{study}_analysis_text1' / '{study}_res_text1') so they never collide
    with the computational analysis/results rows that run_batch_geo_pipeline produces for own GSEs.

    When `prefetched_findings` is provided (the lean merged extraction already
    pulled them — see extract_tables_from_text), they are REUSED directly and NO separate findings
    LLM call is made. Pass None to keep the standalone behavior (one dedicated call)."""
    import csv
    if prefetched_findings is not None:
        findings = prefetched_findings
        if report is not None:
            report["n_findings"] = len(findings)
            report.setdefault("n_unverified",
                              sum(1 for f in findings if str(f.get("source") or "").startswith(_UNVERIFIED)))
    else:
        findings = extract_reported_findings(study_id, paper_text, organism, verify=verify,
                                             report=report, usage=usage)
    out = {"analysis": [], "results": [], "gene": [], "pathway": [],
           "experiment": [], "interventions": [], "exercise": []}
    if not findings:
        return out

    # Do not promote article-reported genes/pathways into gene.csv/pathway.csv.
    # The article-derived file is the evidence layer (`reported_findings.csv` +
    # reconciliation rows). The schema tables are now data-derived:
    # DEG -> gene, GSEA/GMT -> pathway/enrichment.

    os.makedirs(os.path.dirname(findings_csv_path) or ".", exist_ok=True)
    with open(findings_csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_FINDINGS_COLUMNS)
        w.writeheader()
        for f in findings:
            w.writerow({c: f.get(c) for c in _FINDINGS_COLUMNS})

    arow = {
        "analysis_id": f"{study_id}_analysis_text1",
        "study_id": study_id,
        "input_data": "Publication full text (no raw expression data computed)",
        "input_data_id": study_id,
        "analysis_name": "Literature-reported findings (text-mined)",
        "da_method": "text-mining",
        "n_deg": str(len(findings)),
        "reference_source": "GEO",
        "reference_source_id": study_id,
    }
    rrow = {
        "results_id": f"{study_id}_res_text1",
        "experiment_id": f"{study_id}_exp1",
        "analysis_type": "reported in publication (text-mined)",
        "original_assay_type": "literature",
        "datatype": "Spreadsheet",
        "dataset_size": str(len(findings)),
        "file_access": findings_csv_path,
        "file_type": "csv",
    }
    out["analysis"].append({c: arow.get(c) for c in csv_columns("analysis")})
    out["results"].append({c: rrow.get(c) for c in csv_columns("results")})
    return out


def build_reconciliation_rows(study_id: str, agreement_csv_path: str, summary: dict,
                              n_findings: int = 0) -> dict:
    """Promote computed-vs-reported reconciliation into the SEA-CDM result layer.

    The #6 agreement table (`agreement_csv_path`) already holds, per paper finding, the paper's
    claim (entity/direction/source) ALONGSIDE our computed value (log2FC/padj/significant) and a
    verdict — disagreements (contradicted / not_detected) included, not hidden. This returns the
    {'analysis':[row], 'results':[row]} contributions that point `results` at that table, so a
    study carries BOTH 'what the paper concluded' AND 'what our data shows' in one result row.

    `summary` is agreement_tools' verdict-count dict; `n_deg` on the analysis row is repurposed to
    the number of DISAGREEMENTS so a reader sees the inconsistency count at the relational level."""
    out = {"analysis": [], "results": []}
    if not summary:
        return out
    breakdown = ", ".join(f"{k}={v}" for k, v in sorted(summary.items()))
    n_disagree = int(summary.get("contradicted", 0)) + int(summary.get("not_detected", 0))
    arow = {
        "analysis_id": f"{study_id}_analysis_recon1",
        "study_id": study_id,
        "input_data": "Paper reported findings (#5) joined to our computed DEG (#1/#8)",
        "input_data_id": study_id,
        "analysis_name": "Computed-vs-reported reconciliation",
        "da_method": "reconciliation",
        "n_deg": str(n_disagree),  # repurposed: count of DISAGREEMENTS (contradicted + not_detected)
        "reference_source": "GEO",
        "reference_source_id": study_id,
    }
    rrow = {
        "results_id": f"{study_id}_res_recon1",
        "experiment_id": f"{study_id}_exp1",
        "analysis_type": "computed-vs-reported reconciliation (paper claim + our DEG + verdict)",
        "original_assay_type": "in-silico comparison",
        "datatype": "Spreadsheet",
        "dataset_size": f"{n_findings} findings: {breakdown}; {n_disagree} disagreement(s)",
        "file_access": agreement_csv_path,
        "file_type": "csv",
    }
    out["analysis"].append({c: arow.get(c) for c in csv_columns("analysis")})
    out["results"].append({c: rrow.get(c) for c in csv_columns("results")})
    return out


# --- The tool --------------------------------------------------------------------------

@tool
def extract_sea_cdm_tables(
    study_id: str,
    paper_text_path: str,
    organism: str = "",
    csv_out_dir: str = "",
    max_chars: int = 100000,
    metadata_csv: str = "",
) -> str:
    """Extract SEA-CDM tables (study/experiment/subject/sample/groups/interventions/assay/
    material/documentation) from a paper's full text using three grouped structured-output
    LLM calls, with per-field provenance. Writes output/{study_id}/seacdm_tables.json.

    Args:
        study_id: the GEO accession to use as the study PK (e.g. 'GSE279359').
        paper_text_path: path to the paper's full-text .txt (from fetch_paper_text).
        organism: optional 'Mouse'/'Human' hint.
        csv_out_dir: if set, also append the rows into the SEA-CDM CSV set in this directory.
        max_chars: truncate paper text to this many chars (cost guard).
        metadata_csv: optional path to the study's GEO metadata CSV. When given (or when
            data/{study_id}/{study_id}_metadata.csv exists), subject/sample/groups/assay are
            derived deterministically from it instead of from the LLM.
    """
    if not os.path.exists(paper_text_path):
        return f"ERROR: paper text not found at {paper_text_path}"
    with open(paper_text_path, "r", encoding="utf-8", errors="ignore") as f:
        paper_text = f.read()
    if len(paper_text) > max_chars:
        paper_text = paper_text[:max_chars]

    if _get_llm() is None:
        return "ERROR: configured LLM API key not set — cannot run extraction."

    prov: dict = {}
    try:
        tables = extract_tables_from_text(study_id, paper_text, organism, report=prov,
                                          metadata_csv=(metadata_csv or None))
    except Exception as e:
        return f"ERROR in extraction: {type(e).__name__}: {e}"

    json_path = write_study_tables_json(study_id, tables)

    # Persist the provenance audit (which quotes failed verbatim verification) next to the json.
    prov_path = os.path.join(os.path.dirname(json_path), "seacdm_provenance.json")
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump(prov, f, indent=2, ensure_ascii=False)

    csv_note = ""
    if csv_out_dir:
        paths = append_tables_to_csvs(tables, csv_out_dir)
        csv_note = f" Appended to {len(paths)} CSVs in {csv_out_dir}."

    counts = {t: len(rows) for t, rows in tables.items() if rows}
    prov_note = (
        f" Provenance: {prov.get('n_verified', 0)}/{prov.get('n_total', 0)} source quotes "
        f"verbatim-verified, {prov.get('n_unverified', 0)} flagged [UNVERIFIED]."
    )
    return (
        f"SEA-CDM tables extracted for {study_id}. Rows: {counts}. "
        f"Saved {json_path}.{csv_note}{prov_note}"
    )
