"""DESeq2 apeglm LFC shrinkage, added after the 2026-10-19 large-run pilot (GSE283493's
authors thresholded apeglm-shrunken log2FC; the tool only wrote the MLE)."""
import numpy as np
import pandas as pd
import pytest

from tools.deseq2_tools import run_deseq2_analysis


def _write(tmp_path, with_batch):
    rng = np.random.default_rng(1)
    samples = [f"S{i}" for i in range(8)]
    counts = pd.DataFrame(rng.negative_binomial(5, 0.05, (1500, 8)),
                          index=[f"g{i}" for i in range(1500)], columns=samples)
    counts.iloc[:150, 4:] *= 4  # up in the treatment arm
    # Control name sorts AFTER the treatment, so the reference level must be set explicitly.
    meta = pd.DataFrame({"group": ["zsham"] * 4 + ["exercise"] * 4,
                         "batch": ["b1", "b2"] * 4}, index=samples)
    counts.to_csv(tmp_path / "counts.csv")
    meta.to_csv(tmp_path / "meta.csv")
    args = {"counts_csv": str(tmp_path / "counts.csv"), "metadata_csv": str(tmp_path / "meta.csv"),
            "design_column": "group", "control_group": "zsham", "treatment_group": "exercise",
            "output_dir": str(tmp_path / "out")}
    if with_batch:
        args["covariate_columns"] = "batch"
    return args


@pytest.mark.parametrize("with_batch", [False, True])
def test_shrunk_lfc_written_beside_mle(tmp_path, with_batch):
    out = run_deseq2_analysis.invoke(_write(tmp_path, with_batch))
    assert "completed successfully" in out, out
    assert "apeglm" in out and "skipped" not in out
    res = pd.read_csv(next((tmp_path / "out").glob("DEG_results_*.csv")), index_col=0)
    up, null = res.loc[[f"g{i}" for i in range(150)]], res.drop([f"g{i}" for i in range(150)])
    # Treatment vs control direction, MLE kept, shrinkage pulls toward 0 but keeps the true signal.
    assert up["log2FoldChange"].median() > 1.5
    assert up["log2FoldChange_shrunk"].median() > 1.0
    assert (res["log2FoldChange_shrunk"].abs() <= res["log2FoldChange"].abs() + 1e-6).mean() > 0.95
    assert null["log2FoldChange_shrunk"].abs().median() < null["log2FoldChange"].abs().median()
