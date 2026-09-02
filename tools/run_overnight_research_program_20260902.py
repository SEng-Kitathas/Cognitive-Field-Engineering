from pathlib import Path
import subprocess,sys,os,json,time,hashlib,collections,re
root=Path.cwd();stage=root/'research/campaigns/overnight_20260902';stage.mkdir(parents=True,exist_ok=True)
labels=['MACHINERY','CARTOGRAPHY','EXTERNAL'];receipt={'schema':'cfe.overnight.program.v1','status':'RUNNING','started':time.time(),'stages':[],'promotion_authority':'NONE'}
def save(): (stage/'OVERNIGHT_PROGRAM_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
save()
for label in labels:
 seed=stage/f'SEED_{label}.json';env=os.environ.copy();env['CFE_OVERNIGHT_LABEL']=label;env['CFE_CAMPAIGN_SEED_PATH']=str(seed)
 t=time.time();cp=subprocess.run([sys.executable,'tools/run_overnight_cfe_campaigns.py'],cwd=root,env=env,capture_output=True,text=True,errors='replace',timeout=9000)
 (stage/f'{label}.stdout.log').write_text(cp.stdout,encoding='utf-8');(stage/f'{label}.stderr.log').write_text(cp.stderr,encoding='utf-8');receipt['stages'].append({'label':label,'return_code':cp.returncode,'seconds':time.time()-t});save()
# aggregate all produced overnight campaign pass artifacts without promoting them
runs=sorted((root/'research/campaigns').glob('OVERNIGHT_*_3x20_*'))
terms=collections.Counter();survivors=[];scars=[];demotions=[];questions=[]
for rr in runs:
 for p in rr.glob('C*/P[0-9][0-9].json'):
  try:d=json.loads(p.read_text(encoding='utf-8'));questions.append(d.get('active_question',''));survivors.append(d.get('SURVIVE',''));scars.append(d.get('SCAR',''));demotions.append(d.get('DEMOTE',''))
  except:pass
for text in survivors+scars+demotions:
 for t in re.findall(r'[A-Za-z][A-Za-z0-9_+.-]{3,}',text.lower()):terms[t]+=1
agg={'schema':'cfe.overnight.aggregate.v1','status':'RESEARCH_ONLY','runs':[str(r.relative_to(root)) for r in runs],'pass_files':len(questions),'top_terms':terms.most_common(100),'survivors':survivors,'scars':scars,'demotions':demotions,'promotion_authority':'NONE'}
(stage/'OVERNIGHT_RESEARCH_AGGREGATE.json').write_text(json.dumps(agg,indent=2)+'\n',encoding='utf-8')
# terminate dedicated inference service only after research stages finish
subprocess.run(['taskkill','/PID','34916','/T','/F'],capture_output=True,text=True,errors='replace')
receipt['status']='COMPLETE' if all(x['return_code']==0 for x in receipt['stages']) else 'COMPLETE_WITH_STAGE_FAILURES';receipt['completed']=time.time();receipt['pass_files']=len(questions);save();(stage/'RESEARCH_LANE_COMPLETE.sentinel').write_text(receipt['status']+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2),flush=True)
