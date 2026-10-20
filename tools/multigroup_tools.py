"""Validated execution for explicit multi-level and paired-change designs.

The ordinary batch path is intentionally conservative and accepts one
control-vs-treatment contrast at a time.  This module is the explicit-plan
path: the caller supplies a patsy formula and named coefficient vectors, while
this module validates exact sample alignment, design rank, residual degrees of
freedom, and contrast names before fitting limma on a log-scale matrix.
"""

from __future__ import annotations

import json
import os
from typing import Any

import numpy as np
import pandas as pd

from tools.analysis_policy import enforce_method_matrix_compatibility, numeric_matrix, PolicyViolation
from tools.de_common import limma_standard_error


def collapse_duplicate_genes(df: pd.DataFrame, label: str = "counts") -> pd.DataFrame:
    # Imported lazily: deseq2_tools pulls in pydeseq2 at module import.
    from tools.de_common import collapse_duplicate_genes as _collapse
    return _collapse(df, label)


def _prepare_metadata(meta: pd.DataFrame, plan: dict[str, Any]) -> pd.DataFrame:
    """Apply explicit, auditable metadata derivations requested by a plan.

    GEO series often encode paired time points in sample names (for example
    ``B_1M``/``IPE_1M``) rather than separate metadata fields.  A plan may
    request ``__sample_index__`` for subject/time and may declare regex-based
    derived columns.  These are deterministic transformations; no biological
    labels are guessed here.
    """
    out = meta.copy()
    derived = plan.get("derived_columns") or {}
    for name, spec in derived.items():
        if not isinstance(spec, dict):
            raise PolicyViolation(f"derived column {name!r} must be an object")
        source = str(spec.get("source_column", ""))
        if source not in out.columns:
            raise PolicyViolation(f"derived column {name!r} source is missing: {source!r}")
        pattern = spec.get("regex")
        if not pattern:
            raise PolicyViolation(f"derived column {name!r} requires regex")
        out[name] = out[source].astype(str).str.extract(str(pattern), expand=False)
        if out[name].isna().any():
            raise PolicyViolation(f"derived column {name!r} regex did not match all samples")
    if "__sample_index__" in (plan.get("subject_column"), plan.get("time_column")):
        idx = out.index.astype(str)
        # q1/q2-style paired labels: q1_<subject> and q2_<subject>.
        if idx.str.match(r"^q[12]_", case=False).all():
            if plan.get("subject_column") == "__sample_index__":
                out["__subject__"] = idx.str.replace(r"^q[12]_", "", regex=True)
            if plan.get("time_column") == "__sample_index__":
                out["__time__"] = idx.str.extract(r"^(q[12])_", expand=False).str.lower().map({"q1": "baseline", "q2": "followup"})
        else:
            # Common GEO longitudinal names: <subject>_<time> or <time>_<subject>.
            sep = idx.str.rsplit("_", n=1)
            if plan.get("subject_column") == "__sample_index__":
                out["__subject__"] = sep.str[0]
            if plan.get("time_column") == "__sample_index__":
                out["__time__"] = sep.str[1]
    return out


def _read_matrix(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0, sep=None, engine="python")
    df = numeric_matrix(df, label="explicit multi-group expression matrix")
    if df.index.has_duplicates:
        df = collapse_duplicate_genes(df, "explicit multi-group")
    df = df.loc[df.notna().sum(axis=1) >= max(3, int(df.shape[1] * 0.5))]
    df = df.loc[df.var(axis=1, skipna=True) > 0]
    if df.empty or df.shape[1] < 4:
        raise PolicyViolation(f"expression matrix has insufficient usable data: {df.shape}")
    return df


def _validate_design(meta: pd.DataFrame, formula: str):
    from patsy import dmatrix

    if not formula or not isinstance(formula, str):
        raise PolicyViolation("an explicit patsy formula is required for a multi-group plan")
    try:
        design = dmatrix(formula, meta)
    except Exception as exc:
        raise PolicyViolation(f"could not construct design matrix {formula!r}: {exc}") from exc
    matrix = np.asarray(design, dtype=float)
    rank = int(np.linalg.matrix_rank(matrix))
    if rank < matrix.shape[1]:
        raise PolicyViolation(f"design matrix is rank deficient ({rank}/{matrix.shape[1]})")
    residual_df = int(matrix.shape[0] - rank)
    if residual_df < 1:
        raise PolicyViolation(f"no residual degrees of freedom remain (df={residual_df})")
    return design, rank, residual_df


