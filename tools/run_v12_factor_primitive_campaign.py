#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, time
from pathlib import Path
from v12_factor_primitive_common import *

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();contract=loadj(a.contract);verify_lock(root,a.lock);pre=loadj(a.preexec)
 if pre.get('status')!='V12_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
 a.out.mkdir(parents=True,exist_ok=True);receipt={'schema':'cfe.v12.factor-primitive-campaign.v1','status':'RUNNING','started':time.time(),'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec),'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 jobs=[(seed,arm) for seed in contract['seeds'] for arm in contract['execution_order'][str(seed)]]
 for ix,(seed,arm) in enumerate(jobs):
  job=a.out/str(seed)/arm;tr=job/'train';ev=job/'eval'
  if (ev/'EVAL_MANIFEST.json').exists():
   receipt['jobs'].append({'seed':seed,'arm':arm,'status':'ALREADY_COMPLETE','eval_manifest_sha256':sha256_file(ev/'EVAL_MANIFEST.json')});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);continue
  if tr.exists() or ev.exists():raise SystemExit(f'PARTIAL_OUTPUT_REFUSE {job}')
  print('TRAIN',ix+1,len(jobs),seed,arm,flush=True);cmd=[sys.executable,str(root/'tools/train_v12_factor_primitive.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(tr)];cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');job.mkdir(parents=True,exist_ok=True);(job/'train.stdout.log').write_text(cp.stdout,encoding='utf-8');(job/'train.stderr.log').write_text(cp.stderr,encoding='utf-8')
  if cp.returncode!=0:receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'arm':arm,'status':'TRAIN_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-4000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
  print('EVAL',seed,arm,flush=True);cmd=[sys.executable,str(root/'tools/evaluate_v12_factor_primitive.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--adapter',str(tr/'adapter'),'--run-manifest',str(tr/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ev)];cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(job/'eval.stdout.log').write_text(cp.stdout,encoding='utf-8');(job/'eval.stderr.log').write_text(cp.stderr,encoding='utf-8')
  if cp.returncode!=0:receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'arm':arm,'status':'EVAL_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-4000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
  em=loadj(ev/'EVAL_MANIFEST.json');receipt['jobs'].append({'seed':seed,'arm':arm,'status':'COMPLETE','run_manifest_sha256':sha256_file(tr/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ev/'EVAL_MANIFEST.json'),'metrics':em['metrics']});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 # aggregate
 agg={'schema':'cfe.v12.factor-primitive-aggregate.v1','status':'COMPLETE__HOSTILE_INTERPRETATION_REQUIRED','seeds':{},'summary':{},'dispositions':{}}
 comp_d=[];pred_d=[]
 for seed in contract['seeds']:
  ms={arm:loadj(a.out/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics'] for arm in ARMS};n=ms[ARM_NARROW];i=ms[ARM_IDENT];cd=i['COMPOSED_ACTION_PRIMARY']['overall']['accuracy']-n['COMPOSED_ACTION_PRIMARY']['overall']['accuracy'];pd=i['PREDICATE_DIRECT']['overall']['accuracy']-n['PREDICATE_DIRECT']['overall']['accuracy'];comp_d.append(cd);pred_d.append(pd);agg['seeds'][str(seed)]={'narrow':n,'identifying':i,'compose_delta':cd,'predicate_delta':pd}
 # pooled truth sides composed and policy direct arm summaries
 truth={};policy={}
 for arm in ARMS:
  truth[arm]={};policy_acc=[]
  for z in ['false','true']:
   c=ncount=0
   for seed in contract['seeds']:
    m=loadj(a.out/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics']['COMPOSED_ACTION_PRIMARY']['by_truth'][z];c+=m['correct'];ncount+=m['n']
   truth[arm][z]={'correct':c,'n':ncount,'accuracy':c/ncount}
  for seed in contract['seeds']:policy_acc.append(loadj(a.out/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics']['POLICY_DIRECT']['overall']['accuracy'])
  policy[arm]={'seed_accuracies':policy_acc,'mean_accuracy':sum(policy_acc)/len(policy_acc)}
 meancomp=sum(comp_d)/6;meanpred=sum(pred_d)/6;wins=sum(x>0 for x in comp_d);false_delta=truth[ARM_IDENT]['false']['accuracy']-truth[ARM_NARROW]['false']['accuracy'];true_delta=truth[ARM_IDENT]['true']['accuracy']-truth[ARM_NARROW]['true']['accuracy'];policy_gate=all(policy[a]['mean_accuracy']>=0.95 for a in ARMS);supported=meancomp>0 and wins>=4 and false_delta>0 and true_delta>0 and policy_gate and meanpred>0
 agg['summary']={'compose_seed_deltas':comp_d,'compose_mean_delta':meancomp,'compose_positive_seeds':wins,'predicate_seed_deltas':pred_d,'predicate_mean_delta':meanpred,'composed_truth_pooled':truth,'composed_truth_deltas_identifying_minus_narrow':{'false':false_delta,'true':true_delta},'policy_direct':policy}
 agg['dispositions']={'COMPOSITION_BASIS':'SUPPORTED' if supported else 'NOT_SUPPORTED','manual_hostile_review_required_for':'COMPOSITION_PRESENT_BUT_PREDICATE_UNRESOLVED','next_branch':'HOSTILE_INTERPRETATION_BEFORE_ANY_NEW_SCREEN'};dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE';receipt['completed']=time.time();receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
