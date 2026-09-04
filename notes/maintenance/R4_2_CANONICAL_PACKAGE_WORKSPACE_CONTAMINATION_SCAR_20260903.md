# Engineering Scar — Canonical Package Root / Receiver Workspace Contamination

Date: 2026-09-03
Status: ACTIVE SCAR / EXECUTION-ENVIRONMENT LESSON

## Observed event
During CFE project-local verification of the exact R4.2 materialization, the first verifier launch used the canonical extracted package directory as the receiver execution working directory. The receiver created `.pcmmad_sync_runs` files inside that canonical tree. The package verifier correctly rejected the resulting extra members.

## Recovery
1. Detect the unexpected noncanonical files.
2. Remove only receiver-created debris.
3. Re-establish exact 38/38 extracted member identity against the canonical ZIP.
4. Reroute execution so receiver/transient logs are outside the canonical package root.
5. Re-run the package-native verifier: PASS.
6. Re-run hostile tests: 26/26 expected rejections; zero unexpected passes.

## Generalizable lesson
`CANONICAL PACKAGE ROOT SHOULD NOT DOUBLE AS TRANSIENT EXECUTION / RECEIVER WORKSPACE` when the execution plane can materialize logs or state in its working directory.

This is a scar-informed default, not a universal prohibition. A future execution path may use a canonical root only if it is proven non-mutating or otherwise preserves exact package identity.

## Scientific effect
NONE. This was execution-plane contamination, not a CFE scientific result and not a defect in the canonical R4.2 package.
