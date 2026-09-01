# CFE Model Service Coordination Policy

Status: **ACTIVE / FIRST-CLASS EXECUTION CONTROL**
Effective: 2026-09-01
Supersedes: `policy/CFE_TRAINING_HOST_EXCLUSIVITY_POLICY.md`
Reason: operator identified that one or more resident model servers may power Microseed/SOP machinery; process-class termination is therefore unsafe.

## Core correction
CFE SHALL NOT infer ownership or expendability from executable class.

`PROCESS CLASS != AUTHORITY`

`MODEL SERVER != ORPHAN`

`UNKNOWN MODEL SERVICE => PRESERVE + BLOCK, NEVER AUTO-KILL`

`PROTECTED/RESIDENT SERVICE => PRESERVE`

`CFE MAY TERMINATE ONLY AN EXPLICITLY CFE-OWNED TASK TREE OR REGISTERED CFE-MANAGED TRANSIENT SERVICE`

## Two authority namespaces
### Resident service registry
Resident or potentially load-bearing services are described in:

`state/host_control/AUTHORIZED_MODEL_SERVICE_REGISTRY.json`

A registry entry binds service identity to stable process evidence such as:
- executable path;
- model path or command signature;
- port;
- owner/purpose when known;
- classification;
- whether its presence blocks a CFE model task.

A PID is runtime evidence, not permanent identity. PID reuse SHALL trigger identity re-check.

### CFE model-task leases
Every CFE-launched train/eval/model-loading child process receives an owned task lease under:

`state/host_control/task_leases/`

The lease records:
- wrapper PID;
- child PID;
- phase;
- exact command;
- open/close timestamps;
- return code.

Only a PID/tree owned by such a CFE lease may be force-terminated by generic CFE task cleanup.

## Pre-task behavior
Before CFE launches a model-heavy task:
1. discover current model-serving processes;
2. classify each against the resident-service registry;
3. preserve every registered resident/protected service;
4. preserve every unknown service;
5. if any unknown or `blocks_cfe_model_task=true` service is present, FAIL CLOSED **without killing it**;
6. proceed only when service/resource ownership is unambiguous.

This converts hidden resource collisions into explicit coordination blockers rather than destructive cleanup.

## Post-task behavior
After a CFE-owned model task:
- close its task lease;
- terminate only its still-live explicitly leased child tree if necessary;
- terminate only services explicitly registered as `TERMINATE_CFE_MANAGED_TRANSIENT`;
- preserve resident/protected/unknown model services;
- record discovery state for the next task.

An unknown resident service after a task is an attention/blocker condition, not permission to kill it.

## Historical 8091/8092 services
The two Singularity Works llama-server signatures discovered during DD2 are registered as `PROTECTED_PENDING_IDENTITY`:
- Qwen2.5-Coder-7B-Instruct-abliterated on port 8091;
- Qwen2.5-Coder-1.5B-Instruct-abliterated on port 8092.

Operator reports one or both may have powered Microseed/SOP machinery. CFE has not proven which one. Therefore both are protected until identity is resolved.

No current Windows service, scheduled task, or Startup entry was found that proves their launcher/owner.

## Scientific boundary
This policy governs host/process coordination only.

`PROCESS COORDINATION != SCIENTIFIC ADAPTATION`

It SHALL NOT alter frozen experimental rows, schedules, seeds, tokenization, learner identity, optimizer, evaluator, or disposition rules.
