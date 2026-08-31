#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, time
from pathlib import Path
from v13_optimizer_interference_common import *

def pooled(runroot:Path,seeds,arm,readout,slice_name):
 c=n=0
 for seed in seeds:
  m=loadj(runroot/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics'][readout]['by_truth'][slice_name];c+=m['correct'];n+=m['n']
 return {'correct':c,'n':n,'accuracy':c/n}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();contract=loadj(a.contract);verify_lock(root,a.lock);pre=loadj(a.preexec)
 if pre.get('status')!='V13_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
 if a.out.exists():raise SystemExit('REFUSE_EXISTING_CAMPAIGN_ROOT')
 a.out.mkdir(parents=True);receipt={'schema':'cfe.v13.optimizer-interference-campaign.v1','status':'RUNNING','started':time.time(),'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec),'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 jobs=[(seed,arm) for seed in contract['seeds'] for arm in contract['execution_order'][str(seed)]]
 for ix,(seed,arm) in enumerate(jobs):
  job=a.out/str(seed)/arm;tr=job/'train';ev=job/'eval'
  print('TRAIN',ix+1,len(jobs),seed,arm,flush=True)
  cmd=[sys.executable,str(root/'tools/train_v13_optimizer_interference.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(tr)];cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');job.mkdir(parents=True,exist_ok=True);(job/'train.stdout.log').write_text(cp.stdout,encoding='utf-8');(job/'train.stderr.log').write_text(cp.stderr,encoding='utf-8')
  if cp.returncode!=0:
   receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'arm':arm,'status':'TRAIN_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-5000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
  print('EVAL',seed,arm,flush=True)
  cmd=[sys.executable,str(root/'tools/evaluate_v13_optimizer_interference.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--adapter',str(tr/'adapter'),'--run-manifest',str(tr/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ev)];cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(job/'eval.stdout.log').write_text(cp.stdout,encoding='utf-8');(job/'eval.stderr.log').write_text(cp.stderr,encoding='utf-8')
  if cp.returncode!=0:
   receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'arm':arm,'status':'EVAL_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-5000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
  em=loadj(ev/'EVAL_MANIFEST.json');receipt['jobs'].append({'seed':seed,'arm':arm,'status':'COMPLETE','run_manifest_sha256':sha256_file(tr/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ev/'EVAL_MANIFEST.json'),'predicate_balanced_accuracy':em['metrics']['PREDICATE_DIRECT']['balanced_accuracy'],'predicate_accuracy':em['metrics']['PREDICATE_DIRECT']['overall']['accuracy'],'policy_accuracy':em['metrics']['POLICY_DIRECT']['overall']['accuracy'],'composed_accuracy':em['metrics']['COMPOSED_ACTION_PRIMARY']['overall']['accuracy']});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 seeds=contract['seeds'];agg={'schema':'cfe.v13.optimizer-interference-aggregate.v1','status':'COMPLETE__HOSTILE_INTERPRETATION_REQUIRED','seeds':{},'summary':{},'dispositions':{}}
 pd=[];cd=[];pwins=0;cwins=0
 for seed in seeds:
  mm={arm:loadj(a.out/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics'] for arm in ARMS};mix=mm[ARM_MIXED];sep=mm[ARM_SEPARATED];pdelta=sep['PREDICATE_DIRECT']['balanced_accuracy']-mix['PREDICATE_DIRECT']['balanced_accuracy'];cdelta=sep['COMPOSED_ACTION_PRIMARY']['overall']['accuracy']-mix['COMPOSED_ACTION_PRIMARY']['overall']['accuracy'];pd.append(pdelta);cd.append(cdelta);pwins+=pdelta>0;cwins+=cdelta>0;agg['seeds'][str(seed)]={'LOCAL_MIXED':mix,'WINDOW_SEPARATED':sep,'predicate_balanced_delta':pdelta,'compose_delta':cdelta}
 pred_truth={arm:{z:pooled(a.out,seeds,arm,'PREDICATE_DIRECT',z) for z in ['false','true']} for arm in ARMS};comp_truth={arm:{z:pooled(a.out,seeds,arm,'COMPOSED_ACTION_PRIMARY',z) for z in ['false','true']} for arm in ARMS}
 policy={arm:{'seed_accuracies':[loadj(a.out/str(seed)/arm/'eval'/'EVAL_MANIFEST.json')['metrics']['POLICY_DIRECT']['overall']['accuracy'] for seed in seeds]} for arm in ARMS}
 for arm in ARMS:policy[arm]['mean_accuracy']=sum(policy[arm]['seed_accuracies'])/len(seeds)
 sep_pred_ba=[loadj(a.out/str(seed)/ARM_SEPARATED/'eval'/'EVAL_MANIFEST.json')['metrics']['PREDICATE_DIRECT']['balanced_accuracy'] for seed in seeds];sep_pred_over=[loadj(a.out/str(seed)/ARM_SEPARATED/'eval'/'EVAL_MANIFEST.json')['metrics']['PREDICATE_DIRECT']['overall']['accuracy'] for seed in seeds];sep_false=[loadj(a.out/str(seed)/ARM_SEPARATED/'eval'/'EVAL_MANIFEST.json')['metrics']['PREDICATE_DIRECT']['by_truth']['false']['accuracy'] for seed in seeds];sep_true=[loadj(a.out/str(seed)/ARM_SEPARATED/'eval'/'EVAL_MANIFEST.json')['metrics']['PREDICATE_DIRECT']['by_truth']['true']['accuracy'] for seed in seeds]
 mean_pd=sum(pd)/len(pd);mean_cd=sum(cd)/len(cd);pf_delta=pred_truth[ARM_SEPARATED]['false']['accuracy']-pred_truth[ARM_MIXED]['false']['accuracy'];pt_delta=pred_truth[ARM_SEPARATED]['true']['accuracy']-pred_truth[ARM_MIXED]['true']['accuracy'];cf_delta=comp_truth[ARM_SEPARATED]['false']['accuracy']-comp_truth[ARM_MIXED]['false']['accuracy'];ct_delta=comp_truth[ARM_SEPARATED]['true']['accuracy']-comp_truth[ARM_MIXED]['true']['accuracy'];policy_gate=all(policy[a]['mean_accuracy']>=0.95 for a in ARMS)
 local_supported=mean_pd>0 and pwins>=4 and pf_delta>=0 and pt_delta>=0 and policy_gate
 local_weakened=mean_pd<=0 or pwins<4 or ((pf_delta>0 and pt_delta<0) or (pt_delta>0 and pf_delta<0))
 competence=(sum(sep_pred_ba)/6)>=0.75 and sum(x>=0.65 for x in sep_false)>=4 and sum(x>=0.65 for x in sep_true)>=4 and sum(x>=0.75 for x in sep_pred_over)>=4
 comp_supported=local_supported and mean_cd>0 and cwins>=4 and cf_delta>=0 and ct_delta>=0
 helped_no_comp=local_supported and (mean_cd<=0 or cwins<4)
 agg['summary']={'predicate_balanced_seed_deltas':pd,'predicate_balanced_mean_delta':mean_pd,'predicate_balanced_positive_seeds':pwins,'predicate_truth_pooled':pred_truth,'predicate_truth_deltas_separated_minus_mixed':{'false':pf_delta,'true':pt_delta},'policy_direct':policy,'separated_predicate_seed_balanced_accuracies':sep_pred_ba,'separated_predicate_seed_overall_accuracies':sep_pred_over,'separated_predicate_seed_false_accuracies':sep_false,'separated_predicate_seed_true_accuracies':sep_true,'composed_seed_deltas':cd,'composed_mean_delta':mean_cd,'composed_positive_seeds':cwins,'composed_truth_pooled':comp_truth,'composed_truth_deltas_separated_minus_mixed':{'false':cf_delta,'true':ct_delta}}
 agg['dispositions']={'LOCAL_INTERFERENCE_SUPPORTED':local_supported,'LOCAL_INTERFERENCE_WEAKENED':local_weakened,'TWO_SIDED_PREDICATE_COMPETENCE_EARNED':competence,'INTERFERENCE_HELPED_BUT_COMPOSITION_DID_NOT':helped_no_comp,'INTERFERENCE_AND_COMPOSITION_SUPPORTED':comp_supported,'next_branch':'HOSTILE_INTERPRETATION_REQUIRED'}
 dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE';receipt['completed']=time.time();receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
