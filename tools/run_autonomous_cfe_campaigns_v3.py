from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
LIVE_CFE = Path(r"C:\Users\ancal\ProtoAGI\CFE")
SEALED_PARENT = LIVE_CFE / "sealed_parents" / "v09" / "CFE_RND_V0_9_2026-08-25"
HOST_QUAL = LIVE_CFE / "host_qualification"
PCMMAD = Path(r"E:\new pc\AI_Pushes_Sandbox\projects\PCMMAD")
R31 = PCMMAD / "HOSTILE_OS" / "authority" / "RAHL_ENGINEERING_R3_1_EXACT_EXTRACTED" / "RAHL_ENGINEERING_IN_HOUSE_SOP_SPLIT_CANDIDATE_R3_1_2026-08-29"
MODEL = Path(r"D:\Singularity_Works\repo\corpus\models\salvaged_from_lmstudio\Melvin56\Qwen2.5-Coder-7B-Instruct-abliterated-Q4_K_M-GGUF\qwen2.5-coder-7b-instruct-abliterated-q4_k_m.gguf")
MODEL_SHA256 = "b77b39f196ddd460b622fe101a500723887c470db50aebd217fec7370e6724c3"
RUNTIME = Path(r"D:\Singularity_Works\repo\tools\llama_cpp_runtime\b8831_cuda13\llama-server.exe")
RUNTIME_SHA256 = "01ddbfd39cb4f1aaea98dab3108179a78d5caa2105fbc971b871ca158e858c74"
SERVER = "http://127.0.0.1:8091/v1/chat/completions"
RUN_ID = time.strftime("%Y%m%d_%H%M%S")
RUNROOT = PROJECT / "research" / "campaigns" / f"CFE_AUTO_3x20_V3_{RUN_ID}"

SOP_SOURCES = [
    R31 / "03_INTERNAL_RESEARCH_GOVERNANCE.md",
    R31 / "03A_RESEARCH_MACHINERY_AND_MODES.md",
    R31 / "04_EXECUTION_AND_RELEASE_DISCIPLINE.md",
    R31 / "01_ENGINEERING_AUTHORITY_SURFACE.md",
]

RAILS = """CFE PCMMAD/R3.1 scientific-pass law:
1. Evidence inherits; confidence does not. Prior model prose is not evidence. UNKNOWN across untested gaps.
2. Pass N+1 is earned by Pass N. The NEXT question becomes the next pass question verbatim. No prewritten future questions.
3. Exactly 20 qualified scientific passes per campaign. P20 hard-stops; no P21. P20 NEXT is the successor-campaign question.
4. OARR is mandatory each pass: give a concrete rival prediction, counterexample, removal, or altered variant. OARR=NONE is invalid.
5. LOOP+ is mandatory each pass: widen one adjacent plausible branch before convergence. LOOP=NONE is invalid.
6. Semantic Helix is mandatory: emit current survivor plus any new scar/demotion delta. Evidence may persist; confidence is recomputed.
7. Attention Reservoir is mandatory each pass: name a neglected evidence class/branch or explicitly state bounded-complete with what was checked. RESERVOIR=NONE is invalid.
8. CSC is audit-only with ZERO promotion authority and runs after P20. It cannot promote claims or architecture.
9. Research success does not auto-promote product/architecture. Sealed v0.9 is immutable.
10. Action/test output != qualified consequence. Keep source evidence distinct from inference.
11. Every accepted pass must finish cleanly, satisfy all method fields, and produce a complete grammatical NEXT question.
"""

TEXT_SUFFIXES = {".md",".txt",".json",".jsonl",".py",".ps1",".sh",".yaml",".yml",".toml",".ini",".cfg",".csv",".log",".bat",".cmd",".rst"}
STOP = {"the","a","an","and","or","of","to","in","for","on","with","is","are","be","as","by","at","from","this","that","it","its","we","our","you","your","do","does","did","not","no","if","then","than","what","which","how","why","when","where","can","could","should","would","will","must","may","into"}
PASS_FIELDS = ["ANSWER","EVIDENCE","OARR","LOOP","SURVIVE","SCAR","DEMOTE","RESERVOIR","DISPOSITION","CONFIDENCE","NEXT"]

@dataclass
class Chunk:
    source: str
    text: str
    terms: set[str]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def termset(text: str) -> set[str]:
    return {x for x in re.findall(r"[A-Za-z0-9_+.-]{3,}", text.lower()) if x not in STOP}


