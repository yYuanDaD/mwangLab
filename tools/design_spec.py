"""Paper-design helpers for explicit multi-factor contrasts."""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class DesignSpec:
    factors: tuple[str, ...]
    formula: str
    contrasts: tuple[tuple[str, str, str], ...]


def build_design_spec(metadata: pd.DataFrame, factors: list[str], contrasts: list[tuple[str, str, str]],
                      interactions: list[tuple[str, str]] | None = None) -> DesignSpec:
    """Validate a paper-derived design and return a patsy-style formula/contrast manifest.

    Contrast tuples are ``(factor, control_level, treatment_level)``. This function never
    guesses factor names or levels from keywords; the paper/Bo manifest must provide them.
    """
    missing = [f for f in factors if f not in metadata.columns]
    if missing:
        raise ValueError(f"design factors missing from metadata: {missing}")
    for factor, ctrl, treat in contrasts:
        if factor not in factors:
            raise ValueError(f"contrast factor {factor!r} is not in factors")
        levels = set(metadata[factor].dropna().astype(str))
        if str(ctrl) not in levels or str(treat) not in levels:
            raise ValueError(f"contrast levels unavailable for {factor}: {ctrl!r}, {treat!r}")
    terms = list(factors)
    for a, b in interactions or []:
        if a not in factors or b not in factors:
            raise ValueError("interaction factors must be listed in factors")
        terms.append(f"{a}:{b}")
    return DesignSpec(tuple(factors), "~ " + " + ".join(terms), tuple(contrasts))
