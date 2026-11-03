"""Build the review packets for every calibration case (no model calls).

    python test/experiments/review_calibration_20261103/make_packets.py --src <runs_claude> --root <checkout>

--src: the 211-paper run's runs_claude folder (clean and real cases are read there, never written).
--root: the checkout that the records' relative paths and the paper paths start from.
Packets go to reviews/<name>/ (packet_A.md, packet_B.md, flags.json).
"""

import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))

from tools.case_review import build  # noqa: E402


def rows(src: str):
    with open(HERE / "cases.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["case_dir"] = r["case_dir"].replace("{HERE}", str(HERE)).replace("{SRC}", src)
            yield r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    root = Path(args.root)
    index = {}
    for r in rows(args.src):
        if args.only and not any(r["name"].startswith(o) for o in args.only.split(",")):
            continue
        out = HERE / "reviews" / r["name"]
        s = build(Path(r["case_dir"]), out, paper=str(root / r["paper"]), root=root)
        index[r["name"]] = {"case_dir": r["case_dir"], "review_dir": str(out), "paper": str(root / r["paper"]),
                            "flags": [f["flag"] for f in s["flags"]]}
        print(r["name"], index[r["name"]]["flags"])
    (HERE / "reviews" / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
