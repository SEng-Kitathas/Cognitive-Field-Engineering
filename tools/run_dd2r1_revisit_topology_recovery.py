#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,time
from pathlib import Path
from dd2_revisit_topology_common import *


def creds(pub: Path):
    cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=pub,check=True)
    vals={}
    for line in cp.stdout.splitlines():
        if '=' in line:
            k,v=line.split('=',1); vals[k]=v
    env=os.environ.copy(); env['GH_TOKEN']=vals['password']; return env


def upload(root: Path, tag: str, repo: str, p: Path, name: str):
    pub=root/'publication/github/Cognitive-Field-Engineering'; env=creds(pub)
    links=root/'.pcmmad_sync_runs/dd2r1_release_links'; links.mkdir(parents=True,exist_ok=True)
    link=links/name
    if link.exists(): link.unlink()
    os.link(p,link)
    last=None
    for _ in range(3):
        last=subprocess.run(['gh','release','upload',tag,str(link),'--repo',repo,'--clobber'],cwd=pub,env=env,capture_output=True,text=True,timeout=None)
        if last.returncode==0: break
        time.sleep(5)
    link.unlink(missing_ok=True)
    if last is None or last.returncode!=0:
        raise RuntimeError('UPLOAD_FAIL '+(last.stderr[-1000:] if last else 'NO_ATTEMPT'))
    q=subprocess.run(['gh','api',f'repos/{repo}/releases/tags/{tag}'],cwd=pub,env=env,capture_output=True,text=True,check=True)
    release=json.loads(q.stdout); asset=next((x for x in release['assets'] if x['name']==name),None)
    sha=sha256_file(p)
    if not asset or asset['size']!=p.stat().st_size or asset.get('digest')!='sha256:'+sha:
        raise RuntimeError('REMOTE_VERIFY_FAIL '+name)
    return {'asset_name':name,'bytes':asset['size'],'sha256':sha,'remote_digest':asset['digest'],'release_url':release['html_url']}


