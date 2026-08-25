"""Create eight machine-draft result-card files for human annotation.

The command never labels drafts as gold.  Existing cards are preserved unless
``--overwrite`` is explicitly supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, default=Path(__file__).with_name("cases_seed.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    seed = json.loads(args.seed.read_text(encoding="utf-8"))
    template = json.loads(Path(__file__).with_name("gold_card_template.json").read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    manifest_cases = []
    for case in seed["cases"]:
        paper = root / case["paper_path"]
        if not paper.is_file():
            raise FileNotFoundError(f"Missing paper source for {case['case_id']}: {paper}")
        card_path = args.output_dir / f"{case['case_id']}.json"
        if args.overwrite or not card_path.exists():
            card = json.loads(json.dumps(template))
            card["article_id"] = case["article_id"]
            card["accessions"] = case["accessions"]
            card["claims"][0]["source_uri"] = case["paper_path"]
            card_path.write_text(json.dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
        manifest_cases.append({
            **case,
            "paper_sha256": _sha256(paper),
            "annotation_status": "unreviewed",
            "gold_card": str(card_path.relative_to(args.output_dir.parent)).replace("\\", "/"),
        })

    manifest = {
        "schema_version": "1.0",
        "benchmark": seed["benchmark"],
        "annotation_policy": seed["annotation_policy"],
        "case_count": len(manifest_cases),
        "cases": manifest_cases,
    }
    manifest_path = args.output_dir.parent / "gold_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "draft_cards": len(manifest_cases)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
