#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,hashlib,collections
from pathlib import Path

def norm(s):return re.sub(r'\s+',' ',str(s or '').strip().lower())
def toks(s):return re.findall(r'[a-z0-9_./:-]+',norm(s))
def grams(s,n=3):
 t=toks(s); return {tuple(t[i:i+n]) for i in range(len(t)-n+1)} if len(t)>=n else ({tuple(t)} if t else set())
def jac(a,b):return len(a&b)/len(a|b) if a and b else 0.0
def readjl(p):
 a=[]
 with Path(p).open('r',encoding='utf-8',newline='') as f:
  for line in f:
   line=line.rstrip('\n').rstrip('\r')
   if line:a.append(json.loads(line))
 return a
def visible(r):
 s='\n'.join(f"{m.get('role')}: {m.get('content','')}" for m in r['content']['messages'])
 if r['source']['repo']=='CFE/project-generated-standard-uplift':s+='\nassistant: '+str(r['content'].get('final_answer') or '')
 return s
# Curator-side mechanism predicates are deliberately conservative. A hit is a hunt lead, never verified coverage.
RULES={
 'ADAPTIVE_REASONING_EFFORT_VALUE_OF_COMPUTATION':[
   (re.compile(r'(?i)\b(?:worth|cost|takes? \d+|minutes?|hours?|delay|expensive|cheap|low[- ]cost|additional check|another check|another diagnostic|extra (?:check|search|test|trace|review))\b'),2),
   (re.compile(r'(?i)\b(?:stop|continue|sufficient|enough evidence|resolve|distinguish|unlikely to change|can change|reverse the choice)\b'),2)],
 'LIVE_ALTERNATIVES_AND_NONCOMMITMENT':[
   (re.compile(r'(?i)\b(?:either|two (?:possible|candidate|live)|compatible with|could be|alternatives?|hypotheses?)\b'),2),
   (re.compile(r'(?i)\b(?:distinguish|discriminate|resolve|insufficient|uncertain|not enough evidence)\b'),2)],
 'SUPPORT_LINEAGE_AND_DEPENDENCY_LOCAL_REPAIR':[
   (re.compile(r'(?i)\b(?:depends? on|dependency|because|caused by|shared boundary|only .* affected|preserve|unchanged|rollback|revise)\b'),2)],
 'TEMPORAL_REQUALIFICATION_AND_CURRENTNESS':[
   (re.compile(r'(?i)\b(?:later|newer|current|updated|supersed|changed to|now says|stale|latest)\b'),2),
   (re.compile(r'(?i)\b(?:earlier|previous|old|was|formerly|prior)\b'),1)],
 'EXTERNAL_EVIDENCE_AUTHORITY_AND_UNKNOWN':[
   (re.compile(r'(?i)\b(?:readback|measurement|report|primary source|signed|observed|evidence|checksum|test result|log)\b'),1),
   (re.compile(r'(?i)\b(?:unknown|unresolved|defer|not established|insufficient)\b'),2)],
 'REPRESENTATION_ADEQUACY_AND_REFINEMENT':[
   (re.compile(r'(?i)\b(?:model|representation|category|schema|coordinate|distinction|alias|cannot explain|does not fit|refine|split)\b'),1)],
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--mechanism',required=True,choices=sorted(RULES));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--limit',type=int,default=100);a=ap.parse_args();rows=readjl(a.candidate);rules=RULES[a.mechanism];leads=[]
 for r in rows:
  text=visible(r);score=0;ev=[]
  for rx,w in rules:
   ms=[m.group(0) for m in rx.finditer(text)]
   if ms:score+=w;ev.extend(ms[:4])
  if score:
   leads.append({'atom_id':r['atom_id'],'source':r['source']['repo'],'split':r['source']['split'],'interaction_shape':r['capability']['interaction_shape'],'score':score,'matched_surface':ev,'learner_visible_excerpt':text[:5000]})
 leads=sorted(leads,key=lambda x:(-x['score'],x['source'],x['atom_id']))[:a.limit]
 out={'schema':'cfe.isomorphic-predator.v1','status':'HUNT_LEADS_ONLY__NO_COVERAGE_CLAIM','mechanism':a.mechanism,'candidate_sha256':hashlib.sha256(a.candidate.read_bytes()).hexdigest(),'candidate_rows':len(rows),'lead_count':len(leads),'leads':leads,'laws':['ISOMORPHIC_PREDATOR = CURATOR_SIDE_ONLY','SURFACE MATCH != STRUCTURAL ISOMORPH','POSITIVE ISOMORPH REQUIRES LEARNER_VISIBLE CONSEQUENCE','ANTI_ISOMORPH REQUIRED BEFORE LOAD_BEARING COVERAGE','PERSONAL/CFE/HISTORICAL PROVENANCE STAYS SIDECAR_ONLY','TRAINING BODY != CONTROL PLANE']};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':out['status'],'mechanism':a.mechanism,'lead_count':len(leads)},indent=2))
if __name__=='__main__':main()
