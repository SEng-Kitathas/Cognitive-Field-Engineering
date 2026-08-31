#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def H(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main(root:Path,out:Path):
 rels=[
  'state/next_steps/V12_FACTOR_PRIMITIVE_COMPOSITION_PREREG_DRAFT_2026-08-30.json',
  'state/next_steps/V12_FACTOR_PRIMITIVE_TRAINING_CONTRACT_2026-08-30.json',
  'state/qualification/V12_FACTOR_PRIMITIVE_STATIC_HOSTILE_2026-08-30.json',
  'state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/ADMISSION.json',
  'state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/PREDICATE_RESULTS.jsonl',
  'state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/POLICY_RESULTS.jsonl',
  'state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/COMPOSE_RESULTS.jsonl',
  'tools/build_v12_factor_primitive_composition_candidate.py',
  'tools/audit_v12_factor_primitive_composition_candidate.py',
  'tools/run_v12_factor_primitive_baseline_admission.py',
  'tools/v12_factor_primitive_common.py',
  'tools/train_v12_factor_primitive.py',
  'tools/evaluate_v12_factor_primitive.py',
  'tools/run_v12_factor_primitive_campaign.py'
 ]
 cand=root/'state/candidates/v12_factor_primitive_composition_20260830'
 for p in sorted(cand.iterdir()):
  if p.is_file():rels.append(p.relative_to(root).as_posix())
 files={}
 for rel in rels:
  p=root/rel
  if not p.is_file():raise SystemExit(f'MISSING {rel}')
  files[rel]={'bytes':p.stat().st_size,'sha256':H(p)}
 anchors={
  'prereg_sha256':'e929a4ab201a86faaf7f910438b53e1349d4ac2a7a0d29a960d1381392657bf9',
  'training_contract_sha256':'a2136043b8fdefb9acf9100bb341458e823324216c384ffd91c4e75b8aefe58f',
  'candidate_manifest_sha256':'b03b0eca0ecf39554491e787e64a5fae0102bcff7700c81630f66c3005bc1ca1',
  'token_schedule_audit_sha256':'f3aa40f53d7c75b277213ed3753b51fb806d3eccc07097d508b4c115e6423679',
  'static_qualification_sha256':'3f72abbcf839085972186cf6c129111a2dd1de6633672653bb8e6619750a2ee6',
  'baseline_admission_sha256':'b8adf6c257e1a1344c43951a47081f37bfdc0bfdafd4d0747a906057024a866c'
 }
 checks={
  'prereg_sha256':files['state/next_steps/V12_FACTOR_PRIMITIVE_COMPOSITION_PREREG_DRAFT_2026-08-30.json']['sha256'],
  'training_contract_sha256':files['state/next_steps/V12_FACTOR_PRIMITIVE_TRAINING_CONTRACT_2026-08-30.json']['sha256'],
  'candidate_manifest_sha256':files['state/candidates/v12_factor_primitive_composition_20260830/MANIFEST.json']['sha256'],
  'token_schedule_audit_sha256':files['state/candidates/v12_factor_primitive_composition_20260830/TOKEN_SCHEDULE_AUDIT.json']['sha256'],
  'static_qualification_sha256':files['state/qualification/V12_FACTOR_PRIMITIVE_STATIC_HOSTILE_2026-08-30.json']['sha256'],
  'baseline_admission_sha256':files['state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/ADMISSION.json']['sha256']
 }
 if checks!=anchors:raise SystemExit('ANCHOR_DRIFT '+repr({k:(checks[k],anchors[k]) for k in anchors if checks[k]!=anchors[k]}))
 lock={'schema':'cfe.v12.factor-primitive-input-lock.v1','status':'LOCKED_PRE_RUNTIME__NO_V12_SCIENTIFIC_TRAINING','file_count':len(files),'files':files,'anchors':anchors,'scientific_training_authorized':False,'mutation_rule':'Any locked-byte change invalidates this lock and requires new identity/runtime qualification.','laws':['LOCKED_INPUTS != QUALIFIED_RUNTIME','BASELINE_ADMITTED != COMPOSITION_EFFECT','LOCK_MUTATION_REQUIRES_NEW_IDENTITY']}
 if out.exists():raise SystemExit('REFUSE_OVERWRITE')
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(lock,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':lock['status'],'file_count':lock['file_count'],'lock_sha256':H(out)},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/locks/V12_FACTOR_PRIMITIVE_INPUT_LOCK_2026-08-30.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
