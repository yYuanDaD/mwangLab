"""Short review sheet: the wrong/doubtful rows, three policy questions, five back-linked papers."""
import os, random
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

REV = "test/experiments/paper_screen_20261019/review_20261027"
src = load_workbook(os.path.join(REV, "review_sheet.xlsx"))
wb = Workbook()
yellow = PatternFill("solid", fgColor="FFF2CC"); blue = PatternFill("solid", fgColor="DDEBF7")

# 1. wrong / doubtful rows
s1 = src["复核"]
rows = [r for r in range(2, s1.max_row + 1) if s1.cell(r, 8).value in ("错", "存疑")]
ws = wb.active; ws.title = "1 确认我的判断"
keep = ["#", "标题", "相关 GSE", "我的判断", "我的说明", "原文摘录", "全文（本地）", "全文（PMC）", "GEO 链接"]
ws.append(keep + ["你的结论", "你的备注"])
hdr = [c.value for c in s1[1]]
for r in rows:
    ws.append([s1.cell(r, hdr.index(k) + 1).value for k in keep] + ["", ""])
    for k, name in enumerate(keep, 1):
        h = s1.cell(r, hdr.index(name) + 1).hyperlink
        if h is not None:
            c = ws.cell(ws.max_row, k); c.hyperlink = h.target; c.style = "Hyperlink"
for c in ws[1]: c.font = Font(bold=True); c.fill = blue
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
for k, w in enumerate([4, 40, 16, 8, 55, 70, 18, 18, 18, 14, 30], 1): ws.column_dimensions[ws.cell(1, k).column_letter].width = w
for r in range(2, ws.max_row + 1): ws.cell(r, 10).fill = yellow; ws.cell(r, 11).fill = yellow
dv = DataValidation(type="list", formula1='"我说得对,我说错了,看不出"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"J2:J{ws.max_row}")
ws.freeze_panes = "C2"

# 2. policy questions
wp = wb.create_sheet("2 政策问题")
wp.append(["问题", "受影响的文章（1000 篇里）", "例子", "我的建议", "你的决定"])
wp.append(["芯片数据要不要走 limma？", "24 篇首个排除原因是芯片（自有芯片系列 38 个）",
           "#31 人肌肉冷适应与训练前后（GSE53598、GSE156249）", "要。技能本身支持芯片，人肌肉训练的经典数据多是芯片", ""])
wp.append(["只有 FPKM/TPM/log 值的数据要不要走 limma？", "33 篇（only normalized）",
           "#45 饮食+运动前后 log2CPM 13 对 13；#38 Lindholm 耐力训练 FPKM", "要。导师的方法表写了 log(TPM/RPKM) → limma", ""])
wp.append(["只有 SRA 原始 reads（GEO 无矩阵）的要不要？", "非 GEO 中的 SRA 部分 + 无矩阵 15 篇中的一部分",
           "#29 跑台+甲基苯丙胺 9 样本；#40 大鼠骨 14 样本", "暂不要。需要从 FASTQ 比对，流程不支持，代价大", ""])
wp.append(["人、小鼠、大鼠以外的物种要不要？", "11 篇", "#36 斑马鱼游泳训练；#37 果蝇", "不要，除非研究问题需要", ""])
for c in wp[1]: c.font = Font(bold=True); c.fill = blue
for row in wp.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    row[4].fill = yellow
for k, w in enumerate([36, 30, 45, 40, 20], 1): wp.column_dimensions[wp.cell(1, k).column_letter].width = w
dv = DataValidation(type="list", formula1='"要,不要,再说"', allow_blank=True); wp.add_data_validation(dv); dv.add("E2:E5")

# 3. five back-linked papers (on topic, analyzable on the data side)
s2 = src["GEO反查可补回"]
hdr2 = [c.value for c in s2[1]]
cand = [r for r in range(2, s2.max_row + 1) if s2.cell(r, 4).value == "是" and s2.cell(r, 7).value.startswith("analyzable")]
pick = sorted(random.Random(20261027).sample(cand, 5))
w3 = wb.create_sheet("3 补回抽查5篇")
keep2 = ["#", "原筛选层", "标题", "PMID", "GSE", "分组", "原文摘录", "全文（本地）", "全文（PMC）", "GEO 链接"]
w3.append(keep2 + ["是本文自己的运动数据吗", "你的备注"])
for r in pick:
    w3.append([s2.cell(r, hdr2.index(k) + 1).value for k in keep2] + ["", ""])
    for k, name in enumerate(keep2, 1):
        h = s2.cell(r, hdr2.index(name) + 1).hyperlink
        if h is not None:
            c = w3.cell(w3.max_row, k); c.hyperlink = h.target; c.style = "Hyperlink"
for c in w3[1]: c.font = Font(bold=True); c.fill = blue
for row in w3.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
for k, w in enumerate([4, 20, 45, 10, 12, 36, 60, 18, 18, 18, 16, 30], 1): w3.column_dimensions[w3.cell(1, k).column_letter].width = w
for r in range(2, w3.max_row + 1): w3.cell(r, 11).fill = yellow; w3.cell(r, 12).fill = yellow
dv = DataValidation(type="list", formula1='"是,不是,看不出"', allow_blank=True); w3.add_data_validation(dv); dv.add(f"K2:K{w3.max_row}")
w3.freeze_panes = "D2"
out = os.path.join(REV, "review_sheet_short.xlsx"); wb.save(out)
print(out, len(rows), "rows;", [s2.cell(r, 3).value[:50] for r in pick])

# 4. correctly excluded examples, one per layer
wb = load_workbook(out)
w4 = wb.create_sheet("4 正确排除的例子")
EX = [2, 5, 13, 16, 20, 24, 41, 46]   # review, off-topic, meta-analysis, qPCR, reuse, privacy, DE tables only, scRNA n=2
keep4 = ["#", "筛选层", "标题", "相关 GSE", "筛选器的理由", "我的说明", "原文摘录", "全文（本地）", "全文（PMC）", "DOI", "GEO 链接"]
w4.append(keep4 + ["你的结论", "你的备注"])
for i in EX:
    r = i + 1
    w4.append([s1.cell(r, hdr.index(k) + 1).value for k in keep4] + ["", ""])
    for k, name in enumerate(keep4, 1):
        h = s1.cell(r, hdr.index(name) + 1).hyperlink
        if h is not None:
            c = w4.cell(w4.max_row, k); c.hyperlink = h.target; c.style = "Hyperlink"
for c in w4[1]: c.font = Font(bold=True); c.fill = blue
for row in w4.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
for k, w in enumerate([4, 20, 40, 14, 36, 45, 60, 16, 16, 16, 16, 14, 30], 1): w4.column_dimensions[w4.cell(1, k).column_letter].width = w
for r in range(2, w4.max_row + 1): w4.cell(r, 12).fill = yellow; w4.cell(r, 13).fill = yellow
dv = DataValidation(type="list", formula1='"确实不能用,其实能用,看不出"', allow_blank=True); w4.add_data_validation(dv); dv.add(f"L2:L{w4.max_row}")
w4.freeze_panes = "D2"
wb.save(out); print("sheet 4:", [w4.cell(r, 3).value[:40] for r in range(2, w4.max_row + 1)])
