# GSE208714 复核

总体结论：human（需人工处理）

## 未确定项

### stop_reason（unsure，major）
- 论文 Supplementary Data 2（含逐样本 RNA 产量）未下载，是最可能含“实验室编号到条件”对应关系的文件；因此“任何来源都没有 key”的说法证据不够宽。
- 其余来源（GEO、SOFT、SRA、BioSample、CUT&RUN 系列）已查，NT 6 / TG 14 的前缀分布无法对应任何分组，停止本身合理。
- 建议：获授权后下载该补充表核对；若有对应关系，把它作为带来源说明的 key 重新运行；否则联系作者。在此之前把停止理由改写为“已存数据中未找到 key；补充表未核对”。

## 待人工确认
- 是否授权下载 Supplementary Data 2。
- 论文剔除的 2 个 sedentary、1 个 ELE 离群样本未被命名，即使有 key 也无法还原 3 vs 2。

其余各项检查（run_or_refuse、threshold 同意；其他因未运行分析而不适用）。
