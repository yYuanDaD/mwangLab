"""Score the calibration reviews against cases.csv.

    python test/experiments/review_calibration_20261103/score.py [--arm sonnet]

Reads reviews/<name>/review.json (or reviews_<arm>/ when --arm is given). A seeded or real case is
caught when a check listed in `expected` is `disagree` with severity blocking or major. Every
blocking/major `disagree` on a clean case is listed for hand adjudication (a reviewer may find a
real problem in a "clean" run). Writes scores.csv and prints a summary.
"""

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="")
    args = ap.parse_args()
    base = HERE / (f"reviews_{args.arm}" if args.arm else "reviews")
    out = []
    with open(HERE / "cases.csv", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))
    for c in cases:
        p = base / c["name"] / "review.json"
        row = {"name": c["name"], "kind": c["kind"], "expected": c["expected"], "reviewed": p.exists()}
        if p.exists():
            r = json.loads(p.read_text(encoding="utf-8"))
            hits = [k for k in r.get("checks", []) if k.get("verdict") == "disagree" and
                    k.get("severity") in ("blocking", "major")]
            row["overall"] = r.get("overall")
            row["major_disagree"] = ";".join(f"{k['id']}:{k['severity']}" for k in hits)
            exp = {e for e in c["expected"].split(";") if e}
            row["caught"] = bool(exp & {k["id"] for k in hits}) if exp else ""
            row["n_checks"] = len(r.get("checks", []))
        out.append(row)
    keys = ["name", "kind", "expected", "reviewed", "overall", "caught", "major_disagree", "n_checks"]
    with open(HERE / f"scores{'_' + args.arm if args.arm else ''}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in out:
            w.writerow({k: r.get(k, "") for k in keys})
    seeded = [r for r in out if r["kind"] in ("seeded", "real") and r["reviewed"]]
    clean = [r for r in out if r["kind"] == "clean" and r["reviewed"]]
    print(f"caught {sum(bool(r['caught']) for r in seeded)}/{len(seeded)} seeded+real; "
          f"clean with blocking/major items {sum(bool(r.get('major_disagree')) for r in clean)}/{len(clean)} "
          f"(adjudicate by hand)")
    for r in out:
        print(r["name"], r.get("overall"), r.get("caught"), r.get("major_disagree"))


if __name__ == "__main__":
    main()
