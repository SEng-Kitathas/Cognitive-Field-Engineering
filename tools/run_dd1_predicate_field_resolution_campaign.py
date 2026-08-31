#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,time,hashlib,shutil
from pathlib import Path
from dd1_predicate_field_resolution_common import *
def upload_and_verify(root,release_tag,repo,asset_path,asset_name):
 pub=root/'publication/github/Cognitive-Field-Engineering';cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=pub,check=True);vals={}
 for line in cp.stdout.splitlines():
  if '=' in line:
   k,v=line.split('=',1);vals[k]=v
 env=os.environ.copy();env['GH_TOKEN']=vals['password'];links=root/'.pcmmad_sync_runs/dd1_release_links';links.mkdir(parents=True,exist_ok=True);link=links/asset_name
 if link.exists():link.unlink()
 os.link(asset_path,link);up=subprocess.run(['gh','release','upload',release_tag,str(link),'--repo',repo,'--clobber'],cwd=pub,env=env,capture_output=True,text=True,timeout=None)
 link.unlink(missing_ok=True)
 if up.returncode!=0:raise RuntimeError('RELEASE_UPLOAD_FAIL '+up.stderr[-2000:])
 api=subprocess.run(['gh','api',f'repos/{repo}/releases/tags/{release_tag}'],cwd=pub,env=env,capture_output=True,text=True,check=True);d=json.loads(api.stdout);a=next((x for x in d['assets'] if x['name']==asset_name),None);local_sha=sha256_file(asset_path);ok=bool(a and a['size']==asset_path.stat().st_size and a.get('digest')=='sha256:'+local_sha)
 if not ok:raise RuntimeError('REMOTE_DIGEST_VERIFY_FAIL '+asset_name)
 return {'asset_name':asset_name,'bytes':a['size'],'sha256':local_sha,'remote_digest':a.get('digest'),'release_url':d['html_url']}
def run(cmd,root,stdout,stderr):
 p=subprocess.run(cmd,cwd=root,capture_output=True,text=True,errors='replace');stdout.write_text(p.stdout,encoding='utf-8');stderr.write_text(p.stderr,encoding='utf-8');return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--contract',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--host-lock',type=Path,required=True);ap.add_argument('--profile-lock',type=Path,required=True);ap.add_argument('--preexec',type=Path,required=True);ap.add_argument('--release-tag',required=True);ap.add_argument('--repo',default='SEng-Kitathas/Cognitive-Field-Engineering');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();verify_lock(root,a.lock);c=loadj(a.contract);pre=loadj(a.preexec)
 if pre.get('status')!='DD1_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED':raise SystemExit('PREEXEC_NOT_AUTHORIZED')
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 a.out.mkdir(parents=True);receipt={'schema':'cfe.dd1.campaign-receipt.v1','status':'RUNNING','identity':c['identity'],'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec),'release_tag':a.release_tag,'jobs':[]};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);py=sys.executable
 for seed in c['seeds']:
  pair=[];init=None
  for arm in c['arms']:
   sd=a.out/str(seed)/arm;td=sd/'train';ed=sd/'eval';print('TRAIN',seed,arm,flush=True)
   cmd=[py,str(root/'tools/train_dd1_predicate_field_resolution.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--profile-lock',str(a.profile_lock),'--out',str(td)];p=run(cmd,root,sd/'train.stdout.log',sd/'train.stderr.log')
   if p.returncode!=0:
    receipt['status']='BLOCKED';receipt['failure']={'seed':seed,'arm':arm,'phase':'TRAIN','return_code':p.returncode};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(p.returncode)
   rm=loadj(td/'RUN_MANIFEST.json')
   if init is None:init=rm['initial_trainable_sha256']
   elif rm['initial_trainable_sha256']!=init:raise RuntimeError(f'PAIRED_INIT_MISMATCH {seed}')
   print('EVAL',seed,arm,flush=True);cmd=[py,str(root/'tools/evaluate_dd1_predicate_field_resolution.py'),'--project-root',str(root),'--candidate',str(a.candidate),'--arm',arm,'--seed',str(seed),'--adapter',str(td/'adapter'),'--run-manifest',str(td/'RUN_MANIFEST.json'),'--contract',str(a.contract),'--lock',str(a.lock),'--host-lock',str(a.host_lock),'--out',str(ed)];p=run(cmd,root,sd/'eval.stdout.log',sd/'eval.stderr.log')
   if p.returncode!=0:
    receipt['status']='BLOCKED';receipt['failure']={'seed':seed,'arm':arm,'phase':'EVAL','return_code':p.returncode};dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);raise SystemExit(p.returncode)
   em=loadj(ed/'EVAL_MANIFEST.json');asset=td/'adapter'/'adapter_model.safetensors';asset_name=f'dd1_seed{seed}_{arm}_adapter_model.safetensors';print('UPLOAD',asset_name,flush=True);remote=upload_and_verify(root,a.release_tag,a.repo,asset,asset_name)
   # reclaim only heavy model after remote digest verification; preserve config + manifests
   asset.unlink();pair.append({'arm':arm,'run_manifest_sha256':sha256_file(td/'RUN_MANIFEST.json'),'eval_manifest_sha256':sha256_file(ed/'EVAL_MANIFEST.json'),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']})
  receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR','paired_initialization_sha256':init,'arms':pair});dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
 # aggregate
 per=[]
 for j in receipt['jobs']:
  by={x['arm']:x for x in j['arms']};A=by['IDENTIFYING_COVISIBLE']['metrics'];B=by['MARGIN_HOMOGENEOUS_DISPERSED']['metrics'];per.append({'seed':j['seed'],'identifying_ba':A['balanced_accuracy'],'dispersed_ba':B['balanced_accuracy'],'delta_ba':A['balanced_accuracy']-B['balanced_accuracy'],'identifying_false':A['by_truth']['false']['accuracy'],'dispersed_false':B['by_truth']['false']['accuracy'],'identifying_true':A['by_truth']['true']['accuracy'],'dispersed_true':B['by_truth']['true']['accuracy'],'identifying_overall':A['overall']['accuracy'],'dispersed_overall':B['overall']['accuracy']})
 mean=lambda k:sum(x[k] for x in per)/len(per);agg={'schema':'cfe.dd1.aggregate.v1','status':'COMPLETE_6_OF_6','identity':c['identity'],'per_seed':per,'summary':{'mean_identifying_ba':mean('identifying_ba'),'mean_dispersed_ba':mean('dispersed_ba'),'mean_delta_ba':mean('delta_ba'),'identifying_wins':sum(x['delta_ba']>0 for x in per),'dispersed_wins':sum(x['delta_ba']<0 for x in per),'ties':sum(x['delta_ba']==0 for x in per),'mean_identifying_false':mean('identifying_false'),'mean_dispersed_false':mean('dispersed_false'),'mean_identifying_true':mean('identifying_true'),'mean_dispersed_true':mean('dispersed_true'),'identifying_two_sided_ge_065':sum(x['identifying_false']>=.65 and x['identifying_true']>=.65 for x in per)}};dumpj(a.out/'AGGREGATE.json',agg);receipt['status']='COMPLETE_6_OF_6';receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json');dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt);print(json.dumps(agg,indent=2,sort_keys=True),flush=True)
if __name__=='__main__':main()
