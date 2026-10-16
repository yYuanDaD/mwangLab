"""Structured full text for papers: sections, figures, tables, and citable block IDs.

``paper_tools.fetch_paper_text`` used to flatten Europe PMC JATS XML into one line of
plain text, which loses the section boundaries, table cells, and figure legends that
the paper-first workflow depends on (sample groups, design, method, threshold). This
module keeps that structure.

Every paragraph, figure legend, table, and supplementary file becomes a *block* with a
stable ID:

    ABS.p1      abstract paragraph 1
    S2.3.p1     body section 2, subsection 3, paragraph 1
    DA.p1       data-availability statement
    FIG1        first figure legend (in document order)
    TAB2        second table, rendered as a Markdown table
    SUP1        first supplementary file (label, caption, file name)

Use the IDs as ``paper.locator`` / ``source_locator`` values in decision records so a
reviewer can resolve them with ``resolve_locator`` and read the exact evidence.

Reading is by section, not by vector top-k: ``read_section(doc, "methods")`` returns
the whole Methods section, so a sample-group table or a statistics paragraph is never
cut in half.

Standard library only (xml.etree); ``requests`` is imported lazily for ``fetch``.

CLI (run from the repository root):

    python -m tools.paper_structure fetch PMC12989000 --out data/papers
    python -m tools.paper_structure parse paper.xml --out data/papers
    python -m tools.paper_structure outline data/papers/PMC12989000.paper.json
    python -m tools.paper_structure section data/papers/PMC12989000.paper.json methods
    python -m tools.paper_structure block   data/papers/PMC12989000.paper.json S2.2.p1 TAB1
    python -m tools.paper_structure find    data/papers/PMC12989000.paper.json sedentary control
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Iterable

SCHEMA_VERSION = 1
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
EPMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
EPMC_SUPPLEMENTS = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/supplementaryFiles"

# Section classes, matched against section titles in this order (first match wins), so
# "Results and discussion" is results and "Materials and methods" is methods.
SECTION_CLASSES = (
    "abstract", "introduction", "methods", "results", "discussion", "conclusion",
    "data_availability", "supplementary", "other",
)
_TITLE_RULES: tuple[tuple[str, re.Pattern], ...] = (
    ("data_availability", re.compile(
        r"data\b.{0,30}\b(availab|access|deposit|sharing)|availability of (data|materials)|"
        r"accession (number|code)|code availab|data and code|data access", re.I)),
    ("supplementary", re.compile(r"supplement|supporting information|additional (file|information)", re.I)),
    ("methods", re.compile(
        r"method|materials?\b|experimental (design|procedure|section|model)|study design|"
        r"patients|participants|subjects|animals?\b|statistic|sample collection|protocol", re.I)),
    ("results", re.compile(r"result|findings", re.I)),
    ("discussion", re.compile(r"discussion", re.I)),
    ("conclusion", re.compile(r"conclu", re.I)),
    ("introduction", re.compile(r"introduction|background", re.I)),
    ("abstract", re.compile(r"^\s*(abstract|summary)\s*$", re.I)),
)
_SEC_TYPE_RULES = (
    ("data_availability", ("data-availability", "data_availability", "data-access")),
    ("supplementary", ("supplementary-material", "supplementary")),
    ("methods", ("methods", "materials", "materials|methods", "subjects", "cases")),
    ("results", ("results",)),
    ("discussion", ("discussion",)),
    ("conclusion", ("conclusions", "conclusion")),
    ("introduction", ("intro", "introduction")),
)
_CLASS_ALIASES = {
    "method": "methods", "materials": "methods", "results": "results", "result": "results",
    "intro": "introduction", "conclusions": "conclusion", "data": "data_availability",
    "data_availability": "data_availability", "availability": "data_availability",
    "supplement": "supplementary", "supplementary": "supplementary", "supp": "supplementary",
    "figure": "figures", "figures": "figures", "fig": "figures", "legends": "figures",
    "table": "tables", "tables": "tables",
}

# Repository accessions worth indexing (where each one is mentioned).
_ACCESSION_RE = re.compile(
    r"\b(GSE\d{3,}|GSM\d{3,}|GDS\d{3,}|SRP\d{4,}|SRR\d{4,}|SRX\d{4,}|PRJNA\d{3,}|PRJEB\d{3,}|"
    r"E-[A-Z]{4}-\d+|PXD\d{6}|ERP\d{4,}|phs\d{6}|HRA\d{6}|CRA\d{6})\b"
)

_FLOAT_TAGS = {"fig", "fig-group", "table-wrap", "table-wrap-group", "supplementary-material"}
_SKIP_INLINE = _FLOAT_TAGS | {"label", "title", "alternatives"}


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _local(tag) -> str:
    """Element tag without namespace ('' for comments/processing instructions)."""
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1]


def _clean(s: str) -> str:
    s = s.replace("\u00a0", " ").replace("\u2009", " ")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _formula_text(el) -> str:
    for t in el.iter():
        if _local(t.tag) == "tex-math" and (t.text or "").strip():
            return f"${t.text.strip()}$"
    return "".join(el.itertext())


def _inline(el, skip: set[str] = _SKIP_INLINE, top: bool = True) -> str:
    """Text of an element, skipping floats (emitted as their own blocks)."""
    parts: list[str] = []
    if el.text:
        parts.append(el.text)
    for child in el:
        name = _local(child.tag)
        if name in skip:
            pass
        elif name in ("inline-formula", "disp-formula"):
            parts.append(_formula_text(child))
        elif name == "break":
            parts.append("\n")
        elif name == "list":
            items = [_inline(li, skip, False) for li in child if _local(li.tag) == "list-item"]
            parts.append("\n" + "\n".join(f"- {_clean(i)}" for i in items if _clean(i)) + "\n")
        elif name in ("sup",):
            parts.append("^" + _inline(child, skip, False))
        elif name in ("sub",):
            parts.append("_" + _inline(child, skip, False))
        elif name:
            parts.append(_inline(child, skip, False))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _title_of(el) -> str:
    t = el.find("title")
    return _clean(_inline(t, set())) if t is not None else ""


def _label_of(el) -> str:
    t = el.find("label")
    return _clean("".join(t.itertext())) if t is not None else ""


def _caption_of(el) -> str:
    cap = el.find("caption")
    if cap is None:
        return ""
    pieces = []
    title = cap.find("title")
    if title is not None:
        pieces.append(_clean(_inline(title, set())))
    for p in cap:
        if _local(p.tag) == "p":
            pieces.append(_clean(_inline(p)))
    return _clean(" ".join(x for x in pieces if x))


def classify_title(title: str, sec_type: str = "") -> str:
    """Map a section title (and optional JATS sec-type) to a SECTION_CLASSES value."""
    st = (sec_type or "").strip().lower()
    for cls, names in _SEC_TYPE_RULES:
        if st in names or any(st.startswith(n) for n in names if "|" not in n):
            return cls
    for cls, rx in _TITLE_RULES:
        if rx.search(title or ""):
            return cls
    return "other"


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------

def _cell_text(cell) -> str:
    txt = _clean(_inline(cell, {"label"}))
    return txt.replace("|", "\\|").replace("\n", " / ")


def _table_rows(table) -> tuple[list[list[str]], int]:
    """Grid of cell texts with rowspan/colspan expanded (spanned text is repeated).

    Returns (rows, n_header_rows).
    """
    rows: list[list[str]] = []
    n_head = 0
    carry: dict[int, tuple[int, str]] = {}  # column -> (rows remaining, text)
    trs = []
    for part in table:
        name = _local(part.tag)
        if name == "tr":
            trs.append((part, False))
        elif name in ("thead", "tbody", "tfoot"):
            for tr in part:
                if _local(tr.tag) == "tr":
                    trs.append((tr, name == "thead"))
    for tr, in_head in trs:
        cells = [c for c in tr if _local(c.tag) in ("td", "th")]
        row: list[str] = []
        col = 0
        it = iter(cells)
        nxt = next(it, None)
        while nxt is not None or col in carry:
            if col in carry:
                left, text = carry[col]
                row.append(text)
                if left <= 1:
                    del carry[col]
                else:
                    carry[col] = (left - 1, text)
                col += 1
                continue
            cell = nxt
            nxt = next(it, None)
            text = _cell_text(cell)
            try:
                cspan = max(1, int(cell.get("colspan", "1") or 1))
                rspan = max(1, int(cell.get("rowspan", "1") or 1))
            except ValueError:
                cspan, rspan = 1, 1
            for _ in range(cspan):
                row.append(text)
                if rspan > 1:
                    carry[col] = (rspan - 1, text)
                col += 1
        rows.append(row)
        if in_head:
            n_head += 1
    if not n_head and trs and all(_local(c.tag) == "th" for c in trs[0][0] if _local(c.tag) in ("td", "th")):
        n_head = 1
    return rows, n_head


def table_to_markdown(table) -> str:
    rows, n_head = _table_rows(table)
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    if n_head >= 1:
        header = []
        for c in range(width):
            seen: list[str] = []
            for r in rows[:n_head]:
                if r[c] and r[c] not in seen:
                    seen.append(r[c])
            header.append(" / ".join(seen))
        body = rows[n_head:]
    else:
        header, body = rows[0], rows[1:]
    out = ["| " + " | ".join(h or " " for h in header) + " |",
           "|" + "|".join(["---"] * width) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# JATS parsing
# ---------------------------------------------------------------------------

class _Builder:
    def __init__(self):
        self.sections: list[dict] = []
        self.blocks: list[dict] = []
        self.counters = {"figure": 0, "table": 0, "supplement": 0}
        self._para_count: dict[str, int] = {}

    def add_section(self, sid: str, title: str, cls: str, level: int, parent: str | None,
                    path: list[str]) -> dict:
        sec = {"id": sid, "title": title, "class": cls, "level": level, "parent": parent,
               "path": path, "block_ids": []}
        self.sections.append(sec)
        return sec

    def add_block(self, sec: dict, kind: str, text: str, **extra) -> dict | None:
        text = _clean(text)
        if not text and kind == "paragraph":
            return None
        if kind in self.counters:
            self.counters[kind] += 1
            prefix = {"figure": "FIG", "table": "TAB", "supplement": "SUP"}[kind]
            bid = f"{prefix}{self.counters[kind]}"
        else:
            n = self._para_count.get(sec["id"], 0) + 1
            self._para_count[sec["id"]] = n
            bid = f"{sec['id']}.p{n}"
        block = {"id": bid, "kind": kind, "section_id": sec["id"], "section_class": sec["class"],
                 "section_path": sec["path"], "text": text}
        block.update({k: v for k, v in extra.items() if v not in (None, "", [])})
        self.blocks.append(block)
        sec["block_ids"].append(bid)
        return block

    # -- floats ---------------------------------------------------------
    def add_figure(self, sec: dict, fig) -> None:
        label, caption = _label_of(fig), _caption_of(fig)
        text = f"**{label}** {caption}" if label else caption
        self.add_block(sec, "figure", text or "(figure without caption)", label=label,
                       anchor=fig.get("id"))

    def add_table(self, sec: dict, tw) -> None:
        label, caption = _label_of(tw), _caption_of(tw)
        md_tables = [table_to_markdown(t) for t in tw.iter() if _local(t.tag) == "table"]
        md = "\n\n".join(m for m in md_tables if m)
        foot = []
        for f in tw.iter():
            if _local(f.tag) == "table-wrap-foot":
                foot.append(_clean(_inline(f, {"label"})))
        head = f"**{label}** {caption}".strip() if label else caption
        body = md or "(table provided only as an image; contents not machine-readable)"
        text = "\n\n".join(x for x in (head, body, "\n".join(foot)) if x)
        self.add_block(sec, "table", text, label=label, anchor=tw.get("id"),
                       image_only=not bool(md))

    def add_supplement(self, sec: dict, sm) -> None:
        label, caption = _label_of(sm), _caption_of(sm)
        files = []
        for m in sm.iter():
            href = m.get(XLINK_HREF)
            if href and _local(m.tag) in ("media", "graphic", "inline-supplementary-material",
                                          "supplementary-material", "ext-link"):
                files.append(href)
        if not caption:
            caption = _clean(_inline(sm, {"label", "caption"}))
        text = " ".join(x for x in (f"**{label}**" if label else "", caption) if x)
        if files:
            text += "\nFiles: " + ", ".join(files)
        self.add_block(sec, "supplement", text or "(supplementary file)", label=label,
                       files=files, anchor=sm.get("id"))

    def add_floats_within(self, sec: dict, el) -> None:
        for d in el.iter():
            if d is el:
                continue
            name = _local(d.tag)
            if name == "fig":
                self.add_figure(sec, d)
            elif name == "table-wrap":
                self.add_table(sec, d)
            elif name == "supplementary-material":
                self.add_supplement(sec, d)

    # -- containers -----------------------------------------------------
    def walk(self, el, sec: dict, child_prefix: str) -> None:
        """Emit blocks for el's children into sec; nested <sec> become subsections."""
        sub = 0
        for child in el:
            name = _local(child.tag)
            if name in ("title", "label", "sec-meta", "") or name == "ref-list":
                continue
            if name == "sec":
                if re.fullmatch(r"\s*(references?|bibliography|literature cited)\s*", _title_of(child), re.I):
                    continue
                sub += 1
                self.walk_section(child, f"{child_prefix}.{sub}" if child_prefix else f"S{sub}",
                                  parent=sec)
            elif name == "p":
                self.add_block(sec, "paragraph", _inline(child))
                self.add_floats_within(sec, child)
            elif name in ("fig", "fig-group"):
                if name == "fig":
                    self.add_figure(sec, child)
                else:
                    self.add_floats_within(sec, child)
            elif name in ("table-wrap", "table-wrap-group"):
                if name == "table-wrap":
                    self.add_table(sec, child)
                else:
                    self.add_floats_within(sec, child)
            elif name == "supplementary-material":
                self.add_supplement(sec, child)
            elif name in ("boxed-text", "app", "app-group", "notes"):
                self.walk(child, sec, child_prefix)
            elif name in ("list", "def-list", "disp-formula", "statement", "disp-quote",
                          "preformat", "verse-group"):
                if name == "list":
                    text = "\n".join(f"- {_clean(_inline(li))}" for li in child
                                     if _local(li.tag) == "list-item")
                else:
                    text = _inline(child)
                self.add_block(sec, "paragraph", text)
                self.add_floats_within(sec, child)

    def walk_section(self, el, sid: str, parent: dict | None, title: str | None = None,
                     cls: str | None = None) -> dict:
        title = title if title is not None else _title_of(el)
        own = classify_title(title, el.get("sec-type", ""))
        if cls is None:
            if parent is None or parent["class"] in ("other",):
                cls = own
            elif own in ("data_availability", "supplementary"):
                cls = own
            else:
                cls = parent["class"]
        path = (parent["path"] if parent else []) + [title or sid]
        level = (parent["level"] + 1) if parent else 1
        sec = self.add_section(sid, title, cls, level, parent["id"] if parent else None, path)
        self.walk(el, sec, sid)
        return sec


