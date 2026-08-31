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
  'state/next_steps/V13_OPTIMIZER_VISIBLE_PRIMITIVE_INTERFERENCE_PREREG_2026-08-31.json',
  'state/next_steps/V13_OPTIMIZER_INTERFERENCE_TRAINING_CONTRACT_2026-08-31.json',
  'state/qualification/V13_OPTIMIZER_INTERFERENCE_STATIC_HOSTILE_2026-08-31.json',
  'state/qualification/V13_BASELINE_INHERITANCE_20260831.json',
  'state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/ADMISSION.json',
  'tools/audit_v13_optimizer_interference_candidate.py',
  'tools/v13_optimizer_interference_common.py',
  'tools/train_v13_optimizer_interference.py',
  'tools/evaluate_v13_optimizer_interference.py',
  'tools/run_v13_optimizer_interference_campaign.py',
  'tools/lock_v13_optimizer_interference.py'
 ]
 cand=root/'state/candidates/v13_optimizer_interference_20260831'
 for p in sorted(cand.iterdir()):
  if p.is_file():rels.append(p.relative_to(root).as_posix())
 files={}
 for rel in rels:
  p=root/rel
  if not p.is_file():raise SystemExit(f'MISSING {rel}')
  files[rel]={'bytes':p.stat().st_size,'sha256':H(p)}
 anchors={
  'preregistration_sha256':'da66a2202fc89aa726c8381681c1ffbcac4c98cf8dc65ea86cb2db998ae296b5',
  'training_contract_sha256':'0bb1130de69c0d896a457c78ac1ccc7f895bb527e2d71d8cefb68b2692f6b390',
  'candidate_manifest_sha256':'afb37e44a427f8352dac9b50e03503cd96c282c81d44f74759cc69cb9d93ef31',
  'static_qualification_sha256':'d372ccae53489fb944364586f6144d117f0567cb73a7448a8601eebd68ffb6b3',
  'baseline_inheritance_sha256':'b541ee80cc8e4f309e77064fce42544d231f4b5653a2841b9b4809a4c59446fa',
  'source_v12_baseline_admission_sha256':'b8adf6c257e1a1344c43951a47081f37bfdc0bfdafd4d0747a906057024a866c'
 }
 checks={
  'preregistration_sha256':files['state/next_steps/V13_OPTIMIZER_VISIBLE_PRIMITIVE_INTERFERENCE_PREREG_2026-08-31.json']['sha256'],
  'training_contract_sha256':files['state/next_steps/V13_OPTIMIZER_INTERFERENCE_TRAINING_CONTRACT_2026-08-31.json']['sha256'],
  'candidate_manifest_sha256':files['state/candidates/v13_optimizer_interference_20260831/MANIFEST.json']['sha256'],
  'static_qualification_sha256':files['state/qualification/V13_OPTIMIZER_INTERFERENCE_STATIC_HOSTILE_2026-08-31.json']['sha256'],
  'baseline_inheritance_sha256':files['state/qualification/V13_BASELINE_INHERITANCE_20260831.json']['sha256'],
  'source_v12_baseline_admission_sha256':files['state/qualification/V12_FACTOR_PRIMITIVE_BASELINE_ADMISSION_20260830/ADMISSION.json']['sha256']
 }
 if checks!=anchors:raise SystemExit('ANCHOR_DRIFT '+repr({k:(checks[k],anchors[k]) for k in anchors if checks[k]!=anchors[k]}))
 lock={'schema':'cfe.v13.optimizer-interference-input-lock.v1','status':'LOCKED_PRE_RUNTIME__NO_V13_SCIENTIFIC_TRAINING','file_count':len(files),'files':files,'anchors':anchors,'scientific_training_authorized':False,'scientific_difference':'accumulation-window primitive mixing only','mutation_rule':'Any locked-byte change invalidates this lock and requires new identity/runtime qualification.','laws':['LOCKED_INPUTS != QUALIFIED_RUNTIME','SAME EXPERIENCE MULTISET != SAME OPTIMIZER-VISIBLE DEVELOPMENTAL PRESSURE','LOCK MUTATION REQUIRES NEW IDENTITY']}
 if out.exists():raise SystemExit('REFUSE_OVERWRITE')
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(lock,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':lock['status'],'file_count':lock['file_count'],'lock_sha256':H(out)},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/locks/V13_OPTIMIZER_INTERFERENCE_INPUT_LOCK_2026-08-31.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
