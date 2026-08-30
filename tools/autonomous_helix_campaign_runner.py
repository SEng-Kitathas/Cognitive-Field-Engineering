from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

PROJECT_ROOT = Path.cwd()
LIVE_CFE = Path(r"C:\Users\ancal\ProtoAGI\CFE")
PARENT = LIVE_CFE / "sealed_parents" / "v09" / "CFE_RND_V0_9_2026-08-25"
HOST = LIVE_CFE / "host_qualification"
MODEL_PATH = Path(r"D:\Project_Linked_Tensors\monster-standard-inference-revival-2026-04-06\incoming\qwen3_4b_thinking_3shard")
PCMMAD = Path(r"E:\new pc\AI_Pushes_Sandbox\projects\PCMMAD\HOSTILE_OS")
SOP_ROOT = PCMMAD / "authority" / "RAHL_ENGINEERING_R3_1_EXACT_EXTRACTED" / "RAHL_ENGINEERING_IN_HOUSE_SOP_SPLIT_CANDIDATE_R3_1_2026-08-29"
SOP_SOURCES = [
    SOP_ROOT / "03_INTERNAL_RESEARCH_GOVERNANCE.md",
    SOP_ROOT / "03A_RESEARCH_MACHINERY_AND_MODES.md",
    SOP_ROOT / "04_EXECUTION_AND_RELEASE_DISCIPLINE.md",
    SOP_ROOT / "05_ACTIVE_SCAR_INDEX.md",
    SOP_ROOT / "07_COLD_START_USE_ORDER.md",
    SOP_ROOT / "ancestry" / "V7" / "02_ENGINEERING_RESEARCH_CONSTITUTION.md",
    PCMMAD / "research" / "campaigns" / "C001" / "C001_HSP_EXECUTION_MAP.md",
]

RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
OUT = PROJECT_ROOT / "campaigns" / f"AUTONOMOUS_HELIX_{RUN_ID}"
OUT.mkdir(parents=True, exist_ok=False)

TEXT_SUFFIXES = {".py", ".md", ".json", ".jsonl", ".txt", ".ps1", ".sh", ".csv", ".toml", ".yaml", ".yml"}
STOP = {
    "the","and","for","with","that","this","from","into","what","when","where","which","while","then","than","have","has","had","are","was","were","will","would","could","should","must","can","may","not","but","about","after","before","current","next","question","pass","cfe","v1","v0"
}
MAIN_PREFIXES = [
    "OBSERVED:", "LOOP_PLUS:", "OARR:", "PDVER:", "HELIX_SURVIVOR:",
    "HELIX_SCAR:", "RESERVOIR:", "SOP_CHECK:", "DECISION:", "NEXT_QUESTION:"
]

PROCESS_CONTRACT = """
PCMMAD/R3.1 CFE campaign contract:
- All inbound material is controlled evidence; source prestige is not truth.
- Evidence, inference, provisional claim, and UNKNOWN remain distinct. Do not promote by tone.
- Research output never mutates or promotes CFE mainline automatically.
- Exactly 20 scientific passes per campaign. Hard stop at P20; no P21.
- Pass N+1 question MUST be the NEXT_QUESTION authored by Pass N. No prewritten sequence.
- Loop+ is problem-space expansion: widen alternatives, hidden equivalences, wrong paths, counterexamples.
- OARR is hostile bounded discriminator work: state rival predictions and seek falsifiers rather than consensus.
- PDVER keeps prediction/derivation/embodiment/verification distinct; observed consequence outranks plausible narration.
- Semantic Helix carries survivors/scars/unknowns forward; evidence inherits, confidence does not.
- Attention Reservoir checks neglected alternatives and prevents local-optimum lock-in.
- CSC is audit-only. It has no selection, veto, runtime, or promotion authority.
- SOP execution scars apply: command/trace/test output != qualified consequence; ambiguous execution remains UNKNOWN; source/runtime splits and silent promotion are forbidden.
- Historical parent state is evidence, but PROJECT CURRENT STATE is the currentness authority for this run.
- Do not resurrect rejected mechanisms by renaming. Re-earning requires a discriminator addressing the old failure.
- Keep every field terse. The final NEXT_QUESTION must be one complete question that is answerable by the next pass.
""".strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    return text if limit is None else text[:limit]


