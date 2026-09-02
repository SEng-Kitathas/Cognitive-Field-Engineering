#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, time
from pathlib import Path
from pypdf import PdfReader


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True); a.manifest.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for p in sorted(a.root.rglob('*.pdf')):
        rel=p.relative_to(a.root)
        dst=a.out/(str(rel).replace('\\','__').replace('/','__')+'.txt')
        rec={'pdf':str(p),'relative_pdf':str(rel),'text_path':str(dst),'status':None}
        try:
            r=PdfReader(str(p)); chunks=[]; extracted_pages=0
            for i,page in enumerate(r.pages,1):
                txt=page.extract_text() or ''
                if txt.strip(): extracted_pages += 1
                chunks.append(f'\n\n===== PAGE {i} =====\n{txt}')
            text=''.join(chunks)
            dst.write_text(text,encoding='utf-8',newline='\n')
            rec.update(status='EXTRACTED',pages=len(r.pages),pages_with_text=extracted_pages,text_bytes=len(text.encode('utf-8')),text_sha256=sha256_bytes(text.encode('utf-8')))
        except Exception as e:
            rec.update(status='ERROR',error=repr(e))
        rows.append(rec); print(json.dumps(rec,sort_keys=True),flush=True)
    m={'schema':'cfe.reasoning-archaeology.pdf-text-cache.v1','created_unix':time.time(),'policy':'LOCAL_DERIVED_TEXT_CACHE_NOT_FOR_RAW_SOURCE_PUBLICATION','count':len(rows),'success':sum(x['status']=='EXTRACTED' for x in rows),'errors':sum(x['status']=='ERROR' for x in rows),'items':rows}
    a.manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'manifest':str(a.manifest),'count':m['count'],'success':m['success'],'errors':m['errors']},indent=2))
if __name__=='__main__': main()
