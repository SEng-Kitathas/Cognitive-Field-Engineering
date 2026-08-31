#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,subprocess,sys,time,shutil
from pathlib import Path
SEEDS=[2026083111,2026083112,2026083113,2026083114,2026083115,2026083116]
HORIZONS=['H1','H2','H4']
def H(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def J(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def L(p):return json.loads(Path(p).read_text())
def verify_adapter_from_run(root,run,seed,h):
 ck=run['checkpoints'][h]; ad=root/str(seed)/'train'/'checkpoints'/h/'adapter'
 for rel,m in ck['adapter_files'].items():
  p=ad/rel
  if not p.is_file() or p.stat().st_size!=m['bytes'] or H(p)!=m['sha256']:raise SystemExit(f'ADAPTER_VERIFY_FAIL {seed} {h} {rel}')
 return ad
def extract_eval(ev):
 em=L(ev/'EVAL_MANIFEST.json');m=em['metrics']['PREDICATE_DIRECT']
 return {'eval_manifest_sha256':H(ev/'EVAL_MANIFEST.json'),'balanced_accuracy':m['balanced_accuracy'],'overall_accuracy':m['overall']['accuracy'],'false_accuracy':m['by_truth']['false']['accuracy'],'true_accuracy':m['by_truth']['true']['accuracy']}
def run_eval(py,root,candidate,contract,lock,host,seed,h,adapter,run_manifest,out):
 if out.exists():shutil.rmtree(out)
 cmd=[py,str(root/'tools/evaluate_v14_predicate_horizon.py'),'--project-root',str(root),'--candidate',str(candidate),'--seed',str(seed),'--horizon',h,'--adapter',str(adapter),'--run-manifest',str(run_manifest),'--contract',str(contract),'--lock',str(lock),'--host-lock',str(host),'--out',str(out)]
 ep=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(out.parent/f'{h}.stdout.log').write_text(ep.stdout,encoding='utf-8');(out.parent/f'{h}.stderr.log').write_text(ep.stderr,encoding='utf-8')
 if ep.returncode!=0:raise RuntimeError(f'EVAL_FAIL seed={seed} h={h} rc={ep.returncode} stderr={ep.stderr[-3000:]}')
 return extract_eval(out)
def run_train(py,root,candidate,contract,lock,host,profile,seed,out):
 cmd=[py,str(root/'tools/train_v14_predicate_horizon.py'),'--project-root',str(root),'--candidate',str(candidate),'--seed',str(seed),'--contract',str(contract),'--lock',str(lock),'--host-lock',str(host),'--profile-lock',str(profile),'--out',str(out)]
 ep=subprocess.run(cmd,cwd=str(root),capture_output=True,text=True,errors='replace');(out.parent/'train.stdout.log').write_text(ep.stdout,encoding='utf-8');(out.parent/'train.stderr.log').write_text(ep.stderr,encoding='utf-8')
 if ep.returncode!=0:raise RuntimeError(f'TRAIN_FAIL seed={seed} rc={ep.returncode} stderr={ep.stderr[-3000:]}')
 return L(out/'RUN_MANIFEST.json')
def main():
 ap=argparse.ArgumentParser();
 for x in ['project-root','candidate','contract','lock','host-lock','profile-lock','source-attempt','amendment','out']:ap.add_argument('--'+x,type=Path,required=True)
 a=ap.parse_args();root=a.project_root.resolve();out=a.out.resolve();src=a.source_attempt.resolve();py=sys.executable
 if out.exists():raise SystemExit('REFUSE_OVERWRITE')
 out.mkdir(parents=True)
 # immutable parent lock verify
 lock=L(a.lock)
 for rel,m in lock['files'].items():
  p=root/rel
  if not p.is_file() or p.stat().st_size!=m['bytes'] or H(p)!=m['sha256']:raise SystemExit('PARENT_LOCK_DRIFT '+rel)
 amend=L(a.amendment);receipt={'schema':'cfe.v14r2.recovery-campaign.v1','status':'RUNNING','started':time.time(),'identity':amend['identity'],'parent_attempt':str(src),'jobs':[],'parent_lock_sha256':H(a.lock),'amendment_sha256':H(a.amendment)};J(out/'CAMPAIGN_RECEIPT.json',receipt)
 old=L(src/'CAMPAIGN_RECEIPT.json');old_by={int(j['seed']):j for j in old['jobs']}
 for seed in SEEDS:
  print('SEED',seed,flush=True);sd=out/str(seed);evals={}
  if seed in [2026083111,2026083112]:
   oj=old_by.get(seed)
   if not oj or oj.get('status')!='COMPLETE':raise SystemExit(f'EXPECTED_COMPLETE_MISSING {seed}')
   run=L(src/str(seed)/'train'/'RUN_MANIFEST.json')
   for h in HORIZONS:
    verify_adapter_from_run(src,run,seed,h)
    ev=src/str(seed)/h/'eval'; got=extract_eval(ev)
    if got['eval_manifest_sha256']!=oj['horizons'][h]['eval_manifest_sha256']:raise SystemExit(f'OLD_EVAL_HASH_MISMATCH {seed} {h}')
    evals[h]=got
   receipt['jobs'].append({'seed':seed,'status':'COMPLETE_SALVAGED','source_run_manifest_sha256':H(src/str(seed)/'train'/'RUN_MANIFEST.json'),'horizons':evals});J(out/'CAMPAIGN_RECEIPT.json',receipt);continue
  if seed==2026083113:
   runp=src/str(seed)/'train'/'RUN_MANIFEST.json';run=L(runp)
   if run.get('status')!='TRAINING_EXECUTED__SCIENTIFIC_EFFECT_UNQUALIFIED' or run.get('train_result',{}).get('epoch')!=16.0:raise SystemExit('SEED3113_TRAIN_NOT_COMPLETE')
   for h in HORIZONS:verify_adapter_from_run(src,run,seed,h)
   for h in HORIZONS:
    print('REEVAL',seed,h,flush=True);evals[h]=run_eval(py,root,a.candidate,a.contract,a.lock,a.host_lock,seed,h,src/str(seed)/'train'/'checkpoints'/h/'adapter',runp,sd/h/'eval')
   receipt['jobs'].append({'seed':seed,'status':'COMPLETE_TRAIN_SALVAGED_REEVALUATED','source_run_manifest_sha256':H(runp),'horizons':evals});J(out/'CAMPAIGN_RECEIPT.json',receipt);continue
  print('TRAIN',seed,flush=True);tr=sd/'train';run=run_train(py,root,a.candidate,a.contract,a.lock,a.host_lock,a.profile_lock,seed,tr)
  for h in HORIZONS:
   print('EVAL',seed,h,flush=True);adapter=verify_adapter_from_run(out,run,seed,h);evals[h]=run_eval(py,root,a.candidate,a.contract,a.lock,a.host_lock,seed,h,adapter,tr/'RUN_MANIFEST.json',sd/h/'eval')
  receipt['jobs'].append({'seed':seed,'status':'COMPLETE_FRESH','run_manifest_sha256':H(tr/'RUN_MANIFEST.json'),'horizons':evals});J(out/'CAMPAIGN_RECEIPT.json',receipt)
 if len(receipt['jobs'])!=6:raise SystemExit('SIX_SEEDS_REQUIRED')
 # longitudinal aggregate only now
 agg={'schema':'cfe.v14r2.predicate-horizon-aggregate.v1','status':'COMPLETE_6_OF_6','identity':amend['identity'],'parent_lock_sha256':H(a.lock),'amendment_sha256':H(a.amendment),'seeds':SEEDS,'per_seed':receipt['jobs']}
 for h in HORIZONS:
  vals=[j['horizons'][h]['balanced_accuracy'] for j in receipt['jobs']];agg[h]={'balanced_accuracy_mean':sum(vals)/len(vals),'balanced_accuracy_values':vals}
 # paired deltas
 for a1,a2,name in [('H1','H2','H2_MINUS_H1'),('H2','H4','H4_MINUS_H2'),('H1','H4','H4_MINUS_H1')]:
  ds=[j['horizons'][a2]['balanced_accuracy']-j['horizons'][a1]['balanced_accuracy'] for j in receipt['jobs']];agg[name]={'mean':sum(ds)/len(ds),'values':ds,'positive':sum(x>0 for x in ds),'negative':sum(x<0 for x in ds),'zero':sum(x==0 for x in ds)}
 J(out/'AGGREGATE.json',agg);receipt['status']='COMPLETE_6_OF_6';receipt['aggregate_sha256']=H(out/'AGGREGATE.json');receipt['completed']=time.time();J(out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps({'status':receipt['status'],'aggregate_sha256':receipt['aggregate_sha256']},indent=2))
if __name__=='__main__':main()
