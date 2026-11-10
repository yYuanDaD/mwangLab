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

## PMID41126185 / GSE289091 (2026-11-10)

- policy: Whether an in-vitro mechanical-stretch series counts as an exercise study (open policy).
- policy: Which threshold to report when the paper's counts fit |lfc|>1 but the Fig6 legend states 0.5 (open policy).

## ef574c2d9b2d7f168faeb39ddc5cb09258575c41 / GSE60833 (2026-11-10)

- policy: Open policy: which threshold to report when the paper's rule (OPLS loadings) has no p-value equivalent and the headline counts (852/928) are far above what BH padj < 0.05 gives (0/6); the case's choice (padj 0.05 applied, p<0.01 audit) is recorded and labelled, so it is not an error.
- policy: Open policy: the paper's headline result needs T1/T2 from GSE58608/GSE60590; whether a joint multi-accession analysis should be queued is a scoping decision for the person.

## 4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16 / GSE327036 (2026-11-10)

- policy: Open policy: a genotype-only series (muscle KO with exercise-intolerance phenotype) is refused for an exercise question; if the person wants it as a genotype baseline reproduction, that would be a declared deviation (limma on log2 TPM).

## PMID38576560 / GSE256152 (2026-11-10)

- direction (unsure, major): Ours (treatment/Tnm) up/down: swim 73/138, cur 110/54, union 286/237; paper 79/55, 28/79, 154/291. In all three contrasts the dominant direction is opposite to the paper's; a single global sign flip (Tnm over treatment) reproduces the dominant direction in all three (flipped: swim 138/73, cur 54/110, union 237/286). The study caveat 'no single sign flip reconciles all three' is therefore not supported. The paper does not state the sign convention; Fig 3C gene directions are not available in the text.
- policy: Sign convention of the paper's up/down counts is not stated. Ours is the reverse in dominant direction for all three contrasts; the pattern is consistent with the paper using Tnm over treatment, but this cannot be settled from the paper text. Decide whether to report with a confirmed or flagged sign (Fig 3C / author query).

## PMID40000838 / GSE280656_cartilage (2026-11-10)

- policy: Code vs skill conflict: suitability.py hard-fails sample_size and decision_contract.py rejects a valid design under that verdict, against the skill rule 'small n alone is not a stop'. The gate may need changing, or the case must go through the contract's exploratory path.
- policy: Joint versus pairwise fit when the paper is silent (open policy question).

## PMID40000838 / GSE280656_synovium (2026-11-10)

- policy: Joint versus pairwise fits when the paper is silent (open policy question); the joint fit follows the iDEP default.

## PMID37928906 / GSE237736 (2026-11-10)

- policy: Joint limma model on all 16 samples versus the paper's pair-wise fits: the paper says 'pair-wise' but not whether the model was joint (open policy question).

## PMID38012706 / GSE242861 (2026-11-10)

- policy: Open policy: miR-30 was chosen from the exercise-response arrays (S2.6.p1), so GSE242861 is an in-vitro exercise-mediator series. Decide whether such series count as exercise studies; if yes, run miR-30a/c vs scramble with donor blocking (donor key supported) and record the paper's unblocked Sex * Condition model as a discrepancy.

## f719c1147eb0f406823e085b4396d05fdfa410d2 / GSE293221 (2026-11-10)

- policy: Primary fit choice: the joint ~grp model gives 32 EX DEGs (count equals the paper's, but Lipe/Plin1/Slc7a10 get padj NA because the heterogeneous PHAM arm drives Cook flags), while the two-arm CON+EX fit recovers all five paper-named exercise genes but calls 385 DEGs. The paper is silent on joint vs pairwise dispersion, so which to label primary is the open policy question.
- policy: PHAM vs CON gives 3694 DEGs vs the paper's 176 because two of three PHAM tumors are transcriptionally distinct; whether to treat this as a sample or tissue-content issue is for a person.

## 2148e268704227111378324e8a4175163d2e8e5f / GSE110507 (2026-11-10)

- policy: Open policy: whether a VDR-OE vs control run is wanted as a non-exercise sensitivity/reference result (paired edgeR, P<0.05, paper 3,330 genes). Not required: the case is correctly refused for the exercise question. The paper's exercise data (GSE47881 human RET microarray) would need a separate case.

## PMID40169574 / GSE269020 (2026-11-10)

- policy: Policy (open): whether a KO vs WT genetic contrast in a series with an exercise-factor paper should be offered as a labelled non-exercise result; the case chose to refuse, consistent with the skill.

## be59c707b58c7328d0828ad5b9b2975ab6940ac8 / GSE229755 (2026-11-10)

- policy: Open policy question (not an error): the paper's 88 DEGs are not reproduced from FPKM; whether to also seek counts from SRA (the series is type SRA) for a DESeq run is a person's call.

## PMID38348322 / GSE237950 (2026-11-10)

- policy: Open policy question: the paper gives no threshold, so the workflow default is used; a person may want to confirm that default for data-descriptor papers.
- policy: Fat HE vs H and H arms have n=2: results are low power, correctly labelled exploratory.

## PMID38982049 / GSE266883 (2026-11-10)

- policy: Open policy: report which threshold when the paper states none (workflow default padj<0.05 used); joint vs pairwise fits when the paper is silent.

## PMID42897930 / GSE325957 (2026-11-10)

- policy: Open policy question: whether to still run the paper's own (batch-aliased) comparison as a labelled paper-reproduction with no biological claim, since the paper itself did exactly this; the skill's gate stops it.
- policy: Not an error: the CPM-only deposit would need limma on log2(CPM+1) even if the covariance gate were waived.
