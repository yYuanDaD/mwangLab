"""Offline tests for tools/case_review.py (review packet, no LLM)."""

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools import case_review  # noqa: E402


def _gse283493_like():
    """48 libraries: 2 depots x 4 groups x letters a-f; the same rat gives one SAT and one VAT."""
    rows = []
    for tissue in ("SAT", "VAT"):
        for grp in ("AM_Cont", "AM_Exp", "PM_Cont", "PM_Exp"):
            for letter in "abcdef":
                lib = f"{tissue}_{grp}_{letter}"
                rows.append({"gsm": f"GSM{len(rows):03d}", "title": f"{tissue} {grp} rep{'abcdef'.index(letter) + 1}",
                             "description": f"Library name: {lib}", "library": lib, "tissue": tissue,
                             "group": grp})
    return pd.DataFrame(rows).set_index("gsm")


def test_pairing_search_prefers_group_plus_letter():
    meta = _gse283493_like()
    cands = case_review.pairing_search(meta)
    by_key = {c["key"]: c for c in cands if c["across"] == "tissue"}
    # the letter alone repeats inside a depot: it cannot be the rat
    assert by_key["suffix of library"]["keys_with_duplicates_in_a_level"] > 0
    stripped = by_key["library without the tissue level"]
    assert stripped["keys_with_duplicates_in_a_level"] == 0
    assert stripped["keys_in_every_level_once"] == 24
    combo = by_key["group (without tissue) + suffix of library"]
    assert combo["keys_in_every_level_once"] == 24
    assert cands[0]["keys_with_duplicates_in_a_level"] == 0 and cands[0]["samples_linked"] == 48


def _write_case(tmp: Path, meta: pd.DataFrame, records: list, design_cols=("tissue", "group")):
    case = tmp / "run" / "CASE1"
    (case / "aligned").mkdir(parents=True)
    meta.to_csv(case / "aligned" / "aligned_metadata.csv")
    meta[list(design_cols)].to_csv(case / "aligned" / "design_metadata.csv")
    (case / "decisions.json").write_text(json.dumps(records), encoding="utf-8")
    return case


def _rec(stage, final, status="valid", stop=""):
    return {"stage": stage, "final": final, "decision_status": status, "execution_status": "not_started",
            "stop_reason": stop, "reasoning": "", "candidates": []}


def test_packet_flags_wrong_pairing_stop_reason():
    meta = _gse283493_like()
    records = [_rec("design", {"design_column": "group", "contrasts": [
                   {"name": "g", "control": "AM_Cont", "treatment": "AM_Exp"}]}),
               _rec("covariance", {"status": "required", "blocking_terms": []}, "manual_review",
                    "SAT and VAT come from the same rats but GEO has no animal ID (replicate letters cannot be "
                    "verified as rats).")]
    with tempfile.TemporaryDirectory() as t:
        case = _write_case(Path(t), meta, records)
        s = case_review.build(case, Path(t) / "review", expr=False)
        names = [f["flag"] for f in s["flags"]]
        assert "pairing_key_candidate" in names
        assert "stop_reason_vs_pairing_search" in names
        assert s["stop_claims"][0]["kinds"] == ["pairing"]
        a = (Path(t) / "review" / "packet_A.md").read_text(encoding="utf-8")
        b = (Path(t) / "review" / "packet_B.md").read_text(encoding="utf-8")
        assert "Candidate pairing keys" in a and "manual_review" in b
        assert "covariance" not in a  # packet A carries no decisions


