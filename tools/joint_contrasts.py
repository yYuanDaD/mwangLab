"""Fit one model on all samples, then extract every comparison from it.

The two-group executors subset to the two compared arms, so each comparison gets its
own dispersion (DESeq2) or variance (limma) estimate from a few samples. In the large
run this cost power on every multi-group paper (GSE308674: 10 of 28 samples per fit,
328 vs the paper's 474 DEGs; GSE164798: 8 of 24, Chgb padj ~1 vs 0.02). Here the model
is a cell-means design (one cell per combination of the design factors, plus optional
covariates or a blocking term) fitted once; each comparison from
``suitability.enumerate_comparisons`` is a contrast vector on it:

    simple       cell(test) - cell(reference)
    interaction  (a:b - ref:b) - (a:ref - ref:ref)

``run_joint_deseq2`` is for raw (or rounded estimated) counts; ``run_joint_limma``
for log-scale matrices, through ``multigroup_tools.run_multigroup_analysis``.
"""

from __future__ import annotations

import os
import re
from typing import Any, Sequence

import numpy as np
import pandas as pd

from tools.analysis_policy import PolicyViolation, enforce_method_matrix_compatibility, numeric_matrix

_SIGNS = {"simple": (1, -1), "interaction": (1, -1, -1, 1)}


def _cell_factors(comparisons: Sequence[dict]) -> list[str]:
    cols: list[str] = []
    for c in comparisons:
        for cell in c["cells"]:
            cols += [k for k in cell["cell"] if k not in cols]
    return cols


def add_cell_column(meta: pd.DataFrame, comparisons: Sequence[dict], column: str = "cell"):
    """Add a formula-safe cell code (c00, c01, ...) per combination of the design factors.

    Returns (metadata restricted to samples with every factor known, {code: {factor: level}})."""
    factors = _cell_factors(comparisons)
    missing = [f for f in factors if f not in meta.columns]
    if missing:
        raise PolicyViolation(f"comparison factors not in metadata: {missing}")
    meta = meta.copy()
    keys = meta[factors].astype(str).agg("\x1f".join, axis=1)
    known = meta[factors].notna().all(axis=1)
    meta = meta[known]
    keys = keys[known]
    labels = sorted(keys.unique())
    codes = {k: f"c{i:02d}" for i, k in enumerate(labels)}
    meta[column] = keys.map(codes)
    cells = {codes[k]: dict(zip(factors, k.split("\x1f"))) for k in labels}
    return meta, cells


def _code(cells: dict, cell: dict) -> str:
    for code, levels in cells.items():
        if all(str(levels.get(k)) == str(v) for k, v in cell.items()) and len(levels) == len(cell):
            return code
    raise PolicyViolation(f"no samples in cell {cell}")


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "contrast"


def _numeric_covariates(meta: pd.DataFrame, covariates: Sequence[str]) -> list[str]:
    """Covariates whose values are all numbers (RIN, age): fitted as continuous, not as factors."""
    return [c for c in covariates if pd.to_numeric(meta[c], errors="coerce").notna().all()]


