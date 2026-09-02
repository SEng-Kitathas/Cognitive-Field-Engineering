#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

UNKNOWN_FEATURES = {
    "explicit_multi_hypothesis": "UNKNOWN",
    "branch_backtracking": "UNKNOWN",
    "dependency_local_rollback": "UNKNOWN",
    "representation_refinement": "UNKNOWN",
    "external_verification": "UNKNOWN",
    "persistent_state_across_steps": "UNKNOWN",
    "consequence_propagation": "UNKNOWN",
    "learning_from_deliberation": "UNKNOWN",
    "adaptive_reasoning_effort": "UNKNOWN",
    "authority_separation": "UNKNOWN",
    "trace_visibility": "UNKNOWN",
    "trace_faithfulness": "UNKNOWN",
}

ERA_BOUNDS = [
    (1940, 1967, "A_SYMBOLIC_SEARCH_THEOREM_PROVING"),
    (1968, 1979, "B_SCIENTIFIC_INFERENCE_DIALOGUE_EXPERT_SYSTEMS"),
    (1980, 1999, "C_COGNITIVE_ARCHITECTURES_LARGE_SEARCH"),
    (2000, 2021, "D_STATISTICAL_SEARCH_RL_HYBRIDS"),
    (2022, 2023, "E_LLM_INTERMEDIATE_REASONING"),
    (2024, 2100, "F_TRAINED_REASONING_HYBRID_VERIFICATION"),
]

DOCUMENTED_EDGES = [
    {
        "source": "1955_logic_theorist_archive",
        "relation": "DOCUMENTED_ANTECEDENT_OF",
        "target": "1959_gps",
        "evidence": "GPS 1959 explicitly states GPS grew out of Logic Theorist",
        "state": "VERIFIED",
    },
    {
        "source": "2022_chain_of_thought",
        "relation": "METHOD_ANTECEDENT_OF",
        "target": "2022_self_consistency",
        "evidence": "Self-Consistency explicitly extends chain-of-thought decoding by sampling diverse reasoning paths",
        "state": "VERIFIED",
    },
    {
        "source": "2022_chain_of_thought",
        "relation": "METHOD_ANTECEDENT_OF",
        "target": "2023_tree_of_thoughts",
        "evidence": "Tree of Thoughts explicitly generalizes Chain of Thought",
        "state": "VERIFIED",
    },
]


def era_for(year: int) -> str:
    for lo, hi, label in ERA_BOUNDS:
        if lo <= year <= hi:
            return label
    return "UNKNOWN"


def hash_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--raw-manifest", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    raw = {}
    if args.raw_manifest and args.raw_manifest.exists():
        rm = json.loads(args.raw_manifest.read_text(encoding="utf-8"))
        raw = {x["id"]: x for x in rm.get("items", [])}

    nodes = []
    for src in registry["sources"]:
        cache = raw.get(src["id"])
        nodes.append({
            "specimen_id": src["id"],
            "artifact": {
                "title": src["title"],
                "year": src["year"],
                "source_url": src["source_url"],
                "source_state": src["source_state"],
                "rights": src["rights"],
                "raw_policy": src["raw_policy"],
                "local_raw_status": cache.get("status") if cache else None,
                "local_raw_path": cache.get("path") if cache and cache.get("status") != "ERROR" else None,
                "local_raw_sha256": cache.get("sha256") if cache else None,
            },
            "system": {
                "name": src["system"],
                "lineage": src["lineage"],
            },
            "temporal": {
                "year": src["year"],
                "era": era_for(src["year"]),
            },
            "trace_surface": {
                "target": src["trace_target"],
            },
            "silent_questions": src["silent_questions"],
            "planes": {
                "object_state": [],
                "hypothesis_state": [],
                "representation_state": [],
                "control_state": [],
                "authority_state": [],
                "learning_state": [],
            },
            "events": [],
            "relations": [],
            "silent_inferences": [],
            "lbe_composite": {
                "required_capabilities": [],
                "provided_capabilities": [],
                "state_assumptions": [],
                "effects": [],
                "invariants": [],
                "authority_ceiling": "SOURCE_ONLY__NO_STRUCTURAL_PROMOTION",
                "hazards": [],
                "unknowns": ["Full structural annotation pending"],
                "exact_lineage": [src["source_url"]],
            },
            "feature_vector": dict(UNKNOWN_FEATURES),
            "qualification": {
                "state": "SOURCE_ONLY",
                "notes": ["Registry-ingested skeleton; no silent-invariant annotation yet"],
                "reviewed_against_schema": False,
            },
        })

    chronological = sorted(nodes, key=lambda x: (x["temporal"]["year"], x["specimen_id"]))
    edges = list(DOCUMENTED_EDGES)
    for a, b in zip(chronological, chronological[1:]):
        edges.append({
            "source": a["specimen_id"],
            "relation": "HISTORICALLY_PRECEDES",
            "target": b["specimen_id"],
            "state": "VERIFIED_CHRONOLOGY_ONLY",
            "evidence": "source year ordering; no causal implication",
        })

    eras = {}
    for n in chronological:
        eras.setdefault(n["temporal"]["era"], []).append(n["specimen_id"])

    out = {
        "schema": "cfe.reasoning-archaeology.lbe-field.v1",
        "status": "SOURCE_FIELD_SKELETON__ANNOTATION_PENDING",
        "source_registry_sha256": hash_file(args.registry),
        "raw_manifest_sha256": hash_file(args.raw_manifest) if args.raw_manifest and args.raw_manifest.exists() else None,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "eras": eras,
        "nodes": nodes,
        "edges": edges,
        "laws": [
            "CHRONOLOGY != CAUSATION",
            "FUNCTIONAL RECURRENCE != DOCUMENTED LINEAGE",
            "UNKNOWN FEATURE != ABSENT FEATURE",
            "SOURCE FIELD SKELETON != ANNOTATED LBE",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": out["status"], "nodes": len(nodes), "edges": len(edges), "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