def _meta(root) -> dict:
    meta: dict = {}
    am = root.find(".//front/article-meta")
    if am is None:
        return meta
    tg = am.find("title-group/article-title")
    if tg is not None:
        meta["title"] = _clean(_inline(tg, set()))
    for aid in am.findall("article-id"):
        t = (aid.get("pub-id-type") or "").lower()
        v = (aid.text or "").strip()
        if t in ("pmc", "pmcid"):
            meta["pmcid"] = v if v.upper().startswith("PMC") else f"PMC{v}"
        elif t == "pmid":
            meta["pmid"] = v
        elif t == "doi":
            meta["doi"] = v
    jt = root.find(".//front/journal-meta//journal-title")
    if jt is not None:
        meta["journal"] = _clean("".join(jt.itertext()))
    for pd in am.findall("pub-date"):
        y = pd.findtext("year")
        if y:
            meta["year"] = y.strip()
            break
    return meta


def parse_jats(xml: bytes | str, source: str = "", fetched_url: str = "") -> dict:
    """Parse JATS XML (Europe PMC / PMC OA) into a structured paper document."""
    root = ET.fromstring(xml if isinstance(xml, (bytes, bytearray)) else xml.encode("utf-8"))
    if _local(root.tag) != "article":
        art = next((e for e in root.iter() if _local(e.tag) == "article"), None)
        if art is None:
            raise ValueError("No <article> element found; not JATS XML.")
        root = art
    b = _Builder()
    meta = _meta(root)

    # Abstract: the first abstract without abstract-type (or the first one at all).
    abstracts = root.findall(".//front/article-meta/abstract")
    main_abs = next((a for a in abstracts if not a.get("abstract-type")), abstracts[0] if abstracts else None)
    if main_abs is not None:
        sec = b.add_section("ABS", "Abstract", "abstract", 1, None, ["Abstract"])
        # Structured abstracts (Background/Methods/...) are flattened with bold run-in titles.
        for child in main_abs:
            name = _local(child.tag)
            if name == "p":
                b.add_block(sec, "paragraph", _inline(child))
            elif name == "sec":
                t = _title_of(child)
                for p in child.iter():
                    if _local(p.tag) == "p":
                        txt = _inline(p)
                        b.add_block(sec, "paragraph", f"**{t}.** {txt}" if t else txt)

    # Front-matter notes (e.g. Data in Brief "Specifications Table").
    for i, n in enumerate(root.findall("./front/notes"), 1):
        b.walk_section(n, f"FN{i}" if i > 1 else "FN", None)

    body = root.find("body")
    if body is not None:
        loose = [c for c in body if _local(c.tag) != "sec"]
        if any(_local(c.tag) in ("p", "fig", "table-wrap", "list") for c in loose):
            s0 = b.add_section("S0", "", "other", 1, None, ["(untitled)"])
            for c in loose:
                wrapper = ET.Element("x")
                wrapper.append(c)
                b.walk(wrapper, s0, "S0")
        n = 0
        for c in body:
            if _local(c.tag) == "sec":
                # "Associated Data" is a Europe PMC wrapper that repeats the supplements
                # and data-availability statement already present elsewhere.
                if re.fullmatch(r"\s*(references?|bibliography|literature cited|associated data)\s*",
                                _title_of(c), re.I):
                    continue
                n += 1
                b.walk_section(c, f"S{n}", None)

    back = root.find("back")
    if back is not None:
        da_n = 0
        bk_n = 0
        for c in back:
            name = _local(c.tag)
            if name in ("ref-list", "fn-group", "glossary", "ack", "ref"):
                continue
            if name in ("notes", "sec", "app-group", "app"):
                title = _title_of(c)
                if not title and name == "notes":
                    inner = c.find("sec")
                    title = _title_of(inner) if inner is not None else ""
                cls = classify_title(title, c.get("notes-type", "") or c.get("sec-type", ""))
                if cls == "data_availability":
                    da_n += 1
                    sid = "DA" if da_n == 1 else f"DA{da_n}"
                elif name in ("app-group", "app"):
                    bk_n += 1
                    sid = f"APP{bk_n}"
                else:
                    # Funding, contributions, declarations: rarely needed, kept as BK sections.
                    bk_n += 1
                    sid = f"BK{bk_n}"
                b.walk_section(c, sid, None, title=title or name, cls=cls)

    # Figures and tables collected at the end of the article (<floats-group>).
    floats = root.find("floats-group")
    if floats is not None and len(floats):
        sec = b.add_section("FLT", "Figures and tables", "other", 1, None, ["Figures and tables"])
        b.walk(floats, sec, "FLT")

    # Supplementary material declared outside any walked container.
    # Match on file names too: Europe PMC's "Associated Data" wrapper repeats the same
    # files under new element ids.
    seen_ids = {blk.get("anchor") for blk in b.blocks if blk["kind"] == "supplement"}
    seen_files = {f for blk in b.blocks if blk["kind"] == "supplement" for f in blk.get("files", [])}
    extra = []
    for sm in root.iter():
        if _local(sm.tag) != "supplementary-material" or not sm.get("id") or sm.get("id") in seen_ids:
            continue
        files = {m.get(XLINK_HREF) for m in sm.iter() if m.get(XLINK_HREF)}
        if files and files <= seen_files:
            continue
        extra.append(sm)
    if extra:
        sec = b.add_section("SUPP", "Supplementary material", "supplementary", 1, None,
                            ["Supplementary material"])
        for sm in extra:
            b.add_supplement(sec, sm)

    # Drop empty sections that have no subsections (untitled wrappers, empty notes).
    parents = {s["parent"] for s in b.sections if s["parent"]}
    b.sections = [s for s in b.sections if s["block_ids"] or s["id"] in parents]

    doc = {
        "schema_version": SCHEMA_VERSION,
        "structure_quality": "jats",
        "source": source,
        "fetched_url": fetched_url,
        **meta,
        "sections": b.sections,
        "blocks": b.blocks,
    }
    if meta.get("pmcid"):
        doc["supplementary_download_url"] = EPMC_SUPPLEMENTS.format(pmcid=meta["pmcid"])
    doc["accession_mentions"] = accession_index(doc)
    return doc


