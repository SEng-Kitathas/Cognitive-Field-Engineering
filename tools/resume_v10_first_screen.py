from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

CONTROL = "CONTROL_STRICT_CELL_SCRAMBLE"
TREATMENT = "TREATMENT_NEIGHBORHOOD"
DEFAULT_LIVE = Path(r"C:\Users\ancal\ProtoAGI\CFE\CFE_RND_V1_0_PREEXECUTION")
DEFAULT_PYTHON = Path(r"C:\Users\ancal\ProtoAGI\CFE\.venv_cuda\Scripts\python.exe")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fail(msg: str, code: int = 2):
    print(json.dumps({"status": "BLOCKED", "reason": msg}, indent=2))
    raise SystemExit(code)


def verify_adapter(train_dir: Path, run: dict) -> list[str]:
    failures = []
    adapter = train_dir / "adapter"
    for rel, meta in run.get("adapter_files", {}).items():
        p = adapter / rel
        if not p.is_file():
            failures.append(f"missing adapter file {p}")
            continue
        if p.stat().st_size != meta.get("bytes"):
            failures.append(f"adapter byte mismatch {p}")
        if sha256_file(p) != meta.get("sha256"):
            failures.append(f"adapter hash mismatch {p}")
    return failures


def verify_train(train_dir: Path, seed: int, arm: str, static_sha: str, host_sha: str, profile_sha: str, expected_steps: int) -> list[str]:
    rp = train_dir / "RUN_MANIFEST.json"
    if not rp.is_file():
        return [f"missing run manifest {rp}"]
    r = load_json(rp)
    failures = []
    if r.get("arm") != arm or int(r.get("seed", -1)) != int(seed):
        failures.append(f"run identity mismatch {rp}")
    if r.get("static_input_lock_sha256") != static_sha:
        failures.append(f"static lock mismatch {rp}")
    if r.get("host_lock_sha256") != host_sha:
        failures.append(f"host lock mismatch {rp}")
    if r.get("profile_lock_sha256") != profile_sha:
        failures.append(f"profile lock mismatch {rp}")
    if int(r.get("global_step", -1)) != int(expected_steps):
        failures.append(f"global step mismatch {rp}")
    failures.extend(verify_adapter(train_dir, r))
    return failures


def verify_eval(eval_dir: Path, train_manifest: Path | None, static_sha: str, host_sha: str) -> list[str]:
    mp = eval_dir / "EVAL_MANIFEST.json"
    rp = eval_dir / "RESULTS.jsonl"
    failures = []
    if not mp.is_file():
        failures.append(f"missing eval manifest {mp}")
        return failures
    if not rp.is_file():
        failures.append(f"missing eval results {rp}")
        return failures
    m = load_json(mp)
    if m.get("results_sha256") != sha256_file(rp):
        failures.append(f"eval results hash mismatch {eval_dir}")
    if m.get("static_input_lock_sha256") != static_sha:
        failures.append(f"eval static lock mismatch {eval_dir}")
    if m.get("host_lock_sha256") != host_sha:
        failures.append(f"eval host lock mismatch {eval_dir}")
    if train_manifest is None:
        if m.get("adapter") is not None or m.get("producer_run_manifest_sha256") is not None:
            failures.append(f"NF4 base unexpectedly bound to adapter {eval_dir}")
    else:
        if m.get("producer_run_manifest_sha256") != sha256_file(train_manifest):
            failures.append(f"eval producer mismatch {eval_dir}")
    return failures


def run_step(python: Path, live: Path, run_root: Path, name: str, args: list[str]) -> None:
    logs = run_root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    log = logs / f"resume_{stamp}_{name}.log"
    cmd = [str(python), *args]
    print(f"RUN {name}: {cmd}", flush=True)
    cp = subprocess.run(cmd, cwd=str(live), capture_output=True, text=True, errors="replace")
    log.write_text(
        "COMMAND=" + repr(cmd) + "\n"
        + f"RETURN_CODE={cp.returncode}\n\nSTDOUT\n{cp.stdout}\nSTDERR\n{cp.stderr}",
        encoding="utf-8",
        newline="\n",
    )
    receipt = run_root / "RESUME_STEP_RECEIPTS.jsonl"
    rec = {
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "step": name,
        "command": cmd,
        "return_code": cp.returncode,
        "log": str(log.relative_to(run_root)),
        "log_sha256": sha256_file(log),
    }
    with receipt.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, separators=(",", ":")) + "\n")
    print(f"DONE {name}: rc={cp.returncode} log={log}", flush=True)
    if cp.returncode != 0:
        fail(f"step {name} failed rc={cp.returncode}; see {log}", cp.returncode)


