"""Proteomics dispatch utilities for PRIDE-sourced datasets.

The first step in any proteomics DA pipeline is classifying the study as
labeled (TMT / iTRAQ / SILAC / ...) vs label-free, because preprocessing
differs completely:
  - Labeled: within-plex log-ratios, cross-plex batch correction mandatory
  - Label-free: intensity per sample, missing-value imputation mandatory

PRIDE exposes the necessary signals as structured (or semi-structured) JSON
fields via its REST API; this module turns that into a single classifier with
a deterministic fallback cascade — LLM is only the last resort.

Also provides `download_pride_project` — mirrors the per-project layout used
for GEO accessions (data/{PXD}/) but keeps only processed quantification
matrices (skips RAW / .mzML / .mzid which are out of our matrix-in scope).
"""

import gzip
import json
import os
import re
from collections import Counter
from typing import Optional, Literal

import numpy as np
import pandas as pd
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

PRIDE_BASE = "https://www.ebi.ac.uk/pride/ws/archive/v3"

# Labeled-reagent regexes. Order = scan order; first hit wins.
# Word boundaries used to avoid catching e.g. "Tmtc1" gene name false positives.
_LABELED_REAGENT_PATTERNS = [
    ("TMT", re.compile(r"\btmt(?:\d{1,2}|pro)?(?:plex)?\b|tandem mass tag", re.I)),
    ("iTRAQ", re.compile(r"\bitraq\b", re.I)),
    ("ICAT", re.compile(r"\bicat\b", re.I)),
    ("SILAC", re.compile(r"\bsilac\b", re.I)),
    ("MeCAT", re.compile(r"\bmecat\b", re.I)),
    ("dimethyl", re.compile(r"\bdimethyl labeling\b|\bdimethyl label\b", re.I)),
    ("NeuCode", re.compile(r"\bneucode\b", re.I)),
    ("TAILS", re.compile(r"\btails\b", re.I)),
]

# Label-free signal regex. The `\blfq[a-z]*\b` allows compound words like
# "LFQintensities" / "LFQnorm" — surfaced 2026-05-28 on PXD028408 where the
# submitter wrote "LFQintensities" with no space, defeating a strict `\blfq\b`.
# Compound-word forms in proteomics are essentially always LFQ-related, so the
# false-positive risk of `lfq[a-z]*` is negligible.
_LABEL_FREE_PATTERN = re.compile(
    r"\blabel[- ]?free\b|\blfq[a-z]*\b|\bintensity[- ]based absolute quantif\w*\b|\bibaq\b",
    re.I,
)

# Quant-matrix file detection. Accepts:
#   - .mztab / .mztab.gz (PRIDE standard tab-delimited quant)
#   - .csv / .tsv / .xlsx / .xls (custom processed matrices)
#   - MaxQuant outputs: proteinGroups.txt / peptides.txt / evidence.txt
#   - Files whose name hints "intensity" / "abundance" / "quant" / "matrix" with .txt
_QUANT_MATRIX_EXTS = {".mztab", ".csv", ".tsv", ".xlsx", ".xls"}
_QUANT_MATRIX_NAME_HINTS = (
    "proteingroups", "peptides", "evidence",
    "intensity", "abundance", "quant", "matrix",
)

# Protein-ID column patterns (in priority order — first match wins).
# Used by `_load_quant_matrix` to pick the right index column from generic
# CSV/TSV/XLSX inputs where the protein ID isn't necessarily at column 0.
# Surfaced 2026-05-28 on PXD025560 where col 0 was `PG.Pvalue` (a score) and
# the real ID was at col 3 (`PG.ProteinGroups`).
_PROTEIN_ID_PATTERNS = [
    re.compile(r"protein[._\s-]?group", re.I),      # Spectronaut: PG.ProteinGroups; MaxQuant: Protein group
    re.compile(r"protein[._\s-]?accession", re.I),  # Spectronaut: PG.ProteinAccessions
    re.compile(r"majority[._\s-]?protein", re.I),   # MaxQuant: Majority protein IDs
    re.compile(r"protein[._\s-]?id\b", re.I),       # generic Protein_ID / ProteinID
    re.compile(r"^accession$", re.I),               # mzTab convention: bare "accession"
    re.compile(r"^uniprot", re.I),                  # UniprotID / UniProtAccession
    re.compile(r"^entry$", re.I),                   # UniProt direct export
]

