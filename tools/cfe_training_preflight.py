#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, subprocess, time
from datetime import datetime
from pathlib import Path

MODEL_PROCESS_NAME_PATTERNS=(
    'llama-server','llama-server.exe','ollama','ollama.exe','koboldcpp','koboldcpp.exe',
    'lmstudio','lm studio','localai','local-ai','jan.exe',
)
MODEL_COMMAND_PATTERNS=(
    'llama-server','ollama serve','koboldcpp','text-generation-webui','text_generation_server',
    'text-generation-launcher','vllm.entrypoints','vllm serve','lmstudio','lm studio','localai',
    'local-ai','transformers.commands.serving','transformers serve','openai_api_server','oobabooga',
    'tabbyapi','aphrodite','exllamav2.server',
)
REGISTRY_REL=Path('state/host_control/AUTHORIZED_MODEL_SERVICE_REGISTRY.json')
DISCOVERY_REL=Path('state/host_control/LAST_MODEL_SERVICE_DISCOVERY.json')
LEASE_DIR_REL=Path('state/host_control/task_leases')
STABLE_OBSERVATION_SECONDS=4.0
POLL_SECONDS=1.0


def _ps_json(script:str):
    cp=subprocess.run(['powershell','-NoProfile','-Command',script],capture_output=True,text=True,errors='replace',check=True)
    text=cp.stdout.strip()
    if not text:return []
    data=json.loads(text)
    return data if isinstance(data,list) else [data]


def _processes():
    return _ps_json("Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine | ConvertTo-Json -Depth 3")


def _is_model_service(proc:dict)->bool:
    name=str(proc.get('Name') or '').lower();cmd=str(proc.get('CommandLine') or '').lower()
    return any(p in name for p in MODEL_PROCESS_NAME_PATTERNS) or any(p in cmd for p in MODEL_COMMAND_PATTERNS)


def _load_registry(root:Path)->dict:
    p=root/REGISTRY_REL
    if not p.is_file():raise RuntimeError('MODEL_SERVICE_REGISTRY_MISSING')
    return json.loads(p.read_text(encoding='utf-8'))


def _entry_matches(proc:dict,entry:dict)->bool:
    match=entry.get('match') or {}
    exe=str(proc.get('ExecutablePath') or '').lower()
    cmd=str(proc.get('CommandLine') or '').lower()
    expected_exe=match.get('executable_path')
    if expected_exe and exe!=str(expected_exe).lower():return False
    for token in match.get('command_contains',[]):
        if str(token).lower() not in cmd:return False
    return True


def _classify(root:Path,proc:dict)->dict:
    registry=_load_registry(root)
    for entry in registry.get('services',[]):
        if _entry_matches(proc,entry):
            return {'kind':'REGISTERED','service_id':entry['service_id'],'classification':entry['classification'],'action':entry['action'],'blocks_cfe_model_task':bool(entry.get('blocks_cfe_model_task',False)),'registry_entry':entry}
    return {'kind':'UNKNOWN','service_id':None,'classification':'UNKNOWN_MODEL_SERVICE','action':'PRESERVE_AND_BLOCK_MODEL_TASK','blocks_cfe_model_task':True}


def _discover(root:Path)->list[dict]:
    rows=[]
    for proc in _processes():
        if not _is_model_service(proc):continue
        c=_classify(root,proc)
        rows.append({'process':proc,**{k:v for k,v in c.items() if k!='registry_entry'}})
    return rows