# ---------------------------------------------------------------------------
# PDF fallback (degraded: heuristic headings, chunked paragraphs)
# ---------------------------------------------------------------------------

_PDF_HEADING = re.compile(
    r"^\s*(?:\d{1,2}(?:\.\d{1,2})*\.?\s+)?"
    r"(abstract|summary|introduction|background|results?(?: and discussion)?|discussion|"
    r"conclusions?|(?:materials? and )?methods?(?: and materials?)?|experimental (?:procedures|section)|"
    r"star\s*methods|data (?:and code )?availability(?: statement)?|data access|"
    r"supplementary (?:material|information)|acknowledge?ments?|references|funding)\s*:?\s*$",
    re.I,
)


def _chunk(text: str, target: int = 1200) -> list[str]:
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z(\[])", re.sub(r"\s+", " ", text).strip())
    out, cur = [], ""
    for s in sents:
        if cur and len(cur) + len(s) > target:
            out.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        out.append(cur)
    return out


def parse_pdf_pages(pages: list[str], source: str = "", fetched_url: str = "") -> dict:
    """Structure plain PDF text by heuristic headings. Tables are NOT recovered.

    Quality is marked ``pdf_heuristic``; reviewers should treat locators as approximate
    and check table values against the PDF itself.
    """
    b = _Builder()
    sec = b.add_section("S0", "", "other", 1, None, ["(front matter)"])
    n = 0
    buf: list[str] = []
    stop = False

    def flush():
        for c in _chunk("\n".join(buf)):
            b.add_block(sec, "paragraph", c)
        buf.clear()

    for pno, page in enumerate(pages, 1):
        for line in (page or "").splitlines():
            m = _PDF_HEADING.match(line)
            if m:
                flush()
                title = m.group(1).strip()
                if re.match(r"references|acknowledge?ments?|funding", title, re.I):
                    stop = title.lower().startswith("reference")
                    if stop:
                        break
                cls = classify_title(title)
                if cls == "abstract" or title.lower() == "abstract":
                    sid = "ABS"
                    cls = "abstract"
                elif cls == "data_availability":
                    sid = "DA"
                else:
                    n += 1
                    sid = f"S{n}"
                if any(s["id"] == sid for s in b.sections):
                    n += 1
                    sid = f"S{n}"
                sec = b.add_section(sid, title, cls, 1, None, [title])
            else:
                buf.append(line)
        if stop:
            break
    flush()
    doc = {"schema_version": SCHEMA_VERSION, "structure_quality": "pdf_heuristic",
           "source": source, "fetched_url": fetched_url, "sections": b.sections,
           "blocks": b.blocks}
    doc["accession_mentions"] = accession_index(doc)
    return doc


