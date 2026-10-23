"""Pre-analysis suitability checks: can this study's data support the analysis?

One report per case, written before the design gate is decided (todo 2026-10-16,
section 2). Each check returns a status and the evidence for it; ``report`` combines
them into one verdict:

    data_type     the matrix type and whether a route exists for it        (2.1)
    grouping      the design factors are present and determinable           (2.2)
    covariance    blocking terms and covariates, with the reason for each   (2.3)
    sample_size   every compared group has >= 3 samples                     (2.4)
    comparisons   every sensible comparison of the design, not just one     (2.5)
    sex           expression-based sex vs metadata; per-sex analysis plan   (2.6)
    required_data the files and fields the data type needs                  (2.7)

The report is part of the ``design`` gate (2.8): the design record cites it as
evidence and carries its verdict in ``final.suitability``; a design that the report
calls ``not_analyzable`` cannot be recorded as valid. No new gate is added.

Deterministic, no LLM, no network (the sex check uses gene symbols already in the
matrix). Decisions stay with the agent; these functions list facts and candidates.
"""

from __future__ import annotations

import itertools
import json
import re
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd

MIN_GROUP = 3

# ---------------------------------------------------------------------------
# 2.7 Required data per data type
# ---------------------------------------------------------------------------

REQUIRED_DATA = {
    "bulk_rnaseq_counts": {
        "files": ["gene x sample raw (or estimated) count matrix", "sample metadata table"],
        "fields": ["sample ID matching the matrix columns", "group / condition per sample",
                   "subject or animal ID when samples are repeated", "sex (for the sex check)",
                   "batch, lane or sequencing run when the paper used it"],
        "route": "DESeq2 / edgeR / limma-voom",
    },
    "bulk_rnaseq_normalized": {
        "files": ["gene x sample FPKM/RPKM/TPM matrix", "sample metadata table"],
        "fields": ["sample ID", "group / condition", "subject ID for repeated samples", "sex"],
        "route": "limma on log2(x+1); count models are not valid",
    },
    "microarray": {
        "files": ["normalized log-scale intensity matrix (series matrix)", "platform annotation (probe -> gene)"],
        "fields": ["sample ID", "group / condition", "subject ID for repeated samples", "sex", "batch"],
        "route": "limma",
    },
    "scrnaseq": {
        "files": ["cell x gene count matrix (10x or table)", "cell metadata with donor/sample and cell type"],
        "fields": ["donor or sample ID per cell", "cell type or cluster", "group / condition per donor"],
        "route": "pseudobulk per donor and cell type, then DESeq2 / edgeR",
    },
    "proteomics": {
        "files": ["protein x sample intensity matrix (LFQ / TMT reporter)", "sample annotation"],
        "fields": ["sample ID", "group / condition", "TMT plex / batch", "subject ID for repeated samples"],
        "route": "limma on log2 intensities",
    },
    "methylation": {
        "files": ["CpG x sample beta (or M-value) matrix", "sample annotation"],
        "fields": ["sample ID", "group / condition", "array batch / slide", "sex"],
        "route": "limma on M-values",
    },
}

_TYPE_TO_KEY = (
    ("single", "scrnaseq"), ("pseudobulk", "scrnaseq"), ("estimated", "bulk_rnaseq_counts"), ("raw", "bulk_rnaseq_counts"), ("count", "bulk_rnaseq_counts"),
    ("fpkm", "bulk_rnaseq_normalized"), ("rpkm", "bulk_rnaseq_normalized"), ("tpm", "bulk_rnaseq_normalized"),
    ("beta", "methylation"), ("m-value", "methylation"), ("intensity", "proteomics"),
    ("array", "microarray"), ("log", "microarray"),
)


def required_data(data_type: str) -> dict:
    """Files and fields a data type needs (``data_type`` is a REQUIRED_DATA key or a matrix type)."""
    key = data_type if data_type in REQUIRED_DATA else next(
        (k for word, k in _TYPE_TO_KEY if word in str(data_type).lower()), "")
    return {"data_type": data_type, "key": key, **REQUIRED_DATA.get(key, {"files": [], "fields": [], "route": ""})}


