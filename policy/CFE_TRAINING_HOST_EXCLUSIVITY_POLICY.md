# CFE Training / Model-Task Host Cleanliness Policy

Status: **ACTIVE / FIRST-CLASS EXECUTION CONTROL**
Effective: 2026-09-01
Authority: explicit operator directive after repeated host-memory collisions and rediscovered model-server leftovers.

## Core rule
CFE model work SHALL leave the host cleaner than it found it.

Before **every CFE training launch**, all recognized local model-serving runtimes SHALL be force-terminated and the host SHALL remain free of them for a stable-clean dwell window before training may begin.

After **every CFE training task**, whether it succeeds, fails, throws, or is interrupted through the managed launcher, the same cleanup SHALL run in a `finally` path and SHALL require a stable-clean dwell before completion is accepted.

`TRAINING_START => FORCE_EXIT + STABLE_CLEAN_DWELL`

`TRAINING_SUCCESS_OR_FAILURE => POST_CLEANUP + STABLE_CLEAN_DWELL`

The current stable-clean dwell is 6 continuous seconds. If a model runtime respawns during that interval, it is terminated, the respawn is logged, and the dwell window restarts.

## Mandatory launchers
Training subprocesses SHALL run through:

`tools/cfe_training_launch.py`

General model-loading tasks, including evaluations in newly authored campaign runners, SHOULD run through:

`tools/cfe_model_task_launch.py`

Both use:

`tools/cfe_training_preflight.py`

Historical/frozen scientific trainer or evaluator files SHALL NOT be rewritten merely to add host controls. The execution layer SHALL wrap them externally.

## Recognized model-serving runtimes
The cleanup targets model-serving processes by explicit executable or command-line signature, including:
- llama-server / llama.cpp server
- Ollama
- KoboldCPP
- text-generation-webui / text-generation server
- vLLM serving processes
- LM Studio serving runtime
- LocalAI
- Jan model server
- TabbyAPI
- Aphrodite
- ExLlamaV2 server processes
- equivalent explicit model-serving commands

Python processes are **not** terminated merely because they are Python.

## Protected processes
The policy SHALL NOT kill solely by broad process class:
- PCMMAD receiver/control server
- active CFE campaign runner
- current CFE train/eval task
- unrelated Python processes without a model-serving signature

## Post-task audit
Every managed cleanup receipt SHALL include:
- model-serving processes found;
- processes force-exited;
- any respawn events during the dwell window;
- final survivors;
- task return code when available;
- an `nvidia-smi` compute-process snapshot when available.

A post-task cleanup is PASS only if no recognized model-serving runtime survives the stable-clean dwell.

## Fail-closed behavior
If a recognized model-serving runtime survives or repeatedly reappears such that stable cleanliness cannot be established, a new training launch SHALL fail before loading the training model.

If post-task cleanup cannot establish a clean host, the task result may remain scientifically valid if already manifested, but the execution layer SHALL report host cleanup failure and SHALL NOT silently proceed to another model task.

## Restoration rule
CFE SHALL NOT automatically restore model-serving runtimes after training or evaluation unless the operator explicitly identifies them as required services and supplies/approves the restoration command.

The rediscovered Singularity Works llama-server processes on ports 8091/8092 are specifically **not restoration obligations**.

## Static qualification rule
New campaign/recovery runners SHALL fail static qualification if a training subprocess bypasses `cfe_training_launch.py` or an equivalent immediate call to the same preflight/post-cleanup controls.

Newly authored model-loading evaluation runners SHOULD use `cfe_model_task_launch.py` so the same cleanup guarantee applies after final evaluation, not only before the next training arm.

## Scientific boundary
This is an execution/host-control policy only.

`HOST CLEANUP != SCIENTIFIC ADAPTATION`

It SHALL NOT alter frozen rows, schedules, seeds, tokenization, learner identity, optimizer settings, evaluators, or decision rules.
