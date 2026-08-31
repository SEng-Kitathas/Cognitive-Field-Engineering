#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter
from pathlib import Path

def L(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def HS(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode('utf-8')).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--identifying',type=Path,required=True);ap.add_argument('--dispersed',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--separator',default='\n<DD0_EVENT_BOUNDARY>\n');a=ap.parse_args()
 host=L(a.host_lock);A=L(a.identifying);B=L(a.dispersed)
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(host['base_snapshot_path'],local_files_only=True,trust_remote_code=False,use_fast=True)
 checks=[]
 def ck(n,v,d=None):checks.append({'check':n,'pass':bool(v),'detail':d})
 def event_token_records(C):
  rows=[]
  for ep in C['episodes']:
   for e in ep['events']:
    ids=tok(e['payload'],add_special_tokens=False)['input_ids'];rows.append({'id':e['id'],'payload_sha256':e['payload_sha256'],'token_ids':ids,'token_sha256':HS(ids),'tokens':len(ids)})
  return rows
 RA,RB=event_token_records(A),event_token_records(B)
 sigA=Counter((r['id'],r['payload_sha256'],r['token_sha256'],r['tokens']) for r in RA);sigB=Counter((r['id'],r['payload_sha256'],r['token_sha256'],r['tokens']) for r in RB)
 ck('per_event_token_multiset_equal',sigA==sigB,{'events_A':len(RA),'events_B':len(RB),'total_event_tokens_A':sum(r['tokens'] for r in RA),'total_event_tokens_B':sum(r['tokens'] for r in RB)})
 ck('event_payload_sha_multiset_equal',Counter(r['payload_sha256'] for r in RA)==Counter(r['payload_sha256'] for r in RB))
 def compiled(C):
  windows=[];flat=[]
  for ep in C['episodes']:
   s=a.separator.join(e['payload'] for e in ep['events']);ids=tok(s,add_special_tokens=False)['input_ids'];windows.append({'window_index':ep['window_index'],'tokens':len(ids),'sha256':HS(ids)});flat.extend(ids)
  return windows,flat
 WA,FA=compiled(A);WB,FB=compiled(B)
 ck('window_count_equal',len(WA)==len(WB),{'A':len(WA),'B':len(WB)})
 ck('compiled_total_tokens_reported',True,{'identifying':len(FA),'dispersed':len(FB),'delta':len(FA)-len(FB)})
 # We deliberately do NOT require full stream equality; that would erase the intervention.
 out={'schema':'cfe.dd0.token-exposure-audit.v1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','host_lock_sha256':H(a.host_lock),'tokenizer_snapshot':host['base_snapshot_path'],'tokenizer_repo':host.get('hf_repo'),'tokenizer_revision':host.get('hf_revision'),'identifying_sha256':H(a.identifying),'dispersed_sha256':H(a.dispersed),'separator':a.separator,'checks':checks,'metrics':{'per_event_total_tokens_identifying':sum(r['tokens'] for r in RA),'per_event_total_tokens_dispersed':sum(r['tokens'] for r in RB),'compiled_full_sequence_tokens_identifying':len(FA),'compiled_full_sequence_tokens_dispersed':len(FB),'compiled_full_sequence_token_delta':len(FA)-len(FB),'compiled_stream_sha256_identifying':HS(FA),'compiled_stream_sha256_dispersed':HS(FB),'compiled_streams_identical':FA==FB,'window_token_counts_identifying':[x['tokens'] for x in WA],'window_token_counts_dispersed':[x['tokens'] for x in WB]},'interpretation_ceiling':'Token audit only. Equal per-event tokenized content does not imply equal compiled sequence, and unequal compiled sequence does not by itself establish learner-visible causal geometry.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