# ---------------------------------------------------------------------------
# Markdown input (PDF converted by Docling / pymupdf4llm, or hand-written)
# ---------------------------------------------------------------------------

_MD_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
_MD_NUMBERED = re.compile(r"^\s*((?:\d{1,2}\.)*\d{1,2})\.?\s+(\S.*)$")
_MD_TABLE_CAPTION = re.compile(r"^(?:\*\*|_)*\s*(table\s*S?\d+[a-z]?)\b[.:|]?\s*(.*)$", re.I | re.S)
_MD_FIG_CAPTION = re.compile(r"^(?:\*\*|_)*\s*((?:figure|fig\.?)\s*S?\d+[a-z]?)\b[.:|]?\s*(.*)$", re.I | re.S)
_MD_STOP = re.compile(r"^(references?|bibliography|literature cited|works cited)$", re.I)
_MD_IMAGE = re.compile(r"^(<!--\s*image\s*-->|!\[[^\]]*\]\([^)]*\)|\*{0,2}==>\s*picture.*<==\*{0,2})$", re.I)
_MD_BACK_MATTER = re.compile(
    r"^(acknowledge?ments?|funding|author contributions?|conflicts? of interest|competing interests?|"
    r"declaration|ethics|abbreviations|keywords?|highlights|graphical abstract|footnotes?)", re.I)
