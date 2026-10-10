"""Rerun representative historical manual-review cases with explicit plans.

The source inputs are the frozen acquisition from native_codex_blind_50.  We
rebuild sample-ID mappings from labels embedded in the matrix/title metadata,
then run the current production batch entry point.  No external LLM validator
is enabled: these are Codex-reviewed explicit plans, and all refusals remain
refusals when the evidence is insufficient.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.batch_tools import run_batch_geo_pipeline  # noqa: E402


SOURCE = ROOT / "output" / "native_codex_blind_50_20261001T164148Z" / "input"
WORK = ROOT / "output" / "manual_review_rerun_20261002_workspace"
OUT = ROOT / "output" / "manual_review_rerun_20261002"

CASES = {
    "GSE279359": "GSE279359_processed_counts.txt.gz",
    "GSE282641": "GSE282641_rawCounts.txt.gz",
    "GSE302911": "GSE302911_RNA-seq_Count_Matrix_TPM_allconditions.tsv.gz",
    "GSE304653": "GSE304653_CounTable.txt.gz",
    "GSE319603": "GSE319603_All_gene_counts.csv",
    "GSE328094": "GSE328094_counts.txt.gz",
}


def matrix_columns(path: Path) -> list[str]:
    head = pd.read_csv(path, sep=None, engine="python", nrows=1)
    cols = [str(c) for c in head.columns]
    if path.name.startswith("GSE279359"):
        return [c for c in cols if re.match(r"^(B|IPE|X1hPE|X24hPE)_", c)]
    if path.name.startswith("GSE319603"):
        return [c for c in cols if re.match(r"^(HM|C|H)\d+$", c)]
    if path.name.startswith("GSE304653"):
        return [c for c in cols if re.match(r"^[CS][NR]\d+$", c)]
    if path.name.startswith("GSE328094"):
        return [c for c in cols if re.match(r"^(N-A|NC|TS|TSA)\d+$", c)]
    return cols


def source_row_map(acc: str, sample: str, meta: pd.DataFrame) -> int:
    titles = meta["title"].astype(str)
    if acc == "GSE279359":
        sm = re.search(r"_(\d+)([MF])$", sample)
        subject = ("Male" if sm.group(2) == "M" else "Female") + sm.group(1)
        time = {
            "B": "pre-exercise",
            "IPE": "immediately post-exercise",
            "X1hPE": "1 hour post-exercise",
            "X24hPE": "24 hours post-exercise",
        }[sample.split("_")[0]]
        hit = meta[
            (meta["characteristics_ch1.1.time"].astype(str) == time)
            & titles.str.contains(subject, regex=False)
        ]
    elif acc == "GSE282641":
        n = re.search(r"_(\d+)$", sample).group(1)
        hit = meta[titles.str.match(rf".*_{re.escape(n)}$")]
    elif acc == "GSE297707":
        n = re.search(r"_(\d+)$", sample).group(1)
        hit = meta[titles.str.match(rf".*?,\s*{re.escape(n)}$")]
    elif acc == "GSE302911":
        m = re.match(r"(Sedentary|Untrained|Trained)(?:_(\d+h))?(\d+)$", sample)
        state, time, rep = m.groups()
        rep = int(rep)
        if state == "Sedentary":
            hit = meta[titles.str.contains(r"sedentary.*rep\s*" + str(rep), case=False, regex=True)]
        else:
            hit = meta[
                titles.str.contains(rf"(?:^|,\s){state}(?:,|$)", case=False, regex=True)
                & titles.str.contains((time or "") + r" post exercise", case=False, regex=True)
                & titles.str.contains(r"rep\s*" + str(rep), case=False, regex=True)
            ]
    elif acc == "GSE304653":
        cell = "cancer cells (iRFP+)" if sample[0] == "C" else "TME cells (iRFP-)"
        treatment = "Sendentary" if sample[1] == "N" else "Exercise"
        rep = int(sample[2:])
        hit = meta[
            meta["characteristics_ch1.1.cell type"].astype(str).str.lower().eq(cell.lower())
            & titles.str.contains(treatment, case=False, regex=False)
            & titles.str.contains(r"rep\s*" + str(rep) + r"(?:$|[^0-9])", case=False, regex=True)
        ]
    elif acc == "GSE319603":
        prefix = re.match(r"(HM|C|H)", sample).group(1)
        rep = int(re.search(r"(\d+)$", sample).group(1))
        if prefix == "HM":
            group_hit = titles.str.match(r"^high-fat diet with MICT", case=False)
        elif prefix == "H":
            group_hit = titles.str.match(r"^high-fat diet\d", case=False)
        else:
            group_hit = titles.str.match(r"^control\d", case=False)
        hit = meta[group_hit & titles.str.endswith(str(rep))]
    elif acc == "GSE328094":
        label = sample
        hit = meta[titles.str.contains(re.escape(label), case=False, regex=True)]
    else:
        raise ValueError(acc)
    if len(hit) != 1:
        raise RuntimeError(f"{acc}: cannot uniquely map {sample!r}; hits={hit.index.tolist()}")
    return int(meta.index.get_loc(hit.index[0]))


def stage_inputs() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    (WORK / "data").mkdir(parents=True)
    for acc, matrix_name in CASES.items():
        src = SOURCE / acc
        dst = WORK / "data" / acc
        dst.mkdir(parents=True)
        shutil.copy2(src / matrix_name, dst / matrix_name)
        meta = pd.read_csv(src / f"{acc}_metadata.csv", index_col=0)
        cols = matrix_columns(src / matrix_name)
        rows = [source_row_map(acc, c, meta) for c in cols]
        aligned = meta.iloc[rows].copy()
        aligned.index = cols
        if acc == "GSE319603":
            aligned["group"] = aligned["title"].str.extract(
                r"^(control|high-fat diet with MICT|high-fat diet)", expand=False
            )
        if acc == "GSE328094":
            mapping = {
                "control": ("no", "no"),
                "exercise": ("no", "yes"),
                "tumor-bearing": ("yes", "no"),
                "tumor-bearing + exercise": ("yes", "yes"),
            }
            vals = aligned["characteristics_ch1.2.treatment"].astype(str).map(mapping)
            aligned["tumor"] = vals.map(lambda x: x[0])
            aligned["exercise"] = vals.map(lambda x: x[1])
        aligned.to_csv(dst / f"{acc}_metadata.csv")


def plans() -> dict[str, dict]:
    return {
        "GSE279359": {
            "analysis_type": "paired_change",
            "formula": "~ C(sex)",
            "subject_column": "subject",
            "time_column": "characteristics_ch1.1.time",
            "baseline_level": "pre-exercise",
            "followup_levels": ["immediately post-exercise", "1 hour post-exercise", "24 hours post-exercise"],
            "group_column": "sex",
            "derived_columns": {
                "subject": {"source_column": "title", "regex": r"((?:Male|Female)\d+)"},
                "sex": {"source_column": "title", "regex": r"(Male|Female)\d+"},
            },
            "contrasts": [{"name": "Male_vs_Female_change", "coefficients": {"C(sex)[T.Male]": 1}}],
            "run_gsea": False,
        },
        "GSE282641": {
            "analysis_type": "factorial",
            "formula": "~ C(genotype)*C(treatment) + C(zt) + C(sex)",
            "derived_columns": {x: {"source_column": c, "regex": r"(.+)"} for x, c in {
                "genotype": "characteristics_ch1.3.genotype",
                "treatment": "characteristics_ch1.4.treatment",
                "zt": "characteristics_ch1.2.zt",
                "sex": "characteristics_ch1.1.Sex",
            }.items()},
            "contrasts": [
                {"name": "Sedentary_vs_Exercise_in_KO", "coefficients": {"C(treatment)[T.sed]": 1}},
                {"name": "Sedentary_vs_Exercise_in_WT", "coefficients": {"C(treatment)[T.sed]": 1, "C(genotype)[T.wt]:C(treatment)[T.sed]": 1}},
                {"name": "Genotype_by_Exercise_interaction", "coefficients": {"C(genotype)[T.wt]:C(treatment)[T.sed]": 1}},
            ],
            "run_gsea": False,
        },
        "GSE297707": {
            "analysis_type": "factorial",
            "formula": "~ C(genotype)*C(treatment) + C(sex)",
            "derived_columns": {
                "genotype": {"source_column": "characteristics_ch1.1.genotype", "regex": r"(.+)"},
                "treatment": {"source_column": "characteristics_ch1.2.treatment", "regex": r"(.+)"},
                "sex": {"source_column": "title", "regex": r",\s*(M|F),"},
            },
            "contrasts": [
                {"name": "Sedentary_vs_HIIT_in_nTG", "coefficients": {"C(treatment)[T.sedentary]": 1}},
                {"name": "Sedentary_vs_HIIT_in_TG", "coefficients": {"C(treatment)[T.sedentary]": 1, "C(genotype)[T.TG]:C(treatment)[T.sedentary]": 1}},
                {"name": "Genotype_by_HIIT_interaction", "coefficients": {"C(genotype)[T.TG]:C(treatment)[T.sedentary]": 1}},
            ],
            "run_gsea": False,
        },
        "GSE302911": {
            "analysis_type": "multilevel",
            "formula": "~ 0 + C(group)",
            "derived_columns": {"group": {"source_column": "characteristics_ch1.3.treatment", "regex": r"(.+)"}},
            "contrasts": [
                {"name": "Untrained_0h_vs_Sedentary", "coefficients": {"C(group)[untrained 0h post-exercise]": 1, "C(group)[sedentary]": -1}},
                {"name": "Untrained_6h_vs_Sedentary", "coefficients": {"C(group)[untrained 6h post-exercise]": 1, "C(group)[sedentary]": -1}},
                {"name": "Trained_0h_vs_Untrained_0h", "coefficients": {"C(group)[trained 0h post-exercise]": 1, "C(group)[untrained 0h post-exercise]": -1}},
                {"name": "Trained_6h_vs_Untrained_6h", "coefficients": {"C(group)[trained 6h post-exercise]": 1, "C(group)[untrained 6h post-exercise]": -1}},
            ],
            "run_gsea": False,
        },
        "GSE304653": {
            "analysis_type": "factorial",
            "formula": "~ C(cell_type)*C(treatment)",
            "derived_columns": {
                "cell_type": {"source_column": "characteristics_ch1.1.cell type", "regex": r"(.+)"},
                "treatment": {"source_column": "characteristics_ch1.3.treatment", "regex": r"(.+)"},
            },
            "contrasts": [
                {"name": "Sedentary_vs_Exercise_in_Cancer", "coefficients": {"C(treatment)[T.Sedentary]": 1}},
                {"name": "Sedentary_vs_Exercise_in_TME", "coefficients": {"C(treatment)[T.Sedentary]": 1, "C(cell_type)[T.TME cells (iRFP-)]:C(treatment)[T.Sedentary]": 1}},
                {"name": "CellType_by_Exercise_interaction", "coefficients": {"C(cell_type)[T.TME cells (iRFP-)]:C(treatment)[T.Sedentary]": 1}},
            ],
            "run_gsea": False,
        },
        "GSE319603": {
            "analysis_type": "multilevel",
            "formula": "~ 0 + C(group)",
            "derived_columns": {"group": {"source_column": "group", "regex": r"(.+)"}},
            "contrasts": [
                {"name": "HFD_MICT_vs_HFD", "coefficients": {"C(group)[high-fat diet with MICT]": 1, "C(group)[high-fat diet]": -1}},
                {"name": "HFD_vs_Control", "coefficients": {"C(group)[high-fat diet]": 1, "C(group)[control]": -1}},
                {"name": "HFD_MICT_vs_Control", "coefficients": {"C(group)[high-fat diet with MICT]": 1, "C(group)[control]": -1}},
            ],
            "run_gsea": False,
        },
        "GSE328094": {
            "analysis_type": "factorial",
            "formula": "~ C(tumor)*C(exercise)",
            "derived_columns": {
                "tumor": {"source_column": "tumor", "regex": r"(.+)"},
                "exercise": {"source_column": "exercise", "regex": r"(.+)"},
            },
            "contrasts": [
                {"name": "Exercise_effect_without_tumor", "coefficients": {"C(exercise)[T.yes]": 1}},
                {"name": "Exercise_effect_with_tumor", "coefficients": {"C(exercise)[T.yes]": 1, "C(tumor)[T.yes]:C(exercise)[T.yes]": 1}},
                {"name": "Tumor_by_Exercise_interaction", "coefficients": {"C(tumor)[T.yes]:C(exercise)[T.yes]": 1}},
            ],
            "run_gsea": False,
        },
    }


def main() -> None:
    stage_inputs()
    payload = {
        "accessions": list(CASES),
        "organism": "Mouse",
        "treatment_keywords": ["exercise", "ex", "hiit", "run", "sedentary", "control", "tumor", "hfd", "mict"],
        "control_keywords": ["control", "sedentary", "sed", "pre"],
        "output_base": str(OUT.parent),
        "run_label": OUT.name.removeprefix("cohort_"),
        "raw_da_method": "deseq2",
        "llm_datatype": False,
        "llm_contrast_strict": False,
        "design_plans_json": json.dumps(plans(), ensure_ascii=False),
    }
    old = Path.cwd()
    try:
        os.chdir(WORK)
        result = run_batch_geo_pipeline.invoke(payload)
        print(result)
    finally:
        os.chdir(old)


if __name__ == "__main__":
    main()
