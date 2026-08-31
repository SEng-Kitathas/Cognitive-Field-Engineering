#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--checkout-root',type=Path,required=True);ap.add_argument('--seal',type=Path,required=True);a=ap.parse_args();root=a.checkout_root.resolve();seal=json.loads(a.seal.read_text(encoding='utf-8'))
 rows={};counts={'EXACT_BYTES':0,'NORMALIZATION_EQUIVALENT':0,'FAIL':0,'MISSING':0}
 for rel,meta in seal['files'].items():
  p=root/rel
  if not p.is_file():status='MISSING';rows[rel]={'status':status};counts[status]+=1;continue
  raw=p.read_bytes();rh=sha(raw)
  if len(raw)==meta['raw_bytes'] and rh==meta['raw_sha256']:
   status='EXACT_BYTES'
  else:
   canon=raw.replace(b'\r\n',b'\n');ch=sha(canon)
   status='NORMALIZATION_EQUIVALENT' if len(canon)==meta['canonical_bytes'] and ch==meta['canonical_sha256'] else 'FAIL'
  counts[status]+=1;rows[rel]={'status':status,'checked_bytes':len(raw),'checked_sha256':rh}
 overall='PASS_EXACT' if counts['EXACT_BYTES']==len(rows) else 'PASS_NORMALIZATION_EQUIVALENT' if counts['FAIL']==0 and counts['MISSING']==0 else 'FAIL'
 out={'schema':'cfe.lock-portability-verification.v1','status':overall,'seal_sha256':sha(a.seal.read_bytes()),'counts':counts,'files':rows,'authority_ceiling':seal['authority_ceiling']}
 print(json.dumps(out,indent=2,sort_keys=True))
 if overall=='FAIL':raise SystemExit(2)
if __name__=='__main__':main()
