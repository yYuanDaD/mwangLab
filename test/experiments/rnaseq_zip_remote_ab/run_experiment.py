"""Compare frozen ZIP pairwise inputs with freshly downloaded GEO inputs.

The ZIP is treated as the trusted reference.  Each pairwise matrix is run in its
own isolated cohort because the batch pipeline selects one expression matrix per
accession.  The remote arm runs in a separate workspace with normal GEO download
behavior, so files cannot leak between arms.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[3]
ZIP_ROOT = ROOT / "_rnaseq_benchmark_input"
WORK_ROOT = ROOT / "output" / "rnaseq_zip_remote_ab"

sys.path.insert(0, str(ROOT))

from tools.batch_tools import run_batch_geo_pipeline  # noqa: E402
import tools.batch_tools as batch_tools  # noqa: E402
import tools.enrichment_tools as enrichment_tools  # noqa: E402
from tools.evidence import file_sha256  # noqa: E402


CASES = [
    ("GSE194151_FC_vs_MC", "GSE194151", "FC_vs_MC.rawcount.txt", "FC_vs_MC.metadata.txt", "FC", "MC"),
    ("GSE194151_FH_vs_FC", "GSE194151", "FH_vs_FC.rawcount.txt", "FH_vs_FC.metadata.txt", "FH", "FC"),
    ("GSE194151_FH_vs_MH", "GSE194151", "FH_vs_MH.rawcount.txt", "FH_vs_MH.metadata.txt", "FH", "MH"),
    ("GSE194151_MH_vs_MC", "GSE194151", "MH_vs_MC.rawcount.txt", "MH_vs_MC.metadata.txt", "MH", "MC"),
    ("GSE195482_WMF_vs_WCF", "GSE195482", "WMF_vs_WCF.rawcount.txt", "WMF_vs_WCF.metadata.txt", "WMF", "WCF"),
    ("GSE195482_WMM_vs_WCM", "GSE195482", "WMM_vs_WCM.rawcount.txt", "WMM_vs_WCM.metadata.txt", "WMM", "WCM"),
]


def _clean(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _stage_local(case, workspace: Path) -> dict:
    label, accession, matrix_name, metadata_name, treatment, control = case
    source_dir = ZIP_ROOT / accession
    matrix_src = source_dir / matrix_name
    metadata_src = source_dir / metadata_name
    if not matrix_src.is_file() or not metadata_src.is_file():
        raise FileNotFoundError(f"missing ZIP input for {label}: {matrix_src} / {metadata_src}")
    data_dir = workspace / "data" / accession
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True)
    matrix_dst = data_dir / f"{accession}_frozen.tsv"
    metadata_dst = data_dir / f"{accession}_metadata.csv"
    shutil.copy2(matrix_src, matrix_dst)
    pd.read_csv(metadata_src, sep=None, engine="python").to_csv(metadata_dst, index=False)
    # Preserve the small, human-readable processing recipes shipped with the BO ZIP.
    # The pipeline reads these as bounded provenance evidence; it never executes them.
    for helper in sorted(source_dir.glob("*.r")) + sorted(source_dir.glob("*.py")):
        shutil.copy2(helper, data_dir / helper.name)
    return {
        "matrix": str(matrix_dst),
        "metadata": str(metadata_dst),
        "matrix_sha256": file_sha256(str(matrix_dst)),
        "metadata_sha256": file_sha256(str(metadata_dst)),
    }


def _run_case(case, workspace: Path, output_root: Path, local: bool) -> dict:
    label, accession, _matrix, _metadata, treatment, control = case
    output_root.mkdir(parents=True, exist_ok=True)
    old_cwd = Path.cwd()
    try:
        os.chdir(workspace)
        if local:
            class _NoopDownload:
                def invoke(self, _args):
                    return "LOCAL_FROZEN_INPUT: download skipped."

            batch_tools.download_geo_data = _NoopDownload()
            batch_tools.download_supplementary_files = _NoopDownload()
        result = run_batch_geo_pipeline.invoke({
            "accessions": [accession],
            "organism": "Mouse",
            "treatment_keywords": [treatment],
            "control_keywords": [control],
            "output_base": str(output_root),
            "run_label": label,
            "raw_da_method": "deseq2",
            "llm_datatype": True,
        })
    finally:
        os.chdir(old_cwd)
    return {"label": label, "accession": accession, "local": local, "message": str(result)}


def _summary_row(run_root: Path, label: str) -> dict:
    path = run_root / f"cohort_{label}" / "summary.csv"
    if not path.is_file():
        return {"label": label, "status": "missing_summary"}
    rows = pd.read_csv(path).to_dict(orient="records")
    return rows[0] if rows else {"label": label, "status": "empty_summary"}


def _find_artifact(run_root: Path, label: str, suffix: str) -> Path | None:
    study = run_root / f"cohort_{label}" / next((p.name for p in run_root.glob(f"cohort_{label}/*") if p.is_dir()), "")
    hits = sorted(study.glob(f"*{suffix}")) if study.is_dir() else []
    return hits[0] if hits else None


def _compare_case(local_root: Path, remote_root: Path, label: str) -> dict:
    left = _summary_row(local_root, label)
    right = _summary_row(remote_root, label)
    out = {
        "label": label,
        "local_status": left.get("status", ""),
        "remote_status": right.get("status", ""),
        "local_matrix_type": left.get("matrix_type", ""),
        "remote_matrix_type": right.get("matrix_type", ""),
        "local_da_method": left.get("da_method", ""),
        "remote_da_method": right.get("da_method", ""),
        "local_n_samples": left.get("n_samples", ""),
        "remote_n_samples": right.get("n_samples", ""),
        "local_n_deg": left.get("n_deg", ""),
        "remote_n_deg": right.get("n_deg", ""),
        "local_n_gsea_sig": left.get("n_gsea_sig", ""),
        "remote_n_gsea_sig": right.get("n_gsea_sig", ""),
    }
    for arm, root in (("local", local_root), ("remote", remote_root)):
        deg = _find_artifact(root, label, ".csv")
        gsea = _find_artifact(root, label, "_GSEA_Hallmark.csv")
        out[f"{arm}_deg_file"] = str(deg) if deg else ""
        out[f"{arm}_gsea_file"] = str(gsea) if gsea else ""
    local_deg = Path(out["local_deg_file"]) if out["local_deg_file"] else None
    remote_deg = Path(out["remote_deg_file"]) if out["remote_deg_file"] else None
    if local_deg and remote_deg and local_deg.is_file() and remote_deg.is_file():
        a = pd.read_csv(local_deg, index_col=0)
        b = pd.read_csv(remote_deg, index_col=0)
        def sig(df):
            return set(df.index[df["padj"].notna() & (df["padj"] < .05) & (df["log2FoldChange"].abs() > 1)])
        sa, sb = sig(a), sig(b)
        out["deg_sig_jaccard"] = len(sa & sb) / len(sa | sb) if sa | sb else 1.0
        common = sorted(sa & sb)
        out["deg_sig_overlap"] = len(common)
    return out


def _load_frozen_hallmark_gmt(path: Path) -> dict:
    if not path.is_file():
        url = "https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2024.1.Mm/mh.all.v2024.1.Mm.symbols.gmt"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        path.write_bytes(response.content)
    gmt = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("\t")
        if len(fields) >= 3:
            gmt[fields[0]] = fields[2:]
    if not gmt:
        raise RuntimeError(f"Frozen Hallmark GMT is empty: {path}")
    return gmt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rerun", action="store_true")
    parser.add_argument("--arm", choices=("both", "local", "remote"), default="both")
    args = parser.parse_args()
    local_workspace = WORK_ROOT / "workspace_local"
    remote_workspace = WORK_ROOT / "workspace_remote"
    local_output = WORK_ROOT / "output_local"
    remote_output = WORK_ROOT / "output_remote"
    if args.rerun or not WORK_ROOT.exists():
        if args.arm == "both" or not WORK_ROOT.exists():
            _clean(WORK_ROOT)
        else:
            for p in ((local_workspace, local_output) if args.arm == "local"
                      else (remote_workspace, remote_output)):
                _clean(p)
    for p in (local_workspace, remote_workspace, local_output, remote_output):
        p.mkdir(parents=True, exist_ok=True)

    manifest = {"zip_source": str(ZIP_ROOT), "cases": []}
    frozen_gmt = _load_frozen_hallmark_gmt(WORK_ROOT / "mh.all.v2024.1.Mm.symbols.gmt")
    enrichment_tools._get_hallmark_gmt = lambda _category, _dbver: frozen_gmt
    original_download = (batch_tools.download_geo_data, batch_tools.download_supplementary_files)
    try:
        for case in CASES if args.arm in ("both", "local") else []:
            label = case[0]
            case_workspace = local_workspace / label
            case_workspace.mkdir(parents=True, exist_ok=True)
            frozen = _stage_local(case, case_workspace)
            manifest["cases"].append({"label": label, **frozen})
            _run_case(case, case_workspace, local_output, local=True)
        if args.arm in ("both", "remote"):
            batch_tools.download_geo_data, batch_tools.download_supplementary_files = original_download
            for case in CASES:
                _run_case(case, remote_workspace, remote_output, local=False)
    finally:
        batch_tools.download_geo_data, batch_tools.download_supplementary_files = original_download

    comparisons = [_compare_case(local_output, remote_output, case[0]) for case in CASES]
    (WORK_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    pd.DataFrame(comparisons).to_csv(WORK_ROOT / "comparison.csv", index=False)
    (WORK_ROOT / "comparison.json").write_text(json.dumps(comparisons, indent=2, default=str), encoding="utf-8")
    print(json.dumps(comparisons, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
