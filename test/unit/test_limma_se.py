"""limma lfcSE: inmoose writes the unscaled SD (one constant for every gene); found in the
2026-10-20 large run on GSE273041, where lfcSE was 0.447 for every gene."""
import numpy as np
import pandas as pd

from tools.limma_tools import run_limma_analysis


def test_limma_lfcse_is_per_gene_moderated_se(tmp_path):
    rng = np.random.default_rng(0)
    samples = [f"S{i}" for i in range(8)]
    expr = pd.DataFrame(rng.normal(6, 1, (400, 8)), index=[f"g{i}" for i in range(400)], columns=samples)
    expr.iloc[:40, 4:] += 2
    meta = pd.DataFrame({"group": ["ctrl"] * 4 + ["trt"] * 4}, index=samples)
    expr.to_csv(tmp_path / "expr.csv")
    meta.to_csv(tmp_path / "meta.csv")
    out = run_limma_analysis.invoke({
        "normalized_csv": str(tmp_path / "expr.csv"), "metadata_csv": str(tmp_path / "meta.csv"),
        "design_column": "group", "control_group": "ctrl", "treatment_group": "trt",
        "output_dir": str(tmp_path / "out")})
    res = pd.read_csv(next((tmp_path / "out").glob("DEG_results_*.csv")), index_col=0)
    assert res["lfcSE"].nunique() > 100, out
    assert np.allclose(res["lfcSE"], (res["log2FoldChange"] / res["stat"]).abs())
