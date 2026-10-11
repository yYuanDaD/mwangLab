"""Plain-function runtime for agent sessions that run the workflow skill natively.

A native session (Codex, Claude Code, or another agent that loads the
``bioinformatics-workflow`` skill) makes every scientific decision itself and
uses this module for deterministic checks, tool execution, and record keeping:

- ``enable_native_mode`` blocks hidden external LLM calls inside repository tools.
- ``profile_matrix``, ``align_to_metadata``, ``design_check``,
  ``confounding_report``, ``pairing_report`` summarize evidence; they never decide.
- ``call_tool`` runs a repository tool as a plain function and raises on failure.
- ``apply_threshold`` applies a stated threshold to a full results table.
- ``RunRecorder`` writes the standard run layout that ``audit_run.py`` and the
  decision-contract validator read.

Only pandas, numpy, and (for RunRecorder) pydantic are imported here.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd

from tools import decision_contract
from tools.analysis_policy import LOG_SCALE_MAX, RAW_INTEGER_FRACTION, PolicyViolation, numeric_matrix
from tools.analysis_policy import profile_matrix as _profile

NATIVE_ENV = "BIOAGENT_DISABLE_EXTERNAL_LLM"
# Repository tools report failure in their return text. These patterns cover the
# leading line of every failure message they currently produce.
_FAILURE_PATTERNS = (
    re.compile(r"^\s*(fatal error|policy blocked|error)\b", re.I),
    re.compile(r"\b(failed|aborted|unavailable)\b", re.I),
    re.compile(r"^\s*(only \d+ |no pseudobulk|this file looks like|no obvious grouping)", re.I),
)
GATES = ("paper_reconstruction", "ownership", "alignment", "matrix", "design",
         "covariance", "method", "threshold", "execution", "study")
SUMMARY_COLUMNS = (
    "case_id", "accession", "status", "decision_status", "execution_status", "stop_stage",
    "stop_reason", "route", "matrix_type", "da_method", "design_col", "formula", "control",
    "treatment", "n_contrasts", "covariance_status", "blocking_terms", "threshold_source",
    "applied_threshold", "n_deg", "deg_sanity",
)
REPO_ROOT = Path(__file__).resolve().parents[1]


class NativeToolError(RuntimeError):
    """A repository tool or a native check refused or failed."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


# ---------------------------------------------------------------- native mode

def enable_native_mode() -> dict:
    """Block every external LLM client created by repository tools in this process."""
    os.environ[NATIVE_ENV] = "1"
    return external_llm_status()


def external_llm_status() -> dict:
    disabled = os.environ.get(NATIVE_ENV, "").strip().lower() in {"1", "true", "yes", "on"}
    try:
        from tools.model_factory import blocked_external_llm_attempts
    except ImportError as exc:  # python-dotenv missing: nothing can create a client either
        return {"disabled": disabled, "blocked_attempts": [], "note": f"model_factory unavailable: {exc}"}
    return {"disabled": disabled, "blocked_attempts": blocked_external_llm_attempts()}


def load_tool(spec: str) -> Any:
    """Import ``"module:function"`` (for example ``"tools.deseq2_tools:run_deseq2_analysis"``).

    A missing package becomes a NativeToolError whose text can be recorded as
    the execution_error, so a decision-only environment fails cleanly.
    """
    module_name, _, attribute = spec.partition(":")
    if not attribute:
        raise NativeToolError(f"tool spec must look like 'module:function', got {spec!r}")
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise NativeToolError(f"cannot import {module_name}: {type(exc).__name__}: {exc}. "
                              "Install the missing package (see the preflight report) and rerun.") from exc
    try:
        return getattr(module, attribute)
    except AttributeError as exc:
        raise NativeToolError(f"{module_name} has no {attribute!r}") from exc


def call_tool(tool: Any, **kwargs) -> Any:
    """Run a repository tool and fail loudly.

    ``tool`` is a LangChain ``@tool``, a plain function, or a ``"module:function"``
    string (preferred: an import failure then raises NativeToolError too).
    Raises NativeToolError when native mode is off, when the tool returns an
    error string, or when the tool tried to reach an external LLM.
    """
    if os.environ.get(NATIVE_ENV) != "1":
        raise NativeToolError("call enable_native_mode() before running repository tools")
    if isinstance(tool, str):
        tool = load_tool(tool)
    function = getattr(tool, "func", None) or tool
    before = len(external_llm_status()["blocked_attempts"])
    try:
        result = function(**kwargs)
    except PolicyViolation as exc:
        raise NativeToolError(f"POLICY BLOCKED: {exc}") from exc
    attempts = external_llm_status()["blocked_attempts"][before:]
    if attempts:
        raise NativeToolError(
            f"{getattr(function, '__name__', 'tool')} tried to call an external LLM "
            f"(blocked: {attempts}). Resolve the input it needed, for example by aligning sample IDs "
            "with align_to_metadata first.")
    if isinstance(result, str) and tool_failed(result):
        raise NativeToolError(result.strip())
    return result


