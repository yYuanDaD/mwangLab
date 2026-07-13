"""Regression test for the search_index handle fix in tools/paper_tools.py (NO LLM).

Bug it guards against: the agent picked the right paper by title but mutated the
8-digit PMCID when retyping it into fetch_paper_text (PMC12248044 -> PMC11906498),
silently fetching an unrelated paper and burning its fetch budget on dead ends.

Fix: search_papers exposes a stable [#N] handle and caches the ranked rows;
fetch_paper_text(search_index=N) resolves the EXACT pmcid/pdf_url so the LLM never
retypes an id. A hand-typed pmcid not in the latest search is rejected as a typo.

This test asserts:
  1. fetch_paper_text(search_index=N) fetches the EXACT pmcid of hit #N (handle round-trip).
  2. A directly-passed pmcid that is NOT in the latest search is rejected.
  3. An out-of-range / no-search search_index fails loudly rather than fetching anything.

Run:  python test/unit/test_paper_handle.py
(On Windows set PYTHONIOENCODING=utf-8 first — the tools print emojis.)

Network-dependent: Semantic Scholar may 429 and Europe PMC may lack an OA hit for the
top result; both are source flakes, not code bugs — the test reports them as SKIP.
"""

import os
import sys

# chdir prelude: always run with the project root as CWD regardless of invocation dir.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import tools.paper_tools as pt
from tools.paper_tools import search_papers, fetch_paper_text

KEYWORD = "exercise skeletal muscle transcriptome"
OUT = "test/output/smoke_test/paper_handle"


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    res = search_papers.invoke({
        "keyword": KEYWORD,
        "fields_of_study": "Medicine,Biology",
        "require_pdf": True,
        "min_year": 2018,
        "max_results": 30,
        "output_dir": OUT,
    })
    if "rate limit" in res.lower() or "no open-access" in res.lower():
        print(f"SKIP: search_papers unavailable this run:\n{res}")
        return 0

    rows = pt._LAST_SEARCH_ROWS
    assert rows, "search_papers did not cache _LAST_SEARCH_ROWS"
    assert all(r["idx"] == i for i, r in enumerate(rows, 1)), "idx is not a 1-based contiguous rank"
    print(f"search_papers cached {len(rows)} ranked hits.")

    # --- Check 2 first (no network): a pmcid NOT in the results is rejected. ---
    bogus = "PMC99999999"
    assert not pt._pmcid_in_last_search(bogus)
    rej = fetch_paper_text.invoke({"pmcid": bogus, "output_dir": OUT})
    assert "NOT among the latest" in rej, f"bogus pmcid was not rejected:\n{rej}"
    print("PASS: directly-passed pmcid not in search results is rejected (anti-typo guard).")

    # --- Check 3 (no network): out-of-range index fails loudly. ---
    oor = fetch_paper_text.invoke({"search_index": len(rows) + 1, "output_dir": OUT})
    assert "out of range" in oor, f"out-of-range index did not fail loudly:\n{oor}"
    print("PASS: out-of-range search_index fails loudly.")

    # --- Check 1 (network): index resolves to the EXACT pmcid of that hit. ---
    target = next((r for r in rows if r["pmcid"]), None)
    if target is None:
        print("SKIP: no hit has a PMCID this run — cannot test Europe PMC round-trip.")
        return 0
    idx, want_pmcid = target["idx"], target["pmcid"]
    out = fetch_paper_text.invoke({"search_index": idx, "output_dir": OUT})
    if "Europe PMC has no open-access full text" in out or "did not return a PDF" in out:
        print(f"SKIP: hit #{idx} ({want_pmcid}) has no fetchable OA full text this run:\n{out}")
        return 0
    assert want_pmcid in out, (
        f"search_index={idx} should have fetched {want_pmcid}, but the output does not mention it:\n{out}"
    )
    print(f"PASS: fetch_paper_text(search_index={idx}) resolved to the exact pmcid {want_pmcid}.")

    # Bonus: if the known GSE-bearing paper is present, confirm its GSE surfaces.
    known = next((r for r in rows if r["pmcid"] == "PMC12248044"), None)
    if known:
        out2 = fetch_paper_text.invoke({"search_index": known["idx"], "output_dir": OUT})
        if "GSE279359" in out2:
            print("PASS (bonus): PMC12248044 fetched via handle and its own GSE279359 surfaced.")
        else:
            print("NOTE: PMC12248044 present but GSE279359 not in fetched text this run (OA/text variance).")

    print("\nALL HANDLE CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
