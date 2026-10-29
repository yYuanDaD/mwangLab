"""Gate 10 (GSEA Hallmark on the planned contrasts, gene-level), gate 11 (study), case and run finish."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40295575"
run = native.RunRecorder.open(RUN)
case = run.case("GSE283250")
paper = case.evidence_item("paper:PMC12038050.paper.json")
res = case.dir / "results"
ex = json.loads((case.dir / "execution_results.json").read_text(encoding="utf-8"))
SYM = RUN + "/GSE283250_merge/transcript_to_symbol.csv"
sym_item = case.evidence_item("tool_output:transcript_to_symbol.csv")
PLANNED = ["grp_SS_vs_CON", "grp_SS_vs_SES", "grp_SES_vs_SER"]

enr_summary = {}
for n in PLANNED:
    gdir = res / "gsea" / n
    gdir.mkdir(parents=True, exist_ok=True)
    col = native.collapse_to_genes(ex[n]["file"], gdir / f"DEG_genelevel_{n}.csv", mapping_csv=SYM,
                                   mapping_column="gene_symbol", rule="max_abs_score", score_column="stat")
    col_item = case.add_output(col["output"] if "output" in col else gdir / f"DEG_genelevel_{n}.csv", f"genelevel_{n}")
    final = {"method": "GSEA preranked (gseapy prerank) on limma moderated t", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
             "organism": "Mouse", "feature_id_type": "refseq_transcript", "contrast": n,
             "id_mapping": {"source": "per-sample GEO tables (Gene symbol column)", "file": SYM,
                            "rule": "max_abs_score on stat (one transcript per symbol)",
                            "record": col.get("mapping_record", {k: v for k, v in col.items() if k != "output"})},
             "ranking": "stat (sign: positive = higher in the first-named group)",
             "paper_route": {"method": "Broad GSEA Java, MSigDB M5 GO, gene-set permutation x1000, FDR < 25%",
                             "status": "blocked", "reason": "executor supports Hallmark preranked GSEA only; M5 GO and phenotype/gene-set permutation are not available"}}
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(gdir / f"DEG_genelevel_{n}.csv"),
                               organism="Mouse", ranking_metric="stat", output_dir=str(gdir))
        outs = [str(p) for p in gdir.glob("*GSEA*.csv")]
        for p in outs:
            case.add_output(p, f"gsea_{n}")
        top = None
        if outs:
            g = pd.read_csv(outs[0])
            fdr_col = next((c for c in g.columns if "fdr" in c.lower()), None)
            sig = g[pd.to_numeric(g[fdr_col], errors="coerce") < 0.25] if fdr_col else g
            top = sig[[c for c in g.columns if c in ("Term", "NES", fdr_col)]].head(10).to_dict("records")
        enr_summary[n] = {"status": "completed", "outputs": outs, "top_fdr_lt_0.25": top}
        final["outputs"] = outs
        case.decide("enrichment", final=final, evidence=[col_item, sym_item, paper], paper={"locator": "S4.11.p4"},
                    confidence="medium", execution_status="completed",
                    reasoning=f"Gene-level ranking of {n} (transcripts collapsed to symbols by max |t|); Hallmark GSEA as a declared deviation from the paper's M5 GO GSEA.")
    except native.NativeToolError as e:
        enr_summary[n] = {"status": "failed", "error": str(e)[:500]}
        final["execution_error"] = str(e)[:1000]
        case.decide("enrichment", final=final, evidence=[col_item, sym_item, paper], paper={"locator": "S4.11.p4"},
                    confidence="medium", execution_status="failed", reasoning=f"GSEA for {n} failed; DE result unaffected.")
case.write_json("enrichment_summary.json", enr_summary, role="enrichment_summary")
print(json.dumps(enr_summary, indent=1, default=str)[:4000])

# ---------------- reproduction summary + study
paper_counts = {"grp_SS_vs_CON": {"total": 2305, "up_in_SS": 1301, "down_in_SS": 1004}}
repro = {
    "applied_threshold": "raw p < 0.05 and |log2FC| > log2(1.3) (paper rule on limma moderated t)",
    "contrasts": {n: {"role": v["role"], "n_deg_applied": v["applied"]["n_significant"], "up": v["applied"]["n_up"],
                      "down": v["applied"]["n_down"], "n_tested": v["applied"]["n_tested"],
                      "audit_bh_lt_0.05": v["audit_bh005"]["n_significant"],
                      "paper": paper_counts.get(n, "not_reported")} for n, v in ex.items()},
    "comparison_to_paper": "SS vs CON: 2911 (1792 up / 1119 down in SS) vs paper 2305 (1301 / 1004); same direction balance. "
                           "Other paper contrasts have volcano plots only (FIG3c-d), no counts.",
    "validation": "Under BH < 0.05 within contrast, 1-13 transcripts per contrast: with n = 3 per group the raw-p rule is the paper's choice, and the counts are largely noise-level at FDR control.",
    "enrichment": enr_summary,
}
case.write_json("reproduction_summary.json", repro, role="reproduction_summary")
plan = {"route": "declared_deviation", "executor": "tools.joint_contrasts:run_joint_limma", "formula": "~ 0 + grp",
        "transform": "log2(CPM+1) after count >= 10 in >= 3 samples", "planned": PLANNED,
        "exploratory": [n for n in ex if n not in PLANNED], "threshold": "paper rule on deviation route"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
disc = [
    {"item": "matrix scale", "paper": "cuffdiff geometric-normalized FPKM", "data": "cufflinks integer read counts per RefSeq transcript", "disposition": "requires_explicit_deviation", "action": "log2(CPM+1)"},
    {"item": "test", "paper": "unpaired Student's t-test per pair of groups", "data": "no t-test executor", "disposition": "requires_explicit_deviation", "action": "limma moderated t from one 4-group model"},
    {"item": "pre-filter", "paper": "not_reported (all 33,299 rows annotated)", "data": "count >= 10 in >= 3 samples keeps 20,565", "disposition": "requires_explicit_deviation", "action": "recorded"},
    {"item": "VWR duration", "paper": "4 weeks (S2.1.p2, S4.4.p1)", "data": "GEO title 'Voluntary wheel running 14d'", "disposition": "executable_without_change", "action": "paper value kept; GEO label noted"},
    {"item": "animal numbers", "paper": "not reported", "data": "no. 12 in CON and SES, no. 19 in SS and SER", "disposition": "executable_without_change", "action": "treated as distinct animals (mutually exclusive treatments)"},
    {"item": "GSEA", "paper": "Broad GSEA, MSigDB M5 GO, 1000 permutations", "data": "Hallmark preranked only", "disposition": "requires_explicit_deviation", "action": "Hallmark preranked on gene-level t"},
    {"item": "tar merge key", "paper": "33,299 transcript rows", "data": "repository merger keys on symbol and drops duplicates", "disposition": "executable_without_change", "action": "own merge on Transcript ID (scripts/s02_merge.py)"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
case.decide("study", final={"route": "declared_deviation", "planned": PLANNED,
                            "exploratory_contrasts": [n for n in ex if n not in PLANNED],
                            "exploratory_reason": "residual df = 8 (>= 4) and n = 3 per arm, so the planned contrasts are not exploratory by the size rule; the three non-paper pairs are exploratory by design",
                            "n_deg_applied": {n: ex[n]["applied"]["n_significant"] for n in ex},
                            "primary_exercise_contrast": "grp_SS_vs_SES"},
            evidence=[case.evidence_item("tool_output:execution_results.json"), paper], paper={"locator": "S4.11.p2; FIG3"},
            confidence="medium", execution_status="completed",
            reasoning="Paper route (t-test on FPKM) blocked; limma on log2(CPM+1) of deposited counts with the paper threshold.")
case.finish(n_deg=ex["grp_SS_vs_SES"]["applied"]["n_significant"], deg_sanity=ex["grp_SS_vs_SES"]["applied"]["deg_sanity"])
print(run.finish())
