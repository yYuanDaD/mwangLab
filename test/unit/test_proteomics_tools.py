"""Smoke tests for tools/proteomics_tools.py — identify_proteomics_labeling
and download_pride_project.

No LLM call — hits PRIDE REST API and downloads a small (~100 KB) .mztab.
Run with: PYTHONIOENCODING=utf-8 python test/unit/test_proteomics_tools.py
"""

import json
import os
import sys

# chdir to project root so the import is stable regardless of CWD
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd

from tools.proteomics_tools import (
    identify_proteomics_labeling,
    download_pride_project,
    preprocess_proteomics_matrix,
    _parse_mztab,
)

# --- Section 1: identify_proteomics_labeling ---------------------------------

LABELING_CASES = [
    # PXD000001: TMT spike-in dataset, but quantificationMethods is empty.
    # Should fall through to identifiedPTMStrings and detect TMT6plex reagent.
    # Ships a .mztab quant matrix.
    ("PXD000001", "labeled", "TMT", "identifiedPTMStrings", True,
     "rung 2 (identifiedPTMStrings)"),

    # PXD019643: HLA-Ligand-Atlas, label-free. quantificationMethods = ["Label free"].
    # Direct hit on rung 1. Ships 3425 files but NO quant matrix (all RAW + mzML + mzid).
    ("PXD019643", "label_free", None, "quantificationMethods", False,
     "rung 1 (quantificationMethods, label-free)"),
]


def test_labeling():
    print("=" * 70)
    print(" identify_proteomics_labeling (PRIDE REST API)")
    print("=" * 70)
    n_pass, n_fail = 0, 0
    for pxd, exp_label, exp_reagent, exp_source, exp_has_matrix, note in LABELING_CASES:
        print(f"\n[{pxd}] testing {note}")
        result = json.loads(identify_proteomics_labeling.invoke({"pxd_accession": pxd}))
        checks = [
            ("labeling", result.get("labeling"), exp_label),
            ("reagent", result.get("reagent"), exp_reagent),
            ("source", result.get("source"), exp_source),
            ("has_quant_matrix", result.get("has_quant_matrix"), exp_has_matrix),
        ]
        passed = True
        for field, actual, expected in checks:
            status = "OK " if actual == expected else "FAIL"
            if actual != expected:
                passed = False
            print(f"  [{status}] {field}: got {actual!r}, expected {expected!r}")
        if passed:
            n_pass += 1
            print(f"  reasoning: {result.get('reasoning')}")
        else:
            n_fail += 1
    return n_pass, n_fail


# --- Section 2: download_pride_project ---------------------------------------

def test_download():
    print("\n" + "=" * 70)
    print(" download_pride_project (PRIDE FTP-over-HTTPS)")
    print("=" * 70)
    n_pass, n_fail = 0, 0

    # Case 1: PXD000001 ships exactly one .mztab quant matrix (~100 KB).
    # After download, the data dir must contain the .mztab + the project JSON.
    pxd = "PXD000001"
    mztab_name = "PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz"
    data_dir = os.path.join("data", pxd)
    mztab_path = os.path.join(data_dir, mztab_name)
    meta_path = os.path.join(data_dir, f"{pxd}_project.json")

    print(f"\n[{pxd}] first download (may reuse if previously run)")
    out1 = download_pride_project.invoke({"pxd_accession": pxd})
    print("  " + out1.splitlines()[0])
    mztab_ok = os.path.exists(mztab_path) and os.path.getsize(mztab_path) > 50_000
    meta_ok = os.path.exists(meta_path) and os.path.getsize(meta_path) > 1_000
    print(f"  [{'OK ' if mztab_ok else 'FAIL'}] .mztab written: {mztab_path}")
    print(f"  [{'OK ' if meta_ok else 'FAIL'}] project JSON written: {meta_path}")
    if mztab_ok and meta_ok:
        n_pass += 1
    else:
        n_fail += 1

    # Case 2: re-download — must reuse existing file (skip-if-exists)
    print(f"\n[{pxd}] second download (must reuse — skip-if-exists)")
    out2 = download_pride_project.invoke({"pxd_accession": pxd})
    reused = "reused" in out2 and "0 downloaded" in out2
    print(f"  [{'OK ' if reused else 'FAIL'}] skip-if-exists fired (output mentions 'reused' and '0 downloaded')")
    if reused:
        n_pass += 1
    else:
        n_fail += 1
        print(f"  output snippet: {out2.splitlines()[3] if len(out2.splitlines()) > 3 else out2[:200]}")

    # Case 3: PXD019643 has no quant matrix — must say 'NO QUANT MATRIX' and not download spectra
    pxd2 = "PXD019643"
    print(f"\n[{pxd2}] RAW-only project (must report NO QUANT MATRIX)")
    out3 = download_pride_project.invoke({"pxd_accession": pxd2})
    refused = out3.startswith("NO QUANT MATRIX")
    print(f"  [{'OK ' if refused else 'FAIL'}] reported NO QUANT MATRIX")
    # Project JSON should still be saved
    meta2 = os.path.exists(os.path.join("data", pxd2, f"{pxd2}_project.json"))
    print(f"  [{'OK ' if meta2 else 'FAIL'}] project JSON saved even when skipped")
    if refused and meta2:
        n_pass += 1
    else:
        n_fail += 1
        print(f"  first line of output: {out3.splitlines()[0]}")

    return n_pass, n_fail


