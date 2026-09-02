#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def stable_json(x: Any) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    rows=[]
    with p.open('r',encoding='utf-8',newline='') as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except Exception as exc: raise ValueError(f'JSONL_PARSE_ERROR {p} line={line_no}: {exc}') from exc
    return rows


def write_jsonl(p: Path, rows: list[dict[str, Any]]) -> str:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='\n') as f:
        for r in rows: f.write(stable_json(r)+'\n')
    return sha256_file(p)


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--pilot',type=Path,required=True); ap.add_argument('--license-resolution',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    if a.out.exists(): raise SystemExit(f'REFUSE_OVERWRITE {a.out}')
    summary=json.loads((a.pilot/'SUMMARY.json').read_text(encoding='utf-8'))
    src=a.pilot/'SFT_QUARANTINE_ATOMS.jsonl'; pref=a.pilot/'PREFERENCE_QUARANTINE.jsonl'
    if sha256_file(src)!=summary['sft_sha256'] or sha256_file(pref)!=summary['preference_sha256']: raise SystemExit('PILOT_HASH_MISMATCH')
    lic=json.loads(a.license_resolution.read_text(encoding='utf-8'))
    if lic.get('disposition')!='RESOLVE_PILOT_ROWS_TO_CC-BY-4.0_WITH_PINNED_CARD_PROVENANCE': raise SystemExit('LICENSE_RESOLUTION_NOT_ADMISSIBLE')
    rows=load_jsonl(src); prefs=load_jsonl(pref)
    excluded=[]; working=[]
    for r in rows:
        reasons=[]
        if r.get('quality',{}).get('state')=='RAW': reasons.append('QUALITY_RAW')
        if r.get('source',{}).get('repo')=='nvidia/Open-SWE-Traces': reasons.append('SWE_EVAL_CONTAMINATION_NOT_CLEARED')
        if reasons:
            z=dict(r); z['pre_admission_exclusion']={'reasons':sorted(set(reasons))}; excluded.append(z); continue
        z=json.loads(json.dumps(r))
        if z.get('source',{}).get('repo')=='nvidia/Nemotron-SFT-Agentic-v2':
            if z.get('source',{}).get('revision') != lic['revision']: raise SystemExit('NEMOTRON_AGENT_REVISION_MISMATCH')
            z['license']={
                'state':'RESOLVED_PINNED_DATASET_CARD',
                'labels':['cc-by-4.0'],
                'additional_labels':['apache-2.0','mit'],
                'row_specific':False,
                'notes':'Resolved from pinned dataset card; retain source attribution/provenance.',
                'evidence_sha256':lic['readme_sha256'],
                'evidence_record':str(a.license_resolution).replace('\\','/')
            }
        working.append(z)
    # Repeated exact prompt: keep one deterministic representative; preserve alternates separately.
    groups=defaultdict(list)
    for r in working: groups[r['dedup']['canonical_prompt_hash']].append(r)
    selected=[]; alternates=[]; duplicate_groups=[]
    for ph,grp in groups.items():
        if len(grp)==1:
            selected.append(grp[0]); continue
        ordered=sorted(grp,key=lambda r:r['atom_id'])
        keep=ordered[0]; selected.append(keep)
        alts=ordered[1:]
        for x in alts:
            x['alternate_trajectory_quarantine']={'canonical_prompt_hash':ph,'representative_atom_id':keep['atom_id'],'reason':'EXACT_PROMPT_REPEATED__NO_OBJECTIVE_TRAJECTORY_RANK__KEEP_ONE_DETERMINISTIC_REPRESENTATIVE'}
            alternates.append(x)
        duplicate_groups.append({'canonical_prompt_hash':ph,'input_rows':len(grp),'representative_atom_id':keep['atom_id'],'alternate_atom_ids':[x['atom_id'] for x in alts]})
    selected=sorted(selected,key=lambda r:r['atom_id'])
    for r in selected:
        r['admission']={'state':'PRE_ADMISSION_CANDIDATE','reason':'quality/raw/SWE/prompt-repeat curation applied; contamination/tokenization/final quality/invariant gates remain','review_history':(r.get('admission',{}).get('review_history') or [])+['PRE_ADMISSION_CURATION_V1']}
    a.out.mkdir(parents=True)
    cand_sha=write_jsonl(a.out/'SFT_PRE_ADMISSION_CANDIDATE.jsonl',selected)
    exc_sha=write_jsonl(a.out/'EXCLUDED_QUARANTINE.jsonl',sorted(excluded,key=lambda r:r['atom_id']))
    alt_sha=write_jsonl(a.out/'ALTERNATE_TRAJECTORY_QUARANTINE.jsonl',sorted(alternates,key=lambda r:r['atom_id']))
    pref_sha=write_jsonl(a.out/'PREFERENCE_QUARANTINE.jsonl',prefs)
    manifest={
      'schema':'cfe.standard-uplift.pre-admission-candidate.v1','status':'PRE_ADMISSION_CANDIDATE__CONTAMINATION_AND_FINAL_QUALITY_GATES_PENDING','created_unix':time.time(),
      'input_pilot':str(a.pilot).replace('\\','/'),'input_summary_sha256':sha256_file(a.pilot/'SUMMARY.json'),'input_sft_sha256':summary['sft_sha256'],
      'license_resolution_sha256':sha256_file(a.license_resolution),'candidate_atoms':len(selected),'excluded_rows':len(excluded),'alternate_trajectory_rows':len(alternates),'preference_rows':len(prefs),
      'candidate_sha256':cand_sha,'excluded_sha256':exc_sha,'alternate_sha256':alt_sha,'preference_sha256':pref_sha,
      'candidate_quality_states':dict(Counter(r['quality']['state'] for r in selected)),'candidate_license_states':dict(Counter(r['license']['state'] for r in selected)),'candidate_contamination_states':dict(Counter(r['contamination']['state'] for r in selected)),
      'candidate_domain_families':dict(Counter(f for r in selected for f in r['invariants']['lhit_cross_domain']['domain_families'])),
      'exclusion_reasons':dict(Counter(reason for r in excluded for reason in r['pre_admission_exclusion']['reasons'])),
      'duplicate_prompt_groups_processed':len(duplicate_groups),'duplicate_group_manifest':duplicate_groups,
      'laws':['PRE_ADMISSION_CANDIDATE != TRAINABLE CORPUS','ALTERNATE TRAJECTORY != DUPLICATE CONTENT','NO OBJECTIVE TRAJECTORY RANK -> DO NOT PRETEND LENGTH IS QUALITY','SWE TRACE EXCLUDED UNTIL CONTAMINATION CLEARED','RAW QUALITY EXCLUDED','PINNED LICENSE EVIDENCE REQUIRED FOR LICENSE RESOLUTION','PREFERENCE DATA REMAINS SEPARATE']
    }
    (a.out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
