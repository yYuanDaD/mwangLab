# GSE280656_cartilage 审查结果

总体结论:**fix**

关节软骨(cartilage)病例因每个运动组仅有 n=2 而在 design 阶段停止,没有产出任何结果。但论文本身在 n=2 下用 iDEP/DESeq2 做了分析,且技能规则明确写明“小样本本身不是停止理由,应运行并标记为探索性”,所以停止理由与规则相矛盾(重大)。建议按计划对比以探索性方式运行并标注 n=2;分组、方向、阈值(FDR<0.1,FC>2)记录均正确。

## run_or_refuse (disagree, major)

证据:Paper analysed cartilage RNA-seq with the same groups (Fig 4, Fig 5, S2.4); packet A metadata carry control/S1/S4/S24/R24. The case was refused at design only because of n=2 per exercise arm.

修改建议:Run the planned cartilage contrasts as exploratory instead of refusing.

## stop_reason (disagree, major)

证据:Stop reason 'n=2 per exercise arm, sample_size hard fail' is true as a fact about the data, but SKILL.md line 84 and decision-contract.md line 78 say 'Small n alone is not a stop': run and label exploratory (fewer than 3 replicates in an arm). The paper itself ran iDEP DESeq2 at n=2 vs 3. The design record itself notes the conflict with tools/suitability.py and tools/decision_contract.py:172-173.

修改建议:Record design as valid with the planned contrasts (S1/S4/S24/R24 vs Control, S4 vs S1, S24 vs S4, R24 vs S24); run tools.joint_contrasts:run_joint_deseq2 with include for the small-n planned contrasts and exploratory_reason 'arm n=2 < 3'; label every cartilage result exploratory; enrich S1 and R24 vs Control as for synovium.

## 待人工决定
- Code vs skill conflict: suitability.py hard-fails sample_size and decision_contract.py rejects a valid design under that verdict, against the skill rule 'small n alone is not a stop'. The gate may need changing, or the case must go through the contract's exploratory path.
- Joint versus pairwise fit when the paper is silent (open policy question).