def _write_json(path:Path,obj:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')


def _write_discovery(root:Path,phase:str,rows:list[dict])->Path:
    obj={'schema':'cfe.model-service-discovery.v1','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'services':rows}
    p=root/DISCOVERY_REL;_write_json(p,obj);return p


def _write_receipt(root:Path,prefix:str,obj:dict)->Path:
    d=root/'state/host_preflight';d.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z');p=d/f'{prefix}_{stamp}.json';_write_json(p,obj);return p


def _terminate_registered_cfe_transient(proc:dict,classification:dict)->bool:
    if classification.get('action')!='TERMINATE_CFE_MANAGED_TRANSIENT':return False
    pid=int(proc['ProcessId'])
    subprocess.run(['taskkill','/PID',str(pid),'/T','/F'],capture_output=True,text=True,errors='replace')
    return True


def enforce_model_service_boundary(project_root:Path,*,phase:str='MODEL_TASK')->dict:
    """Identity-first preflight. Never auto-kill unknown/protected resident model services."""
    root=Path(project_root).resolve();observations=[];deadline=time.monotonic()+STABLE_OBSERVATION_SECONDS
    while True:
        rows=_discover(root);observations.append({'timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'services':rows})
        # Only explicitly registered CFE-managed transient services may be terminated.
        changed=False
        for row in rows:
            if row['kind']=='REGISTERED' and row['action']=='TERMINATE_CFE_MANAGED_TRANSIENT':
                changed=_terminate_registered_cfe_transient(row['process'],row) or changed
        blockers=[r for r in rows if r['blocks_cfe_model_task']]
        if blockers:
            _write_discovery(root,phase,rows)
            receipt={'schema':'cfe.model-service-boundary-preflight.v1','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'status':'BLOCKED_MODEL_SERVICE_PRESENT','blockers':blockers,'observations':observations,'law':'UNKNOWN_OR_PROTECTED_MODEL_SERVICE => PRESERVE_AND_BLOCK_NOT_KILL'}
            _write_receipt(root,'MODEL_SERVICE_BOUNDARY_PREFLIGHT',receipt)
            raise RuntimeError('MODEL_SERVICE_BOUNDARY_BLOCKED:'+','.join(str((r.get('service_id') or 'UNKNOWN')) for r in blockers))
        if time.monotonic()>=deadline:
            _write_discovery(root,phase,rows)
            receipt={'schema':'cfe.model-service-boundary-preflight.v1','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'status':'PASS','services':rows,'stable_observation_seconds':STABLE_OBSERVATION_SECONDS,'law':'NO_PROCESS_CLASS_KILLING'}
            _write_receipt(root,'MODEL_SERVICE_BOUNDARY_PREFLIGHT',receipt)
            return receipt
        time.sleep(POLL_SECONDS)


def force_exit_model_runtimes(project_root:Path,*,phase:str='MODEL_TASK')->dict:
    """Compatibility alias. Semantics changed: identity-first boundary, no broad killing."""
    return enforce_model_service_boundary(project_root,phase=phase)


def cleanup_after_model_task(project_root:Path,*,phase:str,task_return_code:int|None=None)->dict:
    """Post-task audit. Terminates only explicitly registered CFE-managed transient services."""
    root=Path(project_root).resolve();rows=_discover(root);terminated=[]
    for row in rows:
        if row['kind']=='REGISTERED' and row['action']=='TERMINATE_CFE_MANAGED_TRANSIENT':
            if _terminate_registered_cfe_transient(row['process'],row):terminated.append(row)
    after=_discover(root);unknown=[r for r in after if r['kind']=='UNKNOWN'];protected=[r for r in after if r['kind']=='REGISTERED' and r['action'].startswith('PRESERVE')]
    _write_discovery(root,phase,after)
    status='PASS'
    if unknown:status='ATTENTION_UNKNOWN_SERVICE_PRESERVED'
    elif protected:status='PASS_RESIDENT_SERVICES_PRESERVED'
    receipt={'schema':'cfe.model-task-postcleanup.v3','timestamp':datetime.now().astimezone().isoformat(timespec='seconds'),'phase':phase,'task_return_code':task_return_code,'status':status,'terminated_cfe_managed_transients':terminated,'resident_services_preserved':protected,'unknown_services_preserved':unknown,'law':'POST_TASK_CLEANUP_MAY_TERMINATE_ONLY_EXPLICIT_CFE_MANAGED_TRANSIENTS'}
    _write_receipt(root,'MODEL_TASK_POSTCLEANUP',receipt)
    return receipt



def validate_cfe_task_isolation(project_root:Path,command:list[str])->dict:
    """Reject commands that attempt to claim Microseed-reserved ports/jobs; shared immutable Forge files remain allowed."""
    root=Path(project_root).resolve();reg=_load_registry(root);joined=' '.join(str(x) for x in command).lower()
    conflicts=[]
    for port in reg.get('reserved_ports',[]):
        tokens=[f'--port {port}',f'--port={port}',f':{port}',f' 127.0.0.1:{port}']
        if any(t.lower() in joined for t in tokens):conflicts.append({'kind':'PORT','value':port})
    for job in reg.get('reserved_jobs',[]):
        if str(job).lower() in joined:conflicts.append({'kind':'JOB','value':job})
    result={'schema':'cfe.task-isolation-validation.v1','status':'PASS' if not conflicts else 'FAIL_RESERVED_MICROSEED_IDENTITY','conflicts':conflicts,'shared_asset_rule':reg.get('shared_asset_rule'),'working_directory':str(root)}
    if conflicts:raise RuntimeError('CFE_TASK_ISOLATION_CONFLICT:'+json.dumps(conflicts,sort_keys=True))
    return result

def open_task_lease(project_root:Path,*,phase:str,child_pid:int,command:list[str])->Path:
    root=Path(project_root).resolve();d=root/LEASE_DIR_REL;d.mkdir(parents=True,exist_ok=True)
    obj={'schema':'cfe.model-task-lease.v1','status':'RUNNING','timestamp_opened':datetime.now().astimezone().isoformat(timespec='seconds'),'owner':'CFE','wrapper_pid':os.getpid(),'child_pid':int(child_pid),'phase':phase,'command':command}
    p=d/f'{child_pid}.json';_write_json(p,obj);return p


def close_task_lease(path:Path,*,return_code:int|None,status:str='CLOSED')->None:
    obj=json.loads(path.read_text(encoding='utf-8'));obj['status']=status;obj['return_code']=return_code;obj['timestamp_closed']=datetime.now().astimezone().isoformat(timespec='seconds');_write_json(path,obj)


def terminate_owned_task_tree(child_pid:int)->dict:
    """Terminate only a PID explicitly leased to CFE, including its descendants."""
    cp=subprocess.run(['taskkill','/PID',str(int(child_pid)),'/T','/F'],capture_output=True,text=True,errors='replace')
    return {'pid':int(child_pid),'return_code':cp.returncode,'stdout':cp.stdout[-2000:],'stderr':cp.stderr[-2000:]}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--project-root',type=Path,required=True);ap.add_argument('--phase',default='MODEL_TASK');ap.add_argument('--post-cleanup',action='store_true');ap.add_argument('--task-return-code',type=int);a=ap.parse_args()
    fn=cleanup_after_model_task if a.post_cleanup else enforce_model_service_boundary;kwargs={'phase':a.phase}
    if a.post_cleanup:kwargs['task_return_code']=a.task_return_code
    print(json.dumps(fn(a.project_root,**kwargs),indent=2,sort_keys=True))
