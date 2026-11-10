"""Give the reviewers neutral case folders, so a path cannot tell them what to look for.

    python test/experiments/review_calibration_20261103/blind.py make --src <runs_claude> --root <checkout>
    python test/experiments/review_calibration_20261103/blind.py collect

The calibration's own names say the answer (runs/s1_GSE267512_unpaired, reviews/c1_...), and seeded and
clean cases live under different roots. `make` copies each case to <repo>/.review_queue/case_NN/run/<case_id>
in a shuffled order, rewrites the case's own path prefixes to that folder, drops the seeded request tag,
builds the packets there, and refuses to finish if a telling string is left. `collect` copies each
review.json and review.md, and the packets the reviewer saw, back to reviews/<name>/ for score.py.
The name-to-alias map is reviews/blind_map.json. No model calls.
"""

import argparse
import csv
import json
import random
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))

from tools.case_review import build  # noqa: E402

QUEUE = REPO / ".review_queue"
MAP = HERE / "reviews" / "blind_map.json"
SEP = r"[\\/]+"
TELLING = re.compile(r"review[ _]calibration|seeded|s[1-5]_GSE|r1_GSE|c[1-5]_GSE|forced_run|wrong_control|"
                     r"runs_claude[\\/]+[^\\/\"]+[\\/]+(interaction_lrt|GSE\d+)[\\/]", re.I)


def _rx(path: str) -> str:
    return SEP.join(re.escape(p) for p in re.split(r"[\\/]+", path))


def _rewrite(text: str, prefixes: list[tuple[str, str]]) -> str:
    for prefix, target in prefixes:
        text = re.sub(f"(?:[A-Za-z]:{SEP}agent{SEP}[^\\\\/\"]+{SEP})?{_rx(prefix)}", lambda m, t=target: t, text)
    text = re.sub(r'"run_id": "[^"]*"', '"run_id": "run"', text)
    return text.replace(" [review calibration: seeded case]", "")


def _copy_case(case_dir: Path, dest: Path, prefixes: list[tuple[str, str]]):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(case_dir, dest, ignore=shutil.ignore_patterns("_previous", "*.log"))
    handback = case_dir.parent / "HANDBACK.md"
    if handback.exists():
        shutil.copy(handback, dest.parent / "HANDBACK.md")
    for p in [*dest.rglob("*.json"), *dest.rglob("*.md"), *dest.parent.glob("*.md")]:
        text = p.read_text(encoding="utf-8", errors="replace")
        new = _rewrite(text, prefixes)
        if new != text:
            p.write_text(new, encoding="utf-8")


def make(src: str, root: Path, seed: int = 20261103):
    with open(HERE / "cases.csv", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))
    aliases = [f"case_{i:02d}" for i in range(1, len(cases) + 1)]
    random.Random(seed).shuffle(aliases)
    QUEUE.mkdir(exist_ok=True)
    (QUEUE / ".gitignore").write_text("*\n", encoding="utf-8")
    table, leaks = {}, []
    for c, alias in zip(cases, aliases):
        case_dir = Path(c["case_dir"].replace("{HERE}", str(HERE)).replace("{SRC}", src))
        case_id, parent = case_dir.name, case_dir.parent
        dest = QUEUE / alias / "run" / case_id
        review_dir = QUEUE / alias / "review"
        if parent.is_relative_to(REPO):
            # A seeded run's own folder; the original run's folder it reads inputs from is left as it is.
            rel = parent.relative_to(REPO).as_posix()
            prefixes = [(f"{rel}/{case_id}", dest.as_posix()), (rel, dest.parent.as_posix())]
        else:
            prefixes = [(f"{parent.relative_to(root).as_posix()}/{case_id}", dest.as_posix())]
        _copy_case(case_dir, dest, prefixes)
        if review_dir.exists():
            shutil.rmtree(review_dir)
        s = build(dest, review_dir, paper=str(root / c["paper"]), root=root)
        table[c["name"]] = {"alias": alias, "case_dir": dest.as_posix(), "review_dir": review_dir.as_posix(),
                            "paper": (root / c["paper"]).as_posix(), "flags": [f["flag"] for f in s["flags"]]}
        for p in [*dest.rglob("*.json"), *dest.rglob("*.md"), *dest.parent.glob("*.md"), *review_dir.iterdir()]:
            for m in TELLING.finditer(p.read_text(encoding="utf-8", errors="replace")):
                leaks.append(f"{alias}/{p.name}: {m.group(0)}")
        print(c["name"], "->", alias, table[c["name"]]["flags"])
    MAP.write_text(json.dumps(table, indent=1), encoding="utf-8")
    if leaks:
        print("LEFT IN THE BLIND COPIES:", *sorted(set(leaks)), sep="\n  ")
        return 1
    print("no telling strings left")
    return 0


def collect():
    table = json.loads(MAP.read_text(encoding="utf-8"))
    for name, t in table.items():
        rd, out = Path(t["review_dir"]), HERE / "reviews" / name
        (out / "seen").mkdir(parents=True, exist_ok=True)
        for f in ("packet_A.md", "packet_B.md"):
            shutil.copy(rd / f, out / "seen" / f)
        got = [f for f in ("review.json", "review.md") if (rd / f).exists()]
        for f in got:
            shutil.copy(rd / f, out / f)
        print(name, t["alias"], got)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "collect"])
    ap.add_argument("--src")
    ap.add_argument("--root")
    args = ap.parse_args()
    sys.exit(make(args.src, Path(args.root)) if args.cmd == "make" else collect())


if __name__ == "__main__":
    main()
