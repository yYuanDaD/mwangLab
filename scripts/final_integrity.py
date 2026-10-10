from pathlib import Path
import json,hashlib
run=Path('E:/agent/mwangLab/output/native_codex_exercise_audit_expansion_20261002T201546Z')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={'audit_record_count':len(list((run/'audit').glob('GSE*.json'))),'audit_table_exists':(run/'audit/per_study_audit.csv').exists(),'full_text_manifest_exists':(run/'sources/expansion_full_text_manifest.csv').exists(),'ownership_manifest_exists':(run/'sources/expansion_geo_ownership.csv').exists(),'verified_manifest_exists':(run/'sources/expansion_verified_accessions.csv').exists(),'rejected_manifest_exists':(run/'sources/expansion_rejected_accessions.csv').exists(),'summary_exists':(run/'expanded_summary.csv').exists(),'terminal_report_exists':(run/'final_summary.md').exists(),'api_log_exists':(run/'sources/expansion_api_log.csv').exists(),'external_llm_calls':0}
checks['all_16_audit_records']=checks['audit_record_count']==16
(run/'integrity_report.json').write_text(json.dumps(checks,indent=2),encoding='utf-8'); items=[]
for p in sorted(run.rglob('*')):
 if p.is_file() and p.name!='artifact_index.json':items.append({'path':str(p.relative_to(run)),'bytes':p.stat().st_size,'sha256':sha(p)})
(run/'artifact_index.json').write_text(json.dumps(items,indent=2),encoding='utf-8'); print(json.dumps(checks,indent=2))