# --- Section 3: preprocess_proteomics_matrix (synthetic CSV tests) ----------
# Synthetic data lets us assert specific invariants (log-scale ceiling, median
# centering ~0, no NaN after imputation) deterministically — real PRIDE matrices
# vary too much in scale/missingness for tight assertions.

def _make_synthetic_matrix(n_features: int, n_samples: int, missing_rate: float = 0.0,
                           seed: int = 42, col_prefix: str = "S") -> pd.DataFrame:
    """Generate a fake positive-intensity matrix (log-uniform between 1e3 and 1e6,
    matching real proteomics intensity ranges). Optionally drops `missing_rate`
    fraction of cells to NaN."""
    rng = np.random.default_rng(seed)
    data = np.exp(rng.uniform(np.log(1e3), np.log(1e6), (n_features, n_samples)))
    if missing_rate > 0:
        mask = rng.random(data.shape) < missing_rate
        data[mask] = np.nan
    return pd.DataFrame(
        data,
        index=[f"P{i:05d}" for i in range(n_features)],
        columns=[f"{col_prefix}{i + 1}" for i in range(n_samples)],
    )


def test_preprocess_labeled_synthetic():
    """Labeled branch: log2-transform linear data, median-center, preserve all rows."""
    print("\n" + "=" * 70)
    print(" preprocess_proteomics_matrix — labeled branch (synthetic)")
    print("=" * 70)
    out_dir = "test/output/proteomics_synth"
    os.makedirs(out_dir, exist_ok=True)
    csv = os.path.join(out_dir, "synth_labeled.csv")
    _make_synthetic_matrix(10, 6, missing_rate=0.0, seed=1, col_prefix="TMT_").to_csv(csv)

    print(preprocess_proteomics_matrix.invoke({
        "quant_path": csv,
        "labeling": "labeled",
        "output_dir": out_dir,
    }))
    out = pd.read_csv(os.path.join(out_dir, "synth_labeled_preprocessed.csv"), index_col=0)

    checks = [
        ("shape preserved (no LFQ filter for labeled)", out.shape == (10, 6)),
        ("log-scale (max < 30)", out.max().max() < 30),
        ("median-centered to ~0", abs(out.median(axis=0)).max() < 1e-9),
        ("no NaN (input had none)", int(out.isna().sum().sum()) == 0),
    ]
    return _run_checks(checks)


def test_id_and_score_filtering():
    """Regression test for the v1 polish (2026-05-28 PXD025560 verification):
    `_load_quant_matrix` must (a) pick the protein-ID column by name pattern
    rather than blindly using col 0, and (b) exclude per-protein score columns
    from sample_cols. Synthetic Excel mirroring the PXD025560 Spectronaut layout
    — Pvalue/Qvalue/Cscore first, ProteinGroups in the middle, samples last."""
    print("\n" + "=" * 70)
    print(" _load_quant_matrix — ID + score-column filtering (synthetic)")
    print("=" * 70)
    from tools.proteomics_tools import _load_quant_matrix
    out_dir = "test/output/proteomics_synth"
    os.makedirs(out_dir, exist_ok=True)
    xlsx = os.path.join(out_dir, "spectronaut_like.xlsx")

    # 5 proteins, 3 score cols + 1 ID col + 1 description col + 4 sample cols
    rng = np.random.default_rng(7)
    df = pd.DataFrame({
        "PG.Pvalue": rng.random(5) * 1e-3,
        "PG.Qvalue": rng.random(5) * 1e-2,
        "PG.Cscore": rng.uniform(0, 100, 5),
        "PG.ProteinGroups": [f"P{i:05d}" for i in range(5)],
        "PG.ProteinDescriptions": [f"desc {i}" for i in range(5)],
        "[1] sample01.PG.MS2Quantity": rng.uniform(1e3, 1e6, 5),
        "[2] sample02.PG.MS2Quantity": rng.uniform(1e3, 1e6, 5),
        "[3] sample03.PG.MS2Quantity": rng.uniform(1e3, 1e6, 5),
        "[4] sample04.PG.MS2Quantity": rng.uniform(1e3, 1e6, 5),
    })
    df.to_excel(xlsx, index=False)

    loaded, sample_cols = _load_quant_matrix(xlsx)
    checks = [
        ("index picked = PG.ProteinGroups (not col 0)", loaded.index.name == "PG.ProteinGroups"),
        ("index values = real protein IDs", list(loaded.index[:2]) == ["P00000", "P00001"]),
        ("sample_cols has exactly 4 entries", len(sample_cols) == 4),
        ("no Pvalue in sample_cols", not any("Pvalue" in c for c in sample_cols)),
        ("no Qvalue in sample_cols", not any("Qvalue" in c for c in sample_cols)),
        ("no Cscore in sample_cols", not any("Cscore" in c for c in sample_cols)),
        ("all sample_cols are MS2Quantity", all("MS2Quantity" in c for c in sample_cols)),
    ]
    return _run_checks(checks)


