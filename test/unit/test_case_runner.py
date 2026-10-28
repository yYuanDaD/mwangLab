"""Offline test of tools/case_runner.py (inspect + execute) on synthetic GEO-style series.

Covers: inspect (alignment key detection via title), a three-arm DESeq2 case with a joint
sensitivity model, a limma log2(CPM+1) run on a subset, a gene-set gate refused for
non-symbol IDs, a case refused at design, a spec error, and a rerun that moves the first
attempt aside. No network: enrichment is planned but the synthetic IDs are not gene-set
ready, so those records are not_run.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_case_runner.py
"""
import json
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np
import pandas as pd

from tools import case_runner

ROOT = os.path.join("test", "output", "test_case_runner")
shutil.rmtree(ROOT, ignore_errors=True)
DATA = os.path.join(ROOT, "data")
rng = np.random.default_rng(7)


def series(acc, groups, n_genes=500, n_de=40):
    """Counts with columns named by sample title, GEO-like metadata indexed by GSM."""
    d = os.path.join(DATA, acc)
    os.makedirs(d, exist_ok=True)
    base = rng.gamma(2.0, 60.0, n_genes)
    cols, rows = {}, []
    for gi, (label, n) in enumerate(groups):
        fold = np.ones(n_genes)
        if gi == 1:
            fold[:n_de] = 4.0
        for r in range(n):
            mu = base * fold * rng.uniform(0.8, 1.2)
            counts = rng.negative_binomial(10, 10 / (10 + mu))
            title = f"{label}_rep{r + 1}"
            cols[title] = counts
            rows.append({"gsm": f"GSM{900000 + len(rows)}", "title": title,
                         "characteristics_ch1.0.group": label, "characteristics_ch1.1.sex": "male",
                         "data_processing": "featureCounts gene counts"})
    # Illumina probe IDs: not gene-set ready, so planned enrichment is recorded as not_run offline.
    genes = [f"ILMN_{1000000 + i}" for i in range(n_genes)]
    pd.DataFrame(cols, index=pd.Index(genes, name="gene")).to_csv(os.path.join(d, f"{acc}_counts.csv.gz"))
    pd.DataFrame(rows).set_index("gsm").to_csv(os.path.join(d, f"{acc}_metadata.csv"))
    return d


def gate(final=None, reasoning="synthetic", **extra):
    return {"final": final or {}, "reasoning": reasoning, **extra}


