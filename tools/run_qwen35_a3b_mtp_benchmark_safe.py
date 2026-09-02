#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROMPTS = [
    "A software system caches authorization decisions. A dependency changes after the cache entry was created. Explain the safest design for deciding whether the cached authorization may still be used, and identify the invariant that matters most.",
    "A training experiment improves primitive classification but zero-shot composition remains unchanged. Give the strongest causal interpretation, the main confounders, and the next discriminator without pretending the null transfer proves composition is impossible.",
    "Write a compact Python design for an append-only evidence ledger where later corrections supersede earlier claims without deleting them. Explain the integrity invariant before showing code structure.",
    "An autonomous research loop begins with a question about developmental geometry, then gradually drifts into hash functions and random-number generation while each individual step still looks locally plausible. Diagnose the mechanism-level failure and propose the smallest control change that would distinguish useful exploration from semantic basin capture."
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(64 * 1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def dumpj(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run_guard(root: Path, port: int, expected_vram_mib: int, expected_ram_gb: float, owned_pid: int | None = None):
    cmd = [
        sys.executable,
        str(root / "tools" / "cfe_resource_authority_guard.py"),
        "--project-root", str(root),
        "--class", "HEAVY_MODEL",
        "--expected-vram-mib", str(expected_vram_mib),
        "--expected-ram-gb", str(expected_ram_gb),
        "--min-free-vram-margin-mib", "256",
        "--port", str(port),
    ]
    if owned_pid is not None:
        cmd += ["--owned-pid", str(owned_pid)]
    cp = subprocess.run(cmd, cwd=root, capture_output=True, text=True, errors="replace", timeout=30)
    try:
        data = json.loads(cp.stdout)
    except Exception:
        data = {"status": "ERROR", "stdout": cp.stdout[-5000:], "stderr": cp.stderr[-5000:], "return_code": cp.returncode}
    return cp.returncode, data


def health(port: int, timeout_s: float = 240.0):
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as r:
                data = json.loads(r.read().decode("utf-8"))
                if data.get("status") == "ok":
                    return data
                last = data
        except Exception as e:
            last = repr(e)
        time.sleep(2)
    raise RuntimeError(f"SERVER_HEALTH_TIMEOUT port={port} last={last!r}")


def complete(port: int, prompt: str):
    body = json.dumps({
        "prompt": prompt,
        "n_predict": 128,
        "temperature": 0,
        "seed": 20260902,
        "stream": False,
        "cache_prompt": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/completion",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.loads(r.read().decode("utf-8"))
    elapsed = time.time() - t0
    content = data.get("content", "")
    timings = data.get("timings") or {}
    return {
        "elapsed_s": elapsed,
        "tokens_predicted": data.get("tokens_predicted"),
        "tokens_evaluated": data.get("tokens_evaluated"),
        "predicted_per_second": timings.get("predicted_per_second"),
        "prompt_per_second": timings.get("prompt_per_second"),
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content": content,
    }


def stop_owned(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=15)


def phase(root: Path, runtime: Path, target: Path, mtp: Path | None, out: Path, name: str, port: int, expected_vram: int):
    rc, gate = run_guard(root, port, expected_vram, 18.0)
    dumpj(out / name / "PRELAUNCH_RESOURCE_GATE.json", gate)
    if rc != 0:
        raise RuntimeError(f"RESOURCE_GATE_BLOCKED phase={name}")

    cmd = [
        str(runtime),
        "-m", str(target),
        "-c", "4096",
        "-ngl", "auto",
        "-fa", "on",
        "--host", "127.0.0.1",
        "--port", str(port),
        "--parallel", "1",
        "--cache-ram", "0",
        "-lv", "4",
    ]
    if mtp is not None:
        cmd += [
            "--spec-type", "draft-mtp",
            "--spec-draft-model", str(mtp),
            "--spec-draft-ngl", "auto",
            "--spec-draft-n-max", "3",
        ]

    pd = out / name
    pd.mkdir(parents=True, exist_ok=True)
    so = (pd / "server.stdout.log").open("w", encoding="utf-8", newline="\n")
    se = (pd / "server.stderr.log").open("w", encoding="utf-8", newline="\n")
    proc = subprocess.Popen(cmd, cwd=runtime.parent, stdout=so, stderr=se, text=True)
    try:
        health(port)
        rc2, gate2 = run_guard(root, port, expected_vram, 18.0, owned_pid=proc.pid)
        dumpj(pd / "POSTLAUNCH_RESOURCE_GATE.json", gate2)
        if rc2 != 0:
            raise RuntimeError(f"RESOURCE_GATE_CHANGED_AFTER_LAUNCH phase={name}")
        rows = []
        for i, prompt in enumerate(PROMPTS):
            row = complete(port, prompt)
            row["prompt_index"] = i
            row["prompt_sha256"] = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            rows.append(row)
        speeds = [r["predicted_per_second"] for r in rows if isinstance(r.get("predicted_per_second"), (int, float))]
        result = {
            "phase": name,
            "pid": proc.pid,
            "port": port,
            "speculation": "draft-mtp" if mtp is not None else "none",
            "rows": rows,
            "mean_predicted_tokens_per_s": sum(speeds) / len(speeds) if speeds else None,
            "command": cmd,
        }
        dumpj(pd / "RESULT.json", result)
        return result
    finally:
        stop_owned(proc)
        so.close()
        se.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--mtp", type=Path, required=True)
    ap.add_argument("--runtime", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--preflight-only", action="store_true")
    a = ap.parse_args()
    root = a.project_root.resolve()
    target, mtp, runtime = a.target.resolve(), a.mtp.resolve(), a.runtime.resolve()
    for p in (target, mtp, runtime):
        if not p.is_file():
            raise SystemExit(f"MISSING_REQUIRED_FILE {p}")
    if sha256_file(target) != "d1ed134b54a8509a6dc773d30d7eadb70b59bc2e5d010ee2fd40c4cb02b24992":
        raise SystemExit("TARGET_SHA_MISMATCH")
    if mtp.stat().st_size != 1990649856 or sha256_file(mtp) != "54f372d7ce6625a9cf66e296f9da7b2786efdb12a2ec3c957cdfec3ff6d36ed7":
        raise SystemExit("MTP_IDENTITY_MISMATCH")

    if a.preflight_only:
        checks = {}
        for name, port, vram in [("TARGET_ONLY", 18226, 3500), ("MTP_Q8", 18227, 5000)]:
            rc, data = run_guard(root, port, vram, 18.0)
            checks[name] = {"return_code": rc, "gate": data}
        print(json.dumps(checks, indent=2))
        raise SystemExit(0 if all(x["return_code"] == 0 for x in checks.values()) else 23)

    if a.out.exists():
        raise SystemExit(f"REFUSE_OVERWRITE {a.out}")
    a.out.mkdir(parents=True)
    receipt = {
        "schema": "cfe.qwen35-a3b-mtp-benchmark.v1",
        "status": "RUNNING",
        "target_sha256": sha256_file(target),
        "mtp_sha256": sha256_file(mtp),
        "runtime": str(runtime),
        "phases": [],
    }
    dumpj(a.out / "RECEIPT.json", receipt)
    try:
        base = phase(root, runtime, target, None, a.out, "TARGET_ONLY", 18226, 3500)
        receipt["phases"].append(base)
        dumpj(a.out / "RECEIPT.json", receipt)
        mtpr = phase(root, runtime, target, mtp, a.out, "MTP_Q8", 18227, 5000)
        receipt["phases"].append(mtpr)
        b = base.get("mean_predicted_tokens_per_s")
        m = mtpr.get("mean_predicted_tokens_per_s")
        receipt["status"] = "COMPLETE"
        receipt["mean_speedup_ratio"] = (m / b) if b and m else None
        dumpj(a.out / "RECEIPT.json", receipt)
        print(json.dumps(receipt, indent=2))
    except Exception as e:
        receipt["status"] = "FAILED_OR_BLOCKED"
        receipt["error"] = repr(e)
        dumpj(a.out / "RECEIPT.json", receipt)
        raise


if __name__ == "__main__":
    main()
