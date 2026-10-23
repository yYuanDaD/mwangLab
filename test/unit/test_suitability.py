"""Pre-analysis suitability checks (tools/suitability.py) and joint-model contrasts
(tools/joint_contrasts.py) — synthetic data, NO LLM, NO network.

Run:  python test/unit/test_suitability.py
"""

import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import numpy as np
import pandas as pd

from tools import joint_contrasts as jc
from tools import suitability as su


def _design(n=3):
    """2 (sed/ex) x 2 (wt/ko) x n animals, half male, half female per cell."""
    rows = []
    for grp in ("sed", "ex"):
        for gen in ("WT", "KO"):
            for i in range(2 * n):
                rows.append({"sample": f"{grp}_{gen}_{i}", "grp": grp, "geno": gen,
                             "sex": "male" if i % 2 == 0 else "female", "batch": f"b{i % 2}"})
    return pd.DataFrame(rows).set_index("sample")


def _counts(meta, seed=0, de_gene_fc=4.0):
    rng = np.random.default_rng(seed)
    genes = [f"G{i}" for i in range(300)] + ["Xist", "Ddx3y", "Uty", "Kdm5d"]
    base = rng.gamma(2.0, 100.0, size=len(genes))
    mat = {}
    for s, r in meta.iterrows():
        mu = base.copy()
        if r["grp"] == "ex":
            mu[0] *= de_gene_fc
        male = r["sex"] == "male"
        mu[-4] = 1 if male else 3000
        mu[-3:] = 800 if male else 1
        mat[s] = rng.negative_binomial(10, 10 / (10 + mu))
    return pd.DataFrame(mat, index=genes)


def test_reference_and_time_order():
    assert su.reference_level(["exercise", "sedentary"]) == "sedentary"
    assert su.reference_level(["Base", "IP", "IP120"]) == "Base"
    assert su.reference_level(["A", "B"]) is None
    assert su._time_order(["24h", "0h", "3h"]) == ["0h", "3h", "24h"]


def test_enumerate_comparisons_factorial():
    meta = _design()
    comps = su.enumerate_comparisons(meta, ["grp", "geno"], references={"geno": "WT"})
    simple = [c for c in comps if c["kind"] == "simple"]
    inter = [c for c in comps if c["kind"] == "interaction"]
    # ex vs sed within WT and within KO; KO vs WT within sed and within ex; one interaction
    assert len(simple) == 4 and len(inter) == 1, [c["name"] for c in comps]
    assert {(c["test"], c["reference"], tuple(c["within"].values())) for c in simple if c["factor"] == "grp"} == \
        {("ex", "sed", ("WT",)), ("ex", "sed", ("KO",))}
    assert inter[0]["test"] == "ex:KO" and inter[0]["reference"] == "sed:WT"
    assert all(c["analyzable"] for c in comps)


def test_enumerate_comparisons_time_series_all_pairs():
    meta = pd.DataFrame({"t": ["Base"] * 4 + ["IP"] * 4 + ["IP120"] * 4}, index=[f"s{i}" for i in range(12)])
    comps = su.enumerate_comparisons(meta, ["t"])
    assert {(c["test"], c["reference"]) for c in comps} == {("IP", "Base"), ("IP120", "Base"), ("IP120", "IP")}, comps


def test_sample_size_and_grouping():
    meta = _design(n=1)   # 2 per cell
    comps = su.enumerate_comparisons(meta, ["grp", "geno"])
    ss = su.check_sample_size(comps)
    assert ss["status"] == "fail" and ss["n_analyzable"] == 0, ss
    meta.loc[meta.index[0], "grp"] = ""
    g = su.check_grouping(meta, ["grp", "geno"])
    assert g["status"] == "fail" and "without a value" in g["problems"][0], g
    assert su.check_grouping(meta, ["missing"])["status"] == "fail"


def test_covariance_decisions():
    meta = _design()
    cv = su.check_covariance(meta, ["grp", "geno"], candidates=["batch"])
    assert cv["status"] == "pass" and cv["covariates"] == ["batch"], cv
    meta["run"] = meta["grp"]   # sequencing run aliased with the exercise arm (GSE297318)
    cv = su.check_covariance(meta, ["grp"], candidates=["run"])
    assert cv["status"] == "fail" and cv["stopping_columns"] == ["run"], cv
    # Paired: each subject sampled pre and post.
    paired = pd.DataFrame({"time": ["pre", "post"] * 4, "subject": [f"p{i // 2}" for i in range(8)]},
                          index=[f"s{i}" for i in range(8)])
    cv = su.check_covariance(paired, ["time"])
    assert cv["blocking_terms"] == ["subject"] and cv["covariance_status"] == "required", cv


