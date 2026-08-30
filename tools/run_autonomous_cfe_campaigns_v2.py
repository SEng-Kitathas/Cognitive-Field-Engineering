from __future__ import annotations

import hashlib
import json
import re
import sys
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
RUNTIME = Path(r"D:\Singularity_Works\repo\tools\llama_cpp_runtime\b8831_cuda13\llama-server.exe")
SERVER = "http://127.0.0.1:8091/v1/chat/completions"
OUTROOT = PROJECT / "research" / "campaigns"
RUN_ID = time.strftime("%Y%m%d_%H%M%S")
RUNROOT = OUTROOT / f"CFE_AUTO_3x20_V2_{RUN_ID}"

PROCESS_SOURCES = [
    R31 / "03_INTERNAL_RESEARCH_GOVERNANCE.md",
    R31 / "03A_RESEARCH_MACHINERY_AND_MODES.md",
    R31 / "04_EXECUTION_AND_RELEASE_DISCIPLINE.md",
    R31 / "01_ENGINEERING_AUTHORITY_SURFACE.md",
]

PROCESS_RAILS = """PCMMAD/R3.1 campaign rails, mandatory:
- Evidence inherits; confidence does not. Prior model prose is not evidence. UNKNOWN across untested gaps.
- Pass N+1 is earned only by Pass N and uses Pass N's NEXT question exactly. Do not prewrite future passes.
- Exactly 20 scientific passes per campaign. P20 hard-stops and emits a successor-campaign question. No P21.
- OARR: each pass must expose a rival prediction, counterexample, removal, or altered variant.
- LOOP+: each pass must widen one adjacent plausible branch before converging.
- Semantic Helix: explicitly carry survivors, scars, and demotions; no silent resurrection.
- Attention Reservoir: each pass checks for a neglected evidence class/branch or says bounded-complete.
- CSC is audit-only, has ZERO promotion authority, and runs after the campaign.
- Research success never auto-promotes product/architecture. The sealed v0.9 parent is immutable.
- Tool/action/test output is not automatically qualified consequence. Source evidence and inference stay separate.
"""

TEXT_SUFFIXES = {".md",".txt",".json",".jsonl",".py",".ps1",".sh",".yaml",".yml",".toml",".ini",".cfg",".csv",".log",".bat",".cmd",".rst"}
STOP = {"the","a","an","and","or","of","to","in","for","on","with","is","are","be","as","by","at","from","this","that","it","its","we","our","you","your","do","does","did","not","no","if","then","than","what","which","how","why","when","where","can","could","should","would","will","must","may","into"}

@dataclass
class Chunk:
    source: str
    text: str
    terms: set[str]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def termset(text: str) -> set[str]:
    return {x for x in re.findall(r"[A-Za-z0-9_+.-]{3,}", text.lower()) if x not in STOP}


def read_text(path: Path, limit: int = 1_000_000) -> str:
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
    for p in [PROJECT/"state"/"current.md", PROJECT/"state"/"next_steps.md"]:
        if p.exists(): paths.append(p)
    for root in [SEALED_PARENT, HOST_QUAL]:
        if not root.exists(): continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and ".venv" not in str(p).lower():
                paths.append(p)
    out: list[Chunk] = []
    for p in paths:
        txt = read_text(p)
        if not txt.strip(): continue
        for i, para in enumerate(re.split(r"\n\s*\n", txt)):
            para = " ".join(para.strip().split())
            if len(para) < 45: continue
            for j in range(0, len(para), 650):
                sub = para[j:j+760]
                if len(sub) >= 45:
                    out.append(Chunk(f"{p}#p{i}.{j//650}", sub, termset(sub)))
    return out


