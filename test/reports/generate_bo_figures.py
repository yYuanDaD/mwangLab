import pandas as pd, numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

root=Path('E:/agent/mwangLab')
out=root/'output'/'bo_figures_20260911'; out.mkdir(parents=True, exist_ok=True)
sns.set_theme(style='whitegrid', context='talk')

# GSE279359 method comparison
base=root/'output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359'
rows=[]
for label,stem in [('Immediate','immediately_post-exercise_vs_pre-exercise'),('1 h','1_hour_post-exercise_vs_pre-exercise'),('24 h','24_hours_post-exercise_vs_pre-exercise')]:
    for method in ['deseq2','edger','limma-voom']:
        p=base/f'DEG_results_{stem}__{method}.csv'
        df=pd.read_csv(p)
        # standard column names
        fc='log2FoldChange' if 'log2FoldChange' in df else 'log2FC'
        padj='padj' if 'padj' in df else 'FDR'
        n=((df[padj]<0.05)&(df[fc].abs()>1)).sum()
        rows.append((label,method,int(n)))
counts=pd.DataFrame(rows,columns=['time','method','n'])
plt.figure(figsize=(10,6)); sns.barplot(data=counts,x='time',y='n',hue='method',palette='Set2'); plt.ylabel('Significant features (padj < 0.05, |log2FC| > 1)'); plt.xlabel('Post-exercise time'); plt.title('GSE279359: Agent differential-analysis counts'); plt.tight_layout(); plt.savefig(out/'gse279359_method_comparison.png',dpi=220); plt.close()

# GSE282641 GSEA NES
p=root/'output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/DEG_results_ko_vs_wt_GSEA_Hallmark.csv'
df=pd.read_csv(p); keep=df[df['Term'].str.contains('OXIDATIVE_PHOSPHORYLATION|GLYCOLYSIS|FATTY_ACID_METABOLISM',regex=True)].copy(); keep['label']=keep['Term'].str.replace('HALLMARK_','').str.replace('_',' ').str.title(); keep=keep.sort_values('NES')
plt.figure(figsize=(10,5)); colors=['#4c78a8' if x>0 else '#f58518' for x in keep.NES]; plt.barh(keep.label,keep.NES,color=colors); plt.axvline(0,color='black',lw=.8); plt.xlabel('Normalized enrichment score (NES)'); plt.title('GSE282641: Agent Hallmark GSEA (KO vs WT)');
for y,v,q in zip(range(len(keep)),keep.NES,keep['FDR q-val']): plt.text(v+(0.06 if v>=0 else -0.06),y,f'{v:.2f}  FDR={q:.3f}',va='center',ha='left' if v>=0 else 'right',fontsize=10)
plt.xlim(-1.9,3.55); plt.tight_layout(); plt.savefig(out/'gse282641_gsea_nes.png',dpi=220); plt.close()

# GSE317978 metrics
metrics=pd.DataFrame({'metric':['Pearson r','Spearman rho','Same-sign fraction','DEG overlap Jaccard','Jaccard with |log2FC|>1'], 'value':[.665,.789,.739,.306,.137]})
plt.figure(figsize=(10,5)); sns.barplot(data=metrics,x='value',y='metric',color='#59a14f'); plt.xlim(0,1); plt.xlabel('Agreement metric'); plt.title('GSE317978: Agent vs author result agreement');
for i,v in enumerate(metrics.value): plt.text(v+.02,i,f'{v:.3f}',va='center',fontsize=11)
plt.tight_layout(); plt.savefig(out/'gse317978_agreement_metrics.png',dpi=220); plt.close()

# Kang scRNA cell-type DEG
p=root/'output/scrna_demo_kang/scrna_pseudobulk_summary.csv'; df=pd.read_csv(p); df=df.sort_values('n_deg',ascending=True)
plt.figure(figsize=(10,6)); colors=['#e15759' if s!='deg_gsea_ok' else '#76b7b2' for s in df.status]; plt.barh(df.celltype,df.n_deg.fillna(0),color=colors); plt.xlabel('DEG count (Agent pseudobulk DESeq2)'); plt.title('Kang scRNA-seq: Agent DEG counts by cell type');
for i,(v,s) in enumerate(zip(df.n_deg.fillna(0),df.status)): plt.text(v+max(df.n_deg.fillna(0))*0.01,i,f'{int(v)}' if pd.notna(v) else 'NA',va='center',fontsize=10)
plt.tight_layout(); plt.savefig(out/'kang_scrna_deg_by_celltype.png',dpi=220); plt.close()

# evidence index
counts.to_csv(out/'gse279359_method_counts.csv',index=False)
keep[['Term','NES','FDR q-val']].to_csv(out/'gse282641_selected_gsea.csv',index=False)
metrics.to_csv(out/'gse317978_agreement_metrics.csv',index=False)
print('\n'.join(str(x) for x in sorted(out.glob('*'))))

