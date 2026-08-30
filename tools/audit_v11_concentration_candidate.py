#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, py_compile
from collections import Counter
from pathlib import Path

def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root:Path,out:Path):
    failures=[];checks=[]
    def chk(cond,name,detail=None):
        checks.append({'check':name,'pass':bool(cond),'detail':detail})
        if not cond:failures.append(f'{name}: {detail}')
    cand=root/'state/candidates/v11_concentration_20260830'; ev=root/'state/candidates/v11_fresh_eval_compiled_20260830'
    arms=['K1_TRUE_NEIGHBORHOOD','K2_PAIRED_NEIGHBORHOODS','K4_STRICT_SCRAMBLE']; topo=dict(zip(arms,[1,2,4]))
    m=json.loads((cand/'manifest.json').read_text(encoding='utf-8')); chk(m.get('status')=='CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_PREREGISTERED','candidate_status_prelock')
    ex_ref=None;src_ref=None
    for arm in arms:
        rows=jl(cand/(arm+'.jsonl')); side=jl(cand/(arm+'.sidecar.private.jsonl'))
        chk(len(rows)==len(side)==72,f'{arm}_rows_72')
        exp=Counter();src=Counter()
        for r,s in zip(rows,side):
            chk(set(r)=={'id','messages'},f'{arm}_{r.get("id")}_learner_keys')
            chk(len(r['messages'])==8 and [x['role'] for x in r['messages']]==['user','assistant']*4,f'{arm}_{r.get("id")}_roles')
            chk(len(set(s['member_neighborhood_ids']))==topo[arm],f'{arm}_{r.get("id")}_topology')
            src.update(s['member_source_ids'])
            for i in range(0,8,2):exp[json.dumps(r['messages'][i:i+2],sort_keys=True,separators=(',',':'))]+=1
        chk(len(src)==288 and set(src.values())=={1},f'{arm}_each_source_once')
        raw=(cand/(arm+'.jsonl')).read_text(encoding='utf-8');bad=[x for x in ['neighborhood_id','field_object_id','curator_factors','cell_keys','source_object_id','ancestry_hash'] if x in raw];chk(not bad,f'{arm}_no_curator_metadata',bad)
        if ex_ref is None:ex_ref,src_ref=exp,src
        else:chk(exp==ex_ref and src==src_ref,f'{arm}_global_parity')
    k2=jl(cand/'K2_PAIRED_NEIGHBORHOODS.sidecar.private.jsonl'); pc=Counter(tuple(x['offsets']) for x in k2);chk(sorted(pc.values())==[24,24,24],'k2_partition_balance',{str(k):v for k,v in pc.items()})
    ta=json.loads((cand/'TOKEN_AUDIT.json').read_text(encoding='utf-8'));chk(ta.get('status')=='PASS','token_audit_pass');chk(len({v['global_tokens'] for v in ta['stats'].values()})==1,'token_global_equal');chk(len({v['supervised_tokens'] for v in ta['stats'].values()})==1,'supervision_global_equal')
    oa=json.loads((ev/'OVERLAP_AUDIT.json').read_text(encoding='utf-8'));chk(oa.get('status')=='PASS','fresh_eval_overlap_pass');chk(oa.get('new_field_overlap_with_training_individual_experiences')==0 and oa.get('new_field_overlap_with_old_eval')==0 and oa.get('new_lhit_overlap_with_old_eval')==0,'fresh_eval_zero_exact_overlap')
    sched=json.loads((root/'state/next_steps/V11_FRESH_SEED_ARM_ORDER_2026-08-30.json').read_text(encoding='utf-8'));orders=[tuple(v) for v in sched['execution_order'].values()];chk(len(set(orders))==6,'all_six_permutations_once');pos=Counter((arm,i) for o in orders for i,arm in enumerate(o));chk(all(pos[(a,i)]==2 for a in arms for i in range(3)),'arm_position_balance',dict((str(k),v) for k,v in pos.items()))
    for p in [root/'tools/build_v11_concentration_screen.py',root/'tools/build_v11_fresh_eval_source.py']:
        try:py_compile.compile(str(p),doraise=True);chk(True,'compile_'+p.name)
        except Exception as e:chk(False,'compile_'+p.name,repr(e))
    report={'schema':'cfe.v11.static-hostile-candidate.v1','status':'PASS_CANDIDATE__NOT_LOCKED__NOT_RUNTIME_QUALIFIED__NOT_TRAINED' if not failures else 'FAIL','failures':failures,'check_count':len(checks),'checks':checks,'bindings':{'candidate_manifest_sha256':H(cand/'manifest.json'),'token_audit_sha256':H(cand/'TOKEN_AUDIT.json'),'fresh_eval_overlap_audit_sha256':H(ev/'OVERLAP_AUDIT.json'),'seed_order_sha256':H(root/'state/next_steps/V11_FRESH_SEED_ARM_ORDER_2026-08-30.json')},'claims_not_authorized':['scientific start','runtime qualification','blind evaluation','independent replication','CFE effect']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':report['status'],'check_count':report['check_count'],'failures':failures,'bindings':report['bindings']},indent=2,sort_keys=True));
    if failures:raise SystemExit(2)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/qualification/V11_STATIC_HOSTILE_CANDIDATE_2026-08-30.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
