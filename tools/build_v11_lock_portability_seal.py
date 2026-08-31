#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--lock',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.project_root.resolve();lock=json.loads(a.lock.read_text(encoding='utf-8'))
 if a.out.exists():raise SystemExit('REFUSE_OVERWRITE')
 rows={}
 for rel,meta in lock['files'].items():
  p=root/rel
  if not p.is_file():raise SystemExit(f'MISSING {rel}')
  raw=p.read_bytes()
  if sha(raw)!=meta['sha256'] or len(raw)!=meta['bytes']:raise SystemExit(f'RAW_LOCK_MISMATCH {rel}')
  canon=raw.replace(b'\r\n',b'\n')
  rows[rel]={'raw_bytes':len(raw),'raw_sha256':sha(raw),'canonical_rule':'CRLF_TO_LF_ONLY','canonical_bytes':len(canon),'canonical_sha256':sha(canon),'raw_contains_crlf':b'\r\n' in raw}
 out={'schema':'cfe.lock-portability-seal.v1','status':'COMPANION_PORTABILITY_SEAL__ORIGINAL_LOCK_UNCHANGED','original_lock_sha256':sha(a.lock.read_bytes()),'normalization_rule':'Replace each CRLF byte pair (0D 0A) with LF (0A); perform no other transformation.','file_count':len(rows),'files':rows,'authority_ceiling':'NORMALIZATION_EQUIVALENT establishes transport-equivalent text provenance only; original scientific execution remains bound to original raw lock/runtime receipts.','laws':['LOCKED_BYTES != CHECKED_OUT_BYTES','NORMALIZATION_EQUIVALENT != EXACT_BYTES','REPRODUCTION_PROVENANCE_EQUIVALENCE != ORIGINAL_EXECUTION_AUTHORIZATION']}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'status':out['status'],'file_count':out['file_count'],'seal_sha256':sha(a.out.read_bytes())},indent=2))
if __name__=='__main__':main()
