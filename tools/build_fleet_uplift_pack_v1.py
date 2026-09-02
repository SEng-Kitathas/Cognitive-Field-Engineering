#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,json,random,re,time
from pathlib import Path
import requests
BASE='https://datasets-server.huggingface.co'
SEED=20260902
SOURCES={
 'openr1':dict(dataset='open-r1/OpenR1-Math-220k',config='default',split='train',n=93733,license='apache-2.0'),
 'nemscience':dict(dataset='nvidia/Nemotron-Science-v1',config='default',split='MCQ',n=174155,license='cc-by-4.0'),
 'openthoughts':dict(dataset='open-thoughts/OpenThoughts-114k',config='default',split='train',n=114000,license='apache-2.0'),
 'agent':dict(dataset='open-thoughts/OpenThoughts-Agent-SFT-100K',config='default',split='train',n=94334,license='apache-2.0'),
 'nemchat':dict(dataset='nvidia/Nemotron-Instruction-Following-Chat-v1',config='default',split='chat_if',n=283000,license='odc-by-1.0'),
 'nemstruct':dict(dataset='nvidia/Nemotron-Instruction-Following-Chat-v1',config='default',split='structured_outputs',n=4969,license='cc-by-4.0'),
}
def normspace(s):return re.sub(r'\s+',' ',s or '').strip()
def key_text(s):return hashlib.sha256(normspace(s).lower().encode('utf-8')).hexdigest()
def get_rows(src,offset,length=100):
 s=SOURCES[src];r=requests.get(BASE+'/rows',params={'dataset':s['dataset'],'config':s['config'],'split':s['split'],'offset':offset,'length':length},timeout=45);r.raise_for_status();return [(z['row_idx'],z['row']) for z in r.json()['rows']]
def combine_reasoning(content,reasoning):
 content=(content or '').strip(); reasoning=(reasoning or '').strip()
 if reasoning and '<think>' not in content:
  return f'<think>\n{reasoning}\n</think>\n\n{content}'
 return content
def normalize_openthoughts(s):
 s=s.replace('<|begin_of_thought|>','<think>').replace('<|end_of_thought|>','</think>')
 s=s.replace('<|begin_of_solution|>','').replace('<|end_of_solution|>','').strip()
 return s
