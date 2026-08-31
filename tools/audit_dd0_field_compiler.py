#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path

def L(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pairkey(a,b):return tuple(sorted((a,b)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--field',type=Path,required=True);ap.add_argument('--identifying',type=Path,required=True);ap.add_argument('--dispersed',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();src=L(a.field);A=L(a.identifying);B=L(a.dispersed)
 checks=[]
 def ck(name,v,detail=None):checks.append({'check':name,'pass':bool(v),'detail':detail})
 ck('event_multiset_equal',Counter(A['event_multiset'])==Counter(B['event_multiset']))
 ck('payload_multiset_equal',Counter(A['payload_sha256_multiset'])==Counter(B['payload_sha256_multiset']))
 ck('window_size_equal',A['window_size']==B['window_size'])
 # no sidecar metadata leakage
 forbidden=set(src.get('learner_forbidden_literals',[]));texts=[]
 for C in [A,B]:
  for ep in C['episodes']:
   texts.extend(e['payload'] for e in ep['events'])
 leaked=sorted(x for x in forbidden if any(x in t for t in texts));ck('no_forbidden_literal_leak',not leaked,leaked)
 targets=set(src['projection']['target_relation_types']);pairs={pairkey(r['source'],r['target']) for r in src['relations'] if r['type'] in targets}
 def cov(C):
  c=0
  for ep in C['episodes']:
   s={e['id'] for e in ep['events']};c+=sum(1 for p,q in pairs if p in s and q in s)
  return c
 ca,cb=cov(A),cov(B);ck('identifying_has_more_target_covisibility',ca>cb,{'identifying':ca,'dispersed':cb})
 # replay determinism for each output mode
 for C,path in [(A,a.identifying),(B,a.dispersed)]:
  with tempfile.TemporaryDirectory() as td:
   q=Path(td)/'x.json';cmd=[sys.executable,str(root/'tools/dd0_compile_field.py'),'--field',str(a.field),'--mode',C['mode'],'--seed',str(C['seed']),'--out',str(q)];cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
   ck('replay_exit_'+C['mode'],cp.returncode==0,cp.stderr[-1000:]);ck('replay_sha_'+C['mode'],cp.returncode==0 and H(q)==H(path),{'expected':H(path),'actual':H(q) if q.exists() else None})
 out={'schema':'cfe.dd0.field-compiler-audit.v1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','field_sha256':H(a.field),'identifying_sha256':H(a.identifying),'dispersed_sha256':H(a.dispersed),'checks':checks,'metrics':{'target_covisibility_identifying':ca,'target_covisibility_dispersed':cb}}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