def check_data_type(matrix_type: str, metadata: pd.DataFrame | None = None) -> dict:
    """2.1 + 2.7: a route exists for the matrix type and the metadata has the fields it needs."""
    req = required_data(matrix_type)
    if not req["key"] or "ambiguous" in str(matrix_type).lower() or "unknown" in str(matrix_type).lower():
        return {"status": "fail", "matrix_type": matrix_type, "reason": "matrix type unknown or ambiguous",
                "required": req}
    return {"status": "pass", "matrix_type": matrix_type, "route": req["route"], "required": req}


# ---------------------------------------------------------------------------
# 2.2 Grouping
# ---------------------------------------------------------------------------

_BLANK = {"", "nan", "none", "na", "n/a", "null", "missing", "not applicable", "unknown", "--"}


def check_grouping(metadata: pd.DataFrame, factors: Sequence[str]) -> dict:
    """Every design factor exists, has no blank value, and has two or more levels.

    A factor that fails stops the case: the groups cannot be determined from the data
    (give the model the sample titles and subject IDs before giving up, B3)."""
    problems, levels = [], {}
    for f in factors:
        if f not in metadata.columns:
            problems.append(f"{f}: not in metadata")
            continue
        values = metadata[f].astype(str).str.strip()
        blank = values.str.lower().isin(_BLANK)
        if blank.any():
            problems.append(f"{f}: {int(blank.sum())} sample(s) without a value: {list(values.index[blank][:5])}")
        levels[f] = values[~blank].value_counts().to_dict()
        if len(levels[f]) < 2 and len(factors) == 1:
            problems.append(f"{f}: one level only ({list(levels[f])})")
    if len(factors) > 1 and all(len(v) < 2 for v in levels.values()):
        problems.append("no factor has two or more levels")
    return {"status": "fail" if problems else "pass", "factors": list(factors), "levels": levels,
            "problems": problems}


# ---------------------------------------------------------------------------
# 2.5 Comparisons
# ---------------------------------------------------------------------------

REFERENCE_WORDS = re.compile(
    r"^(ctrl|control|con|sed|sedentary|untrained|vehicle|veh|pbs|saline|wt|wild[- ]?type|baseline|base|"
    r"pre|pre[- ]?(training|exercise|intervention)?|rest|resting|sham|placebo|pla|chow|normal|day ?0|0 ?h|"
    r"t0|week ?0|before|naive|non[- ]?exercise|no exercise|inactive|cage)\b", re.I)


def reference_level(levels: Sequence[str]) -> str | None:
    """The level that reads as the control (sedentary, baseline, wild type...), else None."""
    hits = [lv for lv in levels if REFERENCE_WORDS.search(str(lv).strip())]
    return hits[0] if len(hits) == 1 else None


def _time_order(levels: Sequence[str]) -> list[str] | None:
    """Levels sorted by the number they carry (0h, 3h, 24h; week 0/4/8), when all carry one."""
    nums = []
    for lv in levels:
        m = re.search(r"-?\d+(\.\d+)?", str(lv))
        if not m:
            return None
        nums.append(float(m.group(0)))
    return [lv for _, lv in sorted(zip(nums, levels))] if len(set(nums)) == len(nums) else None


def _cell_mask(meta: pd.DataFrame, cell: dict) -> pd.Series:
    mask = pd.Series(True, index=meta.index)
    for col, val in cell.items():
        mask &= meta[col].astype(str) == str(val)
    return mask


