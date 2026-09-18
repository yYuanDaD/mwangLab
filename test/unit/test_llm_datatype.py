"""Tests for req #1 — LLM-determined data type → DA route (tools/llm_helpers.classify_matrix_with_llm
and the batch_tools integration helpers).

The deterministic parts run with NO network:
  - _matrix_stats_preview  (numeric profile the classifier reasons over)
  - _mvalue_transform_matrix  (methylation β→M pre-transform that normalizes methylation onto the
                               existing log/limma route)
  - _apply_llm_matrix_type  (vocab → pipeline route mapping)
  - _llm_datatype_decision  (the cost gate: raw counts skip by default; strict mode forces semantic review)
  - _gather_matrix_candidates  (excludes the *_mvalue.csv artifact)

A final LIVE test calls the real LLM only if CLAUDE_API_KEY is set (skipped otherwise).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_llm_datatype.py
"""
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np
import pandas as pd

from tools.batch_tools import (
    _matrix_stats_preview, _mvalue_transform_matrix, _apply_llm_matrix_type,
    _round_estimated_counts_matrix, _provenance_authorizes_rounding,
    _llm_datatype_decision, _gather_matrix_candidates, _classify_matrix,
)
from tools import batch_tools
from tools.llm_helpers import MatrixTypeClassification, classify_matrix_with_llm

_TMP = tempfile.mkdtemp(prefix="datatype_test_")


def _write(name, df):
    p = os.path.join(_TMP, name)
    df.to_csv(p, index=True)
    return p


def _raw_counts_csv():
    rng = np.random.default_rng(0)
    df = pd.DataFrame(rng.integers(0, 5000, size=(50, 6)),
                      index=[f"Gene{i}" for i in range(50)],
                      columns=[f"S{j}" for j in range(6)])
    return _write("raw_counts.csv", df)


def _beta_csv(name="GSE0_methylation_beta.csv"):
    rng = np.random.default_rng(1)
    # per-site baseline so sites actually vary (not a degenerate all-0.5 matrix)
    base = rng.uniform(0.05, 0.95, size=(40, 1))
    noise = rng.normal(0, 0.03, size=(40, 6))
    beta = np.clip(base + noise, 0.001, 0.999)
    df = pd.DataFrame(beta, index=[f"cg{i:07d}" for i in range(40)],
                      columns=[f"S{j}" for j in range(6)])
    return _write(name, df)


def _fpkm_csv():
    rng = np.random.default_rng(2)
    df = pd.DataFrame(rng.gamma(2.0, 800.0, size=(50, 6)).round(3),
                      index=[f"Gene{i}" for i in range(50)],
                      columns=[f"S{j}" for j in range(6)])
    return _write("fpkm.csv", df)


def test_stats_preview():
    raw = _raw_counts_csv()
    stats, preview = _matrix_stats_preview(raw)
    assert stats is not None and preview
    assert stats["frac_integer_of_nonzero"] == 1.0, stats
    assert stats["frac_negative"] == 0.0
    assert stats["max"] > 100
    assert stats["row_id_examples"][0].startswith("Gene")

    beta = _beta_csv()
    bstats, _ = _matrix_stats_preview(beta)
    assert bstats["frac_in_0_1"] >= 0.99, bstats
    assert bstats["max"] <= 1.001
    assert bstats["row_id_examples"][0].startswith("cg")
    print("  [ok] _matrix_stats_preview: raw counts integer-heavy, β in [0,1]")


def test_mvalue_transform():
    beta = _beta_csv("beta_for_mvalue.csv")
    mv_path = _mvalue_transform_matrix(beta)
    assert os.path.exists(mv_path) and mv_path.endswith("_mvalue.csv")
    mv = pd.read_csv(mv_path, index_col=0)
    assert np.isfinite(mv.to_numpy()).all(), "M-values must be finite"
    # monotone: β>0.5 -> M>0, β<0.5 -> M<0
    b = pd.read_csv(beta, index_col=0)
    bmean, mmean = b.mean(axis=1), mv.mean(axis=1)
    hi, lo = bmean.idxmax(), bmean.idxmin()
    assert mmean[hi] > 0 and mmean[lo] < 0, (mmean[hi], mmean[lo])
    # idempotent
    assert _mvalue_transform_matrix(beta) == mv_path
    print("  [ok] _mvalue_transform_matrix: finite M, sign tracks β, idempotent")


