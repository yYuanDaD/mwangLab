"""Smoke test for tools/llm_helpers.py::align_samples_with_llm_fallback.

Runs three scenarios end-to-end:

  1. String match succeeds — exact intersection wins; LLM is NEVER called.
  2. LLM rescue — counts use sequencer abbreviations (HC_F1_TL_S54_L003),
     metadata uses full words (HomeCage1_Female1_TotalLysate); the 3 string
     strategies fail and the LLM 4th strategy bridges the gap.
  3. Truly unmatched — random tokens on both sides; LLM also can't help and
     the method returns 'no_match' / 'no_match_llm_too_few'.

Run when you want to validate the LLM hookup; not part of any automated suite.

Usage:
    python test/unit/test_llm_align.py
"""

import os
import sys

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

from tools.llm_helpers import align_samples_with_llm_fallback  # noqa: E402


def _print_result(label: str, mapping: dict, method: str, expected_method_prefix: str):
    print(f"\n--- {label} ---")
    print(f"method: {method}")
    print(f"mapped {len(mapping)} pairs:")
    for k, v in list(mapping.items())[:10]:
        print(f"  {k!r:50s} -> {v!r}")
    if len(mapping) > 10:
        print(f"  ... and {len(mapping) - 10} more")
    ok = method.startswith(expected_method_prefix)
    print(f"PASS" if ok else f"FAIL (expected method starting with {expected_method_prefix!r})")


def scenario_string_match():
    counts_cols = [f"GSM{1000+i}" for i in range(6)]
    metadata = pd.DataFrame(
        {"title": [f"sample {i}" for i in range(6)]},
        index=counts_cols,
    )
    mapping, method = align_samples_with_llm_fallback(counts_cols, metadata)
    _print_result("Scenario 1: STRING MATCH (LLM should NOT be called)",
                  mapping, method, "exact")


def scenario_llm_rescue():
    # Counts use sequencer-style abbreviations; metadata uses descriptive labels.
    counts_cols = [
        "HC_F1_TL_S54_L003", "HC_F2_TL_S55_L003", "HC_F3_TL_S56_L003",
        "HC_M1_TL_S57_L003", "HC_M2_TL_S58_L003", "HC_M3_TL_S59_L003",
        "EE_F1_TL_S60_L003", "EE_F2_TL_S61_L003", "EE_F3_TL_S62_L003",
        "EE_M1_TL_S63_L003", "EE_M2_TL_S64_L003", "EE_M3_TL_S65_L003",
    ]
    meta_rows = [
        ("GSM_HomeCage_F1", "HomeCage", "Female", 1),
        ("GSM_HomeCage_F2", "HomeCage", "Female", 2),
        ("GSM_HomeCage_F3", "HomeCage", "Female", 3),
        ("GSM_HomeCage_M1", "HomeCage", "Male", 1),
        ("GSM_HomeCage_M2", "HomeCage", "Male", 2),
        ("GSM_HomeCage_M3", "HomeCage", "Male", 3),
        ("GSM_EnvEnriched_F1", "EnvironmentalEnrichment", "Female", 1),
        ("GSM_EnvEnriched_F2", "EnvironmentalEnrichment", "Female", 2),
        ("GSM_EnvEnriched_F3", "EnvironmentalEnrichment", "Female", 3),
        ("GSM_EnvEnriched_M1", "EnvironmentalEnrichment", "Male", 1),
        ("GSM_EnvEnriched_M2", "EnvironmentalEnrichment", "Male", 2),
        ("GSM_EnvEnriched_M3", "EnvironmentalEnrichment", "Male", 3),
    ]
    metadata = pd.DataFrame(
        [
            {"title": f"{cond}_{sex}_rep{n}_TotalLysate",
             "source_name_ch1": f"{cond} {sex} replicate {n} total lysate",
             "characteristics_ch1.0.condition": cond,
             "characteristics_ch1.1.sex": sex,
             "characteristics_ch1.2.replicate": n}
            for (_, cond, sex, n) in meta_rows
        ],
        index=[gsm for (gsm, _, _, _) in meta_rows],
    )
    mapping, method = align_samples_with_llm_fallback(counts_cols, metadata)
    _print_result("Scenario 2: LLM RESCUE (HC=HomeCage, EE=EnvEnriched, F/M=Female/Male)",
                  mapping, method, "llm")


def scenario_no_match():
    counts_cols = ["alpha", "bravo", "charlie", "delta"]
    metadata = pd.DataFrame(
        {"title": ["completely", "unrelated", "metadata", "labels"]},
        index=["zeta", "eta", "theta", "iota"],
    )
    mapping, method = align_samples_with_llm_fallback(counts_cols, metadata)
    _print_result("Scenario 3: TRULY UNMATCHED (string + LLM both should fail)",
                  mapping, method, "no_match")


if __name__ == "__main__":
    if not os.getenv("CLAUDE_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
    if not os.getenv("CLAUDE_API_KEY"):
        print("CLAUDE_API_KEY not found in environment or .env. Aborting.")
        sys.exit(1)

    print("=" * 60)
    print("LLM sample-alignment smoke test")
    print("=" * 60)
    scenario_string_match()
    scenario_llm_rescue()
    scenario_no_match()
    print("\n" + "=" * 60)
    print("Done.")
