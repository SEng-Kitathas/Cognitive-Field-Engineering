#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, time
from collections import Counter
from pathlib import Path
from v11_predicate_policy_common import *

def verify_adapter(adapter:Path,run_manifest:Path):
    run=loadj(run_manifest)
    for rel,meta in run['adapter_files'].items():
        p=adapter/rel
        if not p.is_file() or p.stat().st_size!=meta['bytes'] or sha256_file(p)!=meta['sha256']:
            raise SystemExit(f'ADAPTER_HASH_FAILURE {p}')
    return run

def metric(rows):
    n=len(rows);c=sum(bool(r['correct']) for r in rows);return {'n':n,'correct':c,'accuracy':c/n if n else None,'json_parse_rate':sum(r['parsed'] is not None for r in rows)/n if n else None}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--task',choices=['PREDICATE','POLICY'],required=True);ap.add_argument('--adapter',type=Path,required=True);ap.add_argument('--run-manifest',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.project_root.resolve();
    if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
    a.out.mkdir(parents=True)
    verify_lock(root,a.lock);contract=loadj(a.contract);host=loadj(a.host_lock);run=verify_adapter(a.adapter,a.run_manifest)
    expected_dataset=POLICY if a.task=='POLICY' else run['dataset']
    if a.task=='PREDICATE' and run['dataset'] not in (PRED_NARROW,PRED_IDENT):raise SystemExit('PREDICATE_EVAL_WRONG_DATASET')
    if a.task=='POLICY' and run['dataset']!=POLICY:raise SystemExit('POLICY_EVAL_WRONG_DATASET')
    cases=loadjl(a.candidate/('PREDICATE_EVAL.private.jsonl' if a.task=='PREDICATE' else 'POLICY_EVAL.private.jsonl'))
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
    from peft import PeftModel
    opt=contract['optimization'];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
    tok=AutoTokenizer.from_pretrained(host['base_snapshot_path'],use_fast=False,trust_remote_code=False,local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(host['base_snapshot_path'],quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'],local_files_only=True);model=PeftModel.from_pretrained(model,str(a.adapter),is_trainable=False);model.eval();model.config.use_cache=True
    im_end=tok.convert_tokens_to_ids('<|im_end|>');eos=list(dict.fromkeys(x for x in [tok.eos_token_id,im_end] if isinstance(x,int) and x>=0));rows=[];t0=time.time();torch.cuda.reset_peak_memory_stats()
    for i,c in enumerate(cases):
        enc=tok(chatml([{'role':'user','content':c['prompt']}],gen=True),return_tensors='pt',add_special_tokens=True);enc={k:v.to('cuda') for k,v in enc.items()}
        with torch.inference_mode():out=model.generate(**enc,max_new_tokens=48,do_sample=False,use_cache=True,eos_token_id=eos if len(eos)>1 else eos[0],pad_token_id=tok.eos_token_id)
        gen=out[0,enc['input_ids'].shape[1]:];raw=tok.decode(gen,skip_special_tokens=False).strip();obj=parse_json_output(raw);rows.append({**c,'raw_output':raw,'parsed':obj,'correct':obj==c['expected']})
    dumpjl(a.out/'RESULTS.jsonl',rows);metrics={'overall':metric(rows)}
    if a.task=='PREDICATE':
        metrics['by_support']={k:metric([r for r in rows if r['support_bucket']==k]) for k in sorted({r['support_bucket'] for r in rows})}
        metrics['out_of_original_support']=metric([r for r in rows if r['margin'] not in (0,1)])
    else:
        metrics['by_action']={k:metric([r for r in rows if r['action_class']==k]) for k in sorted({r['action_class'] for r in rows})}
        metrics['by_factor']={f'{str(ov).lower()}__{mode}':metric([r for r in rows if r['overflow']==ov and r['mode']==mode]) for ov in [False,True] for mode in ['transactional','latest_state']}
    manifest={'schema':'cfe.v11.predicate-policy-eval.v1','status':'EVALUATION_EXECUTED__SCIENTIFIC_EFFECT_UNQUALIFIED','task':a.task,'dataset':run['dataset'],'seed':run['seed'],'input_lock_sha256':sha256_file(a.lock),'host_lock_sha256':sha256_file(a.host_lock),'contract_sha256':sha256_file(a.contract),'producer_run_manifest_sha256':sha256_file(a.run_manifest),'candidate_manifest_sha256':sha256_file(a.candidate/'MANIFEST.json'),'metrics':metrics,'runtime_seconds':time.time()-t0,'peak_allocated_bytes':int(torch.cuda.max_memory_allocated()),'peak_reserved_bytes':int(torch.cuda.max_memory_reserved()),'results_sha256':sha256_file(a.out/'RESULTS.jsonl'),'interpretation_ceiling':['Evaluation of a preregistered mechanism screen is descriptive until paired-seed aggregate qualification is complete.','New domain is not independent replication.']}
    dumpj(a.out/'EVAL_MANIFEST.json',manifest);print(json.dumps(manifest,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