def enumerate_comparisons(metadata: pd.DataFrame, factors: Sequence[str], *,
                          references: dict[str, str] | None = None, strata: Sequence[str] = (),
                          min_group: int = MIN_GROUP, max_pairwise_levels: int = 6) -> list[dict]:
    """Every sensible comparison of a categorical design, each with its group sizes.

    - For each factor, every pair of its levels (test vs reference; with no reference,
      vs the earlier level in time order or name order), within every combination of
      the other factors (simple effects). Levels above ``max_pairwise_levels`` keep
      only comparisons to the reference and between neighbours in time order.
    - For every pair of factors, each 2x2 interaction (difference of differences)
      between a non-reference level and the reference of both.
    - ``strata`` (for example a sex column) repeat everything within each stratum.

    Each comparison: ``name``, ``kind`` (simple / interaction), ``factor``, ``test``,
    ``reference``, ``within`` (fixed levels of other factors), ``cells`` (the cells that
    enter it, with n), ``analyzable`` (every cell has >= ``min_group`` samples).
    The paper's planned contrasts are a subset; the rest run as exploratory.
    """
    references = dict(references or {})
    meta = metadata.copy()
    for f in list(factors) + list(strata):
        meta[f] = meta[f].astype(str)
    out: list[dict] = []
    stratum_values = [dict(zip(strata, combo)) for combo in
                      itertools.product(*[sorted(meta[s].unique()) for s in strata])] or [{}]
    for stratum in stratum_values:
        sub = meta[_cell_mask(meta, stratum)] if stratum else meta
        levels = {f: sorted(sub[f].unique()) for f in factors}
        refs = {f: references.get(f) or reference_level(levels[f]) for f in factors}
        for f in factors:
            lv = levels[f]
            ref = refs[f] if refs[f] in lv else None
            order = _time_order(lv)
            if ref is None and order:
                ref = order[0]
            pairs = []
            if len(lv) <= max_pairwise_levels:
                for a, b in itertools.combinations(order or lv, 2):
                    # test vs reference when one is the reference, else later vs earlier.
                    pairs.append((a, b) if b == ref else (b, a))
            else:
                pairs = [(x, ref) for x in lv if ref and x != ref]
                if order:
                    pairs += [(b, a) for a, b in zip(order, order[1:]) if a != ref]
            others = [g for g in factors if g != f]
            for combo in itertools.product(*[levels[g] for g in others]):
                within = dict(zip(others, combo))
                for test, refl in pairs:
                    cells = [{**stratum, **within, f: test}, {**stratum, **within, f: refl}]
                    out.append(_comparison("simple", f, test, refl, {**stratum, **within}, cells, sub, min_group))
        for f, g in itertools.combinations(factors, 2):
            rf, rg = refs[f], refs[g]
            if rf not in levels[f] or rg not in levels[g]:
                continue
            rest = [h for h in factors if h not in (f, g)]
            for combo in itertools.product(*[levels[h] for h in rest]):
                within = dict(zip(rest, combo))
                for a in [x for x in levels[f] if x != rf]:
                    for b in [x for x in levels[g] if x != rg]:
                        cells = [{**stratum, **within, f: a, g: b}, {**stratum, **within, f: rf, g: b},
                                 {**stratum, **within, f: a, g: rg}, {**stratum, **within, f: rf, g: rg}]
                        c = _comparison("interaction", f"{f}:{g}", f"{a}:{b}", f"{rf}:{rg}",
                                        {**stratum, **within}, cells, sub, min_group)
                        out.append(c)
    return out


def _comparison(kind, factor, test, ref, within, cells, meta, min_group) -> dict:
    sized = [{"cell": c, "n": int(_cell_mask(meta, c).sum())} for c in cells]
    where = "".join(f"_{k}-{v}" for k, v in within.items())
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{factor}_{test}_vs_{ref}{where}").strip("_")
    return {"name": name, "kind": kind, "factor": factor, "test": test, "reference": ref,
            "within": within, "cells": sized,
            "analyzable": all(c["n"] >= min_group for c in sized)}


def check_sample_size(comparisons: Sequence[dict], planned: Sequence[str] = ()) -> dict:
    """2.4: comparisons with a group under 3 are not analyzable. Fails when no
    comparison (or no planned one, when given) is analyzable.

    ``planned`` uses the enumerated names (``grp_O_vs_Y``); names that match no
    comparison are listed in ``unknown_planned`` and make the check ``partial``."""
    names = {c["name"] for c in comparisons}
    ok = [c["name"] for c in comparisons if c["analyzable"]]
    small = [c["name"] for c in comparisons if not c["analyzable"]]
    known = [p for p in planned if p in names]
    unknown = [p for p in planned if p not in names]
    planned_ok = [p for p in known if p in ok]
    status = "pass" if (planned_ok if known else ok) else "fail"
    if status == "pass" and (small or unknown):
        status = "partial"
    return {"status": status, "n_comparisons": len(comparisons), "n_analyzable": len(ok),
            "too_small": small, "planned_analyzable": planned_ok, "unknown_planned": unknown}


# ---------------------------------------------------------------------------
# 2.3 Covariance
# ---------------------------------------------------------------------------

