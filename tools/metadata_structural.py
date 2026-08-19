"""Deterministic derivation of the SEA-CDM structural child tables
(subject / sample / groups / assay) from a GEO metadata CSV.

WHY THIS EXISTS (req #3 — "重复跑 SEA-CDM 看 json 是否一致").
The v1 extractor asks an LLM to read a paper's free text and emit lists of
subjects / samples / groups / assays. Even at temperature=0 the model emits a
DIFFERENT NUMBER of rows each run — on the same paper (GSE208615) three runs
produced subject [1,1,4], sample [2,7,7], groups [6,6,21], assay [3,1,1]. So the
13-table JSON's *shape* is not reproducible run-to-run, which is exactly what #3
flags.

But those four tables describe the study's ACTUAL SAMPLES, and GEO already ships
that as a structured, per-sample table:

    data/{accession}/{accession}_metadata.csv          (GEOparse phenotype_data)

— one row per GSM with stable column conventions:
    organism_ch1, taxid_ch1, source_name_ch1, molecule_ch1, extract_protocol_ch1,
    characteristics_ch1.N.<label>  (Sex / age / strain / treatment / time / ...),
    instrument_model, library_strategy, library_source, library_selection, title.

Reading that CSV with pandas and grouping it is a PURE FUNCTION of the file:
same input -> byte-identical rows / ids / order every run. So for these four
tables we replace the LLM's run-varying guess with a deterministic read of the
ground truth. Counts, values, ids and ordering are all reproducible.

SCOPE. Only subject / sample / groups / assay — the per-sample structural facts
that live in the metadata. study / experiment / documentation / material /
interventions stay LLM-text-derived (they are not per-sample and/or not present
in the metadata). The experiment table is already pinned to exactly one row
upstream (flatten_extraction), so experiment + these four = the deterministic
structural skeleton; the residual run-to-run drift is confined to the
descriptive text tables (cosmetic paraphrase / reagent-list churn).

PROVENANCE. Every metadata-derived Sourced field records the metadata COLUMN it
came from, prefixed with `META_SOURCE_PREFIX` (e.g.
"GEO metadata: organism_ch1"). This is honest structured provenance, not a
verbatim paper quote, so verify_provenance() in seacdm_tools exempts any source
starting with that prefix from the paper-substring check.
"""

import os
import re
from typing import Optional

import pandas as pd

from tools.sea_cdm_schema import csv_columns


META_SOURCE_PREFIX = "GEO metadata:"


# --- column-role detection (deterministic, by GEO naming convention) -------------------

# Columns that are never grouping axes (ids / dates / contact / counts). Skipped when
# scoring the design column so they can't accidentally become "groups".
_DENY_COLS = {
    "geo_accession", "status", "submission_date", "last_update_date", "type",
    "channel_count", "taxid_ch1", "data_row_count", "platform_id", "series_id",
    "relation", "molecule_ch1", "extract_protocol_ch1", "data_processing",
    "instrument_model", "library_selection", "library_source", "library_strategy",
    "supplementary_file_1", "supplementary_file", "organism_ch1",
}

# Label tokens that mark a column as an experimental design / treatment axis.
_DESIGN_WORDS = (
    "treatment", "condition", "time", "timepoint", "time point", "group", "dose",
    "dosage", "exercise", "training", "intervention", "stimulus", "diet", "agent",
    "drug", "protocol", "duration", "exposure", "regimen", "infection", "stimulation",
    "genotype", "phenotype", "disease", "status", "arm", "challenge", "knockout",
)
# Label tokens that mark a column as a per-organism DESCRIPTOR (subject fields), not an arm.
_DESCRIPTOR_WORDS = (
    "sex", "gender", "age", "stage", "strain", "background", "species", "organism",
    "tissue", "race", "ethnicity", "ancestry", "breed", "cell type", "cell line",
)

_AGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([A-Za-z].*)?$")


def _nonblank(v) -> bool:
    if v is None:
        return False
    if isinstance(v, float) and pd.isna(v):
        return False
    s = str(v).strip()
    return s != "" and s.lower() != "nan"


def _norm(v) -> Optional[str]:
    return str(v).strip() if _nonblank(v) else None


def _char_label(col) -> str:
    """'characteristics_ch1.2.exercise parameters' -> 'exercise parameters'; '' for non-char cols."""
    c = str(col)
    if c.lower().startswith("characteristics"):
        return c.split(".")[-1].strip().lower()
    return ""


