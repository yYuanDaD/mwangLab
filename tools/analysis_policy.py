"""Deterministic scientific policies shared by differential-analysis tools.

These are invariants, not LLM guidance.  A caller cannot bypass them by choosing
different wording in a prompt: invalid designs and incompatible matrix/method
combinations are rejected before a statistical model is fitted.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


MIN_REPLICATES_PER_GROUP = 2
MIN_ALIGNED_FRACTION_PER_GROUP = 0.5
RAW_INTEGER_FRACTION = 0.99
LOG_SCALE_RAW_LIKE_MAX = 100.0


class PolicyViolation(ValueError):
    """Raised when a stable scientific invariant is violated."""


@dataclass(frozen=True)
class MatrixProfile:
    n_features: int
    n_samples: int
    n_values: int
    min_value: float
    max_value: float
    integer_fraction: float


def numeric_matrix(df: pd.DataFrame, *, label: str) -> pd.DataFrame:
    """Remove annotation-only columns and require a usable numeric matrix."""
    coerced = df.apply(pd.to_numeric, errors="coerce")
    annotation_cols = coerced.columns[coerced.isna().all(axis=0)].tolist()
    numeric = coerced.drop(columns=annotation_cols)
    if numeric.shape[1] < 2:
        raise PolicyViolation(
            f"{label} must contain at least two numeric sample columns; "
            f"found {numeric.shape[1]}. The input may be metadata rather than an expression matrix."
        )
    if numeric.shape[0] == 0:
        raise PolicyViolation(f"{label} contains no feature rows.")
    return numeric


def profile_matrix(df: pd.DataFrame) -> MatrixProfile:
    values = df.to_numpy(dtype=float, copy=False)
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        raise PolicyViolation("Expression matrix contains no finite numeric values.")
    integer_fraction = float(np.isclose(finite, np.rint(finite), atol=1e-8).mean())
    return MatrixProfile(
        n_features=int(df.shape[0]),
        n_samples=int(df.shape[1]),
        n_values=int(finite.size),
        min_value=float(finite.min()),
        max_value=float(finite.max()),
        integer_fraction=integer_fraction,
    )


def enforce_method_matrix_compatibility(df: pd.DataFrame, *, method: str) -> MatrixProfile:
    """Enforce the stable matrix-type -> DA-method mapping.

    DESeq2, edgeR and limma-voom require non-negative integer raw counts.
    Plain limma requires a transformed/log-scale matrix; a clearly raw-count-like
    matrix is rejected rather than merely warned about.
    """
    p = profile_matrix(df)
    method = method.lower()
    if method in {"deseq2", "edger", "limma-voom"}:
        if p.n_values != df.shape[0] * df.shape[1]:
            raise PolicyViolation(
                f"{method} requires a complete raw-count matrix; missing/non-finite values are present."
            )
        if p.min_value < 0:
            raise PolicyViolation(f"{method} requires non-negative raw counts; minimum={p.min_value:g}.")
        if p.integer_fraction < RAW_INTEGER_FRACTION:
            raise PolicyViolation(
                f"{method} requires raw integer counts, but only {p.integer_fraction:.1%} "
                "of finite values are integer-like. Do not round normalized/FPKM/TPM data; "
                "use a suitable log transform followed by limma."
            )
    elif method == "limma":
        raw_like = p.integer_fraction >= RAW_INTEGER_FRACTION and p.max_value > LOG_SCALE_RAW_LIKE_MAX
        if raw_like:
            raise PolicyViolation(
                f"limma requires transformed/log-scale expression, but this matrix is raw-count-like "
                f"({p.integer_fraction:.1%} integer-like; max={p.max_value:g}). "
                "Use DESeq2/edgeR/limma-voom for raw counts."
            )
    else:
        raise PolicyViolation(f"Unknown differential-analysis method: {method!r}.")
    return p


def select_valid_two_group_design(
    metadata: pd.DataFrame,
    *,
    design_column: str,
    control_group: str,
    treatment_group: str,
    available_samples,
    min_replicates: int = MIN_REPLICATES_PER_GROUP,
    min_group_coverage: float = MIN_ALIGNED_FRACTION_PER_GROUP,
) -> tuple[pd.DataFrame, pd.Series]:
    """Validate a two-arm design and return aligned contrast metadata."""
    if design_column not in metadata.columns:
        raise PolicyViolation(
            f"Design column {design_column!r} does not exist. Available columns: {list(metadata.columns)}"
        )
    if str(control_group) == str(treatment_group):
        raise PolicyViolation("Control and treatment groups must be different values.")

    available = set(available_samples)
    requested = metadata[metadata[design_column].isin([control_group, treatment_group])]
    expected_counts = requested[design_column].value_counts()
    selected = requested
    selected = selected.loc[[idx for idx in selected.index if idx in available]]
    counts = selected[design_column].value_counts()

    missing = [g for g in (control_group, treatment_group) if int(counts.get(g, 0)) == 0]
    if missing:
        all_groups = metadata[design_column].dropna().unique().tolist()
        raise PolicyViolation(
            f"The requested contrast is unavailable after sample alignment; missing groups={missing}. "
            f"Available values in {design_column!r}: {all_groups}"
        )
    underpowered = {str(g): int(counts.get(g, 0)) for g in (control_group, treatment_group)
                    if int(counts.get(g, 0)) < min_replicates}
    if underpowered:
        raise PolicyViolation(
            f"Each contrast arm needs at least {min_replicates} biological replicates; "
            f"observed {underpowered}."
        )
    low_coverage = {}
    for group in (control_group, treatment_group):
        expected = int(expected_counts.get(group, 0))
        aligned = int(counts.get(group, 0))
        coverage = aligned / expected if expected else 0.0
        if coverage < min_group_coverage:
            low_coverage[str(group)] = f"{aligned}/{expected} ({coverage:.1%})"
    if low_coverage:
        raise PolicyViolation(
            f"Aligned sample coverage is below {min_group_coverage:.0%} in a contrast arm: "
            f"{low_coverage}. Refusing a potentially biased partial-sample analysis."
        )
    return selected, counts
