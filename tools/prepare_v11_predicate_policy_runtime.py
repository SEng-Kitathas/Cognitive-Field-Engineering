#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, subprocess, sys
from pathlib import Path
from v11_predicate_policy_common import *

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--v10-run-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.project_root.resolve();verify_lock(root,a.lock)
    if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
    a.out.mkdir(parents=True)
    oldhost=loadj(a.v10_run_root/'host/HOST_LOCK.json');oldbase=loadj(a.v10_run_root/'host/base_snapshot_manifest.json');oldenv=loadj(a.v10_run_root/'host/runtime_environment.json');oldprof=loadj(a.v10_run_root/'profile/PROFILE_LOCK.json')
    snap=Path(oldhost['base_snapshot_path']);fail=[]
    for rel,meta in oldbase['files'].items():
        p=snap/rel
        if not p.is_file() or p.stat().st_size!=meta['bytes'] or sha256_file(p)!=meta['sha256']:fail.append(rel)
    if fail:raise SystemExit('BASE_SNAPSHOT_REVERIFY_FAIL '+repr(fail))
    # Critical runtime identity.
    import torch, transformers, peft, bitsandbytes, numpy
    crit={'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'torch_cuda':torch.version.cuda,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__,'numpy':numpy.__version__,'cuda_available':torch.cuda.is_available(),'gpu_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'gpu_total_memory_bytes':torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,'compute_capability':list(torch.cuda.get_device_capability(0)) if torch.cuda.is_available() else None,'executable':sys.executable}
    checks={'torch':oldenv['torch'],'torch_cuda':oldenv['torch_cuda'],'cuda_available':oldenv['cuda_available'],'gpu_name':oldenv['gpu_name'],'gpu_total_memory_bytes':oldenv['gpu_total_memory_bytes'],'compute_capability':oldenv['compute_capability']}
    for k,v in checks.items():
        if crit[k]!=v:raise SystemExit(f'CRITICAL_RUNTIME_DRIFT {k} current={crit[k]!r} old={v!r}')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True)
    replay={};mism=[]
    for name in ALL_DATASETS:
        rows=loadjl(a.candidate/(name+'.jsonl'));refs=loadjl(a.candidate/(name+'.token_reference.private.jsonl'))
        if len(rows)!=len(refs):raise SystemExit(('REF_COUNT',name,len(rows),len(refs)))
        for i,(r,ref) in enumerate(zip(rows,refs)):
            ids=tok(chatml(r['messages']),add_special_tokens=True,return_attention_mask=False)['input_ids']
            if ids!=ref['input_ids']:mism.append({'dataset':name,'row':i,'id':r['id']})
        replay[name]={'rows':len(rows),'mismatches':sum(x['dataset']==name for x in mism),'max_tokens':max(r['tokens'] for r in refs)}
    if mism:dumpj(a.out/'TOKENIZER_MISMATCHES.json',mism);raise SystemExit(('TOKENIZER_REPLAY_FAIL',len(mism)))
    oldrefdir=Path(r'C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION\pilot\first_screen_v09\token_reference_q3')
    oldmax=max(r['tokens'] for arm in ['CONTROL_STRICT_CELL_SCRAMBLE','TREATMENT_NEIGHBORHOOD'] for r in loadjl(oldrefdir/(arm+'.token_reference.private.jsonl')))
    newmax=max(v['max_tokens'] for v in replay.values())
    if newmax>oldmax:raise SystemExit(('PROFILE_INHERITANCE_LENGTH_FAIL',newmax,oldmax))
    dumpj(a.out/'RUNTIME_ENVIRONMENT_CRITICAL.json',crit)
    host={'schema':'cfe.v11.predicate-policy-host-lock.v1','status':'HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING','input_lock_sha256':sha256_file(a.lock),'inherited_v10_host_lock_sha256':sha256_file(a.v10_run_root/'host/HOST_LOCK.json'),'base_snapshot_manifest_sha256':sha256_file(a.v10_run_root/'host/base_snapshot_manifest.json'),'base_snapshot_path':str(snap),'hf_repo':oldhost['hf_repo'],'hf_revision':oldhost['hf_revision'],'snapshot_file_count':len(oldbase['files']),'snapshot_all_files_reverified':True,'runtime_critical':crit,'tokenizer_replay':replay,'runtime_tokenizer_exact_match':True,'old_qualified_max_tokens':oldmax,'new_max_tokens':newmax,'profile_inheritance_length_gate':newmax<=oldmax,'inherited_selected_profile':oldprof['selected_profile'],'old_profile_lock_sha256':sha256_file(a.v10_run_root/'profile/PROFILE_LOCK.json'),'laws':['SAME_MODEL_ID != SAME_BYTES','OLD_PROFILE_FIT != NEW_LOCK_REPEATABILITY','SHORTER_SEQUENCE_SUPPORTS_FIT_INHERITANCE_ONLY_WITH_SAME_RUNTIME_AND_PROFILE']}
    dumpj(a.out/'HOST_LOCK.json',host);print(json.dumps(host,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
