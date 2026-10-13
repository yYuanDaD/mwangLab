"""Export ExerGeneDB sample annotations as a frozen control/treatment gold set.

ExerGeneDB (https://exergenedb.com) curates every included sample as
`Exercise` or `Sedentary`. This script pages through the public sample
endpoints used by the site's Explore > Sample view and writes:

    exergenedb_samples.csv          one row per sample (deduplicated)
    exergenedb_series.csv           one row per series with design summary
    covariance_annotations.csv      manual template; created once, never overwritten
    manifest.json                   endpoints, row counts, and file hashes

Scope of the gold labels:
- `group` is usable as control/treatment gold at the sample level.
- It is NOT a pairing/covariance gold: every Sedentary sample is labelled
  "Pre exercise", including between-subject sedentary animals, and there is no
  subject/donor ID. Pairing must be annotated from GEO or the paper.
- The database was last updated in 2023, so recent GEO series are absent.

Usage:
    python scripts/fetch_exergenedb_labels.py
    python scripts/fetch_exergenedb_labels.py --out-dir test/validation/exergenedb_gold
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://exergenedb.com/"
SOURCES = [
    ("getData/getHumanPdList", "Homo sapiens"),
    ("getData/getMousePdList", "Mus musculus"),
    ("getData/getMousePdList", "Rattus norvegicus"),
]
PAGE_SIZE = 1000
CONTROL_LABEL = "Sedentary"
TREATMENT_LABEL = "Exercise"
STRATUM_FIELDS = ["tissue_char1", "health_condition", "gender", "other_treatment", "age_char2"]
LEADING_COLUMNS = [
    "sample_id", "series_id", "organism", "role", "group", "sampling_time",
    "stratum_key", "seqtech", "seqtype", "tissue_char1", "tissue_char2",
    "health_condition", "gender", "age_char1", "age_char1_week", "age_char2",
    "other_treatment", "exe_pattern", "exe_type", "exe_modality", "exe_intensity",
    "exe_time", "exe_freq", "exe_duration", "strain_char1", "strain_char2",
    "bmi_char1", "bmi_char2", "egdb_ids",
]
ANNOTATION_COLUMNS = [
    "accession", "design_class", "pairing_unit", "pairing_evidence",
    "required_covariates", "interaction_terms", "primary_contrast",
    "annotator", "annotated_on", "notes",
]


def post_json(session: requests.Session, path: str, body: dict, retries: int = 3) -> dict:
    last_error = None
    for attempt in range(retries):
        try:
            resp = session.post(BASE_URL + path, json=body, timeout=120)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("code") != 0:
                raise RuntimeError(f"{path}: API returned code={payload.get('code')}")
            return payload["data"]
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{path} failed after {retries} attempts: {last_error}")


def fetch_organism(session: requests.Session, path: str, organism: str) -> tuple[list[dict], int]:
    rows: list[dict] = []
    page = 1
    total = None
    while True:
        data = post_json(session, path, {"organism": [organism], "page": page, "pageSize": PAGE_SIZE})
        total = int(data["total"])
        batch = data["list"]
        rows.extend(batch)
        if len(batch) < PAGE_SIZE or len(rows) >= total:
            break
        page += 1
        time.sleep(0.5)
    if len(rows) != total:
        raise RuntimeError(f"{organism}: fetched {len(rows)} rows but API reported total={total}")
    return rows, total


def join_unique(values) -> str:
    seen = []
    for value in values:
        text = "" if value is None else str(value).strip()
        if text and text not in seen:
            seen.append(text)
    return ";".join(seen)


def deduplicate_samples(records: list[dict]) -> pd.DataFrame:
    """Collapse mRNA/ncRNA duplicate rows per sample; fail closed on label conflicts."""
    raw = pd.DataFrame(records)
    for column in raw.columns:
        raw[column] = raw[column].map(lambda v: "" if v is None else str(v).strip())
    conflicts = raw.groupby("sample_id")["group"].nunique()
    conflicts = conflicts[conflicts > 1]
    if not conflicts.empty:
        raise RuntimeError(f"conflicting group labels for samples: {conflicts.index[:10].tolist()}")
    unknown = sorted(set(raw["group"]) - {CONTROL_LABEL, TREATMENT_LABEL})
    if unknown:
        raise RuntimeError(f"unexpected group labels: {unknown}")

    collapsed = raw.groupby("sample_id", sort=True).agg(join_unique).reset_index()
    collapsed = collapsed.rename(columns={"id": "egdb_ids"})
    collapsed["role"] = collapsed["group"].map({CONTROL_LABEL: "control", TREATMENT_LABEL: "treatment"})
    collapsed["stratum_key"] = collapsed.apply(
        lambda r: " | ".join(str(r.get(f, "")) for f in STRATUM_FIELDS), axis=1)
    ordered = [c for c in LEADING_COLUMNS if c in collapsed.columns]
    rest = sorted(c for c in collapsed.columns if c not in ordered)
    return collapsed[ordered + rest]


def design_class(n_time_levels: int, n_strata: int) -> str:
    multi_time = n_time_levels > 2
    multi_strata = n_strata > 1
    if multi_time and multi_strata:
        return "multi_time_and_strata"
    if multi_time:
        return "multi_time"
    if multi_strata:
        return "multi_strata"
    return "simple"


def summarize_series(samples: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for accession, group in samples.groupby("series_id", sort=True):
        times = sorted(set(group["sampling_time"]))
        strata = sorted(set(group["stratum_key"]))
        rows.append({
            "accession": accession,
            "is_geo_series": accession.startswith("GSE"),
            "organism": join_unique(group["organism"]),
            "seqtech": join_unique(group["seqtech"]),
            "n_samples": len(group),
            "n_treatment": int((group["role"] == "treatment").sum()),
            "n_control": int((group["role"] == "control").sum()),
            "n_time_levels": len(times),
            "time_levels": ";".join(times),
            "n_strata": len(strata),
            "strata": " || ".join(strata),
            "design_class": design_class(len(times), len(strata)),
        })
    return pd.DataFrame(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_annotation_template(series: pd.DataFrame, path: Path) -> bool:
    if path.exists():
        return False
    template = pd.DataFrame({"accession": series["accession"], "design_class": series["design_class"]})
    for column in ANNOTATION_COLUMNS:
        if column not in template.columns:
            template[column] = ""
    template[ANNOTATION_COLUMNS].to_csv(path, index=False)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", default=str(ROOT / "test" / "validation" / "exergenedb_gold"))
    args = parser.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"Accept": "application/json", "User-Agent": "mwangLab-gold-export/1.0"})
    records: list[dict] = []
    totals = {}
    for path, organism in SOURCES:
        rows, total = fetch_organism(session, path, organism)
        records.extend(rows)
        totals[organism] = total
        print(f"{organism}: {total} rows")

    samples = deduplicate_samples(records)
    series = summarize_series(samples)
    samples_path = out_dir / "exergenedb_samples.csv"
    series_path = out_dir / "exergenedb_series.csv"
    samples.to_csv(samples_path, index=False)
    series.to_csv(series_path, index=False)
    created_template = write_annotation_template(series, out_dir / "covariance_annotations.csv")

    geo = series[series["is_geo_series"]]
    manifest = {
        "source": BASE_URL,
        "endpoints": [{"path": p, "organism": o} for p, o in SOURCES],
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "api_rows_by_organism": totals,
        "api_rows_total": len(records),
        "unique_samples": len(samples),
        "series_total": len(series),
        "geo_series": len(geo),
        "geo_design_class_counts": geo["design_class"].value_counts().to_dict(),
        "role_counts": samples["role"].value_counts().to_dict(),
        "files": {p.name: sha256(p) for p in (samples_path, series_path)},
        "gold_scope": "sample-level control/treatment only; pairing and covariates are not encoded",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"unique samples: {len(samples)} | series: {len(series)} (GEO {len(geo)})")
    print(f"design classes (GEO): {manifest['geo_design_class_counts']}")
    if created_template:
        print("created covariance_annotations.csv template")
    print(f"wrote {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