def _parse_age(v):
    """'8 weeks' -> ('8','weeks'); '8' -> ('8', None); 'adult' -> ('adult', None)."""
    if not _nonblank(v):
        return (None, None)
    s = str(v).strip()
    m = _AGE_RE.match(s)
    if m:
        return (m.group(1), (m.group(2).strip() if m.group(2) else None))
    return (s, None)


def _load_metadata(path) -> pd.DataFrame:
    """Read GEO metadata as all-string (no NA coercion so '1'/'2'/'0-0-0' survive), GSM-indexed,
    deduped on index. keep_default_na=False makes empty cells '' (treated as blank by _nonblank)."""
    df = pd.read_csv(path, index_col=0, dtype=str, keep_default_na=False)
    df.index = df.index.astype(str)
    df = df[~df.index.duplicated(keep="first")]
    return df.sort_index(kind="stable")


def _resolve_roles(df: pd.DataFrame) -> dict:
    cols = list(df.columns)
    low = {c: str(c).lower() for c in cols}

    def find_std(*names):
        for c in cols:
            if low[c] in names:
                return c
        return None

    def find_contains(*subs):
        # prefer a characteristics column whose LABEL matches, then any column name match
        for c in cols:
            lbl = _char_label(c)
            if lbl and any(s in lbl for s in subs):
                return c
        for c in cols:
            if any(s in low[c] for s in subs):
                return c
        return None

    return {
        "species": find_std("organism_ch1", "organism") or find_contains("organism", "species"),
        "source_name": find_std("source_name_ch1", "source_name"),
        "molecule": find_std("molecule_ch1", "molecule"),
        "extract_protocol": find_std("extract_protocol_ch1", "extract_protocol"),
        "instrument": find_std("instrument_model") or find_contains("instrument"),
        "library_strategy": find_std("library_strategy"),
        "library_source": find_std("library_source"),
        "library_selection": find_std("library_selection"),
        "platform_id": find_std("platform_id"),
        "sample_type": find_std("type"),
        "label_protocol": find_std("label_protocol_ch1", "label_protocol"),
        "hyb_protocol": find_std("hyb_protocol"),
        "scan_protocol": find_std("scan_protocol"),
        "data_processing": find_std("data_processing"),
        "description": find_std("description"),
        "title": find_std("title"),
        "sex": find_contains("sex", "gender"),
        "age": find_contains("age", "developmental stage", "dev stage", "stage"),
        "lineage": find_contains("strain", "genotype", "background", "lineage", "cell line", "subtype"),
        "race": find_contains("race", "ethnicity", "ancestry", "breed", "population"),
        "tissue": find_contains("tissue", "cell type", "organ"),
    }


def summarize_geo_scope(metadata_csv: str, max_values: int = 6) -> str:
    """Return a compact deterministic description of the target GEO accession's samples.

    This is prompt context, not a scientific inference. It intentionally contains only GEO
    metadata so a paper-wide extractor can exclude independent validation cohorts.
    """
    df = _load_metadata(metadata_csv)
    if df.empty:
        raise ValueError(f"metadata CSV has no rows: {metadata_csv}")
    roles = _resolve_roles(df)
    selected = []
    preferred = (
        roles.get("title"), roles.get("source_name"), roles.get("species"),
        roles.get("molecule"), roles.get("sample_type"), roles.get("platform_id"),
        roles.get("instrument"), roles.get("library_strategy"), roles.get("description"),
    )
    for col in preferred:
        if col and col not in selected:
            selected.append(col)
    for col in df.columns:
        if _char_label(col) and col not in selected:
            selected.append(col)

    lines = [f"GEO sample count: {len(df)}"]
    for col in selected:
        values = []
        for raw in df[col].tolist():
            value = _norm(raw)
            if not value:
                continue
            value = re.sub(r"\s+", " ", value)[:320]
            if value not in values:
                values.append(value)
        if values:
            # Do not keep only the first N values: GEO rows are commonly sorted by arm, so the
            # first six titles can all be controls and hide the exercise arm at the end. Sample
            # evenly across the ordered unique values while keeping the prompt compact.
            if len(values) > max_values:
                indices = [round(i * (len(values) - 1) / (max_values - 1))
                           for i in range(max_values)] if max_values > 1 else [0]
                values = [values[index] for index in dict.fromkeys(indices)]
            lines.append(f"{col}: " + " | ".join(values))
    return "\n".join(lines)


