#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, math, re, time
from collections import Counter
from pathlib import Path
from typing import Any


def stable_json(x: Any) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    # JSONL records are delimited by ASCII LF. str.splitlines() is unsafe here because it also
    # splits on Unicode line separators that may legitimately occur inside escaped/source text.
    rows = []
    with p.open("r", encoding="utf-8", newline="") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                raise ValueError(f"JSONL_PARSE_ERROR {p} line={line_no}: {exc}") from exc
    return rows


def write_jsonl(p: Path, rows: list[dict[str, Any]]) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(stable_json(r) + "\n")
    return sha256_file(p)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def prompt_text(atom: dict[str, Any]) -> str:
    for m in atom.get("content",{}).get("messages") or []:
        if m.get("role") == "user":
            return m.get("content","")
    return ""


def word_shingles(s: str, n: int = 3) -> set[tuple[str,...]]:
    toks=re.findall(r"[a-z0-9_./:-]+", norm(s))
    if len(toks)<n:
        return {tuple(toks)} if toks else set()
    return {tuple(toks[i:i+n]) for i in range(len(toks)-n+1)}


def jaccard(a: set[Any], b: set[Any]) -> float:
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",type=Path,required=True,help="Existing v2 pilot directory")
    ap.add_argument("--generated",type=Path,required=True,help="Verified project-generated gap-filler directory")
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--near-dup-fail",type=float,default=0.90)
    a=ap.parse_args()
    if a.out.exists(): raise SystemExit(f"REFUSE_OVERWRITE {a.out}")
    base_summary=json.loads((a.base/"SUMMARY.json").read_text(encoding="utf-8"))
    base_sft=a.base/"SFT_QUARANTINE_ATOMS.jsonl"; base_pref=a.base/"PREFERENCE_QUARANTINE.jsonl"
    if sha256_file(base_sft) != base_summary["sft_sha256"]: raise SystemExit("BASE_SFT_SHA_MISMATCH")
    if sha256_file(base_pref) != base_summary["preference_sha256"]: raise SystemExit("BASE_PREF_SHA_MISMATCH")
    gen_manifest=json.loads((a.generated/"MANIFEST.json").read_text(encoding="utf-8"))
    gen_verify=json.loads((a.generated/"VERIFICATION.json").read_text(encoding="utf-8"))
    gen_jsonl=a.generated/"PROJECT_GENERATED_SFT_QUARANTINE.jsonl"
    if gen_verify.get("status") != "PASS": raise SystemExit("GENERATED_VERIFICATION_NOT_PASS")
    if sha256_file(gen_jsonl) != gen_manifest["jsonl_sha256"] or sha256_file(gen_jsonl) != gen_verify["jsonl_sha256"]: raise SystemExit("GENERATED_SHA_MISMATCH")
    base_atoms=load_jsonl(base_sft); gen_atoms=load_jsonl(gen_jsonl); prefs=load_jsonl(base_pref)
    # Exact dedup across base+generated is fail-closed.
    base_ids={r["atom_id"] for r in base_atoms}; base_ph={r["dedup"]["canonical_prompt_hash"] for r in base_atoms}; base_ch={r["dedup"]["conversation_hash"] for r in base_atoms}
    exact_conflicts=[]
    for r in gen_atoms:
        if r["atom_id"] in base_ids: exact_conflicts.append((r["atom_id"],"ATOM_ID"))
        if r["dedup"]["canonical_prompt_hash"] in base_ph: exact_conflicts.append((r["atom_id"],"PROMPT"))
        if r["dedup"]["conversation_hash"] in base_ch: exact_conflicts.append((r["atom_id"],"CONVERSATION"))
    if exact_conflicts: raise SystemExit(f"CROSS_CORPUS_EXACT_DUPLICATE {exact_conflicts[:10]}")
    # Lightweight lexical near-dup audit: generated prompts vs base prompts only.
    base_pairs=[(r["atom_id"],word_shingles(prompt_text(r))) for r in base_atoms]
    near=[]; max_sim=(0.0,None,None)
    for g in gen_atoms:
        gs=word_shingles(prompt_text(g))
        best=(0.0,None)
        for bid,bs in base_pairs:
            sim=jaccard(gs,bs)
            if sim>best[0]: best=(sim,bid)
        if best[0]>max_sim[0]: max_sim=(best[0],g["atom_id"],best[1])
        if best[0] >= a.near_dup_fail: near.append({"generated":g["atom_id"],"base":best[1],"jaccard_3gram":best[0]})
    if near: raise SystemExit(f"CROSS_CORPUS_NEAR_DUPLICATE >= {a.near_dup_fail}: {near[:10]}")
    all_atoms=base_atoms+gen_atoms
    a.out.mkdir(parents=True)
    sft_sha=write_jsonl(a.out/"SFT_QUARANTINE_ATOMS.jsonl",all_atoms)
    pref_sha=write_jsonl(a.out/"PREFERENCE_QUARANTINE.jsonl",prefs)
    source_stats=dict(base_summary.get("source_stats") or {})
    source_stats["project_memory_currentness_v1"]={"repo":"CFE/project-generated-standard-uplift","split":"quarantine","requested":64,"normalized":64,"scanned":64,"read_modes":{"PROJECT_GENERATED_VERIFIED":64},"error":None}
    source_stats["project_science_diagnosis_v1"]={"repo":"CFE/project-generated-standard-uplift","split":"quarantine","requested":64,"normalized":64,"scanned":64,"read_modes":{"PROJECT_GENERATED_VERIFIED":64},"error":None}
    summary={
        "schema":"cfe.standard-uplift.intake-pilot.v3",
        "status":"NORMALIZATION_PILOT_COMPLETE__SOURCE_GAPS_FILLED_AT_QUARANTINE__NOT_TRAINABLE",
        "created_unix":time.time(),
        "base_pilot":str(a.base).replace("\\","/"),
        "base_schema":base_summary.get("schema"),
        "base_sft_sha256":base_summary["sft_sha256"],
        "generated_manifest_sha256":sha256_file(a.generated/"MANIFEST.json"),
        "generated_verification_sha256":sha256_file(a.generated/"VERIFICATION.json"),
        "source_stats":source_stats,
        "sft_atoms":len(all_atoms),
        "preference_atoms":len(prefs),
        "sft_sha256":sft_sha,
        "preference_sha256":pref_sha,
        "quality_states":dict(Counter(r["quality"]["state"] for r in all_atoms)),
        "interaction_shapes":dict(Counter(r["capability"]["interaction_shape"] for r in all_atoms)),
        "license_states":dict(Counter(r["license"]["state"] for r in all_atoms)),
        "contamination_states":dict(Counter(r["contamination"]["state"] for r in all_atoms)),
        "lhit_cross_domain_dimensions":dict(Counter(x for r in all_atoms for x in r["invariants"]["lhit_cross_domain"]["candidate_dimensions"])),
        "lhit_domain_families":dict(Counter(x for r in all_atoms for x in r["invariants"]["lhit_cross_domain"]["domain_families"])),
        "lhit_dimension_by_domain":dict(Counter(f"{f}::{d}" for r in all_atoms for f in r["invariants"]["lhit_cross_domain"]["domain_families"] for d in r["invariants"]["lhit_cross_domain"]["candidate_dimensions"])),
        "cross_corpus_exact_duplicates":0,
        "cross_corpus_near_duplicate_threshold":a.near_dup_fail,
        "cross_corpus_near_duplicates_at_or_above_threshold":0,
        "cross_corpus_max_prompt_jaccard_3gram":{"score":max_sim[0],"generated_atom":max_sim[1],"base_atom":max_sim[2]},
        "laws":[
            "PILOT QUARANTINE != TRAINABLE CORPUS",
            "PROJECT GENERATED != CONTAMINATION CLEARED",
            "GENERATOR CONTRACT PASS != HOSTILE QUALITY PASS",
            "LHIT != CONVERSATION FORMAT",
            "SOURCE FAMILY PRESENT != FINAL QUALIFIED COVERAGE",
            "PREFERENCE DATA REMAINS PHYSICALLY SEPARATE FROM SFT",
            "BASE V2 BYTES VERIFIED BEFORE MERGE"
        ]
    }
    (a.out/"SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
