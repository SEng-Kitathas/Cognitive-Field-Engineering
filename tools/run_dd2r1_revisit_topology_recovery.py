#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,time,shutil
from pathlib import Path
from dd2_revisit_topology_common import *
def creds(pub):
 cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=pub,check=True);v={}
 for line in cp.stdout.splitlines():
  if '=' in line:
   k,x=line.split('=',1);v[k]=x
 e=os.environ.copy();e['GH_TOKEN']=v['password'];return e
def release(root,tag,repo):
 pub=root/'publication/github/Cognitive-Field-Engineering';e=creds(pub);cp=subprocess.run(['gh','api',f'repos/{repo}/releases/tags/{tag}'],cwd=pub,env=e,capture_output=True,text=True,check=True);return json.loads(cp.stdout),e
def download_salvage(root,tag,repo,name,dest,sha,size):
 d,e=release(root,tag,repo);a=next((x for x in d['assets'] if x['name']==name),None)
 if not a or a['size']!=size or a.get('digest')!='sha256:'+sha:raise RuntimeError('SALVAGE_REMOTE_IDENTITY_FAIL')
 dest.parent.mkdir(parents=True,exist_ok=True);dest.unlink(missing_ok=True);cp=subprocess.run(['gh','release','download',tag,'--repo',repo,'--pattern',name,'--dir',str(dest.parent),'--clobber'],cwd=root/'publication/github/Cognitive-Field-Engineering',env=e,capture_output=True,text=True,timeout=None)
 if cp.returncode!=0:raise RuntimeError('SALVAGE_DOWNLOAD_FAIL '+cp.stderr[-1000:])
 got=dest.parent/name
 if got!=dest:shutil.move(str(got),str(dest))
 if dest.stat().st_size!=size or sha256_file(dest)!=sha:raise RuntimeError('SALVAGE_LOCAL_VERIFY_FAIL')
 return {'asset_name':name,'bytes':size,'sha256':sha,'remote_digest':'sha256:'+sha,'release_url':d['html_url']}
def upload(root,tag,repo,p,name):
 pub=root/'publication/github/Cognitive-Field-Engineering';d,e=release(root,tag,repo);link=root/'.pcmmad_sync_runs/dd2r1_links'/name;link.parent.mkdir(parents=True,exist_ok=True);link.unlink(missing_ok=True);os.link(p,link)
 last=None
 for _ in range(3):
  last=subprocess.run(['gh','release','upload',tag,str(link),'--repo',repo,'--clobber'],cwd=pub,env=e,capture_output=True,text=True,timeout=None)
  if last.returncode==0:break
  time.sleep(5)
 link.unlink(missing_ok=True)
 if last.returncode!=0:raise RuntimeError('UPLOAD_FAIL '+last.stderr[-1000:])
 d,_=release(root,tag,repo);a=next((x for x in d['assets'] if x['name']==name),None);sha=sha256_file(p)
 if not a or a['size']!=p.stat().st_size or a.get('digest')!='sha256:'+sha:raise RuntimeError('UPLOAD_VERIFY_FAIL')
 return {'asset_name':name,'bytes':a['size'],'sha256':sha,'remote_digest':a['digest'],'release_url':d['html_url']}
