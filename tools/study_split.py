"""Split ONE GSE into multiple per-condition 'study' records + enumerate the pairwise group
comparisons between them (user direction 2026-06-23: "把 0周/2周/4周/8周 拆成多条 study").

Why this is sound: every condition's samples come from the SAME GSE (same platform / library prep /
processing), so a DEG between any two conditions just re-pools those two conditions' samples into one
matrix — statistically identical to the current within-study contrast. Splitting into studies is a
RELABELING of the relational model, not a change to what is comparable. Each split study carries
`source_gse` so the provenance (all came from one paper/GSE) is preserved; a comparison between two
split studies is a CROSS-study analysis (its two group arms live in two different study records).

Deterministic, zero LLM: the design column is chosen by metadata_structural._pick_design_column and
the split/pairing is a pure function of the metadata CSV.
"""
import os
import re
import itertools
from typing import Optional

import pandas as pd

from tools.metadata_structural import _pick_design_column
from tools.sea_cdm_schema import csv_columns


def _slug(s: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(s).lower())).strip("_")[:40] or "cond"


def _is_baseline(level: str, control_keywords) -> bool:
    lv = str(level).lower()
    ck = [k.lower() for k in (control_keywords or [])]
    # whole-word-ish baseline markers + the caller's control keywords
    base_markers = ("pre", "baseline", "control", "sedentary", "sham", "rest", "untreated",
                    "vehicle", "wt", "wildtype", "day0", "week0", "0w", "0wk", "t0", "naive")
    return any(k and k in lv for k in ck) or any(b in lv for b in base_markers)


def _level_order_key(level: str):
    """Order conditions sensibly: pull the first number (2 'week', 24 'h') so 0<2<4<8 / pre<post.
    Baseline-ish levels sort first. Falls back to the string."""
    lv = str(level).lower()
    base = 0 if _is_baseline(lv, []) else 1
    m = re.search(r"(\d+(?:\.\d+)?)", lv)
    num = float(m.group(1)) if m else float("inf")
    return (base, num, lv)


def split_into_studies(gse: str, metadata_csv: str, control_keywords=None,
                       design_column: Optional[str] = None, max_pairs: Optional[int] = None,
                       pairing: str = "all") -> dict:
    """Return {design_column, levels, studies, comparisons, note}.

    studies     : one dict per design-column level — study_id=f'{gse}__{slug(level)}', source_gse=gse,
                  condition, is_baseline, n_samples, sample_ids.
    comparisons : list of {treatment_study, control_study, treatment, control, label, both_arms_n}
                  one per pair. `pairing`='all' => every C(n,2) pair; 'baseline' => each non-baseline
                  vs the baseline; 'baseline+adjacent' => baseline pairs + consecutive-ordered pairs.
                  Orientation: a baseline level is always the control; otherwise the later-ordered
                  level is the treatment (deterministic via _level_order_key).
    """
    out = {"design_column": None, "levels": [], "studies": [], "comparisons": [], "note": ""}
    try:
        df = pd.read_csv(metadata_csv, index_col=0, dtype=str, keep_default_na=False)
    except Exception as e:
        out["note"] = f"metadata unreadable: {e}"
        return out
    col = design_column or _pick_design_column(df, exclude=set())
    if not col or col not in df.columns:
        out["note"] = "no design column -> single study (nothing to split)"
        return out
    out["design_column"] = col

    series = df[col].astype(str)
    levels = [lv for lv in series.unique().tolist() if lv.strip()]
    levels = sorted(levels, key=_level_order_key)
    out["levels"] = levels
    if len(levels) < 2:
        out["note"] = "design column has <2 levels -> single study"
        return out

    for lv in levels:
        ids = series.index[series == lv].astype(str).tolist()
        out["studies"].append({
            "study_id": f"{gse}__{_slug(lv)}", "source_gse": gse, "design_column": col,
            "condition": lv, "is_baseline": _is_baseline(lv, control_keywords),
            "n_samples": len(ids), "sample_ids": ids,
        })

    n_by_level = {s["condition"]: s["n_samples"] for s in out["studies"]}
    sid_by_level = {s["condition"]: s["study_id"] for s in out["studies"]}

    def _orient(a, b):
        """Return (treatment_level, control_level): baseline is control; else later-ordered = treatment."""
        a_base, b_base = _is_baseline(a, control_keywords), _is_baseline(b, control_keywords)
        if a_base and not b_base:
            return b, a
        if b_base and not a_base:
            return a, b
        return (a, b) if _level_order_key(a) > _level_order_key(b) else (b, a)

    if pairing == "baseline":
        pairs = [(t, c) for c in levels if _is_baseline(c, control_keywords)
                 for t in levels if t != c and not _is_baseline(t, control_keywords)]
    elif pairing == "baseline+adjacent":
        baseline = next((lv for lv in levels if _is_baseline(lv, control_keywords)), None)
        pairs = [_orient(t, baseline) for t in levels if baseline and t != baseline]
        pairs += [_orient(levels[i], levels[i + 1]) for i in range(len(levels) - 1)]
    else:  # all pairwise
        pairs = [_orient(a, b) for a, b in itertools.combinations(levels, 2)]

    seen = set()
    for treat, ctrl in pairs:
        key = (treat, ctrl)
        if key in seen or treat == ctrl:
            continue
        seen.add(key)
        out["comparisons"].append({
            "treatment_study": sid_by_level[treat], "control_study": sid_by_level[ctrl],
            "treatment": treat, "control": ctrl,
            "label": f"{treat} vs {ctrl}",
            "both_arms_n": n_by_level[treat] + n_by_level[ctrl],
        })
    if max_pairs and len(out["comparisons"]) > max_pairs:
        out["note"] = f"capped {len(out['comparisons'])} -> {max_pairs} comparisons"
        out["comparisons"] = out["comparisons"][:max_pairs]
    return out


