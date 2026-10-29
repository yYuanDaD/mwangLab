import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
run = native.RunRecorder.open("test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436")
info = {"fatigued_pbmt_vs_ctrl": {"paper": {"up": 302, "down": 156}, "loc": "S2.3.p1"},
        "sedentary_pbmt_vs_ctrl": {"paper": {"up": "~586", "down": "~802"}, "loc": "S2.1.p1"}}
for cid, inf in info.items():
    case = run.case(cid)
    cnt = json.load(open(case.dir / "threshold_counts.json", encoding="utf-8"))
    aud = json.load(open(case.dir / "audit_threshold_counts.json", encoding="utf-8"))
    disc = [
        {"item": "DEG counts vs threshold", "paper": f"{inf['paper']} at 'adjusted p<0.05' ({inf['loc']}, S4.9.p1)",
         "data": f"DESeq2 padj<0.05: {cnt['n_up']} up/{cnt['n_down']} down; raw p<0.05 (audit): {aud['n_up']} up/{aud['n_down']} down",
         "disposition": "executable_without_change", "note": "paper counts reproduce almost exactly under raw p<0.05, so the reported counts were most likely raw-p based despite the 'adjusted' wording; paper rule kept as stated, raw-p counts reported only as audit"},
        {"item": "DESeq2 implementation", "paper": "DESeq2 'version 1.4.1' (R)", "data": "pydeseq2 0.5.4", "disposition": "executable_without_change"},
        {"item": "enrichment", "paper": "clusterProfiler GO/KEGG ORA", "data": "Enrichr GO 2023/KEGG 2019 ORA + Hallmark GSEA", "disposition": "requires_explicit_deviation"},
        {"item": "run duration", "paper": "variable run times, discussed as source of variability (S2.3.p1)", "data": "not in GEO metadata", "disposition": "executable_without_change"},
    ]
    case.write_json("paper_data_discrepancies.json", disc)
    case.write_json("reproduction_plan.json", {"route": "paper_aligned", "method": "DESeq2 ~ grp, 6 vs 6 within one Admera project", "threshold": "padj<0.05, no effect cutoff (paper)", "audit": "raw p<0.05"})
    case.write_json("reproduction_summary.json", {"paper_counts": inf["paper"], "paper_rule_counts": {k: cnt[k] for k in ("n_up", "n_down", "n_tested")},
                                                  "audit_raw_p_counts": {k: aud[k] for k in ("n_up", "n_down")}, "discrepancies": disc})
    case.decide("study", final={"route": "paper_aligned", "paper_counts": inf["paper"],
                                "paper_rule_counts": {"up": cnt["n_up"], "down": cnt["n_down"]},
                                "audit_raw_p_counts": {"up": aud["n_up"], "down": aud["n_down"]}},
                evidence=[case.add_output(case.dir / "reproduction_summary.json", "reproduction_summary_ref")],
                paper={"locator": inf["loc"]}, confidence="high", execution_status="completed",
                reasoning="Paper route reproduced; counts differ at the stated rule but match under raw p (audit).")
    print(cid, case.finish(n_deg=cnt["n_significant"], deg_sanity=cnt["deg_sanity"]))
case = run.case("exercise_vs_sedentary_ctrl")
case.write_json("paper_data_discrepancies.json", [{"item": "exercise contrast", "paper": "not analysed transcriptomically", "data": "fatctl (project 23263-01) vs sedctl (23263-02) aliased with sequencing project", "disposition": "blocks_reproduction"}])
print("exercise", case.finish())
print(run.finish())
