"""Batch pipeline orchestrator: runs the per-study RNA-seq flow across many GEO
accessions for keyword-driven cohort analysis. Designed to follow up on a
search_geo_studies result. Per-study failures are caught and logged; the batch
continues."""

import gzip
import json
import os
import re
import sys
import tarfile
from datetime import datetime

import numpy as np
import pandas as pd
from langchain_core.tools import tool


# Derived-stat column name patterns. Surfaced 2026-05-28 on GSE317978's
# `core_table3.csv.gz` which mixes 6 `fpkm_Sample16-21` columns with 6
# `diffexp_log2fc_*` / `diffexp_*_pvalue` / `diffexp_*_qvalue` derived stats.
# The negative log2fc values made `_classify_matrix` flag the file as
# log_transformed (so the pipeline ran limma on raw FPKM, producing biological
# garbage: 9906/17043 ≈ 58% DEG at padj<0.05, max value 666117).
#
# Used by both `_classify_matrix` (to base scale heuristics on real samples
# only) and `_align_metadata_to_expression` (so LLM-A's sample candidate set
# excludes derived stats).
_DERIVED_STAT_PATTERN = re.compile(
    r"diffexp"                                     # diffexp_log2fc_*, diffexp_*_qvalue
    r"|log2[._\s-]?fc|log2[._\s-]?fold"            # log2fc / log2_fold_change
    r"|\blfc\b"
    r"|\b[qp][._\s-]?value\b|\bpvalue\b|\bqvalue\b"
    r"|\bpadj\b|\bp[._]?adj\b|\bfdr\b"
    r"|\b(?:t|f|z)[._\s-]?stat\b"
    r"|\bscore\b"
    r"|\bmean\b|\bmedian\b|\bvariance\b"
    r"|\b(?:std|sd|sem|stderr)\b",
    re.I,
)


def _is_derived_stat_column(name) -> bool:
    """Whether a numeric column name looks like a per-feature derived statistic
    (log2FC, p/q value, FDR, t-stat, score, mean/std, etc.) rather than a
    per-sample measurement."""
    return bool(_DERIVED_STAT_PATTERN.search(str(name)))


class _Tee:
    """Write to multiple streams. Used to mirror stdout into workflow.log so the
    full agent trail is preserved alongside the terminal stream."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s); st.flush()
            except Exception:
                pass

    def flush(self):
        for st in self.streams:
            try: st.flush()
            except Exception: pass

    def isatty(self):
        return False

from tools.geo_tools import download_geo_data, download_supplementary_files
from tools.preprocess_tools import preprocess_counts
from tools.stats_tools import sample_qc_summary
from tools.deseq2_tools import run_deseq2_analysis, deg_filename
from tools.limma_tools import run_limma_analysis
from tools.edger_tools import run_edger_analysis
from tools.limma_voom_tools import run_limma_voom_analysis
from tools.enrichment_tools import run_gsea_analysis
from tools.evaluation_tools import evaluate_repeated_results_core
from tools.llm_helpers import (
    summarize_metadata_for_llm, validate_contrast_with_llm, choose_raw_da_method_with_llm,
    choose_raw_da_method_rule, classify_matrix_with_llm,
    llm_usage_checkpoint, llm_usage_summary, reset_llm_alignment_cache,
)
from tools.evidence import EvidenceRecorder, SCHEMA_VERSION
from tools.run_status import ConsoleStatusRenderer, RunStatusTracker

# Raw-counts DA methods (the mentor's matrix: any of the three). The log/FPKM branch always
# uses limma-trend. 'auto' picks by DETERMINISTIC RULE (DESeq2 default, no LLM — req #1);
# 'auto-llm' restores the per-study LLM picker; an explicit method name forces that one.
_RAW_DA_METHODS = {"deseq2", "edger", "limma-voom"}
# Ordered list run together when raw_da_method='all' (multi-method consensus). DESeq2 first so it
# is the GSEA representative and the back-compat "first method".
_ALL_RAW_METHODS = ["deseq2", "edger", "limma-voom"]


class _DecisionLog:
    """Accumulates structured per-study decision records and writes decisions.json.

    Complements workflow.log (a free-text stream of everything) and summary.csv
    (one row per study) with a machine-readable trace of every decision point and
    its reason for a single study — the E4 structured-logging artifact."""

    def __init__(self, accession):
        self.accession = accession
        self.started = datetime.now().isoformat(timespec="seconds")
        self.entries = []
        self.evidence = EvidenceRecorder(
            run_id=f"batch:{accession}:{self.started}", subject_id=accession,
        )
        self.pipeline_source = self.evidence.add_source(
            "computation", "run_batch_geo_pipeline", locator=accession,
        )

    @staticmethod
    def _method(step, decision):
        text = f"{step} {decision}".lower()
        if "llm" in text:
            return "llm", "llm", "Claude structured decision"
        if decision == "param":
            return "user", "user", "user-supplied pipeline parameter"
        if step in {"gsea", "deseq2", "edger", "limma", "limma-voom",
                    "differential_expression", "subset_evaluation", "sex_check"}:
            return "computation", "computation", f"computed pipeline stage: {step}"
        if step == "download":
            return "computation", "external_api", "GEO/download result"
        return "rule", "rule", f"deterministic pipeline rule: {step}"

    @staticmethod
    def _artifact_candidates(details):
        extensions = (".csv", ".tsv", ".json", ".png", ".pdf", ".gz", ".txt", ".tar")
        for key, value in details.items():
            values = value if isinstance(value, (list, tuple)) else [value]
            for item in values:
                if isinstance(item, str) and item.lower().endswith(extensions):
                    yield key, item

    def record(self, step, decision, reason="", **details):
        self.entries.append({
            "step": step,
            "decision": decision,
            "reason": reason,
            "details": details,
        })
        method, origin, label = self._method(step, decision)
        source_id = self.evidence.add_source(origin, label, locator=self.accession)
        decision_id = self.evidence.add_decision(
            step, decision, reason=reason, method=method,
            evidence_ids=[source_id], details=details,
        )
        for role, path in self._artifact_candidates(details):
            # Decision details historically stored inputs relative to data/
            # (for example GSE123/matrix.csv). Evidence bundles live under
            # output/, so auditors could not resolve or hash those strings.
            candidates = [path]
            if not os.path.isabs(path):
                candidates.append(os.path.join("data", path))
            resolved = next(
                (os.path.abspath(candidate) for candidate in candidates
                 if os.path.isfile(candidate)),
                path,
            )
            self.evidence.add_artifact(
                resolved, role=role, produced_by=decision_id, evidence_ids=[source_id],
            )

    def save(self, path, status=None, error=None):
        evidence_path = os.path.join(os.path.dirname(path), "evidence.json")
        self.evidence.finish(status=status, error=error)
        if status is not None:
            self.evidence.add_claim(
                self.accession, "pipeline_status", status,
                f"Batch pipeline finished with status {status}", method="computation",
                evidence_ids=[self.pipeline_source], status="computed",
            )
        payload = {
            "schema_version": SCHEMA_VERSION,
            "accession": self.accession,
            "started": self.started,
            "finished": datetime.now().isoformat(timespec="seconds"),
            "final_status": status,
            "error": error,
            "decisions": self.entries,
            "evidence_file": evidence_path,
        }
        try:
            self.evidence.save(evidence_path)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  [decision-log] failed to write {path}: {e}")


def _run_sex_check(counts_path, metadata_csv, organism, study_out):
    """Run infer_sex_from_expression for the batch flow and return a structured
    summary for the decision log: one-line verdict text + parsed mismatch count.
    Never raises — sex QC must not abort a study."""
    from tools.stats_tools import infer_sex_from_expression
    try:
        msg = infer_sex_from_expression.invoke({
            "counts_csv": counts_path, "metadata_csv": metadata_csv,
            "organism": organism, "output_dir": study_out,
        })
    except Exception as e:
        return {"verdict": "error", "summary": f"{type(e).__name__}: {e}",
                "n_mismatch": None, "mismatched": []}
    base = os.path.splitext(os.path.basename(counts_path))[0]
    tsv = os.path.join(study_out, f"{base}_sex_check.tsv")
    n_mismatch, mismatched = None, []
    if os.path.exists(tsv):
        try:
            sx = pd.read_csv(tsv, sep="\t", index_col=0)
            if "agreement" in sx.columns:
                mismatched = sx.index[sx["agreement"] == "MISMATCH"].astype(str).tolist()
                n_mismatch = len(mismatched)
        except Exception:
            pass
    if n_mismatch is None:
        verdict = "no_crosscheck"
    elif n_mismatch > 0:
        verdict = "mismatch"
    else:
        verdict = "ok"
    return {"verdict": verdict, "summary": msg.split("\n")[0],
            "n_mismatch": n_mismatch, "mismatched": mismatched}


def _open_maybe_gz(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, encoding="utf-8", errors="replace")


def _classify_matrix(path):
    """Return ('raw_counts' | 'fpkm_or_tpm' | 'log_transformed' | ..., preview_df_or_None)."""
    try:
        with _open_maybe_gz(path) as fh:
            head = fh.read(8192)
        if path.endswith((".csv", ".csv.gz")):
            sep = ","
        elif "\t" in head:
            sep = "\t"
        else:
            sep = ","
        with _open_maybe_gz(path) as fh:
            df = pd.read_csv(fh, sep=sep, nrows=2000, low_memory=False)
    except Exception:
        return "unreadable", None
    if df.shape[1] < 3:
        return "too_few_cols", df
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return "no_numeric_cols", df
    # Exclude derived stat columns (diffexp_log2fc_*, p/q values, scores) BEFORE
    # the sign/magnitude heuristic. Otherwise a FPKM matrix with embedded
    # diffexp_* columns is misclassified as log_transformed because the log2FC
    # negatives dominate the sign check (GSE317978 bug, 2026-05-28).
    sample_cols = [c for c in numeric.columns if not _is_derived_stat_column(c)]
    if sample_cols:
        numeric = numeric[sample_cols]
    # else: keep all numeric — pathological case where every numeric col is a
    # stat (file IS a stats-only output, not an expression matrix); the
    # heuristic will likely return log_transformed or ambiguous, which is fine
    # because such a file can't be analyzed as expression anyway.
    vals = numeric.to_numpy(dtype=float, na_value=np.nan).ravel()
    nz = vals[(~np.isnan(vals)) & (vals != 0)]
    if len(nz) == 0:
        return "all_zero", df
    has_neg = bool((nz < 0).any())
    has_dec = bool((nz % 1 != 0).any())
    nz_max = float(nz.max())
    if has_neg:
        return "log_transformed", df
    if not has_dec and nz_max > 100:
        return "raw_counts", df
    if has_dec:
        # Decimals with small max → already log-scale (log2(CPM+1) caps ~25,
        # log-FPKM ~20). Decimals with large max → linear FPKM/TPM (real-world
        # FPKMs routinely exceed 10000 for housekeeping genes; old `< 1000`
        # cap was too strict and misrouted real FPKM matrices, GSE317978 case).
        if nz_max < 30:
            return "log_transformed", df
        return "fpkm_or_tpm", df
    return "ambiguous_decimal", df


def _unpack_and_merge_geo_tar(data_dir):
    """If data_dir contains a *_RAW.tar with per-sample count files inside,
    extract and merge into a single counts matrix (gene_id as index, sample
    filenames as columns). Returns the merged CSV path or None on failure.

    Per-sample file convention: first column is gene_id, the rightmost numeric
    column is the count. Works for plain `gene_id\\tcount` files and for
    featureCounts output (auto-skips `#`-prefixed metadata lines)."""
    tar_path = None
    for n in os.listdir(data_dir):
        if n.lower().endswith("_raw.tar") or n.lower().endswith(".tar"):
            tar_path = os.path.join(data_dir, n)
            break
    if tar_path is None:
        return None

    acc = os.path.basename(data_dir.rstrip("/\\"))
    extract_dir = os.path.join(data_dir, "_unpacked")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        with tarfile.open(tar_path) as t:
            members = [m for m in t.getmembers() if m.isfile() and
                       m.name.lower().endswith((".txt", ".tsv", ".csv",
                                                ".txt.gz", ".tsv.gz", ".csv.gz"))]
            if not members:
                return None
            t.extractall(extract_dir)
    except Exception as e:
        print(f"  tar extract failed: {e}")
        return None

    print(f"  unpacked {len(members)} per-sample files from {os.path.basename(tar_path)}")
    series = []
    skipped = []   # (filename, reason) — a skipped SAMPLE file is a dropped sample (fail loud)
    for m in members:
        p = os.path.join(extract_dir, m.name)
        try:
            df = pd.read_csv(p, sep=None, engine="python", comment="#")
        except Exception as e:
            skipped.append((m.name, f"parse_error:{type(e).__name__}"))
            continue
        if df.shape[1] < 2:
            skipped.append((m.name, f"too_few_cols({df.shape[1]})"))
            continue
        gene_col = df.columns[0]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            skipped.append((m.name, "no_numeric_col"))
            continue
        count_col = numeric_cols[-1]
        # Sample id = leading part of filename, drops extensions
        base = os.path.basename(m.name)
        for suf in (".gz", ".txt", ".tsv", ".csv"):
            if base.lower().endswith(suf):
                base = base[: -len(suf)]
        s = df.set_index(gene_col)[count_col]
        s.name = base
        s = s[~s.index.duplicated(keep="first")]
        series.append(s)

    # Fail loud: an unparseable per-sample file is a DROPPED SAMPLE. GSE291636 silently lost
    # samples this way. Some tar members are legitimately non-sample (README/filelist), so we
    # REPORT rather than abort — a merged-sample-count mismatch is now visible, not silent.
    if skipped:
        shown = "; ".join(f"{n} [{r}]" for n, r in skipped[:8])
        print(f"  WARNING: skipped {len(skipped)}/{len(members)} tar members "
              f"(possible dropped samples): {shown}" + (" ..." if len(skipped) > 8 else ""))

    if not series:
        return None

    merged = pd.concat(series, axis=1, join="outer").fillna(0)
    merged.index.name = "gene_id"
    out_path = os.path.join(data_dir, f"{acc}_merged_from_tar.csv")
    merged.to_csv(out_path)
    print(f"  merged matrix: {merged.shape[0]} genes x {merged.shape[1]} samples "
          f"({len(series)}/{len(members)} members merged) -> {out_path}")
    return out_path


_ANALYZABLE_TYPES = ("raw_counts", "log_transformed", "fpkm_or_tpm")

# Filename fragments that mark a NON-expression file (sample/clinical annotation, design
# sheets, docs). These can pass the numeric heuristic — e.g. a clinical phenotype data
# dictionary has many numeric columns (VO2max, treadmill speed, body composition) and looks
# like a log-scale matrix — and get mis-picked as the expression matrix. 'metadata' was the
# original guard; the rest were added after GSE242358 (MoTrPAC) mis-picked
# `*_phenotype_viallabel_data-v5.txt.gz` as log_transformed instead of reaching the real
# expression in its _RAW.tar.
_NONEXPRESSION_NAME_HINTS = (
    "metadata", "meta_", "phenotype", "viallabel", "clinical", "data_dictionary",
    "datadict", "dictionary", "sample_sheet", "samplesheet", "sdrf", "readme",
)


def _gather_matrix_candidates(data_dir):
    """Sorted (largest first) list of candidate expression-matrix file PATHS in data_dir.

    Excludes non-expression-named files (metadata/phenotype/...) and pipeline-generated
    artifacts (`*_log2.csv` / `*_preprocessed.csv` / `*_aligned.csv` / `*_mvalue.csv`) so the
    candidate set is the original SOURCE data only. Shared by `_find_expression_file` and the
    req#1 LLM data-type rescue path."""
    if not os.path.isdir(data_dir):
        return []
    cands = []
    for root, _, names in os.walk(data_dir):
        for n in names:
            n_lower = n.lower()
            if any(h in n_lower for h in _NONEXPRESSION_NAME_HINTS):
                continue
            if ("_log2.csv" in n_lower or "_preprocessed.csv" in n_lower
                    or "_aligned.csv" in n_lower or "_mvalue.csv" in n_lower):
                continue
            p = os.path.join(root, n)
            if n_lower.endswith((".csv", ".tsv", ".txt", ".csv.gz", ".tsv.gz", ".txt.gz")):
                cands.append((os.path.getsize(p), p))
    cands.sort(reverse=True)
    return [p for _, p in cands]


