# CFE / Microseed Model Service Coordination Policy

Status: **ACTIVE / FIRST-CLASS CROSS-PROJECT EXECUTION CONTROL**
Effective: 2026-09-01
Supersedes: broad host-exclusivity / model-class kill policies.

## Core distinction
Shared immutable Forge assets are safe to reuse. Live runtime ownership is not shared.

`SHARED FORGE FILES != SHARED PROCESS OWNERSHIP`

`SHARED MODEL FILES != SHARED PORTS`

`SHARED MODEL FILES != SHARED JOBS`

`SHARED MODEL FILES != SHARED RUNTIME DIRECTORIES`

`PROCESS CLASS != AUTHORITY`

## Microseed ownership
Microseed currently owns these resident model services:

### Primary
- job: `job-7f0dcbe757dc`
- port: `18191`
- model: Qwen2.5-Coder-7B

### CSC reviewer
- job: `job-489435c7630f`
- port: `18192`
- model: Qwen2.5-Coder-1.5B

These live services SHALL be preserved by CFE.

CFE SHALL NOT:
- terminate them;
- reuse their PIDs as authority;
- bind ports 18191/18192;
- reuse their job IDs;
- adopt their live runtime directories;
- broadly kill Forge/llama processes by executable class.

## Shared Forge assets
The underlying immutable files under the Forge/Singularity Works paths MAY be read by both projects.

CFE MAY start its own process using the same immutable model/runtime files when:
- the process is CFE-owned;
- it has a distinct job identity;
- it uses a distinct port if a server port is required;
- it uses CFE-owned output/runtime state directories;
- host memory/GPU capacity has been independently qualified.

The source model/runtime files SHALL be treated as read-only shared assets unless a separate mutation contract exists.

## CFE task ownership
Every CFE-launched model task receives a task lease under:

`state/host_control/task_leases/`

The lease records wrapper PID, child PID, exact command, phase, timestamps, and return code.

Generic task cleanup may terminate only the explicitly leased CFE child tree.

## Pre-task discovery
Before a CFE model task:
1. discover model-serving processes;
2. classify them using `state/host_control/AUTHORIZED_MODEL_SERVICE_REGISTRY.json`;
3. preserve known Microseed resident services;
4. preserve unknown services;
5. fail closed only on unknown/conflicting ownership, not merely because authorized Microseed services exist;
6. reject any CFE command that attempts to claim reserved Microseed ports/jobs;
7. independently verify adequate resource capacity for the intended CFE model task when the task is material.

## Unknown services
`UNKNOWN MODEL SERVICE => PRESERVE + BLOCK, NEVER AUTO-KILL`

Unknown process identity is a coordination seam, not permission to infer orphan status.

## Post-task behavior
After a CFE-owned model task:
- close its CFE task lease;
- reap only its still-live leased CFE process tree if needed;
- preserve Microseed residents;
- preserve unknown services;
- record post-task service discovery.

## Cross-project research status boundary
Microseed frontier results supplied in the ownership handoff are cross-project context, not CFE scientific occupancy.

Current operator-reported Microseed status:
- G_NAKED sealed;
- B_DRIFT sealed;
- A_TARGET sealed;
- K_RED_TEAM sealed;
- C_SCALE passed its bounded three-level execution discriminator and result-level CSC PASS; research-branch sealing / dedicated continuity reconciliation remained pending at handoff;
- I_GROWTH is a verified negative and remains open under CSC REVIEW;
- no canonical Microseed production code was changed by those frontier results.

CFE SHALL NOT promote these facts into CFE causal doctrine without an explicit transfer argument and CFE evidence.

## Scientific boundary
`PROCESS COORDINATION != SCIENTIFIC ADAPTATION`

This policy SHALL NOT alter frozen CFE rows, schedules, seeds, tokenization, learner identity, optimizer, evaluator, or disposition rules.
