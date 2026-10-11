"""Report which workflow gates can run in the current environment.

Usage:
    python <skill_dir>/scripts/preflight.py [--out preflight.json]

Checks the Python version, the repository location and commit, every package
the repository tools import, Rscript (limma-voom only), and that the
external-LLM block works. Prints a JSON report. Exit code 1 means the native
runtime itself cannot load; missing optional packages only disable the gates
that need them.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _repo import find_repo  # noqa: E402

# capability -> (python packages, repository modules)
CAPABILITIES = {
    "native_runtime": (["pandas", "numpy", "pydantic", "dotenv"],
                       ["tools.native", "tools.decision_contract", "tools.model_factory"]),
    "deseq2": (["pydeseq2", "langchain_core"], ["tools.deseq2_tools"]),
    "limma_two_group": (["patsy", "inmoose", "langchain_core"], ["tools.limma_tools"]),
    "limma_multigroup": (["patsy", "inmoose"], ["tools.multigroup_tools"]),
    "edger": (["patsy", "inmoose", "langchain_core"], ["tools.edger_tools"]),
    "limma_voom": (["langchain_core"], ["tools.limma_voom_tools"]),
    "preprocess_and_qc": (["langchain_core", "sklearn", "matplotlib", "seaborn"],
                          ["tools.preprocess_tools", "tools.stats_tools"]),
    "gsea_and_ora": (["gseapy", "mygene", "lxml", "langchain_core"], ["tools.enrichment_tools"]),
    "geo_download": (["GEOparse", "bs4", "requests", "langchain_core"], ["tools.geo_tools"]),
    "single_cell_pseudobulk": (["anndata", "scipy", "langchain_core"], ["tools.scrna_tools"]),
}
INSTALL_NAMES = {"dotenv": "python-dotenv", "sklearn": "scikit-learn", "bs4": "beautifulsoup4",
                 "langchain_core": "langchain-core"}


def _missing(packages: list[str]) -> list[str]:
    return [p for p in packages if importlib.util.find_spec(p) is None]


def _import_errors(modules: list[str]) -> dict[str, str]:
    errors = {}
    for module in modules:
        try:
            importlib.import_module(module)
        except Exception as exc:  # report every failure, keep checking
            errors[module] = f"{type(exc).__name__}: {exc}"
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, help="also write the report to this file")
    args = parser.parse_args()

    root = find_repo()
    report: dict = {
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 10),
        "python_recommended": ">=3.12",
        "os": platform.platform(),
        "repo_root": str(root) if root else None,
    }
    if root is None:
        report["error"] = ("mwangLab repository not found; run from inside it or set MWANGLAB_ROOT "
                           "(see references/setup.md)")
        print(json.dumps(report, indent=2))
        return 1
    sys.path.insert(0, str(root))
    try:
        report["repo_commit"] = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True,
            timeout=10).stdout.strip() or None
    except Exception:
        report["repo_commit"] = None

    capabilities = {}
    missing_all: set[str] = set()
    for name, (packages, modules) in CAPABILITIES.items():
        missing = _missing(packages)
        errors = {} if missing else _import_errors(modules)
        missing_all.update(missing)
        capabilities[name] = {"available": not missing and not errors, "missing_packages": missing,
                              "import_errors": errors}
    rscript = shutil.which("Rscript") or shutil.which("Rscript.exe")
    capabilities["limma_voom"]["rscript"] = rscript
    if rscript:
        try:
            probe = subprocess.run([rscript, "-e", "library(limma)"], capture_output=True,
                                   text=True, timeout=60)
            capabilities["limma_voom"]["r_limma"] = probe.returncode == 0
        except Exception as exc:
            capabilities["limma_voom"]["r_limma"] = f"check failed: {exc}"
    if not rscript or capabilities["limma_voom"].get("r_limma") is not True:
        capabilities["limma_voom"]["available"] = False
    report["capabilities"] = capabilities
    de_routes = ("deseq2", "limma_two_group", "limma_multigroup", "edger", "limma_voom")
    report["de_capable"] = any(capabilities[name]["available"] for name in de_routes)
    if not report["de_capable"]:
        report["decision_only_note"] = (
            "No differential-analysis executor is available. Decisions can still be made and "
            "recorded; every valid plan will be recorded as execution failed with its error. "
            "Tell the user and install the missing packages to execute.")

    native_ok = capabilities["native_runtime"]["available"]
    if native_ok:
        os.environ["BIOAGENT_DISABLE_EXTERNAL_LLM"] = "1"
        from tools import model_factory
        before = len(model_factory.blocked_external_llm_attempts())
        blocked = model_factory.create_structured_chat_model(required=False) is None
        recorded = len(model_factory.blocked_external_llm_attempts()) == before + 1
        report["external_llm_block"] = {"works": blocked and recorded}
    report["install_hint"] = (
        "python -m pip install -r requirements.txt" if missing_all else None)
    report["missing_packages"] = sorted(INSTALL_NAMES.get(p, p) for p in missing_all)
    if platform.system() == "Windows":
        report["windows_note"] = "set PYTHONIOENCODING=utf-8 before running repository tools"
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0 if native_ok and report["python_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
