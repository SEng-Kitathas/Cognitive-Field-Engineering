#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REQUIRED_TOP = ["atom_id","source","license","content","capability","quality","invariants","contamination","dedup","tokenization","admission"]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    rows=[]
    with p.open("r",encoding="utf-8",newline="") as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            try: rows.append(json.loads(line))
            except Exception as exc: raise ValueError(f"JSONL_PARSE_ERROR {p} line={line_no}: {exc}") from exc
    return rows


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--pilot",type=Path,required=True); ap.add_argument("--generated-verification",type=Path,required=True); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    summary=json.loads((a.pilot/"SUMMARY.json").read_text(encoding="utf-8")); sft=a.pilot/"SFT_QUARANTINE_ATOMS.jsonl"; pref=a.pilot/"PREFERENCE_QUARANTINE.jsonl"
    if sha256_file(sft)!=summary["sft_sha256"]: raise SystemExit("SFT_SHA_MISMATCH")
    if sha256_file(pref)!=summary["preference_sha256"]: raise SystemExit("PREF_SHA_MISMATCH")
    gv=json.loads(a.generated_verification.read_text(encoding="utf-8"))
    if gv.get("status")!="PASS": raise SystemExit("GENERATED_VERIFICATION_NOT_PASS")
    rows=load_jsonl(sft); prefs=load_jsonl(pref)
    missing=[]; ids=[]; prompt_groups=defaultdict(list); conv_groups=defaultdict(list); source_counts=Counter(); family_counts=Counter(); dims=Counter()
    learner_donor_hits=[]
    for i,r in enumerate(rows):
        miss=[k for k in REQUIRED_TOP if k not in r]
        if miss: missing.append({"row":i,"atom_id":r.get("atom_id"),"missing":miss})
        ids.append(r.get("atom_id")); prompt_groups[r.get("dedup",{}).get("canonical_prompt_hash")].append(r.get("atom_id")); conv_groups[r.get("dedup",{}).get("conversation_hash")].append(r.get("atom_id"))
        source_counts[r.get("source",{}).get("config") or r.get("source",{}).get("repo")]+=1
        for fam in r.get("invariants",{}).get("lhit_cross_domain",{}).get("domain_families",[]): family_counts[fam]+=1
        for d in r.get("invariants",{}).get("lhit_cross_domain",{}).get("candidate_dimensions",[]): dims[d]+=1
        text="\n".join(m.get("content","") for m in r.get("content",{}).get("messages",[]))+"\n"+(r.get("content",{}).get("final_answer") or "")
        semantic_patterns = [
            ("COGNITIVE_FIELD_ENGINEERING", r"\bcognitive\s+field\s+engineering\b"),
            ("ASSUMPTION_BASED_TMS", r"\bassumption[- ]based\s+(?:truth\s+maintenance\s+system|tms)\b"),
            ("TRUTH_MAINTENANCE_SYSTEM", r"\btruth\s+maintenance\s+system\b"),
            ("LHIT_LITERAL", r"\bLHIT\b"),
            ("LONG_HORIZON_INTERACTION_TRAINING", r"\blong[- ]horizon\s+interaction\s+training\b"),
            ("CDCL_EXPLICIT", r"\bconflict[- ]driven\s+clause\s+learning\b"),
        ]
        for label, pattern in semantic_patterns:
            if re.search(pattern, text, re.I):
                learner_donor_hits.append({"atom_id":r.get("atom_id"),"term":label})
    dup_prompt={k:v for k,v in prompt_groups.items() if k and len(v)>1}; dup_conv={k:v for k,v in conv_groups.items() if k and len(v)>1}
    blockers=[]
    contam=Counter(r.get("contamination",{}).get("state") for r in rows); licenses=Counter(r.get("license",{}).get("state") for r in rows); quality=Counter(r.get("quality",{}).get("state") for r in rows); adm=Counter(r.get("admission",{}).get("state") for r in rows)
    if missing: blockers.append("MISSING_REQUIRED_FIELDS")
    if len(set(ids))!=len(rows): blockers.append("DUPLICATE_ATOM_IDS")
    if any(k not in {"CLEARED"} for k in contam): blockers.append("CONTAMINATION_NOT_CLEARED")
    if licenses.get("SEGREGATION_REQUIRED",0): blockers.append("LICENSE_SEGREGATION_REQUIRED")
    if quality.get("RAW",0): blockers.append("RAW_QUALITY_ROWS_REMAIN")
    if dup_prompt: blockers.append("PROMPT_DEDUP_REQUIRED")
    if learner_donor_hits: blockers.append("LEARNER_FACING_DONOR_JARGON")
    if any(k!="QUARANTINE" for k in adm): blockers.append("UNEXPECTED_ADMISSION_STATE")
    # Quarantine is itself a blocker for trainable promotion.
    if adm.get("QUARANTINE",0)==len(rows): blockers.append("ALL_ROWS_STILL_QUARANTINE")
    gap_presence={"MEMORY_CURRENTNESS":family_counts.get("MEMORY_CURRENTNESS",0),"SCIENCE_DIAGNOSIS":family_counts.get("SCIENCE_DIAGNOSIS",0)}
    if not all(gap_presence.values()): blockers.append("LHIT_REQUIRED_SOURCE_FAMILY_MISSING")
    report={
      "schema":"cfe.standard-uplift.intake-v3-integrity.v1",
      "status":"SOURCE_GAPS_FILLED__FINAL_ADMISSION_BLOCKED" if all(gap_presence.values()) and blockers else ("PASS" if not blockers else "FAIL"),
      "pilot":str(a.pilot).replace("\\","/"),"summary_sha256":sha256_file(a.pilot/"SUMMARY.json"),"sft_sha256":sha256_file(sft),"preference_sha256":sha256_file(pref),
      "sft_atoms":len(rows),"preference_atoms":len(prefs),"unique_atom_ids":len(set(ids)),"missing_required_count":len(missing),"missing_required":missing[:50],
      "duplicate_prompt_hash_groups":len(dup_prompt),"duplicate_prompt_rows":sum(len(v) for v in dup_prompt.values()),"duplicate_conversation_hash_groups":len(dup_conv),"duplicate_conversation_rows":sum(len(v) for v in dup_conv.values()),
      "quality_states":dict(quality),"license_states":dict(licenses),"contamination_states":dict(contam),"admission_states":dict(adm),"source_counts":dict(source_counts),"lhit_domain_families":dict(family_counts),"lhit_dimension_counts":dict(dims),
      "required_gap_family_presence":gap_presence,"generated_verification_status":gv.get("status"),"generated_jsonl_sha256":gv.get("jsonl_sha256"),"learner_donor_jargon_hits":learner_donor_hits,
      "blockers":blockers,
      "laws":["SOURCE GAP FILLED != TRAINING ADMITTED","QUARANTINE != TRAINABLE","HEURISTIC COVERAGE != QUALIFIED COVERAGE","CONTAMINATION CLEARANCE MUST BE EXPLICIT","LICENSE SEGREGATION MUST PRECEDE MERGE","PROMPT DUPLICATE GROUP != AUTOMATIC DUPLICATE ANSWER—REVIEW BEFORE COLLAPSE"]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); print(json.dumps(report,indent=2))

if __name__=="__main__": main()