def retry(cmd,root,so,se,manifest,phase):
 if manifest.exists():raise RuntimeError(phase+'_MANIFEST_PREEXISTS')
 for i in range(1,4):
  cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True,errors='replace');so.write_text((so.read_text(encoding='utf-8',errors='replace') if so.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stdout,encoding='utf-8');se.write_text((se.read_text(encoding='utf-8',errors='replace') if se.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stderr,encoding='utf-8')
  if cp.returncode==0:return
  if manifest.exists():raise RuntimeError(phase+'_FAILED_AFTER_MANIFEST')
  time.sleep(20)
 raise RuntimeError(phase+'_RETRIES_EXHAUSTED')
def fresh(py,root,a,seed,arm,sd):
 td=sd/'train';ed=sd/'eval';cmd=[py,str(root/'tools/train_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(td)];retry(cmd,root,sd/'train.stdout.log',sd/'train.stderr.log',td/'RUN_MANIFEST.json','TRAIN');rm=loadj(td/'RUN_MANIFEST.json');cmd=[py,str(root/'tools/evaluate_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--adapter',str(td/'adapter'),'--run-manifest',str(td/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ed)];retry(cmd,root,sd/'eval.stdout.log',sd/'eval.stderr.log',ed/'EVAL_MANIFEST.json','EVAL');em=loadj(ed/'EVAL_MANIFEST.json');asset=td/'adapter/adapter_model.safetensors';remote=upload(root,a.release_tag,a.repo,asset,f'dd2_seed{seed}_{arm}_adapter_model.safetensors');asset.unlink();return {'arm':arm,'run_manifest_sha256':sha256_file(td/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ed/'EVAL_MANIFEST.json'),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--amendment',type=Path,required=True);ap.add_argument('--parent-campaign',type=Path,required=True);ap.add_argument('--release-tag',required=True);ap.add_argument('--repo',default='SEng-Kitathas/Cognitive-Field-Engineering');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();am=loadj(a.amendment);c=loadj(a.contract);lk=loadj(a.lock)
 sentinel=root/am['research_lane_gate'];deadline=time.time()+7*3600
 while not sentinel.exists() and time.time()<deadline:time.sleep(30)
 if not sentinel.exists():raise SystemExit('RESEARCH_SENTINEL_TIMEOUT')
 for rel,m in lk['files'].items():
  p=root/rel
  if not p.is_file() or p.stat().st_size!=m['bytes'] or sha256_file(p)!=m['sha256']:raise SystemExit('LOCK_FAIL '+rel)
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);receipt={'schema':'cfe.dd2r1.recovery.v1','status':'RUNNING','identity':am['identity'],'parent_scientific_identity':am['parent_scientific_identity'],'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);py=sys.executable;sr=am['salvage'];tr=root/sr['train_manifest_path'];rm=loadj(tr)
 if sha256_file(tr)!=sr['train_manifest_sha256'] or rm['initial_trainable_sha256']!=sr['initial_trainable_sha256']:raise SystemExit('SALVAGE_TRAIN_BINDING_FAIL')
 sad=a.out/'2026083121/CYCLIC_SPACED/salvage_adapter/adapter_model.safetensors';remote=download_salvage(root,a.release_tag,a.repo,sr['remote_asset'],sad,sr['adapter_sha256'],sr['adapter_bytes']);ed=a.out/'2026083121/CYCLIC_SPACED/eval';cmd=[py,str(root/'tools/evaluate_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm','CYCLIC_SPACED','--seed','2026083121','--adapter',str(sad.parent),'--run-manifest',str(tr),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ed)];retry(cmd,root,a.out/'2026083121/CYCLIC_SPACED/eval.stdout.log',a.out/'2026083121/CYCLIC_SPACED/eval.stderr.log',ed/'EVAL_MANIFEST.json','SALVAGE_EVAL');em=loadj(ed/'EVAL_MANIFEST.json');sad.unlink();salv={'arm':'CYCLIC_SPACED','status':'SALVAGED_REMOTE_VERIFIED','run_manifest_sha256':sha256_file(tr),'eval_manifest_sha256':sha256_file(ed/'EVAL_MANIFEST.json'),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']}
 mass=fresh(py,root,a,2026083121,'WINDOW_MASSED',a.out/'2026083121/WINDOW_MASSED');
 if mass['initial_trainable_sha256']!=salv['initial_trainable_sha256']:raise SystemExit('PAIRED_INIT_MISMATCH_3121')
 receipt['jobs'].append({'seed':2026083121,'status':'COMPLETE_PAIR_RECOVERED','paired_initialization_sha256':salv['initial_trainable_sha256'],'arms':[salv,mass]});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 for seed in c['seeds'][1:]:
  arms=[];init=None
  for arm in c['arms']:
   x=fresh(py,root,a,seed,arm,a.out/str(seed)/arm);init=x['initial_trainable_sha256'] if init is None else init
   if x['initial_trainable_sha256']!=init:raise SystemExit('PAIRED_INIT_MISMATCH_'+str(seed))
   arms.append(x)
  receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR_FRESH','paired_initialization_sha256':init,'arms':arms});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 per=[]
 for j in receipt['jobs']:
  by={x['arm']:x for x in j['arms']};S=by['CYCLIC_SPACED']['metrics'];M=by['WINDOW_MASSED']['metrics'];per.append({'seed':j['seed'],'spaced_ba':S['balanced_accuracy'],'massed_ba':M['balanced_accuracy'],'delta_ba':S['balanced_accuracy']-M['balanced_accuracy'],'spaced_false':S['by_truth']['false']['accuracy'],'massed_false':M['by_truth']['false']['accuracy'],'spaced_true':S['by_truth']['true']['accuracy'],'massed_true':M['by_truth']['true']['accuracy'],'spaced_overall':S['overall']['accuracy'],'massed_overall':M['overall']['accuracy']})
 mean=lambda k:sum(x[k] for x in per)/6;agg={'schema':'cfe.dd2.aggregate.v1','status':'COMPLETE_6_OF_6','identity':am['parent_scientific_identity'],'execution_identity':am['identity'],'per_seed':per,'summary':{'mean_spaced_ba':mean('spaced_ba'),'mean_massed_ba':mean('massed_ba'),'mean_delta_ba':mean('delta_ba'),'spaced_wins':sum(x['delta_ba']>0 for x in per),'massed_wins':sum(x['delta_ba']<0 for x in per),'ties':sum(x['delta_ba']==0 for x in per),'mean_spaced_false':mean('spaced_false'),'mean_massed_false':mean('massed_false'),'mean_spaced_true':mean('spaced_true'),'mean_massed_true':mean('massed_true')}};dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE_6_OF_6';receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2),flush=True)
if __name__=='__main__':main()
