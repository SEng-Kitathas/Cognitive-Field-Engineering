from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def extract_last_json(text: str) -> dict | None:
    text = text.strip()
    if not text:
        return None
    # Runner emits one pretty-printed JSON object on normal audit/step completion.
    starts = [i for i, ch in enumerate(text) if ch == "{"]
    for i in reversed(starts):
        try:
            obj = json.loads(text[i:])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


def run_runner(cmd: list[str], cwd: Path, execute: bool) -> tuple[int, str, str, dict | None]:
    argv = [*cmd, *( ["--execute"] if execute else [] )]
    cp = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, errors="replace")
    obj = extract_last_json(cp.stdout)
    return cp.returncode, cp.stdout, cp.stderr, obj


def emit(event: str, **fields) -> None:
    rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "event": event, **fields}
    print(json.dumps(rec, separators=(",", ":")), flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Drive CFE v1.0 recovery runner until a real blocker or Stage-2 terminal state.")
    ap.add_argument("--run-root", type=Path, required=True)
    ap.add_argument("--live-root", type=Path, required=True)
    ap.add_argument("--qualified-python", type=Path, required=True)
    ap.add_argument("--runner", type=Path, default=Path(__file__).with_name("resume_v10_first_screen.py"))
    ap.add_argument("--max-steps", type=int, default=32)
    ap.add_argument("--audit-only", action="store_true")
    a = ap.parse_args()

    cwd = Path(__file__).resolve().parents[1]
    cmd = [
        str(a.qualified_python), str(a.runner.resolve()),
        "--run-root", str(a.run_root),
        "--live-root", str(a.live_root),
        "--python", str(a.qualified_python),
    ]

    step_count = 0
    while step_count < a.max_steps:
        rc, out, err, audit = run_runner(cmd, cwd, execute=False)
        emit("AUDIT", step=step_count, rc=rc, state=audit, stderr_tail=err[-2000:])
        if rc != 0 or audit is None:
            emit("BLOCKER", reason="audit_failed_or_unparseable", rc=rc, stdout_tail=out[-5000:], stderr_tail=err[-5000:])
            return rc or 20

        status = audit.get("status")
        if status == "BLOCKED":
            emit("BLOCKER", reason=audit.get("reason"), state=audit)
            return 21
        if status in {"STAGE2_COMPLETE__NO_FURTHER_ADAPTIVE_EXTENSION", "STAGE1_COMPLETE__PREREG_STOP"}:
            emit("TERMINAL", state=audit, steps_executed=step_count)
            return 0
        if status != "READY":
            emit("BLOCKER", reason="unexpected_audit_state", state=audit)
            return 22
        if a.audit_only:
            emit("AUDIT_ONLY_COMPLETE", state=audit)
            return 0

        next_step = audit.get("next_step")
        seed = audit.get("seed")
        arm = audit.get("arm")
        emit("EXECUTE_START", step=step_count + 1, next_step=next_step, seed=seed, arm=arm)
        rc, out, err, result = run_runner(cmd, cwd, execute=True)
        emit("EXECUTE_END", step=step_count + 1, rc=rc, state=result, stdout_tail=out[-6000:], stderr_tail=err[-4000:])
        if rc != 0 or result is None:
            emit("BLOCKER", reason="execution_failed_or_unparseable", rc=rc, stdout_tail=out[-8000:], stderr_tail=err[-8000:])
            return rc or 23
        if result.get("status") == "BLOCKED":
            emit("BLOCKER", reason=result.get("reason"), state=result)
            return 24
        if result.get("status") != "ONE_STEP_COMPLETE":
            emit("BLOCKER", reason="unexpected_execution_state", state=result)
            return 25
        step_count += 1

    emit("BLOCKER", reason="max_steps_guard_reached", max_steps=a.max_steps)
    return 26


if __name__ == "__main__":
    raise SystemExit(main())
