#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def ps_json(script: str):
    cp = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        errors="replace",
        timeout=20,
    )
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr[-2000:])
    s = cp.stdout.strip()
    return json.loads(s) if s else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, required=True)
    ap.add_argument("--class", dest="run_class", choices=["HEAVY_MODEL", "GPU_TRAIN", "LIGHT_MODEL", "READ_ONLY"], required=True)
    ap.add_argument("--expected-vram-mib", type=int, default=0)
    ap.add_argument("--expected-ram-gb", type=float, default=0)
    ap.add_argument("--port", type=int)
    ap.add_argument("--owned-pid", type=int, action="append", default=[])
    ap.add_argument("--min-free-vram-margin-mib", type=int, default=512)
    ap.add_argument("--min-free-ram-margin-gb", type=float, default=4.0)
    a = ap.parse_args()

    procs = ps_json(
        "$x=Get-CimInstance Win32_Process | "
        "Where-Object {"
        "$_.Name -match '^(llama-server|llama-cli|ollama|koboldcpp|lmstudio|vllm).*' "
        "-or ($_.Name -match '^python(w)?\\.exe$' -and $_.CommandLine -match '(vllm|text-generation|model[_-]server|train[_-]|evaluate[_-]|transformers.*from_pretrained)')"
        "} | Select-Object ProcessId,Name,ExecutablePath,CommandLine; @($x)|ConvertTo-Json -Depth 4"
    ) or []
    if isinstance(procs, dict):
        procs = [procs]

    listeners = ps_json(
        "$x=Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | "
        "Select-Object LocalAddress,LocalPort,OwningProcess; @($x)|ConvertTo-Json -Depth 3"
    ) or []
    if isinstance(listeners, dict):
        listeners = [listeners]

    mem = ps_json(
        "$o=Get-CimInstance Win32_OperatingSystem; "
        "[pscustomobject]@{total_gb=[math]::Round($o.TotalVisibleMemorySize*1KB/1GB,3);"
        "free_gb=[math]::Round($o.FreePhysicalMemory*1KB/1GB,3)}|ConvertTo-Json"
    )

    cp = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=memory.total,memory.used,memory.free,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    gpu = None
    if cp.returncode == 0 and cp.stdout.strip():
        vals = [x.strip() for x in cp.stdout.strip().splitlines()[0].split(",")]
        gpu = {
            "total_mib": int(vals[0]),
            "used_mib": int(vals[1]),
            "free_mib": int(vals[2]),
            "util_pct": int(vals[3]),
        }

    owned = set(a.owned_pid)
    foreign = []
    for p in procs:
        pid = int(p.get("ProcessId") or 0)
        if pid and pid not in owned:
            foreign.append(p)

    conflicts = []
    if a.port is not None:
        for l in listeners:
            if int(l.get("LocalPort") or -1) == a.port and int(l.get("OwningProcess") or 0) not in owned:
                conflicts.append({"kind": "PORT_OWNED", "port": a.port, "pid": int(l.get("OwningProcess") or 0)})

    if a.run_class in ("HEAVY_MODEL", "GPU_TRAIN") and foreign:
        conflicts.append({"kind": "FOREIGN_MODEL_RUNTIME_ACTIVE", "processes": foreign})

    if a.expected_ram_gb and mem and mem["free_gb"] < a.expected_ram_gb + a.min_free_ram_margin_gb:
        conflicts.append(
            {
                "kind": "RAM_HEADROOM",
                "free_gb": mem["free_gb"],
                "needed_plus_margin_gb": a.expected_ram_gb + a.min_free_ram_margin_gb,
            }
        )

    if a.expected_vram_mib:
        if gpu is None:
            conflicts.append({"kind": "GPU_UNAVAILABLE"})
        elif gpu["free_mib"] < a.expected_vram_mib + a.min_free_vram_margin_mib:
            conflicts.append(
                {
                    "kind": "VRAM_HEADROOM",
                    "free_mib": gpu["free_mib"],
                    "needed_plus_margin_mib": a.expected_vram_mib + a.min_free_vram_margin_mib,
                }
            )

    out = {
        "schema": "cfe.resource-authority-guard.v1",
        "status": "PASS" if not conflicts else "BLOCKED",
        "run_class": a.run_class,
        "project_root": str(a.project_root.resolve()),
        "owned_pids": sorted(owned),
        "foreign_model_processes": foreign,
        "memory": mem,
        "gpu": gpu,
        "requested_port": a.port,
        "conflicts": conflicts,
        "laws": [
            "RESOURCE_AVAILABILITY != RESOURCE_AUTHORITY",
            "PID_OWNERSHIP_REQUIRED_FOR_TERMINATION",
            "FOREIGN_MODEL_RUNTIME_BLOCKS_HEAVY_CFE_RUN_BY_DEFAULT",
        ],
    }
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if not conflicts else 23)


if __name__ == "__main__":
    main()