def _find_expression_file(data_dir):
    """Scan the GEO data dir for the largest file that classifies as an analyzable
    expression matrix (raw_counts | log_transformed | fpkm_or_tpm).
    Returns (path, matrix_type) on success, or (None, reason) on miss.

    Excludes files whose name matches a non-expression hint (metadata / phenotype /
    viallabel / clinical / data dictionary / sample sheet / sdrf / readme) — these can pass
    the numeric heuristic (metadata's data_row_count is a large int; a clinical phenotype
    dictionary is full of numeric columns) and get mis-picked as the matrix. See
    _NONEXPRESSION_NAME_HINTS.

    If no usable matrix is found AND a *_RAW.tar exists, tries to unpack it and
    merge per-sample files into a synthetic matrix; the merged file is then
    re-classified and accepted if it matches any analyzable type."""
    if not os.path.isdir(data_dir):
        return None, "data_dir_missing"
    # Pipeline-artifact / non-expression exclusion lives in _gather_matrix_candidates
    # (without it a prior run's `<base>_log2.csv` outgrows the source and gets selected
    # by the size sort → double-logged limma input; surfaced 2026-05-28 on GSE283691).
    cand_paths = _gather_matrix_candidates(data_dir)
    if cand_paths:
        # First pass: prefer raw_counts if any of the top 3 files have it (DESeq2 is preferred
        # when applicable). Second pass: accept any analyzable type.
        for p in cand_paths[:3]:
            cls, _ = _classify_matrix(p)
            if cls == "raw_counts":
                return p, "raw_counts"
        for p in cand_paths[:3]:
            cls, _ = _classify_matrix(p)
            if cls in _ANALYZABLE_TYPES:
                return p, cls

    # Fallback: extract & merge per-sample files from *_RAW.tar
    merged = _unpack_and_merge_geo_tar(data_dir)
    if merged is not None:
        cls, _ = _classify_matrix(merged)
        if cls == "raw_counts":
            return merged, "raw_counts_from_tar"
        if cls in _ANALYZABLE_TYPES:
            return merged, cls
        return None, f"tar_merged_but_not_analyzable({cls})"

    if not cand_paths:
        return None, "no_matrix_file"
    top_cls, _ = _classify_matrix(cand_paths[0])
    return None, f"top_files_not_analyzable({top_cls})"


def _log2_transform_matrix(path):
    """Write a log2(x+1)-transformed sibling of `path` (numeric columns only;
    string annotation columns are preserved as-is). Returns the new file path.
    Idempotent — if the sibling exists already, just returns it.

    Used for FPKM/TPM (linear-scale) inputs before handing to limma, which
    assumes log-scale expression. Without this, fold-changes and moderation
    are computed on a wrong scale and become biologically meaningless."""
    base, ext = os.path.splitext(path)
    if ext.lower() == ".gz":
        base, _ = os.path.splitext(base)
    out_path = f"{base}_log2.csv"
    if os.path.exists(out_path):
        return out_path
    df = pd.read_csv(path, sep=None, engine="python", index_col=0)
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = np.log2(df[numeric_cols].clip(lower=0).fillna(0) + 1)
    df.to_csv(out_path)
    print(f"  log2-transformed -> {out_path}")
    return out_path


def _mvalue_transform_matrix(path):
    """Write an M-value sibling of a methylation β matrix (β in [0,1] or 0-100%):
    M = log2((β+ε)/(1-β+ε)). Returns the new path; idempotent. This routes a methylation matrix
    through the EXISTING log-scale (limma) dispatch — β→M is the limma-recommended transform for
    bounded β, identical to what run_methylation_da does (req #1 methylation route)."""
    from tools.methylation_tools import _beta_to_mvalue
    base, ext = os.path.splitext(path)
    if ext.lower() == ".gz":
        base, _ = os.path.splitext(base)
    out_path = f"{base}_mvalue.csv"
    if os.path.exists(out_path):
        return out_path
    df = pd.read_csv(path, sep=None, engine="python", index_col=0)
    mv = _beta_to_mvalue(df)
    mv.to_csv(out_path)
    print(f"  methylation β→M-values -> {out_path}")
    return out_path


def _matrix_stats_preview(path, max_rows=80):
    """Compact numeric profile + small text preview of an expression matrix, for the req#1 LLM
    data-type classifier. Returns (stats_dict, preview_text) or (None, None) if unreadable.

    The stats are the exact discriminators the classifier reasons over (integer-ness, sign,
    fraction in [0,1]/[0,100], magnitude) plus example row IDs (gene vs CpG/UniProt) and column
    names — i.e. everything the heuristic `_classify_matrix` throws away after its branch."""
    try:
        with _open_maybe_gz(path) as fh:
            head = fh.read(8192)
        sep = "," if path.endswith((".csv", ".csv.gz")) else ("\t" if "\t" in head else ",")
        with _open_maybe_gz(path) as fh:
            df = pd.read_csv(fh, sep=sep, nrows=max_rows, low_memory=False)
    except Exception:
        return None, None
    if df.shape[1] < 2:
        return None, None
    first_col = df.columns[0]
    numeric = df.select_dtypes(include="number")
    sample_cols = [c for c in numeric.columns if not _is_derived_stat_column(c)]
    if sample_cols:
        numeric = numeric[sample_cols]
    if numeric.shape[1] == 0:
        return None, None
    vals = numeric.to_numpy(dtype=float, na_value=np.nan).ravel()
    finite = vals[np.isfinite(vals)]
    nz = finite[finite != 0]
    if finite.size == 0:
        return None, None

    def _f(mask):
        return round(float(np.mean(mask)), 3)

    stats = {
        "n_rows_sampled": int(df.shape[0]),
        "n_numeric_cols": int(numeric.shape[1]),
        "min": round(float(np.min(finite)), 4),
        "max": round(float(np.max(finite)), 4),
        "median_nonzero": round(float(np.median(nz)), 4) if nz.size else 0.0,
        "frac_negative": _f(finite < 0),
        "frac_integer_of_nonzero": round(float(np.mean(nz % 1 == 0)), 3) if nz.size else None,
        "frac_in_0_1": _f((finite >= 0) & (finite <= 1)),
        "frac_in_0_100": _f((finite >= 0) & (finite <= 100)),
        "row_id_examples": [str(x) for x in df[first_col].head(5).tolist()],
        "numeric_col_examples": [str(c) for c in list(numeric.columns[:6])],
    }
    preview_cols = [first_col] + list(numeric.columns[:5])
    try:
        preview_text = df[preview_cols].head(5).to_string(index=False, max_colwidth=18)
    except Exception:
        preview_text = ""
    return stats, preview_text


def _platform_hint_from_metadata(meta_df):
    """Short platform/assay hint string from GEO metadata columns (platform_id / instrument_model /
    library_strategy / title / data_processing) — disambiguates proteomics & methylation for the
    LLM data-type classifier, which the numeric profile alone cannot."""
    hint_cols = ("platform_id", "instrument_model", "library_strategy", "library_source",
                 "title", "data_processing", "extract_protocol")
    bits = []
    for c in meta_df.columns:
        cl = str(c).lower()
        if any(h in cl for h in hint_cols):
            vals = [v for v in meta_df[c].dropna().astype(str).unique()[:3]]
            if vals:
                bits.append(f"{c}={'|'.join(vals)}")
        if len(bits) >= 6:
            break
    return "; ".join(bits)[:600]