def test_apply_mapping():
    raw = _raw_counts_csv()

    def cls(t, log=False):
        return MatrixTypeClassification(matrix_type=t, already_log_scale=log,
                                        confidence="high", reasoning="test")

    _, mt, _ = _apply_llm_matrix_type(cls("raw_counts"), raw)
    assert mt == "raw_counts"
    try:
        _apply_llm_matrix_type(cls("estimated_counts"), raw)
    except ValueError as exc:
        assert "estimated_counts_requires_count_workflow" in str(exc)
    else:
        raise AssertionError("estimated counts must never be silently treated as FPKM/TPM")
    # The BO recipe is an explicit reproduction exception: only a documented round→DESeq2 route
    # may convert estimated counts into the integer-count branch.
    rounded_cls = MatrixTypeClassification(
        matrix_type="estimated_counts", already_log_scale=False, confidence="high",
        reasoning="explicit recipe", recommended_route="deseq2_after_rounding")
    rounded_path, rounded_type, rounded_note = _apply_llm_matrix_type(
        rounded_cls, raw, provenance="DESeq2 reads this matrix and round(count_matrix) before DESeq2")
    assert rounded_type == "raw_counts" and rounded_path.endswith("_rounded_counts.csv")
    assert "rounded-count route" in rounded_note
    rounded = pd.read_csv(rounded_path, index_col=0)
    assert np.issubdtype(rounded.to_numpy().dtype, np.integer)
    assert _provenance_authorizes_rounding("DESeq2 reads rawcount and round(count_matrix)")
    assert not _provenance_authorizes_rounding("round(cpm_matrix) for a limma-only report")
    _, mt, _ = _apply_llm_matrix_type(cls("fpkm_or_tpm"), raw)
    assert mt == "fpkm_or_tpm"
    _, mt, _ = _apply_llm_matrix_type(cls("log_transformed"), raw)
    assert mt == "log_transformed"
    _, mt, _ = _apply_llm_matrix_type(cls("proteomics_intensity", log=True), raw)
    assert mt == "log_transformed"
    _, mt, _ = _apply_llm_matrix_type(cls("proteomics_intensity", log=False), raw)
    assert mt == "fpkm_or_tpm"
    _, mt, _ = _apply_llm_matrix_type(cls("ambiguous"), raw)
    assert mt is None, "ambiguous must map to None (keep heuristic)"

    beta = _beta_csv("beta_apply.csv")
    new_path, mt, note = _apply_llm_matrix_type(cls("methylation_beta"), beta)
    assert mt == "log_transformed" and new_path.endswith("_mvalue.csv"), (mt, new_path)
    assert "M-value" in note or "M-values" in note
    print("  [ok] _apply_llm_matrix_type: estimated counts + all other vocab routes; methylation pre-transforms")