def test_preprocess_lfq_synthetic():
    """LFQ branch: log + missingness filter + MinProb impute + median-center."""
    print("\n" + "=" * 70)
    print(" preprocess_proteomics_matrix — label-free branch (synthetic)")
    print("=" * 70)
    out_dir = "test/output/proteomics_synth"
    os.makedirs(out_dir, exist_ok=True)
    csv = os.path.join(out_dir, "synth_lfq.csv")
    df = _make_synthetic_matrix(20, 6, missing_rate=0.3, seed=2, col_prefix="S")
    # First 5 rows: ≥83% missing, must be filtered (only 1 of 6 cells populated)
    df.iloc[:5, :] = np.nan
    df.iloc[:5, 0] = 1e5
    df.to_csv(csv)

    print(preprocess_proteomics_matrix.invoke({
        "quant_path": csv,
        "labeling": "label_free",
        "output_dir": out_dir,
        "missing_threshold": 0.5,
    }))
    out = pd.read_csv(os.path.join(out_dir, "synth_lfq_preprocessed.csv"), index_col=0)

    checks = [
        ("filtered the 5 high-missing rows", out.shape[0] <= 15 and out.shape[0] > 0),
        ("kept all 6 sample columns", out.shape[1] == 6),
        ("log-scale (max < 30)", out.max().max() < 30),
        ("all NaN imputed (no missing after MinProb)", int(out.isna().sum().sum()) == 0),
        ("median-centered to ~0", abs(out.median(axis=0)).max() < 1e-9),
    ]
    return _run_checks(checks)


def test_mztab_parser_on_pxd000001():
    """Real-data check: parser handles a (sparse) PRIDE-auto-generated mzTab.

    PXD000001's mzTab is from 2012 and most abundance columns are literally
    'null' — this test verifies the parser correctly (a) finds the PRH header,
    (b) filters 21 decoy rows leaving 475 non-decoys, (c) detects the 6 abundance
    columns, (d) treats 'null' as NaN. It does NOT test the preprocess tool
    end-to-end because the source data is genuinely empty."""
    print("\n" + "=" * 70)
    print(" _parse_mztab — PXD000001 (real, sparse data)")
    print("=" * 70)
    df, abundance_cols = _parse_mztab(
        "data/PXD000001/PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz"
    )
    checks = [
        ("decoys filtered (475 non-decoy proteins of 496 total)", len(df) == 475),
        ("6 abundance columns detected", len(abundance_cols) == 6),
        ("abundance cols are protein_abundance_assay[N]",
         all("abundance_assay" in c for c in abundance_cols)),
        ("DECOY_ accessions filtered out",
         not any(str(i).startswith("DECOY_") for i in df.index)),
        ("'null' coerced to NaN in abundance cols",
         df[abundance_cols].isna().sum().sum() > 0),
    ]
    return _run_checks(checks)


def _run_checks(checks: list) -> tuple[int, int]:
    """Print and tally check results."""
    n_pass = n_fail = 0
    for desc, ok in checks:
        status = "OK " if ok else "FAIL"
        if ok: n_pass += 1
        else:  n_fail += 1
        print(f"  [{status}] {desc}")
    return (1 if n_fail == 0 else 0), (0 if n_fail == 0 else 1)


def run():
    label_pass, label_fail = test_labeling()
    dl_pass, dl_fail = test_download()
    pre_lab_pass, pre_lab_fail = test_preprocess_labeled_synthetic()
    id_pass, id_fail = test_id_and_score_filtering()
    pre_lfq_pass, pre_lfq_fail = test_preprocess_lfq_synthetic()
    mztab_pass, mztab_fail = test_mztab_parser_on_pxd000001()

    total_pass = label_pass + dl_pass + pre_lab_pass + id_pass + pre_lfq_pass + mztab_pass
    total_fail = label_fail + dl_fail + pre_lab_fail + id_fail + pre_lfq_fail + mztab_fail
    print("\n" + "=" * 70)
    print(f" TOTAL: {total_pass} passed, {total_fail} failed")
    print(f"   identify_proteomics_labeling:    {label_pass}/{label_pass + label_fail}")
    print(f"   download_pride_project:          {dl_pass}/{dl_pass + dl_fail}")
    print(f"   preprocess labeled (synth):      {pre_lab_pass}/{pre_lab_pass + pre_lab_fail}")
    print(f"   ID + score filtering (synth):    {id_pass}/{id_pass + id_fail}")
    print(f"   preprocess LFQ (synth):          {pre_lfq_pass}/{pre_lfq_pass + pre_lfq_fail}")
    print(f"   _parse_mztab (PXD000001):        {mztab_pass}/{mztab_pass + mztab_fail}")
    print("=" * 70)
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
