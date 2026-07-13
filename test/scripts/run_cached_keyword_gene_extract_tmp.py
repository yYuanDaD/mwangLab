import csv
import os
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.seacdm_tools import build_reported_findings


ARTICLES = [
    {
        "study_id": "GSE279359",
        "organism": "Mouse",
        "text_path": "data/papers/2267864b41e9b481bd2c3bbf6967fca3f0db8c34.txt",
        "label": "acute_endurance_splicing",
    },
    {
        "study_id": "GSE208615",
        "organism": "Mouse",
        "text_path": "data/papers/ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt",
        "label": "exercise_epigenetic_memory",
    },
    {
        "study_id": "PMC10913554",
        "organism": "Mouse",
        "text_path": "data/papers/fece27c2b0e906d7628a162d39a4589e153b63e7.txt",
        "label": "swimming_aging_lens",
    },
]


def main():
    out_dir = Path("output/cached_keyword_gene_check")
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for art in ARTICLES:
        text_path = Path(art["text_path"])
        text = text_path.read_text(encoding="utf-8", errors="ignore")
        study_id = art["study_id"]
        study_dir = out_dir / study_id
        study_dir.mkdir(parents=True, exist_ok=True)
        report = {}
        usage = []
        rows = build_reported_findings(
            study_id,
            text[:100000],
            str(study_dir / "reported_findings.csv"),
            organism=art["organism"],
            verify=True,
            report=report,
            existing_tables={
                "experiment": [{"experiment_id": f"{study_id}_exp1"}],
                "interventions": [{
                    "intervention_id": f"{study_id}_exp1_int1",
                    "material": "exercise",
                    "intervention_type": "exercise",
                }],
            },
            usage=usage,
        )
        gene_rows = rows.get("gene", [])
        if gene_rows:
            with open(study_dir / "gene.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(gene_rows[0].keys()))
                writer.writeheader()
                writer.writerows(gene_rows)
        summary.append({
            "study_id": study_id,
            "label": art["label"],
            "text_chars": len(text),
            "n_findings": report.get("n_findings", 0),
            "n_verified": report.get("n_verified", 0),
            "n_unverified": report.get("n_unverified", 0),
            "n_gene_rows": len(gene_rows),
            "genes": ";".join(g.get("gene_symbol") or "" for g in gene_rows[:30]),
            "input_tokens": sum((u.get("input_tokens") or 0) for u in usage),
            "output_tokens": sum((u.get("output_tokens") or 0) for u in usage),
        })
        print(summary[-1])

    with open(out_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    print(f"summary: {out_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
