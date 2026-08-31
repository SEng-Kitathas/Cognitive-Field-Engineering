#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, py_compile
from collections import Counter
from pathlib import Path

def H(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def main(root:Path,out:Path):
 cand=root/'state/candidates/v13_optimizer_interference_20260831';src=root/'state/candidates/v12_factor_primitive_composition_20260830';pr=root/'state/next_steps/V13_OPTIMIZER_VISIBLE_PRIMITIVE_INTERFERENCE_PREREG_2026-08-31.json';man=json.loads((cand/'MANIFEST.json').read_text());fail=[];checks=[]
 def chk(cond,name,detail=None):
  checks.append({'check':name,'pass':bool(cond),'detail':detail})
  if not cond:fail.append(f'{name}: {detail}')
 chk(man.get('status')=='CANDIDATE_GENERATED__NOT_LOCKED__NOT_TRAINED','candidate_status')
 chk(man.get('v13_prereg_sha256')==H(pr),'prereg_binding')
 chk(man.get('source_v12_candidate_manifest_sha256')==H(src/'MANIFEST.json'),'v12_manifest_binding')
 for fn,meta in man['files'].items():
  cp=cand/fn;sp=src/fn;chk(cp.is_file(),f'candidate_file_{fn}');chk(sp.is_file(),f'source_file_{fn}');
  if cp.is_file() and sp.is_file():
   chk(H(cp)==H(sp)==meta['source_sha256']==meta['copied_sha256'],f'exact_copy_{fn}',(H(cp),H(sp),meta))
   chk(cp.stat().st_size==sp.stat().st_size==meta['bytes'],f'exact_bytes_{fn}')
 pred=jl(cand/'PREDICATE_IDENTIFYING_V12.token_reference.private.jsonl');pol=jl(cand/'POLICY_Z_SHARED.token_reference.private.jsonl');chk(len(pred)==72,'predicate_ref_count');chk(len(pol)==72,'policy_ref_count')
 pt=sum(x['tokens'] for x in pred);qt=sum(x['tokens'] for x in pol);ps=sum(x['supervised_tokens'] for x in pred);qs=sum(x['supervised_tokens'] for x in pol);chk(pt+qt==31200,'global_token_burden',pt+qt);chk(ps+qs==4608,'supervised_token_burden',ps+qs);chk(max(x['tokens'] for x in pred+pol)<=512,'max_seq_512',max(x['tokens'] for x in pred+pol))
 # no joint prompt in either primitive stream
 for fn in ['PREDICATE_IDENTIFYING_V12.jsonl','POLICY_Z_SHARED.jsonl']:
  rows=jl(cand/fn)
  for ix,r in enumerate(rows):
   user=' '.join(m['content'].lower() for m in r['messages'] if m['role']=='user')
   if fn.startswith('PREDICATE'):chk('mode=' not in user,f'predicate_no_mode_{ix}')
   else:chk(all(x not in user for x in ['capacity=','queued=','incoming=']),f'policy_no_numeric_{ix}')
 # schedule audits
 for seed,arms in man['schedules'].items():
  parsed={}
  for arm,meta in arms.items():
   s=[tuple(x) for x in meta['schedule']];parsed[arm]=s;chk(len(s)==144,f'{seed}_{arm}_len');chk(Counter(k for k,_ in s)==Counter({'P':72,'Q':72}),f'{seed}_{arm}_primitive_counts');chk(sorted(i for k,i in s if k=='P')==list(range(72)),f'{seed}_{arm}_pred_once');chk(sorted(i for k,i in s if k=='Q')==list(range(72)),f'{seed}_{arm}_policy_once');chk(hashlib.sha256(json.dumps(meta['schedule'],separators=(',',':')).encode()).hexdigest()==meta['sha256'],f'{seed}_{arm}_sha')
   wins=[s[w*8:(w+1)*8] for w in range(18)]
   if arm=='LOCAL_MIXED':
    chk(all(sum(k=='P' for k,_ in win)==4 and sum(k=='Q' for k,_ in win)==4 for win in wins),f'{seed}_mixed_4plus4')
   else:
    kinds=[win[0][0] if len({k for k,_ in win})==1 else 'MIXED' for win in wins];chk(all(k!='MIXED' for k in kinds),f'{seed}_separated_homogeneous');chk(Counter(kinds)==Counter({'P':9,'Q':9}),f'{seed}_separated_9plus9');chk(all(kinds[i]!=kinds[i+1] for i in range(17)),f'{seed}_separated_alternating')
  chk(Counter(parsed['LOCAL_MIXED'])==Counter(parsed['WINDOW_SEPARATED']),f'{seed}_exact_multiset_equal')
 # eval counts unchanged
 chk(len(jl(cand/'PREDICATE_EVAL.private.jsonl'))==48,'predicate_eval_48');chk(len(jl(cand/'POLICY_EVAL.private.jsonl'))==48,'policy_eval_48');chk(len(jl(cand/'COMPOSE_EVAL.private.jsonl'))==96,'compose_eval_96')
 # no v13 scientific outputs before qualification
 v13runs=root/'state/analysis/V13_OPTIMIZER_INTERFERENCE_CAMPAIGN'
 chk(not v13runs.exists(),'no_v13_scientific_run_root')
 try:py_compile.compile(str(root/'tools/audit_v13_optimizer_interference_candidate.py'),doraise=True);chk(True,'audit_script_compiles')
 except Exception as e:chk(False,'audit_script_compiles',repr(e))
 report={'schema':'cfe.v13.optimizer-interference-static-hostile.v1','status':'PASS_CANDIDATE__NOT_LOCKED__NOT_TRAINED' if not fail else 'FAIL','check_count':len(checks),'failures':fail,'bindings':{'prereg_sha256':H(pr),'candidate_manifest_sha256':H(cand/'MANIFEST.json'),'source_v12_candidate_manifest_sha256':H(src/'MANIFEST.json')},'burden':{'global_tokens':pt+qt,'supervised_tokens':ps+qs,'rows':144},'causal_difference':'accumulation-window primitive mixing only','claims_not_authorized':['optimizer interference effect','two-sided predicate competence','composition effect','Microseed transfer']}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':report['status'],'check_count':report['check_count'],'failures':fail,'bindings':report['bindings'],'burden':report['burden']},indent=2,sort_keys=True));
 if fail:raise SystemExit(2)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/qualification/V13_OPTIMIZER_INTERFERENCE_STATIC_HOSTILE_2026-08-31.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
