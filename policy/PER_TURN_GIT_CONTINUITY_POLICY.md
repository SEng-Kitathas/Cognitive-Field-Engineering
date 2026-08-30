# Per-Turn Git Continuity Policy

Status: ACTIVE PROJECT POLICY

## Rule
After every **material** conversational turn:
1. re-read/reconcile `continuity/live_shadow.md` and current machine state;
2. update load-bearing state/next-step/doctrine/revisit/trace surfaces as required;
3. append the exchange to the Design Thread Stream;
4. update `transcript/THIS_CONVERSATION.md` when the exchange changes project state or scientific interpretation;
5. run secret/size/policy checks;
6. `git add` only intended repository-surface changes;
7. commit with a turn-scoped message;
8. push to the configured GitHub remote in the same turn when authenticated network access exists;
9. read back the pushed commit SHA/remote head before claiming publication.

## No fake success
- local commit != remote push;
- push attempt != push success;
- remote acceptance != release-asset upload;
- GitHub UI visibility is not assumed without remote readback.

## Material turn definition
A turn is material if it changes any of:
- current objective/resume point;
- scientific claim posture;
- experiment state;
- code/data/artifact state;
- doctrine/policy;
- blockers/failure interpretation;
- next actions.

Chitchat with no state change may produce `No load-bearing state change this turn` in Live Shadow and need not create content churn, but the DTS may still be appended according to continuity doctrine.

## Heavy assets
Per-turn policy never means recommitting giant archives. Release assets are immutable/versioned; Git commits update their manifests/pointers only unless a new asset version is intentionally published.