# req#1 LLM data-type → pipeline route. The classifier's vocabulary is normalized onto the three
# existing dispatch branches (raw / fpkm / log) by doing any type-specific pre-transform up front,
# so nothing downstream of matrix_type needs a new branch.
def _apply_llm_matrix_type(llm_res, counts_path):
    """Map a MatrixTypeClassification onto (counts_path, pipeline_matrix_type, note), performing
    a pre-transform when the type needs one. Returns pipeline_matrix_type=None for ambiguous/
    unroutable so the caller keeps the heuristic answer."""
    t = (llm_res.matrix_type or "").lower().strip()
    if t == "raw_counts":
        return counts_path, "raw_counts", "LLM: integer read counts → DESeq2/edgeR/voom"
    if t == "fpkm_or_tpm":
        return counts_path, "fpkm_or_tpm", "LLM: linear normalized expression (FPKM/TPM) → log2 then limma"
    if t == "log_transformed":
        return counts_path, "log_transformed", "LLM: already log-scale expression → limma as-is"
    if t == "proteomics_intensity":
        if llm_res.already_log_scale:
            return counts_path, "log_transformed", "LLM: proteomics intensities already log-scale → limma as-is"
        return counts_path, "fpkm_or_tpm", "LLM: proteomics intensities (linear) → log2 then limma"
    if t == "methylation_beta":
        mv = _mvalue_transform_matrix(counts_path)
        return mv, "log_transformed", "LLM: methylation β → M-values → limma (β→M, limma-recommended transform)"
    return counts_path, None, f"LLM: {t} (unroutable / ambiguous — kept heuristic)"


def _llm_datatype_decision(counts_path, heuristic_cls, platform_hint, organism):
    """Run the req#1 LLM data-type classifier when warranted, else return None.

    Gate: integer raw_counts are reliable → SKIP the call (cost ≈ 0). Fire only on the decimal /
    ambiguous zone (fpkm/log/ambiguous_decimal) or when the filename/platform hints a non-RNA assay
    (proteomics / methylation). Returns a MatrixTypeClassification or None (LLM off / unavailable)."""
    name = os.path.basename(counts_path).lower()
    hint = (platform_hint or "").lower()
    suspect_special = any(k in name or k in hint for k in (
        "methyl", "rrbs", "wgbs", "bisulf", "450k", "850k", "epic", "beta_",
        "proteom", "protein", "intensity", "lfq", "tmt", "olink", "maxquant", "_dia"))
    uncertain = heuristic_cls in ("ambiguous_decimal", "fpkm_or_tpm", "log_transformed")
    if not (uncertain or suspect_special):
        return None
    stats, preview = _matrix_stats_preview(counts_path)
    if stats is None:
        return None
    return classify_matrix_with_llm(
        filename=os.path.basename(counts_path), platform=platform_hint,
        value_stats=stats, preview_text=preview or "", heuristic_label=heuristic_cls,
        organism=organism)


def _da_model_params(method, matrix_type):
    """Full model spec + parameters used for the DA step, recorded into decisions.json
    for transparency. Pure record-keeping — does NOT affect the analysis.

    IMPORTANT (honest disclosure): every backend here fits a SINGLE-FACTOR model
    (`~ condition`, one 2-group contrast). NO covariate adjustment (no sex / batch /
    age / tissue). Covariate + per-sex / interaction modelling is roadmap E1/E5.
    """
    normalization = {
        "deseq2": "DESeq2 internal median-of-ratios size factors (fit on raw integer counts)",
        "edger": "edgeR TMM normalization (fit on raw integer counts)",
        "limma-voom": "voom log2-CPM + mean-variance precision weights (fit on raw integer counts)",
        "limma": ("log2(x+1) applied to the FPKM/TPM matrix before limma"
                  if matrix_type == "fpkm_or_tpm"
                  else "none — matrix is already log-scale"),
    }.get(method, "unknown")
    return {
        "design_formula": "~ condition  (single 2-group factor)",
        "covariates": [],  # none — no sex/batch/age adjustment (roadmap E1/E5)
        "da_method": method,
        "normalization": normalization,
        "deg_significance_cutoff": "padj < 0.05",
        "pvalue_adjustment": "Benjamini-Hochberg (FDR)",
        "gsea_fdr_cutoff": 0.25,
    }


def _invoke_da_method(method, counts_path, da_input_path, metadata_for_design,
                      col, ctrl, treat, study_out):
    """Dispatch to one DA backend. Each writes the canonical DEG_results_<treat>_vs_<ctrl>.csv
    into study_out (same filename regardless of method — the caller renames it if needed).
    Returns the backend's text report."""
    if method == "deseq2":
        return run_deseq2_analysis.invoke({
            "counts_csv": counts_path, "metadata_csv": metadata_for_design,
            "design_column": col, "control_group": ctrl, "treatment_group": treat,
            "output_dir": study_out,
        })
    elif method == "edger":
        return run_edger_analysis.invoke({
            "counts_csv": counts_path, "metadata_csv": metadata_for_design,
            "design_column": col, "control_group": ctrl, "treatment_group": treat,
            "output_dir": study_out,
        })
    elif method == "limma-voom":
        return run_limma_voom_analysis.invoke({
            "counts_csv": counts_path, "metadata_csv": metadata_for_design,
            "design_column": col, "control_group": ctrl, "treatment_group": treat,
            "output_dir": study_out,
        })
    else:  # limma-trend (log_transformed / fpkm_or_tpm branch)
        return run_limma_analysis.invoke({
            "normalized_csv": da_input_path, "metadata_csv": metadata_for_design,
            "design_column": col, "control_group": ctrl, "treatment_group": treat,
            "output_dir": study_out,
        })


def _gsea_for_deg(deg_csv, organism, study_out, dlog, fail_log, acc, label):
    """Run GSEA on one DEG file. Returns (n_gsea_sig, status) where status is
    'deg_gsea_ok' or 'deg_ok_gsea_failed'. Records the decision + any failure."""
    gsea_msg = run_gsea_analysis.invoke({
        "deg_csv": deg_csv, "organism": organism,
        "ranking_metric": "stat", "output_dir": study_out,
    })
    print(gsea_msg[:300])
    if "gsea analysis failed" in gsea_msg.lower():
        gsea_err = gsea_msg.strip().splitlines()[0][:300]
        dlog.record("gsea", "failed", reason=gsea_err, contrast=label)
        with open(fail_log, "a", encoding="utf-8") as f:
            f.write(f"{acc} | GSEA failed for {label}: {gsea_err}\n")
        return None, "deg_ok_gsea_failed"
    n_gsea_sig = None
    for line in gsea_msg.splitlines():
        if "significant at FDR" in line and "tested" in line:
            try:
                n_gsea_sig = int(line.split(",")[1].strip().split()[0])
            except Exception:
                pass
            break
    dlog.record("gsea", "ok",
                reason=(f"preranked GSEA of contrast '{label}' against MSigDB Hallmark "
                        f"(gseapy, genes ranked by DESeq2 stat); "
                        f"{n_gsea_sig if n_gsea_sig is not None else 'NA'} sets significant at FDR q<0.25"),
                n_gsea_sig=n_gsea_sig, contrast=label,
                library="MSigDB Hallmark", method="prerank (gseapy)",
                ranking_metric="stat", fdr_cutoff=0.25)
    return n_gsea_sig, "deg_gsea_ok"


def _deg_sanity_flags(n_sig, n_tested, metadata_for_design, col, ctrl, treat,
                      sig_frac_warn=0.50, min_group_n=3):
    """Post-DA implausibility guard. A DA result can pass every existing check (valid file,
    valid numbers, >=4 samples) yet be statistically UNTRUSTWORTHY — most often when an absurd
    FRACTION of the genome is called significant. That is the signature of too-few replicates,
    wrong-scale input, or a batch confound; n=2-per-group limma is the canonical case
    (GSE317978: a real 2v2 KO-vs-CTR contrast -> 66% of genes 'DE' because zero within-group
    variance inflates eBayes moderation). Such results LOOK normal and otherwise pass silently.

    Returns a ';'-joined flag string ('' when clean) computed from two cheap, principled signals:
      - implausible_sig_fraction: > sig_frac_warn of tested genes significant at padj<0.05,
      - tiny_n_per_group: fewer than min_group_n samples in either arm (weak/unreliable moderation).
    The caller warns loudly + records it so the result is no longer silently wrong."""
    flags = []
    try:
        if n_sig is not None and n_tested:
            frac = n_sig / n_tested
            if frac > sig_frac_warn:
                flags.append(f"implausible_sig_fraction={frac:.0%}({n_sig}/{n_tested})")
    except Exception:
        pass
    try:
        md = pd.read_csv(metadata_for_design, index_col=0)
        n_ctrl = int((md[col].astype(str) == str(ctrl)).sum())
        n_treat = int((md[col].astype(str) == str(treat)).sum())
        if min(n_ctrl, n_treat) < min_group_n:
            flags.append(f"tiny_n_per_group={min(n_ctrl, n_treat)}(ctrl{n_ctrl}/treat{n_treat})")
    except Exception:
        pass
    return ";".join(flags)


def _record_deg_sanity(res, sanity, label, method, dlog, fail_log, acc):
    """Attach a DEG-sanity verdict to a contrast result + warn loudly when it's not clean."""
    res["deg_sanity"] = sanity or "ok"
    if sanity:
        print(f"  !! DEG SANITY [{label} ({method})]: {sanity} -> result is statistically "
              f"UNTRUSTWORTHY (too few replicates / wrong scale / confound); treat n_deg as unreliable.")
        dlog.record(method, "sanity_warning", contrast=label, flags=sanity)
        with open(fail_log, "a", encoding="utf-8") as f:
            f.write(f"{acc} | DEG SANITY WARNING for {label} ({method}): {sanity}\n")