def retrieve(corpus: list[Chunk], question: str, carry: str, k: int = 4) -> list[Chunk]:
    q = termset(question + " " + carry)
    scored: list[tuple[float, Chunk]] = []
    for c in corpus:
        ov = len(q & c.terms)
        if not ov: continue
        score = ov / (1.0 + 0.02 * max(0, len(c.terms)-30))
        s = c.source.lower()
        if "state\\current.md" in s or "state/current.md" in s: score += 1.5
        if "next_steps" in s: score += 1.0
        scored.append((score,c))
    scored.sort(key=lambda x:(-x[0],x[1].source))
    return [c for _,c in scored[:k]]


def ask(user: str, max_tokens: int = 190, temperature: float = 0.22) -> tuple[str, dict[str, Any]]:
    payload = {
        "model":"local",
        "messages":[
            {"role":"system","content":PROCESS_RAILS + "\nBe terse. Follow the requested labeled format exactly. Never place '||' inside a field value."},
            {"role":"user","content":user},
        ],
        "temperature":temperature,
        "max_tokens":max_tokens,
        "stream":False,
    }
    req = urllib.request.Request(SERVER,data=json.dumps(payload).encode("utf-8"),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=120) as r:
        raw = json.loads(r.read().decode("utf-8"))
    content = (raw["choices"][0]["message"].get("content") or "").strip()
    return content, {"usage":raw.get("usage"),"timings":raw.get("timings"),"model":raw.get("model"),"fingerprint":raw.get("system_fingerprint"),"finish_reason":raw["choices"][0].get("finish_reason")}


def parse_fields(text: str, names: list[str]) -> dict[str,str]:
    # Normalize multiline labels into the same parser. Values may span until the next known label.
    clean = text.replace("\r"," ").replace("\n"," || ")
    positions: list[tuple[int,str,int]] = []
    for name in names:
        m = re.search(rf"(?i)(?:^|\|\|)\s*{re.escape(name)}\s*=\s*", clean)
        if not m:
            m = re.search(rf"(?i)(?:^|\|\|)\s*{re.escape(name)}\s*:\s*", clean)
        if m: positions.append((m.start(),name,m.end()))
    positions.sort()
    out: dict[str,str] = {}
    for idx,(start,name,val_start) in enumerate(positions):
        end = positions[idx+1][0] if idx+1 < len(positions) else len(clean)
        val = clean[val_start:end].strip(" |\t\n\r\"'")
        out[name] = val
    return out


def required_parse(text: str, names: list[str], repair_prompt: str, max_tokens: int) -> tuple[dict[str,str], list[str]]:
    raws=[text]
    parsed=parse_fields(text,names)
    missing=[n for n in names if not parsed.get(n)]
    if not missing:
        return parsed, raws
    repair, _ = ask(repair_prompt + "\nRAW OUTPUT TO REFORMAT:\n" + text[:2500], max_tokens=max_tokens, temperature=0.05)
    raws.append(repair)
    parsed=parse_fields(repair,names)
    missing=[n for n in names if not parsed.get(n)]
    if missing:
        raise RuntimeError(f"required labeled fields missing after repair: {missing}; raw={raws!r}")
    return parsed, raws


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(obj,ensure_ascii=False)+"\n")


def seed_question(corpus: list[Chunk]) -> tuple[str,dict[str,Any]]:
    state=read_text(PROJECT/"state"/"current.md",80_000)
    nxt=read_text(PROJECT/"state"/"next_steps.md",80_000)
    prompt=(
        "AUTONOMOUS PASS-0 SELECTION. Discriminator A / Windows newline diagnosis is CLOSED and MUST NOT be selected or re-proved. "
        "Choose the highest-information unresolved CFE discriminator beyond that closed result, grounded only in CURRENT STATE and NEXT STEPS. "
        "It must be narrow enough to drive an adaptive 20-pass pre-live campaign and must not require model download/training yet. "
        "FORMAT EXACTLY: QUESTION=<one question?> || RATIONALE=<brief> || BOUNDARY=<what evidence may answer it>\n\n"
        f"CURRENT STATE:\n{state[:2600]}\n\nNEXT STEPS:\n{nxt[:2600]}"
    )
    raw,meta=ask(prompt,max_tokens=150,temperature=0.22)
    fields,raws=required_parse(raw,["QUESTION","RATIONALE","BOUNDARY"],"REFORMAT ONLY. FORMAT EXACTLY: QUESTION=<one question?> || RATIONALE=<brief> || BOUNDARY=<brief>",170)
    q=fields["QUESTION"].strip()
    if not q.endswith("?"): q=q.rstrip(". ")+"?"
    return q,{"fields":fields,"raw_outputs":raws,"model_meta":meta}

