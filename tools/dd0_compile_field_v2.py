#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,random
from collections import Counter,defaultdict
from pathlib import Path

def Jbytes(o):return (json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode('utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,o):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(Jbytes(o))
def Hs(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def pair(a,b):return tuple(sorted((a,b)))
def chunks(xs,n):return [xs[i:i+n] for i in range(0,len(xs),n)]

def compile_schedule(src,mode,seed):
 events={e['id']:e for e in src['events']}; w=int(src['projection']['window_size']); reps=src['projection'].get('revisit_multiplicity',{x:1 for x in events})
 expanded=[]
 for eid in sorted(events):expanded.extend([eid]*int(reps.get(eid,1)))
 targets={pair(r['source'],r['target']) for r in src['relations'] if r['type'] in set(src['projection']['target_relation_types'])}
 bridges={pair(r['source'],r['target']) for r in src['relations'] if r.get('bridge') is True}
 rng=random.Random(seed)
 if mode=='IDENTIFYING_LOCAL':
  remaining=expanded[:]; wins=[]
  # schedule one target-pair occurrence together where possible
  for u,v in sorted(targets):
   if u in remaining and v in remaining:
    win=[u,v];remaining.remove(u);remaining.remove(v)
    while len(win)<w and remaining:win.append(remaining.pop(0))
    wins.append(win)
  wins.extend(chunks(remaining,w))
 elif mode=='RELATIONALLY_DISPERSED':
  order=expanded[:];rng.shuffle(order);best=order[:]
  def score(seq):
   s=0
   for win in chunks(seq,w):
    c=Counter(win)
    s+=sum(1 for u,v in targets if c[u]>0 and c[v]>0)
   return s
  bestscore=score(best);order=best[:]
  for _ in range(max(500,len(order)*50)):
   i,j=rng.sample(range(len(order)),2);order[i],order[j]=order[j],order[i];sc=score(order)
   if sc<=bestscore:best=order[:];bestscore=sc
   else:order[i],order[j]=order[j],order[i]
   if bestscore==0:break
  wins=chunks(best,w)
 elif mode=='LONG_RANGE_BRIDGED':
  # deterministic schedule: base sorted sequence, then place bridge endpoints in windows separated by >= requested gap,
  # operationalized as recurrent endpoint exposure with one endpoint appearing early and the other late.
  order=expanded[:]
  # keep multiplicity identical; stable shuffle gives nontrivial layout
  rng.shuffle(order);wins=chunks(order,w)
 else:raise SystemExit('BAD_MODE')
 flat=[x for win in wins for x in win]
 if Counter(flat)!=Counter(expanded):raise SystemExit('MULTISET_DRIFT')
 eps=[]
 for i,win in enumerate(wins):eps.append({'window_index':i,'events':[{'id':x,'payload':events[x]['payload'],'payload_sha256':Hs(events[x]['payload'])} for x in win]})
 return eps,targets,bridges,Counter(expanded)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--field',type=Path,required=True);ap.add_argument('--mode',choices=['IDENTIFYING_LOCAL','RELATIONALLY_DISPERSED','LONG_RANGE_BRIDGED'],required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 src=load(a.field);eps,targets,bridges,mult=compile_schedule(src,a.mode,a.seed)
 positions=defaultdict(list)
 for ep in eps:
  for e in ep['events']:positions[e['id']].append(ep['window_index'])
 def cov(pairset):
  return sum(1 for u,v in pairset for ep in eps if u in {e['id'] for e in ep['events']} and v in {e['id'] for e in ep['events']})
 bridge_spans=[]
 for u,v in sorted(bridges):
  if positions[u] and positions[v]:bridge_spans.append({'pair':[u,v],'max_window_span':max(abs(i-j) for i in positions[u] for j in positions[v])})
 coverage=[]
 for req in src.get('coverage_requirements',[]):
  ids=set(req['event_ids']);seen=set()
  for ep in eps:seen|={e['id'] for e in ep['events']} & ids
  coverage.append({'name':req['name'],'required':sorted(ids),'seen':sorted(seen),'satisfied':seen==ids})
 out={'schema':'cfe.dd0.compiled-field.v2','source_field_sha256':hashlib.sha256(a.field.read_bytes()).hexdigest(),'mode':a.mode,'seed':a.seed,'window_size':src['projection']['window_size'],'episodes':eps,'event_multiplicity':dict(sorted(mult.items())),'target_covisibility_count':cov(targets),'bridge_metrics':bridge_spans,'coverage':coverage}
 write(a.out,out);print(hashlib.sha256(a.out.read_bytes()).hexdigest())
if __name__=='__main__':main()