def test_sex_check_and_split():
    meta = _design()
    counts = _counts(meta)
    swapped = meta.index[0]               # labelled male, expressed as female
    counts.loc[["Xist", "Ddx3y", "Uty", "Kdm5d"], swapped] = [3000, 0, 0, 0]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "counts.csv")
        counts.to_csv(path)
        sx = su.check_sex(path, meta, out_dir=d)
        assert sx["status"] == "mismatch" and sx["mismatched"] == [swapped], sx
        plan = su.sex_split_plan(meta, ["grp"], sx["sex_by_sample"])
        assert plan["split"] and plan["analyzable_per_sex"]["male"] and plan["analyzable_per_sex"]["female"], plan
        one = su.sex_split_plan(meta, ["grp"], {s: "male" for s in meta.index})
        assert not one["split"] and one["reason"] == "one sex only"


def test_report_and_markdown():
    meta = _design()
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "counts.csv")
        _counts(meta).to_csv(path)
        r = su.report(case_id="toy", matrix_type="raw_counts", metadata=meta, factors=["grp", "geno"],
                      matrix_csv=path, covariate_candidates=["batch"], out_dir=d)
        assert r["verdict"] == "analyzable", (r["failed"], r["warnings"])
        md = open(os.path.join(d, "suitability.md"), encoding="utf-8").read()
        assert "Verdict: **analyzable**" in md and "interaction" in md and "per-sex analysis: yes" in md
        saved = json.load(open(os.path.join(d, "suitability.json"), encoding="utf-8"))
        assert saved["checks"]["covariance"]["covariates"] == ["batch"]
        bad = su.report(case_id="toy", matrix_type="ambiguous", metadata=meta, factors=["grp"], out_dir=d)
        assert bad["verdict"] == "not_analyzable" and bad["failed"] == ["data_type"]
    assert su.required_data("FPKM")["key"] == "bulk_rnaseq_normalized"


def test_joint_deseq2_uses_every_sample():
    meta = _design()
    counts = _counts(meta)
    comps = su.enumerate_comparisons(meta, ["grp", "geno"], references={"geno": "WT"})
    with tempfile.TemporaryDirectory() as d:
        cpath, mpath = os.path.join(d, "counts.csv"), os.path.join(d, "meta.csv")
        counts.to_csv(cpath)
        meta.to_csv(mpath)
        out = jc.run_joint_deseq2(cpath, mpath, comps, d, n_cpus=1)
        assert out["n_samples"] == 24 and len(out["results"]) == 5, out
        ex = next(r for r in out["results"] if r["name"].startswith("grp_ex_vs_sed_geno-WT"))
        res = pd.read_csv(ex["path"], index_col=0)
        assert res.loc["G0", "padj"] < 1e-3 and 1.5 < res.loc["G0", "log2FoldChange"] < 2.5, res.loc["G0"]
        inter = next(r for r in out["results"] if r["kind"] == "interaction")
        res = pd.read_csv(inter["path"], index_col=0)
        assert abs(res.loc["G0", "log2FoldChange"]) < 0.7, res.loc["G0"]   # same effect in WT and KO


def test_joint_limma():
    meta = _design()
    logm = np.log2(_counts(meta) + 1)
    comps = su.enumerate_comparisons(meta, ["grp"])
    with tempfile.TemporaryDirectory() as d:
        epath, mpath = os.path.join(d, "log.csv"), os.path.join(d, "meta.csv")
        logm.to_csv(epath)
        meta.to_csv(mpath)
        out = jc.run_joint_limma(epath, mpath, comps, d, covariates=["sex"])
        assert out["n_samples"] == 24 and out["n_contrasts"] == 1, out
        res = pd.read_csv(out["results"][0]["path"], index_col=0)
        assert res.loc["G0", "padj"] < 1e-3, res.loc["G0"]


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__}: {str(e)[:600]}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