PASS_FIELDS=["ANSWER","EVIDENCE","OARR","LOOP","SURVIVE","SCAR","DEMOTE","RESERVOIR","DISPOSITION","CONFIDENCE","NEXT"]


def run_pass(cnum:int,pnum:int,question:str,corpus:list[Chunk],prev:dict[str,Any]|None)->tuple[dict[str,Any],dict[str,Any]]:
    carry="" if not prev else " ".join(str(prev.get(k,"")) for k in ["SURVIVE","SCAR","DEMOTE","DISPOSITION"])
    ev=retrieve(corpus,question,carry,k=4)
    evtxt="\n".join(f"[{i+1}] {c.source}: {c.text[:430]}" for i,c in enumerate(ev))
    pred="NONE" if prev is None else f"ANSWER={prev.get('ANSWER','')} | DISPOSITION={prev.get('DISPOSITION','')} | SURVIVE={prev.get('SURVIVE','')} | SCAR={prev.get('SCAR','')} | DEMOTE={prev.get('DEMOTE','')}"
    slice_name=["A","B","C","D"][(pnum-1)//5]
    p20 = pnum==20
    format_line="ANSWER=<brief supported answer> || EVIDENCE=<source numbers and evidence/inference boundary> || OARR=<rival/counterexample/removal> || LOOP=<adjacent branch widened> || SURVIVE=<helix survivor> || SCAR=<helix scar or NONE> || DEMOTE=<helix demotion or NONE> || RESERVOIR=<neglected evidence class or bounded-complete> || DISPOSITION=<provisional status> || CONFIDENCE=<0..1> || NEXT=<one next question?>"
    prompt=(
        f"CFE AUTONOMOUS CAMPAIGN {cnum}, PASS {pnum}/20, OARR SLICE {slice_name}.\n"
        f"ACTIVE QUESTION: {question}\n"
        f"PREDECESSOR CARRY: {pred[:850]}\n"
        f"RETRIEVED PROJECT EVIDENCE:\n{evtxt[:2300]}\n\n"
        "Answer only from admitted evidence; label inference as inference. The NEXT field is the single highest-information discriminator earned by this result. "
        + ("This is P20: DISPOSITION must include HARD_STOP_P20 and NEXT must be a successor-CAMPAIGN question. There is no P21. " if p20 else "NEXT will become Pass N+1 verbatim. ")
        + "FORMAT EXACTLY ONE LABELED RECORD: " + format_line
    )
    raw,meta=ask(prompt,max_tokens=205,temperature=0.24)
    repair="REFORMAT ONLY; do not add new reasoning. FORMAT EXACTLY: "+format_line
    f,raws=required_parse(raw,PASS_FIELDS,repair,225)
    nextq=f["NEXT"].strip()
    if not nextq.endswith("?"): nextq=nextq.rstrip(". ")+"?"
    f["NEXT"]=nextq
    try: conf=float(re.findall(r"(?:0(?:\.\d+)?|1(?:\.0+)?)",f["CONFIDENCE"])[0])
    except Exception: conf=None
    obj={**f,"confidence_numeric":conf,"campaign":cnum,"pass":pnum,"active_question":question,"oarr_slice":slice_name,"source_refs":[c.source for c in ev],"promotion_authority":"NONE","raw_outputs":raws}
    if p20:
        obj["hard_stop"]=True
        if "HARD_STOP_P20" not in obj["DISPOSITION"]:
            obj["DISPOSITION"]="HARD_STOP_P20 | "+obj["DISPOSITION"]
    return obj,meta


def csc_audit(cdir:Path,records:list[dict[str,Any]])->dict[str,Any]:
    errs=[]
    if len(records)!=20: errs.append(f"pass_count={len(records)}")
    for i in range(19):
        if records[i]["NEXT"]!=records[i+1]["active_question"]: errs.append(f"question_chain_break_{i+1}_{i+2}")
    if not records[-1].get("hard_stop"): errs.append("p20_hard_stop_missing")
    if any(cdir.glob("P21*")): errs.append("p21_present")
    if any(r.get("promotion_authority")!="NONE" for r in records): errs.append("promotion_authority_leak")
    ledger="\n".join(f"P{r['pass']:02d} Q={r['active_question']} | D={r['DISPOSITION']} | NEXT={r['NEXT']} | S={r['SURVIVE']} | SCAR={r['SCAR']}" for r in records)
    prompt=(
        "CSC SHADOW AUDIT ONLY. ZERO promotion authority. Audit the completed 20-pass chain for causality, evidence/inference separation, UNKNOWN discipline, OARR, LOOP+, Helix carry, Reservoir breadth, P20 hard stop, and no auto-promotion. "
        "FORMAT EXACTLY: VERDICT=<PASS or REVIEW> || ERRORS=<brief or NONE> || WARNINGS=<brief or NONE> || SURVIVOR=<strongest> || SCAR=<strongest> || SUCCESSOR_VALID=<YES or NO>\n"
        f"DETERMINISTIC STRUCTURAL ERRORS: {errs}\nPASS LEDGER:\n{ledger[:6500]}"
    )
    raw,meta=ask(prompt,max_tokens=165,temperature=0.08)
    fields,raws=required_parse(raw,["VERDICT","ERRORS","WARNINGS","SURVIVOR","SCAR","SUCCESSOR_VALID"],"REFORMAT ONLY. FORMAT EXACTLY: VERDICT=<PASS or REVIEW> || ERRORS=<brief or NONE> || WARNINGS=<brief or NONE> || SURVIVOR=<brief> || SCAR=<brief> || SUCCESSOR_VALID=<YES or NO>",185)
    return {"authority":"AUDIT_ONLY_NONE_PROMOTION","structural_errors":errs,"model_fields":fields,"raw_outputs":raws,"model_meta":meta,"pass_count":len(records),"p20_successor_question":records[-1]["NEXT"],"verdict":"PASS" if not errs and fields["VERDICT"].upper().startswith("PASS") else "REVIEW"}


def main()->int:
    RUNROOT.mkdir(parents=True,exist_ok=False)
    corpus=build_corpus()
    manifest={
        "run_id":RUN_ID,"campaigns":3,"passes_per_campaign":20,"planned_scientific_passes":60,
        "question_authoring":"AUTONOMOUS_CHAIN_ONLY","p20_rule":"P20_EMITS_SUCCESSOR_CAMPAIGN_QUESTION_NO_P21",
        "model_path":str(MODEL),"model_sha256":"b77b39f196ddd460b622fe101a500723887c470db50aebd217fec7370e6724c3","model_sha256_source":"direct SHA-256 2026-08-29 before campaign","runtime_path":str(RUNTIME),"runtime_sha256":"01ddbfd39cb4f1aaea98dab3108179a78d5caa2105fbc971b871ca158e858c74","runtime_sha256_source":"verified prior same-path run manifest 20260829_162825",
        "server":SERVER,"sealed_parent":str(SEALED_PARENT),"sealed_parent_mutation_allowed":False,"corpus_chunks":len(corpus),
        "sop_sources":[str(p) for p in PROCESS_SOURCES],"process_rails":PROCESS_RAILS,"csc_authority":"AUDIT_ONLY_NONE_PROMOTION","network_downloads":"NONE"
    }
    write_json(RUNROOT/"RUN_MANIFEST.json",manifest)
    qualified_seed_path=PROJECT/"state"/"qualified_campaign_seed.json"
    if qualified_seed_path.exists():
        qualified=json.loads(qualified_seed_path.read_text(encoding="utf-8"))
        first=str(qualified["question"]).strip()
        if not first.endswith("?"):
            first=first.rstrip(". ")+"?"
        seedmeta={"source":"QUALIFIED_MODEL_GENERATED_PASS0_SEED","qualified_seed":qualified}
    else:
        first,seedmeta=seed_question(corpus)
        seedmeta={"source":"FRESH_MODEL_GENERATED_PASS0_SEED",**seedmeta}
    write_json(RUNROOT/"PASS0_AUTONOMOUS_SEED.json",{"question":first,**seedmeta})
    campaign_seed=first
    summaries=[]
    for cnum in range(1,4):
        cdir=RUNROOT/f"C{cnum:03d}"; cdir.mkdir(parents=True)
        write_json(cdir/"CAMPAIGN_SEED.json",{"campaign":cnum,"question":campaign_seed,"source":"PASS0" if cnum==1 else "PRIOR_P20_NEXT"})
        records=[]; q=campaign_seed; prev=None
        for pnum in range(1,21):
            obj,meta=run_pass(cnum,pnum,q,corpus,prev)
            write_json(cdir/f"P{pnum:02d}.json",{"result":obj,"model_meta":meta})
            append_jsonl(cdir/"HELIX_LEDGER.jsonl",{"pass":pnum,"survive":obj["SURVIVE"],"scar":obj["SCAR"],"demote":obj["DEMOTE"],"disposition":obj["DISPOSITION"]})
            append_jsonl(cdir/"OARR_LOOP_LEDGER.jsonl",{"pass":pnum,"slice":obj["oarr_slice"],"oarr":obj["OARR"],"loop_plus":obj["LOOP"]})
            append_jsonl(cdir/"RESERVOIR_LEDGER.jsonl",{"pass":pnum,"reservoir":obj["RESERVOIR"],"sources":obj["source_refs"]})
            records.append(obj); prev=obj; q=obj["NEXT"]
            print(json.dumps({"event":"pass_complete","campaign":cnum,"pass":pnum,"disposition":obj["DISPOSITION"],"next_question":q},ensure_ascii=False),flush=True)
        audit=csc_audit(cdir,records); write_json(cdir/"CSC_AUDIT.json",audit)
        write_json(cdir/"P20_HANDOFF.json",{"hard_stop":True,"no_p21":True,"successor_campaign_question":records[-1]["NEXT"],"csc_verdict":audit["verdict"],"campaign_disposition":records[-1]["DISPOSITION"]})
        summaries.append({"campaign":cnum,"seed_question":records[0]["active_question"],"p20_disposition":records[-1]["DISPOSITION"],"successor_question":records[-1]["NEXT"],"csc_verdict":audit["verdict"],"csc_structural_errors":audit["structural_errors"]})
        campaign_seed=records[-1]["NEXT"]
        print(json.dumps({"event":"campaign_complete","campaign":cnum,"csc":audit["verdict"],"successor_question":campaign_seed},ensure_ascii=False),flush=True)
    write_json(RUNROOT/"CAMPAIGN_SUMMARY.json",summaries)
    write_json(RUNROOT/"FINAL_HANDOFF.json",{"completed_campaigns":3,"completed_scientific_passes":60,"hard_stops_honored":True,"next_question":campaign_seed,"promotion_authority":"NONE","sealed_parent_mutated":False})
    print(json.dumps({"event":"run_complete","runroot":str(RUNROOT),"next_question":campaign_seed},ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
