#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,collections,re
from pathlib import Path

def readjl(p):
 a=[]
 with Path(p).open('r',encoding='utf-8',newline='') as f:
  for line in f:
   line=line.rstrip('\n').rstrip('\r')
   if line:a.append(json.loads(line))
 return a

def structure(r):
 msgs=r['content']['messages'];roles=collections.Counter(m.get('role') for m in msgs)
 tool_calls=[]
 for m in msgs:
  if m.get('role')=='assistant' and m.get('tool_calls'):
   for tc in m['tool_calls']:
    fn=(tc.get('function') or {}).get('name') if isinstance(tc,dict) else None
    tool_calls.append(str(fn))
 tool_results=sum(m.get('role')=='tool' for m in msgs)
 users=[str(m.get('content') or '') for m in msgs if m.get('role')=='user']; visible='\n'.join(users)
 return {'turns':len(msgs),'user_turns':roles.get('user',0),'assistant_turns':roles.get('assistant',0),'tool_calls':len(tool_calls),'tool_results':tool_results,'tool_names':tool_calls,'embedded_tool_responses':visible.count('<tool_response>'),'has_research_state_summary':'RESEARCH STATE SUMMARY (prev_state)' in visible,'has_current_date':bool(re.search(r"(?i)today.?s date|current date|as of",visible))}

def assign_project(r):
 cfg=r['source'].get('config');sub=r['pilot'].get('subtype')
 if cfg=='adaptive_effort_v1r1':return 'T3_OPEN_WORLD','EXPLICIT_PROJECT_GENERATED_CONTRACT','Cost-aware STOP/CONTINUE requires evidence sufficiency, live alternatives and value of another check.'
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
 return None

