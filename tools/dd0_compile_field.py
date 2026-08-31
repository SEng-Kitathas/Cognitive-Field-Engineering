#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,random
from collections import Counter
from pathlib import Path

def Hs(s:str)->str:return hashlib.sha256(s.encode('utf-8')).hexdigest()
def Jbytes(o):return (json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode('utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,o):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(Jbytes(o))

def pairkey(a,b):return tuple(sorted((a,b)))
def chunks(xs,n):return [xs[i:i+n] for i in range(0,len(xs),n)]

def score_window(win,target_pairs):
 s=set(win);return sum(1 for a,b in target_pairs if a in s and b in s)

def compile_identifying(ids,target_pairs,w):
 remaining=set(ids);wins=[]
 # greedily seed windows with target pairs, then fill deterministically
 for a,b in sorted(target_pairs):
  if a in remaining and b in remaining:
   win=[a,b];remaining.remove(a);remaining.remove(b)
   for x in sorted(list(remaining)):
    if len(win)>=w:break
    win.append(x);remaining.remove(x)
   wins.append(win)
 for rest in chunks(sorted(remaining),w):wins.append(rest)
 return wins

def compile_dispersed(ids,target_pairs,w,seed):
 rng=random.Random(seed);order=sorted(ids);rng.shuffle(order)
 # deterministic local search minimizing target co-visibility
 best=order[:];bestscore=sum(score_window(x,target_pairs) for x in chunks(best,w))
 for _ in range(max(200,len(ids)*20)):
  i,j=rng.sample(range(len(order)),2);order[i],order[j]=order[j],order[i]
  sc=sum(score_window(x,target_pairs) for x in chunks(order,w))
  if sc<=bestscore:best=order[:];bestscore=sc
  else:order[i],order[j]=order[j],order[i]
  if bestscore==0:break
 return chunks(best,w)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--field',type=Path,required=True);ap.add_argument('--mode',choices=['IDENTIFYING_LOCAL','RELATIONALLY_DISPERSED'],required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 src=load(a.field);events={e['id']:e for e in src['events']};ids=list(events)
 if len(ids)!=len(set(ids)):raise SystemExit('DUP_EVENT_ID')
 target_types=set(src['projection']['target_relation_types']);pairs=[]
 for r in src['relations']:
  if r['type'] in target_types:pairs.append(pairkey(r['source'],r['target']))
 w=int(src['projection']['window_size'])
 wins=compile_identifying(ids,pairs,w) if a.mode=='IDENTIFYING_LOCAL' else compile_dispersed(ids,pairs,w,a.seed)
 flat=[x for w0 in wins for x in w0]
 if Counter(flat)!=Counter(ids):raise SystemExit('EVENT_MULTISET_DRIFT')
 episodes=[]
 for i,win in enumerate(wins):
  episodes.append({'window_index':i,'events':[{'id':x,'payload':events[x]['payload'],'payload_sha256':Hs(events[x]['payload'])} for x in win]})
 out={'schema':'cfe.dd0.compiled-field.v1','source_field_sha256':hashlib.sha256(Path(a.field).read_bytes()).hexdigest(),'mode':a.mode,'seed':a.seed,'window_size':w,'episodes':episodes,'event_multiset':sorted(flat),'payload_sha256_multiset':sorted(Hs(events[x]['payload']) for x in flat)}
 write(a.out,out);print(hashlib.sha256(a.out.read_bytes()).hexdigest())
if __name__=='__main__':main()
