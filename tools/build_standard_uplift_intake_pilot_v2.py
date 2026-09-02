#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import time
import requests
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from datasets import load_dataset
from huggingface_hub import hf_hub_url

SEED = 20260902

SOURCES = [
    {"key": "openr1", "repo": "open-r1/OpenR1-Math-220k", "revision": "e4e141ec9dea9f8326f4d347be56105859b2bd68", "config": "default", "split": "train", "license": ["apache-2.0"], "lane": ["math", "reasoning"], "n": 180},
    {"key": "nem_math", "repo": "nvidia/Nemotron-SFT-Math-v4", "revision": "84d42ad0cb960f07f951b9baa9ed2b46a5a18c66", "config": "default", "split": "train", "license": ["row-specific"], "lane": ["math", "reasoning"], "n": 180},
    {"key": "openthoughts", "repo": "open-thoughts/OpenThoughts-114k", "revision": "bd093c3994fd54d2390985b66988ddf282a55eb6", "config": "default", "split": "train", "license": ["apache-2.0"], "lane": ["reasoning", "math", "science", "code"], "n": 160},
    {"key": "nem_if_off", "repo": "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2", "revision": "1a9454ed054b8544503ab8d8c0a519d141a44c5b", "config": "default", "split": "reasoning_off", "license": ["odc-by"], "lane": ["instruction_following", "chat", "structured_output"], "n": 100, "raw_jsonl": "data/reasoning_off.jsonl"},
    {"key": "nem_if_on", "repo": "nvidia/Nemotron-SFT-Instruction-Following-Chat-v2", "revision": "1a9454ed054b8544503ab8d8c0a519d141a44c5b", "config": "default", "split": "reasoning_on", "license": ["odc-by"], "lane": ["instruction_following", "reasoning"], "n": 100, "raw_jsonl": "data/reasoning_on.jsonl"},
    {"key": "nem_agent_interactive", "repo": "nvidia/Nemotron-SFT-Agentic-v2", "revision": "7c804833427f633ccd53b582dbf02525fd680f78", "config": "default", "split": "interactive_agent", "license": ["mixed-source"], "lane": ["tool_use", "agent", "long_horizon"], "n": 80, "raw_jsonl": "data/interactive_agent.jsonl"},
    {"key": "nem_agent_search", "repo": "nvidia/Nemotron-SFT-Agentic-v2", "revision": "7c804833427f633ccd53b582dbf02525fd680f78", "config": "default", "split": "search", "license": ["mixed-source"], "lane": ["tool_use", "agent", "search", "research"], "n": 80, "raw_jsonl": "data/search.jsonl"},
    {"key": "nem_agent_tools", "repo": "nvidia/Nemotron-SFT-Agentic-v2", "revision": "7c804833427f633ccd53b582dbf02525fd680f78", "config": "default", "split": "tool_calling", "license": ["mixed-source"], "lane": ["tool_use", "agent"], "n": 80, "raw_jsonl": "data/tool_calling.jsonl"},
    {"key": "nem_code_py", "repo": "nvidia/Nemotron-SFT-Competitive-Programming-v2", "revision": "778afc98a9e027e10b3cd78020c120e93e142ef2", "config": "default", "split": "competitive_coding_python", "license": ["row-specific"], "lane": ["code", "reasoning"], "n": 100, "raw_jsonl": "data/competitive_programming_python_00.jsonl"},
    {"key": "nem_code_cpp", "repo": "nvidia/Nemotron-SFT-Competitive-Programming-v2", "revision": "778afc98a9e027e10b3cd78020c120e93e142ef2", "config": "default", "split": "competitive_coding_cpp", "license": ["row-specific"], "lane": ["code", "reasoning"], "n": 80, "raw_jsonl": "data/competitive_programming_cpp_00.jsonl"},
    {"key": "nem_sql", "repo": "nvidia/Nemotron-SFT-Competitive-Programming-v2", "revision": "778afc98a9e027e10b3cd78020c120e93e142ef2", "config": "default", "split": "text_to_sql", "license": ["row-specific"], "lane": ["code", "sql", "structured_output"], "n": 60, "raw_jsonl": "data/text_to_sql.jsonl"},
    {"key": "swe", "repo": "nvidia/Open-SWE-Traces", "revision": "1e02268b36de153ab4b18707571c1cedba62cd10", "config": "v1.0", "split": "openhands", "license": ["row-specific"], "lane": ["software_engineering", "agent", "tool_use"], "n": 80, "force_contam_review": True},
    {"key": "quest_open", "repo": "osunlp/QUEST-SFT-Data-Open-ended", "revision": "3d3d79ac4e2e6e0b8d1072d19bd57512c40c469b", "config": "default", "split": "train", "license": ["mit"], "lane": ["deep_research", "evidence_synthesis", "search"], "n": 100},
    {"key": "quest_obj", "repo": "osunlp/QUEST-SFT-Data-Objective", "revision": "5eddb5e9503cbe60761e573c16eff251b017cebe", "config": "default", "split": "train", "license": ["mit"], "lane": ["deep_research", "objective_research", "reasoning"], "n": 80},
    {"key": "lite_research", "repo": "simplex-ai-inc/LiteResearcher-SFT-Data", "revision": "5c8caa17121e216f8ad8f928e6a8d4f51d3fefee", "config": "default", "split": "train", "license": ["apache-2.0"], "lane": ["deep_research", "search", "long_horizon"], "n": 100},
    {"key": "nextsearch", "repo": "NextTokenAI/NextSearch-1-Trajectories", "revision": "d32183c6289d32c5d51b6247e68d53a58dddd495", "config": "sft-trajectories", "split": "train", "license": ["apache-2.0"], "lane": ["deep_research", "search", "tool_use"], "n": 100},
    {"key": "capybara", "repo": "LDJnr/Capybara", "revision": "c2bc39ac72f24748f60f5fb55b77e08fb0660ba6", "config": "default", "split": "train", "license": ["apache-2.0"], "lane": ["long_horizon_interaction", "multi_turn"], "n": 180},
]

