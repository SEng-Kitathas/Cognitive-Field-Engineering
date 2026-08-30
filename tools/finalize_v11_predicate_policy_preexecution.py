#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, py_compile
from pathlib import Path
from v11_predicate_policy_common import *

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--static',type=Path,required=True);ap.add_argument('--admission',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--repeatability',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();lock=verify_lock(root,a.lock)
    static=loadj(a.static);adm=loadj(a.admission);host=loadj(a.host_lock);rep=loadj(a.repeatability);prof=loadj(a.profile_lock);contract=loadj(a.contract);fail=[]
    def req(cond,msg):
        if not cond:fail.append(msg)
    req(static.get('status')=='PASS_CANDIDATE__BASELINE_ADMISSION_NOT_RUN__NOT_LOCKED__NOT_TRAINED','static status')
    req(adm.get('status')=='BASELINE_ADMISSION_COMPLETE__NO_NEW_TRAINED_ARM_OUTCOME','admission status');req(adm.get('predicate_screen_admitted') is True,'predicate admission');req(adm.get('policy_training_admitted') is True,'policy admission')
    req(host.get('status')=='HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING','host status');req(host.get('input_lock_sha256')==sha256_file(a.lock),'host lock binding');req(host.get('snapshot_all_files_reverified') is True,'snapshot reverify');req(host.get('runtime_tokenizer_exact_match') is True,'token replay')
    req(rep.get('status')=='REPEATABILITY_PASS','repeatability');req(prof.get('status')=='PROFILE_INHERITED_AND_REPEATABILITY_QUALIFIED','profile status');req(prof.get('input_lock_sha256')==sha256_file(a.lock),'profile input binding');req(prof.get('host_lock_sha256')==sha256_file(a.host_lock),'profile host binding');req(prof.get('repeatability_qualification_sha256')==sha256_file(a.repeatability),'profile repeat binding')
    req(contract.get('status')=='FROZEN_PRE_SCIENTIFIC_TRAINING','contract status');req(contract.get('baseline_admission_sha256')==sha256_file(a.admission),'contract admission hash');req(contract.get('preregistration_sha256')==lock['anchors']['prereg_sha256'],'contract prereg hash')
    for p in [root/'tools/train_v11_predicate_policy.py',root/'tools/evaluate_v11_predicate_policy.py',root/'tools/run_v11_predicate_policy_campaign.py']:
        try:py_compile.compile(str(p),doraise=True)
        except Exception as e:fail.append(f'compile {p.name}: {e}')
    if fail:raise SystemExit('PREEXEC_FAIL '+repr(fail))
    out={'schema':'cfe.v11.predicate-policy-preexecution.v1','status':'V11_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED','input_lock_sha256':sha256_file(a.lock),'static_qualification_sha256':sha256_file(a.static),'baseline_admission_sha256':sha256_file(a.admission),'host_lock_sha256':sha256_file(a.host_lock),'repeatability_qualification_sha256':sha256_file(a.repeatability),'profile_lock_sha256':sha256_file(a.profile_lock),'training_contract_sha256':sha256_file(a.contract),'selected_profile':prof['selected_profile'],'scientific_training_authorized':True,'authorized_datasets':[PRED_NARROW,PRED_IDENT,POLICY],'authorized_seeds':contract['seeds'],'claim_ceiling':'RUNTIME PACKAGE QUALIFIED; NO V11 MECHANISM EFFECT YET','laws':['QUALIFIED_RUNTIME != SCIENTIFIC_EFFECT','AUTHORIZED != EXECUTED','PREDICATE_RESULT != POLICY_RESULT','MECHANISM_SCREEN != GENERAL_CFE_VALIDATION']}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
    dumpj(a.out,out);print(json.dumps(out,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
