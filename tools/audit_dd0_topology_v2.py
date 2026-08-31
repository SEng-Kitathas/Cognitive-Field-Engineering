#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,subprocess,sys,tempfile
from collections import Counter
from pathlib import Path

def L(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--field',type=Path,required=True);ap.add_argument('--identifying',type=Path,required=True);ap.add_argument('--dispersed',type=Path,required=True);ap.add_argument('--bridged',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();src=L(a.field);A=L(a.identifying);B=L(a.dispersed);C=L(a.bridged);checks=[]
 def ck(n,v,d=None):checks.append({'check':n,'pass':bool(v),'detail':d})
 ck('multiplicity_equal_AB',A['event_multiplicity']==B['event_multiplicity'])
 ck('multiplicity_equal_AC',A['event_multiplicity']==C['event_multiplicity'])
 ck('coverage_A',all(x['satisfied'] for x in A['coverage']),A['coverage']);ck('coverage_B',all(x['satisfied'] for x in B['coverage']),B['coverage']);ck('coverage_C',all(x['satisfied'] for x in C['coverage']),C['coverage'])
 ck('identifying_more_target_covisibility',A['target_covisibility_count']>B['target_covisibility_count'],{'A':A['target_covisibility_count'],'B':B['target_covisibility_count']})
 minspan=int(src['projection'].get('min_long_range_bridge_span',2));spans=[x['max_window_span'] for x in C['bridge_metrics']];ck('bridged_has_required_long_range_span',bool(spans) and max(spans)>=minspan,{'spans':spans,'required':minspan})
 # revisit check from source multiplicity
 required=src['projection'].get('revisit_multiplicity',{});ck('revisit_multiplicity_preserved',all(int(C['event_multiplicity'].get(k,0))==int(v) for k,v in required.items()),required)
 # deterministic replay all modes
 for obj,path in [(A,a.identifying),(B,a.dispersed),(C,a.bridged)]:
  with tempfile.TemporaryDirectory() as td:
   x=Path(td)/'o.json';cp=subprocess.run([sys.executable,str(root/'tools/dd0_compile_field_v2.py'),'--field',str(a.field),'--mode',obj['mode'],'--seed',str(obj['seed']),'--out',str(x)],cwd=root,capture_output=True,text=True);ck('replay_exit_'+obj['mode'],cp.returncode==0,cp.stderr[-500:]);ck('replay_sha_'+obj['mode'],cp.returncode==0 and H(x)==H(path),{'expected':H(path),'actual':H(x) if x.exists() else None})
 out={'schema':'cfe.dd0.topology-v2-audit.v1','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'metrics':{'target_covisibility_identifying':A['target_covisibility_count'],'target_covisibility_dispersed':B['target_covisibility_count'],'bridge_spans':[x['max_window_span'] for x in C['bridge_metrics']]}}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
