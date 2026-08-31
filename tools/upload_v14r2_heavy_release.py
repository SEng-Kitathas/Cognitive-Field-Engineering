#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys,shutil
from pathlib import Path
ROOT=Path.cwd(); REPO=ROOT/'publication/github/Cognitive-Field-Engineering'; TAG='cfe-v14r2-predicate-horizon-research-2026-08-31'; OWNER_REPO='SEng-Kitathas/Cognitive-Field-Engineering'
OUT=ROOT/'state/analysis/V14R2_PREDICATE_HORIZON_RECOVERY_CAMPAIGN_20260831T1853Z'; SRC=ROOT/'state/analysis/V14R_PREDICATE_HORIZON_CAMPAIGN_ATTEMPT2_20260831T1730Z'
def H(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)
 return h.hexdigest()
def token_env():
 cp=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,cwd=REPO,check=True);vals={}
 for line in cp.stdout.splitlines():
  if '=' in line:
   k,v=line.split('=',1);vals[k]=v
 env=os.environ.copy();env['GH_TOKEN']=vals['password'];return env
def main():
 env=token_env();links=ROOT/'.pcmmad_sync_runs/v14r2_release_links';shutil.rmtree(links,ignore_errors=True);links.mkdir(parents=True,exist_ok=True); local={}
 for seed in [2026083111,2026083112,2026083113,2026083114,2026083115,2026083116]:
  base=(SRC if seed in [2026083111,2026083112,2026083113] else OUT)/str(seed)/'train'/'checkpoints'
  for hor in ['H1','H2','H4']:
   src=base/hor/'adapter'/'adapter_model.safetensors';name=f'v14r2_seed{seed}_{hor}_adapter_model.safetensors';dst=links/name
   os.link(src,dst);local[name]={'bytes':src.stat().st_size,'sha256':H(src),'source_path':src.relative_to(ROOT).as_posix()}
 cmd=['gh','release','upload',TAG,'--repo',OWNER_REPO,'--clobber']+[str(links/n) for n in sorted(local)]
 print('UPLOAD_COUNT',len(local),flush=True);cp=subprocess.run(cmd,cwd=REPO,env=env,text=True,capture_output=True,timeout=None);print(cp.stdout,flush=True);print(cp.stderr,flush=True,file=sys.stderr)
 if cp.returncode!=0:raise SystemExit(cp.returncode)
 api=subprocess.run(['gh','api',f'repos/{OWNER_REPO}/releases/tags/{TAG}'],cwd=REPO,env=env,text=True,capture_output=True,check=True);d=json.loads(api.stdout);remote={a['name']:{'bytes':a['size'],'digest':a.get('digest'),'id':a['id']} for a in d.get('assets',[])}
 checks=[]
 for n,m in local.items():
  r=remote.get(n);expected='sha256:'+m['sha256'];checks.append({'name':n,'present':r is not None,'size_match':bool(r and r['bytes']==m['bytes']),'digest_match':bool(r and r.get('digest')==expected),'local_sha256':m['sha256'],'remote_digest':r.get('digest') if r else None,'bytes':m['bytes'],'remote_bytes':r.get('bytes') if r else None,'source_path':m['source_path']})
 status='PASS' if all(x['present'] and x['size_match'] and x['digest_match'] for x in checks) else 'FAIL'
 out={'schema':'cfe.v14r2.heavy-release-remote-verification.v1','status':status,'tag':TAG,'release_id':d['id'],'html_url':d['html_url'],'checks':checks,'verified_assets':len(checks)}
 vp=ROOT/'state/analysis/V14R2_HEAVY_RELEASE_REMOTE_VERIFICATION_2026-08-31.json';vp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':status,'verified_assets':len(checks),'verification_path':str(vp)},indent=2),flush=True);shutil.rmtree(links,ignore_errors=True);raise SystemExit(0 if status=='PASS' else 2)
if __name__=='__main__':main()
