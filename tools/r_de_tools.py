"""Differential expression with the R packages that papers name (tools/r_de.R via Rscript).

The pydeseq2 / inmoose executors cover the common routes. Papers in the large run also
used methods those ports do not have; each was a declared deviation:

    surrogate variables          sva::svaseq / sva::sva            any engine, ``n_sv``
    DESeq2 LRT                   DESeq(test = "LRT", reduced)      engine "deseq2", ``reduced``
    LFC shrinkage                lfcShrink apeglm / ashr / normal  engine "deseq2", ``shrink``
    IHW adjustment               IHW::ihw(pvalue ~ baseMean)       engine "deseq2", ``p_adjust="IHW"``
    edgeR QL with TMM            glmQLFit / glmQLFTest             engine "edger_ql"
    voom + TMM, any design       voom (+ duplicateCorrelation)     engine "voom", ``block``
    mixed-effects ANOVA          lmerTest + emmeans Tukey          run_r_mixed_anova
    the original DESeq (v1)      newCountDataSet / nbinomTest      engine "deseq1"

Both functions follow the case_runner execution contract (a matrix path, ``metadata_csv``,
``output_dir``) and return {"results": [{"name", "path"}], "formula", ...}; result tables
have the DESeq2 columns (baseMean, log2FoldChange, lfcSE, stat, pvalue, padj), so
``native.apply_threshold`` and the enrichment tools read them unchanged. With ``shrink``
the shrunken estimate is ``log2FoldChange`` and the MLE is kept as ``log2FoldChange_mle``.

Samples must already be aligned: every metadata row must name a matrix column. Contrasts:
    {"name", "factor", "test", "ref"}   DESeq2 / DESeq-style level comparison
    {"name", "coef"}                    one model column (DESeq2 resultsNames, or the
                                        make.names()'d model.matrix column for edgeR/limma)
    {"name", "expr"}                    limma makeContrasts expression over model columns
    {"name", "emmeans_label", "by"}     mixed_anova: a row of pairs(emmeans(...), reverse=TRUE),
                                        e.g. label "H0 - BL", by "HC"
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Optional, Sequence

import pandas as pd

from tools.analysis_policy import PolicyViolation, numeric_matrix
from tools.limma_voom_tools import _find_rscript

_R_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r_de.R")
COUNT_ENGINES = ("deseq2", "edger_ql", "voom", "deseq1")
LOG_ENGINES = ("limma_trend", "mixed_anova")
_INTEGER_ENGINES = ("deseq2", "deseq1")


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "contrast"


def _design_columns(formula: Optional[str], meta: pd.DataFrame) -> list[str]:
    if not formula:
        return []
    tokens = set(re.findall(r"[A-Za-z_.][A-Za-z0-9_.]*", formula))
    return [c for c in meta.columns if c in tokens]


def _run(matrix_csv: str, metadata_csv: str, output_dir: str, config: dict, *,
         subset: Optional[dict] = None, extra_columns: Sequence[str] = (),
         round_estimated_counts: bool = False, timeout: int = 7200) -> dict[str, Any]:
    rscript = _find_rscript()
    if not rscript:
        raise PolicyViolation("Rscript not found; set BIOAGENT_RSCRIPT or install R")
    os.makedirs(output_dir, exist_ok=True)
    engine = config["engine"]
    matrix = numeric_matrix(pd.read_csv(matrix_csv, index_col=0, sep=None, engine="python"),
                            label=f"{engine} matrix")
    if matrix.index.has_duplicates:
        from tools.de_common import collapse_duplicate_genes
        matrix = collapse_duplicate_genes(matrix, engine)
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta.index = meta.index.astype(str)
    matrix.columns = matrix.columns.astype(str)
    for col, keep in (subset or {}).items():
        meta = meta[meta[col].astype(str).isin([str(v) for v in keep])]
    missing = [s for s in meta.index if s not in set(matrix.columns)]
    if missing:
        raise PolicyViolation(f"{len(missing)} metadata samples are not matrix columns (align first): {missing[:5]}")
    columns = []
    for formula in (config.get("design"), config.get("reduced"), config.get("sv_null")):
        columns += [c for c in _design_columns(formula, meta) if c not in columns]
    for c in [config.get("block"), config.get("random"), config.get("condition"), *extra_columns]:
        if c and c not in columns:
            columns.append(c)
    unknown = [c for c in columns if c not in meta.columns]
    if unknown:
        raise PolicyViolation(f"design columns not in metadata: {unknown}")
    incomplete = meta[columns].isna().any(axis=1)
    if incomplete.any():
        raise PolicyViolation(f"{int(incomplete.sum())} samples lack a design value in {columns}; subset them out first")
    matrix = matrix.loc[:, list(meta.index)]
    if engine in COUNT_ENGINES:
        if (matrix < 0).any().any():
            raise PolicyViolation(f"{engine} needs counts; the matrix has negative values (log scale?)")
        fractional = (matrix.round() != matrix).any().any()
        if engine in _INTEGER_ENGINES and fractional and not round_estimated_counts:
            raise PolicyViolation(f"{engine} needs integer counts; pass round_estimated_counts=True for "
                                  "salmon/RSEM estimated counts and record the rounding")
        matrix = matrix.loc[(matrix != 0).any(axis=1)]
    tmp = tempfile.mkdtemp(prefix=f"rde_{engine}_")
    try:
        matrix.to_csv(os.path.join(tmp, "matrix.csv"))
        meta[columns].to_csv(os.path.join(tmp, "metadata.csv"))
        with open(os.path.join(tmp, "config.json"), "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=2)
        proc = subprocess.run([rscript, _R_SCRIPT, os.path.join(tmp, "config.json")], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
        report_path = os.path.join(tmp, "report.json")
        if proc.returncode != 0 or not os.path.isfile(report_path):
            err = (proc.stderr or proc.stdout or "").strip()
            tail = err[err.rfind("Error"):][:1500] if "Error" in err else err[-1500:]
            raise PolicyViolation(f"{engine} (R) failed (exit {proc.returncode}): {tail}")
        with open(report_path, encoding="utf-8") as fh:
            report = json.load(fh)
        results = []
        for out in report.get("outputs", []):
            path = os.path.join(output_dir, f"DEG_results_{_safe(out['name'])}.csv")
            shutil.move(out["path"], path)
            table = pd.read_csv(path, index_col=0)
            results.append({"name": out["name"], "path": path,
                            "n_padj_0.05": int((pd.to_numeric(table["padj"], errors="coerce") < 0.05).sum())})
        report["outputs"] = results
        report["config"] = config
        report["warnings"] = [line for line in (proc.stderr or "").splitlines() if "Warning" in line][:20]
        with open(os.path.join(output_dir, f"r_de_{_safe(config.get('label') or engine)}_report.json"),
                  "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    method = {"deseq2": "DESeq2 (R)" + (" LRT" if config.get("reduced") else " Wald"),
              "edger_ql": "edgeR QL F-test (R), TMM", "voom": "limma-voom (R), TMM",
              "deseq1": "DESeq (R, original package) nbinomTest", "limma_trend": "limma-trend (R)",
              "mixed_anova": "mixed-effects ANOVA (lmerTest) + emmeans Tukey (R)"}[engine]
    extras = [x for x in (f"{config['n_sv']} SVs" if config.get("n_sv") else "",
                          f"{config['shrink']} shrinkage" if config.get("shrink") else "",
                          "IHW" if config.get("p_adjust") == "IHW" else "",
                          f"block {config['block']}" if config.get("block") else "",
                          "quality weights" if config.get("quality_weights") else "") if x]
    return {"method": method + (f" ({', '.join(extras)})" if extras else ""),
            "formula": report.get("formula"), "n_samples": int(matrix.shape[1]), "n_genes": int(matrix.shape[0]),
            "results": results, "report": report}


def run_r_de(counts_csv: str, metadata_csv: str, output_dir: str, *, engine: str, design: str,
             contrasts: Sequence[dict] = (), reduced: Optional[str] = None, lrt_name: str = "LRT",
             levels: Optional[dict] = None, numeric: Sequence[str] = (), n_sv: int = 0,
             sv_null: str = "~ 1", shrink: Optional[str] = None, p_adjust: str = "BH",
             block: Optional[str] = None, quality_weights: bool = False, filter_by_expr: bool = False,
             normalization: str = "TMM", fit_type: str = "parametric", alpha: float = 0.05,
             condition: Optional[str] = None, disp_method: str = "pooled", sharing_mode: str = "maximum",
             pairwise_fit: bool = False, subset: Optional[dict] = None, round_estimated_counts: bool = False,
             label: Optional[str] = None) -> dict[str, Any]:
    """Count-based DE in R: engine "deseq2", "edger_ql", "voom" or "deseq1" (see the module docstring).

    ``design`` is an R formula over metadata columns (``~ subject + time``); ``levels``
    gives each factor's levels with the reference first; ``numeric`` lists continuous
    covariates (age, RIN). ``n_sv`` surrogate variables are estimated against ``sv_null``
    and put first in the design (and the LRT reduced model). ``block`` (voom only) is a
    random blocking column fitted with duplicateCorrelation. deseq1 compares levels of
    ``condition``; ``pairwise_fit`` refits size factors and dispersions on the two groups.
    """
    if engine not in COUNT_ENGINES:
        raise PolicyViolation(f"engine must be one of {COUNT_ENGINES}")
    if engine == "deseq1" and not condition:
        raise PolicyViolation("deseq1 needs condition (the group column)")
    if not reduced and not contrasts:
        raise PolicyViolation("give contrasts, or reduced for an LRT")
    if shrink and engine != "deseq2":
        raise PolicyViolation("shrink is a DESeq2 option")
    config = {"engine": engine, "design": design, "contrasts": list(contrasts), "reduced": reduced,
              "lrt_name": lrt_name, "levels": levels or {}, "numeric": list(numeric), "n_sv": n_sv,
              "sv_null": sv_null, "shrink": shrink, "p_adjust": p_adjust, "block": block,
              "quality_weights": quality_weights, "filter_by_expr": filter_by_expr,
              "normalization": normalization, "fit_type": fit_type, "alpha": alpha, "condition": condition,
              "disp_method": disp_method, "sharing_mode": sharing_mode, "pairwise_fit": pairwise_fit,
              "label": label}
    return _run(counts_csv, metadata_csv, output_dir, {k: v for k, v in config.items() if v is not None},
                subset=subset, round_estimated_counts=round_estimated_counts)


def run_r_log_de(expression_csv: str, metadata_csv: str, output_dir: str, *, engine: str, design: str,
                 contrasts: Sequence[dict], random: Optional[str] = None, emmeans_specs: Optional[str] = None,
                 anova_term: Optional[str] = None, anova_type: str = "I", df_method: str = "satterthwaite",
                 block: Optional[str] = None, levels: Optional[dict] = None, numeric: Sequence[str] = (),
                 n_sv: int = 0, sv_null: str = "~ 1", n_cores: int = 8, subset: Optional[dict] = None,
                 label: Optional[str] = None) -> dict[str, Any]:
    """Log-scale DE in R: engine "mixed_anova" (per gene ``y ~ design + (1 | random)``, Type
    ``anova_type`` ANOVA, Tukey-adjusted emmeans pairs per ``emmeans_specs``, BH across
    genes per contrast) or "limma_trend" (optional duplicateCorrelation ``block``)."""
    if engine not in LOG_ENGINES:
        raise PolicyViolation(f"engine must be one of {LOG_ENGINES}")
    if engine == "mixed_anova" and not (random and emmeans_specs):
        raise PolicyViolation("mixed_anova needs random (subject column) and emmeans_specs (e.g. '~ time | diet')")
    config = {"engine": engine, "design": design, "contrasts": list(contrasts), "random": random,
              "emmeans_specs": emmeans_specs, "anova_term": anova_term, "anova_type": anova_type,
              "df_method": df_method, "block": block, "levels": levels or {}, "numeric": list(numeric),
              "n_sv": n_sv, "sv_null": sv_null, "n_cores": n_cores, "label": label}
    return _run(expression_csv, metadata_csv, output_dir, {k: v for k, v in config.items() if v is not None},
                subset=subset)
