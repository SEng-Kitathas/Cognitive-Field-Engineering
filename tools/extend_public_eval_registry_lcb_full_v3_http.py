from pathlib import Path
import json, hashlib, time, re, requests, sys
from collections import Counter
import pyarrow.parquet as pq
sys.path.insert(0,'tools')
from read_remote_parquet_columns_http import HTTPRangeReader

root=Path('.')
v2=root/'state/analysis/eval_registries/STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V2_20260902'
v3=root/'state/analysis/eval_registries/STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V3_20260902'
if v3.exists(): raise SystemExit(f'REFUSE_OVERWRITE {v3}')
v3.mkdir(parents=True)
rows=[]
with (v2/'PUBLIC_EVAL_REGISTRY.jsonl').open('r',encoding='utf-8',newline='') as f:
    for line in f:
        if line.strip(): rows.append(json.loads(line))
base_manifest=json.loads((v2/'MANIFEST.json').read_text(encoding='utf-8'))

def norm(s): return re.sub(r'\s+',' ',(s or '').strip())
def h(s): return hashlib.sha256(norm(s).lower().encode()).hexdigest()
def add(text,iid,variant):
    t=norm(text)
    if len(t)<10:return
    rows.append({'family':'LIVECODEBENCH_RELEASE_V6','item_id':str(iid),'variant':variant,'text':t,'normalized_sha256':h(t),'source':{'repo':'lighteval/code_generation_lite','revision':'89e5fc5c2a8e748f50e95bc7235fab2372d49bfa','config':'release_v6','split':'test','path':None},'notes':'question-only column projection from pinned public parquet mirror; private tests not materialized'})

repo='lighteval/code_generation_lite'; rev='89e5fc5c2a8e748f50e95bc7235fab2372d49bfa'; prefix='release_v6/'
api=f'https://huggingface.co/api/datasets/{repo}/tree/{rev}/{prefix.rstrip("/")}'
r=requests.get(api,params={'recursive':'false','limit':100},timeout=45); r.raise_for_status()
files=sorted([(x['path'],int(x['size'])) for x in r.json() if x.get('type')=='file' and x.get('path','').endswith('.parquet')])
if len(files)!=9: raise SystemExit(f'EXPECTED_9_LCB_SHARDS got={len(files)} files={files}')
mirror={}; transfer=[]
for path,size in files:
    url=f'https://huggingface.co/datasets/{repo}/resolve/{rev}/{path}'
    rr=HTTPRangeReader(url,size,block_size=4*1024*1024,max_blocks=24)
    pf=pq.ParquetFile(rr)
    table=pf.read(columns=['question_id','question_title','question_content'])
    ids=table['question_id'].to_pylist(); titles=table['question_title'].to_pylist(); contents=table['question_content'].to_pylist()
    for iid,title,content in zip(ids,titles,contents):
        iid=str(iid); title=title or ''; content=content or ''
        if iid in mirror and h(mirror[iid]['content'])!=h(content): raise SystemExit(f'DUP_ID_CONTENT_MISMATCH {iid}')
        mirror[iid]={'content':norm(content),'title_plus':norm((title+'\n'+content) if title else content)}
        add(content,iid,'question_content')
        if title: add(title+'\n'+content,iid,'title_plus_question')
    transfer.append({'path':path,'source_bytes':size,'rows':table.num_rows,'bytes_fetched':rr.bytes_fetched,'range_requests':rr.requests_count})
# Cross-check direct official v6 increment already in V2.
official={}
for r in rows:
    if r.get('family')=='LIVECODEBENCH_V6_SLICE' and r.get('variant')=='question_content': official[str(r['item_id'])]=norm(r['text'])
missing=[]; mismatch=[]
for iid,text in official.items():
    if iid not in mirror: missing.append(iid)
    elif h(text)!=h(mirror[iid]['content']): mismatch.append(iid)
if missing or mismatch: raise SystemExit(f'LCB_MIRROR_CROSSCHECK_FAIL missing={len(missing)} mismatch={len(mismatch)} sample_missing={missing[:5]} sample_mismatch={mismatch[:5]}')
if len(mirror)!=1055: raise SystemExit(f'EXPECTED_1055_LCB_CASES got={len(mirror)}')
reg=v3/'PUBLIC_EVAL_REGISTRY.jsonl'
with reg.open('w',encoding='utf-8',newline='\n') as f:
    for r in rows: f.write(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n')
family=Counter(r['family'] for r in rows)
manifest={
 'schema':'cfe.standard-uplift.public-eval-registry.v3','status':'ACQUIRED_COMPLETE_FOR_CURRENT_PUBLIC_LOCK','created_unix':time.time(),'base_registry':'STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V2_20260902','base_manifest_sha256':hashlib.sha256((v2/'MANIFEST.json').read_bytes()).hexdigest(),'registry_rows':len(rows),'unique_normalized_texts':len({r['normalized_sha256'] for r in rows}),'family_rows':dict(family),'registry_sha256':hashlib.sha256(reg.read_bytes()).hexdigest(),'registry_path':str(reg).replace('\\','/'),
 'livecodebench_full':{'repo':repo,'revision':rev,'config':'release_v6','cases':len(mirror),'retained_fields':['question_id','question_title','question_content'],'private_tests_retained':False,'official_increment_crosscheck_cases':len(official),'official_increment_missing':len(missing),'official_increment_mismatch':len(mismatch),'crosscheck':'PASS','shards':transfer,'total_source_bytes':sum(x['source_bytes'] for x in transfer),'total_bytes_fetched':sum(x['bytes_fetched'] for x in transfer),'total_range_requests':sum(x['range_requests'] for x in transfer)},
 'blockers':[],'scope':'Protected public evaluation input text for current exclusion lock. Full registry local/non-Git.','laws':['QUESTION-ONLY LCB HTTP RANGE PROJECTION','MIRROR MUST MATCH DIRECT OFFICIAL OVERLAP','EVAL REGISTRY != TRAINING DATA','ANSWERS/RATIONALES/PRIVATE TESTS NOT RETAINED','FINAL FLEET EVAL FREEZE REQUIRES RERUN']}
(v3/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:manifest[k] for k in ['status','registry_rows','unique_normalized_texts','registry_sha256','livecodebench_full','blockers']},indent=2))
