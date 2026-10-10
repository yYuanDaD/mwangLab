"""Native Codex retry for the GSE128078 longitudinal design.

This is a reproducible evaluation script, not a replacement for the batch
pipeline.  It keeps disease and time separate, uses subject blocking for
within-group time contrasts, and runs cross-sectional disease contrasts at
each timepoint.  It intentionally does not pool repeated samples as if they
were independent.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from patsy import dmatrix
from inmoose.limma import lmFit, eBayes, topTable


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "output" / "native_codex_multigroup_retry_20261001_"
INPUT = ROOT / "output" / "native_codex_paper_first_20_20261001_" / "input" / "GSE128078"


def _fit(expr: pd.DataFrame, meta: pd.DataFrame, formula: str, contrast: str, label: str):
    # Keep patsy.DesignMatrix so inmoose preserves coefficient names.
    design = dmatrix(formula, meta)
    rank = int(np.linalg.matrix_rank(np.asarray(design, dtype=float)))
    if rank < design.shape[1]:
        raise RuntimeError(f"rank deficient {rank}/{design.shape[1]} for {formula}")
    if len(meta) - rank < 1:
        raise RuntimeError(f"no residual degrees of freedom for {formula}")
    fit = eBayes(lmFit(expr.loc[:, meta.index], design=design))
    if contrast not in design.design_info.column_names:
        raise RuntimeError(f"contrast {contrast!r} not present in design columns {list(design.design_info.column_names)}")
    top = pd.DataFrame(topTable(fit, coef=label, number=expr.shape[0], sort_by="P", adjust_method="fdr_bh"))
    top = top.rename(columns={"adj_pvalue": "padj"})
    n_sig = int((top["padj"] < 0.05).sum()) if "padj" in top else 0
    return top, {"formula": formula, "contrast": contrast, "rank": rank,
                 "n_samples": int(len(meta)), "residual_df": int(len(meta) - rank),
                 "n_significant_padj_lt_0_05": n_sig}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    meta = pd.read_csv(INPUT / "GSE128078_metadata.csv", index_col=0)
    meta = meta.rename(columns={
        "characteristics_ch1.1.disease state": "disease",
        "characteristics_ch1.3.timepoint (day)": "time",
        "characteristics_ch1.4.individual identifier": "subject",
    })
    meta["disease"] = meta["disease"].astype(str)
    meta["time"] = meta["time"].astype(str)
    meta["subject"] = meta["subject"].astype(str)
    meta["title"] = meta["title"].astype(str)
    meta = meta.set_index("title", drop=False)

    expr = pd.read_csv(INPUT / "GSE128078_FES_isoforms_FPKM.txt.gz", sep="\t", index_col=0)
    expr = expr.apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="all")
    expr = np.log2(expr.clip(lower=0) + 1.0)
    common = [s for s in expr.columns if s in meta.index]
    expr = expr.loc[:, common]
    meta = meta.loc[common]
    if len(common) != 99:
        raise RuntimeError(f"expected 99 aligned samples, found {len(common)}")

    # Remove genes with no usable variance after alignment.
    expr = expr.loc[expr.notna().sum(axis=1) >= 20]
    expr = expr.loc[expr.var(axis=1, skipna=True) > 0]

    records = []
    outputs = []
    for disease in ["ME/CFS", "Control"]:
        sub = meta[meta["disease"] == disease].copy()
        formula = "~ C(time) + C(subject)"
        for t in ["2", "3", "7"]:
            contrast = f"C(time)[T.{t}]"
            top, rec = _fit(expr, sub, formula, contrast, contrast)
            out = RUN / f"GSE128078_{disease.replace('/', '_')}_day{t}_vs_day1.csv"
            top.to_csv(out)
            rec.update({"scope": "within_disease_time", "disease": disease,
                        "comparison": f"day{t} vs day1", "artifact": str(out)})
            records.append(rec)

    for day in ["1", "2", "3", "7"]:
        sub = meta[meta["time"] == day].copy()
        formula = "~ C(disease)"
        contrast = "C(disease)[T.ME/CFS]"
        top, rec = _fit(expr, sub, formula, contrast, contrast)
        out = RUN / f"GSE128078_ME_CFS_vs_Control_day{day}.csv"
        top.to_csv(out)
        rec.update({"scope": "cross_sectional_disease", "comparison": f"ME/CFS vs Control day{day}",
                    "artifact": str(out)})
        records.append(rec)

    # Difference-in-differences: within-subject change from day 1, then compare
    # those changes between disease groups.  This is the longitudinal analogue
    # of the disease-by-time interaction and uses only complete subject pairs.
    for day in ["2", "3", "7"]:
        delta_cols = []
        delta_rows = []
        for subject, s_meta in meta.groupby("subject"):
            by_time = s_meta.set_index("time")
            if "1" not in by_time.index or day not in by_time.index:
                continue
            base = by_time.loc["1", "title"]
            follow = by_time.loc[day, "title"]
            delta_cols.append(subject)
            delta_rows.append({"subject": subject,
                               "disease": str(by_time.iloc[0]["disease"]),
                               "base": base, "follow": follow})
        delta_meta = pd.DataFrame(delta_rows).set_index("subject")
        delta_expr = pd.DataFrame(
            {row["subject"]: expr[row["follow"]] - expr[row["base"]] for row in delta_rows}
        )
        delta_meta["disease"] = delta_meta["disease"].astype(str)
        top, rec = _fit(delta_expr, delta_meta, "~ C(disease)", "C(disease)[T.ME/CFS]", "C(disease)[T.ME/CFS]")
        out = RUN / f"GSE128078_change_day{day}_vs_day1_ME_CFS_vs_Control.csv"
        top.to_csv(out)
        rec.update({"scope": "difference_in_differences", "comparison": f"change day{day}-day1: ME/CFS vs Control",
                    "complete_subject_pairs": int(len(delta_meta)), "artifact": str(out)})
        records.append(rec)

    report = {
        "accession": "GSE128078",
        "design": {
            "factors": {"disease": ["ME/CFS", "Control"], "time": ["1", "2", "3", "7"]},
            "blocking": "subject",
            "matrix": "FPKM -> log2(x+1)",
            "alignment": "expression title == metadata title",
            "n_samples": len(common),
        },
        "records": records,
        "note": "Planned within-disease time contrasts and per-time disease contrasts; no pooled repeated-sample two-arm analysis.",
    }
    (RUN / "GSE128078_plan_and_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
