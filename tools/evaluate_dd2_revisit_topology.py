#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from dd2_revisit_topology_common import *
def metric(rows):
 n=len(rows);c=sum(bool(r['correct']) for r in rows);return {'n':n,'correct':c,'accuracy':c/n if n else None,'json_parse_rate':sum(r['parsed'] is not None for r in rows)/n if n else None}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--arm',choices=ARMS,required=True);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--adapter',type=Path,required=True);ap.add_argument('--run-manifest',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 lock=loadj(a.lock)
 for rel,m in lock['files'].items():
  p=root/rel
  if not p.is_file() or p.stat().st_size!=m['bytes'] or sha256_file(p)!=m['sha256']:raise SystemExit('LOCK_FAIL '+rel)
 c=loadj(a.contract);host=loadj(a.host_lock);run=loadj(a.run_manifest)
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
 from peft import PeftModel
 opt=c['optimization'];bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type=opt['bnb_quant_type'],bnb_4bit_use_double_quant=opt['bnb_double_quant'],bnb_4bit_compute_dtype=torch.float16);tok=AutoTokenizer.from_pretrained(host['base_snapshot_path'],use_fast=False,trust_remote_code=False,local_files_only=True);model=AutoModelForCausalLM.from_pretrained(host['base_snapshot_path'],quantization_config=bnb,device_map={'':0},trust_remote_code=False,attn_implementation=opt['attention_backend'],local_files_only=True);model=PeftModel.from_pretrained(model,str(a.adapter),is_trainable=False);model.eval();model.config.use_cache=True
 im_end=tok.convert_tokens_to_ids('<|im_end|>');eos=list(dict.fromkeys(x for x in [tok.eos_token_id,im_end] if isinstance(x,int) and x>=0));rows=[];a.out.mkdir(parents=True);t0=time.time()
 for ex in loadjl(a.candidate/'PREDICATE_EVAL.private.jsonl'):
  enc=tok(chatml([{'role':'user','content':ex['prompt']}],gen=True),return_tensors='pt',add_special_tokens=True);enc={k:v.to('cuda') for k,v in enc.items()}
  with torch.inference_mode():o=model.generate(**enc,max_new_tokens=24,do_sample=False,use_cache=True,eos_token_id=eos if len(eos)>1 else eos[0],pad_token_id=tok.eos_token_id)
  raw=tok.decode(o[0,enc['input_ids'].shape[1]:],skip_special_tokens=False).strip();obj=parse_json_output(raw);rows.append({**ex,'raw_output':raw,'parsed':obj,'correct':obj==ex['expected']})
 dumpjl(a.out/'PREDICATE_DIRECT.jsonl',rows);m={'overall':metric(rows),'by_truth':{str(z).lower():metric([r for r in rows if r['expected']['condition_z']==z]) for z in [False,True]},'by_support':{k:metric([r for r in rows if r['support_bucket']==k]) for k in sorted({r['support_bucket'] for r in rows})}};m['balanced_accuracy']=(m['by_truth']['false']['accuracy']+m['by_truth']['true']['accuracy'])/2;man={'schema':'cfe.dd2.eval.v1','status':'EVALUATION_COMPLETE__PAIR_UNQUALIFIED','arm':a.arm,'seed':a.seed,'metrics':m,'run_manifest_sha256':sha256_file(a.run_manifest),'adapter_sha256':run['adapter_files']['adapter_model.safetensors']['sha256'],'results_sha256':sha256_file(a.out/'PREDICATE_DIRECT.jsonl'),'runtime_seconds':time.time()-t0};dumpj(a.out/'EVAL_MANIFEST.json',man);print(json.dumps(man,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
