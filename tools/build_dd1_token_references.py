#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def dumpjl(p,rows):Path(p).write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def chatml(ms):return ''.join(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in ms)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--verify-source-candidate',type=Path,required=True);a=ap.parse_args();host=json.loads(a.host_lock.read_text())
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(host['base_snapshot_path'],use_fast=False,trust_remote_code=False,local_files_only=True)
 def ref(r):
  full=chatml(r['messages']);ids=tok(full,add_special_tokens=True,return_attention_mask=False)['input_ids'];mask=[0]*len(ids)
  # Mark assistant content plus im_end, matching historical CFE supervision.
  prefix_msgs=[]
  for m in r['messages']:
   if m['role']=='assistant':
    before=chatml(prefix_msgs)+"<|im_start|>assistant\n"
    through=before+m['content']+"<|im_end|>"
    a0=len(tok(before,add_special_tokens=True,return_attention_mask=False)['input_ids'])
    b0=len(tok(through,add_special_tokens=True,return_attention_mask=False)['input_ids'])
    for i in range(a0,b0):mask[i]=1
   prefix_msgs.append(m)
  return {'id':r['id'],'tokens':len(ids),'supervised_tokens':sum(mask),'input_ids':ids,'loss_mask':mask}
 # historical equivalence gate
 src=a.verify_source_candidate;oldrows=jl(src/'PREDICATE_IDENTIFYING_V12.jsonl');oldrefs=jl(src/'PREDICATE_IDENTIFYING_V12.token_reference.private.jsonl');m=[]
 for i,(r,o) in enumerate(zip(oldrows,oldrefs)):
  n=ref(r)
  if n['input_ids']!=o['input_ids'] or n['loss_mask']!=o['loss_mask']:m.append(i)
 if m:raise SystemExit('HISTORICAL_MASK_REPLAY_FAIL '+repr(m[:10]))
 print('HISTORICAL_MASK_REPLAY_PASS',len(oldrows),flush=True)
 for stem in ['IDENTIFYING_COVISIBLE','MARGIN_HOMOGENEOUS_DISPERSED']:
  rows=jl(a.candidate/(stem+'.jsonl'));refs=[ref(r) for r in rows];dumpjl(a.candidate/(stem+'.token_reference.private.jsonl'),refs);print(stem,'rows',len(refs),'tokens',sum(x['tokens'] for x in refs),'sup',sum(x['supervised_tokens'] for x in refs),'max',max(x['tokens'] for x in refs),flush=True)
if __name__=='__main__':main()
