#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def H(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
def main(root:Path,out:Path):
    rels=[
      'state/next_steps/V11_PREDICATE_POLICY_MECHANISM_PREREG_DRAFT_2026-08-30.json',
      'state/next_steps/V11_PREDICATE_POLICY_PREREG_AMENDMENT_PRE_OUTCOME_2026-08-30.md',
      'state/next_steps/V11_PREDICATE_POLICY_TRAINING_CONTRACT_2026-08-30.json',
      'state/qualification/V11_PREDICATE_POLICY_STATIC_HOSTILE_2026-08-30.json',
      'state/qualification/V11_PREDICATE_POLICY_BASELINE_ADMISSION_20260830/ADMISSION.json',
      'state/qualification/V11_PREDICATE_POLICY_BASELINE_ADMISSION_20260830/PREDICATE_RESULTS.jsonl',
      'state/qualification/V11_PREDICATE_POLICY_BASELINE_ADMISSION_20260830/POLICY_RESULTS.jsonl',
      'tools/build_v11_predicate_policy_candidate.py',
      'tools/audit_v11_predicate_policy_candidate.py',
      'tools/run_v11_predicate_policy_baseline_admission.py',
      'tools/v11_predicate_policy_common.py',
      'tools/train_v11_predicate_policy.py',
      'tools/evaluate_v11_predicate_policy.py',
      'tools/run_v11_predicate_policy_campaign.py'
    ]
    cand=root/'state/candidates/v11_predicate_policy_r2_20260830'
    for p in sorted(cand.iterdir()):
        if p.is_file():rels.append(p.relative_to(root).as_posix())
    files={}
    for rel in rels:
        p=root/rel
        if not p.is_file():raise SystemExit(f'MISSING_LOCK_INPUT {rel}')
        files[rel]={'bytes':p.stat().st_size,'sha256':H(p)}
    # exact expected anchors
    anchors={
      'prereg_sha256':'ebb014831500a6f74961a4fb06af75bf33ba99a290af11e3ff954f8850e196a4',
      'amendment_sha256':'bdd51ca7ff97679dc032529b0386dd1b143c9ab514c51d58e2b100775dc8f1c1',
      'training_contract_sha256':'9945f8369f195a2a7796d96c687f5830ee7ff8d85ab1af7bc517d2ac6800ea6f',
      'candidate_manifest_sha256':'18a846937cce18cef89d48926ebc271817b4ebb3114c45cf13077ab326d4f352',
      'token_audit_sha256':'51c7c8cc10ce435d1a26e0618d45fee968925b40a980b77d31f33135a2c92bbe',
      'baseline_admission_sha256':'695ad60d898072cdf4f7efb58a709969002ee5f52c76ba65adefb8c2f2498917'
    }
    checks={
      'prereg_sha256':files['state/next_steps/V11_PREDICATE_POLICY_MECHANISM_PREREG_DRAFT_2026-08-30.json']['sha256'],
      'amendment_sha256':files['state/next_steps/V11_PREDICATE_POLICY_PREREG_AMENDMENT_PRE_OUTCOME_2026-08-30.md']['sha256'],
      'training_contract_sha256':files['state/next_steps/V11_PREDICATE_POLICY_TRAINING_CONTRACT_2026-08-30.json']['sha256'],
      'candidate_manifest_sha256':files['state/candidates/v11_predicate_policy_r2_20260830/MANIFEST.json']['sha256'],
      'token_audit_sha256':files['state/candidates/v11_predicate_policy_r2_20260830/TOKEN_AUDIT.json']['sha256'],
      'baseline_admission_sha256':files['state/qualification/V11_PREDICATE_POLICY_BASELINE_ADMISSION_20260830/ADMISSION.json']['sha256']
    }
    if checks!=anchors:raise SystemExit('ANCHOR_HASH_DRIFT '+repr({k:(checks[k],anchors[k]) for k in anchors if checks[k]!=anchors[k]}))
    lock={'schema':'cfe.v11.predicate-policy-input-lock.v1','status':'LOCKED_PRE_RUNTIME__NO_SCIENTIFIC_TRAINING','file_count':len(files),'files':files,'anchors':anchors,'scientific_training_authorized':False,'mutation_rule':'Any byte change to a locked file invalidates this lock and requires a new lock before runtime qualification.','laws':['LOCKED_INPUTS != QUALIFIED_RUNTIME','BASELINE_ADMITTED != SCIENTIFIC_EFFECT','LOCK_MUTATION_REQUIRES_NEW_IDENTITY']}
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise SystemExit('REFUSE_OVERWRITE')
    out.write_text(json.dumps(lock,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':lock['status'],'file_count':lock['file_count'],'lock_sha256':H(out)},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path('state/locks/V11_PREDICATE_POLICY_INPUT_LOCK_2026-08-30.json'));a=ap.parse_args();main(a.root.resolve(),a.out)