def read_text(path: Path, limit: int = 1_200_000) -> str:
    try:
        data = path.read_bytes()[:limit]
    except Exception:
        return ""
    if b"\x00" in data[:4096]:
        for enc in ("utf-16","utf-16-le","utf-8"):
            try: return data.decode(enc)
            except Exception: pass
        return ""
    for enc in ("utf-8","utf-8-sig","cp1252"):
        try: return data.decode(enc)
        except Exception: pass
    return ""


def build_corpus() -> list[Chunk]:
    paths: list[Path] = []
    for p in [PROJECT/"state"/"current.md", PROJECT/"state"/"next_steps.md", PROJECT/"state"/"qualified_campaign_seed.json"]:
        if p.exists(): paths.append(p)
    for root in (SEALED_PARENT, HOST_QUAL):
        if not root.exists(): continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and ".venv" not in str(p).lower():
                paths.append(p)
    chunks: list[Chunk] = []
    for p in paths:
        txt = read_text(p)
        if not txt.strip(): continue
        for i, para in enumerate(re.split(r"\n\s*\n", txt)):
            para = " ".join(para.strip().split())
            if len(para) < 45: continue
            for j in range(0, len(para), 650):
                sub = para[j:j+760]
                if len(sub) >= 45:
                    chunks.append(Chunk(f"{p}#p{i}.{j//650}", sub, termset(sub)))
    return chunks


def retrieve(corpus: list[Chunk], question: str, helix: dict[str,list[str]], k: int = 5) -> list[Chunk]:
    carry = " ".join(helix["survivors"][-3:] + helix["scars"][-3:] + helix["demotions"][-3:])
    q = termset(question + " " + carry)
    scored: list[tuple[float,Chunk]] = []
    for c in corpus:
        ov = len(q & c.terms)
        if not ov: continue
        score = ov / (1.0 + 0.02 * max(0,len(c.terms)-30))
        s = c.source.lower()
        if "state\\current.md" in s or "state/current.md" in s: score += 1.8
        if "next_steps" in s: score += 1.3
        scored.append((score,c))
    scored.sort(key=lambda x:(-x[0],x[1].source))
    return [c for _,c in scored[:k]]


def ask(user: str, max_tokens: int = 175, temperature: float = 0.18) -> tuple[str,dict[str,Any]]:
    payload = {
        "model":"local",
        "messages":[
            {"role":"system","content":RAILS + "\nBe compact. Do not echo instructions. Never put '||' inside a field value."},
            {"role":"user","content":user},
        ],
        "temperature":temperature,
        "max_tokens":max_tokens,
        "stream":False,
    }
    req = urllib.request.Request(SERVER,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=120) as r:
        raw=json.loads(r.read().decode("utf-8"))
    ch=raw["choices"][0]
    return (ch["message"].get("content") or "").strip(), {
        "finish_reason":ch.get("finish_reason"),"usage":raw.get("usage"),"timings":raw.get("timings"),
        "model":raw.get("model"),"fingerprint":raw.get("system_fingerprint")
    }


def parse_fields(text: str, names: list[str]) -> dict[str,str]:
    clean=text.replace("\r"," ").replace("\n"," || ")
    positions=[]
    for name in names:
        pat=rf"(?i)(?:^|\|\|)\s*{re.escape(name)}\s*(?:=|:)\s*"
        m=re.search(pat,clean)
        if m: positions.append((m.start(),name,m.end()))
    positions.sort()
    out={}
    for i,(st,name,vs) in enumerate(positions):
        end=positions[i+1][0] if i+1<len(positions) else len(clean)
        out[name]=clean[vs:end].strip(" |\t\n\r\"'")
    return out


def question_valid(q: str) -> tuple[bool,str]:
    q=q.strip()
    if not q.endswith("?"): return False,"missing question mark"
    words=re.findall(r"\b[\w`.+/-]+\b",q)
    if len(words)<8: return False,"too short"
    if re.search(r"\b(on|of|for|with|to|in|by|from|about|between|and|or)\?\s*$",q,re.I): return False,"ends on dangling preposition/conjunction"
    if "<" in q or ">" in q: return False,"contains placeholder"
    if q.lower().startswith("what is the next step") and len(words)<12: return False,"generic next-step question"
    return True,"ok"


def field_invalid(v: str) -> bool:
    return not v.strip() or v.strip().upper() in {"NONE","N/A","NA","UNKNOWN"}


