"""Backfill explicit exercise.csv for cohorts produced before the 17-table schema.

The new schema represents the ontology-level Exercise node directly:

    gene.exercise_id -> exercise.exercise_id

Older cohorts only had exercise-like rows in interventions.csv. This script derives exercise.csv
from those intervention rows and adds gene.exercise_id while preserving gene.intervention_id.
"""

import os
import sys
from collections import defaultdict

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.sea_cdm_schema import csv_columns
from tools.seacdm_tools import exercise_rows_from_interventions


DEFAULT_COHORTS = [
    "output/agentA_cohort_gene_consistency_chunked_a_0630",
    "output/agentA_cohort_gene_consistency_chunked_b_0630",
    "output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701",
    "output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701",
]


def _csv_dir(cohort_dir: str) -> str:
    cand = os.path.join(cohort_dir, "csv")
    return cand if os.path.isdir(cand) else cohort_dir


def _records(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df.to_dict("records")


def _study_from_experiment(experiment_id: str) -> str:
    if "_exp" in str(experiment_id):
        return str(experiment_id).split("_exp", 1)[0]
    return str(experiment_id or "").strip()


def _is_blank(value) -> bool:
    text = "" if value is None else str(value).strip()
    return not text or text.lower() in {"nan", "none", "<na>"}


def backfill(cohort_dir: str) -> tuple[int, int]:
    csv_dir = _csv_dir(cohort_dir)
    interventions_path = os.path.join(csv_dir, "interventions.csv")
    gene_path = os.path.join(csv_dir, "gene.csv")
    exercise_path = os.path.join(csv_dir, "exercise.csv")

    interventions = _records(interventions_path)
    by_study: dict[str, list[dict]] = defaultdict(list)
    for row in interventions:
        study_id = _study_from_experiment(row.get("experiment_id"))
        if study_id:
            by_study[study_id].append(row)

    exercise_rows = []
    for study_id, rows in sorted(by_study.items()):
        exercise_rows.extend(exercise_rows_from_interventions(
            study_id, {"interventions": rows, "exercise": []}
        ))

    ex_cols = csv_columns("exercise")
    pd.DataFrame(exercise_rows, columns=ex_cols).to_csv(exercise_path, index=False)

    intervention_to_exercise = {
        row.get("intervention_id"): row.get("exercise_id")
        for row in exercise_rows
        if row.get("intervention_id") and row.get("exercise_id")
    }

    updated_gene_rows = 0
    if os.path.isfile(gene_path):
        gene_df = pd.read_csv(gene_path, dtype=str, keep_default_na=False)
        if "exercise_id" not in gene_df.columns:
            insert_at = list(gene_df.columns).index("intervention_id") + 1 if "intervention_id" in gene_df.columns else len(gene_df.columns)
            gene_df.insert(insert_at, "exercise_id", None)
        for idx, row in gene_df.iterrows():
            if _is_blank(row.get("exercise_id")):
                eid = intervention_to_exercise.get(row.get("intervention_id"))
                if eid:
                    gene_df.at[idx, "exercise_id"] = eid
                    updated_gene_rows += 1
        gene_df = gene_df.reindex(columns=csv_columns("gene"))
        gene_df.to_csv(gene_path, index=False)

    return len(exercise_rows), updated_gene_rows


def main() -> None:
    cohorts = sys.argv[1:] or DEFAULT_COHORTS
    for cohort in cohorts:
        n_ex, n_gene = backfill(cohort)
        print(f"{cohort}: exercise rows={n_ex}, gene rows updated={n_gene}")


if __name__ == "__main__":
    main()
