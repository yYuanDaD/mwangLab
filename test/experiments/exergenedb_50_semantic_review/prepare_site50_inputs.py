"""Inventory and download GEO supplementary inputs; no external LLM calls.

Run without --download to inspect the inventory, then supply --download.
Original review inputs and records remain unchanged.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "output/exergenedb_site50_random_review_20261001"
STAGE = OUT / "input_data"
ARCHIVE = ROOT / "archive/runtime/data_20260930"


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def inventory(acc):
    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{acc[:-3]}nnn/{acc}/suppl/"
    result = {"accession": acc, "source_url": url, "files": [], "errors": []}
    try:
        r = requests.get(url, timeout=(15, 60))
        if r.status_code == 404:
            result["status"] = "no_supplementary_directory"
            return result
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a[href]"):
            href = a["href"]
            name = unquote(href.split("/")[-1])
            if not name.startswith(acc) or not name or href.endswith("/"):
                continue
            if Path(name).name != name:
                continue
            item = {"filename": name, "url": urljoin(url, href)}
            lines = soup.get_text("\n", strip=False).splitlines()
            item["listing_text"] = next((line.strip() for line in lines if name in line), name)
            # Listing text retains source-side size/time even without Content-Length.
            result["files"].append(item)
        result["status"] = "listed" if result["files"] else "no_supplementary_files"
    except Exception as exc:
        result["status"] = "listing_failed"
        result["errors"].append(f"{type(exc).__name__}: {exc}")
    return result


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_study(study):
    acc = study["accession"]
    folder = STAGE / acc
    folder.mkdir(parents=True, exist_ok=True)
    source_metadata = ARCHIVE / acc / f"{acc}_metadata.csv"
    target_metadata = folder / f"{acc}_metadata.csv"
    if source_metadata.exists() and not target_metadata.exists():
        shutil.copy2(source_metadata, target_metadata)
    result = {"accession": acc, "downloads": []}
    for item in study["files"]:
        row = dict(item)
        name = row["filename"]
        path = folder / name
        row["path"] = str(path.relative_to(ROOT))
        # GEO supplementary data (including RAW.tar) are processed submissions.
        # If a submission includes actual sequencing reads, leave them for SRA routing.
        if name.lower().endswith((".fastq", ".fastq.gz", ".fq.gz", ".bam", ".cram", ".sra")):
            row["status"] = "sequencing_reads_not_expression_matrix"
            result["downloads"].append(row)
            continue
        if path.exists() and path.stat().st_size:
            row["status"] = "already_present"
            row["bytes"] = path.stat().st_size
            row["sha256"] = sha256(path)
            result["downloads"].append(row)
            continue
        partial = path.with_name(path.name + ".part")
        for attempt in range(1, 4):
            try:
                print(f"DOWNLOAD {acc} {name} attempt={attempt}", flush=True)
                with requests.get(row["url"], stream=True, timeout=(15, 60)) as response:
                    response.raise_for_status()
                    expected = int(response.headers.get("Content-Length", "0"))
                    h = hashlib.sha256()
                    size = 0
                    with partial.open("wb") as fh:
                        next_progress = 64 * 1024 * 1024
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                fh.write(chunk)
                                h.update(chunk)
                                size += len(chunk)
                                if size >= next_progress:
                                    print(f"PROGRESS {acc} {name} bytes={size}", flush=True)
                                    next_progress += 64 * 1024 * 1024
                    if expected and size != expected:
                        raise ValueError(f"incomplete transfer: {size}/{expected}")
                    if not size:
                        raise ValueError("empty download")
                partial.replace(path)
                row.update(status="downloaded", bytes=size, sha256=h.hexdigest(), attempts=attempt)
                print(f"READY {acc} {name} bytes={size}", flush=True)
                break
            except Exception as exc:
                row.update(status="download_failed", error=f"{type(exc).__name__}: {exc}", attempts=attempt)
        result["downloads"].append(row)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    review = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
    accessions = [r["accession"] for r in review["records"] if r.get("matrix") is None]
    inventory_path = OUT / "supplementary_inventory.json"
    if inventory_path.exists():
        entries = json.loads(inventory_path.read_text(encoding="utf-8"))["studies"]
    else:
        entries = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for study in pool.map(inventory, accessions):
                entries.append(study)
                print(f"LIST {study['accession']} {study['status']} files={len(study['files'])}", flush=True)
        save("supplementary_inventory.json", {"created_at": datetime.now(timezone.utc).isoformat(), "studies": entries})
    if args.download:
        completed = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(download_study, study): study["accession"] for study in entries}
            for future in concurrent.futures.as_completed(futures):
                completed.append(future.result())
                save("download_manifest.json", {"updated_at": datetime.now(timezone.utc).isoformat(), "studies": completed})
        print(f"Completed downloads for {len(completed)} studies", flush=True)


if __name__ == "__main__":
    main()
