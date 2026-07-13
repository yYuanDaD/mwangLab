"""Flow-chart annotation figures for #1 (DA method selection) and #3 (metadata -> structural tables).
Each box is tagged with the code function so the diagram maps 1:1 onto the implementation.
Output -> 0623/04_method_walkthrough/.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/reports/make_req_diagrams.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = "0623/04_method_walkthrough"
os.makedirs(OUT, exist_ok=True)


def box(ax, x, y, w, h, title, body="", code="", fc="#eef2f7", ec="#9bb0c3", lw=1.0, tsize=11, bsize=8.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.01",
                                fc=fc, ec=ec, lw=lw))
    cy = y + h - 0.018
    ax.text(x + 0.012, cy, title, fontsize=tsize, fontweight="bold", va="top")
    if code:
        ax.text(x + 0.012, cy - 0.030, code, fontsize=7.0, va="top", family="monospace", color="#5b6b7b")
    if body:
        ax.text(x + 0.012, y + 0.012, body, fontsize=bsize, va="bottom", color="#23303c")


def arrow(ax, x1, y1, x2, y2, label="", color="#7f8c9a"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13, color=color, lw=1.3))
    if label:
        ax.text((x1 + x2) / 2 + 0.008, (y1 + y2) / 2, label, fontsize=7.8, color="#444", va="center")


# ======================= #1 — DA method selection =======================
fig = plt.figure(figsize=(13.5, 7.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
fig.suptitle("#1 DA 方法选择 —— 两层:① 矩阵类型自动分发  ② raw_da_method 选法(去掉每研究 LLM)",
             fontsize=13, fontweight="bold", y=0.975)

# 左列：第0层 矩阵分发
box(ax, 0.03, 0.86, 0.34, 0.085, "输入:一个研究的表达矩阵", code="batch_tools._classify_matrix", fc="#dfe7f0")
arrow(ax, 0.20, 0.86, 0.20, 0.80)
box(ax, 0.03, 0.70, 0.34, 0.095, "第 0 层 · 按矩阵类型分发", "决定哪一族方法合法(自动,非 #1)", fc="#eef2f7")
# 三个类型分支
arrow(ax, 0.12, 0.70, 0.10, 0.585)
arrow(ax, 0.20, 0.70, 0.20, 0.585)
arrow(ax, 0.30, 0.70, 0.31, 0.585)
box(ax, 0.015, 0.50, 0.165, 0.085, "raw_counts", "→ DESeq2 / edgeR / limma-voom\n(进入第 1 层)", fc="#e7f0e9", ec="#7bb38e", lw=1.6)
box(ax, 0.195, 0.50, 0.085, 0.085, "fpkm/tpm\nlog", "→ limma-trend", fc="#f2efe6", bsize=8)
box(ax, 0.29, 0.50, 0.095, 0.085, "蛋白组强度", "→ limma", fc="#f2efe6", bsize=8)
ax.text(0.03, 0.46, "(甲基化 β→M值→limma 见 methylation_tools;ATAC/变异/纯SRA → fail-loud 跳过)",
        fontsize=7.4, color="#777", va="top")

# raw_counts → 第1层
arrow(ax, 0.098, 0.50, 0.098, 0.43, color="#7bb38e")
ax.text(0.115, 0.455, "仅 raw_counts 进入 →", fontsize=8, color="#3a7a52")

# 右列：第1层 raw_da_method 决策树
box(ax, 0.43, 0.84, 0.54, 0.075, "第 1 层 · raw_da_method 选三法之一", code="batch_tools.py:1083  switch(raw_da_method)", fc="#dfe7f0")
modes = [
    ("'auto'  (#1 默认省钱)", "→ DESeq2", "choose_raw_da_method_rule",
     "decision=rule · 零 LLM · 确定性规则", "#e7f0e9", "#b03a2e", 1.8),
    ("'all'", "→ DESeq2+edgeR+limma-voom 共识", "_run_contrast_multi",
     "decision=all · 零 LLM · ≥2 法显著=DEG", "#eef2f7", "#1b2a38", 1.0),
    ("'auto-llm' (可选)", "→ LLM 挑", "choose_raw_da_method_with_llm",
     "decision=llm · 1 次 LLM/研究 · 自适应(旧逻辑保留)", "#fbeae7", "#1b2a38", 1.0),
    ("'deseq2'/'edger'/'limma-voom'", "→ 强制该法", "",
     "decision=param · 零 LLM", "#eef2f7", "#1b2a38", 1.0),
    ("其它/未知", "→ DESeq2", "",
     "decision=default · 零 LLM · 兜底", "#eef2f7", "#1b2a38", 1.0),
]
y = 0.80
for title, meth, code, foot, fc, fcol, lw in modes:
    h = 0.085
    y -= h + 0.018
    box(ax, 0.43, y, 0.54, h, f"{title}   {meth}", foot, code, fc=fc, ec=("#d6604d" if lw > 1 else "#9bb0c3"), lw=lw)
arrow(ax, 0.40, 0.46, 0.43, 0.46, color="#7bb38e")
ax.text(0.50, 0.05, "记录:summary.csv da_method/da_method_reason + decisions.json da_method_select(decision+reason)",
        fontsize=8, color="#444", va="bottom")
fig.savefig(os.path.join(OUT, "req1_da_selection_flow.png"), dpi=140, bbox_inches="tight"); plt.close(fig)
print("saved req1_da_selection_flow.png")


# ======================= #3 — metadata -> structural tables =======================
fig = plt.figure(figsize=(14, 7.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
fig.suptitle("#3 确定性 —— GEO 元数据 CSV → 确定性派生 4 张结构表(纯函数,零 LLM → 跨跑字节一致)",
             fontsize=13, fontweight="bold", y=0.975)

# 左：元数据
box(ax, 0.02, 0.40, 0.20, 0.30, "GEO 元数据 CSV", "一行 = 一个 GSM 样本\n列:organism_ch1 /\ncharacteristics_ch1.1.time /\ninstrument_model /\nlibrary_strategy / …",
    code="metadata_structural._load_metadata", fc="#dfe7f0", bsize=8.4)
arrow(ax, 0.22, 0.55, 0.27, 0.55)

# 中：三步
box(ax, 0.27, 0.62, 0.26, 0.10, "① 认列(语义角色)", "列名模式 → species/sex/age/\ninstrument/strategy…", code="_resolve_roles", fc="#eef2f7", bsize=8)
box(ax, 0.27, 0.47, 0.26, 0.11, "② 挑设计列(确定性打分)", "设计词+2 / 描述符−1 / 均衡+1 /\n非characteristics−2;平手→更多值", code="_pick_design_column:162", fc="#eef2f7", bsize=8)
box(ax, 0.27, 0.34, 0.26, 0.10, "③ 排序枚举 + 去重", "GSM排序 / 组织去重 /\n设计值排序 / 平台组合排序", code="build_structural_tables:241", fc="#eef2f7", bsize=8)
arrow(ax, 0.53, 0.50, 0.585, 0.50)

# 右：四张表
tables = [
    ("sample", "一行/GSM(排序编号)", "samp{n}", 0.83),
    ("subject", "一行/不同生物体(去重)", "subj{n}", 0.635),
    ("groups", "设计列不同值(排序)", "grp{n}", 0.44),
    ("assay", "一行/(仪器,strategy) 组合", "assay{n}", 0.245),
]
for name, body, idfmt, y in tables:
    box(ax, 0.585, y, 0.255, 0.155, f"{name}", body + f"\nid={idfmt} · 每字段带 _source",
        fc="#e7f0e9", ec="#7bb38e", lw=1.4, bsize=8.2)
# fan-out arrows from step③ output to each of the 4 table boxes
for _, _, _, y in tables:
    arrow(ax, 0.555, 0.39, 0.585, y + 0.0775, color="#7bb38e")

# provenance + result banners
box(ax, 0.27, 0.05, 0.57, 0.10, "出处 _srow", "每字段两列:<field> 值 + <field>_source = \"GEO metadata: <列名>\"\nverify_provenance 豁免这类结构出处(非论文逐字引)", code="metadata_structural._srow", fc="#fff6e6", ec="#d8b25a", bsize=8.4)
ax.text(0.02, 0.16,
        "覆盖点:flatten_extraction(metadata_csv) 用这 4 张表\n替换 LLM 抽的版本(fail-soft)\n→ seacdm_tools.py:694",
        fontsize=7.8, color="#444", va="top", family="monospace")
ax.text(0.86, 0.55,
        "确定性结果\n(3 次跑字节一致)\n\nsample [2,7,7]→[70,70,70]\ngroups [6,6,21]→[6,6,6]\n字段稳定 68%→89.9%",
        fontsize=8.2, color="#b03a2e", va="center", fontweight="bold")
fig.savefig(os.path.join(OUT, "req3_metadata_to_structural_flow.png"), dpi=140, bbox_inches="tight"); plt.close(fig)
print("saved req3_metadata_to_structural_flow.png")
print("DONE.")