SUBJECT_COLUMN = re.compile(r"subject|donor|patient|participant|individual|animal|mouse id|rat id|pair", re.I)
BATCH_COLUMN = re.compile(r"batch|lane|flow ?cell|run|plate|chip|slide|library|seq(uencing)?[ _-]?(date|run)|"
                          r"processing|cohort|site|center|centre", re.I)


def check_covariance(metadata: pd.DataFrame, factors: Sequence[str], *,
                     subject: str | None = None, candidates: Sequence[str] | None = None) -> dict:
    """2.3: blocking terms and covariates with the reason for each decision.

    - A subject column with repeated samples across a factor's levels is a required
      blocking term (paired / repeated measures).
    - A batch-like column crossed with the factors is a candidate covariate (include
      when the paper used it or the design stays full rank; the agent decides).
    - A column completely confounded with a factor stops that comparison.
    Columns are judged by their values, never added because of their names alone.
    """
    from tools import native
    meta = metadata.copy()
    decisions, blocking, covariates, stop = [], [], [], []
    subject = subject or next((c for c in meta.columns if SUBJECT_COLUMN.search(str(c))
                               and c not in factors and 1 < meta[c].nunique() < len(meta)), None)
    if subject and subject not in meta.columns:
        decisions.append({"column": subject, "decision": "omit",
                          "reason": "not a sample-level column (for example a pseudobulk key built later)"})
        subject = None
    if subject:
        repeated = any(native.pairing_report(meta, subject, f, sorted(meta[f].astype(str).unique()))
                       ["repeated_across_levels"] for f in factors)
        if repeated:
            blocking.append(subject)
            decisions.append({"column": subject, "decision": "block",
                              "reason": "same subject sampled at several levels: repeated measures"})
        else:
            decisions.append({"column": subject, "decision": "omit",
                              "reason": "one sample per subject per factor level set: an identifier, not a block"})
    cand = list(candidates) if candidates is not None else [
        c for c in meta.columns if BATCH_COLUMN.search(str(c)) and c not in factors and c != subject]
    for col in cand:
        worst = "crossed"
        for f in factors:
            rep = native.confounding_report(meta, f, [col])[0]["status"]
            if rep in ("complete_confounding", "primary_nested_in_candidate"):
                worst = rep
                break
            if rep in ("constant", "sample_identifier"):
                worst = rep
        if worst in ("constant", "sample_identifier"):
            decisions.append({"column": col, "decision": "omit", "reason": f"{worst}: carries no batch information"})
        elif worst in ("complete_confounding", "primary_nested_in_candidate"):
            stop.append(col)
            decisions.append({"column": col, "decision": "stop",
                              "reason": f"{worst} with a design factor: its effect cannot be separated"})
        else:
            covariates.append(col)
            decisions.append({"column": col, "decision": "candidate_covariate",
                              "reason": "crossed with the design factors; include if the paper did or PCA shows it"})
    terms = list(factors) + blocking + covariates
    rank = native.design_check(meta, terms) if terms else None
    if rank and not rank["full_rank"]:
        # Covariates that break the rank are dropped from the candidate list, with the reason.
        for col in list(covariates):
            trial = native.design_check(meta, [t for t in terms if t != col])
            if trial["full_rank"]:
                covariates.remove(col)
                decisions.append({"column": col, "decision": "omit", "reason": "makes the design rank deficient"})
                terms.remove(col)
                rank = trial
    status = "fail" if stop or (rank and not rank["full_rank"]) or (rank and rank["residual_df"] < 1) else "pass"
    return {"status": status, "covariance_status": "required" if blocking else "not_required",
            "blocking_terms": blocking, "covariates": covariates, "stopping_columns": stop,
            "decisions": decisions,
            "design": {k: rank[k] for k in ("formula_equivalent", "rank", "full_rank", "residual_df",
                                             "min_cell_size")} if rank else None}


# ---------------------------------------------------------------------------
# 2.6 Sex
# ---------------------------------------------------------------------------

