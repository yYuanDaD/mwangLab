"""Rebuild three finished large-run papers as case specs, to check that tools/case_runner.py
reproduces their numbers from the same decisions.

The gate decisions (final, reasoning, confidence, locator, candidates) are copied from each
paper's committed decisions.json; only the mechanical parts (alignment rules, executor calls)
are written out here, from the paper's driver scripts. Computed fields in the old records
(alignment counts, suitability, design check, outputs) are left out: the runner recomputes them.

    python test/experiments/case_runner_validation_20261028/make_specs.py --pdf-root E:/agent/mwangLab_pdf
"""

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "large_run_pilot_20261019" / "runs_claude"
COMPUTED = {"suitability", "design_check", "confounding", "profile", "outputs", "applied_counts",
            "n_deg_paper_rule", "results", "comparison", "paper_gene_check", "levels"}


def old_gates(paper: str, case_dir: str) -> dict:
    records = json.loads((RUNS / paper / case_dir / "decisions.json").read_text(encoding="utf-8"))
    gates = {}
    for r in records:
        if r["stage"] in ("execution", "enrichment"):
            continue
        gates[r["stage"]] = {
            "final": {k: v for k, v in r["final"].items() if k not in COMPUTED},
            "reasoning": r["reasoning"], "confidence": r["confidence"], "candidates": r.get("candidates") or [],
            **({"locator": r["paper"]["locator"]} if (r.get("paper") or {}).get("locator") else {}),
        }
    return gates


def gate(gates: dict, stage: str, **extra) -> dict:
    g = dict(gates[stage])
    if stage in ("alignment", "matrix"):  # runner recomputes everything but the reasoning
        g["final"] = {}
    g.update(extra)
    return g


def gse293221(root: str) -> dict:
    g = old_gates("PMID41787055", "GSE293221")
    eff = math.log2(1.5)
    pair = lambda name, ctrl, trt: {  # noqa: E731
        "name": name, "tool": "tools.deseq2_tools:run_deseq2_analysis", "role": "primary" if trt == "EX" else "secondary",
        "args": {"design_column": "grp", "control_group": ctrl, "treatment_group": trt, "alpha": 0.05},
        "reasoning": f"{trt} vs {ctrl}, two-arm DESeq2 as the paper's group-pairwise tests"}
    return {
        "case_id": "GSE293221", "accession": "GSE293221",
        "inputs": {"paper": [f"{root}/test/experiments/paper_screen_20261019/papers/PMC13076624.paper.md"],
                   "metadata": f"{root}/data/GSE293221/GSE293221_metadata.csv", "raw_tar": True},
        "gates": {
            "paper_reconstruction": g["paper_reconstruction"], "ownership": g["ownership"],
            "alignment": gate(g, "alignment", patterns={"grp": ["title", r"^(Control|Exercise|Nexrutine), rep\d$"]},
                              recode={"grp": {"Control": "CON", "Exercise": "EX", "Nexrutine": "PHAM"}}),
            "matrix": gate(g, "matrix", matrix_type="raw counts", recommended_method="DESeq2"),
            "design": gate(g, "design", factors=["grp"], references={"grp": "CON"}, organism="Mouse",
                           planned=["grp_EX_vs_CON", "grp_PHAM_vs_CON"]),
            "covariance": gate(g, "covariance", confounding_candidates=["description"]),
            "method": g["method"], "threshold": g["threshold"],
            "study": gate(g, "study", paper_counts={"grp_EX_vs_CON": 32, "grp_PHAM_vs_CON": 176,
                                                    "joint/grp_EX_vs_CON": 32, "joint/grp_PHAM_vs_CON": 176},
                          paper_genes={"grp_EX_vs_CON": ["Lipe", "Plin1", "Slc7a10", "Dgat2l6", "Lman1l", "Bb123696"]}),
        },
        "executions": [pair("grp_EX_vs_CON", "CON", "EX"), pair("grp_PHAM_vs_CON", "CON", "PHAM"),
                       {"name": "joint", "tool": "tools.joint_contrasts:run_joint_deseq2", "args": {"comparisons": "all"},
                        "role": "sensitivity", "reasoning": "one DESeq2 model ~ grp on all 9 samples"}],
        "enrichment": [{"execution": "grp_EX_vs_CON", "reasoning": "paper reports GO and gene-set enrichment (FIG3C-D)"}],
        "_expected": {"grp_EX_vs_CON": 385, "grp_PHAM_vs_CON": 2589, "joint/grp_EX_vs_CON": 32},
        "_effect_cutoff": eff,
    }