def source_fingerprint(paths: Iterable[Path]) -> list[dict]:
    out = []
    for p in paths:
        if not p.exists() or not p.is_file():
            out.append({"path": str(p), "exists": False})
            continue
        b = p.read_bytes()
        out.append({"path": str(p), "exists": True, "bytes": len(b), "sha256": sha256_bytes(b)})
    return out


def build_file_index() -> list[Path]:
    roots = [PARENT, HOST, PROJECT_ROOT / "state"]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            try:
                if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and p.stat().st_size <= 2_000_000:
                    files.append(p)
            except OSError:
                pass
    return sorted(set(files), key=lambda p: str(p).lower())


def terms(query: str) -> list[str]:
    return [t for t in re.findall(r"[A-Za-z0-9_\-]{3,}", query.lower()) if t not in STOP]


def extract_window(text: str, qs: list[str], max_chars: int = 4200) -> str:
    if len(text) <= max_chars:
        return text
    lower = text.lower()
    locs = [lower.find(q) for q in qs if lower.find(q) >= 0]
    if not locs:
        return text[:max_chars]
    center = min(locs)
    start = max(0, center - max_chars // 3)
    return text[start:start + max_chars]


def retrieve(index: list[Path], query: str, k: int = 4) -> list[dict]:
    qs = terms(query)
    scored = []
    for p in index:
        text = read_text(p, 240_000)
        if not text:
            continue
        low = text.lower()
        pstr = str(p).lower()
        score = 0
        for q in qs:
            score += min(low.count(q), 8)
            if q in pstr:
                score += 8
        if score:
            scored.append((score, p, text))
    scored.sort(key=lambda x: (-x[0], str(x[1]).lower()))
    packet = []
    for score, p, text in scored[:k]:
        raw = p.read_bytes()
        packet.append({
            "score": score,
            "path": str(p),
            "sha256": sha256_bytes(raw),
            "excerpt": extract_window(text, qs),
        })
    return packet


def render_evidence(packet: list[dict]) -> str:
    if not packet:
        return "NO_RETRIEVED_FILE_EVIDENCE"
    chunks = []
    for x in packet:
        chunks.append(f"SOURCE {x['path']}\nSHA256 {x['sha256']}\n{x['excerpt']}")
    return "\n\n---\n\n".join(chunks)


def load_model():
    q = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    tok = AutoTokenizer.from_pretrained(str(MODEL_PATH), local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True,
        quantization_config=q,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tok, model


def direct_generate(tok, model, system: str, user: str, first_prefix: str, max_new_tokens: int) -> tuple[str, float]:
    # This checkpoint's packaged template forces a thinking preamble. We do not mutate it;
    # instead prefill an already-closed empty think block and the first schema key.
    prompt = (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{user}<|im_end|>\n"
        f"<|im_start|>assistant\n<think>\n</think>\n\n{first_prefix}"
    )
    inp = tok(prompt, return_tensors="pt").to(model.device)
    t0 = time.time()
    with torch.inference_mode():
        out = model.generate(
            **inp,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id,
            eos_token_id=tok.convert_tokens_to_ids("<|im_end|>"),
            use_cache=True,
        )
    sec = time.time() - t0
    tail = tok.decode(out[0][inp["input_ids"].shape[1]:], skip_special_tokens=True)
    return first_prefix + tail, sec


def parse_main(text: str) -> dict | None:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Find the last complete ordered schema in case the model emitted noise.
    for start in range(len(lines) - 1, -1, -1):
        if not lines[start].startswith(MAIN_PREFIXES[0]):
            continue
        cand = lines[start:start + len(MAIN_PREFIXES)]
        if len(cand) != len(MAIN_PREFIXES):
            continue
        if all(cand[i].startswith(MAIN_PREFIXES[i]) and cand[i][len(MAIN_PREFIXES[i]):].strip() for i in range(len(MAIN_PREFIXES))):
            return {MAIN_PREFIXES[i][:-1]: cand[i][len(MAIN_PREFIXES[i]):].strip() for i in range(len(MAIN_PREFIXES))}
    return None


def generate_seed(tok, model, current_state: str, next_steps: str) -> tuple[str, dict]:
    system = PROCESS_CONTRACT + "\n\nChoose the single highest-information lawful first campaign question. Do not answer it."
    user = f"PROJECT CURRENT STATE:\n{current_state}\n\nPROJECT NEXT STEPS:\n{next_steps}\n\nReturn one complete question only after SEED_QUESTION:."
    raw, sec = direct_generate(tok, model, system, user, "SEED_QUESTION:", 80)
    m = re.search(r"SEED_QUESTION:\s*(.+?)(?:\r?\n|$)", raw)
    if not m or not m.group(1).strip():
        # Model-authored repair only; no human fallback question.
        raw2, sec2 = direct_generate(tok, model, system, user + "\nPrevious format failed. Emit a single complete question now.", "SEED_QUESTION:", 96)
        raw += "\n---REPAIR---\n" + raw2
        sec += sec2
        m = re.search(r"SEED_QUESTION:\s*(.+?)(?:\r?\n|$)", raw2)
    if not m:
        raise RuntimeError("Model failed to author a seed question; campaign not started.")
    q = m.group(1).strip()
    return q, {"raw": raw, "seconds": sec}


def generate_pass(tok, model, campaign: int, pnum: int, question: str, current_state: str, helix_tail: str, evidence: str) -> tuple[dict, str, float, int]:
    system = PROCESS_CONTRACT + "\n\n" + (
        "Output exactly ten nonempty lines, in this exact order, using these prefixes: "
        + ", ".join(MAIN_PREFIXES)
        + ". Each field <= 12 words except NEXT_QUESTION <= 18 words. No prose outside the schema. "
        "OBSERVED must be grounded in supplied evidence or say UNKNOWN. DECISION is research posture only, never promotion."
    )
    user = (
        f"CAMPAIGN: {campaign}\nPASS: {pnum}/20\n"
        f"CURRENT QUESTION (authored by prior pass or seed): {question}\n\n"
        f"PROJECT CURRENT STATE:\n{current_state[:9000]}\n\n"
        f"HELIX CARRY FROM PRIOR PASSES:\n{helix_tail or 'NONE'}\n\n"
        f"RETRIEVED LOCAL EVIDENCE:\n{evidence[:18000]}"
    )
    raw_total = []
    total_sec = 0.0
    for attempt in range(1, 4):
        suffix = "" if attempt == 1 else f"\n\nFORMAT REPAIR ATTEMPT {attempt}: prior output was invalid. Re-author this pass from the same evidence; do not copy malformed prose."
        raw, sec = direct_generate(tok, model, system, user + suffix, "OBSERVED:", 190)
        total_sec += sec
        raw_total.append(raw)
        parsed = parse_main(raw)
        if parsed and parsed["NEXT_QUESTION"].rstrip().endswith("?"):
            return parsed, "\n\n---ATTEMPT---\n\n".join(raw_total), total_sec, attempt
    raise RuntimeError(f"Campaign {campaign} pass {pnum}: model failed schema after 3 attempts")


def generate_csc_audit(tok, model, pass_result: dict, question: str) -> tuple[str, str, float]:
    system = PROCESS_CONTRACT + "\n\nYou are CSC SHADOW AUDIT ONLY. No selection, veto, next-question authorship, or promotion authority."
    user = (
        f"QUESTION: {question}\n"
        f"PASS RESULT:\n{json.dumps(pass_result, ensure_ascii=False, indent=2)}\n\n"
        "Audit only for missing obligation, authority inversion, stale-currentness use, or evidence/inference collapse. "
        "Return CSC_AUDIT: PASS - reason or CSC_AUDIT: FLAG - reason."
    )
    raw, sec = direct_generate(tok, model, system, user, "CSC_AUDIT:", 64)
    line = next((ln.strip() for ln in raw.splitlines() if ln.strip().startswith("CSC_AUDIT:")), "")
    if not line:
        raw2, sec2 = direct_generate(tok, model, system, user + "\nFormat repair: one CSC_AUDIT line only.", "CSC_AUDIT:", 64)
        raw += "\n---REPAIR---\n" + raw2
        sec += sec2
        line = next((ln.strip() for ln in raw2.splitlines() if ln.strip().startswith("CSC_AUDIT:")), "CSC_AUDIT: UNKNOWN - malformed audit")
    return line[len("CSC_AUDIT:"):].strip(), raw, sec


def main() -> int:
    current_path = PROJECT_ROOT / "state" / "current.md"
    next_path = PROJECT_ROOT / "state" / "next_steps.md"
    current_state = read_text(current_path)
    next_steps = read_text(next_path)
    if not current_state or not next_steps:
        raise RuntimeError("Missing CFE current/next state; refusing autonomous campaign.")
    if not PARENT.exists():
        raise RuntimeError(f"Sealed parent missing: {PARENT}")
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Local model missing: {MODEL_PATH}")

    manifest = {
        "run_id": RUN_ID,
        "started": datetime.now().isoformat(),
        "project_root": str(PROJECT_ROOT),
        "live_cfe": str(LIVE_CFE),
        "sealed_parent": str(PARENT),
        "model_path": str(MODEL_PATH),
        "model_files": source_fingerprint(sorted(MODEL_PATH.glob("model-*.safetensors"))),
        "state_files": source_fingerprint([current_path, next_path]),
        "sop_sources": source_fingerprint(SOP_SOURCES),
        "campaign_count": 3,
        "passes_per_campaign": 20,
        "mainline_mutation_authority": "NONE",
        "csc_authority": "AUDIT_ONLY",
        "question_authorship": "MODEL_ONLY_SEED_THEN_PREVIOUS_PASS_NEXT_QUESTION",
    }
    (OUT / "RUN_MANIFEST.initial.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    (OUT / "PROCESS_CONTRACT.md").write_text(PROCESS_CONTRACT + "\n\nSOP source bindings:\n" + "\n".join(f"- {p}" for p in SOP_SOURCES) + "\n", encoding="utf-8", newline="\n")

    index = build_file_index()
    (OUT / "EVIDENCE_INDEX.txt").write_text("\n".join(str(p) for p in index) + "\n", encoding="utf-8", newline="\n")

    print(f"RUN {RUN_ID} index_files={len(index)} out={OUT}", flush=True)
    tok, model = load_model()
    print(f"MODEL_LOADED device={model.device}", flush=True)

    seed, seed_meta = generate_seed(tok, model, current_state, next_steps)
    (OUT / "SEED_GENERATION.md").write_text(
        f"# Model-authored seed\n\nSeed question: {seed}\n\nSeconds: {seed_meta['seconds']:.3f}\n\n```text\n{seed_meta['raw']}\n```\n",
        encoding="utf-8", newline="\n"
    )
    print(f"SEED {seed}", flush=True)

    question = seed
    chain = []
    global_helix: list[str] = []
    total_passes = 0

    for campaign in range(1, 4):
        cdir = OUT / f"C{campaign:03d}"
        cdir.mkdir()
        campaign_seed = question
        (cdir / "SEED_QUESTION.txt").write_text(campaign_seed + "\n", encoding="utf-8", newline="\n")
        print(f"CAMPAIGN {campaign} START seed={campaign_seed}", flush=True)
        campaign_rows = []

        for pnum in range(1, 21):
            pass_question = question
            helix_tail = "\n".join(global_helix[-12:])
            packet = retrieve(index, pass_question + " " + helix_tail, k=4)
            evidence = render_evidence(packet)
            parsed, raw, main_sec, attempts = generate_pass(
                tok, model, campaign, pnum, pass_question, current_state, helix_tail, evidence
            )
            csc, csc_raw, csc_sec = generate_csc_audit(tok, model, parsed, pass_question)
            next_question = parsed["NEXT_QUESTION"].strip()

            global_helix.append(f"C{campaign:03d}/P{pnum:02d} SURVIVOR: {parsed['HELIX_SURVIVOR']}")
            global_helix.append(f"C{campaign:03d}/P{pnum:02d} SCAR: {parsed['HELIX_SCAR']}")

            pass_doc = [
                f"# C{campaign:03d} / P{pnum:02d}", "",
                f"Question: {pass_question}", "",
                f"Main generation seconds: {main_sec:.3f}",
                f"CSC audit seconds: {csc_sec:.3f}",
                f"Schema attempts: {attempts}", "",
                "## Evidence bindings",
            ]
            for x in packet:
                pass_doc += [f"- `{x['path']}`", f"  - sha256: `{x['sha256']}`", f"  - retrieval_score: {x['score']}"]
            pass_doc += ["", "## Pass result"]
            for pref in MAIN_PREFIXES:
                key = pref[:-1]
                pass_doc.append(f"{pref} {parsed[key]}")
            pass_doc += ["", f"CSC_AUDIT: {csc}", "", "## Raw model emission", "```text", raw, "```", "", "## Raw CSC emission", "```text", csc_raw, "```", ""]
            ppath = cdir / f"P{pnum:02d}.md"
            ppath.write_text("\n".join(pass_doc), encoding="utf-8", newline="\n")

            row = {
                "campaign": campaign,
                "pass": pnum,
                "question": pass_question,
                "next_question": next_question,
                "main_seconds": main_sec,
                "csc_seconds": csc_sec,
                "attempts": attempts,
                "csc_audit": csc,
                "evidence": [{k: x[k] for k in ("path", "sha256", "score")} for x in packet],
                "pass_sha256": sha256_bytes(ppath.read_bytes()),
            }
            campaign_rows.append(row)
            total_passes += 1
            print(f"C{campaign:03d} P{pnum:02d} next={next_question}", flush=True)

            # Critical law: exact model-authored handoff; no human or runner-authored question.
            question = next_question

        # Hard stop. No P21 generation is reachable in this loop.
        p20_next = question
        (cdir / "P20_NEXT_QUESTION.txt").write_text(p20_next + "\n", encoding="utf-8", newline="\n")
        (cdir / "CAMPAIGN_LEDGER.json").write_text(json.dumps(campaign_rows, indent=2), encoding="utf-8", newline="\n")
        summary = {
            "campaign": campaign,
            "seed_question": campaign_seed,
            "passes_completed": len(campaign_rows),
            "hard_stop": "P20",
            "p21_generated": False,
            "p20_next_question": p20_next,
            "csc_flag_count": sum(1 for r in campaign_rows if r["csc_audit"].upper().startswith("FLAG")),
            "repair_pass_count": sum(1 for r in campaign_rows if r["attempts"] > 1),
        }
        (cdir / "SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8", newline="\n")
        chain.append(summary)
        print(f"CAMPAIGN {campaign} STOP P20 next_for_chain={p20_next}", flush=True)

    (OUT / "SEMANTIC_HELIX_LEDGER.md").write_text("# Semantic Helix ledger\n\nEvidence inherits; confidence does not.\n\n" + "\n".join(f"- {x}" for x in global_helix) + "\n", encoding="utf-8", newline="\n")
    (OUT / "CAMPAIGN_CHAIN_SUMMARY.json").write_text(json.dumps(chain, indent=2), encoding="utf-8", newline="\n")
    manifest["completed"] = datetime.now().isoformat()
    manifest["passes_completed"] = total_passes
    manifest["campaign_chain"] = chain
    manifest["final_next_question"] = question
    (OUT / "RUN_MANIFEST.final.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8", newline="\n")
    print(f"COMPLETE passes={total_passes} final_next={question} out={OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