# --- the descriptive study fields a split record INHERITS from its parent GSE's study row ---
_INHERIT_FIELDS = ("study_description", "study_description_source", "study_type", "study_type_source",
                   "study_focus", "study_focus_source", "study_keywords", "study_keywords_source",
                   "comments", "comments_source")


def build_split_study_rows(plan: dict, parent_study_row: Optional[dict] = None) -> list:
    """One schema-conformant `study` row per split condition. The descriptive fields
    (description / type / focus / keywords / comments + their _source) are INHERITED from the
    parent GSE's study row (user direction); study_id / study_name / source_gse are set per-split."""
    cols = csv_columns("study")
    parent = parent_study_row or {}
    rows = []
    for s in plan["studies"]:
        row = {c: None for c in cols}
        for f in _INHERIT_FIELDS:                       # inherit the descriptive text from the parent
            row[f] = parent.get(f)
        row.update({
            "study_id": s["study_id"],
            "reference_source": parent.get("reference_source") or "GEO",
            "reference_source_id": s["source_gse"],
            "source_gse": s["source_gse"],
            "study_name": s["condition"],
            "study_name_source": f"GEO metadata: {s['design_column']}",
        })
        rows.append(row)
    return rows


def split_and_compare(gse: str, counts_csv: str, design_metadata_csv: str, out_dir: str,
                      split_metadata_csv: Optional[str] = None, parent_study_row: Optional[dict] = None,
                      control_keywords=None, design_column: Optional[str] = None,
                      pairing: str = "all", max_pairs: Optional[int] = None, report: Optional[dict] = None) -> dict:
    """End-to-end per-condition study split + cross-study pairwise DESeq2, reusable from the cohort.

    counts_csv          : the raw-counts matrix.
    design_metadata_csv : metadata whose index matches the counts columns (the ALIGNED metadata) —
                          used to RUN each pairwise DESeq2.
    split_metadata_csv  : metadata to derive the split plan from (defaults to design_metadata_csv).
    parent_study_row    : the parent GSE's study row (dict) whose descriptive fields are inherited.

    Writes <out_dir>/study_split.csv (split study rows) + cross_study_comparisons.csv, and one
    DEG_results_<treat>_vs_<ctrl>.csv per pair. Returns {design_column, studies, comparisons}."""
    from tools.deseq2_tools import run_deseq2_analysis, deg_filename   # lazy: avoid import cycle
    os.makedirs(out_dir, exist_ok=True)
    plan = split_into_studies(gse, split_metadata_csv or design_metadata_csv,
                              control_keywords=control_keywords, design_column=design_column,
                              pairing=pairing, max_pairs=max_pairs)
    col = plan["design_column"]
    if not col or len(plan["studies"]) < 2:
        if report is not None:
            report["note"] = plan["note"] or "single-condition study; nothing to split"
        return plan

    # 1) split `study` rows (inherit descriptive fields from the parent GSE study row)
    study_rows = build_split_study_rows(plan, parent_study_row)
    pd.DataFrame(study_rows, columns=csv_columns("study")).to_csv(
        os.path.join(out_dir, "study_split.csv"), index=False)

    # 2) one real DESeq2 per pairwise comparison + a cross-study comparison row
    comp_rows = []
    for c in plan["comparisons"]:
        msg = run_deseq2_analysis.invoke({
            "counts_csv": counts_csv, "metadata_csv": design_metadata_csv, "design_column": col,
            "control_group": c["control"], "treatment_group": c["treatment"], "output_dir": out_dir,
        })
        deg_path = os.path.join(out_dir, deg_filename(c["treatment"], c["control"]))
        n_deg = n_tested = None
        if os.path.isfile(deg_path):
            d = pd.read_csv(deg_path, index_col=0)
            n_tested = int(d["padj"].notna().sum())
            n_deg = int((d["padj"] < 0.05).sum())
        comp_rows.append({
            "contrast_label": c["label"], "treatment_study": c["treatment_study"],
            "control_study": c["control_study"], "both_arms_n": c["both_arms_n"],
            "n_tested": n_tested, "n_deg": n_deg,
            "status": "ok" if n_deg is not None else f"FAILED: {(msg or '').splitlines()[0][:80]}",
        })
    pd.DataFrame(comp_rows).to_csv(os.path.join(out_dir, "cross_study_comparisons.csv"), index=False)

    if report is not None:
        report.update({"design_column": col, "n_studies": len(study_rows),
                       "n_comparisons": len(comp_rows),
                       "n_ok": sum(1 for r in comp_rows if r["n_deg"] is not None)})
    plan["study_rows"] = study_rows
    plan["comparison_rows"] = comp_rows
    return plan