def gse164890(root: str) -> dict:
    g = old_gates("PMID35456380", "GSE164890")
    return {
        "case_id": "GSE164890", "accession": "GSE164890",
        "inputs": {"paper": [f"{root}/test/experiments/paper_screen_20261019/papers/PMC9027771.paper.md"],
                   "metadata": f"{root}/data/GSE164890/GSE164890_metadata.csv",
                   "matrix": f"{root}/data/GSE164890/GSE164890_rsem.genes.counts.tsv.gz"},
        "gates": {
            "paper_reconstruction": g["paper_reconstruction"], "ownership": g["ownership"],
            "alignment": gate(g, "alignment", key_column="description",
                              aliases={"time": "characteristics_ch1.1.time point"},
                              patterns={"subject": ["description", r"^(\d)(?:before|after)$"]},
                              recode={"time": {"before exercise": "pre", "after exercise": "post"},
                                      "subject": {str(i): f"d{i}" for i in range(1, 8)}}),
            "matrix": gate(g, "matrix", matrix_type="estimated counts (RSEM expected counts)",
                           recommended_method="DESeq2 on rounded counts"),
            "design": gate(g, "design", factors=["time"], references={"time": "pre"}, subject="subject",
                           organism="Human", planned=["time_post_vs_pre"]),
            "covariance": g["covariance"],
            "method": gate(g, "method", transform="round"),
            "threshold": g["threshold"],
            "study": gate(g, "study", paper_counts={"time_post_vs_pre": 4058}),
        },
        "executions": [{"name": "time_post_vs_pre", "tool": "tools.deseq2_tools:run_deseq2_analysis",
                        "args": {"design_column": "time", "control_group": "pre", "treatment_group": "post",
                                 "covariate_columns": "subject", "alpha": 0.1},
                        "role": "primary", "reasoning": "DESeq2 ~ subject + time on rounded RSEM counts (author script)"}],
        "enrichment": [{"execution": "time_post_vs_pre", "ora": False, "gsea": True,
                        "reasoning": "paper ran GSEA on the DESeq2 ranking"}],
        "_expected": {"time_post_vs_pre": 4243},
    }


def gse273041(root: str) -> dict:
    g = old_gates("PMID40069235", "case_01")
    design = g["design"]["final"]
    # combine joins the recoded diet/time values
    tgrp = {f"{d}_{t}": ("BL" if t == "BL" else f"{d}_{t}") for d in ("HC", "LC") for t in ("BL", "H0", "H2")}
    plan = {"analysis_type": "repeated_multilevel", "formula": design["formula"], "contrasts": design["contrasts"]}
    return {
        "case_id": "case_01", "accession": "GSE273041",
        "inputs": {"paper": [f"{root}/test/experiments/paper_screen_20261019/papers/PMC11897176.paper.md"],
                   "metadata": f"{root}/data/GSE273041/GSE273041_metadata.csv",
                   "matrix": f"{root}/data/GSE273041/GSE273041_raw_counts.txt.gz"},
        "gates": {
            "paper_reconstruction": g["paper_reconstruction"], "ownership": g["ownership"],
            "alignment": gate(g, "alignment", key_column="description",
                              aliases={"diet": "characteristics_ch1.2.diet", "time": "characteristics_ch1.3.timepoint"},
                              patterns={"subject": ["characteristics_ch1.1.participant id", r"^(\d+)_(?:Base|IP|IP120|IP20)$"]},
                              combine={"tgrp": ["diet", "time"]},
                              recode={"diet": {"HiCarb": "HC", "LowCarb": "LC"},
                                      "time": {"Base": "BL", "IP": "H0", "IP120": "H2"}, "tgrp": tgrp}),
            "matrix": gate(g, "matrix", matrix_type="RPKM (linear, filtered/floored by submitter)",
                           recommended_method="limma on log2(RPKM+1)"),
            "design": gate(g, "design", factors=["tgrp"], references={"tgrp": "BL"}, subject="subject",
                           organism="Human", planned=["tgrp_HC_H0_vs_BL", "tgrp_HC_H2_vs_BL",
                                                      "tgrp_LC_H0_vs_BL", "tgrp_LC_H2_vs_BL"]),
            "covariance": g["covariance"],
            "method": gate(g, "method", transform="log2(x+1)"),
            "threshold": g["threshold"],
            "study": gate(g, "study", paper_counts={"limma/HC_H0_vs_BL": 330, "limma/HC_H2_vs_BL": 222,
                                                    "limma/LC_H0_vs_BL": 161, "limma/LC_H2_vs_BL": 193}),
        },
        "executions": [{"name": "limma", "tool": "tools.multigroup_tools:run_multigroup_analysis", "args": {"plan": plan},
                        "role": "primary", "reasoning": "one limma model ~ subject + tgrp over all 60 samples"}],
        "enrichment": [{"execution": "limma/HC_H0_vs_BL", "reasoning": "paper's pathway analysis per diet and time"}],
        "_expected": {"limma/HC_H0_vs_BL": 311, "limma/HC_H2_vs_BL": 287, "limma/LC_H0_vs_BL": 299,
                      "limma/LC_H2_vs_BL": 399},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-root", default="E:/agent/mwangLab_pdf", help="checkout holding data/ and the paper files")
    ap.add_argument("--out", default=str(HERE / "runs"))
    args = ap.parse_args()
    expected = {}
    for build, paper in ((gse293221, "PMID41787055"), (gse164890, "PMID35456380"), (gse273041, "PMID40069235")):
        case = build(args.pdf_root.rstrip("/"))
        expected[paper] = case.pop("_expected")
        case.pop("_effect_cutoff", None)
        run_dir = Path(args.out) / paper
        run_dir.mkdir(parents=True, exist_ok=True)
        spec = {"run_dir": str(run_dir), "decision_maker": "validation: decisions copied from the 2026-10 large run",
                "request": f"Re-run {paper} through tools/case_runner.py with its recorded decisions",
                "platform": "case_runner_validation", "cases": [case]}
        (run_dir / "case_spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
        print(run_dir / "case_spec.json")
    (Path(args.out) / "expected.json").write_text(json.dumps(expected, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
