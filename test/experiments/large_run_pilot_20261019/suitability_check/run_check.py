"""Suitability report + joint-model contrasts on three papers from the large run.

Compares each planned contrast fitted once on all samples (tools.joint_contrasts)
with the earlier two-arm fit and with the paper's DEG count, under the same
threshold the run applied. Writes suitability/ and joint/ per case and results.csv.

Run (repository root):  python test/experiments/large_run_pilot_20261019/suitability_check/run_check.py
"""

import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import pandas as pd

from tools import joint_contrasts as jc
from tools import native
from tools import suitability as su

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs_claude"

CASES = [
    {"case": "GSE308674", "dir": RUNS / "PMID41314005/GSE308674", "organism": "Mouse",
     "factors": ["grp"], "references": {"grp": "C"}, "covariates": ["batch"],
     "threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 0.5},
     "planned": {"grp_H_vs_C": ("H_vs_C", 474), "grp_HM_vs_C": ("HM_vs_C", 414),
                 "grp_L_vs_C": ("L_vs_C", 857), "grp_M_vs_C": ("M_vs_C", 40)}},
    {"case": "GSE164798", "dir": RUNS / "521e147b373c7ea5b57c74f077556ddee2985440/GSE164798", "organism": "Mouse",
     "factors": ["genotype", "activity"], "references": {"activity": "sed"}, "covariates": [],
     "threshold": {"metric": "padj", "cutoff": 0.05},
     "planned": {}},
    {"case": "GSE255280", "dir": RUNS / "53b3c29043c2380447afdb1b84c69d28ac523f4f/case_01", "organism": "Mouse",
     "factors": ["geno", "ex"], "references": {"geno": "veh", "ex": "ctrl"}, "covariates": [],
     "threshold": {"metric": "padj", "cutoff": 0.05},
     "planned": {"ex_ex_vs_ctrl_geno-veh": ("vehicle_ex_vs_ctrl", 989), "ex_ex_vs_ctrl_geno-ko": ("ko_ex_vs_ctrl", 517)}},
]


def old_count(case_dir: Path, sub: str, th: dict):
    hits = [p for p in glob.glob(str(case_dir / "results" / sub / "DEG_results_*.csv")) if "GSEA" not in p
            and "_GO_" not in p and "KEGG" not in p]
    return native.apply_threshold(hits[0], **th)["n_significant"] if hits else None


rows = []
for c in CASES:
    out = HERE / c["case"]
    meta = pd.read_csv(c["dir"] / "aligned/design_metadata.csv", index_col=0)
    matrix = c["dir"] / "aligned/aligned_matrix.csv"
    rep = su.report(case_id=c["case"], matrix_type="raw counts", metadata=meta, factors=c["factors"],
                    matrix_csv=matrix, organism=c["organism"], references=c["references"],
                    covariate_candidates=c["covariates"] or None, out_dir=out / "suitability")
    print(c["case"], rep["verdict"], rep["failed"], rep["warnings"], len(rep["comparisons"]), "comparisons")
    meta_path = out / "design_metadata.csv"
    meta.to_csv(meta_path)
    joint = jc.run_joint_deseq2(str(matrix), str(meta_path), rep["comparisons"], str(out / "joint"),
                                covariates=c["covariates"])
    within = {x["name"]: x["within"] for x in rep["comparisons"]}
    for r in joint["results"]:
        r["within"] = within[r["name"]]
        n = native.apply_threshold(r["path"], **c["threshold"])["n_significant"]
        sub, paper = c["planned"].get(r["name"], (None, None))
        if c["case"] == "GSE164798" and r["kind"] == "simple" and r["name"].startswith("activity_"):
            full = {"acu": "acute", "chr": "chronic", "sed": "sed"}
            g = r["within"]["genotype"] if "within" in r else r["name"].rsplit("-", 1)[1]
            a, b = full[r["name"].split("_")[1]], full[r["name"].split("_vs_")[1].split("_")[0]]
            sub = next((x for x in (f"{g}_{a}_vs_{g}_{b}", f"{g}_{b}_vs_{g}_{a}")
                        if (c["dir"] / "results" / x).exists()), None)
        old = old_count(c["dir"], sub, c["threshold"]) if sub else None
        rows.append({"case": c["case"], "comparison": r["name"], "kind": r["kind"],
                     "planned": bool(c["planned"].get(r["name"])), "joint_n_deg": n,
                     "two_arm_n_deg": old, "paper_n_deg": paper, "n_samples_joint": joint["n_samples"]})
pd.DataFrame(rows).to_csv(HERE / "results.csv", index=False)
print(pd.DataFrame(rows).to_string())