def atom(src,idx,row):
 lic=row.get('license') or SOURCES[src]['license']; meta={};messages=[];skill='general';quality={}
 if src=='openr1':
  if int(row.get('correctness_count') or 0)<2:return None
  if not row.get('messages') or len(row['messages'])!=2:return None
  messages=[{'role':m['role'],'content':m['content']} for m in row['messages']]
  if '<think>' not in messages[-1]['content']:return None
  skill='math:'+str(row.get('problem_type','other')).lower().replace(' ','_')
  quality={'correctness_count':row.get('correctness_count'),'source':row.get('source'),'question_type':row.get('question_type')}
  meta={'problem_type':row.get('problem_type'),'source_subtype':row.get('source'),'question_type':row.get('question_type')}
 elif src=='nemscience':
  ms=row.get('messages') or []
  if len(ms)!=2 or ms[1].get('role')!='assistant' or not ms[1].get('reasoning_content'):return None
  messages=[{'role':'user','content':ms[0].get('content','')},{'role':'assistant','content':combine_reasoning(ms[1].get('content'),ms[1].get('reasoning_content'))}]
  skill='science';quality={'reasoning_content':True}
 elif src=='openthoughts':
  cs=row.get('conversations') or []
  if len(cs)<2:return None
  for m in cs:
   role={'human':'user','user':'user','gpt':'assistant','assistant':'assistant'}.get(m.get('from'),m.get('role'))
   text=m.get('value',m.get('content',''))
   if role not in ('user','assistant'):continue
   if role=='assistant':text=normalize_openthoughts(text)
   messages.append({'role':role,'content':text})
  if len(messages)<2 or messages[-1]['role']!='assistant' or '<think>' not in messages[-1]['content']:return None
  u=messages[0]['content'].lower();skill='code' if any(x in u for x in ['python','function','code','algorithm','stdin','program']) else ('math' if any(x in u for x in ['prove','equation','integer','geometry','calculate','number']) else 'reasoning')
  quality={'thought_trace':True}
 elif src=='agent':
  if row.get('result') is not None:return None
  if row.get('trace_source') not in ('main',None):return None
  cs=row.get('conversations') or []
  if not (10<=len(cs)<=36):return None
  messages=[{'role':m.get('role'),'content':m.get('content','')} for m in cs if m.get('role') in ('user','assistant','system','tool') and isinstance(m.get('content'),str)]
  if not messages:return None
  assistant='\n'.join(m['content'] for m in messages if m['role']=='assistant')
  if '"task_complete": true' not in assistant.lower() and 'task_complete":true' not in assistant.lower():return None
  skill='agent:'+str(row.get('trace_source') or 'main');quality={'no_exception_result':True,'task_complete_true':True,'turns':len(cs)};meta={'task':row.get('task'),'trace_source':row.get('trace_source')}
 elif src=='nemchat':
  if row.get('capability_target')!='instruction_following':return None
  ms=row.get('messages') or []
  for m in ms:
   if m.get('role') not in ('system','user','assistant'):continue
   content=m.get('content','')
   if m.get('role')=='assistant' and row.get('reasoning')=='on':content=combine_reasoning(content,m.get('reasoning_content'))
   messages.append({'role':m.get('role'),'content':content})
  if len(messages)<2:return None
  if row.get('reasoning')=='on' and not any('<think>' in m['content'] for m in messages if m['role']=='assistant'):return None
  skill='instruction_following:'+str(row.get('reasoning'));quality={'reasoning_mode':row.get('reasoning'),'capability_target':row.get('capability_target')};meta={'reasoning':row.get('reasoning')}
 elif src=='nemstruct':
  ms=row.get('messages') or []
  messages=[{'role':m.get('role'),'content':m.get('content','')} for m in ms if m.get('role') in ('system','user','assistant')]
  if len(messages)<2:return None
  skill='structured_output';quality={'schema_constrained':True}
 else:return None
 # common quality bounds
 if not any(m['role']=='user' for m in messages) or not any(m['role']=='assistant' for m in messages):return None
 chars=sum(len(m['content']) for m in messages)
 if chars<250 or chars>18000:return None
 first_user=next(m['content'] for m in messages if m['role']=='user')
 aid=f'{src}:{idx}:{key_text(first_user)[:16]}'
 return {'atom_id':aid,'source_key':src,'dataset':SOURCES[src]['dataset'],'config':SOURCES[src]['config'],'split':SOURCES[src]['split'],'source_row_idx':idx,'license':lic,'skill':skill,'quality':quality,'meta':meta,'chars':chars,'prompt_sha256':key_text(first_user),'messages':messages}
