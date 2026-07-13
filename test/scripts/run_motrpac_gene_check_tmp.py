import csv
import os
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from typing import List, Optional

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

from tools.seacdm_tools import extract_reported_findings, gene_rows_from_reported_findings


STUDY = "PMC11062907"
TEXT = Path("data/papers/PMC11062907.txt").read_text(encoding="utf-8", errors="ignore")
OUTDIR = "output/motrpac_paper_gene_check"


class ComparedGene(BaseModel):
    gene_symbol: str = Field(description="Gene/protein symbol exactly as written in the text")
    measurement: Optional[str] = Field(default=None, description="transcript/protein/phosphosite/kinase activity/etc.")
    tissue: Optional[str] = Field(default=None)
    direction_or_role: Optional[str] = Field(default=None, description="increased/decreased/target/substrate/driver/etc.")
    comparison: Optional[str] = Field(default=None, description="training/exercise comparison or timepoint")
    source: str = Field(description="short exact quote copied from the provided text")


class ComparedGeneExtraction(BaseModel):
    genes: List[ComparedGene] = Field(default_factory=list)


def extract_compared_genes_limited(text: str) -> tuple[list[dict], dict]:
    load_dotenv()
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return [], {"error": "CLAUDE_API_KEY missing"}
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=api_key,
        temperature=0,
        max_tokens=3000,
    )
    structured = llm.with_structured_output(ComparedGeneExtraction, include_raw=True)
    prompt = f"""Extract at most 15 named genes/proteins from the text below.

Only include genes/proteins that are explicitly connected to endurance training, exercise response,
training-regulated transcripts/proteins/phosphosites, kinase activity, substrates, or comparison across
training time/sex/tissue. Do not include generic method names, repository names, database names, or genes
that appear only in references/background.

For each item:
- gene_symbol must be copied exactly as printed.
- source must be a short exact quote from the text below.
- If many genes are present, prefer the first 15 with an explicit direction, substrate/target relation, or tissue.

TEXT START
{text}
TEXT END
"""
    res = structured.invoke(prompt)
    raw = res.get("raw")
    parsed = res.get("parsed")
    usage = getattr(raw, "usage_metadata", None) or {}
    rows = [g.model_dump() for g in (parsed.genes if parsed else [])]
    return rows, usage


def main():
    print("paper_chars", len(TEXT))
    for key in ["Results", "Discussion", "Extended Data", "Data availability", "GSE242358"]:
        print("section", key, TEXT.find(key))

    os.makedirs(OUTDIR, exist_ok=True)
    if os.getenv("RUN_FULL_FINDINGS", "0") == "1":
        report = {}
        usage = []
        findings = extract_reported_findings(
            STUDY,
            TEXT[:100000],
            organism="Rat",
            verify=True,
            report=report,
            usage=usage,
        )
        genes = gene_rows_from_reported_findings(
            STUDY,
            findings,
            organism="Rat",
            tables={
                "experiment": [{"experiment_id": f"{STUDY}_exp1"}],
                "interventions": [{
                    "intervention_id": f"{STUDY}_exp1_int1",
                    "material": "endurance exercise training",
                    "intervention_type": "exercise",
                }],
            },
        )

        with open(os.path.join(OUTDIR, "reported_findings.csv"), "w", newline="", encoding="utf-8") as f:
            fieldnames = ["entity", "entity_type", "direction", "magnitude", "comparison", "source"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(findings)

        gene_fieldnames = list(genes[0].keys()) if genes else ["gene_id", "study_id", "gene_symbol"]
        with open(os.path.join(OUTDIR, "gene.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=gene_fieldnames)
            writer.writeheader()
            writer.writerows(genes)

        print({
            "report": report,
            "usage": usage,
            "n_findings": len(findings),
            "n_gene_rows": len(genes),
            "outdir": OUTDIR,
        })
        print("genes", [g.get("gene_symbol") for g in genes[:50]])

    gene_hints = [
        "HGF", "SRC", "PRKACA", "MEF2C", "PLIN4",
    ]
    chunks = []
    lowered = TEXT.lower()
    for hint in gene_hints:
        pos = lowered.find(hint.lower())
        if pos >= 0:
            chunks.append(TEXT[max(0, pos - 450): min(len(TEXT), pos + 850)])
    excerpt = "\n\n---\n\n".join(dict.fromkeys(chunks))
    Path(os.path.join(OUTDIR, "gene_rich_excerpt.txt")).write_text(
        excerpt, encoding="utf-8"
    )

    if os.getenv("RUN_FULL_FINDINGS", "0") == "1":
        excerpt_report = {}
        excerpt_usage = []
        excerpt_findings = extract_reported_findings(
            STUDY,
            excerpt,
            organism="Rat",
            verify=True,
            report=excerpt_report,
            usage=excerpt_usage,
        )
        excerpt_genes = gene_rows_from_reported_findings(
            STUDY,
            excerpt_findings,
            organism="Rat",
            tables={
                "experiment": [{"experiment_id": f"{STUDY}_exp1"}],
                "interventions": [{
                    "intervention_id": f"{STUDY}_exp1_int1",
                    "material": "endurance exercise training",
                    "intervention_type": "exercise",
                }],
            },
        )
        with open(os.path.join(OUTDIR, "gene_excerpt.csv"), "w", newline="", encoding="utf-8") as f:
            fieldnames = list(excerpt_genes[0].keys()) if excerpt_genes else ["gene_id", "study_id", "gene_symbol"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(excerpt_genes)
        print({
            "excerpt_chars": len(excerpt),
            "excerpt_report": excerpt_report,
            "excerpt_usage": excerpt_usage,
            "excerpt_findings": len(excerpt_findings),
            "excerpt_gene_rows": len(excerpt_genes),
        })
        print("excerpt_genes", [g.get("gene_symbol") for g in excerpt_genes])

    limited_genes, limited_usage = extract_compared_genes_limited(excerpt)
    with open(os.path.join(OUTDIR, "compared_genes_limited.csv"), "w", newline="", encoding="utf-8") as f:
        fieldnames = ["gene_symbol", "measurement", "tissue", "direction_or_role", "comparison", "source"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(limited_genes)
    print({
        "limited_gene_rows": len(limited_genes),
        "limited_usage": limited_usage,
        "limited_out": os.path.join(OUTDIR, "compared_genes_limited.csv"),
    })
    print("limited_genes", [g.get("gene_symbol") for g in limited_genes])


if __name__ == "__main__":
    main()
