"""Search `exercise`, fetch papers, and freeze a shared 10-paper GEO-backed manifest."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

import pandas as pd
import requests


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import ROOT, file_hash  # noqa: E402

from tools.cohort_tools import (  # noqa: E402
    _is_exercise_relevant_search_hit,
    _locate_text,
)
from tools.geo_tools import download_geo_data, search_geo_studies  # noqa: E402
from tools.paper_tools import fetch_paper_text  # noqa: E402


def now():
    return datetime.now(timezone.utc).isoformat()


def _epmc_record(pmid: str) -> dict:
    response = requests.get(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        params={"query": f"EXT_ID:{pmid} AND SRC:MED", "format": "json",
                "resultType": "core", "pageSize": 1},
        timeout=30,
    )
    response.raise_for_status()
    rows = response.json().get("resultList", {}).get("result", [])
    return rows[0] if rows else {}


def _open_pdf(record: dict) -> str:
    urls = record.get("fullTextUrlList", {}).get("fullTextUrl", []) or []
    for row in urls:
        if str(row.get("documentStyle", "")).lower() == "pdf":
            return row.get("url", "")
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--keyword", default="exercise")
    parser.add_argument("--papers", type=int, default=10)
    parser.add_argument("--search-pool", type=int, default=60)
    args = parser.parse_args()
    if args.keyword.casefold() != "exercise":
        raise SystemExit("This frozen development experiment requires keyword='exercise'")
    if not 8 <= args.papers <= 12:
        raise SystemExit("papers must be approximately ten (8..12)")

    out = Path(args.output_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty experiment directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    print(f"Searching GEO-linked papers for {args.keyword!r}...", flush=True)
    report = search_geo_studies.invoke({
        "keyword": args.keyword, "organism": "Any", "min_samples": 6,
        "max_samples": 300, "max_results": args.search_pool,
        "output_dir": str(out),
    })
    geo_csv = out / "geo_search_exercise.csv"
    if not geo_csv.is_file():
        raise SystemExit(f"GEO search returned no table: {report}")
    rows = pd.read_csv(geo_csv, dtype=str, keep_default_na=False).to_dict("records")

    selected, considered, seen_gse = [], [], set()
    for position, row in enumerate(rows, 1):
        relevance_row = {"title": row.get("title", ""), "abstract": row.get("summary", "")}
        relevant, reason = _is_exercise_relevant_search_hit(relevance_row)
        study_id = row.get("accession", "").upper()
        item = {
            "search_index": position, "study_id": study_id,
            "title": row.get("title", ""), "exercise_relevant": relevant,
            "relevance_reason": reason, "status": "",
        }
        if not relevant:
            item["status"] = "skipped_not_exercise_relevant"
            considered.append(item)
            continue
        pmids = [value for value in re.split(r"[;,\s]+", row.get("pubmed_id", "")) if value]
        if not pmids:
            item["status"] = "skipped_no_pubmed_id"
            considered.append(item)
            continue
        pmid = pmids[0]
        try:
            epmc = _epmc_record(pmid)
        except Exception as exc:
            item["status"] = f"skipped_epmc_lookup:{type(exc).__name__}"
            considered.append(item)
            continue
        pmcid = epmc.get("pmcid", "") or ""
        pdf_url = _open_pdf(epmc)
        if not pmcid and not pdf_url:
            item["status"] = "skipped_no_open_fulltext"
            considered.append(item)
            continue
        paper_id = f"{study_id}_{pmid}"
        print(f"  fetch #{position} {study_id}: {(row.get('title') or '')[:65]}", flush=True)
        fetch_result = fetch_paper_text.invoke({
            "pmcid": pmcid, "pdf_url": pdf_url, "paper_id": paper_id,
        })
        text_path_raw = _locate_text(paper_id, pmcid)
        if not text_path_raw:
            item["status"] = "skipped_fetch_failed"
            item["fetch_result"] = str(fetch_result)[:400]
            considered.append(item)
            continue
        text_path = (ROOT / text_path_raw).resolve() if not Path(text_path_raw).is_absolute() else Path(text_path_raw)
        text = text_path.read_text(encoding="utf-8", errors="ignore")
        if study_id in seen_gse:
            item["status"] = "skipped_duplicate_gse"
            considered.append(item)
            continue
        metadata = ROOT / "data" / study_id / f"{study_id}_metadata.csv"
        if not metadata.is_file():
            print(f"    metadata {study_id} downloading...", flush=True)
            download_geo_data.invoke({"geo_accession": study_id})
        if not metadata.is_file():
            item["status"] = "skipped_no_metadata"
            considered.append(item)
            continue
        n_samples = max(0, sum(1 for _ in metadata.open(encoding="utf-8", errors="ignore")) - 1)
        selected_row = {
            **item, "status": "selected", "pmid": pmid, "pmcid": pmcid,
            "paper_id": paper_id, "organism": row.get("organism", ""),
            "text_path": str(text_path),
            "metadata_path": str(metadata.resolve()), "metadata_samples": n_samples,
            "paper_sha256": file_hash(text_path), "metadata_sha256": file_hash(metadata),
            "source_accessions": sorted(
                {item.upper() for item in re.findall(r"\bGSE\d+\b", text, re.I)} | {study_id}
            ),
        }
        selected.append(selected_row)
        considered.append(selected_row)
        seen_gse.add(study_id)
        print(f"    selected {study_id}: {n_samples} metadata samples", flush=True)
        if len(selected) >= args.papers:
            break

    if len(selected) < 8:
        (out / "prepare_considered.json").write_text(
            json.dumps(considered, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        raise SystemExit(f"Only {len(selected)} GEO-backed papers found; need at least 8")

    manifest = {
        "schema_version": "1.0", "keyword": args.keyword,
        "prepared_at": now(), "requested_papers": args.papers,
        "selected_papers": len(selected), "search_pool": args.search_pool,
        "search_report": str(report), "cases": selected,
        "frozen_rules": {
            "same_manifest_both_models": True, "strategy": "staged",
            "temperature": 0, "max_stage_retries": 1, "max_chars": 100000,
            "required_tables": [
                "study", "experiment", "subject", "sample", "groups", "interventions",
                "exercise", "assay", "documentation",
            ],
            "blocking": [
                "exception", "schema_error", "fk_error", "missing_required_table",
                "group_error", "metadata_sample_count_mismatch", "foreign_design_accession",
            ],
        },
    }
    manifest_path = out / "frozen_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "prepare_considered.json").write_text(
        json.dumps(considered, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({
        "manifest": str(manifest_path), "selected": len(selected),
        "studies": [row["study_id"] for row in selected],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
