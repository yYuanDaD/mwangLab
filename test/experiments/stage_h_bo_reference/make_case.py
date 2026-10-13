"""Stage H: build a blind skill workspace from Bo's frozen RNA-seq benchmark.

    python make_case.py <bo_root> <workspace> [--accession GSE195482]

<bo_root> is the unpacked RNAseqData4Testing folder (one subfolder per accession).
The workspace receives the pairwise count matrices and metadata only. Bo's DEG
and GSEA results, and his R scripts, stay out of it; they are the reference
that compare_to_reference.py scores against.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

REFERENCE_PATTERNS = (r"\.DEGs?_", r"\.gsea", r"\.r$", r"\.R$", r"\.py$", r"\.rds$", r"\.RData$")


def find_accession_dir(bo_root: Path, accession: str) -> Path:
    hits = [p for p in bo_root.rglob(accession) if p.is_dir()]
    if not hits:
        raise SystemExit(f"no folder named {accession} under {bo_root}")
    return hits[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bo_root", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--accession", default="GSE195482")
    args = parser.parse_args()

    source = find_accession_dir(args.bo_root, args.accession)
    case_dir = args.workspace / "cases" / args.accession
    case_dir.mkdir(parents=True, exist_ok=True)
    copied, withheld = [], []
    for path in sorted(source.iterdir()):
        if not path.is_file():
            continue
        if any(re.search(p, path.name) for p in REFERENCE_PATTERNS):
            withheld.append(path.name)
            continue
        if path.name.endswith((".rawcount.txt", ".metadata.txt")):
            shutil.copy2(path, case_dir / path.name)
            copied.append(path.name)
    if not copied:
        raise SystemExit(f"no *.rawcount.txt or *.metadata.txt in {source}")

    contrasts = sorted({name.split(".")[0] for name in copied})
    entry = {
        "case_id": args.accession,
        "accession": args.accession,
        "source": "frozen local snapshot of the pairwise benchmark inputs; do not download the matrices",
        "paper": "not supplied; fetch the linked publication through the skill if network is available",
        "contrasts_supplied": contrasts,
        "files": {name: f"{args.accession}/{name}" for name in copied},
    }
    (args.workspace / "cases" / "manifest.json").write_text(json.dumps([entry], indent=2), encoding="utf-8")
    print(f"copied {len(copied)} files for {contrasts}; withheld {len(withheld)} reference files")


if __name__ == "__main__":
    main()
