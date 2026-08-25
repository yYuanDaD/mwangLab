"""Freeze the 20-study x 3-repeat full-pipeline stability benchmark."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.batch_tools import _find_expression_file  # noqa: E402
from tools.evidence import file_sha256  # noqa: E402


CASE_SPECS = [
    {"accession": "GSE117161", "organism": "Mouse", "treatment_keywords": ["high", "moderate"], "control_keywords": ["basal"], "expected_matrix": "GSE117161_RNA-seq_raw_counts_Exercise_performance_project.csv.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.2.running protocole", "expected_control": "Basal", "expected_treatments": ["High", "Moderate"], "expected_n_contrasts": 2, "expected_min_aligned": 18},
    {"accession": "GSE130401", "organism": "Human", "treatment_keywords": ["trametinib"], "control_keywords": ["dmso"], "expected_matrix": "GSE130401_YAPstudy.FPKM.rsem.Calibrated.txt.gz", "expected_matrix_type": "fpkm_or_tpm", "expected_method": "limma", "expected_design": "characteristics_ch1.2.treatment", "expected_control": "0.01% DMSO", "expected_treatments": ["20 nM Trametinib"], "expected_n_contrasts": 1, "expected_min_aligned": 15},
    {"accession": "GSE132520", "organism": "Mouse", "treatment_keywords": ["exercised"], "control_keywords": ["sedentary"], "expected_matrix": "GSE132520_log2fpkm.csv", "expected_matrix_type": "log_transformed", "expected_method": "limma", "expected_design": "characteristics_ch1.3.treatment", "expected_control": "sedentary", "expected_treatments": ["exercised"], "expected_n_contrasts": 1, "expected_min_aligned": 16},
    {"accession": "GSE163356", "organism": "Human", "treatment_keywords": ["post"], "control_keywords": ["pre"], "expected_matrix": "GSE163356_logCPM.tsv.gz", "expected_matrix_type": "log_transformed", "expected_method": "limma", "expected_design": "characteristics_ch1.4.exercise", "expected_control": "Pre", "expected_treatments": ["Post"], "expected_n_contrasts": 1, "expected_min_aligned": 41},
    {"accession": "GSE164798", "organism": "Mouse", "treatment_keywords": ["acute", "chronic"], "control_keywords": ["sedentary"], "expected_matrix": "GSE164798_Raw_gene_counts_matrix.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.6.treatment synonym", "expected_control": "sedentary", "expected_treatments": ["acute", "chronic"], "expected_n_contrasts": 2, "expected_min_aligned": 24},
    {"accession": "GSE194193", "organism": "Mouse", "treatment_keywords": ["training"], "control_keywords": ["notraining"], "expected_matrix": "GSE194193_counts.csv.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.0.training_state", "expected_control": "noTraining", "expected_treatments": ["Training"], "expected_n_contrasts": 1, "expected_min_aligned": 53},
    {"accession": "GSE208615", "organism": "Mouse", "treatment_keywords": ["14-0-0"], "control_keywords": ["0-0-0"], "expected_matrix": "GSE208615_fpkm.csv.gz", "expected_matrix_type": "fpkm_or_tpm", "expected_method": "limma", "expected_design": "characteristics_ch1.2.exercise parameters", "expected_control": "0-0-0", "expected_treatments": ["14-0-0"], "expected_n_contrasts": 1, "expected_min_aligned": 70},
    {"accession": "GSE266241", "organism": "Mouse", "treatment_keywords": ["aortic cross clamping"], "control_keywords": ["sham"], "expected_matrix": "GSE266241_4hr_Counts.csv", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.2.treatment", "expected_control": "Sham", "expected_treatments": ["Aortic Cross Clamping"], "expected_n_contrasts": 1, "expected_min_aligned": 23},
    {"accession": "GSE270703", "organism": "Human", "treatment_keywords": ["exercised"], "control_keywords": ["sedentary"], "expected_matrix": "GSE270703_merged_from_tar.csv", "expected_matrix_type": "log_transformed", "expected_method": "limma", "expected_design": "characteristics_ch1.1.treatment", "expected_control": "Sedentary", "expected_treatments": ["Exercised"], "expected_n_contrasts": 1, "expected_min_aligned": 10},
    {"accession": "GSE279359", "organism": "Mouse", "treatment_keywords": ["immediately post-exercise"], "control_keywords": ["pre-exercise"], "expected_matrix": "GSE279359_processed_counts.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.1.time", "expected_control": "pre-exercise", "expected_treatments": ["immediately post-exercise"], "expected_n_contrasts": 1, "expected_min_aligned": 20},
    {"accession": "GSE282641", "organism": "Mouse", "treatment_keywords": ["ko"], "control_keywords": ["wt"], "expected_matrix": "GSE282641_rawCounts.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.3.genotype", "expected_control": "wt", "expected_treatments": ["ko"], "expected_n_contrasts": 1, "expected_min_aligned": 64},
    {"accession": "GSE294305", "organism": "Mouse", "treatment_keywords": ["msnba", "methylsulfonyl"], "control_keywords": ["control"], "expected_matrix": "GSE294305_SMX09.unq.refseq.umi.dat.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.1.treatment", "expected_control": "Control", "expected_treatments": ["100 碌M N-[4-(methylsulfonyl)-2-nitrophenyl]-1,3-benzodioxol-5-amine"], "expected_n_contrasts": 1, "expected_min_aligned": 12},
    {"accession": "GSE297707", "organism": "Mouse", "treatment_keywords": ["hiit"], "control_keywords": ["sedentary"], "expected_matrix": "GSE297707_raw_counts.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.2.treatment", "expected_control": "sedentary", "expected_treatments": ["HIIT"], "expected_n_contrasts": 1, "expected_min_aligned": 64},
    {"accession": "GSE302944", "organism": "Mouse", "treatment_keywords": ["ko"], "control_keywords": ["wt"], "expected_matrix": "GSE302944_merged_from_tar.csv", "expected_matrix_type": "fpkm_or_tpm", "expected_method": "limma", "expected_design": "characteristics_ch1.1.genotype", "expected_control": "WT", "expected_treatments": ["KO"], "expected_n_contrasts": 1, "expected_min_aligned": 6},
    {"accession": "GSE308674", "organism": "Mouse", "treatment_keywords": ["hiit"], "control_keywords": ["pbs injection"], "expected_matrix": "GSE308674_gene_counts.csv.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.3.treatment", "expected_control": "PBS injection", "expected_treatments": ["HIIT", "HIIT+MCT1/2 inhibitor"], "expected_n_contrasts": 2, "expected_min_aligned": 28},
    {"accession": "GSE315612", "organism": "Mouse", "treatment_keywords": ["db/db"], "control_keywords": ["db/m"], "expected_matrix": "GSE315612_raw_gene_counts.txt.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.2.genotype", "expected_control": "db/m (wild-type)", "expected_treatments": ["db/db (leptin receptor mutant)"], "expected_n_contrasts": 1, "expected_min_aligned": 12, "expected_alignment_prefix": "llm"},
    {"accession": "GSE315678", "organism": "Mouse", "treatment_keywords": ["cdahfd"], "control_keywords": ["control chow"], "expected_matrix": "GSE315678_mtarc1_mouse_RNA_salmon_quant.txt.gz", "expected_matrix_type": "fpkm_or_tpm", "expected_method": "limma", "expected_design": "characteristics_ch1.2.diet", "expected_control": "Control chow diet", "expected_treatments": ["CDAHFD"], "expected_n_contrasts": 1, "expected_min_aligned": 26},
    {"accession": "GSE316347", "organism": "Mouse", "treatment_keywords": ["pyrodostigmine", "tumor necrosis"], "control_keywords": ["control"], "expected_matrix": "GSE316347_merged_from_tar.csv", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.1.treatment", "expected_control": "control", "expected_treatments": ["Pyrodostigmine Bromide", "Tumor Necrosis Factor-alpha"], "expected_n_contrasts": 2, "expected_min_aligned": 21},
    {"accession": "GSE317978", "organism": "Mouse", "treatment_keywords": ["ko_pbs"], "control_keywords": ["ctr_pbs"], "expected_matrix": "GSE317978_core_table3.csv.gz", "expected_matrix_type": "fpkm_or_tpm", "expected_method": "limma", "expected_design": "characteristics_ch1.1.sample group", "expected_control": "CTR_PBS", "expected_treatments": ["KO_PBS"], "expected_n_contrasts": 1, "expected_min_aligned": 6, "expected_alignment_prefix": "llm"},
    {"accession": "GSE326587", "organism": "Mouse", "treatment_keywords": ["run"], "control_keywords": ["control"], "expected_matrix": "GSE326587_Adler_raw_counts.csv.gz", "expected_matrix_type": "raw_counts", "expected_method": "deseq2", "expected_design": "characteristics_ch1.3.treatment", "expected_control": "Control", "expected_treatments": ["Run"], "expected_n_contrasts": 1, "expected_min_aligned": 28, "expected_alignment_prefix": "llm"},
]


def _commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def build_manifest() -> dict:
    cases = []
    for spec in CASE_SPECS:
        acc = spec["accession"]
        data_dir = ROOT / "data" / acc
        metadata = data_dir / f"{acc}_metadata.csv"
        selected, matrix_type = _find_expression_file(str(data_dir))
        if not selected or not metadata.is_file():
            raise RuntimeError(f"Missing frozen inputs for {acc}: matrix={selected}, metadata={metadata}")
        matrix = Path(selected).resolve()
        if matrix.name != spec["expected_matrix"] or matrix_type != spec["expected_matrix_type"]:
            raise RuntimeError(
                f"Frozen route mismatch for {acc}: {matrix.name}/{matrix_type}; "
                f"expected {spec['expected_matrix']}/{spec['expected_matrix_type']}"
            )
        case = dict(spec)
        case.update({
            "id": acc,
            "matrix_path": str(matrix.relative_to(ROOT)),
            "matrix_sha256": file_sha256(str(matrix)),
            "metadata_path": str(metadata.resolve().relative_to(ROOT)),
            "metadata_sha256": file_sha256(str(metadata)),
        })
        cases.append(case)
    return {
        "schema_version": "1.0",
        "experiment": "full_pipeline_stability_20x3",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "code_commit": _commit(),
        "case_count": len(cases),
        "repeats": 3,
        "trials": len(cases) * 3,
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="output/full_pipeline_stability_20x3_inputs/frozen_manifest.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    if args.dry_run:
        print(json.dumps({
            "status": "pass", "case_count": manifest["case_count"],
            "repeats": manifest["repeats"], "trials": manifest["trials"],
            "matrix_types": {kind: sum(c["expected_matrix_type"] == kind for c in manifest["cases"])
                             for kind in ("raw_counts", "fpkm_or_tpm", "log_transformed")},
        }, indent=2))
        return 0
    output = (ROOT / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())