"""Agent A (Study Curation) paper-discovery tools.

Entry point of the paper-first workflow: given a keyword, query the Semantic
Scholar Academic Graph API for open-access papers, returning a curated triage
list (mirrors the search_geo_studies pattern). Does NOT download PDFs — that is
the job of a later stage (fetch_paper_text).

The website filter URL
  https://www.semanticscholar.org/search?fos[0]=medicine&fos[1]=biology&q=exercise&sort=relevance&pdf=true
maps to the API as:
  query=exercise & fieldsOfStudy=Medicine,Biology & openAccessPdf (flag) & sort=relevance(default)
"""

import glob
import hashlib
import io
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime

import pandas as pd
import requests
from langchain_core.tools import tool


_S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"

# Cache of the most recent search_papers result (ranked list of row dicts), so
# fetch_paper_text can resolve a stable [#N] handle to the EXACT pmcid/pdf_url.
# The LLM reliably corrupts 8-digit PMCIDs when retyping them into a tool call
# (observed: it picked the right paper by title but mutated PMC12248044 → PMC11906498,
# silently fetching an unrelated neuroscience paper). Passing an index it cannot
# mistype, and looking the id up here, removes that whole failure mode.
_LAST_SEARCH_ROWS = []


def _search_row_by_index(idx: int):
    """Return the cached search row at 1-based idx, or None if out of range."""
    if isinstance(idx, int) and 1 <= idx <= len(_LAST_SEARCH_ROWS):
        return _LAST_SEARCH_ROWS[idx - 1]
    return None


def _pmcid_in_last_search(pmcid: str) -> bool:
    """True if pmcid matches a hit in the most recent search (normalized compare)."""
    norm = _normalize_pmcid(pmcid)
    return bool(norm) and any(_normalize_pmcid(r.get("pmcid")) == norm for r in _LAST_SEARCH_ROWS)

# Abstract terms that hint the study generated sequencing/expression data worth
# chasing for a repository accession. Used only as a soft ranking signal — the
# definitive check is regex-ing the full PDF text for a GSE accession downstream.
_SEQ_SIGNAL_TERMS = (
    "rna-seq", "rna seq", "rnaseq", "transcriptom", "sequencing",
    "scrna", "single-cell", "single cell", "bulk rna",
    "geo", "deposited", "accession", "differential expression",
)

# GEO series accession, e.g. GSE266241. Word-bounded to avoid matching inside
# longer tokens.
_GSE_PATTERN = re.compile(r"\bGSE\d{3,}\b")

# Europe PMC serves open-access full text as JATS XML with no auth and (unlike publisher
# PDFs behind Cloudflare) rarely 403s — the reliable bridge from a paper to its accessions.
_EPMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
_HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (mwangLab-agent; bioinformatics research)"}


def _normalize_pmcid(value) -> str:
    """Return a canonical 'PMC<digits>' id, or '' if value isn't a PMC id.

    Semantic Scholar's externalIds.PubMedCentral is a bare number (e.g. '12181168'),
    which pandas later round-trips as a float ('12181168.0'). Both forms — and an
    already-prefixed 'PMC12181168' — normalize here so Europe PMC URLs are well-formed.
    """
    s = str(value or "").strip()
    if not s or s.lower() == "nan":
        return ""
    if s.upper().startswith("PMC"):
        s = s[3:]
    s = s.split(".")[0]  # drop a trailing '.0' from a float round-trip
    return f"PMC{s}" if s.isdigit() else ""


def _fetch_europepmc_text(pmcid: str):
    """Fetch an open-access article's full text as plain text from Europe PMC.

    Returns (text, url). text is '' when the article isn't in Europe PMC's OA full-text
    set (404) or the XML won't parse. The JATS XML includes the Data Availability section
    where GEO/SRA accessions are stated, so GSE hit-rate is far higher than scraping PDFs.
    """
    norm = _normalize_pmcid(pmcid)
    url = _EPMC_FULLTEXT.format(pmcid=norm) if norm else ""
    if not norm:
        return "", url
    try:
        r = requests.get(url, headers=_HTTP_HEADERS, timeout=60)
        if r.status_code != 200 or not r.content.strip():
            return "", url
        root = ET.fromstring(r.content)
        text = " ".join(t for t in root.itertext() if t and t.strip())
        return (text if text.strip() else ""), url
    except Exception:
        return "", url


