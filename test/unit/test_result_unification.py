"""Tests for the two coupled meeting notes:
  #3 (one-pass): the paper's reported findings (#5) are pulled in the SAME lean extraction call as
      the descriptive tables, and reused (no separate findings LLM call) on the own-GSE path.
  #2 (both into result): the computed-vs-reported reconciliation (#6 agreement table) is promoted
      into the SEA-CDM result layer — a results+analysis row carrying BOTH the paper's claim AND
      our computed value, with disagreements flagged.

All offline (no network): without CLAUDE_API_KEY the lean call returns an empty container, which is
exactly enough to prove the WIRING (the reported_findings key is set in lean mode, absent in full
mode → that's how the cohort decides one-pass vs standalone).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_result_unification.py
"""
import os
import sys
import csv
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.seacdm_tools import (
    LeanExtraction, ReportedFinding, build_reconciliation_rows, build_reported_findings,
    extract_tables_from_text, _UNVERIFIED,
)
from tools.sea_cdm_schema import csv_columns


def test_lean_schema_carries_findings():
    le = LeanExtraction(reported_findings=[
        ReportedFinding(entity="Bdnf", entity_type="gene", direction="up", source="Bdnf up-regulated")])
    assert len(le.reported_findings) == 1 and le.reported_findings[0].entity == "Bdnf"
    # default empty
    assert LeanExtraction().reported_findings == []
    print("  [ok] LeanExtraction validates with reported_findings (req #3 one-pass schema)")


def test_reconciliation_rows():
    summary = {"confirmed": 3, "contradicted": 1, "direction_only": 2,
               "not_detected": 2, "not_in_results": 1, "not_checkable": 4}
    rows = build_reconciliation_rows("GSE208615", "out/GSE208615_agreement.csv", summary, n_findings=13)
    a, r = rows["analysis"][0], rows["results"][0]
    assert a["analysis_id"] == "GSE208615_analysis_recon1"
    assert a["da_method"] == "reconciliation"
    # n_deg repurposed to disagreement count = contradicted + not_detected = 1 + 2 = 3
    assert a["n_deg"] == "3", a["n_deg"]
    assert r["results_id"] == "GSE208615_res_recon1"
    assert r["file_access"] == "out/GSE208615_agreement.csv"
    assert "disagreement" in r["dataset_size"] and "13 findings" in r["dataset_size"]
    # rows must conform to the CDM column order (so append_tables_to_csvs writes cleanly)
    assert list(a.keys()) == csv_columns("analysis")
    assert list(r.keys()) == csv_columns("results")
    # empty summary -> nothing (no findings or no DEG to reconcile)
    assert build_reconciliation_rows("X", "p", {}, 0) == {"analysis": [], "results": []}
    print("  [ok] build_reconciliation_rows: analysis+results rows, disagreement count, CDM-ordered")


def test_prefetched_findings_no_llm_call():
    # If the LLM were called it would need a key; prefetched must bypass it entirely.
    d = tempfile.mkdtemp()
    fcsv = os.path.join(d, "GSE1_reported_findings.csv")
    pf = [
        {"entity": "Sirt2", "entity_type": "gene", "direction": "changed", "magnitude": None,
         "comparison": "ex vs sed", "source": "Sirt2 changed"},
        {"entity": "Pgc1a", "entity_type": "gene", "direction": "up", "magnitude": "2-fold",
         "comparison": "ex vs sed", "source": f"{_UNVERIFIED} paraphrased pgc1a went up"},
    ]
    rep = {}
    out = build_reported_findings("GSE1", "irrelevant text", fcsv, "Mouse",
                                  report=rep, prefetched_findings=pf)
    assert rep["n_findings"] == 2
    assert rep["n_unverified"] == 1, rep  # the [UNVERIFIED]-prefixed one is counted
    assert os.path.exists(fcsv)
    written = list(csv.DictReader(open(fcsv, encoding="utf-8")))
    assert len(written) == 2 and written[0]["entity"] == "Sirt2"
    assert out["results"][0]["results_id"] == "GSE1_res_text1"
    assert out["analysis"][0]["n_deg"] == "2"
    print("  [ok] build_reported_findings(prefetched=...): reuses findings, no LLM call, CSV+rows written")


def test_one_pass_wiring_offline():
    """In lean mode the report gets reported_findings (=[] without a key); in full mode it does not.
    That key presence is exactly how the cohort decides one-pass vs standalone."""
    d = tempfile.mkdtemp()
    paper = os.path.join(d, "paper.txt")
    open(paper, "w", encoding="utf-8").write("Exercise increased Bdnf in the hippocampus.")
    text = open(paper, encoding="utf-8").read()

    # minimal GEO-style metadata so use_lean=True
    meta = os.path.join(d, "GSEX_metadata.csv")
    with open(meta, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sample", "title", "characteristics_ch1.0.genotype", "organism_ch1", "instrument_model"])
        w.writerow(["GSM1", "ctrl rep1", "WT", "Mus musculus", "Illumina NovaSeq 6000"])
        w.writerow(["GSM2", "ex rep1", "WT", "Mus musculus", "Illumina NovaSeq 6000"])

    lean_rep = {}
    extract_tables_from_text("GSEX", text, "Mouse", report=lean_rep, metadata_csv=meta)
    assert lean_rep.get("extraction_mode") == "lean(1-call)", lean_rep.get("extraction_mode")
    assert "reported_findings" in lean_rep, "lean mode must stash reported_findings (key present)"
    assert isinstance(lean_rep["reported_findings"], list)

    full_rep = {}
    extract_tables_from_text("GSEY", text, "Mouse", report=full_rep, metadata_csv=None)
    assert full_rep.get("extraction_mode") == "full(3-call)", full_rep.get("extraction_mode")
    assert "reported_findings" not in full_rep, "full mode must NOT stash (key absent -> standalone #5)"
    print("  [ok] one-pass wiring: lean sets reported_findings key (reuse), full leaves it absent (standalone)")


if __name__ == "__main__":
    test_lean_schema_carries_findings()
    test_reconciliation_rows()
    test_prefetched_findings_no_llm_call()
    test_one_pass_wiring_offline()
    print("\nALL TESTS PASSED.")
