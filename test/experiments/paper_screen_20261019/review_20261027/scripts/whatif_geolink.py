"""What-if: treat every GEO series that GEO links to the paper's PMID as the paper's own,
for papers the screen dropped at the text/ownership layers. Run the data layers on them."""
import csv, json, os, re, sys
sys.path.insert(0, os.getcwd())
from tools import paper_screen as ps
RUN = "test/experiments/paper_screen_20261019"; REV = os.path.join(RUN, "review_20261027")
http = ps.Http(cache_dir=os.path.join(RUN, "_http_cache"))
scr = {r["paper_id"]: r for r in csv.DictReader(open(os.path.join(REV, "screen.csv"), encoding="utf-8"))}
geo = {r["paper_id"]: json.loads(r["geo_linked"]) for r in csv.DictReader(open(os.path.join(REV, "geo_by_pmid.csv"), encoding="utf-8"))}
topic = re.compile(ps.DEFAULT_TOPIC, re.I)
LAYERS = ("no_full_text", "no_exercise_contrast", "no_own_deposit", "data_on_request", "non_geo_repository")
out = []
for pid, r in scr.items():
    if r["verdict"] != "excluded" or not r["reason"].startswith(LAYERS):
        continue
    for s in geo.get(pid, []):
        gse = s["gse"]
        info = ps.geo_summary(gse, http)
        files = design = None
        if info and set(info["data_type"].split("+")) & ps.SUPPORTED_ROUTES and ps.organism_ok(info["taxon"], ps.DEFAULT_ORGANISMS):
            files = ps.classify_supplementary(ps.list_geo_dir(ps.GEO_SUPPL.format(stub=ps.geo_stub(gse), gse=gse), http))
            design = ps.geo_design(gse, http)
            if files["status"] == "raw_counts":
                files["value_check"] = vc = ps.check_raw_values(gse, files, http, design.get("processing", ""))
                if vc["status"] in ("normalized_only", "decimal_unexplained"):
                    files["status"] = "raw_tar" if files["tar"] else vc["status"]
            design.pop("processing", None)
            if files["status"] == "raw_tar":
                inside = ps.inspect_sample_files(design.get("sample_files", []), http)
                files["status"] = {"raw_counts": "raw_counts_in_tar", "normalized_only": "normalized_only",
                                   "no_count_files": "none"}.get(inside["status"], "raw_tar")
            design.pop("sample_files", None)
        v, why = ps.judge_series(info, files, design, ps.SUPPORTED_ROUTES, ps.DEFAULT_ORGANISMS)
        out.append({"paper_id": pid, "layer": r["reason"].split(":")[0] + (":" + r["reason"].split(":")[1] if r["reason"].startswith("no_own_deposit:") else ""),
                    "title_on_topic": bool(topic.search(r["title"])), "title": r["title"], "gse": gse,
                    "data_type": info["data_type"] if info else "", "taxon": info["taxon"] if info else "",
                    "verdict": v, "reason": why, "files": (files or {}).get("status", ""),
                    "groups": json.dumps((design or {}).get("groups"), ensure_ascii=False)[:200]})
        print(pid[:14], gse, v, why, flush=True)
with open(os.path.join(REV, "whatif_geolink.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
