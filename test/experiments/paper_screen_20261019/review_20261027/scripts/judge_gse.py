"""Run the screener's per-series layers on given GSEs as if they were the paper's own."""
import sys, os, json
sys.path.insert(0, os.getcwd())
from tools import paper_screen as ps
http = ps.Http(cache_dir="test/experiments/paper_screen_20261019/_http_cache")
for gse in sys.argv[1:]:
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
            files["tar_inspection"] = inside = ps.inspect_sample_files(design.get("sample_files", []), http)
            files["status"] = {"raw_counts": "raw_counts_in_tar", "normalized_only": "normalized_only",
                               "no_count_files": "none"}.get(inside["status"], "raw_tar")
        design.pop("sample_files", None)
    v = ps.judge_series(info, files, design, ps.SUPPORTED_ROUTES, ps.DEFAULT_ORGANISMS)
    print(gse, v, info["data_type"] if info else None)
    if files: print("   files:", json.dumps({k: files[k] for k in ("status", "tar_inspection") if k in files}, ensure_ascii=False)[:300])
    if design: print("   design:", json.dumps(design.get("groups"), ensure_ascii=False)[:300])
