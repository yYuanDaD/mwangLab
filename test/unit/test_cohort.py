"""Phase 3 tests for tools/cohort_tools.py — keyword -> SEA-CDM CSV cohort orchestrator.

Run:  PYTHONIOENCODING=utf-8 python test/unit/test_cohort.py
      PYTHONIOENCODING=utf-8 python test/unit/test_cohort.py --live   # hits S2 + EuropePMC + LLM

Offline: own-vs-cited classifier, GSE selection, CSV scaffolding, pipeline-row builder.
Live: a tiny real cohort (text tables only, with_analysis=False).
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.sea_cdm_schema import csv_columns, SEA_TABLES
from tools.cohort_tools import (
    classify_gse_ownership, choose_own_gse,
    init_cohort_csvs, build_pipeline_rows, _count_csv_rows,
    run_agent_a_cohort, _is_exercise_relevant_search_hit, normalize_agent_a_request,
)


def test_ownership_offline():
    own_text = ("Total RNA was sequenced. The mouse RNA-seq data are deposited in the NCBI Gene "
                "Expression Omnibus database under accession number GSE279359.")
    cited_text = ("Public datasets were downloaded from the Gene Expression Omnibus "
                  "(accession numbers GSE87749 and GSE151066, respectively) and re-analyzed.")
    o, so, _ = classify_gse_ownership(own_text, "GSE279359")
    assert o == "own", f"expected own, got {o}"
    c, sc, _ = classify_gse_ownership(cited_text, "GSE87749")
    assert c == "cited", f"expected cited, got {c}"

    # mixed paper: own GSE + two cited GSEs -> choose the own one
    mixed = own_text + " Separately, " + cited_text
    chosen, tag, classes = choose_own_gse(mixed)
    assert chosen == "GSE279359", f"expected GSE279359, got {chosen}"
    assert tag == "own"
    kinds = {c["gse"]: c["ownership"] for c in classes}
    assert kinds["GSE87749"] == "cited" and kinds["GSE151066"] == "cited"

    # single ambiguous GSE -> assumed own (study_id only)
    amb = "We profiled muscle. Data: GSE999999."
    chosen2, tag2, _ = choose_own_gse(amb)
    assert chosen2 == "GSE999999" and tag2 == "own_assumed_single", (chosen2, tag2)

    # no GSE at all
    chosen3, tag3, classes3 = choose_own_gse("No accession here.")
    assert chosen3 == "" and tag3 == "" and classes3 == []
    print("[offline] own-vs-cited classification + GSE selection: PASS")


def test_scaffold_and_pipeline_rows_offline():
    out = "test/output/smoke_test/cohort_offline"
    if os.path.isdir(out):
        import shutil; shutil.rmtree(out)
    csv_dir = os.path.join(out, "csv")
    init_cohort_csvs(csv_dir)
    # all registered schema CSVs exist, including the ontology stub.
    for entry in SEA_TABLES.values():
        assert os.path.exists(os.path.join(csv_dir, entry["csv"])), f"missing {entry['csv']}"
    # study.csv header matches schema
    with open(os.path.join(csv_dir, "study.csv"), encoding="utf-8") as f:
        assert f.readline().strip().split(",") == csv_columns("study")

    # pipeline rows: correct ids, ordering, and column alignment
    summary_row = {"da_method": "deseq2", "n_deg": 42, "status": "deg_gsea_ok"}
    rows = build_pipeline_rows("GSE279359", summary_row, "nonexistent_dir")  # no DEG/GSEA files -> no results rows
    assert len(rows["analysis"]) == 1
    a = rows["analysis"][0]
    assert a["analysis_id"] == "GSE279359_analysis1"
    assert a["da_method"] == "deseq2" and str(a["n_deg"]) == "42"
    assert list(a.keys()) == csv_columns("analysis"), "analysis row column mismatch"
    for r in rows["results"]:
        assert list(r.keys()) == csv_columns("results")
    print(f"[offline] CSV scaffold ({len(SEA_TABLES)} files) + pipeline-row builder: PASS")


def test_exercise_relevance_gate_offline():
    ok, reason = _is_exercise_relevant_search_hit({
        "title": "Skeletal muscle transcriptome after treadmill exercise",
        "abstract": "Mice completed an acute exercise bout on a treadmill before RNA-seq.",
    })
    assert ok, reason

    ok, reason = _is_exercise_relevant_search_hit({
        "title": "Integrated analysis of single-cell RNA-seq and bulk RNA-seq in acute myeloid leukemia",
        "abstract": "The TCGA cohort was used as the training dataset for model construction.",
    })
    assert not ok, reason

    ok, reason = _is_exercise_relevant_search_hit({
        "title": "Twin study of LDL-C and HDL-C levels",
        "abstract": "Smoking habit, exercise habit, and drinking habit were assessed by questionnaire.",
    })
    assert not ok, reason

    print("[offline] exercise relevance gate: PASS")


def test_request_normalization_offline():
    req = normalize_agent_a_request(
        keyword="  exercise RNA-seq  ", organism="human", max_papers=0,
        search_pool=1, run_label=" unsafe / cohort ",
        treatment_keywords=["Exercise", "exercise", " trained "],
        control_keywords=["Control", "control", "sedentary"],
    )
    assert req.keyword == "exercise RNA-seq"
    assert req.organism == "Human"
    assert req.max_papers == 1 and req.search_pool == 1
    assert req.run_label == "unsafe_cohort"
    assert req.treatment_keywords == ["Exercise", "trained"]
    assert req.control_keywords == ["Control", "sedentary"]
    try:
        normalize_agent_a_request(keyword="x", treatment_keywords=["control"],
                                  control_keywords=["Control"])
        raise AssertionError("overlapping arm keywords should be rejected")
    except ValueError as exc:
        assert "overlap" in str(exc)
    print("[offline] request normalization + validation: PASS")


def test_cohort_live():
    out_base = "test/output/smoke_test"
    label = "cohort_live"
    cohort_dir = os.path.join(out_base, f"agentA_cohort_{label}")
    if os.path.isdir(cohort_dir):
        import shutil; shutil.rmtree(cohort_dir)
    report = run_agent_a_cohort(
        keyword="acute exercise skeletal muscle RNA-seq",
        max_papers=2,
        organism="Mouse",
        with_analysis=False,
        run_label=label,
        output_base=out_base,
    )
    print("\n[live]\n" + report)
    csv_dir = os.path.join(cohort_dir, "csv")
    assert os.path.isdir(csv_dir), "csv dir not created"
    counts = _count_csv_rows(csv_dir)
    assert counts.get("study", 0) >= 1, f"expected >=1 study row, got {counts}"
    assert os.path.exists(os.path.join(cohort_dir, "papers.csv"))
    print(f"[live] CSV row counts: { {t: c for t, c in counts.items() if c} }")


if __name__ == "__main__":
    test_ownership_offline()
    test_scaffold_and_pipeline_rows_offline()
    test_exercise_relevance_gate_offline()
    test_request_normalization_offline()
    if "--live" in sys.argv:
        test_cohort_live()
    else:
        print("\n(pass --live to run a tiny real 2-paper cohort)")
