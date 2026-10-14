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


# --- Estimand-aware scoring -------------------------------------------------
#
# The sample gold encodes one comparison axis per series. A paper can analyse
# other exercise axes too (athletes versus controls next to pre/post), so the
# axis a decision chose is scored separately from whether its sample labels are
# right on that axis. Annotations live in
# test/validation/exergenedb_gold/estimand_annotations.json.

PURE = {"correct", "reversed"}


def corrected_roles(roles: pd.Series, annotation: Optional[dict]) -> tuple[pd.Series, int]:
    """Apply an annotation's label_corrections to the gold roles."""
    fixes = (annotation or {}).get("label_corrections") or []
    if not fixes:
        return roles, 0
    roles = roles.copy()
    for fix in fixes:
        roles[fix["sample_id"]] = fix["role"]
    return roles, len(fixes)


def roles_from_rules(meta: pd.DataFrame, rules: list[dict]) -> pd.Series:
    """Sample roles for an alternate axis from (column, control values, treatment values) rules."""
    roles: dict[str, str] = {}
    for rule in rules:
        for role, key in ((CONTROL, "control"), (TREATMENT, "treatment")):
            for value in rule.get(key, []):
                ids, how = samples_for_value(meta, rule["column"], value)
                if how == "missing_column" or not ids:
                    raise ValueError(f"axis rule selects nothing: {rule['column']!r} = {value!r}")
                for s in ids:
                    if roles.get(s, role) != role:
                        raise ValueError(f"axis rules give {s} both roles")
                    roles[s] = role
    return pd.Series(roles, dtype=str)


def subject_ids(meta: pd.DataFrame, subject: Optional[dict]) -> Optional[pd.Series]:
    """Subject ID per sample from an annotation's subject spec, or None."""
    if not subject or subject.get("column") not in meta.columns:
        return None
    values = meta[subject["column"]].astype(str)
    if subject.get("regex"):
        values = values.str.extract(subject["regex"], expand=False)
    return values


def score_pairing(gold: Optional[str], gold_column: Optional[str], call: Optional[str],
                  call_column: Optional[str]) -> dict[str, Any]:
    """Compare a pairing call (required / not_required / unknown) with the gold for its axis."""
    call = (call or "unknown").lower()
    if gold not in ("required", "not_required"):
        verdict = "no_gold"
    elif call not in ("required", "not_required"):
        verdict = "abstained"
    else:
        verdict = "correct" if call == gold else ("over_called" if call == "required" else "missed")
    column_ok = None
    if verdict == "correct" and gold == "required" and gold_column:
        # The validator shows subject IDs embedded in longer values as a grouped pseudo-column.
        column_ok = call_column in (gold_column, gold_column + REPLICATE_SUFFIX)
    return {"pairing_verdict": verdict, "pairing_column_ok": column_ok}


def score_estimand_decision(meta: pd.DataFrame, roles: pd.Series, annotation: dict,
                            contrasts: list[Contrast], pairing: Optional[str] = None,
                            pairing_column: Optional[str] = None) -> dict[str, Any]:
    """Score which axis a decision chose and, separately, its labels on that axis.

    axis              gold estimand, an alternate estimand, `off_axis` (mixed on every
                      annotated axis), or the set verdict when nothing was selected
                      (`refused`, `unresolvable`, `unscorable`)
    axis_admissible   the axis is the gold estimand or one the paper analyses
    label_verdict     the contrast-set verdict on the chosen axis (correct / reversed),
                      `mixed` when off axis
    estimand_correct  admissible axis and correct labels
    """
    roles, n_fixed = corrected_roles(roles, annotation)
    gold_axis = annotation["gold_estimand"]
    admissible = {gold_axis, *annotation.get("paper_estimands", [])}
    on_gold = score_contrast_set(meta, roles, contrasts)
    axis, label, pairing_gold, pairing_gold_col = None, None, None, None
    if on_gold["verdict"] in PURE:
        axis, label = gold_axis, on_gold["verdict"]
        pairing_gold, pairing_gold_col = annotation.get("pairing"), annotation.get("pairing_column")
    elif on_gold["verdict"] == "mixed":
        for alt in annotation.get("alternate_axes", []):
            s = score_contrast_set(meta, roles_from_rules(meta, alt["roles"]), contrasts)
            if s["verdict"] in PURE:
                axis, label = alt["estimand"], s["verdict"]
                pairing_gold, pairing_gold_col = alt.get("pairing"), alt.get("pairing_column")
                break
        if axis is None:
            axis, label = "off_axis", "mixed"
    else:
        axis = on_gold["verdict"]
    result = {
        "gold_verdict": on_gold["verdict"], "gold_purity": on_gold["purity"],
        "n_label_corrections": n_fixed, "axis": axis,
        "axis_is_gold": axis == gold_axis,
        "axis_admissible": (axis in admissible) if label is not None else None,
        "label_verdict": label,
        "estimand_correct": bool(axis in admissible and label == "correct"),
    }
    if label in PURE:
        result.update(score_pairing(pairing_gold, pairing_gold_col, pairing, pairing_column))
    else:
        result.update({"pairing_verdict": "n/a", "pairing_column_ok": None})
    return result


def check_estimand_annotation(meta: pd.DataFrame, roles: pd.Series, annotation: dict) -> list[str]:
    """Consistency problems in one series annotation (empty list when it checks out)."""
    problems = []
    roles, _ = corrected_roles(roles, annotation)
    labelled = roles[roles.index.isin(meta.index.astype(str))]
    subjects = subject_ids(meta, annotation.get("subject"))
    if annotation.get("subject") and subjects is None:
        problems.append(f"subject column missing: {annotation['subject'].get('column')!r}")
    if annotation.get("pairing") == "required" and subjects is not None:
        ctrl = set(subjects.reindex(labelled.index[labelled == CONTROL]).dropna())
        treat = set(subjects.reindex(labelled.index[labelled == TREATMENT]).dropna())
        if len(ctrl & treat) < 2:
            problems.append(f"pairing required but only {len(ctrl & treat)} subjects span both arms")
    col = annotation.get("pairing_column")
    if col and col not in meta.columns:
        problems.append(f"pairing_column missing: {col!r}")
    for alt in annotation.get("alternate_axes", []):
        try:
            roles_from_rules(meta, alt["roles"])
        except ValueError as e:
            problems.append(f"{alt['estimand']}: {e}")
    return problems
