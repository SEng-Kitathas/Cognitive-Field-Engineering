#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, py_compile
from collections import Counter
from pathlib import Path

def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root:Path,out:Path):
    cand=root/'state/candidates/v11_predicate_policy_r2_20260830'
    prereg=root/'state/next_steps/V11_PREDICATE_POLICY_MECHANISM_PREREG_DRAFT_2026-08-30.json'
    amend=root/'state/next_steps/V11_PREDICATE_POLICY_PREREG_AMENDMENT_PRE_OUTCOME_2026-08-30.md'
    failures=[]; checks=[]
    def chk(cond,name,detail=None):
        checks.append({'check':name,'pass':bool(cond),'detail':detail})
        if not cond:failures.append(f'{name}: {detail}')
    m=json.loads((cand/'MANIFEST.json').read_text(encoding='utf-8')); ta=json.loads((cand/'TOKEN_AUDIT.json').read_text(encoding='utf-8')); pr=json.loads(prereg.read_text(encoding='utf-8'))
    chk(m['status']=='CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_LOCKED__NOT_TRAINED','candidate_prelock_status')
    chk(ta['status']=='PASS','token_audit_pass')
    chk(pr.get('status')=='FROZEN_DRAFT_V2_PRE_OUTCOME__OPAQUE_PREDICATE_TARGET','prereg_v2_status')
    chk(pr.get('pre_outcome_amendment_sha256')==H(amend),'amendment_binding')
    arms=['PREDICATE_NARROW_SLICE','PREDICATE_IDENTIFYING_BASIS']; side={}
    for arm in arms:
        rows=jl(cand/(arm+'.jsonl')); ss=jl(cand/(arm+'.sidecar.private.jsonl')); side[arm]=ss
        chk(len(rows)==len(ss)==72,f'{arm}_72_blocks')
        for i,(r,s) in enumerate(zip(rows,ss)):
            chk(len(r['messages'])==8 and [x['role'] for x in r['messages']]==['user','assistant']*4,f'{arm}_roles_{i}')
            user=' '.join(x['content'].lower() for x in r['messages'] if x['role']=='user')
            chk('overflow' not in user and 'queued + incoming > capacity' not in user and 'margin' not in user,f'{arm}_no_semantic_formula_leak_{i}')
            chk(Counter(s['target_pattern'])==Counter({False:2,True:2}),f'{arm}_target_balance_{i}')
    for i,(a,b) in enumerate(zip(side[arms[0]],side[arms[1]])):
        ak=[(x['domain'],x['capacity'],x['incoming']) for x in a['members']]; bk=[(x['domain'],x['capacity'],x['incoming']) for x in b['members']]
        chk(ak==bk,f'paired_context_identity_{i}')
        chk(sorted(x['margin'] for x in a['members'])==[0,0,1,1],f'narrow_support_{i}')
        chk(sorted(x['margin'] for x in b['members'])==[-3,0,1,3],f'identifying_support_{i}')
    chk(ta['stats'][arms[0]]['global_tokens']==ta['stats'][arms[1]]['global_tokens'],'predicate_global_token_equal')
    chk(ta['stats'][arms[0]]['supervised_tokens']==ta['stats'][arms[1]]['supervised_tokens'],'predicate_supervised_token_equal')
    chk(ta['predicate_pair_exact_lengths']==72 and ta['predicate_pair_max_abs_length_delta']==0,'predicate_pair_lengths_exact')
    chk(ta['predicate_paired_supervised_equal'],'predicate_paired_supervision_exact')
    pe=jl(cand/'PREDICATE_EVAL.private.jsonl'); chk(len(pe)==56,'predicate_eval_56'); chk({x['margin'] for x in pe}=={-7,-3,-1,0,1,3,7},'predicate_eval_support'); chk(len({x['prompt'] for x in pe})==56,'predicate_eval_unique')
    chk(all('overflow' not in x['prompt'].lower() and 'margin' not in x['prompt'].lower() and 'queued + incoming > capacity' not in x['prompt'].lower() for x in pe),'predicate_eval_no_semantic_formula_leak')
    po=jl(cand/'POLICY_FACTORIZED.jsonl'); ps=jl(cand/'POLICY_FACTORIZED.sidecar.private.jsonl'); chk(len(po)==len(ps)==72,'policy_72_blocks')
    target_cells={(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')}
    for i,(r,s) in enumerate(zip(po,ps)):
        chk({(x['overflow'],x['mode']) for x in s['members']}==target_cells,f'policy_factorial_{i}')
        user=' '.join(x['content'].lower() for x in r['messages'] if x['role']=='user'); chk(all(k not in user for k in ['capacity=','queued=','incoming=']),f'policy_no_arithmetic_{i}')
    poe=jl(cand/'POLICY_EVAL.private.jsonl');chk(len(poe)==48,'policy_eval_48');chk({x['domain'] for x in poe}.isdisjoint(set(m['policy_train_domains'])),'policy_eval_domain_disjoint')
    # Token references must exist and bind exactly.
    for name in arms+['POLICY_FACTORIZED']:
        tr=cand/(name+'.token_reference.private.jsonl');chk(tr.is_file(),f'{name}_token_reference_present');
        if tr.is_file():chk(len(jl(tr))==72,f'{name}_token_reference_72')
    # generator/evaluator support files syntax
    for p in [root/'tools/build_v11_predicate_policy_candidate.py']:
        try:py_compile.compile(str(p),doraise=True);chk(True,'compile_'+p.name)
        except Exception as e:chk(False,'compile_'+p.name,repr(e))
    report={'schema':'cfe.v11.predicate-policy-static-hostile.v1','status':'PASS_CANDIDATE__BASELINE_ADMISSION_NOT_RUN__NOT_LOCKED__NOT_TRAINED' if not failures else 'FAIL','check_count':len(checks),'failures':failures,'checks':checks,'bindings':{'candidate_manifest_sha256':H(cand/'MANIFEST.json'),'token_audit_sha256':H(cand/'TOKEN_AUDIT.json'),'prereg_sha256':H(prereg),'amendment_sha256':H(amend),'generator_sha256':H(root/'tools/build_v11_predicate_policy_candidate.py')},'claims_not_authorized':['scientific start','wrong-basis mechanism confirmed','policy separability confirmed','CFE works']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':report['status'],'check_count':report['check_count'],'failures':failures,'bindings':report['bindings']},indent=2,sort_keys=True));
    if failures:raise SystemExit(2)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/qualification/V11_PREDICATE_POLICY_STATIC_HOSTILE_2026-08-30.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
