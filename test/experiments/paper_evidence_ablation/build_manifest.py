"""Freeze the series set for the paper-evidence ablation (stage B of PAPER_STRUCTURE_PLAN).

For every GEO series in the ExerGeneDB gold export:
  1. GSE -> PubMed IDs (NCBI E-utilities, db=gds esummary)
  2. PMID -> PMCID (NCBI PMC ID converter)
  3. Europe PMC JATS full text -> data/papers/<PMCID>.paper.json (tools.paper_structure)
  4. GEO metadata -> data/<GSE>/<GSE>_metadata.csv (download_geo_data, cached)

A series is eligible when all four succeed and the metadata overlaps the gold samples.
The manifest records hashes of the gold files, every paper JSON, and every metadata CSV,
so later arms can verify they read exactly the frozen inputs.

    python test/experiments/paper_evidence_ablation/build_manifest.py --n 24
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools import paper_structure as ps  # noqa: E402

GOLD_DIR = ROOT / "test" / "validation" / "exergenedb_gold"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
HEADERS = {"User-Agent": "mwangLab-agent (bioinformatics research)"}
SEED = 20261014


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def gse_to_pmids(accessions: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for i in range(0, len(accessions), 40):
        chunk = accessions[i:i + 40]
        term = " OR ".join(f"{a}[ACCN]" for a in chunk) + " AND gse[ETYP]"
        r = requests.get(f"{EUTILS}/esearch.fcgi", params={"db": "gds", "term": term, "retmax": 500,
                                                            "retmode": "json"}, headers=HEADERS, timeout=60)
        ids = r.json()["esearchresult"]["idlist"]
        time.sleep(0.4)
        if not ids:
            continue
        r = requests.post(f"{EUTILS}/esummary.fcgi", data={"db": "gds", "id": ",".join(ids), "retmode": "json"},
                          headers=HEADERS, timeout=60)
        res = r.json()["result"]
        for uid in res.get("uids", []):
            doc = res[uid]
            acc = doc.get("accession", "")
            if acc in chunk:
                out[acc] = [str(p) for p in doc.get("pubmedids", [])]
        time.sleep(0.4)
    return out


def pmids_to_pmcids(pmids: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i in range(0, len(pmids), 150):
        r = requests.get(IDCONV, params={"ids": ",".join(pmids[i:i + 150]), "format": "json",
                                         "tool": "mwanglab", "email": "noreply@example.org"},
                         headers=HEADERS, timeout=60)
        for rec in r.json().get("records", []):
            if rec.get("pmcid"):
                out[str(rec.get("pmid"))] = rec["pmcid"]
        time.sleep(0.4)
    return out


def ensure_paper(pmcid: str, paper_dir: Path) -> tuple[Path | None, str]:
    path = paper_dir / f"{pmcid}.paper.json"
    if path.exists():
        return path, "cached"
    xml, _url = ps.fetch_jats(pmcid)
    if not xml:
        return None, "no_oa_fulltext"
    doc = ps.parse_jats(xml, source=f"Europe PMC full-text XML ({pmcid})", fetched_url=_url)
    ps.save(doc, str(paper_dir), pmcid, raw_xml=xml)
    return path, "fetched"


def ensure_metadata(accession: str, data_dir: Path) -> tuple[Path | None, str]:
    path = data_dir / accession / f"{accession}_metadata.csv"
    if path.exists() and path.stat().st_size > 0:
        return path, "cached"
    from tools.geo_tools import download_geo_data
    args = {"geo_accession": accession, "base_dir": str(data_dir)}
    msg = download_geo_data.invoke(args) if hasattr(download_geo_data, "invoke") else download_geo_data(**args)
    if path.exists() and path.stat().st_size > 0:
        return path, "downloaded"
    return None, f"metadata_failed: {str(msg)[:160]}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=24, help="series to freeze (stratified by design class)")
    ap.add_argument("--out", default=str(Path(__file__).parent / "manifest.json"))
    ap.add_argument("--data-dir", default=str(ROOT / "data"))
    ap.add_argument("--paper-dir", default=str(ROOT / "data" / "papers"))
    a = ap.parse_args(argv)

    series = pd.read_csv(GOLD_DIR / "exergenedb_series.csv")
    series = series[series["is_geo_series"] == True]  # noqa: E712
    gold = pd.read_csv(GOLD_DIR / "exergenedb_samples.csv", dtype=str)
    accs = series["accession"].tolist()
    print(f"{len(accs)} GEO series in gold")

    pmids = gse_to_pmids(accs)
    all_pmids = sorted({p for v in pmids.values() for p in v})
    pmc = pmids_to_pmcids(all_pmids)
    print(f"with PMID: {sum(1 for v in pmids.values() if v)}; PMIDs with PMCID: {len(pmc)}")

    paper_dir, data_dir = Path(a.paper_dir), Path(a.data_dir)
    paper_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for rec in series.to_dict("records"):
        acc = rec["accession"]
        row = {"accession": acc, "design_class": rec["design_class"], "organism": rec["organism"],
               "seqtech": rec["seqtech"], "pmids": pmids.get(acc, [])}
        cands = [(p, pmc[p]) for p in row["pmids"] if p in pmc]
        if not row["pmids"]:
            row["status"] = "no_pmid"
        elif not cands:
            row["status"] = "no_pmcid"
        else:
            row["pmid"], row["pmcid"] = cands[0]
            ppath, pstat = ensure_paper(row["pmcid"], paper_dir)
            row["paper_status"] = pstat
            row["status"] = "no_oa_fulltext" if ppath is None else "paper_ok"
        rows.append(row)
        print(acc, row["status"], row.get("pmcid", ""))

    eligible_pool = [r for r in rows if r["status"] == "paper_ok"]
    # Stratified draw before downloading metadata, so the download budget stays small.
    rng = random.Random(SEED)
    by_class: dict[str, list[dict]] = {}
    for r in eligible_pool:
        by_class.setdefault(r["design_class"], []).append(r)
    for v in by_class.values():
        rng.shuffle(v)
    order: list[dict] = []
    while any(by_class.values()):  # round-robin over classes keeps every class represented
        for cls in sorted(by_class):
            if by_class[cls]:
                order.append(by_class[cls].pop())

    frozen = []
    for r in order:
        if len(frozen) >= a.n:
            break
        mpath, mstat = ensure_metadata(r["accession"], data_dir)
        r["metadata_status"] = mstat
        if mpath is None:
            r["status"] = "metadata_failed"
            continue
        meta = pd.read_csv(mpath, index_col=0)
        overlap = int(meta.index.astype(str).isin(gold.loc[gold["series_id"] == r["accession"], "sample_id"]).sum())
        if overlap == 0:
            r["status"] = "no_gold_overlap"
            continue
        r["status"] = "frozen"
        r["n_gold_overlap"] = overlap
        r["metadata_csv"] = str(mpath.relative_to(ROOT)).replace("\\", "/")
        r["metadata_sha256"] = sha256(mpath)
        pj = paper_dir / f"{r['pmcid']}.paper.json"
        r["paper_json"] = str(pj.relative_to(ROOT)).replace("\\", "/")
        r["paper_sha256"] = sha256(pj)
        frozen.append(r)

    manifest = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": SEED,
        "gold_samples_sha256": sha256(GOLD_DIR / "exergenedb_samples.csv"),
        "gold_series_sha256": sha256(GOLD_DIR / "exergenedb_series.csv"),
        "funnel": pd.Series([r["status"] for r in rows]).value_counts().to_dict(),
        "n_frozen": len(frozen),
        "frozen_design_classes": pd.Series([r["design_class"] for r in frozen]).value_counts().to_dict(),
        "series": frozen,
        "all_series": rows,
    }
    Path(a.out).write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("funnel", "n_frozen", "frozen_design_classes")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