def assign(r):
 if r['source']['repo']=='CFE/project-generated-standard-uplift':
  x=assign_project(r)
  if x:return x
  return 'UNRESOLVED_TIER','UNRESOLVED_PROJECT_GENERATED_CONTRACT','No frozen dependency-depth rule for this generated subtype.'
 s=structure(r);src=r['source']['repo']
 # QUEST: learner-visible compressed research state explicitly carries prior searches, trusted/uncertain claims and open gaps.
 if src in {'osunlp/QUEST-SFT-Data-Open-ended','osunlp/QUEST-SFT-Data-Objective'} and s['has_research_state_summary']:
  return 'T3_OPEN_WORLD','LEARNER_VISIBLE_RESEARCH_STATE_CARRY','Episode explicitly resumes a compressed research state containing prior searches/evidence/support status; continuation must preserve and update that state rather than restart.'
 # NextSearch: stage from actual search/fetch trajectory depth, never from the source label alone.
 if src=='NextTokenAI/NextSearch-1-Trajectories':
  tc=s['tool_calls'];names=s['tool_names'];fetch=sum(n=='fetch' for n in names)
  if tc==1 and s['tool_results']>=1:return 'T1_RELATIONAL','LEARNER_VISIBLE_TOOL_TOPOLOGY','One external evidence action followed by an observation and answer; direct evidence-to-conclusion relation.'
  if 2<=tc<=4 and s['tool_results']>=2 and fetch==0:return 'T2_SYSTEMS','LEARNER_VISIBLE_TOOL_TOPOLOGY','Multiple evidence actions/observations must be integrated; dependency burden exceeds a single lookup.'
  if tc>=5 or (fetch>=1 and tc>=3):return 'T3_OPEN_WORLD','LEARNER_VISIBLE_TOOL_TOPOLOGY','Extended search/fetch trajectory with repeated evidence acquisition and source integration under open-world uncertainty.'
 # Nemotron Agentic: direct tool act -> T1; multi-step dependent tool/user state -> T2; extended stateful agent trajectory -> T3.
 if src=='nvidia/Nemotron-SFT-Agentic-v2':
  tc=s['tool_calls'];ut=s['user_turns']
  if tc==1 and s['tool_results']>=1:return 'T1_RELATIONAL','LEARNER_VISIBLE_TOOL_TOPOLOGY','Single task-world tool action and result condition the assistant response.'
  if 2<=tc<=5 and s['tool_results']>=2:return 'T2_SYSTEMS','LEARNER_VISIBLE_TOOL_TOPOLOGY','Multi-step tool trajectory integrates several task-world observations/actions; later state depends on earlier tool results.'
  if tc>=6 or (tc>=3 and ut>=4):return 'T3_OPEN_WORLD','LEARNER_VISIBLE_TOOL_TOPOLOGY','Extended multi-turn agent trajectory maintains task state across repeated actions/observations and user updates.'
 # LiteResearcher encodes tool observations as user-side <tool_response> continuations.
 if src=='simplex-ai-inc/LiteResearcher-SFT-Data':
  er=s['embedded_tool_responses'];ut=s['user_turns']
  if er==1 and ut<=2:return 'T1_RELATIONAL','LEARNER_VISIBLE_EMBEDDED_RESEARCH_TOPOLOGY','One explicit research observation is incorporated into a subsequent answer.'
  if 1<=er<=3 and ut>=2:return 'T2_SYSTEMS','LEARNER_VISIBLE_EMBEDDED_RESEARCH_TOPOLOGY','Multiple/continued research observations must be integrated across turns.'
  if er>=4 or ut>=5:return 'T3_OPEN_WORLD','LEARNER_VISIBLE_EMBEDDED_RESEARCH_TOPOLOGY','Extended iterative research history is carried across many evidence/update turns.'
 return 'UNRESOLVED_TIER','UNVERIFIED_SOURCE_EPISODE','No learner-visible structural rule currently justifies dependency depth; do not infer from source, domain, trace length or heuristic tags.'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--stage-spec',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();rows=readjl(a.candidate);items=[]
 for i,r in enumerate(rows):
  stage,basis,reason=assign(r);items.append({'atom_id':r['atom_id'],'index':i,'stage':stage,'assignment_basis':basis,'reason':reason,'source':r['source']['repo'],'config':r['source'].get('config'),'subtype':r['pilot'].get('subtype'),'structure':structure(r)})
 counts=collections.Counter(x['stage'] for x in items);basis=collections.Counter(x['assignment_basis'] for x in items);srcstage=collections.Counter((x['source'],x['stage']) for x in items if x['stage']!='UNRESOLVED_TIER')
 out={'schema':'cfe.isd.developmental-stage-map.v2','status':'PARTIAL_STAGE_MAP_V2__STRUCTURAL_SOURCE_RULES_ADDED__UNRESOLVED_ROWS_STILL_BLOCK_FINAL_ORDER_FREEZE','candidate_sha256':hashlib.sha256(a.candidate.read_bytes()).hexdigest(),'candidate_rows':len(rows),'stage_spec_sha256':hashlib.sha256(a.stage_spec.read_bytes()).hexdigest(),'stage_counts':dict(counts),'assignment_basis_counts':dict(basis),'source_stage_counts':{f'{s}::{t}':n for (s,t),n in sorted(srcstage.items())},'resolved_rows':len(rows)-counts.get('UNRESOLVED_TIER',0),'unresolved_rows':counts.get('UNRESOLVED_TIER',0),'items':items,'laws':['STAGE ASSIGNMENT = SIDECAR ONLY','EPISODE TOPOLOGY MAY JUSTIFY DEPENDENCY DEPTH; SOURCE NAME MAY NOT','TOOL COUNT ALONE IS NOT QUALITY OR TIER; RULES REQUIRE OBSERVATION/STATE STRUCTURE','RESEARCH STATE CARRY IS LEARNER-VISIBLE CAUSAL HISTORY','UNRESOLVED_TIER != FAILURE','MATH/CODE DIFFICULTY DOES NOT AUTO-PROMOTE TIER','NO FINAL TRAINING ORDER UNTIL STAGE MAP IS ADEQUATE','NO LEARNER-FACING STAGE LABELS']};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':out['status'],'rows':len(rows),'stage_counts':dict(counts),'resolved_rows':out['resolved_rows'],'unresolved_rows':out['unresolved_rows'],'basis_counts':dict(basis)},indent=2))
if __name__=='__main__':main()