def _run_contrast_multi(methods, counts_path, da_input_path, metadata_for_design,
                        col, ctrl, treat, study_out, organism, matrix_type,
                        dlog, fail_log, acc, gsea_method="deseq2"):
    """raw_da_method='all': run EVERY method in `methods` on the SAME contrast, then compare.

    Why run several: DESeq2, edgeR and limma-voom make different statistical assumptions
    (NB with per-gene shrinkage / NB with TMM dispersion / voom-weighted normal). A gene that
    only one method flags is far more likely a method artifact than a robust biological signal,
    so the reported headline n_deg is the CONSENSUS (genes significant in >=2 methods). Per-method
    DEG files are kept (DEG_results_<treat>_vs_<ctrl>__<method>.csv), plus a per-gene comparison
    CSV and pairwise log2FC concordance, so nothing is hidden.

    Returns a dict shaped like _run_contrast_da's (control/treatment/design_col/n_deg/n_gsea_sig/
    status) so the per-study aggregation reuses it, plus: per_method (method->n_deg), consensus_deg
    (>=2 methods), consensus_all_deg (all methods), pairwise_r, methods_ok, compare_csv."""
    label = f"{treat} vs {ctrl}"
    canon = os.path.join(study_out, deg_filename(treat, ctrl))
    base = deg_filename(treat, ctrl)[:-4]  # strip '.csv'
    per = {}  # method -> {"n_deg": int|None, "csv": tagged_path, "df": DataFrame}
    for m in methods:
        if os.path.exists(canon):
            os.remove(canon)  # ensure we only pick up THIS method's fresh output
        try:
            print(_invoke_da_method(m, counts_path, da_input_path, metadata_for_design,
                                    col, ctrl, treat, study_out)[:200])
        except Exception as e:
            dlog.record(m, "failed", reason=f"{type(e).__name__}: {e}", contrast=label,
                        design_column=col, control=ctrl, treatment=treat)
            with open(fail_log, "a", encoding="utf-8") as f:
                f.write(f"{acc} | {m} raised on {label}: {type(e).__name__}: {e}\n")
            continue
        if not os.path.exists(canon):
            dlog.record(m, "failed", reason="DEG output missing", contrast=label,
                        design_column=col, control=ctrl, treatment=treat)
            with open(fail_log, "a", encoding="utf-8") as f:
                f.write(f"{acc} | DEG output missing for {label} ({m})\n")
            continue
        tagged = os.path.join(study_out, f"{base}__{m}.csv")
        os.replace(canon, tagged)
        df = pd.read_csv(tagged, index_col=0)
        n_deg = int((df["padj"] < 0.05).sum()) if "padj" in df.columns else None
        per[m] = {"n_deg": n_deg, "csv": tagged, "df": df}
        dlog.record(m, "ok",
                    reason=(f"{m} differential expression on contrast '{label}' (design column '{col}', "
                            f"{ctrl} vs {treat}); {n_deg if n_deg is not None else 'NA'} genes at padj<0.05"),
                    n_deg=n_deg, contrast=label, design_column=col,
                    control=ctrl, treatment=treat, model_params=_da_model_params(m, matrix_type))
        print(f"  [{m}] {label}: {n_deg} DEG (padj<.05)")

    res = {"control": ctrl, "treatment": treat, "design_col": col,
           "n_deg": None, "n_gsea_sig": None, "status": None,
           "per_method": {m: per[m]["n_deg"] for m in per},
           "consensus_deg": None, "consensus_all_deg": None,
           "pairwise_r": {}, "methods_ok": list(per.keys()), "compare_csv": None}
    if not per:
        res["status"] = "deg_failed"
        return res

    # Per-gene comparison table: each method's log2FC + padj side by side, plus a consensus count.
    cols = {}
    sig_flags = {}
    for m, d in per.items():
        df = d["df"]
        if "log2FoldChange" in df.columns:
            cols[f"{m}_log2FC"] = df["log2FoldChange"]
        if "padj" in df.columns:
            cols[f"{m}_padj"] = df["padj"]
            sig_flags[m] = df["padj"] < 0.05
    merged = pd.DataFrame(cols)
    if sig_flags:
        flags = pd.DataFrame(sig_flags).reindex(merged.index).fillna(False)
        merged["n_methods_sig"] = flags.sum(axis=1).astype(int)
        merged["consensus_ge2"] = merged["n_methods_sig"] >= 2
        res["consensus_deg"] = int((merged["n_methods_sig"] >= 2).sum())
        res["consensus_all_deg"] = int((merged["n_methods_sig"] >= len(per)).sum())
        merged = merged.sort_values("n_methods_sig", ascending=False)
    compare_csv = os.path.join(study_out, f"{base}__DA_compare.csv")
    merged.to_csv(compare_csv)
    res["compare_csv"] = compare_csv
    # headline DEG count for an 'all' run = robust consensus (>=2 methods agree).
    res["n_deg"] = res["consensus_deg"] if res["consensus_deg"] is not None else None

    # same implausibility guard as the single-method path, on the consensus fraction.
    sanity = _deg_sanity_flags(res["n_deg"], len(merged), metadata_for_design, col, ctrl, treat)
    _record_deg_sanity(res, sanity, label, "all", dlog, fail_log, acc)

    # Pairwise log2FC concordance on the genes each method pair shares.
    ms = list(per.keys())
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            a, b = ms[i], ms[j]
            da_, db = per[a]["df"], per[b]["df"]
            if "log2FoldChange" not in da_.columns or "log2FoldChange" not in db.columns:
                continue
            common = da_.index.intersection(db.index)
            if len(common) >= 10:
                r = da_.loc[common, "log2FoldChange"].corr(db.loc[common, "log2FoldChange"])
                if pd.notna(r):
                    res["pairwise_r"][f"{a}~{b}"] = round(float(r), 3)

    dlog.record("da_method_comparison", "ok",
                reason=(f"cross-checked {len(ms)} methods ({','.join(ms)}) on contrast '{label}'; "
                        f"headline n_deg = consensus of >=2 methods = {res['consensus_deg']} "
                        f"(all {len(ms)} agree on {res['consensus_all_deg']}); "
                        f"pairwise log2FC concordance r={res['pairwise_r']}"),
                contrast=label, methods=ms,
                per_method_deg=res["per_method"], consensus_ge2=res["consensus_deg"],
                consensus_all=res["consensus_all_deg"], logfc_pairwise_r=res["pairwise_r"],
                compare_csv=os.path.relpath(compare_csv, study_out))

    # GSEA once, on the representative method (DESeq2 if it ran, else the first that did).
    gm = gsea_method if gsea_method in per else ms[0]
    n_sig, gstatus = _gsea_for_deg(per[gm]["csv"], organism, study_out, dlog, fail_log, acc,
                                   f"{label} ({gm})")
    res["n_gsea_sig"] = n_sig
    res["status"] = gstatus
    res["gsea_method"] = gm
    return res


def _run_contrast_da(method, counts_path, da_input_path, metadata_for_design,
                     col, ctrl, treat, study_out, organism, matrix_type,
                     dlog, fail_log, acc):
    """Run ONE control-vs-treatment contrast end to end: DA -> DEG -> GSEA (req #8).

    Each contrast writes its own DEG_results_<treat>_vs_<ctrl>.csv (so sibling contrasts of the
    same study don't collide) and its own GSEA. Per-step decisions are tagged with the contrast
    label. Returns {control, treatment, design_col, deg_csv, n_deg, n_gsea_sig, status}."""
    label = f"{treat} vs {ctrl}"
    print(_invoke_da_method(method, counts_path, da_input_path, metadata_for_design,
                            col, ctrl, treat, study_out)[:300])

    deg_csv = os.path.join(study_out, deg_filename(treat, ctrl))
    res = {"control": ctrl, "treatment": treat, "design_col": col,
           "deg_csv": deg_csv, "n_deg": None, "n_gsea_sig": None, "status": None}
    if not os.path.exists(deg_csv):
        res["status"] = "deg_failed"
        dlog.record(method, "failed", reason="DEG output missing", contrast=label,
                    design_column=col, control=ctrl, treatment=treat)
        with open(fail_log, "a", encoding="utf-8") as f:
            f.write(f"{acc} | DEG output missing for {col}: {label} ({method})\n")
        return res

    deg_df = pd.read_csv(deg_csv, index_col=0)
    res["n_deg"] = int((deg_df["padj"] < 0.05).sum())
    n_tested = int(deg_df["padj"].notna().sum())
    dlog.record(method, "ok",
                reason=(f"{method} differential expression on contrast '{label}' (design column '{col}', "
                        f"{ctrl} vs {treat}); {res['n_deg']} genes at padj<0.05 of {n_tested} tested"),
                n_deg=res["n_deg"], contrast=label,
                design_column=col, control=ctrl, treatment=treat,
                model_params=_da_model_params(method, matrix_type))

    sanity = _deg_sanity_flags(res["n_deg"], n_tested, metadata_for_design, col, ctrl, treat)
    _record_deg_sanity(res, sanity, label, method, dlog, fail_log, acc)

    res["n_gsea_sig"], res["status"] = _gsea_for_deg(
        deg_csv, organism, study_out, dlog, fail_log, acc, label)
    return res


def _safe_eval_label(text: str) -> str:
    return re.sub(r"_+", "_", re.sub(r'[^A-Za-z0-9_.-]+', "_", str(text))).strip("_") or "contrast"


def _run_subset_evaluation(method, counts_path, da_input_path, metadata_for_design,
                           col, ctrl, treat, study_out, organism, matrix_type,
                           dlog, fail_log, acc, n_runs=3, subset_fraction=0.8,
                           min_group_n=2, include_gsea=False, use_llm_judge=False,
                           seed=42):
    """Run repeated stratified subset DA for one contrast, then compare outputs.

    This is an opt-in stability check: it keeps the main analysis untouched, writes all subset
    artifacts under `<study_out>/evaluation/<contrast>/`, and summarizes whether reruns on
    sample subsets preserve the same DEG/GSEA signal. It never raises to the main pipeline.
    """
    label = f"{treat} vs {ctrl}"
    eval_root = os.path.join(study_out, "evaluation", _safe_eval_label(label))
    os.makedirs(eval_root, exist_ok=True)
    try:
        meta = pd.read_csv(metadata_for_design, index_col=0)
        sub_meta = meta[meta[col].astype(str).isin([str(ctrl), str(treat)])].copy()
        groups = {
            str(ctrl): sub_meta[sub_meta[col].astype(str) == str(ctrl)],
            str(treat): sub_meta[sub_meta[col].astype(str) == str(treat)],
        }
        if any(len(g) < min_group_n for g in groups.values()):
            reason = (f"too few samples for subset evaluation: "
                      f"{ctrl}={len(groups[str(ctrl)])}, {treat}={len(groups[str(treat)])}, "
                      f"min_group_n={min_group_n}")
            dlog.record("subset_evaluation", "skipped", reason=reason, contrast=label)
            return {"status": "skipped", "reason": reason}

        deg_csvs, gsea_csvs = [], []
        rng = np.random.default_rng(seed)
        for run_idx in range(1, int(n_runs) + 1):
            run_dir = os.path.join(eval_root, f"run_{run_idx}")
            os.makedirs(run_dir, exist_ok=True)
            sampled_parts = []
            for group_name, gdf in groups.items():
                n_take = max(int(min_group_n), int(np.floor(len(gdf) * float(subset_fraction))))
                n_take = min(len(gdf), max(1, n_take))
                # Use pandas' stable sampling with a generated integer seed so runs are reproducible
                # while still drawing different subsets.
                rs = int(rng.integers(0, 2**31 - 1))
                sampled_parts.append(gdf.sample(n=n_take, replace=False, random_state=rs))
            sampled = pd.concat(sampled_parts, axis=0)
            subset_meta = os.path.join(run_dir, f"metadata_subset_run_{run_idx}.csv")
            sampled.to_csv(subset_meta)
            print(f"  [eval] subset run {run_idx}/{n_runs}: {len(sampled)} samples -> {run_dir}")
            msg = _invoke_da_method(method, counts_path, da_input_path, subset_meta,
                                    col, ctrl, treat, run_dir)
            print(str(msg)[:200])
            deg_csv = os.path.join(run_dir, deg_filename(treat, ctrl))
            if os.path.exists(deg_csv):
                deg_csvs.append(deg_csv)
                if include_gsea:
                    n_sig, gstatus = _gsea_for_deg(
                        deg_csv, organism, run_dir, dlog, fail_log, acc,
                        f"{label} subset_eval_run_{run_idx}")
                    gsea_path = os.path.join(
                        run_dir, f"{os.path.splitext(os.path.basename(deg_csv))[0]}_GSEA_Hallmark.csv")
                    if gstatus == "deg_gsea_ok" and os.path.exists(gsea_path):
                        gsea_csvs.append(gsea_path)
            else:
                with open(fail_log, "a", encoding="utf-8") as f:
                    f.write(f"{acc} | subset evaluation DEG missing for {label} run {run_idx}\n")

        if len(deg_csvs) < 2 and len(gsea_csvs) < 2:
            reason = f"not enough successful subset outputs: DEG={len(deg_csvs)}, GSEA={len(gsea_csvs)}"
            dlog.record("subset_evaluation", "failed", reason=reason, contrast=label)
            return {"status": "failed", "reason": reason}

        summary = evaluate_repeated_results_core(
            deg_csvs=deg_csvs,
            gsea_csvs=gsea_csvs,
            output_dir=eval_root,
            label="subset_stability",
            use_llm_judge=use_llm_judge,
        )
        dlog.record("subset_evaluation", "ok", contrast=label,
                    verdict=summary.get("judge", {}).get("verdict"),
                    deg=summary.get("deg"), gsea=summary.get("gsea"),
                    artifacts=summary.get("artifacts"))
        print(f"  [eval] {label}: {summary.get('judge', {}).get('verdict')} | "
              f"{summary.get('judge', {}).get('reasoning')}")
        return {"status": "ok", "summary": summary}
    except Exception as e:
        reason = f"{type(e).__name__}: {e}"
        dlog.record("subset_evaluation", "failed", reason=reason, contrast=label)
        with open(fail_log, "a", encoding="utf-8") as f:
            f.write(f"{acc} | subset evaluation failed for {label}: {reason}\n")
        return {"status": "failed", "reason": reason}


