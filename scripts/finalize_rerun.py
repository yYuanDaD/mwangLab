from pathlib import Path
import pandas as pd, json, hashlib, os
from datetime import datetime, timezone
run=Path('output/native_codex_exercise_paperfirst_rerun_20261002T192328Z')
s=pd.read_csv(run/'summary.csv'); c=pd.read_csv(run/'sources/candidate_manifest.csv')
status=s.status.value_counts().to_dict()
metrics={'n_paper_candidates':int(len(c)),'n_full_texts_fetched':int((c.full_text_status=='ok').sum()),'n_papers_with_verified_accession':int(c.ownership_verified.sum()),'n_retained':int(len(s)),'n_rejected_for_no_database_or_ownership':int((~c.ownership_verified).sum()),'n_manual_review':int(s.manual_review.sum()),'manual_review_rate':float(s.manual_review.mean()),'paper_first_rate':1.0,'supplemental_GEO_rate':0.0,'baseline_manual_review_n':19,'baseline_candidate_n':50,'baseline_manual_review_rate':0.38,'manual_review_rate_delta_vs_baseline':float(s.manual_review.mean()-0.38),'status_counts':status}
report={'run_id':run.name,'generated_at_utc':datetime.now(timezone.utc).isoformat(),'keyword':'exercise','decision_maker':'current Codex conversation','external_llm_calls':0,'analysis_mode':'native Codex paper-first rerun; no LangChain agent or hidden validator','candidate_counts':metrics,'comparison_to_baseline':{'baseline_run':'output/native_codex_exercise_50_20261002T184212Z','baseline_manual_review_rate':0.38,'rerun_manual_review_rate':metrics['manual_review_rate'],'interpretation':'rate is lower, but denominator is the 16 retained paper-owned studies; 33 unlinked GEO-ranked hits were intentionally excluded rather than substituted'},'blocking_findings':['Semantic Scholar live API returned HTTP 429; cached ranked results reused with provenance','GSE24006 rejected because GEO metadata contradicts paper ownership','3 retained studies unsupported for independent matrix analysis','4 retained studies validly refused because no defensible exercise contrast or replication'], 'artifacts':{'paper_search':'sources/paper_search_semantic_scholar_cached.csv','paper_manifest':'sources/candidate_manifest.csv','accession_manifest':'sources/accession_manifest.csv','full_text_manifest':'sources/full_text_manifest.csv','summary':'summary.csv','workflow_log':'workflow.log','run_status':'run_status.json','evidence_dir':'evidence','decisions':'decision_records.json','failures':'failures.log','integrity':'integrity_report.json'}}
(run/'run_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
status={'run_id':run.name,'status':'completed_with_blocking_findings','updated_at_utc':datetime.now(timezone.utc).isoformat(),'study_total':len(s),'study_completed':int((s.execution_status=='completed').sum()),'study_manual_review':int(s.manual_review.sum()),'study_unsupported':int(s.status.str.startswith('unsupported').sum()),'study_refused':int((s.status=='valid_refusal').sum()),'warnings':['fresh Semantic Scholar endpoint rate limited; cache provenance preserved'],'evidence_dir':'evidence','summary':'summary.csv'}
(run/'run_status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False),encoding='utf-8')
# integrity checks
checks=[]
for _,r in s.iterrows():
 g=r.accession; ev=run/'evidence'/f'{g}.json'; checks.append({'accession':g,'evidence_exists':ev.exists(),'paper_full_text_exists':Path(json.loads(ev.read_text(encoding='utf-8'))['paper']['full_text_path']).exists(),'geo_metadata_exists':Path(json.loads(ev.read_text(encoding='utf-8'))['geo']['metadata_path']).exists(),'decision_exists':(run/'decisions'/f'{g}.json').exists()})
integrity={'run_id':run.name,'all_retained_have_evidence':all(x['evidence_exists'] for x in checks),'all_retained_have_paper_text':all(x['paper_full_text_exists'] for x in checks),'all_retained_have_geo_metadata':all(x['geo_metadata_exists'] for x in checks),'checks':checks,'external_llm_calls':0,'notes':['No p-values or DEG files were used to justify matrix/method validity.']}
(run/'integrity_report.json').write_text(json.dumps(integrity,indent=2,ensure_ascii=False),encoding='utf-8')
# index all current artifacts
arts=[]
for p in run.rglob('*'):
 if p.is_file() and p.name not in ('artifact_index.json',): arts.append({'path':str(p.relative_to(run)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(run/'artifact_index.json').write_text(json.dumps(arts,indent=2),encoding='utf-8')
print(json.dumps(metrics,indent=2))