def check_sex(matrix_csv: str | Path, metadata: pd.DataFrame, *, organism: str = "Mouse",
              out_dir: str | Path = ".") -> dict:
    """2.6: sex from X/Y genes (Xist vs Ddx3y/Uty/Kdm5d/Eif2s3y/Rps4y1), compared with the
    metadata sex column. Reuses ``stats_tools.infer_sex_from_expression``.

    status: ``pass`` (agrees, or no metadata sex to compare), ``mismatch`` (labels to
    fix before analysis: a swap or mislabel), ``no_markers`` (cannot check).
    ``sex_by_sample`` is the metadata sex where present, else the confident prediction;
    use it to stratify."""
    from tools.stats_tools import _detect_sex_column, _normalize_sex_value, infer_sex_from_expression
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_csv = out_dir / "_sex_check_metadata.csv"
    metadata.to_csv(meta_csv)
    msg = infer_sex_from_expression.invoke({"counts_csv": str(matrix_csv), "metadata_csv": str(meta_csv),
                                            "organism": organism, "output_dir": str(out_dir)})
    meta_csv.unlink(missing_ok=True)
    tsv = out_dir / f"{Path(matrix_csv).stem}_sex_check.tsv"
    if not tsv.exists():
        return {"status": "no_markers", "summary": msg.splitlines()[0] if msg else "", "sex_by_sample": {}}
    table = pd.read_csv(tsv, sep="\t", index_col=0)
    table.index = table.index.astype(str)
    sex_col = _detect_sex_column(metadata)
    reported = metadata[sex_col].map(_normalize_sex_value) if sex_col else pd.Series(dtype=str)
    mismatched = table.index[table.get("agreement", pd.Series(dtype=str)) == "MISMATCH"].tolist()
    by_sample = {}
    for s in table.index:
        r = str(reported.get(s, "")) if sex_col else ""
        p = table.at[s, "predicted_sex"] if table.at[s, "confidence"] != "ambiguous" else "unknown"
        by_sample[s] = r or (p if p != "unknown" else "")
    predicted = table["predicted_sex"].value_counts().to_dict()
    return {"status": "mismatch" if mismatched else "pass",
            "summary": msg.splitlines()[0] if msg else "",
            "metadata_sex_column": sex_col, "predicted": predicted, "mismatched": mismatched,
            "table": str(tsv), "sex_by_sample": by_sample,
            "sexes": sorted(v for v in set(by_sample.values()) if v)}


def sex_split_plan(metadata: pd.DataFrame, factors: Sequence[str], sex_by_sample: dict,
                   min_group: int = MIN_GROUP, references: dict | None = None) -> dict:
    """Run males and females separately when both are present, even if the paper pooled them.

    Returns the comparisons per sex (from ``enumerate_comparisons`` with sex as a
    stratum) and whether each sex alone has an analyzable comparison. With one sex
    present there is nothing to split."""
    meta = metadata.copy()
    meta["_sex"] = [sex_by_sample.get(str(s), "") for s in meta.index]
    known = meta[meta["_sex"].isin(["male", "female"])]
    sexes = sorted(known["_sex"].unique())
    if len(sexes) < 2:
        return {"split": False, "sexes": sexes,
                "reason": "one sex only" if sexes else "sex unknown for every sample"}
    comps = enumerate_comparisons(known, factors, strata=["_sex"], min_group=min_group, references=references)
    per_sex = {sx: [c["name"] for c in comps if c["within"].get("_sex") == sx and c["analyzable"]] for sx in sexes}
    return {"split": True, "sexes": sexes, "n_unknown": int((~meta["_sex"].isin(sexes)).sum()),
            "analyzable_per_sex": per_sex, "comparisons": comps,
            "note": "the pooled analysis follows the paper; per-sex analyses are added as exploratory "
                    "when the paper pooled"}


# ---------------------------------------------------------------------------
# 2.8 The report
# ---------------------------------------------------------------------------

