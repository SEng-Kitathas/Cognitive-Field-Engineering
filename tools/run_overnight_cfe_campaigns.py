from __future__ import annotations

import hashlib
import json
import os
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
GEN_MODEL = Path(r"D:\Singularity_Works\repo\corpus\models\salvaged_from_lmstudio\Melvin56\Qwen2.5-Coder-7B-Instruct-abliterated-Q4_K_M-GGUF\qwen2.5-coder-7b-instruct-abliterated-q4_k_m.gguf")
GEN_SHA = "b77b39f196ddd460b622fe101a500723887c470db50aebd217fec7370e6724c3"
DIV_MODEL = Path(r"D:\Singularity_Works\repo\corpus\models\internet_acquired\bartowski\Qwen2.5-Coder-1.5B-Instruct-abliterated-GGUF\Qwen2.5-Coder-1.5B-Instruct-abliterated-Q4_K_L.gguf")
DIV_SHA = "108902ab59d8988d6efa27b06eb0675dcbf52b8209c7b49332172e2f5c003535"
RUNTIME = Path(r"D:\Singularity_Works\repo\tools\llama_cpp_runtime\b8831_cuda13\llama-server.exe")
RUNTIME_SHA = "01ddbfd39cb4f1aaea98dab3108179a78d5caa2105fbc971b871ca158e858c74"
GEN_SERVER = "http://127.0.0.1:8091/v1/chat/completions"
DIV_SERVER = "http://127.0.0.1:8092/v1/chat/completions"
RUN_ID = time.strftime("%Y%m%d_%H%M%S")
OVERNIGHT_LABEL = os.environ.get("CFE_OVERNIGHT_LABEL","GENERAL").strip().replace(" ","_")
RUNROOT = PROJECT / "research" / "campaigns" / f"OVERNIGHT_{OVERNIGHT_LABEL}_3x20_{RUN_ID}"

SOP_SOURCES = [
    R31 / "03_INTERNAL_RESEARCH_GOVERNANCE.md",
    R31 / "03A_RESEARCH_MACHINERY_AND_MODES.md",
    R31 / "04_EXECUTION_AND_RELEASE_DISCIPLINE.md",
    R31 / "01_ENGINEERING_AUTHORITY_SURFACE.md",
]

RAILS = """CFE PCMMAD/R3.1 campaign law:
- Evidence inherits; confidence does not. Model prose is not evidence. UNKNOWN across untested gaps.
- Pass N+1 is earned only by Pass N. No future pass questions are preauthored.
- Exactly 20 qualified passes; P20 hard-stop; no P21; P20 emits successor-campaign question.
- OARR hostile rival/counterexample/removal is mandatory each pass and has no promotion authority.
- LOOP+ adjacent possibility expansion is mandatory each pass and has no promotion authority.
- Semantic Helix explicitly persists survivors/scars/demotions while confidence is re-earned.
- Attention Reservoir breadth check runs every pass.
- CSC is audit-only with ZERO promotion authority and runs after P20.
- Research success never auto-promotes product/architecture; sealed v0.9 remains immutable.
- Tool/test/action output != qualified consequence. Current project evidence outranks stale narrative.
- No model download/training execution inside these pre-live campaigns.
"""

TEXT_SUFFIXES={".md",".txt",".json",".jsonl",".py",".ps1",".sh",".yaml",".yml",".toml",".ini",".cfg",".csv",".log",".bat",".cmd",".rst"}
STOP={"the","a","an","and","or","of","to","in","for","on","with","is","are","be","as","by","at","from","this","that","it","its","we","our","you","your","do","does","did","not","no","if","then","than","what","which","how","why","when","where","can","could","should","would","will","must","may","into"}
SYN_FIELDS=["ANSWER","EVIDENCE","SURVIVE","SCAR","DEMOTE","DISPOSITION","CONFIDENCE","NEXT"]

