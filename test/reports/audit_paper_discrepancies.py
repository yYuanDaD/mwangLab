"""Recount existing paper-discrepancy evidence, without LLM or analysis calls.

Run with the project venv. All input paths are relative to the repository, even
when invoked from another working directory. Missing sources fail explicitly.
This audits archived outputs; it does not reproduce the authors' analyses.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SOURCES: dict[str, dict] = {}
STABILITY = Path("output/full_pipeline_stability_20x3_20260825")
OLD = Path("output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359")


def source(path: str | Path) -> Path:
    path = Path(path)
    raw = path.read_bytes()
    SOURCES[path.as_posix()] = {
        "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
    }
    return path


def frame(path: str | Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(source(path), **kwargs)


def document(path: str | Path) -> dict:
    return json.loads(source(path).read_text(encoding="utf-8-sig"))


def paper_anchor(path: str, phrase: str) -> dict:
    text = " ".join(source(path).read_text(encoding="utf-8").split())
    offset = text.find(phrase)
    if offset < 0:
        raise ValueError(f"Paper anchor missing: {path}: {phrase}")
    return {"path": path, "anchor": phrase, "normalized_text_offset": offset}


def count_da(path: Path) -> dict:
    df = frame(path, index_col=0)
    if df.index.has_duplicates:
        raise ValueError(f"Duplicate result row IDs: {path}")
    lfc = pd.to_numeric(df["log2FoldChange"], errors="raise")
    q = pd.to_numeric(df["padj"], errors="raise")
    return {
        "path": path.as_posix(), "n_rows": len(df),
        "n_padj_lt_005": int(q.lt(.05).sum()),
        "n_padj_lt_005_abs_lfc_gt_1": int((q.lt(.05) & lfc.abs().gt(1)).sum()),
        "n_padj_lt_005_abs_lfc_gt_1_5": int((q.lt(.05) & lfc.abs().gt(1.5)).sum()),
    }


def splicing_case() -> dict:
    paper = "data/papers/GSE279359_40693573.txt"
    # Paper-reported numbers, located in section 3.2 / Figure 2F-H.
    reported = {
        "immediately": (46, 23, 6323), "1_hour": (32, 13, 5459),
        "24_hours": (49, 31, 6125),
    }
    counts = frame("data/GSE279359/GSE279359_processed_counts.txt.gz",
                   sep=None, engine="python", index_col=0)
    comparisons = []
    for time, (n_relaxed, n_strict, n_genes) in reported.items():
        stem = f"DEG_results_{time}_post-exercise_vs_pre-exercise"
        methods = {m: count_da(OLD / f"{stem}__{m}.csv")
                   for m in ("deseq2", "edger", "limma-voom")}
        # Establish the row-level identity; equal sizes alone are insufficient.
        for method in methods:
            ids = frame(methods[method]["path"], index_col=0).index
            if set(ids.astype(str)) != set(counts.index.astype(str)):
                raise ValueError(f"Result rows differ from transcript input: {time}/{method}")
        comparisons.append({
            "timepoint": time, "paper_detected_genes": n_genes,
            "paper_padj_lt_005_abs_lfc_gt_1": n_relaxed,
            "paper_padj_lt_005_abs_lfc_gt_1_5": n_strict,
            "agent_methods": methods,
        })
    immediate = frame(OLD / "DEG_results_immediately_post-exercise_vs_pre-exercise__deseq2.csv",
                      index_col=0)
    ube = counts[counts.annot_gene_name.eq("Ube2d1")]
    ube_rows = immediate.loc[ube.index, ["log2FoldChange", "padj"]]
    return {
        "classification": "non_reproduction_with_feature_unit_mismatch",
        "decisions_path": source(OLD / "decisions.json").as_posix(),
        "confirmed_opposite_primary_conclusion": False,
        "paper_version": "archived preprint PMID40693573; final PMID40746864 checked separately",
        "paper_anchors": [paper_anchor(paper, phrase) for phrase in (
            "46 genes that reached statistical significance",
            "32 genes that reached statistical significance",
            "49 genes that reached statistical significance",
            "Swan v2.0", "known genes that were detected in at least half of the samples")],
        "matrix_rows": len(counts), "unique_gene_ID": int(counts.gene_ID.nunique()),
        "unique_transcript_ID": int(counts.transcript_ID.nunique()),
        "rows_sharing_gene_ID": int(counts.gene_ID.duplicated(keep=False).sum()),
        "gene_novelty_rows": counts.gene_novelty.value_counts().to_dict(),
        "sirt2_row_ids": counts.index[counts.annot_gene_name.eq("Sirt2")].tolist(),
        "ube2d1_immediate_agent": ube_rows.reset_index().to_dict("records"),
        "paper_validation_genes_absent_from_selected_matrix": [
            g for g in ("Fbxo32", "Fos") if not counts.annot_gene_name.eq(g).any()],
        "comparisons": comparisons,
        "limitation": "Counts compare gene-level paper results to transcript-row agent results; they are not gene recall or proof of no exercise effect.",
    }


def circadian_case() -> dict:
    paper = "data/papers/GSE282641_40627397.txt"
    repeats = []
    for repeat in range(1, 4):
        run = STABILITY / f"repeat_{repeat:02d}/runs/cohort_GSE282641/GSE282641"
        decisions = document(run / "decisions.json")
        da = next(x for x in decisions["decisions"] if x["step"] == "deseq2")
        gsea = frame(run / "DEG_results_ko_vs_wt_GSEA_Hallmark.csv")
        selected = gsea[gsea.Term.isin([
            "HALLMARK_OXIDATIVE_PHOSPHORYLATION", "HALLMARK_GLYCOLYSIS",
            "HALLMARK_FATTY_ACID_METABOLISM",
        ])][["Term", "NES", "FDR q-val"]]
        repeats.append({"repeat": repeat, "model": da["details"]["model_params"],
                        "da": count_da(run / "DEG_results_ko_vs_wt.csv"),
                        "n_gsea_fdr_lt_025": int(gsea["FDR q-val"].lt(.25).sum()),
                        "pathways": selected.to_dict("records")})
    meta = frame(STABILITY / "repeat_01/runs/cohort_GSE282641/GSE282641/GSE282641_metadata_aligned.csv")
    return {
        "classification": "main_claim_not_tested_direction_consistent",
        "confirmed_opposite_primary_conclusion": False,
        "paper_anchors": [paper_anchor(paper, phrase) for phrase in (
            "~0 + group + sex", "One sample was excluded due to low coverage",
            "ZT3 (N = 516)", "ZT15 (N = 91)")],
        "metadata_sample_count": len(meta),
        "design_dimensions": {c: meta[c].value_counts().to_dict() for c in meta
                              if c.startswith("characteristics_ch1")},
        "repeats": repeats,
    }


def card_inventory() -> dict:
    paths = sorted(Path("output/claim_evidence_repeat_v1").glob("repeat_*/cards/*.json"))
    if len(paths) != 24:
        raise ValueError(f"Expected archived 8 x 3 cards; found {len(paths)}")
    relations, origins = Counter(), Counter()
    for path in paths:
        card = document(path)
        evidence = {e["evidence_id"]: e for e in card["evidence"]}
        for link in card["links"]:
            relations[link["relation"]] += 1
            origins[evidence.get(link.get("evidence_id"), {}).get("origin", "none")] += 1
    return {"n_cards": len(paths), "relation_counts": dict(relations),
            "linked_evidence_origins": dict(origins),
            "limitation": "Machine draft inventory, not an independent biological correctness score."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("output/paper_discrepancy_audit_20260909/evidence.json"))
    args = parser.parse_args()
    result = {"schema_version": "1.0", "audit_date": "2026-09-09",
              "audit_type": "archived_result_recount_no_new_analysis",
              "GSE279359": splicing_case(), "GSE282641": circadian_case(),
              "claim_cards": card_inventory()}
    final_xml = source("output/paper_discrepancy_audit_20260909/PMC12312519.xml")
    final_text = " ".join(" ".join(ET.fromstring(final_xml.read_bytes()).itertext()).split())
    final_anchors = {}
    for phrase in ("46 genes", "32 genes", "49 genes", "Swan v2.0"):
        offset = final_text.find(phrase)
        if offset < 0:
            raise ValueError(f"Published article anchor missing: {phrase}")
        final_anchors[phrase] = offset
    result["GSE279359"]["published_version_check"] = {
        "source": final_xml.as_posix(),
        "url": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12312519/fullTextXML",
        "article_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12312519/",
        "normalized_text_offsets": final_anchors,
    }
    deck = source("output/presentation_sample_20260826/bioinformatics_agent_report_short_20260827_final_title.pptx")
    with zipfile.ZipFile(deck) as z:
        result["presentation_slides"] = {
            str(n): " | ".join(e.text for e in
                               ET.fromstring(z.read(f"ppt/slides/slide{n}.xml"))
                               .iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t")
                               if e.text) for n in (6, 7, 8, 10)
        }
    source("output/bo_discussion_materials_20260903/BO_DISCUSSION_BRIEF.md")
    source("output/full_pipeline_stability_20x3_20260825/agent_evaluation.md")
    result["sources"] = SOURCES
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                           encoding="utf-8")
    print(f"Evidence written: {args.output.resolve()} ({len(SOURCES)} hashed sources)")


if __name__ == "__main__":
    main()
