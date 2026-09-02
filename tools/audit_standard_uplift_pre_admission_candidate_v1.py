#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any


def H(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''): h.update(b)
    return h.hexdigest()


def jl(p: Path) -> list[dict[str,Any]]:
    out=[]
    with p.open('r',encoding='utf-8',newline='') as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: out.append(json.loads(line))
            except Exception as e: raise ValueError(f'JSONL_PARSE {p}:{i}:{e}') from e
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate-dir',type=Path,required=True); ap.add_argument('--input-pilot',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    man=json.loads((a.candidate_dir/'MANIFEST.json').read_text(encoding='utf-8'))
    cand=jl(a.candidate_dir/'SFT_PRE_ADMISSION_CANDIDATE.jsonl'); exc=jl(a.candidate_dir/'EXCLUDED_QUARANTINE.jsonl'); alt=jl(a.candidate_dir/'ALTERNATE_TRAJECTORY_QUARANTINE.jsonl'); pref=jl(a.candidate_dir/'PREFERENCE_QUARANTINE.jsonl'); inp=jl(a.input_pilot/'SFT_QUARANTINE_ATOMS.jsonl')
    errors=[]; warnings=[]
    files={'candidate':'SFT_PRE_ADMISSION_CANDIDATE.jsonl','excluded':'EXCLUDED_QUARANTINE.jsonl','alternate':'ALTERNATE_TRAJECTORY_QUARANTINE.jsonl','preference':'PREFERENCE_QUARANTINE.jsonl'}
    expected={'candidate':'candidate_sha256','excluded':'excluded_sha256','alternate':'alternate_sha256','preference':'preference_sha256'}
    for k,fn in files.items():
        if H(a.candidate_dir/fn)!=man[expected[k]]: errors.append(f'HASH_MISMATCH:{k}')
    ci={r['atom_id'] for r in cand}; ei={r['atom_id'] for r in exc}; ai={r['atom_id'] for r in alt}; ii={r['atom_id'] for r in inp}
    if len(ci)!=len(cand): errors.append('DUP_CANDIDATE_ATOM_IDS')
    if (ci&ei) or (ci&ai) or (ei&ai): errors.append('PARTITION_OVERLAP')
    if ci|ei|ai != ii: errors.append('PARTITION_NOT_CONSERVATIVE')
    prompts=[r['dedup']['canonical_prompt_hash'] for r in cand]; convs=[r['dedup']['conversation_hash'] for r in cand]
    if len(set(prompts))!=len(prompts): errors.append('CANDIDATE_DUP_PROMPTS')
    if len(set(convs))!=len(convs): errors.append('CANDIDATE_DUP_CONVERSATIONS')
    if any(r['quality']['state']=='RAW' for r in cand): errors.append('RAW_IN_CANDIDATE')
    if any(r['source']['repo']=='nvidia/Open-SWE-Traces' for r in cand): errors.append('SWE_IN_CANDIDATE')
    unresolved=[r['atom_id'] for r in cand if r['license']['state'] not in {'RESOLVED','RESOLVED_PINNED_DATASET_CARD','RESOLVED_PROJECT_GENERATED'}]
    if unresolved: errors.append(f'UNRESOLVED_LICENSES:{len(unresolved)}')
    if any(r['admission']['state']!='PRE_ADMISSION_CANDIDATE' for r in cand): errors.append('BAD_CANDIDATE_ADMISSION_STATE')
    fam=Counter(f for r in cand for f in r['invariants']['lhit_cross_domain']['domain_families'])
    if fam.get('MEMORY_CURRENTNESS',0)<64: errors.append('MEMORY_CURRENTNESS_UNDER_64')
    if fam.get('SCIENCE_DIAGNOSIS',0)<64: errors.append('SCIENCE_DIAGNOSIS_UNDER_64')
    donor=[]
    pats=[('CFE',r'\bcognitive\s+field\s+engineering\b'),('ATMS',r'\bassumption[- ]based\s+(?:truth\s+maintenance\s+system|tms)\b'),('LHIT',r'\bLHIT\b|\blong[- ]horizon\s+interaction\s+training\b')]
    for r in cand:
        text='\n'.join(m.get('content','') for m in r['content'].get('messages',[]))+'\n'+(r['content'].get('final_answer') or '')
        for label,pat in pats:
            if re.search(pat,text,re.I): donor.append({'atom_id':r['atom_id'],'label':label})
    if donor: errors.append(f'DONOR_JARGON:{len(donor)}')
    contam=Counter(r['contamination']['state'] for r in cand)
    blockers=[]
    if any(k!='CLEARED' for k in contam): blockers.append('CONTAMINATION_CLEARANCE_PENDING')
    if len(cand)<1800 or len(cand)>3000: blockers.append('A0_SIZE_RANGE_VIOLATION')
    report={'schema':'cfe.standard-uplift.pre-admission-candidate-audit.v1','status':'PASS_STRUCTURAL__CONTAMINATION_PENDING' if not errors and blockers==['CONTAMINATION_CLEARANCE_PENDING'] else ('PASS' if not errors and not blockers else 'FAIL'),'candidate_dir':str(a.candidate_dir).replace('\\','/'),'manifest_sha256':H(a.candidate_dir/'MANIFEST.json'),'candidate_atoms':len(cand),'excluded_atoms':len(exc),'alternate_atoms':len(alt),'preference_atoms':len(pref),'input_atoms':len(inp),'partition_conservation':len(ci|ei|ai)==len(ii) and ci|ei|ai==ii and not((ci&ei)or(ci&ai)or(ei&ai)),'unique_candidate_prompts':len(set(prompts)),'unique_candidate_conversations':len(set(convs)),'quality_states':dict(Counter(r['quality']['state'] for r in cand)),'license_states':dict(Counter(r['license']['state'] for r in cand)),'contamination_states':dict(contam),'domain_families':dict(fam),'donor_jargon_hits':donor,'errors':errors,'blockers':blockers,'laws':['STRUCTURAL PASS != TRAINABLE','PARTITION CONSERVATION REQUIRED','A0 SIZE RANGE 1800-3000','CONTAMINATION MUST BE EXPLICITLY CLEARED BEFORE TRAINING','NO RAW OR SWE-REVIEW ROWS IN PRE-ADMISSION CANDIDATE']}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n'); print(json.dumps(report,indent=2)); raise SystemExit(0 if not errors else 3)
if __name__=='__main__': main()
