#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter, defaultdict
from pathlib import Path

SEED=81120260830
K4_OFFSETS=(0,2,4,6)
K2_PARTITIONS=((0,0,4,4),(0,4,0,4),(0,4,4,0))

def H(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def loadjl(p:Path):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def dumpjl(p:Path,rows):p.write_text('\n'.join(json.dumps(r,sort_keys=True,separators=(',',':')) for r in rows)+'\n',encoding='utf-8',newline='\n')
def cell_key(w):return json.dumps(w['curator_factors'],sort_keys=True,separators=(',',':'))
def target(w):return json.dumps(w['consequence'],sort_keys=True,separators=(',',':'))

def render(w):
    fam=w['field_family'];d=w['domain'];s=w['state'];e=w['entities']
    if fam=='dependency_currentness':
        p=(f"In a {d}, objects {e['source_a']}, {e['source_b']}, and {e['target']} are tracked. The recorded dependency is parent({e['target']})={s['parent']}. "
           f"Before an update, {e['source_a']} and {e['source_b']} are version {s['version_before']}. Then {s['changed_source']} advances to version {s['version_after']}. "
           f"After that update, rebuild({e['target']})={'yes' if s['rebuilt'] else 'no'}. A target is current exactly when its recorded actual-parent version matches the current version of that actual parent. Return JSON only: {{\"current\":true|false}}.")
    elif fam=='bounded_transport':
        p=(f"A {d} has capacity {s['capacity']} {e['unit']}, queued {s['queued']}, incoming {s['incoming']}, mode {s['mode']}. Overflow is strict: queued + incoming > capacity. If no overflow, accept_all. If overflow in transactional mode, backpressure_or_fail_explicitly. If overflow in latest_state mode, drop_oldest_keep_latest. Return JSON only with action.")
    elif fam=='warrant_vs_taint':
        p=(f"In a {d} evidence graph, origin({e['evidence_a']})={s['origin_a']} and origin({e['evidence_b']})={s['origin_b']}. Roots {e['root_a']} and {e['root_b']} are distinct. Review {s['review_code']}. The primary line is {'tainted' if s['primary_tainted'] else 'clean'}. Evidence lines are independent only when their root ancestry is disjoint. Independent clean corroboration can restore proposition warrant but does not erase taint ancestry. Return JSON only with proposition_warranted and taint_present booleans.")
    else:raise ValueError(fam)
    return p,target(w)

def pair(w):
    p,a=render(w);return [{'role':'user','content':p},{'role':'assistant','content':a}]

def compile(field:Path,out:Path):
    worlds=loadjl(field)
    if len(worlds)!=288:raise AssertionError(('source_count',len(worlds)))
    by=defaultdict(lambda:defaultdict(dict))
    for w in worlds:
        by[(w['field_family'],w['domain'])][w['neighborhood_id']][cell_key(w)]=w
    for g,nbs in by.items():
        if len(nbs)!=8:raise AssertionError((g,'nbs',len(nbs)))
        supports={tuple(sorted(x)) for x in nbs.values()}
        if len(supports)!=1 or len(next(iter(supports)))!=4:raise AssertionError((g,'cell_support'))
    rng=random.Random(SEED);groups=sorted(by);rng.shuffle(groups)
    arms={'K1_TRUE_NEIGHBORHOOD':[],'K2_PAIRED_NEIGHBORHOODS':[],'K4_STRICT_SCRAMBLE':[]}
    sides={k:[] for k in arms}; pair_index=0
    for group_index,g in enumerate(groups):
        nids=sorted(by[g]);rot=rng.randrange(8);nids=nids[rot:]+nids[:rot]
        cells=sorted(next(iter(by[g].values())).keys());rng.shuffle(cells)
        for i,nid in enumerate(nids):
            maps={
              'K1_TRUE_NEIGHBORHOOD':(0,0,0,0),
              'K2_PAIRED_NEIGHBORHOODS':K2_PARTITIONS[group_index%3],
              'K4_STRICT_SCRAMBLE':K4_OFFSETS,
            }
            ref_targets=None
            for arm,offs in maps.items():
                ws=[by[g][nids[(i+offs[j])%8]][ck] for j,ck in enumerate(cells)]
                tg=[target(w) for w in ws]
                if ref_targets is None:ref_targets=tg
                elif tg!=ref_targets:raise AssertionError(('target_mismatch',pair_index,arm))
                msgs=[]
                for w in ws:msgs.extend(pair(w))
                pid=f'pair-{pair_index:03d}'
                arms[arm].append({'id':f'{pid}-{arm[:2]}','messages':msgs})
                sides[arm].append({'pair_id':pid,'arm':arm,'family':g[0],'domain':g[1],'member_source_ids':[w['field_object_id'] for w in ws],'member_neighborhood_ids':[w['neighborhood_id'] for w in ws],'cell_keys':cells,'assistant_targets':tg,'offsets':list(offs)})
            pair_index+=1
    if pair_index!=72:raise AssertionError(pair_index)
    # global individual experience multiset and source use parity
    def experiences(rows):return Counter(json.dumps(r['messages'][j:j+2],sort_keys=True,separators=(',',':')) for r in rows for j in range(0,8,2))
    ref=None
    source_ref=None
    topo={'K1_TRUE_NEIGHBORHOOD':1,'K2_PAIRED_NEIGHBORHOODS':2,'K4_STRICT_SCRAMBLE':4}
    for arm in arms:
        if len(arms[arm])!=72:raise AssertionError((arm,len(arms[arm])))
        ex=experiences(arms[arm]); src=Counter(x for s in sides[arm] for x in s['member_source_ids'])
        if len(src)!=288 or set(src.values())!={1}:raise AssertionError((arm,'source_once'))
        if any(len(set(s['member_neighborhood_ids']))!=topo[arm] for s in sides[arm]):raise AssertionError((arm,'topology'))
        if ref is None:ref=ex;source_ref=src
        elif ex!=ref or src!=source_ref:raise AssertionError((arm,'global_multiset'))
    # paired family/domain/cell/target equality
    for i in range(72):
        sigs=[]
        for arm in arms:
            s=sides[arm][i];sigs.append((s['family'],s['domain'],tuple(s['cell_keys']),tuple(s['assistant_targets'])))
        if len(set(map(repr,sigs)))!=1:raise AssertionError(('paired_signature',i))
    # K2 partition balance
    pcounts=Counter(tuple(s['offsets']) for s in sides['K2_PAIRED_NEIGHBORHOODS'])
    if pcounts!=Counter({p:24 for p in K2_PARTITIONS}):raise AssertionError(('k2_balance',pcounts))
    out.mkdir(parents=True,exist_ok=False)
    files={}
    for arm in arms:
        for suffix,rows in [('.jsonl',arms[arm]),('.sidecar.private.jsonl',sides[arm])]:
            fn=arm+suffix;dumpjl(out/fn,rows);files[fn]={'bytes':(out/fn).stat().st_size,'sha256':H((out/fn).read_bytes())}
    manifest={'schema':'cfe.v11.neighborhood-concentration-candidate.v1','status':'CANDIDATE_GENERATED__NOT_TOKEN_QUALIFIED__NOT_PREREGISTERED','source_field':str(field),'source_field_sha256':H(field.read_bytes()),'seed':SEED,'pairs':72,'arms':{a:{'distinct_neighborhoods_per_block':topo[a]} for a in arms},'k2_partition_counts':{str(k):v for k,v in pcounts.items()},'global_individual_experience_multiset_equal':True,'global_source_multiset_equal':True,'each_source_once_per_arm':True,'paired_family_domain_cell_target_sequence_equal':True,'files':files,'laws':['CANDIDATE_GENERATION != SCIENTIFIC START','GLOBAL EXPERIENCE PARITY != TOKEN BURDEN PARITY','NEIGHBORHOOD CONCENTRATION != GENERAL RELATIONAL LEARNING']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--field',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();compile(a.field,a.out)