_MD_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def _md_plain(s: str) -> str:
    """Heading text without emphasis markers or trailing colon."""
    s = re.sub(r"(\*\*|__|\*|_|`)", "", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(":").strip()


def _md_bold_heading(line: str) -> str | None:
    """A standalone bold/italic line that names a standard section (converters that
    miss the font-size cue still keep the emphasis)."""
    m = re.fullmatch(r"\s*(\*\*|__)(.+?)\1\s*", line)
    if not m:
        return None
    title = _md_plain(m.group(2))
    return title if _PDF_HEADING.match(title) else None


def _md_repeated_lines(lines: list[str]) -> set[str]:
    """Short lines that repeat many times (running headers, footers, journal names)."""
    counts: dict[str, int] = {}
    for ln in lines:
        t = ln.strip()
        if t and len(t) <= 90 and not t.startswith("|") and not _MD_HEADING.match(t):
            counts[t] = counts.get(t, 0) + 1
    out = set()
    for t, n in counts.items():
        if re.fullmatch(r"[-*_=\s]+", t):
            continue
        # Three repeats, or two of a line that is not a sentence (a journal header).
        if n >= 3 or (n == 2 and len(t) >= 15 and not re.search(r"[.!?]$", t)):
            out.add(t)
    return out


def _md_table_to_rows(lines: list[str]) -> str:
    """Normalise a pipe table: drop empty rows, keep one separator after the header."""
    rows = [ln.strip() for ln in lines if ln.strip()]
    body = [r for r in rows if not _MD_SEPARATOR.match(r)]
    if not body:
        return ""
    width = max(r.strip("|").count("|") + 1 for r in body)
    cells = []
    for r in body:
        c = [x.strip() for x in r.strip().strip("|").split("|")]
        cells.append(c + [""] * (width - len(c)))
    if all(not "".join(c) for c in cells):
        return ""
    out = ["| " + " | ".join(x or " " for x in cells[0]) + " |", "|" + "|".join(["---"] * width) + "|"]
    out += ["| " + " | ".join(c) + " |" for c in cells[1:]]
    return "\n".join(out)


def parse_markdown(md: str, source: str = "", fetched_url: str = "",
                   quality: str = "markdown") -> dict:
    """Structure Markdown (e.g. a PDF converted by Docling or pymupdf4llm) into the same
    document schema as :func:`parse_jats`.

    Headings become sections (classified like JATS titles; numbering such as "2.1."
    sets the nesting, because converters often emit every heading at the same level),
    pipe tables become ``TAB`` blocks with their "Table N" caption attached, "Figure N"
    paragraphs become ``FIG`` blocks, and everything after References is dropped.
    Running headers/footers that repeat on most pages are removed.
    """
    raw_lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    repeated = _md_repeated_lines(raw_lines)
    b = _Builder()
    front = b.add_section("S0", "", "other", 1, None, ["(front matter)"])
    sec = front
    title = ""
    top_n = 0
    stack: list[dict] = []          # numbered/nested sections, by level
    sub_counts: dict[str, int] = {}
    pending_caption: tuple[str, str] | None = None   # (label, caption) seen just before a table

    def new_section(heading: str) -> dict | None:
        nonlocal top_n, sec, stack
        plain = _md_plain(heading)
        if not plain:
            return None
        num, rest = None, plain
        m = _MD_NUMBERED.match(plain)
        if m and not re.match(r"^\d{4}\b", plain):
            num, rest = m.group(1), m.group(2).strip()
        cls_own = classify_title(rest)
        depth = num.count(".") + 1 if num else 1
        # Converters often emit every heading at one level, so an unnumbered heading
        # nests under the current top-level section when it is not itself a main
        # section name: Docling's flat "## Animals" or "## Statistical analysis"
        # inside "## Materials and methods", or a sentence-like Results subheading.
        top = stack[0] if stack else None
        if (num is None and top is not None and top["class"] != "other"
                and not _MD_BACK_MATTER.match(rest) and not _PDF_HEADING.match(rest)
                and cls_own in ("other", top["class"])):
            depth = 2
        while len(stack) >= depth:
            stack.pop()
        parent = stack[-1] if stack else None
        if parent is None:
            if cls_own == "abstract" and not any(s["id"] == "ABS" for s in b.sections):
                sid = "ABS"
            elif cls_own == "data_availability" and not any(s["id"] == "DA" for s in b.sections):
                sid = "DA"
            else:
                top_n += 1
                sid = f"S{top_n}"
            cls = cls_own
        else:
            sub_counts[parent["id"]] = sub_counts.get(parent["id"], 0) + 1
            sid = f"{parent['id']}.{sub_counts[parent['id']]}"
            cls = cls_own if cls_own in ("data_availability", "supplementary") else parent["class"]
        path = (parent["path"] if parent else []) + [plain]
        s = b.add_section(sid, plain, cls, (parent["level"] + 1) if parent else 1,
                          parent["id"] if parent else None, path)
        stack.append(s)
        sec = s
        return s

    def emit_paragraph(text: str) -> None:
        nonlocal pending_caption
        text = text.strip()
        if not text or _MD_IMAGE.match(text):
            return
        m = _MD_FIG_CAPTION.match(text)
        if m and len(text) < 2500:
            label = _md_plain(m.group(1))
            b.add_block(sec, "figure", f"**{label}** {m.group(2).strip()}".strip(), label=label)
            return
        m = _MD_TABLE_CAPTION.match(text)
        if m and len(text) < 1200:
            pending_caption = (_md_plain(m.group(1)), m.group(2).strip())
            return
        flush_caption()
        # Rejoin a paragraph that a page or column break split mid-sentence.
        last = b.blocks[-1] if b.blocks else None
        if (last and last["kind"] == "paragraph" and last["section_id"] == sec["id"]
                and re.match(r"^[a-z(]", text) and not re.search(r"[.!?:]\)?$", last["text"])):
            last["text"] = _clean(f"{last['text']} {text}")
            return
        b.add_block(sec, "paragraph", text)

    def flush_caption() -> None:
        """A "Table N" caption that was not followed by a table (table was an image)."""
        nonlocal pending_caption
        if pending_caption:
            label, cap = pending_caption
            pending_caption = None
            b.add_block(sec, "table", f"**{label}** {cap}\n\n(table provided only as an image; "
                        f"contents not machine-readable)", label=label, image_only=True)

    para: list[str] = []
    table: list[str] = []
    stopped = False

    def flush_para() -> None:
        if para:
            emit_paragraph(" ".join(x.strip() for x in para))
            para.clear()

    def flush_table() -> None:
        nonlocal pending_caption
        if not table:
            return
        md_tab = _md_table_to_rows(table)
        table.clear()
        if not md_tab:
            return
        label, cap = pending_caption or ("", "")
        pending_caption = None
        head = f"**{label}** {cap}".strip() if label else ""
        b.add_block(sec, "table", "\n\n".join(x for x in (head, md_tab) if x), label=label)

    for line in raw_lines:
        stripped = line.strip()
        if stripped in repeated or re.fullmatch(r"(page\s*)?\d{1,4}(\s*(of|/)\s*\d{1,4})?", stripped, re.I):
            continue
        if stripped.startswith("|"):
            flush_para()
            table.append(stripped)
            continue
        flush_table()
        hm = _MD_HEADING.match(line)
        heading = hm.group(2) if hm else _md_bold_heading(line)
        if heading is not None:
            flush_para()
            plain = _md_plain(heading)
            if _MD_STOP.match(plain):
                stopped = True
                break
            # The first heading, before any section, is the paper title (Docling emits it
            # as "##", pymupdf4llm as "#").
            if hm and not title and len(b.sections) == 1 and classify_title(plain) == "other":
                title = plain
                continue
            # A "Table 1 ..." or "Figure 1 ..." heading is a caption, not a section.
            if _MD_TABLE_CAPTION.match(plain) or _MD_FIG_CAPTION.match(plain):
                emit_paragraph(plain)
                continue
            flush_caption()
            new_section(heading)
            continue
        if not stripped:
            flush_para()
            continue
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line) and para and not re.match(r"^\s*([-*+]|\d+[.)])\s+", para[-1]):
            flush_para()
        para.append(line)
    if not stopped:
        flush_para()
        flush_table()
    flush_caption()

    # Drop the front-matter section when nothing landed in it.
    if not front["block_ids"]:
        b.sections.remove(front)
    doc = {"schema_version": SCHEMA_VERSION, "structure_quality": quality, "source": source,
           "fetched_url": fetched_url, "title": title, "sections": b.sections, "blocks": b.blocks}
    doc["accession_mentions"] = accession_index(doc)
    return doc


