"""Recompute scope and intervention-recall checks from saved extraction artifacts.

This performs no model calls and never mutates the original run or its evidence hashes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import run_experiment as runner


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    args = parser.parse_args()
    run_dir = Path(args.run_dir).resolve()
    records = []
    for case_name, case in runner.CASES.items():
        reference = json.loads(case["reference_path"].read_text(encoding="utf-8"))
        scoped_reference = runner._scoped_reference_tables(
            reference, case["reference_scope_experiment_ids"]
        )
        expected = runner._semantic_sets(scoped_reference, {})["intervention"]
        for repeat in range(1, 4):
            artifact_dir = run_dir / case_name / f"r{repeat}"
            tables = json.loads(
                (artifact_dir / "seacdm_tables.json").read_text(encoding="utf-8")
            )
            report = json.loads(
                (artifact_dir / "seacdm_provenance.json").read_text(encoding="utf-8")
            )
            got = runner._semantic_sets(tables, report)["intervention"]
            scope = runner._scope_audit(tables, case)
            records.append({
                "case": case_name,
                "repeat": repeat,
                "study_id": case["study_id"],
                "experiment_scope_consistent": scope["passed"],
                "required_hits": scope["required_hits"],
                "excluded_hits": scope["excluded_hits"],
                "intervention_reference_recall": round(
                    runner._reference_recall(got, expected, threshold=0.45), 4
                ),
                "source_tables": str((artifact_dir / "seacdm_tables.json").resolve()),
                "source_provenance": str(
                    (artifact_dir / "seacdm_provenance.json").resolve()
                ),
            })

    passed = all(row["experiment_scope_consistent"] for row in records)
    result = {
        "schema_version": "1.0",
        "evaluation_unit": "zero-call rescore of saved SEA-CDM artifacts",
        "scope_policy": "target_geo_accession",
        "verdict": "pass" if passed else "fail",
        "blocking_findings": [
            f"{row['case']}:r{row['repeat']}:experiment_scope_consistent"
            for row in records if not row["experiment_scope_consistent"]
        ],
        "records": records,
    }
    json_path = run_dir / "scope_rescore.json"
    md_path = run_dir / "scope_rescore.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# SEA-CDM GEO-scope rescore",
        "",
        f"- Verdict: **{result['verdict']}**",
        "- Model calls: **0** (saved artifacts only)",
        "- Rule: the target GEO design must be present; paper-only cohorts must not be linked to it.",
        "",
        "| Case | Repeat | Scope consistent | Intervention recall | Excluded hits |",
        "|---|---:|---:|---:|---|",
    ]
    for row in records:
        lines.append(
            f"| {row['case']} | {row['repeat']} | {row['experiment_scope_consistent']} | "
            f"{row['intervention_reference_recall']:.1%} | "
            f"{'; '.join(row['excluded_hits']) or 'none'} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "verdict": result["verdict"],
        "records": records,
        "report": str(md_path),
    }, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
