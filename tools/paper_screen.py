"""Paper screening: keep only papers whose deposited data can support a proper analysis.

Goal: filter at the input instead of at review time. A paper enters the analysis run only
when its full text is readable, it deposits its OWN data, the deposit is a supported data
type, the data files needed for that route exist, and the sample design has at least two
groups of three. Every paper gets one row with the verdict, the reason, and the evidence
(block IDs, file names, group sizes), so the loss at each layer can be counted.

Layers (each cheap enough to run on a few hundred papers; nothing here calls an LLM):

    1. text      full text via Europe PMC JATS, else the PDF (tools.pdf_markdown); own vs.
                 cited accessions from the section each one appears in
    2. deposit   GEO series summary (E-utilities esummary): data type, organism, sample
                 count, platform; non-GEO repositories (PRIDE, ArrayExpress, SRA-only,
                 GSA) are recorded and routed, not analysed
    3. files     GEO supplementary listing: raw counts vs. normalised-only vs. per-sample
                 tar vs. nothing (bulk RNA-seq only)
    4. design    GEO sample characteristics (series matrix): groups, smallest group, sex
                 column; uses metadata_structural's deterministic design-column picker

Verdicts: ``analyzable`` · ``needs_inspection`` (a layer could not decide, e.g. only a
``_RAW.tar``) · ``excluded`` with a reason code.

Network access goes through one ``Http`` object with an on-disk cache, so reruns are
free and tests inject canned responses.

CLI (repository root):

    python -m tools.paper_screen collect "exercise skeletal muscle" --out output/screen_run --max 200
    python -m tools.paper_screen screen output/screen_run/papers.csv --out output/screen_run
    python -m tools.paper_screen summary output/screen_run/screen.csv
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, field

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
GEO_SUPPL = "https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{gse}/suppl/"
GEO_MATRIX = "https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{gse}/matrix/"
S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
_UA = {"User-Agent": "mwangLab-paper-screen/1.0 (bioinformatics research)"}

# Section classes where a GSE mention usually means the paper's own deposit.
OWN_SECTIONS = {"methods", "data_availability", "supplementary", "other"}
CITED_SECTIONS = {"introduction", "discussion"}

_REPO_PATTERNS = {
    "geo": re.compile(r"\bGSE\d{3,}\b"),
    "pride": re.compile(r"\bPXD\d{6}\b"),
    "arrayexpress": re.compile(r"\bE-[A-Z]{4}-\d+\b"),
    "sra": re.compile(r"\b(?:PRJNA\d{3,}|PRJEB\d{3,}|SRP\d{4,})\b"),
    "gsa": re.compile(r"\b(?:CRA\d{6}|HRA\d{6}|PRJCA\d{6})\b"),
    "dbgap": re.compile(r"\bphs\d{6}\b"),
}
_ON_REQUEST = re.compile(r"(available|provided|obtained)\s+(from the corresponding author\s+)?"
                         r"(up)?on\s+(reasonable\s+)?request", re.I)

_GDSTYPE = (
    ("expression profiling by high throughput sequencing", "rnaseq"),
    ("expression profiling by array", "microarray"),
    ("methylation profiling", "methylation"),
    ("non-coding rna profiling by high throughput sequencing", "ncrna_seq"),
    ("non-coding rna profiling by array", "ncrna_array"),
    ("genome binding/occupancy", "chromatin"),
    ("genome variation", "genome_variation"),
    ("protein profiling", "proteomics"),
)
_SINGLE_CELL = re.compile(r"single[- ]?(cell|nucle(us|i))|scRNA|snRNA|10x genomics|chromium|drop-?seq", re.I)

# Supplementary file names.
_RAW_COUNT_NAME = re.compile(
    r"(raw[._ -]?counts?|read[._ -]?counts?|counts?[._ -]?(matrix|table)|featurecounts?|htseq|"
    r"gene[._ -]?counts?|_counts?\.|\bcounts?\b|expected[._ -]?count|umi[._ -]?counts?)", re.I)
_NORMALISED_NAME = re.compile(r"(fpkm|rpkm|tpm|cpm|normali[sz]ed|norm[._]|vst|rlog|log2|abundance)", re.I)
_MATRIX_EXT = re.compile(r"\.(csv|tsv|txt|xlsx?|tab)(\.gz)?$", re.I)


# ---------------------------------------------------------------------------
# HTTP with an on-disk cache
# ---------------------------------------------------------------------------

class Http:
    """GET with retries, NCBI rate limiting, and a response cache keyed by URL+params."""

    def __init__(self, cache_dir: str = "", api_key: str = "", min_interval: float = 0.0):
        self.cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        self.api_key = api_key or os.getenv("NCBI_API_KEY", "")
        self.min_interval = min_interval or (0.11 if self.api_key else 0.35)
        self._last = 0.0

    def _key(self, url: str, params: dict | None) -> str:
        raw = url + "?" + json.dumps(params or {}, sort_keys=True)
        return os.path.join(self.cache_dir, hashlib.sha1(raw.encode()).hexdigest()[:20])

    def get(self, url: str, params: dict | None = None, binary: bool = False, timeout: int = 60):
        """Body (str, or bytes when binary) or None on 404 / repeated failure."""
        params = dict(params or {})
        if url.startswith(EUTILS) and self.api_key:
            params["api_key"] = self.api_key
        path = self._key(url, {k: v for k, v in params.items() if k != "api_key"}) if self.cache_dir else ""
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read()
            if data == b"\x00404":
                return None
            return data if binary else data.decode("utf-8", errors="replace")
        import requests
        data = None
        for attempt in range(4):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                r = requests.get(url, params=params, headers=_UA, timeout=timeout)
            except Exception:
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 404:
                data = b"\x00404"
                break
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** (attempt + 1))
                continue
            r.raise_for_status()
            data = r.content
            break
        if data is None:
            return None
        if path:
            with open(path, "wb") as f:
                f.write(data)
        if data == b"\x00404":
            return None
        return data if binary else data.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Layer 1: own vs cited accessions from structured full text
# ---------------------------------------------------------------------------

def deposits_from_doc(doc: dict) -> dict:
    """Accessions the paper deposits, from a structured paper (tools.paper_structure).

    A GEO series counts as the paper's own when it is mentioned in Methods, the data
    availability statement, supplementary material or front matter. One that appears only
    in the Introduction or Discussion is a citation. Returns
    ``{"own": {repo: [ids]}, "cited": [GSE...], "evidence": {id: [block ids]},
    "on_request": bool}``.
    """
    by_id = {b["id"]: b for b in doc.get("blocks", [])}
    where: dict[str, set] = {}
    evidence: dict[str, list] = {}
    on_request = False
    for b in doc.get("blocks", []):
        cls = b.get("section_class", "other")
        for repo, pat in _REPO_PATTERNS.items():
            for acc in dict.fromkeys(pat.findall(b["text"])):
                where.setdefault(acc, set()).add(cls)
                evidence.setdefault(acc, []).append(b["id"])
        if cls in ("data_availability", "methods") and _ON_REQUEST.search(b["text"]):
            on_request = True
    own: dict[str, list] = {}
    cited = []
    for acc, classes in where.items():
        repo = next(r for r, p in _REPO_PATTERNS.items() if p.fullmatch(acc))
        if classes & OWN_SECTIONS or not classes <= CITED_SECTIONS:
            # A Results mention of a GSE is ambiguous; keep it as own only when no
            # citation phrase surrounds it (handled by ownership_hint below).
            if classes <= {"results"} and _cited_phrase(acc, evidence[acc], by_id):
                cited.append(acc)
                continue
            own.setdefault(repo, []).append(acc)
        else:
            cited.append(acc)
    return {"own": own, "cited": cited, "evidence": evidence, "on_request": on_request}


_CITED_NEAR = re.compile(r"(downloaded|obtained|retrieved|publicly available|previously (published|"
                         r"reported|described)|re-?analy[sz]|from (a|the) (previous|published))", re.I)


def _cited_phrase(acc: str, block_ids: list, by_id: dict) -> bool:
    for bid in block_ids:
        text = by_id[bid]["text"]
        i = text.find(acc)
        if i >= 0 and _CITED_NEAR.search(text[max(0, i - 200): i + 60]):
            return True
    return False


# ---------------------------------------------------------------------------
# Layer 2: GEO series summary
# ---------------------------------------------------------------------------

def geo_stub(gse: str) -> str:
    n = gse[3:]
    return f"GSE{n[:-3]}nnn" if len(n) > 3 else "GSEnnn"


def classify_gdstype(gdstype: str, text: str = "") -> str:
    """Data type for routing; several types joined by '+' (e.g. 'rnaseq+chromatin')."""
    low = (gdstype or "").lower()
    kinds = [k for phrase, k in _GDSTYPE if phrase in low]
    if "rnaseq" in kinds and _SINGLE_CELL.search(text or ""):
        kinds[kinds.index("rnaseq")] = "scrnaseq"
    return "+".join(dict.fromkeys(kinds)) or ("other" if low else "unknown")


def geo_summary(gse: str, http: Http) -> dict | None:
    """esummary fields for one GSE, or None when GEO has no such public series."""
    s = http.get(f"{EUTILS}/esearch.fcgi", {"db": "gds", "term": f"{gse}[ACCN] AND gse[ETYP]",
                                               "retmode": "json"})
    try:
        ids = json.loads(s)["esearchresult"]["idlist"] if s else []
    except (ValueError, KeyError):
        ids = []
    if not ids:
        return None
    s = http.get(f"{EUTILS}/esummary.fcgi", {"db": "gds", "id": ids[0], "retmode": "json"})
    try:
        rec = json.loads(s)["result"][ids[0]]
    except (ValueError, KeyError, TypeError):
        return None
    text = " ".join(str(rec.get(k, "")) for k in ("title", "summary"))
    return {
        "gse": gse,
        "title": rec.get("title", ""),
        "gdstype": rec.get("gdstype", ""),
        "data_type": classify_gdstype(rec.get("gdstype", ""), text),
        "taxon": rec.get("taxon", ""),
        "n_samples": int(rec.get("n_samples") or 0),
        "platforms": rec.get("gpl", ""),
        "suppfile": rec.get("suppfile", ""),
        "sample_titles": [x.get("title", "") for x in rec.get("samples", []) or []],
    }


# ---------------------------------------------------------------------------
# Layer 3: supplementary files (bulk RNA-seq)
# ---------------------------------------------------------------------------

def list_geo_dir(url: str, http: Http) -> list[str]:
    html = http.get(url)
    if not html:
        return []
    names = re.findall(r'href="([^"?/][^"]*)"', html)
    return [n for n in dict.fromkeys(names) if not n.startswith(("http", "/", "?"))]


def classify_supplementary(names: list[str]) -> dict:
    """What the supplementary files offer for a count-based analysis.

    status: ``raw_counts`` (a file named like a count matrix), ``raw_tar`` (only a
    per-sample ``_RAW.tar``; its members may be counts or FPKM and need inspection),
    ``normalized_only`` (FPKM/TPM/normalised files only), ``none``.
    """
    names = [n for n in names if n.lower() not in ("filelist.txt",)]
    raw = [n for n in names if _MATRIX_EXT.search(n) and _RAW_COUNT_NAME.search(n)
           and not _NORMALISED_NAME.search(n)]
    norm = [n for n in names if _MATRIX_EXT.search(n) and _NORMALISED_NAME.search(n)]
    tar = [n for n in names if n.lower().endswith("_raw.tar")]
    other = [n for n in names if _MATRIX_EXT.search(n) and n not in raw and n not in norm]
    if raw:
        status = "raw_counts"
    elif tar:
        status = "raw_tar"
    elif norm:
        status = "normalized_only"
    elif other:
        status = "unlabelled_matrix"
    else:
        status = "none"
    return {"status": status, "raw": raw, "normalized": norm, "tar": tar, "other": other}


# ---------------------------------------------------------------------------
# Layer 4: sample design from the series matrix header
# ---------------------------------------------------------------------------

def parse_series_matrix_samples(text: str):
    """Sample table (pandas DataFrame) from the ``!Sample_`` header lines of a series matrix."""
    import pandas as pd
    cols: dict[str, list] = {}
    char_n: Counter = Counter()
    for line in text.splitlines():
        if line.startswith("!series_matrix_table_begin"):
            break
        if not line.startswith("!Sample_"):
            continue
        parts = next(csv.reader([line], delimiter="\t"))
        key, vals = parts[0][len("!Sample_"):], [v.strip() for v in parts[1:]]
        if key == "characteristics_ch1":
            # "tissue: muscle" -> column characteristics_ch1.<i>.tissue
            label = next((v.split(":", 1)[0].strip() for v in vals if ":" in v), "")
            char_n[key] += 1
            key = f"characteristics_ch1.{char_n[key]}.{label}" if label else f"{key}.{char_n[key]}"
            vals = [v.split(":", 1)[1].strip() if ":" in v else v for v in vals]
        elif key in cols:
            continue
        cols[key] = vals
    if not cols:
        return pd.DataFrame()
    n = max(len(v) for v in cols.values())
    return pd.DataFrame({k: v + [""] * (n - len(v)) for k, v in cols.items()})


def design_from_samples(df) -> dict:
    """Groups and the smallest group size, using metadata_structural's design-column picker
    (falls back to sample titles that differ only by a replicate number)."""
    from tools import metadata_structural as ms
    if df is None or df.empty:
        return {"status": "no_metadata"}
    exclude = {c for c in df.columns if c in ("geo_accession", "title")}
    col = ms._pick_design_column(df, exclude)
    if col is not None:
        series = df[col].astype(str)
        source = col
    else:
        series = ms._title_design_series(df, "title" if "title" in df.columns else None)
        source = "title"
    sex_col = next((c for c in df.columns if re.search(r"\b(sex|gender)\b", str(c), re.I)), "")
    sexes = sorted(set(df[sex_col].astype(str).str.lower())) if sex_col else []
    if series is None:
        return {"status": "single_group", "n_samples": len(df), "sex_column": sex_col, "sexes": sexes}
    sizes = series.value_counts()
    return {
        "status": "ok" if int(sizes.min()) >= 3 else "group_too_small",
        "design_column": source,
        "groups": {str(k): int(v) for k, v in sizes.items()},
        "min_group": int(sizes.min()),
        "n_samples": len(df),
        "sex_column": sex_col,
        "sexes": sexes,
    }


def geo_design(gse: str, http: Http) -> dict:
    stub = geo_stub(gse)
    files = [n for n in list_geo_dir(GEO_MATRIX.format(stub=stub, gse=gse), http)
             if n.endswith("_series_matrix.txt.gz")]
    if not files:
        return {"status": "no_series_matrix"}
    raw = http.get(GEO_MATRIX.format(stub=stub, gse=gse) + files[0], binary=True, timeout=120)
    if not raw:
        return {"status": "no_series_matrix"}
    # Only the header is needed; stop decompressing at the data table.
    head = []
    with gzip.open(io.BytesIO(raw), "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                break
            head.append(line)
    out = design_from_samples(parse_series_matrix_samples("".join(head)))
    out["matrix_files"] = len(files)
    return out


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

SUPPORTED_ROUTES = {"rnaseq"}   # raw-count-only run; widen to route other data types


@dataclass
class Screen:
    paper_id: str
    title: str = ""
    pmcid: str = ""
    doi: str = ""
    text_source: str = ""
    own_gse: list = field(default_factory=list)
    other_repos: dict = field(default_factory=dict)
    cited_gse: list = field(default_factory=list)
    evidence: dict = field(default_factory=dict)
    series: list = field(default_factory=list)
    data_types: str = ""
    verdict: str = ""
    reason: str = ""
    analyzable_gse: list = field(default_factory=list)

    def row(self) -> dict:
        return {
            "paper_id": self.paper_id, "title": self.title, "pmcid": self.pmcid, "doi": self.doi,
            "verdict": self.verdict, "reason": self.reason,
            "analyzable_gse": ";".join(self.analyzable_gse), "data_types": self.data_types,
            "own_gse": ";".join(self.own_gse), "cited_gse": ";".join(self.cited_gse),
            "other_repos": ";".join(f"{k}:{','.join(v)}" for k, v in self.other_repos.items()),
            "text_source": self.text_source,
            "series_json": json.dumps(self.series, ensure_ascii=False),
            "evidence_json": json.dumps(self.evidence, ensure_ascii=False),
        }


# Order matters: the reason recorded for a paper is the earliest layer it fails.
REASONS = (
    "no_full_text", "no_own_deposit", "data_on_request", "non_geo_repository",
    "geo_not_public", "unsupported_data_type", "no_processed_matrix", "normalized_only",
    "single_group", "group_too_small",
)


def judge_series(info: dict | None, files: dict | None, design: dict | None,
                 routes: set = SUPPORTED_ROUTES) -> tuple[str, str]:
    """(verdict, reason) for one GSE."""
    if info is None:
        return "excluded", "geo_not_public"
    if not set(info["data_type"].split("+")) & routes:
        return "excluded", f"unsupported_data_type:{info['data_type']}"
    if files is not None:
        st = files["status"]
        if st == "none":
            return "excluded", "no_processed_matrix"
        if st == "normalized_only":
            return "excluded", "normalized_only"
    if design is not None:
        ds = design.get("status")
        if ds == "single_group":
            return "excluded", "single_group"
        if ds == "group_too_small":
            return "excluded", "group_too_small"
    if files is not None and files["status"] in ("raw_tar", "unlabelled_matrix"):
        return "needs_inspection", f"matrix_{files['status']}"
    if design is not None and design.get("status") not in ("ok",):
        return "needs_inspection", f"design_{design.get('status')}"
    return "analyzable", ""


def screen_paper(row: dict, doc: dict | None, http: Http | None, check_files: bool = True,
                 check_design: bool = True, routes: set = SUPPORTED_ROUTES) -> Screen:
    """Screen one paper. ``doc`` is its structured full text (None when unavailable)."""
    s = Screen(paper_id=row.get("paper_id") or row.get("paperId") or row.get("pmcid") or row.get("doi", ""),
               title=row.get("title", ""), pmcid=row.get("pmcid", ""), doi=row.get("doi", ""))
    if not doc or not doc.get("blocks"):
        s.verdict, s.reason = "excluded", "no_full_text"
        return s
    s.text_source = doc.get("structure_quality", "")
    dep = deposits_from_doc(doc)
    s.own_gse = dep["own"].get("geo", [])
    s.other_repos = {k: v for k, v in dep["own"].items() if k != "geo"}
    s.cited_gse = dep["cited"]
    s.evidence = {k: v[:4] for k, v in dep["evidence"].items()}
    if not s.own_gse:
        if s.other_repos:
            s.verdict, s.reason = "excluded", "non_geo_repository:" + ",".join(sorted(s.other_repos))
        elif dep["on_request"]:
            s.verdict, s.reason = "excluded", "data_on_request"
        else:
            s.verdict, s.reason = "excluded", "no_own_deposit"
        return s
    results = []
    types = []
    for gse in s.own_gse:
        info = geo_summary(gse, http) if http else None
        files = design = None
        if info and set(info["data_type"].split("+")) & routes:
            if check_files:
                files = classify_supplementary(list_geo_dir(GEO_SUPPL.format(stub=geo_stub(gse), gse=gse), http))
            if check_design:
                design = geo_design(gse, http)
        verdict, reason = judge_series(info, files, design, routes)
        types.append(info["data_type"] if info else "not_public")
        results.append({"gse": gse, "verdict": verdict, "reason": reason,
                        "data_type": info["data_type"] if info else "", "taxon": info["taxon"] if info else "",
                        "n_samples": info["n_samples"] if info else 0,
                        "files": files, "design": design})
    s.series = results
    s.data_types = ";".join(dict.fromkeys(types))
    s.analyzable_gse = [r["gse"] for r in results if r["verdict"] == "analyzable"]
    if s.analyzable_gse:
        s.verdict, s.reason = "analyzable", ""
    elif any(r["verdict"] == "needs_inspection" for r in results):
        s.verdict = "needs_inspection"
        s.reason = next(r["reason"] for r in results if r["verdict"] == "needs_inspection")
    else:
        s.verdict = "excluded"
        # Report the reason that got furthest through the layers.
        rank = {r: i for i, r in enumerate(REASONS)}
        s.reason = max((r["reason"] for r in results), key=lambda x: rank.get(x.split(":")[0], -1))
    return s


# ---------------------------------------------------------------------------
# Paper collection (Semantic Scholar + PubMed) and full-text loading
# ---------------------------------------------------------------------------

def collect_papers(query: str, http: Http, max_papers: int = 200, end_year: int = 0) -> list[dict]:
    """Relevance-ranked open-access papers from Semantic Scholar, merged with PubMed hits
    that have a PMC full text. Deduplicated by DOI, then PMID, then title."""
    rows: list[dict] = []
    offset = 0
    while len(rows) < max_papers and offset < 1000:
        params = {"query": query, "fields": "title,abstract,year,externalIds,openAccessPdf",
                  "limit": min(100, max_papers - len(rows)), "offset": offset,
                  "fieldsOfStudy": "Medicine,Biology"}
        if end_year:
            params["year"] = f"-{end_year}"
        s = http.get(S2_SEARCH + "?openAccessPdf", params)
        data = (json.loads(s).get("data") or []) if s else []
        if not data:
            break
        for p in data:
            ext = p.get("externalIds") or {}
            rows.append({"paper_id": p.get("paperId", ""), "source": "semantic_scholar",
                         "title": (p.get("title") or "").strip(), "year": p.get("year") or "",
                         "doi": (ext.get("DOI") or "").lower(), "pmid": str(ext.get("PubMed") or ""),
                         "pmcid": _pmcid(ext.get("PubMedCentral", "")),
                         "pdf_url": (p.get("openAccessPdf") or {}).get("url", "")})
        offset += len(data)
    term = f"({query}) AND free full text[sb]"
    s = http.get(f"{EUTILS}/esearch.fcgi", {"db": "pubmed", "term": term, "retmax": max_papers,
                                               "sort": "relevance", "retmode": "json"})
    pmids = json.loads(s)["esearchresult"]["idlist"] if s else []
    for i in range(0, len(pmids), 200):
        s = http.get(f"{EUTILS}/esummary.fcgi", {"db": "pubmed", "id": ",".join(pmids[i:i + 200]),
                                                    "retmode": "json"})
        res = json.loads(s).get("result", {}) if s else {}
        for pid in res.get("uids", []):
            r = res[pid]
            ids = {a.get("idtype"): a.get("value", "") for a in r.get("articleids", [])}
            rows.append({"paper_id": f"PMID{pid}", "source": "pubmed", "title": r.get("title", "").strip(),
                         "year": (r.get("pubdate") or "")[:4], "doi": ids.get("doi", "").lower(),
                         "pmid": pid, "pmcid": _pmcid(ids.get("pmc", "")), "pdf_url": ""})
    seen, out = set(), []
    for r in rows:
        keys = [k for k in (r["doi"] and "doi:" + r["doi"], r["pmid"] and "pmid:" + r["pmid"],
                            "t:" + re.sub(r"\W+", "", r["title"].lower())[:80]) if k]
        if any(k in seen for k in keys):
            continue
        seen.update(keys)
        out.append(r)
    return out


def _pmcid(v) -> str:
    v = str(v or "").strip().upper()
    return v if v.startswith("PMC") else (f"PMC{v}" if v.isdigit() else "")


def load_full_text(row: dict, papers_dir: str, http: Http) -> dict | None:
    """Structured full text: cached .paper.json, else Europe PMC JATS, else the PDF."""
    from tools import paper_structure as ps
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", row.get("pmcid") or row.get("paper_id") or "paper")
    cached = os.path.join(papers_dir, f"{stem}.paper.json")
    if os.path.exists(cached):
        return ps.load(cached)
    if row.get("pmcid"):
        xml = http.get(ps.EPMC_FULLTEXT.format(pmcid=row["pmcid"]), binary=True)
        if xml and b"<article" in xml[:5000]:
            doc = ps.parse_jats(xml, source=f"Europe PMC full-text XML ({row['pmcid']})")
            ps.save(doc, papers_dir, stem, raw_xml=xml)
            return doc
    if row.get("pdf_url"):
        pdf = http.get(row["pdf_url"], binary=True, timeout=120)
        if pdf and pdf[:5] == b"%PDF-":
            from tools import pdf_markdown
            os.makedirs(papers_dir, exist_ok=True)
            pdf_path = os.path.join(papers_dir, f"{stem}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf)
            doc, _ = pdf_markdown.save_pdf(pdf_path, papers_dir, stem, fetched_url=row["pdf_url"])
            return doc
    return None


# ---------------------------------------------------------------------------
# Batch + summary
# ---------------------------------------------------------------------------

FIELDS = ["paper_id", "title", "pmcid", "doi", "verdict", "reason", "analyzable_gse", "data_types",
          "own_gse", "cited_gse", "other_repos", "text_source", "series_json", "evidence_json"]


def screen_file(papers_csv: str, out_dir: str, limit: int = 0, check_design: bool = True,
                routes: set = SUPPORTED_ROUTES) -> str:
    os.makedirs(out_dir, exist_ok=True)
    http = Http(cache_dir=os.path.join(out_dir, "_http_cache"))
    with open(papers_csv, encoding="utf-8") as f:
        papers = list(csv.DictReader(f))
    if limit:
        papers = papers[:limit]
    out_csv = os.path.join(out_dir, "screen.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for i, row in enumerate(papers, 1):
            try:
                doc = load_full_text(row, os.path.join(out_dir, "papers"), http)
                s = screen_paper(row, doc, http, check_design=check_design, routes=routes)
            except Exception as e:  # one bad paper never stops the batch
                s = Screen(paper_id=row.get("paper_id", ""), title=row.get("title", ""),
                           verdict="needs_inspection", reason=f"error:{type(e).__name__}: {e}"[:200])
            w.writerow(s.row())
            f.flush()
            print(f"[{i}/{len(papers)}] {s.verdict:16} {s.reason[:40]:40} {s.title[:60]}")
    summary = summarize(out_csv)
    with open(os.path.join(out_dir, "screen_summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)
    return out_csv


def summarize(screen_csv: str) -> str:
    with open(screen_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    verdicts = Counter(r["verdict"] for r in rows)
    reasons = Counter(r["reason"].split(":")[0] for r in rows if r["verdict"] == "excluded")
    types = Counter(t for r in rows for t in r["data_types"].split(";") if t)
    lines = [f"# Paper screening summary ({n} papers)", "", "| Verdict | Papers |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in verdicts.most_common()]
    lines += ["", "## Why papers were excluded (first failing layer)", "", "| Reason | Papers |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k in REASONS for v in [reasons.get(k, 0)] if v]
    lines += [f"| {k} | {v} |" for k, v in reasons.items() if k not in REASONS]
    lines += ["", "## Data types of the papers' own GEO series", "", "| Data type | Papers |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in types.most_common()]
    return "\n".join(lines) + "\n"


def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.paper_screen", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("collect", help="search Semantic Scholar + PubMed, write papers.csv")
    p.add_argument("query")
    p.add_argument("--out", required=True)
    p.add_argument("--max", type=int, default=200)
    p.add_argument("--end-year", type=int, default=0)
    p = sub.add_parser("screen", help="screen a papers.csv, write screen.csv + screen_summary.md")
    p.add_argument("papers_csv")
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--no-design", action="store_true", help="skip the series-matrix design layer")
    p.add_argument("--routes", default="rnaseq", help="comma-separated supported data types")
    p = sub.add_parser("summary")
    p.add_argument("screen_csv")
    a = ap.parse_args(argv)
    if a.cmd == "collect":
        os.makedirs(a.out, exist_ok=True)
        rows = collect_papers(a.query, Http(cache_dir=os.path.join(a.out, "_http_cache")), a.max, a.end_year)
        path = os.path.join(a.out, "papers.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["paper_id"])
            w.writeheader()
            w.writerows(rows)
        print(f"{len(rows)} papers -> {path}")
    elif a.cmd == "screen":
        out = screen_file(a.papers_csv, a.out, a.limit, not a.no_design, set(a.routes.split(",")))
        print(open(os.path.join(a.out, "screen_summary.md"), encoding="utf-8").read())
        print(out)
    else:
        print(summarize(a.screen_csv))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    sys.exit(_main())
