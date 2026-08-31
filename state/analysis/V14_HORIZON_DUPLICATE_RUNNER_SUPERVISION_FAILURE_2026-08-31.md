# V14 Horizon Duplicate-Runner / Supervision Failure

Date: 2026-08-31 13:34 Eastern Daylight Time
Status: EXECUTION-CONTROL FAILURE — NO SCIENTIFIC OUTCOME

## Verified failure
Two horizon jobs were concurrently active:
- V14R: `job-1c115593cb12`, started 2026-08-31 10:58:56 ET.
- V14R1: `job-d4aac6ed6175`, started 2026-08-31 11:07:19 ET.

Both were marked `SUPERVISION_LOST` at the same instant: 2026-08-31 13:25:04 ET. Both had null exit code, no signal, no host-preempted flag, empty stderr, and only `TRAIN 2026083111` on parent stdout. Windows event logs showed no application crash, GPU-driver fault, kernel-power event, or resource-exhaustion event in the surrounding window. No relevant Python child survived.

Each campaign root contained only the initial `CAMPAIGN_RECEIPT.json`; neither produced a train manifest, checkpoint, evaluation, or sealed trajectory. Therefore no scientific outcome exists from either attempt.

## Control defect
V14R was already the properly recovered identity binding current v1.3 disposition SHA `48f29fa9...`. V14R1 was an unnecessary duplicate recovery path launched without noticing V14R was active. This violated the standing single-runner control.

## Scientific disposition
- V14R remains authoritative scientific identity.
- V14R1 is demoted to execution-control error lineage only.
- Both failed campaign attempts are provenance-only.
- Because V14R locked scientific bytes did not change and no outcome was produced, recovery requires a fresh execution attempt, not a new scientific identity.

## Recovery
V14R Attempt 2 launched as job `job-1b72da92b63f`, PID `4616`, fresh output root `state/analysis/V14R_PREDICATE_HORIZON_CAMPAIGN_ATTEMPT2_20260831T1730Z`. At this readback PID is `ALIVE`, receipt status `RUNNING`, 0/6 trajectories sealed.

## New control scar
`QUALIFIED IDENTITY != UNIQUE ACTIVE RUNNER`

Before every future scientific launch, enumerate active project jobs and fail closed if another job owns the same scientific family/GPU path.
