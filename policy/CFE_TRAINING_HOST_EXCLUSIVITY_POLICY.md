# CFE Training Host Exclusivity Policy

Status: **ACTIVE / FIRST-CLASS EXECUTION CONTROL**
Effective: 2026-09-01
Authority: explicit operator directive after host-memory collision during DD2.

## Core rule
Before **every CFE training launch**, all recognized local model-serving runtimes SHALL be force-terminated and a second process scan SHALL verify that none survive.

`TRAINING_START => MODEL_SERVERS_FORCE_EXITED + SURVIVOR_SCAN_PASS`

This applies even when the model-serving runtime was not started by the operator and even when it appears idle.

## Mandatory launcher
All CFE training subprocesses SHALL be launched through:

`tools/cfe_training_launch.py`

which invokes:

`tools/cfe_training_preflight.py`

before starting the frozen trainer command.

Historical/frozen scientific trainer files SHALL NOT be rewritten merely to add this host-control rule. The execution layer wraps them externally.

## Recognized model-serving runtime classes
The preflight targets local model servers by executable and/or command-line signature, including:
- llama-server / llama.cpp server
- Ollama serving runtime
- KoboldCPP
- text-generation-webui / Hugging Face text-generation server
- vLLM OpenAI/server processes
- LM Studio serving runtime
- LocalAI
- Jan model server
- TabbyAPI
- Aphrodite
- ExLlamaV2 server processes
- equivalent Python serving commands identified by explicit model-serving signatures

Python processes are **not** killed merely because they are Python.

## Protected processes
The following SHALL NOT be killed solely by this policy:
- PCMMAD receiver/control server
- the active CFE campaign runner
- the CFE training process being launched
- ordinary unrelated Python processes without a model-serving signature

## Fail-closed behavior
If a recognized model-serving runtime survives termination or reappears before the survivor scan completes, the training launch SHALL fail before loading the training model.

## Evaluation default
CFE GPU/model evaluations SHOULD use the same preflight because they load the same base model and can collide with host commit/GPU resources. Active recovery runners may enforce it for both TRAIN and EVAL.

## Restoration rule
CFE SHALL NOT automatically restore model-serving runtimes after training unless the operator explicitly identifies them as required services and supplies/approves the restoration command.

The orphan Singularity Works llama-server processes discovered during DD2 are specifically **not restoration obligations**.

## Static qualification rule
New campaign/recovery runners SHALL fail static qualification if a training subprocess bypasses `cfe_training_launch.py` or an equivalent call to `force_exit_model_runtimes()` immediately before training.

## Provenance
This policy was introduced after DD2 evaluation repeatedly failed under host commit pressure while two unrelated orphan `llama-server` processes consumed approximately 15 GB of resident memory. Removing them allowed the frozen base-model load smoke to pass.
