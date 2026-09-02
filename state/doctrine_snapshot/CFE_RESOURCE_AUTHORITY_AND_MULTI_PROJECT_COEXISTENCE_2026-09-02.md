# CFE Resource Authority and Multi-Project Coexistence Law

Activated: 2026-09-02
Status: **ACTIVE PROJECT LAW**

## Operator constraint
Multiple independent GPT/project threads may interact with the same machine/server concurrently. CFE SHALL NOT steal a model, port, process, runtime directory, GPU working set, or enough RAM to destabilize another project.

## Core laws

`RESOURCE AVAILABILITY != RESOURCE AUTHORITY`
`SHARED IMMUTABLE MODEL FILE != SHARED LIVE MODEL INSTANCE`
`FREE VRAM != AUTHORIZATION TO CONSUME RAM`
`JOB TABLE IDLE != HOST IDLE`
`PID OWNERSHIP MUST BE PROVEN BEFORE TERMINATION`

## Shareable read-only surfaces
CFE MAY read immutable/shared model files, GGUFs, checkpoints, tokenizers, public caches, and research corpora when no mutation/lock conflict is introduced.

## Exclusive/live surfaces
The following are ownership-sensitive:
- listening ports;
- process IDs and process trees;
- model server instances;
- runtime working directories when mutable;
- GPU allocations;
- large RAM/commit allocations;
- training output directories;
- CUDA contexts and model caches;
- job identities.

## Heavy-run gate
Before any CFE model load, training run, large evaluation, speculative-decoding benchmark, or other heavy accelerator/RAM action:
1. inspect live OS model processes;
2. inspect listeners/ports;
3. inspect GPU free memory/utilization;
4. inspect system free RAM;
5. inspect CFE's own execution jobs;
6. identify which processes are provably CFE-owned;
7. treat every unowned model process as foreign;
8. fail closed if the intended run could materially contend with a foreign live model process.

For the current 35B-A3B + MTP benchmark, **any foreign live model server blocks launch** unless an explicit later resource-sharing contract is created.

## Termination authority
CFE MAY terminate a process only when ownership is proven by at least:
- exact PID;
- expected executable identity;
- expected command-line fingerprint or uniquely identifying arguments;
- direct lineage to a CFE-submitted job or CFE-created interactive test.

CFE SHALL NOT broadly kill `llama-*`, Python, Forge, CUDA, or model-server processes.

## Stale-process cleanup
A CFE-owned stale process SHOULD be removed once proven stale, because leaving it resident is itself resource theft from other projects.

## Evidence scar — 2026-09-02
The CFE execution-job surface reported `running_global=0`, while OS inspection showed a live foreign `llama-server.exe` PID 34152 on port 8114 serving alias `hsp-pass346-arm-b-14b`. Therefore job-table state alone is insufficient for resource authority.

A separate stale CFE-owned `llama-cli.exe` PID 35524 was identified by exact command line and removed by targeted PID kill only.

## Default posture
When a foreign model runtime is active, CFE defaults to low-impact work:
- file inspection;
- hashing;
- documentation;
- dataset curation that does not exhaust RAM/disk I/O;
- code preparation;
- static validation;
- research synthesis.

Heavy work waits for a later verified safe window.
