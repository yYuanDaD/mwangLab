"""PDF → Markdown → structured paper, for papers without Europe PMC full-text XML.

About half of the evaluated papers have no Europe PMC open-access XML, so their only
source is the publisher PDF. This module converts the PDF to Markdown with an existing
open-source converter and hands the Markdown to ``paper_structure.parse_markdown``,
which produces the same document schema (sections, ``TAB``/``FIG`` blocks, citable
block IDs) as the JATS route.

Backends, tried in this order by ``backend="auto"``:

    docling      IBM Docling (MIT). Layout model + TableFormer: best reading order on
                 two-column papers and real table cells. Downloads its models from
                 Hugging Face on first use. ``pip install docling``
    pymupdf4llm  PyMuPDF4LLM (AGPL). No models, fast, offline; tables via PyMuPDF's
                 table finder, headings from font size. ``pip install pymupdf4llm``
    pypdf        Plain text + heuristic headings (``parse_pdf_pages``); no tables.
                 Always available (pypdf is a core dependency).

The ``structure_quality`` field records which backend produced the document
(``pdf_markdown:docling``, ``pdf_markdown:pymupdf4llm`` or ``pdf_heuristic``), so a
reviewer knows how far to trust table values and heading boundaries.

CLI (run from the repository root):

    python -m tools.pdf_markdown paper.pdf --out data/papers [--backend docling] [--stem ID]
    python -m tools.pdf_markdown --check          # which backends are installed
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

from tools import paper_structure as ps

BACKENDS = ("docling", "pymupdf4llm", "pypdf")
_MODULE = {"docling": "docling", "pymupdf4llm": "pymupdf4llm", "pypdf": "pypdf"}
_docling_converter = None


def available_backends() -> list[str]:
    return [b for b in BACKENDS if importlib.util.find_spec(_MODULE[b]) is not None]


def _docling_markdown(path: str) -> str:
    global _docling_converter
    if _docling_converter is None:   # model loading is slow; reuse across papers
        from docling.document_converter import DocumentConverter
        _docling_converter = DocumentConverter()
    return _docling_converter.convert(path).document.export_to_markdown()


def _pymupdf4llm_markdown(path: str) -> str:
    import pymupdf4llm
    return pymupdf4llm.to_markdown(path, show_progress=False)


def _pypdf_pages(path: str) -> list[str]:
    from pypdf import PdfReader
    pages = []
    for p in PdfReader(path).pages:
        try:
            pages.append(p.extract_text() or "")
        except Exception:
            pages.append("")
    return pages


def pdf_to_markdown(path: str, backend: str = "auto") -> tuple[str, str]:
    """Markdown for a PDF and the backend that produced it.

    ``backend="auto"`` tries docling, then pymupdf4llm. Raises RuntimeError when no
    Markdown backend is installed or every one fails (callers fall back to pypdf).
    """
    order = [b for b in ("docling", "pymupdf4llm") if backend in ("auto", b)]
    if not order:
        raise ValueError(f"unknown Markdown backend {backend!r}; choose from docling, pymupdf4llm")
    errors = []
    for b in order:
        if importlib.util.find_spec(_MODULE[b]) is None:
            errors.append(f"{b}: not installed")
            continue
        try:
            md = _docling_markdown(path) if b == "docling" else _pymupdf4llm_markdown(path)
        except Exception as e:  # a converter crash should not lose the paper
            errors.append(f"{b}: {type(e).__name__}: {e}")
            continue
        if md and md.strip():
            return md, b
        errors.append(f"{b}: empty output (scanned PDF without a text layer?)")
    raise RuntimeError("; ".join(errors))


def structure_pdf(path: str, backend: str = "auto", source: str = "",
                  fetched_url: str = "") -> tuple[dict, str]:
    """Structured paper document for a PDF, plus the Markdown it was built from ('' for pypdf).

    Falls back to the heuristic pypdf parser when no Markdown backend works, so a PDF
    always yields a document (possibly with no tables).
    """
    source = source or f"PDF {os.path.basename(path)}"
    if backend != "pypdf":
        try:
            md, used = pdf_to_markdown(path, backend)
            doc = ps.parse_markdown(md, source=f"{source} via {used}", fetched_url=fetched_url,
                                    quality=f"pdf_markdown:{used}")
            if doc["blocks"]:
                return doc, md
            fallback_reason = f"{used} produced no blocks"
        except Exception as e:
            if backend != "auto":
                raise
            fallback_reason = str(e)
    else:
        fallback_reason = "pypdf requested"
    doc = ps.parse_pdf_pages(_pypdf_pages(path), source=source, fetched_url=fetched_url)
    doc["markdown_fallback_reason"] = fallback_reason
    return doc, ""


def save_pdf(path: str, out_dir: str, stem: str = "", backend: str = "auto",
             source: str = "", fetched_url: str = "") -> tuple[dict, dict]:
    """Structure a PDF and write <stem>.paper.json, <stem>.paper.md and <stem>.converted.md."""
    doc, md = structure_pdf(path, backend, source, fetched_url)
    stem = stem or os.path.splitext(os.path.basename(path))[0]
    paths = ps.save(doc, out_dir, stem)
    if md:
        paths["converted_md"] = os.path.join(out_dir, f"{stem}.converted.md")
        with open(paths["converted_md"], "w", encoding="utf-8") as f:
            f.write(md)
    return doc, paths


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.pdf_markdown", description=__doc__.split("\n")[0])
    ap.add_argument("pdf", nargs="*")
    ap.add_argument("--out", default="data/papers")
    ap.add_argument("--backend", default="auto", choices=("auto",) + BACKENDS)
    ap.add_argument("--stem", default="", help="output file stem (single PDF only)")
    ap.add_argument("--check", action="store_true", help="list installed backends and exit")
    a = ap.parse_args(argv)
    if a.check or not a.pdf:
        print("installed backends:", ", ".join(available_backends()) or "none")
        return 0
    rc = 0
    for pdf in a.pdf:
        try:
            doc, paths = save_pdf(pdf, a.out, a.stem if len(a.pdf) == 1 else "", a.backend)
        except Exception as e:
            print(f"{pdf}: FAILED {type(e).__name__}: {e}", file=sys.stderr)
            rc = 1
            continue
        print(json.dumps(paths, indent=1))
        print(ps.outline(doc))
    return rc


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    sys.exit(_main())