def _align_metadata_to_expression(metadata_csv, expr_path, study_out, acc):
    """Restrict metadata rows to samples that actually appear in the expression
    file, renaming the index to use expression-column names. Writes a filtered
    sibling CSV and returns (path_to_use, info_dict).

    Why: LLM-A picks a control-vs-treatment contrast by reading metadata column
    values. When GEO metadata has more samples than the supplementary expression
    file (e.g. GSE317978: 25 GSMs in metadata, 6 samples in the supplementary
    matrix), LLM-A can pick a contrast whose samples don't exist in the data,
    and DA fails downstream with no useful diagnostic. Pre-aligning here forces
    LLM-A to reason over the actual sample set.

    On any non-trivial failure (read error, no numeric cols, no alignment) this
    returns the ORIGINAL metadata_csv path so the existing behaviour is preserved
    — the bug fix only kicks in when we CAN align cleanly. info_dict's "verdict"
    field records what happened for the decision log."""
    try:
        meta_df = pd.read_csv(metadata_csv, index_col=0)
        expr_df = pd.read_csv(expr_path, sep=None, engine="python",
                              index_col=0, nrows=200)
    except Exception as e:
        return metadata_csv, {"verdict": "read_failed", "error": str(e)}

    coerced = expr_df.apply(pd.to_numeric, errors="coerce")
    numeric_cols = [c for c in expr_df.columns if not coerced[c].isna().all()]
    # Exclude derived stat columns from the sample candidate set — they're
    # numeric but not per-sample (e.g. diffexp_log2fc_*, *_pvalue). Without
    # this filter, LLM-A's alignment tries to map metadata GSMs to stat cols
    # too, inflating false-positive risk. Same rationale as _classify_matrix
    # (GSE317978 bug).
    sample_cols = [c for c in numeric_cols if not _is_derived_stat_column(c)]
    if not sample_cols:
        sample_cols = numeric_cols  # fall back rather than abort
    info = {
        "n_meta": len(meta_df),
        "n_numeric_cols": len(numeric_cols),
        "n_sample_cols_after_stat_filter": len(sample_cols),
    }
    if not sample_cols:
        info["verdict"] = "no_numeric_cols"
        return metadata_csv, info

    # Fast path: counts cols are already in metadata index — no LLM call needed.
    meta_idx_set = set(str(x) for x in meta_df.index)
    common_exact = meta_idx_set & set(sample_cols)
    exact_target = min(len(sample_cols), len(meta_df))
    if common_exact and len(common_exact) >= max(1, int(np.ceil(exact_target * 0.5))):
        info["verdict"] = "exact_match"
        info["n_aligned"] = len(common_exact)
        if len(common_exact) < len(meta_df):
            filtered = meta_df[meta_df.index.astype(str).isin(common_exact)]
            out_path = os.path.join(study_out, f"{acc}_metadata_aligned.csv")
            filtered.to_csv(out_path)
            info["filtered"] = True
            return out_path, info
        return metadata_csv, info

    # Slow path: counts cols use a different naming convention. Use the same
    # LLM-aided alignment cascade that DA tools use, so the contrast detection
    # and DA see consistent sample identities.
    from tools.llm_helpers import align_samples_with_llm_fallback
    mapping, method = align_samples_with_llm_fallback(sample_cols, meta_df)
    info["method"] = method
    if not mapping:
        info["verdict"] = "no_align"
        return metadata_csv, info

    info["n_aligned"] = len(mapping)
    # No actual filtering needed if alignment covered every metadata row.
    if len(mapping) == len(meta_df):
        info["verdict"] = "all_aligned"
        # Even when all rows aligned, the index naming might differ — rename so
        # downstream DA's exact-match strategy succeeds without re-running LLM-B.
        renamed = meta_df.rename(index={str(k): v for k, v in mapping.items()})
        out_path = os.path.join(study_out, f"{acc}_metadata_aligned.csv")
        renamed.to_csv(out_path)
        info["filtered"] = True
        return out_path, info

    # Partial: keep only aligned rows, rename to counts col names so DA exact-matches.
    aligned_meta_ids = set(mapping.keys())
    filtered = meta_df[meta_df.index.astype(str).isin(aligned_meta_ids)].copy()
    filtered.rename(index={k: mapping[str(k)] for k in filtered.index}, inplace=True)
    out_path = os.path.join(study_out, f"{acc}_metadata_aligned.csv")
    filtered.to_csv(out_path)
    info["verdict"] = "filtered"
    info["filtered"] = True
    return out_path, info


# Strong baseline/control markers: when a value contains one of these as a WHOLE WORD it is the
# control even if it also contains a treatment keyword (e.g. 'pre-exercise' is the baseline, not a
# treatment, despite the word 'exercise'). Whole-word matching avoids substring collisions like
# 'rest' inside 'resistance'. These are inherent control concepts, so a real treatment value won't
# carry one as a whole word.
_BASELINE_MARKERS = ("pre", "baseline", "basal", "sedentary", "untrained", "sham",
                     "control", "vehicle", "naive", "wildtype", "wild-type")
_BASELINE_RE = [re.compile(r"\b" + re.escape(b) + r"\b") for b in _BASELINE_MARKERS]


def _auto_detect_contrasts(metadata_csv, treatment_keywords, control_keywords, min_per_group=2):
    """Find the metadata design column and return ALL clean control-vs-treatment contrasts in it
    — one per treatment-like LEVEL (req #8).

    Biology: an exercise study often encodes its arms in ONE column with a baseline/control value
    plus several treatment levels — e.g. time.point = {pre, immediately-post, 1h-post, 24h-post},
    or treatment = {Control, Training-1week, Training-2weeks, Training-4weeks}. Pooling every
    'post'/'Training' level into a single treatment group mixes biologically distinct conditions
    (a 1-week and a 2-week trained mouse are NOT the same). So instead of one pooled contrast we
    emit one (control vs each treatment level): immediately-post vs pre, 1h-post vs pre, ... — each
    becomes its own differential analysis downstream.

    Column scoring (pick the single best design column):
      +1 base for any column with a ctrl-only value and >=1 treat-only level
      +1 if the column name mentions 'treatment' / 'condition' / 'time'
      +1 if every emitted contrast has both groups >= 3 samples (DESeq2-viable)
    Ties broken toward the column yielding MORE valid contrasts (richer stratification).

    A value is a ctrl candidate only if it matches a control keyword AND NOT a treatment keyword
    (avoids ambiguous strings like 'sedentary control'); symmetrically for treatment levels. Only
    levels with >= min_per_group samples (control included) are kept.

    Returns a list of (column, control_value, treatment_value) — possibly length 1 (identical to
    the old single-contrast behavior) — or [] if no column yields a clean control + >=1 treatment."""
    try:
        df = pd.read_csv(metadata_csv, index_col=0)
    except Exception:
        return []
    tk = [k.lower() for k in (treatment_keywords or [])]
    ck = [k.lower() for k in (control_keywords or [])]
    if not tk or not ck:
        return []

    name_hints = ("characteristics", "title", "source", "treatment", "group",
                  "condition", "phenotype", "time")
    best = None  # (score, n_contrasts, col, ctrl_val, [treat_vals])
    for col in df.columns:
        col_low = col.lower()
        if not any(h in col_low for h in name_hints):
            continue
        vals = df[col].dropna().astype(str).unique().tolist()
        if not (2 <= len(vals) <= 8):
            continue

        # The (single) control value + ALL non-ambiguous treatment levels in this column.
        ctrl_val = None
        treat_vals = []
        for v in vals:
            v_low = v.lower()
            hits_ctrl = any(k in v_low for k in ck)
            hits_treat = any(k in v_low for k in tk)
            # A whole-word strong baseline marker makes control win over an incidental treatment
            # keyword in the same value (rescues 'pre-exercise', 'sedentary control', ...).
            strong_baseline = any(rx.search(v_low) for rx in _BASELINE_RE)
            if hits_ctrl and (not hits_treat or strong_baseline):
                if ctrl_val is None:
                    ctrl_val = v
            elif hits_treat and not hits_ctrl:
                treat_vals.append(v)

        if not (ctrl_val and treat_vals):
            continue
        ctrl_n = int((df[col] == ctrl_val).sum())
        if ctrl_n < min_per_group:
            continue
        treat_vals = [t for t in treat_vals
                      if t != ctrl_val and int((df[col] == t).sum()) >= min_per_group]
        if not treat_vals:
            continue

        score = 1
        if "treatment" in col_low or "condition" in col_low or "time" in col_low:
            score += 1
        if all(min(ctrl_n, int((df[col] == t).sum())) >= 3 for t in treat_vals):
            score += 1

        cand = (score, len(treat_vals), col, ctrl_val, treat_vals)
        if best is None or (cand[0], cand[1]) > (best[0], best[1]):
            best = cand

    if best is None:
        return []
    _, _, col, ctrl_val, treat_vals = best
    return [(col, ctrl_val, t) for t in treat_vals]


def _auto_detect_design(metadata_csv, treatment_keywords, control_keywords):
    """Backward-compatible single-contrast wrapper over _auto_detect_contrasts: returns the first
    (column, control_value, treatment_value) or None. Kept for callers/tests that expect one pick."""
    contrasts = _auto_detect_contrasts(metadata_csv, treatment_keywords, control_keywords)
    return contrasts[0] if contrasts else None


def _viable_design_columns(df, tk, ck, min_n):
    """Metadata columns that yield a clean keyword-grounded control + >=1 treatment level, each
    with >= min_n samples — mirrors the per-column viability rule of _auto_detect_contrasts. Used
    only to detect CROSS-COLUMN ambiguity for the LLM-validation skip gate."""
    hints = ("characteristics", "title", "source", "treatment", "group",
             "condition", "phenotype", "time")
    out = []
    for col in df.columns:
        if not any(h in col.lower() for h in hints):
            continue
        vals = df[col].dropna().astype(str).unique().tolist()
        if not (2 <= len(vals) <= 8):
            continue
        ctrl_val, treat_vals = None, []
        for v in vals:
            vl = v.lower()
            hc, ht = any(k in vl for k in ck), any(k in vl for k in tk)
            sb = any(rx.search(vl) for rx in _BASELINE_RE)
            if hc and (not ht or sb):
                if ctrl_val is None:
                    ctrl_val = v
            elif ht and not hc:
                treat_vals.append(v)
        if not (ctrl_val and treat_vals):
            continue
        if int((df[col] == ctrl_val).sum()) < min_n:
            continue
        if any(t != ctrl_val and int((df[col] == t).sum()) >= min_n for t in treat_vals):
            out.append(col)
    return out


