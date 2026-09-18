"""Offline, read-only export of contrast-selection review candidates, not gold SFT.

Uses only the Python standard library. Relative CLI paths are repository-relative,
including when invoked from another working directory. No agent modules, APIs or
model inference are invoked. Existing dataset destinations are never overwritten.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {"accession", "status", "design_col", "control", "treatment"}
HINTS = ("characteristics", "title", "source", "treatment", "group", "condition",
         "phenotype", "agent", "stimulus", "tissue", "diet", "genotype",
         "intervention", "exposure")


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def file_ref(path: Path) -> dict:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def clean(value: Any) -> str | None:
    text = str(value).strip() if value is not None else ""
    return None if text.lower() in {"", "nan", "none", "null"} else text


def workflow_context(path: Path) -> tuple[dict, dict | None]:
    context = {"organism": None, "control_keywords": None, "treatment_keywords": None}
    if not path.is_file():
        return context, None
    # Read headers only as context; never turn post-decision log text into input.
    with path.open(encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                break
            for key in context:
                prefix = f"# {key}="
                if not line.startswith(prefix):
                    continue
                value = line[len(prefix):].strip()
                if key == "organism":
                    context[key] = clean(value)
                else:
                    try:
                        parsed = ast.literal_eval(value)
                    except (SyntaxError, ValueError):
                        continue
                    if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
                        context[key] = sorted(set(parsed))
    return context, file_ref(path)


def metadata_context(path: Path) -> tuple[dict, dict | None]:
    if not path.is_file():
        return {}, None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = [c for c in (reader.fieldnames or [])[1:]
                   if any(h in c.lower() for h in HINTS)]
        counts = {col: Counter() for col in columns}
        overflow = set()
        for row in reader:
            for col in columns:
                if col in overflow:
                    continue
                value = row.get(col)
                if value is not None and value.strip():
                    counts[col][value] += 1
                    if len(counts[col]) > 12:
                        overflow.add(col)
                        counts[col].clear()
    # Deterministic order; reconstruction may differ from historical prompts.
    summary = {col: {"unique_values": sorted(values), "counts": dict(sorted(values.items()))}
               for col, values in sorted(counts.items()) if 2 <= len(values) <= 12}
    return summary, file_ref(path)


def label_origin(row: dict) -> str:
    validated = (clean(row.get("llm_validated")) or "").lower()
    if (clean(row.get("llm_overrode")) or "").lower() == "true":
        return "llm_override"
    if validated.startswith("skipped"):
        return "python_confident"
    if validated in {"true", "1"}:
        return "llm_confirmed"
    if clean(row.get("llm_reasoning")):
        return "llm_weak"
    return "pipeline_rule_or_unresolved"


def label_issues(label: dict, metadata: dict) -> list[str]:
    col, ctrl, treat = (label[k] for k in ("design_column", "control_value", "treatment_value"))
    if not all((col, ctrl, treat)):
        # An absent label may mean execution failed, not that refusal is correct.
        return ["missing_contrast_not_a_verified_refusal"]
    issues = []
    if ctrl == treat:
        issues.append("identical_arms")
    values = metadata.get(col, {}).get("counts", {})
    if not values:
        issues.append("design_column_not_in_current_metadata_summary")
    elif ctrl not in values or treat not in values:
        issues.append("arm_not_in_current_metadata")
    elif min(values[ctrl], values[treat]) < 3:
        issues.append("fewer_than_3_samples_in_an_arm_review_required")
    return issues


def export_dataset(output_root: Path, data_root: Path, dataset_dir: Path) -> dict:
    output_root, data_root, dataset_dir = (p.resolve() for p in (output_root, data_root, dataset_dir))
    if not output_root.is_dir():
        raise ValueError(f"Output source does not exist: {output_root}")
    if dataset_dir.exists():
        raise ValueError(f"Dataset destination already exists; choose a new directory: {dataset_dir}")
    if dataset_dir == data_root or data_root in dataset_dir.parents:
        raise ValueError("Dataset destination must be outside the source data directory")
    inventory, errors, groups, metadata_cache = [], [], {}, {}
    scanned_rows = candidate_rows = 0
    for summary_path in sorted(output_root.rglob("summary.csv")):
        entry = {"path": str(summary_path), "status": "skipped_incompatible_schema", "rows": 0}
        inventory.append(entry)
        try:
            with summary_path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = set(reader.fieldnames or [])
                if not REQUIRED <= fields:
                    continue
                rows = list(reader)
            entry["rows"] = len(rows)
            scanned_rows += len(rows)
            # Experiment aggregate summaries repeat batch output, often without
            # the original intent. Export the underlying cohort rows only.
            log_path = summary_path.parent / "workflow.log"
            if not log_path.is_file():
                entry["status"] = "skipped_no_workflow_context"
                continue
            context, log_ref = workflow_context(log_path)
            summary_ref = file_ref(summary_path)
            entry["status"] = "processed"
        except (OSError, UnicodeError, csv.Error) as exc:
            entry["status"] = "read_error"
            errors.append({"path": str(summary_path), "error": str(exc)})
            continue
        for row_number, row in enumerate(rows, 2):
            accession = clean(row.get("accession"))
            if not accession or not re.fullmatch(r"GSE\d+", accession):
                errors.append({"path": str(summary_path), "row": row_number, "error": "invalid_accession"})
                continue
            if None in row or any(v is None for v in row.values()):
                errors.append({"path": str(summary_path), "row": row_number, "error": "malformed_csv_row"})
                continue
            if accession not in metadata_cache:
                path = data_root / accession / f"{accession}_metadata.csv"
                try:
                    metadata_cache[accession] = metadata_context(path)
                except (OSError, UnicodeError, csv.Error) as exc:
                    errors.append({"path": str(path), "error": str(exc)})
                    metadata_cache[accession] = ({}, None)
            metadata, metadata_ref = metadata_cache[accession]
            input_payload = {"accession": accession, **context, "metadata_columns_summary": metadata}
            # Outcome fields NEVER enter the input or the grouping key. Missing
            # intent is not assumed identical across different source runs.
            key_payload = {"task": "contrast_selection", "input": input_payload}
            if any(context[k] is None for k in context):
                key_payload["unknown_context_source"] = str(summary_path)
            key = digest(key_payload)
            label = {"design_column": clean(row.get("design_col")),
                     "control_value": clean(row.get("control")),
                     "treatment_value": clean(row.get("treatment"))}
            source = {"summary": summary_ref, "csv_record_number": row_number, "workflow": log_ref,
                      "metadata": metadata_ref, "observed_output": row,
                      "label_source": label_origin(row)}
            evidence_path = summary_path.parent / accession / "evidence.json"
            source["evidence"] = file_ref(evidence_path) if evidence_path.is_file() else None
            group = groups.setdefault(key, {
                "example_id": key, "task": "contrast_selection", "input": input_payload,
                "study_group": accession, "input_origin": "reconstructed_current_metadata_and_log_headers",
                "review_status": "pending", "training_ready": False, "flags": [
                    "historical_model_input_not_captured", "scientific_label_not_adjudicated",
                    "current_metadata_may_differ_from_run_or_aligned_subset"], "variants": {}})
            if not metadata:
                group["flags"] = sorted(set(group["flags"] + ["metadata_summary_missing"]))
            if any(context[k] is None for k in context):
                group["flags"] = sorted(set(group["flags"] + ["intent_context_incomplete"]))
            variant = group["variants"].setdefault(digest(label), {
                "candidate_label": label, "flags": label_issues(label, metadata), "sources": []})
            variant["sources"].append(source)
            candidate_rows += 1

    records = []
    for key, group in sorted(groups.items()):
        group["label_variants"] = [v for _, v in sorted(group.pop("variants").items())]
        group["label_conflict"] = len(group["label_variants"]) > 1
        group["occurrences"] = sum(len(v["sources"]) for v in group["label_variants"])
        group["flags"] = sorted(group["flags"])
        records.append(group)
    variant_count = sum(len(g["label_variants"]) for g in records)
    manifest = {
        "schema_version": "training-candidates-v0.2", "task": "contrast_selection",
        "source_output_root": str(output_root), "source_data_root": str(data_root),
        "summary_files_scanned": len(inventory), "summary_file_statuses": dict(Counter(x["status"] for x in inventory)),
        "compatible_schema_rows": scanned_rows, "candidate_rows": candidate_rows,
        "unique_input_groups": len(records), "unique_input_label_pairs": variant_count,
        "repeated_input_label_rows_collapsed": candidate_rows - variant_count,
        "unique_accessions": len({g["study_group"] for g in records}),
        "conflicting_input_groups": sum(g["label_conflict"] for g in records),
        "input_groups_with_metadata_summary": sum(bool(g["input"]["metadata_columns_summary"]) for g in records),
        "input_groups_with_complete_contrast": sum(any(all(v["candidate_label"].values()) for v in g["label_variants"]) for g in records),
        "training_ready_examples": 0, "read_or_row_errors": len(errors),
        "label_source_occurrences": dict(Counter(s["label_source"] for g in records for v in g["label_variants"] for s in v["sources"])),
        "split_policy": "No split yet. Adjudicate labels and link accessions by publication before allocating train/dev/test; preserve existing blind benchmarks.",
        "limitations": ["Only batch contrast-selection candidates, not full agent trajectories or alignment/SEA-CDM training data.",
                        "Hashes identify files at export time, not historical input snapshots.",
                        "Mechanical consistency and pipeline completion do not prove biological validity.",
                        "All conflicting labels and repeat provenance retained. No preferred gold label chosen."],
        "files": ["contrast_candidates.jsonl", "conflicts.jsonl", "source_inventory.json", "errors.json", "manifest.json"],
    }
    dataset_dir.mkdir(parents=True, exist_ok=False)
    for name, values in (("contrast_candidates.jsonl", records),
                         ("conflicts.jsonl", [g for g in records if g["label_conflict"]])):
        with (dataset_dir / name).open("w", encoding="utf-8", newline="\n") as handle:
            for value in values:
                handle.write(canonical(value) + "\n")
    for name, value in (("manifest.json", manifest), ("source_inventory.json", inventory), ("errors.json", errors)):
        (dataset_dir / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("output"))
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--dataset-dir", type=Path, default=Path("output/training_dataset_v0_candidates"))
    args = parser.parse_args()
    paths = [p if p.is_absolute() else ROOT / p for p in (args.output_root, args.data_root, args.dataset_dir)]
    try:
        manifest = export_dataset(*paths)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
