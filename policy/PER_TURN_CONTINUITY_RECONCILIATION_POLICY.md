# CFE Per-Turn Continuity Reconciliation Policy

Status: **ACTIVE OPERATOR-DIRECTED CONTROL POLICY**
Effective: 2026-08-31

Operator directive:

> Ensure that every decision, every piece of research, every Commander's Intent, and all continuity documents are kept fresh per turn.

## Meaning

Every substantive CFE turn SHALL perform a bounded reconciliation pass before the turn is considered complete.

Freshness does **not** mean rewriting sealed history.

The project preserves two different duties:

1. **historical immutability / append-only lineage**
2. **current-state freshness**

Both must hold at the same time.

## Immutable or append-only surfaces

The following SHALL NOT be silently rewritten merely to look current:

- original Commander's Intent source artifacts;
- sealed preregistrations;
- sealed input locks;
- raw experiment results;
- historical FAIL/PASS records;
- completed campaign receipts;
- historical hostile interpretations;
- published heavy-artifact identities.

Changed interpretation SHALL be represented by a new closeout, supersession, active binding, or turn receipt.

## Per-turn active reconciliation set

Every substantive turn SHALL reconcile, and update when needed:

1. `state/live_shadow.md`
2. `state/design_thread_stream.md`
3. `state/current.md`
4. `state/next_steps.md`
5. active doctrine snapshot / doctrine delta
6. active Revisit Ledger
7. active Trace Matrix
8. active Commander's Intent binding/readback
9. research/publication manifest/frontier
10. current Git/publication head when publication is available
11. active campaign/job identity and status when execution is live
12. any newly created decision, research artifact, failure, repair, promotion, or demotion

## Commander's Intent freshness

The verbatim source Commander's Intent remains immutable.

Each substantive turn SHALL verify its source identity and reconcile the current scientific frontier against it.

If the active program binding has become stale, create a new dated binding rather than rewriting the verbatim source.

The turn receipt SHALL record:

- source Commander's Intent path and SHA-256;
- current active binding path and SHA-256;
- whether the current branch is aligned, in tension, or requires operator review;
- the reason.

## Research freshness

`every piece of research kept fresh` means:

- every new material artifact is entered into the publication/trace frontier;
- current claims point to the newest valid interpretation without erasing older evidence;
- superseded interpretations remain recoverable;
- unresolved research seams remain visible in the Revisit Ledger;
- active research status is not allowed to lag behind completed execution.

It does **not** mean editing old experiment outputs to contain the latest interpretation.

## Decision freshness

Every material decision SHALL have a durable record containing at minimum:

- decision statement;
- evidence basis;
- status: provisional / frozen / promoted / demoted / superseded;
- current consequence;
- demotion or replay trigger when known.

A decision that exists only in chat is not considered safely persisted.

## Turn reconciliation receipt

Every substantive turn SHOULD create or refresh a compact machine-readable receipt under:

`state/trace_matrix/turn_reconciliation/`

The receipt SHALL bind:

- timestamp;
- active mode and role;
- current experiment frontier;
- current Commander source/binding hashes;
- continuity-surface hashes after reconciliation;
- new material research artifacts created in the turn;
- new decisions;
- active blockers;
- publication/Git head if verified;
- next exact action.

## No-stale completion gate

Before ending a substantive turn, ask:

1. Does Live Shadow describe the actual current experiment?
2. Does Current State describe what is verified now rather than what used to be true?
3. Does Next Steps begin at the real frontier?
4. Are open mechanism seams in the Revisit Ledger?
5. Are load-bearing claims traceable in the Trace Matrix?
6. Is Commander's Intent still bound to the current branch?
7. Are new research artifacts represented in the publication frontier?
8. Is any live process/job identity recorded accurately?

If any answer is no, the turn is continuity-incomplete.

## Failure handling

If the local control plane is unavailable, record the intended reconciliation as pending and do not claim it completed.

On recovery, continuity reconciliation is the first mutation before widening scientific work.

## Laws

- `FRESH ACTIVE STATE != REWRITTEN HISTORY`
- `CHAT DECISION != PERSISTED DECISION`
- `NEW INTERPRETATION != MUTATED OLD EVIDENCE`
- `COMMANDERS INTENT FRESHNESS = SOURCE IDENTITY + CURRENT BINDING + CURRENT ALIGNMENT`
- `TURN COMPLETE => CONTINUITY RECONCILED OR EXPLICITLY BLOCKED`
## First-class cartography reconciliation

By explicit operator directive, CFE negative-space cartography is now a first-class governance surface with SOP-peer operational priority.

Every substantive turn that changes scientific state SHALL additionally reconcile:

13. active negative-space intervention lattice;
14. occupied-cell evidence bindings;
15. boundary/exclusion state;
16. ranked one-move/next-hole frontier;
17. experiment-to-cell binding for any active or proposed experiment.

Before freezing a new experiment, the turn reconciliation receipt SHALL identify the map cell/edge being probed and why that move is information-maximizing relative to the current shape.

A turn that advances scientific state while leaving cartography stale is continuity-incomplete.

`SCIENTIFIC FRONTIER CHANGE => CARTOGRAPHY RECONCILIATION REQUIRED`