# Per-protein score / stat / structural-property column patterns. These look
# numeric (so pass the "is numeric" sample-column heuristic) but are NOT per-
# sample measurements. Excluding them prevents fake "samples" in the output.
# Surfaced 2026-05-28 on PXD025560 (`PG.Pvalue`, `PG.Qvalue`, `PG.Cscore`).
_SCORE_OR_STAT_PATTERNS = [
    # p / q / e / pep values (allow ., _, -, space between letter and "value")
    re.compile(r"\b[qpe][._\s-]?value\b", re.I),
    re.compile(r"\bpep[._\s-]?value\b", re.I),
    re.compile(r"\bpvalue\b|\bqvalue\b|\bevalue\b", re.I),
    # confidence / search-engine scores
    re.compile(r"\bc[._\s-]?score\b", re.I),
    re.compile(r"\bscore\b", re.I),
    # coverage / counts / structural per-protein properties
    re.compile(r"\bcoverage\b", re.I),
    re.compile(r"\b(?:num(?:ber)?|n)[._\s-]?(?:of[._\s-])?(?:psm|peptide|protein|spec|ms2)", re.I),
    re.compile(r"\bms[/_.\s-]?ms[._\s-]?count\b", re.I),
    re.compile(r"\b(?:unique|distinct|razor)[._\s-]?peptide", re.I),
    re.compile(r"\bsequence[._\s-]?length\b", re.I),
    re.compile(r"\bmol[._\s-]?weight\b|\bmolecular[._\s-]?weight\b|\bmw\b", re.I),
    # PEP standalone (Posterior Error Probability) — won't match "Peptide"
    # because `\bpep\b` requires word boundary after pep (t in Peptide blocks it).
    re.compile(r"\bpep\b", re.I),
]


def _find_protein_id_column(columns) -> Optional[str]:
    """Pick the most likely protein-ID column from a list of candidates by name.
    Returns None if no pattern matches (caller falls back to column 0)."""
    for pat in _PROTEIN_ID_PATTERNS:
        for c in columns:
            if pat.search(str(c)):
                return c
    return None


def _is_score_or_stat_column(name) -> bool:
    """Whether a numeric-looking column is actually a per-protein score/stat
    rather than a per-sample measurement."""
    s = str(name)
    return any(p.search(s) for p in _SCORE_OR_STAT_PATTERNS)


class ProteomicsLabelingResult(BaseModel):
    """Structured output for `identify_proteomics_labeling`."""
    accession: str
    labeling: Literal["labeled", "label_free", "unknown"]
    reagent: Optional[str] = Field(
        default=None,
        description="Specific labeling reagent (TMT / iTRAQ / SILAC / ...) when labeling=='labeled'.",
    )
    source: Literal["quantificationMethods", "identifiedPTMStrings", "text_scan", "no_signal", "error"]
    has_quant_matrix: Optional[bool] = Field(
        default=None,
        description="Whether the PRIDE project ships at least one processed "
                    "quantification matrix file (mztab/csv/tsv/xlsx/MaxQuant-output). "
                    "None when the files-list endpoint could not be queried.",
    )
    quant_files: list[str] = Field(
        default_factory=list,
        description="Filenames of detected quant-matrix files (capped at 20).",
    )
    n_files_total: Optional[int] = None
    raw_quantification_methods: list[str] = Field(default_factory=list)
    raw_keywords: list[str] = Field(default_factory=list)
    reasoning: str = ""


