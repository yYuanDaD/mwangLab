"""Run a larger integration cohort through the production batch entry point.

The repository's cached GEO matrices use author sample labels while GEO
metadata is indexed by GSM.  For this integration test only, metadata rows are
reindexed to the corresponding matrix labels using deterministic title/order
rules.  The original metadata files are restored in a finally block.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.batch_tools import run_batch_geo_pipeline


DATA = ROOT / "data"
OUT = ROOT / "output" / "main_multigroup_batch_20261002"


def _expr_columns(acc: str, filename: str) -> list[str]:
    df = pd.read_csv(DATA / acc / filename, index_col=0, sep=None, engine="python", nrows=20)
    numeric = df.apply(pd.to_numeric, errors="coerce")
    cols = [str(c) for c in df.columns if not numeric[c].isna().all()]
    if acc == "GSE279359":
        cols = [c for c in cols if c.startswith(("B_", "IPE_", "X1hPE_", "X24hPE_"))]
    return cols


def _aligned_metadata(acc: str, expr_cols: list[str]) -> pd.DataFrame:
    meta_path = DATA / acc / f"{acc}_metadata.csv"
    meta = pd.read_csv(meta_path, index_col=0)
    if acc == "GSE117161":
        lookup = {str(v): i for i, v in enumerate(meta["title"].astype(str))}
        order = [lookup[c] for c in expr_cols]
    elif acc == "GSE132520":
        lookup = {str(v): i for i, v in enumerate(meta["title"].astype(str))}
        order = [lookup[c] for c in expr_cols]
    elif acc == "GSE130401":
        # The supplementary matrix abbreviates the same labels used in GEO
        # titles (NLF→DMSO, sgCON→SGCONTROL).
        title_to_i = {str(v): i for i, v in enumerate(meta["title"].astype(str))}
        order = []
        for c in expr_cols:
            if c.startswith("DMSO_"):
                key = "NLF_" + c[len("DMSO_"):]
            elif c.startswith("SGCONTROL_"):
                key = "sgCON_" + c[len("SGCONTROL_"):]
            else:
                key = c
            order.append(title_to_i[key])
    elif acc == "GSE279359":
        # Matrix order is B (pre), IPE (immediate), X1hPE, X24hPE; GEO titles
        # are in the same biological order and five-sample block order.
        order = []
        for prefix in ("pre-exercise", "immediately post-exercise",
                       "1 hour post-exercise", "24 hours post-exercise"):
            block = meta[meta["characteristics_ch1.1.time"].astype(str) == prefix]
            order.extend(block.index.tolist())
        meta = meta.loc[order]
        return meta.set_axis(expr_cols, axis=0)
    else:
        # The cached quantification matrices preserve GEO sample order.
        order = list(range(len(expr_cols)))
    return meta.iloc[order].set_axis(expr_cols, axis=0)


def _plans() -> dict[str, dict]:
    return {
        "GSE117161": {
            "analysis_type": "multigroup",
            "formula": "~ 0 + C(protocol)",
            "derived_columns": {
                "protocol": {"source_column": "characteristics_ch1.2.running protocole", "regex": "(.+)"}
            },
            "contrasts": [
                {"name": "High_vs_Basal", "coefficients": {"C(protocol)[High]": 1, "C(protocol)[Basal]": -1}},
                {"name": "Moderate_vs_Basal", "coefficients": {"C(protocol)[Moderate]": 1, "C(protocol)[Basal]": -1}},
            ],
            "run_gsea": False,
        },
        "GSE132520": {
            "analysis_type": "factorial",
            "formula": "~ C(genotype)*C(exercise)",
            "derived_columns": {
                "genotype": {"source_column": "characteristics_ch1.1.genotype/variation", "regex": "(.+)"},
                "exercise": {"source_column": "characteristics_ch1.3.treatment", "regex": "(.+)"},
            },
            "contrasts": [
                {"name": "Wildtype_vs_Mutant_at_exercised", "coefficients": {
                    "C(genotype)[T.Wildtype]": 1,
                }},
                {"name": "Exercise_effect_in_Wildtype", "coefficients": {
                    "C(exercise)[T.sedentary]": -1,
                    "C(genotype)[T.Wildtype]:C(exercise)[T.sedentary]": -1,
                }},
            ],
            "run_gsea": False,
        },
        "GSE130401": {
            "analysis_type": "multilevel",
            "formula": "~ 0 + C(genotype)",
            "derived_columns": {
                "genotype": {"source_column": "characteristics_ch1.1.genetic alteration", "regex": "(.+)"}
            },
            "contrasts": [
                {"name": "YAP1_KO_vs_Parental", "coefficients": {"C(genotype)[YAP1 gene knockout]": 1, "C(genotype)[Parental cell line]": -1}},
                {"name": "Scrambled_vs_Parental", "coefficients": {"C(genotype)[scrambled sgRNA]": 1, "C(genotype)[Parental cell line]": -1}},
            ],
            "run_gsea": False,
        },
        "GSE279359": {
            "analysis_type": "paired_change",
            "formula": "~ C(sex)",
            "subject_column": "subject",
            "time_column": "characteristics_ch1.1.time",
            "baseline_level": "pre-exercise",
            "followup_levels": ["immediately post-exercise", "1 hour post-exercise", "24 hours post-exercise"],
            "group_column": "sex",
            "derived_columns": {
                "subject": {"source_column": "title", "regex": "((?:Male|Female)\\d+)$"},
                "sex": {"source_column": "title", "regex": "(Male|Female)\\d+$"}
            },
            "contrasts": [
                {"name": "Male_vs_Female_change", "coefficients": {"C(sex)[T.Male]": 1}},
            ],
            "run_gsea": False,
        },
        "GSE315678": {
            "analysis_type": "multilevel",
            "formula": "~ 0 + C(genotype)",
            "derived_columns": {
                "genotype": {"source_column": "characteristics_ch1.1.genotype", "regex": "(.+)"}
            },
            "contrasts": [
                {"name": "Homozygous_KO_vs_WT", "coefficients": {"C(genotype)[Mtarc1 Homozygous KO]": 1, "C(genotype)[WT]": -1}},
                {"name": "Heterozygous_KO_vs_WT", "coefficients": {"C(genotype)[Mtarc1 Heterozygous KO]": 1, "C(genotype)[WT]": -1}},
            ],
            "run_gsea": False,
        },
        "GSE316347": {
            "analysis_type": "multilevel",
            "formula": "~ 0 + C(treatment)",
            "derived_columns": {
                "treatment": {"source_column": "characteristics_ch1.1.treatment", "regex": "(.+)"}
            },
            "contrasts": [
                {"name": "Pyrodostigmine_vs_Control", "coefficients": {"C(treatment)[Pyrodostigmine Bromide]": 1, "C(treatment)[control]": -1}},
                {"name": "TNFa_vs_Control", "coefficients": {"C(treatment)[Tumor Necrosis Factor-alpha]": 1, "C(treatment)[control]": -1}},
            ],
            "run_gsea": False,
        },
    }


def main() -> None:
    plans = _plans()
    matrix_files = {
        "GSE117161": "GSE117161_RNA-seq_raw_counts_Exercise_performance_project.csv.gz",
        "GSE132520": "GSE132520_log2fpkm.csv",
        "GSE130401": "GSE130401_YAPstudy.FPKM.rsem.Calibrated_log2.csv",
        "GSE279359": "GSE279359_processed_counts.txt.gz",
        "GSE315678": "GSE315678_mtarc1_mouse_RNA_salmon_quant_log2.csv",
        "GSE316347": "GSE316347_merged_from_tar.csv",
    }
    originals: dict[str, Path] = {}
    try:
        for acc, filename in matrix_files.items():
            path = DATA / acc / f"{acc}_metadata.csv"
            originals[acc] = path.with_suffix(path.suffix + ".main_test_backup")
            shutil.copy2(path, originals[acc])
            cols = _expr_columns(acc, filename)
            _aligned_metadata(acc, cols).to_csv(path)
        OUT.mkdir(parents=True, exist_ok=True)
        result = run_batch_geo_pipeline.invoke({
            "accessions": list(plans),
            "organism": "Mouse",
            "output_base": str(OUT.parent),
            "run_label": OUT.name.removeprefix("cohort_") if OUT.name.startswith("cohort_") else "main_multigroup_batch_20261002",
            "raw_da_method": "deseq2",
            "llm_datatype": False,
            "design_plans_json": json.dumps(plans, ensure_ascii=False),
        })
        print(result)
    finally:
        for acc, backup in originals.items():
            target = DATA / acc / f"{acc}_metadata.csv"
            if backup.exists():
                shutil.move(str(backup), str(target))


if __name__ == "__main__":
    main()
