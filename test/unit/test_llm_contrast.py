"""Smoke test for tools/llm_helpers.py::validate_contrast_with_llm.

Runs three scenarios against the real Claude API to confirm the structured
output schema works end-to-end:

  1. Happy path — Python picks a sensible contrast; LLM should confirm.
  2. Override — Python picks a less suitable column (genotype) when a cleaner
     treatment column exists; LLM should override.
  3. No clean contrast — metadata has only multi-factor / confounded columns
     with no clean 2-group split for the user's intent; LLM should refuse.

Each scenario costs roughly $0.001-0.005 (Sonnet 4.6, ~1-2K tokens). Run
when you want to validate the LLM hookup; not part of any automated suite.

Usage:
    python test/unit/test_llm_contrast.py
"""

import os
import sys
import tempfile

import pandas as pd

# Make project root importable when invoked from any cwd
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

from tools.llm_helpers import (  # noqa: E402
    summarize_metadata_for_llm,
    validate_contrast_with_llm,
)


def _write_csv(rows: list[dict]) -> str:
    """Write rows to a temp metadata CSV (first key = sample ID column)."""
    fd, path = tempfile.mkstemp(suffix="_metadata.csv")
    os.close(fd)
    df = pd.DataFrame(rows).set_index(list(rows[0].keys())[0])
    df.to_csv(path)
    return path


def _print_result(label: str, result, proposed) -> None:
    print(f"\n--- {label} ---")
    print(f"proposed (python): {proposed}")
    if result is None:
        print("LLM result: None (call failed or LLM unavailable)")
        return
    print(f"  is_valid: {result.is_valid}")
    print(f"  design_column: {result.design_column}")
    print(f"  control_value: {result.control_value}")
    print(f"  treatment_value: {result.treatment_value}")
    print(f"  reasoning: {result.reasoning}")


def scenario_happy_path():
    rows = [
        {"sample": f"GSM_{i:02d}", "characteristics_ch1.0.tissue": tissue}
        for i, tissue in enumerate(
            ["Cervical Spinal Cord"] * 4 + ["Thoracic and Lumbar Spinal Cord"] * 4
        )
    ]
    path = _write_csv(rows)
    proposed = ("characteristics_ch1.0.tissue", "Cervical Spinal Cord",
                "Thoracic and Lumbar Spinal Cord")
    summary = summarize_metadata_for_llm(path)
    result = validate_contrast_with_llm(
        accession="TEST_HAPPY",
        metadata_columns_summary=summary,
        treatment_keywords=["thoracic", "lumbar"],
        control_keywords=["cervical"],
        proposed=proposed,
    )
    _print_result("Scenario 1: HAPPY PATH (LLM should confirm)", result, proposed)


def scenario_override():
    rows = []
    for i in range(4):
        rows.append({
            "sample": f"GSM_KO_sed_{i}",
            "characteristics_ch1.0.genotype": "knockout",
            "characteristics_ch1.1.treatment": "sedentary",
        })
        rows.append({
            "sample": f"GSM_WT_sed_{i}",
            "characteristics_ch1.0.genotype": "wildtype",
            "characteristics_ch1.1.treatment": "sedentary",
        })
        rows.append({
            "sample": f"GSM_KO_exe_{i}",
            "characteristics_ch1.0.genotype": "knockout",
            "characteristics_ch1.1.treatment": "exercise",
        })
        rows.append({
            "sample": f"GSM_WT_exe_{i}",
            "characteristics_ch1.0.genotype": "wildtype",
            "characteristics_ch1.1.treatment": "exercise",
        })
    path = _write_csv(rows)
    proposed = ("characteristics_ch1.0.genotype", "wildtype", "knockout")
    summary = summarize_metadata_for_llm(path)
    result = validate_contrast_with_llm(
        accession="TEST_OVERRIDE",
        metadata_columns_summary=summary,
        treatment_keywords=["exercise", "training", "exe", "run"],
        control_keywords=["sedentary", "control", "sed"],
        proposed=proposed,
    )
    _print_result(
        "Scenario 2: OVERRIDE (Python picked genotype; LLM should pick treatment)",
        result, proposed,
    )


def scenario_no_clean_contrast():
    rows = [
        {"sample": "GSM_01", "characteristics_ch1.0.genotype": "WT",
         "characteristics_ch1.1.tissue": "liver", "characteristics_ch1.2.timepoint": "0h"},
        {"sample": "GSM_02", "characteristics_ch1.0.genotype": "WT",
         "characteristics_ch1.1.tissue": "kidney", "characteristics_ch1.2.timepoint": "6h"},
        {"sample": "GSM_03", "characteristics_ch1.0.genotype": "KO",
         "characteristics_ch1.1.tissue": "liver", "characteristics_ch1.2.timepoint": "24h"},
        {"sample": "GSM_04", "characteristics_ch1.0.genotype": "KO",
         "characteristics_ch1.1.tissue": "kidney", "characteristics_ch1.2.timepoint": "48h"},
    ]
    path = _write_csv(rows)
    summary = summarize_metadata_for_llm(path)
    result = validate_contrast_with_llm(
        accession="TEST_NO_CONTRAST",
        metadata_columns_summary=summary,
        treatment_keywords=["exercise", "training"],
        control_keywords=["sedentary", "control"],
        proposed=None,
    )
    _print_result(
        "Scenario 3: NO CLEAN CONTRAST (no exercise/sedentary columns; LLM should refuse)",
        result, None,
    )


if __name__ == "__main__":
    if not os.getenv("CLAUDE_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
    if not os.getenv("CLAUDE_API_KEY"):
        print("CLAUDE_API_KEY not found in environment or .env. Aborting.")
        sys.exit(1)

    print("=" * 60)
    print("LLM contrast-validation smoke test")
    print("=" * 60)
    scenario_happy_path()
    scenario_override()
    scenario_no_clean_contrast()
    print("\n" + "=" * 60)
    print("Done.")