def _python_pick_is_confident(metadata_csv, design, treatment_keywords, control_keywords, min_n=3):
    """True only when the Python contrast pick is UNAMBIGUOUS -> the LLM contrast-validation call
    would merely confirm it and can be SKIPPED (per-study cost cut). Conditions:
      - a pick exists (a returned contrast is, by construction, already keyword-grounded on BOTH arms),
      - its chosen control & treatment arms each have >= min_n samples (DESeq2-viable), AND
      - EXACTLY ONE metadata column is a viable keyword-grounded design (no cross-column ambiguity —
        the exact failure mode the LLM was protecting against).
    Fails safe to False (-> keep the LLM) on any read error / missing keywords / no design."""
    if not design:
        return False
    tk = [k.lower() for k in (treatment_keywords or []) if k]
    ck = [k.lower() for k in (control_keywords or []) if k]
    if not tk or not ck:
        return False
    try:
        df = pd.read_csv(metadata_csv, index_col=0)
    except Exception:
        return False
    col, ctrl, treat = design
    if col not in df.columns:
        return False
    if int((df[col] == ctrl).sum()) < min_n or int((df[col] == treat).sum()) < min_n:
        return False
    return len(_viable_design_columns(df, tk, ck, min_n)) == 1


@tool
def run_batch_geo_pipeline(
    accessions: list[str],
    organism: str = "Mouse",
    treatment_keywords: list[str] | None = None,
    control_keywords: list[str] | None = None,
    output_base: str = "./output",
    run_label: str = "",
    source_search_csv: str = "",
    raw_da_method: str = "deseq2",
    llm_datatype: bool = True,
    evaluate_subsets: bool = False,
    evaluation_runs: int = 3,
    evaluation_subset_fraction: float = 0.8,
    evaluation_include_gsea: bool = False,
    evaluation_use_llm_judge: bool = False,
) -> str:
    """
    Run download + raw-counts detection + preprocess + QC on each GEO accession in
    parallel cohorts. If BOTH treatment_keywords AND control_keywords are provided
    AND a metadata column with a matching two-group split is auto-detected, ALSO
    run DESeq2 + GSEA for that study.

    Per-study failures are caught (logged to failures.log) and do NOT abort the batch.
    Returns a status summary; per-study outputs live in output_base/run_label/{accession}/.

    Args:
        accessions: List of GSE accessions to process.
        organism: 'Mouse' or 'Human'. Forwarded to GSEA Hallmark library selection.
        treatment_keywords: Substrings that identify the treatment group in metadata
            values (e.g. ['exercise', 'training', 'HIIT', 'exe', 'run']). Case-insensitive.
            Required (with control_keywords) for auto-DEG.
        control_keywords: Substrings that identify the control group
            (e.g. ['sedentary', 'control', 'sham', 'sed']). Case-insensitive.
        output_base: Root directory under which a cohort_{run_label}/ subdir is created.
        run_label: Label for the cohort (e.g. 'Exercise_top10'); used in the dir name.
        source_search_csv: Optional path to the search_geo_studies result CSV that
            produced this accession list; entries matching the accessions are recorded
            at the start of workflow.log for full provenance.
        raw_da_method: Which DA method to use for RAW-count studies — one of
            'deseq2' (default), 'edger', 'limma-voom', 'auto' (deterministic rule:
            DESeq2, no LLM call — req #1), 'auto-llm' (per-study LLM picker based on
            n-samples/design), or 'all' (run DESeq2 + edgeR + limma-voom on the same
            matrix and report the CONSENSUS — genes significant in >=2 methods — with
            per-method DEG files, a per-gene comparison CSV, and pairwise log2FC
            concordance). The chosen method is recorded in summary.csv's da_method
            column. The log/FPKM/TPM branch always uses limma-trend ('all' there ran
            limma-trend alone, since the NB methods require integer counts).
        llm_datatype: When True (default), the LLM determines the matrix DATA TYPE (req #1)
            whenever the fast heuristic is uncertain — i.e. on any decimal matrix (the FPKM-vs-log
            boundary) or when the filename/platform hints proteomics / methylation. Integer raw
            counts are detected by the heuristic and SKIP the LLM call (cost ≈ 0). The decision
            drives the DA route: raw→DESeq2/edgeR/voom, fpkm/log→limma, proteomics→limma,
            methylation β→M-values→limma. Set False to force the heuristic-only path.
        evaluate_subsets: If True, after each successful DA contrast, run repeated stratified
            subset analyses and compare the resulting DEG/GSEA files for stability. This is opt-in
            because it multiplies runtime and, if evaluation_include_gsea=True, may add network calls.
        evaluation_runs: Number of subset reruns per contrast when evaluate_subsets=True.
        evaluation_subset_fraction: Fraction of each contrast arm to keep per subset rerun.
        evaluation_include_gsea: If True, run GSEA for each subset DEG and include pathway stability
            in the evaluation. Default False keeps the evaluation cheap/offline after DA.
        evaluation_use_llm_judge: If True, ask an independent structured LLM judge to interpret the
            stability metrics; otherwise a deterministic heuristic verdict is used.
    """
    label = run_label or datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_label = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in label)
    run_dir = os.path.join(output_base, f"cohort_{safe_label}")
    os.makedirs(run_dir, exist_ok=True)
    status_path = os.path.join(run_dir, "run_status.json")
    status_tracker = RunStatusTracker(
        status_path, run_id=f"cohort_{safe_label}", profile="geo_batch",
        stages=("acquire", "classify", "preprocess", "qc", "align", "design",
                "analyze_enrich", "evaluate", "report"),
        study_total=len(accessions), renderer=ConsoleStatusRenderer(sys.stdout),
    )
    status_tracker.start("batch initialized")
    reset_llm_alignment_cache()
    llm_usage_start = llm_usage_checkpoint()
    fail_log = os.path.join(run_dir, "failures.log")
    log_path = os.path.join(run_dir, "workflow.log")
    auto_deg = bool(treatment_keywords and control_keywords)

    log_file = open(log_path, "w", encoding="utf-8")
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = _Tee(old_stdout, log_file)
    try:
        print(f"# Batch GEO pipeline | run_label={label} | start={datetime.now().isoformat(timespec='seconds')}")
        print(f"# accessions ({len(accessions)}): {accessions}")
        print(f"# organism={organism}")
        print(f"# treatment_keywords={treatment_keywords}")
        print(f"# control_keywords={control_keywords}")
        print(f"# output_dir={run_dir}")
        if source_search_csv and os.path.exists(source_search_csv):
            print(f"# source_search_csv={source_search_csv}")
            try:
                src_df = pd.read_csv(source_search_csv)
                cols = [c for c in ("accession", "n_samples", "organism", "title") if c in src_df.columns]
                subset = src_df[src_df["accession"].isin(accessions)] if "accession" in src_df.columns else src_df.head(len(accessions))
                print("# search context (matched rows):")
                print(subset[cols].to_string(index=False))
            except Exception as e:
                print(f"# (failed to read source_search_csv: {e})")
        print()

        summary_rows = []
        for i, acc in enumerate(accessions, 1):
            status_tracker.begin_study(acc, i, len(accessions))
            status_tracker.set_stage("acquire", current_tool="download_geo_data",
                                     message="downloading GEO metadata and supplements")
            print(f"\n========== [{i}/{len(accessions)}] {acc} ==========")
            row = {
                "accession": acc, "status": "started", "n_samples": None,
                "design_col": None, "control": None, "treatment": None,
                "n_deg": None, "n_gsea_sig": None, "counts_file": None, "error": None,
                "llm_validated": None, "llm_overrode": None, "llm_reasoning": None,
                "sex_mismatch": None, "matrix_type": None, "matrix_type_source": None, "da_method": None,
                "da_method_reason": None,
                # req #8: a study may split into several control-vs-treatment-level contrasts
                # (e.g. 1-week / 2-week / 4-week training each vs control). design_col/control/
                # treatment hold the FIRST contrast (back-compat); these summarize all of them.
                "n_contrasts": None, "contrasts": None, "n_deg_detail": None,
                # raw_da_method='all': multi-method consensus reporting (DESeq2/edgeR/limma-voom on
                # the same data). n_deg above then holds the CONSENSUS (>=2 methods) total.
                "da_methods_run": None, "da_per_method_deg": None,
                "da_consensus_deg": None, "da_logfc_r": None,
                # post-DA implausibility guard: 'ok' or a flag like implausible_sig_fraction /
                # tiny_n_per_group when a result is statistically untrustworthy (req: GSE317978).
                "deg_sanity": None,
                "eval_verdict": None, "eval_deg_log2fc_r": None,
                "eval_sig_deg_jaccard": None, "eval_gsea_nes_r": None,
                "eval_sig_pathway_jaccard": None, "eval_summary_json": None,
            }
            data_dir = os.path.join("data", acc)
            study_out = os.path.join(run_dir, acc)
            os.makedirs(study_out, exist_ok=True)
            dlog = _DecisionLog(acc)
            decisions_path = os.path.join(study_out, "decisions.json")
            try:
                print(download_geo_data.invoke({"geo_accession": acc, "base_dir": "data"})[:200])
                metadata_csv = os.path.join(data_dir, f"{acc}_metadata.csv")
                if not os.path.exists(metadata_csv):
                    dlog.record("download", "failed", reason="metadata not found", path=metadata_csv)
                    raise RuntimeError(f"metadata not found: {metadata_csv}")
                _meta_hint_df = pd.read_csv(metadata_csv, index_col=0)
                row["n_samples"] = int(_meta_hint_df.shape[0])
                platform_hint = _platform_hint_from_metadata(_meta_hint_df)
                dlog.record("download", "ok", n_samples=row["n_samples"])

                print(download_supplementary_files.invoke({"geo_accession": acc, "base_dir": "data"})[:200])

                status_tracker.set_stage("classify", message="selecting and classifying expression matrix")
                counts_path, matrix_type = _find_expression_file(data_dir)
                matrix_type_source = "heuristic"

                # req #1: LLM data-type RESCUE. The heuristic dropped every candidate as
                # non-analyzable (its 'ambiguous' bucket). Ask Claude on the top candidate — it can
                # recognize a real FPKM/log matrix the heuristic gave up on, or a proteomics/methyl
                # matrix the heuristic has no concept of. fail-soft: still skips if nothing confident.
                if (counts_path is None and llm_datatype
                        and ("not_analyzable" in str(matrix_type) or "ambiguous" in str(matrix_type))):
                    rescue_cands = _gather_matrix_candidates(data_dir)
                    if rescue_cands:
                        top = rescue_cands[0]
                        h_cls, _ = _classify_matrix(top)
                        llm_res = _llm_datatype_decision(top, h_cls, platform_hint, organism)
                        if llm_res and llm_res.confidence in ("high", "medium"):
                            new_path, mapped, note = _apply_llm_matrix_type(llm_res, top)
                            if mapped in _ANALYZABLE_TYPES:
                                counts_path, matrix_type, matrix_type_source = new_path, mapped, "llm-rescue"
                                dlog.record("matrix_type_llm", "rescue", heuristic=h_cls,
                                            llm_type=llm_res.matrix_type, mapped=mapped,
                                            confidence=llm_res.confidence, reason=llm_res.reasoning, note=note)
                                print(f"  [datatype-llm] RESCUE {os.path.basename(top)}: "
                                      f"{h_cls} → {mapped} ({llm_res.confidence}) — {llm_res.reasoning}")

                if counts_path is None:
                    row["status"] = f"skipped_{matrix_type}"
                    status_tracker.add_warning(f"{acc}: {row['status']}")
                    status_tracker.set_stage("report", message="recording skipped study")
                    dlog.record("counts_detection", "skip", reason=matrix_type)
                    dlog.save(decisions_path, status=row["status"])
                    summary_rows.append(row)
                    print(f"[SKIP] {acc}: {matrix_type}")
                    continue

                # req #1: LLM data-type CROSS-CHECK on a confident heuristic pick. Fires only on the
                # decimal/ambiguous zone or proteomics/methyl hints (raw counts skip → cost ≈ 0). The
                # LLM may re-route within the limma family (fpkm<->log), promote proteomics, or detect
                # methylation β and trigger the β→M pre-transform. Never demotes to raw_counts (the
                # heuristic owns integer detection); ambiguous LLM answers keep the heuristic pick.
                if llm_datatype and matrix_type_source == "heuristic":
                    llm_res = _llm_datatype_decision(counts_path, matrix_type, platform_hint, organism)
                    if llm_res and llm_res.confidence in ("high", "medium"):
                        new_path, mapped, note = _apply_llm_matrix_type(llm_res, counts_path)
                        if mapped in ("fpkm_or_tpm", "log_transformed") and (
                                mapped != matrix_type or new_path != counts_path):
                            print(f"  [datatype-llm] {matrix_type} → {mapped} "
                                  f"({llm_res.confidence}) — {llm_res.reasoning}")
                            dlog.record("matrix_type_llm", "override", heuristic=matrix_type,
                                        llm_type=llm_res.matrix_type, mapped=mapped,
                                        confidence=llm_res.confidence, reason=llm_res.reasoning, note=note)
                            counts_path, matrix_type, matrix_type_source = new_path, mapped, "llm"
                        else:
                            dlog.record("matrix_type_llm", "confirm", heuristic=matrix_type,
                                        llm_type=llm_res.matrix_type, confidence=llm_res.confidence,
                                        reason=llm_res.reasoning)

                row["counts_file"] = os.path.relpath(counts_path, "data")
                row["matrix_type"] = matrix_type
                row["matrix_type_source"] = matrix_type_source
                dlog.record("counts_detection", "selected", reason=matrix_type,
                            counts_file=row["counts_file"], source=matrix_type_source)
                print(f"expression matrix: {counts_path} | type={matrix_type} | source={matrix_type_source}")

                # Dispatch by matrix type:
                #   raw_counts          -> preprocess_counts (CPM+log2 side artifact) + DESeq2 on raw
                #   log_transformed     -> skip preprocess (already log scale) + limma on file as-is
                #   fpkm_or_tpm         -> log2(x+1) transform + limma on the log2 file
                # preprocess_counts assumes raw integer counts (CPM normalization); applying it to
                # FPKM/TPM produces double-normalized garbage and to log_transformed produces values
                # like log2(CPM(log2(x+1))) which is biologically meaningless.
                is_raw = (matrix_type in ("raw_counts", "raw_counts_from_tar"))
                status_tracker.set_stage("preprocess", message=f"preparing {matrix_type} matrix")
                da_methods = None  # set only for raw_da_method='all'; else falls back to [da_method]
                if is_raw:
                    print(preprocess_counts.invoke({"counts_csv": counts_path, "output_dir": study_out})[:200])
                    da_input_path = counts_path
                    # Resolve which of the three raw-counts methods to use.
                    chosen = raw_da_method.lower().strip()
                    if chosen == "all":
                        # Run EVERY valid raw method and report the consensus (mentor: "use as many
                        # methods as possible"). DESeq2 stays the back-compat first method / GSEA rep.
                        da_methods = list(_ALL_RAW_METHODS)
                        row["da_method"] = "all (deseq2+edger+limma-voom)"
                        row["da_method_reason"] = (
                            "run as many valid methods as possible: all three raw-count backends "
                            "(DESeq2 / edgeR / limma-voom) on the same matrix. Headline n_deg is the "
                            "CONSENSUS (genes significant in >=2 methods); per-method DEG files, a "
                            "per-gene comparison CSV, and pairwise log2FC concordance are kept.")
                        dlog.record("da_method_select", "all", methods=da_methods,
                                    reason=row["da_method_reason"])
                        print(f"  [da-method] ALL: {da_methods} (consensus reporting)")
                    elif chosen == "auto":
                        # req #1: deterministic, zero-cost pick (no per-study LLM call).
                        method, reason = choose_raw_da_method_rule(row["n_samples"])
                        row["da_method"] = method
                        row["da_method_reason"] = reason
                        dlog.record("da_method_select", "rule", method=method, reason=reason)
                        print(f"  [da-method] rule picked {method} (no LLM)")
                    elif chosen == "auto-llm":
                        # Opt-in: restore the per-study LLM method picker.
                        pick = choose_raw_da_method_with_llm(
                            accession=acc, n_samples=row["n_samples"], organism=organism)
                        if pick and pick.method in _RAW_DA_METHODS:
                            row["da_method"] = pick.method
                            row["da_method_reason"] = pick.reasoning
                            dlog.record("da_method_select", "llm", method=pick.method, reason=pick.reasoning)
                            print(f"  [da-method] LLM picked {pick.method}: {pick.reasoning}")
                        else:
                            row["da_method"] = "deseq2"
                            row["da_method_reason"] = "LLM unavailable/invalid; defaulted to deseq2 (robust NB default)"
                            dlog.record("da_method_select", "default", method="deseq2",
                                        reason=row["da_method_reason"])
                    elif chosen in _RAW_DA_METHODS:
                        row["da_method"] = chosen
                        row["da_method_reason"] = f"specified by caller via raw_da_method='{chosen}'"
                        dlog.record("da_method_select", "param", method=chosen, reason=row["da_method_reason"])
                    else:
                        row["da_method"] = "deseq2"
                        row["da_method_reason"] = f"unknown raw_da_method={raw_da_method!r}; defaulted to deseq2"
                        dlog.record("da_method_select", "default", method="deseq2", reason=row["da_method_reason"])
                elif matrix_type == "fpkm_or_tpm":
                    da_input_path = _log2_transform_matrix(counts_path)
                    dlog.record("log2_transform", "ok", source=row["counts_file"],
                                output=os.path.relpath(da_input_path, "data"))
                    row["da_method"] = "limma"
                    row["da_method_reason"] = ("limma-trend: FPKM/TPM (linear-scale) matrix -> log2(x+1) "
                                               "then moderated-t/eBayes; the raw-count methods "
                                               "(DESeq2/edgeR/limma-voom) require integer counts.")
                else:  # log_transformed
                    da_input_path = counts_path
                    row["da_method"] = "limma"
                    row["da_method_reason"] = ("limma-trend: matrix is already log-scale -> moderated-t/eBayes "
                                               "directly; the raw-count methods (DESeq2/edgeR/limma-voom) "
                                               "require integer counts.")

                # 'all' on a non-integer matrix can't honestly run the NB methods — limma-trend is
                # the only valid backend. Say so rather than pretend a multi-method comparison.
                if not is_raw and raw_da_method.lower().strip() == "all":
                    row["da_method_reason"] += (" | raw_da_method='all' requested, but only limma-trend "
                                                "is valid for a non-integer matrix (DESeq2/edgeR/limma-voom "
                                                "require raw integer counts) — ran limma-trend alone.")
                if da_methods is None:
                    da_methods = [row["da_method"]]

                status_tracker.set_stage("qc", current_tool="sample_qc_summary",
                                         message="running sample quality summary")
                print(sample_qc_summary.invoke({
                    "counts_csv": da_input_path, "metadata_csv": metadata_csv, "output_dir": study_out,
                })[:200])
                row["status"] = "preprocess_ok"
                dlog.record("preprocess_qc", "ok", da_method=row["da_method"],
                            qc_filter=("low-expression filter min_count>=10 in >=3 samples + log2(CPM+1) "
                                       "— applied to the QC/normalized side artifacts (PCA/correlation); "
                                       "raw-count DA runs on the unfiltered matrix with method-internal "
                                       "normalization" if is_raw
                                       else "n/a — non-raw matrix, no CPM filter (DA runs on log-scale input)"))

                sex = _run_sex_check(counts_path, metadata_csv, organism, study_out)
                row["sex_mismatch"] = sex["n_mismatch"]
                dlog.record("sex_check", sex["verdict"], reason=sex["summary"],
                            n_mismatch=sex["n_mismatch"], mismatched=sex["mismatched"])
                if sex["mismatched"]:
                    status_tracker.add_warning(f"{acc}: sex metadata mismatch")
                    print(f"  [sex-check] WARNING {len(sex['mismatched'])} mismatch(es) vs metadata: {sex['mismatched']}")
                else:
                    print(f"  [sex-check] {sex['verdict']} ({sex['summary']})")

                if auto_deg:
                    status_tracker.set_stage("align", message="aligning metadata to expression samples")
                    # Pre-align metadata to actual expression-file samples BEFORE LLM-A
                    # reads it. Prevents the GSE317978-class bug where LLM-A picks a
                    # contrast whose samples don't exist in the expression matrix.
                    metadata_for_design, align_info = _align_metadata_to_expression(
                        metadata_csv, da_input_path, study_out, acc)
                    dlog.record("metadata_alignment",
                                align_info.get("verdict", "unknown"),
                                **{k: v for k, v in align_info.items() if k != "verdict"})
                    if align_info.get("filtered"):
                        print(f"  [metadata-align] {align_info['n_meta']} -> "
                              f"{align_info.get('n_aligned', '?')} samples "
                              f"({align_info.get('method', 'exact_match')})")
                    elif align_info.get("verdict") == "no_align":
                        print(f"  [metadata-align] WARNING could not align metadata "
                              f"to expression cols; LLM-A will reason over full metadata "
                              f"({align_info.get('method')})")

                    status_tracker.set_stage("design", message="detecting control-treatment contrasts")
                    contrasts = _auto_detect_contrasts(
                        metadata_for_design, treatment_keywords, control_keywords)
                    design = contrasts[0] if contrasts else None  # representative for LLM validation
                    if design is not None:
                        print(f"auto-design (python): {design[0]} | {len(contrasts)} contrast(s): "
                              + "; ".join(f"{t} vs {c}" for _, c, t in contrasts))
                        dlog.record("auto_design_python", "match",
                                    design_column=design[0], control=design[1], treatment=design[2],
                                    n_contrasts=len(contrasts),
                                    contrasts=[{"control": c, "treatment": t} for _, c, t in contrasts])
                    else:
                        print("auto-design (python): NO MATCH")
                        dlog.record("auto_design_python", "no_match")

                    # cost gate: skip the per-study LLM contrast validation when the Python pick is
                    # UNAMBIGUOUS (both arms keyword-grounded & n>=3, and no competing design column)
                    # — the LLM would only confirm it. Ambiguous / no-design studies still go to the
                    # LLM (the safety net for keyword gaps like PBS/Vehicle and multi-axis designs).
                    skipped_confident = _python_pick_is_confident(
                        metadata_for_design, design, treatment_keywords, control_keywords)
                    if skipped_confident:
                        llm_result = None
                        print(f"  [llm-validation] SKIPPED (cost) — python pick unambiguous: "
                              f"{design[2]} vs {design[1]} on '{design[0]}'")
                        dlog.record("llm_contrast_validation", "skipped_python_confident",
                                    design_column=design[0], control=design[1], treatment=design[2])
                        row["llm_validated"] = "skipped(confident)"
                    else:
                        md_summary = summarize_metadata_for_llm(metadata_for_design)
                        llm_result = validate_contrast_with_llm(
                            accession=acc,
                            metadata_columns_summary=md_summary,
                            treatment_keywords=treatment_keywords,
                            control_keywords=control_keywords,
                            proposed=design,
                        )
                    final_design = design
                    if llm_result is not None:
                        row["llm_validated"] = bool(llm_result.is_valid)
                        row["llm_reasoning"] = llm_result.reasoning
                        print(f"  [llm-validation] is_valid={llm_result.is_valid} | {llm_result.reasoning}")
                        # Trust the LLM's structured triple whenever it is fully populated — this is
                        # the contrast it actually identified, regardless of the is_valid label. (A
                        # confirm with no Python pick used to discard a perfectly good LLM proposal.)
                        llm_triple = None
                        if (llm_result.design_column and llm_result.control_value
                                and llm_result.treatment_value):
                            llm_triple = (llm_result.design_column,
                                          llm_result.control_value,
                                          llm_result.treatment_value)
                        if llm_result.is_valid and design is not None:
                            # Confirm the Python pick.
                            final_design = design
                            dlog.record("llm_contrast_validation", "confirm", reason=llm_result.reasoning)
                        elif llm_triple is not None:
                            # LLM proposed a contrast where Python found none, or overrode a wrong pick.
                            final_design = llm_triple
                            verb = "proposed" if design is None else "override"
                            print(f"  [llm-validation] {verb} -> "
                                  f"{llm_triple[0]} | {llm_triple[1]} vs {llm_triple[2]}")
                            dlog.record("llm_contrast_validation", verb, reason=llm_result.reasoning,
                                        design_column=llm_triple[0], control=llm_triple[1], treatment=llm_triple[2])
                        else:
                            # No usable contrast (LLM refused, or claimed valid but gave nothing usable).
                            final_design = None
                            print("  [llm-validation] no clean contrast; skipping DEG")
                            dlog.record("llm_contrast_validation", "refuse", reason=llm_result.reasoning)
                        row["llm_overrode"] = (final_design != design)
                    elif not skipped_confident:
                        print("  [llm-validation] unavailable; using python result")
                        dlog.record("llm_contrast_validation", "unavailable")

                    # req #8: build the FULL contrast set to run. Multi-contrast only when the
                    # keyword detector drove it AND the LLM didn't override to a different pick:
                    #   - LLM confirmed / unavailable (final_design == the python first pick) -> run
                    #     ALL sibling levels on that column (e.g. 1wk/2wk/4wk training vs control).
                    #   - LLM overrode or proposed a single triple -> run just that one contrast.
                    if final_design is None:
                        final_contrasts = []
                    elif final_design == design and contrasts:
                        final_contrasts = contrasts
                    else:
                        final_contrasts = [final_design]

                    if not final_contrasts:
                        row["status"] = "preprocess_ok_no_design"
                        status_tracker.add_warning(f"{acc}: no clean contrast")
                        dlog.record("differential_expression", "skipped",
                                    reason="no clean 2-group contrast")
                    else:
                        multi = len(da_methods) > 1
                        row["design_col"] = final_contrasts[0][0]
                        row["control"] = final_contrasts[0][1]
                        row["treatment"] = final_contrasts[0][2]
                        row["n_contrasts"] = len(final_contrasts)
                        row["contrasts"] = "; ".join(f"{t} vs {c}" for _, c, t in final_contrasts)
                        print(f"final design: {final_contrasts[0][0]} | "
                              f"{len(final_contrasts)} contrast(s) | "
                              f"method={'+'.join(da_methods) if multi else da_methods[0]}")
                        cres = []
                        eval_results = []
                        status_tracker.set_stage("analyze_enrich",
                                                 message=f"running {len(final_contrasts)} contrast(s)")
                        for (col, ctrl, treat) in final_contrasts:
                            print(f"  --- contrast: {col} | {ctrl} vs {treat} ---")
                            if multi:
                                r = _run_contrast_multi(
                                    da_methods, counts_path, da_input_path, metadata_for_design,
                                    col, ctrl, treat, study_out, organism, matrix_type,
                                    dlog, fail_log, acc)
                            else:
                                r = _run_contrast_da(
                                    da_methods[0], counts_path, da_input_path, metadata_for_design,
                                    col, ctrl, treat, study_out, organism, matrix_type,
                                    dlog, fail_log, acc)
                            cres.append(r)
                            if evaluate_subsets and r.get("n_deg") is not None:
                                status_tracker.set_stage("evaluate", message="evaluating subset stability")
                                eval_method = da_methods[0]
                                print(f"  [eval] subset stability enabled: {evaluation_runs} runs, "
                                      f"fraction={evaluation_subset_fraction}, method={eval_method}, "
                                      f"include_gsea={evaluation_include_gsea}")
                                eval_results.append(_run_subset_evaluation(
                                    eval_method, counts_path, da_input_path, metadata_for_design,
                                    col, ctrl, treat, study_out, organism, matrix_type,
                                    dlog, fail_log, acc,
                                    n_runs=evaluation_runs,
                                    subset_fraction=evaluation_subset_fraction,
                                    include_gsea=evaluation_include_gsea,
                                    use_llm_judge=evaluation_use_llm_judge,
                                ))
                        # Aggregate the per-contrast results into the one-row-per-study summary.
                        # design_col/control/treatment hold the first contrast (back-compat); n_deg
                        # is the total across contrasts, with the per-contrast breakdown alongside.
                        # In 'all' mode each r["n_deg"] is already the consensus (>=2 methods) count.
                        deg_ok = [r for r in cres if r["n_deg"] is not None]
                        if deg_ok:
                            row["n_deg"] = int(sum(r["n_deg"] for r in deg_ok))
                            if multi:
                                row["n_deg_detail"] = "; ".join(
                                    f"{r['treatment']} vs {r['control']}: consensus>=2={r['n_deg']} "
                                    "[" + ",".join(f"{m}={r['per_method'][m]}" for m in r["per_method"]) + "]"
                                    for r in deg_ok)
                            else:
                                row["n_deg_detail"] = "; ".join(
                                    f"{r['treatment']} vs {r['control']}: {r['n_deg']}" for r in deg_ok)
                        sig = [r["n_gsea_sig"] for r in cres if r["n_gsea_sig"] is not None]
                        if sig:
                            row["n_gsea_sig"] = int(sum(sig))
                        ok_evals = [e.get("summary") for e in eval_results
                                    if isinstance(e, dict) and e.get("status") == "ok" and e.get("summary")]
                        if ok_evals:
                            row["eval_verdict"] = "; ".join(
                                e.get("judge", {}).get("verdict", "unknown") for e in ok_evals)
                            deg_r = [e.get("deg", {}).get("mean_log2fc_pearson") for e in ok_evals
                                     if e.get("deg")]
                            deg_j = [e.get("deg", {}).get("mean_sig_deg_jaccard") for e in ok_evals
                                     if e.get("deg")]
                            gsea_r = [e.get("gsea", {}).get("mean_nes_pearson") for e in ok_evals
                                      if e.get("gsea")]
                            gsea_j = [e.get("gsea", {}).get("mean_sig_pathway_jaccard") for e in ok_evals
                                      if e.get("gsea")]
                            row["eval_deg_log2fc_r"] = round(float(np.mean(deg_r)), 4) if deg_r else None
                            row["eval_sig_deg_jaccard"] = round(float(np.mean(deg_j)), 4) if deg_j else None
                            row["eval_gsea_nes_r"] = round(float(np.mean(gsea_r)), 4) if gsea_r else None
                            row["eval_sig_pathway_jaccard"] = round(float(np.mean(gsea_j)), 4) if gsea_j else None
                            row["eval_summary_json"] = "; ".join(
                                e.get("artifacts", {}).get("summary_json", "") for e in ok_evals
                                if e.get("artifacts", {}).get("summary_json"))
                        # DEG-sanity rollup: surface any implausible-result flag so a statistically
                        # untrustworthy run (e.g. n=2/group -> 66% DEG) is visible in summary.csv.
                        flagged = [f"{r['treatment']} vs {r['control']}: {r['deg_sanity']}"
                                   for r in cres if r.get("deg_sanity") and r["deg_sanity"] != "ok"]
                        row["deg_sanity"] = "; ".join(flagged) if flagged else "ok"
                        statuses = [r["status"] for r in cres]
                        if any(s == "deg_gsea_ok" for s in statuses):
                            row["status"] = ("deg_gsea_ok" if all(s == "deg_gsea_ok" for s in statuses)
                                             else "deg_gsea_ok_partial")
                        elif any(s == "deg_ok_gsea_failed" for s in statuses):
                            row["status"] = "deg_ok_gsea_failed"
                        else:
                            row["status"] = "deg_failed"
                        # 'all' mode: roll up the multi-method comparison across contrasts.
                        if multi:
                            methods_seen, per_tot, rvals = [], {}, []
                            for r in cres:
                                for m, nd in (r.get("per_method") or {}).items():
                                    if m not in methods_seen:
                                        methods_seen.append(m)
                                    per_tot[m] = per_tot.get(m, 0) + (nd or 0)
                                rvals.extend(r.get("pairwise_r", {}).values())
                            row["da_methods_run"] = ",".join(methods_seen)
                            row["da_per_method_deg"] = "; ".join(f"{m}:{per_tot[m]}" for m in methods_seen)
                            row["da_consensus_deg"] = row["n_deg"]
                            if rvals:
                                row["da_logfc_r"] = round(sum(rvals) / len(rvals), 3)
            except Exception as e:
                row["status"] = "exception"
                row["error"] = f"{type(e).__name__}: {e}"
                status_tracker.add_failure(f"{acc}: {row['error']}")
                dlog.record("exception", type(e).__name__, reason=str(e))
                with open(fail_log, "a", encoding="utf-8") as f:
                    f.write(f"{acc} | {row['error']}\n")
                print(f"[ERROR] {acc}: {row['error']}")
            status_tracker.set_stage(
                "report", message=f"saving {acc} results",
                evidence_ids=[f"{acc}:{d.decision_id}" for d in dlog.evidence.bundle.decisions],
            )
            dlog.save(decisions_path, status=row["status"], error=row["error"])
            summary_rows.append(row)

        summary_df = pd.DataFrame(summary_rows)
        summary_path = os.path.join(run_dir, "summary.csv")
        summary_df.to_csv(summary_path, index=False)

        status_counts = summary_df["status"].value_counts().to_dict()
        lines = [f"Batch pipeline complete on {len(summary_rows)} studies. Output: {run_dir}", ""]
        lines.append("Status counts:")
        for s, c in status_counts.items():
            lines.append(f"  {s}: {c}")
        lines.append("")
        lines.append("Per-study:")
        for _, srow in summary_df.iterrows():
            bits = [srow["status"]]
            if pd.notna(srow["n_deg"]):
                bits.append(f"DEG(padj<.05)={int(srow['n_deg'])}")
            if pd.notna(srow["n_gsea_sig"]):
                bits.append(f"GSEA_sig={int(srow['n_gsea_sig'])}")
            if pd.notna(srow["sex_mismatch"]) and srow["sex_mismatch"]:
                bits.append(f"sex_mismatch={int(srow['sex_mismatch'])}")
            lines.append(f"  {srow['accession']}: {' | '.join(bits)}")
        lines.append("")
        lines.append(f"Summary CSV: {summary_path}")
        lines.append(f"Workflow log: {log_path}")
        lines.append(f"Run status: {status_path}")
        lines.append(f"Per-study decision logs: {run_dir}/<accession>/decisions.json")
        if os.path.exists(fail_log):
            lines.append(f"Failure log: {fail_log}")
        result = "\n".join(lines)
        partial_statuses = {"exception", "deg_failed", "deg_ok_gsea_failed"}
        is_partial = any(str(x).startswith("skipped_") or x in partial_statuses
                         for x in summary_df["status"].tolist())
        usage = llm_usage_summary(llm_usage_start)
        status_tracker.set_usage(
            llm_calls=usage["llm_calls"],
            estimated_cost_usd=usage["estimated_cost_usd"],
        )
        print(
            f"LLM usage: calls={usage['llm_calls']} input={usage['input_tokens']} "
            f"output={usage['output_tokens']} cost_usd={usage['estimated_cost_usd']:.6f}"
        )
        status_tracker.finish("partial" if is_partial else "completed",
                              "batch completed with issues" if is_partial else "batch completed")
        print()
        print(result)
        return result
    finally:
        if status_tracker.state.status in ("pending", "running", "waiting_approval"):
            status_tracker.add_failure("batch terminated before final report")
            status_tracker.finish("failed", "batch terminated before final report")
        sys.stdout, sys.stderr = old_stdout, old_stderr
        log_file.close()
