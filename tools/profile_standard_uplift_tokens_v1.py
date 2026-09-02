#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import statistics
from pathlib import Path

from transformers import AutoTokenizer


def q(vals, p):
    s = sorted(vals)
    return s[int(p * (len(s) - 1))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atoms", type=Path, required=True)
    ap.add_argument("--tokenizer", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(str(a.tokenizer), local_files_only=True, trust_remote_code=False)
    rows = []
    with a.atoms.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    per = []
    by = collections.defaultdict(lambda: {"rows": 0, "total": 0, "assistant": 0, "tv": [], "av": []})
    for atom in rows:
        total = 0
        assistant = 0
        for m in atom["content"]["messages"]:
            c = m.get("content") or ""
            n = len(tok.encode(c, add_special_tokens=False))
            total += n
            if m.get("role") == "assistant":
                assistant += n
                rc = m.get("reasoning_content") or ""
                if rc:
                    nr = len(tok.encode(rc, add_special_tokens=False))
                    total += nr
                    assistant += nr
        tools = atom["content"].get("tools") or []
        if tools:
            total += len(tok.encode(json.dumps(tools, ensure_ascii=False, separators=(",", ":")), add_special_tokens=False))
        src = atom["source"]["repo"] + "::" + atom["source"]["split"]
        d = by[src]
        d["rows"] += 1
        d["total"] += total
        d["assistant"] += assistant
        d["tv"].append(total)
        d["av"].append(assistant)
        per.append((total, assistant, src, atom["atom_id"]))

    total_vals = [x[0] for x in per]
    assistant_vals = [x[1] for x in per]
    summary = {
        "schema": "cfe.standard-uplift.token-profile.v1",
        "tokenizer_path": str(a.tokenizer.resolve()),
        "tokenizer_class": tok.__class__.__name__,
        "rows": len(rows),
        "total_context_tokens_sum": sum(total_vals),
        "assistant_target_tokens_sum": sum(assistant_vals),
        "total_context": {
            "median": statistics.median(total_vals),
            "p90": q(total_vals, .90),
            "p95": q(total_vals, .95),
            "p99": q(total_vals, .99),
            "max": max(total_vals),
        },
        "assistant_target": {
            "median": statistics.median(assistant_vals),
            "p90": q(assistant_vals, .90),
            "p95": q(assistant_vals, .95),
            "p99": q(assistant_vals, .99),
            "max": max(assistant_vals),
        },
        "over_context": {},
        "sources": {},
    }
    for lim in [2048, 4096, 8192, 16384, 32768, 65536]:
        over = sum(1 for x in total_vals if x > lim)
        summary["over_context"][str(lim)] = {"rows": over, "fraction": over / len(total_vals)}
    for src, d in by.items():
        summary["sources"][src] = {
            "rows": d["rows"],
            "total_context_tokens": d["total"],
            "assistant_target_tokens": d["assistant"],
            "median_total": statistics.median(d["tv"]),
            "p90_total": q(d["tv"], .90),
            "max_total": max(d["tv"]),
            "median_assistant": statistics.median(d["av"]),
            "p90_assistant": q(d["av"], .90),
            "max_assistant": max(d["av"]),
        }
    summary["largest_atoms"] = [
        {"total_tokens": t, "assistant_tokens": at, "source": src, "atom_id": aid}
        for t, at, src, aid in sorted(per, reverse=True)[:20]
    ]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
