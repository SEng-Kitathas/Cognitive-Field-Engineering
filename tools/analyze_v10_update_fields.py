#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,statistics,math,hashlib
from collections import Counter,defaultdict
from pathlib import Path
TOKEN=re.compile(r'[A-Za-z0-9_]+')
SEEDS=[2026082501,2026082502,2026082503,2026082504,2026082505,2026082506]
ARMS=['TREATMENT_NEIGHBORHOOD','CONTROL_STRICT_CELL_SCRAMBLE']

def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def toks(s):return set(x.lower() for x in TOKEN.findall(s))
def jacc(a,b):
 a,b=toks(a),toks(b);return len(a&b)/len(a|b) if a|b else 1.0

def main(live:Path,run:Path,out:Path):
 field=jl(live/'field/v06/train_field.jsonl'); source={w['field_object_id']:w for w in field}
 arm_rows={a:jl(live/'pilot/first_screen_v09'/f'{a}.jsonl') for a in ARMS}
 arm_side={a:jl(live/'pilot/first_screen_v09'/f'{a}.sidecar.private.jsonl') for a in ARMS}
 result={'schema':'cfe.v10.update-field-analysis.v1','status':'POST_HOC_INSTRUMENTATION__NOT_CAUSAL_CONFIRMATION','definition':'One optimizer-visible update-field = 8 consecutive four-cell sequences = 32 supervised exposures before an optimizer step.','seeds':{}}
 seed_summary=[]
 for seed in SEEDS:
  sr={}
  for arm in ARMS:
   man=json.loads((run/'train'/str(seed)/arm/'RUN_MANIFEST.json').read_text(encoding='utf-8')); order=man['dataset_order']
   if len(order)!=72:raise AssertionError((seed,arm,len(order)))
   windows=[]
   for wi in range(9):
    inds=order[wi*8:(wi+1)*8]; sides=[arm_side[arm][i] for i in inds]; rows=[arm_rows[arm][i] for i in inds]
    fam=Counter(s['family'] for s in sides); dom={s['domain'] for s in sides}; nbs={n for s in sides for n in s['member_neighborhood_ids']}; srcs=[source[x] for s in sides for x in s['member_source_ids']]
    seqtext=[' '.join(m['content'] for m in r['messages'] if m['role']=='user') for r in rows]
    sims=[jacc(seqtext[i],seqtext[j]) for i in range(8) for j in range(i+1,8)]
    rec={'window_index':wi,'sequence_indices':inds,'family_counts':dict(fam),'distinct_families':len(fam),'distinct_domains':len(dom),'distinct_neighborhoods':len(nbs),'mean_pairwise_sequence_lexical_jaccard':statistics.mean(sims),'exposures':32}
    b=[w for w in srcs if w['field_family']=='bounded_transport']
    if b:
      caps=[w['state']['capacity'] for w in b]; inc=[w['state']['incoming'] for w in b]; qs=[w['state']['queued'] for w in b]; margins=[q+i-c for q,i,c in zip(qs,inc,caps)]
      rec['bounded_transport']={'exposures':len(b),'distinct_neighborhoods':len({w['neighborhood_id'] for w in b}),'distinct_capacities':len(set(caps)),'capacity_span':max(caps)-min(caps),'distinct_incoming':len(set(inc)),'incoming_span':max(inc)-min(inc),'distinct_queued':len(set(qs)),'queue_span':max(qs)-min(qs),'distinct_margins':sorted(set(margins)),'mode_counts':dict(Counter(w['state']['mode'] for w in b)),'overflow_counts':{str(k):v for k,v in Counter(w['curator_factors']['overflow'] for w in b).items()}}
    wv=[w for w in srcs if w['field_family']=='warrant_vs_taint']
    if wv:
      rec['warrant_vs_taint']={'exposures':len(wv),'distinct_neighborhoods':len({w['neighborhood_id'] for w in wv}),'distinct_review_codes':len({w['state']['review_code'] for w in wv}),'taint_counts':{str(k):v for k,v in Counter(w['curator_factors']['taint_ancestry_present'] for w in wv).items()},'independence_counts':{str(k):v for k,v in Counter(w['curator_factors']['independent_corroboration'] for w in wv).items()}}
    windows.append(rec)
   sr[arm]={'windows':windows,'mean_distinct_neighborhoods':statistics.mean(w['distinct_neighborhoods'] for w in windows),'mean_distinct_domains':statistics.mean(w['distinct_domains'] for w in windows),'mean_lexical_jaccard':statistics.mean(w['mean_pairwise_sequence_lexical_jaccard'] for w in windows),'mean_bounded_capacity_span':statistics.mean(w['bounded_transport']['capacity_span'] for w in windows if 'bounded_transport'in w),'mean_bounded_distinct_capacities':statistics.mean(w['bounded_transport']['distinct_capacities'] for w in windows if 'bounded_transport'in w)}
  result['seeds'][str(seed)]=sr
  # final structural T-C
  ev={}
  for arm in ARMS:
   em=json.loads((run/'eval'/str(seed)/arm/'EVAL_MANIFEST.json').read_text(encoding='utf-8'));ev[arm]=em['metrics']['structural_combined']['accuracy']
  seed_summary.append({'seed':seed,'structural_delta_T_minus_C':ev[ARMS[0]]-ev[ARMS[1]],'T_mean_bounded_capacity_span':sr[ARMS[0]]['mean_bounded_capacity_span'],'C_mean_bounded_capacity_span':sr[ARMS[1]]['mean_bounded_capacity_span'],'T_mean_distinct_neighborhoods':sr[ARMS[0]]['mean_distinct_neighborhoods'],'C_mean_distinct_neighborhoods':sr[ARMS[1]]['mean_distinct_neighborhoods']})
 result['seed_summary']=seed_summary
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':result['status'],'seed_summary':seed_summary,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2,sort_keys=True))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--live',type=Path,required=True);ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();main(a.live,a.run,a.out)
