#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,time
from pathlib import Path
from dd2_revisit_topology_common import *
def creds(pub):
 cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=pub,check=True);v={}
 for line in cp.stdout.splitlines():
  if '=' in line:
   k,x=line.split('=',1);v[k]=x
 e=os.environ.copy();e['GH_TOKEN']=v['password'];return e
def upload(root,tag,repo,p,name):
 pub=root/'publication/github/Cognitive-Field-Engineering';env=creds(pub);links=root/'.pcmmad_sync_runs/dd2_release_links';links.mkdir(parents=True,exist_ok=True);link=links/name
 if link.exists():link.unlink()
 os.link(p,link);last=None
 for _ in range(3):
  last=subprocess.run(['gh','release','upload',tag,str(link),'--repo',repo,'--clobber'],cwd=pub,env=env,capture_output=True,text=True,timeout=None)
  if last.returncode==0:break
  time.sleep(5)
 link.unlink(missing_ok=True)
 if last.returncode!=0:raise RuntimeError('UPLOAD_FAIL '+last.stderr[-1000:])
 q=subprocess.run(['gh','api',f'repos/{repo}/releases/tags/{tag}'],cwd=pub,env=env,capture_output=True,text=True,check=True);d=json.loads(q.stdout);a=next((x for x in d['assets'] if x['name']==name),None);sha=sha256_file(p)
 if not a or a['size']!=p.stat().st_size or a.get('digest')!='sha256:'+sha:raise RuntimeError('REMOTE_VERIFY_FAIL '+name)
 return {'asset_name':name,'bytes':a['size'],'sha256':sha,'remote_digest':a['digest'],'release_url':d['html_url']}
def retry(cmd,root,so,se,manifest,phase):
 last=None
 for i in range(1,4):
  if manifest.exists():raise RuntimeError(phase+'_MANIFEST_PREEXISTS')
  cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True,errors='replace');last=cp;so.write_text((so.read_text(encoding='utf-8',errors='replace') if so.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stdout,encoding='utf-8');se.write_text((se.read_text(encoding='utf-8',errors='replace') if se.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stderr,encoding='utf-8')
  if cp.returncode==0:return
  if manifest.exists():raise RuntimeError(phase+'_FAILED_AFTER_MANIFEST')
  time.sleep(10)
 raise RuntimeError(phase+f'_RETRIES_EXHAUSTED_RC_{last.returncode}')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--release-tag',required=True);ap.add_argument('--repo',default='SEng-Kitathas/Cognitive-Field-Engineering');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();lk=loadj(a.lock)
 for rel,m in lk['files'].items():
  p=root/rel
  if not p.is_file() or p.stat().st_size!=m['bytes'] or sha256_file(p)!=m['sha256']:raise SystemExit('LOCK_FAIL '+rel)
 pre=loadj(a.preexec);c=loadj(a.contract)
 if pre.get('status')!='DD2_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);receipt={'schema':'cfe.dd2.campaign.v1','status':'RUNNING','identity':c['identity'],'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec),'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);py=sys.executable
 for seed in c['seeds']:
  arms=[];init=None
  for arm in c['arms']:
   sd=a.out/str(seed)/arm;td=sd/'train';ed=sd/'eval';print('TRAIN',seed,arm,flush=True);cmd=[py,str(root/'tools/train_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(td)];retry(cmd,root,sd/'train.stdout.log',sd/'train.stderr.log',td/'RUN_MANIFEST.json','TRAIN');rm=loadj(td/'RUN_MANIFEST.json')
   if init is None:init=rm['initial_trainable_sha256']
   elif rm['initial_trainable_sha256']!=init:raise SystemExit(f'PAIRED_INIT_MISMATCH_{seed}')
   print('EVAL',seed,arm,flush=True);cmd=[py,str(root/'tools/evaluate_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--adapter',str(td/'adapter'),'--run-manifest',str(td/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ed)];retry(cmd,root,sd/'eval.stdout.log',sd/'eval.stderr.log',ed/'EVAL_MANIFEST.json','EVAL');em=loadj(ed/'EVAL_MANIFEST.json');asset=td/'adapter'/'adapter_model.safetensors';remote=upload(root,a.release_tag,a.repo,asset,f'dd2_seed{seed}_{arm}_adapter_model.safetensors');asset.unlink();arms.append({'arm':arm,'run_manifest_sha256':sha256_file(td/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ed/'EVAL_MANIFEST.json'),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']})
  receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR','paired_initialization_sha256':init,'arms':arms});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 per=[]
 for j in receipt['jobs']:
  by={x['arm']:x for x in j['arms']};S=by['CYCLIC_SPACED']['metrics'];M=by['WINDOW_MASSED']['metrics'];per.append({'seed':j['seed'],'spaced_ba':S['balanced_accuracy'],'massed_ba':M['balanced_accuracy'],'delta_ba':S['balanced_accuracy']-M['balanced_accuracy'],'spaced_false':S['by_truth']['false']['accuracy'],'massed_false':M['by_truth']['false']['accuracy'],'spaced_true':S['by_truth']['true']['accuracy'],'massed_true':M['by_truth']['true']['accuracy'],'spaced_overall':S['overall']['accuracy'],'massed_overall':M['overall']['accuracy']})
 mean=lambda k:sum(x[k] for x in per)/6;agg={'schema':'cfe.dd2.aggregate.v1','status':'COMPLETE_6_OF_6','identity':c['identity'],'per_seed':per,'summary':{'mean_spaced_ba':mean('spaced_ba'),'mean_massed_ba':mean('massed_ba'),'mean_delta_ba':mean('delta_ba'),'spaced_wins':sum(x['delta_ba']>0 for x in per),'massed_wins':sum(x['delta_ba']<0 for x in per),'ties':sum(x['delta_ba']==0 for x in per),'mean_spaced_false':mean('spaced_false'),'mean_massed_false':mean('massed_false'),'mean_spaced_true':mean('spaced_true'),'mean_massed_true':mean('massed_true')}};dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE_6_OF_6';receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
