#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, py_compile
from collections import Counter
from pathlib import Path

def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(root:Path,out:Path):
    cand=root/'state/candidates/v12_factor_primitive_composition_20260830';prereg=root/'state/next_steps/V12_FACTOR_PRIMITIVE_COMPOSITION_PREREG_DRAFT_2026-08-30.json';fail=[];checks=[]
    def chk(cond,name,detail=None):
        checks.append({'check':name,'pass':bool(cond),'detail':detail})
        if not cond:fail.append(f'{name}: {detail}')
    man=json.loads((cand/'MANIFEST.json').read_text());ta=json.loads((cand/'TOKEN_SCHEDULE_AUDIT.json').read_text());pr=json.loads(prereg.read_text())
    chk(pr.get('status')=='FROZEN_DRAFT_BEFORE_ANY_V12_MODEL_OUTCOME','prereg_status');chk(H(prereg)=='e929a4ab201a86faaf7f910438b53e1349d4ac2a7a0d29a960d1381392657bf9','prereg_hash');chk(man.get('status')=='CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_LOCKED__NOT_TRAINED','candidate_status');chk(ta.get('status')=='PASS','token_schedule_pass')
    arms=['PREDICATE_NARROW_V12','PREDICATE_IDENTIFYING_V12'];side={}
    for arm in arms:
        rows=jl(cand/(arm+'.jsonl'));ss=jl(cand/(arm+'.sidecar.private.jsonl'));side[arm]=ss;chk(len(rows)==len(ss)==72,f'{arm}_72')
        for i,(r,s) in enumerate(zip(rows,ss)):
            chk([x['role'] for x in r['messages']]==['user','assistant']*4,f'{arm}_roles_{i}');chk(Counter(s['target_pattern'])==Counter({False:2,True:2}),f'{arm}_balance_{i}')
            user=' '.join(x['content'].lower() for x in r['messages'] if x['role']=='user');chk('mode=' not in user,f'{arm}_no_joint_mode_{i}');chk(all(term not in user for term in ['overflow','margin','backpressure','drop_oldest','accept_all']),f'{arm}_no_semantic_leak_{i}')
    for i,(a,b) in enumerate(zip(side[arms[0]],side[arms[1]])):
        chk([(x['domain'],x['capacity'],x['incoming']) for x in a['members']]==[(x['domain'],x['capacity'],x['incoming']) for x in b['members']],f'paired_context_{i}');chk(sorted(x['margin'] for x in a['members'])==[0,0,1,1],f'narrow_support_{i}');chk(sorted(x['margin'] for x in b['members'])==[-3,0,1,3],f'ident_support_{i}')
    pol=jl(cand/'POLICY_Z_SHARED.jsonl');ps=jl(cand/'POLICY_Z_SHARED.sidecar.private.jsonl');chk(len(pol)==len(ps)==72,'policy_72');cells={(False,'transactional'),(False,'latest_state'),(True,'transactional'),(True,'latest_state')}
    for i,(r,s) in enumerate(zip(pol,ps)):
        chk({(x['condition_z'],x['mode']) for x in s['members']}==cells,f'policy_factorial_{i}');user=' '.join(x['content'].lower() for x in r['messages'] if x['role']=='user');chk(all(term not in user for term in ['capacity=','queued=','incoming=','overflow','backpressure','drop_oldest','accept_all']),f'policy_no_numeric_semantic_{i}')
    pe=jl(cand/'PREDICATE_EVAL.private.jsonl');poe=jl(cand/'POLICY_EVAL.private.jsonl');ce=jl(cand/'COMPOSE_EVAL.private.jsonl');chk(len(pe)==48,'pred_eval_48');chk(len(poe)==48,'policy_eval_48');chk(len(ce)==96,'compose_eval_96');chk(Counter(x['condition_z'] for x in ce)==Counter({False:48,True:48}),'compose_truth_balance');chk(Counter(x['action_class'] for x in ce)==Counter({'action_r':48,'action_s':24,'action_t':24}),'compose_action_counts')
    for i,x in enumerate(ce):
        q=x['prompt'].lower();chk('condition_z' not in q,f'compose_condition_hidden_{i}');chk(all(term not in q for term in ['overflow','margin','backpressure','drop_oldest','accept_all']),f'compose_semantic_hidden_{i}')
    # exact prompt overlap gates across all train user prompts and eval prompts
    trainprompts=[]
    for fn in [arms[0]+'.jsonl',arms[1]+'.jsonl','POLICY_Z_SHARED.jsonl']:
        for r in jl(cand/fn):trainprompts.extend(x['content'] for x in r['messages'] if x['role']=='user')
    evalprompts=[x['prompt'] for x in pe+poe+ce];chk(len(set(evalprompts))==len(evalprompts),'eval_prompt_unique');chk(set(trainprompts).isdisjoint(set(evalprompts)),'train_eval_exact_disjoint')
    # compare against v11 candidate prompt surfaces to ensure exact novelty
    v11=root/'state/candidates/v11_predicate_policy_r2_20260830';v11prompts=[]
    if v11.exists():
        for p in v11.glob('*.jsonl'):
            if 'token_reference' in p.name or 'sidecar' in p.name:continue
            for r in jl(p):
                if 'messages' in r:v11prompts.extend(x['content'] for x in r['messages'] if x['role']=='user')
                elif 'prompt' in r:v11prompts.append(r['prompt'])
    chk(set(trainprompts+evalprompts).isdisjoint(set(v11prompts)),'v11_exact_prompt_disjoint')
    # token/schedule exactness
    a,b=arms;chk(ta['stats'][a]['global_tokens']==ta['stats'][b]['global_tokens'],'pred_global_equal');chk(ta['stats'][a]['supervised_tokens']==ta['stats'][b]['supervised_tokens'],'pred_supervised_equal');chk(ta['predicate_pair_exact_lengths']==72,'pred_pair_lengths_exact');chk(ta['combined_arm_stats'][a]==ta['combined_arm_stats'][b],'combined_burden_exact');chk(ta['combined_arm_stats'][a]['global_tokens']==31200,'combined_tokens_expected');chk(ta['combined_arm_stats'][a]['supervised_tokens']==4608,'combined_supervised_expected');chk(max(x['max_tokens'] for x in ta['stats'].values())<=512,'max_seq_under_512')
    for seed,s in ta['schedules'].items():chk(s['windows']==18 and s['predicate_per_window']==4 and s['policy_per_window']==4,f'schedule_{seed}')
    # code compile
    for p in [root/'tools/build_v12_factor_primitive_composition_candidate.py']:
        try:py_compile.compile(str(p),doraise=True);chk(True,'compile_'+p.name)
        except Exception as e:chk(False,'compile_'+p.name,repr(e))
    report={'schema':'cfe.v12.factor-primitive-composition-static-hostile.v1','status':'PASS_CANDIDATE__BASELINE_ADMISSION_NOT_RUN__NOT_LOCKED__NOT_TRAINED' if not fail else 'FAIL','check_count':len(checks),'failures':fail,'bindings':{'prereg_sha256':H(prereg),'candidate_manifest_sha256':H(cand/'MANIFEST.json'),'token_schedule_audit_sha256':H(cand/'TOKEN_SCHEDULE_AUDIT.json'),'generator_sha256':H(root/'tools/build_v12_factor_primitive_composition_candidate.py')},'claims_not_authorized':['composition effect','scientific start','general CFE law','Developmental CFE']}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':report['status'],'check_count':report['check_count'],'failures':fail,'bindings':report['bindings']},indent=2,sort_keys=True));
    if fail:raise SystemExit(2)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/qualification/V12_FACTOR_PRIMITIVE_STATIC_HOSTILE_2026-08-30.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