@tool
def search_papers(
    keyword: str,
    fields_of_study: str = "Medicine,Biology",
    require_pdf: bool = True,
    max_results: int = 30,
    min_year: int = 0,
    output_dir: str = "./output",
) -> str:
    """
    Search Semantic Scholar for open-access papers matching a keyword, returning a
    curated triage list suitable for the paper-first curation workflow. Does NOT
    download any PDF — only metadata + abstract.

    Use this as the first step of Agent A: find candidate papers, then hand the
    open-access PDF URLs to a text-extraction step to locate the data accession
    (e.g. a GEO GSE id) the paper deposited.

    Args:
        keyword: Free-text query (e.g. 'exercise', 'endurance training muscle').
        fields_of_study: Comma-separated Semantic Scholar fields of study to
            restrict to (e.g. 'Medicine,Biology'). Pass '' to skip the filter.
        require_pdf: If True (default), only return papers with a public
            open-access PDF (the website's pdf=true filter).
        min_year: If > 0, drop papers published before this year.
        max_results: Cap on papers to fetch (API max per page is 100).
        output_dir: Directory where the result CSV is written.
    """
    try:
        params = {
            "query": keyword,
            "fields": "title,abstract,year,externalIds,openAccessPdf",
            "limit": max(1, min(max_results, 100)),
        }
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study

        # openAccessPdf is a valueless flag param; prefix it on the URL so requests
        # appends the rest with '&' (matches the tested ?openAccessPdf&query=... form).
        url = f"{_S2_SEARCH}?openAccessPdf" if require_pdf else _S2_SEARCH

        api_key = os.getenv("S2_API_KEY")
        headers = {"x-api-key": api_key} if api_key else {}

        print(f"Searching Semantic Scholar: query='{keyword}' fos='{fields_of_study}' pdf={require_pdf}")
        # The shared unauthenticated S2 pool 429s often; back off and retry in-process so the
        # agent isn't stalled at step 1 (it has no delay between its own guarded retries).
        r = None
        for attempt in range(1, 5):
            r = requests.get(url, params=params, headers=headers, timeout=30)
            if r.status_code != 429:
                break
            if attempt < 4:
                wait = 20 * attempt  # 20s, 40s, 60s
                print(f"  S2 rate limit (429); waiting {wait}s and retrying ({attempt}/4)...")
                time.sleep(wait)
        if r.status_code == 429:
            return ("Semantic Scholar rate limit hit (429) after retries. The shared unauthenticated "
                    "pool is throttled. Wait a minute and retry, or set S2_API_KEY in .env for higher "
                    "limits (apply at https://www.semanticscholar.org/product/api#api-key-form).")
        r.raise_for_status()
        payload = r.json()
        total = payload.get("total", 0)
        data = payload.get("data", []) or []
        if not data:
            return f"No open-access papers found for '{keyword}' (fields_of_study={fields_of_study})."

        rows = []
        for p in data:
            year = p.get("year") or 0
            if min_year and year and year < min_year:
                continue
            ext = p.get("externalIds") or {}
            oa = p.get("openAccessPdf") or {}
            abstract = (p.get("abstract") or "").strip()
            abs_low = abstract.lower()
            gse_hits = sorted(set(_GSE_PATTERN.findall(abstract)))
            rows.append({
                "paperId": p.get("paperId", ""),
                "title": (p.get("title") or "").strip(),
                "year": year,
                "doi": ext.get("DOI", ""),
                "pmid": ext.get("PubMed", ""),
                "pmcid": _normalize_pmcid(ext.get("PubMedCentral", "")),
                "pdf_url": oa.get("url", ""),
                "pdf_status": oa.get("status", ""),
                "has_seq_signal": any(t in abs_low for t in _SEQ_SIGNAL_TERMS),
                "geo_in_abstract": ";".join(gse_hits),
                "abstract": abstract[:400],
            })

        if not rows:
            return (f"Search matched {total} papers but none passed the min_year={min_year} filter "
                    f"in the first {len(data)} results.")

        # Triage order: papers that already expose a GSE in the abstract first,
        # then those with a sequencing-data signal, then most recent.
        rows.sort(key=lambda d: (not d["geo_in_abstract"], not d["has_seq_signal"], -(d["year"] or 0)))

        # Stable 1-based handle per hit. fetch_paper_text(search_index=N) resolves it
        # to the exact pmcid below — the LLM never has to retype the id.
        for i, r in enumerate(rows, 1):
            r["idx"] = i
        global _LAST_SEARCH_ROWS
        _LAST_SEARCH_ROWS = rows

        os.makedirs(output_dir, exist_ok=True)
        safe_kw = "".join(c if c.isalnum() else "_" for c in keyword).strip("_")
        out_path = os.path.join(output_dir, f"paper_search_{safe_kw}.csv")
        df = pd.DataFrame(rows)
        df = df[["idx"] + [c for c in df.columns if c != "idx"]]  # idx first for readability
        df.to_csv(out_path, index=False)

        n_signal = sum(1 for r in rows if r["has_seq_signal"])
        n_gse = sum(1 for r in rows if r["geo_in_abstract"])
        lines = [
            f"Found {len(rows)} open-access papers for '{keyword}' "
            f"(total matched on Semantic Scholar: {total}; fields_of_study={fields_of_study}).",
            f"{n_signal}/{len(rows)} mention sequencing/expression data in the abstract; "
            f"{n_gse} expose a GEO GSE id directly in the abstract.",
            "",
            f"### Top {min(10, len(rows))} hits (sorted by GSE-in-abstract, then seq-signal, then year):",
        ]
        for r in rows[:10]:
            flags = []
            if r["geo_in_abstract"]:
                flags.append(f"GEO={r['geo_in_abstract']}")
            elif r["has_seq_signal"]:
                flags.append("[seq-signal]")
            else:
                flags.append("[no-signal]")
            src = r["pmcid"] if r["pmcid"] else ("pdf-only" if r["pdf_url"] else "no-source")
            lines.append(f"- [#{r['idx']}] {r['title'][:80]} ({r['year']}) | {' '.join(flags)} | {src}")
        lines.append("")
        lines.append("To read a hit, call fetch_paper_text(search_index=N) with its [#N] number — the tool "
                     "looks up the exact PMCID/PDF for that hit. Do NOT retype a PMCID into the call.")
        lines.append(f"Full result table saved to: {out_path}")
        return "\n".join(lines)

    except Exception as e:
        return f"Paper search failed. Error: {type(e).__name__}: {e}"


