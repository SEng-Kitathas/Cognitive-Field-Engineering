#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def H(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()

def loadj(p:Path): return json.loads(p.read_text(encoding='utf-8-sig'))

def main(root:Path, lock_path:Path, sidecar_path:Path, assurance:str)->int:
    root=root.resolve(); lock_path=lock_path.resolve(); sidecar_path=sidecar_path.resolve()
    lock=loadj(lock_path); side=loadj(sidecar_path)
    if H(lock_path)!=side['original_lock_sha256']:
        print(json.dumps({'status':'FAIL','reason':'ORIGINAL_LOCK_HASH_MISMATCH'},indent=2)); return 2
    failures=[]; exact=[]; normalized=[]
    for rel,meta in lock['files'].items():
        p=root/rel
        if not p.is_file(): failures.append({'path':rel,'reason':'missing'}); continue
        n=p.stat().st_size; h=H(p)
        if n==meta['bytes'] and h==meta['sha256']:
            exact.append(rel); continue
        ent=side['entries'].get(rel)
        if ent and ent.get('relation_to_sealed_bytes')=='CRLF_TO_LF_ONLY' and n==ent['git_checkout_lf_bytes'] and h==ent['git_checkout_lf_sha256']:
            normalized.append(rel); continue
        failures.append({'path':rel,'reason':'content_mismatch','bytes':n,'sha256':h})
    if failures:
        print(json.dumps({'status':'FAIL','failures':failures,'exact_count':len(exact),'normalized_count':len(normalized)},indent=2)); return 2
    if assurance=='exact' and normalized:
        print(json.dumps({'status':'FAIL__NOT_EXACT_SEALED_BYTES','assurance_requested':'exact','exact_count':len(exact),'normalized_checkout_equivalence_count':len(normalized),'normalized_paths':normalized},indent=2)); return 3
    status='PASS__EXACT_SEALED_BYTE_IDENTITY' if not normalized else 'PASS__NORMALIZED_CHECKOUT_EQUIVALENCE__NOT_SEALED_BYTE_IDENTITY'
    print(json.dumps({'status':status,'assurance_requested':assurance,'file_count':len(lock['files']),'exact_count':len(exact),'normalized_checkout_equivalence_count':len(normalized),'laws':side['laws']},indent=2)); return 0

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path.cwd())
    ap.add_argument('--lock',type=Path,default=Path('state/locks/V11_PREDICATE_POLICY_INPUT_LOCK_2026-08-30.json'))
    ap.add_argument('--sidecar',type=Path,default=Path('state/locks/V11_PREDICATE_POLICY_INPUT_LOCK_PORTABILITY_SIDECAR_2026-08-30.json'))
    ap.add_argument('--assurance',choices=('exact','checkout-equivalent'),default='exact')
    a=ap.parse_args(); raise SystemExit(main(a.root,a.lock,a.sidecar,a.assurance))