PREFERENCE = {"key": "capybara_pref", "repo": "argilla/Capybara-Preferences-Filtered", "revision": "c9ce1cae33b7ab9d84b4137d93e80538d218fddf", "config": "default", "split": "train", "license": ["apache-2.0"], "lane": ["preference", "long_horizon_interaction"], "n": 120}


def stable_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def htext(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def clean_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for m in messages or []:
        role = m.get("role") or m.get("from")
        role = {"human": "user", "gpt": "assistant"}.get(role, role)
        if role not in {"system", "user", "assistant", "tool"}:
            continue
        content = m.get("content")
        if content is None:
            content = m.get("value", "")
        if not isinstance(content, str):
            content = stable_json(content)
        z = {"role": role, "content": content}
        for k in ("tool_calls", "tool_call_id", "name", "reasoning_content"):
            if m.get(k) not in (None, "", []):
                z[k] = m.get(k)
        out.append(z)
    return out


def infer_interaction(messages: list[dict[str, Any]], tools: list[Any] | None = None, lanes: list[str] | None = None) -> str:
    if tools or any(m.get("role") == "tool" or m.get("tool_calls") for m in messages):
        return "RESEARCH_TRAJECTORY" if lanes and any(x in lanes for x in ("deep_research", "search", "research")) else "TOOL_TRAJECTORY"
    users = sum(1 for m in messages if m.get("role") == "user")
    return "MULTI_TURN" if users > 1 else "SINGLE_TURN"


def infer_domain_families(lanes: list[str]) -> list[str]:
    z = set(lanes or [])
    out = []
    if z & {"code", "software_engineering", "sql"}: out.append("CODE_DEBUGGING")
    if z & {"deep_research", "evidence_synthesis", "objective_research", "search", "research"}: out.append("RESEARCH")
    if z & {"tool_use", "agent"}: out.append("PLANNING_TOOL_AGENT")
    if z & {"math", "reasoning", "science"}: out.append("MATH_SCIENCE_REASONING")
    if z & {"long_horizon", "long_horizon_interaction", "multi_turn"}: out.append("LHIT_LONG_HORIZON")
    if z & {"instruction_following", "chat", "structured_output"}: out.append("GENERAL_INTERACTION")
    return sorted(set(out or ["GENERAL_OTHER"]))


def cross_domain_lhit_candidates(messages: list[dict[str, Any]], interaction: str, lanes: list[str], reasoning: str | None = None) -> dict[str, Any]:
    # Curator-side heuristic only. Detect consequence/history structures independently of conversation packaging.
    text = "\n".join(m.get("content", "") for m in messages)
    if reasoning:
        text += "\n" + reasoning
    low = normalize_ws(text).lower()
    dims = set()
    evidence = []
    families = infer_domain_families(lanes)

    def hit(label: str, terms: tuple[str, ...], note: str) -> bool:
        if any(t in low for t in terms):
            dims.add(label); evidence.append(note); return True
        return False

    temporal = hit("CONSEQUENTIAL_HISTORY_CANDIDATE", ("previous", "earlier", "prior ", "later", "subsequent", "after ", "before ", "revisit", "changed", "update", "updated"), "temporal/state-change language")
    current = hit("CURRENTNESS_PROPAGATION_CANDIDATE", ("stale", "outdated", "no longer", "currently", "latest", "new evidence", "updated", "changed since"), "currentness/revision language")
    repair = hit("DEPENDENCY_LOCAL_REPAIR_CANDIDATE", ("debug", "bug", "error", "failed", "failure", "incorrect", "wrong", "regression", "rollback", "revert", "repair", "fix"), "failure/repair language")
    verify = hit("EXTERNAL_OR_ORTHOGONAL_CHECK_CANDIDATE", ("test", "verify", "validate", "check", "measurement", "observation", "tool result", "run the", "execute"), "verification/observation language")
    alternatives = hit("LIVE_ALTERNATIVES_OR_DISCRIMINATOR_CANDIDATE", ("hypothesis", "hypotheses", "alternative", "either", "distinguish", "discriminate", "which of", "root cause"), "alternative/discriminator language")
    representation = hit("REPRESENTATION_REFINEMENT_CANDIDATE", ("representation", "abstraction", "granularity", "schema", "data model", "missing distinction", "too coarse", "refactor"), "representation/abstraction language")
    unresolved = hit("UNRESOLVED_SEAM_PRESERVATION_CANDIDATE", ("unknown", "insufficient evidence", "not enough information", "unresolved", "unclear", "cannot determine"), "explicit unresolved/unknown language")

    if interaction in {"MULTI_TURN", "TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"}:
        dims.add("LONG_HORIZON_STATE_CARRY_CANDIDATE")
        evidence.append("interaction carries state across multiple events")
    if interaction in {"TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"}:
        dims.add("FOLLOWUP_CONSEQUENCE_TRACKING_CANDIDATE")
        dims.add("REVISIT_AFTER_STATE_CHANGE_CANDIDATE")
        evidence.append("tool/research trajectory permits observation-driven revision")
    if "RESEARCH" in families and (alternatives or verify):
        dims.add("ACTIVE_DISCRIMINATOR_CANDIDATE")
    if "CODE_DEBUGGING" in families and repair:
        dims.add("FAILURE_BOUNDARY_TRANSFER_CANDIDATE")
    if "PLANNING_TOOL_AGENT" in families and (temporal or current or interaction in {"TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"}):
        dims.add("STATEFUL_PLAN_REVISION_CANDIDATE")
    if "MATH_SCIENCE_REASONING" in families and repair and verify:
        dims.add("LOCAL_DERIVATION_REVISION_CANDIDATE")
    if "LHIT_LONG_HORIZON" in families:
        dims.add("LONG_HORIZON_STATE_CARRY_CANDIDATE")
    # A single packaged record can still carry LHIT structure; no multi-turn requirement here.
    state = "HEURISTIC_CANDIDATE" if dims else "UNASSESSED"
    return {"state": state, "domain_families": families, "candidate_dimensions": sorted(dims), "evidence": sorted(set(evidence))}


def heuristic_invariants(messages: list[dict[str, Any]], interaction: str, lanes: list[str], reasoning: str | None = None) -> dict[str, Any]:
    cfe = []
    lhit = []
    users = sum(1 for m in messages if m.get("role") == "user")
    assistants = sum(1 for m in messages if m.get("role") == "assistant")
    if interaction in {"MULTI_TURN", "TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"} and users >= 2:
        cfe.append("CONSEQUENTIAL_HISTORY_CANDIDATE")
        lhit.append("LONG_HORIZON_STATE_CARRY_CANDIDATE")
    if interaction in {"TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"}:
        lhit.extend(["FOLLOWUP_CONSEQUENCE_TRACKING_CANDIDATE", "FAILED_BRANCH_RECOVERY_CANDIDATE"])
        cfe.append("CURRENTNESS_AND_REVISION_CANDIDATE")
    if "deep_research" in lanes or "research" in lanes:
        lhit.extend(["QUESTION_RETENTION_CANDIDATE", "EVIDENCE_STATE_SEPARATION_CANDIDATE"])
    if users >= 3 and assistants >= 2:
        lhit.append("MULTITURN_CAPABILITY_GROWTH_CANDIDATE")
    return {"cfe": sorted(set(cfe)), "lhit": sorted(set(lhit)), "lhit_cross_domain": cross_domain_lhit_candidates(messages, interaction, lanes, reasoning), "tags_state": "HEURISTIC" if cfe or lhit else "UNASSESSED"}


def messages_from_row(key: str, row: dict[str, Any]) -> tuple[list[dict[str, Any]], list[Any], str | None, str | None]:
    reasoning = None
    final = None
    tools = row.get("tools") or []
    if key == "openr1":
        msgs = clean_messages(row.get("messages") or [])
        if not msgs:
            msgs = [{"role": "user", "content": row.get("problem", "")}, {"role": "assistant", "content": row.get("solution", "")}]
        final = row.get("answer")
        return msgs, tools, reasoning, final
    if key == "openthoughts":
        msgs = []
        if row.get("system"):
            msgs.append({"role": "system", "content": row["system"]})
        msgs += clean_messages(row.get("conversations") or [])
        return msgs, tools, reasoning, final
    if key == "capybara":
        msgs = []
        for pair in row.get("conversation") or []:
            if pair.get("input"):
                msgs.append({"role": "user", "content": pair.get("input", "")})
            if pair.get("output"):
                msgs.append({"role": "assistant", "content": pair.get("output", "")})
        return msgs, tools, reasoning, final
    if key == "lite_research":
        return clean_messages(row.get("conversations") or []), tools, reasoning, final
    if key == "nextsearch":
        msgs = clean_messages(row.get("messages") or []) + clean_messages(row.get("target") or [])
        rs = [m.get("reasoning_content") for m in msgs if m.get("role") == "assistant" and m.get("reasoning_content")]
        reasoning = "\n\n".join(rs) if rs else None
        return msgs, tools, reasoning, final
    msgs = clean_messages(row.get("messages") or [])
    if msgs:
        # preserve separate source reasoning where possible; do not blindly fuse into visible content
        rs = [m.get("reasoning_content") for m in msgs if m.get("role") == "assistant" and m.get("reasoning_content")]
        reasoning = "\n\n".join(rs) if rs else None
    return msgs, tools, reasoning, final


def license_info(spec: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    rlic = row.get("license")
    if rlic:
        return {"state": "RESOLVED", "labels": [str(rlic).strip()], "row_specific": True, "notes": None}
    labels = list(spec["license"])
    if labels == ["mixed-source"] or labels == ["row-specific"]:
        return {"state": "SEGREGATION_REQUIRED", "labels": labels, "row_specific": False, "notes": "source registry requires row/subset license resolution"}
    return {"state": "RESOLVED", "labels": labels, "row_specific": False, "notes": None}


def make_atom(spec: dict[str, Any], idx: int, row: dict[str, Any]) -> dict[str, Any] | None:
    messages, tools, reasoning, final = messages_from_row(spec["key"], row)
    if len(messages) < 2 or not any(m["role"] == "user" for m in messages) or not any(m["role"] == "assistant" for m in messages):
        return None
    raw = stable_json(row)
    source_row = row.get("uuid") or row.get("id") or row.get("instance_id") or row.get("trajectory_id") or idx
    interaction = infer_interaction(messages, tools, spec["lane"])
    first_user = next((m["content"] for m in messages if m["role"] == "user"), "")
    conv_norm = "\n".join(f"{m['role']}:{normalize_ws(m['content'])}" for m in messages)
    atom_id = htext(f"{spec['repo']}\n{spec['revision']}\n{spec['config']}\n{spec['split']}\n{source_row}\n{htext(raw)}")
    qual_state = "RAW"
    success = None
    reject = []
    if spec["key"] == "openr1":
        cc = int(row.get("correctness_count") or 0)
        success = {"correctness_count": cc, "math_verify": row.get("correctness_math_verify"), "llama_judge": row.get("correctness_llama")}
        if cc >= 2:
            qual_state = "CANDIDATE"
        else:
            reject.append("LOW_OR_UNCLEAR_VERIFIER_SUPPORT")
    elif spec["key"] == "swe":
        success = {"resolved": row.get("resolved"), "repo": row.get("repo")}
        if row.get("resolved") == 1:
            qual_state = "CANDIDATE"
        else:
            reject.append("SWE_NOT_RESOLVED")
    elif spec["key"].startswith("nem_agent"):
        proc = row.get("processing_info") or {}
        success = {"filter_reason": row.get("filter_reason"), "processing_info": proc}
        qual_state = "CANDIDATE" if row.get("filter_reason") in (None, "") else "RAW"
    else:
        qual_state = "CANDIDATE"
    contamination_state = "REVIEW" if spec.get("force_contam_review") else "UNSCREENED"
    return {
        "atom_id": atom_id,
        "source": {
            "repo": spec["repo"], "revision": spec["revision"], "config": spec["config"], "split": spec["split"], "row_id": source_row,
            "source_url": row.get("url"), "upstream_lineage": [str(row.get(x)) for x in ("source", "dataset", "subset", "hf_dataset_name", "repo") if row.get(x)],
            "raw_record_sha256": htext(raw),
        },
        "license": license_info(spec, row),
        "content": {
            "messages": messages,
            "reasoning": reasoning,
            "final_answer": final,
            "tools": tools,
            "observations": [],
            "target_visibility": "TOOL_TRAJECTORY" if interaction in {"TOOL_TRAJECTORY", "RESEARCH_TRAJECTORY"} else ("TARGET_SPECIFIC_RENDER" if reasoning else "ANSWER_ONLY"),
        },
        "capability": {"lanes": spec["lane"], "domains": [str(row.get("domain"))] if row.get("domain") else [], "interaction_shape": interaction, "difficulty": row.get("difficulty"), "composition_required": None},
        "quality": {"state": qual_state, "success_evidence": success, "verifier": None, "teacher_identity": row.get("model"), "objective_check": None, "rejection_reasons": reject},
        "invariants": heuristic_invariants(messages, interaction, spec["lane"], reasoning),
        "contamination": {"state": contamination_state, "exact_fingerprints": [htext(normalize_ws(first_user))], "normalized_fingerprints": [htext(normalize_ws(first_user).lower())], "matched_eval_families": ["SWE-bench family"] if spec.get("force_contam_review") else []},
        "dedup": {"canonical_prompt_hash": htext(normalize_ws(first_user).lower()), "conversation_hash": htext(conv_norm.lower()), "duplicate_of": None, "near_duplicate_cluster": None},
        "tokenization": {"per_target": {}, "destructive_truncation_required": False},
        "admission": {"state": "QUARANTINE", "reason": "pilot normalization only; final license/contamination/invariant/quality filters not yet applied", "review_history": []},
        "pilot": {"char_count": sum(len(m["content"]) for m in messages), "turn_count": len(messages)},
    }


def make_pref(spec: dict[str, Any], idx: int, row: dict[str, Any]) -> dict[str, Any] | None:
    chosen = clean_messages(row.get("chosen") or [])
    rejected = clean_messages(row.get("rejected") or [])
    if not chosen or not rejected:
        return None
    raw = stable_json(row)
    rid = idx
    return {
        "preference_id": htext(f"{spec['repo']}\n{spec['revision']}\n{idx}\n{htext(raw)}"),
        "source": {"repo": spec["repo"], "revision": spec["revision"], "config": spec["config"], "split": spec["split"], "row_id": rid, "raw_record_sha256": htext(raw)},
        "license": {"state": "RESOLVED", "labels": spec["license"], "row_specific": False, "notes": None},
        "chosen": chosen,
        "rejected": rejected,
        "chosen_rating": row.get("chosen_rating"),
        "rejected_rating": row.get("rejected_rating"),
        "chosen_model": row.get("chosen_model"),
        "rejected_model": row.get("rejected_model"),
        "source_label": row.get("source"),
        "admission": {"state": "QUARANTINE", "reason": "preference pilot; never positive SFT by default"},
    }


def iter_rows_with_fallback(spec: dict[str, Any]):
    """Yield (row_idx,row,read_mode) without silently losing source fields.

    If a pinned raw JSONL path is known, stream that exact revision directly. Otherwise prefer pinned
    datasets streaming, then fall back to dataset-server raw rows for pilot-only inspection.
    """
    if spec.get("raw_jsonl"):
        url = hf_hub_url(repo_id=spec["repo"], filename=spec["raw_jsonl"], repo_type="dataset", revision=spec["revision"])
        with requests.get(url, stream=True, timeout=(20, 120)) as r:
            r.raise_for_status()
            for idx, line in enumerate(r.iter_lines(decode_unicode=True)):
                if not line:
                    continue
                yield idx, json.loads(line), "PINNED_RAW_JSONL_STREAM"
        return
    try:
        ds = load_dataset(spec["repo"], spec["config"], split=spec["split"], streaming=True, revision=spec["revision"])
        for idx, row in enumerate(ds):
            yield idx, row, "PINNED_DATASETS_STREAM"
        return
    except Exception:
        base = "https://datasets-server.huggingface.co/rows"
        offset = 0
        page = 100
        while True:
            r = requests.get(base, params={"dataset": spec["repo"], "config": spec["config"], "split": spec["split"], "offset": offset, "length": page}, timeout=45)
            r.raise_for_status()
            payload = r.json()
            rows = payload.get("rows") or []
            if not rows:
                return
            for item in rows:
                yield int(item.get("row_idx", offset)), item.get("row") or {}, "DATASET_SERVER_RAW_FALLBACK"
            offset += len(rows)
            if len(rows) < page:
                return


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(stable_json(r) + "\n")
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        raise SystemExit(f"REFUSE_OVERWRITE {a.out}")
    a.out.mkdir(parents=True)
    rng = random.Random(SEED)
    all_atoms: list[dict[str, Any]] = []
    source_stats = {}
    for spec in SOURCES:
        rows = []
        scanned = 0
        read_modes = Counter()
        error = None
        try:
            for idx, row, read_mode in iter_rows_with_fallback(spec):
                scanned += 1
                read_modes[read_mode] += 1
                atom = make_atom(spec, idx, row)
                if atom is not None:
                    atom["pilot"]["read_mode"] = read_mode
                    rows.append(atom)
                if len(rows) >= spec["n"] or scanned >= max(spec["n"] * 6, 600):
                    break
        except Exception as exc:
            error = repr(exc)
        all_atoms.extend(rows)
        source_stats[spec["key"]] = {"repo": spec["repo"], "split": spec["split"], "requested": spec["n"], "normalized": len(rows), "scanned": scanned, "read_modes": dict(read_modes), "error": error}
        print(spec["key"], len(rows), "/", scanned, 'ERROR='+str(error)[:240] if error else 'OK', flush=True)
    prefs = []
    for idx, row, read_mode in iter_rows_with_fallback(PREFERENCE):
        z = make_pref(PREFERENCE, idx, row)
        if z is not None:
            z["pilot_read_mode"] = read_mode
            prefs.append(z)
        if len(prefs) >= PREFERENCE["n"] or idx >= PREFERENCE["n"] * 3:
            break
    atoms_sha = write_jsonl(a.out / "SFT_QUARANTINE_ATOMS.jsonl", all_atoms)
    prefs_sha = write_jsonl(a.out / "PREFERENCE_QUARANTINE.jsonl", prefs)
    summary = {
        "schema": "cfe.standard-uplift.intake-pilot.v2",
        "status": "NORMALIZATION_PILOT_COMPLETE__NOT_TRAINABLE",
        "seed": SEED,
        "created_unix": time.time(),
        "source_stats": source_stats,
        "sft_atoms": len(all_atoms),
        "preference_atoms": len(prefs),
        "sft_sha256": atoms_sha,
        "preference_sha256": prefs_sha,
        "quality_states": dict(Counter(a["quality"]["state"] for a in all_atoms)),
        "interaction_shapes": dict(Counter(a["capability"]["interaction_shape"] for a in all_atoms)),
        "license_states": dict(Counter(a["license"]["state"] for a in all_atoms)),
        "contamination_states": dict(Counter(a["contamination"]["state"] for a in all_atoms)),
        "cfe_heuristic_tags": dict(Counter(x for a in all_atoms for x in a["invariants"]["cfe"])),
        "lhit_heuristic_tags": dict(Counter(x for a in all_atoms for x in a["invariants"]["lhit"])),
        "lhit_cross_domain_dimensions": dict(Counter(x for a in all_atoms for x in a["invariants"]["lhit_cross_domain"]["candidate_dimensions"])),
        "lhit_domain_families": dict(Counter(x for a in all_atoms for x in a["invariants"]["lhit_cross_domain"]["domain_families"])),
        "lhit_dimension_by_domain": dict(Counter(
            f"{family}::{dim}"
            for a in all_atoms
            for family in a["invariants"]["lhit_cross_domain"]["domain_families"]
            for dim in a["invariants"]["lhit_cross_domain"]["candidate_dimensions"]
        )),
        "laws": [
            "PILOT QUARANTINE != TRAINABLE CORPUS",
            "CFE/LHIT TAG HEURISTIC != VERIFIED INVARIANT",
            "LHIT != MULTI_TURN FORMAT",
            "SINGLE_RECORD EPISODE CAN CARRY CONSEQUENTIAL HISTORY",
            "CROSS_DOMAIN LHIT CANDIDATE != TRAINING ADMISSION",
            "PREFERENCE DATA PHYSICALLY SEPARATE FROM SFT",
            "SWE TRACE QUARANTINE UNTIL EVAL CONTAMINATION CLEARED",
            "SOURCE REVISION PINNED"
        ]
    }
    (a.out / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