def case_spec(acc, *, refuse_design=False):
    rule = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0}
    gates = {
        "paper_reconstruction": gate({"accessions": [acc], "primary_estimand": "EX vs SED",
                                      "planned_contrasts": ["grp_EX_vs_SED"], "paper_threshold": rule}),
        "ownership": gate({"owned": True}),
        "alignment": gate(key_column="title", patterns={"grp": ["title", r"^(SED|EX|DET)_rep\d+$"]}),
        "matrix": gate(matrix_type="raw counts", recommended_method="DESeq2"),
        "design": gate({"analysis_type": "one factor, three levels", "design_column": "grp", "control": "SED",
                        "treatment": "EX", "contrasts": [{"name": "grp_EX_vs_SED", "control": "SED", "treatment": "EX"}]},
                       factors=["grp"], references={"grp": "SED"}, planned=["grp_EX_vs_SED", "grp_DET_vs_SED"]),
        "covariance": gate({"status": "not_required", "blocking_terms": [], "covariates": []}),
        "method": gate({"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp"}),
        "threshold": gate({"paper_threshold": rule, "threshold_source": "paper", "applied_threshold": rule,
                           "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}}),
        "study": gate({"route": "paper_aligned"}, paper_counts={"grp_EX_vs_SED": 40},
                      paper_genes={"grp_EX_vs_SED": ["ILMN_1000000", "ilmn_1000001", "ILMN_1000499", "missing_gene"]}),
    }
    if refuse_design:
        gates["design"] = gate(decision_status="refused", stop_reason="no exercise factor in this series")
        for later in ("covariance", "method", "threshold", "study"):
            gates.pop(later)
    executions = [] if refuse_design else [
        {"name": "grp_EX_vs_SED", "tool": "tools.deseq2_tools:run_deseq2_analysis",
         "args": {"design_column": "grp", "control_group": "SED", "treatment_group": "EX", "alpha": 0.05},
         "role": "primary"},
        {"name": "joint", "tool": "tools.joint_contrasts:run_joint_deseq2", "args": {"comparisons": "planned"},
         "role": "sensitivity"},
        {"name": "limma_EX_SED", "tool": "tools.limma_tools:run_limma_analysis", "transform": "log2(CPM+1)",
         "subset": {"grp": ["SED", "EX"]},
         "args": {"design_column": "grp", "control_group": "SED", "treatment_group": "EX"}, "role": "sensitivity"},
    ]
    return {"case_id": acc, "accession": acc,
            "inputs": {"paper": [], "metadata": os.path.join(DATA, acc, f"{acc}_metadata.csv"),
                       "matrix": os.path.join(DATA, acc, f"{acc}_counts.csv.gz")},
            "gates": gates, "executions": executions,
            "enrichment": [] if refuse_design else [{"execution": "grp_EX_vs_SED", "ora": True, "gsea": True}]}


failures = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


series("GSE900001", [("SED", 4), ("EX", 4), ("DET", 4)])
series("GSE900002", [("SED", 3), ("EX", 3)])

# inspect: finds the counts file and that matrix columns are the metadata titles
info = case_runner.inspect_series("GSE900001", data_root=DATA, download=False)
keys = info["matrices"][0]["alignment_keys"]
check(keys and keys[0]["key"] == "title" and keys[0]["matched"] == 12, f"inspect alignment key: {keys[:1]}")
check("characteristics_ch1.0.group" in info["metadata"]["grouping_columns"], "inspect lists grouping column")

run_dir = os.path.join(ROOT, "run")
os.makedirs(run_dir, exist_ok=True)
spec = {"run_dir": run_dir, "request": "synthetic", "decision_maker": "test", "platform": "test",
        "cases": [case_spec("GSE900001"), case_spec("GSE900002", refuse_design=True)]}
spec_path = os.path.join(run_dir, "case_spec.json")
with open(spec_path, "w") as fh:
    json.dump(spec, fh)

result = case_runner.execute(spec_path)
print(json.dumps({k: result[k] for k in ("run", "validator")}, indent=1, default=str))
c1, c2 = result["cases"]
check(not result["validator"]["errors"], f"decision contract: {result['validator']['records']} records, 0 errors")
check("error" not in c1, f"case 1 ran without error: {c1.get('error')}")
ex = c1.get("executions", {})
n = ex.get("grp_EX_vs_SED", {}).get("grp_EX_vs_SED", {}).get("n")
check(n is not None and 30 <= n <= 45, f"DESeq2 recovers planted DE (40): {n}")
check("joint/grp_DET_vs_SED" in ex.get("joint", {}), f"joint model returns planned contrasts: {list(ex.get('joint', {}))}")
lim = ex.get("limma_EX_SED", {}).get("limma_EX_SED", {})
check(lim.get("n") is not None and lim["n"] > 20, f"limma on a subset ran: {lim}")
look = c1["paper_gene_check"]["grp_EX_vs_SED"]
check(look["missing_gene"] is None and look["ilmn_1000001"]["log2FoldChange"] > 1,
      f"paper gene lookup (case-insensitive, missing reported): {look}")
check(c2.get("stopped", {}).get("stage") == "design", f"case 2 stopped at design: {c2.get('stopped')}")
summary = pd.read_csv(os.path.join(run_dir, "summary.csv"))
check(list(summary["accession"]) == ["GSE900001", "GSE900002"], f"summary accession filled: {list(summary['accession'])}")
check(summary.loc[0, "status"] == "completed" and summary.loc[1, "status"] == "stopped:design",
      f"summary status: {list(summary['status'])}")
decisions = json.load(open(os.path.join(run_dir, "GSE900001", "decisions.json")))
enr = [r for r in decisions if r["stage"] == "enrichment"]
check(len(enr) == 2 and all(r["execution_status"] == "not_run" for r in enr), "enrichment not_run for non-symbol IDs")

# rerun: the first attempt is moved aside, not deleted
result2 = case_runner.execute(spec_path)
prev = result2["previous_attempt"]
check(prev and os.path.exists(os.path.join(prev, "GSE900001", "decisions.json")), f"rerun keeps previous attempt: {prev}")
check(not result2["validator"]["errors"], "rerun validates")

# a broken spec is reported, not run
bad = json.loads(json.dumps(spec))
bad["cases"][0]["gates"].pop("method")
with open(os.path.join(run_dir, "bad_spec.json"), "w") as fh:
    json.dump(bad, fh)
code = case_runner.main(["execute", os.path.join(run_dir, "bad_spec.json")])
check(code == 2, "missing gate is a spec error (exit 2)")

# a bad derived-column pattern is reported with the stage that broke
bad2 = json.loads(json.dumps(spec))
bad2["cases"] = [bad2["cases"][0]]
bad2["cases"][0]["gates"]["alignment"]["patterns"] = {"grp": ["title", r"^(SED|EX)_rep\d+$"]}
with open(os.path.join(run_dir, "bad_pattern.json"), "w") as fh:
    json.dump(bad2, fh)
r3 = case_runner.execute(os.path.join(run_dir, "bad_pattern.json"))
check("did not match every row" in r3["cases"][0].get("error", {}).get("message", ""),
      f"pattern error surfaces: {r3['cases'][0].get('error', {}).get('message', '')[:120]}")

print("\nRESULT:", "FAIL" if failures else "PASS", f"({len(failures)} failed)")
sys.exit(1 if failures else 0)
