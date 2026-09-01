#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess
from pathlib import Path
from cfe_training_preflight import (
    enforce_model_service_boundary, cleanup_after_model_task,
    open_task_lease, close_task_lease, terminate_owned_task_tree, validate_cfe_task_isolation,
)


def main():
    ap=argparse.ArgumentParser(description='CFE model-task launcher with resident-service coordination and PID lease ownership.')
    ap.add_argument('--project-root',type=Path,required=True)
    ap.add_argument('--phase',required=True)
    ap.add_argument('command',nargs=argparse.REMAINDER)
    a=ap.parse_args();cmd=list(a.command)
    if cmd and cmd[0]=='--':cmd=cmd[1:]
    if not cmd:raise SystemExit('MODEL_TASK_COMMAND_REQUIRED')
    validate_cfe_task_isolation(a.project_root,cmd)
    enforce_model_service_boundary(a.project_root,phase=f'{a.phase}:PRE')
    proc=None;lease=None;rc=None
    try:
        proc=subprocess.Popen(cmd,cwd=a.project_root.resolve())
        lease=open_task_lease(a.project_root,phase=a.phase,child_pid=proc.pid,command=cmd)
        rc=proc.wait()
        return rc
    finally:
        if proc is not None and proc.poll() is None:
            terminate_owned_task_tree(proc.pid)
            try: proc.wait(timeout=10)
            except Exception: pass
        if lease is not None:
            close_task_lease(lease,return_code=rc,status='CLOSED')
        cleanup_after_model_task(a.project_root,phase=f'{a.phase}:POST',task_return_code=rc)

if __name__=='__main__':
    raise SystemExit(main())
