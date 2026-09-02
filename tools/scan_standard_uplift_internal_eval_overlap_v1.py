#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, time
from collections import defaultdict
from pathlib import Path
from typing import Any


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def H(s: str) -> str:
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9_./:-]+", norm(s))


def shingles(s: str, n: int = 3) -> set[tuple[str,...]]:
    t=words(s)
    if len(t)<n: return {tuple(t)} if t else set()
    return {tuple(t[i:i+n]) for i in range(len(t)-n+1)}


def jac(a:set[Any],b:set[Any])->float:
    return len(a&b)/len(a|b) if a and b else 0.0


def candidate_prompt(r: dict[str,Any]) -> str:
    return "\n".join(m.get("content","") for m in r.get("content",{}).get("messages",[]) if m.get("role")=="user")


def recursively_collect_text(obj: Any, key: str = "") -> list[tuple[str,str]]:
    out=[]
    if isinstance(obj,str):
        # Only long-enough textual material; caller filters fields/length.
        if len(norm(obj))>=30: out.append((key,obj))
    elif isinstance(obj,list):
        for i,x in enumerate(obj): out.extend(recursively_collect_text(x,f"{key}[{i}]"))
    elif isinstance(obj,dict):
        for k,v in obj.items(): out.extend(recursively_collect_text(v,f"{key}.{k}" if key else str(k)))
    return out


def field_relevant(key: str) -> bool:
    k=key.lower()
    return any(x in k for x in ["prompt","question","input","instruction","message","conversation","scenario","query","task","text","content"])


def read_jsonl(p:Path):
    with p.open('r',encoding='utf-8',errors='replace',newline='') as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: yield i,json.loads(line)
            except Exception: continue


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',type=Path,required=True); ap.add_argument('--project-root',type=Path,default=Path('.')); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--near',type=float,default=0.90); a=ap.parse_args()
    cands=[]
    with a.candidate.open('r',encoding='utf-8',newline='') as f:
        for line in f:
            if line.strip():
                r=json.loads(line); p=candidate_prompt(r); cands.append({'atom_id':r['atom_id'],'prompt':p,'hash':H(p),'sh':shingles(p)})
    eval_paths=[]
    candroot=a.project_root/'state'/'candidates'
    for p in candroot.rglob('*.jsonl'):
        rel=str(p).replace('\\','/')
        if '.private.jsonl' in rel or 'fresh_eval' in rel.lower() or '/eval_' in rel.lower() or '/lhit.jsonl' in rel.lower() or '/independent_rows.jsonl' in rel.lower() or '/neighborhood_blocks.jsonl' in rel.lower() or '/random_blocks_control.jsonl' in rel.lower():
            eval_paths.append(p)
    eval_items=[]; exact_map=defaultdict(list)
    for p in sorted(set(eval_paths)):
        rel=str(p.relative_to(a.project_root)).replace('\\','/')
        for line_no,obj in read_jsonl(p):
            for key,text in recursively_collect_text(obj):
                if not field_relevant(key): continue
                n=norm(text)
                if len(n)<30: continue
                item={'path':rel,'line':line_no,'field':key,'text':text,'hash':H(text),'sh':shingles(text)}
                exact_map[item['hash']].append(len(eval_items)); eval_items.append(item)
    exact=[]; near=[]; max_near={'score':0.0,'candidate_atom':None,'eval_path':None,'eval_line':None,'eval_field':None}
    # Inverted shingle index to avoid all-pairs.
    inv=defaultdict(set)
    for i,e in enumerate(eval_items):
        for sh in e['sh']: inv[sh].add(i)
    for c in cands:
        for idx in exact_map.get(c['hash'],[]):
            e=eval_items[idx]; exact.append({'candidate_atom':c['atom_id'],'eval_path':e['path'],'eval_line':e['line'],'eval_field':e['field']})
        possible=set()
        for sh in c['sh']: possible.update(inv.get(sh,()))
        for idx in possible:
            e=eval_items[idx]; score=jac(c['sh'],e['sh'])
            if score>max_near['score']:
                max_near={'score':score,'candidate_atom':c['atom_id'],'eval_path':e['path'],'eval_line':e['line'],'eval_field':e['field']}
            if score>=a.near and c['hash']!=e['hash']:
                near.append({'candidate_atom':c['atom_id'],'eval_path':e['path'],'eval_line':e['line'],'eval_field':e['field'],'jaccard_3gram':score})
    report={'schema':'cfe.standard-uplift.internal-eval-overlap.v1','date':'2026-09-02','status':'PASS_NO_CURRENT_INTERNAL_OVERLAP' if not exact and not near else 'REVIEW_OVERLAP_FOUND','candidate':str(a.candidate).replace('\\','/'),'candidate_atoms':len(cands),'internal_eval_files':len(set(eval_paths)),'internal_eval_text_items':len(eval_items),'exact_matches':len(exact),'near_threshold':a.near,'near_matches':len(near),'max_nonexact_similarity':max_near,'exact_examples':exact[:100],'near_examples':sorted(near,key=lambda x:-x['jaccard_3gram'])[:100],'scope_guard':'CURRENT_INTERNAL CFE EVAL ONLY. Does not clear protected public benchmark families and must be rerun after final fleet phenotype/eval registry is frozen.','laws':['INTERNAL PASS != GLOBAL DECONTAMINATION','EXACT PRIVATE EVAL MATCH BLOCKS TRAINING','NEAR PRIVATE EVAL MATCH REQUIRES REVIEW','FINAL EVAL FREEZE REQUIRES RERUN']}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
