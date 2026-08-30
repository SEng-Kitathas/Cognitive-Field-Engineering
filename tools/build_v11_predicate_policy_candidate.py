#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter
from pathlib import Path

SEED=92820260830
PRED_ARMS={
    'PREDICATE_NARROW_SLICE':(0,1,0,1),
    'PREDICATE_IDENTIFYING_BASIS':(-3,0,1,3),
}
TRAIN_DOMAINS=('parcel_gate','ingest_lane','transfer_bin')
PRED_EVAL_DOMAIN='freight_buffer'
POLICY_TRAIN_DOMAINS=('routing_desk','dispatch_lane','handoff_gate')
POLICY_EVAL_DOMAIN='release_station'
MODES=('transactional','latest_state')
ACTIONS={
    (False,'transactional'):'accept_all',
    (False,'latest_state'):'accept_all',
    (True,'transactional'):'backpressure_or_fail_explicitly',
    (True,'latest_state'):'drop_oldest_keep_latest',
}

def H(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def hs(s:str)->str:return hashlib.sha256(s.encode('utf-8')).hexdigest()
def dumpjl(p:Path,rows):p.write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def ctx(block:int,j:int,di:int):
    # Keep learner-visible integers two digits where practical so paired arms do not gain token-length cues.
    cap=40+((block*7+j*11+di*5)%45)  # 40..84
    incoming=3+((block+j+di)%7)      # 3..9
    return cap,incoming

def predicate_prompt(domain,cap,queued,incoming):
    return (f"In a {domain}, capacity={cap}, queued={queued}, incoming={incoming}. "
            "Classify condition_z for this state. Return JSON only: {\"condition_z\":true|false}.")
def predicate_target(margin):return {'condition_z':margin>0}
def policy_prompt(domain,overflow,mode,code):
    return (f"In a {domain}, overflow={str(bool(overflow)).lower()}, mode={mode}, case={code}. "
            "Choose the handling action. Return JSON only with action.")
def policy_target(overflow,mode):return {'action':ACTIONS[(bool(overflow),mode)]}
def pair(prompt,target):return [{'role':'user','content':prompt},{'role':'assistant','content':json.dumps(target,sort_keys=True,separators=(',',':'))}]

def make_predicate_train():
    arms={a:[] for a in PRED_ARMS}; sides={a:[] for a in PRED_ARMS}
    rng=random.Random(SEED)
    # 72 blocks = 24 per domain. Paired arms share all contexts and within-block context order.
    for bi in range(72):
        di=bi%3; domain=TRAIN_DOMAINS[di]; local=bi//3
        contexts=[ctx(local,j,di) for j in range(4)]
        order=list(range(4)); rng.shuffle(order)
        contexts=[contexts[j] for j in order]
        for arm,margins0 in PRED_ARMS.items():
            margins=[margins0[j] for j in order]
            msgs=[]; members=[]
            for pos,((cap,inc),margin) in enumerate(zip(contexts,margins)):
                queued=cap-inc+margin
                pr=predicate_prompt(domain,cap,queued,inc); tg=predicate_target(margin); msgs.extend(pair(pr,tg))
                members.append({'position':pos,'domain':domain,'capacity':cap,'incoming':inc,'queued':queued,'margin':margin,'condition_z':margin>0,'context_key':f'{domain}|{cap}|{inc}'})
            pid=f'pred-{bi:03d}'
            arms[arm].append({'id':f'{pid}-{arm}','messages':msgs})
            sides[arm].append({'pair_id':pid,'arm':arm,'domain':domain,'members':members,'target_pattern':[m['condition_z'] for m in members]})
    return arms,sides

def make_predicate_eval():
    rows=[]
    margins=(-7,-3,-1,0,1,3,7)
    for vi in range(8):
        cap=46+vi*5; inc=3+(vi%5)
        for margin in margins:
            queued=cap-inc+margin; pr=predicate_prompt(PRED_EVAL_DOMAIN,cap,queued,inc);tg=predicate_target(margin)
            rows.append({'id':'pe-'+hs(f'{vi}|{margin}|{pr}')[:20],'domain':PRED_EVAL_DOMAIN,'variant':vi,'capacity':cap,'incoming':inc,'queued':queued,'margin':margin,'prompt':pr,'expected':tg,'support_bucket':'negative_slack' if margin<0 else 'equality' if margin==0 else 'near_overflow' if margin==1 else 'far_overflow'})
    return rows

def make_policy_train():
    rows=[]; side=[]; rng=random.Random(SEED^0x51504F4C)
    cells=[(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')]
    for bi in range(72):
        di=bi%3; domain=POLICY_TRAIN_DOMAINS[di]; local=bi//3
        order=list(cells); rng.shuffle(order); msgs=[]; members=[]
        for pos,(ov,mode) in enumerate(order):
            code=f'{chr(65+(local%26))}{di}{pos}';pr=policy_prompt(domain,ov,mode,code);tg=policy_target(ov,mode);msgs.extend(pair(pr,tg));members.append({'position':pos,'overflow':ov,'mode':mode,'action':tg['action'],'case_code':code})
        rows.append({'id':f'policy-{bi:03d}','messages':msgs});side.append({'pair_id':f'policy-{bi:03d}','domain':domain,'members':members})
    return rows,side

def make_policy_eval():
    rows=[]; cells=[(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')]
    for vi in range(12):
        for ov,mode in cells:
            code=f'Z{vi:02d}';pr=policy_prompt(POLICY_EVAL_DOMAIN,ov,mode,code);tg=policy_target(ov,mode)
            rows.append({'id':'poe-'+hs(f'{vi}|{ov}|{mode}|{pr}')[:20],'domain':POLICY_EVAL_DOMAIN,'variant':vi,'overflow':ov,'mode':mode,'prompt':pr,'expected':tg,'action_class':tg['action']})
    return rows

def main(out:Path):
    if out.exists():raise SystemExit('REFUSE_OVERWRITE')
    out.mkdir(parents=True)
    arms,sides=make_predicate_train(); pe=make_predicate_eval(); pol,pols=make_policy_train(); poe=make_policy_eval()
    # Structural fail-closed gates.
    for arm in PRED_ARMS:
        if len(arms[arm])!=72 or len(sides[arm])!=72:raise AssertionError((arm,len(arms[arm]),len(sides[arm])))
        for r,s in zip(arms[arm],sides[arm]):
            if len(r['messages'])!=8 or [m['role'] for m in r['messages']]!=['user','assistant']*4:raise AssertionError(('roles',r['id']))
            if Counter(s['target_pattern'])!=Counter({False:2,True:2}):raise AssertionError(('target_balance',r['id'],s['target_pattern']))
    # Paired context identity and topology.
    for i in range(72):
        a=sides['PREDICATE_NARROW_SLICE'][i];b=sides['PREDICATE_IDENTIFYING_BASIS'][i]
        ak=[(m['domain'],m['capacity'],m['incoming']) for m in a['members']];bk=[(m['domain'],m['capacity'],m['incoming']) for m in b['members']]
        if ak!=bk:raise AssertionError(('paired_context_mismatch',i))
        if sorted(m['margin'] for m in a['members'])!=[0,0,1,1]:raise AssertionError(('narrow_support',i))
        if sorted(m['margin'] for m in b['members'])!=[-3,0,1,3]:raise AssertionError(('identifying_support',i))
    # Learner-visible prompt must not state the target inequality.
    raw='\n'.join(m['content'] for arm in arms.values() for r in arm for m in r['messages'] if m['role']=='user')
    forbidden=['queued + incoming > capacity','queued+incoming>capacity','margin > 0','margin>0','overflow']
    if any(x.lower() in raw.lower() for x in forbidden):raise AssertionError('PREDICATE_SEMANTIC_OR_FORMULA_LEAK')
    if len(pe)!=56 or {r['margin'] for r in pe}!={-7,-3,-1,0,1,3,7}:raise AssertionError('PRED_EVAL_SUPPORT')
    if any(r['domain'] in TRAIN_DOMAINS for r in pe):raise AssertionError('PRED_EVAL_DOMAIN_OVERLAP')
    if len(pol)!=72 or len(poe)!=48:raise AssertionError(('policy_count',len(pol),len(poe)))
    praw='\n'.join(m['content'] for r in pol for m in r['messages'] if m['role']=='user')
    if any(x in praw for x in ['capacity=','queued=','incoming=']):raise AssertionError('POLICY_ARITHMETIC_LEAK')
    # Every policy block must contain exact 2x2 factorial.
    target_cells={(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')}
    for s in pols:
        if {(m['overflow'],m['mode']) for m in s['members']}!=target_cells:raise AssertionError(('policy_factorial',s['pair_id']))
    # Eval must discriminate cheap predicate rivals.
    def rival(name,m):
        return {'EQ1':m==1,'GE0':m>=0,'NE0':m!=0,'GT1':m>1}[name]
    rivals={}
    for name in ['EQ1','GE0','NE0','GT1']:
        mism=[r['id'] for r in pe if rival(name,r['margin'])!=r['expected']['condition_z']];rivals[name]=len(mism)
        if not mism:raise AssertionError(('RIVAL_NOT_DISCRIMINATED',name))
    files={}
    for arm in PRED_ARMS:
        fn=arm+'.jsonl';dumpjl(out/fn,arms[arm]);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
        fn=arm+'.sidecar.private.jsonl';dumpjl(out/fn,sides[arm]);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
    for fn,rows in [('PREDICATE_EVAL.private.jsonl',pe),('POLICY_FACTORIZED.jsonl',pol),('POLICY_FACTORIZED.sidecar.private.jsonl',pols),('POLICY_EVAL.private.jsonl',poe)]:
        dumpjl(out/fn,rows);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
    manifest={'schema':'cfe.v11.predicate-policy-candidate.v1','status':'CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_LOCKED__NOT_TRAINED','seed':SEED,'predicate_blocks_per_arm':72,'predicate_exposures_per_arm':288,'policy_blocks':72,'policy_exposures':288,'predicate_eval_cases':56,'policy_eval_cases':48,'predicate_train_domains':list(TRAIN_DOMAINS),'predicate_eval_domain':PRED_EVAL_DOMAIN,'policy_train_domains':list(POLICY_TRAIN_DOMAINS),'policy_eval_domain':POLICY_EVAL_DOMAIN,'paired_predicate_context_identity':True,'predicate_target_balance_per_block':'2 false / 2 true both arms','predicate_formula_not_supplied':True,'predicate_semantic_overflow_word_not_supplied':True,'policy_arithmetic_absent':True,'predicate_rival_mismatch_counts':rivals,'files':files,'laws':['PREDICATE_IDENTIFICATION != ACTION_POLICY_SELECTION','IDENTIFYING_BASIS != RICH_TRUTH_TABLE','CANDIDATE_GENERATION != SCIENTIFIC_START','NEW_DOMAIN != INDEPENDENT_REPLICATION']}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();main(a.out)
