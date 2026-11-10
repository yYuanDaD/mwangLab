# 评审 GSE242861

总体结论：human（无 disagree 项；仅有一条开放政策问题）

## 需要人工决定
- miR-30 是根据运动反应的 miRNA 阵列结果选出的（S2.6.p1），因此 GSE242861 属于“体外运动介质”类系列。是否把这类系列算作运动研究尚未定论。如果算，则应运行 miR-30a/c 对 scramble 的比较，并以 donor 作为区组（donor 恰好连接每个样本一次，表达相关性检验支持，差值 0.544，p=0.0005），同时把论文未设 donor 区组的 Sex * Condition 模型记为差异。

## 其余检查
run_or_refuse、matrix_method、threshold、paper_match、stop_reason 均 agree；grouping、direction、pairing、model_fit、confounding 因未运行分析而为 na。拒绝理由“无运动因素”属实：18 个样本均为培养肌管，运动数据不在本系列中。