# ---------------------------------------------------------------------------
# Rendering, persistence, reading
# ---------------------------------------------------------------------------

def accession_index(doc: dict) -> dict[str, list[str]]:
    idx: dict[str, list[str]] = {}
    for blk in doc["blocks"]:
        for acc in dict.fromkeys(_ACCESSION_RE.findall(blk["text"])):
            idx.setdefault(acc, []).append(blk["id"])
    return idx


def _block_md(blk: dict) -> str:
    return f"[{blk['id']}] {blk['text']}"


def to_markdown(doc: dict) -> str:
    lines = [f"# {doc.get('title') or doc.get('pmcid') or 'Untitled paper'}", ""]
    ids = " · ".join(f"{k.upper()}: {doc[k]}" for k in ("pmcid", "pmid", "doi") if doc.get(k))
    if ids:
        lines.append(ids)
    lines.append(f"Source: {doc.get('source') or 'unknown'} · structure: {doc.get('structure_quality')}")
    lines.append("Block IDs in [brackets] are citable locators (e.g. paper.locator = \"S2.3.p1\").")
    lines.append("")
    by_id = {b["id"]: b for b in doc["blocks"]}
    for sec in doc["sections"]:
        hashes = "#" * min(1 + sec["level"], 6)
        lines.append(f"{hashes} {sec['title'] or '(untitled)'}  `{sec['id']}` · {sec['class']}")
        lines.append("")
        for bid in sec["block_ids"]:
            lines.append(_block_md(by_id[bid]))
            lines.append("")
    if doc.get("accession_mentions"):
        lines.append("## Accession mentions")
        lines.append("")
        for acc, where in doc["accession_mentions"].items():
            lines.append(f"- {acc}: {', '.join(where)}")
    return "\n".join(lines).rstrip() + "\n"


