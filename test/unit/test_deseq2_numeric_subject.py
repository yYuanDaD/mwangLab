"""Numeric subject IDs passed as a covariate must be a categorical block, not a slope.

GSE308252 (2026-10-25 large run): subject IDs 1..9 were read as int64 and fitted as one
continuous covariate, which silently unpaired the design (1,105 vs 2,819 DEGs)."""
import numpy as np
import pandas as pd

from tools.deseq2_tools import run_deseq2_analysis


def _run(tmp_path, subjects, name):
    rng = np.random.default_rng(3)
    n_sub = 6
    samples = [f"S{i}" for i in range(2 * n_sub)]
    # Strong per-subject level, modest time effect: only a subject block finds it.
    subject_level = rng.gamma(2.0, 2.0, size=(1, n_sub))
    base = rng.gamma(2.0, 50.0, size=(800, 1)) * np.repeat(subject_level, 2, axis=1)
    base[:80, 1::2] *= 1.8
    counts = pd.DataFrame(rng.poisson(base), index=[f"g{i}" for i in range(800)], columns=samples)
    meta = pd.DataFrame({"time": ["pre", "post"] * n_sub, "subject": subjects}, index=samples)
    d = tmp_path / name
    d.mkdir()
    counts.to_csv(d / "counts.csv")
    meta.to_csv(d / "meta.csv")
    out = run_deseq2_analysis.invoke({
        "counts_csv": str(d / "counts.csv"), "metadata_csv": str(d / "meta.csv"),
        "design_column": "time", "control_group": "pre", "treatment_group": "post",
        "output_dir": str(d / "out"), "covariate_columns": "subject"})
    assert "completed successfully" in out, out
    return pd.read_csv(next((d / "out").glob("DEG_results_*.csv")), index_col=0)


def test_numeric_subject_ids_are_blocks(tmp_path):
    ids = [i // 2 + 1 for i in range(12)]
    numeric = _run(tmp_path, ids, "numeric")
    labelled = _run(tmp_path, [f"p{i}" for i in ids], "labelled")
    pd.testing.assert_series_equal(numeric["padj"].sort_index(), labelled["padj"].sort_index(),
                                   check_names=False, atol=1e-8)