def report(*, case_id: str, matrix_type: str, metadata: pd.DataFrame, factors: Sequence[str],
           matrix_csv: str | Path | None = None, organism: str = "Mouse", subject: str | None = None,
           covariate_candidates: Sequence[str] | None = None, references: dict | None = None,
           planned: Sequence[str] = (), out_dir: str | Path = ".") -> dict:
    """Run every check and write ``suitability.json`` + ``suitability.md`` in ``out_dir``.

    verdict: ``analyzable`` (every check passes), ``partially_analyzable`` (some
    comparisons too small, or a sex mismatch to resolve), ``not_analyzable`` (data type,
    grouping, covariance or sample size fails)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    checks: dict[str, Any] = {"data_type": check_data_type(matrix_type)}
    checks["grouping"] = check_grouping(metadata, factors)
    comps: list[dict] = []
    if checks["grouping"]["status"] == "pass":
        checks["covariance"] = check_covariance(metadata, factors, subject=subject,
                                                candidates=covariate_candidates)
        comps = enumerate_comparisons(metadata, factors, references=references)
        checks["sample_size"] = check_sample_size(comps, planned)
    if matrix_csv is not None:
        checks["sex"] = check_sex(matrix_csv, metadata, organism=organism, out_dir=out_dir)
        if checks["grouping"]["status"] == "pass":
            checks["sex"]["split_plan"] = {k: v for k, v in sex_split_plan(
                metadata, factors, checks["sex"].get("sex_by_sample", {}), references=references).items()
                if k != "comparisons"}
        checks["sex"].pop("sex_by_sample", None)
    hard = [k for k in ("data_type", "grouping", "covariance", "sample_size")
            if checks.get(k, {}).get("status") == "fail"]
    soft = [k for k, v in checks.items() if v.get("status") in ("partial", "mismatch")]
    verdict = "not_analyzable" if hard else ("partially_analyzable" if soft else "analyzable")
    result = {"case_id": case_id, "verdict": verdict, "failed": hard, "warnings": soft,
              "factors": list(factors), "checks": checks, "comparisons": comps}
    (out_dir / "suitability.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str),
                                              encoding="utf-8")
    (out_dir / "suitability.md").write_text(to_markdown(result), encoding="utf-8")
    return result


def to_markdown(r: dict) -> str:
    c = r["checks"]
    lines = [f"# Suitability: {r['case_id']}", "", f"Verdict: **{r['verdict']}**"
             + (f" (failed: {', '.join(r['failed'])})" if r["failed"] else "")
             + (f"; check: {', '.join(r['warnings'])}" if r["warnings"] else ""), "",
             "| Check | Status | Detail |", "|---|---|---|"]
    dt = c["data_type"]
    lines.append(f"| Data type | {dt['status']} | {dt['matrix_type']}; route: {dt.get('route') or dt.get('reason')} |")
    g = c["grouping"]
    lines.append(f"| Grouping | {g['status']} | " + ("; ".join(g["problems"]) or
                 "; ".join(f"{f}: {len(v)} levels" for f, v in g["levels"].items())) + " |")
    if "covariance" in c:
        cv = c["covariance"]
        detail = "; ".join(f"{d['column']}: {d['decision']} ({d['reason']})" for d in cv["decisions"]) or "no candidates"
        lines.append(f"| Covariance | {cv['status']} | {cv['covariance_status']}; {detail} |")
    if "sample_size" in c:
        ss = c["sample_size"]
        unknown = f"; planned names not found: {', '.join(ss['unknown_planned'])}" if ss.get("unknown_planned") else ""
        lines.append(f"| Sample size | {ss['status']} | {ss['n_analyzable']}/{ss['n_comparisons']} comparisons "
                     f"have >= {MIN_GROUP} per group{unknown} |")
    if "sex" in c:
        sx = c["sex"]
        split = sx.get("split_plan", {})
        detail = sx.get("summary", "")
        if sx.get("mismatched"):
            detail += f"; mismatch: {', '.join(sx['mismatched'][:6])}"
        if split:
            detail += "; per-sex analysis: " + ("yes" if split.get("split") else f"no ({split.get('reason')})")
        lines.append(f"| Sex | {sx['status']} | {detail} |")
    req = dt.get("required", {})
    if req.get("files"):
        lines.append(f"| Required data | - | files: {'; '.join(req['files'])}. fields: {'; '.join(req['fields'])} |")
    if r["comparisons"]:
        lines += ["", "## Comparisons", "", "| Comparison | Kind | Cells (n) | Analyzable |", "|---|---|---|---|"]
        for comp in r["comparisons"]:
            cells = ", ".join("/".join(map(str, x["cell"].values())) + f" ({x['n']})" for x in comp["cells"])
            lines.append(f"| {comp['name']} | {comp['kind']} | {cells} | {'yes' if comp['analyzable'] else 'no'} |")
    return "\n".join(lines) + "\n"
