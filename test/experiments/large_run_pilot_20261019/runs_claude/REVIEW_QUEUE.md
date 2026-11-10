# Review queue (items for the owner)

One section per case; newest last.

## PMID41555288 / GSE310294 (2026-11-10)

- policy: The DESeq2 result does not reproduce the paper (4459 vs 2076 DEGs; Col1a1, Sp7, Bglap and other named bone-formation genes go the opposite way, Sample_6 outlier). Whether the sampleN_FPKM column order in the supplementary file really equals the GEO Sample 1-6 order cannot be settled from the files; ask the authors or compare with a figure if this series matters.

## 463ad4ee2ce52e09b589fa8ce48a64d7c595a849 / GSE207992 (2026-11-10)

- policy: Open policy question: joint vs pairwise fits when the paper is silent; here the paper is silent and counts differ a lot, both fits are reported.
- policy: Pathway direction for KO SVE vs KO nSVE (OXPHOS/Parkinson down in ours) contradicts S2.5.p1 but agrees with S1.p4; the analysis discloses it, a person may want to adjudicate.

## f7900835fe5a860049245a1bad8be8ffb0d6309e / GSE128078 (2026-11-10)

- policy: Open policy: FDR written '<0.1%' vs Table 4 FDR up to 0.10; applied 0.1 with 0.001 audit, consistent with the skill's discrepancy rule.
- policy: Optional: all-days ME/CFS vs controls (paper 6 DEGs) could be added as a sensitivity analysis with a within-subject correlation model.

## PMID38766755 / GSE263838 (2026-11-10)

- policy: Open policy question: which threshold to report as headline when the paper's counts fit FDR-only unblocked (2965/2224) but its Methods state FDR + |log2FC| > 1; the case applies the stated rule and reports the other as audit.
- policy: Paper's stated directions (oxidative metabolism up with training, GGNBP2 up with SR) are opposite to the data under exercise-over-control ordering; the analysis attributes this to reference-over-test labels (NS3_vs_NS9). A person may want to confirm with the authors before any direction-dependent claim is quoted against the paper.
- policy: Primary fit blocks on participant while the paper's counts match the unblocked fit; joint blocked vs unblocked as the primary is an open policy choice when the paper is silent.

## PMID40695537 / GSE293163 (2026-11-10)

- policy: Which threshold to report when the paper's numbers fit the post-hoc mean-log2FC subset better than the stated FDR rule (open policy question).

## d446594d1ade71b3541cb0f6a971599e29ccdf5a / GSE124819 (2026-11-10)

- policy: Open policy: joint per-set fit vs pairwise fits when the paper is silent.
- policy: Paper says exercised animals collected at 13.5 wk but GEO says 11.5 wk; exercise may be inseparable from time (already recorded as a caveat).

## 86991572b4ea250a7e68eadebb3fa005f4fe2282 / GSE86338 (2026-11-10)

- policy: Open policy question: whether to allow a labelled exploratory sensitivity run (limma ~grp on 8 iWAT samples, SWIM vs CNT, n=2 vs 2 pools) next to the refused record, since the paper itself reports 673/826 DEGs from n=2 pools.

## PMID41078024 / GSE302532 (2026-11-10)

- policy: Open policy: report the padj<0.05 default (0 DEGs) or the paper-implied raw-P/FC>=3 rule (21 DEGs) as the headline when the paper states no rule and its 27 rest on uncorrected P.

## PMID39609254 / GSE281849 (2026-11-10)

- policy: Open policy: report the paper-stated rule (padj<0.05, |log2FC|>0.25: 76/45/134) or the authors' code rule (padj<=0.05, |log2FC|>=0.27: 71/41/126) as headline; the run reports both, with the paper rule applied.
- policy: Optional: joint model AR vs SED has only 1990 tested genes, check whether this is independent filtering or an outlier artefact (sensitivity only).

## PMID40832111 / GSE296683 (2026-11-10)

- policy: Open policy: whether an in-vitro exercise-like (electrical pulse) stimulation series with the drug as the only varied factor counts as an exercise study; the refusal is consistent with the skill rule but the person may want the tomatidine-vs-vehicle contrasts run and labelled as a drug effect under E-Stim.

## 9eef7b263d48ceff706cefc035f28c278d2d060d / GSE124676 (2026-11-10)

- policy: Open policy question: the paper's numbers fit its raw P<0.05 rule on a paired t-test, while our limma route gives 1,984 (up count 529 vs 417); whether to add a plain paired t-test executor to close the gap is a policy choice, not an error.

## e6da17ec35146322588e4f22850014a7def00cc7 / GSE217155 (2026-11-10)

- policy: Joint vs pairwise fit when the paper is silent (open policy question); pairwise fit of EXE vs NASH alone would be a cheap sensitivity check but not required.

## b39292ba0ee11c97d2e351716ebbb6029eeee400 / GSE97718 (2026-11-10)

- policy: Open policy: joint vs pairwise fit when the paper is silent; FPKM limma vs Cuffdiff count gap (3-25x) is a declared deviation.

## b39292ba0ee11c97d2e351716ebbb6029eeee400 / GSE97718_expressed (2026-11-10)

- policy: Open policy: joint vs pairwise fit when the paper is silent; FPKM limma vs Cuffdiff count gap (3-25x) is a declared deviation.
