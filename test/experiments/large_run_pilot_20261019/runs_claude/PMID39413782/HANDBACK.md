# HANDBACK — PMID39413782 / GSE239596

**Status: refused at `design` (no exercise contrast).**

## What ran
1. `python -m tools.case_runner inspect GSE239596 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series and merged `GSE239596_RAW.tar` into a matrix of 32,719 genes x 6 samples. All values are integers (raw exonic read counts).
2. Read the paper (`PMC11706709.paper.md`). The only RNA-seq experiment is jugular-nodose ganglia from mice given PBS (n=3) or S961 (n=3), an insulin-receptor antagonist delivered for 2 weeks (S2.1.p1, S4.2.2.p1).
3. `python -m tools.case_runner execute case_spec.json` recorded these gates:
   - `paper_reconstruction`: valid.
   - `ownership`: valid. S4.1.3.p1 names GSE239596, and the samples match 3 + 3.
   - `alignment`: valid. The GSM prefix of each tar column matched the metadata index exactly, 6 of 6. Groups come from `title` (Ctrl → PBS, Treat → S961).
   - `matrix`: valid, raw counts.
   - `design`: **refused**.
   - The validator returned 0 errors on 5 records. Suitability rated S961 vs PBS analyzable, but that contrast is not an exercise contrast.

## Why refused
The request asks how exercise affects gene expression. The paper has no exercise or training arm:
- The sequenced contrast is pharmacological insulin resistance (S961) against vehicle.
- "Physical activity" appears only as a CLAMS locomotor readout of AAV-FGF3 mice (S2.2.p1, Fig 2W). Those mice were not sequenced.
- Exercise is mentioned only in passing in the Discussion (S3.p2).

Running S961 vs PBS as "exercise" would make up a contrast.

## DEG counts vs paper
- Paper threshold: FDR < 0.05, with no fold-change cutoff (S4.3.2.p1).
- Paper result: 90 DEGs for S961 vs PBS (66 up, 24 down).
- Our result: none. No DE was run because the case stopped at `design`.

## Deviations / discrepancies recorded
- GEO annotates the tissue as "spinal cord", but the paper and the GEO cell-type field say jugular-nodose ganglia. This is an annotation error.
- GEO `characteristics treatment` reads "S961" for all 6 samples, including the controls. I took the groups from `title` instead.
- GEO `data_processing` says the DE method was edgeR glmQLFTest, while the paper says DESeq2 Wald (S4.3.2.p1). This does not matter here because the case stopped.

## Tool problems
- Minor: inspect reports `feature_id_type: "other"` for the merged matrix. The IDs combine Ensembl and symbol (`ENSMUSG00000026602_Nphs2`). Enrichment would need these split or mapped first. Not exercised here.
- No runner or validator errors.
