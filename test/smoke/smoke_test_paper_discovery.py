"""Smoke test for the Agent A paper-discovery chain (NO LLM, NO GEO download).

Validates that  search_papers -> fetch_paper_text -> extract_geo_accession
reliably yields a real GEO GSE accession from an open-access paper's full text.
This is the cheap fast-fail check before running the full agent loop in main.py.

Run:  python test/smoke/smoke_test_paper_discovery.py
(On Windows set PYTHONIOENCODING=utf-8 first — the tools print emojis.)

Artifacts are written under test/output/smoke_test/paper_discovery/ to keep them
isolated from real runs. Network-dependent: Semantic Scholar may 429 and some
open-access PDF links 403 (bioRxiv/Cloudflare) — those are source flakes, not
code bugs; the test tries several candidates before giving up.
"""

import os
import sys
import time

# chdir prelude: always run with the project root as CWD regardless of invocation dir.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import pandas as pd

from tools.paper_tools import search_papers, fetch_paper_text, extract_geo_accession

OUT = "test/output/smoke_test/paper_discovery"
KEYWORD = "exercise skeletal muscle transcriptome"
MAX_FETCH_TRIES = 6


def main() -> int:
    print("=" * 64)
    print("STEP 1: search_papers")
    print("=" * 64)
    # The shared unauthenticated S2 pool 429s often; back off and retry inside the
    # single invocation rather than hammering it with separate process runs.
    res = ""
    for attempt in range(1, 6):
        res = search_papers.invoke({"keyword": KEYWORD, "max_results": 30, "output_dir": OUT})
        if "rate limit hit (429)" not in res:
            break
        wait = 15 + 15 * attempt  # 30, 45, 60, 75 ...
        print(f"  [attempt {attempt}/5] 429 rate limit; waiting {wait}s before retry...")
        time.sleep(wait)
    print(res)

    safe_kw = "".join(c if c.isalnum() else "_" for c in KEYWORD).strip("_")
    csv_path = os.path.join(OUT, f"paper_search_{safe_kw}.csv")
    if not os.path.isfile(csv_path):
        print("\nFAIL: search produced no CSV (likely a 429 rate limit). Retry in ~30s.")
        return 1

    df = pd.read_csv(csv_path)

    def _nonempty(series):
        s = series.astype(str).str.strip()
        return series.notna() & (s != "") & (s.str.lower() != "nan")

    has_pmcid = _nonempty(df["pmcid"])
    has_pdf = _nonempty(df["pdf_url"])
    cand = df[has_pmcid | has_pdf].copy()
    cand["_has_pmcid"] = _nonempty(cand["pmcid"])
    # Prefer PMC-available papers first (Europe PMC full text rarely 403s), keeping triage
    # order within each group (the tool already sorted by GSE-in-abstract -> seq-signal -> year).
    cand = cand.sort_values("_has_pmcid", ascending=False, kind="stable")
    print(f"\nLoaded {len(df)} candidates; {int(has_pmcid.sum())} have a PMCID, {int(has_pdf.sum())} a pdf_url. "
          f"Trying up to {MAX_FETCH_TRIES} (PMC-first).")

    print("\n" + "=" * 64)
    print("STEP 2+3: fetch_paper_text -> extract_geo_accession (until a GSE is found)")
    print("=" * 64)
    def _cell(v):
        return str(v) if pd.notna(v) and str(v).strip().lower() not in ("", "nan") else ""

    found = None
    for _, row in cand.head(MAX_FETCH_TRIES).iterrows():
        print(f"\n--- candidate: {str(row['title'])[:70]} ({row['year']}) ---")
        r = fetch_paper_text.invoke({
            "pdf_url": _cell(row["pdf_url"]),
            "pmcid": _cell(row["pmcid"]),
            "paper_id": str(row["paperId"]),
            "output_dir": OUT,
        })
        print(r)
        if "GEO_series:" in r:
            safe_pid = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in str(row["paperId"]))
            txt = os.path.join(OUT, f"{safe_pid}.txt")
            print(f"\n>>> extract_geo_accession on {txt}")
            ex = extract_geo_accession.invoke({"text_or_path": txt})
            print(ex)
            found = (str(row["title"]), txt, ex)
            break

    print("\n" + "=" * 64)
    if found:
        print("PASS: discovery chain produced a GEO GSE.")
        print(f"  paper: {found[0][:70]}")
        print("  NOTE: check the context snippet above to confirm it is the paper's OWN data,")
        print("        not a citation of another study, before handing it to the pipeline.")
        return 0
    print(f"FAIL: no candidate yielded a GSE in {MAX_FETCH_TRIES} tries.")
    print("  Likely PDF 403s or no accession in the extractable text — a source/network flake.")
    print("  Rerun, widen the keyword, or set S2_API_KEY for steadier search results.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
