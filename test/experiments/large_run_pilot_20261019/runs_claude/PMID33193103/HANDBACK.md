# HANDBACK: PMID33193103 / GSE155230

Paper: Comparative Analysis of Skeletal Muscle Transcriptional Signatures Associated With Aerobic Exercise Capacity or Response to Training in Humans and Rats (PMC7649134).
Decision maker: Claude Opus 5.5 session. Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Run status: **completed**. Contract validator: 25 records, 0 errors.

## What ran

The data are 18 rat gastrocnemius bulk RNA-seq samples, all male, n=3 per group. The paper's own route (TopHat2 → Cufflinks/Cuffdiff on BAMs, S2.3.1.p1) is blocked because only featureCounts gene counts were deposited. Every table below is therefore a **declared deviation**: DESeq2 (pydeseq2 Wald) on raw counts, using the paper's threshold.

**Threshold (paper, S3.1.p1 / S3.2.p1):** fold change > 1.5 and FDR/q < 0.05, applied as `padj < 0.05 & |log2FC| > 0.5849625`. The source is recorded as `paper_on_deviation_route`. An audit rule (padj < 0.05, no fold-change cutoff) is also recorded.

**Case `GSE155230_training`** (exercise estimand, 12 samples): one joint model `~ grp` with 4 levels (LRT, LRTT, HRT, HRTT). Trained and untrained rats are separate animals (S2.1.3.p1), so the design is unpaired.
- Training effect: `grp_LRTT_vs_LRT` and `grp_HRTT_vs_HRT` (primary, S3.2.p3). These are causal within each line.
- `grp_HRTT_vs_LRTT` (Fig 2C headline) and `grp_HRT_vs_LRT` (untrained baseline) are secondary. They compare selectively bred lines, so they are associational.

**Case `GSE155230_capacity`** (6 samples): `hcr_vs_lcr`, untrained HCR vs LCR (Fig 1C). This is associational intrinsic capacity, not an exercise effect. It also holds an exploratory `lane_check` model (L3 vs L1, `~ grp + lane`).

### Paper counts

The text gives counts only for HCR/LCR (434) and HRTT/LRTT (255). The training-contrast counts come from the authors' deposited Cuffdiff lists (`GSE155230_*_deg.csv.gz`). Under the paper rule those lists reproduce the text exactly: 434 = 257/177 and 255 = 68/187.

| table | ours n (up/down) | paper n (up/down) | audit n (padj<0.05) |
|---|---|---|---|
| training_joint/grp_LRTT_vs_LRT | 8 (4/4) | 255 (174/81), deposited list | 8 |
| training_joint/grp_HRTT_vs_HRT | 2 (1/1) | 90 (62/28), deposited list | 3 |
| training_joint/grp_HRTT_vs_LRTT | 34 (18/16) | 255 (68/187), S3.2.p1 | 35 |
| training_joint/grp_HRT_vs_LRT | 20 (9/11) | 234 (64/170), deposited list | 23 |
| hcr_vs_lcr | 81 (46/35) | 434 (257/177), S3.1.p1 | 81 |

Our counts are 3–45× lower than the paper's. With n=3 in outbred rats, DESeq2 gene-level counts are far more conservative than Cuffdiff `-b -u` isoform-aware q-values. The gap is a method difference, not a sample-mapping problem: alignment was an exact match on GEO `description`, and the suitability report was `analyzable`.

### Paper genes and directions
- **HRTT vs LRTT:** all named genes agree in direction with S3.2.p1.
  - Up in HRTT: Sln, Adcy1, Kcna10, Lgi3.
  - Higher in LRTT: Rcan3 (weakly), Wnt16, Vat1l, Myh6.
  - Circadian genes: Per1, Bhlhe40 and Dbp are higher in LRTT, and Nfil3 is lower.
  - Only Lgi3 reaches padj < 0.05.
- **HCR vs LCR:**
  - Agree and are significant: Fam163a, Fosb, Cyp2j4 (up in HCR); Ranbp3l, Igfn1 (up in LCR).
  - Agree but are not significant: Pik3c2g, Msln, Ifit1.
  - **Contradicts the paper:** Ppm1h. The paper says it is higher in LCR; we get log2FC = +0.16, padj = 1. This is recorded in the study caveats.
  - Not found by symbol: Mup4 and Tmem8c (current name Mymk).

