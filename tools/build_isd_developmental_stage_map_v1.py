#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,collections
from pathlib import Path

def readjl(p):
 a=[]
 with Path(p).open('r',encoding='utf-8',newline='') as f:
  for line in f:
   line=line.rstrip('\n').rstrip('\r')
   if line:a.append(json.loads(line))
 return a

def assign(r):
 cfg=r['source'].get('config');sub=r['pilot'].get('subtype')
 if r['source']['repo']!='CFE/project-generated-standard-uplift':
  return 'UNRESOLVED_TIER','UNVERIFIED_SOURCE_EPISODE','Current source/curator tags are not sufficient to prove developmental dependency depth.'
 if cfg=='adaptive_effort_v1r1':
  return 'T3_OPEN_WORLD','EXPLICIT_PROJECT_GENERATED_CONTRACT','Cost-aware STOP/CONTINUE requires evidence sufficiency, live alternatives and value of another check.'
 if cfg=='memory_currentness_v1':
  if sub=='DIRECT_STALE_UPDATE':return 'T0_FOUNDATIONS','EXPLICIT_PROJECT_GENERATED_CONTRACT','Direct newer-over-stale currentness primitive.'
  if sub=='SELECTIVE_PRESERVATION':return 'T1_RELATIONAL','EXPLICIT_PROJECT_GENERATED_CONTRACT','Currentness update plus preservation of unaffected state.'
  if sub=='INDIRECT_PROPAGATED_INVALIDATION':return 'T2_SYSTEMS','EXPLICIT_PROJECT_GENERATED_CONTRACT','Later evidence propagates through dependency structure.'
  if sub=='AMBIGUOUS_CURRENTNESS_DISCRIMINATOR':return 'T2_SYSTEMS','EXPLICIT_PROJECT_GENERATED_CONTRACT','Competing currentness interpretations require a discriminator.'
 if cfg=='science_diagnosis_v1':
  if sub=='CHOOSE_DISCRIMINATOR':return 'T1_RELATIONAL','EXPLICIT_PROJECT_GENERATED_CONTRACT','Few live explanations and an identifying measurement.'
  if sub=='SUPPORT_VS_DISCRIMINATION':return 'T1_RELATIONAL','EXPLICIT_PROJECT_GENERATED_CONTRACT','Distinguishes supporting evidence from identifying evidence.'
  if sub=='UPDATE_CANDIDATES':return 'T2_SYSTEMS','EXPLICIT_PROJECT_GENERATED_CONTRACT','Evidence updates a maintained candidate set.'
  if sub=='REPRESENTATION_REFINEMENT':return 'T3_OPEN_WORLD','EXPLICIT_PROJECT_GENERATED_CONTRACT','Current representation is inadequate and must be refined while preserving valid evidence.'
 if cfg=='deficit_repair_v1':
  if sub in {'STRUCTURED_HANDOFF','CHANGE_ONLY','RATE_CALCULATION'}:return 'T0_FOUNDATIONS','EXPLICIT_PROJECT_GENERATED_CONTRACT','Direct transformation/calculation/current-record primitive.'
  if sub in {'PRESERVE_UNKNOWN','DEPENDENCY_STATE','LOCAL_CODE_REPAIR','MEASUREMENT_DIAGNOSIS','PARTIAL_EVIDENCE','SELECTIVE_ROLLBACK','MULTITURN_CURRENT_STATE','MULTITURN_RULE_UPDATE'}:return 'T1_RELATIONAL','EXPLICIT_PROJECT_GENERATED_CONTRACT','Small dependency/currentness/evidence relation beyond a single primitive.'
 return 'UNRESOLVED_TIER','UNRESOLVED_PROJECT_GENERATED_CONTRACT','No frozen stage rule for this subtype.'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--stage-spec',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();rows=readjl(a.candidate);items=[]
 for i,r in enumerate(rows):
  stage,basis,reason=assign(r);items.append({'atom_id':r['atom_id'],'index':i,'stage':stage,'assignment_basis':basis,'reason':reason,'source':r['source']['repo'],'config':r['source'].get('config'),'subtype':r['pilot'].get('subtype')})
 counts=collections.Counter(x['stage'] for x in items);basis=collections.Counter(x['assignment_basis'] for x in items)
 out={'schema':'cfe.isd.developmental-stage-map.v1','status':'PARTIAL_STAGE_MAP__UNRESOLVED_ROWS_BLOCK_FINAL_ORDER_FREEZE','candidate_sha256':hashlib.sha256(a.candidate.read_bytes()).hexdigest(),'candidate_rows':len(rows),'stage_spec_sha256':hashlib.sha256(a.stage_spec.read_bytes()).hexdigest(),'stage_counts':dict(counts),'assignment_basis_counts':dict(basis),'resolved_rows':len(rows)-counts.get('UNRESOLVED_TIER',0),'unresolved_rows':counts.get('UNRESOLVED_TIER',0),'items':items,'laws':['STAGE ASSIGNMENT = SIDECAR ONLY','UNRESOLVED_TIER != FAILURE','UNVERIFIED SOURCE TAG != DEPENDENCY DEPTH','NO FINAL TRAINING ORDER UNTIL STAGE MAP IS ADEQUATE','ROW ORDER SHALL BE COMPILED FROM STAGES + SPIRAL REVISIT AFTER VERIFICATION','NO LEARNER-FACING STAGE LABELS']};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':out['status'],'rows':len(rows),'stage_counts':dict(counts),'resolved_rows':out['resolved_rows'],'unresolved_rows':out['unresolved_rows']},indent=2))
if __name__=='__main__':main()
