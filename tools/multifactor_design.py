"""Deterministic validation and construction of multifactor DA designs.

The LLM may propose factors and an estimand, but this module owns the safety
checks before a model is fitted: arm replication, missing levels, matrix rank,
and residual degrees of freedom.  It deliberately does not guess a biological
contrast from arbitrary metadata columns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from patsy import dmatrix

from tools.analysis_policy import MIN_REPLICATES_PER_GROUP, PolicyViolation


@dataclass(frozen=True)
class MultifactorPlan:
    primary_factor: str
    control: str
    treatment: str
    covariates: tuple[str, ...]
    interactions: tuple[tuple[str, str], ...]
    formula: str
    coefficient: str
    safe_columns: dict[str, str]
    n_samples: int
    n_control: int
    n_treatment: int
    matrix_rank: int
    residual_df: int


def _safe_name(index: int, prefix: str = "Covariate") -> str:
    return f"{prefix}{index}"


def _normalise_columns(values: Iterable[str] | None) -> tuple[str, ...]:
    out: list[str] = []
    for value in values or ():
        value = str(value).strip()
        if value and value not in out:
            out.append(value)
    return tuple(out)


def candidate_covariates(metadata: pd.DataFrame, primary_factor: str) -> list[str]:
    """Return plausible pre-treatment categorical covariates for review.

    This is a candidate list only.  It never silently adds a covariate to a
    model because a column name happens to contain ``batch`` or ``sex``.
    """
    hints = ("batch", "donor", "subject", "sex", "age", "tissue", "time",
             "genotype", "cohort", "library", "prep", "plate")
    out: list[str] = []
    for col in metadata.columns:
        name = str(col).lower()
        if col == primary_factor or not any(h in name for h in hints):
            continue
        values = metadata[col].dropna()
        if 1 < values.nunique() <= 12:
            out.append(str(col))
    return out


def build_multifactor_plan(
    metadata: pd.DataFrame,
    *,
    primary_factor: str,
    control: str,
    treatment: str,
    covariates: Iterable[str] | None = None,
    interactions: Iterable[tuple[str, str]] | None = None,
    min_replicates: int = MIN_REPLICATES_PER_GROUP,
) -> MultifactorPlan:
    """Validate a two-arm estimand and return a safe patsy/PyDESeq2 plan.

    Covariates are explicit.  A caller that wants a simple two-group model can
    pass none; a caller that wants adjustment must name the factors.  Complete
    confounding and rank-deficient designs raise :class:`PolicyViolation`.
    """
    if primary_factor not in metadata.columns:
        raise PolicyViolation(f"Primary design factor {primary_factor!r} is missing.")
    if str(control) == str(treatment):
        raise PolicyViolation("Control and treatment must be different levels.")

    covs = _normalise_columns(covariates)
    missing = [c for c in covs if c not in metadata.columns]
    if missing:
        raise PolicyViolation(f"Covariate columns missing from metadata: {missing}")
    if any(c == primary_factor for c in covs):
        raise PolicyViolation("The primary factor cannot also be a covariate.")

    selected = metadata[metadata[primary_factor].astype(str).isin({str(control), str(treatment)})].copy()
    if selected.empty:
        raise PolicyViolation("No samples remain for the requested contrast.")
    selected["__Treatment"] = (selected[primary_factor].astype(str) == str(treatment)).astype(int)
    counts = selected["__Treatment"].value_counts().to_dict()
    n_control = int(counts.get(0, 0))
    n_treatment = int(counts.get(1, 0))
    if n_control < min_replicates or n_treatment < min_replicates:
        raise PolicyViolation(
            f"Each arm needs at least {min_replicates} biological replicates; "
            f"observed control={n_control}, treatment={n_treatment}."
        )

    # A categorical covariate with one level in the selected contrast carries
    # no information and is safer to omit than to pretend it was adjusted.
    missing_values = [c for c in covs if selected[c].isna().any()]
    if missing_values:
        raise PolicyViolation(
            f"Selected samples have missing values in covariates: {missing_values}."
        )
    effective_covs = tuple(c for c in covs if selected[c].dropna().nunique() > 1)
    safe_columns: dict[str, str] = {primary_factor: "__Primary"}
    for i, col in enumerate(effective_covs):
        safe_columns[col] = _safe_name(i)

    design_meta = pd.DataFrame({"Treatment": selected["__Treatment"].to_numpy()}, index=selected.index)
    terms = ["Treatment"]
    for col in effective_covs:
        safe = safe_columns[col]
        design_meta[safe] = selected[col].astype(str).to_numpy()
        terms.append(f"C({safe})")

    checked_interactions: list[tuple[str, str]] = []
    for left, right in interactions or ():
        left, right = str(left), str(right)
        if left not in {primary_factor, *effective_covs} or right not in {primary_factor, *effective_covs}:
            raise PolicyViolation(f"Interaction factors must be primary/covariate columns: {(left, right)}")
        if left == right:
            raise PolicyViolation("An interaction must contain two different factors.")
        left_safe = "Treatment" if left == primary_factor else f"C({safe_columns[left]})"
        right_safe = "Treatment" if right == primary_factor else f"C({safe_columns[right]})"
        terms.append(f"{left_safe}:{right_safe}")
        checked_interactions.append((left, right))

    formula = "~ " + " + ".join(terms)
    try:
        matrix = dmatrix(formula, design_meta, return_type="dataframe")
    except Exception as exc:
        raise PolicyViolation(f"Could not construct design matrix {formula!r}: {exc}") from exc
    rank = int(np.linalg.matrix_rank(matrix.to_numpy(dtype=float)))
    columns = int(matrix.shape[1])
    if rank < columns:
        raise PolicyViolation(
            f"Design matrix is rank deficient ({rank}/{columns}); factors may be completely confounded."
        )
    residual_df = int(len(selected) - rank)
    if residual_df < 1:
        raise PolicyViolation(f"No residual degrees of freedom remain after adjustment (df={residual_df}).")

    return MultifactorPlan(
        primary_factor=primary_factor,
        control=str(control),
        treatment=str(treatment),
        covariates=effective_covs,
        interactions=tuple(checked_interactions),
        formula=formula,
        coefficient="Treatment",
        safe_columns=safe_columns,
        n_samples=int(len(selected)),
        n_control=n_control,
        n_treatment=n_treatment,
        matrix_rank=rank,
        residual_df=residual_df,
    )
