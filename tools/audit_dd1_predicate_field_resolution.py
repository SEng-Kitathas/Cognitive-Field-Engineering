#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from collections import Counter
from pathlib import Path

def Ls(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def msgsig(pair):return hashlib.sha256(json.dumps(pair,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();cand=a.candidate.resolve();host=json.loads(a.host_lock.read_text())
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(host['base_snapshot_path'],local_files_only=True,trust_remote_code=False,use_fast=True)
 A=Ls(cand/'IDENTIFYING_COVISIBLE.jsonl');B=Ls(cand/'MARGIN_HOMOGENEOUS_DISPERSED.jsonl');AS=Ls(cand/'IDENTIFYING_COVISIBLE.sidecar.private.jsonl');BS=Ls(cand/'MARGIN_HOMOGENEOUS_DISPERSED.sidecar.private.jsonl');checks=[]
 def ck(n,v,d=None):checks.append({'check':n,'pass':bool(v),'detail':d})
 ck('rows_equal_72',len(A)==len(B)==72,{'A':len(A),'B':len(B)})
 def atoms(rows):
  out=[]
  for r in rows:
   m=r['messages'];ck('row_8_messages_'+r['id'],len(m)==8)
   for i in range(0,len(m),2):out.append(msgsig(m[i:i+2]))
  return Counter(out)
 aa,bb=atoms(A),atoms(B);ck('atomic_message_multiset_equal',aa==bb,{'atoms_A':sum(aa.values()),'atoms_B':sum(bb.values()),'unique':len(aa)})
 ck('sidecar_atom_ids_equal',Counter(x for r in AS for x in r['atom_ids'])==Counter(x for r in BS for x in r['atom_ids']))
 # geometry sidecar only
 ck('A_each_row_four_margins',all(sorted(r['margins'])==[-3,0,1,3] for r in AS))
 ck('B_each_row_one_margin',all(len(set(r['margins']))==1 for r in BS))
 ck('global_margin_multiset_equal',Counter(x for r in AS for x in r['margins'])==Counter(x for r in BS for x in r['margins']))
 # tokenizer: exact chat template and supervised assistant token accounting
 def metrics(rows):
  seq=[];sup=[];lens=[]
  for r in rows:
   ids=tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=False);lens.append(len(ids));seq.extend(ids)
   s=0
   for i in range(1,len(r['messages']),2):s+=len(tok(r['messages'][i]['content'],add_special_tokens=False)['input_ids'])
   sup.append(s)
  return {'total_tokens':len(seq),'sequence_lengths':lens,'supervised_tokens':sum(sup),'supervised_per_row':sup,'stream_sha256':hashlib.sha256(json.dumps(seq,separators=(',',':')).encode()).hexdigest()}
 MA,MB=metrics(A),metrics(B)
 ck('total_tokens_equal',MA['total_tokens']==MB['total_tokens'],{'A':MA['total_tokens'],'B':MB['total_tokens']})
 ck('supervised_tokens_equal',MA['supervised_tokens']==MB['supervised_tokens'],{'A':MA['supervised_tokens'],'B':MB['supervised_tokens']})
 ck('sequence_length_multiset_equal',Counter(MA['sequence_lengths'])==Counter(MB['sequence_lengths']),{'A':Counter(MA['sequence_lengths']),'B':Counter(MB['sequence_lengths'])})
 ck('streams_differ',MA['stream_sha256']!=MB['stream_sha256'],{'A':MA['stream_sha256'],'B':MB['stream_sha256']})
 # public learner rows must not contain curator terms
 forbidden=['margin','identifying','homogeneous','dispersed','source_row','atom_id','causal','bridge','coverage']
 leak=[]
 for name,rows in [('A',A),('B',B)]:
  for r in rows:
   t=json.dumps(r).lower()
   for f in forbidden:
    if f in t:leak.append((name,r['id'],f))
 ck('no_curator_label_leak',not leak,leak[:20])
 out={'schema':'cfe.dd1.predicate-field-resolution-audit.v1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','candidate_manifest_sha256':H(cand/'MANIFEST.json'),'host_lock_sha256':H(a.host_lock),'checks':checks,'metrics':{'A':MA,'B':MB},'scientific_difference':'same 288 atomic predicate experiences, same global margin/truth support, same total/supervised tokens and sequence-length multiset; only four-margin identifying co-visibility vs margin-homogeneous sequence grouping'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
