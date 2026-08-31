#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,py_compile
from pathlib import Path
from v12_factor_primitive_common import verify_lock,loadj,sha256_file,dumpj

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--static',type=Path,required=True);ap.add_argument('--admission',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--repeatability',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--prereg',type=Path,required=True);ap.add_argument('--portability-seal',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();lock=verify_lock(root,a.lock)
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 static=loadj(a.static);adm=loadj(a.admission);host=loadj(a.host_lock);rep=loadj(a.repeatability);prof=loadj(a.profile_lock);contract=loadj(a.contract);pr=loadj(a.prereg);port=loadj(a.portability_seal);fail=[]
 def req(x,msg):
  if not x:fail.append(msg)
 req(lock.get('status')=='LOCKED_PRE_RUNTIME__NO_V12_SCIENTIFIC_TRAINING','input lock status')
 req(lock.get('scientific_training_authorized') is False,'input lock preauthorization false')
 req(static.get('status','').startswith('PASS'),'static qualification')
 req(adm.get('status')=='BASELINE_ADMISSION_COMPLETE__NO_V12_TRAINED_ARM_OUTCOME','baseline status')
 req(adm.get('screen_admitted') is True and adm.get('compose_benchmark_admitted') is True and adm.get('policy_direct_admitted') is True,'baseline admission gates')
 req(host.get('status')=='HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING','host status')
 req(host.get('snapshot_all_files_reverified') is True and host.get('runtime_tokenizer_exact_match') is True,'host identity/tokenizer')
 req(host.get('input_lock_sha256')==sha256_file(a.lock),'host input binding')
 req(rep.get('status')=='REPEATABILITY_PASS','repeatability')
 req(rep.get('input_lock_sha256')==sha256_file(a.lock) and rep.get('host_lock_sha256')==sha256_file(a.host_lock),'repeatability bindings')
 req(prof.get('status')=='PROFILE_INHERITED_AND_REPEATABILITY_QUALIFIED','profile status')
 req(prof.get('input_lock_sha256')==sha256_file(a.lock) and prof.get('host_lock_sha256')==sha256_file(a.host_lock),'profile bindings')
 req(prof.get('repeatability_qualification_sha256')==sha256_file(a.repeatability),'profile repeat binding')
 req(contract.get('status')=='FROZEN_PRE_SCIENTIFIC_TRAINING','contract status')
 req(contract.get('bindings',{}).get('preregistration_sha256')==sha256_file(a.prereg),'contract prereg binding')
 req(contract.get('bindings',{}).get('baseline_admission_sha256')==sha256_file(a.admission),'contract admission binding')
 req(pr.get('status')=='FROZEN_DRAFT_BEFORE_ANY_V12_MODEL_OUTCOME','prereg pre-outcome status')
 req(port.get('status')=='COMPANION_PORTABILITY_SEAL__ORIGINAL_LOCK_UNCHANGED','portability seal status')
 req(port.get('original_lock_sha256')==sha256_file(a.lock),'portability original-lock binding')
 for p in [root/'tools/train_v12_factor_primitive.py',root/'tools/evaluate_v12_factor_primitive.py',root/'tools/run_v12_factor_primitive_campaign.py']:
  try:py_compile.compile(str(p),doraise=True)
  except Exception as e:fail.append(f'compile {p.name}: {e}')
 if fail:raise SystemExit('V12_PREEXEC_FAIL '+repr(fail))
 out={'schema':'cfe.v12.factor-primitive-preexecution.v1','status':'V12_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED','scientific_training_authorized':True,'input_lock_sha256':sha256_file(a.lock),'static_qualification_sha256':sha256_file(a.static),'baseline_admission_sha256':sha256_file(a.admission),'host_lock_sha256':sha256_file(a.host_lock),'repeatability_qualification_sha256':sha256_file(a.repeatability),'profile_lock_sha256':sha256_file(a.profile_lock),'training_contract_sha256':sha256_file(a.contract),'preregistration_sha256':sha256_file(a.prereg),'portability_seal_sha256':sha256_file(a.portability_seal),'authorized_arms':['COMPOSE_NARROW_BASIS','COMPOSE_IDENTIFYING_BASIS'],'authorized_seeds':contract['seeds'],'claim_ceiling':'RUNTIME PACKAGE QUALIFIED; NO V12 COMPOSITION EFFECT YET','laws':['AUTHORIZED != EXECUTED','COMPOSITION TEST != COMPOSED-ANSWER TRAINING','NORMALIZATION_EQUIVALENT != ORIGINAL EXECUTION IDENTITY','IDENTIFYING CFE != DEVELOPMENTAL CFE']}
 a.out.parent.mkdir(parents=True,exist_ok=True);dumpj(a.out,out);print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
