"""Plumbing test of scripts/skill_selftest.py without the statistical packages.

The executors that need pydeseq2, patsy, or inmoose are replaced by small
t-test fakes. Each fake first checks its keyword arguments against the real
tool's signature, read from the source with ``ast``, so a renamed or missing
argument in the self-test fails here. Pure-pandas steps (proteomics
preprocessing, pseudobulk aggregation, log-CPM) run for real.
"""

import ast
import os
import re
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools import native  # noqa: E402

FAKED = {
    "tools.deseq2_tools:run_deseq2_analysis",
    "tools.limma_tools:run_limma_analysis",
    "tools.multigroup_tools:run_multigroup_analysis",
    "tools.methylation_tools:run_methylation_da",
}


def signature(spec: str) -> tuple[set[str], set[str]]:
    """(all parameter names, required parameter names) of the real function."""
    module, function = spec.split(":")
    tree = ast.parse((ROOT / (module.replace(".", "/") + ".py")).read_text(encoding="utf-8"))
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == function)
    names = [a.arg for a in node.args.args]
    required = set(names[: len(names) - len(node.args.defaults)])
    return set(names), required


def checked(spec, fake):
    names, required = signature(spec)

    def wrapper(**kwargs):
        unknown = set(kwargs) - names
        missing = required - set(kwargs)
        if unknown or missing:
            raise AssertionError(f"{spec}: unknown={sorted(unknown)} missing={sorted(missing)}")
        return fake(**kwargs)
    wrapper.__name__ = spec.split(":")[1]
    return wrapper


def _test(matrix: pd.DataFrame, treat: list[str], ctrl: list[str], pairs=None) -> pd.DataFrame:
    if pairs:
        diff = np.stack([matrix[t].to_numpy() - matrix[c].to_numpy() for t, c in pairs], axis=1)
        stat, p = stats.ttest_1samp(diff, 0.0, axis=1)
        lfc = diff.mean(axis=1)
    else:
        stat, p = stats.ttest_ind(matrix[treat], matrix[ctrl], axis=1, equal_var=False)
        lfc = matrix[treat].mean(axis=1) - matrix[ctrl].mean(axis=1)
    p = np.nan_to_num(np.asarray(p, dtype=float), nan=1.0)
    order = np.argsort(p)
    ranked = p[order] * len(p) / (np.arange(len(p)) + 1)
    padj = np.empty_like(p)
    padj[order] = np.minimum.accumulate(ranked[::-1])[::-1].clip(max=1.0)
    return pd.DataFrame({"log2FoldChange": np.asarray(lfc), "stat": np.asarray(stat), "pvalue": p,
                         "padj": padj}, index=matrix.index)


def _write(table: pd.DataFrame, output_dir: str, name: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"DEG_results_{name}.csv")
    table.to_csv(path)
    return path


def fake_deseq2(counts_csv, metadata_csv, design_column, control_group, treatment_group,
                output_dir="./output", covariate_columns="", interaction_terms=""):
    counts = pd.read_csv(counts_csv, index_col=0)
    meta = pd.read_csv(metadata_csv, index_col=0)
    log_cpm = np.log2(counts / counts.sum() * 1e6 + 1)
    ctrl = meta.index[meta[design_column] == control_group].tolist()
    treat = meta.index[meta[design_column] == treatment_group].tolist()
    pairs = None
    if covariate_columns:
        block = covariate_columns.split(",")[0].strip()
        pairs = [(t, next(c for c in ctrl if meta.loc[c, block] == meta.loc[t, block])) for t in treat]
    _write(_test(log_cpm, treat, ctrl, pairs), output_dir, f"{treatment_group}_vs_{control_group}")
    return "DESeq2 analysis complete (fake)"