def save(doc: dict, out_dir: str, stem: str, raw_xml: bytes | None = None) -> dict:
    """Write <stem>.paper.json and <stem>.paper.md (and <stem>.jats.xml when given)."""
    os.makedirs(out_dir, exist_ok=True)
    paths = {"json": os.path.join(out_dir, f"{stem}.paper.json"),
             "md": os.path.join(out_dir, f"{stem}.paper.md")}
    with open(paths["json"], "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    with open(paths["md"], "w", encoding="utf-8") as f:
        f.write(to_markdown(doc))
    if raw_xml:
        paths["xml"] = os.path.join(out_dir, f"{stem}.jats.xml")
        with open(paths["xml"], "wb") as f:
            f.write(raw_xml)
    return paths


def load(path: str) -> dict:
    """Load a structured paper from .paper.json (a .paper.md / .txt / .jats.xml sibling works too)."""
    if path.endswith(".paper.json") and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    for suffix in (".paper.md", ".jats.xml", ".txt", ".pdf", ".paper.json"):
        if path.endswith(suffix):
            cand = path[: -len(suffix)] + ".paper.json"
            if os.path.exists(cand):
                with open(cand, encoding="utf-8") as f:
                    return json.load(f)
    if os.path.exists(path + ".paper.json"):
        with open(path + ".paper.json", encoding="utf-8") as f:
            return json.load(f)
    if path.endswith(".xml") and os.path.exists(path):
        with open(path, "rb") as f:
            return parse_jats(f.read(), source=f"local file {os.path.basename(path)}")
    raise FileNotFoundError(f"No structured paper found for {path!r} (expected <stem>.paper.json).")


def outline(doc: dict) -> str:
    by_id = {b["id"]: b for b in doc["blocks"]}
    lines = [f"{doc.get('title') or '(untitled)'}",
             f"{doc.get('pmcid') or ''} structure={doc.get('structure_quality')}".strip()]
    for sec in doc["sections"]:
        chars = sum(len(by_id[i]["text"]) for i in sec["block_ids"])
        kinds = [by_id[i]["kind"] for i in sec["block_ids"]]
        extra = ", ".join(f"{kinds.count(k)} {k}" for k in ("table", "figure", "supplement") if k in kinds)
        indent = "  " * (sec["level"] - 1)
        lines.append(f"{indent}{sec['id']:<8} [{sec['class']}] {sec['title'] or '(untitled)'}"
                     f" — {len(kinds)} blocks, {chars} chars{'; ' + extra if extra else ''}")
    if doc.get("accession_mentions"):
        acc = "; ".join(f"{a} ({', '.join(w[:4])}{'…' if len(w) > 4 else ''})"
                        for a, w in list(doc["accession_mentions"].items())[:15])
        lines.append(f"Accessions: {acc}")
    lines.append("Read with: section=<class|section id|title words>; classes: "
                 + ", ".join(SECTION_CLASSES[:-1]) + ", figures, tables")
    return "\n".join(lines)


def _descendants(doc: dict, sid: str) -> list[dict]:
    return [s for s in doc["sections"] if s["id"] == sid or s["id"].startswith(sid + ".")]


def select_sections(doc: dict, query: str) -> list[dict]:
    q = query.strip()
    if not q:
        return []
    exact = _descendants(doc, q) if any(s["id"] == q for s in doc["sections"]) else []
    if exact:
        return exact
    cls = _CLASS_ALIASES.get(q.lower(), q.lower())
    if cls in SECTION_CLASSES:
        return [s for s in doc["sections"] if s["class"] == cls]
    ql = q.lower()
    hits = [s for s in doc["sections"] if ql in (s["title"] or "").lower()]
    out: list[dict] = []
    for h in hits:
        for s in _descendants(doc, h["id"]):
            if s not in out:
                out.append(s)
    return out


def read_section(doc: dict, query: str, max_chars: int = 0) -> str:
    """Markdown for every block in the matching sections (in document order).

    query: a section id ("S2", includes subsections), a class ("methods", "results",
    "data_availability", "abstract", ...), "figures"/"tables"/"supplementary" for all
    floats of that kind, or words from a section title ("statistical analysis").
    Several queries can be joined with commas.
    """
    parts: list[str] = []
    seen: set[str] = set()
    by_id = {b["id"]: b for b in doc["blocks"]}
    for q in [x.strip() for x in query.split(",") if x.strip()]:
        key = _CLASS_ALIASES.get(q.lower(), q.lower())
        if key in ("figures", "tables") or (key == "supplementary" and not select_sections(doc, q)):
            kind = {"figures": "figure", "tables": "table", "supplementary": "supplement"}[key]
            blks = [b for b in doc["blocks"] if b["kind"] == kind and b["id"] not in seen]
            if not blks:
                parts.append(f"(no {key} in this paper)")
            for b in blks:
                seen.add(b["id"])
                parts.append(f"{_block_md(b)}\n  (in {b['section_id']}: {' > '.join(b['section_path'])})")
            continue
        secs = select_sections(doc, q)
        if not secs:
            parts.append(f"(no section matches {q!r}; see outline)")
            continue
        for s in secs:
            ids = [i for i in s["block_ids"] if i not in seen]
            parts.append(f"## {' > '.join(s['path'])}  `{s['id']}` · {s['class']}")
            for i in ids:
                seen.add(i)
                parts.append(_block_md(by_id[i]))
    text = "\n\n".join(parts)
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[truncated at {max_chars} chars; request a narrower section id]"
    return text


def resolve_locator(doc: dict, locator: str) -> dict | None:
    """Block for a locator: a block id ("S2.3.p1", "TAB1"), or a float label ("Table 1")."""
    loc = (locator or "").strip()
    for b in doc["blocks"]:
        if b["id"] == loc:
            return b
    norm = re.sub(r"[\s.]+", " ", loc).strip().lower()
    for b in doc["blocks"]:
        if b.get("label") and re.sub(r"[\s.]+", " ", b["label"]).strip().lower() == norm:
            return b
    return None


def get_blocks(doc: dict, ids: Iterable[str]) -> str:
    out = []
    for i in ids:
        b = resolve_locator(doc, i)
        out.append(_block_md(b) if b else f"[{i}] (not found)")
    return "\n\n".join(out)


def find(doc: dict, terms: list[str], mode: str = "any", limit: int = 20,
         width: int = 160) -> list[dict]:
    """Keyword search over blocks; returns [{id, section, kind, snippet}] in document order."""
    rx = [re.compile(re.escape(t), re.I) for t in terms if t.strip()]
    hits = []
    for b in doc["blocks"]:
        found = [r for r in rx if r.search(b["text"])]
        if not found or (mode == "all" and len(found) < len(rx)):
            continue
        m = found[0].search(b["text"])
        s = max(0, m.start() - width // 2)
        snippet = b["text"][s: s + width].replace("\n", " ")
        hits.append({"id": b["id"], "section": " > ".join(b["section_path"]), "kind": b["kind"],
                     "snippet": ("…" if s else "") + snippet + "…"})
        if len(hits) >= limit:
            break
    return hits


# ---------------------------------------------------------------------------
# Fetch (network)
# ---------------------------------------------------------------------------

def fetch_jats(pmcid: str, timeout: int = 60) -> tuple[bytes, str]:
    """Download Europe PMC full-text XML. Returns (xml_bytes or b'', url)."""
    import requests  # lazy: parsing needs no network stack

    s = str(pmcid or "").strip().upper()
    s = s[3:] if s.startswith("PMC") else s
    s = s.split(".")[0]
    if not s.isdigit():
        return b"", ""
    url = EPMC_FULLTEXT.format(pmcid=f"PMC{s}")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (mwangLab-agent; bioinformatics research)"},
                     timeout=timeout)
    if r.status_code != 200 or not r.content.strip():
        return b"", url
    return r.content, url


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.paper_structure", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fetch", help="download Europe PMC JATS and save .paper.json/.paper.md")
    p.add_argument("pmcid")
    p.add_argument("--out", default="data/papers")
    p = sub.add_parser("parse", help="structure a local JATS XML file")
    p.add_argument("xml")
    p.add_argument("--out", default="data/papers")
    p.add_argument("--stem", default="")
    for name in ("outline", "markdown"):
        p = sub.add_parser(name)
        p.add_argument("paper")
    p = sub.add_parser("section")
    p.add_argument("paper")
    p.add_argument("query", help="class, section id, or title words; comma-separated for several")
    p.add_argument("--max-chars", type=int, default=0)
    p = sub.add_parser("block")
    p.add_argument("paper")
    p.add_argument("ids", nargs="+")
    p = sub.add_parser("find")
    p.add_argument("paper")
    p.add_argument("terms", nargs="+")
    p.add_argument("--all", action="store_true", help="require every term in the same block")
    p.add_argument("--limit", type=int, default=20)
    a = ap.parse_args(argv)

    if a.cmd == "fetch":
        xml, url = fetch_jats(a.pmcid)
        if not xml:
            print(f"No Europe PMC open-access full text for {a.pmcid} ({url}).", file=sys.stderr)
            return 2
        doc = parse_jats(xml, source=f"Europe PMC full-text XML ({a.pmcid})", fetched_url=url)
        paths = save(doc, a.out, doc.get("pmcid") or a.pmcid.upper(), raw_xml=xml)
        print(json.dumps(paths, indent=1))
        print(outline(doc))
        return 0
    if a.cmd == "parse":
        with open(a.xml, "rb") as f:
            raw = f.read()
        doc = parse_jats(raw, source=f"local file {os.path.basename(a.xml)}")
        stem = a.stem or doc.get("pmcid") or os.path.splitext(os.path.basename(a.xml))[0]
        print(json.dumps(save(doc, a.out, stem, raw_xml=raw), indent=1))
        print(outline(doc))
        return 0
    doc = load(a.paper)
    if a.cmd == "outline":
        print(outline(doc))
    elif a.cmd == "markdown":
        print(to_markdown(doc))
    elif a.cmd == "section":
        print(read_section(doc, a.query, a.max_chars))
    elif a.cmd == "block":
        print(get_blocks(doc, a.ids))
    elif a.cmd == "find":
        for h in find(doc, a.terms, "all" if a.all else "any", a.limit):
            print(f"[{h['id']}] ({h['kind']}; {h['section']}) {h['snippet']}")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    sys.exit(_main())