def _infer_assay_name(rec: dict, roles: dict) -> tuple[str, str]:
    """Infer an assay label when GEO omits ``library_strategy``.

    Microarray series often have no instrument/library-strategy columns. Calling them
    high-throughput sequencing is wrong; hybridization/CEL/Affymetrix metadata provides a
    deterministic basis for a conservative microarray label.
    """
    strategy_col = roles.get("library_strategy")
    strategy = _norm(rec.get(strategy_col)) if strategy_col else None
    if strategy:
        return strategy, strategy_col

    evidence_cols = [
        roles.get("platform_id"), roles.get("sample_type"), roles.get("label_protocol"),
        roles.get("hyb_protocol"), roles.get("scan_protocol"), roles.get("data_processing"),
        roles.get("description"),
    ]
    text = " ".join(str(rec.get(col) or "") for col in evidence_cols if col).lower()
    if any(term in text for term in (
        "affymetrix", "microarray", "hybridization", "hybridisation", ".cel", " cel ",
        "genechip", "beadchip", "agilent array",
    )):
        source = ";".join(col for col in evidence_cols if col and _nonblank(rec.get(col)))
        return "microarray gene expression profiling", source
    return "high-throughput sequencing", ""


def _pick_design_column(df: pd.DataFrame, exclude: set) -> Optional[str]:
    """Deterministically choose THE single design/treatment column whose distinct values become the
    `groups` arms. Pure function of the dataframe (no LLM, no randomness). Scoring:
      base 1 for any column with 2 <= distinct < n (varies, not an id)
      +2 if its label/name contains a design word (treatment/time/exercise/dose/...)
      -1 if it is a pure descriptor (sex/age/strain/...) and NOT a design word
      +1 if the arms are reasonably balanced (max/min group size <= 4)
      -2 if it is not a characteristics/title/source/treatment/group/condition column
    Ties -> more distinct values (richer stratification) -> earlier column. Returns None if nothing
    scores >= 1 (single-group study)."""
    n = len(df)
    best = None  # (score, n_distinct, -order, col)
    for order, col in enumerate(df.columns):
        low = str(col).lower()
        if col in exclude or low in _DENY_COLS or low.startswith("contact_"):
            continue
        series = df[col].astype(str)
        series = series[series.map(_nonblank)]
        vals = sorted(series.unique().tolist())
        k = len(vals)
        if k < 2 or k >= n:                       # constant, or all-unique (an id)
            continue
        if k > max(2, int(n * 0.8)):              # mostly-unique -> replicate/id label
            continue

        label = _char_label(col) or low
        has_design = any(w in label for w in _DESIGN_WORDS)
        has_descr = any(w in label for w in _DESCRIPTOR_WORDS)
        score = 1
        if has_design:
            score += 2
        if has_descr and not has_design:
            score -= 1
        sizes = series.value_counts()
        if int(sizes.min()) >= 2 and (sizes.max() / sizes.min()) <= 4:
            score += 1
        if not (low.startswith("characteristics") or "title" in low or "source" in low
                or "treatment" in low or "group" in low or "condition" in low):
            score -= 2

        cand = (score, k, -order, col)
        if best is None or cand > best:
            best = cand
    return best[3] if best and best[0] >= 1 else None


def _title_design_series(df: pd.DataFrame, title_col: Optional[str]) -> Optional[pd.Series]:
    """Recover balanced arms from titles that differ only by a replicate-number suffix."""
    if not title_col:
        return None
    values = df[title_col].astype(str).map(
        lambda value: re.sub(
            r"(?i)[\s_-]*(?:rep(?:licate)?[\s_-]*)?\d+$", "", value.strip()
        ).strip(" _-")
    )
    values = values[values.map(_nonblank)]
    k = values.nunique()
    if k < 2 or k >= len(df) or k > max(12, int(len(df) * 0.5)):
        return None
    sizes = values.value_counts()
    if int(sizes.min()) < 2 or (sizes.max() / sizes.min()) > 4:
        return None
    return values


# --- row helpers -----------------------------------------------------------------------

