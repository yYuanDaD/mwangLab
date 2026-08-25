"""Freeze the six cached-input cases for the full RNA-seq pipeline preflight."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.batch_tools import _auto_detect_contrasts, _find_expression_file  # noqa: E402
from tools.evidence import file_sha256  # noqa: E402


CASE_SPECS = [
    {
        "id": "GSE279359_raw_acute",
        "accession": "GSE279359",
        "organism": "Mouse",
        "treatment_keywords": ["immediately post-exercise"],
        "control_keywords": ["pre-exercise"],
        "expected_matrix": "GSE279359_processed_counts.txt.gz",
        "expected_matrix_type": "raw_counts",
        "expected_method": "deseq2",
        "expected_design": "characteristics_ch1.1.time",
        "expected_control": "pre-exercise",
        "expected_treatments": ["immediately post-exercise"],
        "labels": ["raw_counts", "acute", "substring_alignment"],
    },
    {
        "id": "GSE208615_linear_fpkm",
        "accession": "GSE208615",
        "organism": "Mouse",
        "treatment_keywords": ["14-0-0"],
        "control_keywords": ["0-0-0"],
        "expected_matrix": "GSE208615_fpkm.csv.gz",
        "expected_matrix_type": "fpkm_or_tpm",
        "expected_method": "limma",
        "expected_design": "characteristics_ch1.2.exercise parameters",
        "expected_control": "0-0-0",
        "expected_treatments": ["14-0-0"],
        "labels": ["linear_fpkm", "log2_transform", "limma"],
    },
    {
        "id": "GSE297707_prefix_collision",
        "accession": "GSE297707",
        "organism": "Mouse",
        "treatment_keywords": ["hiit"],
        "control_keywords": ["sedentary"],
        "expected_matrix": "GSE297707_raw_counts.txt.gz",
        "expected_matrix_type": "raw_counts",
        "expected_method": "deseq2",
        "expected_design": "characteristics_ch1.2.treatment",
        "expected_control": "sedentary",
        "expected_treatments": ["HIIT"],
        "expected_min_aligned": 64,
        "labels": ["raw_counts", "prefix_collision", "alignment"],
    },
    {
        "id": "GSE163356_human_logcpm",
        "accession": "GSE163356",
        "organism": "Human",
        "treatment_keywords": ["post"],
        "control_keywords": ["pre"],
        "expected_matrix": "GSE163356_logCPM.tsv.gz",
        "expected_matrix_type": "log_transformed",
        "expected_method": "limma",
        "expected_design": "characteristics_ch1.4.exercise",
        "expected_control": "Pre",
        "expected_treatments": ["Post"],
        "labels": ["human", "log_transformed", "limma"],
    },
    {
        "id": "GSE164798_multi_contrast",
        "accession": "GSE164798",
        "organism": "Mouse",
        "treatment_keywords": ["acute", "chronic"],
        "control_keywords": ["sedentary"],
        "expected_matrix": "GSE164798_Raw_gene_counts_matrix.txt.gz",
        "expected_matrix_type": "raw_counts",
        "expected_method": "deseq2",
        "expected_design": "characteristics_ch1.6.treatment synonym",
        "expected_control": "sedentary",
        "expected_treatments": ["acute", "chronic"],
        "labels": ["raw_counts", "multi_contrast"],
    },
    {
        "id": "GSE326587_semantic_alignment",
        "accession": "GSE326587",
        "organism": "Mouse",
        "treatment_keywords": ["run"],
        "control_keywords": ["control"],
        "expected_matrix": "GSE326587_Adler_raw_counts.csv.gz",
        "expected_matrix_type": "raw_counts",
        "expected_method": "deseq2",
        "expected_design": "characteristics_ch1.3.treatment",
        "expected_control": "Control",
        "expected_treatments": ["Run"],
        "expected_alignment_prefix": "llm",
        "expected_min_aligned": 28,
        "labels": ["raw_counts", "semantic_abbreviation", "llm_alignment"],
    },
]


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def _commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return None


def build_manifest() -> dict:
    cases = []
    problems = []
    for spec in CASE_SPECS:
        accession = spec["accession"]
        data_dir = ROOT / "data" / accession
        metadata = data_dir / f"{accession}_metadata.csv"
        selected_raw, matrix_type = _find_expression_file(str(data_dir))
        selected = Path(selected_raw).resolve() if selected_raw else None
        contrasts = _auto_detect_contrasts(
            str(metadata), spec["treatment_keywords"], spec["control_keywords"]
        ) if metadata.is_file() else []

        expected_contrasts = {
            (spec["expected_design"], spec["expected_control"], value)
            for value in spec["expected_treatments"]
        }
        observed_contrasts = {tuple(item) for item in contrasts}
        if selected is None or selected.name != spec["expected_matrix"]:
            problems.append(
                f"{accession}: selected={selected.name if selected else None}, "
                f"expected={spec['expected_matrix']}"
            )
        if matrix_type != spec["expected_matrix_type"]:
            problems.append(
                f"{accession}: matrix_type={matrix_type}, "
                f"expected={spec['expected_matrix_type']}"
            )
        if observed_contrasts != expected_contrasts:
            problems.append(
                f"{accession}: contrasts={sorted(observed_contrasts)}, "
                f"expected={sorted(expected_contrasts)}"
            )
        if not metadata.is_file():
            problems.append(f"{accession}: missing metadata {metadata}")
            continue
        if selected is None or not selected.is_file():
            continue

        metadata_rows = len(pd.read_csv(metadata, index_col=0))
        case = dict(spec)
        case.update({
            "matrix_path": _relative(selected),
            "matrix_sha256": file_sha256(str(selected)),
            "metadata_path": _relative(metadata),
            "metadata_sha256": file_sha256(str(metadata)),
            "metadata_samples": metadata_rows,
            "expected_n_contrasts": len(expected_contrasts),
            "frozen_contrasts": [
                {"design": design, "control": control, "treatment": treatment}
                for design, control, treatment in sorted(expected_contrasts)
            ],
        })
        cases.append(case)

    if problems:
        raise RuntimeError("Manifest preconditions failed:\n- " + "\n- ".join(problems))
    return {
        "schema_version": "1.0",
        "profile": "full_pipeline_six_case_preflight",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "code_commit": _commit(),
        "case_count": len(cases),
        "acquisition_mode": "frozen_cached_inputs",
        "enrichment_mode": "live",
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="output/full_pipeline_production_gate_inputs/frozen_preflight_manifest.json",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    if not args.dry_run:
        target = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Frozen manifest: {target}")
    print(json.dumps({
        "profile": manifest["profile"],
        "case_count": manifest["case_count"],
        "code_commit": manifest["code_commit"],
        "cases": [case["id"] for case in manifest["cases"]],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

