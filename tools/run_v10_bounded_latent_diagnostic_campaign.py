#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, time, hashlib
from pathlib import Path

SEEDS=['2026082501','2026082502','2026082503','2026082504','2026082505','2026082506']
ARMS=['CONTROL_STRICT_CELL_SCRAMBLE','TREATMENT_NEIGHBORHOOD']

def loadj(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dumpj(p,o):Path(p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--live-root',type=Path,required=True);ap.add_argument('--run-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 root=a.project_root.resolve(); out=a.out.resolve(); out.mkdir(parents=True,exist_ok=True)
 cases=root/'state/candidates/v10_bounded_latent_diagnostic_20260830/CASES.jsonl'; host=a.run_root/'host/HOST_LOCK.json'; ev=root/'tools/evaluate_v10_bounded_latent_diagnostic.py'
 jobs=[{'label':'NF4_BASE','adapter':None,'manifest':None}]
 for seed in SEEDS:
  for arm in ARMS:
   tr=a.run_root/'train'/seed/arm
   jobs.append({'label':f'{seed}__{arm}','adapter':tr/'adapter','manifest':tr/'RUN_MANIFEST.json'})
 receipt={'schema':'cfe.v10.bounded-latent-diagnostic-campaign.v1','status':'RUNNING','started':time.time(),'cases_sha256':sha(cases),'jobs':[],'laws':['READ_ONLY_DIAGNOSTIC != SCIENTIFIC_TRAINING','PARTIAL_JOB_SUCCESS != CAMPAIGN_SUCCESS','POST_HOC_DIAGNOSTIC != CONFIRMATION']}
 dumpj(out/'CAMPAIGN_RECEIPT.json',receipt)
 for ix,j in enumerate(jobs):
  od=out/j['label']
  if (od/'EVAL_MANIFEST.json').exists():
   m=loadj(od/'EVAL_MANIFEST.json');receipt['jobs'].append({'label':j['label'],'status':'ALREADY_COMPLETE','eval_manifest_sha256':sha(od/'EVAL_MANIFEST.json'),'results_sha256':m['results_sha256']});dumpj(out/'CAMPAIGN_RECEIPT.json',receipt);continue
  if od.exists(): raise SystemExit(f'PARTIAL_OUTPUT_REFUSE {od}')
  cmd=[sys.executable,str(ev),'--host-lock',str(host),'--cases',str(cases),'--out',str(od),'--label',j['label']]
  if j['adapter'] is not None:cmd += ['--adapter',str(j['adapter']),'--run-manifest',str(j['manifest'])]
  print('START',ix+1,len(jobs),j['label'],flush=True)
  t=time.time();cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace')
  (out/f'{j["label"]}.stdout.log').write_text(cp.stdout,encoding='utf-8',newline='\n');(out/f'{j["label"]}.stderr.log').write_text(cp.stderr,encoding='utf-8',newline='\n')
  if cp.returncode!=0:
   receipt['status']='BLOCKED';receipt['jobs'].append({'label':j['label'],'status':'FAILED','returncode':cp.returncode,'seconds':time.time()-t,'stderr_tail':cp.stderr[-3000:]});dumpj(out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
  m=loadj(od/'EVAL_MANIFEST.json');receipt['jobs'].append({'label':j['label'],'status':'COMPLETE','seconds':time.time()-t,'eval_manifest_sha256':sha(od/'EVAL_MANIFEST.json'),'results_sha256':m['results_sha256'],'metrics':m['metrics']});dumpj(out/'CAMPAIGN_RECEIPT.json',receipt);print('DONE',j['label'],m['metrics']['by_tier'],flush=True)
 # aggregate paired treatment-control deltas
 agg={'schema':'cfe.v10.bounded-latent-diagnostic-aggregate.v1','status':'POST_HOC_READ_ONLY_DIAGNOSTIC_COMPLETE__NOT_CONFIRMATORY','cases_sha256':sha(cases),'seed_pairs':{},'tier_summary':{}}
 for seed in SEEDS:
  ms={arm:loadj(out/f'{seed}__{arm}'/'EVAL_MANIFEST.json') for arm in ARMS}
  sr={}
  for tier in ['RULE_EXPLICIT','BOUNDARY_LATENT','FULL_LATENT']:
   c=ms[ARMS[0]]['metrics']['by_tier'][tier];t=ms[ARMS[1]]['metrics']['by_tier'][tier]
   sr[tier]={'control_correct':c['correct'],'treatment_correct':t['correct'],'delta_correct_T_minus_C':t['correct']-c['correct'],'control_accuracy':c['accuracy'],'treatment_accuracy':t['accuracy'],'delta_accuracy_T_minus_C':t['accuracy']-c['accuracy']}
  for bucket in ['negative_slack','boundary_equal','old_overflow_support','far_overflow']:
   c=ms[ARMS[0]]['metrics']['support_buckets'][bucket];t=ms[ARMS[1]]['metrics']['support_buckets'][bucket]
   sr['support__'+bucket]={'control_correct':c['correct'],'treatment_correct':t['correct'],'delta_correct_T_minus_C':t['correct']-c['correct'],'control_accuracy':c['accuracy'],'treatment_accuracy':t['accuracy'],'delta_accuracy_T_minus_C':t['accuracy']-c['accuracy']}
  agg['seed_pairs'][seed]=sr
 for tier in ['RULE_EXPLICIT','BOUNDARY_LATENT','FULL_LATENT']:
  ds=[agg['seed_pairs'][s][tier]['delta_accuracy_T_minus_C'] for s in SEEDS]
  agg['tier_summary'][tier]={'seed_deltas':ds,'mean_delta_accuracy_T_minus_C':sum(ds)/len(ds),'positive':sum(x>0 for x in ds),'negative':sum(x<0 for x in ds),'zero':sum(x==0 for x in ds)}
 dumpj(out/'AGGREGATE.json',agg)
 receipt['status']='COMPLETE';receipt['completed']=time.time();receipt['aggregate_sha256']=sha(out/'AGGREGATE.json');dumpj(out/'CAMPAIGN_RECEIPT.json',receipt)
 print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
