"""Score control/treatment decisions against a sample-level gold set.

The gold is a mapping from GEO sample ID (GSM) to `control` or `treatment`,
for example the ExerGeneDB export written by scripts/fetch_exergenedb_labels.py.
A decision is one or more contrasts `(design_column, control_value,
treatment_value)` over a GEO metadata table indexed by GSM.

Verdicts for one contrast, using only samples that have a gold label:
    correct       every control sample is gold control and every treatment sample is gold treatment
    reversed      the two arms are swapped
    mixed         at least one arm contains samples from both gold roles
    unscorable    neither arm has a gold-labelled sample
    unresolvable  the column or value does not select samples in the metadata
A decision with no contrasts is `refused`. Refusals are reported separately
from errors because a refusal on insufficient evidence is an acceptable outcome.

This module only scores decisions. It does not judge pairing or covariates;
`pairing_signal` and the strata count are diagnostics that flag contrasts which
would need blocking or stratification before a two-group test is valid.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Optional

import pandas as pd

REPLICATE_SUFFIX = "__replicate_grouped"
CONTROL = "control"
TREATMENT = "treatment"
CONFIDENT_LEVELS = {"high", "medium"}
PAIRING_HINTS = ("subject", "individual", "donor", "patient", "participant",
                 "volunteer", "person", "animal", "mouse id", "pair")

Contrast = tuple[str, str, str]


def load_gold(samples_csv: str) -> pd.DataFrame:
    gold = pd.read_csv(samples_csv, dtype=str).fillna("")
    required = {"sample_id", "series_id", "role"}
    missing = required - set(gold.columns)
    if missing:
        raise ValueError(f"gold file missing columns: {sorted(missing)}")
    bad = set(gold["role"]) - {CONTROL, TREATMENT}
    if bad:
        raise ValueError(f"gold file has unexpected roles: {sorted(bad)}")
    if gold["sample_id"].duplicated().any():
        raise ValueError("gold file has duplicated sample_id rows")
    return gold.set_index("sample_id")


def _group_title(value: str, column_lower: str) -> str:
    # Mirrors the title grouping in tools/llm_helpers.summarize_metadata_for_llm.
    grouped = re.sub(r"[\s._,-]+\d+\s*$", "", value)
    if grouped == value and column_lower.startswith("title"):
        grouped = re.sub(r"\d+\s*$", "", value)
    return grouped.strip(" ._,-")


def samples_for_value(meta: pd.DataFrame, column: str, value: str) -> tuple[list[str], str]:
    """Return metadata sample IDs selected by `column == value` and how the column resolved."""
    if column in meta.columns:
        mask = meta[column].astype(str) == str(value)
        return [str(i) for i in meta.index[mask]], "column"
    if column.endswith(REPLICATE_SUFFIX):
        source = column[: -len(REPLICATE_SUFFIX)]
        if source in meta.columns:
            grouped = meta[source].astype(str).map(lambda v: _group_title(v, source.lower()))
            mask = grouped == str(value)
            return [str(i) for i in meta.index[mask]], "replicate_grouped"
    return [], "missing_column"


def _role_counts(sample_ids: Iterable[str], roles: pd.Series) -> dict[str, int]:
    labelled = [roles[s] for s in sample_ids if s in roles.index]
    return {
        CONTROL: sum(r == CONTROL for r in labelled),
        TREATMENT: sum(r == TREATMENT for r in labelled),
        "unlabelled": sum(1 for s in sample_ids if s not in roles.index),
    }


def score_contrast(meta: pd.DataFrame, roles: pd.Series, contrast: Contrast,
                   gold: Optional[pd.DataFrame] = None) -> dict[str, Any]:
    column, control_value, treatment_value = contrast
    ctrl_ids, ctrl_how = samples_for_value(meta, column, control_value)
    treat_ids, treat_how = samples_for_value(meta, column, treatment_value)
    ctrl = _role_counts(ctrl_ids, roles)
    treat = _role_counts(treat_ids, roles)
    result = {
        "contrast": f"{column} | {control_value} vs {treatment_value}",
        "column_resolution": ctrl_how if ctrl_how == treat_how else f"{ctrl_how}/{treat_how}",
        "executable_column": column in meta.columns,
        "n_control_selected": len(ctrl_ids),
        "n_treatment_selected": len(treat_ids),
        "control_arm_gold": ctrl,
        "treatment_arm_gold": treat,
        "control_ids": ctrl_ids,
        "treatment_ids": treat_ids,
    }
    labelled_ctrl = ctrl[CONTROL] + ctrl[TREATMENT]
    labelled_treat = treat[CONTROL] + treat[TREATMENT]
    if not ctrl_ids or not treat_ids:
        verdict = "unresolvable"
    elif labelled_ctrl == 0 and labelled_treat == 0:
        verdict = "unscorable"
    elif ctrl[TREATMENT] == 0 and treat[CONTROL] == 0:
        verdict = "correct"
    elif ctrl[CONTROL] == 0 and treat[TREATMENT] == 0:
        verdict = "reversed"
    else:
        verdict = "mixed"
    result["verdict"] = verdict
    result["n_labelled_correct"] = ctrl[CONTROL] + treat[TREATMENT]
    result["n_labelled"] = labelled_ctrl + labelled_treat
    if gold is not None and "stratum_key" in gold.columns:
        ids = [s for s in ctrl_ids + treat_ids if s in gold.index]
        result["n_gold_strata"] = int(gold.loc[ids, "stratum_key"].nunique()) if ids else 0
    result["pairing_signal"] = pairing_signal(meta, ctrl_ids, treat_ids)
    return result


def score_contrast_set(meta: pd.DataFrame, roles: pd.Series, contrasts: list[Contrast],
                       gold: Optional[pd.DataFrame] = None) -> dict[str, Any]:
    if not contrasts:
        return {"verdict": "refused", "n_contrasts": 0, "purity": None, "contrasts": [],
                "max_gold_strata": 0, "pairing_signal": []}
    scored = [score_contrast(meta, roles, c, gold) for c in contrasts]
    kinds = {s["verdict"] for s in scored}
    if "mixed" in kinds or {"correct", "reversed"} <= kinds:
        verdict = "mixed"
    elif "reversed" in kinds:
        verdict = "reversed"
    elif "unresolvable" in kinds:
        verdict = "unresolvable"
    elif "unscorable" in kinds:
        verdict = "unscorable"
    else:
        verdict = "correct"
    labelled = sum(s["n_labelled"] for s in scored)
    good = sum(s["n_labelled_correct"] for s in scored)
    signals = sorted({col for s in scored for col, _ in s["pairing_signal"]})
    return {
        "verdict": verdict,
        "n_contrasts": len(scored),
        "purity": round(good / labelled, 4) if labelled else None,
        "contrasts": scored,
        "max_gold_strata": max(s.get("n_gold_strata", 0) for s in scored),
        "pairing_signal": signals,
        "all_columns_executable": all(s["executable_column"] for s in scored),
    }


def pairing_signal(meta: pd.DataFrame, ctrl_ids: list[str], treat_ids: list[str]) -> list[tuple[str, int]]:
    """Subject-like columns whose values recur across both arms (heuristic, not gold)."""
    if not ctrl_ids or not treat_ids:
        return []
    hits = []
    for column in meta.columns:
        if not any(h in str(column).lower() for h in PAIRING_HINTS):
            continue
        ctrl_vals = set(meta.loc[ctrl_ids, column].dropna().astype(str))
        treat_vals = set(meta.loc[treat_ids, column].dropna().astype(str))
        shared = ctrl_vals & treat_vals
        if len(shared) >= 2 and meta[column].nunique(dropna=True) >= 2:
            hits.append((str(column), len(shared)))
    return hits


def _field(obj: Any, name: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def llm_triple(llm: Any) -> Optional[Contrast]:
    values = [_field(llm, k) for k in ("design_column", "control_value", "treatment_value")]
    return tuple(values) if all(values) else None


def llm_accepts(llm: Any) -> bool:
    confidence = str(_field(llm, "confidence") or "low").lower()
    return (llm_triple(llm) is not None and _field(llm, "intent_match") is True
            and confidence in CONFIDENT_LEVELS)


def production_route(python_contrasts: list[Contrast], python_confident: bool, llm: Any,
                     strict: bool = False) -> tuple[list[Contrast], str]:
    """Mirror the contrast policy in tools/batch_tools.run_batch_geo_pipeline.

    Keep this in sync with batch_tools when that policy changes; the unit test
    pins the expected routes.
    """
    design = python_contrasts[0] if python_contrasts else None
    if python_confident and design is not None and not strict:
        return list(python_contrasts), "python_confident"
    if llm is None:
        return [], "llm_unavailable_blocked"
    triple = llm_triple(llm)
    if llm_accepts(llm) and _field(llm, "is_valid") and triple == design:
        return ([triple] if strict else list(python_contrasts)), "llm_confirm"
    if llm_accepts(llm):
        return [triple], "llm_override" if design is not None else "llm_proposed"
    if _field(llm, "intent_match") is False:
        return [], "llm_refuse_intent_mismatch"
    return [], "llm_refuse"
