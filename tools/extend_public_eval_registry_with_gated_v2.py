from pathlib import Path
import json, hashlib, time, re
from collections import Counter
from datasets import load_dataset

root=Path('.')
v1=root/'state/analysis/eval_registries/STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V1_20260902'
v2=root/'state/analysis/eval_registries/STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V2_20260902'
if v2.exists():
    raise SystemExit(f'REFUSE_OVERWRITE {v2}')
v2.mkdir(parents=True)
rows=[]
with (v1/'PUBLIC_EVAL_REGISTRY.jsonl').open('r',encoding='utf-8',newline='') as f:
    for line in f:
        if line.strip(): rows.append(json.loads(line))
base_manifest=json.loads((v1/'MANIFEST.json').read_text(encoding='utf-8'))

def norm(s): return re.sub(r'\s+',' ',(s or '').strip())
def add(family,text,item_id,repo,rev,config,split,variant='question',notes=None):
    t=norm(text)
    if len(t)<10: return
    rows.append({'family':family,'item_id':str(item_id),'variant':variant,'text':t,'normalized_sha256':hashlib.sha256(t.lower().encode()).hexdigest(),'source':{'repo':repo,'revision':rev,'config':config,'split':split,'path':None},'notes':notes})

gp_repo='Idavidrein/gpqa'; gp_rev='633f5ee89ab8ad4522a9f850766b73f62147ffdd'
gp=load_dataset(gp_repo,'gpqa_diamond',split='train',revision=gp_rev)
for i,r in enumerate(gp):
    iid=r.get('Record ID',i)
    add('GPQA_DIAMOND',r.get('Question',''),iid,gp_repo,gp_rev,'gpqa_diamond','train','question')
    if r.get('Pre-Revision Question'): add('GPQA_DIAMOND',r['Pre-Revision Question'],iid,gp_repo,gp_rev,'gpqa_diamond','train','pre_revision_question')
    if r.get('Extra Revised Question'): add('GPQA_DIAMOND',r['Extra Revised Question'],iid,gp_repo,gp_rev,'gpqa_diamond','train','extra_revised_question')

h_repo='cais/hle'; h_rev='5a81a4c7271a2a2a312b9a690f0c2fde837e4c29'
hle=load_dataset(h_repo,'default',split='test',revision=h_rev)
h_ids=hle.data.column('id').to_pylist()
h_q=hle.data.column('question').to_pylist()
for i,(iid,q) in enumerate(zip(h_ids,h_q)):
    add('HLE',q,iid if iid is not None else i,h_repo,h_rev,'default','test','question',notes='question text only; image/answer/rationale not retained')

reg=v2/'PUBLIC_EVAL_REGISTRY.jsonl'
with reg.open('w',encoding='utf-8',newline='\n') as f:
    for r in rows: f.write(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n')
blockers=[b for b in base_manifest.get('blockers',[]) if b.get('family') not in {'GPQA','HLE'}]
family=Counter(r['family'] for r in rows)
manifest={
 'schema':'cfe.standard-uplift.public-eval-registry.v2',
 'status':'ACQUIRED_WITH_PARTIAL_LIVECODEBENCH_BLOCKER' if blockers else 'ACQUIRED_COMPLETE_FOR_CURRENT_PUBLIC_LOCK',
 'created_unix':time.time(),
 'base_registry':'STANDARD_UPLIFT_PUBLIC_EVAL_REGISTRY_V1_20260902',
 'base_manifest_sha256':hashlib.sha256((v1/'MANIFEST.json').read_bytes()).hexdigest(),
 'registry_rows':len(rows),
 'unique_normalized_texts':len({r['normalized_sha256'] for r in rows}),
 'family_rows':dict(family),
 'registry_sha256':hashlib.sha256(reg.read_bytes()).hexdigest(),
 'registry_path':str(reg).replace('\\','/'),
 'gated_sources':[{'family':'GPQA_DIAMOND','repo':gp_repo,'revision':gp_rev,'dataset_rows':len(gp),'retained_fields':['Question','Pre-Revision Question when populated','Extra Revised Question when populated'],'answers_retained':False},{'family':'HLE','repo':h_repo,'revision':h_rev,'dataset_rows':len(hle),'retained_fields':['question'],'images_retained':False,'answers_retained':False,'rationales_retained':False}],
 'blockers':blockers,
 'scope':'Protected public evaluation input text only. Full registry local/non-Git.',
 'laws':['GATED ACCESS USED DIRECTLY AFTER USER ACCEPTANCE','EVAL REGISTRY != TRAINING DATA','ANSWERS/RATIONALES/PRIVATE TESTS NOT RETAINED','PARTIAL REGISTRY != GLOBAL CLEARANCE','FINAL FLEET EVAL FREEZE REQUIRES RERUN']}
(v2/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:manifest[k] for k in ['status','registry_rows','unique_normalized_texts','registry_sha256','blockers']},indent=2))
