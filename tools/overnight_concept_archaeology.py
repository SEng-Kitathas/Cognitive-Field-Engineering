from pathlib import Path
import re,json,hashlib,time
ROOTS=[Path(r'E:\new pc\AI_Pushes_Sandbox\projects'),Path(r'D:\Singularity_Works\repo')]
OUT=Path.cwd()/'research/campaigns/overnight_20260902/local_archaeology'
OUT.mkdir(parents=True,exist_ok=True)
TERMS=['helix','oarr','loop+','loop_plus','attention reservoir','reservoir','csc','co-processing','coprocessing','starmap','cognitive geometry','research loop','semantic helix']
SUF={'.md','.txt','.json','.jsonl','.py','.ps1','.sh','.yaml','.yml','.toml','.csv','.log'}
hits=[];scanned=0;t0=time.time()
for rr in ROOTS:
 if not rr.exists():continue
 for p in rr.rglob('*'):
  try:
   if not p.is_file() or p.suffix.lower() not in SUF or p.stat().st_size>2_000_000:continue
   if any(x in str(p).lower() for x in ['\\.git\\','\\.venv\\','\\node_modules\\','\\publication\\']):continue
   b=p.read_bytes();scanned+=1
   if b'\x00' in b[:2048]:continue
   text=b.decode('utf-8',errors='replace');low=text.lower();matched=[t for t in TERMS if t in low]
   if not matched:continue
   positions=[]
   for t in matched:
    i=low.find(t)
    if i>=0:positions.append(i)
   i=min(positions);excerpt=text[max(0,i-700):i+1800]
   hits.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'terms':matched,'excerpt':excerpt})
   if len(hits)>=1200:break
  except Exception:pass
 if len(hits)>=1200:break
# dedupe by hash, favor more term classes
by={}
for h in hits:
 k=h['sha256'];
 if k not in by or len(h['terms'])>len(by[k]['terms']):by[k]=h
rows=sorted(by.values(),key=lambda x:(-len(x['terms']),x['path'].lower()))
summary={'schema':'cfe.overnight.concept-archaeology.v1','status':'COMPLETE','roots':[str(x) for x in ROOTS],'files_scanned':scanned,'raw_hits':len(hits),'unique_hits':len(rows),'elapsed_seconds':time.time()-t0,'term_counts':{t:sum(t in x['terms'] for x in rows) for t in TERMS}}
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');(OUT/'HITS.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8');
with (OUT/'TOP_HITS.md').open('w',encoding='utf-8',newline='\n') as f:
 f.write('# Overnight concept archaeology\n\n')
 for x in rows[:120]:f.write(f"## {x['path']}\nTerms: {', '.join(x['terms'])}\nSHA: `{x['sha256']}`\n\n```text\n{x['excerpt']}\n```\n\n")
print(json.dumps(summary,indent=2),flush=True)
