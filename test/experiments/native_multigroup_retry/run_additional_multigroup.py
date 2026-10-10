"""Retry additional previously ambiguous studies with explicit multi-level plans."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from patsy import dmatrix
from inmoose.limma import lmFit, eBayes, topTable, contrasts_fit


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "output" / "native_codex_paper_first_20_20261001_" / "analysis"
RUN = ROOT / "output" / "native_codex_multigroup_retry_20261001_"


def fit_contrast(expr: pd.DataFrame, meta: pd.DataFrame, formula: str,
                 vector: dict[str, float], label: str):
    design = dmatrix(formula, meta)
    names = list(design.design_info.column_names)
    missing = [x for x in vector if x not in names]
    if missing:
        raise RuntimeError(f"missing coefficients {missing}; available={names}")
    rank = int(np.linalg.matrix_rank(np.asarray(design, dtype=float)))
    if rank < design.shape[1] or len(meta) - rank < 1:
        raise RuntimeError(f"invalid design rank={rank}/{design.shape[1]} residual_df={len(meta)-rank}")
    fit = lmFit(expr.loc[:, meta.index], design=design)
    c = pd.DataFrame({label: [float(vector.get(n, 0.0)) for n in names]}, index=names)
    cf = eBayes(contrasts_fit(fit, contrasts=c))
    top = pd.DataFrame(topTable(cf, coef=label, number=expr.shape[0], sort_by="P", adjust_method="fdr_bh"))
    top = top.rename(columns={"adj_pvalue": "padj"})
    return top, {"formula": formula, "contrast": label, "n_samples": int(len(meta)),
                 "rank": rank, "residual_df": int(len(meta) - rank),
                 "n_significant_padj_lt_0_05": int((top["padj"] < 0.05).sum())}


def load(acc: str, filename: str):
    d = pd.read_csv(BASE / acc / filename, index_col=0)
    d = d.apply(pd.to_numeric, errors="coerce")
    d = d.loc[d.notna().sum(axis=1) >= max(4, d.shape[1] // 2)]
    d = d.loc[d.var(axis=1, skipna=True) > 0]
    return d


def save(acc, name, top, rec, records):
    out = RUN / f"{acc}_{name}.csv"
    top.to_csv(out)
    rec["artifact"] = str(out)
    records.append(rec)


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    all_records = []

    # Balanced 2x2 genotype x exercise design.
    acc = "GSE207992"
    expr = load(acc, "log2_normcounts.csv")
    meta = pd.read_csv(BASE / acc / "metadata.csv", index_col=0).loc[expr.columns].copy()
    meta["genotype"] = meta["genotype"].astype(str)
    meta["exercise"] = meta["exercise"].astype(str)
    formula = "~ C(genotype)*C(exercise)"
    for name, vector in {
        "WT_vs_KO_at_SVE": {"C(genotype)[T.WT]": 1},
        "nonSVE_vs_SVE_in_KO": {"C(exercise)[T.nonSVE]": 1},
        "interaction_nonSVE_effect_WT_vs_KO": {
            "C(exercise)[T.nonSVE]": 0, "C(genotype)[T.WT]:C(exercise)[T.nonSVE]": 1,
        },
    }.items():
        top, rec = fit_contrast(expr, meta, formula, vector, name)
        rec.update({"design": "genotype x exercise", "cells": {"|".join(map(str, k)): int(v) for k, v in meta.groupby(["genotype", "exercise"]).size().items()}})
        save(acc, name, top, rec, all_records)

    # Paired 2x2 health x time: compare change peak-baseline between health groups.
    acc = "GSE272928"
    expr = load(acc, "transformed_log_expression.csv")
    meta = pd.read_csv(BASE / acc / "metadata.csv", index_col=0).loc[expr.columns].copy()
    meta["subject"] = meta.index.to_series().str.rsplit("_", n=1).str[0].to_numpy()
    meta["health"] = meta["health"].astype(str)
    pairs = []
    for subject, rows in meta.groupby("subject"):
        if set(rows["time"]) != {"baseline", "peak"}:
            continue
        base = rows.index[rows.time == "baseline"][0]
        peak = rows.index[rows.time == "peak"][0]
        pairs.append({"subject": subject, "baseline": base, "peak": peak,
                      "health": rows.iloc[0]["health"]})
    delta_meta = pd.DataFrame(pairs).set_index("subject")
    delta_expr = pd.DataFrame({p["subject"]: expr[p["peak"]] - expr[p["baseline"]] for p in pairs})
    top, rec = fit_contrast(delta_expr, delta_meta, "~ C(health)", {"C(health)[T.CON]": 1}, "CON_vs_ALL_change_peak_minus_baseline")
    rec.update({"design": "health x time with subject pairing", "complete_pairs": int(len(pairs))})
    save(acc, "CON_vs_ALL_change_peak_minus_baseline", top, rec, all_records)

    # Three observed treatment combinations; no unsupported genotype x exercise interaction claimed.
    acc = "GSE205019"
    expr = load(acc, "log2_fpkm.csv")
    meta = pd.read_csv(BASE / acc / "metadata.csv", index_col=0).loc[expr.columns].copy()
    meta["group"] = meta["title"].str.extract(r"^(Control_EV|Exercise_EV|Exercise_AdipoR1)")[0]
    formula = "~ 0 + C(group)"
    names = list(dmatrix(formula, meta).design_info.column_names)
    for name, vector in {
        "Exercise_EV_vs_Control_EV": {"C(group)[Exercise_EV]": 1, "C(group)[Control_EV]": -1},
        "Exercise_AdipoR1_vs_Control_EV": {"C(group)[Exercise_AdipoR1]": 1, "C(group)[Control_EV]": -1},
        "Exercise_AdipoR1_vs_Exercise_EV": {"C(group)[Exercise_AdipoR1]": 1, "C(group)[Exercise_EV]": -1},
    }.items():
        top, rec = fit_contrast(expr, meta, formula, vector, name)
        rec.update({"design": "three observed groups; missing knockdown-control cell",
                    "cells": {str(k): int(v) for k, v in meta["group"].value_counts().items()}})
        save(acc, name, top, rec, all_records)

    # Three-level treatment factor with three biological replicates per level.
    acc = "GSE217155"
    expr = load(acc, "log2_fpkm.csv")
    meta = pd.read_csv(BASE / acc / "metadata.csv", index_col=0).loc[expr.columns].copy()
    meta["treatment"] = meta["characteristics_ch1.4.treatment"].astype(str)
    formula = "~ 0 + C(treatment)"
    for name, vector in {
        "EXE_Ath_vs_Ath": {"C(treatment)[EXE+Ath diet]": 1, "C(treatment)[Ath diet]": -1},
        "Ath_vs_Con": {"C(treatment)[Ath diet]": 1, "C(treatment)[Con]": -1},
    }.items():
        top, rec = fit_contrast(expr, meta, formula, vector, name)
        rec.update({"design": "three-level treatment", "cells": {str(k): int(v) for k, v in meta["treatment"].value_counts().items()}})
        save(acc, name, top, rec, all_records)

    report = {"run": "native_codex_additional_multigroup_retry", "records": all_records,
              "note": "Explicit plans; no pooling of repeated samples and no interaction claimed for missing cells."}
    (RUN / "additional_multigroup_report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
