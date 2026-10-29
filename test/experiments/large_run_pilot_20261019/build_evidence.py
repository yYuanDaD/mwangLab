"""Build runs_claude/EVIDENCE.md: the evidence behind each row of REVIEW.md, from the run records.

For every paper in progress.csv it collects, per case, what the decision records say:
the paper's estimand, contrasts, threshold and reported counts (with locators in the
paper), and our matrix, design, covariance, method, applied threshold, DEG counts,
result files and paper/data discrepancies. Nothing is re-analysed.

    python test/experiments/large_run_pilot_20261019/build_evidence.py
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs_claude"
ROOT = HERE.parents[2]


def compact(value, limit=600):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + " …"


def first(final, *keys):
    for k in keys:
        if final.get(k) not in (None, "", [], {}):
            return final[k]
    return None


def rel(path):
    p = Path(str(path).replace("\\", "/"))
    try:
        return (ROOT / p).resolve().relative_to(RUNS).as_posix() if not p.is_absolute() else p.resolve().relative_to(RUNS).as_posix()
    except ValueError:
        return p.as_posix()


def threshold_text(t):
    if not isinstance(t, dict):
        return compact(t, 200)
    parts = [f"{t.get('metric')} {'≤' if t.get('inclusive') else '<'} {t.get('cutoff')}"]
    if t.get("effect_cutoff") not in (None, 0):
        parts.append(f"|{t.get('effect_metric') or 'log2FC'}| {'≥' if t.get('inclusive') else '>'} {t.get('effect_cutoff')}")
    if t.get("adjustment"):
        parts.append(f"({t['adjustment']})")
    loc = t.get("source_locator")
    return " ".join(parts) + (f" — paper {loc}" if loc else "")


def case_section(case_dir: Path) -> list[str]:
    recs = json.loads((case_dir / "decisions.json").read_text(encoding="utf-8"))
    by = {}
    for r in recs:
        by.setdefault(r["stage"], []).append(r)
    out = [f"#### Case `{case_dir.name}`", ""]

    def final(stage):
        return (by.get(stage) or [{}])[0].get("final") or {}

    pr = final("paper_reconstruction")
    if pr:
        out.append(f"- **Paper's estimand:** {compact(pr.get('primary_estimand', ''), 500)}")
        if pr.get("planned_contrasts"):
            out.append(f"- **Paper's planned contrasts:** {compact(pr['planned_contrasts'], 400)}")
        if pr.get("paper_threshold"):
            out.append(f"- **Paper's threshold:** {threshold_text(pr['paper_threshold'])}")
        counts = first(pr, "reported_counts", "paper_counts", "paper_reported_deg_counts", "reported_deg_counts",
                       "paper_deg_counts")
        if counts:
            out.append(f"- **Counts the paper reports:** {compact(counts, 700)}")
        if pr.get("paper_method"):
            out.append(f"- **Paper's method:** {compact(pr['paper_method'], 300)}")
    m = final("matrix")
    if m:
        out.append(f"- **Matrix:** {compact(m.get('matrix_type', ''), 200)}")
    d = final("design")
    if d:
        suit = d.get("suitability") or {}
        sv = f"; suitability: {suit.get('verdict')}" if suit else ""
        out.append(f"- **Design:** {compact(d.get('analysis_type', ''), 150)}; "
                   f"formula `{d.get('formula') or d.get('design_column')}`{sv}")
    c = final("covariance")
    if c:
        out.append(f"- **Covariance:** {c.get('status')}; blocking {c.get('blocking_terms') or 'none'}; "
                   f"covariates {compact(c.get('covariates') or 'none', 200)}")
    me = final("method")
    if me:
        line = f"- **Method:** {compact(me.get('method', ''), 250)}"
        if me.get("paper_route"):
            line += f" — paper route: {compact(me['paper_route'], 250)}"
        out.append(line)
    th = final("threshold")
    if th:
        out.append(f"- **Applied threshold:** {threshold_text(th.get('applied_threshold'))} "
                   f"(source: {th.get('threshold_source')})")
    for ex in by.get("execution", []):
        f = ex.get("final") or {}
        counts = first(f, "deg_counts", "n_deg", "counts", "threshold_counts")
        if counts is not None:
            out.append(f"- **Our DEG counts ({ex.get('execution_status')}):** {compact(counts, 700)}")
        files = [rel(p) for p in (f.get("outputs") or []) if str(p).lower().endswith(".csv")]
        if files:
            shown = ", ".join(f"`{x}`" for x in files[:6]) + (f" (+{len(files) - 6} more)" if len(files) > 6 else "")
            out.append(f"- **Result tables (on the PC, not in git):** {shown}")
    st = final("study")
    if st:
        out.append(f"- **Route:** {st.get('route')}")
    stops = [r for r in recs if r.get("decision_status") in ("refused", "manual_review", "unresolved")]
    for r in stops:
        out.append(f"- **Stopped at `{r['stage']}` ({r['decision_status']}):** {compact(r.get('stop_reason', ''), 500)}")
    disc = case_dir / "paper_data_discrepancies.json"
    if disc.exists():
        data = json.loads(disc.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("discrepancies", data.get("items", [data]))
        if isinstance(items, dict):
            items = [items]
        out.append(f"- **Paper vs data discrepancies ({len(items)}):**")
        for it in items[:6]:
            out.append(f"  - {compact(it, 300)}")
    out.append(f"- **Records:** `{case_dir.relative_to(RUNS).as_posix()}/decisions.json`")
    out.append("")
    return out


def main():
    queue = {r["paper_id"]: r for r in csv.DictReader(open(HERE / "queue.csv", encoding="utf-8"))}
    progress = list(csv.DictReader(open(RUNS / "progress.csv", encoding="utf-8")))
    lines = ["# Evidence behind REVIEW.md", "",
             "Generated by `build_evidence.py` from each run's decision records. Locators such as `S2.5.p1` "
             "point to a section and paragraph of the paper's structured text; `FIG2` to a figure legend.", ""]
    for i, p in enumerate(progress, 1):
        q = queue.get(p["paper_id"], {})
        gses = [g for g in p["gse"].replace(",", ";").split(";") if g]
        geo = ", ".join(f"[{g}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={g})" for g in gses)
        pmid = q.get("pmid") or (p["paper_id"][4:] if p["paper_id"].startswith("PMID") else "")
        paper = f"[PMID {pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)" if pmid else p["paper_id"]
        lines += [f"## {i}. {p['gse']} — {q.get('title', '')}", "",
                  f"- **Paper:** {paper}; **GEO:** {geo}",
                  f"- **Status:** {p['status']}; validator: {p['validator']}; "
                  f"{p['wall_minutes']} min, {p['subagent_tokens']} tokens",
                  f"- **Comparison with the paper:** {p['vs_paper']}", ""]
        run_dir = RUNS / p["paper_id"]
        cases = sorted(d for d in run_dir.iterdir() if (d / "decisions.json").exists()) if run_dir.exists() else []
        if not cases:
            lines += ["_No decision records found._", ""]
        for c in cases:
            lines += case_section(c)
    (RUNS / "EVIDENCE.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(progress)} papers -> {RUNS / 'EVIDENCE.md'}")


if __name__ == "__main__":
    main()
