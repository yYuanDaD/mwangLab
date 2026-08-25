"""Qualify Claude Opus 5 as a bounded, stage-only fallback for DeepSeek SEA-CDM.

Paid calls are intentionally capped at two: GSE319603 (known failed design stage) and
GSE318937 (forced shadow review). GSE282166 is a zero-cost negative routing control.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
EXERCISE_AB = ROOT / "test" / "experiments" / "seacdm_exercise10_ab"
sys.path.insert(0, str(EXERCISE_AB))

from common import design_scope_audit, exercise_semantics  # noqa: E402
from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.metadata_structural import build_structural_tables, summarize_geo_scope  # noqa: E402
from tools.model_factory import create_structured_chat_model, resolve_model_config  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools import seacdm_tools as S  # noqa: E402


MODEL = "claude-opus-5"
INPUT_PRICE = 5.0
OUTPUT_PRICE = 25.0
PAID_CASES = ("GSE319603", "GSE318937")
NEGATIVE_CASE = "GSE282166"
DESIGN_TERMS = (
    "exercise protocol", "wheel-running", "running wheel", "experimental design",
    "viral", "injection", "treatment", "sedentary", "mice were", "days of exercise",
    "mict", "sprint", "oleuropein", "placebo", "cross-over", "crossover",
)

# Independent scoring rubric. These terms are never included in the model prompt.
CONCEPT_GOLD = {
    "GSE319603": {
        "high-fat diet": ("high-fat diet", "hfd"),
        "MICT exercise": ("mict", "moderate-intensity continuous"),
    },
    "GSE318937": {
        "MICE": ("moderate-intensity continuous", "mice"),
        "SIE": ("sprint interval", "sie"),
        "oleuropein": ("oleuropein", "olive leaf", "ole"),
        "placebo": ("placebo", "pla"),
    },
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _design_payload(tables: dict) -> dict:
    return {
        "experiments": tables.get("experiment") or [],
        "interventions": tables.get("interventions") or [],
        "exercise": tables.get("exercise") or [],
    }


def _design_context(case: dict) -> str:
    text = Path(case["text_path"]).read_text(encoding="utf-8", errors="ignore")[:100000]
    body = S._paper_regions(text)["body"]
    chunks = S._ranked_chunks(body, DESIGN_TERMS, max_chunks=4)
    scope = summarize_geo_scope(case["metadata_path"])
    return f"[TARGET GEO SCOPE]\n{scope}\n[END TARGET GEO SCOPE]\n\n" + "\n\n[EXCERPT]\n".join(chunks)


def _fallback_prompt(case: dict, context: str, prior: dict, findings: list[str]) -> str:
    findings_text = "\n".join(f"- {item}" for item in findings) or "- shadow review requested"
    return f"""You are the bounded fallback for one failed SEA-CDM design-extraction stage.
Target GEO study: {case['study_id']} ({case.get('organism', '')}).

DETERMINISTIC VALIDATOR FINDINGS:
{findings_text}

Repair only the target GEO accession's experiment and interventions. Return exactly one experiment.
Cover every experimental axis represented by TARGET GEO SCOPE, but exclude paper experiments not
represented by those GEO samples. Several arms, timepoints, periods, or crossover sequences remain
one experiment. Return a distinct intervention for each treatment/exercise/diet/placebo axis that
was actually applied to target samples. Preserve supported prior facts, remove unsupported facts,
and never invent a row merely to satisfy the validator.

PRIOR DEEPSEEK STAGE OUTPUT:
{json.dumps(prior, ensure_ascii=False)}

{S._PROVENANCE_RULES}

