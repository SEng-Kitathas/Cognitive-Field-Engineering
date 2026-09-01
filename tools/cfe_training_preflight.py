#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, time
from datetime import datetime
from pathlib import Path

PROCESS_NAME_PATTERNS=(
    'llama-server','llama-server.exe','ollama','ollama.exe','koboldcpp','koboldcpp.exe',
    'lmstudio','lm studio','localai','local-ai','jan.exe',
)
COMMAND_PATTERNS=(
    'llama-server','ollama serve','koboldcpp','text-generation-webui','text_generation_server',
    'text-generation-launcher','vllm.entrypoints','vllm serve','lmstudio','lm studio','localai',
    'local-ai','transformers.commands.serving','transformers serve','openai_api_server','oobabooga',
    'tabbyapi','aphrodite','exllamav2.server',
)
PROTECTED_COMMAND_PATTERNS=(
    'pcmmad_receiver','pcmmad receiver','cfe_training_preflight.py','cfe_training_launch.py',
    'cfe_model_task_launch.py','train_dd1_predicate_field_resolution.py','train_dd2_revisit_topology.py',
    'train_v11_predicate_policy.py','train_v12_factor_primitive.py','train_v13_optimizer_interference.py',
    'train_v14_predicate_horizon.py','evaluate_dd1_disposition.py','evaluate_dd2_revisit_topology.py',
    'run_dd1','run_dd2','run_v11','run_v12','run_v13','run_v14',
)
STABLE_CLEAN_SECONDS=6.0
STABLE_CLEAN_POLL_SECONDS=1.0


def _ps_json(script:str):
    cp=subprocess.run(['powershell','-NoProfile','-Command',script],capture_output=True,text=True,errors='replace',check=True)
    text=cp.stdout.strip()
    if not text:return []
    data=json.loads(text)
    return data if isinstance(data,list) else [data]


def _processes():
    return _ps_json("Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine | ConvertTo-Json -Depth 3")


def _gpu_compute_apps():
    try:
        cp=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader,nounits'],capture_output=True,text=True,errors='replace',timeout=15)
        if cp.returncode!=0:return {'status':'UNAVAILABLE','stderr':cp.stderr[-1000:]}
        rows=[]
        for line in cp.stdout.splitlines():
            parts=[x.strip() for x in line.split(',')]
            if len(parts)>=3:rows.append({'pid':parts[0],'process_name':parts[1],'used_memory_mib':parts[2]})
        return {'status':'PASS','compute_apps':rows}
    except Exception as e:return {'status':'UNAVAILABLE','error':repr(e)}


def _is_target(proc:dict)->bool:
    name=str(proc.get('Name') or '').lower();cmd=str(proc.get('CommandLine') or '').lower()
    if any(p in cmd for p in PROTECTED_COMMAND_PATTERNS):return False
    return any(p in name for p in PROCESS_NAME_PATTERNS) or any(p in cmd for p in COMMAND_PATTERNS)


def _kill_one(proc:dict)->bool:
    pid=int(proc['ProcessId'])
    current=[x for x in _processes() if int(x.get('ProcessId') or -1)==pid]
    if not current or not _is_target(current[0]):return False
    subprocess.run(['powershell','-NoProfile','-Command',f'Stop-Process -Id {pid} -Force -ErrorAction Stop'],capture_output=True,text=True,errors='replace',check=True)
    return True


def _stabilize_clean_host()->dict:
    initial=[p for p in _processes() if _is_target(p)]
    killed=[];respawn_events=[]
    for p in initial:
        if _kill_one(p):killed.append(p)
    deadline=time.monotonic()+STABLE_CLEAN_SECONDS
    while True:
        now=time.monotonic()
        if now>=deadline:break
        time.sleep(min(STABLE_CLEAN_POLL_SECONDS,max(0.05,deadline-now)))
        hits=[p for p in _processes() if _is_target(p)]
        if hits:
            respawn_events.append({'timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'processes':hits})
            for p in hits:
                if _kill_one(p):killed.append(p)
            # Require a full clean dwell after the latest respawn.
            deadline=time.monotonic()+STABLE_CLEAN_SECONDS
    survivors=[p for p in _processes() if _is_target(p)]
    return {'matched_initial':initial,'force_exited':killed,'respawn_events':respawn_events,'survivors':survivors,'stable_clean_seconds':STABLE_CLEAN_SECONDS}


def _write_receipt(project_root:Path,prefix:str,receipt:dict)->Path:
    log_dir=Path(project_root).resolve()/'state'/'host_preflight';log_dir.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z');path=log_dir/f'{prefix}_{stamp}.json'
    path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');return path


def force_exit_model_runtimes(project_root:Path,*,phase:str='TRAINING')->dict:
    project_root=Path(project_root).resolve();st=_stabilize_clean_host()
    receipt={'schema':'cfe.training-model-runtime-preflight.v3','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'policy':'FORCE_EXIT_AND_STABLE_CLEAN_DWELL_BEFORE_CFE_MODEL_TASK',**st,'gpu_snapshot_after_cleanup':_gpu_compute_apps(),'status':'PASS' if not st['survivors'] else 'FAIL_SURVIVORS','protected_rule':'PCMMAD receiver and active CFE execution/model-task processes are never kill targets merely because they are Python processes.','restoration_required':False}
    _write_receipt(project_root,'TRAINING_MODEL_RUNTIME_PREFLIGHT',receipt)
    if st['survivors']:raise RuntimeError('MODEL_RUNTIME_PREFLIGHT_FAIL_SURVIVORS:'+','.join(str(x.get('ProcessId')) for x in st['survivors']))
    return receipt


def cleanup_after_model_task(project_root:Path,*,phase:str,task_return_code:int|None=None)->dict:
    project_root=Path(project_root).resolve();st=_stabilize_clean_host()
    receipt={'schema':'cfe.model-task-postcleanup.v2','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'task_return_code':task_return_code,'policy':'ALWAYS_FORCE_EXIT_AND_STABLE_CLEAN_DWELL_AFTER_MODEL_TASK_SUCCESS_OR_FAILURE',**st,'gpu_snapshot_after_cleanup':_gpu_compute_apps(),'status':'PASS' if not st['survivors'] else 'FAIL_SURVIVORS','restoration_required':False}
    _write_receipt(project_root,'MODEL_TASK_POSTCLEANUP',receipt)
    if st['survivors']:raise RuntimeError('MODEL_RUNTIME_POSTCLEANUP_FAIL_SURVIVORS:'+','.join(str(x.get('ProcessId')) for x in st['survivors']))
    return receipt


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--phase',default='TRAINING');ap.add_argument('--post-cleanup',action='store_true');ap.add_argument('--task-return-code',type=int);a=ap.parse_args()
    fn=cleanup_after_model_task if a.post_cleanup else force_exit_model_runtimes;kwargs={'phase':a.phase}
    if a.post_cleanup:kwargs['task_return_code']=a.task_return_code
    print(json.dumps(fn(a.project_root,**kwargs),indent=2,sort_keys=True))
