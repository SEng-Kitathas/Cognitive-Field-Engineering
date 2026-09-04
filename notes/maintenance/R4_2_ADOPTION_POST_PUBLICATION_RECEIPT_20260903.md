# R4.2 Adoption Post-Publication Receipt — Commit A

Date: 2026-09-03
Status: **COMMIT_A_REMOTE_VERIFIED__COMMIT_B_PENDING**

## Canonical R4.2 identity
- Server-native source: `E:\new pc\AI_Pushes_Sandbox\projects\rahl-engineering-canonical-sop-r4-20260902\RAHL_ENGINEERING_CANONICAL_SOP_R4_2_2026-09-03.zip`
- Canonical SHA-256: `eb167543e9ceb2ae01449f421d2916e61b7dd924270ea2e83e3364c9d808ce9a`
- Bytes: `625556`
- Project-local exact ZIP: `doctrine/rahl_r4_2/RAHL_ENGINEERING_CANONICAL_SOP_R4_2_2026-09-03.zip`
- Source/destination identity: PASS
- Readable materialization identity: PASS 38/38
- Package-native verifier: PASS
- Hostile suite: 26/26 expected rejections; zero unexpected passes

## Semantic admission
- Changed readable R4.2 adoption/state/continuity candidate surfaces: PASS final-byte LHRSG
- Prepublication LHRSG receipt: `state/qualification/R4_2_CFE_ADOPTION_PREPUBLICATION_20260903.json`
- R4.2 canonical readable package semantic evidence reused only under exact-hash + unchanged process-authority scope.

## Commit A
- Commit: `aaffb64c13b7ea9c988b776035c3e4e779ed842f`
- Parent: `6b2dc681ded9151451107b9ec7396099757765dd`
- Message: `Adopt Rahl Engineering SOP R4.2 in CFE`
- Promoted paths: 70
- Actual changed paths: 70
- Zero extra paths: PASS
- Promoted Git-object blob verification: 70/70 PASS
- Local main after A: `aaffb64c13b7ea9c988b776035c3e4e779ed842f`
- Independently queried remote main after A: `aaffb64c13b7ea9c988b776035c3e4e779ed842f`
- Local/remote equality: PASS
- Canonical outer R4.2 ZIP Git-object SHA-256: `eb167543e9ceb2ae01449f421d2916e61b7dd924270ea2e83e3364c9d808ce9a`
- Canonical outer ZIP Git-object identity: PASS
- Private/heavy boundary: PASS by explicit allowlist + precommit scan

## Explicit exclusions upheld
No private learner JSONL, private V2R7 prompt/result JSONL, gated benchmark text, credentials/secrets, models/weights, adapters/checkpoints, transient scanner outputs, `.pcmmad_sync_runs`, unselected execution logs, or nested ancestry ZIP archives were included in Commit A.

## Known scar
The first project-local verifier invocation allowed receiver `.pcmmad_sync_runs` debris into the exact canonical package root. Recovery removed only receiver-created debris, restored 38/38 identity, rerouted execution outside the canonical root, and then achieved verifier PASS. General lesson: a canonical package root should not double as transient receiver/execution workspace unless non-mutation is proven.

## Scientific boundary
R4.2 adoption changes process/cold-start authority only. CFE science is unchanged. Training-body semantic coverage remains 0/1840 and training authorization remains false.

## Closure state
Commit A is remotely verified. The adoption transaction is not fully closed until Commit B publishes this receipt and the minimal continuity updates, and independent readback verifies `Commit B parent == Commit A` and `local main == remote main == Commit B`.
