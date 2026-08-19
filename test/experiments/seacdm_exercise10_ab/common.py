"""Shared deterministic helpers for the exercise 10-paper SEA-CDM A/B."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import csv


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


GENERAL = load_module(
    "exercise10_generalization_helpers",
    ROOT / "test" / "experiments" / "deepseek_seacdm_generalization" / "run_experiment.py",
)
H = GENERAL.H
PRICES = H.PRICES
REQUIRED_TABLES = (
    "study", "experiment", "subject", "sample", "groups", "interventions",
    "assay", "documentation",
)
DESCRIPTIVE_TABLES = ("study", "experiment", "interventions", "material", "documentation")
STRUCTURAL_TABLES = ("subject", "sample", "groups", "assay")

EXERCISE_TERMS = (
    "exercise", "training", "treadmill", "wheel running", "voluntary wheel",
    "running wheel", "endurance", "resistance", "aerobic", "sprint", "hiit", "mict",
    "bfrt", "crest", "ladder climbing", "ladder-climbing",
)


def has_exercise_terms(*values) -> bool:
    text = " ".join(str(value or "").lower() for value in values)
    return any(term in text for term in EXERCISE_TERMS)


def metadata_requires_exercise(metadata_path: str) -> bool:
    """Require Exercise only when the target GEO samples expose an exercise arm/protocol."""
    with open(metadata_path, encoding="utf-8-sig", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        relevant = [name for name in (reader.fieldnames or []) if any(
            token in str(name).lower()
            for token in ("title", "characteristics", "treatment_protocol", "description")
        )]
        if has_exercise_terms(*relevant):
            return True
        return any(has_exercise_terms(*(row.get(name) for name in relevant)) for row in reader)


def exercise_semantics(tables: dict, metadata_path: str) -> dict:
    """Evaluate the hard Exercise-node rule without using provenance/comments as identity."""
    rows = tables.get("exercise") or []
    valid = [row for row in rows if has_exercise_terms(
        row.get("exercise_name"), row.get("exercise_type")
    )]
    invalid_ids = [row.get("exercise_id") for row in rows if row not in valid]
    required = metadata_requires_exercise(metadata_path)
    return {
        "required_by_geo_scope": required,
        "valid_rows": len(valid),
        "invalid_row_ids": invalid_ids,
        "passed": not invalid_ids and (not required or bool(valid)),
    }


def exercise_semantics_after_projection_fix(tables: dict, metadata_path: str) -> dict:
    """Regrade model interventions using the corrected deterministic Exercise projection."""
    exercise_interventions = [row for row in (tables.get("interventions") or []) if
                              has_exercise_terms(row.get("material"), row.get("intervention_type"))]
    required = metadata_requires_exercise(metadata_path)
    return {
        "required_by_geo_scope": required,
        "projected_rows": len(exercise_interventions),
        "passed": not required or bool(exercise_interventions),
    }


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canon_hash(value) -> str:
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def design_scope_audit(tables: dict, target_study: str) -> dict:
    text = GENERAL._table_text(tables, ("experiment", "interventions", "assay"))
    accessions = sorted({item.upper() for item in re.findall(r"\bGSE\d+\b", text, re.I)})
    foreign = [item for item in accessions if item != target_study.upper()]
    return {"design_accessions": accessions, "foreign_design_accessions": foreign,
            "passed": not foreign}


def table_fill(tables: dict) -> dict:
    result = {}
    for name, rows in tables.items():
        cells = [value for row in rows for value in row.values()]
        nonnull = sum(value not in (None, "", []) for value in cells)
        result[name] = {"rows": len(rows), "nonnull": nonnull, "cells": len(cells)}
    return result


def token_overlap(left: str, right: str) -> float:
    a = set(re.findall(r"[a-z0-9]+", str(left).lower()))
    b = set(re.findall(r"[a-z0-9]+", str(right).lower()))
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0
