#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,time,shutil
from pathlib import Path
from dd1_predicate_field_resolution_common import *

def creds(pub):
 cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=pub,check=True);vals={}
 for line in cp.stdout.splitlines():
  if '=' in line:
   k,v=line.split('=',1);vals[k]=v
 env=os.environ.copy();env['GH_TOKEN']=vals['password'];return env

def release_asset(root,tag,repo,name):
 pub=root/'publication/github/Cognitive-Field-Engineering';env=creds(pub);cp=subprocess.run(['gh','api',f'repos/{repo}/releases/tags/{tag}'],cwd=pub,env=env,capture_output=True,text=True,check=True);d=json.loads(cp.stdout);a=next((x for x in d['assets'] if x['name']==name),None);return d,a

def upload_and_verify(root,tag,repo,asset_path,name):
 pub=root/'publication/github/Cognitive-Field-Engineering';env=creds(pub);links=root/'.pcmmad_sync_runs/dd1r1_release_links';links.mkdir(parents=True,exist_ok=True);link=links/name
 if link.exists():link.unlink()
 os.link(asset_path,link)
 last=None
 for attempt in range(3):
  cp=subprocess.run(['gh','release','upload',tag,str(link),'--repo',repo,'--clobber'],cwd=pub,env=env,capture_output=True,text=True,timeout=None);last=cp
  if cp.returncode==0:break
  time.sleep(5)
 link.unlink(missing_ok=True)
 if last.returncode!=0:raise RuntimeError('RELEASE_UPLOAD_FAIL '+last.stderr[-2000:])
 d,a=release_asset(root,tag,repo,name);sha=sha256_file(asset_path);ok=bool(a and a['size']==asset_path.stat().st_size and a.get('digest')=='sha256:'+sha)
 if not ok:raise RuntimeError('REMOTE_DIGEST_VERIFY_FAIL '+name)
 return {'asset_name':name,'bytes':a['size'],'sha256':sha,'remote_digest':a.get('digest'),'release_url':d['html_url']}

def exec_retry(cmd,root,stdout,stderr,manifest,phase):
 if manifest.exists():raise RuntimeError(f'{phase}_MANIFEST_PREEXISTS')
 last=None
 for attempt in range(1,4):
  cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True,errors='replace');last=cp
  stdout.write_text((stdout.read_text(encoding='utf-8',errors='replace') if stdout.exists() else '')+f'\n=== ATTEMPT {attempt} RC {cp.returncode} ===\n'+cp.stdout,encoding='utf-8');stderr.write_text((stderr.read_text(encoding='utf-8',errors='replace') if stderr.exists() else '')+f'\n=== ATTEMPT {attempt} RC {cp.returncode} ===\n'+cp.stderr,encoding='utf-8')
  if cp.returncode==0:return cp
  if manifest.exists():raise RuntimeError(f'{phase}_FAILED_AFTER_MANIFEST attempt={attempt} rc={cp.returncode}')
  time.sleep(10)
 raise RuntimeError(f'{phase}_RETRIES_EXHAUSTED rc={last.returncode}')

