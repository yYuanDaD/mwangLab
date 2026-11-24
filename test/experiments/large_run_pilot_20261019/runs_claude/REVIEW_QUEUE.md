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

## PMID40789206 / GSE297842 (2026-11-10)

- policy: Open policy: joint vs pairwise fit when paper is silent (counts differ 29 vs 93); paper's counts are closer to the joint fit but do not fully match either.

## PMID37059838 / GSE228901 (2026-11-10)

- policy: Open policy question only: whether a series with exercise-performance readouts but no exercise intervention should be reported as an associational analysis; the skill's current rule (refuse) is followed.

## PMID42318351 / GSE277623 (2026-11-10)

- policy: Policy question only: whether a drug-vs-vehicle HFpEF series with an exercise-tolerance endpoint should be refused or run as a non-exercise record is outside this review; the refusal follows the skill's no-exercise-arm rule.

## PMID33598660 / GSE117161 (2026-11-10)

- policy: What the A/B/C letter in the GEO titles denotes (expression check supports same-letter pairing); optional sensitivity run if confirmed.

## PMID34039988 / GSE132520 (2026-11-10)

- policy: Joint versus pairwise fits when the paper is silent (open policy question): the record uses one joint model; the paper's tool (Cuffdiff via GEO field) fits pairs.

## PMID35440516 / GSE198266 (2026-11-10)

- policy: Open policy: when the paper rule (raw p, FC 1.5) gives 1.5-3x the paper's counts with limma, which count is the headline; recorded as a declared deviation.

## PMID26845575 / GSE69699 (2026-11-10)

- policy: Policy: should the runner accept small-n (n=2) planned contrasts as exploratory, given the skill text says small n is not a stop but suitability.py hard-fails n<3?

## PMID42268956 / GSE315575 (2026-11-10)

