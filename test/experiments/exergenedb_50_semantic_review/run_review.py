"""Run a 50-study ExerGeneDB-derived semantic preflight.

This deliberately tests the two high-risk decisions before any p-values are
computed: matrix semantics/method route and control-treatment identification.
It uses the archived GEO inputs collected for the earlier ExerGeneDB workflow,
keeps all LLM inputs/outputs, and flags cases for manual review rather than
silently treating a refusal as a correct answer.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.batch_tools import (
    _auto_detect_contrasts,
    _classify_matrix,
    _matrix_stats_preview,
)
from tools.llm_helpers import (
    classify_matrix_with_llm,
    summarize_metadata_for_llm,
    validate_contrast_with_llm,
    llm_usage_checkpoint,
    llm_usage_summary,
)
from tools.model_factory import resolve_model_config


ARCHIVE_DATA = ROOT / "archive" / "runtime" / "data_20260930"
OUT = ROOT / "output" / "exergenedb_50_semantic_review_20261001"

TREATMENT = [
    "exercise", "exercised", "post", "after", "trained", "training",
    "running", "run", "treadmill", "swimming", "wheel", "acute",
    "endurance", "resistance", "active",
]
CONTROL = [
    "sedentary", "control", "pre", "before", "rest", "sham",
    "baseline", "untrained", "inactive", "non-exercise", "nonexercise",
]

# These were explicitly called out in previous reports or regression reviews.
KNOWN_PROBLEM = [
    "GSE279359", "GSE282641", "GSE270703", "GSE317978", "GSE302944",
    "GSE308674", "GSE315678", "GSE315612", "GSE130401", "GSE208615",
    "GSE194193", "GSE194151",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def choose_matrix(folder: Path, accession: str) -> Path | None:
    candidates = []
    for p in folder.iterdir():
        if not p.is_file() or "metadata" in p.name.lower() or p.name.endswith(".soft.gz"):
            continue
        if p.suffix.lower() not in {".csv", ".tsv", ".txt", ".gz", ".tar"}:
            continue
        if p.name.endswith(".tar"):
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        # Prefer an actual matrix over a result table, sidecar metadata, or a
        # precomputed enrichment table.
        low = p.name.lower()
        penalty = sum(k in low for k in ("deg", "kegg", "gsea", "meta", "log2"))
        candidates.append((penalty, -size, p))
    return sorted(candidates, key=lambda x: (x[0], x[1]))[0][2] if candidates else None


def case_ids() -> list[str]:
    available = sorted(
        p.name for p in ARCHIVE_DATA.glob("GSE*")
        if (p / f"{p.name}_metadata.csv").is_file()
    )
    selected = [x for x in KNOWN_PROBLEM if x in available]
    for acc in available:
        if acc not in selected:
            selected.append(acc)
        if len(selected) >= 50:
            break
    return selected[:50]


def review_one(acc: str, usage_start: int) -> dict:
    folder = ARCHIVE_DATA / acc
    metadata = folder / f"{acc}_metadata.csv"
    df = pd.read_csv(metadata, index_col=0)
    summary = summarize_metadata_for_llm(str(metadata))
    python_contrasts = _auto_detect_contrasts(str(metadata), TREATMENT, CONTROL)
    python_pick = list(python_contrasts[0]) if python_contrasts else None
    result = {
        "accession": acc,
        "input_metadata": str(metadata.relative_to(ROOT)),
        "metadata_sha256": sha256(metadata),
        "n_samples": int(df.shape[0]),
        "metadata_columns": int(df.shape[1]),
        "python_contrasts": [list(x) for x in python_contrasts],
        "python_pick": python_pick,
        "known_problem_case": acc in KNOWN_PROBLEM,
        "matrix": None,
        "contrast": None,
        "flags": [],
    }

    matrix = choose_matrix(folder, acc)
    if matrix is None:
        result["flags"].append("no_local_expression_matrix")
    else:
        heuristic, classified_df = _classify_matrix(str(matrix))
        stats, preview = _matrix_stats_preview(str(matrix))
        matrix_result = {
            "path": str(matrix.relative_to(ROOT)),
            "sha256": sha256(matrix),
            "heuristic": heuristic,
            "heuristic_note": {
                "shape": list(classified_df.shape) if hasattr(classified_df, "shape") else None,
                "columns": [str(x) for x in list(classified_df.columns[:8])]
                if hasattr(classified_df, "columns") else [],
            },
            "input_stats": stats,
            "input_preview": preview,
        }
        if stats is None:
            matrix_result["status"] = "unreadable_matrix"
            result["flags"].append("unreadable_matrix")
        else:
            try:
                llm = classify_matrix_with_llm(
                    filename=matrix.name,
                    platform="",
                    value_stats=stats,
                    preview_text=preview or "",
                    heuristic_label=heuristic,
                    organism="human/mouse/rat unknown",
                    provenance="archived ExerGeneDB-derived GEO input",
                )
                matrix_result["llm"] = llm.model_dump() if llm else None
                if llm is None:
                    result["flags"].append("matrix_llm_unavailable")
                elif llm.matrix_type == "ambiguous" or llm.confidence == "low":
                    result["flags"].append("matrix_semantics_uncertain")
                elif llm.matrix_type != heuristic:
                    result["flags"].append("matrix_llm_disagrees_with_heuristic")
            except Exception as exc:
                matrix_result["error"] = f"{type(exc).__name__}: {exc}"
                result["flags"].append("matrix_llm_error")
        result["matrix"] = matrix_result

    # Always ask the semantic validator in this benchmark. This is intentional:
    # it measures whether a cheap Python confidence gate would have hidden a
    # wrong control group.
    try:
        llm = validate_contrast_with_llm(
            accession=acc,
            metadata_columns_summary=summary,
            treatment_keywords=TREATMENT,
            control_keywords=CONTROL,
            proposed=tuple(python_pick) if python_pick else None,
        )
        contrast_result = {
            "input_metadata_summary": summary,
            "treatment_keywords": TREATMENT,
            "control_keywords": CONTROL,
            "llm": llm.model_dump() if llm else None,
        }
        if llm is None:
            result["flags"].append("contrast_llm_unavailable")
        elif not all((llm.design_column, llm.control_value, llm.treatment_value)):
            result["flags"].append("contrast_refused_or_incomplete")
        elif python_pick and tuple(python_pick) != (
                llm.design_column, llm.control_value, llm.treatment_value):
            result["flags"].append("contrast_llm_overrode_python")
        if llm is not None:
            if llm.intent_match is False:
                result["flags"].append("contrast_intent_mismatch")
            elif llm.intent_match is None:
                result["flags"].append("contrast_intent_unconfirmed")
            if llm.confidence == "low":
                result["flags"].append("contrast_low_confidence")
        result["contrast"] = contrast_result
    except Exception as exc:
        result["contrast"] = {"input_metadata_summary": summary,
                               "error": f"{type(exc).__name__}: {exc}"}
        result["flags"].append("contrast_llm_error")

    usage = llm_usage_summary(usage_start)
    result["llm_usage"] = usage
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    selected = case_ids()
    config = resolve_model_config()
    manifest = {
        "benchmark": "ExerGeneDB-derived 50-study semantic preflight",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_root": str(ARCHIVE_DATA.relative_to(ROOT)),
        "case_count": len(selected),
        "accessions": selected,
        "known_problem_cases": [x for x in selected if x in KNOWN_PROBLEM],
        "treatment_keywords": TREATMENT,
        "control_keywords": CONTROL,
        "provider": config.provider,
        "model": config.model,
        "scope": "semantic decisions only; no p-values or enrichment calls",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    usage_start = llm_usage_checkpoint()
    records = []
    for i, acc in enumerate(selected, 1):
        print(f"[{i}/{len(selected)}] {acc}", flush=True)
        record = review_one(acc, usage_start)
        records.append(record)
        (OUT / "records.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  flags={','.join(record['flags']) or 'none'}", flush=True)

    final = {
        "manifest": manifest,
        "records": records,
        "usage": llm_usage_summary(usage_start),
        "flag_counts": pd.Series(
            [flag for r in records for flag in r["flags"]]
        ).value_counts().to_dict(),
    }
    (OUT / "report.json").write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    flagged = pd.DataFrame([
        {"accession": r["accession"], "known_problem_case": r["known_problem_case"],
         "n_samples": r["n_samples"], "python_pick": r["python_pick"],
         "flags": ";".join(r["flags"])}
        for r in records if r["flags"]
    ])
    flagged.to_csv(OUT / "flagged_cases.csv", index=False)
    print(json.dumps(final["flag_counts"], indent=2, ensure_ascii=False))
    print(json.dumps(final["usage"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
