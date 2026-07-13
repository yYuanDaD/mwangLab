"""Offline test for the provenance verifier (verify_provenance) — no LLM, no network.

Enforces the contract the extraction prompts only *ask* for: every Sourced `<field>_source`
quote must be a verbatim substring of the paper text. A fabricated/paraphrased quote is marked
'[UNVERIFIED]' in place; a faithful quote that differs only in whitespace/punctuation is NOT
flagged; and plain `_source`-suffixed DATA fields (documentation.reference_source = 'GEO') are
never checked against the text.

Run: .venv/Scripts/python.exe test/unit/test_provenance.py   (bare python also works — no heavy deps)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.seacdm_tools import verify_provenance, _norm_quote, _provenance_source_cols, _UNVERIFIED

# A tiny "paper": note the newline inside "long-read\nRNA sequencing" and the ascii hyphen in
# "exercise-induced" — the verifier must see through line-wrapping and punctuation variants.
PAPER = (
    "We profiled the acute exercise transcriptome in mouse gastrocnemius muscle. "
    "Libraries were prepared for long-read\nRNA sequencing on an Oxford Nanopore MinION. "
    "We identified exercise-induced changes in gene expression after a single bout."
)


def _study_row(**over):
    row = {
        "study_id": "GSE000001", "reference_source": "GEO", "reference_source_id": "GSE000001",
        "study_name": "acute exercise transcriptome",
        "study_name_source": "the acute exercise transcriptome in mouse gastrocnemius muscle",  # verbatim
        "study_description": "single-bout exercise study",
        "study_description_source": "we performed a 12-week resistance training program",  # FABRICATED
        "study_focus": None, "study_focus_source": None,                                  # null -> skipped
    }
    row.update(over)
    return row


def _doc_row(**over):
    row = {
        "documentation_id": "GSE000001_doc1", "study_id": "GSE000001",
        "reference_source": "PubMed",  # plain DATA field ending in _source — MUST be ignored
        "document_name": "long-read RNA sequencing paper",
        # quote spans a newline in the text + uses an en-dash where the text has a hyphen:
        "document_name_source": "long-read RNA sequencing on an Oxford Nanopore MinION",
    }
    row.update(over)
    return row


def t_norm_quote():
    assert _norm_quote("  Long-Read\nRNA   sequencing ") == "long-read rna sequencing"
    assert _norm_quote("exercise–induced") == "exercise-induced"   # en-dash -> hyphen
    assert _norm_quote("say “hi”") == 'say "hi"'              # curly -> straight quotes
    assert _norm_quote(None) == "" and _norm_quote("   ") == ""
    print("[PASS] _norm_quote: whitespace collapse + dash/quote folding + blank handling")


def t_source_cols_exclude_plain():
    cols = _provenance_source_cols("documentation")
    assert "document_name_source" in cols, "missing a real Sourced companion column"
    assert "reference_source" not in cols, "plain reference_source wrongly treated as provenance!"
    assert "citation_source" in cols
    # study.reference_source is plain too
    assert "reference_source" not in _provenance_source_cols("study")
    # ontology has no model -> no columns
    assert _provenance_source_cols("ontology") == set()
    print(f"[PASS] _provenance_source_cols: documentation -> {len(cols)} cols, plain reference_source excluded")


def t_verify_flags_only_fabricated():
    tables = {"study": [_study_row()], "documentation": [_doc_row()]}
    rep = verify_provenance(tables, PAPER)

    s, d = tables["study"][0], tables["documentation"][0]
    # verbatim quote: untouched
    assert not s["study_name_source"].startswith(_UNVERIFIED), "verbatim quote wrongly flagged"
    # fabricated quote: flagged in place
    assert s["study_description_source"].startswith(_UNVERIFIED), "fabricated quote NOT flagged"
    assert "12-week resistance" in s["study_description_source"], "original quote not preserved after flag"
    # value left intact for human review
    assert s["study_description"] == "single-bout exercise study"
    # null source: skipped, stays null
    assert s["study_focus_source"] is None
    # whitespace+dash-spanning faithful quote: verified, untouched
    assert not d["document_name_source"].startswith(_UNVERIFIED), "newline/dash quote wrongly flagged"
    # plain DATA field ending in _source: NEVER touched, even though 'GEO'/'PubMed' aren't in the text
    assert s["reference_source"] == "GEO" and d["reference_source"] == "PubMed"

    # report accounting
    assert rep["n_unverified"] == 1, f"expected 1 unverified, got {rep['n_unverified']}"
    assert rep["n_verified"] == rep["n_total"] - 1
    assert rep["n_total"] == 3, f"expected 3 checked quotes (2 study + 1 doc), got {rep['n_total']}"
    assert len(rep["items"]) == 1 and rep["items"][0]["field"] == "study_description"
    assert rep["items"][0]["table"] == "study"
    print(f"[PASS] verify_provenance: {rep['n_verified']}/{rep['n_total']} verbatim, "
          f"1 fabricated flagged, plain fields & nulls untouched")


def t_idempotent():
    tables = {"study": [_study_row()], "documentation": [_doc_row()]}
    r1 = verify_provenance(tables, PAPER)
    flagged_after_1 = tables["study"][0]["study_description_source"]
    r2 = verify_provenance(tables, PAPER)  # re-run must not double-mark or change counts
    assert tables["study"][0]["study_description_source"] == flagged_after_1, "double-marked on re-run"
    assert flagged_after_1.count(_UNVERIFIED) == 1, "marker applied more than once"
    assert (r2["n_total"], r2["n_unverified"]) == (r1["n_total"], r1["n_unverified"]), "counts drifted on re-run"
    print("[PASS] idempotent: re-running does not double-mark or drift counts")


def main():
    print("=" * 74)
    print("PROVENANCE VERIFIER — offline tests")
    print("=" * 74)
    for fn in (t_norm_quote, t_source_cols_exclude_plain, t_verify_flags_only_fabricated, t_idempotent):
        fn()
    print("=" * 74)
    print("ALL PROVENANCE TESTS PASSED")


if __name__ == "__main__":
    main()
