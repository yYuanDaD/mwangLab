"""Run the cached MoTrPAC big paper through the 17-table SEA-CDM extractor.

This is a direct single-paper experiment: it avoids keyword search and paper fetching so the
measured time/cost focus on schema extraction and reported-finding/gene extraction.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.cohort_tools import _count_csv_rows, init_cohort_csvs  # noqa: E402
from tools.cost_timing import RunProfiler  # noqa: E402
from tools.seacdm_tools import (  # noqa: E402
    append_tables_to_csvs,
    build_reported_findings,
    extract_tables_from_text,
)


STUDY_ID = "PMC11062907"
ORGANISM = "Rat"
TEXT_PATH = ROOT / "data" / "papers" / f"{STUDY_ID}.txt"
OUT_DIR = ROOT / "output" / "motrpac_big_paper_17table_0701"
CSV_DIR = OUT_DIR / "csv"
STUDY_DIR = OUT_DIR / "studies" / STUDY_ID
FINDINGS_CSV = STUDY_DIR / "reported_findings.csv"


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str).fillna("")


def _fk_summary() -> dict:
    gene = _read_csv(CSV_DIR / "gene.csv")
    exercise = _read_csv(CSV_DIR / "exercise.csv")
    if gene.empty:
        return {
            "gene_rows": 0,
            "exercise_rows": len(exercise),
            "genes_with_exercise_id": 0,
            "genes_missing_exercise_fk": 0,
        }
    exercise_ids = set(exercise.get("exercise_id", pd.Series(dtype=str)).astype(str))
    gene_exercise = gene.get("exercise_id", pd.Series([""] * len(gene))).astype(str)
    with_exercise = gene_exercise[gene_exercise != ""]
    missing = sorted(set(with_exercise) - exercise_ids)
    return {
        "gene_rows": len(gene),
        "exercise_rows": len(exercise),
        "genes_with_exercise_id": int((gene_exercise != "").sum()),
        "genes_missing_exercise_fk": len(missing),
        "missing_exercise_ids": missing,
    }


def main() -> int:
    if not TEXT_PATH.exists():
        print(f"ERROR: cached paper text not found: {TEXT_PATH}")
        return 2

    text = TEXT_PATH.read_text(encoding="utf-8", errors="ignore")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    init_cohort_csvs(str(CSV_DIR))

    profiler = RunProfiler()

    extraction_report: dict = {}
    extraction_usage: list[dict] = []
    with profiler.stage("schema_extraction"):
        tables = extract_tables_from_text(
            STUDY_ID,
            text,
            organism=ORGANISM,
            report=extraction_report,
            usage=extraction_usage,
        )
    profiler.add_llm_usage("schema_extraction", extraction_usage)
    append_tables_to_csvs(tables, str(CSV_DIR))

    (STUDY_DIR / "seacdm_tables.json").write_text(
        json.dumps(tables, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (STUDY_DIR / "seacdm_provenance.json").write_text(
        json.dumps(extraction_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    findings_report: dict = {}
    findings_usage: list[dict] = []
    with profiler.stage("reported_findings_gene"):
        findings_tables = build_reported_findings(
            STUDY_ID,
            text,
            str(FINDINGS_CSV),
            organism=ORGANISM,
            report=findings_report,
            existing_tables=tables,
            usage=findings_usage,
        )
    profiler.add_llm_usage("reported_findings_gene", findings_usage)
    append_tables_to_csvs(findings_tables, str(CSV_DIR))

    profiler.write_csv(str(OUT_DIR / "cost_timing.csv"))
    counts = _count_csv_rows(str(CSV_DIR))
    fk = _fk_summary()
    summary = {
        "study_id": STUDY_ID,
        "organism_hint": ORGANISM,
        "paper_text_path": str(TEXT_PATH),
        "paper_text_chars": len(text),
        "output_dir": str(OUT_DIR),
        "csv_dir": str(CSV_DIR),
        "row_counts": counts,
        "fk_summary": fk,
        "schema_extraction_report": extraction_report,
        "reported_findings_report": findings_report,
        "cost_timing_csv": str(OUT_DIR / "cost_timing.csv"),
        "total_wall_s": round(profiler.total_wall(), 2),
        "total_llm_calls": profiler.total_llm(),
        "total_input_tokens": profiler.total_in(),
        "total_output_tokens": profiler.total_out(),
        "total_usd_est": round(profiler.total_usd(), 4),
    }
    (OUT_DIR / "run_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