def fake_limma(normalized_csv, metadata_csv, design_column, control_group, treatment_group,
               output_dir="./output", design_formula="", coefficient="", covariate_columns="",
               interaction_terms=""):
    expr = pd.read_csv(normalized_csv, index_col=0)
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta = meta.loc[[s for s in meta.index if s in expr.columns]]
    ctrl = meta.index[meta[design_column] == control_group].tolist()
    treat = meta.index[meta[design_column] == treatment_group].tolist()
    pairs = None
    block = re.search(r"C\((\w+)\)", design_formula or "")
    if block:
        key = block.group(1)
        pairs = [(t, next(c for c in ctrl if meta.loc[c, key] == meta.loc[t, key])) for t in treat
                 if any(meta.loc[c, key] == meta.loc[t, key] for c in ctrl)]
    _write(_test(expr, treat, ctrl, pairs), output_dir, f"{treatment_group}_vs_{control_group}")
    return "limma analysis complete (fake)"


def fake_multigroup(expression_csv, metadata_csv, plan, output_dir):
    expr = pd.read_csv(expression_csv, index_col=0)
    meta = pd.read_csv(metadata_csv, index_col=0)
    results = []
    for contrast in plan["contrasts"]:
        levels = {re.search(r"\[(?:T\.)?(.+)\]", k).group(1): v for k, v in contrast["coefficients"].items()}
        column = re.search(r"C\((\w+)\)", next(iter(contrast["coefficients"]))).group(1)
        plus = [lv for lv, v in levels.items() if v > 0][0]
        minus = [lv for lv, v in levels.items() if v < 0][0]
        treat = meta.index[meta[column] == plus].tolist()
        ctrl = meta.index[meta[column] == minus].tolist()
        path = _write(_test(expr, treat, ctrl), output_dir, contrast["name"])
        results.append({"name": contrast["name"], "path": path})
    return {"analysis_type": plan["analysis_type"], "results": results}


def fake_methylation(beta_matrix_csv, metadata_csv, design_column, control_group, treatment_group,
                     output_dir="./output", beta_offset=1e-3):
    m_path = os.path.join(output_dir, "mvalues.csv")
    native.beta_to_m(beta_matrix_csv, m_path, offset=beta_offset)
    fake_limma(m_path, metadata_csv, design_column, control_group, treatment_group, output_dir)
    return "Differential methylation (fake)"


FAKES = {
    "tools.deseq2_tools:run_deseq2_analysis": fake_deseq2,
    "tools.limma_tools:run_limma_analysis": fake_limma,
    "tools.multigroup_tools:run_multigroup_analysis": fake_multigroup,
    "tools.methylation_tools:run_methylation_da": fake_methylation,
}


class SelfTestPlumbing(unittest.TestCase):
    def test_every_route_passes_with_signature_checked_fakes(self):
        selftest = runpy.run_path(str(ROOT / "scripts" / "skill_selftest.py"))
        real_load = native.load_tool

        def load(spec):
            return checked(spec, FAKES[spec]) if spec in FAKED else real_load(spec)

        with tempfile.TemporaryDirectory() as tmp, patch.object(native, "load_tool", side_effect=load):
            code = selftest["main"](["--out", str(Path(tmp) / "run")])
            report = __import__("json").loads((Path(tmp) / "run" / "selftest_report.json").read_text())
        statuses = {r["route"]: r["status"] for r in report["routes"]}
        self.assertEqual(code, 0, report)
        self.assertEqual({k: v for k, v in statuses.items() if k != "gsea_and_ora"},
                         {"deseq2_paired_blocking": "PASS", "limma_fpkm_log2": "PASS",
                          "limma_multilevel": "PASS", "methylation_beta_to_m": "PASS",
                          "proteomics_label_free": "PASS", "single_cell_paired_pseudobulk": "PASS"}, report)
        self.assertEqual(report["checks"]["decision_contract"]["errors"], [])
        self.assertEqual(report["checks"]["external_llm_attempts"], 0)
        self.assertNotEqual(report["checks"]["audit"].get("verdict"), "fail", report["checks"]["audit"])

    def test_signatures_are_read_from_source(self):
        names, required = signature("tools.limma_tools:run_limma_analysis")
        self.assertIn("design_formula", names)
        self.assertEqual(required, {"normalized_csv", "metadata_csv", "design_column",
                                    "control_group", "treatment_group"})


if __name__ == "__main__":
    unittest.main()