- policy: Policy only (not an error): whether a genotype-only series whose paper frames exercise adaptive homeostasis should be run as a labelled non-exercise genotype analysis (paper's 1023 DEGs could then be reproduced) is a separate request.

## PMID36695573 / GSE198827 (2026-11-10)

- policy: Open policy question: whether the trained-only genotype contrast (LSD1-mKO vs WT under VWR, the paper's Fig 5 analysis) should be reported as an exercise-context result with an explicit 'no exercise factor' label, or refused as done here. Refusal is consistent with the stated rule; this is not an error.

## PMID39141732 / GSE263912 (2026-11-10)

- policy: Open policy question only: whether a muscle knockout genotype series in a paper about exercise signalling should be run as a non-exercise analysis; the refusal follows the stated skill rule.

## PMID36198295 / GSE183239 (2026-11-10)

- policy: Open policy: which threshold/filter reading to treat as primary when the paper's numbers fit another reading (literal all-sample count>10 filter vs total count>10 sensitivity; padj<0.1 closest for scWAT rescue).
- policy: Open policy: joint (~ grp) vs pairwise fits when the paper is silent; only the joint fit is reported.

## PMID36198295 / GSE183239 (2026-11-10)

- policy: Open policy: which threshold/filter reading to treat as primary when the paper's numbers fit another reading (literal all-sample count>10 filter vs total count>10 sensitivity; padj<0.1 closest for scWAT rescue).
- policy: Open policy: joint (~ grp) vs pairwise fits when the paper is silent; only the joint fit is reported.

## PMID35030322 / GSE190355 (2026-11-10)

- policy: Open policy: whether to try SRA re-quantification (SRP349620, GSM-labelled FASTQ) to obtain counts and a verified sample mapping; this is optional follow-up work, not an error in the record.

## PMID34526402 / GSE166322 (2026-11-17)

- policy: Open policy: joint vs pairwise fit when the paper is silent.
- policy: The up/down balance of MDZ vs Ctrl is inverted relative to the paper (1671 up / 301 down vs 604 up / 873 down); cause (TPM+limma vs counts+DESeq2, or mislabelled GEO titles) cannot be settled from the files.

## PMID34870208 / GSE180877 (2026-11-17)

- policy: Policy: whether adding the 3 later-deposited PoW samples to match the paper's counts is acceptable when the paper says triplicate (it is documented and run as sensitivity).

## PMID32601609 / GSE77178 (2026-11-17)

- policy: Joint versus pairwise fits when the paper is silent (open policy question); DEG counts differ 4-12x from the paper.
- policy: Which threshold to report is not in question here: no alternative rule reproduces 248/35.

## PMID42051351 / GSE313585 (2026-11-17)

- policy: Optional: the PMID-linked series holds rat vascular smooth muscle cells, not the paper's C2C12; authors could be asked whether the wrong dataset was deposited.

## PMID33123481 / GSE150620 (2026-11-17)

- policy: Open policy: paper likely used all 22 mice (only the pooled/averaged readings reproduce hypoxia significance); which reading is reported as primary (PBS-only vs all-mice) is a choice for the person.

## PMID32755589 / GSE142678_across_durations (2026-11-17)

- policy: Whether Fig 3A pools the three durations or shows one duration is not stated; the paper's own estimand per time point is in the sibling case.

## PMID32755589 / GSE142678_per_duration (2026-11-17)

- policy: Policy: can the decision contract accept a not_analyzable(sample_size) verdict as exploratory when the paper itself analysed n=2 per cell? Currently blocks the paper's primary estimand.

## PMID30071007 / GSE114062 (2026-11-17)

- policy: Policy: whether a selectively bred high-runner line vs control line (both wheel-exposed) counts as an exercise study; the run labels it associational.
- policy: Whether the primary should be paired when the paper's own model is unpaired (joint vs paper-faithful) is for the person to decide; the sensitivity run is requested.

## PMID40388671 / GSE226005 (2026-11-17)

- policy: Open policy question: the exercise snRNA-seq SubSeries of GSE226008 was not examined; whether to route it as a separate case is for the person.

## PMID35470975 / GSE185957 (2026-11-17)

- policy: Obese post vs pre gives 0 DEGs (min padj 0.32) on every limma route vs paper 104; the paper's exact obese rule or model (maybe raw-count edgeR, or a different threshold) cannot be determined from the files.
- policy: Sex inferred from X/Y (lean 4F, obese 2M2F) disagrees with S2.1.p1 (lean 2M2F, obese 4F) and Table 1 (2F2M each); lean counts match so labels are kept, but a possible group-label issue is not excluded.

## PMID41326383 / GSE302582 (2026-11-17)

- policy: Which threshold to report when padj<0.1 reproduces the paper's 207 although the paper states padj<0.05 (open policy question).
- policy: Joint versus pairwise fits: paper silent, analysis fitted per group plus limma change scores.

## PMID35379817 / GSE186105 (2026-11-17)

- policy: Open policy: whether a genotype-only series from an exercise paper should be refused (as done) or analyzed as a labelled non-exercise KO vs WT contrast.

## PMID42272974 / GSE306842 (2026-11-17)

- policy: Policy (open): whether this in-vitro C2C12 optogenetic stimulation series counts as an exercise study.
- policy: Policy (open): joint ~grp model versus pairwise fits when the paper is silent; paper has no numeric DEG counts to discriminate.

## PMID42272974 / GSE306857 (2026-11-17)

- policy: Policy (open): whether this in-vitro C2C12 optogenetic stimulation series counts as an exercise study.
- policy: Policy (open): joint ~grp model versus pairwise fits when the paper is silent; paper has no numeric DEG counts to discriminate.

## PMID39144140 / GSE272213 (2026-11-17)

- policy: Open policy: which threshold to report when the paper's 22 DEGs fit no tested rule (FDR 0 hits, raw p 223/123); case reports the stated rule and labels the raw-p audit.

## PMID35282369 / GSE193432 (2026-11-17)

- policy: Which threshold to report: paper's counts fit padj rule while results text says raw P (open policy question, recorded as audit).

## PMID38157298 / GSE245760 (2026-11-17)

- policy: Open policy: which threshold to report when the paper states none but draws p=0.01 on a volcano (BH padj<0.05 applied, raw p<0.01 audit).

## PMID37395281 / GSE185154 (2026-11-17)

- policy: Open policy: whether genotype-only series in an exercise paper should be listed as non-exercise (done here) - no change needed.

## PMID37639610 / GSE233485 (2026-11-17)

- policy: Open policy: whether mTG vs WT (sedentary exercise-mimic, SI Fig S3H) should be offered as a labelled genetic-proxy analysis.

## PMID41673803 / GSE286570 (2026-11-17)

- policy: Which threshold to report for HRE vs HFD when the paper's 171 fits padj<0.05 with FC cutoff rather than the stated raw p<0.01 (open policy question).

## PMID39747575 / GSE269053 (2026-11-17)

- policy: Policy question: when an exercise-question series has no exercise arm but a paper disease-model contrast is analyzable, whether to also run the paper's contrasts as a labelled non-exercise record (currently refused only).

## PMID31175296 / GSE125630 (2026-11-17)

- policy: Policy question (not an error): whether to also report a clearly labelled descriptive SWIM/SWW vs CONT contrast despite complete aliasing with collection time.

## PMID36681077 / GSE216094 (2026-11-17)

- policy: Open policy: whether an in-vitro exercise-mediator (PSAP overexpression) series should count as an exercise study; here it was refused and labelled.

## PMID36720890 / GSE214542_delayed (2026-11-17)

- policy: Open policy: does an in-vivo exercise-mediator (recombinant irisin injection) series count as an exercise study? Refusal is consistent with the stated rule but a person should decide whether a pharmacological irisin-vs-MPTP sensitivity run is wanted.

## PMID36720890 / GSE214542_pretreatment (2026-11-17)

- policy: Open policy: does an in-vivo exercise-mediator (recombinant irisin injection) series count as an exercise study? Refusal is consistent with the stated rule but a person should decide whether a pharmacological irisin-vs-MPTP sensitivity run is wanted.

## PMID36481702 / GSE176563 (2026-11-17)

- policy: 论文数字(774)与单独的 P<0.01(794)最接近,而非其声明的 P<0.01 且 FC>2:该情形下应报告哪条阈值属开放政策问题,本案已记录两条论文规则,未发现违反技能规则。

## PMID36611093 / GSE208714 (2026-11-17)

- stop_reason (unsure, major): The claim 'no key in any source' covers GEO, SOFT, SRA, BioSample and the CUT&RUN series, a wide search, but the paper's Supplementary Data 2 (per-sample RNA yields) was not opened because the download was not authorised. It is the most likely holder of lab-ID to condition rows. NT (6) / TG (14) prefix split is not a group label, which is consistent with the stop. The 3 PCA outliers are also unnamed, so the 2 vs 3 set cannot be rebuilt even with a key
- policy: Supplementary Data 2 was never opened; a person must authorise the download or ask the authors to settle whether lab-ID to condition key exists
- policy: Which 2 sedentary and 1 ELE SIT samples were PCA outliers is unnamed in the paper

## PMID36620222 / GSE218103 (2026-11-17)

- policy: Pre/post pool correspondence is undocumented; whether to run a labelled pool-blocked sensitivity is optional.

## PMID36620222 / GSE219099 (2026-11-17)

- policy: Policy (open): whether in-vitro exercise-mediator series such as miR-486 mimic count as exercise studies.

## PMID29610328 / GSE101239 (2026-11-17)

- policy: Open policy: joint three-group limma on FPKM versus the paper's per-stage pairwise Cuffdiff (paper silent on 12w model).

## PMID39523700 / GSE257540_biochem (2026-11-17)

- policy: Which threshold to report when the paper states BH-adjusted p without a cutoff (open policy question); workflow default padj<0.05 was used and labelled.

## PMID39523700 / GSE257540_mech (2026-11-17)

- policy: Which threshold to report when the paper states BH-adjusted p without a cutoff (open policy question); workflow default padj<0.05 was used and labelled.

## PMID39523700 / GSE281241 (2026-11-17)

- policy: Whether in-vitro surrogate-validation series count as exercise studies is the open in-vitro policy question; here the factor is genotype, not stimulation, so the refusal is consistent.

## PMID37178122 / GSE230102_BAT (2026-11-17)

- policy: Primary model choice when the paper is silent: strain-blocked gives many more DEGs than unblocked, and the paper's 'average ~500 DEGs per tissue' (S2.9.p3) fits the unblocked counts; which to report as primary is open.
- policy: Whether the paper's per-tissue counts (Figures S11A/S12A/S13A) can be obtained to settle the model question.

## PMID37178122 / GSE230102_gWAT (2026-11-17)

- policy: Primary model choice when the paper is silent: strain-blocked gives many more DEGs than unblocked, and the paper's 'average ~500 DEGs per tissue' (S2.9.p3) fits the unblocked counts; which to report as primary is open.
- policy: Whether the paper's per-tissue counts (Figures S11A/S12A/S13A) can be obtained to settle the model question.

## PMID37178122 / GSE230102_heart (2026-11-17)

- policy: Primary model choice when the paper is silent: strain-blocked gives many more DEGs than unblocked, and the paper's 'average ~500 DEGs per tissue' (S2.9.p3) fits the unblocked counts; which to report as primary is open.
- policy: Whether the paper's per-tissue counts (Figures S11A/S12A/S13A) can be obtained to settle the model question.

## PMID37178122 / GSE230102_liver (2026-11-17)

- policy: Primary model choice when the paper is silent: strain-blocked gives many more DEGs than unblocked, and the paper's 'average ~500 DEGs per tissue' (S2.9.p3) fits the unblocked counts; which to report as primary is open.
- policy: Whether the paper's per-tissue counts (Figures S11A/S12A/S13A) can be obtained to settle the model question.

## PMID37178122 / GSE230102_quad (2026-11-17)

- policy: Primary model choice when the paper is silent: strain-blocked gives many more DEGs than unblocked, and the paper's 'average ~500 DEGs per tissue' (S2.9.p3) fits the unblocked counts; which to report as primary is open.
- policy: Whether the paper's per-tissue counts (Figures S11A/S12A/S13A) can be obtained to settle the model question.

## PMID36907509 / GSE199111 (2026-11-17)

- policy: Policy question (open): whether the genotype contrast (miR-501dMP vs Pax7Cre, paper's own DEG comparison) should still be run as a labelled non-exercise reference; refusal is consistent with the current rule.

## PMID35847876 / GSE205173 (2026-11-17)

- policy: Open policy: joint vs pairwise fit when paper is silent (both reported here).

## PMID38110408 / GSE239729 (2026-11-17)

- policy: Policy only: whether a sedentary genotype contrast in an exercise paper should ever be run as a labelled non-exercise secondary result (current rule: refuse).

## PMID33513138 / GSE152347 (2026-11-17)

- policy: Which threshold to report when the paper's genotype count (56) is close to padj<0.05 & |lfc|>0.585 (52) although the paper states FDR 5% only (open policy question).

## PMID34252634 / GSE144133 (2026-11-17)

- policy: Open policy question: the paper's 817 DEGs are matched by raw p < 0.05 with |log2FC| > 0.585 (811) rather than the stated FDR < 0.1 (16); which rule to report is not settled.

## PMID25484259 / GSE60591 (2026-11-17)

- policy: Open policy: which threshold to report when the paper's count (4076) is near raw p<0.05 on limma/FPKM (4198) rather than FDR<0.05.

## PMID36780527 / GSE199429 (2026-11-17)

- policy: Open policy: which test to report when limma on CPM cannot reproduce edgeR on counts (113 vs 121, 682 vs 744); recorded as declared deviation.

## PMID31589602 / GSE123879 (2026-11-17)

- policy: Joint 3-group limma vs the paper's pairwise fits when the paper is silent on joint modelling: open policy question.
- policy: Which threshold to report when 900 limma DEGs vs paper 1562 (padj<0.1 gives 1456): open policy question; recorded as declared deviation.

## PMID38686869 / GSE233004 (2026-11-24)

- policy: Joint versus pairwise fit when the paper is silent: joint was selected because it reproduces the paper's counts; open policy question.
- policy: Male count 26 vs paper 22 not exactly reproduced (pydeseq2 vs R DESeq2); noted in the record.

## PMID36084645 / GSE205891 (2026-11-24)

- policy: Which fit to treat as primary when the paper is silent on pairing (joint vs pairwise, paired vs unpaired) and counts differ (SC 0 vs 65).

## PMID35813950 / GSE205907 (2026-11-24)

- policy: Open policy: which threshold to report is not in question here (paper rule applied, FDR audit given).
- policy: E vs M group decoding rests on matrix column letters; no GSM-level confirmation (declared, medium confidence).

## PMID35850762 / GSE185530 (2026-11-24)

- policy: Policy: whether an in-vitro EPS series in C2C12 counts as an exercise study.
- policy: Policy: joint (Degust-style 36-library) versus two-arm voom as the primary fit when the paper implies one model; the executor cannot express a joint voom.

## PMID35291563 / GSE149405 (2026-11-24)

- policy: Which threshold to report when no rule fits the paper's 1344 (open policy); here the stated rule was applied and the mismatch recorded.

## PMID36611902 / GSE221003_acute (2026-11-24)

- policy: Open policy question (not an error): whether a drug-contrast dataset from a paper with an exercise test outcome should ever be run as a sensitivity analysis; skill rule says no exercise arm means refuse.

## PMID36611902 / GSE221003_chronic (2026-11-24)

- policy: Open policy question (not an error): whether drug-contrast series from papers with an exercise test outcome should get a labelled sensitivity run; the skill currently says refuse.

## PMID36120562 / GSE208354 (2026-11-24)

- policy: Open policy: which threshold to report when the paper's 690 DEGs fit none of the tested rules; the large gap (97 vs 690) is attributed to FPKM/limma vs DESeq2 counts and the FPKM>=1 filter, not verified.

## PMID36070371 / GSE202295 (2026-11-24)

- policy: Open policy: joint vs pairwise fit when the paper is silent; the T2D-recovery-unique count is 2349 vs the paper's 3185.
- policy: Paper's own edgeR paired route is blocked by the repository executor; DESeq2 is a declared deviation.

## PMID34880498 / GSE164401_HC_LPS (2026-11-24)

- policy: Open policy: plasma-transfer exercise-mediator series counted as exercise study.
- policy: Open policy: joint vs pairwise fit when paper is silent; padj<0.05 gives only 3 DEGs for LPS+RP vs LPS+CP versus 1395 at raw P.

## PMID34880498 / GSE164401_HC_RP_vs_CP (2026-11-24)

- policy: Open policy: plasma-transfer exercise-mediator series counted as exercise study.

## PMID35482926 / GSE198229_heart (2026-11-24)

- policy: B6 control contrast (a main paper comparison) is not run: ask the submitters for the matrix-column to N-ID map, or confirm from Dataset S1-S11 that the numeric columns correspond to specific GSMs.
- policy: Open policy question: which heart threshold to report when the paper states none (padj 0 DEG vs nominal P audit counts).

## PMID35482926 / GSE198229_soleus (2026-11-24)

- policy: B6 control contrast not run: ask the submitters for the matrix-column to N-ID map.
- policy: ND5 soleus OxPhos induction (S1.2.2.p1) is not seen in our result; judge from Dataset S1-S11 whether this is a data difference (no TMM, rounding, different gene set) or a sign problem.

## PMID35316212 / GSE184951 (2026-11-24)

- policy: Open policy question: the stated rule gives 55 and 1471 DEGs against the paper's 19 and 640, while a mean-count>=10 filter (iDEP default) gets close, especially for PRE vs CON (664). Which one to report as the headline is not settled; the case reports the paper's stated rule and keeps the filtered run as a sensitivity analysis.

## PMID32969079 / GSE146336 (2026-11-24)

- policy: Policy question only: if T3-by-genotype series were ever to count as exercise-adjacent, this case would need reopening. Under the skill's current rules it does not.

## PMID34219410 / GSE159217 (2026-11-24)

- policy: Policy: Older vs Young under matched activity is executable (suitability analyzable) but is an ageing estimand; refusal as an exercise study follows the skill's rule, but a person may want it recorded as non-exercise rather than refused.

## PMID38151020 / GSE198922 (2026-11-24)

- policy: Open policy: counts are 1.35-2x the paper's under the stated rule; whether to also report a pooled-model sensitivity fit.

## PMID34417591 / GSE174210 (2026-11-24)

- policy: Open policy question: whether an exercise-hormone (irisin) overexpression series counts as an exercise study. Refused here with the reason stated; a person may want it run as an exercise-mimetic case, but the deposited matrix is DESeq2-normalized (non-integer), so limma/voom on it would need a stated route.

## PMID34417591 / GSE174211 (2026-11-24)

- policy: Open policy question: joint ~grp versus pairwise fits when the paper is silent (S4.21.p1). Both a joint model and a pooled ~geno model are reported here, so nothing is hidden, but the primary choice is unsettled.
- policy: FNDC5 counts are slightly higher in KO (log2FC +0.36); the study record notes it but genotype labels were not re-verified from data. A person may want to confirm the KO allele design (partial exon deletion with intronic nuclear reads).

## PMID34417591 / GSE179078 (2026-11-24)

- policy: Open policy question: this is a genotype-only series (F5KO vs WT) that the paper itself uses for its DG bulk comparison. Refused for the exercise question; a person may decide whether a knockout of the exercise-hormone gene should be run as a labelled non-exercise case.

## PMID32483463 / GSE128651 (2026-11-24)

- policy: Raw p<0.01 vs FDR<0.05 ambiguity in paper is open policy; record both when the analysis runs.

## PMID36892893 / GSE213649 (2026-11-24)

- policy: Which of the paper's unreported sample exclusions applies is not stated; the exclusion of the two mislabelled liver samples is an inference that matches the paper's counts.

## PMID33042761 / GSE136623 (2026-11-24)

- policy: Policy question (open): whether a genotype contrast on an exercise-capacity gene (MI4OE vs MI4KO) should be run as a labelled non-exercise result. Currently refused; consistent with the skill rule.

## PMID33042761 / GSE140633 (2026-11-24)

- policy: Policy question (open): whether the genotype contrast MI4KO vs flox should be run as a labelled non-exercise result.

## PMID27304508 / GSE75919 (2026-11-24)

- policy: Policy: whether the analyzable genotype contrast (KO vs fl/fl after exercise, 4 vs 5) should be run as a labelled non-exercise result since the paper's RNA-seq estimand is exactly this contrast; refusal is consistent with the exercise-effect question.