@dataclass
class Chunk:
    source:str
    text:str
    terms:set[str]
    cls:str


def sha256_bytes(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def termset(t:str)->set[str]: return {x for x in re.findall(r"[A-Za-z0-9_+.-]{3,}",t.lower()) if x not in STOP}

def read_text(p:Path,limit:int=1_200_000)->str:
    try: data=p.read_bytes()[:limit]
    except Exception: return ""
    if b"\x00" in data[:4096]:
        for enc in ("utf-16","utf-16-le","utf-8"):
            try:return data.decode(enc)
            except Exception:pass
        return ""
    for enc in ("utf-8","utf-8-sig","cp1252"):
        try:return data.decode(enc)
        except Exception:pass
    return ""

def source_class(p:Path)->str:
    s=str(p).lower(); n=p.name.lower()
    if "state\\current" in s or "state/current" in s:return "current_state"
    if "next_steps" in s:return "next_steps"
    if "host_qualification" in s:return "host_qualification"
    if "test" in n or "\\tests\\" in s or "/tests/" in s:return "tests"
    if p.suffix.lower()==".py":return "source_code"
    if "manifest" in n or "sha256" in n:return "manifest_integrity"
    if p.suffix.lower() in {".log",".txt"} and any(k in n for k in ("log","receipt","exit","stdout","stderr")):return "execution_evidence"
    if p.suffix.lower() in {".jsonl",".json",".csv"}:return "data_contract"
    return "documentation"

def build_corpus()->list[Chunk]:
    paths=[]
    for p in [PROJECT/"state"/"current.md",PROJECT/"state"/"next_steps.md",PROJECT/"state"/"qualified_campaign_seed.json"]:
        if p.exists():paths.append(p)
    # Overnight research ingress: current CFE research/cartography evidence plus historical sealed/runtime evidence.
    for root in (PROJECT/"research", PROJECT/"state"/"analysis", PROJECT/"state"/"doctrine_snapshot", PROJECT/"policy", SEALED_PARENT, HOST_QUAL):
        if not root.exists():continue
        for p in root.rglob("*"):
            try:
                if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and ".venv" not in str(p).lower() and p.stat().st_size <= 2_000_000:paths.append(p)
            except OSError:pass
    out=[]
    for p in paths:
        txt=read_text(p)
        if not txt.strip():continue
        cls=source_class(p)
        for i,para in enumerate(re.split(r"\n\s*\n",txt)):
            para=" ".join(para.strip().split())
            if len(para)<45:continue
            for j in range(0,len(para),650):
                sub=para[j:j+760]
                if len(sub)>=45:out.append(Chunk(f"{p}#p{i}.{j//650}",sub,termset(sub),cls))
    return out

def retrieve(corpus:list[Chunk],qtext:str,helix:dict[str,list[str]],k:int=5)->list[Chunk]:
    carry=" ".join(helix["survivors"][-3:]+helix["scars"][-3:]+helix["demotions"][-3:])
    q=termset(qtext+" "+carry); scored=[]
    for c in corpus:
        ov=len(q&c.terms)
        if not ov:continue
        score=ov/(1.0+0.02*max(0,len(c.terms)-30))
        if c.cls=="current_state":score+=2.0
        if c.cls=="next_steps":score+=1.6
        scored.append((score,c))
    scored.sort(key=lambda x:(-x[0],x[1].source))
    # diversity-aware top-k: first best per class, then fill by score
    chosen=[]; seen=set()
    for _,c in scored:
        if c.cls not in seen:
            chosen.append(c);seen.add(c.cls)
            if len(chosen)>=k:break
    if len(chosen)<k:
        for _,c in scored:
            if c not in chosen:
                chosen.append(c)
                if len(chosen)>=k:break
    return chosen

def standing_evidence()->list[tuple[str,str,str]]:
    return [
        ("S1","current_state",read_text(PROJECT/"state"/"current.md",120_000)[:2600]),
        ("S2","next_steps",read_text(PROJECT/"state"/"next_steps.md",120_000)[:2800]),
    ]
def call(url:str,system:str,user:str,max_tokens:int,temp:float)->tuple[str,dict[str,Any]]:
    payload={"model":"local","messages":[{"role":"system","content":system},{"role":"user","content":user}],"temperature":temp,"max_tokens":max_tokens,"stream":False}
    req=urllib.request.Request(url,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=120) as r:raw=json.loads(r.read().decode("utf-8"))
    ch=raw["choices"][0]
    return (ch["message"].get("content") or "").strip(),{"finish_reason":ch.get("finish_reason"),"usage":raw.get("usage"),"timings":raw.get("timings"),"model":raw.get("model"),"fingerprint":raw.get("system_fingerprint")}
def parse_fields(text:str,names:list[str])->dict[str,str]:
    clean=text.replace("\r"," ").replace("\n"," || ");pos=[]
    for name in names:
        m=re.search(rf"(?i)(?:^|\|\|)\s*{re.escape(name)}\s*(?:=|:)\s*",clean)
        if m:pos.append((m.start(),name,m.end()))
    pos.sort();out={}
    for i,(st,name,vs) in enumerate(pos):
        end=pos[i+1][0] if i+1<len(pos) else len(clean)
        out[name]=clean[vs:end].strip(" |\t\n\r\"'")
    return out

def normalize_q(q:str)->str:
    q=q.strip()
    if not q.endswith("?"):q=q.rstrip(". ")+"?"
    return q

def qvalid(q:str)->tuple[bool,str]:
    q=q.strip(); words=re.findall(r"\b[\w`.+/-]+\b",q)
    if not q.endswith("?"):return False,"missing_question_mark"
    if len(words)<8:return False,"too_short"
    if re.search(r"\b(on|of|for|with|to|in|by|from|about|between|and|or)\?\s*$",q,re.I):return False,"dangling_end"
    if "<" in q or ">" in q:return False,"placeholder"
    if q.lower().startswith("what is the impact") and len(words)<12:return False,"underspecified_impact"
    return True,"ok"
def write_json(p:Path,o:Any)->None:
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def append_jsonl(p:Path,o:Any)->None:
    with p.open("a",encoding="utf-8",newline="\n") as f:f.write(json.dumps(o,ensure_ascii=False)+"\n")

def divergence(question:str,evidence:str)->tuple[dict[str,str],dict[str,Any],str]:
    system=("You are R2 Divergent Imagination Engine operating as adversarial pressure only, with ZERO truth/promotion authority. "
            "Generate a mechanistic OARR challenge that could falsify or materially weaken the incumbent path, and a distinct LOOP+ adjacent branch worth checking. "
            "OARR must contain a rival condition plus an observable consequence; LOOP must name an adjacent mechanism/evidence class and why it could change the conclusion. "
            "Do not restate the incumbent, do not output bare artifact names, do not propose downloads/training. "
            "Return exactly: OARR=If <specific rival condition>, then <observable consequence that challenges the current path>. || LOOP=Also test whether <specific adjacent mechanism/evidence branch> changes the conclusion because <brief reason>.")
    raws=[]; metas=[]
    raw,meta=call(GEN_SERVER,system,f"QUESTION: {question}\nSOURCE EVIDENCE:\n{evidence[:4200]}",120,0.28)
    raws.append(raw); metas.append(meta)
    for attempt in range(3):
        f=parse_fields(raw,["OARR","LOOP"])
        o=f.get("OARR",""); l=f.get("LOOP","")
        o_good=(len(o.split())>=10 and any(x in o.lower() for x in ["if ","unless ","would ","could ","fails","differs","mismatch","counterexample"]))
        l_good=(len(l.split())>=10 and any(x in l.lower() for x in ["test","check","inspect","compare","whether","branch","mechanism","evidence"]))
        if o_good and l_good:
            return f,{"attempts":metas},"\n--ATTEMPT--\n".join(raws)
        raw,meta=call(GEN_SERVER,system,"REPAIR DIVERGENCE ONLY. Prior output was insufficiently mechanistic. Do not change the active question. Produce a true rival prediction/counterexample and a distinct adjacent branch.\nQUESTION: "+question+"\nSOURCE EVIDENCE:\n"+evidence[:3600]+"\nPRIOR:\n"+raw[:1300],130,0.18)
        raws.append(raw); metas.append(meta)
    raise RuntimeError(f"divergence qualification failed: {raws[-1]!r}")

def reservoir(retrieved:list[Chunk],seen:set[str],all_classes:set[str])->str:
    now={c.cls for c in retrieved}; seen.update(now)
    neglected=sorted(all_classes-seen)
    if neglected:return "Neglected source class: "+neglected[0]
    missing_now=sorted(all_classes-now)
    if missing_now:return "Breadth check: not in this pass retrieval: "+missing_now[0]
    return "Bounded-complete source-class breadth check"

def synthesize(cnum:int,pnum:int,question:str,evidence:str,div:dict[str,str],resv:str,helix:dict[str,list[str]],issue:str|None=None)->tuple[dict[str,str],dict[str,Any],str]:
    p20=pnum==20
    fmt="ANSWER=<max 28 words> || EVIDENCE=<max 28 words cite S1/S2/Qn> || SURVIVE=<max 14 words> || SCAR=<max 14 words or NONE> || DEMOTE=<max 14 words or NONE> || DISPOSITION=<max 12 words> || CONFIDENCE=<0..1> || NEXT=<one complete specific question?>"
    system=(RAILS+"\nYou are R3/R4 source-grounded synthesizer. OARR/LOOP are attack inputs, not facts. Current standing evidence S1/S2 outranks stale prose. Every factual answer must cite evidence labels. Never claim absence when S1/S2 or Q sources show presence. Keep output compact and exact.")
    prompt=(f"CAMPAIGN {cnum} PASS {pnum}/20. ACTIVE QUESTION: {question}\nOARR ATTACK: {div['OARR']}\nLOOP+ BRANCH: {div['LOOP']}\nATTENTION RESERVOIR: {resv}\nCUMULATIVE HELIX: {json.dumps({k:v[-4:] for k,v in helix.items()},ensure_ascii=False)}\nSOURCE EVIDENCE:\n{evidence[:5200]}\n")
    if issue:prompt+=f"PRIOR AUDIT ISSUE TO CORRECT: {issue}\n"
    prompt+=("This is P20: DISPOSITION must include HARD_STOP_P20 and NEXT must be the successor-campaign question; no P21. " if p20 else "NEXT becomes Pass N+1 verbatim. ")+"FORMAT EXACTLY: "+fmt
    raw,meta=call(GEN_SERVER,system,prompt,180,0.12)
    f=parse_fields(raw,SYN_FIELDS)
    if f.get("NEXT"):f["NEXT"]=normalize_q(f["NEXT"])
    return f,meta,raw

def deterministic_synthesis_errors(f:dict[str,str],meta:dict[str,Any],pnum:int)->list[str]:
    errs=[]
    for n in SYN_FIELDS:
        if not f.get(n):errs.append("missing_"+n)
    if meta.get("finish_reason")!="stop":errs.append("finish_"+str(meta.get("finish_reason")))
    if f.get("EVIDENCE") and not re.search(r"\b(?:S[12]|Q[1-5])\b",f["EVIDENCE"]):errs.append("evidence_no_source_label")
    if f.get("NEXT"):
        ok,why=qvalid(f["NEXT"])
        if not ok:errs.append("next_"+why)
    if pnum==20 and f.get("DISPOSITION") and "HARD_STOP_P20" not in f["DISPOSITION"]:errs.append("p20_no_hard_stop")
    return errs

def audit_pass(question:str,evidence:str,div:dict[str,str],resv:str,f:dict[str,str])->tuple[dict[str,str],dict[str,Any],str]:
    system="You are R1 Conservative Auditor. Source evidence is authoritative for this audit; the synthesis and divergence are hypotheses. Reject any unsupported factual claim, contradiction with S1/S2/Q sources, false absence claim, authority promotion, or malformed/underspecified NEXT. OARR and LOOP need only be plausible attacks, not true. Return exactly: VERDICT=<ACCEPT or REVISE> || ISSUE=<NONE or one specific issue>."
    user=f"ACTIVE QUESTION: {question}\nSOURCE EVIDENCE:\n{evidence[:4800]}\nOARR={div['OARR']}\nLOOP={div['LOOP']}\nRESERVOIR={resv}\nSYNTHESIS={json.dumps(f,ensure_ascii=False)}"
    raw,meta=call(GEN_SERVER,system,user,85,0.01)
    a=parse_fields(raw,["VERDICT","ISSUE"])
    return a,meta,raw

def run_pass(cnum:int,pnum:int,question:str,corpus:list[Chunk],helix:dict[str,list[str]],seen_classes:set[str],all_classes:set[str])->dict[str,Any]:
    ret=retrieve(corpus,question,helix,5)
    standing=standing_evidence()
    evlines=[f"[{label}] class={cls}: {' '.join(txt.split())}" for label,cls,txt in standing]
    evlines += [f"[Q{i+1}] class={c.cls} source={c.source}: {c.text[:520]}" for i,c in enumerate(ret)]
    evidence="\n".join(evlines)
    div,divmeta,divraw=divergence(question,evidence)
    resv=reservoir(ret,seen_classes,all_classes)
    attempts=[]; issue=None
    for attempt in range(1,4):
        f,meta,raw=synthesize(cnum,pnum,question,evidence,div,resv,helix,issue)
        derr=deterministic_synthesis_errors(f,meta,pnum)
        if derr:
            attempts.append({"attempt":attempt,"synthesis":f,"raw":raw,"meta":meta,"deterministic_errors":derr,"audit":None})
            issue="Deterministic qualification errors: "+", ".join(derr)
            continue
        audit,ameta,araw=audit_pass(question,evidence,div,resv,f)
        verdict=audit.get("VERDICT","").upper()
        attempts.append({"attempt":attempt,"synthesis":f,"raw":raw,"meta":meta,"deterministic_errors":derr,"audit":audit,"audit_raw":araw,"audit_meta":ameta})
        if verdict.startswith("ACCEPT"):
            try:conf=float(re.findall(r"(?:0(?:\.\d+)?|1(?:\.0+)?)",f["CONFIDENCE"])[0])
            except Exception:conf=None
            return {**f,"confidence_numeric":conf,"campaign":cnum,"pass":pnum,"active_question":question,"OARR":div["OARR"],"LOOP":div["LOOP"],"RESERVOIR":resv,"source_refs":[c.source for c in ret],"source_classes":[c.cls for c in ret],"promotion_authority":"NONE","divergence_meta":divmeta,"divergence_raw":divraw,"qualification_attempts":attempts,"hard_stop":pnum==20}
        issue=audit.get("ISSUE") or "auditor requested revision"
    raise RuntimeError(f"pass {cnum}/{pnum} failed source-grounded qualification after 3 attempts; last issue={issue}")
def update_helix(h:dict[str,list[str]],r:dict[str,Any])->None:
    for src,dst in (("SURVIVE","survivors"),("SCAR","scars"),("DEMOTE","demotions")):
        v=str(r.get(src,"")).strip()
        if v and v.upper() not in {"NONE","N/A","NA"} and v not in h[dst]:h[dst].append(v)
def csc(cdir:Path,records:list[dict[str,Any]],helix:dict[str,list[str]])->dict[str,Any]:
    errs=[]
    if len(records)!=20:errs.append(f"pass_count={len(records)}")
    for i in range(19):
        if records[i]["NEXT"]!=records[i+1]["active_question"]:errs.append(f"chain_P{i+1:02d}_P{i+2:02d}")
    if not records[-1].get("hard_stop"):errs.append("p20_hard_stop_missing")
    if list(cdir.glob("P21*")):errs.append("p21_present")
    for r in records:
        if not r.get("OARR") or not r.get("LOOP") or not r.get("RESERVOIR"):errs.append(f"P{r['pass']:02d}_machinery_missing")
        if r.get("promotion_authority")!="NONE":errs.append(f"P{r['pass']:02d}_promotion_leak")
        ok,why=qvalid(r["NEXT"])
        if not ok:errs.append(f"P{r['pass']:02d}_NEXT_{why}")
        at=r.get("qualification_attempts",[])
        if not at or not str(at[-1].get("audit",{}).get("VERDICT","")).upper().startswith("ACCEPT"):errs.append(f"P{r['pass']:02d}_no_accepting_audit")
    ledger="\n".join(f"P{r['pass']:02d} Q={r['active_question']} | A={r['ANSWER']} | O={r['OARR']} | L={r['LOOP']} | R={r['RESERVOIR']} | D={r['DISPOSITION']} | NEXT={r['NEXT']}" for r in records)
    system="You are CSC in audit-only shadow mode with ZERO promotion authority. Audit a complete 20-pass CFE campaign for question-chain causality, source-grounding, adversarial OARR, Loop+ breadth, Helix continuity, Reservoir breadth, P20 hard stop, and no auto-promotion. Deterministic errors are authoritative. Return exactly: VERDICT=<PASS or REVIEW> || ISSUE=<NONE or brief> || SUCCESSOR_VALID=<YES or NO>."
    raw,meta=call(GEN_SERVER,system,f"DETERMINISTIC_ERRORS={errs}\nHELIX={json.dumps(helix,ensure_ascii=False)[:1800]}\nLEDGER:\n{ledger[:6800]}",100,0.01)
    a=parse_fields(raw,["VERDICT","ISSUE","SUCCESSOR_VALID"])
    modelok=a.get("VERDICT","").upper().startswith("PASS") and a.get("SUCCESSOR_VALID","").upper().startswith("YES")
    return {"authority":"AUDIT_ONLY_NONE_PROMOTION","deterministic_errors":errs,"model_audit":a,"raw":raw,"meta":meta,"verdict":"PASS" if not errs and modelok else "REVIEW","successor_question":records[-1]["NEXT"]}
def main()->int:
    RUNROOT.mkdir(parents=True,exist_ok=False)
    corpus=build_corpus(); all_classes={c.cls for c in corpus}
    seed_path=Path(os.environ.get("CFE_CAMPAIGN_SEED_PATH", str(PROJECT/"state"/"qualified_campaign_seed.json")));seed=json.loads(seed_path.read_text(encoding="utf-8"));first=normalize_q(str(seed["question"]))
    manifest={"run_id":RUN_ID,"campaigns":3,"passes_per_campaign":20,"planned_qualified_passes":60,"question_authoring":"MODEL_CHAIN_ONLY_NO_HAND_AUTHORED_PASS_QUESTIONS","seed":seed,"seed_sha256":sha256_bytes(seed_path.read_bytes()),"generator_model":str(GEN_MODEL),"generator_sha256":GEN_SHA,"divergence_model":str(GEN_MODEL),"divergence_sha256":GEN_SHA,"divergence_role":"R2 via strong 7B model; separate call; zero truth/promotion authority","runtime":str(RUNTIME),"runtime_sha256":RUNTIME_SHA,"servers":{"generator":GEN_SERVER,"divergence":GEN_SERVER,"legacy_small_divergence_server_unused":DIV_SERVER},"network_downloads":"NONE","sealed_parent":str(SEALED_PARENT),"sealed_parent_mutation_allowed":False,"corpus_chunks":len(corpus),"source_classes":sorted(all_classes),"sop_sources":[str(p) for p in SOP_SOURCES],"rails":RAILS,"qualification":"DIVERGENCE_THEN_STRONG_SYNTHESIS_THEN_STRONG_SOURCE_AUDIT_EACH_PASS_PLUS_CSC"}
    write_json(RUNROOT/"RUN_MANIFEST.json",manifest);write_json(RUNROOT/"PASS0_AUTONOMOUS_SEED.json",seed)
    campaign_seed=first;summaries=[]
    for cnum in range(1,4):
        cdir=RUNROOT/f"C{cnum:03d}";cdir.mkdir(parents=True);write_json(cdir/"CAMPAIGN_SEED.json",{"campaign":cnum,"question":campaign_seed,"source":"QUALIFIED_MODEL_PASS0" if cnum==1 else "PRIOR_P20_NEXT"})
        records=[];helix={"survivors":[],"scars":[],"demotions":[]};seen_classes=set();q=campaign_seed
        for pnum in range(1,21):
            try:r=run_pass(cnum,pnum,q,corpus,helix,seen_classes,all_classes)
            except Exception as exc:
                write_json(cdir/f"P{pnum:02d}_QUALIFICATION_FAILURE.json",{"campaign":cnum,"pass":pnum,"active_question":q,"error":repr(exc),"accepted":False});raise
            update_helix(helix,r);write_json(cdir/f"P{pnum:02d}.json",r)
            append_jsonl(cdir/"HELIX_LEDGER.jsonl",{"pass":pnum,"delta":{"survive":r['SURVIVE'],"scar":r['SCAR'],"demote":r['DEMOTE']},"cumulative":helix})
            append_jsonl(cdir/"OARR_LOOP_LEDGER.jsonl",{"pass":pnum,"oarr":r['OARR'],"loop_plus":r['LOOP']})
            append_jsonl(cdir/"RESERVOIR_LEDGER.jsonl",{"pass":pnum,"reservoir":r['RESERVOIR'],"seen_classes":sorted(seen_classes),"retrieved_classes":r['source_classes']})
            records.append(r);q=r["NEXT"]
            print(json.dumps({"event":"pass_qualified","campaign":cnum,"pass":pnum,"answer":r['ANSWER'],"disposition":r['DISPOSITION'],"next_question":q},ensure_ascii=False),flush=True)
        audit=csc(cdir,records,helix);write_json(cdir/"CSC_AUDIT.json",audit);write_json(cdir/"P20_HANDOFF.json",{"hard_stop":True,"no_p21":True,"successor_campaign_question":records[-1]['NEXT'],"csc_verdict":audit['verdict'],"promotion_authority":"NONE"})
        if audit["verdict"]!="PASS":raise RuntimeError(f"CSC review campaign {cnum}: {audit}")
        summaries.append({"campaign":cnum,"seed_question":records[0]['active_question'],"p20_disposition":records[-1]['DISPOSITION'],"successor_question":records[-1]['NEXT'],"csc_verdict":"PASS","helix":helix})
        campaign_seed=records[-1]["NEXT"]
        print(json.dumps({"event":"campaign_qualified","campaign":cnum,"successor_question":campaign_seed},ensure_ascii=False),flush=True)
    write_json(RUNROOT/"CAMPAIGN_SUMMARY.json",summaries);write_json(RUNROOT/"FINAL_HANDOFF.json",{"qualified_campaigns":3,"qualified_passes":60,"hard_stops_honored":True,"next_question":campaign_seed,"promotion_authority":"NONE","sealed_parent_mutated":False})
    print(json.dumps({"event":"run_qualified","runroot":str(RUNROOT),"next_question":campaign_seed},ensure_ascii=False),flush=True);return 0
if __name__=="__main__":raise SystemExit(main())
