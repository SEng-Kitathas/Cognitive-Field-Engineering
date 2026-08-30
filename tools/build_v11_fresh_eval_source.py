#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random
from pathlib import Path
SEED_DEFAULT=71720260830

def H(s:str)->str:return hashlib.sha256(s.encode()).hexdigest()
def dump(p:Path,rows):p.write_text('\n'.join(json.dumps(r,sort_keys=True) for r in rows)+'\n',encoding='utf-8',newline='\n')

def build(seed:int):
    rng=random.Random(seed);rows=[];lh=[]
    # Fresh currentness vocabulary.
    for v in range(12):
        a,b,t='onyx','spruce','hinge';base=53+v*5;parent=a if v%2==0 else b;other=b if parent==a else a
        for changed_parent in [False,True]:
            for rebuilt in [False,True]:
                changed=parent if changed_parent else other;current=not(changed_parent and not rebuilt);key=f'v11eval|cur|{v}|{changed_parent}|{rebuilt}|{seed}'
                rows.append({'schema':'cfe.v11.fresh-eval-field.v1','split':'eval','field_object_id':'v11e-'+H(key)[:20],'ancestry_hash':H(key),'neighborhood_id':f'v11eval:cur:v{v}','field_family':'dependency_currentness','domain':'cargo_ledger','entities':{'source_a':a,'source_b':b,'target':t},'state':{'parent':parent,'other':other,'version_before':base,'changed_source':changed,'version_after':base+1,'rebuilt':rebuilt},'relations':[{'type':'actual_parent','src':parent,'dst':t}],'consequence':{'current':current},'curator_factors':{'changed_source_is_actual_parent':changed_parent,'target_rebuilt_after_change':rebuilt},'nuisance':{'variant':v,'domain_index':0},'status':'FRESH_EVAL_SOURCE__NEVER_TRAIN'})
        changed=a
        for p in [a,b]:
            key=f'v11eval|lhitcur|{v}|{p}|{seed}';lh.append({'schema':'cfe.lhit-source.v0.6','split':'eval','trajectory_id':'v11t-'+H(key)[:20],'pair_id':f'v11eval:lhit:cur:v{v}','field_family':'dependency_currentness','domain':'cargo_ledger','early_state':{'parent':p,'target':t,'source_a':a,'source_b':b,'version':base},'later_events':[{'changed_source':changed,'version_after':base+1},{'rebuild':False},{'nuisance_ticket':800+v}],'consequence':{'current':p!=changed},'counterfactual_axis':'early_actual_parent','status':'FRESH_EVAL_TRAJECTORY__NEVER_TRAIN'})
    # Fresh transport vocabulary.
    for v in range(12):
        cap=26+v*5;inc=5+(v%2)
        for mode in ['transactional','latest_state']:
            for overflow in [False,True]:
                queued=cap-inc+(1 if overflow else 0);action='accept_all' if not overflow else ('backpressure_or_fail_explicitly' if mode=='transactional' else 'drop_oldest_keep_latest');key=f'v11eval|q|{v}|{mode}|{overflow}|{seed}'
                rows.append({'schema':'cfe.v11.fresh-eval-field.v1','split':'eval','field_object_id':'v11e-'+H(key)[:20],'ancestry_hash':H(key),'neighborhood_id':f'v11eval:q:v{v}','field_family':'bounded_transport','domain':'telemetry_ring','entities':{'container':'telemetry_ring','unit':'packets'},'state':{'capacity':cap,'queued':queued,'incoming':inc,'mode':mode},'relations':[{'type':'strict_capacity_boundary','expression':'queued + incoming > capacity'}],'consequence':{'action':action},'curator_factors':{'mode':mode,'overflow':overflow},'nuisance':{'variant':v,'domain_index':0},'status':'FRESH_EVAL_SOURCE__NEVER_TRAIN'})
                key2=f'v11eval|lhitq|{v}|{mode}|{overflow}|{seed}';lh.append({'schema':'cfe.lhit-source.v0.6','split':'eval','trajectory_id':'v11t-'+H(key2)[:20],'pair_id':f'v11eval:lhit:q:v{v}:{mode}','field_family':'bounded_transport','domain':'telemetry_ring','early_state':{'capacity':cap,'queued':queued,'mode':mode,'unit':'packets'},'later_events':[{'incoming':inc},{'nuisance_lamp':70+v}],'consequence':{'action':action},'counterfactual_axis':'early_queued_state','status':'FRESH_EVAL_TRAJECTORY__NEVER_TRAIN'})
    # Fresh provenance vocabulary; review codes M-X.
    codes=[chr(ord('M')+v) for v in range(12)]
    for v,code in enumerate(codes):
        e1,e2,r1,r2='violet','ash','canyon','fern'
        for taint in [False,True]:
            for indep in [False,True]:
                o2=r2 if indep else r1;warranted=(not taint) or indep;key=f'v11eval|p|{v}|{taint}|{indep}|{seed}'
                rows.append({'schema':'cfe.v11.fresh-eval-field.v1','split':'eval','field_object_id':'v11e-'+H(key)[:20],'ancestry_hash':H(key),'neighborhood_id':f'v11eval:p:v{v}','field_family':'warrant_vs_taint','domain':'audit_dossier','entities':{'evidence_a':e1,'evidence_b':e2,'root_a':r1,'root_b':r2},'state':{'primary_tainted':taint,'origin_a':r1,'origin_b':o2,'review_code':code},'relations':[{'type':'origin','src':e1,'dst':r1},{'type':'origin','src':e2,'dst':o2}],'consequence':{'proposition_warranted':warranted,'taint_present':taint},'curator_factors':{'taint_ancestry_present':taint,'independent_corroboration':indep},'nuisance':{'variant':v,'domain_index':0},'status':'FRESH_EVAL_SOURCE__NEVER_TRAIN'})
        for indep in [False,True]:
            o2=r2 if indep else r1;key=f'v11eval|lhitp|{v}|{indep}|{seed}';lh.append({'schema':'cfe.lhit-source.v0.6','split':'eval','trajectory_id':'v11t-'+H(key)[:20],'pair_id':f'v11eval:lhit:p:v{v}','field_family':'warrant_vs_taint','domain':'audit_dossier','early_state':{'evidence_a':e1,'evidence_b':e2,'root_a':r1,'root_b':r2,'origin_a':r1,'origin_b':o2},'later_events':[{'primary_tainted':True},{'nuisance_note':90+v}],'consequence':{'proposition_warranted':indep,'taint_present':True},'counterfactual_axis':'early_evidence_root_ancestry','status':'FRESH_EVAL_TRAJECTORY__NEVER_TRAIN'})
    rng.shuffle(rows);rng.shuffle(lh);return rows,lh

def main(out:Path,seed:int):
    if out.exists():raise SystemExit('REFUSE_OVERWRITE')
    out.mkdir(parents=True);rows,lh=build(seed)
    if len(rows)!=144 or len(lh)!=96:raise AssertionError((len(rows),len(lh)))
    dump(out/'eval_field_fresh.private.jsonl',rows);dump(out/'eval_lhit_fresh.private.jsonl',lh)
    m={'schema':'cfe.v11.fresh-eval-source.v1','status':'FRESH_HELDOUT_SURFACE__SAME_RESEARCH_AGENT_NOT_INDEPENDENT_REPLICATION','seed_commitment_sha256':H(str(seed)),'field_objects':len(rows),'lhit_objects':len(lh),'domains':sorted({r['domain'] for r in rows}),'families':sorted({r['field_family'] for r in rows}),'claims_not_authorized':['blind evaluation','independent replication','external transfer']}
    for fn in ['eval_field_fresh.private.jsonl','eval_lhit_fresh.private.jsonl']:
        p=out/fn;m[fn+'_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();m[fn+'_bytes']=p.stat().st_size
    (out/'manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seed',type=int,default=SEED_DEFAULT);a=ap.parse_args();main(a.out,a.seed)
