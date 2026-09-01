# CFE Training Host Exclusivity Policy — SUPERSEDED

Status: **SUPERSEDED / DO NOT USE FOR ACTIVE EXECUTION**
Superseded: 2026-09-01
Successor: `policy/CFE_MODEL_SERVICE_COORDINATION_POLICY.md`

## Why superseded
The original policy inferred that model-serving processes were expendable unless explicitly protected. The operator identified that one or more resident model servers may power Microseed/SOP machinery. Therefore process-class termination is unsafe.

The active rule is now identity-first service coordination:

`PROCESS CLASS != AUTHORITY`

`UNKNOWN MODEL SERVICE => PRESERVE + BLOCK, NEVER AUTO-KILL`

`CFE MAY TERMINATE ONLY EXPLICITLY CFE-OWNED TASK TREES OR EXPLICITLY REGISTERED CFE-MANAGED TRANSIENT SERVICES`

Do not implement or revive broad `llama-server` / model-runtime kill-all behavior from this superseded document.
