#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, time
from collections import defaultdict
from pathlib import Path

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
def loadj(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def loadjl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def dumpj(p,o):Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def dumpjl(p,rows):Path(p).write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def chatml(messages,add_generation_prompt=False):
    s=''.join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in messages)
    if add_generation_prompt:s+='<|im_start|>assistant\n'
    return s
def canon(raw):
    raw=raw.strip()
    if '<|im_end|>' in raw:raw=raw.split('<|im_end|>',1)[0].strip()
    raw=raw.strip('`').strip()
    try:return ('json',json.loads(raw))
    except:pass
    for i,c in enumerate(raw):
        if c not in '[{':continue
        for j in range(len(raw),i,-1):
            if raw[j-1] not in ']}':continue
            try:return ('json',json.loads(raw[i:j]))
            except:pass
    return ('text',' '.join(raw.split()))
def eq(raw,expected):
    k,v=canon(raw);return k=='json' and v==expected

def verify_adapter(adapter:Path,run_manifest:Path):
    run=loadj(run_manifest)
    for rel,meta in run['adapter_files'].items():
        p=adapter/rel
        if not p.is_file() or p.stat().st_size!=meta['bytes'] or sha256_file(p)!=meta['sha256']:
            raise SystemExit(f'ADAPTER_HASH_FAILURE {p}')
    return run

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--host-lock',type=Path,required=True)
    ap.add_argument('--cases',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--label',required=True)
    ap.add_argument('--adapter',type=Path,default=None)
    ap.add_argument('--run-manifest',type=Path,default=None)
    a=ap.parse_args()
    if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
    a.out.mkdir(parents=True)
    if bool(a.adapter)!=bool(a.run_manifest):raise SystemExit('ADAPTER_AND_MANIFEST_MUST_PAIR')
    host=loadj(a.host_lock); run=verify_adapter(a.adapter,a.run_manifest) if a.adapter else None
    cases=loadjl(a.cases)
    if len(cases)!=168:raise SystemExit(('CASE_COUNT',len(cases)))
    case_sha=sha256_file(a.cases)
    # Require static manifest sibling binding.
    manp=a.cases.parent/'MANIFEST.json'; man=loadj(manp)
    if man.get('cases_sha256')!=case_sha or man.get('status')!='CANDIDATE_READY_FOR_READ_ONLY_EVALUATION':raise SystemExit('DIAGNOSTIC_MANIFEST_BINDING_FAILURE')
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig
    from peft import PeftModel
    contract=loadj(Path(r'C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION\experiments\first_screen_v09\training_contract.json'))
    opt=contract['optimization']; snap=Path(host['base_snapshot_path'])
    if not torch.cuda.is_available():raise SystemExit('CUDA_REQUIRED')
    bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16)
    tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(str(snap),quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'],local_files_only=True)
    if getattr(model.config,'_attn_implementation',opt['attention_backend'])!=opt['attention_backend']:raise RuntimeError('ATTENTION_BACKEND_MISMATCH')
    if a.adapter:model=PeftModel.from_pretrained(model,str(a.adapter),is_trainable=False)
    model.eval();model.config.use_cache=True
    im_end=tok.convert_tokens_to_ids('<|im_end|>');eos=[]
    for x in [tok.eos_token_id,im_end]:
        if isinstance(x,int) and x>=0 and x not in eos:eos.append(x)
    rows=[];t0=time.time();torch.cuda.reset_peak_memory_stats()
    for i,c in enumerate(cases):
        prompt=chatml([{'role':'user','content':c['prompt']}],add_generation_prompt=True)
        enc=tok(prompt,return_tensors='pt',add_special_tokens=True);enc={k:v.to('cuda') for k,v in enc.items()}
        with torch.inference_mode():
            out=model.generate(**enc,max_new_tokens=48,do_sample=False,use_cache=True,eos_token_id=eos if len(eos)>1 else eos[0],pad_token_id=tok.eos_token_id)
        gen=out[0,enc['input_ids'].shape[1]:];raw=tok.decode(gen,skip_special_tokens=False).strip();correct=eq(raw,c['expected'])
        rows.append({**c,'raw_output':raw,'correct':bool(correct),'prompt_tokens':int(enc['input_ids'].shape[1]),'generated_tokens':int(gen.shape[0])})
        if (i+1)%24==0:print(f'diagnostic {i+1}/{len(cases)}',flush=True)
    dumpjl(a.out/'RESULTS.jsonl',rows)
    def metric(xs):return {'n':len(xs),'correct':sum(bool(r['correct']) for r in xs),'accuracy':sum(bool(r['correct']) for r in xs)/len(xs)}
    metrics={'overall':metric(rows),'by_tier':{},'by_margin':{},'by_tier_margin':{},'by_mode':{},'support_buckets':{}}
    for tier in sorted({r['tier'] for r in rows}):metrics['by_tier'][tier]=metric([r for r in rows if r['tier']==tier])
    for m in sorted({r['margin'] for r in rows}):metrics['by_margin'][str(m)]=metric([r for r in rows if r['margin']==m])
    for tier in sorted({r['tier'] for r in rows}):
      metrics['by_tier_margin'][tier]={str(m):metric([r for r in rows if r['tier']==tier and r['margin']==m]) for m in sorted({x['margin'] for x in rows})}
    for mode in sorted({r['mode'] for r in rows}):metrics['by_mode'][mode]=metric([r for r in rows if r['mode']==mode])
    buckets={'negative_slack':lambda m:m<0,'boundary_equal':lambda m:m==0,'old_overflow_support':lambda m:m==1,'far_overflow':lambda m:m>1}
    for k,fn in buckets.items():metrics['support_buckets'][k]=metric([r for r in rows if fn(r['margin'])])
    report={'schema':'cfe.v10.bounded-latent-diagnostic-eval.v1','status':'POST_HOC_READ_ONLY_DIAGNOSTIC_COMPLETE__NOT_CONFIRMATORY','label':a.label,'cases_sha256':case_sha,'diagnostic_manifest_sha256':sha256_file(manp),'host_lock_sha256':sha256_file(a.host_lock),'base_snapshot_manifest_sha256':host['base_snapshot_manifest_sha256'],'adapter':str(a.adapter) if a.adapter else None,'producer_run_manifest_sha256':sha256_file(a.run_manifest) if a.run_manifest else None,'adapter_files':run['adapter_files'] if run else None,'attention_backend':opt['attention_backend'],'metrics':metrics,'runtime_seconds':time.time()-t0,'peak_allocated_bytes':int(torch.cuda.max_memory_allocated()),'peak_reserved_bytes':int(torch.cuda.max_memory_reserved()),'results_sha256':sha256_file(a.out/'RESULTS.jsonl'),'interpretation_ceiling':['Post-hoc diagnostic only.','Existing weights only; no training occurred.','RULE_EXPLICIT tests application with rule supplied.','BOUNDARY_LATENT removes the inequality but supplies policy.','FULL_LATENT removes both inequality and policy wording; failure may reflect task ambiguity as well as missing latent transfer.']}
    dumpj(a.out/'EVAL_MANIFEST.json',report);print(json.dumps(report,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
