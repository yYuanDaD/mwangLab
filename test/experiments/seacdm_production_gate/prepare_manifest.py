"""Prepare a frozen 30-case GEO-backed SEA-CDM production-gate manifest.

Preparation uses GEO/Europe PMC plus existing local caches, but makes no LLM calls.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pandas as pd
import requests


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "test" / "experiments" / "seacdm_exercise10_ab"))

from common import file_hash, metadata_requires_exercise  # noqa: E402
from tools.geo_tools import download_geo_data, search_geo_studies  # noqa: E402
from tools.paper_tools import fetch_paper_text  # noqa: E402
from tools.cohort_tools import _locate_text  # noqa: E402


EXERCISE_RE = re.compile(
    r"\b(exercis\w*|training|treadmill|wheel[- ]running|endurance|resistance|aerobic|"
    r"physical activity|contractile activity|HIIT|sprint|swimming)\b",
    re.I,
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_commit() -> str:
    completed = subprocess.run(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "rev-parse", "HEAD"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


def _epmc_record(pmid: str) -> dict:
    response = requests.get(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        params={"query": f"EXT_ID:{pmid} AND SRC:MED", "format": "json",
                "resultType": "core", "pageSize": 1},
        timeout=30,
    )
    response.raise_for_status()
    records = response.json().get("resultList", {}).get("result", [])
    return records[0] if records else {}


def _open_pdf(record: dict) -> str:
    for row in record.get("fullTextUrlList", {}).get("fullTextUrl", []) or []:
        if str(row.get("documentStyle", "")).lower() == "pdf":
            return str(row.get("url") or "")
    return ""


def _cached_cases() -> dict[str, dict]:
    manifests = sorted((ROOT / "output").glob("seacdm_exercise10_ab_*/frozen_manifest.json"))
    considered_files = sorted(
        (ROOT / "output").glob("seacdm_production_gate_v1_inputs*/prepare_considered.json")
    )
    cached: dict[str, dict] = {}
    for path in manifests:
        try:
            for case in json.loads(path.read_text(encoding="utf-8")).get("cases", []):
                if Path(case.get("text_path", "")).is_file() and Path(
                    case.get("metadata_path", "")
                ).is_file():
                    cached[str(case["study_id"]).upper()] = case
        except (OSError, ValueError, KeyError):
            continue
    for path in considered_files:
        try:
            for case in json.loads(path.read_text(encoding="utf-8")):
                if Path(case.get("text_path", "")).is_file() and Path(
                    case.get("metadata_path", "")
                ).is_file():
                    cached[str(case["study_id"]).upper()] = case
        except (OSError, ValueError, KeyError):
            continue
    return cached


def _metadata_profile(path: Path) -> dict:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    relevant = [
        col for col in frame.columns
        if "characteristics" in col.lower() or "treatment_protocol" in col.lower()
    ]
    levels = {
        col: int(frame[col].astype(str).str.strip().replace("", pd.NA).nunique(dropna=True))
        for col in relevant
    }
    viable = {
        col: value for col, value in levels.items()
        if 2 <= value <= 12 and value / max(len(frame), 1) <= 0.75
    }
    return {
        "samples": int(len(frame)),
        "relevant_columns": len(relevant),
        "viable_axis_columns": len(viable),
        "max_levels": max(viable.values(), default=0),
        "exercise_required": bool(metadata_requires_exercise(str(path))),
    }


def _labels(source_accessions: list[str], profile: dict) -> list[str]:
    labels = []
    if len(source_accessions) > 1:
        labels.append("multi_accession")
    if profile["viable_axis_columns"] >= 2 or profile["max_levels"] >= 4:
        labels.append("complex_metadata")
    if not profile["exercise_required"]:
        labels.append("target_no_exercise")
    if len(source_accessions) == 1 and profile["viable_axis_columns"] <= 1:
        labels.append("routine_single")
    return labels or ["other_geo_backed"]


def _select_balanced(candidates: list[dict], total: int) -> list[dict]:
    quotas = (
        ("routine_single", 8, lambda case: (
            len(case["source_accessions"]) == 1
            and case["metadata_profile"]["exercise_required"]
            and case["metadata_profile"]["viable_axis_columns"] <= 2
        )),
        ("multi_accession", 8, lambda case: len(case["source_accessions"]) > 1),
        ("complex_metadata", 8, lambda case: (
            len(case["source_accessions"]) == 1
            and case["metadata_profile"]["exercise_required"]
            and case["metadata_profile"]["viable_axis_columns"] >= 3
        )),
        ("target_no_exercise", 6, lambda case: (
            not case["metadata_profile"]["exercise_required"]
        )),
    )
    selected: list[dict] = []
    used: set[str] = set()
    for category, quota, predicate in quotas:
        eligible = sorted(
            (case for case in candidates if case["study_id"] not in used and predicate(case)),
            key=lambda case: int(case["search_index"]),
        )
        for case in eligible[:quota]:
            chosen = dict(case)
            chosen["primary_category"] = category
            selected.append(chosen)
            used.add(case["study_id"])
    if len(selected) < total:
        for case in sorted(candidates, key=lambda item: int(item["search_index"])):
            if case["study_id"] in used:
                continue
            chosen = dict(case)
            chosen["primary_category"] = "diversity_fill"
            selected.append(chosen)
            used.add(case["study_id"])
            if len(selected) == total:
                break
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--cases", type=int, default=30)
    parser.add_argument("--search-pool", type=int, default=250)
    args = parser.parse_args()
    if args.cases != 30:
        raise SystemExit("Production Gate v1 is preregistered for exactly 30 cases")

    out = Path(args.output_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "PREREGISTERED_PROTOCOL.md", out / "PREREGISTERED_PROTOCOL.md")

    report = search_geo_studies.invoke({
        "keyword": "exercise", "organism": "Any", "min_samples": 6,
        "max_samples": 300, "max_results": args.search_pool, "output_dir": str(out),
    })
    search_csv = out / "geo_search_exercise.csv"
    if not search_csv.is_file():
        raise SystemExit(f"GEO search did not produce {search_csv}: {report}")

    cached = _cached_cases()
    rows = pd.read_csv(search_csv, dtype=str, keep_default_na=False).to_dict("records")
    candidates: list[dict] = []
    considered: list[dict] = []
    seen: set[str] = set()
    for position, row in enumerate(rows, 1):
        study_id = str(row.get("accession") or "").upper()
        title = str(row.get("title") or "")
        summary = str(row.get("summary") or "")
        item = {"search_index": position, "study_id": study_id, "title": title}
        if not EXERCISE_RE.search(f"{title}\n{summary}"):
            item["status"] = "skipped_no_explicit_exercise_context"
            considered.append(item)
            continue
        if study_id in seen:
            item["status"] = "skipped_duplicate"
            considered.append(item)
            continue

        cached_case = cached.get(study_id)
        text_path = Path(cached_case["text_path"]) if cached_case else None
        pmids = [value for value in re.split(r"[;,\s]+", row.get("pubmed_id", "")) if value]
        pmid = pmids[0] if pmids else ""
        pmcid = str((cached_case or {}).get("pmcid") or "")
        if not text_path or not text_path.is_file():
            if not pmid:
                item["status"] = "skipped_no_pubmed_id"
                considered.append(item)
                continue
            try:
                epmc = _epmc_record(pmid)
                pmcid = str(epmc.get("pmcid") or "")
                pdf_url = _open_pdf(epmc)
            except Exception as exc:  # network preparation is best-effort per case
                item["status"] = f"skipped_epmc:{type(exc).__name__}"
                considered.append(item)
                continue
            if not pmcid and not pdf_url:
                item["status"] = "skipped_no_open_fulltext"
                considered.append(item)
                continue
            paper_id = f"{study_id}_{pmid}"
            print(f"fetch {position}/{len(rows)} {study_id}: {title[:65]}", flush=True)
            fetch_paper_text.invoke({"pmcid": pmcid, "pdf_url": pdf_url, "paper_id": paper_id})
            located = _locate_text(paper_id, pmcid)
            if not located:
                item["status"] = "skipped_fetch_failed"
                considered.append(item)
                continue
            text_path = Path(located)
            if not text_path.is_absolute():
                text_path = (ROOT / text_path).resolve()

        metadata = ROOT / "data" / study_id / f"{study_id}_metadata.csv"
        if not metadata.is_file():
            print(f"metadata {study_id} downloading", flush=True)
            download_geo_data.invoke({"geo_accession": study_id})
        if not metadata.is_file():
            item["status"] = "skipped_no_metadata"
            considered.append(item)
            continue

        text = text_path.read_text(encoding="utf-8", errors="ignore")
        source_accessions = sorted(
            {match.upper() for match in re.findall(r"\bGSE\d+\b", text, re.I)} | {study_id}
        )
        profile = _metadata_profile(metadata)
        case = {
            **item,
            "status": "candidate",
            "pmid": pmid or str((cached_case or {}).get("pmid") or ""),
            "pmcid": pmcid,
            "organism": str(row.get("organism") or ""),
            "text_path": str(text_path.resolve()),
            "metadata_path": str(metadata.resolve()),
            "metadata_samples": profile["samples"],
            "paper_sha256": file_hash(text_path),
            "metadata_sha256": file_hash(metadata),
            "source_accessions": source_accessions,
            "metadata_profile": profile,
            "case_labels": _labels(source_accessions, profile),
        }
        candidates.append(case)
        considered.append(case)
        seen.add(study_id)

    selected = _select_balanced(candidates, args.cases)
    selected_ids = {case["study_id"] for case in selected}
    for case in considered:
        if case.get("status") == "candidate":
            case["status"] = "selected" if case["study_id"] in selected_ids else "not_selected"
    (out / "prepare_considered.json").write_text(
        json.dumps(considered, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if len(selected) < args.cases:
        raise SystemExit(
            f"Only {len(selected)} eligible cached/open-full-text GEO cases; need {args.cases}"
        )

    manifest = {
        "schema_version": "1.0",
        "experiment": "Large-scale SEA-CDM Production Gate v1",
        "prepared_at": now(),
        "git_commit": _git_commit(),
        "keyword": "exercise",
        "requested_cases": args.cases,
        "selected_cases": len(selected),
        "search_pool": args.search_pool,
        "search_report": str(report),
        "cases": selected,
        "frozen_execution": {
            "provider": "deepseek", "model": "deepseek-v4-pro", "temperature": 0,
            "strategy": "staged", "max_stage_retries": 1, "max_chars": 100000,
            "structured_max_tokens": 16384, "repeats": 3, "shuffle_seed": 20260819,
            "deepseek_budget_usd": 4.50,
        },
    }
    manifest_path = out / "frozen_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({
        "manifest": str(manifest_path),
        "selected": len(selected),
        "labels": {
            label: sum(case.get("primary_category") == label for case in selected)
            for label in ("routine_single", "multi_accession", "complex_metadata",
                          "target_no_exercise")
        },
        "studies": [case["study_id"] for case in selected],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