def collect(src,target,rng):
 n=SOURCES[src]['n']; offsets=list(range(0,max(1,n-100),100));rng.shuffle(offsets);out=[];seen=set();attempt=0
 for off in offsets:
  attempt+=1
  try: batch=get_rows(src,off,100)
  except Exception:continue
  rng.shuffle(batch)
  for idx,row in batch:
   a=atom(src,idx,row)
   if not a or a['prompt_sha256'] in seen:continue
   seen.add(a['prompt_sha256']);out.append(a)
   if len(out)>=target:return out
  if attempt>max(60,target//5):break
 return out
def select(rows,counts,seed):
 rng=random.Random(seed);by=collections.defaultdict(list)
 for r in rows:by[r['source_key']].append(r)
 out=[]
 for src,n in counts.items():
  pool=by[src][:];rng.shuffle(pool);out+=pool[:n]
 assert len({x['atom_id'] for x in out})==len(out)
 return out
def cfe_order(rows,seed):
 # CFE-informed only: coverage-balanced round robin, relation-family revisits, anti-homogeneous source runs.
 rng=random.Random(seed);b=collections.defaultdict(list)
 for r in rows:b[r['skill']].append(r)
 for v in b.values():rng.shuffle(v)
 skills=sorted(b,key=lambda k:(-len(b[k]),k));out=[];last_src=None;last_skill=None
 while any(b.values()):
  candidates=[k for k in skills if b[k]]
  # prefer revisit to a different skill family/source than last, but cycle all buckets before reusing dominant buckets
  scored=[]
  for k in candidates:
   r=b[k][-1];score=0
   if k!=last_skill:score+=3
   if r['source_key']!=last_src:score+=2
   score+=min(2,len(b[k])/20)
   scored.append((score,rng.random(),k))
  _,_,k=max(scored);r=b[k].pop();out.append(r);last_src=r['source_key'];last_skill=k
 return out
def write_jsonl(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')) for x in rows)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);rng=random.Random(SEED)
 targets={'openr1':850,'nemscience':650,'openthoughts':750,'agent':550,'nemchat':1000,'nemstruct':350}
 master=[];status={}
 for src,n in targets.items():
  xs=collect(src,n,rng);master+=xs;status[src]={'requested':n,'collected':len(xs)};print(src,len(xs),flush=True)
 # Target-specific source counts. Require exact availability or fail closed.
 qcounts={'openr1':700,'nemscience':500,'openthoughts':600,'agent':350,'nemchat':250}
 ccounts={'openr1':450,'nemscience':350,'openthoughts':450,'agent':300,'nemchat':850,'nemstruct':300}
 for counts in (qcounts,ccounts):
  for src,n in counts.items():
   if status[src]['collected']<n:raise SystemExit(f'INSUFFICIENT {src} {status[src]["collected"]}<{n}')
 q=select(master,qcounts,SEED+1);c=select(master,ccounts,SEED+2)
 views={}
 for name,rows in [('qwen3_thinking',q),('capybara_general',c)]:
  std=rows[:];random.Random(SEED+10+(0 if name=='qwen3_thinking' else 1)).shuffle(std);cf=cfe_order(rows,SEED+20+(0 if name=='qwen3_thinking' else 1))
  atomset=sorted(x['atom_id'] for x in rows);assert sorted(x['atom_id'] for x in std)==atomset==sorted(x['atom_id'] for x in cf)
  for arm,data in [('STANDARD_BALANCED',std),('CFE_STRUCTURED',cf)]:
   p=a.out/f'{name}.{arm}.jsonl';write_jsonl(p,data);views[f'{name}.{arm}']={'path':p.name,'rows':len(data),'sha256':sha(p),'atom_set_sha256':hashlib.sha256('\n'.join(atomset).encode()).hexdigest(),'source_counts':dict(collections.Counter(x['source_key'] for x in data)),'skill_counts':dict(collections.Counter(x['skill'] for x in data)),'license_counts':dict(collections.Counter(x['license'] for x in data))}
 mp=a.out/'MASTER_ATOMS.jsonl';write_jsonl(mp,master)
 manifest={'schema':'cfe.fleet-uplift-pack.v1','status':'CURATED_ATOMS_AND_ORDERINGS__NOT_TRAINING_AUTHORIZATION','seed':SEED,'created_unix':time.time(),'source_specs':SOURCES,'collection_status':status,'master_rows':len(master),'master_sha256':sha(mp),'views':views,'cfe_status':'CFE_INFORMED_ORDERING_NOT_CFE_LAW','cfe_ordering_description':'coverage-balanced skill/source alternation and revisit; exact atom set matched to STANDARD_BALANCED; no claim that heuristic relations are learner-native','laws':['SAME_ATOMS_ACROSS_ARMS','STANDARD_BALANCED != CFE_STRUCTURED_ORDER_ONLY','NO_FAILED_AGENT_TRAJECTORIES_IN_SFT','VERIFIER_METADATA_PREFERRED','BAD_BASELINE_PRESERVED_SEPARATELY','DATASET_REPUTATION != ROW_QUALITY']}
 (a.out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(manifest,indent=2),flush=True)
if __name__=='__main__':main()
