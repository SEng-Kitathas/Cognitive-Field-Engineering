# V1.4 Input-Lock Mutation Incident

Date: 2026-08-31 10:54 Eastern Daylight Time
Status: ATTEMPT_A_INVALIDATED__RECOVERY_IDENTITY_REQUIRED

## What happened
V1.4 Attempt A locked against the then-current sealed v1.3 final disposition at:
- bytes: `2347`
- SHA-256: `526ae885dc21c53e28a4d5f7773d2756dd27815dd3ed3d8c6646675612f9825f`

After V1.4 qualification/launch, a continuity closeout pass rewrote that lock-bound v1.3 disposition artifact. Current identity became:
- bytes: `1488`
- SHA-256: `48f29fa9c5176c9e7e08c5ecf4ec55758f75902adc26059d592ff7cc93817773`

Training for seed2026083111 completed and produced H1/H2/H4 checkpoints before the evaluator re-verified the lock. H1 evaluation failed closed with `INPUT_LOCK_VERIFY_FAIL` on the v1.3 disposition byte count.

## Classification
This is a **procedural provenance mutation defect**, not a model/evaluator scientific result.

The failed attempt SHALL NOT contribute scientific outcomes. Its checkpoints/logs remain preserved as failed lineage.

## Recovery rule applied
The original lock explicitly states `LOCK MUTATION REQUIRES NEW IDENTITY`. The original 2347-byte artifact could not be recovered from Git objects, project backups, or release archives. Therefore:

1. Do not alter the old lock.
2. Do not reuse Attempt A checkpoints as scientific evidence.
3. Create a new V14R identity with the same scientific design, same seeds, same candidate/evaluator/runtime profile, but a new provenance anchor to the current v1.3 disposition.
4. Re-run runtime identity and repeatability qualification.
5. Retrain all six trajectories from scratch under V14R.

This recovery changes **identity/provenance only**, not the scientific variable.