def _fit_contrasts(expr: pd.DataFrame, meta: pd.DataFrame, formula: str,
                   contrasts: list[dict[str, Any]], output_dir: str):
    from inmoose.limma import contrasts_fit, lmFit, topTable
    from tools.limma_compat import ebayes as eBayes

    design, rank, residual_df = _validate_design(meta, formula)
    names = list(design.design_info.column_names)
    # Fit once, then apply each contrast and empirical-Bayes moderation.  The
    # unmoderated fit is required here; moderating before contrasts_fit would
    # make the contrast standard errors inconsistent with limma's contract.
    fit = lmFit(expr.loc[:, meta.index], design=design)
    results = []
    for item in contrasts:
        if not isinstance(item, dict) or not item.get("name"):
            raise PolicyViolation("each contrast must have a non-empty name")
        name = str(item["name"])
        vector = item.get("coefficients")
        if not isinstance(vector, dict) or not vector:
            raise PolicyViolation(f"contrast {name!r} must provide a coefficient mapping")
        missing = [str(k) for k in vector if str(k) not in names]
        if missing:
            raise PolicyViolation(f"contrast {name!r} references missing coefficients {missing}; available={names}")
        cmat = pd.DataFrame({name: [float(vector.get(n, 0.0)) for n in names]}, index=names)
        cfit = eBayes(contrasts_fit(fit, contrasts=cmat))
        top = limma_standard_error(pd.DataFrame(topTable(cfit, coef=name, number=expr.shape[0], sort_by="P", adjust_method="fdr_bh")))
        top = top.rename(columns={"adj_pvalue": "padj"})
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name).strip("_") or "contrast"
        out = os.path.join(output_dir, f"DEG_results_{safe}.csv")
        top.to_csv(out)
        results.append({
            "name": name,
            "path": out,
            "n_deg": int((top["padj"] < 0.05).sum()),
            "formula": formula,
            "design_rank": rank,
            "residual_df": residual_df,
        })
    return results


def _paired_change(expr: pd.DataFrame, meta: pd.DataFrame, plan: dict[str, Any]):
    subject_col = "__subject__" if plan.get("subject_column") == "__sample_index__" else str(plan.get("subject_column", ""))
    time_col = "__time__" if plan.get("time_column") == "__sample_index__" else str(plan.get("time_column", ""))
    baseline = str(plan.get("baseline_level", ""))
    followups = [str(x) for x in (plan.get("followup_levels") or [])]
    group_col = str(plan.get("group_column", ""))
    required = [subject_col, time_col, group_col]
    missing = [c for c in required if c not in meta.columns]
    if missing or not baseline or not followups:
        raise PolicyViolation(f"paired_change plan missing columns/levels: {missing}")
    outputs = []
    for followup in followups:
        pairs, excluded = complete_subject_pairs(meta, subject_col, time_col, baseline, followup, group_col)
        if len(pairs) < 4:
            raise PolicyViolation(f"follow-up {followup!r} has too few complete subject pairs: {len(pairs)}")
        delta = pd.DataFrame({p["subject"]: expr[p["followup"]] - expr[p["baseline"]] for p in pairs})
        delta_meta = pd.DataFrame(pairs).set_index("subject")
        formula = str(plan.get("formula") or f"~ C({group_col})")
        out_dir = str(plan["_output_dir"])
        contrasts = plan.get("contrasts") or []
        follow_dir = os.path.join(out_dir, f"followup_{followup}")
        os.makedirs(follow_dir, exist_ok=True)
        exclusion_path = os.path.join(follow_dir, "paired_change_pairs.json")
        with open(exclusion_path, "w", encoding="utf-8") as fh:
            json.dump({"baseline": baseline, "followup": followup, "n_complete_pairs": len(pairs),
                       "pairs": pairs, "excluded_subjects": excluded}, fh, indent=2, default=str)
        results = _fit_contrasts(delta, delta_meta.rename(columns={"group": group_col}), formula, contrasts, follow_dir)
        for result in results:
            result["followup_level"] = followup
            result["n_complete_pairs"] = len(pairs)
            result["excluded_subjects"] = excluded
            result["pairs_file"] = exclusion_path
        outputs.extend(results)
    return outputs