def tool_failed(message: str) -> bool:
    """True when a repository tool's return text reports a failure or refusal."""
    first_line = message.strip().splitlines()[0] if message.strip() else ""
    return any(pattern.search(first_line) for pattern in _FAILURE_PATTERNS)


# ---------------------------------------------------------------- evidence summaries

def read_table(path: str | Path) -> pd.DataFrame:
    """Read a CSV/TSV (optionally gzipped) with the first column as index."""
    return pd.read_csv(path, index_col=0, sep=None, engine="python")


def _frame(metadata: pd.DataFrame | str | Path) -> pd.DataFrame:
    if isinstance(metadata, pd.DataFrame):
        frame = metadata.copy()
    else:
        frame = pd.read_csv(metadata, index_col=0)
    frame.index = frame.index.astype(str)
    return frame


def profile_matrix(path: str | Path, sample_columns: Sequence[str] | None = None) -> dict:
    """Describe the numeric profile of a matrix and list type candidates, without choosing."""
    raw = read_table(path)
    numeric = numeric_matrix(raw, label=str(path))
    if sample_columns is not None:
        numeric = numeric.loc[:, [c for c in numeric.columns if str(c) in set(map(str, sample_columns))]]
    profile = _profile(numeric)
    values = numeric.to_numpy(dtype=float)
    finite = values[np.isfinite(values)]
    candidates = []
    if profile.min_value >= 0 and profile.integer_fraction >= RAW_INTEGER_FRACTION:
        candidates.append("raw_counts (confirm against provenance: normalized integers and "
                          "rounded estimated counts look the same)")
    if profile.min_value >= 0 and profile.max_value <= 1:
        candidates.append("methylation_beta_or_proportion")
    if profile.integer_fraction < RAW_INTEGER_FRACTION and profile.min_value >= 0 \
            and profile.max_value > LOG_SCALE_MAX:
        candidates.append("linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts")
    negative_fraction = float((finite < 0).mean()) if finite.size else 0.0
    median = float(np.median(finite)) if finite.size else 0.0
    if profile.max_value <= LOG_SCALE_MAX:
        if profile.min_value >= 0 or (negative_fraction < 0.01 and median > 1):
            candidates.append("log_scale" + ("" if profile.min_value >= 0 else
                              " (a few small negative values, as in RMA or background-corrected arrays)"))
        else:
            candidates.append("signed_log_scale (log ratios, M-values, or centered data)")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "n_features": profile.n_features,
        "n_samples": profile.n_samples,
        "sample_columns": [str(c) for c in numeric.columns],
        "annotation_columns_dropped": [str(c) for c in raw.columns if c not in numeric.columns],
        "duplicated_feature_ids": int(numeric.index.duplicated().sum()),
        "missing_values": int(values.size - finite.size),
        "negative_values": int((finite < 0).sum()),
        "negative_fraction": round(negative_fraction, 6),
        "min": profile.min_value,
        "max": profile.max_value,
        "median": median if finite.size else None,
        "integer_fraction": round(profile.integer_fraction, 4),
        "candidates": candidates,
        "note": "Candidates only. Decide the matrix type from these values together with the file "
                "name, platform, and processing notes, and record the evidence.",
    }


