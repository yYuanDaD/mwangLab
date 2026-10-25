"""Deterministic checks for bioinformatics decision-contract records.

A record captures one decision gate for one case (study). Two levels of checks:

- ``check_record``: structure and stage-specific required fields.
- ``check_case``: invariants across all records of a case, for example that no
  analysis ran after a gate was blocked, that a required blocking term reached
  the fitted formula, and that the method suits the matrix type.

These checks catch internally inconsistent records. They cannot tell whether a
decision matches the paper; that still needs evidence review or a gold set.
Standard library only, so the validator runs on any machine.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

CONTRACT_VERSION = "3"
# v3: a valid design carries final.suitability, the pre-analysis report's verdict
# (tools/suitability.py); records written under v2 are checked without it.
SUITABILITY_VERDICTS = {"analyzable", "partially_analyzable", "not_analyzable"}
STAGES = (
    "paper_reconstruction", "ownership", "alignment", "matrix", "design",
    "covariance", "method", "threshold", "execution", "enrichment", "study",
)
# Stages that run something and therefore may carry completed/failed.
RUN_STAGES = ("execution", "enrichment")
DECISIONS = {"valid", "unresolved", "manual_review", "refused"}
BLOCKED = {"unresolved", "manual_review", "refused"}
EXECUTIONS = {"not_started", "completed", "failed", "not_run"}
CONFIDENCE = {"high", "medium", "low"}
COVARIANCE_STATUS = {"required", "not_required", "unresolved"}
THRESHOLD_SOURCES = {"paper", "paper_on_deviation_route", "workflow_default", "audit"}
STUDY_ROUTES = {"paper_aligned", "declared_deviation", "exploratory", "stopped"}
PRE_EXECUTION_STAGES = ("alignment", "matrix", "design", "covariance", "method", "threshold")
REQUIRED_KEYS = (
    "case_id", "stage", "evidence", "candidates", "final", "confidence",
    "reasoning", "decision_status", "execution_status", "stop_reason",
)
# Fields a *valid* decision must carry in `final`, per stage. Blocked
# decisions only need a stop_reason.
STAGE_FIELDS = {
    "paper_reconstruction": ("accessions", "primary_estimand", "planned_contrasts", "paper_threshold"),
    "ownership": ("accession", "matrix_file", "metadata_file", "owned"),
    "alignment": ("method", "n_aligned", "n_metadata", "coverage"),
    "matrix": ("matrix_type", "recommended_method"),
    "design": ("analysis_type",),
    "covariance": ("status", "blocking_terms", "covariates"),
    "method": ("method", "matrix_type"),
    "threshold": ("paper_threshold", "threshold_source", "applied_threshold"),
    "execution": ("method",),
    "enrichment": ("method", "gene_sets", "organism", "feature_id_type"),
    "study": ("route",),
}
# Feature identifiers the repository gene-set tools accept directly
# (Ensembl gene IDs are converted to symbols through MyGene.info).
GENE_SET_READY_IDS = {"gene_symbol", "ensembl_gene"}
ENRICHMENT_ORGANISMS = {"mouse", "human"}
ORA_PATTERN = re.compile(r"\bora\b|over-?representation|enrichr|\bgo\b|kegg", re.I)
PAIRED_PATTERN = re.compile(r"(?<![a-z])(?<!un)(?<!non-)(paired|repeated|within[- ]subject|longitudinal)", re.I)
_METHOD_HEAD = re.compile(r"\s*(limma[- ]?voom|voom|deseq2|edger|limma|none|null|not_run)\b", re.I)
COUNT_METHODS = ("deseq2", "edger", "limma-voom", "voom")


def matrix_family(value: Any) -> str:
    """Map a free-text matrix_type to a coarse family used by the invariants."""
    text = str(value or "").lower()
    if not text or "ambiguous" in text or "unknown" in text:
        return "ambiguous"
    if "estimated" in text:
        return "estimated_counts"
    if "beta" in text and "m-value" not in text and "m_value" not in text:
        return "methylation_beta"
    if "log" in text or "rma" in text or "m-value" in text or "m_value" in text:
        return "log_scale"
    if any(k in text for k in ("fpkm", "tpm", "rpkm", "linear", "intensity")):
        return "linear_normalized"
    if "count" in text or "raw" in text:
        return "raw_counts"
    return "other"


def method_family(value: Any) -> str:
    """Family of the method named first: 'limma, deviation from DESeq2' is limma."""
    text = str(value or "")
    match = _METHOD_HEAD.match(text)
    if not match:
        return "none" if not text.strip() else "other"
    name = match.group(1).lower()
    if "voom" in name or name in {"deseq2", "edger"}:
        return "count"
    if name == "limma":
        return "log_linear"
    return "none"


def _evidence_errors(evidence: Any, source: str) -> list[str]:
    if not isinstance(evidence, list) or not evidence:
        return [f"{source}: evidence must be a non-empty list"]
    errors = []
    for index, item in enumerate(evidence):
        if not isinstance(item, dict) or not item.get("id") or not item.get("kind"):
            errors.append(f"{source}: evidence[{index}] must be an object with id and kind")
    return errors


def check_record(record: dict[str, Any], source: str = "record", *, legacy: bool = False) -> list[str]:
    """Structural and stage-field checks for one record."""
    if not isinstance(record, dict):
        return [f"{source}: record must be an object"]
    missing = [key for key in REQUIRED_KEYS if key not in record]
    if missing:
        return [f"{source}: missing {', '.join(missing)}"]
    errors: list[str] = []
    stage = record["stage"]
    status = record["decision_status"]
    final = record["final"]
    if not isinstance(record["case_id"], str) or not record["case_id"].strip():
        errors.append(f"{source}: case_id must be a non-empty string")
    if stage not in STAGES:
        errors.append(f"{source}: invalid stage {stage!r}")
    if status not in DECISIONS:
        errors.append(f"{source}: invalid decision_status {status!r}")
    if record["execution_status"] not in EXECUTIONS:
        errors.append(f"{source}: invalid execution_status {record['execution_status']!r}")
    if record["confidence"] not in CONFIDENCE:
        errors.append(f"{source}: confidence must be high, medium, or low")
    if not isinstance(record["candidates"], list):
        errors.append(f"{source}: candidates must be a list")
    if not isinstance(final, dict):
        errors.append(f"{source}: final must be an object")
        return errors
    if status in BLOCKED:
        if not record.get("stop_reason"):
            errors.append(f"{source}: unresolved/review/refused decision needs stop_reason")
        if record["execution_status"] == "completed":
            errors.append(f"{source}: blocked decision cannot have completed execution")
    if status == "valid" and record.get("stop_reason"):
        errors.append(f"{source}: valid decision cannot have stop_reason; use final.execution_error "
                      "for an execution failure")
    if legacy:
        if not isinstance(record["evidence"], list) or not record["evidence"]:
            errors.append(f"{source}: evidence must be a non-empty list")
        return errors

    errors.extend(_evidence_errors(record["evidence"], source))
    if stage not in STAGES:
        return errors
    if status == "valid":
        absent = [key for key in STAGE_FIELDS[stage] if key not in final]
        if absent:
            errors.append(f"{source}: valid {stage} decision missing final.{', final.'.join(absent)}")
    if stage == "paper_reconstruction" and "paper_threshold" in final \
            and not isinstance(final["paper_threshold"], dict):
        errors.append(f"{source}: paper_threshold must be an object")
    if stage == "design" and status == "valid":
        if not (final.get("formula") or final.get("design_column")):
            errors.append(f"{source}: valid design needs final.formula or final.design_column")
        if not (final.get("contrasts") or (final.get("control") and final.get("treatment"))):
            errors.append(f"{source}: valid design needs final.contrasts or final.control and final.treatment")
        suit = final.get("suitability")
        if int(record.get("contract_version") or CONTRACT_VERSION) >= 3 and not legacy:
            if not isinstance(suit, dict) or suit.get("verdict") not in SUITABILITY_VERDICTS:
                errors.append(f"{source}: valid design needs final.suitability with a verdict from "
                              f"case.suitability(...) (one of {sorted(SUITABILITY_VERDICTS)})")
            elif suit["verdict"] == "not_analyzable":
                errors.append(f"{source}: the suitability report says not_analyzable "
                              f"(failed: {suit.get('failed')}); the design cannot be valid")
    if stage == "alignment" and status == "valid":
        coverage = final.get("coverage")
        if not isinstance(coverage, (int, float)) or not 0 <= coverage <= 1:
            errors.append(f"{source}: alignment coverage must be a fraction between 0 and 1")
    if stage == "covariance" and "status" in final:
        cov_status = final.get("status")
        if cov_status not in COVARIANCE_STATUS:
            errors.append(f"{source}: covariance status must be one of {sorted(COVARIANCE_STATUS)}")
        if cov_status == "unresolved" and status == "valid":
            errors.append(f"{source}: unresolved covariance cannot be a valid decision")
        if cov_status == "required" and status == "valid" and not (
                final.get("blocking_terms") or final.get("covariates")):
            errors.append(f"{source}: required covariance needs blocking_terms or covariates")
    if stage == "threshold" and status == "valid":
        if final.get("threshold_source") not in THRESHOLD_SOURCES:
            errors.append(f"{source}: threshold_source must be one of {sorted(THRESHOLD_SOURCES)}")
        if not isinstance(final.get("paper_threshold"), dict):
            errors.append(f"{source}: paper_threshold must be an object")
        if not isinstance(final.get("applied_threshold"), dict):
            errors.append(f"{source}: applied_threshold must be an object")
    if stage in RUN_STAGES and record["execution_status"] == "completed" and not final.get("outputs"):
        errors.append(f"{source}: completed {stage} must list final.outputs")
    if stage in RUN_STAGES and record["execution_status"] == "failed" and not final.get("execution_error"):
        errors.append(f"{source}: failed {stage} must record final.execution_error")
    if stage in RUN_STAGES and status == "valid" and record["execution_status"] == "not_run" \
            and not final.get("reason_not_run"):
        errors.append(f"{source}: a planned {stage} that was not run must record final.reason_not_run")
    # The study record summarizes the case and may mirror the execution outcome.
    if stage not in RUN_STAGES and stage in STAGES and stage != "study" \
            and record["execution_status"] in {"completed", "failed"}:
        errors.append(f"{source}: decision gate {stage} keeps execution_status not_started; "
                      "only execution and enrichment records run something")
    # A planned enrichment that was not run only needs reason_not_run (checked above).
    if stage == "enrichment" and status == "valid" and record["execution_status"] != "not_run":
        errors.extend(_enrichment_errors(final, source))
    if stage == "study" and status == "valid" and final.get("route") not in STUDY_ROUTES:
        errors.append(f"{source}: study route must be one of {sorted(STUDY_ROUTES)}")
    return errors


def _enrichment_errors(final: dict, source: str) -> list[str]:
    errors = []
    id_type = str(final.get("feature_id_type", "")).lower()
    if id_type and id_type not in GENE_SET_READY_IDS and not final.get("id_mapping"):
        errors.append(f"{source}: feature_id_type {id_type!r} needs final.id_mapping (for example a "
                      "platform annotation or ID-to-symbol table) before gene-set analysis")
    organism = str(final.get("organism", "")).lower()
    if organism and organism not in ENRICHMENT_ORGANISMS and not final.get("ortholog_mapping"):
        errors.append(f"{source}: repository gene sets cover Mouse and Human only; {organism!r} needs "
                      "final.ortholog_mapping")
    if ORA_PATTERN.search(str(final.get("method", ""))):
        if not isinstance(final.get("input_threshold"), dict):
            errors.append(f"{source}: over-representation analysis needs final.input_threshold (the gene-list rule)")
        if final.get("input_threshold_source") not in {"applied", "audit"}:
            errors.append(f"{source}: final.input_threshold_source must be 'applied' (the case's applied "
                          "threshold) or 'audit'")
    return errors


def _formula_text(records: Iterable[dict]) -> str:
    parts = []
    for record in records:
        final = record.get("final") or {}
        for key in ("formula", "design_formula", "fitted_formula"):
            if final.get(key):
                parts.append(str(final[key]))
    return " ".join(parts).lower()


def _term_name(term: Any) -> str:
    text = str(term).strip()
    match = re.match(r"C\((.+?)\)", text)
    return (match.group(1) if match else text).strip().lower()


_ADJUSTED_METRICS = {"padj", "fdr", "adj_p", "adjp", "adjusted_p", "adj.p.val", "q", "qvalue", "q_value"}
_RAW_METRICS = {"pvalue", "p", "p_value", "raw_p", "p.value"}


def _metric(value: Any) -> Any:
    """'FDR', 'padj', and 'q-value' name the same kind of cutoff; 'p' and 'pvalue' another."""
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if text in _ADJUSTED_METRICS or text.startswith(("fdr", "padj", "adjusted")):
        return "adjusted_p"
    if text in _RAW_METRICS:
        return "pvalue"
    return value


def _adjustment(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    if not text or "not_reported" in text or "not reported" in text:
        return None
    if "permut" in text:
        return "permutation"
    if "bonferroni" in text:
        return "bonferroni"
    if "storey" in text or "qvalue" in text.replace(" ", ""):
        return "storey"
    if "bh" in text or "benjamini" in text or "fdr" in text:
        return "bh"
    return text


def _same_threshold(applied: dict, paper: dict) -> bool:
    keys = ("metric", "cutoff", "effect_metric", "effect_cutoff")
    norm = lambda key, value: _metric(value) if key == "metric" else value  # noqa: E731
    return all(norm(key, applied.get(key)) == norm(key, paper.get(key))
               for key in keys if key in paper or key in applied)


def check_case(records: list[dict[str, Any]], case_id: str = "case") -> list[str]:
    """Invariants across every record of one case."""
    errors: list[str] = []
    by_stage: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        if isinstance(record, dict):
            by_stage[record.get("stage")].append(record)
    # A blocked enrichment gate does not undo a completed differential analysis.
    blocked = [r for r in records if r.get("decision_status") in BLOCKED and r.get("stage") != "enrichment"]
    completed = [r for r in records if r.get("execution_status") == "completed"]

    if blocked and completed:
        stages = sorted({r.get("stage") for r in blocked})
        errors.append(f"{case_id}: analysis marked completed although gate(s) {stages} are blocked")

    if completed:
        missing = [s for s in PRE_EXECUTION_STAGES
                   if not any(r.get("decision_status") == "valid" for r in by_stage.get(s, []))]
        if missing:
            errors.append(f"{case_id}: completed analysis lacks valid decisions for {missing}")

    valid = lambda stage: [r for r in by_stage.get(stage, []) if r.get("decision_status") == "valid"]  # noqa: E731

    # Matrix and method must agree.
    matrix_types = {matrix_family((r.get("final") or {}).get("matrix_type")) for r in valid("matrix")}
    # A transform declared in the method decision applies to the executed analysis too.
    case_transform = next((str((r.get("final") or {}).get("transform")) for r in valid("method")
                           if (r.get("final") or {}).get("transform")), "")
    # So does documented rounding of estimated counts.
    case_rounding = any((r.get("final") or {}).get("rounding_documented") for r in valid("method"))
    for record in valid("method") + [r for r in by_stage.get("execution", [])
                                     if r.get("execution_status") == "completed"]:
        final = record.get("final") or {}
        family = method_family(final.get("method"))
        types = matrix_types | ({matrix_family(final["matrix_type"])} if final.get("matrix_type") else set())
        transform = str(final.get("transform") or case_transform).lower()
        if family == "count" and types & {"linear_normalized", "log_scale", "methylation_beta"}:
            errors.append(f"{case_id}: count-based method {final.get('method')!r} on {sorted(types)} matrix")
        if family == "count" and "estimated_counts" in types and not (final.get("rounding_documented")
                                                                        or case_rounding):
            errors.append(f"{case_id}: count method on estimated counts needs final.rounding_documented")
        if family == "log_linear" and types & {"raw_counts", "linear_normalized", "methylation_beta",
                                               "estimated_counts"} and not transform:
            errors.append(f"{case_id}: limma on {sorted(types)} matrix needs final.transform "
                          "(for example log2(x+1), log2(CPM+1), or beta-to-M)")
        if "ambiguous" in types and family != "none":
            errors.append(f"{case_id}: method chosen although matrix type is ambiguous")

    # Repeated measures must be handled as covariance.
    design_text = " ".join(str((r.get("final") or {}).get("analysis_type", "")) for r in valid("design"))
    covariance = valid("covariance")
    if PAIRED_PATTERN.search(design_text):
        if not any((r.get("final") or {}).get("status") == "required" for r in covariance):
            errors.append(f"{case_id}: design is paired/repeated but covariance is not 'required'")

    # Required blocking terms must reach the fitted model, unless the design
    # removes the subject effect by differencing (paired_change).
    formulas = _formula_text(valid("design") + valid("method") + by_stage.get("execution", []))
    if formulas and "paired_change" not in design_text.lower():
        for record in covariance:
            final = record.get("final") or {}
            if final.get("status") != "required":
                continue
            terms = list(final.get("blocking_terms") or [])
            for covariate in final.get("covariates") or []:
                if isinstance(covariate, str):
                    terms.append(covariate)
                elif isinstance(covariate, dict) and str(covariate.get("disposition", "")).lower().startswith("included"):
                    terms.append(covariate.get("name", ""))
            for term in terms:
                name = _term_name(term if not isinstance(term, dict) else term.get("name", ""))
                if name and name not in formulas:
                    errors.append(f"{case_id}: required model term {name!r} is not in the fitted formula")

    # Enrichment runs on a completed differential analysis, and an ORA gene list
    # uses the case's applied threshold unless it is labelled as an audit rule.
    de_completed = any(r.get("execution_status") == "completed" for r in by_stage.get("execution", []))
    applied_rules = [(r.get("final") or {}).get("applied_threshold") or {} for r in valid("threshold")]
    for record in by_stage.get("enrichment", []):
        final = record.get("final") or {}
        if record.get("execution_status") == "completed" and not de_completed:
            errors.append(f"{case_id}: enrichment completed without a completed differential analysis")
        if record.get("decision_status") == "valid" and final.get("input_threshold_source") == "applied" \
                and applied_rules and isinstance(final.get("input_threshold"), dict) \
                and not any(_same_threshold(final["input_threshold"], rule) for rule in applied_rules):
            errors.append(f"{case_id}: ORA input_threshold differs from the applied threshold; "
                          "label it input_threshold_source 'audit' or use the applied rule")

    # The paper's threshold cannot be silently changed.
    for record in valid("threshold"):
        final = record.get("final") or {}
        paper = final.get("paper_threshold") or {}
        applied = final.get("applied_threshold") or {}
        source = final.get("threshold_source")
        if source in {"paper", "paper_on_deviation_route"} and paper and applied \
                and not _same_threshold(applied, paper):
            errors.append(f"{case_id}: applied threshold differs from paper_threshold "
                          f"but threshold_source is {source!r}")
        paper_adj, applied_adj = _adjustment(paper.get("adjustment")), _adjustment(applied.get("adjustment"))
        if paper_adj and applied_adj and paper_adj != applied_adj:
            if source != "paper_on_deviation_route" or not final.get("deviation_note"):
                errors.append(f"{case_id}: adjustment changes from {paper_adj!r} to {applied_adj!r}; "
                              "use threshold_source 'paper_on_deviation_route' with final.deviation_note")
    return errors


def load_records(paths: Iterable[Path]) -> list[tuple[str, dict]]:
    out = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("records"), list):
            payload = payload["records"]
        items = payload if isinstance(payload, list) else [payload]
        for index, record in enumerate(items):
            out.append((f"{path}[{index}]", record))
    return out


def validate(paths: Iterable[Path], *, legacy: bool = False) -> tuple[int, list[str]]:
    """Validate record files; returns (record count, errors)."""
    loaded = load_records(paths)
    errors: list[str] = []
    cases: dict[str, list[dict]] = defaultdict(list)
    for source, record in loaded:
        errors.extend(check_record(record, source, legacy=legacy))
        if isinstance(record, dict) and isinstance(record.get("case_id"), str):
            cases[record["case_id"]].append(record)
    for case_id, records in cases.items():
        errors.extend(check_case(records, case_id))
    return len(loaded), errors
