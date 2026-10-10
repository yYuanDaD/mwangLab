from pathlib import Path
import json
import pandas as pd
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from test.experiments.exergenedb_50_semantic_review import run_review as base

ARCHIVE=ROOT/'archive'/'runtime'/'data_20260930'
STAGE=ROOT/'output'/'exergenedb_site50_random_review_20261001'/'input_data'
OUT=ROOT/'output'/'exergenedb_site50_random_review_20261001'
SEARCH=ROOT/'archive'/'runtime'/'output_20260930'/'search_Exercise.csv'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    search_df=pd.read_csv(SEARCH)
    accs=search_df['accession'].astype(str).tolist()
    manifest={
        'benchmark':'ExerGeneDB website-search 50-study ordinary-set semantic preflight',
        'source_csv':str(SEARCH.relative_to(ROOT)),
        'case_count':len(accs),
        'accessions':accs,
        'known_problem_cases':[x for x in accs if x in base.KNOWN_PROBLEM],
        'provider':base.resolve_model_config().provider,
        'model':base.resolve_model_config().model,
        'scope':'semantic decisions only; metadata from GEO, local matrices only where archived; no p-values or enrichment calls',
    }
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    usage_start=base.llm_usage_checkpoint(); records=[]
    for i,acc in enumerate(accs,1):
        archive_meta=ARCHIVE/acc/f'{acc}_metadata.csv'
        base.ARCHIVE_DATA=ARCHIVE if archive_meta.exists() else STAGE
        print(f'[{i}/{len(accs)}] {acc}',flush=True)
        rec=base.review_one(acc,usage_start)
        title=search_df.loc[search_df['accession'].astype(str)==acc,'title'].iloc[0]
        rec['source_list_title']=str(title)
        records.append(rec)
        (OUT/'records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
        print('  flags='+(','.join(rec['flags']) or 'none'),flush=True)
    final={'manifest':manifest,'records':records,'usage':base.llm_usage_summary(usage_start),
           'flag_counts':pd.Series([f for r in records for f in r['flags']]).value_counts().to_dict()}
    (OUT/'report.json').write_text(json.dumps(final,indent=2,ensure_ascii=False),encoding='utf-8')
    pd.DataFrame([{'accession':r['accession'],'n_samples':r['n_samples'],'python_pick':r['python_pick'],'flags':';'.join(r['flags'])} for r in records if r['flags']]).to_csv(OUT/'flagged_cases.csv',index=False,encoding='utf-8-sig')
    print(json.dumps(final['flag_counts'],indent=2,ensure_ascii=False)); print(json.dumps(final['usage'],indent=2,ensure_ascii=False))

if __name__=='__main__': main()
