#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path

def H(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def dumpj(p,o):Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def dumpjl(p,rows):Path(p).write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def chatml(ms,gen=False):
 s=''.join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in ms)
 if gen:s+='<|im_start|>assistant\n'
 return s
def parse(raw):
 raw=raw.strip()
 if '<|im_end|>' in raw:raw=raw.split('<|im_end|>',1)[0].strip()
 raw=raw.strip('`').strip()
 try:return json.loads(raw)
 except:pass
 for i,c in enumerate(raw):
  if c not in '[{':continue
  for j in range(len(raw),i,-1):
   if raw[j-1] not in ']}':continue
   try:return json.loads(raw[i:j])
   except:pass
 return None
def metric(rows):
 n=len(rows);c=sum(r['correct'] for r in rows);return {'n':n,'correct':c,'accuracy':c/n,'json_parse_rate':sum(r['parsed'] is not None for r in rows)/n}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--prereg',type=Path,required=True);ap.add_argument('--qualification',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);host=json.loads(a.host_lock.read_text());pr=json.loads(a.prereg.read_text());qual=json.loads(a.qualification.read_text())
 if qual.get('status')!='PASS_CANDIDATE__BASELINE_ADMISSION_NOT_RUN__NOT_LOCKED__NOT_TRAINED':raise SystemExit('STATIC_QUALIFICATION_REQUIRED')
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
 contract=json.loads(Path(r'C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION\experiments\first_screen_v09\training_contract.json').read_text())
 opt=contract['optimization'];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16);snap=Path(host['base_snapshot_path'])
 tok=AutoTokenizer.from_pretrained(str(snap),use_fast=False,trust_remote_code=False,local_files_only=True);model=AutoModelForCausalLM.from_pretrained(str(snap),quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'],local_files_only=True);model.eval();model.config.use_cache=True
 im_end=tok.convert_tokens_to_ids('<|im_end|>');eos=list(dict.fromkeys(x for x in [tok.eos_token_id,im_end] if isinstance(x,int) and x>=0));jobs=[('PREDICATE',a.candidate/'PREDICATE_EVAL.private.jsonl',24),('POLICY',a.candidate/'POLICY_EVAL.private.jsonl',32),('COMPOSE',a.candidate/'COMPOSE_EVAL.private.jsonl',32)];metrics={};t0=time.time()
 for name,path,maxnew in jobs:
  rows=[]
  for i,c in enumerate(jl(path)):
   enc=tok(chatml([{'role':'user','content':c['prompt']}],gen=True),return_tensors='pt',add_special_tokens=True);enc={k:v.to('cuda') for k,v in enc.items()}
   with torch.inference_mode():out=model.generate(**enc,max_new_tokens=maxnew,do_sample=False,use_cache=True,eos_token_id=eos if len(eos)>1 else eos[0],pad_token_id=tok.eos_token_id)
   gen=out[0,enc['input_ids'].shape[1]:];raw=tok.decode(gen,skip_special_tokens=False).strip();obj=parse(raw);rows.append({**c,'raw_output':raw,'parsed':obj,'correct':obj==c['expected']})
  dumpjl(a.out/(name+'_RESULTS.jsonl'),rows);m=metric(rows)
  if name=='COMPOSE':m['by_truth']={str(z).lower():metric([r for r in rows if r['condition_z']==z]) for z in [False,True]};m['by_action']={k:metric([r for r in rows if r['action_class']==k]) for k in ['action_r','action_s','action_t']}
  if name=='POLICY':m['by_action']={k:metric([r for r in rows if r['action_class']==k]) for k in ['action_r','action_s','action_t']}
  metrics[name]=m;print(name,m,flush=True)
 gates=pr['baseline_admission'];compose_ok=metrics['COMPOSE']['accuracy']<gates['reject_composed_benchmark_if_nf4_accuracy_gte'];policy_ok=metrics['POLICY']['accuracy']<gates['reject_policy_direct_if_nf4_accuracy_gte']
 decision={'schema':'cfe.v12.factor-primitive-baseline-admission.v1','status':'BASELINE_ADMISSION_COMPLETE__NO_V12_TRAINED_ARM_OUTCOME','host_lock_sha256':H(a.host_lock),'candidate_manifest_sha256':H(a.candidate/'MANIFEST.json'),'prereg_sha256':H(a.prereg),'static_qualification_sha256':H(a.qualification),'metrics':metrics,'gates':gates,'compose_benchmark_admitted':compose_ok,'policy_direct_admitted':policy_ok,'screen_admitted':compose_ok and policy_ok,'disposition':'ADMIT_V12_PREEXECUTION_QUALIFICATION' if compose_ok and policy_ok else 'REJECT_OR_REDESIGN_BEFORE_TRAINING','runtime_seconds':time.time()-t0,'results_sha256':{name:H(a.out/(name+'_RESULTS.jsonl')) for name,_,_ in jobs},'laws':['BASELINE_ADMISSION != COMPOSITION_EFFECT','OPAQUE_LABEL_HEADROOM != LEARNED_COMPOSITION','REJECTED_BENCHMARK != NEGATIVE_CFE_RESULT']};dumpj(a.out/'ADMISSION.json',decision);print(json.dumps(decision,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