def _srow(row: dict, field: str, value, col) -> None:
    """Set a Sourced field's two keys: <field> = value, <field>_source = 'GEO metadata: <col>'.
    Source is None when the value is blank or no source column applies (convention constants)."""
    val = _norm(value)
    row[field] = val
    row[f"{field}_source"] = f"{META_SOURCE_PREFIX} {col}" if (val is not None and col) else None


def _order_row(table: str, row: dict) -> dict:
    return {c: row.get(c) for c in csv_columns(table)}


def _subject_descriptors(rec: dict, roles: dict) -> dict:
    age, age_unit = _parse_age(rec.get(roles["age"])) if roles["age"] else (None, None)
    return {
        "subject_type": "Organism",
        "species": _norm(rec.get(roles["species"])) if roles["species"] else None,
        "sex": _norm(rec.get(roles["sex"])) if roles["sex"] else None,
        "age": _norm(age),
        "age_unit": _norm(age_unit),
        "lineage": _norm(rec.get(roles["lineage"])) if roles["lineage"] else None,
        "race": _norm(rec.get(roles["race"])) if roles["race"] else None,
    }


def _subject_key(d: dict) -> tuple:
    return (d["species"], d["sex"], d["age"], d["age_unit"], d["lineage"], d["race"], d["subject_type"])


# --- main builder ----------------------------------------------------------------------