def arm_fresh(py,root,a,seed,arm,sd):
 td=sd/'train';ed=sd/'eval';
 cmd=[py,str(root/'tools/train_dd1_predicate_field_resolution.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(td)]
 exec_retry(cmd,root,sd/'train.stdout.log',sd/'train.stderr.log',td/'RUN_MANIFEST.json','TRAIN');rm=loadj(td/'RUN_MANIFEST.json')
 cmd=[py,str(root/'tools/evaluate_dd1_predicate_field_resolution.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--adapter',str(td/'adapter'),'--run-manifest',str(td/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ed)]
 exec_retry(cmd,root,sd/'eval.stdout.log',sd/'eval.stderr.log',ed/'EVAL_MANIFEST.json','EVAL');em=loadj(ed/'EVAL_MANIFEST.json');asset=td/'adapter'/'adapter_model.safetensors';name=f'dd1_seed{seed}_{arm}_adapter_model.safetensors';remote=upload_and_verify(root,a.release_tag,a.repo,asset,name);asset.unlink();return {'arm':arm,'run_manifest_sha256':sha256_file(td/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ed/'EVAL_MANIFEST.json'),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--amendment',type=Path,required=True);ap.add_argument('--parent-campaign',type=Path,required=True);ap.add_argument('--release-tag',required=True);ap.add_argument('--repo',default='SEng-Kitathas/Cognitive-Field-Engineering');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock);c=loadj(a.contract);am=loadj(a.amendment);pre=loadj(a.preexec)
 if pre.get('status')!='DD1_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 # verify salvage local + remote
 old=a.parent_campaign.resolve();sr=am['salvage'];tr=old/'2026083121/IDENTIFYING_COVISIBLE/train/RUN_MANIFEST.json';ev=old/'2026083121/IDENTIFYING_COVISIBLE/eval/EVAL_MANIFEST.json';rm=loadj(tr);em=loadj(ev)
 if sha256_file(tr)!=sr['train_manifest_sha256'] or sha256_file(ev)!=sr['eval_manifest_sha256']:raise SystemExit('SALVAGE_MANIFEST_HASH_FAIL')
 if rm['initial_trainable_sha256']!=sr['initial_trainable_sha256'] or rm['adapter_files']['adapter_model.safetensors']['sha256']!=sr['adapter_sha256']:raise SystemExit('SALVAGE_CONTENT_FAIL')
 d,ra=release_asset(root,a.release_tag,a.repo,sr['remote_asset'])
 if not ra or ra['size']!=rm['adapter_files']['adapter_model.safetensors']['bytes'] or ra.get('digest')!=sr['remote_digest']:raise SystemExit('SALVAGE_REMOTE_VERIFY_FAIL')
 a.out.mkdir(parents=True);receipt={'schema':'cfe.dd1r1.recovery-campaign.v1','status':'RUNNING','identity':am['identity'],'parent_scientific_identity':am['parent_scientific_identity'],'input_lock_sha256':sha256_file(a.lock),'amendment_sha256':sha256_file(a.amendment),'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);py=sys.executable
 salv={'arm':'IDENTIFYING_COVISIBLE','run_manifest_sha256':sha256_file(tr),'eval_manifest_sha256':sha256_file(ev),'metrics':em['metrics'],'heavy_publication':{'asset_name':sr['remote_asset'],'bytes':ra['size'],'sha256':sr['adapter_sha256'],'remote_digest':ra['digest'],'release_url':d['html_url']},'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256'],'status':'SALVAGED_REMOTE_VERIFIED'}
 print('RECOVER_PAIR 2026083121',flush=True);fresh=arm_fresh(py,root,a,2026083121,'MARGIN_HOMOGENEOUS_DISPERSED',a.out/'2026083121/MARGIN_HOMOGENEOUS_DISPERSED')
 if fresh['initial_trainable_sha256']!=salv['initial_trainable_sha256']:raise SystemExit('PAIRED_INIT_MISMATCH_2026083121')
 receipt['jobs'].append({'seed':2026083121,'status':'COMPLETE_PAIR_RECOVERED','paired_initialization_sha256':salv['initial_trainable_sha256'],'arms':[salv,fresh]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 for seed in c['seeds'][1:]:
  print('PAIR',seed,flush=True);arms=[];init=None
  for arm in c['arms']:
   x=arm_fresh(py,root,a,seed,arm,a.out/str(seed)/arm)
   if init is None:init=x['initial_trainable_sha256']
   elif x['initial_trainable_sha256']!=init:raise SystemExit(f'PAIRED_INIT_MISMATCH_{seed}')
   arms.append(x)
  receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR_FRESH','paired_initialization_sha256':init,'arms':arms});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 per=[]
 for j in receipt['jobs']:
  by={x['arm']:x for x in j['arms']};A=by['IDENTIFYING_COVISIBLE']['metrics'];B=by['MARGIN_HOMOGENEOUS_DISPERSED']['metrics'];per.append({'seed':j['seed'],'identifying_ba':A['balanced_accuracy'],'dispersed_ba':B['balanced_accuracy'],'delta_ba':A['balanced_accuracy']-B['balanced_accuracy'],'identifying_false':A['by_truth']['false']['accuracy'],'dispersed_false':B['by_truth']['false']['accuracy'],'identifying_true':A['by_truth']['true']['accuracy'],'dispersed_true':B['by_truth']['true']['accuracy'],'identifying_overall':A['overall']['accuracy'],'dispersed_overall':B['overall']['accuracy']})
 mean=lambda k:sum(x[k] for x in per)/len(per);agg={'schema':'cfe.dd1.aggregate.v1','status':'COMPLETE_6_OF_6','identity':am['parent_scientific_identity'],'execution_identity':am['identity'],'per_seed':per,'summary':{'mean_identifying_ba':mean('identifying_ba'),'mean_dispersed_ba':mean('dispersed_ba'),'mean_delta_ba':mean('delta_ba'),'identifying_wins':sum(x['delta_ba']>0 for x in per),'dispersed_wins':sum(x['delta_ba']<0 for x in per),'ties':sum(x['delta_ba']==0 for x in per),'mean_identifying_false':mean('identifying_false'),'mean_dispersed_false':mean('dispersed_false'),'mean_identifying_true':mean('identifying_true'),'mean_dispersed_true':mean('dispersed_true'),'identifying_two_sided_ge_065':sum(x['identifying_false']>=.65 and x['identifying_true']>=.65 for x in per)}};dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE_6_OF_6';receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
