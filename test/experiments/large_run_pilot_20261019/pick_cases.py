"""Pick the 5 pilot papers from analyzable.csv: one per stratum, seed 20261019,
preferring designs with 3+ groups (more than one sensible comparison)."""
import csv, json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
SCREEN = os.path.join(HERE, "..", "paper_screen_20261019")
SP = {"Mus musculus": "mouse", "Homo sapiens": "human", "Rattus norvegicus": "rat", "Rattus rattus": "rat"}
STRATA = [("mouse_raw", {"mouse_raw"}), ("human_raw", {"human_raw"}), ("rat_raw", {"rat_raw"}),
          ("mouse_tar", {"mouse_tar"}), ("human_or_rat_tar", {"human_tar", "rat_tar"})]

rows = list(csv.DictReader(open(os.path.join(SCREEN, "analyzable.csv"), encoding="utf-8")))
rng = random.Random(20261019)
out = []
for name, keys in STRATA:
    pool = [r for r in rows if ";" not in r["taxon"] and f"{SP.get(r['taxon'])}_{r['file_kind']}" in keys]
    rich = [r for r in pool if r["groups"].startswith("{") and len(json.loads(r["groups"])) >= 3]
    pick = rng.choice(sorted(rich or pool, key=lambda r: r["paper_id"]))
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", pick["pmcid"] or pick["paper_id"])
    out.append({"stratum": name, "pool": len(pool), "pool_3plus_groups": len(rich), **pick,
                "paper_json": f"test/experiments/paper_screen_20261019/papers/{stem}.paper.json",
                "paper_md": f"test/experiments/paper_screen_20261019/papers/{stem}.paper.md"})
with open(os.path.join(HERE, "cases.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
for o in out:
    print(o["stratum"], o["paper_id"], o["analyzable_gse"], o["groups"][:80], "|", o["title"][:70],
          os.path.exists(os.path.join(HERE, "..", "..", "..", o["paper_json"])))