def build_structural_tables(
    study_id: str,
    experiment_id: str,
    metadata_csv: str,
    report: Optional[dict] = None,
) -> dict:
    """Deterministically derive {subject, sample, groups, assay} rows (each already ordered to its
    csv_columns) from a GEO metadata CSV. Raises on unreadable/empty metadata so the caller can fall
    back to the LLM tables.

    FK wiring (schema convention):
        subject_id = {experiment_id}_subj{n}   (n by first appearance of a distinct organism)
        sample_id  = {experiment_id}_samp{n}   (n by sorted GSM)
        group_id   = {study_id}_grp{n}         (n by sorted distinct design value)
        assay_id   = {experiment_id}_assay{n}  (n by sorted (instrument, strategy))
        sample.organism_id -> subject_id (the lone subject if 1, else the matching organism, else '0')
        sample.group_id, subject.group_id -> groups (subject spans arms => None)
    """
    df = _load_metadata(metadata_csv)
    if df.empty:
        raise ValueError(f"metadata CSV has no rows: {metadata_csv}")
    roles = _resolve_roles(df)
    gsms = list(df.index.astype(str))
    records = df.to_dict("index")
    n = len(gsms)

    # ---- groups: distinct values of the single best design column ----
    design_col = _pick_design_column(df, exclude=set(filter(None, [roles["title"]])))
    design_series = df[design_col].astype(str) if design_col is not None else None
    design_source = design_col
    if design_col is None:
        title_series = _title_design_series(df, roles["title"])
        if title_series is not None:
            design_col = roles["title"]
            design_series = title_series
            design_source = f"{design_col} (replicate suffix normalized)"
    groups_rows, val_to_gid = [], {}
    if design_col is not None:
        series = design_series
        series = series[series.map(_nonblank)]
        sizes = series.value_counts()
        for i, v in enumerate(sorted(series.unique().tolist()), 1):
            gid = f"{study_id}_grp{i}"
            val_to_gid[v] = gid
            grow = {"group_id": gid, "study_id": study_id}
            _srow(grow, "subject_group", v, design_source)
            _srow(grow, "sample_group", v, design_source)
            _srow(grow, "group_size", str(int(sizes[v])), design_source)
            for f in ("min_group_age", "min_age_unit", "max_group_age", "max_age_unit", "comments"):
                _srow(grow, f, None, None)
            groups_rows.append(_order_row("groups", grow))
        single_gid = None
    else:
        # no grouping axis in metadata -> one implicit group of all samples
        single_gid = f"{study_id}_grp1"
        grow = {"group_id": single_gid, "study_id": study_id}
        _srow(grow, "subject_group", "all samples", f"(no design column; {n} samples)")
        _srow(grow, "sample_group", "all samples", f"(no design column; {n} samples)")
        _srow(grow, "group_size", str(n), f"(no design column; {n} samples)")
        for f in ("min_group_age", "min_age_unit", "max_group_age", "max_age_unit", "comments"):
            _srow(grow, f, None, None)
        groups_rows.append(_order_row("groups", grow))

    # ---- subjects: one row per distinct organism descriptor combination ----
    subj_key_to_id, subject_rows = {}, []
    for gsm in gsms:                       # gsms already sorted -> deterministic numbering
        d = _subject_descriptors(records[gsm], roles)
        key = _subject_key(d)
        if key in subj_key_to_id:
            continue
        sid = f"{experiment_id}_subj{len(subj_key_to_id) + 1}"
        subj_key_to_id[key] = sid
        srow = {"subject_id": sid, "experiment_id": experiment_id, "group_id": None}
        _srow(srow, "subject_type", d["subject_type"], roles["species"])
        _srow(srow, "species", d["species"], roles["species"])
        _srow(srow, "organism_race", d["race"], roles["race"])
        _srow(srow, "subject_lineage", d["lineage"], roles["lineage"])
        _srow(srow, "organism_age", d["age"], roles["age"])
        _srow(srow, "organism_age_unit", d["age_unit"], roles["age"])
        _srow(srow, "organism_sex", d["sex"], roles["sex"])
        _srow(srow, "comments", None, None)
        subject_rows.append(_order_row("subject", srow))

    one_subject = len(subj_key_to_id) == 1
    lone_sid = next(iter(subj_key_to_id.values())) if one_subject else None

    # ---- samples: one row per GSM ----
    sample_rows = []
    biosample_col = roles["source_name"] or roles["tissue"]
    for i, gsm in enumerate(gsms, 1):
        rec = records[gsm]
        if one_subject:
            org = lone_sid
        else:
            org = subj_key_to_id.get(_subject_key(_subject_descriptors(rec, roles)), "0")
        gfk = single_gid
        if design_col is not None:
            dv = str(design_series.loc[gsm])
            gfk = val_to_gid.get(dv) if _nonblank(dv) else None
        samprow = {"sample_id": f"{experiment_id}_samp{i}", "organism_id": org, "group_id": gfk}
        _srow(samprow, "biosample_collection", rec.get(roles["extract_protocol"]) if roles["extract_protocol"] else None,
              roles["extract_protocol"])
        biosample = rec.get(biosample_col) if biosample_col else None
        _srow(samprow, "biosample_type", biosample, biosample_col)
        _srow(samprow, "expsample_type", rec.get(roles["molecule"]) if roles["molecule"] else None, roles["molecule"])
        title = _norm(rec.get(roles["title"])) if roles["title"] else None
        comment = f"GSM {gsm}" + (f"; title {title}" if title else "")
        _srow(samprow, "comments", comment, "geo_accession" + (";title" if title else ""))
        sample_rows.append(_order_row("sample", samprow))

    # ---- assays: one row per distinct (instrument, library_strategy) ----
    inst_col, strat_col = roles["instrument"], roles["library_strategy"]
    combos = {}
    for gsm in gsms:
        rec = records[gsm]
        inst = _norm(rec.get(inst_col)) if inst_col else None
        strat = _norm(rec.get(strat_col)) if strat_col else None
        combos.setdefault((inst or "", strat or ""), []).append(gsm)
    assay_rows = []
    for i, key in enumerate(sorted(combos), 1):
        inst, strat = key
        rec0 = records[combos[key][0]]
        arow = {"assay_id": f"{experiment_id}_assay{i}", "experiment_id": experiment_id,
                "documentation_id": None, "organism_input": "true"}
        assay_name, assay_source = _infer_assay_name(rec0, roles)
        _srow(arow, "assay_name", assay_name, assay_source)
        _srow(arow, "assay_type", "Experimental Assay", "")        # SEA-CDM convention -> no source
        reagents = []
        for rc in (roles["molecule"], roles["library_selection"], roles["library_source"]):
            if rc and _nonblank(rec0.get(rc)):
                reagents.append(str(rec0.get(rc)).strip())
        reagents = "; ".join(dict.fromkeys(reagents)) or None
        _srow(arow, "reagents", reagents, "molecule_ch1;library_selection;library_source")
        _srow(arow, "platform", inst or None, inst_col or "")
        assay_rows.append(_order_row("assay", arow))

    out = {"subject": subject_rows, "sample": sample_rows,
           "groups": groups_rows, "assay": assay_rows}
    if report is not None:
        report.update({
            "metadata_csv": metadata_csv,
            "n_samples": n,
            "design_column": design_source,
            "n_subject": len(subject_rows), "n_sample": len(sample_rows),
            "n_groups": len(groups_rows), "n_assay": len(assay_rows),
        })
    return out
