"""Regenerate synthetic_two_column.pdf (needs reportlab): python test/fixtures/papers/make_synthetic_pdf.py

A two-page, two-column article with a running header, numbered and unnumbered
headings, a sample table, a figure legend, a data-availability statement and
references, used by test_paper_structure.py to check PDF -> Markdown -> structure.
"""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Table,
                                TableStyle)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthetic_two_column.pdf")
ss = getSampleStyleSheet()
FILLER = ("Skeletal muscle adapts to repeated contraction through coordinated changes in "
          "gene expression, mitochondrial content and capillary density. ")


def header(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(2 * cm, A4[1] - 1.2 * cm, "Journal of Synthetic Exercise Biology (2024) 12:345")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    w, h = A4
    colw = (w - 5 * cm) / 2
    frames = [Frame(2 * cm, 2 * cm, colw, h - 4 * cm, id="left"),
              Frame(3 * cm + colw, 2 * cm, colw, h - 4 * cm, id="right")]
    doc = BaseDocTemplate(OUT, pagesize=A4, title="Synthetic two-column paper")
    doc.addPageTemplates([PageTemplate(id="two", frames=frames, onPage=header)])
    s = []
    P = lambda t, st="BodyText": s.append(Paragraph(t, ss[st]))
    P("Treadmill training remodels the muscle transcriptome", "Title")
    P("Abstract", "Heading2")
    P("We trained male mice for six weeks and profiled gastrocnemius by RNA-seq. " + FILLER)
    P("1. Introduction", "Heading2")
    P("Earlier microarray work (GSE12345) examined acute exercise. " + FILLER * 4)
    P("2. Materials and methods", "Heading2")
    P("2.1. Animals and training", "Heading3")
    P("Male C57BL/6J mice (n = 6 per group) were assigned to sedentary control or treadmill "
      "training at 12 m/min for 60 min per day. " + FILLER * 3)
    P("Table 1. Sample groups used for RNA-seq.")
    t = Table([["Group", "n", "Sex", "Tissue"], ["Sedentary", "6", "M", "Gastrocnemius"],
               ["Trained", "6", "M", "Gastrocnemius"]])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.black)]))
    s.append(t)
    P("2.2. Statistical analysis", "Heading3")
    P("Differential expression used DESeq2 with padj &lt; 0.05 and |log2FC| &gt; 1. " + FILLER * 3)
    P("3. Results", "Heading2")
    P("Training increased mitochondrial genes. " + FILLER * 6)
    P("Figure 1. Volcano plot of trained versus sedentary muscle.")
    P("4. Discussion", "Heading2")
    P(FILLER * 8)
    P("Data availability", "Heading2")
    P("RNA-seq data are deposited in GEO under accession GSE209999.")
    P("References", "Heading2")
    P("1. Smith J. Exercise and muscle. Cell 2020.")
    doc.build(s)


if __name__ == "__main__":
    build()
    print(OUT)
