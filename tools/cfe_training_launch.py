#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from cfe_training_preflight import force_exit_model_runtimes


def main():
    ap = argparse.ArgumentParser(description='Mandatory CFE training launcher with model-runtime exclusivity preflight.')
    ap.add_argument('--project-root', type=Path, required=True)
    ap.add_argument('--phase', required=True)
    ap.add_argument('command', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = list(a.command)
    if cmd and cmd[0] == '--':
        cmd = cmd[1:]
    if not cmd:
        raise SystemExit('TRAINING_COMMAND_REQUIRED')
    receipt = force_exit_model_runtimes(a.project_root, phase=a.phase)
    if receipt['status'] != 'PASS':
        raise SystemExit('MODEL_RUNTIME_PREFLIGHT_NOT_PASS')
    cp = subprocess.run(cmd, cwd=a.project_root.resolve())
    raise SystemExit(cp.returncode)

if __name__ == '__main__':
    main()
