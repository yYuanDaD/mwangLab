"""Copy pairing gold from estimand_annotations.json into covariance_annotations.csv.

estimand_annotations.json is the source of truth (it also holds alternate axes and
label corrections, which do not fit a flat table). This keeps the per-series CSV
template from scripts/fetch_exergenedb_labels.py filled for the annotated series.

    python test/validation/exergenedb_gold/sync_covariance_annotations.py
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def subject_text(spec):
    if not spec:
        return ""
    return spec["column"] + (f" ~ /{spec['regex']}/" if spec.get("regex") else "")


def main() -> int:
    ann = json.loads((HERE / "estimand_annotations.json").read_text(encoding="utf-8"))
    path = HERE / "covariance_annotations.csv"
    table = pd.read_csv(path, dtype=str).fillna("")
    for acc, a in ann["series"].items():
        row = table.index[table["accession"] == acc]
        if len(row) != 1:
            raise SystemExit(f"{acc} not in {path.name}")
        unit = {"required": "subject", "not_required": "none"}.get(a["pairing"], "unknown")
        alts = "; ".join(f"{x['estimand']} (pairing {x['pairing']})" for x in a.get("alternate_axes", []))
        notes = " ".join(filter(None, [f"Also admissible: {alts}." if alts else "", a.get("notes", "")]))
        table.loc[row, ["pairing_unit", "pairing_evidence", "primary_contrast", "annotator", "annotated_on", "notes"]] = [
            unit, " | ".join(filter(None, [subject_text(a.get("subject")), a.get("evidence", "")])),
            a["gold_estimand"], ann["annotator"], ann["annotated_on"], notes]
    table.to_csv(path, index=False, lineterminator="\n")
    print(f"updated {len(ann['series'])} rows in {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
