#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

MARGINS=(-5,-2,-1,0,1,2,5)
MODES=('transactional','latest_state')
VARIANTS=((23,3),(31,5),(47,7),(61,9))
TIERS=('RULE_EXPLICIT','BOUNDARY_LATENT','FULL_LATENT')

def H(s:str)->str:return hashlib.sha256(s.encode('utf-8')).hexdigest()
def dumpjl(p:Path,rows): p.write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')

def expected(mode,margin):
    if margin<=0:return {'action':'accept_all'}
    return {'action':'backpressure_or_fail_explicitly' if mode=='transactional' else 'drop_oldest_keep_latest'}

def prompt(tier,cap,queued,incoming,mode):
    state=f"A dispatch_reservoir has capacity {cap} packets, queued {queued}, incoming {incoming}, mode {mode}."
    if tier=='RULE_EXPLICIT':
        return state+" Overflow is strict: queued + incoming > capacity. If no overflow, accept_all. If overflow in transactional mode, backpressure_or_fail_explicitly. If overflow in latest_state mode, drop_oldest_keep_latest. Return JSON only with action."
    if tier=='BOUNDARY_LATENT':
        return state+" If there is no overflow, accept_all. If there is overflow in transactional mode, backpressure_or_fail_explicitly. If there is overflow in latest_state mode, drop_oldest_keep_latest. Determine whether overflow is present from the state. Return JSON only with action."
    if tier=='FULL_LATENT':
        return state+" Decide the correct handling action for this state. Return JSON only with action."
    raise ValueError(tier)

def main(out:Path):
    if out.exists():raise SystemExit('REFUSE_OVERWRITE')
    out.mkdir(parents=True)
    rows=[]
    for vi,(cap,inc) in enumerate(VARIANTS):
      for mode in MODES:
        for margin in MARGINS:
          queued=cap-inc+margin
          if queued<0:raise AssertionError('NEG_QUEUE')
          exp=expected(mode,margin)
          state_id=f'v{vi}:{mode}:m{margin:+d}'
          for tier in TIERS:
            pr=prompt(tier,cap,queued,inc,mode)
            rows.append({'schema':'cfe.v10.bounded-latent-diagnostic.v1','id':'diag-'+H(state_id+'|'+tier)[:20],'state_id':state_id,'tier':tier,'family':'bounded_transport','domain':'dispatch_reservoir','capacity':cap,'queued':queued,'incoming':inc,'mode':mode,'margin':margin,'overflow':margin>0,'prompt':pr,'expected':exp,'prompt_sha256':H(pr),'status':'POST_HOC_DIAGNOSTIC__NOT_CONFIRMATORY'})
    if len(rows)!=168:raise AssertionError(len(rows))
    dumpjl(out/'CASES.jsonl',rows)
    # Static identifiability audit against cheap rivals.
    states={(r['state_id'],r['mode'],r['margin'],json.dumps(r['expected'],sort_keys=True)) for r in rows if r['tier']=='RULE_EXPLICIT'}
    if len(states)!=56:raise AssertionError(('states',len(states)))
    def pred(rule,mode,m):
      if rule=='GT0':ov=m>0
      elif rule=='EQ1':ov=m==1
      elif rule=='GE0':ov=m>=0
      elif rule=='NE0':ov=m!=0
      elif rule=='GT1':ov=m>1
      else:raise ValueError(rule)
      if not ov:return {'action':'accept_all'}
      return {'action':'backpressure_or_fail_explicitly' if mode=='transactional' else 'drop_oldest_keep_latest'}
    rivalry={}
    truth=[r for r in rows if r['tier']=='RULE_EXPLICIT']
    for rule in ['EQ1','GE0','NE0','GT1']:
      mism=[r['state_id'] for r in truth if pred(rule,r['mode'],r['margin'])!=r['expected']]
      rivalry[rule]={'mismatch_states':len(mism),'examples':mism[:12]}
      if not mism:raise AssertionError(('RIVAL_NOT_DISCRIMINATED',rule))
    # Tier invariance and support checks.
    bystate={}
    for r in rows:bystate.setdefault(r['state_id'],[]).append(r)
    for sid,rs in bystate.items():
      if {r['tier'] for r in rs}!=set(TIERS):raise AssertionError(('TIERS',sid))
      if len({json.dumps(r['expected'],sort_keys=True) for r in rs})!=1:raise AssertionError(('EXPECTED',sid))
    audit={'schema':'cfe.v10.bounded-latent-diagnostic-audit.v1','status':'PASS_STATIC__POST_HOC_DIAGNOSTIC_ONLY','cases':len(rows),'states':len(bystate),'tiers':list(TIERS),'margins':list(MARGINS),'variants':[{'capacity':c,'incoming':i} for c,i in VARIANTS],'prompt_unique':len({r['prompt_sha256'] for r in rows})==len(rows),'rival_discrimination':rivalry,'laws':['POST_HOC_DIAGNOSTIC != CONFIRMATORY_EVIDENCE','NEW_SUPPORT != NEW_TRAINING','RULE_EXPLICIT != BOUNDARY_LATENT != FULL_LATENT']}
    (out/'STATIC_AUDIT.json').write_text(json.dumps(audit,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    manifest={'schema':'cfe.v10.bounded-latent-diagnostic-manifest.v1','status':'CANDIDATE_READY_FOR_READ_ONLY_EVALUATION','cases_sha256':hashlib.sha256((out/'CASES.jsonl').read_bytes()).hexdigest(),'audit_sha256':hashlib.sha256((out/'STATIC_AUDIT.json').read_bytes()).hexdigest(),'cases_bytes':(out/'CASES.jsonl').stat().st_size,'audit':audit}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();main(a.out)