def test_cost_gate(monkeypatch_calls=None):
    """raw_counts heuristic must SKIP the LLM (cost gate); decimal/methyl must fire it."""
    calls = {"n": 0}

    def _spy(**kwargs):
        calls["n"] += 1
        return None  # simulate unavailable → caller keeps heuristic

    orig = batch_tools.classify_matrix_with_llm
    batch_tools.classify_matrix_with_llm = _spy
    try:
        raw = _raw_counts_csv()
        res = _llm_datatype_decision(raw, "raw_counts", platform_hint="", organism="Mouse")
        assert res is None and calls["n"] == 0, "raw_counts must NOT call the LLM"

        fpkm = _fpkm_csv()
        _llm_datatype_decision(fpkm, "fpkm_or_tpm", platform_hint="", organism="Mouse")
        assert calls["n"] == 1, "decimal matrix must call the LLM once"

        # special-hint fires even if heuristic looked 'log_transformed'
        beta = _beta_csv("beta_gate.csv")
        _llm_datatype_decision(beta, "log_transformed",
                               platform_hint="platform_id=GPL21145 Illumina EPIC methylation",
                               organism="Human")
        assert calls["n"] == 2, "methylation hint must call the LLM"
        _llm_datatype_decision(raw, "raw_counts", platform_hint="normalized TPM", organism="Mouse")
        assert calls["n"] == 3, "integer appearance must not override normalization provenance"
        _llm_datatype_decision(raw, "raw_counts", platform_hint="", organism="Mouse", force=True)
        assert calls["n"] == 4, "strict benchmark mode must review integer-looking matrices"
    finally:
        batch_tools.classify_matrix_with_llm = orig
    print("  [ok] cost gate: raw counts skip LLM; decimals & methyl hints fire it")


def test_candidate_excludes_mvalue():
    d = tempfile.mkdtemp(prefix="cand_")
    pd.DataFrame(np.ones((3, 3))).to_csv(os.path.join(d, "GSE_counts.csv"))
    pd.DataFrame(np.ones((3, 3))).to_csv(os.path.join(d, "GSE_counts_mvalue.csv"))
    cands = _gather_matrix_candidates(d)
    names = [os.path.basename(c) for c in cands]
    assert "GSE_counts.csv" in names
    assert "GSE_counts_mvalue.csv" not in names, "the M-value artifact must be excluded"
    print("  [ok] _gather_matrix_candidates excludes *_mvalue.csv artifact")


def test_candidate_excludes_meta_prefix():
    d = tempfile.mkdtemp(prefix="cand_meta_")
    pd.DataFrame(np.ones((3, 3))).to_csv(os.path.join(d, "meta_wt.csv"))
    pd.DataFrame(np.ones((3, 3))).to_csv(os.path.join(d, "GSE_log2fpkm.csv"))
    names = [os.path.basename(c) for c in _gather_matrix_candidates(d)]
    assert "meta_wt.csv" not in names, "meta_ design helpers must not compete as expression"
    assert "GSE_log2fpkm.csv" in names
    print("  [ok] _gather_matrix_candidates excludes meta_* design helpers")


def test_live_classify():
    if not os.getenv("CLAUDE_API_KEY"):
        print("  [skip] live classify — CLAUDE_API_KEY not set")
        return
    beta = _beta_csv("live_beta.csv")
    stats, preview = _matrix_stats_preview(beta)
    res = classify_matrix_with_llm(
        filename="GSE12345_EPIC_methylation_beta.csv",
        platform="platform_id=GPL21145; instrument_model=Illumina Infinium MethylationEPIC",
        value_stats=stats, preview_text=preview, heuristic_label="log_transformed", organism="Human")
    assert res is not None, "live call returned None"
    print(f"  [live] β matrix → {res.matrix_type} ({res.confidence}): {res.reasoning}")
    assert res.matrix_type == "methylation_beta", f"expected methylation_beta, got {res.matrix_type}"

    raw = _raw_counts_csv()
    stats, preview = _matrix_stats_preview(raw)
    res2 = classify_matrix_with_llm(
        filename="GSE9_raw_counts.csv", platform="library_strategy=RNA-Seq",
        value_stats=stats, preview_text=preview, heuristic_label="raw_counts", organism="Mouse")
    print(f"  [live] raw matrix → {res2.matrix_type} ({res2.confidence})")
    assert res2.matrix_type == "raw_counts"
    print("  [ok] live classify: methylation β and raw counts both correct")


if __name__ == "__main__":
    test_stats_preview()
    test_mvalue_transform()
    test_apply_mapping()
    test_cost_gate()
    test_candidate_excludes_mvalue()
    test_candidate_excludes_meta_prefix()
    test_live_classify()
    print("\nALL TESTS PASSED.")
