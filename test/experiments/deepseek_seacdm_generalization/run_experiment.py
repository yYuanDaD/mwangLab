"""DeepSeek staged SEA-CDM generalization: routine + multifactor papers, 3 repeats each."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import statistics
import sys
import time

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sea_cdm_schema import SEA_TABLES  # noqa: E402
from tools.seacdm_tools import extract_tables_from_text  # noqa: E402


def _load_helpers():
    path = ROOT / "test" / "experiments" / "model_seacdm_ab" / "run_experiment.py"
    spec = importlib.util.spec_from_file_location("seacdm_ab_helpers_generalization", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


H = _load_helpers()
PRICE = H.PRICES["deepseek"]
MAX_CHARS = 100_000
CHECK_WEIGHTS = {
    "completed": 10,
    "schema_conformant": 10,
    "required_tables_present": 10,
    "fk_integrity": 10,
    "no_group_errors": 5,
    "provenance_measured": 5,
    "provenance_verified_at_least_90pct": 15,
    "study_id_preserved": 5,
    "experiment_scope_consistent": 15,
    "critical_facts_recovered": 5,
    "no_unsupported_geo_accession": 5,
    "material_reference_recall_at_least_65pct": 5,
}
CASES = {
    "routine": {
        "study_id": "GSE270703",
        "organism": "Human",
        "paper_path": ROOT / "data" / "papers" / "c98328aa8b9dec8c68619e29850bcf21194a2059.txt",
        "metadata_path": ROOT / "data" / "GSE270703" / "GSE270703_metadata.csv",
        "reference_path": ROOT / "output" / "agentA_cohort_demo" / "studies" / "GSE270703" / "seacdm_tables.json",
        "reference_scope_experiment_ids": ("GSE270703_exp1",),
        "scope_required_term_groups": (("exercise",),),
        "scope_excluded_terms": (),
        "critical_terms": ("endurance", "resistance", "exercise"),
        "description": "single-experiment GEO study with two metadata groups",
    },
    "multifactor": {
        "study_id": "GSE250122",
        "organism": "Human",
        "paper_path": ROOT / "data" / "papers" / "01770d8a48c6c34f18936bd2c7badd34ca2716b8.txt",
        "metadata_path": ROOT / "data" / "GSE250122" / "GSE250122_metadata.csv",
        "reference_path": ROOT / "output" / "agentA_cohort_demo" / "studies" / "GSE250122" / "seacdm_tables.json",
        "reference_scope_experiment_ids": ("GSE250122_exp1",),
        "scope_required_term_groups": (
            ("acute", "60 min", "80%"),
            ("microarray", "affymetrix", "u219"),
        ),
        "scope_excluded_terms": (
            "8-week", "8 week", "3 weeks", "training program", "qPCR",
            "quantitative RT-PCR", "three supervised endurance", "3 sessions per week",
        ),
        "critical_terms": ("endurance", "trained", "baseline"),
        "description": "GEO-linked acute microarray cohort in a paper with an independent training/qPCR cohort",
    },
}


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _deepseek_environment():
    keys = ("BIOAGENT_LLM_PROVIDER", "BIOAGENT_SEACDM_LLM_PROVIDER",
            "BIOAGENT_LLM_MODEL", "BIOAGENT_STRUCTURED_MAX_TOKENS")
    old = {key: os.environ.get(key) for key in keys}
    os.environ["BIOAGENT_LLM_PROVIDER"] = "deepseek"
    os.environ["BIOAGENT_SEACDM_LLM_PROVIDER"] = "deepseek"
    os.environ.pop("BIOAGENT_LLM_MODEL", None)
    os.environ["BIOAGENT_STRUCTURED_MAX_TOKENS"] = "16384"
    try:
        yield
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(value).lower()))


def _overlap(left: str, right: str) -> float:
    a, b = _tokens(left), _tokens(right)
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


def _reference_recall(got: set[str], expected: set[str], threshold: float = 0.60) -> float:
    if not expected:
        return 1.0
    return sum(
        max((_overlap(item, candidate) for candidate in got), default=0.0) >= threshold
        for item in expected
    ) / len(expected)


def _table_text(tables: dict, names: tuple[str, ...]) -> str:
    return " ".join(
        str(value)
        for name in names
        for row in (tables.get(name) or [])
        for value in row.values()
        if value is not None
    ).lower()


def _semantic_sets(tables: dict, report: dict) -> dict[str, set[str]]:
    """Use the shared semantics, but include actual SEA-CDM intervention payload fields.

    The older A/B helper looked for the non-schema field ``intervention_name`` and therefore
    understated recall when material/dosage carried the protocol description.
    """
    semantics = H._semantic_sets(tables, report)
    semantics["intervention"] = {
        re.sub(r"\s+", " ", " ".join(str(row.get(key) or "") for key in (
            "material", "dosage", "intervention_type", "intervention_time", "time_unit",
            "comments",
        )).lower()).strip()
        for row in (tables.get("interventions") or [])
    }
    semantics["intervention"].discard("")
    return semantics


def _scope_audit(tables: dict, case: dict) -> dict:
    """Check the accession-level relation policy without assuming a gold experiment count.

    Paper-level findings/materials may mention validation cohorts, so only relationship-bearing
    design tables are inspected.  A result passes when the GEO-linked design is present and no
    paper-only cohort/intervention/assay has been attached to it.
    """
    text = _table_text(tables, ("experiment", "interventions", "assay"))
    required_hits = {
        " | ".join(group): [term for term in group if term.lower() in text]
        for group in case["scope_required_term_groups"]
    }
    excluded_hits = sorted({
        term for term in case["scope_excluded_terms"] if term.lower() in text
    })
    return {
        "policy": "target_geo_accession",
        "required_hits": required_hits,
        "excluded_hits": excluded_hits,
        "passed": all(required_hits.values()) and not excluded_hits,
    }


def _scoped_reference_tables(tables: dict, experiment_ids: tuple[str, ...]) -> dict:
    """Restrict reference design rows to the frozen GEO-accession scope for recall scoring."""
    scoped = dict(tables)
    allowed = set(experiment_ids)
    scoped["experiment"] = [
        row for row in (tables.get("experiment") or []) if row.get("experiment_id") in allowed
    ]
    for name in ("interventions", "assay"):
        scoped[name] = [
            row for row in (tables.get(name) or []) if row.get("experiment_id") in allowed
        ]
    return scoped


def _canon_hash(value) -> str:
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _score(checks: dict[str, bool]) -> int:
    return sum(weight for name, weight in CHECK_WEIGHTS.items() if checks.get(name))


def _run_one(case_name: str, repeat: int, out: Path) -> dict:
    case = CASES[case_name]
    study_id = case["study_id"]
    paper_text = case["paper_path"].read_text(encoding="utf-8", errors="ignore")[:MAX_CHARS]
    source_accessions = {item.upper() for item in re.findall(r"\bGSE\d+\b", paper_text, re.I)}
    run_dir = out / case_name / f"r{repeat}"
    run_dir.mkdir(parents=True, exist_ok=True)
    usage, report = [], {}
    tables = {name: [] for name in SEA_TABLES}
    error = ""
    started = _utc_now()
    t0 = time.perf_counter()
    try:
        with _deepseek_environment():
            tables = extract_tables_from_text(
                study_id, paper_text, case["organism"], verify=True, report=report,
                metadata_csv=str(case["metadata_path"]), lean=True, usage=usage,
                strategy="staged", max_stage_retries=1,
            )
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - t0, 3)

    schema_errors = H._schema_errors(tables)
    fk_errors = H._fk_errors(tables)
    row_counts = {name: len(rows) for name, rows in tables.items()}
    required = all(row_counts.get(name, 0) > 0 for name in (
        "study", "experiment", "subject", "sample", "groups", "interventions",
        "exercise", "assay", "documentation",
    ))
    n_total = int(report.get("n_total") or 0)
    n_verified = int(report.get("n_verified") or 0)
    provenance_rate = n_verified / n_total if n_total else 0.0
    text = H._all_text(tables, report)
    output_accessions = set(re.findall(r"\bGSE\d+\b", text, flags=re.I))
    unsupported = sorted(item.upper() for item in output_accessions
                         if item.upper() not in source_accessions | {study_id})
    critical = {term: term in text for term in case["critical_terms"]}
    semantics = _semantic_sets(tables, report)
    reference_tables = json.loads(case["reference_path"].read_text(encoding="utf-8"))
    scoped_reference = _scoped_reference_tables(
        reference_tables, case["reference_scope_experiment_ids"]
    )
    reference_semantics = _semantic_sets(scoped_reference, {})
    material_recall = _reference_recall(semantics["material"], reference_semantics["material"])
    intervention_recall = _reference_recall(
        semantics["intervention"], reference_semantics["intervention"], threshold=0.45
    )
    scope_audit = _scope_audit(tables, case)
    checks = {
        "completed": not error,
        "schema_conformant": not schema_errors,
        "required_tables_present": required,
        "fk_integrity": not fk_errors,
        "no_group_errors": not report.get("group_errors"),
        "provenance_measured": n_total > 0,
        "provenance_verified_at_least_90pct": provenance_rate >= 0.90,
        "study_id_preserved": bool(tables.get("study")) and
                              tables["study"][0].get("study_id") == study_id,
        "experiment_scope_consistent": scope_audit["passed"],
        "critical_facts_recovered": all(critical.values()),
        "no_unsupported_geo_accession": not unsupported,
        "material_reference_recall_at_least_65pct": material_recall >= 0.65,
    }
    blocking_names = (
        "completed", "schema_conformant", "required_tables_present", "fk_integrity",
        "no_group_errors", "study_id_preserved", "experiment_scope_consistent",
        "critical_facts_recovered", "no_unsupported_geo_accession",
        "material_reference_recall_at_least_65pct",
    )
    blocking = [name for name in blocking_names if not checks[name]]
    input_tokens = sum(int(row.get("input_tokens") or 0) for row in usage)
    output_tokens = sum(int(row.get("output_tokens") or 0) for row in usage)
    cost = (input_tokens * PRICE["input"] + output_tokens * PRICE["output"]) / 1_000_000
    structural = {name: tables.get(name, []) for name in ("subject", "sample", "groups", "assay")}

    tables_path = run_dir / "seacdm_tables.json"
    provenance_path = run_dir / "seacdm_provenance.json"
    decision_trace_path = run_dir / "decision_trace.json"
    tables_path.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    decision_trace_path.write_text(json.dumps({
        "case": case_name, "study_id": study_id, "attempts": report.get("decision_trace", []),
        "stage_errors": report.get("stage_errors", {}), "usage": usage,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    record = {
        "case": case_name, "repeat": repeat, "study_id": study_id,
        "started_at": started, "finished_at": _utc_now(), "elapsed_seconds": elapsed,
        "error": error, "checks": checks, "score": _score(checks), "coverage": 100.0,
        "blocking": blocking, "schema_errors": schema_errors, "fk_errors": fk_errors,
        "row_counts": row_counts, "critical_facts": critical,
        "provenance_total": n_total, "provenance_verified": n_verified,
        "provenance_rate": round(provenance_rate, 4), "unsupported_accessions": unsupported,
        "material_reference_recall": round(material_recall, 4),
        "intervention_reference_recall": round(intervention_recall, 4),
        "scope_audit": scope_audit,
        "usage": {"calls": len(usage), "input_tokens": input_tokens, "output_tokens": output_tokens},
        "estimated_cost_usd": round(cost, 8),
        "semantic_sets": {name: sorted(values) for name, values in semantics.items()},
        "structural_hash": _canon_hash(structural), "whole_output_hash": _canon_hash(tables),
        "tables_path": str(tables_path.resolve()),
        "provenance_path": str(provenance_path.resolve()),
        "decision_trace_path": str(decision_trace_path.resolve()),
    }
    trace_path = run_dir / "trace.json"
    record["trace_path"] = str(trace_path.resolve())
    trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return record


def _pairwise_jaccard(sets: list[set[str]]) -> float:
    pairs = [H._jaccard(a, b) for a, b in itertools.combinations(sets, 2)]
    return statistics.mean(pairs) if pairs else 1.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    if args.repeats != 3:
        raise SystemExit("LLM generalization validation requires exactly three repeats per case")
    for case in CASES.values():
        for key in ("paper_path", "metadata_path", "reference_path"):
            if not case[key].is_file():
                raise SystemExit(f"Frozen input/reference missing: {case[key]}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir).resolve() if args.output_dir else (
        ROOT / "output" / f"deepseek_seacdm_generalization_{stamp}"
    )
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="deepseek_seacdm_generalization",
        stages=["freeze_inputs", "extract", "stability", "report"],
    )
    tracker.start("DeepSeek staged SEA-CDM routine + multifactor generalization")
    tracker.set_stage("freeze_inputs", message="two cached papers, GEO metadata, Sonnet references")

    records = []
    tracker.set_stage("extract", message="two cases x three repeats; alternating case order")
    for repeat in range(1, args.repeats + 1):
        order = ("multifactor", "routine") if repeat % 2 else ("routine", "multifactor")
        for case_name in order:
            print(f"[{repeat}/3] {case_name}:{CASES[case_name]['study_id']} extracting...", flush=True)
            records.append(_run_one(case_name, repeat, out))

    tracker.set_stage("stability", message="within-case structure and semantic stability")
    per_case = {}
    for name in CASES:
        rows = [row for row in records if row["case"] == name]
        passed = [row for row in rows if not row["blocking"]]
        per_case[name] = {
            "study_id": CASES[name]["study_id"], "runs": len(rows), "passed": len(passed),
            "mean_score": round(statistics.mean(row["score"] for row in rows), 2),
            "mean_provenance_rate": round(statistics.mean(row["provenance_rate"] for row in rows), 4),
            "mean_material_reference_recall": round(statistics.mean(
                row["material_reference_recall"] for row in rows), 4),
            "mean_intervention_reference_recall": round(statistics.mean(
                row["intervention_reference_recall"] for row in rows), 4),
            "median_latency_seconds": round(statistics.median(row["elapsed_seconds"] for row in rows), 3),
            "cost_per_run_usd": round(statistics.mean(row["estimated_cost_usd"] for row in rows), 6),
            "structural_identical": len({row["structural_hash"] for row in rows}) == 1,
            "material_jaccard": round(_pairwise_jaccard([
                set(row["semantic_sets"]["material"]) for row in rows
            ]), 4),
            "finding_jaccard": round(_pairwise_jaccard([
                set(row["semantic_sets"]["finding"]) for row in rows
            ]), 4),
        }
    blocking = sorted({f"{row['case']}:r{row['repeat']}:{item}"
                       for row in records for item in row["blocking"]})
    acceptance = {
        "all_six_runs_pass": all(item["passed"] == 3 for item in per_case.values()),
        "zero_blocking_findings": not blocking,
        "provenance_at_least_90pct": all(
            item["mean_provenance_rate"] >= 0.90 for item in per_case.values()),
        "material_reference_recall_at_least_65pct": all(
            item["mean_material_reference_recall"] >= 0.65 for item in per_case.values()),
        "structure_stable": all(item["structural_identical"] for item in per_case.values()),
        "cost_per_run_at_most_30pct_of_sonnet": all(
            item["cost_per_run_usd"] <= 0.253341 * 0.30 for item in per_case.values()),
    }
    verdict = "deepseek_staged_generalized" if all(acceptance.values()) else "retain_sonnet_for_seacdm"

    summary_rows = [{
        "accession": row["study_id"], "case": row["case"], "repeat": row["repeat"],
        "status": "completed" if not row["blocking"] else "failed",
        "score": row["score"], "coverage": row["coverage"],
        "provenance_rate": row["provenance_rate"],
        "experiment_rows": row["row_counts"].get("experiment", 0),
        "group_rows": row["row_counts"].get("groups", 0),
        "material_rows": row["row_counts"].get("material", 0),
        "reported_findings": len(row["semantic_sets"]["finding"]),
        "material_reference_recall": row["material_reference_recall"],
        "experiment_scope_consistent": row["checks"]["experiment_scope_consistent"],
        "scope_excluded_hits": "; ".join(row["scope_audit"]["excluded_hits"]),
        "llm_calls": row["usage"]["calls"], "elapsed_seconds": row["elapsed_seconds"],
        "estimated_cost_usd": row["estimated_cost_usd"], "artifact": row["tables_path"],
        "error": row["error"],
    } for row in records]
    pd.DataFrame(summary_rows).to_csv(out / "summary.csv", index=False)
    report = {
        "schema_version": "1.1", "evaluation_unit": "two-case SEA-CDM generalization",
        "scope_policy": (
            "Target GEO accession. Paper-only cohorts may be omitted; if included in design tables, "
            "they must not be attached to the target GEO experiment."
        ),
        "verdict": verdict, "coverage": 100.0, "blocking_findings": blocking,
        "cases": {name: {**{k: str(v.resolve()) if isinstance(v, Path) else v
                             for k, v in case.items()}} for name, case in CASES.items()},
        "repeats": 3, "per_case": per_case, "acceptance": acceptance, "records": records,
        "unmeasured_checks": [
            "Manual domain-expert adjudication of every extracted field",
            "Paper without GEO metadata (legacy full structural extraction)",
            "Paper-level multi-experiment extraction; this benchmark is explicitly accession-scoped",
        ],
    }
    report_path = out / "deepseek_seacdm_generalization.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# DeepSeek staged SEA-CDM generalization", "", f"- Verdict: **{verdict}**",
        "- Coverage: **100%**", f"- Blocking findings: **{len(blocking)}**", "",
        "| Metric | Routine GSE270703 | Multifactor GSE250122 |", "|---|---:|---:|",
        f"| Runs passed | {per_case['routine']['passed']}/3 | {per_case['multifactor']['passed']}/3 |",
        f"| Mean score | {per_case['routine']['mean_score']} | {per_case['multifactor']['mean_score']} |",
        f"| Provenance | {per_case['routine']['mean_provenance_rate']:.1%} | {per_case['multifactor']['mean_provenance_rate']:.1%} |",
        f"| Material reference recall | {per_case['routine']['mean_material_reference_recall']:.1%} | {per_case['multifactor']['mean_material_reference_recall']:.1%} |",
        f"| GEO-scope runs passed | {sum(row['checks']['experiment_scope_consistent'] for row in records if row['case'] == 'routine')}/3 | {sum(row['checks']['experiment_scope_consistent'] for row in records if row['case'] == 'multifactor')}/3 |",
        f"| Structural identical | {per_case['routine']['structural_identical']} | {per_case['multifactor']['structural_identical']} |",
        f"| Median latency (s) | {per_case['routine']['median_latency_seconds']} | {per_case['multifactor']['median_latency_seconds']} |",
        f"| Cost/run (USD) | {per_case['routine']['cost_per_run_usd']} | {per_case['multifactor']['cost_per_run_usd']} |",
        "", "## Acceptance gates", "",
    ]
    lines.extend(f"- {name}: **{'pass' if value else 'fail'}**" for name, value in acceptance.items())
    lines.extend(["", "## Unmeasured checks", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "deepseek_seacdm_generalization.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "workflow.log").write_text("\n".join([
        "DeepSeek staged SEA-CDM generalization", "model=deepseek-v4-pro", "temperature=0",
        "strategy=staged", "max_tokens=16384", "retries=1", "cases=routine,multifactor",
        "repeats=3", "case_order=alternated", f"verdict={verdict}",
    ]) + "\n", encoding="utf-8")

    evidence = EvidenceRecorder(out.name, subject_id="SEA-CDM generalization")
    source_ids = {}
    for name, case in CASES.items():
        paper_source = evidence.add_source("paper", f"{case['study_id']} source paper",
                                           uri=str(case["paper_path"].resolve()))
        evidence.bundle.sources[-1].sha256 = file_sha256(str(case["paper_path"]))
        metadata_source = evidence.add_source("metadata", f"{case['study_id']} GEO metadata",
                                              uri=str(case["metadata_path"].resolve()))
        evidence.bundle.sources[-1].sha256 = file_sha256(str(case["metadata_path"]))
        source_ids[name] = [paper_source, metadata_source]
    for row in records:
        decision = evidence.add_decision(
            "staged_seacdm_generalization",
            {"case": row["case"], "study_id": row["study_id"], "repeat": row["repeat"]},
            reason="Three-repeat DeepSeek staged extraction on frozen inputs", method="llm",
            evidence_ids=source_ids[row["case"]],
            details={"score": row["score"], "checks": row["checks"]},
        )
        for key, kind in (("tables_path", "SEA-CDM tables"),
                          ("provenance_path", "provenance audit"),
                          ("decision_trace_path", "decision trace"),
                          ("trace_path", "run trace")):
            evidence.add_artifact(row[key], kind, produced_by=decision,
                                  evidence_ids=source_ids[row["case"]])
    for path, kind in ((out / "summary.csv", "evaluation summary"),
                       (report_path, "evaluation report"),
                       (out / "workflow.log", "workflow log")):
        evidence.add_artifact(str(path), kind)
    evidence.finish("completed")
    evidence.save(str(out / "evidence.json"))

    tracker.set_stage("report", message=verdict)
    tracker.set_usage(llm_calls=sum(row["usage"]["calls"] for row in records),
                      estimated_cost_usd=sum(row["estimated_cost_usd"] for row in records))
    for item in blocking:
        tracker.add_warning(item)
    tracker.finish("completed", verdict)
    print(json.dumps({"verdict": verdict, "per_case": per_case, "acceptance": acceptance,
                      "output_dir": str(out.resolve())}, indent=2, ensure_ascii=False))
    return 0 if verdict == "deepseek_staged_generalized" else 1


if __name__ == "__main__":
    raise SystemExit(main())