def retry(cmd,root,stdout_path,stderr_path,manifest,phase):
    last=None
    for i in range(1,4):
        if manifest.exists(): raise RuntimeError(phase+'_MANIFEST_PREEXISTS')
        cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True,errors='replace'); last=cp
        stdout_path.parent.mkdir(parents=True,exist_ok=True)
        stdout_path.write_text((stdout_path.read_text(encoding='utf-8',errors='replace') if stdout_path.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stdout,encoding='utf-8')
        stderr_path.write_text((stderr_path.read_text(encoding='utf-8',errors='replace') if stderr_path.exists() else '')+f'\n=== ATTEMPT {i} RC {cp.returncode} ===\n'+cp.stderr,encoding='utf-8')
        if cp.returncode==0: return
        if manifest.exists(): raise RuntimeError(phase+'_FAILED_AFTER_MANIFEST')
        time.sleep(10)
    raise RuntimeError(phase+f'_RETRIES_EXHAUSTED_RC_{last.returncode}')


def verify_lock(root: Path, lock_path: Path):
    lock=loadj(lock_path)
    for rel,m in lock['files'].items():
        p=root/rel
        if not p.is_file() or p.stat().st_size!=m['bytes'] or sha256_file(p)!=m['sha256']:
            raise SystemExit('LOCK_FAIL '+rel)


def eval_arm(py,root,candidate,contract,lock,host_lock,seed,arm,adapter,run_manifest,out_dir,log_dir):
    cmd=[py,str(root/'tools/evaluate_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(candidate),'--arm',arm,'--seed',str(seed),'--adapter',str(adapter),'--run-manifest',str(run_manifest),'--contract',str(contract),'--lock',str(lock),'--host-lock',str(host_lock),'--out',str(out_dir)]
    retry(cmd,root,log_dir/'eval.stdout.log',log_dir/'eval.stderr.log',out_dir/'EVAL_MANIFEST.json','EVAL')
    return loadj(out_dir/'EVAL_MANIFEST.json')


def train_arm(py,root,candidate,contract,lock,host_lock,profile_lock,seed,arm,out_dir,log_dir):
    cmd=[py,str(root/'tools/train_dd2_revisit_topology.py'),'--project-root',str(root),'--candidate',str(candidate),'--arm',arm,'--seed',str(seed),'--contract',str(contract),'--lock',str(lock),'--host-lock',str(host_lock),'--profile-lock',str(profile_lock),'--out',str(out_dir)]
    retry(cmd,root,log_dir/'train.stdout.log',log_dir/'train.stderr.log',out_dir/'RUN_MANIFEST.json','TRAIN')
    return loadj(out_dir/'RUN_MANIFEST.json')


def arm_receipt(root,tag,repo,seed,arm,run_manifest,eval_manifest,adapter,provenance):
    rm=loadj(run_manifest); em=loadj(eval_manifest)
    remote=upload(root,tag,repo,adapter,f'dd2_seed{seed}_{arm}_adapter_model.safetensors')
    adapter.unlink()
    return {'arm':arm,'provenance':provenance,'run_manifest_sha256':sha256_file(run_manifest),'eval_manifest_sha256':sha256_file(eval_manifest),'metrics':em['metrics'],'heavy_publication':remote,'initial_trainable_sha256':rm['initial_trainable_sha256'],'final_trainable_sha256':rm['final_trainable_sha256']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',type=Path,required=True); ap.add_argument('--candidate',type=Path,required=True)
    ap.add_argument('--contract',type=Path,required=True); ap.add_argument('--lock',type=Path,required=True)
    ap.add_argument('--host-lock',type=Path,required=True); ap.add_argument('--profile-lock',type=Path,required=True)
    ap.add_argument('--preexec',type=Path,required=True); ap.add_argument('--amendment',type=Path,required=True)
    ap.add_argument('--parent-campaign',type=Path,required=True); ap.add_argument('--release-tag',required=True)
    ap.add_argument('--repo',default='SEng-Kitathas/Cognitive-Field-Engineering'); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); root=a.project_root.resolve(); verify_lock(root,a.lock)
    pre=loadj(a.preexec); contract=loadj(a.contract); amendment=loadj(a.amendment)
    if pre.get('status')!='DD2_RUNTIME_QUALIFIED__SCIENTIFIC_TRAINING_AUTHORIZED': raise SystemExit('PREEXEC_NOT_AUTHORIZED')
    if amendment.get('status')!='FROZEN_EXECUTION_RECOVERY_PRE_RUNTIME' or amendment.get('scientific_design_changed') is not False: raise SystemExit('RECOVERY_AMENDMENT_INVALID')
    if a.out.exists(): raise SystemExit('REFUSE_OVERWRITE')
    a.out.mkdir(parents=True)
    receipt={'schema':'cfe.dd2r1.campaign.v1','status':'RUNNING','identity':amendment['identity'],'parent_scientific_identity':contract['identity'],'input_lock_sha256':sha256_file(a.lock),'preexec_sha256':sha256_file(a.preexec),'amendment_sha256':sha256_file(a.amendment),'jobs':[]}
    dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt); py=sys.executable

    # Recover seed 2026083121 CYCLIC_SPACED without retraining manifested science.
    seed=contract['seeds'][0]; arm='CYCLIC_SPACED'; parent_arm=a.parent_campaign/str(seed)/arm
    parent_rm=parent_arm/'train/RUN_MANIFEST.json'; parent_adapter_dir=parent_arm/'train/adapter'; parent_adapter=parent_adapter_dir/'adapter_model.safetensors'
    if sha256_file(parent_rm)!=amendment['salvage']['train_manifest_sha256'] or sha256_file(parent_adapter)!=amendment['salvage']['adapter_sha256']:
        raise SystemExit('SALVAGE_HASH_MISMATCH')
    print('RECOVER_EVAL',seed,arm,flush=True)
    rec_sd=a.out/str(seed)/arm; rec_eval=rec_sd/'eval'
    em=eval_arm(py,root,a.candidate,a.contract,a.lock,a.host_lock,seed,arm,parent_adapter_dir,parent_rm,rec_eval,rec_sd)
    spaced=arm_receipt(root,a.release_tag,a.repo,seed,arm,parent_rm,rec_eval/'EVAL_MANIFEST.json',parent_adapter,'SALVAGED_TRAIN__RECOVERED_EVAL')

    # Train only the missing paired arm fresh.
    arm='WINDOW_MASSED'; sd=a.out/str(seed)/arm; td=sd/'train'; ed=sd/'eval'
    print('TRAIN',seed,arm,flush=True); rm=train_arm(py,root,a.candidate,a.contract,a.lock,a.host_lock,a.profile_lock,seed,arm,td,sd)
    if rm['initial_trainable_sha256']!=amendment['salvage']['initial_trainable_sha256']: raise SystemExit(f'PAIRED_INIT_MISMATCH_{seed}')
    print('EVAL',seed,arm,flush=True); eval_arm(py,root,a.candidate,a.contract,a.lock,a.host_lock,seed,arm,td/'adapter',td/'RUN_MANIFEST.json',ed,sd)
    massed=arm_receipt(root,a.release_tag,a.repo,seed,arm,td/'RUN_MANIFEST.json',ed/'EVAL_MANIFEST.json',td/'adapter/adapter_model.safetensors','FRESH_RECOVERY_TRAIN')
    receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR_RECOVERED','paired_initialization_sha256':rm['initial_trainable_sha256'],'arms':[spaced,massed]}); dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)

    # Remaining seeds: both arms fresh under unchanged science.
    for seed in contract['seeds'][1:]:
        arms=[]; init=None
        for arm in contract['arms']:
            sd=a.out/str(seed)/arm; td=sd/'train'; ed=sd/'eval'
            print('TRAIN',seed,arm,flush=True); rm=train_arm(py,root,a.candidate,a.contract,a.lock,a.host_lock,a.profile_lock,seed,arm,td,sd)
            if init is None: init=rm['initial_trainable_sha256']
            elif rm['initial_trainable_sha256']!=init: raise SystemExit(f'PAIRED_INIT_MISMATCH_{seed}')
            print('EVAL',seed,arm,flush=True); eval_arm(py,root,a.candidate,a.contract,a.lock,a.host_lock,seed,arm,td/'adapter',td/'RUN_MANIFEST.json',ed,sd)
            arms.append(arm_receipt(root,a.release_tag,a.repo,seed,arm,td/'RUN_MANIFEST.json',ed/'EVAL_MANIFEST.json',td/'adapter/adapter_model.safetensors','FRESH_RECOVERY_TRAIN'))
        receipt['jobs'].append({'seed':seed,'status':'COMPLETE_PAIR_FRESH','paired_initialization_sha256':init,'arms':arms}); dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)

    per=[]
    for job in receipt['jobs']:
        by={x['arm']:x for x in job['arms']}; s=by['CYCLIC_SPACED']['metrics']; m=by['WINDOW_MASSED']['metrics']
        per.append({'seed':job['seed'],'spaced_ba':s['balanced_accuracy'],'massed_ba':m['balanced_accuracy'],'delta_ba':s['balanced_accuracy']-m['balanced_accuracy'],'spaced_false':s['by_truth']['false']['accuracy'],'massed_false':m['by_truth']['false']['accuracy'],'spaced_true':s['by_truth']['true']['accuracy'],'massed_true':m['by_truth']['true']['accuracy'],'spaced_overall':s['overall']['accuracy'],'massed_overall':m['overall']['accuracy']})
    mean=lambda k:sum(x[k] for x in per)/len(per)
    agg={'schema':'cfe.dd2.aggregate.v1','status':'COMPLETE_6_OF_6','identity':contract['identity'],'execution_recovery_identity':amendment['identity'],'per_seed':per,'summary':{'mean_spaced_ba':mean('spaced_ba'),'mean_massed_ba':mean('massed_ba'),'mean_delta_ba':mean('delta_ba'),'spaced_wins':sum(x['delta_ba']>0 for x in per),'massed_wins':sum(x['delta_ba']<0 for x in per),'ties':sum(x['delta_ba']==0 for x in per),'mean_spaced_false':mean('spaced_false'),'mean_massed_false':mean('massed_false'),'mean_spaced_true':mean('spaced_true'),'mean_massed_true':mean('massed_true')}}
    dumpj(a.out/'AGGREGATE.json',agg); receipt['status']='COMPLETE_6_OF_6'; receipt['aggregate_sha256']=sha256_file(a.out/'AGGREGATE.json'); dumpj(a.out/'CAMPAIGN_RECEIPT.json',receipt)
    print(json.dumps(agg,indent=2,sort_keys=True),flush=True)

if __name__=='__main__': main()