def complete_subject_pairs(meta: pd.DataFrame, subject_col: str, time_col: str, baseline: str,
                           followup: str, group_col: str) -> tuple[list[dict], list[dict]]:
    """Return complete baseline/follow-up pairs and every subject left out, with a reason.

    A subject is paired only when it has exactly one baseline and exactly one
    follow-up sample. Missing or duplicated samples are reported, never guessed.
    """
    pairs, excluded = [], []
    for subject, rows in meta.groupby(subject_col, dropna=False):
        b = rows[rows[time_col].astype(str) == baseline]
        f = rows[rows[time_col].astype(str) == followup]
        if len(b) == 1 and len(f) == 1:
            pairs.append({"subject": str(subject), "baseline": b.index[0], "followup": f.index[0],
                          "group": str(f.iloc[0][group_col])})
            continue
        if len(b) == 0 or len(f) == 0:
            reason = "missing_" + ("baseline" if len(b) == 0 else "followup")
        else:
            reason = "duplicate_samples"
        excluded.append({"subject": str(subject), "reason": reason,
                         "n_baseline": int(len(b)), "n_followup": int(len(f)),
                         "samples": [str(x) for x in rows.index]})
    return pairs, excluded


def run_multigroup_analysis(expression_csv: str, metadata_csv: str,
                            plan: dict[str, Any], output_dir: str) -> dict[str, Any]:
    """Run a validated explicit multi-level/factorial/paired-change plan."""
    if not isinstance(plan, dict):
        raise PolicyViolation("multi-group plan must be an object")
    os.makedirs(output_dir, exist_ok=True)
    expr = _read_matrix(expression_csv)
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta_ids = set(str(x) for x in meta.index)
    common = [c for c in expr.columns if str(c) in meta_ids]
    # Some GEO processed matrices carry numeric annotation columns (length,
    # exon count, etc.) alongside samples.  They are not samples and should be
    # dropped once every metadata sample is covered.  Refuse the opposite case
    # (uncovered metadata rows) rather than silently fitting a partial design.
    if len(common) < len(meta) or len(common) < 4:
        raise PolicyViolation(f"exact metadata alignment incomplete: {len(common)}/{len(meta)} metadata samples")
    meta.index = meta.index.astype(str)
    expr.columns = expr.columns.astype(str)
    expr = expr.loc[:, common]
    # This executor fits limma, so the sample columns must already be on a log
    # scale: raw counts need log-CPM (or voom), FPKM/TPM need log2(x+1) first.
    # Checked after numeric annotation columns (length, exon count) are dropped.
    enforce_method_matrix_compatibility(expr, method="limma")
    meta = meta.loc[common]
    meta = _prepare_metadata(meta, plan)
    if plan.get("analysis_type") == "paired_change":
        local = dict(plan)
        local["_output_dir"] = output_dir
        results = _paired_change(expr, meta, local)
        first = results[0] if results else {}
        return {"analysis_type": "paired_change", "n_samples": int(len(meta)),
                "design_rank": first.get("design_rank"),
                "residual_df": first.get("residual_df"),
                "n_contrasts": len(results), "results": results,
                "matrix": expression_csv, "metadata": metadata_csv}

    formula = str(plan.get("formula", ""))
    contrasts = plan.get("contrasts") or []
    results = _fit_contrasts(expr, meta, formula, contrasts, output_dir)
    design, rank, residual_df = _validate_design(meta, formula)
    return {"analysis_type": str(plan.get("analysis_type", "multigroup")),
            "formula": formula, "n_samples": int(len(meta)),
            "design_rank": rank, "residual_df": residual_df,
            "n_contrasts": len(results), "results": results,
            "matrix": expression_csv, "metadata": metadata_csv}