def align_to_metadata(matrix_path: str | Path, metadata_path: str | Path, out_dir: str | Path, *,
                      key_column: str | None = None) -> dict:
    """Exact, auditable alignment of matrix columns to metadata sample IDs.

    Matches matrix columns to the metadata index, or to ``key_column`` (for
    example ``title``) when the matrix uses author labels. Never matches by
    position or substring. Writes ``aligned_matrix.csv`` (columns renamed to the
    metadata sample IDs), ``aligned_metadata.csv``, and ``alignment_map.csv``.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw = read_table(matrix_path)
    numeric = numeric_matrix(raw, label=str(matrix_path))
    meta = _frame(metadata_path)
    if key_column is None:
        lookup = {sample: sample for sample in meta.index}
        method = "exact:metadata_index"
    else:
        if key_column not in meta.columns:
            raise NativeToolError(f"key column {key_column!r} not in metadata columns {list(meta.columns)}")
        keys = meta[key_column].astype(str)
        duplicated = sorted(set(keys[keys.duplicated()]))
        if duplicated:
            raise NativeToolError(f"key column {key_column!r} is not unique: {duplicated[:10]}")
        lookup = dict(zip(keys, meta.index))
        method = f"exact:{key_column}"
    mapping = {str(col): lookup[str(col)] for col in numeric.columns if str(col) in lookup}
    if not mapping:
        raise NativeToolError("no matrix column matched the metadata exactly; choose key_column "
                              "or record the alignment as unresolved")
    ordered = [sample for sample in meta.index if sample in set(mapping.values())]
    inverse = {sample: col for col, sample in mapping.items()}
    aligned = numeric.loc[:, [inverse[s] for s in ordered]]
    aligned.columns = ordered
    aligned_meta = meta.loc[ordered]
    paths = {
        "aligned_matrix": out / "aligned_matrix.csv",
        "aligned_metadata": out / "aligned_metadata.csv",
        "alignment_map": out / "alignment_map.csv",
    }
    aligned.to_csv(paths["aligned_matrix"])
    aligned_meta.to_csv(paths["aligned_metadata"])
    pd.DataFrame({"matrix_column": [inverse[s] for s in ordered], "sample_id": ordered,
                  "method": method}).to_csv(paths["alignment_map"], index=False)
    return {
        "method": method,
        "n_matrix_columns": int(numeric.shape[1]),
        "n_metadata": int(len(meta)),
        "n_aligned": len(ordered),
        "coverage": round(len(ordered) / len(meta), 4) if len(meta) else 0.0,
        "unmatched_matrix_columns": [str(c) for c in numeric.columns if str(c) not in mapping],
        "unmatched_metadata_samples": [s for s in meta.index if s not in set(ordered)],
        "annotation_columns_dropped": [str(c) for c in raw.columns if c not in numeric.columns],
        "outputs": {name: {"path": str(p), "sha256": sha256(p)} for name, p in paths.items()},
    }


def derive_columns(metadata_csv: str | Path, out_csv: str | Path, *,
                   aliases: dict[str, str] | None = None,
                   patterns: dict[str, tuple[str, str]] | None = None,
                   recode: dict[str, dict[str, str]] | None = None) -> dict:
    """Write a metadata copy with short, formula-safe columns, and return the mapping.

    GEO columns such as ``characteristics_ch1.1.time point`` cannot be used in a
    patsy formula. Use this before any formula-based step:

    - ``aliases``: ``{"subject": "characteristics_ch1.0.subject"}`` copies a column.
    - ``patterns``: ``{"grp": ("title", r"soleus_(.+)_rep")}`` extracts a regex group.
    - ``recode``: ``{"grp": {"sedentary_control": "sed", ...}}`` maps values of a new
      column to safe labels; every value must be mapped.

    Raises when a source column is missing, a pattern does not match every row,
    or a recode leaves a value unmapped. Never guesses a label.
    """
    meta = _frame(metadata_csv)
    record: dict[str, Any] = {"source": str(metadata_csv), "columns": {}}
    for new, source in (aliases or {}).items():
        if source not in meta.columns:
            raise NativeToolError(f"alias source column {source!r} not in metadata")
        meta[new] = meta[source]
        record["columns"][new] = {"alias_of": source}
    for new, (source, pattern) in (patterns or {}).items():
        if source not in meta.columns:
            raise NativeToolError(f"pattern source column {source!r} not in metadata")
        extracted = meta[source].astype(str).str.extract(pattern, expand=False)
        if extracted.isna().any():
            missing = meta.index[extracted.isna()].tolist()[:5]
            raise NativeToolError(f"pattern {pattern!r} did not match every row of {source!r}: {missing}")
        meta[new] = extracted
        record["columns"][new] = {"source": source, "regex": pattern}
    for column, mapping in (recode or {}).items():
        if column not in meta.columns:
            raise NativeToolError(f"recode column {column!r} not in metadata")
        unmapped = sorted(set(meta[column].astype(str)) - set(mapping))
        if unmapped:
            raise NativeToolError(f"recode for {column!r} leaves values unmapped: {unmapped}")
        meta[column] = meta[column].astype(str).map(mapping)
        record["columns"].setdefault(column, {})["recode"] = mapping
    for new in record["columns"]:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", new):
            raise NativeToolError(f"derived column name {new!r} is not formula-safe")
    out = Path(out_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta.to_csv(out)
    record.update(output=str(out), sha256=sha256(out),
                  levels={c: meta[c].astype(str).value_counts().to_dict() for c in record["columns"]})
    return record


def design_check(metadata: pd.DataFrame | str | Path, terms: Sequence[str],
                 interactions: Iterable[tuple[str, str]] = (),
                 samples: Sequence[str] | None = None) -> dict:
    """Rank, residual df, and cell sizes of a categorical design. No model is fitted.

    Every term is treated as categorical with treatment coding plus an intercept,
    the same column space as ``~ C(a) + C(b) + C(a):C(b)``.
    """
    meta = _frame(metadata)
    if samples is not None:
        meta = meta.loc[[str(s) for s in samples]]
    missing_columns = [t for t in terms if t not in meta.columns]
    if missing_columns:
        raise NativeToolError(f"design terms not in metadata: {missing_columns}")
    missing_values = {t: int(meta[t].isna().sum()) for t in terms if meta[t].isna().any()}
    blocks = [pd.DataFrame({"Intercept": np.ones(len(meta))}, index=meta.index)]
    dummies = {}
    for term in terms:
        dummies[term] = pd.get_dummies(meta[term].astype(str), prefix=term, drop_first=True, dtype=float)
        blocks.append(dummies[term])
    interactions = [tuple(pair) for pair in interactions]
    for left, right in interactions:
        for a in dummies[left].columns:
            for b in dummies[right].columns:
                blocks.append(pd.DataFrame({f"{a}:{b}": dummies[left][a] * dummies[right][b]}))
    design = pd.concat(blocks, axis=1)
    rank = int(np.linalg.matrix_rank(design.to_numpy(dtype=float)))
    cells = meta.groupby([meta[t].astype(str) for t in terms]).size()
    formula = "~ " + " + ".join(f"C({t})" for t in terms)
    formula += "".join(f" + C({a}):C({b})" for a, b in interactions)
    return {
        "formula_equivalent": formula,
        "n_samples": int(len(meta)),
        "n_columns": int(design.shape[1]),
        "columns": list(design.columns),
        "rank": rank,
        "full_rank": rank == design.shape[1],
        "residual_df": int(len(meta) - rank),
        "levels": {t: meta[t].astype(str).value_counts().to_dict() for t in terms},
        "cells": [{"cell": list(k) if isinstance(k, tuple) else [k], "n": int(v)} for k, v in cells.items()],
        "min_cell_size": int(cells.min()) if len(cells) else 0,
        "missing_values": missing_values,
    }


def confounding_report(metadata: pd.DataFrame | str | Path, primary: str,
                       candidates: Sequence[str] | None = None,
                       samples: Sequence[str] | None = None) -> list[dict]:
    """How every candidate covariate relates to the primary factor.

    Status values: ``constant``, ``sample_identifier``, ``complete_confounding``
    (one-to-one with the primary factor), ``nested_in_primary`` (for example
    animals nested in arms), ``primary_nested_in_candidate`` (contrasts across
    candidate levels are confounded), or ``crossed``.
    """
    meta = _frame(metadata)
    if samples is not None:
        meta = meta.loc[[str(s) for s in samples]]
    if primary not in meta.columns:
        raise NativeToolError(f"primary factor {primary!r} not in metadata")
    columns = list(candidates) if candidates is not None else [c for c in meta.columns if c != primary]
    report = []
    for column in columns:
        values = meta[column].astype(str)
        n_levels = int(values.nunique())
        if n_levels <= 1:
            status = "constant"
        elif n_levels == len(meta):
            status = "sample_identifier"
        else:
            table = pd.crosstab(values, meta[primary].astype(str)) > 0
            candidate_in_one = bool((table.sum(axis=1) == 1).all())
            primary_in_one = bool((table.sum(axis=0) == 1).all())
            status = ("complete_confounding" if candidate_in_one and primary_in_one else
                      "nested_in_primary" if candidate_in_one else
                      "primary_nested_in_candidate" if primary_in_one else "crossed")
        entry = {"column": str(column), "n_levels": n_levels, "status": status}
        if status not in {"constant", "sample_identifier"}:
            entry["crosstab"] = pd.crosstab(values, meta[primary].astype(str)).to_dict()
        report.append(entry)
    return report


def pairing_report(metadata: pd.DataFrame | str | Path, subject_column: str, condition_column: str,
                   levels: Sequence[str], samples: Sequence[str] | None = None) -> dict:
    """Which subjects have exactly one sample at every level of the condition."""
    meta = _frame(metadata)
    if samples is not None:
        meta = meta.loc[[str(s) for s in samples]]
    for column in (subject_column, condition_column):
        if column not in meta.columns:
            raise NativeToolError(f"column {column!r} not in metadata")
    levels = [str(x) for x in levels]
    subset = meta[meta[condition_column].astype(str).isin(levels)]
    counts = pd.crosstab(subset[subject_column].astype(str), subset[condition_column].astype(str))
    counts = counts.reindex(columns=levels, fill_value=0)
    complete = counts.index[(counts == 1).all(axis=1)].tolist()
    duplicated = counts.index[(counts > 1).any(axis=1)].tolist()
    incomplete = counts.index[(counts == 0).any(axis=1) & ~(counts > 1).any(axis=1)].tolist()
    return {
        "subject_column": subject_column,
        "condition_column": condition_column,
        "levels": levels,
        "n_subjects": int(len(counts)),
        "n_complete": len(complete),
        "complete_subjects": complete,
        "incomplete_subjects": incomplete,
        "duplicated_subjects": duplicated,
        "repeated_across_levels": bool(len(complete) > 0),
        "complete_and_unique": not incomplete and not duplicated and len(complete) > 0,
    }


def log_transform(matrix_csv: str | Path, out_csv: str | Path, *, pseudocount: float = 1.0) -> dict:
    """Write log2(x + pseudocount) of a linear, non-negative matrix (for example FPKM/TPM)."""
    matrix = numeric_matrix(read_table(matrix_csv), label=str(matrix_csv))
    values = matrix.to_numpy(dtype=float)
    if np.nanmin(values) < 0:
        raise NativeToolError("log_transform needs a non-negative linear matrix; negative values found")
    if np.nanmax(values) <= LOG_SCALE_MAX:
        raise NativeToolError(f"matrix max is {np.nanmax(values):g}; it may already be log-scale. "
                              "Record the evidence and decide before transforming again.")
    out = Path(out_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.log2(matrix + pseudocount).to_csv(out)
    return {"input": str(matrix_csv), "output": str(out), "sha256": sha256(out),
            "transform": f"log2(x+{pseudocount:g})"}


def deg_outputs(output_dir: str | Path) -> list[str]:
    """Result tables written by the repository DE tools in output_dir, newest first."""
    paths = sorted(Path(output_dir).rglob("DEG_results_*.csv"), key=lambda p: p.stat().st_mtime,
                   reverse=True)
    return [str(p) for p in paths]


def apply_threshold(deg_csv: str | Path, *, metric: str = "padj", cutoff: float = 0.05,
                    effect_cutoff: float | None = None, effect_column: str | None = None,
                    inclusive: bool = False, min_group_n: int | None = None) -> dict:
    """Apply a stated threshold to a full results table. Adds no unstated cutoff.

    Repository tools print their own ``n_deg`` summaries (some at
    ``|log2FC| > 1``). Use this function, not those summaries, for any count
    that is reported under ``paper_threshold``.
    """
    table = pd.read_csv(deg_csv, index_col=0)
    options = {
        "padj": ("padj", "adj_pvalue", "adj.P.Val", "FDR", "qvalue"),
        "fdr": ("padj", "adj_pvalue", "adj.P.Val", "FDR", "qvalue"),
        "pvalue": ("pvalue", "P.Value", "PValue", "pval"),
    }
    names = options.get(metric.lower())
    if names is None:
        raise NativeToolError(f"unsupported metric {metric!r}; use padj, fdr, or pvalue")
    p_column = next((c for c in names if c in table.columns), None)
    if p_column is None:
        raise NativeToolError(f"no {metric} column in {deg_csv}; columns={list(table.columns)}")
    p = pd.to_numeric(table[p_column], errors="coerce")
    significant = (p <= cutoff) if inclusive else (p < cutoff)
    e_column = effect_column or next((c for c in ("log2FoldChange", "logFC", "log2FC") if c in table.columns), None)
    effect = pd.to_numeric(table[e_column], errors="coerce") if e_column else None
    if effect_cutoff is not None:
        if effect is None:
            raise NativeToolError("effect_cutoff given but no effect-size column found")
        significant &= (effect.abs() >= effect_cutoff) if inclusive else (effect.abs() > effect_cutoff)
    significant = significant.fillna(False)
    n_tested = int(p.notna().sum())
    n_sig = int(significant.sum())
    flags = []
    if n_tested and n_sig / n_tested > 0.5:
        flags.append(f"implausible_sig_fraction={n_sig / n_tested:.0%}({n_sig}/{n_tested})")
    if min_group_n is not None and min_group_n < 3:
        flags.append(f"tiny_n_per_group={min_group_n}")
    op = "<=" if inclusive else "<"
    rule = f"{p_column} {op} {cutoff:g}"
    if effect_cutoff is not None:
        rule += f" and |{e_column}| {'>=' if inclusive else '>'} {effect_cutoff:g}"
    return {
        "deg_csv": str(deg_csv),
        "rule": rule,
        "n_tested": n_tested,
        "n_significant": n_sig,
        "n_up": int((significant & (effect > 0)).sum()) if effect is not None else None,
        "n_down": int((significant & (effect < 0)).sum()) if effect is not None else None,
        "deg_sanity": ";".join(flags) or "ok",
    }


# ---------------------------------------------------------------- run layout

def _git_commit() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
                              text=True, check=True, timeout=10).stdout.strip()
    except Exception:
        return None


class RunRecorder:
    """Write the standard native run layout.

    <run_dir>/run_manifest.json, run_status.json, summary.csv, workflow.log
    <run_dir>/<case_id>/decisions.json, evidence.json, case_summary.json, case files

    Every decision record is checked against the decision contract when it is
    written, and every case is checked for cross-record invariants when it is
    finished, so an inconsistent record is rejected instead of saved. State is
    written to disk after every call, so a run can be continued from a later
    process with ``RunRecorder.open(run_dir)``.
    """

    def __init__(self, run_dir: str | Path, *, request: str, platform_name: str,
                 decision_maker: str, case_ids: Sequence[str] = (), _resume: bool = False):
        from tools.run_status import RunStatus, RunStatusTracker

        self.run_dir = Path(run_dir)
        manifest_path = self.run_dir / "run_manifest.json"
        if manifest_path.exists() and not _resume:
            raise NativeToolError(f"{self.run_dir} already holds a run; continue it with "
                                  "RunRecorder.open(run_dir) or choose a new directory")
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.run_id = self.run_dir.name
        self.cases: dict[str, CaseRecorder] = {}
        self._case_order = list(case_ids)
        status_path = self.run_dir / "run_status.json"
        previous_status = json.loads(status_path.read_text(encoding="utf-8")) if _resume and status_path.exists() else None
        self.tracker = RunStatusTracker(str(status_path), run_id=self.run_id, profile="native-skill",
                                        stages=GATES, study_total=len(self._case_order))
        if previous_status:
            self.tracker.state = RunStatus.model_validate(previous_status)
            self.tracker._started_monotonic -= float(previous_status.get("elapsed_seconds") or 0)
            self.tracker.state.finished_at = None
        self.tracker.start("native skill run resumed" if _resume else "native skill run started")
        if _resume:
            self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self._llm_baseline = len(external_llm_status()["blocked_attempts"])
            self._previous_attempts = list(self.manifest.get("external_llm", {}).get("blocked_attempts", []))
            self.log("run resumed")
            return
        self.manifest = {
            "run_id": self.run_id,
            "request": request,
            "platform": platform_name,
            "decision_maker": decision_maker,
            "contract_version": decision_contract.CONTRACT_VERSION,
            "case_ids": list(case_ids),
            "repo_commit": _git_commit(),
            "python": sys.version.split()[0],
            "os": platform.platform(),
            "started_at": _now(),
            "external_llm": external_llm_status(),
        }
        # The blocked-attempt ledger is process-wide; count only this run's attempts.
        self._llm_baseline = len(self.manifest["external_llm"]["blocked_attempts"])
        self._previous_attempts = []
        self.manifest["external_llm"]["blocked_attempts"] = []
        self._write_manifest()
        self.log(f"run started: {request}")

    @classmethod
    def open(cls, run_dir: str | Path) -> "RunRecorder":
        """Continue a run written by an earlier process (for example one shell call per gate)."""
        run_dir = Path(run_dir)
        manifest_path = run_dir / "run_manifest.json"
        if not manifest_path.exists():
            raise NativeToolError(f"no run to continue in {run_dir}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run = cls(run_dir, request=manifest.get("request", ""), platform_name=manifest.get("platform", ""),
                  decision_maker=manifest.get("decision_maker", ""), case_ids=manifest.get("case_ids", []),
                  _resume=True)
        for case_dir in sorted(p for p in run_dir.iterdir() if (p / "decisions.json").exists()):
            run.cases[case_dir.name] = CaseRecorder._load(run, case_dir)
            if case_dir.name not in run._case_order:
                run._case_order.append(case_dir.name)
        return run

    def _attempts(self) -> list[dict]:
        return self._previous_attempts + external_llm_status()["blocked_attempts"][self._llm_baseline:]

    def _write_manifest(self) -> None:
        (self.run_dir / "run_manifest.json").write_text(
            json.dumps(self.manifest, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    def log(self, message: str) -> None:
        with open(self.run_dir / "workflow.log", "a", encoding="utf-8") as handle:
            handle.write(f"{_now()} {message}\n")

    def case(self, case_id: str, accession: str | None = None) -> "CaseRecorder":
        if case_id not in self.cases:
            if case_id not in self._case_order:
                self._case_order.append(case_id)
            index = self._case_order.index(case_id) + 1
            self.tracker.begin_study(accession or case_id, index, len(self._case_order))
            self.cases[case_id] = CaseRecorder(self, case_id, accession)
        return self.cases[case_id]

    def finish(self) -> dict:
        for case in self.cases.values():
            if not case.finished:
                case.finish()
        rows = [self.cases[c].row for c in self._case_order if c in self.cases]
        with open(self.run_dir / "summary.csv", "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=SUMMARY_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        failed = [r for r in rows if r["status"].startswith("failed")]
        status = "completed" if not failed else "partial" if len(failed) < len(rows) else "failed"
        attempts = self._attempts()
        self.tracker.set_usage(llm_calls=0, estimated_cost_usd=0.0)
        for row in failed:
            self.tracker.add_failure(f"{row['case_id']}: {row.get('stop_reason') or 'execution failed'}")
        self.tracker.finish(status, f"{len(rows)} case(s); {len(failed)} execution failure(s)")
        self.manifest.update(finished_at=_now(), status=status, n_cases=len(rows),
                             external_llm={"disabled": external_llm_status()["disabled"],
                                           "blocked_attempts": attempts})
        self._write_manifest()
        self.log(f"run finished: {status}")
        return {"status": status, "summary_csv": str(self.run_dir / "summary.csv"),
                "external_llm_blocked_attempts": len(attempts)}


class CaseRecorder:
    def __init__(self, run: RunRecorder, case_id: str, accession: str | None):
        from tools.evidence import EvidenceRecorder

        self.run = run
        self.case_id = case_id
        self.accession = accession
        self.dir = run.run_dir / case_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.records: list[dict] = []
        self.evidence = EvidenceRecorder(run.run_id, subject_id=case_id)
        self._source_ids: dict[str, str] = {}
        self.finished = False
        self.row: dict = {}

    @classmethod
    def _load(cls, run: RunRecorder, case_dir: Path) -> "CaseRecorder":
        from tools.evidence import EvidenceBundle

        state_path = case_dir / "case_state.json"
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
        case = cls(run, case_dir.name, state.get("accession"))
        case.records = json.loads((case_dir / "decisions.json").read_text(encoding="utf-8"))
        evidence_path = case_dir / "evidence.json"
        if evidence_path.exists():
            case.evidence.bundle = EvidenceBundle.model_validate(
                json.loads(evidence_path.read_text(encoding="utf-8")))
            for source in case.evidence.bundle.sources:
                case.evidence._source_keys[(source.origin, source.label, source.uri, source.locator)] = source.source_id
            for artifact in case.evidence.bundle.artifacts:
                case.evidence._artifact_paths[os.path.normpath(artifact.path)] = artifact.artifact_id
        case._source_ids = state.get("source_ids", {})
        case.finished = bool(state.get("finished"))
        case.row = state.get("row", {})
        return case

    def _save_state(self) -> None:
        self.evidence.save(str(self.dir / "evidence.json"))
        (self.dir / "case_state.json").write_text(json.dumps({
            "accession": self.accession, "source_ids": self._source_ids,
            "finished": self.finished, "row": self.row}, indent=2, default=str), encoding="utf-8")

    def _evidence_item(self, path: Path, kind: str, source_id: str) -> dict:
        self._source_ids[f"{kind}:{path.name}"] = source_id
        self._save_state()
        return {"id": f"{kind}:{path.name}", "kind": kind, "path": str(path), "sha256": sha256(path)}

    def evidence_item(self, item_id: str) -> dict:
        """Rebuild the evidence item for an input or output registered earlier (also after open())."""
        if item_id not in self._source_ids:
            raise NativeToolError(f"unknown evidence id {item_id!r}; known: {sorted(self._source_ids)}")
        kind = item_id.split(":", 1)[0]
        return {"id": item_id, "kind": kind}

    def add_input(self, path: str | Path, kind: str, label: str | None = None) -> dict:
        """Register an input (kind: paper, metadata, matrix, user, ...) and return its evidence item."""
        path = Path(path)
        origin = {"paper": "paper", "metadata": "metadata", "user": "user"}.get(kind, "artifact")
        source_id = self.evidence.add_source(origin, label or path.name, uri=str(path),
                                             attributes={"sha256": sha256(path), "kind": kind})
        return self._evidence_item(path, kind, source_id)

    def add_output(self, path: str | Path, role: str) -> dict:
        """Register a file this case produced and return its evidence item."""
        path = Path(path)
        artifact_id = self.evidence.add_artifact(str(path), role=role)
        return self._evidence_item(path, "tool_output", artifact_id)

    def write_json(self, name: str, payload: Any, role: str | None = None) -> dict:
        path = self.dir / name
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        return self.add_output(path, role or Path(name).stem)

    def decide(self, stage: str, *, final: dict, evidence: list[dict], reasoning: str,
               confidence: str, decision_status: str = "valid", execution_status: str = "not_started",
               candidates: Sequence[dict] = (), stop_reason: str | None = None,
               paper: dict | None = None) -> dict:
        if self.finished:
            raise NativeToolError(f"case {self.case_id} is already finished")
        record = {
            "contract_version": decision_contract.CONTRACT_VERSION,
            "case_id": self.case_id,
            "stage": stage,
            "evidence": list(evidence),
            "candidates": list(candidates),
            "final": final,
            "paper": paper or {},
            "confidence": confidence,
            "reasoning": reasoning,
            "decision_status": decision_status,
            "execution_status": execution_status,
            "stop_reason": stop_reason,
            "recorded_at": _now(),
        }
        errors = decision_contract.check_record(record, f"{self.case_id}/{stage}")
        if errors:
            raise NativeToolError("decision record rejected:\n" + "\n".join(errors))
        self.records.append(record)
        (self.dir / "decisions.json").write_text(
            json.dumps(self.records, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        source_ids = [self._source_ids[e["id"]] for e in evidence if e.get("id") in self._source_ids]
        self.evidence.add_decision(stage, final, reason=reasoning, method="llm", evidence_ids=source_ids,
                                   confidence={"high": 0.9, "medium": 0.6, "low": 0.3}[confidence],
                                   details={"decision_status": decision_status,
                                            "execution_status": execution_status,
                                            "stop_reason": stop_reason})
        self._save_state()
        if stage in GATES:
            self.run.tracker.set_stage(stage, message=f"{self.case_id}: {decision_status}")
        self.run.log(f"{self.case_id} {stage}: {decision_status}/{execution_status}"
                     + (f" ({stop_reason})" if stop_reason else ""))
        return record

    def _final(self, stage: str) -> dict:
        valid = [r for r in self.records if r["stage"] == stage and r["decision_status"] == "valid"]
        return valid[-1]["final"] if valid else {}

    def finish(self, *, n_deg: int | None = None, deg_sanity: str | None = None) -> dict:
        errors = decision_contract.check_case(self.records, self.case_id)
        if errors:
            raise NativeToolError("case records are inconsistent:\n" + "\n".join(errors))
        blocked = next((r for r in self.records if r["decision_status"] in decision_contract.BLOCKED), None)
        executions = [r["execution_status"] for r in self.records if r["stage"] == "execution"]
        if blocked:
            status = f"stopped:{blocked['stage']}"
        elif "completed" in executions:
            status = "completed"
        elif "failed" in executions:
            status = "failed_execution"
        else:
            status = "decided_not_executed"
        design, method = self._final("design"), self._final("method")
        covariance, threshold = self._final("covariance"), self._final("threshold")
        if blocked:  # a stopped case reports no contrast
            design, method, threshold = {}, {}, {}
        contrasts = design.get("contrasts") or []
        treatment = design.get("treatment")
        if not treatment and contrasts:
            treatment = "; ".join(str(c.get("name", c)) if isinstance(c, dict) else str(c) for c in contrasts)
        execution_error = next((r["final"].get("execution_error") for r in self.records
                                if r["stage"] == "execution" and r["final"].get("execution_error")), "")
        self.row = {
            "case_id": self.case_id,
            "accession": self.accession or "",
            "status": status,
            "decision_status": blocked["decision_status"] if blocked else "valid",
            "execution_status": executions[-1] if executions else "not_run",
            "stop_stage": blocked["stage"] if blocked else "",
            "stop_reason": blocked["stop_reason"] if blocked else execution_error,
            "route": "stopped" if blocked else self._final("study").get("route", ""),
            "matrix_type": self._final("matrix").get("matrix_type", ""),
            "da_method": method.get("method", ""),
            "design_col": design.get("design_column") or design.get("formula", ""),
            "formula": method.get("formula") or design.get("formula", ""),
            "control": design.get("control", ""),
            "treatment": "; ".join(treatment) if isinstance(treatment, list) else (treatment or ""),
            "n_contrasts": len(contrasts) if contrasts else (1 if design.get("treatment") else 0),
            "covariance_status": covariance.get("status", ""),
            "blocking_terms": "; ".join(map(str, covariance.get("blocking_terms") or [])),
            "threshold_source": threshold.get("threshold_source", ""),
            "applied_threshold": json.dumps(threshold.get("applied_threshold", {}), sort_keys=True)
            if threshold else "",
            "n_deg": "" if n_deg is None else n_deg,
            "deg_sanity": deg_sanity or ("" if n_deg is None else "ok"),
        }
        self.evidence.finish(status=status)
        self.finished = True
        self._save_state()
        self.run.log(f"{self.case_id} finished: {status}")
        return self.row
