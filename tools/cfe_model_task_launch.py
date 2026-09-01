#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess
from pathlib import Path
from cfe_training_preflight import force_exit_model_runtimes, cleanup_after_model_task


def main():
    ap=argparse.ArgumentParser(description='CFE model-task launcher: stable-clean preflight + guaranteed post-task cleanup.')
    ap.add_argument('--project-root',type=Path,required=True)
    ap.add_argument('--phase',required=True)
    ap.add_argument('command',nargs=argparse.REMAINDER)
    a=ap.parse_args()
    cmd=list(a.command)
    if cmd and cmd[0]=='--':cmd=cmd[1:]
    if not cmd:raise SystemExit('MODEL_TASK_COMMAND_REQUIRED')
    force_exit_model_runtimes(a.project_root,phase=f'{a.phase}:PRE')
    rc=None
    try:
        cp=subprocess.run(cmd,cwd=a.project_root.resolve())
        rc=cp.returncode
        return rc
    finally:
        cleanup_after_model_task(a.project_root,phase=f'{a.phase}:POST',task_return_code=rc)

if __name__=='__main__':
    raise SystemExit(main())