def validate_pass(fields: dict[str,str], meta: dict[str,Any], pnum:int) -> list[str]:
    errs=[]
    for f in PASS_FIELDS:
        if not fields.get(f): errs.append(f"missing {f}")
    if meta.get("finish_reason") != "stop": errs.append(f"finish_reason={meta.get('finish_reason')}")
    for f in ("OARR","LOOP","SURVIVE","RESERVOIR"):
        if f in fields and field_invalid(fields[f]): errs.append(f"{f} lacks mandatory content")
    if "EVIDENCE" in fields and field_invalid(fields["EVIDENCE"]): errs.append("EVIDENCE empty/unknown")
    if "NEXT" in fields:
        ok,why=question_valid(fields["NEXT"] if fields["NEXT"].endswith("?") else fields["NEXT"]+"?")
        if not ok: errs.append(f"NEXT invalid: {why}")
    if pnum==20 and "DISPOSITION" in fields and "HARD_STOP_P20" not in fields["DISPOSITION"]:
        errs.append("P20 disposition missing HARD_STOP_P20")
    return errs


def normalize_next(q:str)->str:
    q=q.strip()
    if not q.endswith("?"): q=q.rstrip(". ")+"?"
    return q


def generate_pass(cnum:int,pnum:int,question:str,corpus:list[Chunk],helix:dict[str,list[str]],prev:dict[str,Any]|None) -> tuple[dict[str,Any],dict[str,Any]]:
    ev=retrieve(corpus,question,helix,k=5)
    evtxt="\n".join(f"[{i+1}] {c.source}: {c.text[:410]}" for i,c in enumerate(ev))
    prevtxt="NONE" if prev is None else f"ANSWER={prev['ANSWER']} | DISPOSITION={prev['DISPOSITION']} | SURVIVE={prev['SURVIVE']} | SCAR={prev['SCAR']} | DEMOTE={prev['DEMOTE']}"
    htxt=json.dumps({k:v[-3:] for k,v in helix.items()},ensure_ascii=False)
    slice_name=["A","B","C","D"][(pnum-1)//5]
    p20=pnum==20
    fmt="ANSWER=<max 24 words> || EVIDENCE=<max 24 words, cite [n]> || OARR=<max 16 words concrete rival/counterexample/removal> || LOOP=<max 14 words adjacent branch> || SURVIVE=<max 12 words current survivor> || SCAR=<max 12 words or NONE> || DEMOTE=<max 12 words or NONE> || RESERVOIR=<max 14 words neglected evidence class or bounded-complete check> || DISPOSITION=<max 10 words> || CONFIDENCE=<0..1> || NEXT=<one complete specific question?>"
    prompt=(
        f"CAMPAIGN {cnum} PASS {pnum}/20. OARR SLICE {slice_name}.\nACTIVE QUESTION: {question}\n"
        f"PREDECESSOR: {prevtxt[:700]}\nCUMULATIVE HELIX: {htxt[:900]}\nSOURCE EVIDENCE:\n{evtxt[:2500]}\n\n"
        "Produce one qualified scientific-pass record. OARR, LOOP, SURVIVE, and RESERVOIR MUST contain substantive content; do not write NONE for those fields. "
        "SCAR and DEMOTE may be NONE only if no new delta is earned. Distinguish evidence from inference. "
        + ("This is P20: DISPOSITION MUST contain HARD_STOP_P20; NEXT MUST be a successor-campaign question, never P21. " if p20 else "NEXT will become the next pass question verbatim. ")
        + "FORMAT EXACTLY: "+fmt
    )
    attempts=[]
    raw,meta=ask(prompt,max_tokens=190,temperature=0.16)
    for attempt in range(1,4):
        fields=parse_fields(raw,PASS_FIELDS)
        if fields.get("NEXT"): fields["NEXT"]=normalize_next(fields["NEXT"])
        errs=validate_pass(fields,meta,pnum)
        attempts.append({"attempt":attempt,"raw":raw,"meta":meta,"errors":errs})
        if not errs:
            try: conf=float(re.findall(r"(?:0(?:\.\d+)?|1(?:\.0+)?)",fields["CONFIDENCE"])[0])
            except Exception: conf=None
            obj={**fields,"confidence_numeric":conf,"campaign":cnum,"pass":pnum,"active_question":question,"oarr_slice":slice_name,"source_refs":[c.source for c in ev],"promotion_authority":"NONE","qualification_attempts":attempts}
            if p20: obj["hard_stop"]=True
            return obj,meta
        repair=(
            f"SAME PASS REPAIR. Do not change ACTIVE QUESTION. Your prior record failed qualification: {errs}. "
            "Re-answer from the SAME evidence below; do not invent new evidence. Fill every mandatory process field. "
            f"ACTIVE QUESTION: {question}\nSOURCE EVIDENCE:\n{evtxt[:2200]}\nPRIOR RAW:\n{raw[:1800]}\nFORMAT EXACTLY: {fmt}"
        )
        raw,meta=ask(repair,max_tokens=205,temperature=0.08)
    raise RuntimeError(f"pass {cnum}/{pnum} failed method qualification after 3 model attempts: {attempts[-1]['errors']}")


def update_helix(helix:dict[str,list[str]],obj:dict[str,Any])->dict[str,list[str]]:
    mapping={"SURVIVE":"survivors","SCAR":"scars","DEMOTE":"demotions"}
    for src,dst in mapping.items():
        v=obj.get(src,"").strip()
        if v and v.upper() not in {"NONE","N/A","NA"} and v not in helix[dst]: helix[dst].append(v)
    return helix


def write_json(path:Path,obj:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")


def append_jsonl(path:Path,obj:Any)->None:
    with path.open("a",encoding="utf-8",newline="\n") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")


def csc_audit(cdir:Path,records:list[dict[str,Any]],helix:dict[str,list[str]])->dict[str,Any]:
    errs=[]
    if len(records)!=20: errs.append(f"pass_count={len(records)}")
    for i in range(19):
        if records[i]["NEXT"]!=records[i+1]["active_question"]: errs.append(f"question_chain_break_P{i+1:02d}_P{i+2:02d}")
    if not records[-1].get("hard_stop"): errs.append("p20_hard_stop_missing")
    if list(cdir.glob("P21*")): errs.append("p21_present")
    for r in records:
        for f in ("OARR","LOOP","SURVIVE","RESERVOIR"):
            if field_invalid(str(r.get(f,""))): errs.append(f"P{r['pass']:02d}_{f}_missing")
        if r.get("promotion_authority")!="NONE": errs.append(f"P{r['pass']:02d}_promotion_leak")
        ok,why=question_valid(r["NEXT"]); 
        if not ok: errs.append(f"P{r['pass']:02d}_NEXT_{why}")
    ledger="\n".join(f"P{r['pass']:02d} Q={r['active_question']} | OARR={r['OARR']} | LOOP={r['LOOP']} | RES={r['RESERVOIR']} | D={r['DISPOSITION']} | NEXT={r['NEXT']}" for r in records)
    fmt="VERDICT=<PASS or REVIEW> || ERRORS=<NONE or brief> || WARNINGS=<NONE or brief> || SURVIVOR=<strongest survivor> || SCAR=<strongest scar or NONE> || SUCCESSOR_VALID=<YES or NO>"
    prompt=(
        "CSC SHADOW AUDIT. ZERO promotion authority. Audit the 20-pass chain for discriminator causality, evidence/inference separation, OARR pressure, LOOP+ breadth, Helix continuity, Attention Reservoir breadth, hard stop, and no auto-promotion. "
        f"DETERMINISTIC ERRORS={errs}. CUMULATIVE HELIX={json.dumps(helix,ensure_ascii=False)[:1500]}. PASS LEDGER:\n{ledger[:6500]}\nFORMAT EXACTLY: {fmt}"
    )
    raw,meta=ask(prompt,max_tokens=145,temperature=0.05)
    names=["VERDICT","ERRORS","WARNINGS","SURVIVOR","SCAR","SUCCESSOR_VALID"]
    fields=parse_fields(raw,names)
    if any(not fields.get(n) for n in names):
        raw2,meta2=ask("REFORMAT ONLY THIS CSC AUDIT. FORMAT EXACTLY: "+fmt+"\nRAW:\n"+raw[:2000],max_tokens=155,temperature=0.02)
        fields=parse_fields(raw2,names); raw=raw+"\n---REPAIR---\n"+raw2; meta={"first":meta,"repair":meta2}
    model_pass=fields.get("VERDICT","").upper().startswith("PASS") and fields.get("SUCCESSOR_VALID","").upper().startswith("YES")
    return {"authority":"AUDIT_ONLY_NONE_PROMOTION","deterministic_errors":errs,"model_fields":fields,"raw":raw,"model_meta":meta,"verdict":"PASS" if not errs and model_pass else "REVIEW","p20_successor_question":records[-1]["NEXT"]}


def main()->int:
    RUNROOT.mkdir(parents=True,exist_ok=False)
    corpus=build_corpus()
    seed_path=PROJECT/"state"/"qualified_campaign_seed.json"
    seed=json.loads(seed_path.read_text(encoding="utf-8"))
    first=normalize_next(str(seed["question"]))
    manifest={
        "run_id":RUN_ID,"campaign_count":3,"passes_per_campaign":20,"planned_scientific_passes":60,
        "qualification":"HARD_PER_PASS_OARR_LOOP_HELIX_RESERVOIR_NEXT_GATE","question_authoring":"MODEL_CHAIN_ONLY_NO_HAND_AUTHORED_PASS_QUESTIONS",
        "seed_source":str(seed_path),"seed_sha256":sha256_bytes(seed_path.read_bytes()),"seed_question":first,
        "model_path":str(MODEL),"model_sha256":MODEL_SHA256,"runtime_path":str(RUNTIME),"runtime_sha256":RUNTIME_SHA256,
        "network_downloads":"NONE","server":SERVER,"corpus_chunks":len(corpus),"sealed_parent":str(SEALED_PARENT),"sealed_parent_mutation_allowed":False,
        "sop_sources":[str(p) for p in SOP_SOURCES],"rails":RAILS,"csc_authority":"AUDIT_ONLY_NONE_PROMOTION"
    }
    write_json(RUNROOT/"RUN_MANIFEST.json",manifest)
    write_json(RUNROOT/"PASS0_AUTONOMOUS_SEED.json",seed)
    summaries=[]; campaign_seed=first
    for cnum in range(1,4):
        cdir=RUNROOT/f"C{cnum:03d}"; cdir.mkdir(parents=True)
        write_json(cdir/"CAMPAIGN_SEED.json",{"campaign":cnum,"question":campaign_seed,"source":"QUALIFIED_PASS0" if cnum==1 else "PRIOR_CAMPAIGN_P20_NEXT"})
        records=[]; helix={"survivors":[],"scars":[],"demotions":[]}; q=campaign_seed; prev=None
        for pnum in range(1,21):
            try:
                obj,meta=generate_pass(cnum,pnum,q,corpus,helix,prev)
            except Exception as exc:
                write_json(cdir/f"P{pnum:02d}_QUALIFICATION_FAILURE.json",{"campaign":cnum,"pass":pnum,"active_question":q,"error":repr(exc),"accepted":False})
                raise
            update_helix(helix,obj)
            write_json(cdir/f"P{pnum:02d}.json",{"result":obj,"model_meta":meta})
            append_jsonl(cdir/"HELIX_LEDGER.jsonl",{"pass":pnum,"delta":{"survive":obj["SURVIVE"],"scar":obj["SCAR"],"demote":obj["DEMOTE"]},"cumulative":helix})
            append_jsonl(cdir/"OARR_LOOP_LEDGER.jsonl",{"pass":pnum,"slice":obj["oarr_slice"],"oarr":obj["OARR"],"loop_plus":obj["LOOP"]})
            append_jsonl(cdir/"RESERVOIR_LEDGER.jsonl",{"pass":pnum,"reservoir":obj["RESERVOIR"],"sources":obj["source_refs"]})
            records.append(obj); prev=obj; q=obj["NEXT"]
            print(json.dumps({"event":"pass_qualified","campaign":cnum,"pass":pnum,"oarr":obj["OARR"],"loop":obj["LOOP"],"reservoir":obj["RESERVOIR"],"disposition":obj["DISPOSITION"],"next_question":q},ensure_ascii=False),flush=True)
        audit=csc_audit(cdir,records,helix); write_json(cdir/"CSC_AUDIT.json",audit)
        write_json(cdir/"P20_HANDOFF.json",{"hard_stop":True,"no_p21":True,"successor_campaign_question":records[-1]["NEXT"],"csc_verdict":audit["verdict"],"campaign_disposition":records[-1]["DISPOSITION"],"promotion_authority":"NONE"})
        if audit["verdict"]!="PASS":
            raise RuntimeError(f"CSC audit failed/review at campaign {cnum}: {audit['deterministic_errors']} {audit['model_fields']}")
        summaries.append({"campaign":cnum,"seed_question":records[0]["active_question"],"p20_disposition":records[-1]["DISPOSITION"],"successor_question":records[-1]["NEXT"],"csc_verdict":audit["verdict"],"helix":helix})
        campaign_seed=records[-1]["NEXT"]
        print(json.dumps({"event":"campaign_qualified","campaign":cnum,"csc":"PASS","successor_question":campaign_seed},ensure_ascii=False),flush=True)
    write_json(RUNROOT/"CAMPAIGN_SUMMARY.json",summaries)
    write_json(RUNROOT/"FINAL_HANDOFF.json",{"completed_campaigns":3,"qualified_scientific_passes":60,"hard_stops_honored":True,"next_question":campaign_seed,"promotion_authority":"NONE","sealed_parent_mutated":False})
    print(json.dumps({"event":"run_qualified","runroot":str(RUNROOT),"next_question":campaign_seed},ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