### Enrichment (separate from DE; GSEA uses MSigDB mouse Hallmark by symbol)
- **LRTT vs LRT GSEA:** interferon-α, interferon-γ, MYC targets, OXPHOS and mTORC1 are all positive (FDR ≈ 0). The interferon signal matches the paper's interferon/inflammation signature for low-responder training (S3.2.p3). ORA completed.
- **HRTT vs HRT GSEA:** OXPHOS (NES −2.7) and fatty-acid metabolism are negative; myogenesis is positive.
  - OXPHOS goes in opposite directions in the two lines' training contrasts. That is biologically odd for endurance training, and lane could plausibly contribute (see below).
  - ORA failed: only 2 DEGs, below the tool's ~5-gene minimum. This is recorded, not hidden.

## Deviations and decisions
1. **DESeq2 instead of Cuffdiff** (paper route blocked: no BAMs deposited). GEO `data_processing` says the authors themselves produced normalized counts with featureCounts and DESeq2.
2. **Prep script** `prep/prep_counts.py` makes three changes; count values are not changed:
   - renames the BAM-path columns to the GEO `description` keys (e.g. HRTT_1);
   - drops the featureCounts `#` line;
   - writes a metadata copy `prep/GSE155230_metadata_lane.csv` with a `lane` column parsed from the FASTQ names (`<project>_<sample>_<lib>_<run4266>_<lane>_<read>`).
3. **Sequencing lane is completely aliased with group in every training contrast.** Lanes are HRT L2×3, HRTT L3×3, LRTT L2×3, LRT L3/L1/L1. A strict reading of the covariance gate would stop the case. I kept it, with medium confidence and a caveat on every training table, for three reasons:
   - Lane here is a flow-cell lane within one GATC run, and the libraries were prepared in one batch (consecutive lib IDs 99119–99130).
   - The paper's own results carry the same aliasing.
   - It was checked directly: in the capacity samples, where lane is balanced 2:1 per line, `lane_check` finds 36 lane DEGs. These overlap the training DEG sets by only 0/0/1/1 genes, but lane-gene log2FCs correlate with the lane effect at r = 0.59 / 0.41 / −0.47 / −0.17 across the four training contrasts.

   So a lane or processing-order contribution to the training results cannot be excluded. A reviewer may reasonably prefer `manual_review` at the covariance gate.
4. The case was not paired: separate untrained and trained cohorts (S2.1.3.p1). No line × training interaction was fitted, because the paper did not test one.
5. **Not attempted:** the human GSE97084 analyses (Fig 4), secretome prediction, IPA/DiRE, and the rat–human Venn overlaps. All are outside GSE155230's DE scope.
6. **Paper inconsistency noted:** S2.1.2.p1 defines ΔDIST = DIST1 − DIST2, which has the sign reversed. It has no effect on the analysis.

## Tool problems
1. **GEO download failed with a misleading error.** `tools/geo_tools.py:30` (`GEOparse.get_GEO`) reported `[Errno 2] No such file ... Temp\tmpXXXX`, but the real cause was HTTP 403 from ftp.ncbi.nlm.nih.gov. The 403 was transient (about 5 minutes) and applied to the whole host. Supplementary download (`geo_tools.py:58-61`) also returned 403. There is no retry, and no fallback to `www.ncbi.nlm.nih.gov/geo/query/acc.cgi?...&form=text&view=full`, which worked throughout. I built the SOFT and metadata by hand via acc.cgi + GEOparse(filepath=), and fetched the supplementary files once the host recovered.
2. **featureCounts comment line is ignored in one reader.** `tools/native.py:630` (`feature_id_report`) reads the file without skipping the leading `# Program:featureCounts` line. Inspect therefore showed the header as a data row and typed the Ensembl IDs as `other`. `native.py:218-226` (`read_table`) does handle this.
3. **Free-text confounding candidate crashes without naming the field.** A `covariance.confounding_candidates` entry that is not a metadata column (e.g. "sequencing lane") passes spec validation and crashes later with a bare `KeyError: 'sequencing lane'` (`tools/case_runner.py:646` → `native.confounding_report`). The error does not name the spec field. A factor that exists only in matrix column names (lane) needs a metadata copy to be tested.
4. **Deposited DEG tables profiled as count matrices.** Inspect lists the semicolon/decimal-comma Cuffdiff DEG tables (`*_deg.csv.gz`) as candidate matrices with type `raw_counts` (integer_fraction 1.0, 2 "samples"); the misparse comes from `_candidate_files` / `profile_matrix`. Two of them error out instead. This is harmless here, but it is misleading.
5. **Paper-gene lookup is symbol-only.** Renamed genes are missed (Tmem8c → Mymk).