def test_threshold_and_direction_flags():
    rng = np.random.default_rng(0)
    n = 4000
    p = rng.uniform(size=n)
    p[:300] = rng.uniform(0, 0.049, size=300)
    df = pd.DataFrame({"log2FoldChange": rng.normal(0, 1, n), "pvalue": p,
                       "padj": np.minimum(1, p * n / (np.argsort(np.argsort(p)) + 1))})
    meta = pd.DataFrame({"title": [f"s{i}" for i in range(6)], "grp": ["Sed"] * 3 + ["Ex"] * 3},
                        index=[f"GSM{i}" for i in range(6)])
    n_p = int((df["pvalue"] < 0.05).sum())
    n_padj = int((df["padj"] < 0.05).sum())
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        out_csv = tmp / "DEG_results_Sed_vs_Ex.csv"
        df.to_csv(out_csv)
        records = [_rec("design", {"design_column": "grp", "contrasts": [
                       {"name": "grp_Sed_vs_Ex", "control": "Ex", "treatment": "Sed"}]}),
                   _rec("execution", {"outputs": [str(out_csv)], "counts": {"t": {}}}),
                   _rec("study", {"paper_counts": {"t": n_p}, "results": {"t": {"n_deg": n_padj,
                                                                               "rule": "padj < 0.05"}}})]
        case = _write_case(tmp, meta, records, design_cols=("grp",))
        s = case_review.build(case, tmp / "review", expr=False, root=tmp)
        names = [f["flag"] for f in s["flags"]]
        assert "possible_reversed_contrast" in names
        assert "other_rule_matches_paper" in names
        thr = [f for f in s["flags"] if f["flag"] == "other_rule_matches_paper"][0]
        assert thr["closest_rule"].startswith("pvalue<0.05")


def test_refusal_with_exercise_words_is_flagged():
    meta = pd.DataFrame({"title": ["WT sed 1", "WT sed 2", "WT run 1", "WT run 2"],
                         "treatment": ["sedentary", "sedentary", "wheel running", "wheel running"]},
                        index=["GSM1", "GSM2", "GSM3", "GSM4"])
    records = [_rec("design", {"analysis_type": "none"}, "refused", "No exercise arm in this series.")]
    with tempfile.TemporaryDirectory() as t:
        case = _write_case(Path(t), meta, records, design_cols=("treatment",))
        s = case_review.build(case, Path(t) / "review", expr=False)
        assert "refusal_vs_exercise_words" in [f["flag"] for f in s["flags"]]


def test_expression_check_supports_true_key():
    meta = _gse283493_like()
    rng = np.random.default_rng(1)
    genes = 400
    rat = meta["group"] + "|" + meta["library"].str[-1]
    animal = {r: rng.normal(0, 0.6, genes) for r in rat.unique()}
    base = rng.uniform(4, 10, genes)
    logm = np.column_stack([base + animal[rat[s]] + rng.normal(0, 0.3, genes) for s in meta.index])
    counts = pd.DataFrame(np.round(2 ** logm), index=[f"g{i}" for i in range(genes)], columns=meta.index)
    records = [_rec("covariance", {"status": "required", "blocking_terms": []}, "manual_review",
                    "no animal ID in GEO")]
    with tempfile.TemporaryDirectory() as t:
        case = _write_case(Path(t), meta, records)
        counts.to_csv(case / "aligned" / "aligned_matrix.csv")
        s = case_review.build(case, Path(t) / "review", expr=True)
        assert s["pairing_expression_check"]["status"] == "supported", s["pairing_expression_check"]


def test_pairing_search_finds_glued_names_and_many_subjects():
    """GSE267512-like: titles ALORPRE / ALORPOST, 30 subjects (more levels than a grouping column)."""
    subs = [f"S{chr(65 + i // 26)}{chr(65 + i % 26)}X" for i in range(30)]
    rows = [{"title": f"{s}{t}", "time": t, "subject": s} for s in subs for t in ("PRE", "POST")]
    meta = pd.DataFrame(rows, index=[f"GSM{i}" for i in range(len(rows))])
    cands = {c["key"]: c for c in case_review.pairing_search(meta) if c["across"] == "time"}
    assert cands["title without the time level"]["keys_in_every_level_once"] == 30
    assert cands["subject"]["keys_in_every_level_once"] == 30


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
