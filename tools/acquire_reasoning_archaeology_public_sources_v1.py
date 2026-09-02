#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import requests

SOURCES = [
    {
        "id": "1959_gps",
        "url": "https://iiif.library.cmu.edu/file/Newell_box00039_fld03042_doc0001/Newell_box00039_fld03042_doc0001.pdf",
        "filename": "1959_GPS_A_General_Problem_Solving_Program.pdf",
    },
    {
        "id": "1959_advice_taker",
        "url": "https://logic.stanford.edu/logicprogramming/readings/mccarthy.pdf",
        "filename": "1959_McCarthy_Programs_With_Common_Sense.pdf",
    },
    {
        "id": "1985_soar_chunking",
        "url": "https://iiif.library.cmu.edu/file/Newell_box00016_fld01156_doc0001/Newell_box00016_fld01156_doc0001.pdf",
        "filename": "1985_Chunking_in_Soar.pdf",
    },
    {
        "id": "2022_chain_of_thought",
        "url": "https://arxiv.org/pdf/2201.11903",
        "filename": "2022_Chain_of_Thought_Prompting.pdf",
    },
    {
        "id": "2022_self_consistency",
        "url": "https://arxiv.org/pdf/2203.11171",
        "filename": "2022_Self_Consistency.pdf",
    },
    {
        "id": "2022_star",
        "url": "https://arxiv.org/pdf/2203.14465",
        "filename": "2022_STaR.pdf",
    },
    {
        "id": "2022_react",
        "url": "https://arxiv.org/pdf/2210.03629",
        "filename": "2022_ReAct.pdf",
    },
    {
        "id": "2023_reflexion",
        "url": "https://arxiv.org/pdf/2303.11366",
        "filename": "2023_Reflexion.pdf",
    },
    {
        "id": "2023_tree_of_thoughts",
        "url": "https://arxiv.org/pdf/2305.10601",
        "filename": "2023_Tree_of_Thoughts.pdf",
    },
    {
        "id": "2023_prm800k",
        "url": "https://arxiv.org/pdf/2305.20050",
        "filename": "2023_Lets_Verify_Step_by_Step.pdf",
    },
    {
        "id": "2025_deepseek_r1",
        "url": "https://arxiv.org/pdf/2501.12948",
        "filename": "2025_DeepSeek_R1.pdf",
    },
    {
        "id": "2025_qwen3",
        "url": "https://arxiv.org/pdf/2505.09388",
        "filename": "2025_Qwen3_Technical_Report.pdf",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "CFE-Reasoning-Archaeology/1.0 research-cache"})
    results = []
    for src in SOURCES:
        dst = args.out / src["filename"]
        rec = {"id": src["id"], "url": src["url"], "path": str(dst), "status": None}
        try:
            if dst.exists() and dst.stat().st_size > 0:
                rec.update({
                    "status": "EXISTING_VERIFIED",
                    "bytes": dst.stat().st_size,
                    "sha256": sha256_file(dst),
                })
            else:
                with session.get(src["url"], stream=True, timeout=(20, 180), allow_redirects=True) as r:
                    r.raise_for_status()
                    ctype = r.headers.get("content-type")
                    tmp = dst.with_suffix(dst.suffix + ".part")
                    with tmp.open("wb") as f:
                        for chunk in r.iter_content(1024 * 1024):
                            if chunk:
                                f.write(chunk)
                    tmp.replace(dst)
                    rec.update({
                        "status": "DOWNLOADED_VERIFIED",
                        "bytes": dst.stat().st_size,
                        "sha256": sha256_file(dst),
                        "content_type": ctype,
                        "final_url": r.url,
                    })
        except Exception as exc:
            rec.update({"status": "ERROR", "error": repr(exc)})
            part = dst.with_suffix(dst.suffix + ".part")
            if part.exists():
                part.unlink()
        results.append(rec)
        print(json.dumps(rec, sort_keys=True), flush=True)

    manifest = {
        "schema": "cfe.reasoning-archaeology.raw-cache-manifest.v1",
        "created_unix": time.time(),
        "raw_cache_policy": "LOCAL_RESEARCH_CACHE_NOT_FOR_GIT_PUBLICATION",
        "count": len(results),
        "success": sum(r["status"] in {"DOWNLOADED_VERIFIED", "EXISTING_VERIFIED"} for r in results),
        "errors": sum(r["status"] == "ERROR" for r in results),
        "items": results,
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"manifest": str(args.manifest), "success": manifest["success"], "errors": manifest["errors"]}, indent=2))


if __name__ == "__main__":
    main()
