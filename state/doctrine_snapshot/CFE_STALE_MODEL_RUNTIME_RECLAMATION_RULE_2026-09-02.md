# CFE Stale Model Runtime Reclamation Rule

Activated: 2026-09-02
Status: **ACTIVE RESOURCE-AUTHORITY COMPANION RULE**

## Purpose
Prevent two opposite failures:
1. stealing a live model/runtime from another project;
2. treating an orphaned warm model load as permanent foreign authority and wasting shared RAM/VRAM.

## Core distinctions

`LISTENING SOCKET != ACTIVE OWNER`
`HEALTHY SERVER != ACTIVE WORKLOAD`
`IDLE MODEL LOAD != STALE BY ITSELF`
`STALE RECLAMATION REQUIRES MULTI-SIGNAL EVIDENCE`

## Stale-runtime evidence bundle
A foreign-appearing model runtime MAY be reclassified as a stale orphan only when several independent signals agree. Preferred evidence:
- parent/launcher process is gone;
- no established client connections;
- server slot(s) report idle / not processing;
- no CPU movement across a bounded observation window;
- no meaningful GPU activity attributable to the process;
- runtime has been resident materially longer than its last observed task;
- command line and listening port identify the exact model service being evaluated.

No single item is sufficient by itself.

## Reclamation authority
After the stale bundle is satisfied, CFE MAY reclaim only the exact orphaned PID after re-reading its executable path, command line, alias/model, and port immediately before termination.

CFE SHALL NOT use a process-name-wide kill.

## 2026-09-02 earned scar
PID 34152 appeared to be another project's live 14B server on port 8114. Direct inspection showed:
- `llama-server.exe`, alias `hsp-pass346-arm-b-14b`;
- uptime ~3.52 hours;
- parent PID no longer existed;
- `/health` = ok;
- only slot `is_processing=false` after a prior 1123-token task;
- zero established TCP clients;
- CPU delta = 0.0000 seconds over a 6-second observation;
- `--gpu-layers 0` and negligible current GPU activity;
- ~7.113 GiB private RAM retained.

The process was therefore classified **STALE_ORPHAN_VERIFIED** and terminated by exact PID/fingerprint only. Host free RAM rose sufficiently to admit the guarded CFE benchmark.

## Relationship to resource-authority law
`RESOURCE AVAILABILITY != RESOURCE AUTHORITY` remains active.
This companion rule adds:

> **Authority claims can also become stale and must be tested against live consequence.**

A stale load is not allowed to monopolize shared resources merely because a socket still answers health checks.
