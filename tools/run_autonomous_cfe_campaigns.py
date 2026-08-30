from __future__ import annotations

import hashlib
import json
import os
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
MODEL = Path(r"C:\Users\ancal\Downloads\CEG_CAPYBARA_Q3KS_HANDOFF\capybarahermes-2.5-mistral-7b.Q3_K_S.gguf")
RUNTIME = Path(r"D:\Singularity_Works\repo\tools\llama_cpp_runtime\b8831_cuda13\llama-server.exe")
SERVER = "http://127.0.0.1:8091/v1/chat/completions"
OUTROOT = PROJECT / "research" / "campaigns"
RUN_ID = time.strftime("%Y%m%d_%H%M%S")
RUNROOT = OUTROOT / f"CFE_AUTO_3x20_{RUN_ID}"

TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".py", ".ps1", ".sh", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".csv", ".log", ".bat", ".cmd", ".rst"
}
STOP = {
    "the","a","an","and","or","of","to","in","for","on","with","is","are","be","as","by","at","from",
    "this","that","it","its","we","our","you","your","do","does","did","not","no","if","then","than",
    "what","which","how","why","when","where","can","could","should","would","will","must","may","into"
}

PROCESS_FILES = [
    R31 / "03_INTERNAL_RESEARCH_GOVERNANCE.md",
    R31 / "03A_RESEARCH_MACHINERY_AND_MODES.md",
    R31 / "04_EXECUTION_AND_RELEASE_DISCIPLINE.md",
    R31 / "01_ENGINEERING_AUTHORITY_SURFACE.md",
]

@dataclass
class Chunk:
    source: str
    text: str
    terms: set[str]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def terms(text: str) -> set[str]:
    return {x for x in re.findall(r"[A-Za-z0-9_+.-]{3,}", text.lower()) if x not in STOP}


def read_text(path: Path, max_bytes: int = 1_500_000) -> str:
    try:
        data = path.read_bytes()
    except Exception:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    if b"\x00" in data[:4096]:
        # UTF-16 logs are common in this corpus.
        for enc in ("utf-16", "utf-16-le", "utf-8"):
            try:
                return data.decode(enc)
            except Exception:
                pass
        return ""
    for enc in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return data.decode(enc)
        except Exception:
            pass
    return ""


def build_corpus() -> list[Chunk]:
    paths: list[Path] = []
    for p in [PROJECT / "state" / "current.md", PROJECT / "state" / "next_steps.md"]:
        if p.exists(): paths.append(p)
    for root in [SEALED_PARENT, HOST_QUAL]:
        if root.exists():
            for p in root.rglob("*"):
                if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and ".venv" not in str(p).lower():
                    paths.append(p)
    chunks: list[Chunk] = []
    for p in paths:
        txt = read_text(p)
        if not txt.strip():
            continue
        # Paragraph/window chunks preserve source contact while staying retrieval-friendly.
        paras = re.split(r"\n\s*\n", txt)
        for i, para in enumerate(paras):
            para = para.strip()
            if len(para) < 40:
                continue
            if len(para) > 1800:
                for j in range(0, len(para), 1400):
                    sub = para[j:j+1600]
                    chunks.append(Chunk(f"{p}#p{i}.{j//1400}", sub, terms(sub)))
            else:
                chunks.append(Chunk(f"{p}#p{i}", para, terms(para)))
    return chunks


def doctrine_digest() -> str:
    lines: list[str] = []
    keys = (
        "campaign", "pass", "evidence", "helix", "oarr", "loop+", "attention reservoir", "csc",
        "promotion", "discriminator", "consequence", "unknown", "witness", "scar", "authority"
    )
    for p in PROCESS_FILES:
        txt = read_text(p, 800_000)
        for line in txt.splitlines():
            lo = line.lower().strip()
            if lo and any(k in lo for k in keys):
                lines.append(f"[{p.name}] {line.strip()}")
    # Stable bounded excerpt; full source path retained in run manifest.
    return "\n".join(lines[:70])[:5_000]


def retrieve(corpus: list[Chunk], question: str, helix_text: str, k: int = 4) -> list[Chunk]:
    q = terms(question + " " + helix_text)
    scored: list[tuple[float, Chunk]] = []
    for c in corpus:
        overlap = len(q & c.terms)
        if not overlap:
            continue
        score = overlap / (1.0 + 0.03 * max(0, len(c.terms) - 30))
        if "state\\current.md" in c.source.lower() or "state/current.md" in c.source.lower():
            score += 1.5
        if "next_steps" in c.source.lower():
            score += 1.0
        scored.append((score, c))
    scored.sort(key=lambda x: (-x[0], x[1].source))
    return [c for _, c in scored[:k]]


