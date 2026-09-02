#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

FORBIDDEN_LEARNER_TERMS = ["ATMS", "CDCL", "LHIT", "CFE", "nogood", "truth maintenance"]
EXPECTED_FAMILY_COUNTS = {"MEMORY_CURRENTNESS": 64, "SCIENCE_DIAGNOSIS": 64}
EXPECTED_SUBTYPES = {
    "MEMORY_CURRENTNESS": {
        "DIRECT_STALE_UPDATE": 16,
        "INDIRECT_PROPAGATED_INVALIDATION": 16,
        "SELECTIVE_PRESERVATION": 16,
        "AMBIGUOUS_CURRENTNESS_DISCRIMINATOR": 16,
    },
    "SCIENCE_DIAGNOSIS": {
        "CHOOSE_DISCRIMINATOR": 16,
        "UPDATE_CANDIDATES": 16,
        "SUPPORT_VS_DISCRIMINATION": 16,
        "REPRESENTATION_REFINEMENT": 16,
    },
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalized_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--jsonl",type=Path,required=True); ap.add_argument("--manifest",type=Path,required=True); ap.add_argument("--out",type=Path,required=True); a=ap.parse_args()
    rows=load_jsonl(a.jsonl); manifest=json.loads(a.manifest.read_text(encoding="utf-8"))
    errors=[]; warnings=[]
    fam=Counter(); sub=Counter(); pack=Counter(); ids=set(); prompts=set(); convs=set(); dim_by_family=defaultdict(Counter)
    if sha256_file(a.jsonl) != manifest.get("jsonl_sha256"): errors.append("MANIFEST_JSONL_SHA_MISMATCH")
    if len(rows) != manifest.get("rows"): errors.append("MANIFEST_ROW_COUNT_MISMATCH")
    for i,r in enumerate(rows):
        rid=r.get("atom_id")
        if not rid or rid in ids: errors.append(f"DUPLICATE_OR_MISSING_ATOM_ID:{i}")
        ids.add(rid)
        family=r.get("pilot",{}).get("family"); subtype=r.get("pilot",{}).get("subtype"); packaging=r.get("pilot",{}).get("packaging")
        fam[family]+=1; sub[(family,subtype)]+=1; pack[(family,packaging)]+=1
        if r.get("admission",{}).get("state") != "QUARANTINE": errors.append(f"NON_QUARANTINE:{i}")
        if r.get("contamination",{}).get("state") != "UNSCREENED_PROJECT_GENERATED": errors.append(f"BAD_CONTAM_STATE:{i}")
        if r.get("license",{}).get("labels") != ["CC0-1.0"]: errors.append(f"BAD_LICENSE:{i}")
        if r.get("quality",{}).get("state") != "CANDIDATE": errors.append(f"BAD_QUALITY_STATE:{i}")
        msgs=r.get("content",{}).get("messages") or []
        if not msgs or not any(m.get("role")=="user" for m in msgs): errors.append(f"MISSING_USER:{i}")
        if packaging=="MULTI_TURN" and len(msgs)<3: errors.append(f"BAD_MULTI_TURN:{i}")
        if packaging=="SINGLE_TURN" and len(msgs)!=1: errors.append(f"BAD_SINGLE_TURN:{i}")
        learner="\n".join(m.get("content","") for m in msgs)+"\n"+(r.get("content",{}).get("final_answer") or "")
        for term in FORBIDDEN_LEARNER_TERMS:
            if term.lower() in learner.lower(): errors.append(f"FORBIDDEN_LEARNER_TERM:{i}:{term}")
        ph=r.get("dedup",{}).get("canonical_prompt_hash"); ch=r.get("dedup",{}).get("conversation_hash")
        if ph in prompts: errors.append(f"DUPLICATE_PROMPT:{i}")
        if ch in convs: errors.append(f"DUPLICATE_CONVERSATION:{i}")
        prompts.add(ph); convs.add(ch)
        x=r.get("invariants",{}).get("lhit_cross_domain",{})
        if x.get("state") != "CURATOR_STRUCTURE_BY_CONSTRUCTION": errors.append(f"BAD_INVARIANT_STATE:{i}")
        if x.get("domain_families") != [family]: errors.append(f"FAMILY_MISMATCH:{i}")
        for d in x.get("candidate_dimensions",[]): dim_by_family[family][d]+=1
        hidden=r.get("pilot",{}).get("hidden_curator_contract") or {}
        final=r.get("content",{}).get("final_answer") or ""
        if hidden.get("expected") and hidden["expected"] != final: errors.append(f"MEMORY_EXPECTED_MISMATCH:{i}")
        if family=="SCIENCE_DIAGNOSIS":
            if subtype=="CHOOSE_DISCRIMINATOR":
                best=hidden.get("best_test"); ties=hidden.get("best_ties") or []; scores=hidden.get("test_scores") or {}
                ranks={t:(z["partition_gain"],z["outcome_count"]) for t,z in scores.items()}
                if not ranks or best not in ranks: errors.append(f"MISSING_DISCRIMINATOR_SCORES:{i}")
                else:
                    mx=max(ranks.values()); actual=sorted(t for t,v in ranks.items() if v==mx)
                    if actual != sorted(ties): errors.append(f"BEST_TIES_MISMATCH:{i}")
                    if best not in actual: errors.append(f"BEST_TEST_NOT_BEST:{i}")
                    if len(actual)==1 and "strongest partition" not in final: errors.append(f"UNIQUE_BEST_WORDING_MISMATCH:{i}")
                    if len(actual)>1 and "one of the most discriminating" not in final: errors.append(f"TIED_BEST_WORDING_MISMATCH:{i}")
            elif subtype=="UPDATE_CANDIDATES":
                survivors=hidden.get("survivors") or []
                for h in survivors:
                    if h not in final: errors.append(f"SURVIVOR_MISSING_FROM_FINAL:{i}:{h}")
            elif subtype=="SUPPORT_VS_DISCRIMINATION":
                scores=hidden.get("test_scores") or {}; best=hidden.get("preferred"); other=hidden.get("comparison"); relation=hidden.get("rank_relation")
                ranks={t:(z["partition_gain"],z["outcome_count"]) for t,z in scores.items()}
                if best not in ranks or other not in ranks: errors.append(f"COMPARISON_SCORE_MISSING:{i}")
                elif relation=="STRICT" and not (ranks[best]>ranks[other]): errors.append(f"FALSE_STRICT_RANK:{i}")
                elif relation=="TIED" and ranks[best]!=ranks[other]: errors.append(f"FALSE_TIED_RANK:{i}")
            elif subtype=="REPRESENTATION_REFINEMENT":
                if not hidden.get("requires_model_refinement"): errors.append(f"MISSING_REFINEMENT_FLAG:{i}")
                if "model class is inadequate" not in final: errors.append(f"REFINEMENT_FINAL_MISSING:{i}")
    if dict(fam) != EXPECTED_FAMILY_COUNTS: errors.append(f"FAMILY_COUNTS:{dict(fam)}")
    for family, expect in EXPECTED_SUBTYPES.items():
        got={st:sub[(family,st)] for st in expect}
        if got != expect: errors.append(f"SUBTYPE_COUNTS:{family}:{got}")
    # Require single-record and multi-turn memory; science intentionally single-record to break conversation-shape dependence.
    if pack[("MEMORY_CURRENTNESS","SINGLE_TURN")] != 32 or pack[("MEMORY_CURRENTNESS","MULTI_TURN")] != 32: errors.append(f"MEMORY_PACKAGING:{dict(pack)}")
    if pack[("SCIENCE_DIAGNOSIS","SINGLE_TURN")] != 64: errors.append(f"SCIENCE_PACKAGING:{dict(pack)}")
    required_dims={
        "MEMORY_CURRENTNESS":{"CONSEQUENTIAL_HISTORY_CANDIDATE","CURRENTNESS_PROPAGATION_CANDIDATE","DEPENDENCY_LOCAL_REPAIR_CANDIDATE","UNRESOLVED_SEAM_PRESERVATION_CANDIDATE"},
        "SCIENCE_DIAGNOSIS":{"LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE","ACTIVE_DISCRIMINATOR_CANDIDATE","EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE","REPRESENTATION_REFINEMENT_CANDIDATE","CURRENTNESS_PROPAGATION_CANDIDATE"},
    }
    for family,dims in required_dims.items():
        missing=[d for d in dims if dim_by_family[family][d] <= 0]
        if missing: errors.append(f"MISSING_REQUIRED_DIMENSIONS:{family}:{missing}")
    report={
        "schema":"cfe.standard-uplift.project-generated-gap-fillers-verification.v1",
        "status":"PASS" if not errors else "FAIL",
        "jsonl":str(a.jsonl).replace("\\","/"),
        "jsonl_sha256":sha256_file(a.jsonl),
        "rows":len(rows),
        "family_counts":dict(fam),
        "subtype_counts":{f"{k[0]}::{k[1]}":v for k,v in sorted(sub.items())},
        "packaging_counts":{f"{k[0]}::{k[1]}":v for k,v in sorted(pack.items())},
        "dimension_counts":{f:dict(c) for f,c in dim_by_family.items()},
        "unique_atom_ids":len(ids),"unique_prompts":len(prompts),"unique_conversations":len(convs),
        "errors":errors,"warnings":warnings,
        "claim_ceiling":"PASS verifies generator contracts, uniqueness, quarantine/license metadata, and learner-facing structural expectations. It does not perform contamination screening, semantic near-dedup against upstream corpora, or scientific validation of the underlying invariants."
    }
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(report,indent=2)); raise SystemExit(0 if not errors else 3)

if __name__=="__main__": main()
