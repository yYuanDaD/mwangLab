# GSE216408 复核结论:pass

GSE216408 的 7 个测序样本(GAS,KO n=4,WT n=3)全部来自制动小鼠,只有基因型不同,没有运动组。拒绝分析正确。

## 需关注项(不影响结论)
- stop_reason(minor):“无运动组”的理由属实。suitability 报告里的 sample_size 失败是空因子列表造成的假象,HANDBACK 已说明。可选修复:tools/suitability.py 在无设计因子时报告为 no design。

## 待人工确认的开放政策
- 制动下的基因型对比是否可算运动研究:目前按规则拒绝。
