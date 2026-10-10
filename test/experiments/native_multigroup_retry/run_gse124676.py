"""Native Codex retry for the GSE124676 paired exercise design.

The original paper identifies 21 paired before/after samples and randomized
them to MET or Tai chi.  The GEO description fields use q1/q2 technical names,
but the sample title and paper establish the pairing; the retry records that
evidence explicitly instead of treating the pairing as unknown.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from patsy import dmatrix
from inmoose.limma import lmFit, eBayes, topTable


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "output" / "native_codex_multigroup_retry_20261001_"
INPUT = ROOT / "output" / "native_codex_paper_first_20_20261001_" / "analysis" / "GSE124676"


def fit(expr: pd.DataFrame, meta: pd.DataFrame, formula: str, coef: str, label: str):
    design = dmatrix(formula, meta)
    rank = int(np.linalg.matrix_rank(np.asarray(design, dtype=float)))
    if rank < design.shape[1] or len(meta) - rank < 1:
        raise RuntimeError(f"invalid design rank={rank}/{design.shape[1]} residual_df={len(meta)-rank}")
    fitted = eBayes(lmFit(expr.loc[:, meta.index], design=design))
    if coef not in design.design_info.column_names:
        raise RuntimeError(f"missing coefficient {coef!r}: {list(design.design_info.column_names)}")
    top = pd.DataFrame(topTable(fitted, coef=label, number=expr.shape[0], sort_by="P", adjust_method="fdr_bh"))
    top = top.rename(columns={"adj_pvalue": "padj"})
    return top, {"formula": formula, "coefficient": coef, "n_samples": int(len(meta)),
                 "rank": rank, "residual_df": int(len(meta) - rank),
                 "n_significant_padj_lt_0_05": int((top["padj"] < 0.05).sum())}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    expr = pd.read_csv(INPUT / "log2_fpkm.csv", index_col=0)
    meta = pd.read_csv(INPUT / "metadata.csv", index_col=0)
    meta = meta.loc[expr.columns].copy()
    meta["time"] = meta.index.to_series().map(lambda x: "before" if str(x).startswith("q1_") else "after").to_numpy()
    meta["subject"] = meta.index.to_series().map(lambda x: str(x).split("_", 1)[1]).to_numpy()
    meta["exercise"] = meta["characteristics_ch1.1.exercise"].astype(str).to_numpy()
    expr = expr.apply(pd.to_numeric, errors="coerce")
    expr = expr.loc[expr.notna().sum(axis=1) >= 20]
    expr = expr.loc[expr.var(axis=1, skipna=True) > 0]

    records = []
    outputs = []
    for scope, sub in [("all", meta), ("MET", meta[meta.exercise == "MET"]), ("Tai_chi", meta[meta.exercise == "Tai chi"])]:
        top, rec = fit(expr, sub, "~ C(time) + C(subject)", "C(time)[T.before]", "C(time)[T.before]")
        # With alphabetical coding, after is the reference and before is the coefficient;
        # report the sign convention explicitly as before relative to after.
        out = RUN / f"GSE124676_{scope}_before_vs_after_paired.csv"
        top.to_csv(out)
        rec.update({"scope": "paired_time", "stratum": scope, "comparison": "before vs after",
                    "artifact": str(out)})
        records.append(rec)

    # Difference in paired changes: does the exercise modality change the response?
    pairs = []
    for subject, rows in meta.groupby("subject"):
        if set(rows["time"]) != {"before", "after"}:
            continue
        before = rows.index[rows.time == "before"][0]
        after = rows.index[rows.time == "after"][0]
        pairs.append({"subject": subject, "before": before, "after": after,
                      "exercise": rows.iloc[0]["exercise"]})
    delta_meta = pd.DataFrame(pairs).set_index("subject")
    delta_expr = pd.DataFrame({p["subject"]: expr[p["after"]] - expr[p["before"]] for p in pairs})
    top, rec = fit(delta_expr, delta_meta, "~ C(exercise)", "C(exercise)[T.Tai chi]", "C(exercise)[T.Tai chi]")
    out = RUN / "GSE124676_change_after_minus_before_Tai_chi_vs_MET.csv"
    top.to_csv(out)
    rec.update({"scope": "difference_in_differences", "comparison": "change after-before: Tai chi vs MET",
                "complete_pairs": int(len(delta_meta)), "artifact": str(out)})
    records.append(rec)

    report = {"accession": "GSE124676", "pairing_evidence": {
        "paper": "21 PD patients randomized to MET or Tai chi; blood collected before and after 12 weeks",
        "geo_id_rule": "q1_<id> before paired with q2_<id> after",
        "complete_pairs": int(len(delta_meta)),
    }, "records": records,
              "note": "Paper-grounded paired reanalysis; no unpaired pooled before/after analysis."}
    (RUN / "GSE124676_plan_and_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