def _pride_get(path: str) -> dict | list:
    """Thin GET against PRIDE REST API. Raises on HTTP error."""
    url = f"{PRIDE_BASE}/{path}"
    resp = requests.get(url, timeout=30, headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def _pride_get_all_files(pxd_accession: str, max_pages: int = 100) -> list[dict]:
    """Paginate through PRIDE's `/projects/{pxd}/files` endpoint.

    The endpoint caps each page at 100 results regardless of `pageSize`, so
    enumerating large projects requires iterating pages. Stops at the first
    short page (<100 results) or `max_pages`, whichever comes first."""
    all_files: list[dict] = []
    for page in range(max_pages):
        try:
            chunk = _pride_get(f"projects/{pxd_accession}/files?page={page}&pageSize=100")
        except Exception:
            break
        if not isinstance(chunk, list) or not chunk:
            break
        all_files.extend(chunk)
        if len(chunk) < 100:
            break
    return all_files


def _http_url_from_pride_locations(locations) -> Optional[str]:
    """Convert PRIDE's FTP-protocol publicFileLocation entry to an HTTPS URL.

    PRIDE mirrors `ftp://ftp.pride.ebi.ac.uk/...` at `https://ftp.pride.ebi.ac.uk/...`
    (verified 2026-05-28). Using HTTPS lets us stream via requests rather than
    the awkward ftplib path."""
    if not locations:
        return None
    for loc in locations:
        name = (loc.get("name") or "").lower()
        url = loc.get("value") or ""
        if "ftp" in name and url.startswith("ftp://"):
            return "https://" + url[len("ftp://"):]
    return None


def _download_file_stream(url: str, dest_path: str, skip_if_exists: bool = True) -> tuple[str, int]:
    """Stream a URL to dest_path. Returns ('downloaded' | 'skipped_exists', bytes).

    Writes to a `.tmp` sibling and atomically renames on success so an interrupted
    download leaves no half-files in place. Raises on HTTP / network failure;
    caller handles."""
    if skip_if_exists and os.path.exists(dest_path):
        return ("skipped_exists", os.path.getsize(dest_path))
    tmp_path = dest_path + ".tmp"
    try:
        with requests.get(url, stream=True, timeout=300) as resp:
            resp.raise_for_status()
            total = 0
            with open(tmp_path, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        fh.write(chunk)
                        total += len(chunk)
        os.replace(tmp_path, dest_path)
        return ("downloaded", total)
    except Exception:
        if os.path.exists(tmp_path):
            try: os.remove(tmp_path)
            except OSError: pass
        raise


def _is_quant_matrix_filename(name: str) -> bool:
    """Whether a PRIDE file looks like a processed quantification matrix our DA
    layer can consume. Same logic as `_detect_quant_matrix` per-file."""
    if not name:
        return False
    low = name.lower()
    inner = low[:-3] if low.endswith(".gz") else low
    ext = "." + inner.rsplit(".", 1)[-1] if "." in inner else ""
    if ext in _QUANT_MATRIX_EXTS:
        return True
    if ext == ".txt" and any(h in inner for h in _QUANT_MATRIX_NAME_HINTS):
        return True
    return False


def _detect_reagent(text: str) -> Optional[str]:
    """Return the first labeled-reagent name matched in text, or None."""
    if not text:
        return None
    for name, pat in _LABELED_REAGENT_PATTERNS:
        if pat.search(text):
            return name
    return None


def _is_label_free(text: str) -> bool:
    return bool(text and _LABEL_FREE_PATTERN.search(text))


def _extract_names(field) -> list[str]:
    """Pull human-readable names from a PRIDE CvParam-style field, which may
    appear as: a plain string, a list of strings, a single dict, or a list of
    {name, value, accession} dicts."""
    if field is None:
        return []
    if isinstance(field, str):
        return [field]
    if isinstance(field, dict):
        return [field.get("name") or field.get("value") or ""]
    if isinstance(field, list):
        out = []
        for item in field:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                out.append(item.get("name") or item.get("value") or "")
        return [s for s in out if s]
    return []


def _classify_from_metadata(meta: dict) -> tuple[str, Optional[str], str, str]:
    """3-rung deterministic classification cascade. Returns
    (labeling, reagent, source, reasoning)."""
    # Rung 1: structured quantificationMethods (most direct when populated)
    qm_names = _extract_names(meta.get("quantificationMethods"))
    if qm_names:
        joined = " ".join(qm_names)
        if _is_label_free(joined):
            return "label_free", None, "quantificationMethods", f"quantificationMethods={qm_names}"
        reagent = _detect_reagent(joined)
        if reagent:
            return "labeled", reagent, "quantificationMethods", f"quantificationMethods={qm_names}"
        # Populated but no labeled reagent — submitter SAID a quant method, just
        # not one our regex recognizes by name (e.g. "TIC", "iBAQ", "MaxLFQ",
        # "Spectral counting", "XIC"). The PRIDE controlled vocabulary's non-
        # reagent entries are essentially all LFQ variants, so default to
        # label_free with a "(unrecognized)" tag in the reasoning. Surfaced
        # 2026-05-28 on PXD025560 which had quantificationMethods=["TIC"].
        return ("label_free", None, "quantificationMethods",
                f"quantificationMethods={qm_names} — unrecognized term, "
                f"defaulting to label-free (PRIDE vocabulary's non-reagent "
                f"quant methods are typically LFQ variants)")

    # Rung 2: PTM strings (TMT/iTRAQ reagents appear here as e.g.
    # "TMT6plex-126 reporter+balance reagent acylated residue")
    ptm_names = _extract_names(meta.get("identifiedPTMStrings"))
    for ptm in ptm_names:
        reagent = _detect_reagent(ptm)
        if reagent:
            return "labeled", reagent, "identifiedPTMStrings", f"PTM signal: {ptm}"

    # Rung 3: free-text scan over keywords + protocols + title + description
    keywords = _extract_names(meta.get("keywords"))
    text_blob = " ".join([
        " ".join(keywords),
        str(meta.get("sampleProcessingProtocol") or ""),
        str(meta.get("dataProcessingProtocol") or ""),
        str(meta.get("title") or ""),
        str(meta.get("projectDescription") or ""),
    ])
    if _is_label_free(text_blob):
        return "label_free", None, "text_scan", "label-free keyword in protocols/keywords"
    reagent = _detect_reagent(text_blob)
    if reagent:
        return "labeled", reagent, "text_scan", f"{reagent} keyword in protocols/keywords"

    return "unknown", None, "no_signal", (
        "No deterministic signal in quantificationMethods, identifiedPTMStrings, "
        "keywords, or protocol text. LLM fallback would be needed to read the full protocol."
    )


def _detect_quant_matrix(files: list[dict]) -> tuple[bool, list[str]]:
    """Scan a PRIDE files list for processed quantification matrices.
    Returns (has_any, matched_filenames[:20])."""
    matches = [f.get("fileName") for f in files
               if _is_quant_matrix_filename(f.get("fileName") or "")]
    return bool(matches), matches[:20]


@tool
def identify_proteomics_labeling(pxd_accession: str) -> str:
    """Classify a PRIDE project as labeled (TMT/iTRAQ/SILAC/...) vs label-free
    proteomics, and check whether it ships a processed quantification matrix.

    USE THIS AS THE FIRST STEP in any proteomics workflow — preprocessing
    differs completely between labeled (within-plex log-ratios + cross-plex
    batch correction) and label-free (per-sample intensity + missing-value
    imputation). DA tool (`run_limma_analysis`) is shared but everything
    upstream branches on this classification.

    Detection cascade (deterministic; LLM only if all 3 fail):
      1. PRIDE `quantificationMethods` field (most direct when populated)
      2. `identifiedPTMStrings` reagent scan (TMT6plex / iTRAQ4plex / etc.)
      3. Keyword/protocol text scan for "label free" / "TMT" / "iTRAQ" / ...

    Also inspects the project file list for processed quant matrices (`.mztab`,
    `.csv`, `.tsv`, `.xlsx`, MaxQuant `proteinGroups.txt` / `peptides.txt`).
    Projects without these ship only RAW + `.mzML` + `.mzid` and are out of
    our matrix-in DA scope — caller should skip them.

    Args:
        pxd_accession: PRIDE accession (e.g. "PXD019643"). Case-sensitive,
            must include the "PXD" prefix.

    Returns: JSON string of ProteomicsLabelingResult (labeling, reagent, source,
        has_quant_matrix, quant_files, raw_quantification_methods, raw_keywords,
        reasoning).
    """
    try:
        meta = _pride_get(f"projects/{pxd_accession}")
    except Exception as e:
        return json.dumps({
            "accession": pxd_accession,
            "labeling": "unknown",
            "source": "error",
            "reasoning": f"PRIDE project fetch failed: {type(e).__name__}: {e}",
        }, indent=2)

    labeling, reagent, source, reasoning = _classify_from_metadata(meta)

    # File-level matrix detection (best-effort; non-fatal on failure). Paginates —
    # the PRIDE endpoint caps each page at 100 results, so single-page enumeration
    # silently misses quant matrices on large projects.
    has_matrix, quant_files, n_files = None, [], None
    try:
        files = _pride_get_all_files(pxd_accession)
        if files:
            n_files = len(files)
            has_matrix, quant_files = _detect_quant_matrix(files)
    except Exception as e:
        reasoning = f"{reasoning} | files-list fetch failed: {type(e).__name__}: {e}"

    result = ProteomicsLabelingResult(
        accession=pxd_accession,
        labeling=labeling,
        reagent=reagent,
        source=source,
        has_quant_matrix=has_matrix,
        quant_files=quant_files,
        n_files_total=n_files,
        raw_quantification_methods=_extract_names(meta.get("quantificationMethods")),
        raw_keywords=_extract_names(meta.get("keywords")),
        reasoning=reasoning,
    )
    return result.model_dump_json(indent=2)


@tool
def download_pride_project(pxd_accession: str, base_dir: str = "data") -> str:
    """Download a PRIDE project's processed quantification matrices to local disk.

    Mirrors the GEO download layout: writes to `{base_dir}/{PXD}/` with one
    `{PXD}_project.json` metadata file (full PRIDE project JSON — sampleAttributes,
    organisms, protocols, etc.) plus the matrix file(s). RAW spectra, `.mzML`
    peak lists, and `.mzid` peptide IDs are EXPLICITLY EXCLUDED — they are out
    of our matrix-in DA scope and would waste GBs per project.

    Always call `identify_proteomics_labeling` first to verify the project
    actually has a quant matrix (`has_quant_matrix=true`). If you call this on a
    RAW-only project the tool returns 'NO QUANT MATRIX' and downloads only the
    project JSON metadata (zero spectra files).

    All downloads are skip-if-exists, written via `.tmp` + atomic rename so an
    interrupted run leaves no partial files behind. The PRIDE FTP URLs are
    transparently rewritten to HTTPS for streaming via `requests` (PRIDE mirrors
    `ftp://ftp.pride.ebi.ac.uk/...` at `https://ftp.pride.ebi.ac.uk/...`).

    Args:
        pxd_accession: PRIDE accession (e.g. "PXD000001"). Case-sensitive, must
            include the "PXD" prefix.
        base_dir: Root directory under which `{PXD}/` is created. Defaults to
            'data' (matches the GEO download layout).

    Returns: a multi-line text summary — output dir, metadata path, lists of
        downloaded / reused / failed files with byte counts.
    """
    out_dir = os.path.join(base_dir, pxd_accession)
    os.makedirs(out_dir, exist_ok=True)

    # 1. Project metadata JSON (always saved — contains sampleAttributes / protocols)
    try:
        meta = _pride_get(f"projects/{pxd_accession}")
    except Exception as e:
        return f"ERROR: PRIDE project fetch failed for {pxd_accession}: {type(e).__name__}: {e}"
    meta_path = os.path.join(out_dir, f"{pxd_accession}_project.json")
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)

    # 2. Enumerate ALL files (paginated; PRIDE caps at 100 per page)
    all_files = _pride_get_all_files(pxd_accession)
    if not all_files:
        return (f"ERROR: no files returned by PRIDE for {pxd_accession}.\n"
                f"Project metadata saved to: {meta_path}")

    # 3. Filter to quant-matrix-relevant files
    relevant = [f for f in all_files if _is_quant_matrix_filename(f.get("fileName") or "")]
    cats = Counter(f.get("fileCategory", {}).get("value", "?") for f in all_files)
    if not relevant:
        return (
            f"NO QUANT MATRIX: {pxd_accession} has {len(all_files)} files but none look "
            f"like a processed quantification matrix (.mztab / .csv / .tsv / .xlsx / "
            f"MaxQuant proteinGroups.txt etc.).\n"
            f"File categories present: {dict(cats)}\n"
            f"This project likely ships RAW + .mzML + .mzid only and is out of our "
            f"matrix-in DA scope — skip it.\n"
            f"Project metadata saved to: {meta_path}"
        )

    # 4. Download with skip-if-exists
    print(f"PRIDE download: {pxd_accession} | {len(relevant)} relevant of {len(all_files)} total files")
    downloaded, skipped, failed = [], [], []
    for f in relevant:
        name = f.get("fileName") or "<unnamed>"
        # Belt-and-suspenders: strip any path separators a malformed entry could inject
        safe_name = name.replace("/", "_").replace("\\", "_")
        dest = os.path.join(out_dir, safe_name)
        url = _http_url_from_pride_locations(f.get("publicFileLocations"))
        if not url:
            failed.append((name, "no FTP URL in publicFileLocations"))
            print(f"  [FAILED] {name}: no FTP URL")
            continue
        size_hint = f.get("fileSizeBytes")
        if size_hint and size_hint > 500_000_000:
            print(f"  [LARGE] {name} reports {size_hint:,} bytes — downloading anyway")
        try:
            status, size = _download_file_stream(url, dest, skip_if_exists=True)
            if status == "skipped_exists":
                skipped.append((safe_name, size))
                print(f"  [reused] {safe_name} ({size:,} bytes)")
            else:
                downloaded.append((safe_name, size))
                print(f"  [downloaded] {safe_name} ({size:,} bytes)")
        except Exception as e:
            failed.append((name, f"{type(e).__name__}: {e}"))
            print(f"  [FAILED] {name}: {type(e).__name__}: {e}")

    # 5. Summary
    lines = [
        f"PRIDE download complete: {pxd_accession}",
        f"Output dir: {out_dir}",
        f"Project metadata: {meta_path}",
        f"Quant matrix files: {len(downloaded)} downloaded, {len(skipped)} reused, "
        f"{len(failed)} failed (of {len(relevant)} relevant; {len(all_files)} files total)",
    ]
    if downloaded:
        lines.append("Downloaded:")
        for name, size in downloaded:
            lines.append(f"  - {name} ({size:,} bytes)")
    if skipped:
        lines.append("Already present (reused):")
        for name, size in skipped:
            lines.append(f"  - {name} ({size:,} bytes)")
    if failed:
        lines.append("Failed:")
        for name, reason in failed:
            lines.append(f"  - {name}: {reason}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Preprocessing layer — turns a PRIDE quant matrix into log-scale, normalized,
# (optionally imputed) expression ready for run_limma_analysis.
# ---------------------------------------------------------------------------

# Recognized abundance column patterns in mzTab PRH header. mzTab 1.0 uses
# `protein_abundance_assay[N]` for raw per-channel/per-sample intensities;
# `protein_abundance_study_variable[N]` aggregates multiple assays and is NOT
# what we want for per-sample DA.
_MZTAB_ABUNDANCE_PATTERN = re.compile(r"protein_abundance_assay\[\d+\]", re.I)


def _parse_mztab(path: str) -> tuple[pd.DataFrame, list[str]]:
    """Parse the protein-level abundance section of an mzTab file.

    Returns (df, abundance_cols):
      - df: indexed by accession, columns = all PRH columns minus the leading PRT
        prefix, with decoy rows removed and "null" strings coerced to NaN
      - abundance_cols: subset of df.columns holding per-sample/per-channel
        intensities (protein_abundance_assay[N])

    Handles .gz transparently. Pads short rows. Filters decoys by either the
    standard PRIDE decoy flag (`opt_global_cv_PRIDE:0000303_Decoy_hit == 1`) or
    accession prefix `DECOY_`. Reads `mzTab-type` / `mzTab-mode` from MTD section
    so the caller can detect Identification-only files (no per-sample quant) and
    fail with a useful error rather than silently producing an empty matrix.
    """
    opener = gzip.open if path.endswith(".gz") else open
    prh: Optional[list[str]] = None
    prt_rows: list[list[str]] = []
    mztab_type: Optional[str] = None
    mztab_mode: Optional[str] = None
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("MTD\tmzTab-type\t"):
                mztab_type = line.rstrip("\n").split("\t", 2)[2].strip()
            elif line.startswith("MTD\tmzTab-mode\t"):
                mztab_mode = line.rstrip("\n").split("\t", 2)[2].strip()
            elif line.startswith("PRH\t"):
                prh = line.rstrip("\n").split("\t")[1:]
            elif line.startswith("PRT\t"):
                row = line.rstrip("\n").split("\t")[1:]
                if prh is not None:
                    if len(row) < len(prh):
                        row = row + [""] * (len(prh) - len(row))
                    elif len(row) > len(prh):
                        row = row[: len(prh)]
                prt_rows.append(row)
    if prh is None:
        raise ValueError("mzTab: no PRH (protein header) line found")
    if not prt_rows:
        raise ValueError("mzTab: PRH present but no PRT rows")

    df = pd.DataFrame(prt_rows, columns=prh)
    # mzTab uses literal "null" for missing values; pandas needs to be told.
    df = df.replace({"null": np.nan, "NaN": np.nan, "": np.nan})

    # Decoy filter — both the standard flag and the DECOY_ accession prefix.
    decoy_col = next((c for c in df.columns if "decoy_hit" in c.lower()), None)
    if decoy_col:
        df = df[df[decoy_col].fillna("0").astype(str).str.strip() != "1"]
    if "accession" in df.columns:
        df = df[~df["accession"].fillna("").astype(str).str.startswith("DECOY_")]
        df = df.set_index("accession")

    abundance_cols = [c for c in df.columns if _MZTAB_ABUNDANCE_PATTERN.search(c)]
    # If there are no abundance columns, the file is identification-only — fail
    # loudly so the caller's "no sample columns" path can report something
    # actionable instead of silently producing an empty matrix.
    if not abundance_cols and mztab_type and mztab_type.lower() != "quantification":
        raise ValueError(
            f"mzTab is identification-only (mzTab-type='{mztab_type}', "
            f"mzTab-mode='{mztab_mode}'). It has no protein_abundance_assay[N] "
            f"columns — per-sample quant is not in this file. Look for a separate "
            f"proteinGroups.txt / .csv / .xlsx in the project, or this project "
            f"may not have deposited a quant matrix."
        )
    return df, abundance_cols


def _load_quant_matrix(quant_path: str) -> tuple[pd.DataFrame, list[str]]:
    """Read a proteomics quant matrix from disk in any supported format.

    Returns (df, sample_cols). df is indexed by protein ID (picked by name
    pattern — `PG.ProteinGroups` / `Majority protein IDs` / `accession` etc.);
    sample_cols is the subset of df.columns that look like per-sample
    intensities AFTER excluding per-protein score/stat columns (`PG.Qvalue`,
    `PG.Cscore`, search-engine `Score`, `Coverage`, peptide counts, etc.).

    Supported formats:
      - .mztab / .mztab.gz   — PRIDE standard, via _parse_mztab (handles its
        own ID + abundance column detection)
      - .csv / .tsv / .txt   — generic; pandas separator sniffer
      - .xlsx / .xls         — generic Excel

    For non-mzTab formats: read all columns first, pick the protein-ID column
    by `_find_protein_id_column` (falls back to column 0 if no name matches),
    then exclude `_is_score_or_stat_column` matches from the numeric-looking
    candidates. Surfaced 2026-05-28 on PXD025560 where blindly using col 0 as
    index picked `PG.Pvalue` (a score) instead of `PG.ProteinGroups` (real ID),
    and 3 score columns slipped in as fake "samples".
    """
    low = quant_path.lower()
    inner = low[:-3] if low.endswith(".gz") else low
    if ".mztab" in inner:
        return _parse_mztab(quant_path)

    if inner.endswith((".csv", ".tsv", ".txt")):
        df = pd.read_csv(quant_path, sep=None, engine="python")  # no index_col yet
    elif inner.endswith((".xlsx", ".xls")):
        df = pd.read_excel(quant_path)
    else:
        raise ValueError(
            f"Unsupported quant matrix format: {os.path.basename(quant_path)}. "
            f"Supported: .mztab[.gz], .csv, .tsv, .txt, .xlsx, .xls"
        )

    # Pick the protein-ID column by name pattern; fall back to col 0.
    id_col = _find_protein_id_column(df.columns)
    if id_col is None:
        id_col = df.columns[0]
    df = df.set_index(id_col)

    coerced = df.apply(pd.to_numeric, errors="coerce")
    numeric_cols = [c for c in df.columns if not coerced[c].isna().all()]
    sample_cols = [c for c in numeric_cols if not _is_score_or_stat_column(c)]
    return df, sample_cols


@tool
def preprocess_proteomics_matrix(
    quant_path: str,
    labeling: str,
    output_dir: str = "./output",
    missing_threshold: float = 0.5,
    minprob_shift: float = 1.8,
    minprob_width: float = 0.3,
) -> str:
    """Preprocess a PRIDE proteomics quantification matrix for DA analysis.

    THIRD step in the proteomics chain (after identify_proteomics_labeling →
    download_pride_project). Reads the quant matrix (mzTab / CSV / TSV / XLSX),
    extracts intensity columns, log2-transforms if needed, applies labeling-
    specific normalization, and writes a preprocessed log-scale matrix ready
    for run_limma_analysis.

    Labeled branch (TMT / iTRAQ / SILAC):
      - log2-transform if matrix is on linear intensity scale
      - sample-level median centering (per-column median subtraction)
      - v0 does NOT do Internal Reference Scaling (IRS); proper cross-plex
        correction needs reference-channel metadata which is not auto-discoverable
        from PRIDE. Median centering is a reasonable first approximation.

    Label-free branch:
      - log2(x+1) transform
      - drop proteins with > `missing_threshold` fraction of samples missing
      - MinProb imputation (per-sample draw from N(μ - shift*σ, width*σ),
        Perseus-style defaults of 1.8 / 0.3) — replaces remaining NaN with
        low-tail values representing "below detection"
      - sample-level median centering

    Output CSV is column-compatible with what run_limma_analysis expects (rows
    = proteins, columns = samples, log-scale numeric values). Sample column
    names are preserved from the input — caller is responsible for aligning
    them to a metadata CSV before calling DA.

    Args:
        quant_path: Path to the quant matrix file. mzTab/csv/tsv/xlsx supported.
        labeling: 'labeled' or 'label_free' — typically from
            identify_proteomics_labeling.labeling.
        output_dir: Where to write `<base>_preprocessed.csv`.
        missing_threshold: LFQ only — drop proteins with more than this fraction
            of samples missing. Default 0.5.
        minprob_shift: LFQ only — MinProb mean shift in σ. Default 1.8 (Perseus).
        minprob_width: LFQ only — MinProb distribution width in σ. Default 0.3.
    """
    os.makedirs(output_dir, exist_ok=True)
    if labeling not in ("labeled", "label_free"):
        return (f"ERROR: labeling must be 'labeled' or 'label_free' (got {labeling!r}). "
                f"Call identify_proteomics_labeling first and pass its `labeling` field.")

    try:
        df, sample_cols = _load_quant_matrix(quant_path)
    except Exception as e:
        return f"ERROR: failed to load {quant_path}: {type(e).__name__}: {e}"

    if not sample_cols:
        return (f"ERROR: no per-sample intensity columns detected in {quant_path}. "
                f"For mzTab this means no `protein_abundance_assay[N]`; for CSV/TSV "
                f"this means all numeric-looking columns are empty after coercion.")

    expr = df[sample_cols].apply(pd.to_numeric, errors="coerce")
    n_features_in, n_samples = expr.shape
    n_missing_in = int(expr.isna().sum().sum())
    cells_in = n_features_in * n_samples
    pct_missing_in = (n_missing_in / cells_in) if cells_in else 0.0
    print(f"Loaded {os.path.basename(quant_path)}: {n_features_in} features x "
          f"{n_samples} samples | {n_missing_in} missing ({pct_missing_in:.1%})")
    print(f"  sample columns: {sample_cols[:6]}{' ...' if len(sample_cols) > 6 else ''}")

    # log2-transform if matrix looks linear-scale. Threshold: log2(CPM+1) tops
    # out around 20-25; raw intensities can hit 1e6+. Use 50 as a safe cutoff.
    finite = expr.values[np.isfinite(expr.values)]
    max_val = float(finite.max()) if finite.size else 0.0
    if max_val >= 50:
        expr = np.log2(expr.clip(lower=0) + 1)
        print(f"  log2(x+1) transformed (max before: {max_val:.1f})")
    else:
        print(f"  detected log-scale (max: {max_val:.2f}) — skipping log transform")

    # Branch on labeling
    n_imputed_total = 0
    n_filtered = 0
    if labeling == "label_free":
        # LFQ: filter by missingness, then MinProb-impute the rest
        valid_frac = expr.notna().mean(axis=1)
        keep_mask = valid_frac >= (1.0 - missing_threshold)
        n_filtered = int((~keep_mask).sum())
        expr = expr.loc[keep_mask]
        print(f"  missingness filter: dropped {n_filtered} features with "
              f"> {missing_threshold:.0%} missing ({len(expr)} retained)")

        rng = np.random.default_rng(42)  # deterministic for reproducibility
        for col in expr.columns:
            col_vals = expr[col].dropna()
            if len(col_vals) < 2:
                continue
            mu = float(col_vals.mean())
            sigma = float(col_vals.std()) or 1.0
            mask = expr[col].isna()
            n_imp = int(mask.sum())
            if n_imp == 0:
                continue
            draws = rng.normal(mu - minprob_shift * sigma, minprob_width * sigma, n_imp)
            expr.loc[mask, col] = draws
            n_imputed_total += n_imp
        print(f"  MinProb imputed: {n_imputed_total} values "
              f"(shift={minprob_shift}σ, width={minprob_width}σ)")
    else:
        # Labeled: v0 leaves NaN in place (limma can downweight per-feature) and
        # skips IRS. Just centering for batch baseline.
        print(f"  labeled branch v0: no imputation, no IRS — only median centering")

    # Sample-level median centering (both branches)
    col_medians = expr.median(axis=0, skipna=True)
    expr = expr.subtract(col_medians, axis=1)
    print(f"  median-centered each sample column to zero")

    # Output filename: strip recognized extensions from the input basename
    base = os.path.basename(quant_path)
    for suf in (".gz",):
        if base.lower().endswith(suf):
            base = base[: -len(suf)]
    for suf in (".mztab", ".csv", ".tsv", ".txt", ".xlsx", ".xls"):
        if base.lower().endswith(suf):
            base = base[: -len(suf)]
    out_path = os.path.join(output_dir, f"{base}_preprocessed.csv")
    expr.to_csv(out_path)

    n_features_out = len(expr)
    n_missing_out = int(expr.isna().sum().sum())
    return (
        f"preprocess_proteomics_matrix complete | labeling={labeling}\n"
        f"Input:  {n_features_in} features x {n_samples} samples ({pct_missing_in:.1%} missing)\n"
        f"Output: {n_features_out} features x {n_samples} samples ({n_missing_out} missing)\n"
        f"  filtered (LFQ missingness): {n_filtered}\n"
        f"  imputed (LFQ MinProb):     {n_imputed_total}\n"
        f"Output file: {out_path}\n"
        f"Next step: hand to run_limma_analysis as `normalized_csv` (already log-scale)."
    )
