#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, platform, sys
from pathlib import Path
from v12_factor_primitive_common import *

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--v10-run-root',type=Path,required=True);ap.add_argument('--v11-host-lock',type=Path,required=True);ap.add_argument('--v11-profile-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock)
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);v11h=loadj(a.v11_host_lock);v11p=loadj(a.v11_profile_lock);oldbase=loadj(a.v10_run_root/'host/base_snapshot_manifest.json');snap=Path(v11h['base_snapshot_path']);fail=[]
 for rel,meta in oldbase['files'].items():
  p=snap/rel
  if not p.is_file() or p.stat().st_size!=meta['bytes'] or sha256_file(p)!=meta['sha256']:fail.append(rel)
 if fail:raise SystemExit('BASE_SNAPSHOT_REVERIFY_FAIL '+repr(fail))
 import torch,transformers,peft,bitsandbytes,numpy
 crit={'python':sys.version,'platform':platform.platform(),'torch':torch.__version__,'torch_cuda':torch.version.cuda,'transformers':transformers.__version__,'peft':peft.__version__,'bitsandbytes':bitsandbytes.__version__,'numpy':numpy.__version__,'cuda_available':torch.cuda.is_available(),'gpu_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'gpu_total_memory_bytes':torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,'compute_capability':list(torch.cuda.get_device_capability(0)) if torch.cuda.is_available() else None,'executable':sys.executable}
 for k in ['torch','torch_cuda','transformers','peft','bitsandbytes','numpy','cuda_available','gpu_name','gpu_total_memory_bytes','compute_capability']:
  if crit[k]!=v11h['runtime_critical'][k]:raise SystemExit(f'CRITICAL_RUNTIME_DRIFT {k} current={crit[k]!r} v11={v11h["runtime_critical"][k]!r}')
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True);replay={};mism=[]
 for name in ['PREDICATE_NARROW_V12','PREDICATE_IDENTIFYING_V12','POLICY_Z_SHARED']:
  rows=loadjl(a.candidate/(name+'.jsonl'));refs=loadjl(a.candidate/(name+'.token_reference.private.jsonl'))
  if len(rows)!=len(refs):raise SystemExit(('REFCOUNT',name))
  for i,(r,ref) in enumerate(zip(rows,refs)):
   ids=tok(chatml(r['messages']),add_special_tokens=True,return_attention_mask=False)['input_ids']
   if ids!=ref['input_ids']:mism.append({'dataset':name,'row':i,'id':r['id']})
  replay[name]={'rows':len(rows),'mismatches':sum(x['dataset']==name for x in mism),'max_tokens':max(r['tokens'] for r in refs)}
 if mism:dumpj(a.out/'TOKENIZER_MISMATCHES.json',mism);raise SystemExit(('TOKENIZER_REPLAY_FAIL',len(mism)))
 newmax=max(v['max_tokens'] for v in replay.values());oldmax=int(v11h['new_max_tokens'])
 if newmax>oldmax:raise SystemExit(('PROFILE_LENGTH_INHERIT_FAIL',newmax,oldmax))
 host={'schema':'cfe.v12.factor-primitive-host-lock.v1','status':'HOST_REVERIFIED__TOKENIZER_REPLAY_PASS__PROFILE_REPEATABILITY_PENDING','input_lock_sha256':sha256_file(a.lock),'base_snapshot_manifest_sha256':v11h['base_snapshot_manifest_sha256'],'base_snapshot_path':str(snap),'hf_repo':v11h['hf_repo'],'hf_revision':v11h['hf_revision'],'snapshot_file_count':len(oldbase['files']),'snapshot_all_files_reverified':True,'runtime_critical':crit,'v11_host_lock_sha256':sha256_file(a.v11_host_lock),'runtime_tokenizer_exact_match':True,'tokenizer_replay':replay,'v11_qualified_max_tokens':oldmax,'v12_max_tokens':newmax,'profile_inheritance_length_gate':newmax<=oldmax,'inherited_selected_profile':v11p['selected_profile'],'v11_profile_lock_sha256':sha256_file(a.v11_profile_lock),'laws':['SAME_SOURCE != SAME_EXECUTABLE_ENVIRONMENT','OLD_PROFILE_FIT != NEW_LOCK_REPEATABILITY','TOKEN_REFERENCE_PRESENT != LIVE_TOKENIZER_MATCH']};dumpj(a.out/'HOST_LOCK.json',host);dumpj(a.out/'RUNTIME_ENVIRONMENT_CRITICAL.json',crit);print(json.dumps(host,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