------- TARGET SCOPE AND PAPER EXCERPTS START -------
{context}
------- TARGET SCOPE AND PAPER EXCERPTS END -------
"""


def _merge_repair(case: dict, base: dict, extraction) -> dict:
    design = S.DesignExtraction(experiments=extraction.experiments, subjects=[], groups=[])
    methods = S.MethodsExtraction(samples=[], interventions=extraction.interventions, assays=[])
    partial = S.flatten_extraction(
        case["study_id"], S.StudyLevelExtraction(), design, methods,
        metadata_csv=case["metadata_path"],
    )
    merged = {name: list(rows) for name, rows in base.items()}
    for name in ("experiment", "interventions", "exercise", "subject", "sample", "groups", "assay"):
        merged[name] = partial[name]
    return merged


def _concept_score(study_id: str, tables: dict) -> dict:
    text = " ".join(
        str(value or "").lower()
        for name in ("experiment", "interventions", "exercise")
        for row in (tables.get(name) or [])
        for key, value in row.items()
        if not key.endswith("_source") and key != "comments"
    )
    found = {
        label: any(term in text for term in alternatives)
        for label, alternatives in CONCEPT_GOLD[study_id].items()
    }
    return {"found": found, "passed": all(found.values())}


def _score(case: dict, tables: dict, paper_text: str) -> dict:
    study_id = case["study_id"]
    schema_errors = S.H._schema_errors(tables) if hasattr(S, "H") else []
    # Reuse the frozen experiment scorer for the complete schema and FK checks.
    import common as C
    schema_errors = C.H._schema_errors(tables)
    fk_errors = C.H._fk_errors(tables)
    provenance = S.verify_provenance(tables, paper_text)
    scope = design_scope_audit(tables, study_id)
    exercise = exercise_semantics(tables, case["metadata_path"])
    concepts = _concept_score(study_id, tables)
    checks = {
        "schema_conformant": not schema_errors,
        "fk_integrity": not fk_errors,
        "metadata_sample_count_matches": len(tables.get("sample") or []) == int(case["metadata_samples"]),
        "target_geo_scope_only": scope["passed"],
        "exercise_semantics_valid": exercise["passed"],
        "concept_gold_covered": concepts["passed"],
        "provenance_at_least_90pct": (
            int(provenance.get("n_verified") or 0) / max(1, int(provenance.get("n_total") or 0))
        ) >= 0.90,
    }
    return {
        "checks": checks,
        "passed": all(checks.values()),
        "schema_errors": schema_errors,
        "fk_errors": fk_errors,
        "scope": scope,
        "exercise": exercise,
        "concepts": concepts,
        "provenance": provenance,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-experiment", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--paid-cases", nargs="+", choices=PAID_CASES,
                        default=list(PAID_CASES))
    args = parser.parse_args()
    source = Path(args.source_experiment).resolve()
    out = Path(args.output_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    workflow = out / "workflow.log"
    workflow.write_text("Opus 5 stage-only fallback qualification\n", encoding="utf-8")

    manifest = _json(source / "frozen_manifest.json")
    cases = {case["study_id"]: case for case in manifest["cases"]}
    tracker = RunStatusTracker(
        str(out / "run_status.json"), run_id=out.name,
        profile="seacdm_opus5_fallback_qualification", stages=["route", "fallback", "report"],
    )
    tracker.start("Opus 5 stage-only fallback qualification")
    evidence = EvidenceRecorder(out.name, subject_id="seacdm:fallback:opus5")
    records = []
    total_calls = 0
    total_cost = 0.0
    config = resolve_model_config(provider="anthropic", model=MODEL, effort="medium")
    llm = create_structured_chat_model(config, max_tokens=4096)

    tracker.set_stage("route", message=f"{len(args.paid_cases)} paid cases + 1 negative control")
    for study_id in (*args.paid_cases, NEGATIVE_CASE):
        case = cases[study_id]
        base_path = source / "deepseek" / "studies" / study_id / "seacdm_tables.json"
        base = _json(base_path)
        paper_path = Path(case["text_path"])
        source_ids = [
            evidence.add_source("paper", f"{study_id} full text", uri=str(paper_path),
                                attributes={"sha256": file_sha256(str(paper_path))}),
            evidence.add_source("metadata", f"{study_id} GEO metadata", uri=case["metadata_path"],
                                attributes={"sha256": file_sha256(case["metadata_path"])}),
            evidence.add_source("artifact", f"{study_id} DeepSeek baseline", uri=str(base_path),
                                attributes={"sha256": file_sha256(str(base_path))}),
        ]
        if study_id == NEGATIVE_CASE:
            route = exercise_semantics(base, case["metadata_path"])
            record = {
                "study_id": study_id, "mode": "negative_route_control", "called_opus": False,
                "route": route, "status": "success" if route["passed"] else "failed",
                "blocking": [] if route["passed"] else ["unexpected_fallback_requirement"],
                "llm_calls": 0, "input_tokens": 0, "output_tokens": 0,
                "cost_usd": 0.0, "elapsed_seconds": 0.0,
            }
            decision = evidence.add_decision(
                "fallback_route", {"study_id": study_id, "called_opus": False},
                reason="Target GEO scope has no exercise arm and baseline passes hard scope rules.",
                method="rule", evidence_ids=source_ids, details=route,
            )
            records.append(record)
            continue

        findings = (["Target GEO scope contains an exercise arm, but the prior output has no valid exercise intervention."]
                    if study_id == "GSE319603" else ["Forced shadow review of a complex multi-factor design."])
        context = _design_context(case)
        usage = []
        prompt = _fallback_prompt(case, context, _design_payload(base), findings)
        started = time.perf_counter()
        error = ""
        try:
            extraction = S._structured_runnable(
                llm, S.ExperimentInterventionExtraction, usage
            ).invoke(prompt)
            repaired = _merge_repair(case, base, extraction)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            repaired = base
        elapsed = round(time.perf_counter() - started, 3)
        input_tokens = sum(int(item.get("input_tokens") or 0) for item in usage)
        output_tokens = sum(int(item.get("output_tokens") or 0) for item in usage)
        cost = (input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE) / 1_000_000
        total_calls += len(usage)
        total_cost += cost
        paper_text = paper_path.read_text(encoding="utf-8", errors="ignore")[:100000]
        score = _score(case, repaired, paper_text)
        if error:
            score["passed"] = False
            score["checks"]["completed"] = False
        else:
            score["checks"]["completed"] = True
        case_dir = out / "studies" / study_id
        case_dir.mkdir(parents=True, exist_ok=True)
        tables_path = case_dir / "seacdm_tables.json"
        trace_path = case_dir / "trace.json"
        tables_path.write_text(json.dumps(repaired, indent=2, ensure_ascii=False), encoding="utf-8")
        blocking = [name for name, passed in score["checks"].items() if not passed]
        record = {
            "study_id": study_id, "mode": "repair" if study_id == "GSE319603" else "shadow",
            "called_opus": True, "model": MODEL, "started_at": _now(), "error": error,
            "status": "success" if score["passed"] else "failed", "blocking": blocking,
            "score": score, "llm_calls": len(usage), "input_tokens": input_tokens,
            "output_tokens": output_tokens, "cost_usd": round(cost, 8),
            "elapsed_seconds": elapsed, "usage": usage, "tables_path": str(tables_path),
        }
        trace_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        record["trace_path"] = str(trace_path)
        records.append(record)
        decision = evidence.add_decision(
            "opus5_stage_fallback", {"study_id": study_id, "passed": score["passed"]},
            reason="Bounded repair of the design/intervention stage after deterministic routing.",
            method="hybrid", evidence_ids=source_ids, details=score["checks"],
        )
        evidence.add_artifact(str(tables_path), "fallback SEA-CDM tables", produced_by=decision,
                              evidence_ids=source_ids)
        evidence.add_artifact(str(trace_path), "fallback trace", produced_by=decision,
                              evidence_ids=source_ids)
        with workflow.open("a", encoding="utf-8") as handle:
            handle.write(f"{study_id}: status={record['status']} calls={len(usage)} "
                         f"cost=${cost:.6f} elapsed={elapsed}s blocking={blocking}\n")

    tracker.set_stage("fallback", message=f"{total_calls}/2 paid calls used")
    summary_rows = [{
        "study_id": row["study_id"], "status": row["status"], "mode": row["mode"],
        "called_opus": row["called_opus"], "blocking": ";".join(row["blocking"]),
        "llm_calls": row["llm_calls"], "cost_usd": row["cost_usd"],
        "elapsed_seconds": row["elapsed_seconds"],
    } for row in records]
    pd.DataFrame(summary_rows).to_csv(out / "summary.csv", index=False)
    report = {
        "schema_version": "1.0", "model": MODEL, "source_experiment": str(source),
        "paid_call_cap": len(args.paid_cases), "actual_paid_calls": total_calls,
        "total_cost_usd": round(total_cost, 6),
        "passed": sum(row["status"] == "success" for row in records),
        "cases": len(records), "records": records,
    }
    report_path = out / "qualification_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    evidence.add_artifact(str(out / "summary.csv"), "qualification summary")
    evidence.add_artifact(str(report_path), "qualification report")
    evidence.add_artifact(str(workflow), "workflow log")
    evidence.finish("completed" if report["passed"] == report["cases"] else "partial")
    evidence.save(str(out / "evidence.json"))
    tracker.set_stage("report", message=f"{report['passed']}/{report['cases']} passed")
    tracker.set_usage(llm_calls=total_calls, estimated_cost_usd=round(total_cost, 6))
    for row in records:
        for blocker in row["blocking"]:
            tracker.add_warning(f"{row['study_id']}:{blocker}")
    tracker.finish("completed" if report["passed"] == report["cases"] else "partial",
                   f"{report['passed']}/{report['cases']} passed")
    print(json.dumps({
        "output_dir": str(out), "passed": report["passed"], "cases": report["cases"],
        "paid_calls": total_calls, "cost_usd": report["total_cost_usd"],
    }, indent=2))
    return 0 if report["passed"] == report["cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
