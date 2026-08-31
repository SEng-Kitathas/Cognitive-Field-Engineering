#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter
from pathlib import Path

SEED=120260830
PRED_ARMS={
  'PREDICATE_NARROW_V12':(0,1,0,1),
  'PREDICATE_IDENTIFYING_V12':(-3,0,1,3),
}
PRED_TRAIN_DOMAINS=('signal_bay','cargo_node','transfer_cell')
POLICY_TRAIN_DOMAINS=('mode_desk','routing_cell','handoff_node')
PRED_EVAL_DOMAIN='reserve_gate'
POLICY_EVAL_DOMAIN='control_desk'
COMPOSE_EVAL_DOMAIN='allocation_gate'
MODES=('transactional','latest_state')
ACTIONS={(False,'transactional'):'action_r',(False,'latest_state'):'action_r',(True,'transactional'):'action_s',(True,'latest_state'):'action_t'}

def H(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def hs(s:str)->str:return hashlib.sha256(s.encode('utf-8')).hexdigest()
def dumpjl(p:Path,rows):p.write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def pair(prompt,target):return [{'role':'user','content':prompt},{'role':'assistant','content':json.dumps(target,sort_keys=True,separators=(',',':'))}]
def ctx(block:int,j:int,di:int):
    cap=44+((block*9+j*13+di*7)%41)  # 44..84
    inc=2+((block*3+j+di)%8)         # 2..9
    return cap,inc

def pred_prompt(domain,cap,queued,inc):
    return f"In {domain}, capacity={cap}, queued={queued}, incoming={inc}. Classify condition_z. Return JSON only with condition_z."
def pred_target(m):return {'condition_z':m>0}
def policy_prompt(domain,z,mode,code):
    return f"In {domain}, condition_z={str(bool(z)).lower()}, mode={mode}, case={code}. Choose the action. Return JSON only with action."
def policy_target(z,mode):return {'action':ACTIONS[(bool(z),mode)]}
def compose_prompt(domain,cap,queued,inc,mode,code):
    return f"In {domain}, capacity={cap}, queued={queued}, incoming={inc}, mode={mode}, case={code}. Choose the action. Return JSON only with action."

def build_predicate_train():
    arms={a:[] for a in PRED_ARMS}; sides={a:[] for a in PRED_ARMS};rng=random.Random(SEED)
    for bi in range(72):
        di=bi%3;domain=PRED_TRAIN_DOMAINS[di];local=bi//3;contexts=[ctx(local,j,di) for j in range(4)];order=list(range(4));rng.shuffle(order);contexts=[contexts[j] for j in order]
        for arm,m0 in PRED_ARMS.items():
            margins=[m0[j] for j in order];msgs=[];members=[]
            for pos,((cap,inc),m) in enumerate(zip(contexts,margins)):
                q=cap-inc+m;pr=pred_prompt(domain,cap,q,inc);tg=pred_target(m);msgs.extend(pair(pr,tg));members.append({'position':pos,'domain':domain,'capacity':cap,'incoming':inc,'queued':q,'margin':m,'condition_z':m>0,'context_key':f'{domain}|{cap}|{inc}'})
            pid=f'v12p-{bi:03d}';arms[arm].append({'id':f'{pid}-{arm}','messages':msgs});sides[arm].append({'pair_id':pid,'arm':arm,'domain':domain,'members':members,'target_pattern':[x['condition_z'] for x in members]})
    return arms,sides

def build_policy_train():
    rows=[];side=[];rng=random.Random(SEED^0xBEEF);cells=[(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')]
    for bi in range(72):
        di=bi%3;domain=POLICY_TRAIN_DOMAINS[di];local=bi//3;order=list(cells);rng.shuffle(order);msgs=[];members=[]
        for pos,(z,mode) in enumerate(order):
            code=f'Q{di}{local:02d}{pos}';pr=policy_prompt(domain,z,mode,code);tg=policy_target(z,mode);msgs.extend(pair(pr,tg));members.append({'position':pos,'condition_z':z,'mode':mode,'action':tg['action'],'case_code':code})
        rows.append({'id':f'v12policy-{bi:03d}','messages':msgs});side.append({'pair_id':f'v12policy-{bi:03d}','domain':domain,'members':members})
    return rows,side

def build_pred_eval():
    rows=[];margins=(-7,-2,0,1,4,9)
    for vi in range(8):
        cap=48+vi*4;inc=2+(vi%6)
        for m in margins:
            q=cap-inc+m;pr=pred_prompt(PRED_EVAL_DOMAIN,cap,q,inc);tg=pred_target(m)
            rows.append({'id':'v12pe-'+hs(f'{vi}|{m}|{pr}')[:18],'domain':PRED_EVAL_DOMAIN,'variant':vi,'capacity':cap,'incoming':inc,'queued':q,'margin':m,'prompt':pr,'expected':tg,'truth_side':'false' if m<=0 else 'true','support_bucket':'far_negative' if m<0 else 'equality' if m==0 else 'near_positive' if m==1 else 'far_positive'})
    return rows

def build_policy_eval():
    rows=[];cells=[(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')]
    for vi in range(12):
        for z,mode in cells:
            code=f'R{vi:02d}';pr=policy_prompt(POLICY_EVAL_DOMAIN,z,mode,code);tg=policy_target(z,mode)
            rows.append({'id':'v12poe-'+hs(f'{vi}|{z}|{mode}|{pr}')[:18],'domain':POLICY_EVAL_DOMAIN,'variant':vi,'condition_z':z,'mode':mode,'prompt':pr,'expected':tg,'action_class':tg['action']})
    return rows

def build_compose_eval():
    rows=[];margins=(-7,-2,0,1,4,9)
    for vi in range(8):
        cap=51+vi*4;inc=3+(vi%5)
        for m in margins:
            q=cap-inc+m;z=m>0
            for mode in MODES:
                code=f'C{vi:02d}{mode[0]}';pr=compose_prompt(COMPOSE_EVAL_DOMAIN,cap,q,inc,mode,code);tg=policy_target(z,mode)
                rows.append({'id':'v12ce-'+hs(f'{vi}|{m}|{mode}|{pr}')[:18],'domain':COMPOSE_EVAL_DOMAIN,'variant':vi,'capacity':cap,'incoming':inc,'queued':q,'margin':m,'condition_z':z,'mode':mode,'prompt':pr,'expected':tg,'action_class':tg['action'],'truth_side':'false' if not z else 'true','support_bucket':'far_negative' if m<0 else 'equality' if m==0 else 'near_positive' if m==1 else 'far_positive'})
    return rows

def main(out:Path):
    if out.exists():raise SystemExit('REFUSE_OVERWRITE')
    out.mkdir(parents=True);arms,sides=build_predicate_train();policy,polside=build_policy_train();pe=build_pred_eval();poe=build_policy_eval();ce=build_compose_eval()
    # Structural gates
    for arm in PRED_ARMS:
        if len(arms[arm])!=72 or len(sides[arm])!=72:raise AssertionError(('COUNT',arm))
        for r,s in zip(arms[arm],sides[arm]):
            if len(r['messages'])!=8 or [m['role'] for m in r['messages']]!=['user','assistant']*4:raise AssertionError(('ROLE',r['id']))
            if Counter(s['target_pattern'])!=Counter({False:2,True:2}):raise AssertionError(('BAL',r['id']))
    a0,a1=list(PRED_ARMS)
    for i,(a,b) in enumerate(zip(sides[a0],sides[a1])):
        ak=[(x['domain'],x['capacity'],x['incoming']) for x in a['members']];bk=[(x['domain'],x['capacity'],x['incoming']) for x in b['members']]
        if ak!=bk:raise AssertionError(('CTX',i))
        if sorted(x['margin'] for x in a['members'])!=[0,0,1,1]:raise AssertionError(('NARROW',i))
        if sorted(x['margin'] for x in b['members'])!=[-3,0,1,3]:raise AssertionError(('IDENT',i))
    if len(policy)!=72 or len(polside)!=72:raise AssertionError('POLCOUNT')
    cells={(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')}
    for s in polside:
        if {(x['condition_z'],x['mode']) for x in s['members']}!=cells:raise AssertionError(('POLFACT',s['pair_id']))
    if len(pe)!=48 or len(poe)!=48 or len(ce)!=96:raise AssertionError(('EVAL_COUNTS',len(pe),len(poe),len(ce)))
    if Counter(x['condition_z'] for x in ce)!=Counter({False:48,True:48}):raise AssertionError('COMPOSE_TRUTH_BALANCE')
    if Counter(x['action_class'] for x in ce)!=Counter({'action_r':48,'action_s':24,'action_t':24}):raise AssertionError('COMPOSE_ACTION_COUNTS')
    # Learner-visible semantic leak gates
    forbidden=('overflow','backpressure','drop_oldest','accept_all','queued + incoming > capacity','margin')
    all_user=[]
    for arm in arms.values():all_user.extend(m['content'].lower() for r in arm for m in r['messages'] if m['role']=='user')
    all_user.extend(m['content'].lower() for r in policy for m in r['messages'] if m['role']=='user')
    all_user.extend(x['prompt'].lower() for x in pe+poe+ce)
    if any(term in text for term in forbidden for text in all_user):raise AssertionError('SEMANTIC_LEAK')
    # No joint training example may have both numeric state and mode/action target.
    for arm in arms.values():
        for r in arm:
            for m in r['messages']:
                if m['role']=='user' and 'mode=' in m['content']:raise AssertionError('PRED_JOINT_LEAK')
    for r in policy:
        for m in r['messages']:
            if m['role']=='user' and any(x in m['content'] for x in ['capacity=','queued=','incoming=']):raise AssertionError('POLICY_NUMERIC_LEAK')
    # Training/eval domain separation
    train_domains=set(PRED_TRAIN_DOMAINS)|set(POLICY_TRAIN_DOMAINS);eval_domains={PRED_EVAL_DOMAIN,POLICY_EVAL_DOMAIN,COMPOSE_EVAL_DOMAIN}
    if train_domains & eval_domains:raise AssertionError('DOMAIN_OVERLAP')
    files={}
    for arm in PRED_ARMS:
        for suffix,rows in [('.jsonl',arms[arm]),('.sidecar.private.jsonl',sides[arm])]:
            fn=arm+suffix;dumpjl(out/fn,rows);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
    for fn,rows in [('POLICY_Z_SHARED.jsonl',policy),('POLICY_Z_SHARED.sidecar.private.jsonl',polside),('PREDICATE_EVAL.private.jsonl',pe),('POLICY_EVAL.private.jsonl',poe),('COMPOSE_EVAL.private.jsonl',ce)]:
        dumpjl(out/fn,rows);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
    manifest={'schema':'cfe.v12.factor-primitive-composition-candidate.v1','status':'CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_LOCKED__NOT_TRAINED','seed':SEED,'predicate_train_domains':list(PRED_TRAIN_DOMAINS),'policy_train_domains':list(POLICY_TRAIN_DOMAINS),'eval_domains':sorted(eval_domains),'predicate_rows_per_arm':72,'policy_rows_shared':72,'total_training_rows_per_arm':144,'predicate_exposures_per_arm':288,'policy_exposures_per_arm':288,'joint_training_examples':0,'predicate_context_identity':True,'predicate_target_balance':'2 false / 2 true per block','policy_factorial':'exact 2x2 condition_z x mode per block','composed_eval_cases':96,'composed_truth_balance':'48 false / 48 true','composed_action_counts':{'action_r':48,'action_s':24,'action_t':24},'semantic_action_overflow_terms_absent':True,'files':files,'laws':['PRIMITIVE_ACQUISITION != COMPOSITION','JOINT_TRAINING_EXAMPLE_COUNT = 0','SHARED_INTERFACE_SYMBOL != SHARED_JOINT_TARGET','CANDIDATE_GENERATION != SCIENTIFIC_START']}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(manifest,indent=2,sort_keys=True))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();main(a.out)