def run_joint_deseq2(counts_csv: str, metadata_csv: str, comparisons: Sequence[dict], output_dir: str, *,
                     covariates: Sequence[str] = (), alpha: float = 0.05, n_cpus: int = 8,
                     round_estimated_counts: bool = False, include: Sequence[str] = ()) -> dict[str, Any]:
    """DESeq2 on every sample with ``~ covariates + cell``; one result file per comparison.

    Only comparisons marked ``analyzable`` are extracted; the others are listed as
    skipped unless named in ``include`` (a planned small-n contrast, labelled exploratory).
    Columns match ``run_deseq2_analysis`` (baseMean, log2FoldChange, lfcSE,
    stat, pvalue, padj). Numeric covariates are continuous. Estimated counts (salmon,
    RSEM) need ``round_estimated_counts=True``; record the rounding in the method gate."""
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.ds import DeseqStats

    os.makedirs(output_dir, exist_ok=True)
    counts = numeric_matrix(pd.read_csv(counts_csv, index_col=0, sep=None, engine="python"),
                            label="joint DESeq2 counts")
    if counts.index.has_duplicates:
        from tools.de_common import collapse_duplicate_genes
        counts = collapse_duplicate_genes(counts, "joint DESeq2")
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta.index = meta.index.astype(str)
    counts.columns = counts.columns.astype(str)
    meta, cells = add_cell_column(meta, comparisons)
    common = [s for s in meta.index if s in set(counts.columns)]
    if len(common) < len(meta):
        raise PolicyViolation(f"exact alignment incomplete: {len(common)}/{len(meta)} metadata samples in the matrix")
    counts = counts.loc[:, common]
    if round_estimated_counts:
        counts = counts.round()
    enforce_method_matrix_compatibility(counts, method="deseq2")
    counts = counts.round().astype(int).T
    counts = counts.loc[:, (counts != 0).any(axis=0)]
    meta = meta.loc[common]
    safe_cov = {c: f"cov{i}" for i, c in enumerate(covariates)}
    continuous = [safe_cov[c] for c in _numeric_covariates(meta, covariates)]
    design = meta.rename(columns=safe_cov)[list(safe_cov.values()) + ["cell"]]
    for col in design.columns:
        design[col] = pd.to_numeric(design[col]) if col in continuous else design[col].astype(str)
    dds = DeseqDataSet(counts=counts, metadata=design, design_factors=list(safe_cov.values()) + ["cell"],
                       continuous_factors=continuous or None, refit_cooks=True, n_cpus=n_cpus, quiet=True)
    dds.deseq2()
    columns = list(dds.obsm["design_matrix"].columns)

    def vec(code: str) -> np.ndarray:
        v = np.zeros(len(columns))
        hit = [i for i, c in enumerate(columns) if c.startswith("cell") and c.endswith(f"[T.{code}]")]
        if hit:
            v[hit[0]] = 1.0
        return v

    results, skipped = [], []
    for comp in comparisons:
        if not comp.get("analyzable", True) and comp["name"] not in include:
            skipped.append({"name": comp["name"], "reason": "a cell has fewer than 3 samples"})
            continue
        codes = [_code(cells, c["cell"]) for c in comp["cells"]]
        contrast = sum(s * vec(k) for s, k in zip(_SIGNS[comp["kind"]], codes))
        stat = DeseqStats(dds, contrast=contrast, alpha=alpha, quiet=True, n_cpus=n_cpus)
        stat.summary()
        res = stat.results_df.sort_values("padj")
        path = os.path.join(output_dir, f"DEG_results_{_safe(comp['name'])}.csv")
        res.to_csv(path)
        results.append({"name": comp["name"], "kind": comp["kind"], "path": path,
                        "n_padj_0.05": int((res["padj"] < 0.05).sum()), "cells": codes})
    return {"method": "DESeq2 joint model", "formula": "~ " + " + ".join(list(covariates) + ["cell"]),
            "n_samples": int(len(meta)), "n_genes": int(counts.shape[1]),
            "cells": cells, "results": results, "skipped": skipped}


def run_joint_limma(expression_csv: str, metadata_csv: str, comparisons: Sequence[dict], output_dir: str, *,
                    covariates: Sequence[str] = (), include: Sequence[str] = ()) -> dict[str, Any]:
    """limma on a log-scale matrix with ``~ 0 + C(cell) + covariates``, via run_multigroup_analysis."""
    from tools.multigroup_tools import run_multigroup_analysis

    os.makedirs(output_dir, exist_ok=True)
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta.index = meta.index.astype(str)
    meta, cells = add_cell_column(meta, comparisons)
    safe_cov = {c: f"cov{i}" for i, c in enumerate(covariates)}
    continuous = {safe_cov[c] for c in _numeric_covariates(meta, covariates)}
    meta = meta.rename(columns=safe_cov)
    for c in safe_cov.values():
        meta[c] = pd.to_numeric(meta[c]) if c in continuous else meta[c].astype(str)
    meta_path = os.path.join(output_dir, "joint_metadata.csv")
    meta[["cell"] + list(safe_cov.values())].to_csv(meta_path)
    contrasts, skipped = [], []
    for comp in comparisons:
        if not comp.get("analyzable", True) and comp["name"] not in include:
            skipped.append({"name": comp["name"], "reason": "a cell has fewer than 3 samples"})
            continue
        coef: dict[str, float] = {}
        for s, c in zip(_SIGNS[comp["kind"]], comp["cells"]):
            key = f"C(cell)[{_code(cells, c['cell'])}]"
            coef[key] = coef.get(key, 0.0) + s
        contrasts.append({"name": _safe(comp["name"]), "coefficients": coef})
    formula = "~ 0 + C(cell)" + "".join(f" + {c}" if c in continuous else f" + C({c})" for c in safe_cov.values())
    out = run_multigroup_analysis(expression_csv, meta_path,
                                  {"analysis_type": "multilevel", "formula": formula, "contrasts": contrasts},
                                  output_dir)
    out.update({"method": "limma joint model", "cells": cells, "skipped": skipped,
                "covariates": dict(safe_cov)})
    return out
