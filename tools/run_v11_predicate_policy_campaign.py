#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, time
from pathlib import Path
from v11_predicate_policy_common import *

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.project_root.resolve();contract=loadj(a.contract);pre=loadj(a.preexec);verify_lock(root,a.lock)
    if pre.get('status')!='V11_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
    a.out.mkdir(parents=True,exist_ok=True); receipt={'schema':'cfe.v11.predicate-policy-campaign.v1','status':'RUNNING','started':time.time(),'jobs':[],'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec)};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
    jobs=[]
    for seed in contract['seeds']:
        for ds in contract['predicate_execution_order'][str(seed)]:jobs.append((seed,ds,'PREDICATE'))
        jobs.append((seed,POLICY,'POLICY'))
    for ix,(seed,ds,task) in enumerate(jobs):
        rootjob=a.out/str(seed)/ds; tr=rootjob/'train'; ev=rootjob/'eval'
        if (ev/'EVAL_MANIFEST.json').exists():
            receipt['jobs'].append({'seed':seed,'dataset':ds,'task':task,'status':'ALREADY_COMPLETE','eval_manifest_sha256':sha256_file(ev/'EVAL_MANIFEST.json')});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);continue
        if tr.exists() or ev.exists():raise SystemExit(f'PARTIAL_OUTPUT_REFUSE {rootjob}')
        print('TRAIN',ix+1,len(jobs),seed,ds,flush=True)
        cmd=[sys.executable,str(root/'tools/train_v11_predicate_policy.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--dataset',ds,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(tr)]
        cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(rootjob/'train.stdout.log').parent.mkdir(parents=True,exist_ok=True);(rootjob/'train.stdout.log').write_text(cp.stdout,encoding='utf-8');(rootjob/'train.stderr.log').write_text(cp.stderr,encoding='utf-8')
        if cp.returncode!=0:receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'dataset':ds,'task':task,'status':'TRAIN_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-3000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
        print('EVAL',seed,ds,flush=True)
        cmd=[sys.executable,str(root/'tools/evaluate_v11_predicate_policy.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--task',task,'--adapter',str(tr/'adapter'),'--run-manifest',str(tr/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ev)]
        cp=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(rootjob/'eval.stdout.log').write_text(cp.stdout,encoding='utf-8');(rootjob/'eval.stderr.log').write_text(cp.stderr,encoding='utf-8')
        if cp.returncode!=0:receipt['status']='BLOCKED';receipt['jobs'].append({'seed':seed,'dataset':ds,'task':task,'status':'EVAL_FAILED','rc':cp.returncode,'stderr_tail':cp.stderr[-3000:]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(cp.returncode)
        em=loadj(ev/'EVAL_MANIFEST.json');receipt['jobs'].append({'seed':seed,'dataset':ds,'task':task,'status':'COMPLETE','run_manifest_sha256':sha256_file(tr/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ev/'EVAL_MANIFEST.json'),'metrics':em['metrics']});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
    # aggregate/dispositions
    agg={'schema':'cfe.v11.predicate-policy-aggregate.v1','status':'COMPLETE__HOSTILE_INTERPRETATION_REQUIRED','predicate':{'seeds':{}},'policy':{'seeds':{}},'dispositions':{}}
    deltas=[];out_deltas=[]
    for seed in contract['seeds']:
        em={ds:loadj(a.out/str(seed)/ds/'eval'/'EVAL_MANIFEST.json') for ds in (PRED_NARROW,PRED_IDENT)}
        n=em[PRED_NARROW]['metrics']['overall'];i=em[PRED_IDENT]['metrics']['overall'];no=em[PRED_NARROW]['metrics']['out_of_original_support'];io=em[PRED_IDENT]['metrics']['out_of_original_support']
        d=i['accuracy']-n['accuracy'];do=io['accuracy']-no['accuracy'];deltas.append(d);out_deltas.append(do);agg['predicate']['seeds'][str(seed)]={'narrow':n,'identifying':i,'delta':d,'narrow_out_of_original_support':no,'identifying_out_of_original_support':io,'out_delta':do}
        pm=loadj(a.out/str(seed)/POLICY/'eval'/'EVAL_MANIFEST.json')['metrics'];agg['policy']['seeds'][str(seed)]=pm
    pos=sum(x>0 for x in deltas);mean=sum(deltas)/len(deltas);meanout=sum(out_deltas)/len(out_deltas)
    agg['predicate']['summary']={'seed_deltas':deltas,'mean_delta':mean,'positive_seeds':pos,'mean_out_of_original_support_delta':meanout}
    policy_acc=[agg['policy']['seeds'][str(s)]['overall']['accuracy'] for s in contract['seeds']];classpool={}
    for action in ['accept_all','backpressure_or_fail_explicitly','drop_oldest_keep_latest']:
        c=sum(agg['policy']['seeds'][str(s)]['by_action'][action]['correct'] for s in contract['seeds']);n=sum(agg['policy']['seeds'][str(s)]['by_action'][action]['n'] for s in contract['seeds']);classpool[action]=c/n
    polmean=sum(policy_acc)/len(policy_acc);polhigh=sum(x>=0.90 for x in policy_acc)
    wrong_supported=mean>0 and pos>=4 and meanout>0
    policy_learn=polmean>=0.95 and polhigh>=5 and all(v>0.80 for v in classpool.values())
    agg['policy']['summary']={'seed_accuracies':policy_acc,'mean_accuracy':polmean,'seeds_gte_0_90':polhigh,'pooled_action_accuracy':classpool}
    agg['dispositions']={'H_WRONG_BASIS':'SUPPORTED' if wrong_supported else 'WEAKENED','POLICY_SEPARABILITY':'LEARNABLE' if policy_learn else 'NOT_CLEANLY_SEPARABLE','next_branch':'JOINT_IDENTIFYING_PREREG_REQUIRED' if wrong_supported and policy_learn else 'STOP_AND_REASSESS_MECHANISTIC_PICTURE'}
    dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE';receipt['completed']=time.time();receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