def stage1_sequence(contract: dict):
    order = contract["execution_order"]
    for seed in contract["seeds"]:
        for arm in order[str(seed)]:
            yield int(seed), arm


def stage2_sequence(prereg: dict):
    order = prereg["stage2_if_triggered"]["execution_order"]
    for seed in prereg["stage2_if_triggered"]["seeds"]:
        for arm in order[str(seed)]:
            yield int(seed), arm


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail-closed recovery runner for an existing CFE v1.0 first-screen run root.")
    ap.add_argument("--run-root", type=Path, required=True)
    ap.add_argument("--live-root", type=Path, default=DEFAULT_LIVE)
    ap.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    ap.add_argument("--execute", action="store_true", help="Execute exactly one missing lawful step, verify it, then return. Without this flag, audit only.")
    a = ap.parse_args()

    live = a.live_root.resolve()
    run_root = a.run_root.resolve()
    python = a.python.resolve()
    exp = live / "experiments" / "first_screen_v09"
    lock = live / "design" / "CFE_V10_FIRST_SCREEN_INPUT_LOCK.json"
    host = run_root / "host" / "HOST_LOCK.json"
    profile = run_root / "profile" / "PROFILE_LOCK.json"
    repeat = run_root / "repeatability" / "REPEATABILITY_QUALIFICATION.json"
    base_eval = run_root / "eval" / "NF4_BASE"

    for p, label in [(live, "live root"), (run_root, "run root"), (python, "qualified python"), (lock, "input lock"), (host, "host lock"), (profile, "profile lock"), (repeat, "repeatability qualification")]:
        if not p.exists():
            fail(f"missing {label}: {p}")

    contract = load_json(exp / "training_contract.json")
    prereg = load_json(exp / "SEED_EXTENSION_PREREGISTRATION_V10.json")
    static_sha = sha256_file(lock)
    host_sha = sha256_file(host)
    profile_sha = sha256_file(profile)
    host_obj = load_json(host)
    profile_obj = load_json(profile)
    repeat_obj = load_json(repeat)

    if host_obj.get("input_lock_sha256") != static_sha:
        fail("host lock does not bind current static input lock")
    if profile_obj.get("input_lock_sha256") != static_sha or profile_obj.get("host_lock_sha256") != host_sha:
        fail("profile lock binding mismatch")
    if repeat_obj.get("status") != "REPEATABILITY_PASS" or repeat_obj.get("mismatches") not in ({}, None):
        fail("repeatability qualification is not a clean pass")

    base_failures = verify_eval(base_eval, None, static_sha, host_sha)
    if base_failures:
        fail("NF4 base evaluation is incomplete/corrupt: " + "; ".join(base_failures))

    expected_steps = int(contract["sequence"]["expected_optimizer_steps"])
    audit = []

    # Stage 1: exact preregistered order. Existing partial directories are a hard stop.
    for seed, arm in stage1_sequence(contract):
        train = run_root / "train" / str(seed) / arm
        ev = run_root / "eval" / str(seed) / arm
        tm = train / "RUN_MANIFEST.json"
        em = ev / "EVAL_MANIFEST.json"

        if train.exists() and not tm.is_file():
            fail(f"partial train output exists without RUN_MANIFEST: seed={seed} arm={arm} path={train}")
        if train.exists():
            fs = verify_train(train, seed, arm, static_sha, host_sha, profile_sha, expected_steps)
            if fs:
                fail("completed train failed verification: " + "; ".join(fs))
            audit.append({"seed": seed, "arm": arm, "train": "VERIFIED"})
        else:
            if ev.exists():
                fail(f"eval exists before train output: seed={seed} arm={arm}")
            if not a.execute:
                print(json.dumps({"status": "READY", "next_step": "TRAIN", "seed": seed, "arm": arm, "audit": audit}, indent=2))
                return 0
            run_step(python, live, run_root, f"train_{seed}_{arm}", [
                str(exp / "train_first_screen_v09.py"), "--arm", arm, "--seed", str(seed),
                "--host-lock", str(host), "--profile-lock", str(profile), "--out", str(train), "--lock", str(lock)
            ])
            fs = verify_train(train, seed, arm, static_sha, host_sha, profile_sha, expected_steps)
            if fs:
                fail("new train output failed verification: " + "; ".join(fs))
            audit.append({"seed": seed, "arm": arm, "train": "EXECUTED_AND_VERIFIED"})
            print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "TRAIN", "seed": seed, "arm": arm, "audit": audit}, indent=2))
            return 0

        if ev.exists() and not em.is_file():
            fail(f"partial eval output exists without EVAL_MANIFEST: seed={seed} arm={arm} path={ev}")
        if ev.exists():
            fs = verify_eval(ev, tm, static_sha, host_sha)
            if fs:
                fail("completed eval failed verification: " + "; ".join(fs))
            audit[-1]["eval"] = "VERIFIED"
        else:
            if not a.execute:
                print(json.dumps({"status": "READY", "next_step": "EVAL", "seed": seed, "arm": arm, "audit": audit}, indent=2))
                return 0
            run_step(python, live, run_root, f"eval_{seed}_{arm}", [
                str(exp / "evaluate_first_screen_v09.py"), "--host-lock", str(host),
                "--adapter", str(train / "adapter"), "--run-manifest", str(tm),
                "--label", f"{arm}_SEED_{seed}", "--out", str(ev), "--lock", str(lock)
            ])
            fs = verify_eval(ev, tm, static_sha, host_sha)
            if fs:
                fail("new eval output failed verification: " + "; ".join(fs))
            audit[-1]["eval"] = "EXECUTED_AND_VERIFIED"
            print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "EVAL", "seed": seed, "arm": arm, "audit": audit}, indent=2))
            return 0

    # Stage 1 qualification / analysis / deterministic extension decision.
    qual = run_root / "EXECUTION_QUALIFICATION.json"
    if not qual.exists():
        if not a.execute:
            print(json.dumps({"status": "READY", "next_step": "QUALIFY_STAGE1", "audit": audit}, indent=2))
            return 0
        run_step(python, live, run_root, "90_qualify", [str(exp / "qualify_executed_first_screen_v09.py"), "--run-root", str(run_root), "--lock", str(lock)])
        print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "QUALIFY_STAGE1"}, indent=2))
        return 0
    q = load_json(qual)
    if not str(q.get("status", "")).startswith("EXECUTION_INTEGRITY_PASS"):
        fail(f"stage1 qualification not pass: {q.get('status')}")

    analysis = run_root / "SCIENTIFIC_ANALYSIS.json"
    if not analysis.exists():
        if not a.execute:
            print(json.dumps({"status": "READY", "next_step": "ANALYZE_STAGE1", "audit": audit}, indent=2))
            return 0
        run_step(python, live, run_root, "91_analyze", [str(exp / "analyze_scientific_effect_v09.py"), "--run-root", str(run_root)])
        print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "ANALYZE_STAGE1"}, indent=2))
        return 0

    decision = run_root / "SEED_EXTENSION_DECISION.json"
    if not decision.exists():
        if not a.execute:
            print(json.dumps({"status": "READY", "next_step": "DECIDE_EXTENSION", "audit": audit}, indent=2))
            return 0
        run_step(python, live, run_root, "92_seed_extension_decision", [str(exp / "decide_seed_extension_v10.py"), "--run-root", str(run_root)])
        print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "DECIDE_EXTENSION"}, indent=2))
        return 0
    d = load_json(decision)
    if d.get("preregistration_sha256") != sha256_file(exp / "SEED_EXTENSION_PREREGISTRATION_V10.json"):
        fail("extension decision preregistration hash mismatch")

    if d.get("decision") == "STOP_STAGE1_DIRECTIONALLY_CONSISTENT":
        print(json.dumps({"status": "STAGE1_COMPLETE__PREREG_STOP", "decision": d, "audit": audit}, indent=2))
        return 0
    if d.get("decision") != "EXTEND_STAGE2_PREREGISTERED":
        fail(f"unknown extension decision: {d.get('decision')}")

    # Stage 2: same fail-closed resume behavior; no additional adaptive extension.
    for seed, arm in stage2_sequence(prereg):
        train = run_root / "train" / str(seed) / arm
        ev = run_root / "eval" / str(seed) / arm
        tm = train / "RUN_MANIFEST.json"
        em = ev / "EVAL_MANIFEST.json"
        if train.exists() and not tm.is_file():
            fail(f"partial stage2 train output without RUN_MANIFEST: seed={seed} arm={arm}")
        if train.exists():
            fs = verify_train(train, seed, arm, static_sha, host_sha, profile_sha, expected_steps)
            if fs: fail("stage2 train failed verification: " + "; ".join(fs))
        else:
            if ev.exists(): fail(f"stage2 eval exists before train: seed={seed} arm={arm}")
            if not a.execute:
                print(json.dumps({"status": "READY", "next_step": "TRAIN_STAGE2", "seed": seed, "arm": arm}, indent=2))
                return 0
            run_step(python, live, run_root, f"train_{seed}_{arm}", [
                str(exp / "train_first_screen_v09.py"), "--arm", arm, "--seed", str(seed),
                "--host-lock", str(host), "--profile-lock", str(profile),
                "--extension-decision", str(decision), "--out", str(train), "--lock", str(lock)
            ])
            fs = verify_train(train, seed, arm, static_sha, host_sha, profile_sha, expected_steps)
            if fs: fail("new stage2 train failed verification: " + "; ".join(fs))
            print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "TRAIN_STAGE2", "seed": seed, "arm": arm}, indent=2))
            return 0

        if ev.exists() and not em.is_file():
            fail(f"partial stage2 eval output without EVAL_MANIFEST: seed={seed} arm={arm}")
        if ev.exists():
            fs = verify_eval(ev, tm, static_sha, host_sha)
            if fs: fail("stage2 eval failed verification: " + "; ".join(fs))
        else:
            if not a.execute:
                print(json.dumps({"status": "READY", "next_step": "EVAL_STAGE2", "seed": seed, "arm": arm}, indent=2))
                return 0
            run_step(python, live, run_root, f"eval_{seed}_{arm}", [
                str(exp / "evaluate_first_screen_v09.py"), "--host-lock", str(host),
                "--adapter", str(train / "adapter"), "--run-manifest", str(tm),
                "--label", f"{arm}_SEED_{seed}", "--out", str(ev), "--lock", str(lock)
            ])
            fs = verify_eval(ev, tm, static_sha, host_sha)
            if fs: fail("new stage2 eval failed verification: " + "; ".join(fs))
            print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "EVAL_STAGE2", "seed": seed, "arm": arm}, indent=2))
            return 0

    q2 = run_root / "SEED_EXTENSION_QUALIFICATION.json"
    if not q2.exists():
        if not a.execute:
            print(json.dumps({"status": "READY", "next_step": "QUALIFY_STAGE2"}, indent=2))
            return 0
        run_step(python, live, run_root, "93_qualify_seed_extension", [str(exp / "qualify_seed_extension_v10.py"), "--run-root", str(run_root), "--lock", str(lock)])
        print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "QUALIFY_STAGE2"}, indent=2))
        return 0
    a2 = run_root / "SEED_EXTENSION_ANALYSIS.json"
    if not a2.exists():
        if not a.execute:
            print(json.dumps({"status": "READY", "next_step": "ANALYZE_STAGE2"}, indent=2))
            return 0
        run_step(python, live, run_root, "94_analyze_seed_extension", [str(exp / "analyze_seed_extension_v10.py"), "--run-root", str(run_root)])
        print(json.dumps({"status": "ONE_STEP_COMPLETE", "completed_step": "ANALYZE_STAGE2"}, indent=2))
        return 0

    print(json.dumps({"status": "STAGE2_COMPLETE__NO_FURTHER_ADAPTIVE_EXTENSION", "run_root": str(run_root)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