# Data-repository accession patterns. GEO series is the actionable one (the existing
# pipeline downloads GEO); SRA/ArrayExpress are reported but not yet auto-fetched.
_ACCESSION_PATTERNS = {
    "GEO_series": re.compile(r"\bGSE\d{3,}\b"),
    "SRA_study": re.compile(r"\b(?:SRP\d{4,}|PRJNA\d{4,}|PRJEB\d{4,}|PRJDB\d{4,})\b"),
    "ArrayExpress": re.compile(r"\bE-(?:MTAB|GEOD|MEXP)-\d+\b"),
}


def _extract_accessions(text: str) -> dict:
    """Return {repository_kind: [unique accession ids]} found anywhere in text."""
    out = {}
    for kind, pat in _ACCESSION_PATTERNS.items():
        hits = sorted(set(pat.findall(text)))
        if hits:
            out[kind] = hits
    return out


def _context_for(text: str, token: str, width: int = 110) -> str:
    """Return a whitespace-collapsed snippet around the first occurrence of token.
    Helps a human/agent judge whether the accession is the paper's OWN deposited
    data vs. a citation of another study's data."""
    i = text.find(token)
    if i < 0:
        return ""
    s, e = max(0, i - width), min(len(text), i + len(token) + width)
    return " ".join(text[s:e].split())


