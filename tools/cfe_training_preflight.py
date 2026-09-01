#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, time
from datetime import datetime
from pathlib import Path

# Local model-serving runtimes that must never coexist with a CFE training launch.
# Match by executable name or command-line signature. Python itself is NOT a target.
PROCESS_NAME_PATTERNS = (
    'llama-server', 'llama-server.exe', 'ollama', 'ollama.exe', 'koboldcpp',
    'koboldcpp.exe', 'lmstudio', 'lm studio', 'localai', 'local-ai', 'jan.exe',
)
COMMAND_PATTERNS = (
    'llama-server', 'ollama serve', 'koboldcpp', 'text-generation-webui',
    'text_generation_server', 'text-generation-launcher', 'vllm.entrypoints',
    'vllm serve', 'lmstudio', 'lm studio', 'localai', 'local-ai',
    'transformers.commands.serving', 'transformers serve', 'openai_api_server',
    'oobabooga', 'tabbyapi', 'aphrodite', 'exllamav2.server',
)
PROTECTED_COMMAND_PATTERNS = (
    'pcmmad_receiver', 'pcmmad receiver',
    'cfe_training_preflight.py',
    'train_dd1_predicate_field_resolution.py',
    'train_dd2_revisit_topology.py',
    'train_v11_predicate_policy.py',
    'train_v12_factor_primitive.py',
    'train_v13_optimizer_interference.py',
    'train_v14_predicate_horizon.py',
    'run_dd1', 'run_dd2', 'run_v11', 'run_v12', 'run_v13', 'run_v14',
)


def _ps_json(script: str):
    cp = subprocess.run(
        ['powershell', '-NoProfile', '-Command', script],
        capture_output=True, text=True, errors='replace', check=True,
    )
    text = cp.stdout.strip()
    if not text:
        return []
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def _processes():
    return _ps_json(
        "Get-CimInstance Win32_Process | "
        "Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine | "
        "ConvertTo-Json -Depth 3"
    )


def _is_target(proc: dict) -> bool:
    name = str(proc.get('Name') or '').lower()
    cmd = str(proc.get('CommandLine') or '').lower()
    if any(p in cmd for p in PROTECTED_COMMAND_PATTERNS):
        return False
    return any(p in name for p in PROCESS_NAME_PATTERNS) or any(p in cmd for p in COMMAND_PATTERNS)


def force_exit_model_runtimes(project_root: Path, *, phase: str = 'TRAINING') -> dict:
    """Force-exit recognized local model-serving runtimes and fail closed if any survive."""
    project_root = Path(project_root).resolve()
    before = _processes()
    targets = [p for p in before if _is_target(p)]
    killed = []
    for p in targets:
        pid = int(p['ProcessId'])
        # Re-check the exact PID immediately before stopping it.
        current = [x for x in _processes() if int(x.get('ProcessId') or -1) == pid]
        if not current or not _is_target(current[0]):
            continue
        subprocess.run(
            ['powershell', '-NoProfile', '-Command', f'Stop-Process -Id {pid} -Force -ErrorAction Stop'],
            capture_output=True, text=True, errors='replace', check=True,
        )
        killed.append(current[0])
    time.sleep(1.0)
    survivors = [p for p in _processes() if _is_target(p)]
    receipt = {
        'schema': 'cfe.training-model-runtime-preflight.v1',
        'timestamp': datetime.now().astimezone().isoformat(timespec='seconds'),
        'phase': phase,
        'policy': 'FORCE_EXIT_ALL_RECOGNIZED_LOCAL_MODEL_SERVERS_BEFORE_CFE_TRAINING',
        'matched_before': targets,
        'force_exited': killed,
        'survivors': survivors,
        'status': 'PASS' if not survivors else 'FAIL_SURVIVORS',
        'protected_rule': 'PCMMAD receiver and active CFE execution/training processes are never kill targets merely because they are Python processes.',
        'restoration_required': False,
    }
    log_dir = project_root / 'state' / 'host_preflight'
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z')
    path = log_dir / f'TRAINING_MODEL_RUNTIME_PREFLIGHT_{stamp}.json'
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    if survivors:
        raise RuntimeError('MODEL_RUNTIME_PREFLIGHT_FAIL_SURVIVORS: ' + ','.join(str(x.get('ProcessId')) for x in survivors))
    return receipt


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', type=Path, required=True)
    ap.add_argument('--phase', default='TRAINING')
    a = ap.parse_args()
    print(json.dumps(force_exit_model_runtimes(a.project_root, phase=a.phase), indent=2, sort_keys=True))