def chat(system: str, user: str, max_tokens: int = 180, temperature: float = 0.25, retries: int = 2) -> tuple[dict[str, Any], dict[str, Any]]:
    last = None
    for attempt in range(1, retries + 1):
        payload = {
            "model": "local",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature if attempt == 1 else 0.1,
            "max_tokens": max_tokens + (80 if attempt > 1 else 0),
            "stream": False,
            "response_format": {"type": "json_object"},
        }
        req = urllib.request.Request(SERVER, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = json.loads(r.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"].strip()
            # Strip code fences if the model ignores the JSON-only instruction.
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.I | re.S).strip()
            obj = json.loads(content)
            return obj, {"attempt": attempt, "usage": raw.get("usage"), "timings": raw.get("timings"), "model": raw.get("model"), "fingerprint": raw.get("system_fingerprint")}
        except Exception as e:
            last = repr(e)
            system = system + "\nSTRICT RETRY: output exactly one valid JSON object and nothing else."
    raise RuntimeError(f"model JSON failure after retries: {last}")


def compact_helix(pass_obj: dict[str, Any]) -> str:
    h = pass_obj.get("helix") or {}
    if not isinstance(h, dict):
        return str(h)[:900]
    return json.dumps({
        "survivors": h.get("survivors", []),
        "scars": h.get("scars", []),
        "demotions": h.get("demotions", []),
    }, ensure_ascii=False)[:1200]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def make_seed(corpus: list[Chunk], doctrine: str) -> tuple[str, dict[str, Any]]:
    state = read_text(PROJECT / "state" / "current.md", 100_000)
    nxt = read_text(PROJECT / "state" / "next_steps.md", 100_000)
    system = (
        "You are the autonomous Pass-0 campaign selector for CFE under PCMMAD/R3.1. "
        "Do not invent evidence. Do not mutate the sealed parent. Choose one high-information discriminator from the verified current frontier. "
        "The question must be answerable by evidence/reasoning/inspection before model training and must be narrow enough to drive a 20-pass adaptive campaign. "
        "Return JSON only with keys campaign_question, rationale, evidence_boundary."
    )
    user = f"CURRENT STATE:\n{state[:3000]}\n\nNEXT STEPS:\n{nxt[:3000]}\n\nPROCESS LAW EXCERPT:\n{doctrine[:1400]}"
    obj, meta = chat(system, user, max_tokens=120, temperature=0.25)
    q = str(obj.get("campaign_question", "")).strip()
    if not q:
        raise RuntimeError("seed model returned no campaign_question")
    return q, {"selection": obj, "model_meta": meta}


def run_pass(campaign: int, pnum: int, question: str, corpus: list[Chunk], doctrine: str, prev: dict[str, Any] | None) -> tuple[dict[str, Any], dict[str, Any], list[Chunk]]:
    prev_helix = compact_helix(prev) if prev else "{}"
    evidence = retrieve(corpus, question, prev_helix, k=4)
    evtxt = "\n\n".join(f"SOURCE {c.source}\n{c.text[:520]}" for c in evidence)
    slice_name = ["A", "B", "C", "D"][(pnum - 1) // 5]
    system = (
        "You are one autonomous scientific pass in CFE. R3.1 is the operating SOP; R6 is parent authority. "
        "Evidence inherits; confidence does not. A prior model statement is not evidence. UNKNOWN is required across unread/untested gaps. "
        "Keep HELIX/OARR/LOOP+/Attention-Reservoir/CSC roles distinct: this pass performs research/derivation; CSC has no promotion authority and audits later. "
        "OARR must expose at least one rival prediction/counterexample/removal. LOOP+ must widen one adjacent plausible branch before convergence. "
        "HELIX carries survivors/scars/demotions only; do not silently resurrect rejected claims. Reservoir check must name a neglected evidence class or say bounded-complete. "
        "No architecture/product promotion is allowed from campaign prose. Pass N+1 must be earned by this pass's result. "
        "Return one compact JSON object only. Required keys: answer, evidence_claims, oarr, loop_plus, helix, reservoir, disposition, confidence, next_question. "
        "helix is an object with arrays survivors, scars, demotions. confidence is 0..1. next_question is exactly one question sentence."
    )
    predecessor = "NONE" if prev is None else json.dumps({
        "answer": prev.get("answer"),
        "disposition": prev.get("disposition"),
        "confidence": prev.get("confidence"),
        "helix": prev.get("helix"),
        "next_question": prev.get("next_question"),
    }, ensure_ascii=False)[:1000]
    user = (
        f"CAMPAIGN {campaign}; SCIENTIFIC PASS {pnum}/20; OARR SLICE {slice_name}.\n"
        f"ACTIVE QUESTION (authoritative for this pass): {question}\n\n"
        f"PREDECESSOR RESULT:\n{predecessor}\n\n"
        f"RETRIEVED SOURCE EVIDENCE:\n{evtxt[:2800]}\n\n"
        f"PROCESS LAW EXCERPT:\n{doctrine[:1400]}\n\n"
        "Answer only what the admitted evidence supports. Use the result to generate the single highest-information next discriminator. "
        + ("This is P20: next_question MUST be a successor-campaign question, not P21, and the disposition must record HARD_STOP_P20."
           if pnum == 20 else "The next_question will become the exact active question for the next pass; do not prewrite later passes.")
    )
    obj, meta = chat(system, user, max_tokens=180, temperature=0.24)
    nq = str(obj.get("next_question", "")).strip()
    if not nq.endswith("?"):
        nq = nq.rstrip(". ") + "?"
        obj["next_question"] = nq
    obj["campaign"] = campaign
    obj["pass"] = pnum
    obj["active_question"] = question
    obj["oarr_slice"] = slice_name
    obj["source_refs"] = [c.source for c in evidence]
    obj["promotion_authority"] = "NONE"
    if pnum == 20:
        obj["hard_stop"] = True
        if "HARD_STOP_P20" not in str(obj.get("disposition", "")):
            obj["disposition"] = f"HARD_STOP_P20 | {obj.get('disposition','')}".strip()
    return obj, meta, evidence


def csc_audit(cdir: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    structural_errors: list[str] = []
    if len(records) != 20:
        structural_errors.append(f"pass_count={len(records)}")
    for i in range(19):
        if records[i].get("next_question") != records[i+1].get("active_question"):
            structural_errors.append(f"question_chain_break_{i+1}_{i+2}")
    if not records[-1].get("hard_stop"):
        structural_errors.append("p20_hard_stop_missing")
    if any(p.name.startswith("P21") for p in cdir.glob("P21*")):
        structural_errors.append("p21_present")
    if any(str(r.get("promotion_authority")) != "NONE" for r in records):
        structural_errors.append("promotion_authority_leak")

    compact = [{
        "pass": r.get("pass"),
        "question": r.get("active_question"),
        "disposition": r.get("disposition"),
        "confidence": r.get("confidence"),
        "next": r.get("next_question"),
        "helix": r.get("helix"),
    } for r in records]
    system = (
        "You are CSC in audit-only shadow mode. You have ZERO promotion authority. Audit a completed 20-pass CFE campaign for: "
        "question-chain causality, evidence/inference separation, UNKNOWN discipline, OARR challenge pressure, LOOP+ breadth, HELIX scar/survivor continuity, "
        "P20 hard stop, and absence of automatic product/architecture promotion. Return JSON only with keys verdict, errors, warnings, strongest_survivor, strongest_scar, successor_question_valid."
    )
    user = "STRUCTURAL CHECKS:\n" + json.dumps(structural_errors) + "\n\nPASS LEDGER:\n" + json.dumps(compact, ensure_ascii=False)[:7000]
    model_obj, meta = chat(system, user, max_tokens=160, temperature=0.1)
    return {
        "authority": "AUDIT_ONLY_NONE_PROMOTION",
        "structural_errors": structural_errors,
        "model_audit": model_obj,
        "model_meta": meta,
        "pass_count": len(records),
        "p20_successor_question": records[-1].get("next_question") if records else None,
        "verdict": "PASS" if not structural_errors and str(model_obj.get("verdict", "")).upper().startswith("PASS") else "REVIEW",
    }


def main() -> int:
    RUNROOT.mkdir(parents=True, exist_ok=False)
    corpus = build_corpus()
    doctrine = doctrine_digest()
    manifest = {
        "run_id": RUN_ID,
        "mode": "AUTONOMOUS_RESEARCH_CAMPAIGN",
        "campaign_count": 3,
        "passes_per_campaign": 20,
        "scientific_passes_planned": 60,
        "question_authoring": "MODEL_GENERATED_CHAIN_ONLY",
        "p20_rule": "P20_PRESENTS_SUCCESSOR_CAMPAIGN_QUESTION_NO_P21",
        "model_path": str(MODEL),
        "model_sha256": sha256_file(MODEL),
        "runtime_path": str(RUNTIME),
        "runtime_sha256": sha256_file(RUNTIME),
        "server": SERVER,
        "sealed_parent": str(SEALED_PARENT),
        "sealed_parent_mutation_allowed": False,
        "corpus_chunks": len(corpus),
        "doctrine_sources": [str(p) for p in PROCESS_FILES],
        "csc_authority": "AUDIT_ONLY_NONE_PROMOTION",
        "network_downloads": "FORBIDDEN/NOT_USED",
    }
    write_json(RUNROOT / "RUN_MANIFEST.json", manifest)
    (RUNROOT / "DOCTRINE_DIGEST_USED.txt").write_text(doctrine, encoding="utf-8", newline="\n")

    first_question, seed_meta = make_seed(corpus, doctrine)
    write_json(RUNROOT / "PASS0_AUTONOMOUS_SEED.json", {"campaign_question": first_question, **seed_meta})

    campaign_seed = first_question
    summary: list[dict[str, Any]] = []
    for cnum in range(1, 4):
        cdir = RUNROOT / f"C{cnum:03d}"
        cdir.mkdir(parents=True)
        write_json(cdir / "CAMPAIGN_SEED.json", {"campaign": cnum, "question": campaign_seed, "source": "PASS0" if cnum == 1 else "PRIOR_CAMPAIGN_P20"})
        records: list[dict[str, Any]] = []
        q = campaign_seed
        prev = None
        for pnum in range(1, 21):
            obj, meta, evidence = run_pass(cnum, pnum, q, corpus, doctrine, prev)
            write_json(cdir / f"P{pnum:02d}.json", {"result": obj, "model_meta": meta})
            append_jsonl(cdir / "HELIX_LEDGER.jsonl", {"pass": pnum, "helix": obj.get("helix"), "disposition": obj.get("disposition")})
            append_jsonl(cdir / "RESERVOIR_LEDGER.jsonl", {"pass": pnum, "reservoir": obj.get("reservoir"), "source_refs": obj.get("source_refs")})
            append_jsonl(cdir / "OARR_LOOP_LEDGER.jsonl", {"pass": pnum, "slice": obj.get("oarr_slice"), "oarr": obj.get("oarr"), "loop_plus": obj.get("loop_plus")})
            records.append(obj)
            prev = obj
            q = obj["next_question"]
            print(json.dumps({"event":"pass_complete","campaign":cnum,"pass":pnum,"disposition":obj.get("disposition"),"next_question":q}, ensure_ascii=False), flush=True)
        audit = csc_audit(cdir, records)
        write_json(cdir / "CSC_AUDIT.json", audit)
        write_json(cdir / "P20_HANDOFF.json", {
            "hard_stop": True,
            "no_p21": True,
            "successor_campaign_question": records[-1]["next_question"],
            "campaign_disposition": records[-1].get("disposition"),
            "csc_verdict": audit.get("verdict"),
        })
        summary.append({
            "campaign": cnum,
            "seed_question": records[0]["active_question"],
            "p20_disposition": records[-1].get("disposition"),
            "successor_question": records[-1]["next_question"],
            "csc_verdict": audit.get("verdict"),
            "csc_structural_errors": audit.get("structural_errors"),
        })
        campaign_seed = records[-1]["next_question"]
        print(json.dumps({"event":"campaign_complete","campaign":cnum,"csc":audit.get("verdict"),"successor_question":campaign_seed}, ensure_ascii=False), flush=True)

    write_json(RUNROOT / "CAMPAIGN_SUMMARY.json", summary)
    write_json(RUNROOT / "FINAL_HANDOFF.json", {
        "completed_campaigns": 3,
        "completed_scientific_passes": 60,
        "hard_stops_honored": True,
        "next_question": campaign_seed,
        "promotion_authority": "NONE",
        "note": "Campaign evidence is research pressure only. It does not mutate the sealed parent or auto-promote product/architecture claims."
    })
    print(json.dumps({"event":"run_complete","runroot":str(RUNROOT),"next_question":campaign_seed}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