@tool
def fetch_paper_text(pdf_url: str = "", paper_id: str = "", pmcid: str = "", search_index: int = 0, output_dir: str = "./data/papers") -> str:
    """
    Download an open-access paper's full text and report any data-repository accessions
    (GEO/SRA/ArrayExpress) found — the bridge from a paper to its data.

    PREFERRED CALL after search_papers: pass search_index=N (the [#N] rank shown by
    search_papers). The tool looks up that hit's EXACT pmcid/pdf_url for you, so you never
    retype an id. Do NOT copy the PMCID digits into the call yourself — mistyping them
    silently fetches an unrelated paper.

    Two sources are tried in order:
      1. Europe PMC full-text XML (when a pmcid is available) — no auth, rarely 403s, and the
         JATS XML includes the Data Availability section where accessions are stated.
      2. Direct open-access PDF download + text extraction (when there is no pmcid, or the
         article is not in Europe PMC's open-access set). Publisher PDFs (bioRxiv/MDPI/
         Wiley) often 403 under bot protection — if one fails, try a different candidate.

    Args:
        pdf_url: Direct open-access PDF URL. Only needed when starting from a known URL with
            no prior search_papers call; otherwise prefer search_index.
        paper_id: Optional id used to name saved files (the 'paperId' from search_papers).
        pmcid: PubMed Central id. Only pass this directly when you started from a KNOWN paper
            (no search_papers call this session). For a search hit, use search_index instead —
            a directly-passed pmcid that isn't in the latest search is rejected as a likely typo.
        search_index: 1-based [#N] rank from the most recent search_papers result. When >=1,
            its exact pmcid/pdf_url/paperId are used and the pmcid/pdf_url args are ignored.
        output_dir: Directory where the extracted .txt (and downloaded .pdf, if used) are saved.
    """
    try:
        # Resolve a search-result handle to exact identifiers FIRST. This is the path that
        # eliminates PMCID transcription errors — the LLM passes a small index it can't corrupt.
        if search_index and int(search_index) >= 1:
            row = _search_row_by_index(int(search_index))
            if row is None:
                if not _LAST_SEARCH_ROWS:
                    return ("search_index was given but no search_papers result is cached this session. "
                            "Call search_papers first and fetch by its [#N] index, or pass pdf_url for a known URL.")
                return (f"search_index={search_index} is out of range — the last search returned "
                        f"{len(_LAST_SEARCH_ROWS)} hits (valid indices 1..{len(_LAST_SEARCH_ROWS)}).")
            pmcid = row.get("pmcid", "") or pmcid
            pdf_url = row.get("pdf_url", "") or pdf_url
            paper_id = paper_id or row.get("paperId", "")
            if not pmcid and not pdf_url:
                return (f"Search hit #{search_index} ('{(row.get('title') or '')[:60]}') has neither a PMCID "
                        f"nor a PDF URL and cannot be fetched — pick a different hit.")
        # Anti-hallucination guard: a directly-passed pmcid that isn't in the latest search is
        # almost certainly a mistyped id that would fetch the wrong paper. Reject in the search
        # flow; allow it when no search has run (a seeded known-paper run has nothing to check).
        elif pmcid and _LAST_SEARCH_ROWS and not _pmcid_in_last_search(pmcid):
            return (f"pmcid '{pmcid}' is NOT among the latest search_papers results "
                    f"({len(_LAST_SEARCH_ROWS)} hits) — this usually means the id was mistyped. "
                    f"Do NOT retype PMCIDs: call fetch_paper_text(search_index=N) using the [#N] rank, "
                    f"which resolves the exact id for you.")

        if not pdf_url and not pmcid:
            return "Provide at least one of search_index, pmcid, or pdf_url."
        os.makedirs(output_dir, exist_ok=True)
        pid = paper_id or _normalize_pmcid(pmcid) or hashlib.md5(pdf_url.encode()).hexdigest()[:12]
        safe_pid = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in pid)

        text = ""
        source = ""
        notes = []

        # Strategy 1: Europe PMC full-text XML (preferred — reliable, has Data Availability).
        if pmcid:
            xml_text, _epmc_url = _fetch_europepmc_text(pmcid)
            if xml_text:
                text, source = xml_text, f"Europe PMC full-text XML ({_normalize_pmcid(pmcid)})"
            else:
                notes.append(f"Europe PMC had no open-access full text for {_normalize_pmcid(pmcid) or pmcid} "
                             f"(not in its OA set); falling back to PDF.")

        # Strategy 2: download the PDF and extract text (fallback).
        if not text:
            if not pdf_url:
                return ("No text obtained: Europe PMC has no open-access full text for "
                        f"{_normalize_pmcid(pmcid) or pmcid} and no pdf_url was provided.")
            r = requests.get(pdf_url, headers=_HTTP_HEADERS, timeout=60, allow_redirects=True)
            r.raise_for_status()
            content = r.content
            ctype = r.headers.get("Content-Type", "").lower()
            if not (content[:5] == b"%PDF-" or "application/pdf" in ctype):
                return (f"The URL did not return a PDF (Content-Type: {ctype or 'unknown'}). "
                        f"openAccessPdf links sometimes point to a publisher landing page — if the paper "
                        f"has a pmcid, call this tool again with that instead. First bytes: {content[:20]!r}")
            pdf_path = os.path.join(output_dir, f"{safe_pid}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(content)
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content))
            pages = []
            for p in reader.pages:
                try:
                    pages.append(p.extract_text() or "")
                except Exception:
                    pages.append("")
            text = "\n".join(pages)
            if not text.strip():
                return (f"Downloaded the PDF ({len(content)} bytes, {len(reader.pages)} pages) but extracted no "
                        f"text — likely a scanned/image PDF with no text layer (OCR not supported). Saved to {pdf_path}.")
            source = f"PDF download ({len(reader.pages)} pages)"
            notes.append(f"PDF saved to: {pdf_path}")

        txt_path = os.path.join(output_dir, f"{safe_pid}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        accs = _extract_accessions(text)
        lines = [
            f"Fetched paper text via {source}: {len(text)} chars.",
            f"- Text saved to: {txt_path}",
        ]
        for n in notes:
            lines.append(f"- {n}")
        if accs:
            lines.append("- Data-repository accessions found:")
            for kind, hits in accs.items():
                lines.append(f"    {kind}: {', '.join(hits)}")
            for gse in accs.get("GEO_series", [])[:3]:
                ctx = _context_for(text, gse)
                if ctx:
                    lines.append(f"    [{gse} context] …{ctx}…")
            lines.append("- NOTE: a GSE in the text may be the paper's OWN data OR a citation of another "
                         "study — check the context snippet before downloading.")
        else:
            lines.append("- No GEO/SRA/ArrayExpress accession found in the text (data may be in "
                         "supplementary files, or text extraction missed it).")
        return "\n".join(lines)
    except Exception as e:
        return f"Failed to fetch paper text. Error: {type(e).__name__}: {e}"


@tool
def extract_geo_accession(text_or_path: str) -> str:
    """
    Scan text for data-repository accessions (GEO GSE, SRA, ArrayExpress). Accepts
    either raw text or a path to a saved .txt file (e.g. the output of fetch_paper_text).

    GEO series (GSE…) are the actionable ones — pass them to download_geo_data.

    Args:
        text_or_path: A path to a .txt file, or a raw text string to scan.
    """
    try:
        text = text_or_path
        if len(text_or_path) < 1000 and os.path.isfile(text_or_path):
            with open(text_or_path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        accs = _extract_accessions(text)
        if not accs:
            return "No GEO/SRA/ArrayExpress accessions found."
        lines = ["Accessions found:"]
        for kind, hits in accs.items():
            lines.append(f"- {kind}: {', '.join(hits)}")
        gse = accs.get("GEO_series", [])
        if gse:
            lines.append("")
            lines.append("GEO series (usable by download_geo_data):")
            for g in gse:
                ctx = _context_for(text, g)
                lines.append(f"- {g}: …{ctx}…" if ctx else f"- {g}")
        return "\n".join(lines)
    except Exception as e:
        return f"Accession extraction failed. Error: {type(e).__name__}: {e}"


# -----------------------------------------------------------------------------
@tool
def assemble_agent_a_record(
    paper_id: str,
    pmcid: str,
    chosen_gse: str,
    chosen_reason: str,
    rejected_gses: list,
    cohort_run_label: str,
    paper_title: str = "",
    paper_year: int = 0,
    paper_doi: str = "",
    paper_pmid: str = "",
    organism: str = "",
    output_dir: str = "./output/agentA",
) -> str:
    """LEGACY: assemble the deprecated flat Agent A v0 record.

    Kept for compatibility with historical scripts. New workflows must use
    ``run_agent_a_cohort`` and its relational SEA-CDM outputs.

    Args:
        paper_id: Semantic Scholar paperId from search_papers' CSV. Pass "" if
            unknown (e.g. seeded run starting from a PMCID).
        pmcid: PubMed Central id (e.g. 'PMC12248044') passed to fetch_paper_text.
        chosen_gse: The GSE identified as the paper's OWN deposited data.
        chosen_reason: Short tag explaining why it is own data
            (e.g. "deposition language: 'are deposited'").
        rejected_gses: List of dicts for any other GSE accessions found in the
            text but rejected as cited/reused. Each dict: {"gse": "...", "reason": "..."}.
            Pass [] if none were rejected.
        cohort_run_label: The run_label you passed to run_batch_geo_pipeline.
        paper_title, paper_year, paper_doi, paper_pmid: Bibliographic fields from
            the search_papers row. Pass "" / 0 if unknown.
        organism: 'Human' or 'Mouse' (whatever you passed to run_batch_geo_pipeline).
        output_dir: Directory for the record JSON. Default ./output/agentA.
    """
    try:
        norm_pmcid = _normalize_pmcid(pmcid) or pmcid
        record = {
            "version": "LEGACY v0.1 — deprecated SEA-CDM subset",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "paper": {
                "paperId": paper_id,
                "title": paper_title,
                "year": paper_year or None,
                "pmcid": norm_pmcid,
                "pmid": paper_pmid,
                "doi": paper_doi,
            },
            "organism": organism or None,
            "data_discovery": {
                "chosen_gse": chosen_gse,
                "chosen_reason": chosen_reason,
                "chosen_snippet_verified": None,
                "rejected_gses": [dict(r) for r in (rejected_gses or [])],
            },
            "study_extracted": None,
            "secondary_analysis": None,
            "provenance": {},
            "sea_cdm_alignment_notes": "Deprecated flat subset; use run_agent_a_cohort.",
            "issues": [],
        }

        # 1. Locate the paper text on disk (used to verify snippets defensively).
        candidates = [
            os.path.join("data", "papers", f"{paper_id}.txt") if paper_id else "",
            os.path.join("data", "papers", f"{norm_pmcid}.txt") if norm_pmcid else "",
            os.path.join("data", "papers", f"{pmcid}.txt"),
        ]
        text_path = next((p for p in candidates if p and os.path.isfile(p)), None)
        paper_text = ""
        if text_path:
            try:
                with open(text_path, encoding="utf-8", errors="replace") as f:
                    paper_text = f.read()
                record["provenance"]["paper_text"] = text_path
            except Exception as e:
                record["issues"].append(f"paper text file unreadable: {e}")
        else:
            record["issues"].append(
                f"paper text not found under data/papers/ (tried paper_id, pmcid). "
                f"Snippets cannot be re-verified — record will rely on agent-provided `reason` strings."
            )

        # 2. Re-derive verified context snippets for chosen + rejected GSEs.
        if paper_text:
            if chosen_gse:
                record["data_discovery"]["chosen_snippet_verified"] = _context_for(paper_text, chosen_gse) or None
            for r in record["data_discovery"]["rejected_gses"]:
                gse = str(r.get("gse", ""))
                if gse:
                    r["snippet_verified"] = _context_for(paper_text, gse) or None

        # 2b. Fabrication check (fail-loud). Any GSE the agent passed that is NOT
        # present in the paper text is almost certainly hallucinated — from training
        # memory, from a search_geo_studies fallback, or invented. Flag CRITICALLY so
        # a reviewer cannot miss it. This is the single most important integrity check
        # in the v0 record.
        if paper_text:
            if chosen_gse and not record["data_discovery"]["chosen_snippet_verified"]:
                record["issues"].append(
                    f"CRITICAL: chosen_gse '{chosen_gse}' does NOT appear in the paper text "
                    f"({text_path}). Almost certainly fabricated — do not trust this record without "
                    f"manual verification of the paper's Data Availability section."
                )
            for r in record["data_discovery"]["rejected_gses"]:
                if r.get("gse") and not r.get("snippet_verified"):
                    record["issues"].append(
                        f"CRITICAL: rejected_gse '{r['gse']}' does NOT appear in the paper text."
                    )

        # 2c. If the agent reported no GSE was findable, record that explicitly (not an error).
        if not chosen_gse:
            record["data_discovery"]["chosen_gse"] = None
            if not chosen_reason:
                record["data_discovery"]["chosen_reason"] = "no GSE accession found in fetched paper text"

        # 3. Cohort artifacts (decisions.json + summary.csv).
        cohort_dir = os.path.join("output", f"cohort_{cohort_run_label}")
        study_cohort_dir = os.path.join(cohort_dir, chosen_gse)
        if os.path.isdir(study_cohort_dir):
            record["provenance"]["cohort_dir"] = cohort_dir
        else:
            record["issues"].append(f"cohort study dir not found: {study_cohort_dir}")

        decisions = None
        decisions_path = os.path.join(study_cohort_dir, "decisions.json")
        if os.path.isfile(decisions_path):
            try:
                with open(decisions_path, encoding="utf-8") as f:
                    decisions = json.load(f)
                record["provenance"]["decisions_log"] = decisions_path
            except Exception as e:
                record["issues"].append(f"decisions.json unreadable: {e}")

        summary_row = None
        summary_path = os.path.join(cohort_dir, "summary.csv")
        if os.path.isfile(summary_path):
            try:
                df = pd.read_csv(summary_path)
                if "accession" in df.columns:
                    rows = df[df["accession"].astype(str) == chosen_gse]
                    if not rows.empty:
                        summary_row = {k: (None if pd.isna(v) else v) for k, v in rows.iloc[0].to_dict().items()}
                record["provenance"]["summary_csv"] = summary_path
            except Exception as e:
                record["issues"].append(f"summary.csv unreadable: {e}")

        if decisions or summary_row:
            da_method = (summary_row or {}).get("da_method") or "unknown"
            input_data_descriptions = {
                "deseq2": "Raw RNA-seq integer counts (per-gene, per-sample matrix)",
                "limma": "Log-scale expression matrix (log2-transformed CPM / FPKM / TPM)",
                "unknown": None,
            }
            deg_csvs = sorted(glob.glob(os.path.join(study_cohort_dir, "DEG_results_*.csv")))
            gsea_csvs = sorted(glob.glob(os.path.join(study_cohort_dir, "*_GSEA_*.csv")))
            gsea_failure = None
            if decisions:
                for d in decisions.get("decisions", []):
                    if d.get("step") == "gsea" and d.get("decision") == "failed":
                        gsea_failure = d.get("reason")
                        break

            analysis_row = {
                "analysis_id": f"{chosen_gse}_DE_v0" if chosen_gse else None,
                "group_id": None,
                "documentation_id": None,
                "input_data": input_data_descriptions.get(da_method),
                "input_data_id": chosen_gse or None,
                "file_access": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={chosen_gse}" if chosen_gse else None,
                "analysis_name": "Differential expression analysis" + (f" + GSEA (Hallmark)" if gsea_csvs else ""),
                "analysis_name_id": None,
                "reference_source": "GEO" if chosen_gse else None,
                "reference_source_id": chosen_gse or None,
            }
            sa = {
                "source": "run_batch_geo_pipeline + LLM-A contrast validation",
                "analysis": analysis_row,
                "contrast": {
                    "design_column": (summary_row or {}).get("design_col"),
                    "control": (summary_row or {}).get("control"),
                    "treatment": (summary_row or {}).get("treatment"),
                },
                "outcome": {
                    "status": (summary_row or {}).get("status"),
                    "matrix_type": (summary_row or {}).get("matrix_type"),
                    "da_method": da_method if da_method != "unknown" else None,
                    "n_deg": (summary_row or {}).get("n_deg"),
                    "n_gsea_sig": (summary_row or {}).get("n_gsea_sig"),
                    "deg_csv": deg_csvs[0] if deg_csvs else None,
                    "gsea_csvs": gsea_csvs or None,
                    "gsea_failure": gsea_failure,
                },
                "decisions": {
                    "llm_validated": (summary_row or {}).get("llm_validated"),
                    "llm_overrode": (summary_row or {}).get("llm_overrode"),
                    "llm_reasoning": (summary_row or {}).get("llm_reasoning"),
                    "sex_mismatch": (summary_row or {}).get("sex_mismatch"),
                },
            }
            record["secondary_analysis"] = sa

        seacdm_path = os.path.join("output", f"{chosen_gse}_seacdm.json")
        if os.path.isfile(seacdm_path):
            try:
                with open(seacdm_path, encoding="utf-8") as f:
                    raw = json.load(f)
                record["provenance"]["study_seacdm"] = seacdm_path

                study_row = {
                    "study_id": raw.get("study_id"),
                    "study_name": None,
                    "study_description": raw.get("study_objective"),
                    "study_type": None,
                    "study_type_id": None,
                    "study_focus": None,
                    "study_focus_id": None,
                    "study_keywords": None,
                    "study_keyword_id": None,
                    "reference_source": "GEO" if raw.get("study_id", "").startswith("GSE") else None,
                    "reference_source_id": raw.get("study_id"),
                    "comments": None,
                }

                assay_rows = []
                for i, a in enumerate(raw.get("assays", []) or []):
                    assay_rows.append({
                        "assay_id": f"{raw.get('study_id') or 'unknown'}_assay_{i+1}",
                        "documentation_id": None,
                        "assay_name": a.get("assay_type"),
                        "assay_name_id": None,
                        "assay_type": "Experimental Assay",
                        "organism_input": True,
                        "reagents": [],
                        "platform": [a.get("platform")] if a.get("platform") else [],
                    })

                record["study_extracted"] = {
                    "study": study_row,
                    "assays": assay_rows,
                    "_extraction_source": raw,
                    "_unmapped_fields": [
                        "experiments[].subject_species  → subject.species",
                        "experiments[].treatment_group  → groups + interventions",
                        "experiments[].control_group    → groups",
                        "experiments[].tissue_or_cell   → sample.biosample_type",
                        "assays[].platform              → material_id list (currently free text)",
                    ],
                }
            except Exception as e:
                record["issues"].append(f"{seacdm_path} unreadable: {e}")
        else:
            record["issues"].append(
                f"{seacdm_path} not found — Legacy flat extraction was not run."
            )

        metadata_path = os.path.join("data", chosen_gse, f"{chosen_gse}_metadata.csv")
        if os.path.isfile(metadata_path):
            record["provenance"]["metadata_csv"] = metadata_path

        os.makedirs(output_dir, exist_ok=True)
        stem_raw = norm_pmcid or paper_id or "unknown_paper"
        stem = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in stem_raw)
        out_path = os.path.join(output_dir, f"{stem}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

        crit = [i for i in record["issues"] if i.startswith("CRITICAL")]
        info = [i for i in record["issues"] if not i.startswith("CRITICAL")]
        lines = [
            f"LEGACY Agent A v0 record written: {out_path}",
            f"- paper: paperId={paper_id or '∅'} | pmcid={norm_pmcid or '∅'} | year={record['paper']['year'] or '∅'}",
        ]
        if chosen_gse:
            lines.append(f"- chosen GSE: {chosen_gse} ({len(record['data_discovery']['rejected_gses'])} rejected)")
        else:
            lines.append(f"- chosen GSE: ∅ (no GSE found in fetched paper text — honest stop)")
        if record["secondary_analysis"]:
            sa = record["secondary_analysis"]
            outcome = sa.get("outcome", {})
            contrast = sa.get("contrast", {})
            analysis = sa.get("analysis", {})
            lines.append(
                f"- secondary analysis: status={outcome.get('status', '∅')} | "
                f"method={outcome.get('da_method', '∅')} | "
                f"n_deg={outcome.get('n_deg', '∅')} | "
                f"design={contrast.get('design_column', '∅')} | "
                f"analysis_id={analysis.get('analysis_id', '∅')}"
            )
        else:
            lines.append("- secondary analysis: no cohort artifacts found")
        if record["study_extracted"]:
            lines.append("- study_extracted: present (Legacy flat extractor)")
        else:
            lines.append("- study_extracted: absent (Legacy flat extractor not called)")
        if crit:
            lines.append(f"!!! CRITICAL issues ({len(crit)}) — record is likely fabricated:")
            for issue in crit:
                lines.append(f"    {issue}")
        if info:
            lines.append(f"- informational issues ({len(info)}):")
            for issue in info:
                lines.append(f"    • {issue}")
        if not record["issues"]:
            lines.append("- no issues (all expected artifacts found AND chosen_gse verified in paper text)")
        return "\n".join(lines)

    except Exception as e:
        return f"assemble_agent_a_record failed. Error: {type(e).__name__}: {e}"
